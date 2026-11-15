# Import time of `superclaude.cli.review.findings` (step 0.5, measured 2026-11-14)

Command, five times, wall clock around the whole process: `uv run --frozen --project <repo> python -c "import superclaude.cli.review.findings"` (with `PYTHONDONTWRITEBYTECODE=1`).

| Run | Seconds |
|---|---|
| 1 | 0.283 |
| 2 | 0.295 |
| 3 | 0.271 |
| 4 | 0.272 |
| 5 | 0.279 |
| **Median** | **0.279** |

The number includes `uv run` start-up and interpreter start. `RL/DESIGN.md` 10.1 uses it for the row-check time budget: the row check itself is timed excluding interpreter start (the Task 9 test), and the per-panel overhead of one interpreter start is about 0.28 s. The sibling measured 0.28 s once; this build agrees.
