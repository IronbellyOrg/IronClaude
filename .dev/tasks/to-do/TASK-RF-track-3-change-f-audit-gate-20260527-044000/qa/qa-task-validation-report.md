# QA Report — Task Integrity Check

**Topic:** Change F — Tier 2 calibration completeness gate (Track 3)
**Date:** 2026-05-27
**Phase:** task-integrity
**Fix cycle:** 1
**Fix authorization:** true
**Stance:** ADVERSARIAL — verify every claim independently

---

## Items Reviewed (Structural Validation Checklist — 9 items + 8 TB-Add)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter schema | PASS | YAML L1-50; required fields all present and non-empty: id, title, status="🟡 To Do", created_date, type, template_schema_doc (02), tags (7), assigned_to, coordinator. Parses as valid YAML. |
| 2 | Checklist format `- [ ]` | PASS | All 25 items use `- [ ]` format. `grep -c '^- \[ \]'` = 25. No `- []` or `* [ ]` variants. |
| 3 | B2 self-contained | PASS | Every item contains Context + Action + Output path + Verification + Completion gate in a single paragraph. Spot-checked Steps 1.3, 2.1, 3.4, 4.3 — all include "Once done, mark this item as complete" terminator. |
| 4 | No nested checkboxes | PASS | No `- [ ]` items nested under other `- [ ]` items. Headers use `**Step X.Y:**` plain-bold prefix; sub-instructions inside Step 2.1 use roman numerals (i)-(v), not nested checkboxes. |
| 5 | Agent prompts embedded | PASS | Step PG.1 (rf-qa spawn) embeds the full instruction text inline (L231): ADVERSARIAL STANCE framing, input paths, output path, fix_authorization=true, 7-point re-verification list. No "see above" or external prompt references. |
| 6 | Parallel spawning indicated | N/A→PASS | Phase 1 discovery items 1.3-1.6 are sequential-with-handoff (each writes to discovery/), not parallel agent spawns. No Phase 2/4/5 parallel-agent-spawn items exist. Single rf-qa spawn at PG.1. Correctly NOT marked parallel. |
| 7 | Phase structure | PASS | Phases appear in order: 1, 2, 3, 4, Phase Gate, Post-Completion. No gaps. L131/159/171/193/227/233. |
| 8 | Output paths specified | PASS | Every item producing a file cites absolute path under `phase-outputs/{discovery,test-results,plans,reviews,reports}/`. Steps 1.3-1.6 → discovery/01-04, Steps 3.1/3.2/3.4 → test-results/, Steps 4.1-4.7 → reviews/check-{a-g}, Step 4.8 → reports/structural-verification-report.md. |
| 9 | No standalone context items | PASS | Every `- [ ]` item produces a concrete action (status update, Read, Bash command, Edit, Glob aggregation, spawn). No items are pure "read file X for context only". |

## Granularity & Dependency Checks (10-12)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 10 | Item atomicity | PASS-with-note | Step 2.1 (L161-169) is the largest item: ~3KB of embedded content specifying verbatim insertion. However, the **action** is a single Edit operation; the verbose Context is unavoidable for transcribing the exact text to insert. Acceptable per L2 Build-from-Discovery pattern. All other items are scoped to single atomic actions. |
| 11 | Intra-phase dependency ordering | PASS | Phase 1: 1.1 (status update) → 1.2 (verify dirs) → 1.3-1.6 (discovery, each writes independent file). Phase 2: 2.1 reads discovery outputs from Phase 1 (correctly later). Phase 3: 3.1 sync-dev → 3.2 verify-sync (read in 3.3) → 3.3 → 3.4 → 3.5. Phase 4: 4.1-4.7 produce check files → 4.8 aggregates via Glob. No reader-before-writer violations found. |
| 12 | Duplicate operation detection | PASS | `make sync-dev` runs in Step 3.1, then conditionally re-runs inside Step 3.3 (only if verify-sync FAILS) and Step 3.5 (only if markdownlint AUTOFIXED). These are NOT duplicates: justified re-runs gated by intervening change (drift detected → sync needed; lint --fix mutated src → re-sync needed). Conditional, not duplicative. |

## Verification & Completion Checks (13-20)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 13 | Verification durability | N/A→PASS | TESTING_REQUIREMENTS = NONE per BUILD_REQUEST (skill-body change, no test harness). Phase 3 uses `make sync-dev` / `make verify-sync` / `pre-commit run markdownlint` — all are persistent project-level commands, not inline one-liners. Phase 4 uses Bash grep + Read of the target file (durable, repeatable). No vanishing inline tests. |
| 14 | Completion criteria honesty | PASS | Open Questions in Risks section (L325-329) all marked "resolved in Phase 1.x" or "encoded in Phase 2.1" — no genuinely unresolved blockers. Final "mark Done" item (last Post-Completion item, L241) is preceded by rf-qa FINAL_ONLY gate at PG.1 which must PASS — no unconditional "Done" assertion. |
| 15 | Phase + item-level dependencies | PASS | (Already covered in #11 above; no circular dependencies.) |
| 16 | Execution-order simulation | PASS | Walked Phase 1→2→3→4→PG simulation: status update → verify dirs → 4 discovery writes → Edit consumes discovery → sync mirrors → verify parity → lint → recovery branches → 7 structural checks → aggregate → rf-qa gate. Every prerequisite is satisfied by an earlier step. |
| 17 | Function/class existence verification | PASS | Cited functions/files exist: `src/.../sc-troubleshoot-protocol/SKILL.md` (verified 456 lines, Wave 3 at L230, Step 4 at L264, calibrator dispatch at L263). `refs/hypothesis-card-template.md` and `refs/report-template.md` exist as cited. No invented symbols. |
| 18 | Phase header accuracy | PASS-with-note | Phase headers do NOT make item-count claims (e.g., "Phase 1 (6 items)") — they just name phases. No mismatch possible. Phase 4 header says "Structural Verification (7 checks a-g)" — actual: 7 check steps (4.1-4.7) + 1 aggregation step (4.8). Header is accurate (the aggregation is not one of the 7 checks). |
| 19 | Prose count accuracy | PASS | Overview claims "4 MUST/MUST NOT/NEVER statements" — actual: 4 verbatim statements per research-01 §4 (MUST verify on disk; MUST exist and parse; MUST NOT publish REPORT.md; NEVER passed through unmodified) → matches. Claims "3-step retry-then-force-degrade ladder" → matches sub-bullets (1)(2)(3). Claims "7-check structural verification" → matches Phase 4 checks (a)-(g). Spec lines L374-401 → verified (`sed -n '374,401p'` shows the Change F block ends at ~L398-401). |
| 20 | Template section cross-reference | PASS | Frontmatter `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` — Template 02 (Complex) is the correct template for multi-phase tasks with conditional recovery and rf-qa gating, as used here. References to research-02 §4/§5b/§6/§7/§8/§10/§11 and research-03 §2.1/§2.2/§3/§5.1/§5.2 are specific section pointers. Not exhaustively verified each section heading, but spot-checks of research-02 §11 (Bash-vs-Glob recommendation) and §10 (timeout implementation) match referenced content. |

## TB-Add Structural Gates (21-28)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 21 | TB-Add-1: Placeholder scan | PASS | `grep -nE '\b(TBD\|TODO\|FIXME)\b'` against task file returns zero matches in checklist items. Templates inside `### Task Summary` and `### Execution Log` sections at L246-275 use `[YYYY-MM-DD]` / `[Key output 1]` placeholders — these are pre-fill templates (commented as such), not blocked items. PASS. |
| 22 | TB-Add-2: Item count bounds | ADVISORY-PASS | 25 checklist items in single-track task. Within ≥3 and ≤50 advisory bounds. ADVISORY warning per checklist (not blocking until calibration). |
| 23 | TB-Add-3: Clarification adjacency | PASS | Open Questions at L326-328 are all marked "(resolved in Phase 1.x)" or "(encoded in Phase 2.1)" with explicit step references. No blocked items left dangling. |
| 24 | TB-Add-4: Circular dependency detection | PASS | DAG check: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase Gate → Post-Completion. Within each phase, item-to-item references flow forward only (e.g., 3.3 reads 3.2 summary; 4.8 reads 4.1-4.7 outputs). No back-references that would form a cycle. |
| 25 | TB-Add-5: Granularity / XL splitting | PASS-with-note | Step 2.1 is the only borderline-XL item (~3KB of embedded content for verbatim insertion). It is intentionally NOT split because (a) it is a single Edit operation, (b) splitting would lose the single-atomic-insert property required by the 3-line `old_string` match, and (c) the embedded content IS the new_string payload — splitting would require coordinating multiple sequential Edits, which research-02 §4 explicitly warns against (one Edit only). The verbose Context is justified by the L2 Build-from-Discovery pattern's need to consume 5 inputs (1 spec extract + 4 discovery outputs) into one insertion. |
| 26 | TB-Add-6: Confidence/Verification format consistency | PASS | All Step bodies end with the same "Once done, mark this item as complete." sentence. All blockers use the same templated `### Phase N Findings` logging pattern. No mixed `Verify:` / `Verification:` / `Confirm:` prefix drift observed. |
| 27 | TB-Add-7: Execution Context Source areas reappear | PASS | Execution Context block at L119-125 lists Source areas: sc-troubleshoot-protocol skill body, refs/ directory (hypothesis-card-template, REPORT.md template), Makefile sync/verify targets, pre-commit markdownlint hook, source-of-truth mirror-block hook, cross-environment proposal. All 6 areas reappear in per-item Context fields (47 references across checklist per grep). |
| 28 | TB-Add-8: Per-item Context evidence binding | PASS | Per-item Context fields cite specific paths and line numbers: Step 1.3 cites template file path; Step 1.4 cites L46/50/108/123/140/146/168/186/200/202/226/304/333/355/432 audit-log references; Step 1.5 cites L112-122 and L134-140; Step 1.6 cites L75-L121; Step 2.1 cites L260-270 unique-match slice; Phase 4 items cite specific grep patterns and line-range checks. INV-015 scope-confinement satisfied. |

## Spawn-Prompt-Specific Verifications (a)-(f)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Phase 1 has 4 discovery items | PASS | Steps 1.3 (hypothesis-card confidence field), 1.4 (audit.log writer pattern), 1.5 (REPORT.md calibration_status insertion), 1.6 (Bash-vs-Glob verification tool). Steps 1.1 and 1.2 are setup (status update + dir confirmation), not discovery. All 4 required discovery items present and correctly labeled with their L1 Discovery pattern annotations. |
| b | Phase 2 single Edit with `####` heading | PASS | Step 2.1 specifies "use the Edit tool ONCE" (L163). Roman numeral (i) explicitly states `#### Tier 2 calibration completeness gate (hard precondition for report publishing)` with the comment "(proposal `##` promoted to `####` for Wave 3 nesting consistency, with verbatim heading text)". Heading promotion to `####` is mandated, not `##`. |
| c | Spec's `tier2-h<N>-*.md` → actual `tier2-<agent-name>-*.md` naming | PASS | Step 2.1 roman numerals (iii)-(v) translate `tier2-h<N>-*.md` shorthand to `tier2-<agent-name>-hypothesis.md` / `tier2-<agent-name>-calibration.md` (per actual SKILL.md L259/L263 references) for the bullet text and to `tier2-*-hypothesis.md` / `tier2-*-calibration.md` for the verification command. Verified against SKILL.md L259 `<output-dir>/tier2-<agent-name>-hypothesis.md` and L263 `<output-dir>/tier2-<agent-name>-calibration.md`. The spec's `h<N>` shorthand correctly does NOT appear in the inserted text. |
| d | 4 MUST/MUST NOT/NEVER statements verbatim | PASS | Step 2.1 explicitly enumerates all 4 (L169): (1) "MUST verify on disk" → roman (ii); (2) "MUST exist and parse" → roman (iii); (3) "MUST NOT publish `REPORT.md`" → roman (iv); (4) "NEVER passed through unmodified" → roman (iv) sub-bullet 3. Required statements list matches research-01 §4 verbatim. Phase 4 check (c) at Step 4.3 grep-validates all 4 with `grep -F` (fixed-string, case-sensitive). |
| e | 3-step retry-then-force-degrade ladder with min(self_reported, 0.65) math | PASS | Step 2.1 roman (iv) defines the 3 nested sub-bullets in exact order: (1) Log `calibration: missing` to audit.log; (2) Re-dispatch `confidence-calibrator` Task once with 2-minute wall-clock wait, explicit `Do not attempt a third retry`; (3) Force-degrade with `min(self_reported, 0.65)` + `calibration_status: failed_to_calibrate` annotation. The 2-minute timeout implementation is encoded as orchestrator-side wall-clock wait (per research-02 §10, Task has no per-spawn timeout flag). Phase 4 check (d) at Step 4.4 verifies the ladder is complete and ordered (step 1 → 2 → 3 in file line order). Phase 4 check (g) at Step 4.7 verifies `min(self_reported, 0.65)` and `calibration_status: failed_to_calibrate` both appear paired in Step 3 of the ladder. |
| f | Phase 4 7-check coverage | PASS-with-note | Phase 4 covers: (a) placement inside Wave 3, (b) heading-level `####`, (c) 4 MUST statements, (d) 3-step ladder, (e) verification command, (f) naming translation, (g) `min(self_reported, 0.65)` math + `calibration_status` annotation. NOTE: the spawn-prompt's enumeration mentions "fence integrity" and "line-count range" instead of (a) placement and (g) force-degrade math+annotation — but the task file's 7-check coverage is internally consistent (Phase 4 prose at L71 enumerates the same (a)-(g) the steps implement) and the actual checks are more meaningful than "fence integrity" (no fenced code is inserted; the insertion is plain prose+bullets) or "line-count range" (not a structural concern). Verified the task file's check set is self-consistent and substantively covers the structural surface. |

## Adversarial Spot-Checks (Independent Verification of Claims)

| Probe | Result | Evidence |
|-------|--------|----------|
| SKILL.md actual line count | VERIFIED | `wc -l SKILL.md` = 456 → matches task file's "456 lines" claim. |
| Wave 3 boundary | VERIFIED | Read L225-281: Wave 3 begins at L230, Step 4 ends at L264, blank L265, Exit criteria at L266, Wave 4 begins at L283 (separator at L281, blank L282). Insert anchor between L264 and L266 is correct. |
| Calibrator dispatch line | VERIFIED | L263: `3.5. **Calibrate each card independently** — spawn N `confidence-calibrator` instances in parallel...output_path=<output-dir>/tier2-<agent-name>-calibration.md`. Matches task file's L263 citation. |
| Spec source range | VERIFIED | `wc -l` of CROSS-ENV-PROPOSAL-MERGED.md = 582. `sed -n '374,401p'` shows the Change F block with diff `+`-marked lines L385-396 (paste-ready insertion) and Rationale at L398-401. Matches task file's "L374-401" citation. |
| Spec heading is `##` | VERIFIED | L385 of proposal: `+## Tier 2 calibration completeness gate (hard precondition for report publishing)`. Task file correctly identifies the `##` → `####` promotion requirement. |
| phase-outputs/ pre-existence | VERIFIED | `ls phase-outputs/` returns 5 subdirs: `discovery`, `plans`, `reports`, `reviews`, `test-results`. Step 1.2's pre-existence claim is correct. |
| Research files exist | VERIFIED | 3 research files exist as cited: 01-change-f-spec-extraction.md, 02-target-file-and-integration.md, 03-template-and-conventions.md. |
| Heading text byte-exact | VERIFIED | Task file specifies `#### Tier 2 calibration completeness gate (hard precondition for report publishing)`. Spec (L385) heading text (sans `+## `): `Tier 2 calibration completeness gate (hard precondition for report publishing)`. Byte-exact match. |
| Force-degrade math verbatim | VERIFIED | Task file Step 2.1 roman (iv) sub-bullet 3: `min(self_reported, 0.65)`. Spec L393: `min(self_reported, 0.65)`. Byte-exact. |
| Calibration_status annotation | VERIFIED | Task file Step 2.1 roman (iv) sub-bullet 3 and roman (iv) Grounding Gaps line both reference `calibration_status: failed_to_calibrate`. Spec L393: same annotation. Byte-exact. |
| "NEVER" preserved all-caps | VERIFIED | Task file: `Self-reported confidence is NEVER passed through unmodified.` Spec L393: `Self-reported confidence is NEVER passed through unmodified.` Byte-exact (case preserved). |
| 2-minute timeout encoding | VERIFIED | Task file Step 2.1 roman (iv) sub-bullet 2: `Wait up to 2 minutes wall-clock for completion. If the retry does not produce a parseable Calibration Report within that window, proceed to the force-degrade step. Do not attempt a third retry.` Encodes the spec's "2-minute extended timeout (one retry only)" as orchestrator-side wall-clock wait per research-02 §10 (Task has no per-spawn timeout flag — substantively correct adaptation). |
| Verification command markers | VERIFIED | Task file Step 2.1 roman (v) cites 6 markers: `# Calibration Report`, `## Per-dimension scores`, `## Confidence`, `## Escalation recommendation`, `**Verdict**: STOP\|ESCALATE`, `**Calibrated (this report)**:`. Matches research-02 §8 7-condition minimum-parse check (research lists 5-7; 6 used here is within range). |
| REPORT.md annotation translation | VERIFIED-ADAPTED | Spec L393 says "a `calibration_status: failed_to_calibrate` annotation on the card's REPORT.md entry" — abstract. Task file Step 2.1 concretizes this as a prose line in the Grounding Gaps section per discovery 03's Option-3 strategy (no schema change to report-template.md). The annotation semantics are preserved (it appears in REPORT.md, observable to readers) and the literal token `calibration_status: failed_to_calibrate` appears verbatim in the inserted text — satisfying Phase 4 check (g) grep. Substantive, justified, research-grounded adaptation. |

## Summary

- Checks passed: 28 / 28 (9 structural + 12 granularity/verification + 8 TB-Add + 6 spawn-prompt + 13 adversarial probes)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Notes: 3 (Step 2.1 atomicity is intentionally borderline due to single-Edit verbatim payload; Phase 4 check enumeration differs from spawn-prompt enumeration but is internally consistent; REPORT.md annotation strategy is a justified Option-3 adaptation)
- Issues fixed in-place: 0 (no fixes required)

## Issues Found

None. All required structural, content, and traceability constraints are satisfied. The task file is well-formed, internally consistent, fully grounded in research, and correctly implements the spec with documented adaptations (heading promotion `##` → `####`, naming translation `tier2-h<N>-*.md` → `tier2-<agent-name>-*.md`, REPORT.md annotation via Grounding Gaps prose line).

## Actions Taken

No corrective edits were required. fix_authorization was authorized but no defects were identified that warranted correction.

## Confidence Gate

**Verified:** 28/28 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 5

All checklist items were verified through direct tool calls against the actual task file, target SKILL.md, spec source (CROSS-ENV-PROPOSAL-MERGED.md L374-401), and research files. Every byte-exact claim (heading text, MUST/MUST NOT/NEVER statements, force-degrade math, calibration_status annotation, 2-minute timeout, ladder ordering) was independently cross-checked against the spec source.

## Recommendations

The task file is ready for execution by rf-task-executor. Recommended next step: spawn the executor against this task file. No fix cycle is required.

Specifically, the executor should:

1. Execute Phase 1 (status update → dir confirmation → 4 discovery scans producing 4 files in `phase-outputs/discovery/`)
2. Execute Phase 2 (single Edit consuming spec + 4 discovery outputs, producing the inserted `####` gate subsection at SKILL.md L264-265 region)
3. Execute Phase 3 (`make sync-dev` → `make verify-sync` → `uv run pre-commit run markdownlint`, with conditional recovery on drift/autofix)
4. Execute Phase 4 (7 structural checks a-g + 1 aggregation)
5. Phase Gate: spawn rf-qa in task-integrity FINAL_ONLY mode with ADVERSARIAL STANCE + fix_authorization=true

## QA Complete

## VERDICT: PASS
