# QA Report — task-qualitative (operational-correctness)

**Topic:** pr_submit V1.1 (FR-8/9/10) — NFR-6 core purity + INV-001 verbatim
**Date:** 2026-06-12
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## Overall Verdict: FAIL

One CRITICAL operational contradiction (T-N50 ⇄ review-retrigger.md gh-token), one IMPORTANT
omission (stale run_log.py:148 docstring count), and one MINOR test-marker/strict-markers note.
The CRITICAL defect will halt Phase 6 (Step 6.9 `pytest test_static_grep.py` fails at T-N50) if
executed literally. All other 12 operational dimensions verified sound against current source.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | Baseline `uv run pytest tests/pr_submit/ -q` = **138 passed in 0.21s** (Step 1.3 GREEN precondition holds). `make lint` / `ruff format --check src/ tests/` / `make verify-sync` are real targets; the two-gate split (Step 2.4/7.2) is real (CLAUDE.md confirms `make lint`=ruff check only). Phase 5/6 selectors target real files. |
| 2 | Project convention compliance | none | PASS | All skill edits target `src/superclaude/skills/...` then `make sync-dev`+`make verify-sync` (Step 6.9); NEVER stage `.claude/` is stated (Steps 6.9, 8.6). Core edits go to `src/superclaude/pr_submit/*.py`. Boundary respected. |
| 3 | Intra-phase execution-order simulation | none | PASS | DAG: models.py (Ph2) → classifier/detection (Ph3) + run_log (Ph4) → fsm (Ph5) → skill (Ph6) → validation (Ph7). fsm edges reference `S5A/S5B` members that Ph2 creates first. Step 5.9 reuses `decline-initial-poll.json` created in Step 3.6 — cross-ref consistent. No item reads an artifact a later item creates. |
| 4 | Function-signature verification | none | PASS | `round_counter += 1` confirmed at **fsm.py:793**, the ONLY mutation (grep: single hit). `run_skill()` does NOT call `transition()` (grep: only def+comment, no call site) — dual-surface claim accurate. `classify(payload, contract)` → 3 states (decline-first achievable). `DetectionContract` has 9 fields + `from_yaml` per-field `data.get` (3 new wire consistently). `IDEMPOTENCY_SETS` 5-tuple at run_log.py:27. fsm.py `field` import EXISTS (line 22) — Step 5.2 claim accurate. `loop_guard.should_halt(round_counter, max_rounds)` sig confirmed (Step 5.5 cap-1 call achievable). |
| 5 | Module-context analysis | none | PASS | run_log.py fold idioms verified: COUNT (`ROUND_INCREMENTED` :167), ADD-TO-SET guarded (`THREAD_RESOLVED` :177) — the cited models. MONOTONE-MIN (IDIOM C) genuinely has no precedent (no `min(` in folds) — task flags this correctly. `_noop` default at fsm.py:627 (Step 5.2 seam mirror correct). models.py EventType 33-member enum + `MonitorState` working/terminal split + `SkillResult` plain `@dataclass` all confirmed (Steps 2.1-2.3 idioms accurate). |
| 6 | Downstream-consumer analysis | AX-3 | **FAIL** | run_log.py:148 `rebuild_state` docstring "the 5 idempotency sets" is NOT updated by any item. Step 4.1 updates only the :26 comment; Step 4.3 updates only the "33" EventType prose. The 5→6 docstring at :148 is an un-addressed downstream consumer of the count change. See IMPORTANT finding I-1. |
| 7 | Test validity | none | PASS | Tests drive the real core via `RunConfig(...)` + `run_skill` with recorder seams (`do_retrigger`/`invoke_auggie_review`), NO real gh/git. T-PUSH-WITHOUT-REREVIEW-NO-TICK + T-AUGGIE-AT-MOST-ONCE explicitly required NON-VACUOUS (Steps 5.8/5.9). `len(EventType)==37` drift-guard (Step 4.5). Fixtures carry `expected` blocks + real `augment-code[bot]` login (matches existing fixtures). |
| 8 | Test coverage of primary use case | none | PASS | Steps 5.8/5.9 feed the full re-trigger + fallback paths through `run_skill` end-to-end (push→S5a→re-trigger→attributed-tick; decline→S5b→clamp→single-invoke→re-enter). §9 FR→T-ID matrix traced per-phase + final M4 fidelity gate (Step 7.GB) does phantom-coverage detection. |
| 9 | Error-path coverage | none | PASS | Watermark `None` = "accept any decline" (Step 3.2); stale pre-watermark decline ignored (EC-23, Step 3.6); index-out-of-range guard on `rereview_outcome[cycle_index]` (Step 5.4); locked:false HALT unaffected (Step 3.4). Decline both-regex-AND prevents false positives. |
| 10 | Runtime failure-path trace | AX-2 | **FAIL** | Data-flow break at Phase 6 gate. T-N50 (`test_tn50_core_pure_no_gh_git_tokens`, lines 98-109) scans `CORE_PURE_FILES` with a RAW line grep `re.compile(r"\bgh\b\|\bgit\b")` — NO fenced-block exemption. Step 6.8 adds `review-retrigger.md` to that set, but Step 6.5 requires that ref to contain a `gh api ... repos/IronbellyOrg/IronClaude/issues/<N>/comments` POST surface. Step 6.9's `pytest test_static_grep.py` then FAILS at T-N50. See CRITICAL finding C-1. |
| 11 | Completion-scope honesty | none | PASS | OQ-1 (recovery.py resume target) correctly HALTs: Step 5.7 leaves recovery.py SOURCE UNCHANGED, writes PENDING note + `### Follow-Up Items` entry (already pre-seeded at task line 655), per `feedback_human_decision_items_must_halt`. recovery.py:111 Branch-A→`S5_AWAITING_REREVIEW` confirmed as the real OQ-1 site. OQ-2 follows the spec reuse recommendation. No "done-anyway" over an open question. |
| 12 | Ambient-dependency completeness | none | PASS | Step 3.5 conditionally wires `__init__.py` re-exports ONLY if a test imports `STATE_DECLINED`/`is_decline` at package root (grep-gated — correct, avoids dead export). `--strict-markers` ON (pyproject:111); markers `inv`/`loop_guard`/`recovery` registered (139-142); every test step says "register new marker in pyproject or prefer reuse". SKILL.md lazy-load rows for both new refs (Step 6.1c). |
| 13 | Kwarg-sequencing red flags | none | PASS | Step 5.2 (add `do_retrigger`/`invoke_auggie_review`/`rereview_outcome` seams) precedes Step 5.4/5.5 (which CALL them). Step 5.3 (transition edges) + 5.4/5.5 (run_skill surface) are explicitly LOCK-STEP dual-surface. No "pass kwarg before signature exists" inversion. |
| 14 | Function-existence claims grep-verified | none | PASS | Verified absent (CREATE): `test_review_retrigger.py`, `test_auggie_fallback.py`, `review-retrigger.md`, `auggie-fallback.md`, `retrigger-review.sh`, S5a/S5b in state-machine.md (count 0). Verified present (MOD/EXT): the 5 EXT test modules, 8 refs, 2 scripts, all 5 core modules, `should_halt`/`user_label`/`RoundCounter`, `thread-reply.md:72` POST surface, `loop-guard.md:51/68` 33/5 counts. Zero unverified existence claims. |
| 15 | Template / cross-reference accuracy | none | PASS | auggie-review.md flag surface verified: `--depth quick`, `--remediation-offer` (default true, :52), `--auggie-model claude-sonnet-4-6` (:55), `--post-pr` default true on PR (:50). No `--fix` flag exists on auggie-review (grep empty) — so the `--depth quick --fix` STOP non-conflict (Step 6.6) is domain-accurate (that STOP is the troubleshoot surface; T-N40 enforces it). |

---

## Summary
- Checks passed: 13 / 15
- Checks failed: 2 (item 6 IMPORTANT, item 10 CRITICAL)
- Critical issues: 1
- Important issues: 1
- Minor issues: 1
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| C-1 | CRITICAL | Task Steps 6.5 + 6.8 + Key-Constraints (task:123); `tests/pr_submit/test_static_grep.py:98-109` | T-N50 scans `CORE_PURE_FILES` with a raw `\bgh\b\|\bgit\b` grep that does NOT exempt fenced code blocks (unlike T-104's `_command_lines`). Step 6.8 adds `refs/review-retrigger.md` to `CORE_PURE_FILES`, but Step 6.5 mandates that same ref contain a `gh api … repos/IronbellyOrg/IronClaude/issues/<N>/comments` POST surface. The two instructions are mutually incompatible: the ref is required to both contain `gh api` AND be asserted gh/git-token-free. `thread-reply.md` (8 gh tokens) is deliberately EXCLUDED from `CORE_PURE_FILES` for exactly this reason; the 3 current core-pure refs each have 0 gh/git tokens. Executed literally, Step 6.9 `pytest test_static_grep.py` FAILS at T-N50 and the Phase 6 gate halts. | EITHER (a) do NOT add `review-retrigger.md` to `CORE_PURE_FILES`; instead cover it with a T-104-style fenced+fork-scope test (the existing `_command_lines`/`_fork_scoped` path) — mirroring how `thread-reply.md` is handled — and keep only `auggie-fallback.md` (no `gh` surface) in the pure set; OR (b) extend T-N50 to skip fenced code blocks via `_command_lines` before adding the ref. Option (a) is lower-risk (T-N50's strict raw grep is a deliberate purity guard; weakening it affects fsm.py/loop_guard.py too). Note `augment-poll.md` (11 gh tokens) is similarly ineligible and is correctly never added. |
| I-1 | IMPORTANT | `src/superclaude/pr_submit/run_log.py:148` | `rebuild_state` docstring reads "the 5 idempotency sets" — a downstream consumer of the 5→6 count change that NO checklist item updates. Step 4.1 updates only the `:26` inline comment; Step 4.3 updates only the EventType "33"→"37" prose. After the 6th set lands, :148 is a stale count. Won't fail the suite (docstring prose), but contradicts the task's own "no stale count" discipline and the Phase 4 internal-consistency lens premise. | Add a clause to Step 4.1 (or 4.3): also bump the `rebuild_state` docstring at run_log.py:148 "the 5 idempotency sets"→"the 6 idempotency sets" (re-grep `'5 idempotency'` in run_log.py — TWO sites: :26 comment and :148 docstring). |
| M-1 | MINOR | Task Steps 5.8/5.9/3.6/4.4 (marker guidance) | Steps prefer reusing `loop_guard`/`inv`/`recovery` markers "or no marker". `--strict-markers` is ON, so if any NEW module introduces an UNregistered marker the WHOLE suite errors (not just that test). The NEW modules `test_review_retrigger.py`/`test_auggie_fallback.py` have no pre-existing marker convention — an executor adding e.g. `@pytest.mark.retrigger` without registering it bricks the run. | Tighten to: NEW test modules MUST use ONLY already-registered markers (`inv`/`loop_guard`/`recovery`) or none; ANY new marker MUST be appended to `pyproject.toml [tool.pytest.ini_options] markers` in the SAME item before the targeted pytest run. |

---

## Actions Taken
None — `fix_authorization: false`. All findings documented for the executor/orchestrator. No files
modified.

Scope note: All three findings concern files referenced by checklist items (test_static_grep.py
Step 6.8; run_log.py Steps 4.1/4.3; test modules Steps 5.8/5.9). None are `[OUT-OF-SCOPE]`.

---

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

Relied on the A.10 / A.10.25 PASS items below (skipped structural re-checking), and for each ran an
independent SEMANTIC operational check with my own tool engagement:

- Relied on **A.10 rf-qa phase-structure PASS** (8-phase DAG, models.py-first, gate floors) →
  semantic counterpart verified: I independently grep-confirmed the DAG is operationally executable —
  fsm.py Phase-5 edges reference `S5A/S5B` MonitorState members that Phase-2 (`models.py`) creates
  first, and `field` is already imported at fsm.py:22 so Step 5.2's `field(default_factory=list)` seam
  resolves. Structure being well-formed (rf-qa) did not tell me the increment site is a SINGLE mutation
  — I grep-verified `round_counter += 1` has exactly one hit (fsm.py:793) and `run_skill` never calls
  `transition()`, which is what makes the dual-surface relocation operationally coherent.
- Relied on **A.10 rf-qa b2-self-containment PASS** (111 items self-contained; fsm relocation +
  recovery OQ-1 HALT "verified safe") → semantic counterpart verified: self-containment is structural;
  I independently checked the OQ-1 HALT is operationally safe by reading recovery.py:102-111 and
  confirming Branch-A returns `S5_AWAITING_REREVIEW` (the real seam), and that Step 5.7 leaves the
  SOURCE unchanged + writes PENDING. **Where rf-qa PASS was INSUFFICIENT:** structural self-containment
  did NOT surface that Step 6.5 (review-retrigger.md must contain `gh api`) and Step 6.8 (add that ref
  to the zero-gh-token T-N50 set) are mutually contradictory — that required me to READ
  test_static_grep.py:98-109 and confirm T-N50's raw grep has no fenced-block exemption, then
  cross-check thread-reply.md (8 gh tokens, deliberately excluded). This is the CRITICAL C-1 finding
  that machine structural verification could not catch.
- Relied on **A.10.25 rf-analyst research-alignment PASS** (every §6 delta present; 5→6 idempotency
  correct; 0 fabrications) → semantic counterpart verified: alignment confirms the deltas are PRESENT;
  I independently checked one is OPERATIONALLY COMPLETE and found it is not — the 5→6 change leaves
  run_log.py:148's docstring count stale (I-1), a consumer the matrix-alignment check does not gauge.

---

## Self-Audit (mandatory)

1. **Factual claims independently verified against source:** ~30 — including the single-site
   `round_counter += 1` (fsm.py:793), `run_skill`∌`transition()`, IDEMPOTENCY_SETS 5-tuple, the two
   run_log "33" sites + the third models "33rd", DetectionContract 9-field/from_yaml shape, the three
   fold idioms (COUNT/ADD-TO-SET present, MONOTONE-MIN absent), fsm.py `field` import, loop_guard
   signatures, pyproject `--strict-markers`+marker registry, all five auggie-review flags, absence of
   the 7 NEW files, state-machine.md S5a/S5b absence, loop-guard.md 33/5 counts, thread-reply.md:72
   POST surface, and the decisive T-N50 raw-grep semantics.
2. **Specific files read:** task file (all 666 lines), `pr_submit/{models,fsm,classifier,detection,run_log,recovery}.py`,
   `tests/pr_submit/test_static_grep.py`, `tests/pr_submit/test_detection_contract.py`, `pyproject.toml`,
   `commands/auggie-review.md`, `skills/sc-pr-submit-protocol/refs/{thread-reply,state-machine,loop-guard,detection-contract}.md`,
   directory listings of skill refs/scripts + tests/pr_submit + fixtures, and a live baseline pytest run.
3. **Why trust this is thorough (not a 0-issue rubber-stamp):** I ran the actual baseline suite (138
   passed), then traced the T-N50 data-flow through the actual grep implementation rather than trusting
   the task's "extended to scan the 2 NEW refs" prose — which is exactly where the CRITICAL
   contradiction lives. I cross-checked it against how `thread-reply.md` (8 gh tokens) is currently kept
   OUT of the pure set, proving the exclusion is intentional and the proposed inclusion breaks it.
4. **Web research performed:** None — all verification was local-file-bound (source + tests + task). No
   Tavily/fallback engagement required or recorded.

---

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 6 (multi-pattern Bash) | Glob: 0 | Bash: 7
  (tool calls ≥ 15 checklist items; each Bash/Read mapped to specific checks — fsm/run_log/classifier/
  detection/recovery reads, anchor greps, baseline run, flag verification)
- All 15 items VERIFIED with tool evidence; 0 UNVERIFIABLE; 0 UNCHECKED.

---

## Recommendations

1. **Resolve C-1 before Phase 6 executes.** The one defect that mechanically halts the run. Preferred
   fix: keep `review-retrigger.md` OUT of `CORE_PURE_FILES`; add a T-104-style fenced + fork-scope
   assertion for it (mirroring thread-reply.md handling); add only the gh-free `auggie-fallback.md` to
   the T-N50 pure set. Rewrite Step 6.8 and adjust Key-Constraints (task:123) "T-N50 (extended to scan
   the 2 NEW refs)" → "T-N50 scans auggie-fallback.md; review-retrigger.md is covered by the T-104
   fenced/fork-scope path."
2. **Resolve I-1.** Add the run_log.py:148 docstring 5→6 bump to Step 4.1; re-grep `'5 idempotency'` to
   confirm both sites updated.
3. **Tighten M-1** marker guidance to an imperative for the two NEW modules under `--strict-markers`.

These are plan-level fixes to the task file (Steps 6.8 / 4.1 / 5.8-5.9), not source edits. Once C-1 and
I-1 are corrected in the task, the plan is operationally sound to execute.

VERDICT: FAIL

Unfixable-without-task-revision issues:
- C-1 (CRITICAL): T-N50 ⇄ review-retrigger.md gh-token contradiction (Steps 6.5/6.8) — halts Phase 6.
- I-1 (IMPORTANT): stale run_log.py:148 "5 idempotency sets" docstring (Steps 4.1/4.3 gap).
- M-1 (MINOR): strict-markers footgun for NEW test modules (Steps 5.8/5.9 marker guidance).
