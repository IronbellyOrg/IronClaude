# QA Consolidated Fix Log — task-qualitative (I20 serialized fix round)

**Topic:** pr_submit V1.1 (FR-8/9/10) — NFR-6 core purity + INV-001 verbatim
**Date:** 2026-06-12
**Phase:** task-qualitative → fix-cycle (consolidated)
**Role:** SINGLE fix authority (I20 serialized) for A.10.5 operational + A.10.5 sufficiency + carried A.10.25 I-2
**fix_authorization:** true
**Task file:** `.dev/tasks/to-do/TASK-RF-pr-submit-v11-20260612-013419/TASK-RF-pr-submit-v11-20260612-013419.md`

Source findings consolidated from three upstream reports:
- `qa/qa-qualitative-operational-report.md` (C-1 CRITICAL, I-1 IMPORTANT, M-1 MINOR)
- `qa/qa-qualitative-sufficiency-report.md` (I-2 IMPORTANT carry-in)
- `qa/qa-task-research-alignment-report.md` (I-2 corroborated)

All four fixes are plan-level edits to the TASK FILE (not source-code edits). Each anchor was
re-verified against actual current source BEFORE editing (no reliance on the reports' frozen line
numbers). Scope: every edited item references files already in the task's checklist — none
`[OUT-OF-SCOPE]`.

---

## VERDICT: FIXES_APPLIED (4 of 4)

| Fix | Severity | Status |
|-----|----------|--------|
| FIX-C1 | CRITICAL | APPLIED |
| FIX-I1 | IMPORTANT | APPLIED |
| FIX-I2 | IMPORTANT | APPLIED |
| FIX-M1 | MINOR | APPLIED |

---

## FIX-C1 (CRITICAL) — T-N50 ⇄ review-retrigger.md gh-token self-contradiction

**Defect:** The task required `refs/review-retrigger.md` to contain a `gh api …/issues/<N>/comments`
POST surface (Step 6.5) AND added it to T-N50's zero-`gh`/`git`-token `CORE_PURE_FILES` set (Step 6.8).
Executed literally, T-N50 (`test_static_grep.py`) fails on the `gh` token and Phase 6 halts.

**Verification before edit (actual source):**
- `tests/pr_submit/test_static_grep.py:27-34` — `CORE_PURE_FILES` = state-machine.md, severity-routing.md,
  loop-guard.md, fsm.py, severity_router.py, loop_guard.py (3 gh-free refs + 3 core .py).
- `:98-109` — `test_tn50_core_pure_no_gh_git_tokens` compiles `re.compile(r"\bgh\b|\bgit\b")` and scans
  EVERY line of each pure file — NO fenced-block exemption.
- `:45-95` — `_command_lines` (fenced/`.sh`-aware) + `_fork_scoped` is the T-104 path; `test_t104…`
  already globs `SKILL_DIR.rglob("*")`, so it ALREADY scans the new gh-bearing ref + script.
- addendum §6.4 (line 262) + §6.5 (line 274): auggie-fallback.md = `> Skill sc:auggie-review-protocol`
  invocation (no `gh`); review-retrigger.md + retrigger-review.sh = the `gh api` surfaces.
- Confirmed `thread-reply.md` / `augment-poll.md` (gh-bearing) are deliberately ABSENT from
  `CORE_PURE_FILES` for exactly this reason.

**Edits (3 sites):**
1. **Step 6.8** (the T-N50 extension item) — rewrote into explicit (a)/(b)/(c) guidance:
   - before: "T-N50's `CORE_PURE_FILES` includes the two NEW refs `review-retrigger.md` and `auggie-fallback.md`"
   - after: (a) add ONLY the gh-free `auggie-fallback.md` to `CORE_PURE_FILES`, with a mandatory
     `grep -nE '\bgh\b|\bgit\b'` zero-match RE-VERIFY before adding; explicit "DO NOT add
     `review-retrigger.md`" + "`retrigger-review.sh` … MUST NOT go in `CORE_PURE_FILES`", citing the
     thread-reply.md/augment-poll.md exclusion precedent. (b) cover the gh-bearing
     `review-retrigger.md` + `retrigger-review.sh` with a T-104-style `_command_lines`+`_fork_scoped`
     fork-pin assertion (NOT the T-N50 raw grep). (c) keep T-1105/T-1115 static-parity tests.
2. **Step 6.5** (review-retrigger.md creation item) — appended a "NOTE (core-purity boundary)":
   this ref carries a `gh` token by design → covered by the T-104 fork-pin path, NOT T-N50; MUST NOT
   be added to `CORE_PURE_FILES` (cross-ref Step 6.8), exactly as thread-reply.md is kept out. This
   makes the T-N50 Verification explicit that a gh-bearing ref in CORE_PURE_FILES would (correctly)
   fail T-N50 — FIX-C1(c).
3. **Key Constraints (task:123)** — replaced "Statically asserted by T-N50 (extended to scan the 2 NEW
   refs)" → "T-N50 … extended to scan ONLY the gh-FREE new ref `auggie-fallback.md`; the gh-BEARING
   `review-retrigger.md` ref + `retrigger-review.sh` script are covered by the T-104 fork-pin path …
   mirroring how `thread-reply.md`/`augment-poll.md` are deliberately excluded from `CORE_PURE_FILES`."

Step 6.7 (retrigger-review.sh creation) needed NO change — it already mandates the fork pin and never
claims the script enters `CORE_PURE_FILES`.

---

## FIX-I1 (IMPORTANT) — second "5 idempotency" prose site (run_log.py:148) un-bumped

**Defect:** TWO "5 idempotency" prose sites exist in run_log.py; the 6th-set item (Step 4.1) updated
only the `:26` tuple comment, leaving the `rebuild_state` docstring "the 5 idempotency sets" at `:148`
stale after the 5→6 change.

**Verification before edit (actual source):**
- `grep -nE "5 idempotency|5 sets" run_log.py` → `:26` (`# The 5 idempotency sets (§11.4).`) AND
  `:148` (`Reconstructs the FSM state, ``round_counter``, the 5 idempotency sets, and`). Both confirmed.

**Edit (Step 4.1):** extended the Action to (i) append the 6th member (unchanged), (ii) bump the `:26`
comment, AND (iii) bump the `:148` `rebuild_state` docstring 5→6; plus a mandatory AFTER-edit
RE-GREP `grep -nE '5 idempotency|5 sets'` confirming ZERO stale "5"-count prose remains anywhere in the
file (bump any additional site surfaced). Re-grep pattern in the item broadened to include both sites.

---

## FIX-I2 (IMPORTANT) — INV-001 + INV-R1/R2/R3 not inlined verbatim in the task file

**Defect:** Task referenced INV-R1/R2/R3 (27×) and INV-001 by NAME only, routing literal-conformance
agents to a research artifact (`research/06 §4`). A POST-reflect / M4 fidelity pass reading ONLY the
task file could not do byte-level conformance — yet the user explicitly required "honor INV-001 verbatim."

**Verification before edit (source-of-truth copies):**
- INV-R1/R2/R3 verbatim: `merged-spec-v1.1-addendum.md` §5, lines 191-207 (the three `> INV-R…` blocks)
  — copied byte-for-byte from the addendum (source of truth), confirmed to match research/06 §4.
- INV-001 verbatim: `merged-spec.md` §9.1, lines 600-606 (the `> Single normative definition (INV-001,
  verbatim …)` block: S5→S2 edge, `>=` HALT gate, `round_counter + 1` label, `max_rounds=N ⇒ N pushes`)
  — located exactly in the V1.0 spec and transcribed verbatim (so no §10 restatement fallback needed).

**Edit:** Inserted a new durable `## Normative Invariants (Verbatim)` section AFTER `## Open Questions`
and BEFORE `## Detailed Task Instructions` (now at task line 159). It inlines:
- the INV-001 verbatim blockquote (cited to merged-spec.md §9.1 lines 600-606) + a relocation note
  (V1.1 moves only the increment site; edge/gate/monotonicity/N⇒N preserved byte-for-byte);
- the INV-R1/INV-R2/INV-R3 verbatim blockquotes (cited to addendum §5 lines 191-207);
- a one-line note that the Phase 5 INV-fidelity QA lens (Steps 5.G4/7.GA4), the Phase 7 M4
  source-fidelity gate (Step 7.GB), and the Phase 8 POST `/sc:reflect --mode post` gate (Step 8.6)
  check the implementation against THIS inlined verbatim text.

B2 self-containment preserved: the section sits in the informational header region (above the numbered
checklist), so item numbering is untouched.

---

## FIX-M1 (MINOR) — marker guidance not imperative under --strict-markers

**Defect:** Test items used soft "prefer reusing …/or no marker" phrasing. With `--strict-markers` ON,
an unregistered marker in ANY new test errors the ENTIRE suite at collection.

**Verification before edit (actual source):**
- `pyproject.toml:111` — `"--strict-markers"` in `addopts`. Marker registry at `markers = [` (`:114`)
  includes `inv`, `loop_guard`, `recovery` (the markers the items suggest reusing) — confirmed registered.

**Edits (4 test items):** Steps 5.8, 5.9 (the two NEW modules — primary risk), 3.6, 4.4. Each soft
"prefer reusing X or no marker" clause replaced with an imperative: because `--strict-markers` is ON
(`pyproject.toml:111`) and an unregistered marker errors the ENTIRE suite at collection, the item MUST
use ONLY already-registered markers (reuse the named ones, or no marker), and ANY genuinely new marker
MUST be appended to the `pyproject.toml [tool.pytest.ini_options] markers` list in THAT SAME item
BEFORE the item's pytest run (Step 3.7 / 4.6 / 5.11 respectively).

---

## Post-fix verification

- Grep-confirmed: `## Normative Invariants (Verbatim)` at line 159, between `## Open Questions` (154)
  and `## Detailed Task Instructions` (197); INV-001 + INV-R1/R2/R3 verbatim blocks present.
- Grep-confirmed: Key Constraints (123), Step 6.5 (482), Step 6.8 (495) all consistently route
  review-retrigger.md + retrigger-review.sh → T-104 path and only auggie-fallback.md → T-N50.
- Grep-confirmed: Step 4.1 (316) updates both :26 and :148 + re-grep sweep.
- Grep-confirmed: 4 occurrences of the imperative "ANY unregistered marker errors the ENTIRE suite"
  clause (Steps 5.8/5.9/3.6/4.4).
- All edits were surgical Edits preserving item numbering, B2 self-contained shape, and formatting.
  No source-code files were modified (these are plan-level task-file fixes, as the upstream reports
  prescribed).

---

VERDICT: FIXES_APPLIED (4 of 4)
