# QA Report — Task ↔ Research Alignment

**QA Mode:** task-integrity
**Lens:** task-research-alignment
**Task file:** `TASK-RF-submit-pr-20260611-030241.md`
**Research dir:** `research/` (01–08)
**Spec:** `merged-spec.md`
**Stance:** ADVERSARIAL — assume builder dropped/misrepresented findings; find ≥3 alignment gaps.
**Date:** 2026-06-11

---

## Method

Cross-validate that every significant research finding (files 01–08) has a corresponding checklist
item in the task file, and that no task item fabricates actions ungrounded in research/spec. Six-part
checklist: (1) per-research-file coverage; (2) per-Python-module items; (3) canonical invariant tests;
(4) fabrication check; (5) caveats in verification criteria; (6) build-order DAG in phase ordering.

_(Findings appended incrementally below.)_

---

## Checklist Part 1 — Per-research-file coverage

### R01 (component inventory) — every C1–C6 path

| R01 path (C-ID) | Task checklist item acting on it | Status |
|---|---|---|
| `SKILL.md` (C1) | Step 4.4 (skeleton) + 6.3/7.4 (L2/L3 sections) | COVERED |
| `refs/state-machine.md` (C1/FSM) | Step 4.1 | COVERED |
| `refs/detection-contract.md` (DET) | Step 2.1 | COVERED |
| `refs/augment-poll.md` (C2) | Step 6.1 | COVERED |
| `refs/severity-routing.md` (C3) | Step 5.1 | COVERED |
| `refs/finding-verify.md` (C3a) | Step 5.2 | COVERED |
| `refs/troubleshoot-dispatch.md` (C3b) | Step 5.3 | COVERED |
| `refs/thread-reply.md` (C4) | Step 7.2 | COVERED |
| `refs/loop-guard.md` (LG) | Step 8.1 | COVERED |
| `scripts/poll-augment-review.sh` (C2) | Step 7.1 | COVERED |
| `scripts/reply-resolve-thread.sh` (C4) | Step 7.3 | COVERED |
| `commands/submit-pr.md` (C1) | Step 9.1 | COVERED |
| `hooks/scripts/offer-pr-review.sh` (C5 EDIT) | Step 9.2 | COVERED |
| `severity-rubric.md` (C3 REUSE) | Step 5.1 (defer-to) | COVERED |
| `tests/submit_pr/` tree (C6) | Phases 2/4/5/6/7/8/9/10 | COVERED |

All 8 refs, SKILL.md, both scripts, the command, and the hook edit each have a create/edit item. **R01 fully covered.**

### R03 (reuse surfaces) — defer-to, evidence-validator, dispatch flags

- **Severity-routing DEFERS to severity-rubric (reuse, not copy):** Step 5.1 instructs "DEFERS TO `severity-rubric.md` ... do NOT copy the table" and keeps grade(reuse)/route(new) separate. COVERED.
- **C3a reuses evidence-validator grounding:** Step 5.2 explicitly "SPAWN the existing `evidence-validator` agent ... rather than authoring a new verifier agent" and cites SKILL.md:22 / :206-209 / :183/:215. COVERED.
- **C3b dispatch flags (Medium→`--fix`, High/Critical→`--depth deep --fix`, never `--depth quick --fix`):** Step 5.3 documents exactly this and "EXPLICITLY note that `--depth quick --fix` is a STOP/conflict that must NEVER be emitted." COVERED. Spec correction #5 reinforces in Key Constraints.

**R03 fully covered.**

### R04 (test infra + deterministic core)

- **Python core at `src/superclaude/submit_pr/` (underscored):** Source Areas + SPEC CORRECTION #1 + Step 2.2 all use the underscored path. COVERED.
- **`--cov=superclaude.submit_pr`:** SPEC CORRECTION #2 + Step 11.3 use the corrected target with rationale. COVERED.
- **4 markers in pyproject:** SPEC CORRECTION #3 + Step 9.3 register EXACTLY `loop_guard`, `autonomy`, `recovery`, `p0` and explicitly exclude `loop`. COVERED.
- **Test modules + conftest mapped:** all 21 spec test modules have items (see Part 2 / Part 3). COVERED — with a count-precision observation noted under Observations.

### R06 (detection probe + gh surface)

- **R1 DET probe as needs_human_decision HALT:** Step 2.0 is a `needs_human_decision` operator item that "Writes PENDING and HALTs ... NEVER auto-locks." COVERED.
- **detection-contract.md ships `locked:false`:** Step 2.1 ships `locked: false`, `augment_bot_login` stays `<PROBE-LOCKED>`. COVERED.
- **gh poll/reply/resolve surfaces:** Step 6.1 (poll), 7.1 (poll script), 7.2/7.3 (reply+resolve). COVERED.
- **GraphQL resolveReviewThread:** Steps 7.2 and 7.3 document the two-step GraphQL node-id query + `resolveReviewThread(input:{threadId})`. COVERED.

### R08 (run-log / recovery / FSM / validation)

- **33 run-log event types:** SPEC CORRECTION #4 + Step 2.2 ("EXACTLY the 33 ... the 32 from §11.3 PLUS `push_aborted_or_not_landed`"). COVERED.
- **5 idempotency sets:** Step 8.3 lists all 5 by name. COVERED.
- **`fix_key=sha256(path+line+finding_body)`:** Steps 8.3, 8.7, 7.5 all encode the comment_id-independent fix_key. COVERED.
- **INV-007 push triad:** Step 7.4 (`push_decision`→`push_initiated`→`push_completed`) + Step 8.4. COVERED.
- **crash-window 3-way resume:** Step 8.4 documents branches A/B/C verbatim. COVERED.
- **FM-1..12:** Step 8.8 enumerates all 12. COVERED.
- **FSM gate table + INV-016 5-predicate:** Steps 4.1/4.2 (gate table + conjunction). COVERED.
- **VG-1..6 with lint≠format split:** Step 6.2 + SPEC CORRECTION #6 (VG-3≠VG-4) + Steps 11.4/11.5 as two distinct gates. COVERED.

**R08 fully covered.**

### R02 and R05 (secondary research)
R02 conventions are consumed at Steps 4.4, 7.1, 9.1 (house style); R05 integration points at Steps 4.4, 5.3, 6.3, 9.1 (Monitor arming, registration, gh/git discipline). COVERED.

**Part 1 verdict: PASS** — every significant finding in all 8 research files maps to at least one checklist item.

---

## Checklist Part 2 — Per-Python-module items

R04 §★ + R08 name 8 deterministic-core modules (plus `__init__.py`). Mapping to checklist items:

| Module | Create item | Status |
|---|---|---|
| `models.py` | Step 2.2 | COVERED |
| `detection.py` | Step 2.3 | COVERED |
| `classifier.py` | Step 2.3 | COVERED |
| `fsm.py` | Step 4.2 (+ extended in 6.2, 7.4) | COVERED |
| `severity_router.py` | Step 5.1 | COVERED |
| `loop_guard.py` | Step 8.2 | COVERED |
| `run_log.py` | Step 8.3 | COVERED |
| `recovery.py` | Step 8.4 | COVERED |
| `__init__.py` (+ re-exports) | Steps 2.2 (create) + 4.3 (re-exports) + 5.1 (remap_severity re-export) | COVERED |

All 8 named modules + `__init__.py` have dedicated items. **Part 2 verdict: PASS.**

Note (not a gap): R04 originally named the severity module `severity.py`; the task uses `severity_router.py`. This is a faithful adaptation, not a fabrication — the spec's test module is `test_severity_router.py` (merged-spec.md:435) and the public function `remap_severity` (merged-spec.md:944) is preserved and re-exported. The rename aligns the module to the spec's own test-file name.

---

## Checklist Part 3 — Canonical invariant tests

| Canonical test | Checklist item | p0 marker? | Status |
|---|---|---|---|
| T-626-OFF-BY-ONE | Step 8.5 | yes (`@pytest.mark.p0`) | COVERED |
| T-VANISHED-MONO | Step 8.5 | (loop_guard) | COVERED |
| T-CRASH-WINDOW-NO-DOUBLE-PUSH | Step 8.8 | (recovery) | COVERED |
| T-ZERO-EDIT-NO-PUSH | Step 4.7 | yes (asserts all 3 sub-conditions) | COVERED |
| T-VALIDATED-NOT-VERIFIED | Step 8.9 | (INV-015 audit) | COVERED |
| T-N50 (core purity) | Step 9.5 | — | COVERED |
| T-210 (locked HALT) | Step 2.4 (+ proven at 2.5) | — | COVERED |

All 7 required canonical invariant tests have explicit items with the correct fixtures and assertions. T-626-OFF-BY-ONE and T-ZERO-EDIT-NO-PUSH are marked `p0`. **Part 3 verdict: PASS.**

Additionally, the canonical test `T-FRESH-COMMENT-NO-DOUBLE-FIX` (INV-009, the 7th in the spec §6.1 invariant row alongside the above) is covered at Steps 7.5 and 8.7. Spec §6.1 lists 6 invariant tests by name; the task covers all of them plus the locked-HALT (T-210).

---

## Checklist Part 4 — Fabrication check (items NOT grounded in research/spec)

Method: scanned every Phase 2–11 build item for files, patterns, modules, markers, event types, flags, or assertions not traceable to a research file or the spec.

| Candidate (potential fabrication) | Grounded? | Evidence |
|---|---|---|
| `severity_router.py` (vs R04 `severity.py`) | YES | spec test module name `test_severity_router.py` (merged-spec.md:435); function `remap_severity` preserved |
| `recovery.py` module | YES | R08 §2 explicitly recommends `recovery.py`; not in R04's original 7 but called out as the recommended new module name |
| 33rd event `push_aborted_or_not_landed` | YES | R08 §1.3a + spec §12.1 line 771 |
| 4 markers (`loop` excluded) | YES | R04 §E flags `loop` as over-count; SPEC CORRECTION #3 |
| `S4_HALT_BEFORE_PUSH` enum (unprimed) | YES | Key Constraints "Python state-enum naming" — documented spec-faithful adaptation of `S4'_HALT_BEFORE_PUSH` |
| `make lint-architecture` Check 6 / Activation requirement | YES | R05 §3 (command↔skill pairing) referenced in Steps 9.1, 11.2 |
| Default output-dir `.dev/pr-monitor/pr-<N>-<ts>/` | YES | R08 §1.2 / spec §11.2 lines 715-716 |
| `behavioral-drift.json` (INV-015) | YES | spec §6.3 fixture list + AC-13 |
| `/sc:reflect --mode post --diff` POST gate | YES | task-builder convention; `start_commit` captured Step 1.2; consistent with project POST-reflect discipline |

**No fabricated build actions found.** Every file, module, marker, event, flag, and assertion in the checklist traces to a research file or a spec line. The five "SPEC CORRECTION" entries are each justified against a research finding (R04 hyphen-illegality, R08 count gaps, R03 flag conflict), not invented. **Part 4 verdict: PASS.**

---

## Checklist Part 5 — Research-identified caveats in verification criteria

| Caveat | Where required | In verification criteria? | Status |
|---|---|---|---|
| NFR-6 core purity (zero gh/git in fsm/severity_router/loop_guard) | AC-9 / T-N50 | Yes — Step 9.5 (T-N50 static grep), PGB.2 core-purity lens, PGB.7 fidelity agents; per-module "ensuring ... ZERO gh/git tokens" clauses in 2.3, 4.2, 5.1, 8.2 | COVERED |
| SoT discipline (edit src/, never `git add .claude/*`) | Key Constraints | Yes — Steps 9.2, 11.1 ("NEVER `git add` any `.claude/` path"), 11.2 verify-sync (VG-5) | COVERED |
| `--repo IronbellyOrg/IronClaude` pin | FR-1.3 / AC-7 | Yes — Step 9.5 (T-104 static grep asserts every `gh ` pins `--repo`), Steps 7.1/7.2/7.3 ("EVERY call pins `--repo`"), Step 9.6 (T-108 wrong-owner HALT) | COVERED |
| VG-3 ≠ VG-4 (lint≠format split) | SPEC CORRECTION #6 | Yes — Steps 11.4 + 11.5 as two distinct Bash gates; T-511 regression at Step 6.4; 11.6 "do not declare PASS on lint-green-only" | COVERED |
| push target `origin` never `upstream`/`master` | Key Constraints / §10.2 | Yes — Step 7.4 ("push target is `origin`/PR-head never `upstream`/`master`") | COVERED |

**Part 5 verdict: PASS** — all research-identified caveats appear in concrete verification criteria (static tests + QA-lens + fidelity-gate), not merely prose.

---

## Checklist Part 6 — Build-order DAG (DET-first) reflected in phase ordering

Spec §3 DAG: `[0] DET gate → [1] FSM/SKILL → [2] C3/C3a/C3b → [3] VG/S3_FIXING → [4] C4/reply/resolve → [5] LG/run-log → [6] hook+suite+sync`.

| DAG step | Phase | Ordering enforced? |
|---|---|---|
| [0] DET gate (root) | Phase 2 + Phase Gate A | Yes — Phase Gate A L5 verdict gate "withholds authorization for Phase 4+ until contract tests PASS"; Phase 4 header "DO NOT begin until ... GATE A: PASS" |
| [1] FSM + SKILL | Phase 4 | Yes |
| [2] C3/C3a/C3b | Phase 5 | Yes |
| [3] VG + S3_FIXING + HALT_BEFORE_PUSH | Phase 6 | Yes |
| [4] C4 reply/resolve/push | Phase 7 | Yes |
| [5] LG + run-log + recovery | Phase 8 | Yes |
| [6] hook + command + markers + suite + sync | Phases 9–11 | Yes |

The DET-first hard gate is mechanically enforced via the Phase Gate A L5 contract-verdict gate. Phase 10 (test scaffolding/fixtures) is correctly placed AFTER the per-phase test modules because the §18.4 synthetic fixtures unblock all pure phases and the modules reference fixtures by path. **Part 6 verdict: PASS.**

Note: Phase numbering skips "Phase 3" (reserved, line 515) — Phases are 1, 2, Gate A, 4–11, Gate B. This is cosmetic (a reserved-slot artifact), not a DAG-ordering defect; the dependency chain is intact.

---

## Adversarial findings (≥3 required)

The stance required finding at least 3 alignment gaps. After exhaustive cross-validation, the builder's task file is unusually faithful: all 6 checklist parts PASS. The following are the closest items to gaps — all are LOW/MINOR severity and none rise to a coverage gap that drops a research finding:

1. **MINOR — Module-name drift R04→task (`severity.py` → `severity_router.py`).** A reader comparing R04 §★ verbatim to the task could flag this as a deviation. It is a faithful adaptation (matches the spec test-module name and preserves `remap_severity`), but the task does NOT explicitly annotate the rename the way it annotates the `S4'`→`S4_HALT_BEFORE_PUSH` enum adaptation. Recommend a one-line note in Step 5.1 stating the module is named `severity_router.py` to match the spec's `test_severity_router.py` (pre-empts a false internal-consistency flag at Gate B PGB.2). Not a coverage gap.

2. **MINOR — Test-module count phrasing.** The task description (frontmatter line 4) and Step 10 header say "21 test modules"; R01 §C6 says "22 test modules" (counting `conftest.py`) and the spec §6.3 layout lists 21 `test_*.py` modules + `conftest.py` + `__init__.py`. The actual per-module items (Phases 2/4/5/6/7/8/9 + Step 8.9/8.10) enumerate all 21 `test_*.py` modules, so coverage is complete; only the prose count is loosely stated. Recommend standardizing on "21 test modules + conftest + __init__" to avoid a Gate-B count-drift flag. Not a coverage gap.

3. **LOW — `test_validated_not_verified.py` marker.** Step 8.9 creates the INV-015 audit test but does not assign it the `recovery`/`autonomy`/`p0` marker family; spec §6.1 places T-VALIDATED-NOT-VERIFIED in the "Invariant (R3 canonical)" row. No marker is strictly required (it collects under default), but for consistency with the other canonical invariant tests (which carry `p0`/`loop_guard`), consider whether it should be marked. Low impact — `--strict-markers` does not require a marker, only registration of any used. Not a coverage gap.

4. **LOW — INV-009 `T-FRESH-COMMENT-NO-DOUBLE-FIX` appears in two modules.** Steps 7.5 and 8.7 both reference T-FRESH-COMMENT-NO-DOUBLE-FIX. The spec §6.3 layout assigns it to `test_reply_resolve.py` (7.5) AND `test_idempotency.py` (8.7) lists it too. This mirrors the spec's own dual listing (spec lines 441 and 442-ish), so it is faithful — but the executor should ensure ONE authoritative test definition (not a duplicate) to avoid a double-count against the ~115 target. Flagged so the executor de-dupes rather than implementing it twice. Not a coverage gap.

These four are the adversarial yield. None drops or misrepresents a research finding; all are cosmetic-precision or de-dup hygiene items.

---

## VERDICT: PASS

All six research-alignment checklist parts PASS. Every significant finding across research files 01–08 maps to at least one self-contained checklist item; every Python module, every canonical invariant test, and every research-identified caveat (NFR-6 purity, SoT, `--repo` pin, lint≠format, push-target) is represented in build + verification items; the DET-first build DAG is mechanically enforced via the Phase Gate A L5 verdict gate; and no checklist item fabricates an action ungrounded in research or the spec — the five "SPEC CORRECTION" deviations are each justified against a specific research finding.

**Issues (all non-blocking):**
- MINOR: annotate the `severity.py`→`severity_router.py` rename in Step 5.1 (pre-empt Gate-B false flag).
- MINOR: standardize the "21 vs 22 test modules" prose count.
- LOW: consider a canonical-invariant marker on `test_validated_not_verified.py`.
- LOW: ensure T-FRESH-COMMENT-NO-DOUBLE-FIX is defined once (de-dup across Steps 7.5/8.7).

None of these are coverage gaps; the task file is execution-ready from a research-alignment standpoint.

---
