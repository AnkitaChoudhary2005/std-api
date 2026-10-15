#!/bin/bash
set -e

cd /root/student_api

# Only push from the main branch
BRANCH=$(git branch --show-current)

if [ "$BRANCH" != "main" ]; then
    echo "Auto-push stopped: current branch is not main."
    exit 1
fi

# Stage new, modified, and deleted files
git add -A

# Stop if there are no staged changes
if git diff --cached --quiet; then
    echo "No changes to commit."
    exit 0
fi

# Commit and push changes
git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
