#!/bin/bash
# Session end script — commit all memory changes
# Run this at the end of every session

cd "$(dirname "$0")/.." || exit 1

# Check if there are changes
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "No changes to commit."
    exit 0
fi

# Stage all .md files and data changes
git add *.md
git add memory/*.md 2>/dev/null
git add data/*.json 2>/dev/null

# Create commit with timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
git commit -m "memory sync: $TIMESTAMP"

# Push to remote if configured
if git remote get-url origin &>/dev/null; then
    git push
    echo "Memory synced and pushed at $TIMESTAMP"
else
    echo "Memory synced locally at $TIMESTAMP (no remote configured)"
fi
