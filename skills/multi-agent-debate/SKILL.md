---
name: multi-agent-debate
description: >
  Orchestrate a structured multi-round debate among AI agents (optimist, critic,
  researcher, verifier) to produce comprehensive, evidence-based analysis of any
  idea, question, or topic.
allowed-tools:
  - Bash
  - Task
  - WebSearch
  - WebFetch
  - Read
  - Write
metadata:
  version: "1.0.0"
  author: allenenli
  tags:
    - debate
    - analysis
    - multi-agent
  license: MIT
---

# Multi-Agent Debate

Orchestrate a structured multi-round debate with 4 AI agent roles to analyze any idea or question from multiple perspectives.

## Environment Detection

Before executing, determine which mode to use:

### Script Mode (Preferred)

Check if the Python environment is available:

```bash
python3 -c "import openai" 2>/dev/null
```

If the above succeeds, use **Script Mode**. Otherwise, fall back to **Native Mode**.

## Script Mode

Run the debate engine script directly. The script auto-detects API keys from environment variables.

### Required Environment Variables (set one)

| Variable | Provider |
|----------|----------|
| `DEEPSEEK_API_KEY` | DeepSeek (checked first) |
| `OPENAI_API_KEY` | OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic Claude |
| `MINIMAX_API_KEY` | MiniMax |

### Optional Override Variables

| Variable | Purpose |
|----------|---------|
| `DEBATE_PROVIDER` | Display name override |
| `DEBATE_BASE_URL` | Custom API base URL |
| `DEBATE_MODEL_CHAT` | Chat model name |
| `DEBATE_MODEL_REASON` | Reasoning model name |

See `references/PROVIDERS.md` for full provider configuration details.

### Execution

```bash
python3 skills/multi-agent-debate/scripts/debate.py "YOUR_TOPIC_HERE"
```

The script will:
1. Auto-detect API configuration from environment variables
2. Run a 2-3 round structured debate with 4 agent roles
3. Save the full output to `debate_output.md` in the current working directory

### Script Flags

- `--setup` - Force interactive API configuration (ignores env vars and saved config)
- No arguments - Interactive mode (prompts for topic)

## Native Mode (Fallback)

If Python + openai is not available, execute the debate protocol directly using the AI agent's built-in capabilities.

Follow the complete protocol defined in `references/PROTOCOL.md`.

In Native Mode, the AI agent itself plays each debate role sequentially:
1. **Round 1**: Generate independent analyses as optimist, critic, and researcher (use `Task` tool for parallel execution if available)
2. **Round 2**: Cross-examine — identify disagreements, have each role respond, then verify logic
3. **Round 3** (conditional): Deep debate on remaining unresolved disagreements
4. **Synthesis**: Produce the final structured report

Use `WebSearch` to ground arguments in real data when available.

## Output Format

Both modes produce a structured report:

```markdown
# Debate Conclusion: [Topic]
## Core Recommendation
## Consensus Points
## Resolved Disagreements (table)
## Key Data & Evidence
## Risk Assessment (table)
## Action Plan
## Debate Metadata
```
