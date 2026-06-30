# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** pr_submit V1.1 (FR-8 / FR-9 / FR-10)
**Date:** 2026-06-12
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix authorization:** false
**Fix cycle:** N/A

---

## Overall Verdict: PASS (with 6 MINOR/IMPORTANT advisory findings)

## Scope
111 `- [ ]` checklist items across 8 phases. Each preceded by a `**Step N.M:**` label. QA-gate items embed agent spawn prompts. Lens = B2 self-containment (context+action+output+verification+completion-gate; embedded prompts; specific paths; measurable verification; per-file granularity; no contradicted-finding items; TB-Add-8 evidence binding).

## Anchor Verification (tool-backed)
All load-bearing `:line` citations spot-checked against current source on 2026-06-12:
- `fsm.py:792-793` — `# Re-review attributed to our push` + `result.round_counter += 1` — EXACT (the relocation target; confirmed ONLY round_counter mutation: single grep hit).
- `fsm.py:611` RESOLVING/"resolved" edge, `:613` INV-001 `rereview_attributed` edge — EXACT (task cites ~560-619).
- `fsm.py:627` `_noop`, `:654` RunConfig, `:676` do_resolve, `:25` `loop_guard_should_halt` import, `:135` should_halt_rounds — all EXACT.
- `models.py:3,20` "exactly 33 / EXACTLY 33 members", `:166` SkillResult, `:187` proposal — EXACT.
- `run_log.py:26-27` "The 5 idempotency sets" + IDEMPOTENCY_SETS tuple, `:103,109` "33" prose+ValueError — EXACT.
- `recovery.py:111` Branch-A → `MonitorState.S5_AWAITING_REREVIEW` — EXACT (OQ-1 seam).
- `classifier.py:17-19` STATE_ consts, `:60` classify (returns 3 states today) — EXACT.
- `detection.py:56` DetectionContract, `:75` from_yaml — EXACT.
- `thread-reply.md:72` issue-comment POST surface w/ fork pin — EXACT (Step 6.5 source).
- `commands/auggie-review.md` flags `--depth quick`/`--remediation-offer`/`--auggie-model claude-sonnet-4-6`/`--post-pr` default true — ALL present.
- File existence: 5 EXTENDED test modules + 5 cited refs + 2 cited scripts present; 2 NEW test modules, 2 NEW refs, 1 NEW script correctly ABSENT (to be created).
- Placeholder scan: zero TBD/FIXME in the task file.

## B2 Checklist Results (per lens item)

| # | Lens check | Result | Evidence |
|---|-----------|--------|----------|
| 1 | All 5 B2 components per item | PASS | Every `- [ ]` carries context ("because…"), action ("per addendum §6.x add…"), explicit output path, verification ("ensuring…"), and a "mark this item as complete" gate. Verified across all 8 phases. |
| 2 | No un-restated cross-item context | PASS | No "see above" / "continue from previous". Each item re-grounds its anchor (e.g. 5.5 "Re-read run_skill() loop now reflecting Step 5.4's edits"). |
| 3 | Agent-spawning QA items fully embed lens prompts | PASS | All ~40 gate items embed the lens name, adversarial framing string, input files, output path, and report-only/fix flag inline. No "see SKILL.md / use the standard prompt". |
| 4 | File paths specific + real | PASS | All cited source paths verified to exist (anchor table above). NEW artifacts correctly named as to-create. |
| 5 | Verification measurable | PASS | Criteria are concrete (e.g. "exactly one `round_counter += 1` site", "`len(EventType)==37`", "`make verify-sync` reports in sync"), not "verify it works". |
| 6 | Per-file granularity (no batch items) | PASS | models/classifier/detection/run_log/fsm each get own item(s); each ref + each test module + each script its own item. No "process all X". |
| 7 | No items on CODE-CONTRADICTED/UNVERIFIED findings | PASS | research/07 had 0 contradicted, 1 unverified (`accepted_trigger_phrases` planned field). Step 3.3 builds it as a planned default-list field — acceptable per lens note. |
| 8 | TB-Add-8 per-item Context evidence binding | PASS | Every code-surface-referencing Context carries a `file:line` anchor (e.g. `models.py:83-126`, `fsm.py:653-676`, `recovery.py:111`). New-file items cite the source file being created. |

## High-Risk Item Self-Containment (explicit lens asks)

**Step 5.4 (fsm.py increment relocation) — SELF-CONTAINED.** It (a) tells the executor to RE-GREP the anchor (`grep -n 'result.round_counter += 1\|Re-review attributed to our push\|do_resolve\|S5_AWAITING_REREVIEW'`); (b) REMOVE the optimistic `:793` increment + its comment; (c) RELOCATE gated on `config.rereview_outcome[cycle_index] == "attributed"` with index-out-of-range guard; (d) preserves ordering (after push, before next-iter `should_halt_rounds`); (e) explicitly states "EXACTLY ONE `round_counter += 1` site". Names both surfaces. NOTE: see Finding F1 re: the "surface 2 of 2" labelling and the transition()-edit of the same edge.

**Step 5.7 (recovery.py OQ-1) — SELF-CONTAINED and correctly HALTs.** It reads `recovery.py:111`, references OQ-1 by index, instructs DO NOT change Branch-A by default, write a PENDING decision record with explicit `DECISION: PENDING — requires human sign-off`, add a Follow-Up entry, leave source UNCHANGED. Conforms to memory `feedback_human_decision_items_must_halt`. Cross-checked: Follow-Up Items section already pre-seeds the OQ-1 High-priority entry (line 653), and Step 8.5/8.7 carry the PENDING status forward — no auto-default path to Done that ships a recovery.py change.

## Issues Found (advisory — none block PASS under B2 lens)

| # | Severity | Location | Issue | Suggested Fix |
|---|----------|----------|-------|---------------|
| F1 | IMPORTANT | Step 5.4 label + body | Item is labelled "surface 2 of 2" (run_skill), but its body ALSO depends on the transition() edge `(S5_AWAITING_REREVIEW,"declined")→S5B` added in 5.3. The increment relocation itself is purely run_skill — that part is self-contained — but the executor must hold 5.3's edits in mind. Mitigated because run_skill does NOT call transition() (stated in DAG note) and 5.3 precedes 5.4 in-phase. Self-contained ENOUGH to execute safely. | Optional: add a one-line "depends on Step 5.3 edges already applied" pointer in 5.4 Context. |
| F2 | MINOR | Step 5.3 edge (6) `fallback_skip` | The selector reads residual from `context`/`ctx` but the item hedges "read the residual signal from `context`/`ctx`" without binding which name the actual `transition()` signature uses (`transition()` at `fsm.py:560`). Item DOES say "encode the predicate explicitly" and re-grep is mandated globally, so executable, but the ambiguous param name is a soft gap. | Optional: have 5.3 re-grep `def transition(` signature first and bind the residual-context param name. |
| F3 | MINOR | Step 3.1 / 3.2 seam choice | Step 3.1 says implement decline predicate "prefer…in is_decline (Step 3.2)" while 3.2 says implement in classifier.py "or detection.py if…fits better". Two items each defer the module choice; both record the choice in Phase 3 Findings, so self-contained, but the module location is decided at runtime not in the plan. Acceptable under B2 (action + decision-record gate present). | Optional: pre-commit to one module to remove the deferral. |
| F4 | MINOR | Step 3.6 vs 5.9 fixture `decline-initial-poll.json` | Step 3.6 creates it; Step 5.9 says "if not already created in Phase 3 Step 3.6 — reuse it". Conditional reuse is self-contained; Phase 3 precedes Phase 5 so the fixture exists. No execution risk. | None required (correctly handled). |
| F5 | MINOR | Step 5.5(d) wording | "re-enter the V0.1 pipeline" references the pipeline by name; the stages are enumerated inline (`classify → re-grade → verify-before-remediate → route → fix → validate → push`) so self-contained, but "V0.1" is a spec-relative label not re-grounded to a code anchor. | Optional: cite the run_skill() loop region that embodies the pipeline. |
| F6 | MINOR | Step 8.6 `<EXECUTOR_CLASS>` placeholder | The POST-reflect item embeds `--executor-model <EXECUTOR_CLASS>` with an instruction to "substitut[e] the actual executor model class". A runtime substitution token explicitly flagged for substitution (not a stray placeholder) — the one item whose command is not fully literal. | None required (substitution explicitly instructed). |

## Confidence Gate
- **Confidence:** Verified: 8/8 lens checks + 2/2 high-risk items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 4 (each Bash batch directly verified cited anchors: fsm/models/run_log/recovery; classifier/detection/fsm/SkillResult; _noop/RunConfig/test-files/refs/auggie-flags; loop_guard-import/thread-reply/item-count/placeholder-scan)
- Every anchor claim in the high-risk and spot-check set was independently re-grepped. No padding.

## Summary
- Lens checks passed: 8/8
- High-risk items self-contained: 2/2 (Step 5.4 relocation, Step 5.7 OQ-1 HALT)
- Issues found: 6 (0 CRITICAL, 1 IMPORTANT, 5 MINOR) — all advisory; none breaks B2 self-containment
- Every item is independently executable with re-grounded anchors and a completion gate.

## Verdict
**VERDICT: PASS.** All 111 items satisfy MDTM B2 self-containment under this lens. The two named highest-risk items are self-contained enough to execute safely: Step 5.4 mandates the re-grep, removes the `:793` site, relocates conditional on `"attributed"`, and asserts a single increment site; Step 5.7 writes PENDING + HALTs leaving recovery.py unchanged per the human-decision rule. The 6 findings are advisory polish items (1 IMPORTANT cross-item awareness in 5.4, 5 MINOR deferrals/labels) that do not violate self-containment and need not block execution.
