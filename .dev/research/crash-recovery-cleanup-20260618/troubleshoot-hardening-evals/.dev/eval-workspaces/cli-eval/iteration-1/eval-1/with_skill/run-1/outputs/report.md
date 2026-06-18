# eval_smoke run — outcome report

## Selection (via CLI, not a dir scrape)
- `uv run superclaude eval list --json` → exit 0; eval_smoke present (v1.0, 3 evals).
- `uv run superclaude eval describe --suite eval_smoke` → exit 0; ES1/ES2/ES3, each `no_pty: skip`, ephemeral HOME.
- Non-interactive: menu I would have shown = A (--no-pty CI-canary skip), B (real run under FR-G5 empty-HOME workaround, DEFAULT), C (show gate fire, then B). Chose C then B.

## Gotchas surfaced
1. FR-G5 coverage gate (exit 2): host has /config/.claude/settings.json; eval_smoke covers none of its matchers.
   `uv run superclaude eval run --suite eval_smoke --no-mcp --json` → exit 2:
     coverage gate FAILED — uncovered: PostToolUse mcp__auggie__.* (and 2 wider variants).
   Exit 2 = harness/usage gate, NOT an eval failure, NOT a pass.
   Workaround (empty HOME = no matchers):
     TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run --suite eval_smoke --no-mcp --json; rm -rf "$TMPHOME"  → exit 0
2. --no-pty → SKIPPED: all 3 evals are no_pty:skip, so --no-pty short-circuits the whole suite to SKIPPED (not a pass). Omitted --no-pty; handled FR-G5 via the workaround instead.

## Outcome (parsed from on-disk summary.json — machine truth)
Run-dir: .dev/eval-runs/2026-06-12/134335Z-07aca9f1/   (FR-G4 layout intact: summary.{md,json,yaml} + per-eval/ES{1,2,3}/artifacts/ + empty homes/)
| Eval | Status | Duration | skip_reason | error_class |
| ES1  | PASS   | 0.0s     | -           | -           |
| ES2  | PASS   | 0.0s     | -           | -           |
| ES3  | PASS   | 0.0s     | -           | -           |
counts: manifest_n=3, expanded_n_prime=3, kept_k=3, skipped_s=0 (invariant holds)
totals: 3 passed / 0 failed / 0 skipped / 0 errored / 0 interrupted / 0 timeout
Process exit code: 0 (clean). Preserved failed-HOME paths: NONE (no non-PASS eval; homes/ empty, expected for all-PASS without --keep-home).

## Honesty caveat — NOT an authoritative pass
Production PTY executor lands at M5/M6 and is NOT on disk. Current harness uses _NullLifecycleExecutor (canned exit 0), so the 3 PASSes are the plumbing path, not real eval execution. A --verbose re-run surfaced:
  eval run: WARNING: _NullLifecycleExecutor active — run results MUST NOT be treated as authoritative.
(--json suppresses that warning by design; re-ran --verbose specifically to surface it.)

## Bottom line
Selected via CLI; supervised across 3 bounded runs. FR-G5 fired (exit 2) as predicted; empty-HOME workaround cleared it (exit 0). summary.json = 3/3 PASS, exit 0 — a clean harness/plumbing run, NOT yet an authoritative eval pass (needs M5/M6 PTY executor). All-SKIPPED --no-pty path is likewise not a pass.

## Run-dirs created
- .dev/eval-runs/2026-06-12/134326Z-1d7a5f28/  — FR-G5 abort (no summary)
- .dev/eval-runs/2026-06-12/134335Z-07aca9f1/  — workaround run (--json); summary present
- .dev/eval-runs/2026-06-12/134348Z-3b12db34/  — workaround run (--verbose); summary present
