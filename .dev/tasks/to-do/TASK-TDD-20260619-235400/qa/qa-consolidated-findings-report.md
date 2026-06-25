# Consolidated Report-Validation Findings (Gate A, Step 6.11) — TASK-TDD-20260619-235400

**Date:** 2026-06-20
**Agents:** 9 (8 lenses: 4 structural rf-qa + 4 content rf-qa-qualitative + assembly summary). **Consolidated verdict: FAIL** (per gate rule; fixes in Step 6.12). Per-lens: completeness PASS, actionability PASS; template-conformance / internal-consistency / evidence-quality / numbers-metrics / crossref-chain / domain-accuracy FAIL. The TDD's load-bearing structures (OI-1 table, (M,N) table, verdict map, aspirational-vs-current framing) all verified SOUND across lenses; the failures are citation/consistency precision, mostly surgical.

## IMPORTANT (must fix in `tdd.md`)
- **I-A — reduce_wave3 §8.2 signature wrong & self-contradictory (evidence-quality #1, domain-accuracy #1).** §8.2 (labeled "Signatures verbatim from the worktree") shows `reduce_wave3(..., *, mode="normalize+merge", policy=None, ...)`. Actual (`reduce.py:555-561`): `mode` is POSITIONAL (2nd param, before the bare `*`), and the kwarg is **`status_policy`** not `policy`. Contradicts the TDD's own §18.2 (correct) and §6.1/§11.1 positional calls. FIX: correct §8.2 to `def reduce_wave3(worker_results, mode="normalize+merge", *, output_dir=None, workers_requested=None, status_policy=None, ...) -> ResultContract`.
- **I-B — ToC anchor drift §25/§26 (template-conformance #1).** ToC links `#25-operational-readiness` / `#26-cost--resource-estimation`, but headers carry `*(light …)*` qualifiers → real anchors differ → dead links. FIX: move the `*(light…)*` qualifier OUT of the `## 25.`/`## 26.` header lines into a `>` note beneath each (matches how §17 does it), so the header text matches the ToC anchor.
- **I-C — reviewer-count "2-3" vs "2-4" (numbers-metrics #1, internal-consistency F4).** §1/§2.1 say "2-3 reviewers"; §28 glossary says "2-4". FIX: reconcile against the spec — the spec's conceptual framing is "2-3 reviewers on different model classes" while the implemented `--reviewers` clamp is [2,4] default 3. Make it consistent everywhere: describe the ensemble as "2-3 heterogeneous reviewers (the new `--reviewers` flag accepts [2,4], default 3)"; align the §28 glossary entry to that exact phrasing (not bare "2-4").
- **I-D — §15.5 traceability table covers only 4 of 8 NFRs (internal-consistency F3).** Omits NFR-RH2.1/.2/.7/.8 although §15.1 claims to prove .1/.2. FIX: add the 4 missing NFR rows to the §15.5 FR/NFR→test matrix (NFR-7 guard test → NFR-RH2.1/.2; backward-compat suite → NFR-RH2.6 already; observability → .7; proxy contract → .8).
- **I-E — broken spec cross-ref §15.3 I6 (crossref CRITICAL #1, internal-consistency F7).** Cites "spec §5.4 ordering" — spec has no §5.4; the ordering/`mn_guard_table` is in spec §5.3. FIX: "spec §5.4" → "spec §5.3".

## MINOR (fix in same pass — citation/precision)
- **M-1 — FR source-ID mapping note (internal-consistency F1, §5.1).** Note claims IDs "read straight" but the Source column is `.1,.2,.3,.4,.9,.5,.6,.7,.8`. FIX: correct the note to state FR-005 ↔ FR-RH2.9 (the spec orders .9 after .4); the mapping is documented, not straight.
- **M-2 — dual line numbers for the 3 reused swarm symbols (internal-consistency F2).** `dispatch.py:334` vs `:344`; `commands.py:612` vs `:619`; `reduce.py:555` vs `:578` appear in different sections. FIX: standardize each to the `def` line (dispatch_wave1=334, _resolve_run_transport_factory=612, reduce_wave3=555).
- **M-3 — Document Information missing `Last Verified` row (template-conformance #2).** Template has 8 rows; TDD has 7. FIX: add a `Last Verified` row ("2026-06-20 against current worktree source").
- **M-4 — pipeline/process.py disposition dropped (completeness #1).** User-named scope file; research-notes required noting its orthogonality. FIX: add one note in §18 (Dependencies) that `cli/pipeline/process.py` was investigated and is ORTHOGONAL to the reflect Tier-2 seam (a generic ClaudeProcess lifecycle primitive), explicitly out of the FR-RH2 dependency surface.
- **M-5 — §13 "no /v1 literal" over-absolute (domain-accuracy #3).** `/v1` appears in `openai_compat.py` docstring examples. FIX: qualify to "no `/v1`/`/cli`/`:4000`/`:8317` literal in executable transport/config code paths (docstring examples excepted)."
- **M-6 — off-by-one definition-line citations (evidence-quality #2, domain-accuracy #2, numbers-metrics, actionability).** ResultContract `models.py:876`→877; WorkerResult `:1026`→1027; DoneSentinel `:1423`→1424; recipes REGISTRY `:182`→181; STRATEGIES `:209`→208; `mechanical_merge` "8 LOC"→7; §15.4 test line counts 277/221/173→276/220/172; "11 research files"→correct the count (12 enumerated items incl. reuse-audit.yaml) or relabel the enumeration. FIX: correct each (decrement decorator-vs-class drift by aligning to the `class`/dict-literal line).
- **M-7 — minor internal ref nits:** §11.2 "(§12.2)"→"(§12.2.1)"; the §337 "(§9)" amendment ref clarify it points at SPEC §9 not TDD §9 (which is N/A); table sourced to both "spec §5.3" and "spec §5.4" → use §5.3 consistently.

## Non-findings (do NOT change)
- "8 FRs" in some prompts is a scope typo — the spec correctly has 9 FRs (FR-RH2.1-.9); keep 9.
- §22 Q5-Q8 beyond the 4 OIs are legitimate synthesis-derived questions; keep.
- NFR-7 amendment routed to "spec §9 Migration" faithfully transcribes the spec's own instruction (spec L319) — TDD is faithful; not a TDD defect.
- aspirational-vs-current framing (ensemble.py NET-NEW) verified correct across lenses — keep.

## Fix plan (6.12)
Spawn ONE rf-qa (fix_authorization: true) to apply I-A..I-E + M-1..M-7 in-place to `tdd.md`, each verified against source, preserving the pinned path + 1,200-1,800 line budget. Then 6.13 verify (2 agents, max 3 cycles).
