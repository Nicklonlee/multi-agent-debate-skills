Execute the multi-agent-debate skill on the following topic:

$ARGUMENTS

First, check if the Python environment is ready:
```bash
python3 -c "import openai" 2>/dev/null
```

If Python + openai is available, run the debate via script:
```bash
python3 skills/multi-agent-debate/scripts/debate.py "$ARGUMENTS"
```

Otherwise, follow the protocol in `skills/multi-agent-debate/references/PROTOCOL.md`:
Launch optimist, critic, and researcher agents in parallel for Round 1,
then proceed through cross-examination and synthesis as defined in the protocol.
