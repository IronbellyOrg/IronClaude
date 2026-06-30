# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** Pipeline Hardening Closure mode (H0-H5) for sc:troubleshoot-protocol
**Date:** 2026-06-10
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

The task file is structurally strong on hard B2 self-containment: zero "see above" / "continue from previous" / "use the standard prompt" references, every agent-spawning item carries a fully embedded prompt, file paths are specific and verified to exist on disk, the 5 new-ref paths are confirmed ABSENT (no collision), and no item rests on a fabricated path. However, adversarial scrutiny surfaces granularity (B2 atomicity) and embedded-prompt-completeness defects, plus minor accuracy drift, that warrant a FAIL under zero-tolerance gating.

## Items Reviewed (B2 Self-Containment Checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item has all 5 B2 components (context+action+output+verification+completion gate) | PASS (with exceptions in Issues) | All 47 `- [ ]` items inspected; each carries Read-context → action → output path → verification/ensuring clause → "mark this item complete". Phase 4/5 agent items embed adversarial prompt + report path + binary verdict rule. |
| 2 | No item references prior-item context without restating it | PASS | `grep -niE 'see above\|as above\|previous item\|continue from\|same as\|ditto\|use the (standard\|template) (prompt\|from)'` → 0 hits. Every item re-states its input paths verbatim. |
| 3 | Agent-spawning items have FULLY embedded prompts | PASS (12/12) | 12 items contain "with this embedded prompt" + full quoted prompt body. No "see SKILL.md" / "use the standard prompt". Verified Steps 4.2-4.9, 4.12-4.13, 5.1-5.2 each quote the entire agent instruction inline. |
| 4 | File paths specific (the 9 targets) | PASS | All 9 targets verified on disk: 4 edit targets EXIST (`commands/troubleshoot.md`, `SKILL.md`, `refs/report-template.md`, `refs/remediation-handoff.md`); 5 new refs ABSENT (no collision). Exemplar `escalation-rubric.md` EXISTS. |
| 5 | Verification criteria measurable | PASS | Step 3.2 requires literal `✅ All components in sync.`; Step 3.3 markdownlint clean on 9 named files; Step 3.4 grep for staged `.claude/` → CLEAN. No "verify it works". |
| 6 | No batch items (each of 9 file changes its own item) | PASS | 5 new refs = Steps 2.1-2.5 (one each); 4 edits split across Steps 2.6-2.7 (command), 2.8-2.11 (SKILL), 2.12-2.13 (report-template), 2.14 (remediation-handoff). No "create all 5 refs in one item". |
| 7 | No items based on CODE-CONTRADICTED/UNVERIFIED findings | PASS | Research 05 had no contradictions; spot-checked every embedded spec citation against the live spec (see accuracy checks). No fabricated path found. |
| 8 | New-ref items embed/cite the spec card they must reproduce | PASS | Steps 2.1-2.5 each cite exact spec section + line range + reproduce-verbatim instruction. Verified §6.2 (8 fields), §7 H1 card (13 fields, lines 136-151), H2 ledger (9 rows, 171-180), H4 card (10 fields, 241-253), §4/§8 against the live spec — all accurate. |

## Accuracy cross-checks performed (source-truth verification)

- Spec exists (382 lines), all section headers located. H1 card fence = spec L136-151 (item cites 136-151 ✅). H4 card = L241-253 (item cites 241-253 ✅). H2 ledger = L170-180 (item cites 171-180, off-by-one top, GF-1 artifact). §6.2 = exactly 8 fields with enum `pass/blocked/advisory/not_applicable` ✅. §8 `NOT PROVEN` paragraph = L314 (item cites L314 ✅).
- SKILL.md anchors verified: Output Contract last row `diagnosability_hard_stop` (L61, last) ✅; Refs table last row `refs/diagnosability-audit.md` (L546, last) ✅; calibration gate L327 ✅; Wave 5 L385 ✅; Wave 6 L437 ✅; Wave Structure fractional-wave precedent 1.5/1.6/1.7 present ✅.
- report-template.md: four-backtick fence opens L7 closes L203; Follow-up tasks L122; Grounding Gaps L134; Behavior-is-documented rule L233 — all anchors valid; §8 insertion lands inside fence ✅.
- remediation-handoff.md: load-condition L3, `## The user offer` L5, `## Failure modes` table L115 with British "Behaviour" header (Step 2.14 correctly matches spelling) ✅.
- command file: `--output-dir` row L56 text matches Step 2.7's verbatim quote exactly ✅; GF-2 grounds Step 2.6's frontmatter-`description` edit decision ✅; POST-reflect item matches GF-3 authoritative shape ✅.
- GF-1..GF-6 markers all resolve to real gap-fill content ✅.

## Summary
- Checks passed: 8/8 hard B2 self-containment dimensions (with item-level exceptions noted below)
- Issues found: 6 (1 IMPORTANT, 5 MINOR)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 5.5 (L356) | **B2 atomicity violation.** A single `- [ ]` item spawns **2 verification agents** AND folds the entire fidelity verify→consolidate→re-fix→re-verify loop ("repeat Steps 5.3-5.5 up to 3 cycles") into one item. This is not atomic: it is two agent spawns plus a control-flow loop in one checkbox. Contrast Phase 4, which correctly splits verification into Step 4.12 (structural) + Step 4.13 (content) + Step 4.14 (cycle control). The item cannot be executed without scrolling and conflates 4 distinct actions. | Split into: Step 5.5a (spawn structural verification agent), Step 5.5b (spawn content verification agent), Step 5.5c (read both reports + cycle control / HALT), mirroring the Phase 4 4.12/4.13/4.14 decomposition. |
| 2 | MINOR | Step 2.1 (L184) | **Embedded-prompt completeness — H5 line drift.** The item cites the H5 sub-lists as "trigger list at spec lines 270-280, acceptable off-path forms at 282-288, waiver standard at 290-294." Actual live spec: trigger bullets L272-280, acceptable forms L284-288, waiver L292-294 (off by ~2 at the top of each range). This is the GF-1 off-by-one/two artifact the task itself warns about, and the item ALSO cites the named subsections ("acceptable off-path forms", "waiver standard") as text anchors, so it remains executable — but the stale line numbers invite an executor to grab the wrong leading line. | Drop the absolute line numbers in favor of the (already-present) named-heading text anchors, or correct to 272-280 / 284-288 / 292-294. Low risk because TEXT anchoring is mandated. |
| 3 | MINOR | Steps 2.1-2.5, 2.8, 2.12 (multiple) | **Embedded-prompt completeness — line numbers cited but declared unreliable.** Items pervasively cite exact spec line ranges (e.g. "spec lines 136-151", "171-180", "241-253", "202-211") for byte-faithful reproduction, while Key Constraints + GF-1 simultaneously declare line numbers off-by-one artifacts and mandate TEXT anchoring. The dual signal is internally tension-laden: an item is most self-contained when its reproduction anchor is unambiguous. Most ranges verified accurate (H1, H4, §6.2, §8) but H2 (171-180 vs 170-180) and H5 (Issue 2) drift. | For each reproduce-verbatim item, lead with the section name + first/last field TEXT as the anchor and mark line numbers explicitly "(approximate, anchor on text)". |
| 4 | MINOR | Step 2.12 (L242) | **Spec-divergence embedded in instruction without flagging it AS a divergence inside the prompt body.** The item instructs the executor to render `Closure verdict: pass \| blocked \| advisory \| not applicable` but the live spec §8 block (L311) reads `Closure verdict: pass \| blocked \| advisory` (no `not applicable`). The justification (GF-5 / Open Question #2) is real and legitimate, and the item does append "per GF-5" — but a fidelity QA agent in Phase 5 reading spec-vs-output will flag this as a non-faithful reproduction unless the divergence is called out as an *intentional additive reconciliation* at the point of instruction. | Add an inline parenthetical in Step 2.12: "(NOTE: spec §8 omits `not applicable`; adding it is the intentional GF-5 reconciliation, NOT a fidelity error — fidelity agents must not flag it)". Mirror the same note in Step 2.8 and the hub-ref Step 2.1. |
| 5 | MINOR | Step 4.14 (L332) | **B2 atomicity — embedded loop control.** Like Issue 1, this item folds "repeat the consolidation→serialized-fix→verification cycle (Steps 4.10-4.13)" into one checkbox with an embedded cycle counter and HALT branch. It is borderline acceptable as a dedicated control item, but it instructs re-execution of four *other* items from within one item, which is a self-containment grey zone (the executor must re-enter prior items). | Acceptable to keep as a control item, but reword so it is explicit that cycles 2-3 RE-RUN the existing Step 4.10-4.13 items (not new inline work), and the HALT path is the terminal action of THIS item. |
| 6 | MINOR | Step 2.6 (L214) vs spec §5.1 | **Embedded-prompt scope slightly exceeds the cited spec bullet — grounded only via GF-2.** Spec §5.1 bullet 1 says "Update the behavioral summary" (no mention of frontmatter `description:`). Step 2.6 instructs editing BOTH frontmatter `description:` AND `## Behavioral Summary`. This is correctly grounded in GF-2 (which the item cites), so it is not fabrication — but a reader checking the item against the *spec bullet alone* would see an unsupported expansion. The grounding lives only in the research cite, not restated in-item. | Add one clause to Step 2.6: "(the frontmatter `description:` is the operator-facing advertising surface per GF-2 — spec §5.1 bullet 1's 'behavioral summary' maps to this command-layer surface)". |

## Actions Taken
None — `fix_authorization: false`. All issues documented for the orchestrator/fix cycle.

## Confidence Gate

- **Confidence:** "Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
  - All 8 B2 dimensions checked with tool evidence (grep on task file + Read of task file + Bash verification of every cited spec line range, SKILL/refs anchor, and file existence). Confidence is on the *checklist coverage*, not a claim the task is defect-free — 6 issues were found.
- **Tool engagement:** "Read: 3 | Grep: 0 (folded into Bash grep) | Glob: 0 (folded into Bash ls/glob) | Bash: 6"
  - Tool calls (9+ total) > 8 checklist items → engagement minimum satisfied. Each Bash call mapped to a specific verification: file existence, spec line ranges (H1/H2/H4/§6.2/§8), SKILL anchors, report-template/remediation anchors, GF markers, B2 red-flag scan, agent-prompt embedding scan.
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations

Before `/task` execution:
1. **Fix Issue 1 (IMPORTANT):** split Step 5.5 into 5.5a/5.5b/5.5c to restore B2 atomicity, mirroring Phase 4's 4.12/4.13/4.14 decomposition.
2. Address Issues 2-4 (line-number drift, intentional-divergence flagging) so Phase 5 fidelity agents do not raise false positives that burn fix cycles.
3. Issues 5-6 are low-risk polish; acceptable to defer, but Issue 4's fidelity-divergence note is cheap insurance against a self-inflicted Phase 5 FAIL loop.

The task is fundamentally executable and accurately grounded in spec + research. The FAIL is driven by the one IMPORTANT atomicity violation (Step 5.5) under zero-tolerance gating; the remaining MINOR items are quality-drift hardening.

## QA Complete

---
VERDICT: FAIL

Severity-rated issues:
- IMPORTANT (1): Step 5.5 B2 atomicity violation — 2 agent spawns + a 3-cycle verify/fix loop folded into one checklist item.
- MINOR (5): H5 line-number drift (Step 2.1); pervasive unreliable line-number citations vs TEXT-anchor mandate (Steps 2.1-2.5/2.8/2.12); intentional spec-§8 divergence not flagged in-item for fidelity agents (Step 2.12, also 2.8/2.1); Step 4.14 embedded loop control; Step 2.6 scope expansion grounded only via external GF-2 cite.
