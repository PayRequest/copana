# Budget Tracker Plugin

Example: Add budget tracking to your Copana setup.

## Setup

1. Create `budget.md` in your repo root:

```markdown
# Budget

## Monthly Budget: $3,000

## Categories
| Category | Budget | Spent |
|----------|--------|-------|
| Rent | $1,200 | $1,200 |
| Food | $400 | $0 |
| Transport | $150 | $0 |
| Fun | $200 | $0 |

## Transactions
<!-- Add as they happen -->
| Date | Amount | Category | Note |
|------|--------|----------|------|
```

2. Add to CLAUDE.md file registry:

```markdown
| `budget.md` | Monthly budget and spending |
```

3. Your AI will now reference budget when money comes up.

## Optional: Daily Budget Alert

Add a cron job that checks spending:

```python
# scripts/budget_alert.py
from copana_utils import COPANA_DIR, send_notification

budget_file = COPANA_DIR / 'budget.md'
# Parse and check spending vs budget
# Send alert if overspending
```
