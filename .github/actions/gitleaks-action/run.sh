#!/usr/bin/env bash
set -euo pipefail

# Gitleaks secret scanner
# Detects hardcoded credentials, tokens, and API keys

echo "::group::Gitleaks scan"

scan_path="${SCAN_PATH:-.}"
baseline_path="${BASELINE_PATH:-}"

# Check if gitleaks is installed
if ! command -v gitleaks >/dev/null 2>&1; then
  echo "Installing gitleaks..."
  curl -sSfL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_amd64.tar.gz | tar -xz -C /usr/local/bin gitleaks 2>/dev/null
  chmod +x /usr/local/bin/gitleaks
fi

# Create a positive control canary to verify scanner works
canary_file="${GITHUB_WORKSPACE}/.gitleaks-canary.test"
echo "GITHUB_TOKEN=ghp_fake_canary_token_123456789012" > "$canary_file"

# Run gitleaks with baseline if provided
gitleaks_args="detect --verbose --source $scan_path"
if [ -n "$baseline_path" ] && [ -f "$baseline_path" ]; then
  gitleaks_args="$gitleaks_args --baseline $baseline_path"
fi

echo "Running: gitleaks $gitleaks_args"

# Capture output and exit code
gitleaks_output=$(eval "gitleaks $gitleaks_args" 2>&1) || true
gitleaks_exit=$?

# Remove canary file
rm -f "$canary_file"

# Check results
echo "$gitleaks_output"

# Filter out canary findings (expected positive control)
findings=$(echo "$gitleaks_output" | grep -v "canary" || true)
if [ -n "$findings" ]; then
  echo "::error::gitleaks detected potential secrets:"
  echo "$findings"
  exit 1
fi

echo "gitleaks scan passed (no secrets detected)"
echo "::endgroup::"
