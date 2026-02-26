# Fitness Plugin

Example: Add fitness tracking to your Copana setup.

## Setup

1. Create `fitness.md` in your repo root:

```markdown
# Fitness

## Goals
- Workout 3x/week
- Run 5k under 25 minutes

## Schedule
| Day | Activity |
|-----|----------|
| Mon | Upper body |
| Wed | Lower body |
| Fri | Cardio |

## Log
| Date | Activity | Duration | Notes |
|------|----------|----------|-------|
```

2. Add to CLAUDE.md file registry:

```markdown
| `fitness.md` | Workout plan and log |
```

3. Add to personality.md accountability section:

```markdown
## Accountability
- Gym: Mon/Wed/Fri — I'll check
```

4. Your AI will now remind you on gym days and track your consistency.

## Optional: Gym Day Reminder

Add to `proactive_ping.py`:

```python
def check_gym_day():
    today = datetime.now().weekday()
    gym_days = [0, 2, 4]  # Mon, Wed, Fri
    if today in gym_days:
        return "Gym day. No excuses."
    return None
```
