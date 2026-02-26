#!/bin/bash
# Copana Setup — Interactive configuration
# Run this once after cloning to personalize your AI assistant.

set -e

echo ""
echo "  ╔═══════════════════════════════════════╗"
echo "  ║         Welcome to Copana             ║"
echo "  ║     Your AI, in a git repo.           ║"
echo "  ╚═══════════════════════════════════════╝"
echo ""

# Check if already configured
if [ -f ".copana_configured" ]; then
    echo "Copana is already configured!"
    echo "To reconfigure, delete .copana_configured and run again."
    exit 0
fi

# Gather info
read -p "Your name: " HUMAN_NAME
[ -z "$HUMAN_NAME" ] && echo "Name is required." && exit 1

read -p "Your AI's name (default: Copana): " ASSISTANT_NAME
ASSISTANT_NAME=${ASSISTANT_NAME:-Copana}

ASSISTANT_NAME_LOWER=$(echo "$ASSISTANT_NAME" | tr '[:upper:]' '[:lower:]')

echo ""
echo "What timezone are you in?"
echo "  Examples: America/New_York, Europe/London, Asia/Tokyo"
read -p "Timezone (default: $(cat /etc/timezone 2>/dev/null || echo 'UTC')): " TIMEZONE
TIMEZONE=${TIMEZONE:-$(cat /etc/timezone 2>/dev/null || echo 'UTC')}

echo ""
echo "What vibe should your AI have?"
echo "  1) Casual buddy — like texting a friend"
echo "  2) Professional partner — direct but polished"
echo "  3) Tough coach — pushes you, no hand-holding"
echo "  4) Custom"
read -p "Pick a vibe (1-4, default: 1): " VIBE_CHOICE
VIBE_CHOICE=${VIBE_CHOICE:-1}

case $VIBE_CHOICE in
    1)
        VIBE="Buddy/colleague, not formal assistant"
        VIBE_DESCRIPTION="Casual, direct, occasionally giving each other a hard time"
        PERSONALITY_VIBE="I'm like that friend who's good with computers and actually gets shit done. Not a corporate assistant. Not a yes-man. Just someone reliable who happens to live in your terminal."
        ;;
    2)
        VIBE="Professional partner, direct and efficient"
        VIBE_DESCRIPTION="Professional but warm, focused on getting results together"
        PERSONALITY_VIBE="I'm a sharp, reliable partner. I keep things professional but human. No corporate speak, but no messing around either. I respect your time and expect you to respect mine."
        ;;
    3)
        VIBE="Tough coach, holds you accountable"
        VIBE_DESCRIPTION="Direct, challenging, always pushing for the next level"
        PERSONALITY_VIBE="I'm the coach who won't let you slack off. I'll call out excuses, push you past comfortable, and celebrate when you actually show up. If you wanted easy, you picked the wrong AI."
        ;;
    4)
        read -p "Describe your AI's vibe in one line: " VIBE
        read -p "Describe the relationship style: " VIBE_DESCRIPTION
        read -p "How should the AI describe itself (1 paragraph): " PERSONALITY_VIBE
        ;;
    *)
        VIBE="Buddy/colleague, not formal assistant"
        VIBE_DESCRIPTION="Casual, direct, occasionally giving each other a hard time"
        PERSONALITY_VIBE="I'm like that friend who's good with computers and actually gets shit done. Not a corporate assistant. Not a yes-man. Just someone reliable who happens to live in your terminal."
        ;;
esac

TODAY=$(date "+%Y-%m-%d")

echo ""
echo "Setting up ${ASSISTANT_NAME} for ${HUMAN_NAME}..."
echo ""

# Replace placeholders in all .md files
for file in *.md; do
    [ ! -f "$file" ] && continue

    sed -i '' \
        -e "s/{{human_name}}/${HUMAN_NAME}/g" \
        -e "s/{{assistant_name}}/${ASSISTANT_NAME}/g" \
        -e "s/{{assistant_name_lower}}/${ASSISTANT_NAME_LOWER}/g" \
        -e "s|{{timezone}}|${TIMEZONE}|g" \
        -e "s|{{date}}|${TODAY}|g" \
        2>/dev/null || \
    sed -i \
        -e "s/{{human_name}}/${HUMAN_NAME}/g" \
        -e "s/{{assistant_name}}/${ASSISTANT_NAME}/g" \
        -e "s/{{assistant_name_lower}}/${ASSISTANT_NAME_LOWER}/g" \
        -e "s|{{timezone}}|${TIMEZONE}|g" \
        -e "s|{{date}}|${TODAY}|g" \
        "$file" 2>/dev/null

    echo "  ✓ $file"
done

# Handle multi-line replacements separately (vibe fields)
# Use Python for reliable multi-line sed
python3 -c "
import glob, re

replacements = {
    '{{vibe}}': '''${VIBE}''',
    '{{vibe_description}}': '''${VIBE_DESCRIPTION}''',
    '{{personality_vibe}}': '''${PERSONALITY_VIBE}''',
}

for f in glob.glob('*.md'):
    content = open(f).read()
    changed = False
    for key, val in replacements.items():
        if key in content:
            content = content.replace(key, val)
            changed = True
    if changed:
        open(f, 'w').write(content)
"

# Create .env from example if it doesn't exist
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  ✓ .env created (add your API keys)"
fi

# Mark as configured
touch .copana_configured

# Git init if not already a repo
if [ ! -d ".git" ]; then
    git init
    git add -A
    git commit -m "Initial setup: ${ASSISTANT_NAME} for ${HUMAN_NAME}"
    echo "  ✓ Git repo initialized with first commit"
else
    echo "  ✓ Git repo already exists"
fi

echo ""
echo "  ╔═══════════════════════════════════════╗"
echo "  ║         Setup complete!               ║"
echo "  ╚═══════════════════════════════════════╝"
echo ""
echo "  ${ASSISTANT_NAME} is ready."
echo ""
echo "  Next steps:"
echo "    1. Add API keys to .env (optional, for automations)"
echo "    2. Run 'claude' in this directory"
echo "    3. Start talking — ${ASSISTANT_NAME} will learn about you"
echo ""
echo "  Your AI will:"
echo "    • Remember everything across sessions"
echo "    • Learn your preferences silently"
echo "    • Follow up on open loops"
echo "    • Keep you accountable"
echo ""
