#!/usr/bin/env bash
set -euo pipefail

# Docker test runner
# Runs tests inside a Docker container for consistent environments

echo "::group::Docker test runner"

image="${DOCKER_IMAGE:-ubuntu:latest}"
command="${TEST_COMMAND:-bash -c 'echo Running tests... && exit 0'}"
project_path="${PROJECT_PATH:-.}"
extra_flags="${EXTRA_FLAGS:-}"

# Pull the image if not present locally
echo "Pulling image: $image"
docker pull "$image" 2>/dev/null || echo "Using cached image: $image"

# Build docker run command with project mount
docker_cmd="docker run --rm"
docker_cmd="$docker_cmd -v \"$(pwd)/$project_path:/project\""
docker_cmd="$docker_cmd -w /project"
docker_cmd="$docker_cmd $extra_flags"
docker_cmd="$docker_cmd $image"
docker_cmd="$docker_cmd $command"

echo "Running: $docker_cmd"
eval "$docker_cmd"
exit_code=$?

if [ $exit_code -ne 0 ]; then
  echo "::error::Docker test runner exited with code $exit_code"
  exit $exit_code
fi

echo "Docker tests passed"
echo "::endgroup::"
