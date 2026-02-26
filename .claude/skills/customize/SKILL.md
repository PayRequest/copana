# /customize — Guided Customization

Help the user customize their Copana setup by modifying the codebase directly.

## When to use

Run when the user wants to change how their AI works, add new features, or adjust behavior.

## How it works

1. **Ask what they want to change.** Common options:
   - Change the AI's personality or vibe
   - Add new memory files (e.g., fitness.md, budget.md)
   - Modify the startup ritual
   - Add new accountability areas
   - Change notification preferences
   - Add new automation scripts

2. **Read the relevant files** to understand current state.

3. **Make the changes directly** — edit the markdown files or scripts. Copana is designed to be modified.

4. **Update CLAUDE.md** if you added new files — add them to the file registry table.

5. **Commit the changes** with a descriptive message.

## Common customizations

### Add a new domain file
1. Create the `.md` file with section headers
2. Add it to CLAUDE.md file registry table
3. Reference it in the relevant section of CLAUDE.md

### Change personality
1. Edit `soul.md` for values and identity
2. Edit `personality.md` for communication style
3. The AI will follow the updated personality next session

### Add accountability
1. Add the area to `personality.md` accountability section
2. Add relevant checks to `proactive_ping.py` if automation is wanted

### Add a new automation
1. Create script in `scripts/` following the pattern of existing scripts
2. Use `copana_utils.py` for notifications, AI calls, logging
3. Add to `crontab.example`
4. Add to `scripts/README.md`

## Principles
- Keep it simple — don't over-engineer
- Modify code directly, don't add config layers
- If adding a file, update CLAUDE.md registry
- Commit changes so they're version-controlled
