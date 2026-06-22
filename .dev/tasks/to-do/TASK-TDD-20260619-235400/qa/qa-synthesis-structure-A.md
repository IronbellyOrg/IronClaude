# QA Report — Synthesis Gate (Structure Lens, Partition A)

**Topic:** FR-RH2 — Headless Ensemble Fix (drive sc:reflect Tier-2 reviewer ensemble through the swarm dispatch library)
**Date:** 2026-06-20
**Phase:** synthesis-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Assigned files (Partition A):** synth-01-exec-problem-goals.md, synth-02-requirements.md, synth-03-architecture.md, synth-04-data-api.md
**Template:** src/superclaude/examples/tdd_template.md (v1.2)
**Stance:** ADVERSARIAL — assumed ≥10 errors; hunted independently with tool evidence.

> [PARTITION NOTE: This is Partition A of a multi-partition synthesis gate. Cross-file checks (contradictions, cross-references, scope coverage) are limited to the assigned subset synth-01..04. Full cross-file verification (e.g., §22 Open Questions handled in synth-09, §6.5 multi-tenancy in another file) requires merging all partition reports. Where an assigned file defers content to a non-assigned synth file, that deferral is noted but the downstream file was NOT verified here.]

---

## Overall Verdict: PASS

The four assigned synthesis files map cleanly to TDD template sections (synth-01→§1-4, synth-02→§5, synth-03→§6, synth-04→§7-8). Every checked claim traced to a real research file and/or shipped source. All 14 file:line citations I independently re-verified matched the actual source (one cosmetic off-by-one on a tuple-open line). All cited `src/...` paths exist (or are correctly marked NET-NEW/absent). No fabrication, no placeholders, no doc-only architecture claims, no hallucinated paths. FR/NFR numbering is 1:1 traceable to the parent spec. This is unusually disciplined synthesis; the adversarial hunt surfaced only 3 MINOR cosmetic items, none of which gate the synthesis.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match template | PASS | synth-01 §1-4 (Exec/Problem/Goals/Metrics), synth-02 §5 (+5.1/5.2/5.3/5.4), synth-03 §6 (+6.1-6.4/6.6/6.7), synth-04 §7+§8 — all match `tdd_template.md` numbered headings (Read template L199-576). §6.5 multi-tenancy correctly omitted (CLI/backend, not SaaS); §5.3/§5.4/§6.6/§6.7/§8.4 are additive supporting sub-sections, not template-divergent. |
| 2 | Table column structures correct | PASS | Goals table = ID/Goal/Success Criteria (template L243-247 ✓); Non-Goals = ID/Non-Goal/Rationale (✓); FR table = ID/Requirement/Priority/Acceptance Criteria + added Source col (template L297-302, Source is additive ✓); Key Design Decisions = Decision/Choice/Rationale/Alternatives (template L398-402 ✓); Data Entity tables = Field/Type/Required/Description/Constraints (template L443-447 ✓); (M,N) guard + correspondence tables are bespoke but internally consistent. |
| 3 | No fabrication (≥5 claims traced) | PASS | 14+ claims traced to source: `_audit_once`@runner.py:392 ✓, `expected_tier`@L403 ✓, isolation docstring@L8-12 ✓, `dispatch_wave1`@dispatch.py:334 ✓, success predicate@L496 ✓, `ModelPoolTooSmallError`@commands.py:589 ✓, `_resolve_run_transport_factory`@L612 ✓, `mechanical_merge`@merge.py:50 (8 LOC exactly, L50-57) ✓, `WorkerStatus`@models.py:69 ✓, `WorkerResult`@1027 (exactly 12 fields, L1117-1128) ✓, `ResultContract`@877 ✓, `LensEntry`@637 ✓, conftest mock copies fixture into return-contract.yaml (L130) ✓, `pass.yaml:4 tier_reached:2` ✓. Zero unsupported claims found. |
| 4 | Evidence uses actual file paths | PASS | Every claim cites concrete `file:line` (e.g. `contract.py:280-281`, `reduce.py:648`) not vague descriptions. Degraded-trigger line ranges in synth-04 §8.3 (L267/272/276/280/284…) re-verified against contract.py L263-327 — all land in cited ranges. |
| 5 | Architecture includes diagrams | PASS | synth-03 §6.1 ASCII flow diagram (data path runner→ensemble→swarm→adversarial→contract→verdict); §6.2 Mermaid `graph TD` module dependency graph. Content-rule "ASCII diagrams not prose" satisfied. |
| 6 | FR/NFR ID numbering | PASS | synth-02 §5.1 FR-001..FR-009 each carry FR-RH2.N source; §5.2 NFR 5.2.1..5.2.8 each carry NFR-RH2.N source + measurement method. Spec grep confirms FR-RH2.1..9 and NFR-RH2.1..8 all exist. Mapping note (FR-005↔FR-RH2.9) explicitly documented — not a silent renumber. |
| 7 | Cross-section consistency | PASS | (M,N) guard table identical across synth-01 §4.1, synth-02 §5.4, synth-04 §8.3 (M==0→blocked/2/ensemble-empty; M==1→degraded/11/single-reviewer-fallback; etc.). Diversity-over-M (not N) stated consistently in all four files. `--reviewers 1` sentinel-before-clamp invariant consistent (synth-02 §5.3, synth-04 §8.1). No contradictions within partition. |
| 8 | No doc-only claims in §6/§7/§8 | PASS | synth-03 §6 opens with explicit evidence rule "No doc-only claims"; every architectural claim tagged `[CODE-VERIFIED]` with re-verified line numbers. synth-04 §7/§8 sourced from direct re-read of models.py + research 02/03/04/05/09. The one `[CODE-CONTRADICTED]` (public transport-factory API) is correctly surfaced, not asserted as fact. |
| 9 | Stale docs surfaced (§22 routing) | PASS (within partition) | synth-01 §3.3 + provenance note route `[CODE-CONTRADICTED]`/`[UNVERIFIED]` items (public-factory contradiction, diversity-pool reconciliation, ResultContract exact schema) to §22 Open Questions. §22 itself is in a non-assigned file (synth-09) — deferral is correct but downstream landing NOT verified here. |
| 10 | Content-rules compliance (tables over prose) | PASS | Multi-item data consistently tabular (Goals, FRs, NFRs, entities, design decisions, correspondence). No full source-code reproductions — only key signatures (`dispatch_wave1`, `_resolve_run_transport_factory`, `reduce_wave3`) and the 8-LOC merge body, which is legitimately load-bearing. Single-source-of-truth respected (CLI surface owned by synth-02 §5.3 / synth-04 §8.1 with cross-ref, not duplicated divergently). |
| 11 | No placeholders/TODO/TBD | PASS | grep for TODO/TBD/FIXME/XXX/Lorem + template brackets (`[Goal N]`,`[Description]`,etc.) across synth-01..04 → NONE FOUND. |
| 12 | No hallucinated file paths (≥5 spot-checked) | PASS | 12 cited paths checked: 10 existing files all EXIST (runner.py, contract.py, models.py [reflect], dispatch.py, commands.py, reduce.py, merge.py, models.py [swarm], bare_review.py, parallel.py); 2 NET-NEW (`ensemble.py`, `reflect_review.py`) correctly marked ABSENT and labelled NET-NEW. Reflect pkg = exactly 6 files as synth-01 §2.1 claims. |
| 13 | FR traceability to spec | PASS | Parent spec `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` exists (49KB). All FR-RH2.1-9 + NFR-RH2.1-8 present in spec. target_release 4.4.0, complexity_score 0.82, complexity_class HIGH all match the synth headers. (M,N) verdict slugs trace to spec L229-262. |

## Summary
- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 3 (cosmetic; do not gate synthesis)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | synth-03 §6.6, reuse table row 2 ("Nearest prior art") | Cites `bare_review.py:66` for the `/sc:adversarial …` next-command tail. The `recommended_next_command_template=` opens at L65 and the literal `/sc:adversarial` string is on **L67** (L66 is the tuple-open continuation). Off-by-one. The adjacent citations `:40`/`:63`/`:64` are exact. | Change `:66` → `:67` (or cite the `:65` template-open). Cosmetic — the referenced construct unambiguously exists. |
| 2 | MINOR | synth-03 §6.6 reuse table + §6.2 narrative | Reuse-audit row cites `swarm/dispatch.py:344` / `commands.py:619` / `reduce.py:578` as "nearest prior art" line anchors, which differ from the canonical def lines used elsewhere in the same file (`dispatch_wave1`@334, factory@612, `reduce_wave3`@555). These are body-interior anchors from `reuse-audit.yaml`, not the def lines — internally defensible (they point at the fan-out call site, not the signature) but a reader cross-checking against §6.2/§8.2 will see a ~10-line drift. | Optional: add a one-word note ("call-site, not def") or align to def lines. Not a fabrication — both anchor sets are real lines in the cited files. |
| 3 | MINOR | synth-04 §7.1 `ResultContract` header ("19 top-level keys after target.* collapse") | Claim of "19 top-level keys" was not independently field-counted in this pass (the dataclass spans models.py L997-1015 + nested types); the 12-field `WorkerResult` count WAS verified exact. The 19-key figure is plausible and the per-field table is well-formed, but the aggregate count is asserted, not proven, within this partition. | No fix required for the table content. If a downstream gate needs the exact count certified, field-count L997-1015. Flagged for transparency, not as an error. |

## Confidence Gate

Per-item categorization (all 13 checklist items):
- [x] VERIFIED (tool evidence): items 1,2,3,4,5,6,7,8,10,11,12,13 — each cites specific Read/Grep/Bash output above.
- [x] VERIFIED with partition scope-note: item 9 (stale-doc routing) — deferral target (§22 in synth-09) is outside partition; routing intent verified in-file.
- [?] UNVERIFIABLE: 0
- [ ] UNCHECKED: 0

- **Confidence:** "Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 5 (template + 4 synth files) | Grep: ~22 (via Bash grep/sed) | Glob: 0 | Bash: 8"
- No web research performed (all claims internal/source-bound; Principle 6 source-truth-first satisfied locally). tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.

Tool-engagement check: tool calls (>30) exceed checklist item count (13) — verification is not padding; each call mapped to a specific claim or path.

## Actions Taken
None — fix_authorization is false. All findings documented above for the orchestrator/merge step.

## Recommendations
- Green light to proceed to assembly **from this partition's perspective.** The three MINOR items are cosmetic citation hygiene and do not block synthesis; they may be batch-fixed during assembly or deferred.
- Orchestrator: merge this Partition A report with the other synthesis-gate partition(s) before the global synthesis-gate verdict. Cross-file checks (synth-01's §22 deferral landing in synth-09; CLI-surface single-source-of-truth across all 9 files; global (M,N)-table consistency) are out of this partition's scope and MUST be confirmed at merge.
- Note for downstream task-integrity gate: the OI-1 field-correspondence table (synth-04 §8.3) is explicitly the BLOCKING deliverable that sizes `ensemble.py`; ensure the task file treats it as a gate, not a footnote.

## QA Complete
