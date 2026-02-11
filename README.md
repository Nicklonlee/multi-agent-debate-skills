# Multi-Agent Debate System

Orchestrate structured multi-round debates among AI agents to produce comprehensive, evidence-based analysis of any idea, question, or topic.

**4 Agent Roles**: Optimist (opportunities) | Critic (risks) | Researcher (data) | Verifier (logic)

**2-3 Round Process**: Independent analysis → Cross-examination → Deep debate (if needed) → Final synthesis

## Installation

### Option 1: Standalone CLI

```bash
git clone https://github.com/Nicklonlee/multi-agent-debate-skills.git
cd multi-agent-debate-skills
pip install openai
```

Set an API key (the script auto-detects the first one found):

```bash
export DEEPSEEK_API_KEY=sk-xxx    # DeepSeek (default)
# or
export OPENAI_API_KEY=sk-xxx      # OpenAI
# or
export ANTHROPIC_API_KEY=sk-xxx   # Anthropic Claude
# or
export MINIMAX_API_KEY=xxx        # MiniMax
```

Run:

```bash
python3 skills/multi-agent-debate/scripts/debate.py "Should we build a SaaS product for X?"
```

### Option 2: Claude Code Plugin

```
/plugin marketplace add Nicklonlee/multi-agent-debate-skills
/plugin install multi-agent-debate
```

Then use the slash command:

```
/debate Should we build a SaaS product for X?
```

### Option 3: Agent Skills (Universal)

Copy the `skills/multi-agent-debate/` directory into your tool's skills folder:

```bash
# Claude Code
cp -r skills/multi-agent-debate ~/.claude/skills/

# Or any Agent Skills-compatible tool
cp -r skills/multi-agent-debate <YOUR_TOOL_SKILLS_DIR>/
```

The `SKILL.md` file follows the [Agent Skills](https://github.com/anthropics/agent-skills) open standard, compatible with 25+ tools including Claude Code, Gemini CLI, Cursor, VS Code Copilot, and more.

## Configuration

### Environment Variables (Recommended)

The script auto-detects API keys in this order: `DEEPSEEK_API_KEY` → `OPENAI_API_KEY` → `ANTHROPIC_API_KEY` → `MINIMAX_API_KEY`.

Override defaults with:

| Variable | Purpose |
|----------|---------|
| `DEBATE_PROVIDER` | Display name |
| `DEBATE_BASE_URL` | Custom API endpoint |
| `DEBATE_MODEL_CHAT` | Chat model |
| `DEBATE_MODEL_REASON` | Reasoning model |

### Interactive Setup

```bash
python3 skills/multi-agent-debate/scripts/debate.py --setup "your topic"
```

This launches an interactive wizard to select provider, enter API key, and choose models. Configuration is saved to `.debate_config.json`.

### Config File

The script also reads `.debate_config.json` (checked in CWD first, then repo root). This file is created by `--setup` and contains provider, base URL, API key, and model selections.

## Output

The debate produces a structured Markdown report saved to `debate_output.md` in the current working directory, containing:

- Core recommendation
- Consensus points
- Resolved disagreements (with rulings)
- Key data & evidence
- Risk assessment matrix
- Action plan
- Debate metadata

## Dual-Mode Operation

| Mode | Requirement | How It Works |
|------|-------------|--------------|
| **Script Mode** | Python 3 + `openai` package | Runs `debate.py` which calls LLM APIs directly |
| **Native Mode** | None (AI agent only) | The AI agent follows `PROTOCOL.md` to execute the debate itself |

The `SKILL.md` entry point automatically detects which mode to use.

## Project Structure

```
multi-agent-debate/
├── .claude-plugin/
│   └── marketplace.json          # Claude Code Plugin manifest
├── skills/
│   └── multi-agent-debate/
│       ├── SKILL.md              # Agent Skills standard entry
│       ├── scripts/
│       │   └── debate.py         # Debate engine
│       └── references/
│           ├── PROTOCOL.md       # Native mode protocol
│           └── PROVIDERS.md      # API provider reference
├── .claude/
│   └── commands/
│       └── debate.md             # /debate slash command
├── .gitignore
├── README.md
└── CLAUDE.md
```

## License

MIT
