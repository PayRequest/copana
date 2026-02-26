# Social Posting Plugin

Example: Add X/Twitter content management to your Copana setup.

## Setup

1. Create `content-queue.md` in your repo root:

```markdown
# Content Queue

## Content Pillars
- Topic 1: Your expertise
- Topic 2: Behind the scenes
- Topic 3: Opinions and takes

## Voice Guide
- Short, punchy
- Personal, not corporate
- No lies, no exaggeration

## Queue
| # | Tweet | Status |
|---|-------|--------|
| 1 | Your first tweet idea | draft |
| 2 | Another idea | draft |

## Posted
| Date | Tweet | Link |
|------|-------|------|
```

2. Add to CLAUDE.md file registry:

```markdown
| `content-queue.md` | Social media content queue |
```

3. Your AI can help draft tweets, maintain your voice, and manage the queue.

## Optional: Auto-posting

Create `scripts/social_post.py` to post the next queued tweet via the X API. Add to cron for daily posting.
