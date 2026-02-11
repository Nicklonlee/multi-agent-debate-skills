# Multi-Agent Debate Protocol (Native Mode)

This protocol defines how to execute a multi-agent debate without the Python script, using only the AI agent's built-in capabilities.

## Agent Roles

| Role | Focus | Style |
|------|-------|-------|
| **Optimist** (Opportunity Analyst) | Feasibility, market opportunities, success precedents, positive factors | Cite real examples, rate confidence High/Medium/Low |
| **Critic** (Risk Analyst) | Risks, competitive threats, failure cases, regulatory challenges | Cite real failures, rate confidence High/Medium/Low |
| **Researcher** (Deep Researcher) | Market size, players, tech landscape, regulations, unit economics | Provide specific numbers and data |
| **Verifier** (Logic Arbiter) | Logical consistency, contradictions, unsupported claims | Issue clear rulings, be impartial |

## Execution Flow

### Round 1: Independent Analysis

Dispatch optimist, critic, and researcher as **parallel subagents** (use the Task tool to launch all three concurrently). Each agent must:

1. Use WebSearch to find at least 3 relevant and authoritative sources
2. Provide a structured analysis with citations and source URLs
3. Rate their confidence level for each major claim (High / Medium / Low)
4. Output in this format:

```markdown
## [Role Name] Analysis

### Key Points
1. [Point] (Confidence: High/Medium/Low)
   - Evidence: [source URL]
2. ...

### Summary
[2-3 sentence summary of position]
```

### Round 2: Cross-Examination

1. Synthesize all Round 1 outputs. Extract the **core disagreement points** as a numbered list (top 3-5).
2. For each disagreement point:
   - Send to optimist: "The critic argues [X]. Respond with evidence."
   - Send to critic: "The optimist argues [Y]. Respond with evidence."
3. Dispatch researcher to fact-check the top 3 most contested claims.
4. Dispatch verifier to check logical consistency across all arguments and issue rulings.

### Round 3: Deep Debate (Conditional)

Only execute this round if Round 2 still has **more than 2 unresolved major disagreements**.

1. For each remaining disagreement, run a focused 1-on-1 exchange between optimist and critic.
2. Researcher provides supplementary data for each point.
3. Verifier issues a definitive ruling on each disagreement with reasoning.

If there are 2 or fewer disagreements after Round 2, skip directly to Synthesis.

### Synthesis & Final Output

Produce a comprehensive final report with this exact structure:

```markdown
# Debate Conclusion: [Topic]

## Core Recommendation
[One paragraph with the final recommendation]

## Consensus Points
- [Points all agents agreed on]

## Resolved Disagreements
| Issue | Optimist View | Critic View | Ruling | Reasoning |
|-------|--------------|-------------|--------|-----------|
| ...   | ...          | ...         | ...    | ...       |

## Key Data & Evidence
1. [Most important fact/data point] - Source: [URL]
2. ...

## Risk Assessment
| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| ...  | ...      | ...        | ...        |

## Action Plan
1. [Concrete next step]
2. ...

## Debate Metadata
- Rounds completed: [N]
- Sources consulted: [N]
- Key disagreements resolved: [N/M]
```

## Language

All output should be in Chinese (中文) by default. If the user's topic is in English, output in English instead.
