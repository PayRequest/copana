"""
Copana Utilities — Shared functions for all automation scripts.

Provides: notification sending, AI calls, context loading, logging.
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv

# Load environment
COPANA_DIR = Path(__file__).parent.parent
load_dotenv(COPANA_DIR / '.env')

# Config
AI_MODEL = os.getenv('AI_MODEL', 'claude-haiku-4-5-20251001')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NTFY_TOPIC = os.getenv('NTFY_TOPIC')

LOG_DIR = COPANA_DIR / 'logs'
DATA_DIR = COPANA_DIR / 'data'


def log(message: str, log_file: str = 'copana.log'):
    """Log with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)

    LOG_DIR.mkdir(exist_ok=True)
    with open(LOG_DIR / log_file, 'a') as f:
        f.write(log_line + '\n')


def send_notification(message: str, reply_markup: dict = None) -> bool:
    """Send notification via configured channel (Telegram or ntfy)."""
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return send_telegram(message, reply_markup)
    elif NTFY_TOPIC:
        return send_ntfy(message)
    else:
        log("No notification channel configured (set TELEGRAM_BOT_TOKEN or NTFY_TOPIC in .env)")
        return False


def send_telegram(message: str, reply_markup: dict = None) -> bool:
    """Send message via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        log(f"Telegram error: {e}")
        return False


def send_ntfy(message: str) -> bool:
    """Send notification via ntfy.sh."""
    try:
        response = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            timeout=10,
        )
        return response.status_code == 200
    except Exception as e:
        log(f"ntfy error: {e}")
        return False


def call_ai(prompt: str, system: str = None, max_tokens: int = 500) -> str:
    """Call Claude API for AI-powered features."""
    if not ANTHROPIC_API_KEY:
        log("ANTHROPIC_API_KEY not set — AI features disabled")
        return ""

    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    kwargs = {
        "model": AI_MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system

    message = client.messages.create(**kwargs)
    return message.content[0].text


def load_context(files: list = None) -> dict:
    """Load markdown files into a dict for AI context."""
    if files is None:
        files = ['memory.md', 'tasks.md', 'insights.md', 'user.md', 'routines.md']

    context = {}
    for filename in files:
        filepath = COPANA_DIR / filename
        if filepath.exists():
            context[filename] = filepath.read_text()

    return context


def get_open_loops() -> list:
    """Get open loops from memory.md."""
    memory_file = COPANA_DIR / 'memory.md'
    loops = []

    if memory_file.exists():
        content = memory_file.read_text()
        if '## Open Loops' in content:
            section = content.split('## Open Loops')[1].split('##')[0]
            for line in section.split('\n'):
                if line.strip().startswith('|') and 'What' not in line and '---' not in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 3:
                        loops.append({
                            'what': parts[0],
                            'context': parts[1],
                            'added': parts[2],
                        })
    return loops


def get_pending_tasks() -> list:
    """Get pending tasks from tasks.md."""
    import re

    tasks_file = COPANA_DIR / 'tasks.md'
    tasks = []

    if tasks_file.exists():
        content = tasks_file.read_text()
        pattern = r'- \[ \] (.+)'
        for match in re.findall(pattern, content):
            task_text = match.strip()
            tags = re.findall(r'#(\w+)', task_text)
            tasks.append({'text': task_text, 'tags': tags})

    return tasks


def save_data(filename: str, data: dict):
    """Save JSON data to data/ directory."""
    DATA_DIR.mkdir(exist_ok=True)
    filepath = DATA_DIR / filename
    filepath.write_text(json.dumps(data, indent=2))


def load_data(filename: str) -> Optional[dict]:
    """Load JSON data from data/ directory."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        try:
            return json.loads(filepath.read_text())
        except Exception:
            return None
    return None
