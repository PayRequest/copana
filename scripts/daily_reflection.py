#!/usr/bin/env python3
"""
Daily Reflection — Your AI thinks while you sleep.

Reviews all memory files to:
1. Find stale tasks and forgotten follow-ups
2. Identify patterns
3. Generate a morning nudge for tomorrow
4. Write reflection to memory/reflections/

Runs at night (e.g., 23:00) via cron.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from copana_utils import (
    COPANA_DIR, call_ai, send_notification, load_context, log,
)


def analyze_stale_items(context: dict) -> str:
    """Find stale tasks and open loops."""
    prompt = f"""Review these files and identify:

1. **Stale tasks** — items pending too long
2. **Forgotten follow-ups** — mentioned but not acted on
3. **Outdated information** — facts that might have changed
4. **Patterns** — recurring themes or concerns

memory.md:
{context.get('memory.md', 'Not found')[:3000]}

tasks.md:
{context.get('tasks.md', 'Not found')[:2000]}

insights.md:
{context.get('insights.md', 'Not found')[:2000]}

Output a brief summary (max 300 words) of what needs attention."""

    return call_ai(
        prompt,
        system="You review personal productivity files to find patterns and stale items. Be concise and actionable.",
        max_tokens=1000,
    )


def generate_morning_nudge(analysis: str) -> str:
    """Create a brief nudge for tomorrow morning."""
    return call_ai(
        f"""Based on this analysis, write a brief (2-3 lines) nudge for tomorrow morning.
Be direct, specific, and actionable.

Analysis:
{analysis}""",
        system="You write brief morning nudges. Be direct and actionable. No fluff.",
        max_tokens=200,
    )


def write_reflection(analysis: str, nudge: str):
    """Write daily reflection to memory/reflections/."""
    today = datetime.now().strftime('%Y-%m-%d')
    reflection_dir = COPANA_DIR / 'memory' / 'reflections'
    reflection_dir.mkdir(parents=True, exist_ok=True)

    content = f"""# Daily Reflection — {today}

## Analysis
{analysis}

## Tomorrow's Nudge
{nudge}

---
*Generated at {datetime.now().strftime('%H:%M')}*
"""

    (reflection_dir / f'{today}.md').write_text(content)
    log(f"Reflection written for {today}", "daily_reflection.log")


def main():
    log("Starting daily reflection...", "daily_reflection.log")

    context = load_context(['memory.md', 'tasks.md', 'insights.md', 'user.md'])

    if not context:
        log("No context files found, skipping", "daily_reflection.log")
        return

    # Analyze
    log("Analyzing...", "daily_reflection.log")
    analysis = analyze_stale_items(context)

    if not analysis:
        log("AI not configured, skipping analysis", "daily_reflection.log")
        return

    # Generate nudge
    log("Generating morning nudge...", "daily_reflection.log")
    nudge = generate_morning_nudge(analysis)

    # Save nudge for morning briefing
    nudge_file = COPANA_DIR / 'data' / 'morning_nudge.txt'
    nudge_file.parent.mkdir(exist_ok=True)
    nudge_file.write_text(nudge)

    # Write reflection
    write_reflection(analysis, nudge)

    # Notify
    summary = f"Daily Reflection Complete\n\n{nudge}\n\nFull reflection saved to memory/reflections/"
    send_notification(summary)

    log("Done!", "daily_reflection.log")


if __name__ == '__main__':
    main()
