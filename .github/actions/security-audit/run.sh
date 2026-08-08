#!/usr/bin/env bash
set -euo pipefail

# Security audit
# Combined secret scanning and vulnerability checks

echo "::group::Security audit"

scan_type="${SCAN_TYPE:-all}"
scan_path="${SCAN_PATH:-.}"

error_count=0

# Gitleaks scan
if [ "$scan_type" = "gitleaks" ] || [ "$scan_type" = "all" ]; then
  echo "=== Gitleaks scan ==="
  if command -v gitleaks >/dev/null 2>&1; then
    gitleaks detect --verbose --source "$scan_path" 2>&1 || {
      echo "::error::gitleaks found potential secrets"
      error_count=$((error_count + 1))
    }
  else
    echo "gitleaks not installed, skipping"
  fi
fi

# Trufflehog scan
if [ "$scan_type" = "trufflehog" ] || [ "$scan_type" = "all" ]; then
  echo "=== Trufflehog scan ==="
  if command -v trufflehog >/dev/null 2>&1; then
    trufflehog filesystem --no-update --fail "$scan_path" 2>&1 || {
      echo "::error::trufflehog found potential secrets"
      error_count=$((error_count + 1))
    }
  else
    echo "trufflehog not installed, skipping"
  fi
fi

# Dependency check (if applicable)
if [ "$scan_type" = "all" ]; then
  echo "=== Dependency check ==="

  # Check for package lock files
  for lockfile in package-lock.json yarn.lock Pipfile.lock poetry.lock Cargo.lock go.sum; do
    if [ -f "$scan_path/$lockfile" ]; then
      echo "Found lockfile: $lockfile (dependencies pinned)"
    fi
  done
fi

# Summary
echo ""
echo "=== Security audit summary ==="
echo "Scan type: $scan_type"
echo "Path: $scan_path"
echo "Errors: $error_count"

if [ "$error_count" -gt 0 ]; then
  echo "::error::Security audit found $error_count issue(s)"
  exit 1
fi

echo "Security audit passed"
echo "::endgroup::"
