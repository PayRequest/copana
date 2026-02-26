# /add-fitness — Add Fitness Tracking

Add workout tracking and gym accountability to your Copana setup.

## Steps

1. **Ask the user:**
   - What's your fitness goal? (e.g., lose weight, build muscle, run a 5k)
   - How many days per week do you want to work out?
   - Which days? (e.g., Mon/Wed/Fri)
   - Any specific program? (or want a suggestion)

2. **Create `fitness.md`** in the repo root with:
   - Goals section
   - Weekly schedule
   - Workout log table (Date | Activity | Duration | Notes)
   - Current stats if provided (weight, etc.)

3. **Update CLAUDE.md** — add to file registry:
   ```markdown
   | `fitness.md` | Workout plan and log |
   ```

4. **Update `personality.md`** — add accountability:
   ```markdown
   ## Accountability
   - Gym: [days] — I'll check
   ```

5. **Optionally update `proactive_ping.py`** — add gym day check:
   ```python
   def check_gym_day():
       gym_days = [0, 2, 4]  # Mon, Wed, Fri
       if datetime.now().weekday() in gym_days:
           return "Gym day. No excuses."
       return None
   ```

6. **Commit changes.**
