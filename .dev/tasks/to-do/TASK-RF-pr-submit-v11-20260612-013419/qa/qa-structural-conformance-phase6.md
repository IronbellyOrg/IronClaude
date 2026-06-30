# QA Report — Template-Conformance Lens (Phase 6: skill / refs / scripts)

**Topic:** pr_submit V1.1 — Phase 6 structural/template conformance
**Date:** 2026-06-12
**Phase:** structural-conformance (template-conformance lens)
**Fix cycle:** N/A
**Fix authorization:** false (report only — nothing modified)
**Stance:** Adversarial. Sought ≥5 conformance errors; verified every claim by reading the actual files.

---

## Overall Verdict: PASS

No conformance defects found. All three verification targets conform. The adversarial
hunt for ≥5 errors turned up only NON-DEFECT observations (documented below so the
parent can confirm they were checked, not skipped).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | review-retrigger.md follows ref doc structure (purpose/surface/invariant) | PASS | `review-retrigger.md:1` title `# Review Re-trigger (RT) …`; `:15` `## 1. Purpose`; `:20` `## 2. Surface (fork-pinned issue-comment POST)`; `:35` `## 3. Watermark / attribution`; `:43` `## 4. INV-R1 (re-trigger boundedness, normative)`. Mirrors existing `thread-reply.md` (`# Title —`, numbered `##` sections) and `augment-poll.md`. |
| 2 | auggie-fallback.md follows ref doc structure | PASS | `auggie-fallback.md:1` `# Auggie Fallback (AF) …`; `:13` `## 1. Decline detection`; `:26` `## 2. The fallback invocation (byte-exact flag string)`; `:38` `## 3. Strict-once + clamp + single-shot (the invariants)`; `:51` `## 4. Re-entry contract (FR-9.4)`; `:57` `## 5. Terminal (OQ-2 reuse)`. Conforms to convention. |
| 3 | Both refs carry NFR-6 core-purity boundary note | PASS | `review-retrigger.md:8-13` (CARRIES gh token → T-104, excluded from CORE_PURE_FILES); `auggie-fallback.md:9-11` (ZERO shell token → IS in CORE_PURE_FILES). Matches inventory rows 13/14. |
| 4 | retrigger-review.sh shebang `#!/usr/bin/env bash` | PASS | `retrigger-review.sh:1`. |
| 5 | `set -euo pipefail` present | PASS | `retrigger-review.sh:17`. |
| 6 | `die()` helper, template-shaped | PASS | `retrigger-review.sh:19` `die() { printf 'retrigger-review: %s\n' "$1" >&2; exit "${2:-1}"; }` — identical shape to `reply-resolve-thread.sh:20`. |
| 7 | `--pr` arg loop | PASS | `retrigger-review.sh:22-27` `while [ $# -gt 0 ]; do case "$1" in --pr) … ;; *) die "unknown argument" 2`. |
| 8 | `command -v gh` guard | PASS | `retrigger-review.sh:30` `command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 2`. |
| 9 | SoT footer comment | PASS | `retrigger-review.sh:15` `# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.` — byte-identical to `reply-resolve-thread.sh:16`. |
| 10 | fork-pin (`repos/IronbellyOrg/IronClaude/...`, never upstream) | PASS | `retrigger-review.sh:35` `"repos/IronbellyOrg/IronClaude/issues/${PR}/comments"`; reinforced in header `:13`. No upstream path present. |
| 11 | exits 0 (success) / 2 (usage) | PASS | `retrigger-review.sh:40` `exit 0` (success); usage errors `:26,:29,:30` all `die … 2`. (Runtime POST-failure uses exit 1 at `:37` — see Observation O1; this matches the template's `exit "${2:-1}"` default and is not a contract violation.) |
| 12 | retrigger-review.sh is executable (+x) | PASS | `ls -l` → `-rwxr-xr-x … retrigger-review.sh` (and `reply-resolve-thread.sh` likewise). |
| 13 | SKILL Wave table has +Wave 6 re-trigger row + Wave 6b row | PASS | `SKILL.md:82` `Wave 6: … + re-trigger ← loads … refs/review-retrigger.md (S5a)`; `:83` `Wave 6b: (L3) decline → auggie fallback ← loads refs/auggie-fallback.md (S5b, strict-once)`. |
| 14 | Wave 6b bullet well-formed; byte-exact flag string present | PASS | `SKILL.md:94` contains exact `--depth quick --remediation-offer --auggie-model claude-sonnet-4-6` (grep `-o` exact match). Same exact string at `auggie-fallback.md:28`. |
| 15 | No `--no-post-pr` in the invocation | PASS | SKILL.md: zero `no-post-pr` occurrences anywhere. auggie-fallback.md: only occurrence is the prohibition note `:36` (`--no-post-pr must NOT be passed`), NOT in the invocation block `:27-29`. |
| 16 | Lazy-load rows for both new refs in Wave table | PASS | `SKILL.md:82` (review-retrigger.md) and `:83` (auggie-fallback.md), under the heading `:73` "refs are LAZY-loaded per wave, never pre-loaded". |
| 17 | Flag string flags are REAL (anti-hallucination cross-check) | PASS | Verified against authoritative command `commands/auggie-review.md`: `--depth quick` (`:49`), `--remediation-offer` default true (`:52`), `--auggie-model` with literal example `claude-sonnet-4-6` (`:55`), `--post-pr` default true for PR (`:50`). No fabricated flag/value. |
| 18 | `--depth quick` (auggie-review, no --fix) ≠ troubleshoot STOP conflict | PASS | SKILL.md STOP at `:123` is `--depth quick --fix` to **troubleshoot**; fallback `:94` targets **auggie-review** (a review, no `--fix`). Distinction stated correctly at `SKILL.md:94` and `auggie-fallback.md:33`. |

## Summary

- Checks passed: 18 / 18
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None.

## Observations (NON-DEFECTS — verified, not flagged)

These were the candidates the adversarial pass scrutinized; each was confirmed conformant
rather than a defect:

- **O1 — exit 1 (failed POST) at `retrigger-review.sh:37`.** The lens spec lists "exits
  0 (success) / 2 (usage)". The script ALSO has an exit-1 path for a failed `gh api` POST.
  This is NOT a deviation: the convention template `reply-resolve-thread.sh` likewise uses
  `exit "${2:-1}"` (default 1) and carries a 3 path; reserving exit 1 for genuine I/O
  failure (distinct from usage 2 and success 0) is the shared shape, not a violation. The
  script's own header `:10` documents `0/2/1` explicitly. Conformant.
- **O2 — `--auggie-model` is a CLI flag, but the protocol passes the model via the
  `${AUGGIE_MODEL:+--model …}` env-interpolation at `sc-auggie-review-protocol/SKILL.md:162`.**
  Checked because the fallback string uses `--auggie-model`. The authoritative surface is
  the command file (`commands/auggie-review.md:55`), which DOES define `--auggie-model
  claude-sonnet-4-6` as the operator-facing flag (the protocol's `AUGGIE_MODEL` env var is
  the internal plumbing the command maps it onto). The fallback invocation correctly uses
  the operator-facing flag. Conformant.
- **O3 — `--remediation-offer` annotated "(default true)" in `auggie-fallback.md:34`.**
  Cross-checked against `commands/auggie-review.md:52` (`--remediation-offer | true`).
  Annotation is accurate; passing the flag explicitly is harmless and self-documenting.
  Conformant.
- **O4 — `# Title — subtitle` em-dash style.** Both new refs use the em-dash subtitle
  convention (`review-retrigger.md:1`, `auggie-fallback.md:1`) matching `thread-reply.md:1`
  and `detection-contract.md:1`. Consistent.

## Actions Taken

None (report-only; fix_authorization: false; no files modified).

## Recommendations

- Phase 6 skill/refs/scripts surface is structurally green. No remediation required from
  this lens. (Note: the inventory's `make verify-sync` failure on `sc-recommend-protocol
  MISSING in src/` is pre-existing and orthogonal to pr_submit — out of this lens's scope;
  not re-tested here.)

---

## Confidence Gate

**Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 6 | Glob: 0 | Bash: 6

All 18 checklist items marked [x] VERIFIED with cited tool output (file:line + grep/ls
results). Tool-call count (Read+Grep+Bash = 19) ≥ checklist items (18) — not suspect.
No external web lookup was required (all claims local), so no Tavily/web-fallback lines apply.

## QA Complete

VERDICT: PASS
