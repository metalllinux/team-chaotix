#!/usr/bin/env bash
set -euo pipefail

# Checkout with git bundle caching
# Checks for cached git bundle first, falls back to standard checkout

cache_dir="${HOME}/.cache/team-chaotix/git-bundle"
bundle_file="${cache_dir}/repo-bundle.latest"
cache_ts_file="${cache_dir}/bundle-timestamp"
bundle_age_hours=2

mkdir -p "$cache_dir"

# Check if we have a recent bundle cache
if [ -f "$bundle_file" ] && [ -f "$cache_ts_file" ]; then
  cache_ts=$(cat "$cache_ts_file")
  current_ts=$(date +%s)
  age_seconds=$((current_ts - cache_ts))
  age_hours=$((age_seconds / 3600))

  if [ "$age_hours" -lt "$bundle_age_hours" ]; then
    echo "::group::Restoring from git bundle cache (${age_hours}h old)"
    # Use cached bundle for faster checkout
    git clone --bundle-uri "$bundle_file" ./. 2>/dev/null || true
    echo "::endgroup::"
  else
    echo "Bundle cache is ${age_hours}h old, refreshing..."
  fi
fi

# Standard checkout (always runs, bundle is just an optimization)
echo "::group::Git checkout"
git config --global --add safe.directory "$GITHUB_WORKSPACE"
echo "::endgroup::"

# Update bundle cache for next run
echo "::group::Updating git bundle cache"
if git bundle create "$bundle_file" --all 2>/dev/null; then
  date +%s > "$cache_ts_file"
  echo "Bundle cache updated"
fi
echo "::endgroup::"
