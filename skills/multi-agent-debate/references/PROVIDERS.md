# Supported API Providers

The debate engine supports any OpenAI-compatible API. Below are pre-configured providers.

## Provider Configuration

| # | Provider | Base URL | Chat Model | Reasoning Model | Env Variable |
|---|----------|----------|------------|-----------------|--------------|
| 1 | DeepSeek | `https://api.deepseek.com` | `deepseek-chat` | `deepseek-reasoner` | `DEEPSEEK_API_KEY` |
| 2 | OpenAI | `https://api.openai.com/v1` | `gpt-4o` | `gpt-4o` | `OPENAI_API_KEY` |
| 3 | Claude (OpenAI-compat) | `https://api.anthropic.com/v1` | `claude-sonnet-4-5-20250929` | `claude-sonnet-4-5-20250929` | `ANTHROPIC_API_KEY` |
| 4 | MiniMax | `https://api.minimax.chat/v1` | `MiniMax-Text-01` | `MiniMax-Text-01` | `MINIMAX_API_KEY` |
| 5 | Custom | User-defined | User-defined | User-defined | User-defined |

## Auto-Detection Order

When using environment variables (no `--setup` flag), the script checks keys in this order:

1. `DEEPSEEK_API_KEY`
2. `OPENAI_API_KEY`
3. `ANTHROPIC_API_KEY`
4. `MINIMAX_API_KEY`

The first key found is used with its provider's default configuration.

## Override Variables

These environment variables override the auto-detected defaults:

| Variable | Purpose | Example |
|----------|---------|---------|
| `DEBATE_PROVIDER` | Display name (cosmetic) | `MyProvider` |
| `DEBATE_BASE_URL` | API base URL | `https://my-proxy.example.com/v1` |
| `DEBATE_MODEL_CHAT` | Chat model | `gpt-4o-mini` |
| `DEBATE_MODEL_REASON` | Reasoning model | `o1-preview` |

## Examples

### DeepSeek (default)
```bash
export DEEPSEEK_API_KEY=sk-xxx
python3 skills/multi-agent-debate/scripts/debate.py "your topic"
```

### OpenAI with custom models
```bash
export OPENAI_API_KEY=sk-xxx
export DEBATE_MODEL_CHAT=gpt-4o-mini
export DEBATE_MODEL_REASON=o1-preview
python3 skills/multi-agent-debate/scripts/debate.py "your topic"
```

### Custom OpenAI-compatible provider
```bash
export OPENAI_API_KEY=sk-xxx
export DEBATE_BASE_URL=https://my-proxy.example.com/v1
export DEBATE_PROVIDER="My Proxy"
python3 skills/multi-agent-debate/scripts/debate.py "your topic"
```

### Interactive setup (ignores env vars)
```bash
python3 skills/multi-agent-debate/scripts/debate.py --setup "your topic"
```
