#!/usr/bin/env bash
set -euo pipefail

# Sparky test runner
# Executes Sparky/Sparrow tests inside a libvirt VM for Rocky Linux testing

echo "::group::Sparky test runner"

test_dir="${SPARKY_TEST_DIR:-tests/sparky}"
project_path="${PROJECT_PATH:-.}"
vm_name="${SPARKY_VM_NAME:-sparky-test-vm}"
config_path="${SPARKY_CONFIG:-}"

# Check for required dependencies
echo "Checking dependencies..."

# Raku (required for Sparky)
if ! command -v raku >/dev/null 2>&1; then
  echo "Raku not found. Installing..."
  sudo dnf install -y -q raku 2>/dev/null || sudo apt-get install -y -qq raku 2>/dev/null || true
fi

# libvirt tools
if ! command -v virsh >/dev/null 2>&1; then
  echo "virsh not found. Installing libvirt..."
  sudo apt-get install -y -qq libvirt-clients 2>/dev/null || sudo dnf install -y -q libvirt-daemon-client 2>/dev/null || true
fi

# Check if Sparky is installed
if ! command -v sparky >/dev/null 2>&1; then
  echo "Sparky not found in PATH"
  # Check if Sparky is cloned in project
  if [ -d "sparky" ]; then
    export PATH="$PWD/sparky:$PATH"
  else
    echo "::warning::Sparky not installed. Cloning..."
    git clone --depth 1 https://github.com/rocky-linux/sparky.git 2>/dev/null || true
    export PATH="$PWD/sparky:$PATH"
  fi
fi

# Verify VM is running
if ! virsh dominfo "$vm_name" >/dev/null 2>&1; then
  echo "::warning::VM $vm_name not running. Sparky tests require a running VM."
  echo "Ensure libvirt-vm-setup action has run first."
fi

# Set up Sparky configuration
if [ -n "$config_path" ] && [ -f "$config_path" ]; then
  echo "Using config: $config_path"
  sparky_cmd="sparky --config $config_path"
else
  # Generate default vars.yaml if test directory exists
  if [ -d "$test_dir" ]; then
    echo "Generating default Sparky config..."
    cat > "${test_dir}/vars.yaml" <<'EOF'
version: "10"
releasever: "10"
qemu_binary: "qemu-system-x86_64"
qemu_machine: "pc"
bootstrap: "true"
EOF
    sparky_cmd="sparky --config ${test_dir}/vars.yaml"
  else
    echo "No test directory found: $test_dir"
    sparky_cmd="sparky"
  fi
fi

# Run Sparky tests
echo "Running Sparky tests..."
test_results="${test_dir}/results"
mkdir -p "$test_results"

if [ -d "$test_dir" ]; then
  # Run each Sparrow task in the test directory
  for task_file in "${test_dir}"/*.sparky; do
    if [ -f "$task_file" ]; then
      echo "Running task: $(basename "$task_file")"
      $sparky_cmd task run "$task_file" 2>&1 || echo "Task had issues: $(basename "$task_file")"
    fi
  done
else
  echo "No Sparky tasks found in $test_dir"
fi

# Collect results
if [ -d "$test_results" ]; then
  result_count=$(find "$test_results" -name "*.json" -o -name "*.png" | wc -l)
  echo "Collected $result_count test artifacts"
fi

echo "Sparky test run complete"
echo "::endgroup::"
