# Reviewer 1 Analyzer Card — FR-028

## Verdict

**Binary verdict:** sound

**One-line justification:** The status-only injection is placed after hard-failure short-circuit and before recipe normalization/salvage, copies rather than mutates shared args, preserves golden parity in the tested success path, and the full swarm suite passes.

## Finding 1

- **claim:** Non-functional documentation drift remains in the parity gate comments: the `salvage-promoted` scenario still says `normalize_wave2` forwards shared `recipe_args` without per-worker status and that CLI salvage promotion is not exercised because status injection is absent. That statement is now stale because `_normalize_one` injects `worker.status` before calling the recipe. This does not invalidate runtime correctness because the scenario still deliberately drives three success reviewers and the byte-equality gate passes, but it can mislead future maintainers about FR-028 coverage.
- **file:line:** `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_bare_review_parity.py:181` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_bare_review_parity.py:208`; contradicted by `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:439` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:451`.
- **severity:** low
- **grounding:** grounded

## Evidence checks requested

### 1. Placement correctness

- Hard failures still return before status injection: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:424` checks `timeout`/`proxy_error`, emits sidecar, and `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:435` returns.
- Status injection occurs only after the hard-failure branch and raw-body read: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:437` reads raw, `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:448` creates `{**args, "status": worker.status}`.
- Injection is before recipe normalization: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:450` starts the `try`, and `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:451` calls `recipe.normalize(raw, args)`.
- Salvage path is after recipe normalization: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:481` calls `salvage_decision`, and `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:486` calls `salvage_parse_error`.
- Promotion conditions are correct: `salvage_decision` requires `worker_result.status == "parse_error"` at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:163`, `normalized.salvaged` at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:175`, and non-empty text at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:181`; success replacement happens at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:230` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:233`.
- `BareReviewV1.normalize` reads `status = str(args.get("status", "success"))` at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:249`, sets `salvaged = True` for recoverable `parse_error` bodies at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:277` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:286`, and returns that flag with rendered text at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:308` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:309`.

### 2. Determinism claim

- For a success worker, the injected status is `"success"`, matching `BareReviewV1`'s prior default at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:249`.
- `status` is only used as a branch condition; it is not rendered into the frontmatter/body. The rendered frontmatter fields are built at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:293` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:307` and do not include `status`.
- The frozen-golden parity test compares sorted normalized CLI bodies to sorted golden bodies at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_bare_review_parity.py:326` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_bare_review_parity.py:333`.
- Raw test result: `uv run pytest tests/swarm/test_bare_review_parity.py -q` collected 16 items and reported `16 passed in 0.38s`.

### 3. Shared-dict mutation

- The injected dict is a new shallow copy at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/normalize.py:448`, so the shared caller dict is not mutated by adding `status`.
- Regression coverage asserts the original shared args remain without `status`: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_recipe_bare_review.py:346` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/tests/swarm/test_recipe_bare_review.py:361`.

### 4. Recipe contract and other recipes

- `BareReviewV1.normalize` assumes the fix exactly as intended by reading `args.get("status", "success")` at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:249` and gating parse-error salvage at `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:278` through `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/bare_review_v1.py:286`.
- Other built-in recipes found by `rg` also use the same defaulted `args.get("status", "success")` pattern: `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/findings_table_v1.py:296`, `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/hypothesis_table_v1.py:362`, and `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028/src/superclaude/cli/swarm/recipes/verdict_only_v1.py:406`. No divergent built-in status-reading contract was found.

## Test execution

- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028`: `uv run pytest tests/swarm/test_bare_review_parity.py -q` → **16 passed**.
- `/config/workspace/IronClaude/.claude/worktrees/fr028-fr028`: `uv run pytest tests/swarm/ -q` → **2215 passed, 27 skipped**.

## Deviation classification

- **Overall classification:** authorized + necessary.
- **Rationale:** The change is the explicitly user-authorized FR-028 remediation and is narrowly scoped to thread only per-worker `status`. No functional regression found. The only issue identified is low-severity test-comment drift in the parity gate, not runtime behavior.

## Calibrated confidence

- **citation grounding:** 0.95
- **coverage:** 0.92
- **deviation-classification clarity:** 0.94
- **risk-surface coverage:** 0.90
- **recommendation actionability:** 0.88
- **overall calibrated confidence:** 0.92
