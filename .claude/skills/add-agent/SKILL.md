# /add-agent — Create a Custom Subagent

Create a specialized Claude Code subagent for your Copana setup.

## Steps

1. **Ask the user:**
   - What should the agent do? (e.g., "review my code", "manage my calendar", "track habits")
   - Should it have web access? (WebSearch, WebFetch)
   - Should it be able to edit files? (Write, Edit)
   - Should it use a smaller model for speed? (haiku vs sonnet)
   - Should it have persistent memory? (remembers across sessions)

2. **Create `.claude/agents/agent-name.md`** with YAML frontmatter:
   ```yaml
   ---
   name: agent-name
   description: One-line description
   model: haiku  # or omit for default
   tools:
     - Read
     - Write    # only if needed
     - Edit     # only if needed
     - Glob
     - Grep
     - WebSearch  # only if needed
     - WebFetch   # only if needed
   memory: project  # or omit for no persistence
   ---
   ```

3. **Write the agent instructions** below the frontmatter:
   - Clear role description
   - What files it manages
   - Output format
   - Rules and constraints

4. **Test the agent:**
   - Run it with a sample task
   - Verify it stays within its tool permissions
   - Check that output is useful

5. **Commit changes.**

## Built-in Agents

Copana ships with three agents:

| Agent | Purpose | Model |
|-------|---------|-------|
| `memory-manager` | Consolidate and clean memory files | haiku |
| `research` | Web research with structured output | default |
| `daily-review` | End-of-day file review and summary | haiku |

## Tips

- Use `model: haiku` for simple, repetitive tasks (faster and cheaper)
- Only grant tools the agent actually needs — fewer tools = more focused
- `memory: project` lets the agent build up knowledge across sessions
- Keep agent instructions under 100 lines
