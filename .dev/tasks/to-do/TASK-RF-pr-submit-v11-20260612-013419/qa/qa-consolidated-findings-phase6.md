# Phase 6 — Consolidated QA Findings (M3 lens gate)

7 lens agents ran (3 structural + 3 content + 1 domain). (First batch: 2 returned, 5 hit
transient socket errors → re-spawned; all 7 reports on disk.)

| Lens | Verdict |
|---|---|
| template-conformance | PASS |
| internal-consistency / parity | PASS |
| completeness | PASS |
| domain-accuracy | FAIL (3 MINOR naming nits) |
| actionability | PASS (4 MINOR; 1 real F-1) |
| crossref-chain | FAIL (5; 2 IMPORTANT — T-1115 weakness) |
| core-purity / fork-pin | PASS |

## TOP-LINE VERDICT: FAIL → targeted fixes (the core-purity boundary + completeness + parity all PASS)

## Deduplicated findings + disposition

| # | Finding (lens) | Severity | Disposition |
|---|---|---|---|
| F1 | **T-1115 flag-parity is a loose substring test** (crossref F1/F2): `"quick" in cmd` doesn't bind `quick` to `--depth`; `claude-sonnet-4-6` only appears in auggie-review.md as a parenthetical example. | IMPORTANT (test quality) | **FIX** — strengthen T-1115 to assert each flag is a REAL option-table row (`| --depth |`, `| --remediation-offer |`, `| --auggie-model |`) in auggie-review.md, and that the model is the documented `--auggie-model` example. |
| F2 | **retrigger-review.sh: bare `--pr` with no value exits 1 not 2** under `set -u` (`shift 2` fails before the guard) (actionability F-1). | MINOR (real, unreachable via SKILL contract) | **FIX** — guard `[ $# -ge 2 ]` before `shift 2` so a missing value exits 2 (usage). |
| F3 | **Clamp naming drift:** SKILL.md says "clamp the budget to max_rounds=1"; the ref says `effective_max_rounds := min(., 1)` (domain I-1). | MINOR | **FIX (clarity)** — align SKILL.md Wave 6b to name `effective_max_rounds`. |
| F4 | clamp helper `clamp_max_rounds` vs event `max_rounds_clamped` pairing not stated (domain I-2) | MINOR | **NO-FIX (documented)** — different artifacts (a pure helper vs a run-log event); both are correctly named per the core. Adding a cross-note is optional; loop-guard.md already explains the monotone-min fold. |
| F5 | review-retrigger.md prose flips augment review ↔ auggie review (domain I-3) | MINOR | **NO-FIX (documented)** — accurate: the App ACCEPTS augment/auggie/augmentcode review; we POST `auggie review`. The ref already states both correctly. |
| F6 | exit 0/1/2 vs "documented 0/2" (actionability F-2) | INFO | **NO-FIX** — the script HEADER already documents all three ("0 on a completed post; 2 on usage error; 1 on a failed post"). Accurate; the task's "0/2" was success+usage. |
| F7 | crossref F3 (no positive --post-pr test), F4 (T-N50 regex narrower than prose), F5 (declined→S5b prose-only in this ref) | MINOR/LOW | **NO-FIX (documented)** — F3: the negative guard (no --no-post-pr in invocation) is the load-bearing one. F4: `gh|git` is the operational core-purity definition (T-N50). F5: declined→S5b is tested in fsm via `test_transition_v11_edges` (Phase 5). |

## ACTIONABLE FIXES (executor as single I20 writer, Step 6.G6)
- F1: strengthen T-1115 (option-table binding) — test_static_grep.py.
- F2: harden retrigger-review.sh `--pr` arg guard.
- F3: SKILL.md Wave 6b clamp wording → effective_max_rounds.
After any `src/superclaude/skills` touch, re-run `make sync-dev` + verify the mirror; NEVER stage `.claude/`.
