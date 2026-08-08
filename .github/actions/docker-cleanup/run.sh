#!/usr/bin/env bash
set -euo pipefail

# Docker cleanup
# Removes stale containers, dangling images, and unused volumes

echo "::group::Docker cleanup"

# Stop and remove all stopped containers
echo "Removing stopped containers..."
docker ps -a --filter "status=exited" --format "{{.ID}}" | xargs -r docker rm 2>/dev/null || true

# Remove dangling images
echo "Removing dangling images..."
docker images --filter "dangling=true" --format "{{.ID}}" | xargs -r docker rmi 2>/dev/null || true

# Remove unused volumes
echo "Removing unused volumes..."
docker volume ls --filter "dangling=true" --format "{{.Name}}" | xargs -r docker volume rm 2>/dev/null || true

# Keep only the N most recent images
if [ "${KEEP_IMAGES:-5}" != "all" ]; then
  image_count=$(docker images --format "{{.ID}}" | wc -l)
  keep="${KEEP_IMAGES:-5}"
  if [ "$image_count" -gt "$keep" ]; then
    remove_count=$((image_count - keep))
    echo "Keeping $keep most recent images, removing $remove_count..."
    docker images --format "{{.ID}}" | tail -n "$remove_count" | xargs -r docker rmi 2>/dev/null || true
  fi
fi

# Print remaining state
echo "Remaining containers: $(docker ps -a --format '{{.ID}}' | wc -l)"
echo "Remaining images: $(docker images --format '{{.ID}}' | wc -l)"
echo "Remaining volumes: $(docker volume ls --format '{{.Name}}' | wc -l)"

echo "::endgroup::"
