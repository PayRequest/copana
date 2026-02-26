#!/usr/bin/env python3
"""
Morning Briefing — Start your day with context.

Sends a summary via your notification channel:
- Today's tasks and reminders
- Open loops that need attention
- Overnight research (if any)
- AI-generated nudge from last night's reflection

Runs daily (e.g., 7:00 AM via cron).
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))
from copana_utils import (
    COPANA_DIR, send_notification, get_open_loops,
    get_pending_tasks, load_data, log,
)


def get_morning_nudge():
    """Get the AI-generated nudge from daily reflection."""
    nudge_file = COPANA_DIR / 'data' / 'morning_nudge.txt'
    if nudge_file.exists():
        nudge = nudge_file.read_text().strip()
        if nudge:
            return nudge
    return None


def get_research_brief():
    """Get overnight research summaries."""
    research_dir = COPANA_DIR / 'memory' / 'research'
    if not research_dir.exists():
        return None

    yesterday = (datetime.now() - timedelta(days=1)).date()

    topics = []
    for f in research_dir.glob('*_*.md'):
        try:
            date_str = f.stem.split('_')[-1]
            file_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if file_date == yesterday:
                topic = ' '.join(f.stem.split('_')[:-1]).replace('-', ' ').title()
                topics.append(topic)
        except (ValueError, IndexError):
            continue

    if topics:
        return f"OVERNIGHT RESEARCH:\n  " + ', '.join(topics) + "\n  Check memory/research/ for details"
    return None


def get_tasks_due_today():
    """Get tasks with due dates today or overdue."""
    tasks = get_pending_tasks()
    today = datetime.now().strftime('%Y-%m-%d')

    due_today = []
    overdue = []
    for task in tasks:
        text = task['text']
        if f'due:{today}' in text:
            due_today.append(text)
        elif 'due:' in text:
            # Check if overdue
            import re
            due_match = re.search(r'due:(\d{4}-\d{2}-\d{2})', text)
            if due_match and due_match.group(1) < today:
                overdue.append(text)

    return due_today, overdue


def build_message():
    """Build the morning briefing message."""
    now = datetime.now()

    msg = f"MORNING BRIEFING\n"
    msg += f"{now.strftime('%A %d %B').title()}\n\n"

    # AI nudge from daily reflection
    nudge = get_morning_nudge()
    if nudge:
        msg += f">> {nudge}\n\n"

    # Overnight research
    research = get_research_brief()
    if research:
        msg += f"{research}\n\n"

    # Today's tasks
    due_today, overdue = get_tasks_due_today()
    msg += "TODAY:\n"
    if overdue:
        for t in overdue[:5]:
            msg += f"  ! OVERDUE: {t[:50]}\n"
    if due_today:
        for t in due_today[:5]:
            msg += f"  - {t[:50]}\n"
    if not due_today and not overdue:
        msg += "  Nothing due today\n"

    # Open loops
    loops = get_open_loops()
    active_loops = [l for l in loops if l['what'] != '—']
    if active_loops:
        msg += f"\nOPEN LOOPS: {len(active_loops)} pending\n"
        for loop in active_loops[:3]:
            msg += f"  - {loop['what']}\n"

    # Pending task count
    all_tasks = get_pending_tasks()
    if all_tasks:
        msg += f"\nTASKS: {len(all_tasks)} pending\n"

    return msg


def get_morning_buttons():
    """Get inline keyboard buttons for Telegram."""
    return {
        "inline_keyboard": [
            [
                {"text": "Top priority", "callback_data": "morning_priority"},
                {"text": "Open loops", "callback_data": "morning_loops"},
            ]
        ]
    }


def main():
    log("Building morning briefing...", "morning_briefing.log")
    message = build_message()

    print(message)
    print("---")

    buttons = get_morning_buttons()
    if send_notification(message, reply_markup=buttons):
        log("Morning briefing sent!", "morning_briefing.log")
    else:
        log("Failed to send (or no notification channel configured)", "morning_briefing.log")


if __name__ == "__main__":
    main()
