#!/usr/bin/env python3
"""
Proactive Pings — Smart nudges that actually help.

Checks for:
- Stale tasks (open > 3 days)
- Forgotten open loops
- Upcoming birthdays (from contacts.md)
- Overdue items

Philosophy: Only nudge when it's actually helpful. Less noise = more trust.
Sends ONE nudge per run, prioritized by importance.

Runs 2-3x/day via cron (e.g., 10:00, 14:00, 18:00).
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict

sys.path.insert(0, str(Path(__file__).parent))
from copana_utils import (
    COPANA_DIR, send_notification, call_ai, get_open_loops,
    get_pending_tasks, load_data, save_data, log,
)

NUDGE_HISTORY_FILE = COPANA_DIR / 'logs' / 'nudge_history.json'


def was_recently_nudged(topic: str, hours: int = 6) -> bool:
    """Check if we already nudged about this topic recently."""
    if not NUDGE_HISTORY_FILE.exists():
        return False

    try:
        history = json.loads(NUDGE_HISTORY_FILE.read_text())
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        return any(
            e.get('topic') == topic and e.get('time', '') > cutoff
            for e in history
        )
    except (json.JSONDecodeError, Exception):
        return False


def record_nudge(topic: str, message: str):
    """Record that we sent a nudge about this topic."""
    history = []
    if NUDGE_HISTORY_FILE.exists():
        try:
            history = json.loads(NUDGE_HISTORY_FILE.read_text())
        except (json.JSONDecodeError, Exception):
            history = []

    history.append({
        'topic': topic,
        'message': message[:100],
        'time': datetime.now().isoformat(),
    })
    history = history[-50:]  # Keep last 50

    NUDGE_HISTORY_FILE.parent.mkdir(exist_ok=True)
    NUDGE_HISTORY_FILE.write_text(json.dumps(history, indent=2))


def get_upcoming_birthdays() -> List[Dict]:
    """Check contacts.md for birthdays in the next 3 days."""
    contacts_file = COPANA_DIR / 'contacts.md'
    if not contacts_file.exists():
        return []

    content = contacts_file.read_text()
    today = datetime.now()
    upcoming = []

    birthday_pattern = r'\*\*([^*]+)\*\*.*?Birthday[:\s]+(\d{4}-)?(\d{2}-\d{2})'
    for match in re.finditer(birthday_pattern, content, re.IGNORECASE | re.DOTALL):
        name = match.group(1).strip()
        month_day = match.group(3)
        try:
            birthday = datetime.strptime(f"{today.year}-{month_day}", "%Y-%m-%d")
            days_until = (birthday - today).days
            if 0 <= days_until <= 3:
                upcoming.append({'name': name, 'days': days_until, 'date': birthday.strftime('%B %d')})
        except ValueError:
            continue

    return upcoming


def get_overdue_tasks() -> list:
    """Get tasks that are overdue."""
    tasks = get_pending_tasks()
    today = datetime.now().strftime('%Y-%m-%d')
    overdue = []

    for task in tasks:
        due_match = re.search(r'due:(\d{4}-\d{2}-\d{2})', task['text'])
        if due_match and due_match.group(1) < today:
            overdue.append(task['text'])

    return overdue


def should_ping() -> bool:
    """Only ping during reasonable hours."""
    hour = datetime.now().hour
    return 9 <= hour <= 21


def generate_nudge() -> Optional[str]:
    """Generate ONE smart nudge, prioritized."""

    # Priority 1: Birthdays
    birthdays = get_upcoming_birthdays()
    for bday in birthdays:
        topic = f"birthday_{bday['name']}"
        if not was_recently_nudged(topic, hours=24):
            if bday['days'] == 0:
                msg = f"It's {bday['name']}'s birthday today! Send a message?"
            elif bday['days'] == 1:
                msg = f"{bday['name']}'s birthday is tomorrow ({bday['date']})"
            else:
                msg = f"{bday['name']}'s birthday in {bday['days']} days ({bday['date']})"
            record_nudge(topic, msg)
            return msg

    # Priority 2: Overdue tasks
    overdue = get_overdue_tasks()
    if overdue:
        task = overdue[0]
        topic = f"overdue_{task[:30]}"
        if not was_recently_nudged(topic, hours=8):
            msg = f"Overdue: {task[:60]}"
            record_nudge(topic, msg)
            return msg

    # Priority 3: Stale open loops (> 7 days)
    loops = get_open_loops()
    for loop in loops:
        try:
            added = datetime.strptime(loop['added'], '%Y-%m-%d')
            days_old = (datetime.now() - added).days
            if days_old >= 7:
                topic = f"loop_{loop['what'][:30]}"
                if not was_recently_nudged(topic, hours=24):
                    msg = f"Open loop for {days_old} days: {loop['what']}\nStill relevant? Close it or act on it."
                    record_nudge(topic, msg)
                    return msg
        except (ValueError, KeyError):
            continue

    # Priority 4: General task nudge (use AI)
    tasks = get_pending_tasks()
    if tasks and not was_recently_nudged("general_task", hours=8):
        task = tasks[0]
        try:
            msg = call_ai(
                f"Write a brief, friendly one-line nudge about this task: {task['text'][:60]}",
                system="You send brief nudges. One line. Be encouraging, not nagging.",
                max_tokens=100,
            )
            record_nudge("general_task", msg)
            return msg
        except Exception:
            pass

    return None


def main():
    log("Running proactive ping...", "proactive_ping.log")

    if not should_ping():
        log("Outside ping hours, skipping", "proactive_ping.log")
        return

    nudge = generate_nudge()

    if nudge:
        log(f"Sending: {nudge[:50]}...", "proactive_ping.log")
        if send_notification(nudge):
            log("Sent!", "proactive_ping.log")
        else:
            log("Failed to send", "proactive_ping.log")
    else:
        log("Nothing to nudge about", "proactive_ping.log")


if __name__ == '__main__':
    main()
