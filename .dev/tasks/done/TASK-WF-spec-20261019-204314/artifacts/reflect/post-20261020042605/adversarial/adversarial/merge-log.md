# Merge Log

## Metadata
- Merge date: 2026-10-20T06:05:00Z
- Executor: merge-executor (Fable 5.1)
- Base: Variant 3 (R3 refactorer/opus, score 0.860)
- Plan: `refactor-plan.md` (9 changes, auto-approved 2026-10-20T05:50Z)
- Outputs: `../merged-verdict.md`, `../merged-verdict.yaml`
- Inputs read: refactor-plan.md, base-selection.md, debate-transcript.md, invariant-probe.md, variant-1/2/3-original.md, diff-analysis.md, `../../operator-direction.md`
- Constraints honored: no edits outside ROOT; no read-only inputs modified; no tests, git, or CLI execution. One `uv run python -c "yaml.safe_load(...)"` parse check was run against the YAML output only (validation, not CLI execution of the project).

## Changes Applied

### Change 1 — V2 four-class frame, advisories/errata separated
- Status: APPLIED
- Source: Variant 2 §Candidate dispositions / §Canonical deviation / advisory separation / §Evidence limits and errata
- Target: whole-document structure
- Before: V3 order (T7 coverage, W1-D1, W1-D2, W1-D3, Newly alleged, Ordering and limitations)
- After: 1 Verdict summary; 2 Per-task T1..T7; 3 Canonical deviations (D1, D1-explicit, D2, D3, D5, D4); 4 Correctness advisories / evidence gaps; 5 Rejected candidates; 6 Verifiers and limits; 7 Input provenance
- Provenance tag: `<!-- Source: ... -->` on every H2 and each D-subsection (12 tags)
- Validation: heading list matches the required order

### Change 2 — Relabel D1 per forced round, split slices
- Status: APPLIED
- Source: V1 §W1-D1 split disposition; forced-round tally; INV-001
- Target: §3 D1 and D1-explicit
- Before (base): "necessary consequence, documentation gap"; whole D1 treated as one slice
- After: menu option-0 slice = Drift LOW-MEDIUM (V1 50 / V2 64, V3 dissent Regression-LOW 55, reported 0.57, late flip flagged, "not settled"); explicit-mixed slice = Necessary deviation (`:964-988`); anchors :67/:78/:80/:143/:144, `install_mcp.py:1284-1285`, `:1311-1314`, `:486-496`; compliant alternative = visible skip; docs guide:46/73 LOW clarity; test gap no option-0 project/Darwin
- Provenance tag: "Variant 1, §W1-D1 split disposition — merged per Change #2; Debate/forced round"
- Validation: no sentence labels the menu-0 slice Necessary (contradiction scan below)

### Change 3 — Relabel D2 per forced round, append gate enumeration
- Status: APPLIED
- Source: V2 §W1-D2; V1 §W1-D2; INV-002, INV-003
- Target: §3 D2
- Before (base): "advisory correctness gap, no spec-relative regression"
- After: Drift conditional on A-001 (V2, V3 55; V1 dissent advisory 55); predicate chain `:545-552` vs `:85-99`/`:102-116`, `:682-683`, `:693-700`, `install_mcp.py:846-848`, `:597-605`, `:257-264`/`:305-311`; spec :109/:111/:146; INV-002 8 gates listed; umask-002 and host/upstream modes stated as unobserved
- Provenance tag: "Variant 2, §W1-D2 mechanism; Variant 1, §W1-D2 chain; Invariant probe INV-002/INV-003 — merged per Change #3"
- Validation: md and yaml both say Drift / conditional_on A-001 / dissent V1 advisory

### Change 4 — Relabel D3 per forced round
- Status: APPLIED
- Source: V1 §W1-D3 (message omits path `install_mcp.py:577-579`); INV-004
- Target: §3 D3
- Before (base): "no confirmed regression; advisory availability limit"
- After: Drift LOW conditional on symlinked-HOME host (V2, V3 50; V1 dissent advisory 60); anchors `:54-55`, `:88`, `:489`, `:539-544`, `install_mcp.py:572-579`; spec :56 vs :114 (uninstall section); no fixture
- Provenance tag: "Variant 1, §W1-D3 (message omits path); Invariant probe INV-004; Debate/forced round — merged per Change #4"
- Validation: md and yaml agree

### Change 5 — Linux-only authority anchor corrected, cost stated
- Status: APPLIED
- Source: V1 label "authorized"; operator-direction.md:5-7; INV-009
- Target: §3 D5 (replaces base's "operator direction plus source.md:90, disclosed guide:9")
- Before: Authorized "plus source.md:90"
- After: Authorized expansion, authority operator-direction.md:5-7 with both exact quotes (lines 5 and 7); cost: every `superclaude install` on macOS exits 1 (`main.py:255-275`), `install_codebase_memory.py:594`, guide:9, source.md:63; source.md:90 appears only as rejected support
- Provenance tag: "Variant 1 ... Base (original, modified) — source.md:90 removed as support because :90 lists macOS"
- Validation: source.md:90 scan — 2 md hits, 2 yaml hits, all in rejection context (§5 table, §3 D5 tag, yaml `rejected_support`, yaml `rejected_candidates`)

### Change 6 — D4 kept as LOW drift candidate, interpretation open
- Status: APPLIED
- Source: Base §Newly alleged canonical deviation; R2/forced votes
- Target: §3 D4
- Before: "LOW drift ... independent debate should decide"
- After: Drift LOW, candidate, interpretation open; V2 74 / V1 45 / V3 candidate 45; reported 0.55; `main.py:326-330`; source.md:76/:31/:117; guide:50; `--list --dry-run` arguably redundant, `--scope` half stronger; baseline code unread
- Provenance tag: "Base (original, modified) ... wording per Change #6; Debate R2/forced votes"
- Validation: md and yaml agree (status candidate-interpretation-open, 0.55)

### Change 7 — Per-task T1..T7 status table
- Status: APPLIED
- Source: V1 §Assigned completion (T2 7, T4 8, T5 7); V2 §Assigned completion (T1/T3/T6 20 total, no per-task split given); V3 §T7 (7)
- Target: new §2
- After: table with status, AC count, anchors, carried findings; every row "mock-conformant; source.md:151 live gate unverified"; INV-005 note on "49 ACs"; T2/T5 fixture regions marked READ by coordinator (`test_install_mcp_tavily.py:382-462`, `test_update_command.py:31-76`); T4 carries D1 Drift; T2/T3 carry conditional D2; T7 carries doc clarity notes
- Provenance tag: "Variant 1, §Assigned completion; Variant 2, §Assigned completion; Base (original) §T7 — merged per Change #7"
- Validation: T2 sub-range anchors (`:819-821` ... `:885-899`) were trimmed from the md table for length and are kept in merged-verdict.yaml `tasks.T2.anchors` only as the parent range `install_mcp.py:815-899`; sub-ranges remain in variant-1-original.md:13. Noted as a deliberate abbreviation, not a loss of provenance.

### Change 8 — Advisory / evidence-gap section
- Status: APPLIED
- Source: V1 (argv U-003; `AcquisitionResult.acquired` grep `:54,105,254,306`); V2 (canned `mcp_cli` `:821-835`; Click DEGRADE; cross-ref flags); INV-002/005/006/010; grounding gaps (Serena exec; Click reachability)
- Target: new §4
- After: A-001, INV-002, INV-005 warnings; Serena/Click; no fresh tests; canned fixture; INV-006 (`claude --version` twice `:513`/`:830`; option 0 never reaches `check_prerequisites`; `:488` does not name option 0); U-003; `.acquired`; INV-007/008 one line
- Provenance tag: "Variant 1, §Other observations; Variant 2, §Evidence limits and errata; Invariant probe INV-002/005/006/010 — merged per Change #8"
- Validation: none of these items appears in §3 as a deviation class

### Change 9 — Provenance + verifiers/limits block
- Status: APPLIED
- Source: V3 §Ordering and limitations + recommendations; V1/V2 next-step lists
- Target: new §6 and §7
- After: ordering facts (`install_mcp.py:1299-1334`, `main.py:254-275`, `main.py:94-187,326-332`); four plan-named verifiers plus guide edit; limits list; provenance with card paths, calibrations 0.71/0.78/0.80, mean 0.763 method, base scores, topology and degraded independence
- Provenance tags: "Base (original) §Ordering and limitations ... merged per Change #9"; "base-selection.md; debate-transcript.md Metadata"
- Validation: yaml `strongest_verifiers`, `limits`, `input_cards`, `topology` match

## Post-Merge Validation

- Heading hierarchy: H1 x1, H2 x7 (numbered 1-7 in required order), H3 x6 under §3 only. PASS.
- Provenance: 3 header comments present; 12 `<!-- Source: -->` tags, one per H2 and per D-subsection. PASS.
- Internal references: 13 per-point ids in yaml (S-001, S-002, C-001..C-005, X-001..X-003, A-001, A-002, D4) all map to transcript final matrix. Six canonical_deviations ids (D1, D1-explicit, D2, D3, D5, D4) each have a matching md H3. Eight rejected_candidates rows match the plan table 1:1. Seven task keys T1..T7 present. All file:line anchors traced to plan, transcript, probe, or cards; none invented. PASS.
- Contradiction re-scan:
  - Labels/confidences md vs yaml: D1 Drift LOW-MEDIUM 0.57 / V3 Regression-LOW; D1-explicit Necessary; D2 Drift cond. A-001 0.60 / V1 advisory; D3 Drift LOW cond. 0.60 / V1 advisory; D5 Authorized 0.88; D4 Drift LOW candidate 0.55. Agree. PASS.
  - "Necessary deviation" + menu-0: grep hits md:16 (counts the explicit-mixed slice as the Necessary one) and md:113 (rejected-candidates row). Neither labels the menu-0 slice Necessary. PASS.
  - source.md:90 as macOS-exclusion support: all four hits are rejection/erratum context. PASS.
  - No sentence claims fresh tests or live upstream smoke were run. PASS.
- YAML: parses with `yaml.safe_load`; top-level keys exactly the 15 required (base_variant, canonical_deviations, convergence, correctness_advisories, evidence_gaps, input_cards, input_confidence, limits, merge_method, overall_reflect_status, per_point_decisions, rejected_candidates, strongest_verifiers, tasks, topology). PASS.
- Length: merged-verdict.md is 2144 words by `wc -w`, above the ~1800 target. The overage is dominated by required file:line anchor tokens in the T1..T7 table and §3; further cuts would drop plan-mandated anchors. Flagged, not failed.

## Summary
- Planned: 9 | Applied: 9 | Failed: 0 | Skipped: 0
- Deviations from plan: none. One abbreviation (T2 sub-range anchors kept at parent-range granularity in md; see Change 7).
- Result: **PASS** (with length flag)
