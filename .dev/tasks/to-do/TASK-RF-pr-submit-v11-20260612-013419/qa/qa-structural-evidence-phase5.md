# QA Report — Structural Evidence / Anchor-Freshness (Phase 5, fsm.py)

**Topic:** pr_submit V1.1 — fsm.py / recovery.py evidence-quality + anchor-freshness lens
**Date:** 2026-06-12
**Phase:** report-validation (structural evidence gate)
**Fix authorization:** false (report-only)
**Stance:** adversarial — assume ≥5 stale-anchor/unsupported defects exist

---

## Overall Verdict: PASS (with 1 PROMPT-PREMISE DEFECT and 1 ANCHOR DRIFT, neither a code defect)

The four CRITICAL code claims hold against the live files. However, the adversarial
sweep surfaced **two defects in the gate's own framing/evidence anchors** (not in the
code): the claim-1 premise is arithmetically wrong, and the claim-2 anchor ("GENUINELY
UNCHANGED") mis-describes a brand-new staged file. Both are documented below. The
underlying fsm.py implementation is correct; the gate PASSES the code, but the gate's
*assertions about the code* contain stale/unsupported anchors that a future reader would
be misled by.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Optimistic increment removed; relocated, attributed-gated | PASS (code) / **DEFECT in premise** | `grep -c "round_counter += 1"` returns **3**, NOT 1 (fsm.py:779, 825, 988). The prompt's "EXACTLY ONE site" premise is false — see Issue #1 |
| 1a | Old `# Re-review attributed to our push:` comment GONE | PASS | `grep "Re-review attributed to our push"` → exit 1 (no match), fsm.py |
| 1b | Old UNCONDITIONAL increment GONE; single INV-001 site is attributed-gated | PASS | Only bare `result.round_counter += 1` is fsm.py:988, inside `outcome == "attributed"` branch (fsm.py:985 comment, guarded by fsm.py:974/979 decline/timeout early-breaks). `grep -E "[^_]round_counter \+= 1"` → exactly fsm.py:988 |
| 2 | recovery.py Branch-A resume target unchanged → S5_AWAITING_REREVIEW | PASS (code) / **ANCHOR DRIFT** | recovery.py:111 `return BRANCH_A_LANDED, MonitorState.S5_AWAITING_REREVIEW`; :9, :25 intact. BUT file is NEW (`A`, not in HEAD) — "GENUINELY UNCHANGED" is the wrong anchor; see Issue #2 |
| 3 | Core-purity grep shows only docstring/comment matches; no new exec shell/VC token | PASS | Independent live grep `-E "\b(subprocess|os\.system|gh |git |Popen|check_output|run\()"` → NONE-EXECUTABLE. The 4 captured matches (fsm.py:9, 362, 446, 469) are all docstring prose; live grep reproduces them byte-for-byte. .txt artifact matches live file |
| 4a | clamp_max_rounds exists | PASS | def fsm.py:145; used fsm.py:757 |
| 4b | _run_fallback exists | PASS | def fsm.py:737; used fsm.py:875, 977 |
| 4c | RunConfig new fields exist (rereview_outcome, fallback_findings, fallback_residual_findings, do_retrigger, invoke_auggie_review) | PASS | fsm.py:713, 718, 719, 733, 734 (all defined on the dataclass) |
| 4d | S5A_RETRIGGER_REVIEW / S5B_AUGGIE_FALLBACK states exist + reachable | PASS | Defined models.py:115, 116; reached in transition() fsm.py:626/627, 639/642/643/647 |
| 4e | fallback_round_counter is a real, distinct model field (not aliasing round_counter) | PASS | models.py:213 `fallback_round_counter: int = 0`, separate from models.py:189 `round_counter: int = 0` |

---

## Summary

- Checks passed (code-level): 11 / 11
- Code defects found: 0
- Gate-anchor / premise defects found: 2 (Issue #1 false premise, Issue #2 stale anchor)
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | gate prompt claim 1 vs fsm.py:779/825/988 | The instruction asserts `grep "round_counter += 1"` "must return EXACTLY ONE site." It returns **3**. Two are `result.fallback_round_counter += 1` (fsm.py:779, 825 — the independent cap-1 fallback counter, models.py:213) and only one is the INV-001 `result.round_counter += 1` (fsm.py:988). The premise conflates two distinct, intentionally-separate counters. The *code* is correct (the single INV-001 site IS relocated + attributed-gated); the *gate assertion* is arithmetically false and would FAIL a literal automated grep-count check. | Restate the claim as: bare `round_counter += 1` (anchored `[^_]`) returns exactly one site (fsm.py:988); `fallback_round_counter += 1` is a separate counter and out of scope. |
| 2 | MINOR | gate prompt claim 2 vs `git cat-file -e HEAD:...recovery.py` | The instruction says recovery.py is "GENUINELY UNCHANGED (no edit to the Branch-A resume target)." But recovery.py is **not in HEAD** — `git status` shows `A` (newly added, 135 insertions, 1 file changed). "Unchanged" is the wrong anchor for a file that does not yet exist in the baseline. The *intended* invariant (V1.1 did not perturb the Branch-A → S5_AWAITING_REREVIEW resume target) holds — recovery.py:111 is correct — but it holds because the file was authored whole this build, not because an existing file was left alone. | Re-anchor claim 2 as "Branch-A resume target is correct (recovery.py:111 → S5_AWAITING_REREVIEW)" rather than "genuinely unchanged"; the file is a Phase-5 net-new addition, not a preserved prior artifact. |

Note: Per the gate's `fix_authorization: false`, nothing was modified. Both issues are
defects in the *gate's own anchors/premises*, not in fsm.py or recovery.py. The four
CRITICAL code behaviors the gate exists to protect are all intact.

---

## Actions Taken

None (report-only). All verification performed via Read + Grep + Bash(git) only.

---

## Confidence

- **Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 (via Bash) | Glob: 0 | Bash: 4 (grep/git)

Every PASS is backed by a cited grep/git result reproduced live against the on-disk
files this turn. The core-purity .txt artifact was re-derived independently (not trusted)
and matches the live fsm.py byte-for-byte on all 4 cited lines.

### Adversarial note (why PASS despite a "find ≥5 defects" mandate)

The mandate demanded ≥5 stale-anchor/unsupported defects. I found **2 genuine
gate-anchor defects** (Issues #1, #2) and confirmed the remaining suspected defect
classes do NOT exist:

- Increment relocation — verified real, not stale (fsm.py:988 attributed-gated; old comment gone).
- Symbol references — all 5 named symbols (clamp_max_rounds, _run_fallback, the RunConfig fields, S5A/S5B) exist AND are wired (defined + referenced), not dangling.
- Core-purity .txt — verified to match the live file, not a stale captured artifact.
- recovery.py Branch-A target — correct, not regressed.

Manufacturing 3 more "defects" to hit the quota would be fabrication and would violate
the zero-tolerance evidence rule. The honest count is 2, both in the gate's framing,
zero in the code.

## QA Complete

VERDICT: PASS
