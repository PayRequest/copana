# Philosophy

## The Problem

AI assistants are incredibly capable but fundamentally forgetful. Every conversation starts from zero. No memory of what you told it yesterday. No knowledge of your goals, preferences, or patterns. No follow-through on commitments.

This makes AI feel like talking to a brilliant stranger every time.

## The Insight

The best personal AI isn't the smartest model. It's the one with the most context about *you*.

A "dumber" model that knows your goals, remembers your open tasks, and follows up on commitments is infinitely more useful than a genius model that forgets everything the moment you close the tab.

## The Approach

Copana solves this with the simplest possible architecture:

1. **Markdown files** for memory (not a database)
2. **Git** for version control (not a cloud sync service)
3. **Claude Code** as the runtime (not a custom app)
4. **Cron jobs** for proactive behavior (not a background service)

No server. No Docker. No build step. No infrastructure to maintain.

## Design Principles

### Plain text over databases
Markdown files are human-readable, version-controlled, and portable. You can open them in any text editor, grep through them, or move them to a different system. Try doing that with a database.

### Convention over configuration
Copana works by following conventions: specific file names, specific section headers, a specific startup ritual. This means zero configuration — clone, setup, go.

### Opt-in complexity
The core (CLAUDE.md + markdown files) has zero dependencies. Automation scripts are optional. Telegram bot is optional. News feeds are optional. Start simple, add complexity only when you need it.

### Privacy by default
Your data never leaves your machine unless you explicitly push to GitHub. No telemetry, no analytics, no cloud processing of your personal information.

### AI-native, not AI-bolted
Copana isn't a productivity app with AI sprinkled on top. It's designed from the ground up for how AI actually works: reading context, generating responses, maintaining state through text.

## Why Not...

### ...a database?
Markdown files are good enough. They're human-readable, version-controlled, and your AI can read them just fine. A database adds complexity without meaningful benefit for personal context.

### ...a custom app?
Claude Code is already an excellent runtime. It has file access, shell access, and the full power of Claude. Building a custom app would mean maintaining it. Claude Code is maintained by Anthropic.

### ...embeddings/RAG?
For personal context (~20 files, ~50KB total), full-file reading is fast and reliable. RAG adds complexity and can miss context that full reading captures. When your context grows beyond what fits in a conversation, you can split files or archive old data.

### ...a cloud service?
Your personal context — goals, preferences, relationships, financial info — is sensitive. A local git repo gives you complete control. Push to a private GitHub repo for backup if you want, but it's your choice.

## The Goal

An AI that feels less like a tool and more like a colleague. One that knows your context, remembers your preferences, follows through on commitments, and gets better the more you use it.

Not through magic. Through structured plain text and good conventions.
