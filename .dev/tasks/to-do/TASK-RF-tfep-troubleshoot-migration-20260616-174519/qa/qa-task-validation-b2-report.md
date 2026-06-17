# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** TFEP /sc:forensic → /sc:troubleshoot migration tasklist
**Date:** 2026-06-16
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix authorization:** false
**Fix cycle:** N/A

---

## Scope

Task file: `TASK-RF-tfep-troubleshoot-migration-20260616-174519.md` (723 lines, Template 02).
Lens focus: every checklist item must be SELF-CONTAINED per MDTM B2 — context + action + output + verification + completion gate. Plus: no cross-item context reliance, fully-embedded QA lens prompts, specific paths, measurable verification, no batch items, no unverified-architecture items.

## Verification Performed (tool evidence)

- Read the full task file (723 lines, all 7 phases + 6 phase gates + 7 post-completion items).
- `rg`/`sed` verified EVERY cited source anchor exists with the claimed predicate text:
  - sc-task-protocol/SKILL.md §4.5: heading L133, Escalation gradient L172, Step 3 L205, "forensic tier" L206, "forensic pipeline" L213, Step 4 L215, "Forensic artifacts" L250, "committed to git" L253, Escalation Budget L255, freeze block L185. ALL PRESENT.
  - commands/task.md:48 bare-`forensic` ("without structured forensic analysis"). PRESENT.
  - commands/troubleshoot.md: argument-hint L8 ending `[--no-mcp]"`, Options `--no-mcp` row L58, `--scope` row L52 with `(none)` default, parse step L64, surface list L67. ALL PRESENT.
  - sc-troubleshoot-protocol/SKILL.md: Wave 0 parse L115, Wave 0 step 5 audit-header L119+block L129–138, exit criteria L141, STOP conditions L143, Output Contract header L37 (exactly 30 data rows — matches task claim), `contract_version` L62 with default `1.0.0`+NFR-6, `known_escapes_caught` L72, `status` enum L43 (`success/partial/failed`), SUMMARY footer L447–456 ending `duration_sec` L455, Wave 5 step-5 surface L459, exit criteria L466. ALL PRESENT.
  - refs/report-template.md: `## Next Steps` L146, `Tier 3 chain completed` L154, `### Hard-stop variant` L156. ALL PRESENT.

Conclusion on architecture: NO items are based on unverified architecture. Every load-bearing anchor the items target was confirmed to exist. This is a high-fidelity tasklist.

---

## B2 Self-Containment Findings

The file is unusually disciplined: every item carries Context (Read X because…), Action (then replace/insert…), Output (write to path / edit site), Verification (ensuring…), and a Completion gate ("This item cannot be marked as done…Once done, mark this item as complete"). The blocker-logging clause is present on all items. Batch-splitting is excellent — each rename anchor, each flag site, each contract field, each incident-field rebind is its own granular item (Steps 2.1–2.9, 3.1–3.10, 4.1–4.9, 6.1–6.4). QA lens prompts are FULLY embedded (adversarial framing + output path + binary verdict rule inline), not "see above".

That said, the adversarial stance is warranted and the following genuine B2 defects were found.

### Issue 1 — Step 5.5 conflates "verify" with "edit"; action is non-deterministic (IMPORTANT)
Location: Step 5.5 (line 472), "Confirm/encode the Step 4 status branches".
The action says "make ONLY the minimal edits needed so every branch reads an existing adapter field". B2 requires a single deterministic action with a concrete output. This item's output is conditional and unbounded — the executor must first discover what the four current branches say, then decide what "minimal edits" means, with the edit text NOT specified (unlike every sibling item in Phases 2–4 which gives exact before/after strings). It also presumes the current branch text (`status == "partial"` / `recommended_escalation != "none"`) without the item having Read-confirmed it. A reader cannot execute this without interpretation. Fix: split into (5.5a) a Read-and-record item that captures the verbatim current branch lines into a handoff file, and (5.5b) an edit item that rewrites named branches with exact target text keyed off the recorded baseline.

### Issue 2 — Step 5.6 has the same verify-or-encode ambiguity (IMPORTANT)
Location: Step 5.6 (line 476), "Encode the remediation-ownership decision in Step 5 insertion".
Action verb is "verify/encode that Step 5 (a)…(b)…(c)…(d)…". Four sub-conditions are listed but the item does not state whether each already exists (verify) or must be written (encode), and gives no exact insertion text for (a)–(c) — only (d), the ownership note, has a concrete string. The completion gate ("completed in their entirety exactly as described") is therefore unenforceable because "as described" is itself indeterminate. Fix: state for each of (a)–(d) whether it is an assertion to confirm or text to insert, and supply the insert text where it is an insert.

### Issue 3 — Step 6.1 embeds a conditional fallback that creates a second, unscoped action (IMPORTANT)
Location: Step 6.1 (line 530), Root-cause rebind.
The item says "If the incident template has no explicit Root-cause field, record that in the blocker log and rebind the nearest equivalent." "Rebind the nearest equivalent" is an unbounded second action with no defined target — it asks the executor to pick a field by judgment. This violates single-atomic-action. Worse, the premise (that an explicit Root-cause field exists at lines ~241–251) was NOT Read-confirmed by the item; the incident template's field inventory is asserted, not established. Fix: precede Phase 6 with a Read-and-enumerate item that records the incident template's actual field list, then make 6.1/6.2 target named fields from that recorded list (removing the "nearest equivalent" escape hatch).

### Issue 4 — Step 5.5 / 5.6 / 6.1 verification clauses are not measurable (IMPORTANT)
Location: Steps 5.5, 5.6, 6.1 (lines 472, 476, 530).
Per lens criterion (5), verification must be measurable. These three say "ensuring … no branch references a non-existent field" / "ensuring the append-not-replace semantics are preserved" / "ensuring … only the value-source reference changes" — but because the action itself is "verify/encode" with no fixed end-state, there is no objective pass/fail the executor or a later QA agent can check against. Contrast Step 2.2 ("only the parenthetical's phrase is changed … prefix and trailing `):**` preserved verbatim") which is checkable. Fix: once Issues 1–3 split the verify/edit, give each edit item a concrete post-condition (e.g. "rg confirms branch line reads exactly `…`").

### Issue 5 — Step 5.3 cross-item dependency on Step 5.2 enum without restating it (MINOR)
Location: Step 5.2 (line 460) and Step 5.3 (line 464).
5.2 maps triggers to `--depth standard/deep`; 5.3 sets `{depth}` "determined by the Step 3 mapping". 5.3's invocation correctness depends on 5.2 having run, and the depth enum values live only in 5.2. This is tolerable (same phase, ordered) but 5.3 restates none of the depth values, so if executed/reviewed in isolation the `{depth}` token is unresolved. Minor because the items are adjacent and 5.3 names the mapping source. Fix (optional): 5.3 could restate "standard for 1st trigger, deep for escalation/systemic".

### Issue 6 — Step 6.4 leaves a judgment call ("drop … rather than fabricating") inside the action (MINOR)
Location: Step 6.4 (line 542).
"If accurate troubleshoot per-depth bands are not known, drop the parenthetical token figures rather than fabricating them." This is a sound anti-fabrication guard, but it makes the final text non-deterministic (the budget block ends up with-or-without token bands depending on executor knowledge). The item is otherwise excellent (exact replacement lines given). Minor: acceptable as written because both branches are bounded and the fabrication-avoidance rationale is explicit; flagged for completeness under the adversarial mandate.

### Issue 7 — Step PC.5 verification is soft (MINOR)
Location: Step PC.5 (line 632) + Task Summary template (lines 644–663).
PC.5 says author the summary "using the templated format provided there". The template at line 644 has bracketed placeholders — fine — but PC.5's only completion check is "no fabrication", which is not objectively measurable. Self-contained enough to pass, but the verification is soft. Minor.

---

## Items Reviewed (B2 lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 5 B2 components present per item | PASS (3 exceptions) | Every item has Context/Action/Output/Verification/Completion-gate. Steps 5.5, 5.6, 6.1 have a defective (non-deterministic) Action — Issues 1–3. |
| 2 | No item relies on prior-item context without restating | PASS (1 minor) | Phase-gate items restate full paths; Step 5.3 leans on 5.2's depth enum (Issue 5, MINOR). |
| 3 | QA-spawning items have FULLY embedded lens prompt | PASS | All PG2–PG6 + PC.3 lens items embed adversarial framing, output path, binary verdict rule inline. No "see above". |
| 4 | File paths specific (absolute or repo-relative) | PASS | Every path is repo-relative or absolute; no "the relevant file". |
| 5 | Verification measurable | PARTIAL FAIL | Most items measurable (exact before/after, `verify-sync exit 0`, `rg` zero-hits). Steps 5.5/5.6/6.1 not measurable — Issue 4; PC.5 soft — Issue 7. |
| 6 | No batch items (one anchor/field/site per item) | PASS | Excellent granularity: 2.1–2.9 one rename each, 3.x one flag site each, 4.1–4.5 one field each, 6.1–6.4 one rebind each. |
| 7 | No items based on unverified architecture | PASS | All cited anchors confirmed present via rg/sed (see Verification Performed). |

---

## Summary
- Checks fully passing: #2, #3, #4, #6, #7 (5/7)
- Checks with exceptions / partial fail: #1 (3 exceptions), #5 (PARTIAL FAIL)
- Issues found: 7 (CRITICAL: 0, IMPORTANT: 4, MINOR: 3)
- The IMPORTANT cluster (Issues 1–4) is essentially ONE root defect in 3 items: **Steps 5.5, 5.6, and 6.1 conflate "verify-or-encode" into a single non-deterministic action with no exact target text and an unconfirmed premise about current file state.**

## Confidence
Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(Every B2 check applied to every item with tool evidence; all cited anchors independently grep-confirmed.)

## Tool engagement
Read: 6 | Grep(rg): 4 (multi-pattern) | Glob: 0 | Bash: 4 | (no web research required — task is fully local)

---

## Overall Verdict: FAIL

Rationale: Under zero-tolerance B2 standards, an item whose Action is "verify OR encode … make minimal edits" with no exact target text is not self-contained — the executor cannot complete it "exactly as described" because the description does not fix an end-state. This defect appears in Steps 5.5, 5.6, and 6.1 (Issues 1–3) and makes their verification clauses unmeasurable (Issue 4). These are IMPORTANT, not CRITICAL — the surrounding research fidelity is high (all 30+ anchors verified present) and the fix is mechanical (split each into Read-baseline + exact-edit items). All findings regardless of severity must be resolved before the tasklist is execution-ready.

## Required Fixes (priority order)
1. Split Step 5.5 into 5.5a (Read+record verbatim current branch lines → handoff file) and 5.5b (rewrite named branches with exact target text + `rg`-checkable post-condition).
2. Split Step 5.6 likewise; for each sub-condition (a)–(d) state verify-vs-insert and give insert text.
3. Add a Phase 6 "Step 6.0" that Reads and enumerates the incident-template field list; rewrite 6.1/6.2 to target named fields and delete the "rebind the nearest equivalent" escape hatch.
4. After the splits, give 5.5b/5.6/6.1/6.2 a concrete `rg`-checkable post-condition so verification is measurable.
5. (MINOR) Restate the depth enum in Step 5.3; tighten PC.5 verification; leave Step 6.4 as-is (acceptable anti-fabrication guard).

## QA Complete
