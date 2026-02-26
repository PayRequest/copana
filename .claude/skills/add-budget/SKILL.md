# /add-budget — Add Budget Tracking

Add personal budget tracking to your Copana setup.

## Steps

1. **Ask the user:**
   - Monthly budget amount
   - Budget categories (or use sensible defaults: Rent, Food, Transport, Fun, Savings)
   - Currency (default: USD)

2. **Create `budget.md`** in the repo root with:
   - Monthly budget total
   - Categories table (Category | Budget | Spent)
   - Transactions log table (Date | Amount | Category | Note)

3. **Update CLAUDE.md** — add to file registry:
   ```markdown
   | `budget.md` | Monthly budget and spending |
   ```

4. **Add to CLAUDE.md anticipation rules:**
   ```markdown
   - If {{human_name}} mentions money → check budget.md for context
   ```

5. **Optionally create `scripts/budget_alert.py`** — daily budget check:
   - Parse budget.md for spending
   - Calculate remaining budget
   - Send notification if overspending
   - Add to crontab

6. **Commit changes.**
