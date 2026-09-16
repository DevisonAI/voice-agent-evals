# voice-agent-evals

Tiny golden-case harness for Voice-AI / agent behavior.

## Verify

```bash
python3 -m src.eval_runner cases/
# or: make eval
```

Expect `15/15 passed`. No API keys for the seed runner (deterministic stubs).

## Cases

15 golden JSON files under `cases/` — each has `id`, `input`, `expect` (substring or rule).
