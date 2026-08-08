#!/usr/bin/env bash
set -euo pipefail

# Shellcheck linter
# Checks bash scripts for common errors and style issues

echo "::group::Shellcheck"

check_paths="${CHECK_PATHS:-*.sh}"
severity="${SEVERITY:-warning}"

# Check if shellcheck is installed
if ! command -v shellcheck >/dev/null 2>&1; then
  echo "Installing shellcheck..."
  sudo dnf install -y -q shellcheck >/dev/null 2>&1 || true
fi

# Set severity filter
severity_flag=""
case "$severity" in
  info)    severity_flag="--severity=info" ;;
  warning) severity_flag="--severity=warning" ;;
  error)   severity_flag="--severity=error" ;;
  *)       severity_flag="--severity=warning" ;;
esac

# Find and check all matching files
found_files=0
error_count=0

for path_pattern in $check_paths; do
  while IFS= read -r -d '' file; do
    found_files=$((found_files + 1))
    echo "Checking: $file"

    if ! shellcheck_output=$(shellcheck "$severity_flag" "$file" 2>&1); then
      error_count=$((error_count + 1))
      echo "::error file=$file::$shellcheck_output"
    fi
  done < <(find . -path "$path_pattern" -type f -print0 2>/dev/null)
done

if [ "$found_files" -eq 0 ]; then
  echo "No files matched patterns: $check_paths"
fi

echo "Files checked: $found_files"
echo "Errors found: $error_count"

if [ "$error_count" -gt 0 ]; then
  exit 1
fi

echo "Shellcheck passed"
echo "::endgroup::"
