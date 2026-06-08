# QA Report — task-qualitative

**Topic:** Remediate Reflect-V3-Serena UC-2 audit findings (F-1/F-2/G-1/G-2) in sc-reflect-protocol
**Date:** 2026-06-03
**Phase:** task-qualitative
**Fix cycle:** N/A (initial pass; fix_authorization: true → issues fixed in-place)

---

## Overall Verdict: FAIL → all issues FIXED in-place (re-verify by re-running this gate)

Five issues found (1 CRITICAL, 3 IMPORTANT, 1 MINOR). All five were fixed in-place in the task
file per `fix_authorization: true`. Verdict recorded as FAIL because issues existed; re-run this
gate (fix-cycle 1) to confirm clean.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-1 | FAIL→fixed | `markdownlint` NOT on PATH (`command -v markdownlint`=MISSING); bare `markdownlint <file>` in Steps 2.3/3.4/4.2/6.1 → command-not-found → log-and-skip defeats "count ALL rules" convention. `npx markdownlint-cli --version`=0.48.0 works. Fixed: switched to `npx --yes markdownlint-cli`. `make`/`verify-sync`/`uv` present; Step 5.3 one-liner dry-ran `JSON_VALID`. |
| 2 | Project convention compliance | none | PASS | Skill edits target `src/` only; `make verify-sync` PASSES now; sync-dev correctly OMITTED for eval-only Phase 5; F-2 mixed phase (3.4) runs sync-dev for SKILL.md AND JSON-validity for evals.json. Guards=0. |
| 3 | Intra-phase execution simulation | none | PASS | Edit→fixture→validate→gate ordering sound; pre-edit-snapshot dependency (2.1→2.3) consistent. |
| 4 | Embedded current-state strings | none | PASS | Byte-verified vs disk: SKILL.md:230/432, expected.yaml:21, wave0-config:20, evals.json:527, id-22 (609-614), id-24 (718-723) all match. |
| 5 | Module context analysis | none | PASS | C1 predicate L432 = only firing-condition prose; F-2 enum L230 = only `onboarding_status_source` line (L234 not over-matched). |
| 6 | Downstream consumer analysis | AX-3 | FAIL→fixed | F-1 missed `evals.json:805` `text` carrying the OLD inverted predicate. Fixed: added Step 2.2b; grader ignores `text` so eval still grades — IMPORTANT completeness gap. |
| 7 | Test/verification validity | none | PASS | Gates substantive (verify-sync, lint delta, JSON, guard greps, field_path-absent, no-`.claude/`-staged). G-2 swap grader-valid (`check_regex_present` needs only `target`+`pattern`). |
| 8 | Test coverage of criteria | none | PASS | Each finding's spec criterion gated per-phase + final pair. |
| 9 | Error path coverage | none | PASS | Each edit has current-state-mismatch branch; gates have capped fix cycles; final HALTs to Blocked (no auto-default). |
| 10 | Runtime failure path trace | AX-1 | FAIL→fixed | markdownlint baseline `git show HEAD:` invalid — parent task uncommitted (SKILL.md 1661 vs HEAD 1585; HEAD has 0 `onboarding_status_source`, no §6.3). ~76-line spurious delta → SKILL.md gates FAIL → churn. Fixed: pre-edit snapshots in 2.1/3.1/4.1, baseline against them in 2.3/3.4/4.2/6.1. CRITICAL. |
| 11 | Completion scope honesty | none | PASS | Done only if 6.2+6.3 PASS; cap-exhaust→Blocked+blocker_reason, no Done. |
| 12 | Ambient dependency completeness | none | PASS | sync-dev mirrors SKILL/refs; eval files have no mirror (correct); no registry/CLI touchpoints. |
| 13 | Edit sequencing | none | PASS | No kwarg-before-signature; snapshot capture sequenced before the edit it baselines. |
| 14 | Existence claims grep-verified | none | PASS | id-22/24 field_paths present pre-fix; guards=0; contract_version 1.1.0 §9.1 (L545/548); regex_present_count=23 pre-swap. |
| 15 | Cross-ref accuracy / dangerous cmd | AX-2 | FAIL→fixed | Step 2.3 `git stash --keep-index ... pop \|\| true` gratuitous (`git show HEAD:` bypasses worktree) AND dangerous on 22-file dirty tree (3 stash entries; failed pop under `\|\| true` reverts edit). Fixed: removed stash dance. G-1→1.1.0 matches §9.1 — PASS. |

## Summary
- Checks passed: 10 / 15 (5 failed, all FIXED in-place)
- Critical issues: 1 | Important: 3 | Minor: 1
- Issues fixed in-place: 5
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 11 | Bash (grep/dry-run/git): 10

## Issues Found
| # | Severity | Location | Issue | Required Fix (APPLIED) |
|---|----------|----------|-------|------------------------|
| 1 | CRITICAL | Steps 2.3/3.4/6.1 markdownlint baseline | `git show HEAD:SKILL.md` baseline invalid — parent task UNCOMMITTED (HEAD 1585 vs worktree 1661; HEAD lacks §6.3/§0.7, 0 `onboarding_status_source`). Delta measures ~76 lines of parent content → gate FAILs spuriously → 2-cycle churn on out-of-scope content. | Pre-edit `cp` snapshots in 2.1/3.1/4.1; baseline delta against snapshot (not HEAD) in 2.3/3.4/4.2/6.1. |
| 2 | IMPORTANT | Steps 2.3/3.4/4.2/6.1 lint binary | Bare `markdownlint` not on PATH → command-not-found → log-and-skip silently bypasses the mandated all-rule lint. | Switched to `npx --yes markdownlint-cli` (0.48.0, honors `.markdownlint.json`). |
| 3 | IMPORTANT | F-1 phase downstream consumer | `evals.json:805` `text` = third copy of inverted predicate `(slug_count - readonly) > 20`. Fixing only SKILL.md+fixture leaves contradiction at third site. | Added Step 2.2b (reconcile evals.json:805; field value unchanged → still grades); wired into 2.3/2.4/Key-Obj-1. |
| 4 | IMPORTANT | Step 2.3 `git stash` wrapper | Gratuitous (`git show HEAD:` bypasses worktree) AND dangerous: failed `stash pop` under `\|\| true` on dirty tree reverts in-progress edit. | Removed the stash dance. |
| 5 | MINOR | Steps 5.1/5.2 G-2 JSON edit | id-22/24 objects described as compact single-line but on disk are multi-line pretty-printed (6 indented lines+`},`); literal compact `old_string` would mismatch. | Added on-disk-format NOTE; Edit `old_string` must match actual whitespace. |

## Actions Taken
- Pre-edit snapshot capture added to Steps 2.1, 3.1, 4.1; markdownlint comparison rewritten in 2.3, 3.4, 4.2, 6.1 to baseline against snapshot (not HEAD), with inline rationale.
- Replaced bare `markdownlint` with `npx --yes markdownlint-cli` in 2.3, 3.4, 4.2, 6.1.
- Inserted Step 2.2b (reconcile evals.json:805); updated Step 2.3 (evals.json JSON-validity), Step 2.4 (gate inputs + checks b/c), Key Objective #1.
- Removed `git stash --keep-index ... pop || true` from Step 2.3.
- Added on-disk-format NOTEs to Steps 5.1 and 5.2.
- Verified each fix: re-Read edited regions; dry-ran `make verify-sync` (PASS), `npx markdownlint-cli --version` (0.48.0), Step 5.3 one-liner (`JSON_VALID`), `git diff --stat HEAD` + `git cat-file -e HEAD:` (proved parent-task uncommitted).

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
(a) rf-qa PASS items relied on (structural re-check skipped):
- Relied on rf-qa PASS for: frontmatter/sections, B2 self-containment, granularity (F-2 3 sites / G-2 2 ids), per-phase gates, TB-Add-1..8, embedded current-state strings byte-match disk, F-1 predicate fires for 25/24/1, F-2 renames, G-1→1.1.0, G-2→regex_present grader-valid, guardrails.

(b) Independent semantic checks where rf-qa PASS was INSUFFICIENT (≥1 — INV-019):
- **Markdownlint baseline correctness** (`git diff --stat HEAD`, `git cat-file -e`, `wc -l`): rf-qa verified strings byte-match the worktree but NOT that `git show HEAD:` is a valid pre-edit baseline; my tool work proved parent task uncommitted → CRITICAL spurious-delta defect.
- **Downstream-consumer completeness** (grep `slug_count - readonly` across evals.json): found the uncovered third site (evals.json:805).
- **Gate command executability** (`command -v markdownlint`, `npx markdownlint-cli --version`, live `make verify-sync`): proved bare `markdownlint` absent and JSON one-liner runs.

## Recommendations
- Re-run this gate (fix-cycle 1) to confirm the five in-place fixes are clean. Expected: PASS.
- Ensure `/tmp/*-preedit.md` snapshots survive session rollovers; Step 6.1 documents a recovery path.

## QA Complete

VERDICT: FAIL
