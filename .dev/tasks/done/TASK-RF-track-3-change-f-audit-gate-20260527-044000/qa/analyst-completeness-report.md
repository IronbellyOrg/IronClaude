# Research Completeness Verification — Track 3 (Change F)

**Topic:** Change F — Tier 2 calibration completeness gate in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Date:** 2026-05-27
**Files analyzed:** 3 (`01-change-f-spec-extraction.md`, `02-target-file-and-integration.md`, `03-template-and-conventions.md`)
**Depth tier:** Standard-Deep
**Source spec:** `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` L374-401

---

## Verdict: PASS (0 critical gaps, 2 minor observations)

The 3-file research bundle (a folded variant of the 5-researcher plan in `research-notes.md`) covers every load-bearing element of Change F that the executor needs to produce a Template-02 task file: the verbatim insertion content, the unique-match insertion anchor, the naming-convention translation, the 4 cross-cutting integration concerns (audit.log, REPORT.md schema, calibration-report parsing minimum check, force-degrade math edge cases), the heading-level promotion note, the 2-minute timeout / per-spawn-timeout gap, and the Makefile/pre-commit workflow. No critical gap. Two minor observations are filed as Important for the executor's awareness but do not block synthesis.

---

## Coverage Audit

The `research-notes.md` EXISTING_FILES section listed 3 source files; the SUGGESTED_PHASES enumerated 5 researchers. The actual research bundle folds Researchers 2/4/5 into a single deliverable (`02-target-file-and-integration.md`) — this is documented in the file header ("folded researcher (Target File State + Wave 3 Integration + Audit-Log/REPORT.md Conventions)"). Every research topic listed in RECOMMENDED_OUTPUTS is covered:

| Scope Item (from research-notes.md) | Covered By | Status |
|--|--|--|
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` byte state + Wave 3 anchor | `02-target-file-and-integration.md` §1-4 | COVERED |
| `src/superclaude/agents/confidence-calibrator.md` referenced for "must parse as a Calibration Report" check | `02-target-file-and-integration.md` §8 | COVERED |
| `CROSS-ENV-PROPOSAL-MERGED.md` L374-401 spec extraction | `01-change-f-spec-extraction.md` §1-8 | COVERED |
| Source Spec Extraction (Researcher 1) | `01-change-f-spec-extraction.md` | COVERED |
| Target File State + Wave 3 anchor (Researcher 2) | `02-target-file-and-integration.md` §1-4 | COVERED (folded) |
| Template & Conventions (Researcher 3) | `03-template-and-conventions.md` §1-7 | COVERED |
| Wave 3 Integration Points (Researcher 4) | `02-target-file-and-integration.md` §5, 9, 10, 11 | COVERED (folded) |
| Audit Log + REPORT.md (Researcher 5) | `02-target-file-and-integration.md` §6, 7 | COVERED (folded) |
| Sibling-artifact naming convention | `02-target-file-and-integration.md` §5 (b) | COVERED |
| Glob-vs-Bash tool-surface choice | `02-target-file-and-integration.md` §11 | COVERED |
| Force-degrade math edge cases | `02-target-file-and-integration.md` §9 | COVERED |
| 2-minute timeout retry mechanics | `02-target-file-and-integration.md` §10 | COVERED |
| Heading-level promotion `##` → `####` | `01-change-f-spec-extraction.md` §2; `03-template-and-conventions.md` §5.1 | COVERED |
| Template 02 (Complex) fit | `03-template-and-conventions.md` §1 | COVERED |
| Makefile sync-dev / verify-sync workflow | `03-template-and-conventions.md` §2 | COVERED |
| Markdownlint + block-claude-generated-mirrors hooks | `03-template-and-conventions.md` §3, 4 | COVERED |
| MUST / MUST NOT / NEVER phrasing patterns | `03-template-and-conventions.md` §5.3 | COVERED |
| Change B precedent for re-usable workflow | `03-template-and-conventions.md` §7 | COVERED |

**Coverage verdict:** Every research-notes scope item resolves to at least one section in the 3 research files. The folded-researcher decision is explicit (not silent) — `02-target-file-and-integration.md` titles itself a "folded researcher" and includes all three original Researcher-2/4/5 topics in numbered sections. No scope item is orphaned.

---

## Evidence Quality

| Research File | Evidenced Claims | Unsupported Claims | Quality Rating |
|--|--|--|--|
| `01-change-f-spec-extraction.md` | High — every quoted block is cited with proposal line numbers (L374, L376, L378, L380, L385, L387, L389, L390-393, L395, L398, L406); MUST/MUST NOT table is line-cited; rationale block is byte-quoted | None observed | Strong |
| `02-target-file-and-integration.md` | High — every SKILL.md claim is line-cited (L16, L26, L37, L73, L91, L129, L152, L190, L210, L230, L259, L263, L264, L266, L271-279, L283, L312, L359 etc.); confidence-calibrator.md cited (L57-93); REPORT.md template cited (L1-141, L9-21, L114-122, L134-140); structural map produced via `grep -nE` verification | None observed | Strong |
| `03-template-and-conventions.md` | High — Makefile cited (L108-163, L165-301); `.pre-commit-config.yaml` cited (L70-82, L98-109); Template 02 cited (L713-805 with sub-ranges L737-747, L749-759, L773-783, L785-797); skill-body conventions cited (L16, L26, L37, L73, L91, L129, L152, L190, L210, L230, L283, L312, L359); Change B precedent cited (L226-238, L267-268, L275) | None observed | Strong |

**Aggregate:** All three files achieve a Strong evidence-quality rating. Every architectural / structural claim is backed by a file-and-line citation. There are no vague "the system uses X architecture" assertions without grounding.

---

## Documentation Staleness

Per CLAUDE.md and standard `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tagging convention, doc-sourced claims must carry a verification tag. In this research bundle:

| Claim Type | Source | Tag Required? | Status |
|--|--|--|--|
| Wave 3 spans L230-281 (vs research-notes' L230-282) | `02-target-file-and-integration.md` §2 | Self-corrected via Read | OK — explicitly noted "research-notes' L230-282 is off by one" |
| Calibrator dispatch is Step 3.5 at L263 | `02-target-file-and-integration.md` §3 | Verified | OK — verified by Read |
| `tier2-<agent-name>-hypothesis.md` naming (vs spec's `tier2-h<N>-*.md`) | `02-target-file-and-integration.md` §5 (b) | Verified | OK — explicitly flagged "spec is illustrative; actual naming differs" |
| `Task` tool has no per-spawn timeout flag | `02-target-file-and-integration.md` §10 | Verified | OK — "Research outcome" framing makes the verification explicit |
| `maxTurns: 25` in calibrator frontmatter | `02-target-file-and-integration.md` §10 | Cites `confidence-calibrator.md` L7 | OK — line-cited |
| Markdownlint hook `args: ['--fix']` | `03-template-and-conventions.md` §3 | Cites `.pre-commit-config.yaml:75` | OK — line-cited |
| Change B execution log facts (L267, L268, L275) | `03-template-and-conventions.md` §3, §7 | Cites task file line numbers | OK — line-cited |

**No `[CODE-CONTRADICTED]` claims appear** — the research files self-corrected discrepancies inline (e.g., the L230-281 vs L230-282 off-by-one; the `tier2-h<N>-*.md` vs `tier2-<agent-name>-*.md` naming gap) rather than letting them stand. All architectural claims trace to verified file contents.

**Staleness verdict:** No tag-missing doc-sourced claims; no unflagged `[CODE-CONTRADICTED]` claims propagated downstream. PASS.

---

## Completeness (Per-File Structural Check)

| Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
|--|--|--|--|--|--|
| `01-change-f-spec-extraction.md` | Complete (line 7) | §9 Summary present | Implicit — "Out of scope" section at end of §9 acts as gap declaration; explicit gaps deferred to siblings | §9 Summary + "Provenance line for executor" | Complete |
| `02-target-file-and-integration.md` | Complete (line 5) | "Summary" section at L329 | Distributed across §5 (b) gap flag, §7 schema-change flag, §9 missing-self_reported ambiguity, §10 timeout flag absence | Summary section enumerates all key findings as bullets | Complete |
| `03-template-and-conventions.md` | Complete (line 4) | "Summary" section at L257 | Distributed across §6 "Known Gotchas" (G1-G6) | Summary section + Section 7 differences table | Complete |

All three files declare Status: Complete. All three have a Summary block. Gaps are surfaced inline (in §6 Known Gotchas, §5(b) naming-gap flag, §7 schema-change flag, §9 missing-self_reported ambiguity, §10 timeout flag absence) rather than in a single "Gaps and Questions" section — this is a stylistic deviation from a strict template but does not lose any gap content.

**Completeness verdict:** PASS.

---

## Contradictions Found

**Inter-file:** None observed. The three files form a consistent narrative — §2 of `01-change-f-spec-extraction.md` flags the heading-level promotion `##` → `####`, and §5.1 of `03-template-and-conventions.md` confirms `####` is conventionally valid (cross-skill spot-check vs `sc-tasklist-protocol` L492) and also notes that `sc-troubleshoot-protocol/SKILL.md` currently uses bolded-paragraph-headers for in-wave subsections rather than `####`. This is **not** a contradiction — it is a faithful presentation of two valid options.

**Intra-file:** None observed.

**Spec-vs-actuals (correctly surfaced):**

- Spec's `tier2-h<N>-*.md` shorthand vs actual `tier2-<agent-name>-hypothesis.md` — both files acknowledge this with translation guidance (`01-change-f-spec-extraction.md` §2 and §6 defer the call to Researcher 4; `02-target-file-and-integration.md` §5(b) executes the translation).
- Spec's "2-minute extended timeout (one retry only)" vs Claude Code `Task` tool's lack of a per-spawn timeout flag — `02-target-file-and-integration.md` §10 surfaces this and proposes the orchestrator-wait-loop encoding.

These are spec-vs-implementation gaps, not file-vs-file contradictions, and they are correctly surfaced rather than silently resolved.

---

## Compiled Gaps

### Critical Gaps (block synthesis)

None.

### Important Gaps (affect quality)

1. **Hypothesis-card `confidence` field name is unconfirmed** — `02-target-file-and-integration.md` §9 ends with "the hypothesis card's self-reported confidence field name is **not explicitly specified** in the SKILL.md or the calibrator agent" and recommends reading `refs/hypothesis-card-template.md` to confirm. The task file should include a Phase-1 discovery item to read that file before the executor implements the force-degrade math parser. The research did not perform this read.

2. **`audit.log` writer-tool is unspecified** — `02-target-file-and-integration.md` §6 records "**Writer mechanism: not explicitly specified.**" The skill body says "open audit log" / "emit ... header" but names no tool. The research correctly does NOT invent a new convention; the task file should adopt the inferred free-form append pattern (e.g., `Bash` with `printf >> <output-dir>/audit.log`) and document the inference in the task file. The executor needs to surface this choice during Phase 1 / Phase 2 build.

### Minor Gaps (must still be fixed)

1. **REPORT.md per-card calibration_status slot is recommended but not pre-decided** — `02-target-file-and-integration.md` §7 enumerates 3 viable insertion points (header field, Audit section, Grounding Gaps) and recommends Option 3 (Grounding Gaps prose line + Confidence header note). The recommendation is well-reasoned but the final call should be made/confirmed by the executor in Phase 2 build, with a documentation decision recorded in the task log. Not a blocker — the research provides everything needed for the decision.

2. **Anchor placement has two viable candidates** — `02-target-file-and-integration.md` §3 enumerates "after Step 3.5 / between calibrate and distill (Step 3.6)" and "after Step 4 / before Exit criteria" and recommends the latter. The recommendation is well-reasoned (positions gate as last Wave 3 action before exit, downstream of dispatch step it gates, preserves existing numbered flow) but is one of two valid choices. The task file should explicitly carry forward the recommendation with the unique-match `old_string` slice already provided in §4.

---

## Key Verification Foci (from spawn prompt)

| Focus | Coverage | Status |
|--|--|--|
| Spec-extraction captures all MUST/MUST NOT statements | §4 table in `01` lists all 4 normative statements verbatim with proposal line citations (L387, L389, L390, L393) | COVERED |
| 3-step retry-then-force-degrade ladder | §5 table in `01` enumerates Log → Retry-once → Force-degrade with inputs/side-effects/stopping-condition for each step + 5 key invariants | COVERED |
| Verification command pattern | §6 in `01` decomposes the pattern into trigger-timing / iteration-scope / exclusion / assertion / fallback | COVERED |
| Rationale paragraph | §7 in `01` quotes the rationale verbatim (proposal L398) with 5 anchor points (empirical evidence, failure mode, closure claim, load-bearing weight, provenance) | COVERED |
| Precise Wave 3 insertion anchor (Step 3.5 calibrator dispatch at L263; recommended anchor after Step 4 at L264 before Exit criteria at L266) | §3 + §4 in `02` identify Step 3.5 at L263, Step 4 at L264, Exit criteria at L266, and provide the unique-match 3-line `old_string` slice for the Edit operation | COVERED |
| Spec's `tier2-h<N>-*.md` → actual `tier2-<agent-name>-hypothesis.md` naming translation | §5 (b) in `02` provides the explicit before/after table | COVERED |
| audit.log conventions | §6 in `02` inventories 11 audit.log references in SKILL.md (L46, L50, L108, L123, L140, L146, L168, L186, L200, L202, L226, L304, L333, L355, L432), infers path `<output-dir>/audit.log`, and proposes 3 free-form append patterns for Change F's new entries | COVERED |
| REPORT.md schema | §7 in `02` cites template L1-141 with header-field list (L9-21) and Audit section (L134-140) and Grounding Gaps (L112-122); enumerates 3 insertion-point options for `calibration_status` annotation | COVERED |
| Calibration-report-parsing minimum check | §8 in `02` enumerates 7 grep-able conditions (file exists, starts with `# Calibration Report`, contains 3 named headings, contains `**Verdict**:` with STOP/ESCALATE, contains parseable `**Calibrated (this report)**:` float) | COVERED |
| Force-degrade math edge cases | §9 in `02` provides edge-case table covering 8 cases (normal degrade, at-floor, below-floor, 1.0, 0.0, null/missing, non-numeric, out-of-range malformed) | COVERED |
| Heading-level promotion `##` → `####` | §2 in `01` documents the promotion with explanation; §5.1 in `03` confirms `####` is conventionally valid via cross-skill spot-check and notes the file currently uses bolded-paragraph-headers as an alternative | COVERED |
| 2-minute timeout / per-spawn-timeout gap (Task tool has no per-spawn timeout flag) | §10 in `02` explicitly states "The Claude Code `Task` tool does **not expose a per-spawn wall-clock timeout parameter**" and provides 3 implementation options with a recommended encoding (orchestrator-side wall-clock wait) | COVERED |

**All 6 key verification foci from the spawn prompt are covered.**

---

## Depth Assessment

**Expected depth:** Standard-Deep — sufficient to support a Template-02 (Complex) task file with discover-then-build flow, including unique-match anchor capture, integration-point inventories, edge-case enumeration, and convention precedents.

**Actual depth achieved:**

- **Source spec extraction** — verbatim block extraction with `+` stripping, 5-piece anchor decomposition, normative-statement cataloging with polarity, 3-step ladder formalization with invariants, verification-command decomposition, rationale anchor-point analysis, Cause→Fix matrix interpretation. Deep.
- **Target file state** — full structural map (`grep -nE` verified) with line ranges for every Wave; Wave 3 internal step-by-step breakdown (Step 1 through Step 4 + Exit criteria + Failure handling); unique-match `old_string` slice identified and validated as unique. Deep.
- **Wave 3 integration points** — output directory layout traced from Wave 0 through Wave 5; naming-convention translation table; 11 audit.log references inventoried; REPORT.md template traced through L1-141 with three insertion-point options enumerated; calibration-report parsing reduced to 7 grep-able conditions; force-degrade math edge cases enumerated; 2-minute timeout researched against actual `Task` tool surface. Deep.
- **Template / convention research** — Template 02 fit justified against 5 integration-point unknowns; Makefile sync-dev/verify-sync traced through 200+ lines; pre-commit hooks (markdownlint + block-claude-generated-mirrors) cited; cross-skill heading-convention spot-check; MUST/MUST NOT/NEVER phrasing patterns enumerated; 6 Known Gotchas distilled from Change B execution log. Deep.

**Missing depth elements:** None blocking. Two minor follow-ups (hypothesis-card confidence field name needs Read, audit.log writer-tool needs final inference) are surfaced as Important gaps for the executor's Phase 1 discovery.

**Depth verdict:** Achieves Standard-Deep tier. The fold-of-three-into-one for `02-target-file-and-integration.md` does not sacrifice depth — that file is 30KB / ~345 lines and covers Researcher 2 + Researcher 4 + Researcher 5 topics with full inventory.

---

## Recommendations

1. **Synthesis can proceed.** No critical gap blocks the executor from drafting the Template-02 task file. The research bundle provides the verbatim insertion block, the unique-match `old_string` slice, the heading-level promotion guidance, the naming-convention translation, and the integration concerns (audit.log free-form append pattern, REPORT.md Grounding-Gaps-plus-Confidence-note recommendation, calibration-report 7-condition parser, force-degrade edge-case table, orchestrator-wait-loop encoding of the 2-minute retry).

2. **Carry the 2 Important gaps into the task file as Phase 1 discovery items:**
   - `[ ]` Read `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` to confirm the self-reported `confidence` field name before implementing the force-degrade math parser.
   - `[ ]` Document the inferred `<output-dir>/audit.log` append pattern (free-form one-line entries via Bash `printf >> audit.log` or equivalent) in the task file's Phase 2 build item, noting that this is an inference from existing-pattern parity and not from an explicit writer-tool specification.

3. **Carry the 2 Minor gaps as explicit Phase 2 build decisions:**
   - REPORT.md insertion point — adopt Option 3 (Grounding Gaps prose line + Confidence header note) per `02-target-file-and-integration.md` §7 recommendation; optionally update `refs/report-template.md`'s Grounding Gaps examples block (L114-121).
   - Anchor placement — adopt the "after Step 4 / before Exit criteria" recommendation per `02-target-file-and-integration.md` §3 with the unique-match `old_string` slice from §4.

4. **Re-use Change B precedent verbatim** for the sync/verify/lint workflow per `03-template-and-conventions.md` §7. The three-step sequence (`make sync-dev` → `make verify-sync` → `uv run pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`) and the six Known Gotchas (G1-G6) carry forward unchanged.

5. **No re-research required.** The research bundle is complete and internally consistent.
