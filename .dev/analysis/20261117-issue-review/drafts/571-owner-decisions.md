## Owner decisions 2026-11-17 and a question for Clay

**Owner decisions (given in chat, recorded here):**
1. Approved: start wave 1 (PRs 1, 2 and 5: the `prd` command-line pipeline, the cleanup-audit runner, and `/sc:spawn`). This is Clay's work to do, not the owner's.
2. The risk from people installing from git is accepted and ignored. It is no longer a reason to route removals through an `integration` branch. Whether to keep `integration` anyway is Clay's call.

**Question for Clay: how reflect uses swarm, and should swarm be removed?**

Read from origin/master. Reflect's Tier-2 review panel (the several-reviewer ensemble) runs on swarm's engine:
- `src/superclaude/cli/reflect/ensemble.py` (lines 41-61) imports swarm's `dispatch_wave1` (fan out to reviewer models), `normalize_wave2`, `reduce_wave3` and `emit_done_sentinel` (collect and merge results), `_resolve_run_transport_factory`, the transports (`openai_compat`, `stub`), `preflight`, `config` (`T1_MODEL_MAX_SLOTS`), the `reflect_review` lens, and the shared models. Its own docstring says the Tier-2 path "invokes the swarm run surface".
- `src/superclaude/cli/reflect/fallback.py` (lines 15-28) imports `ModelPoolTooSmallError`, `dispatch_wave1`, `normalize_wave2`, `preflight` and the transports for the fallback ladder.
- `src/superclaude/cli/reflect/_diversity.py:5` imports `WorkerResult`.
- Also: `src/superclaude/cli/issue_watch/record.py` (lines 372, 853) uses `swarm.atomic.write_prepared_bytes`, and `src/superclaude/cli/sprint/aienv.py:35` uses `swarm.config` (goes away with sprint, PR 11).

**Recommendation:** remove the swarm surface, but not before the engine is moved. Removing `cli/swarm` as one block would break the reflect review panel that PRs #519 and #581 just built and measured. So keep PR 3 split as the plan says: 3a moves what reflect and issue_watch need (dispatch, transports, normalize, reduce, preflight, models, config, atomic, the `reflect_review` lens) into reflect or a shared module, with the reflect and issue_watch tests passing; 3b then removes the rest (`swarm run` command, `/sc:swarm-wizard`, `sc-bare-review`, the other lenses and recipes, tmux, tui, `docs/swarm`).

**UNVERIFIED:** whether any kept skill uses the other lenses (for example `troubleshoot_hypothesis`); Clay to check in 3a. I did not run any tests.

Clay, please confirm or change this.

Posted by Claude Code on the owner's instruction, 2026-11-17.
