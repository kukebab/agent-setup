# Cost-Aware LLM Pipeline

Patterns for controlling LLM API costs. Model routing, retry, prompt caching. Stack-agnostic — works with any provider (Anthropic, OpenAI, Google, gateway services, etc.).

## Model Routing by Complexity

Most workloads have a long tail of simple tasks (classification, parsing, routing) that don't need a frontier model. Route accordingly:

```python
def select_model(text_length: int, item_count: int = 1, task: str = "general") -> str:
    """Route to the cheapest adequate model."""
    if task in ("intent_parsing", "classification", "routing"):
        return "small"      # Haiku-tier, GPT-mini-tier, Gemini Flash-tier
    if task == "html_generation":
        return "specialized"  # cheap models trained for HTML/code
    if text_length >= 10_000 or item_count >= 30:
        return "frontier"   # Sonnet, GPT, Opus, Gemini Pro
    return "small"          # default — cheapest first
```

The **inversion of intuition**: most production workloads should default to the cheapest model and escalate only when complexity demands it. People over-use frontier models out of habit.

## Retry Logic

```python
import time

_RETRYABLE = (ConnectionError, RateLimitError, ServerError)

def call_with_retry(func, max_retries: int = 3):
    """Retry only transient errors. Fail fast on auth/validation."""
    for attempt in range(max_retries):
        try:
            return func()
        except _RETRYABLE:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # exponential backoff
```

**Don't retry:** auth errors, validation errors, content policy errors. Wasted money.
**Do retry:** rate limits, connection errors, 5xx server errors. Transient.

## Prompt Caching

Most providers support cached system prompts (Anthropic, OpenAI). For repeated calls with a long system prompt, this can cut input cost ~90%.

```python
# Anthropic-style (works via direct API or any compatible gateway)
messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": LONG_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            },
        ],
    },
    {"role": "user", "content": user_input},
]
```

**When caching matters:** pipelines that hit the same system prompt 100+ times in a session. Examples: batch CV parsing, classification jobs, evaluation suites.

**When it doesn't matter:** one-off interactive sessions where each prompt is different.

## Cost Tracking

Track at the unit level — cost per CV parsed, cost per page generated, cost per email sent. This is the metric that matters at scale, not "monthly LLM bill."

```python
def log_call(model, input_tokens, output_tokens, task):
    cost = (input_tokens * MODEL_COSTS[model]["input"]
          + output_tokens * MODEL_COSTS[model]["output"])
    logger.info(f"{task}: {model} ${cost:.4f}")
    metrics.histogram("llm.cost.per_call", cost, tags={"task": task, "model": model})
```

When unit cost exceeds a threshold (e.g. >$0.05 per unit for high-volume work), it's a red flag. Either the workload doesn't justify LLM, or routing is wrong.

## Pricing Reference (rough order of magnitude as of 2026)

| Tier | Examples | Input ($/1M) | Output ($/1M) |
|------|----------|--------------|---------------|
| Frontier | Claude Sonnet, GPT, Gemini Pro | $3 | $15 |
| Frontier-large | Claude Opus, GPT-large | $15 | $75 |
| Mid | Sonnet older, GPT older | $2 | $10 |
| Small | Haiku, GPT-mini, Gemini Flash | $0.5–1 | $2–4 |
| Specialized | GLM, smaller open models | $0.3–1 | $1–3 |

A single frontier call costs ~6–10x a small-model call. A frontier-large call costs ~15–20x. Use frontier for orchestration and reasoning; small models for everything else.

## Anti-Patterns

- Using the biggest model for everything ("just to be safe")
- Retrying auth errors (waste of money)
- NOT using prompt caching for repeated system prompts
- Hardcoding model IDs everywhere (use constants in one place)
- No observability — you can't optimize what you don't measure
- Checking cost only via the provider's monthly dashboard (per-call instrumentation is what you need)
