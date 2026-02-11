#!/usr/bin/env python3
"""
Multi-Agent Debate System
=========================
Orchestrates multiple AI agents through structured multi-round debate.

Supports: DeepSeek, OpenAI, Claude, MiniMax, or any OpenAI-compatible API.

Usage:
    python debate.py "Your idea"          # Use env vars or saved config
    python debate.py --setup "Your idea"  # Re-configure API first
    python debate.py                      # Interactive mode

Environment Variables (auto-detected in order):
    DEEPSEEK_API_KEY   - DeepSeek API
    OPENAI_API_KEY     - OpenAI API
    ANTHROPIC_API_KEY  - Anthropic Claude API
    MINIMAX_API_KEY    - MiniMax API

    Override defaults:
    DEBATE_PROVIDER    - Provider name (for display only)
    DEBATE_BASE_URL    - Custom base URL
    DEBATE_MODEL_CHAT  - Chat model name
    DEBATE_MODEL_REASON - Reasoning model name

Requires:
    pip install openai
"""

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from openai import OpenAI

# ---------- Config ----------

SCRIPT_DIR = Path(__file__).resolve().parent.parent.parent.parent  # repo root
CWD = Path.cwd()

# Check CWD first, then script's repo root for config
CONFIG_PATHS = [CWD / ".debate_config.json", SCRIPT_DIR / ".debate_config.json"]

# Pre-defined providers
PROVIDERS = {
    "1": {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com",
        "models": {"chat": "deepseek-chat", "reason": "deepseek-reasoner"},
        "env_key": "DEEPSEEK_API_KEY",
    },
    "2": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": {"chat": "gpt-4o", "reason": "gpt-4o"},
        "env_key": "OPENAI_API_KEY",
    },
    "3": {
        "name": "Claude (via OpenAI-compatible proxy)",
        "base_url": "https://api.anthropic.com/v1",
        "models": {"chat": "claude-sonnet-4-5-20250929", "reason": "claude-sonnet-4-5-20250929"},
        "env_key": "ANTHROPIC_API_KEY",
    },
    "4": {
        "name": "MiniMax",
        "base_url": "https://api.minimax.chat/v1",
        "models": {"chat": "MiniMax-Text-01", "reason": "MiniMax-Text-01"},
        "env_key": "MINIMAX_API_KEY",
    },
    "5": {
        "name": "Custom (OpenAI-compatible)",
        "base_url": "https://www.chataiapi.com",
        "models": {"chat": "", "reason": ""},
        "env_key": "",
    },
}

# Provider detection order for auto_detect_config
_AUTO_DETECT_ORDER = ["1", "2", "3", "4"]


def auto_detect_config() -> dict | None:
    """Auto-detect API config from environment variables.

    Checks DEEPSEEK_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, MINIMAX_API_KEY
    in order. Returns config dict on first match, or None if nothing found.

    Override variables DEBATE_PROVIDER, DEBATE_BASE_URL, DEBATE_MODEL_CHAT,
    DEBATE_MODEL_REASON take precedence over provider defaults.
    """
    for key in _AUTO_DETECT_ORDER:
        provider = PROVIDERS[key]
        env_key = provider["env_key"]
        api_key = os.environ.get(env_key, "").strip()
        if not api_key:
            continue

        config = {
            "provider": os.environ.get("DEBATE_PROVIDER", provider["name"]),
            "base_url": os.environ.get("DEBATE_BASE_URL", provider["base_url"]),
            "api_key": api_key,
            "model_chat": os.environ.get("DEBATE_MODEL_CHAT", provider["models"]["chat"]),
            "model_reason": os.environ.get("DEBATE_MODEL_REASON", provider["models"]["reason"]),
        }
        print(f"[Auto-detect] Using {env_key} → {config['provider']}")
        return config

    return None


def _find_config_path() -> Path | None:
    """Find existing config file (CWD first, then repo root)."""
    for p in CONFIG_PATHS:
        if p.exists():
            return p
    return None


def setup_config() -> dict:
    """Interactive setup: choose provider, enter API key, pick models."""
    print("\n" + "=" * 60)
    print("  Multi-Agent Debate System - API Configuration")
    print("=" * 60)
    print("\nSelect your LLM provider:\n")
    for k, v in PROVIDERS.items():
        print(f"  [{k}] {v['name']}")
    print()

    choice = input("Enter number (1-5): ").strip()
    if choice not in PROVIDERS:
        print("Invalid choice, defaulting to DeepSeek")
        choice = "1"

    provider = PROVIDERS[choice]

    # Base URL
    if choice == "5":
        base_url = input("Enter base URL (e.g. https://www.chataiapi.com/v1): ").strip()
    else:
        default_url = provider["base_url"]
        custom_url = input(f"Base URL [{default_url}] (press Enter for default): ").strip()
        base_url = custom_url if custom_url else default_url

    # API Key
    env_val = os.environ.get(provider.get("env_key", ""), "")
    if env_val:
        use_env = input(f"Found {provider['env_key']} in environment. Use it? [Y/n]: ").strip().lower()
        if use_env != "n":
            api_key = env_val
        else:
            api_key = input("Enter API key: ").strip()
    else:
        api_key = input("Enter API key: ").strip()

    # Models
    if choice == "5":
        model_chat = input("Enter chat model name: ").strip()
        model_reason = input("Enter reasoning model name (or same as chat): ").strip() or model_chat
    else:
        default_chat = provider["models"]["chat"]
        default_reason = provider["models"]["reason"]
        print(f"\nDefault models - Chat: {default_chat}, Reasoning: {default_reason}")
        custom = input("Use defaults? [Y/n]: ").strip().lower()
        if custom == "n":
            model_chat = input(f"Chat model [{default_chat}]: ").strip() or default_chat
            model_reason = input(f"Reasoning model [{default_reason}]: ").strip() or default_reason
        else:
            model_chat = default_chat
            model_reason = default_reason

    config = {
        "provider": provider["name"],
        "base_url": base_url,
        "api_key": api_key,
        "model_chat": model_chat,
        "model_reason": model_reason,
    }

    # Save to CWD
    save_path = CWD / ".debate_config.json"
    save_path.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    print(f"\nConfig saved to {save_path}")
    print(f"  Provider: {config['provider']}")
    print(f"  Base URL: {config['base_url']}")
    print(f"  Chat Model: {config['model_chat']}")
    print(f"  Reason Model: {config['model_reason']}")
    print(f"  API Key: {config['api_key'][:8]}...{config['api_key'][-4:]}")
    print()
    return config


def load_config() -> dict:
    """Load saved config or run setup."""
    config_path = _find_config_path()
    if config_path:
        config = json.loads(config_path.read_text())
        print(f"[Config] Loaded from {config_path}")
        print(f"  Provider: {config['provider']} | "
              f"Chat: {config['model_chat']} | "
              f"Reason: {config['model_reason']}")
        reconfig = input("Re-configure? [y/N]: ").strip().lower()
        if reconfig == "y":
            return setup_config()
        return config
    return setup_config()


# ---------- LLM Calls ----------

def make_client(config: dict) -> OpenAI:
    return OpenAI(api_key=config["api_key"], base_url=config["base_url"])


def call_llm(client: OpenAI, system: str, user_msg: str,
             model: str, temperature: float = 0.7) -> str:
    """Call LLM with retry logic."""
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=4096,
                temperature=temperature,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            if attempt < 2:
                wait = 2 ** (attempt + 1)
                log_print(f"  [Retry {attempt+1}/3] Error: {e}, waiting {wait}s...")
                time.sleep(wait)
                continue
            return f"[ERROR after 3 retries: {e}]"


def call_parallel(client: OpenAI, tasks: list[dict]) -> list[str]:
    """Run multiple LLM calls in parallel."""
    results = [None] * len(tasks)

    def _run(idx, task):
        results[idx] = call_llm(client, **task)

    with ThreadPoolExecutor(max_workers=min(len(tasks), 4)) as pool:
        futs = [pool.submit(_run, i, t) for i, t in enumerate(tasks)]
        for f in futs:
            f.result()
    return results


# ---------- Output ----------

_output_parts = []

def log_print(text: str):
    """Print with immediate flush and collect output."""
    print(text, flush=True)
    _output_parts.append(text)


# ---------- Agent Definitions ----------

AGENT_SYSTEMS = {
    "optimist": (
        "You are the Opportunity Analyst in a structured multi-agent debate. "
        "Analyze for FEASIBILITY, market opportunities, success precedents, positive factors. "
        "Cite real-world examples and data. Rate each claim: Confidence High/Medium/Low. "
        "Be honest. Output structured markdown in Chinese."
    ),
    "critic": (
        "You are the Risk Analyst in a structured multi-agent debate. "
        "Analyze for RISKS, competitive threats, failures, regulatory challenges. "
        "Cite real-world failures and data. Rate each claim: Confidence High/Medium/Low. "
        "Be fair. Output structured markdown in Chinese."
    ),
    "researcher": (
        "You are the Deep Researcher in a structured multi-agent debate. "
        "Gather comprehensive data: market size, players, tech landscape, regulations, "
        "user trends, business models, unit economics. "
        "Provide specific numbers. Output structured markdown in Chinese."
    ),
    "verifier": (
        "You are the Logic Arbiter in a structured multi-agent debate. "
        "Check logical consistency, identify contradictions, flag unsupported claims. "
        "Issue clear rulings on each disagreement. Be impartial. Output in Chinese."
    ),
}


# ---------- Debate Engine ----------

def run_debate(idea: str, config: dict) -> str:
    """Execute the full multi-agent debate."""
    global _output_parts
    _output_parts = []

    llm = make_client(config)
    mc = config["model_chat"]
    mr = config["model_reason"]

    log_print(f"\n{'='*70}")
    log_print(f"  MULTI-AGENT DEBATE SYSTEM")
    log_print(f"  Topic: {idea}")
    log_print(f"  Provider: {config['provider']} | Chat: {mc} | Reason: {mr}")
    log_print(f"{'='*70}\n")

    # ===== ROUND 1 =====
    log_print(f"{'='*70}")
    log_print("  ROUND 1: Independent Analysis (3 agents in parallel)")
    log_print(f"{'='*70}\n")

    r1_prompt = (
        f"Thoroughly analyze:\n\n**{idea}**\n\n"
        f"Provide structured markdown with:\n"
        f"- Numbered key points with Confidence (High/Medium/Low)\n"
        f"- Specific data, examples, precedents\n"
        f"- 2-3 sentence summary\n"
        f"Write in Chinese."
    )

    log_print("  Launching optimist, critic, researcher in parallel...")
    t0 = time.time()

    r1 = call_parallel(llm, [
        {"system": AGENT_SYSTEMS["optimist"],   "user_msg": r1_prompt, "model": mc},
        {"system": AGENT_SYSTEMS["critic"],     "user_msg": r1_prompt, "model": mc},
        {"system": AGENT_SYSTEMS["researcher"], "user_msg": r1_prompt, "model": mc},
    ])
    optimist_r1, critic_r1, researcher_r1 = r1

    log_print(f"  Round 1 complete ({time.time()-t0:.1f}s)\n")
    log_print(f"\n--- Optimist (Opportunity Analyst) ---\n")
    log_print(optimist_r1)
    log_print(f"\n--- Critic (Risk Analyst) ---\n")
    log_print(critic_r1)
    log_print(f"\n--- Researcher (Evidence Gatherer) ---\n")
    log_print(researcher_r1)

    # ===== ROUND 2 =====
    log_print(f"\n{'='*70}")
    log_print("  ROUND 2: Cross-Examination")
    log_print(f"{'='*70}\n")

    log_print("  Identifying disagreement points...")
    t0 = time.time()

    disagreements = call_llm(llm,
        system="You are a neutral debate moderator. Extract core disagreements clearly.",
        user_msg=(
            f"Three analyses of **{idea}**:\n\n"
            f"## Optimist:\n{optimist_r1}\n\n"
            f"## Critic:\n{critic_r1}\n\n"
            f"## Researcher:\n{researcher_r1}\n\n"
            f"Identify TOP 3-5 core DISAGREEMENTS between optimist and critic. "
            f"Numbered list. Chinese."
        ),
        model=mc, temperature=0.3,
    )
    log_print(f"\n--- Core Disagreements ---\n")
    log_print(disagreements)

    log_print("\n  Cross-examination: agents responding in parallel...")
    r2 = call_parallel(llm, [
        {
            "system": AGENT_SYSTEMS["optimist"],
            "user_msg": (
                f"Critic challenged **{idea}**:\n\n{critic_r1}\n\n"
                f"Disagreements:\n{disagreements}\n\n"
                f"Respond with evidence. Acknowledge valid points. Chinese."
            ),
            "model": mc,
        },
        {
            "system": AGENT_SYSTEMS["critic"],
            "user_msg": (
                f"Optimist argued for **{idea}**:\n\n{optimist_r1}\n\n"
                f"Disagreements:\n{disagreements}\n\n"
                f"Respond to each claim. Acknowledge valid points. Chinese."
            ),
            "model": mc,
        },
        {
            "system": AGENT_SYSTEMS["researcher"],
            "user_msg": (
                f"Debate on **{idea}**:\n\nDisagreements:\n{disagreements}\n\n"
                f"Provide additional data to resolve each. Chinese."
            ),
            "model": mc,
        },
    ])
    opt_r2, crt_r2, res_r2 = r2

    log_print(f"\n--- Optimist Response ---\n")
    log_print(opt_r2)
    log_print(f"\n--- Critic Response ---\n")
    log_print(crt_r2)
    log_print(f"\n--- Researcher Fact-Check ---\n")
    log_print(res_r2)

    # Verifier
    log_print(f"\n  Verifier analyzing (reasoning model: {mr})...")
    verifier_out = call_llm(llm,
        system=AGENT_SYSTEMS["verifier"],
        user_msg=(
            f"Full debate on **{idea}**:\n\n"
            f"## Optimist R1:\n{optimist_r1}\n\n"
            f"## Critic R1:\n{critic_r1}\n\n"
            f"## Disagreements:\n{disagreements}\n\n"
            f"## Optimist R2:\n{opt_r2}\n\n"
            f"## Critic R2:\n{crt_r2}\n\n"
            f"## Researcher:\n{res_r2}\n\n"
            f"Rule on each disagreement. Flag fallacies. Chinese."
        ),
        model=mr, temperature=0.2,
    )
    log_print(f"\n--- Verifier Rulings ---\n")
    log_print(verifier_out)
    log_print(f"  Round 2 complete ({time.time()-t0:.1f}s)\n")

    # ===== ROUND 3 CHECK =====
    need_r3 = call_llm(llm,
        system="Answer ONLY YES or NO.",
        user_msg=f"Are there >2 major unresolved disagreements?\n\n{verifier_out}\n\nYES or NO:",
        model=mc, temperature=0.0,
    ).strip().upper()

    rounds = 2

    if "YES" in need_r3:
        log_print(f"\n{'='*70}")
        log_print("  ROUND 3: Deep Focused Debate")
        log_print(f"{'='*70}\n")
        t0 = time.time()

        r3 = call_parallel(llm, [
            {"system": AGENT_SYSTEMS["optimist"],
             "user_msg": f"Verifier rulings on **{idea}**:\n\n{verifier_out}\n\nFinal arguments on unresolved issues. Chinese.",
             "model": mc},
            {"system": AGENT_SYSTEMS["critic"],
             "user_msg": f"Verifier rulings on **{idea}**:\n\n{verifier_out}\n\nFinal arguments on unresolved issues. Chinese.",
             "model": mc},
        ])

        log_print(f"\n--- Optimist Final ---\n")
        log_print(r3[0])
        log_print(f"\n--- Critic Final ---\n")
        log_print(r3[1])

        log_print(f"\n  Final verification (reasoning model)...")
        verifier_out = call_llm(llm,
            system=AGENT_SYSTEMS["verifier"],
            user_msg=(
                f"FINAL rulings on **{idea}**:\n\n"
                f"Optimist:\n{r3[0]}\n\nCritic:\n{r3[1]}\n\n"
                f"Previous:\n{verifier_out}\n\nDefinitive ruling. Chinese."
            ),
            model=mr, temperature=0.2,
        )
        log_print(f"\n--- Final Rulings ---\n")
        log_print(verifier_out)
        log_print(f"  Round 3 complete ({time.time()-t0:.1f}s)\n")
        rounds = 3
    else:
        log_print("\n  [Disagreements resolved in R2, skipping R3]")

    # ===== SYNTHESIS =====
    log_print(f"\n{'='*70}")
    log_print("  FINAL SYNTHESIS")
    log_print(f"{'='*70}\n")
    t0 = time.time()

    synthesis = call_llm(llm,
        system="You are the Chief Analyst. Produce a comprehensive, balanced, actionable report.",
        user_msg=(
            f"FINAL REPORT for **{idea}**:\n\n"
            f"Optimist R1:\n{optimist_r1}\n\n"
            f"Critic R1:\n{critic_r1}\n\n"
            f"Researcher:\n{researcher_r1}\n\n"
            f"Cross-exam: Opt={opt_r2}\nCrit={crt_r2}\nFacts={res_r2}\n\n"
            f"Verifier:\n{verifier_out}\n\n"
            f"Rounds: {rounds}\n\n"
            f"Output in Chinese:\n\n"
            f"# 辩论结论: [Topic]\n"
            f"## 核心建议\n## 共识点\n"
            f"## 分歧点及裁定 (table)\n"
            f"## 关键数据与证据\n"
            f"## 风险评估 (table)\n"
            f"## 行动计划\n"
            f"## 辩论元数据"
        ),
        model=mr, temperature=0.3,
    )

    log_print(synthesis)
    log_print(f"\n  Synthesis complete ({time.time()-t0:.1f}s)")
    log_print(f"\n{'='*70}")
    log_print("  DEBATE COMPLETE")
    log_print(f"{'='*70}\n")

    # Save full output to CWD
    out_path = CWD / "debate_output.md"
    out_path.write_text("\n".join(_output_parts), encoding="utf-8")
    log_print(f"  Full output saved to: {out_path}\n")

    return "\n".join(_output_parts)


# ---------- Entry ----------

def main():
    # Parse args
    args = sys.argv[1:]
    force_setup = False
    if "--setup" in args:
        force_setup = True
        args.remove("--setup")

    idea = " ".join(args).strip() if args else ""

    print("=" * 60, flush=True)
    print("  Multi-Agent Debate System", flush=True)
    print("  Supports: DeepSeek / OpenAI / Claude / MiniMax / Custom", flush=True)
    print("=" * 60, flush=True)

    # Config resolution order:
    # 1. --setup flag → interactive setup
    # 2. Environment variables → auto-detect
    # 3. .debate_config.json → load saved config
    # 4. Fallback → interactive setup
    if force_setup:
        config = setup_config()
    else:
        config = auto_detect_config()
        if config is None:
            config_path = _find_config_path()
            if config_path:
                config = json.loads(config_path.read_text())
                print(f"[Config] Loaded from {config_path}")
                print(f"  Provider: {config['provider']} | "
                      f"Chat: {config['model_chat']} | "
                      f"Reason: {config['model_reason']}")
            else:
                config = setup_config()

    # Get idea
    if not idea:
        print()
        idea = input("Enter your idea or question:\n> ").strip()
        if not idea:
            print("No input. Exiting.")
            return

    run_debate(idea, config)


if __name__ == "__main__":
    main()
