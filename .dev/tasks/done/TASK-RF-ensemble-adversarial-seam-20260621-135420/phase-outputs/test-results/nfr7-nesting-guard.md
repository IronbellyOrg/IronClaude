# NFR-7 No-Nesting Guard (Step 3.6)

**Date:** 2026-06-22
**Command:** `uv run pytest tests/cli/reflect/test_no_nesting_guard.py -q`

## Output

```
collected 6 items
tests/cli/reflect/test_no_nesting_guard.py X.....                        [100%]
========================= 5 passed, 1 xpassed in 0.10s =========================
```

## Verdict: PASS

The NFR-7 guard confirms `ensemble.py` still contains the `ClaudeProcess` literal and introduces NONE of the banned tokens (`Task(`, `subagent`, `import anthropic`, `from anthropic`, `subprocess.run(`, `Popen(`, `import subprocess`, `async def`, `await `). The new `AdversarialResult` plain dataclass and the widened functions added no banned tokens. (1 xpassed is the suite's pre-existing expected-pass marker, not a regression.)
