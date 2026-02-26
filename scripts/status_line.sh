#!/bin/bash
# Copana status line — shows context at a glance in Claude Code
# Used by .claude/settings.json statusLine config

REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Count open tasks
TASKS=0
if [ -f "$REPO_DIR/tasks.md" ]; then
    TASKS=$(grep -c '^\- \[ \]' "$REPO_DIR/tasks.md" 2>/dev/null || echo 0)
fi

# Count open loops
LOOPS=0
if [ -f "$REPO_DIR/memory.md" ]; then
    LOOPS=$(grep -c '^\-' "$REPO_DIR/memory.md" 2>/dev/null | head -1 || echo 0)
fi

# Last session time
LAST_SESSION=""
if [ -f "$REPO_DIR/memory.md" ]; then
    LAST_SESSION=$(grep -m1 '^\*\*Session' "$REPO_DIR/memory.md" 2>/dev/null | head -1)
fi

# Build status parts
PARTS=""

if [ "$TASKS" -gt 0 ]; then
    PARTS="${PARTS}Tasks: ${TASKS}"
fi

if [ "$LOOPS" -gt 0 ]; then
    [ -n "$PARTS" ] && PARTS="${PARTS} | "
    PARTS="${PARTS}Loops: ${LOOPS}"
fi

if [ -n "$LAST_SESSION" ]; then
    [ -n "$PARTS" ] && PARTS="${PARTS} | "
    PARTS="${PARTS}${LAST_SESSION}"
fi

if [ -z "$PARTS" ]; then
    PARTS="Ready"
fi

echo "$PARTS"
