# Multi-Agent Debate System

A multi-agent debate system that orchestrates 4 AI agent roles (optimist, critic,
researcher, verifier) through structured multi-round debate for comprehensive idea analysis.

## Project Structure

- `skills/multi-agent-debate/SKILL.md` - Agent Skills standard entry point (works with Claude Code, Gemini CLI, Cursor, VS Code Copilot, etc.)
- `skills/multi-agent-debate/scripts/debate.py` - Python debate engine (requires `openai` package)
- `skills/multi-agent-debate/references/PROTOCOL.md` - Native mode protocol (no Python needed)
- `skills/multi-agent-debate/references/PROVIDERS.md` - Supported API providers reference
- `.claude-plugin/marketplace.json` - Claude Code Plugin manifest
- `.claude/commands/debate.md` - `/debate` slash command

## Usage

### Quick Start (CLI)
```bash
export DEEPSEEK_API_KEY=sk-xxx  # or OPENAI_API_KEY, ANTHROPIC_API_KEY, MINIMAX_API_KEY
python3 skills/multi-agent-debate/scripts/debate.py "your topic"
```

### As Claude Code Plugin
Use `/debate your topic` after installing.

### Key Instructions
- The debate engine auto-detects API keys from environment variables
- Run agents in parallel when possible (Round 1 especially)
- The SKILL.md defines dual-mode operation: Script Mode (Python) and Native Mode (fallback)
- Output is saved to `debate_output.md` in the current working directory
