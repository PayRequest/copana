#!/usr/bin/env python3
"""
Weekly Review — Close the loop on your week.

Reviews:
1. Check-ins (mood, energy patterns)
2. Tasks completed vs planned
3. Open loops
4. Generates insights for next week

Runs Sunday evening (e.g., 20:00) via cron.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))
from copana_utils import (
    COPANA_DIR, call_ai, send_notification, load_context,
    get_pending_tasks, log,
)

CHECKIN_LOG = COPANA_DIR / 'logs' / 'checkins.json'
REVIEW_DIR = COPANA_DIR / 'memory' / 'reviews'


def get_week_checkins() -> list:
    """Get check-ins from the past week."""
    if not CHECKIN_LOG.exists():
        return []
    try:
        checkins = json.loads(CHECKIN_LOG.read_text())
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        return [c for c in checkins if c.get('date', '') >= week_ago]
    except (json.JSONDecodeError, Exception):
        return []


def get_completed_tasks() -> list:
    """Get completed tasks from tasks.md."""
    tasks_file = COPANA_DIR / 'tasks.md'
    if not tasks_file.exists():
        return []

    completed = []
    for line in tasks_file.read_text().split('\n'):
        if line.strip().startswith('- [x]'):
            completed.append(line.strip()[6:])
    return completed[-10:]


def generate_review(checkins: list, completed: list, pending: list, context: dict) -> str:
    """Generate weekly review using AI."""
    prompt = f"""Generate a weekly review based on this data:

Check-ins ({len(checkins)} days logged):
{json.dumps(checkins, indent=2) if checkins else "No check-ins recorded"}

Tasks completed: {completed if completed else "None tracked"}
Tasks still pending: {[t['text'][:50] for t in pending[:10]]}

Session notes:
{context.get('memory.md', '')[:1500]}

Generate:
1. Week at a glance (2-3 lines)
2. What went well
3. What to watch (patterns, concerns)
4. Focus for next week (1-2 specific things)

Keep it honest and actionable. Max 400 words."""

    return call_ai(
        prompt,
        system="You write weekly reviews. Be honest, direct, and actionable. Highlight patterns.",
        max_tokens=1500,
    )


def save_review(review: str):
    """Save review to memory/reviews/."""
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime('%Y-%m-%d')
    week_num = datetime.now().isocalendar()[1]

    content = f"""# Weekly Review — Week {week_num}
*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*

{review}
"""

    (REVIEW_DIR / f'{today}-week{week_num}.md').write_text(content)
    log(f"Review saved for week {week_num}", "weekly_review.log")


def main():
    log("Starting weekly review...", "weekly_review.log")

    checkins = get_week_checkins()
    completed = get_completed_tasks()
    pending = get_pending_tasks()
    context = load_context(['memory.md', 'tasks.md'])

    log(f"Data: {len(checkins)} checkins, {len(completed)} completed, {len(pending)} pending", "weekly_review.log")

    review = generate_review(checkins, completed, pending, context)

    if not review:
        log("AI not configured, skipping", "weekly_review.log")
        return

    save_review(review)

    # Send notification
    msg = f"Weekly Review\n\n{review}"
    if len(msg) > 4000:
        msg = msg[:3950] + "\n\n...Full review in memory/reviews/"

    if send_notification(msg):
        log("Review sent!", "weekly_review.log")

    log("Done!", "weekly_review.log")


if __name__ == '__main__':
    main()
