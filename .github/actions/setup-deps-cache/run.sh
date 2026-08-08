#!/usr/bin/env bash
set -euo pipefail

# Setup dependency caches
# Restores cached apt, pip, npm, and cargo packages for faster startup

echo "::group::Restoring dependency caches"

# APT cache
apt_cache_dir="/var/cache/apt/archives"
if [ -d "$apt_cache_dir" ]; then
  echo "APT cache directory exists"
fi

# Pip cache
pip_cache="${HOME}/.cache/pip"
if [ -d "$pip_cache" ]; then
  cache_size=$(du -sh "$pip_cache" 2>/dev/null | cut -f1)
  echo "Pip cache: $cache_size"
else
  mkdir -p "$pip_cache"
  echo "Created pip cache directory"
fi

# NPM cache
npm_cache="${HOME}/.npm"
if [ -d "$npm_cache" ]; then
  cache_size=$(du -sh "$npm_cache" 2>/dev/null | cut -f1)
  echo "NPM cache: $cache_size"
else
  mkdir -p "$npm_cache"
  echo "Created npm cache directory"
fi

# Cargo cache
cargo_cache="${HOME}/.cargo"
if [ -d "$cargo_cache" ]; then
  cache_size=$(du -sh "$cargo_cache" 2>/dev/null | cut -f1)
  echo "Cargo cache: $cache_size"
fi

# Go module cache
go_cache="${HOME}/go/pkg/mod"
if [ -d "$go_cache" ]; then
  cache_size=$(du -sh "$go_cache" 2>/dev/null | cut -f1)
  echo "Go module cache: $cache_size"
fi

echo "::endgroup::"
