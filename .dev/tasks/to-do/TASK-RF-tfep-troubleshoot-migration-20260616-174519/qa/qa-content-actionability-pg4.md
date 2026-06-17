# QA Report — Content Actionability (Phase 4, Wave 5 step 4.5 emission)

**Topic:** TFEP return-contract emission step actionability
**Date:** 2026-06-16
**Phase:** doc-qualitative (actionability lens, adversarial)
**Fix cycle:** N/A (report-only; `fix_authorization: false`)
**Target:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` line 471 (Wave 5 step 4.5)

---

## Overall Verdict: FAIL

The emission step is *mostly* actionable — the field set, the YAML wire-shape, and
most field sources are recoverable from the Output Contract (SKILL.md L37-91) and the
report-template TFEP Consumer block (refs/report-template.md L156-168). But an
implementer hits **5 genuine under-specifications**, one of them blocking: the step
names `tasklist_insertion_path` in the wire schema yet gives **no production rule** for
it anywhere in the skill. An implementer cannot emit that field deterministically.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 7 named fields are emittable | FAIL | 6 of 7 have a derivable source; `tasklist_insertion_path` has none (see I-1) |
| 2 | YAML wire-shape is defined | PASS | refs/report-template.md L160-168 gives the exact YAML key/value template the contract echoes |
| 3 | Emission gated on `caller=task-unified` | PASS | L471 header + L148 ("When `caller=task-unified`, mark Wave 5 to emit") + L481 exit criteria all agree |
| 4 | Each field's source named | FAIL | Step 4.5 sources status/test_is_wrong/remediation_target/root_cause/solution/recommended_escalation but is SILENT on `tasklist_insertion_path` AND `status` (see I-1, I-5) |
| 5 | No `--fix` / no remediation applied | PASS | L471 NOTE is explicit; L481 "If `--fix` is not set... STOP"; matches task-protocol remediation-ownership decision |
| 6 | `return_contract_path` recorded in SUMMARY footer | PASS | L467 footer field `return_contract_path: <abs-path\|none>` exists; L471 instructs recording it |
| 7 | Path form is unambiguous | FAIL | abs/repo-relative contradiction between `<output-dir>` paths and adapter-field "abs path" typing (see I-2) |
| 8 | `recommended_escalation` derivation is executable | FAIL | Inputs named (status+tier+confidence) but NO mapping rule to the 4 enum values (see I-3) |
| 9 | `remediation_target` derivation is executable | PASS | L75 gives the full composition rule from the asymmetric-cost gates incl. the `none`/halt case |
| 10 | Output dir exists at emission time | PASS | L130 creates `<output-dir>/` in Wave 0; REPORT.md already written there by step 2 |

## Summary
- Checks passed: 6 / 10
- Checks failed: 4
- Critical issues: 1 (I-1)
- Important issues: 3 (I-2, I-3, I-4)
- Minor issues: 1 (I-5)
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | CRITICAL | SKILL.md L471 + L74 | `tasklist_insertion_path` is named in the wire schema (L471, template L164) and defined as a *type* (L74: "Path to the adjudicated remediation-plan block the caller should insert"), but **no step anywhere tells the implementer how to PRODUCE this path or what file/block it points to.** Step 4.5 explicitly enumerates sources for the other 6 fields and skips this one. The report template has no "remediation-plan block" artifact, and `task_file_path` (Tier-3 MDTM) is explicitly distinct. An implementer cannot emit this field deterministically — they would either hardcode `null` or invent an artifact. | Add a production rule to step 4.5: define WHICH file the path points to (candidate: a new `<output-dir>/remediation-plan.md` rendered from the Proposed Fix section, OR reuse the REPORT.md `## Proposed Fix` block via anchor), and the null condition (already stated: null when `recommended_escalation: halt` / no remediation). Without naming the source artifact this field is unimplementable. |
| I-2 | IMPORTANT | SKILL.md L471 vs L74 vs L50 vs template L164 | Path-form contradiction. Step 4.5 writes to `<output-dir>/return-contract.yaml`; `tasklist_insertion_path` is typed "(abs path)" (L74) and the YAML template shows `<abs-path\|null>` (L164); but `test_file_path` is "repo-relative" (L50) and the diagnosability/doc-context cards are "repo-relative" (L52, L59-60). The 7-field set does not include `test_file_path`, but `root_cause_summary`/`solution_summary` may quote file paths, and the consumer (task-protocol) must join paths. An implementer does not know whether YAML paths are abs or repo-relative without cross-referencing 4 scattered rows. | State the path convention for the emitted YAML inline in step 4.5: "all path-valued fields in return-contract.yaml are ABSOLUTE (joined against the audit-log repo root)" — and reconcile against the repo-relative convention used by sibling fields, or explicitly note the divergence is intentional. |
| I-3 | IMPORTANT | SKILL.md L471 + L73 | `recommended_escalation` derivation names the INPUTS (`status`+`tier_reached`+`confidence`+Next Steps) but provides **no mapping** from those inputs to the 4 enum values (`none\|retry\|escalate_depth\|halt`). L73 defines what each enum MEANS but not WHEN to pick it. Two implementers will produce different escalations for the same (status, tier, confidence) triple. | Add a deterministic decision rule (truth table or ordered if/else): e.g. `status=failed OR diagnosability_hard_stop → halt`; `status=partial AND confidence<threshold → escalate_depth`; `status=partial AND tier<2 → retry`; `status=success → none`. Cite the confidence threshold (the escalation-rubric.md value). |
| I-4 | IMPORTANT | SKILL.md L471 (field set) vs L75 | The 7-field wire set OMITS `test_file_path`, but `remediation_target=test` is defined as "paired with `test_file_path`" (L75) and the asymmetric-cost contract says the remediation target IS the test file. A TFEP consumer that receives `remediation_target: test` has no path to the test file in the contract — it must reach back into REPORT.md or the broader Output Contract. Either this is an intentional scope cut (consumer reads `test_file_path` from the dict, not the YAML) or an omission. The instruction does not say which. | Clarify in step 4.5 whether `test_file_path` is intentionally excluded from the YAML (and the consumer obtains it elsewhere) or should be added. If `remediation_target: test` is emittable without the path, state where the consumer gets the target file. |
| I-5 | MINOR | SKILL.md L471 | `status` is listed as a wire field but step 4.5 gives no source sentence for it (unlike the other 6). It is trivially the Output Contract `status` already computed in step 3/footer (L457), so this is recoverable — but the enums differ: footer `status` is `<success\|partial>` (L457) while the YAML template allows `<success\|partial\|failed>` (template L161, L43). An implementer may be unsure whether `failed` can appear in the YAML when the footer never emits it. | Add "`status`: copy from the Output Contract `status` (step 3)" and reconcile the `failed` enum: confirm whether a `failed` run reaches step 4.5 at all (if it STOPs earlier, `failed` is unreachable in the YAML and should be dropped from the template). |

## Adversarial Axis Notes (>=5 under-specifications demanded)
The stance required finding at least 5. Found 5 (I-1..I-5), spanning:
- **Missing production rule** (I-1, blocking) — a field with a type but no emitter.
- **Ambiguous path semantics** (I-2) — abs vs repo-relative unreconciled.
- **Named-but-unmapped derivation** (I-3) — inputs without a function.
- **Schema/contract gap** (I-4) — `remediation_target: test` with no companion path in the wire set.
- **Source-silent field + enum mismatch** (I-5) — `status` un-sourced; `failed` reachability unclear.

## Self-Audit (MANDATORY)
1. **Factual claims verified against source:** 10+ — every field definition (L43-77), the
   derivation rules (L79-91), the gating (L148, L471, L481), the SUMMARY footer field
   (L467), the YAML wire template (template L160-168), the report sections
   (Diagnosis L65, Proposed Fix L85, Next Steps L146), output-dir creation (L130), and the
   absence of any `tasklist_insertion_path` production rule (grep -rn across the whole skill
   dir returned only the type-definition and the wire-template echo — no emitter).
2. **Files read:** `SKILL.md` (L37-95, L420-548), `refs/report-template.md` (L85-215),
   plus full-tree grep across `refs/` for `tasklist_insertion_path`, `return-contract`,
   `recommended_escalation`, asymmetric-cost gates.
3. **Why trust this (not 0 issues):** The blocking finding (I-1) was confirmed by a negative
   search: `grep -rn "tasklist_insertion_path\|adjudicated remediation\|remediation-plan block" .`
   returned ONLY the L74 type-definition and the L164 wire-template echo — zero hits for any
   instruction that WRITES the file or RENDERS the block. A field that is typed and echoed but
   never produced is the textbook actionability gap.
4. **Web research:** None performed (this review is entirely local-file-bound). Tavily-first
   rule not triggered; no fallback occurred.

## Confidence
Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 3 | Grep/Bash: 4 | Glob: 0
(Tool calls >= checklist items; no padding — each call targeted a specific field/source claim.)

## Recommendations
Block the emission step until I-1 is resolved (it is unimplementable as written). I-2/I-3/I-4
should be fixed before an implementer touches the code or two implementations will diverge on
path form and escalation values. I-5 is a cleanup. All 5 must be resolved before this passes
(no severity is exempt per the actionability gate).

## QA Complete
