#!/bin/bash
# Worktree management script for Team Chaotix
# Usage: ./manage-worktrees.sh [create|list|remove] [name]

set -euo pipefail

REPO_DIR="${OPENCODE_REPO_DIR:-$(git rev-parse --show-toplevel)}"
WORKTREE_DIR="${REPO_DIR}/../worktrees"

usage() {
    cat <<EOF
Usage: $(basename "$0") {create|list|remove} [name]

Commands:
  create <name>  Create a new worktree for <name>
  list           List all active worktrees
  remove <name>  Remove a worktree for <name>

Examples:
  $(basename "$0") create cinnamon
  $(basename "$0") list
  $(basename "$0") remove cinnamon
EOF
    exit 1
}

create_worktree() {
    local name="$1"
    local worktree_path="${WORKTREE_DIR}/${name}"
    
    if [[ -e "$worktree_path" ]]; then
        echo "Error: Worktree already exists: $worktree_path"
        exit 1
    fi
    
    mkdir -p "$WORKTREE_DIR"
    git worktree add "$worktree_path" -b "worktree/${name}"
    
    # Copy .opencode configuration
    if [[ -d "${REPO_DIR}/.opencode" ]]; then
        cp -r "${REPO_DIR}/.opencode" "$worktree_path/"
    fi
    
    # Copy AGENTS.md
    if [[ -f "${REPO_DIR}/AGENTS.md" ]]; then
        cp "${REPO_DIR}/AGENTS.md" "$worktree_path/"
    fi
    
    echo "Created worktree: $worktree_path"
    echo "To use: cd $worktree_path && opencode"
}

list_worktrees() {
    git worktree list
}

remove_worktree() {
    local name="$1"
    local worktree_path="${WORKTREE_DIR}/${name}"
    
    if [[ ! -e "$worktree_path" ]]; then
        echo "Error: Worktree not found: $worktree_path"
        exit 1
    fi
    
    git worktree remove "$worktree_path"
    git branch -D "worktree/${name}" 2>/dev/null || true
    rm -rf "$worktree_path"
    echo "Removed worktree: $worktree_path"
}

case "${1:-}" in
    create)
        [[ -z "${2:-}" ]] && usage
        create_worktree "$2"
        ;;
    list)
        list_worktrees
        ;;
    remove)
        [[ -z "${2:-}" ]] && usage
        remove_worktree "$2"
        ;;
    *)
        usage
        ;;
esac
