# Resume handoff: interrupted post-execution reflection

Written 2026-10-20 after the run stopped on context limits. Verified from disk, not from memory.

## Paste this into a new session (run from the worktree)

Working directory: `/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP` (branch `CodebaseMemoryMCP`).

```text
/sc:reflect --mode post --tasklist .dev/tasks/done/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md --task-log .dev/tasks/done/TASK-WF-spec-20261019-204314/progress.md --output .dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/reflect/post-20261020042605 --no-promote

RESUME, DO NOT RESTART. This is the continuation of an interrupted run whose Waves 0-4 already completed in the --output directory above. Read RESUME-HANDOFF.md in that directory first and follow it. Reuse that exact directory (do not create a -N suffix copy); append a "resume" row to its audit.log. Do not redo Waves 0-4 unless the input drift check fails. Finish Wave 4's exit check, then Wave 5 (drift recheck, synthesis, mandatory evidence-validator gate, REPORT.md, return-contract.yaml, metrics). Skip Wave 6 (no --remediate). Wave 7 is not applicable: the package is already archived in done/, so record promotion_action: not-applicable and move nothing. No product edits, no tests via Bash in place of the unavailable verification tool, no real upstream install/uninstall, no git staging/commit/push.
```

## What already exists on disk (all under this directory)

| Wave | State | Evidence |
|---|---|---|
| 0 Parse/probe | Done. Aliases: opus `claude-opus-5-5[1m]`, sonnet `claude-sonnet-5-5[1m]`, haiku `grok-4.7[1m]`. Executor class unknown. Serena `get_current_config`, `activate_project`, `execute_shell_command` not exposed, so the verification triangle is unavailable. | `audit.log` rows wave 0 |
| 0.4 Input snapshot | Done. `input_tree_sha256 = 5142787cf9e3e33e4e620174502e566ec7a4b8a4477f595d2e9fcd28939e6bb6`. Baseline tree is the first task start `ddd1f9a31dceab5b73187dcdb68de1d1bbec6424`. | `artifacts/input-snapshot.yaml`, `artifacts/review-context.json` |
| 1 Tier 1 | Done. Tier 1 card, blind calibration C = 0.73. Cross-task interaction scan, runtime-surface sweep (two Click command callbacks DEGRADE, nothing UNREACHED), reuse audit (no rung-L3 duplicate). Verification skipped (tool not exposed). | `artifacts/tier1-card.md`, `artifacts/tier1-calibration.json`, `artifacts/interaction-effects.yaml`, `artifacts/runtime-surface-ledger.yaml`, `artifacts/reuse-audit.yaml`, `verify-logs/invocations.yaml` |
| 2 Tier decision | Done. Tier 2, rule 3 (regression candidates need debate). | `artifacts/tier_decision.yaml` |
| 3 Reviewers | Done. Three restricted reviewers plus independent blind calibrations: 0.71, 0.78, 0.80 (mean 0.763). Calibrator class collides with one reviewer: `calibrator_diversity: degraded`. | `reviewer-briefs/`, `reviewer-cards/*-calibrated.md`, `artifacts/calibration-summary.json` |
| 4 Adversarial merge | Done on disk, but NOT yet logged. `merge_method: adversarial`, convergence 1.0, adversarial status `partial`. | `adversarial/merged-verdict.yaml`, `adversarial/merged-verdict.md`, `adversarial/return-contract.yaml`, `adversarial/adversarial/*` |
| 5-7 | NOT STARTED. No top-level `REPORT.md`, `return-contract.yaml`, `deviation-ledger.yaml`, `metrics.json`, or evidence-validator output. | none |

A post-interruption check found no delivery or package file modified after the snapshot (mtime check). The protocol still requires the hash recheck below.

## Merged findings to carry into the report (from `adversarial/merged-verdict.yaml`)

Re-read each cited line before quoting; these are pointers, not verified quotes.

- **D1 Drift, LOW-MEDIUM (confidence 0.57, one dissent says Regression-LOW).** Menu option `0` (install all individual servers) at project/local scope or on non-Linux rejects the whole selection instead of visibly skipping only Codebase Memory. Source anchors `install_mcp.py:1284-1285`, `:1311-1314`, `:486-496`; spec `source.md:67,78,80,143,144`. No option-0 project/Darwin test.
- **D1-explicit, Necessary deviation (unanimous).** Explicit native-plus-other selections at those scopes/platforms are rejected before effects.
- **D2 Drift, conditional (0.60).** A group-writable canonical directory (for example `~/.local/bin` at mode 0775 under umask 002) makes native discovery/proof fail closed, which can block install or automatic removal. Depends on unobserved host modes; no umask fixture. Anchors `install_codebase_memory.py:85-116`, `:545-552`, `:682-700`.
- **D3 Drift, LOW, conditional on a symlinked HOME.** The fail-closed error omits the offending path. Anchors `install_codebase_memory.py:54-55`, `:539-544`; `install_mcp.py:572-579`.
- **D4 Drift candidate, LOW, interpretation open (0.55).** `mcp --list` rejects `--dry-run`/`--scope` combinations; arguably stricter than `source.md:76,117`. Anchor `main.py:326-330`.
- **D5 Authorized expansion (0.88).** Linux-only automation, authorized by `../../operator-direction.md:5-7`; macOS framework install exits 1 (`main.py:255-275`).
- **Advisories (not deviations):** `claude --version` runs twice on the user/Linux path; restore via `add-json` passes the prior entry, which may contain secret values, on the process argument list; `AcquisitionResult.acquired` used only in tests; mocked fixture proves dispatch only; two LOW documentation clarity notes (option 0 limits, group-writable proof rule).
- **Open medium invariant items:** INV-002 (D2 reachability) and INV-005 (live-smoke gate `source.md:151` unanchored by any task AC). Carry as evidence gaps.

No Regression was established. `deviation_count_by_class` expected: drift 3 confirmed plus 1 candidate (decide D4 by evidence; if left open, route it to `grounding-gaps.yaml`, not the ledger), necessary 1, authorized 1, regression 0.

## Remaining steps in order

1. **Resume row.** Append one `audit.log` row: `wave 5, step "resume"`, naming this handoff file.
2. **Wave 4 exit check (EV-1).** Confirm on disk that `adversarial/merged-verdict.yaml` has `merge_method: adversarial` and `reviewer-cards/` holds 3 calibrated cards. Append the missing wave 4 audit row. Record `adversarial_artifacts_dir` from the producer's `artifacts_dir` field (consumer-side rename).
3. **Drift recheck.** From the worktree root run:
   `PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/config/workspace/IronClaude/.venv uv run --active --no-sync python .dev/tasks/done/TASK-WF-spec-20261019-204314/artifacts/reflect/post-20261020042605/artifacts/review_inputs.py --recheck`
   It writes `artifacts/input-recheck.yaml` and an audit row; exit 1 means drift. On drift: STOP, `status: partial`, `input_drift_detected: true`, report both hashes.
4. **Synthesis.** Write `deviation-ledger.yaml` (4-category taxonomy only) and extend `grounding-gaps.yaml` (existing two rows: missing fresh verification; dynamic Click reachability) with INV-002, INV-005, and D4 if unresolved.
5. **Evidence-validator gate (mandatory).** Draft `REPORT.md` from `/config/.claude/skills/sc-reflect-protocol/refs/report-template.md`, re-Read every cited `file:line`, then hand it to the `evidence-validator` agent. Drop unfounded citations; never ship without this gate.
6. **Contracts.** Write `return-contract.yaml` at `contract_version: "1.7.0"` per SKILL.md §9.1, including the mandatory UC-2 `reachability_*` block, all six `runtime_surface_*` fields (degrade-only run: `runtime_surface_degraded: true`, `runtime_surface_unreached: 0`, `unreached_surfaces: []`), reuse fields, `merge_method: adversarial`, `t2_model_class_diversity: full`, `calibrator_diversity: degraded`, `executor_class_resolved: false`, `verification_ran: false` with `verification_skip_reason: tool-unavailable`, `promotion_action: not-applicable`. Expect `status: partial` and `needs_human_decision: true` because grounding gaps are non-empty. Also write `metrics.json` and append one line to `.dev/reflect/runs.jsonl`.
7. **Memory.** Earlier Serena memory hydrate pointed at the main checkout, not this worktree. Do not write project memory from the wrong root; record `memory_persist_failed: true` with that reason.
8. **Report back.** Status, report path, deviation counts, evidence-validator drop count, and that Wave 7 moved nothing.

## Hard boundaries

- Read-only for product code and docs. Write only inside this output directory (plus the single `runs.jsonl` append).
- Do not move or rewrite the archived package or its `progress.md`. The archive helper owns package location.
- No real upstream installer, native uninstall, Claude MCP mutation, or developer-config change. The isolated live smoke remains a separate, unexecuted release gate.
- No git staging, commit, push, or PR. All delivery changes are still uncommitted on branch `CodebaseMemoryMCP`.
