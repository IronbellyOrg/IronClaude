# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** FR-RSR (T1–T10) reachability MDTM Template-02 tasklist research
**Date:** 2026-06-20
**Phase:** research-gate
**Lens:** gap-detection (find areas research missed entirely)
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Method

Adversarial stance: assume research missed entire areas. Cross-check research
files against the builder's authoring needs across 6 focus areas. Content that
lives in the authoritative TDD or spec is NOT a research gap; only flag what the
builder needs that is in NONE of (research, TDD, spec).

## File Inventory (5 research files + notes, all Status: Complete)

| File | Lines | Status | Scope |
|------|-------|--------|-------|
| research-notes.md | 161 | Complete | Authoritative-source routing, EXISTING_FILES, gaps, phases |
| 01-skill-gather-gate-anchors.md | 148 | Complete | SKILL.md §5.3/§5.4/§6.1/§6.5/§4 gather+gate anchors |
| 02-skill-contract-classify-failopen-anchors.md | 116 | Complete | SKILL.md §9.1/§9.3/§9.4/§10/§17.7/§0.5d anchors |
| 03-refs-inventory.md | 197 | Complete | reviewer-spec / deviation-taxonomy / coverage-mapping / grader-extensions |
| 04-eval-grader-inventory.md | 320 | Complete | evals.json schema, case template, grader.py sigs, skill-snapshot, falsifier-suite |
| 05-template-and-examples.md | 192 | Complete | MDTM Template 02 PART 1/2 rules + real TASK-RF example |

---

## Focus-Area Verdicts (gap-detection lens)

### FA1 — runtime-surface.md CONTENT authorability: NO GAP

The research is correctly STRUCTURAL (where runtime-surface.md plugs in, the §10.8 pattern it
mirrors, the contract emission, ledger artifact-ref routing). The actual CONTENT the builder must
author into runtime-surface.md lives in the authoritative spec/TDD, which I verified directly:

- **Allowlist rows** — spec §3 FR-RSR.1 (spec.md:237 "surface-keyword/decorator allowlist e.g.
  route/command/handler/endpoint decorators"). PRESENT.
- **lang→(test-marker, comment-syntax) table for py/rust/ts/js/go** — spec.md:284 (table mandate),
  spec.md:285-306 (Rust `#[cfg(test)]`, in-file `Test*`), and OQ-RSR.2 resolution at spec.md:750
  ("Author py/rust/ts/js/go rows in v1; others DEGRADE"). PRESENT with the exact 5-language set.
- **4-category degrade oracle a–d** — spec.md:325-335: (a) decorator routes; (b) packaging
  entrypoints `[project.scripts]`; (c) registry/DI/string-dispatch; (d) reflection/dynamic import.
  Each "an explicit table row with a deterministic match predicate". PRESENT verbatim.
- **rootwalk algorithm + depth=1 bound** — spec §3 FR-RSR.4 (spec.md:346-369); depth bound at
  OQ-RSR.3 spec.md:751 + tdd.md:797/942/978 ("mirror the §4.0 link-following depth=1 convention").
  PRESENT.
- **ledger schema** — spec.md:289 + spec.md:551 (`{requirement_id, symbol, edge, status,
  production_referrers[], evidence_ref}`); authored into runtime-surface.md per spec.md:550. PRESENT.

R4 additionally captured the grader.py mechanics needed to ENCODE these as eval assertions. No gap.

### FA2 — FAIL-pre/PASS-post mechanism: NO GAP (well-specified, this is the strongest area)

R4 §3e/§4/§5 concretely specifies the mechanism the builder needs and that does NOT live in
spec/TDD prose: `grade_eval` (grader.py:411-460) partitions assertions by `target` PREFIX —
`with_skill/` → post-change skill (EXPECT PASS), `old_skill/` → snapshot (EXPECT FAIL). The
headline eval id 37 declares assertions on BOTH prefixes. `skill-snapshot/reflect-v1.md` (111
lines, empirically `grep` = 0 runtime_surface refs) is confirmed the fail-before baseline and is
read-only. This is precisely the "where does skill-snapshot/reflect-v1.md plug in" answer; it is a
research-only fact (not in spec/TDD) and R4 captured it with line-level evidence. No gap.

### FA3 — count-invariant assertion gap: NO GAP (flagged WITH a concrete resolution path)

R4 §6 id-41 explicitly flags that `len(unreached_surfaces) == runtime_surface_unreached` cannot be
expressed by the existing grader (`parse_yaml_simple` can't read list length — verified at
grader.py:58 / R4 §3d). R4 offers the concrete resolution: emit a precomputed scalar pair and
cross-check with two `yaml_field` assertions, OR add a new grader type. CRITICALLY, the
authoritative spec itself resolves this at spec.md:539 — "asserts the count invariant ... **via
`yaml_field` (Pass-1 fix)**" — i.e. the precomputed-scalar path is the SPEC-MANDATED resolution,
and R4 independently arrived at the same mechanism. The gap is identified AND has a documented
resolution path in both research and spec. No gap.

### FA4 — per-task DoD inputs (WHERE to copy from): NO GAP

The research correctly routes the builder to authoritative docs (research-notes lines 19-23 names
the six spec mining targets and the TDD DoD sections). I verified each target EXISTS:

- **spec §3 acceptance-criteria `- [ ]` boxes per FR** — spec.md:230 (`## 3. Functional
  Requirements`); per-FR `- [ ]` boxes confirmed (e.g. spec.md:244, 367, 538). PRESENT.
- **spec §6 NFR measurement methods** — spec.md:678 (`## 6. Non-Functional Requirements`); table
  with explicit "how measured" column NFR-RSR.1–6 at spec.md:682-687 (e.g. NFR-RSR.2 "Re-run eval
  fixture twice; assert byte-identical ledger"). PRESENT with measurement methods.
- **TDD §24.1 DoD lines** — tdd.md:975 (`### 24.1 Definition of Done`), §24.2 Release Checklist at
  tdd.md:992. PRESENT.

The builder reads these directly (per the BUILD_REQUEST model where TDD/spec are read alongside
research). No gap.

### FA5 — blocker ordering capturable: NO GAP

TDD §19.3 (tdd.md:865) + §23.2 implementation-phases table (tdd.md:955-968) capture: P1
runtime-surface.md (blocks all); P2 gather FR-RSR.1-4 with "UNREACHED only emittable after
FR-RSR.3/4"; P3 gate FR-RSR.5; tdd.md:967-968 explicitly states oracle+rootwalk "gate them as
blockers of FR-RSR.2's UNREACHED path", FR-RSR.7 contract "parallelizable with the sweep", and
FR-RSR.10 eval "terminal". This matches the TRACK GOAL's stated ordering exactly. R5 captured the
Template-02 mechanics (depends_on, blocker_reason, L-handoff) to ENCODE it. No gap.

### FA6 — integration points: NO GAP

- **sprint-consumer TurnLedger coupling (D12)** — R2 Site 2 (research file 02) captured this AND
  corrected a TDD imprecision: the TurnLedger ROLLBACK is the executor.py row at SKILL.md:858 keyed
  on `per_task_verdicts[].deviation_class == regression`, NOT the top-level
  `deviation_count_by_class.regression` (which drives a SEPARATE sc-task escalate row at :859).
  This is a research STRENGTH (drift correction), not a gap.
- **§0.5d availability surface** — R2 Site 6 (SKILL.md:242-261, four-field contract, `backend: none`
  sentinel, do-not-re-probe rule at :259). CAPTURED.
- **audit.log per-step convention** — R1 Site 7 (SKILL.md:127, `{wave,step,timestamp,outcome,
  evidence_ref}`; new 4b'/4b steps each emit one row). CAPTURED.

---

## Cross-File Checks

- **Doc claims tagged** — research files use `[CODE-VERIFIED]` consistently (esp. file 03). No
  untagged doc-sourced architecture claims found.
- **Contradiction resolution** — R4's `evals/uc2-*` vs `cases/uc2-*` correction (file 04 §0/§24:
  "cases go in `cases/uc2-*`, the brief's `evals/uc2-*` phrasing is incorrect") resolves a
  spec/brief-vs-code drift. The builder MUST follow R4's empirically-verified `cases/` convention,
  NOT the spec.md:552-556 `evals/uc2-*` paths. This is correctly surfaced, but see Issue #1 below —
  it deserves an explicit prominent flag for the builder since the SPEC literally names the wrong
  path and the spec is a doc the builder reads directly.
- **Scope coverage** — every EXISTING_FILES key target (SKILL.md sites, all 4 refs, grader.py,
  evals.json, skill-snapshot, falsifier-suite, template) is discussed by at least one research file.
- **Incremental-writing signs** — files show iterative growth (per-site/per-section structure with
  re-anchoring deltas), not one-shot.

---

## Issues Found (gap-detection lens)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | spec.md:552-556 vs research file 04 §0/§24 | The authoritative SPEC names the new eval case dirs as `evals/uc2-*/` (5 rows). R4 empirically verified cases actually live under `cases/uc2-*/` and registered via `evals/evals.json`. Since the builder reads the spec DIRECTLY, the wrong `evals/uc2-*` path in the spec could leak into the task file's per-item Output specs if the builder copies spec paths verbatim. R4 flags this but the flag is buried in file 04. | The task file MUST adopt R4's `cases/uc2-<name>/{input/diff.patch, input/tasklist.md, expected.yaml}` layout + `evals/evals.json` registration (ids 37-41), NOT the spec's `evals/uc2-*` path. Builder should add an explicit per-item note overriding the spec path. Resolution path EXISTS (R4 §2/§6) — this is a flagged, resolvable item, not a missing area. |

No CRITICAL or IMPORTANT gaps found. The single MINOR item is a doc/code path-drift that research
ALREADY caught and resolved; it is logged here so the builder cannot miss it given the spec is a
directly-read authoritative source.

---

## Confidence Gate

**Checklist categorization (research-gate 10-item):**

1. File inventory (6 files, all Status: Complete, summaries present) — [x] VERIFIED (ls + Read all 6)
2. Evidence density (file:line citations throughout; spot-checked 12 against authoritative docs) — [x] VERIFIED
3. Scope coverage (every EXISTING_FILES target discussed) — [x] VERIFIED
4. Doc cross-validation ([CODE-VERIFIED] tags present, no untagged doc-arch claims) — [x] VERIFIED
5. Contradiction resolution (evals/ vs cases/ drift surfaced + resolved; TurnLedger row corrected) — [x] VERIFIED
6. Gap severity (all 6 focus areas checked; 1 MINOR resolvable item) — [x] VERIFIED
7. Depth appropriateness (Deep tier; R4 traces FAIL-pre/PASS-post end-to-end; R5 traces full lifecycle) — [x] VERIFIED
8. Integration-point coverage (TurnLedger/§0.5d/audit.log all captured) — [x] VERIFIED
9. Pattern documentation (§10.8 mirror, B2/M3/I20 patterns, grader sigs) — [x] VERIFIED
10. Incremental-writing compliance (iterative per-site structure) — [x] VERIFIED

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 5 (ls + 4 grep/sed sweeps over spec.md/tdd.md)

Note on FAIL caveat: this lens is GAP-DETECTION only. A PASS here means "research left no
builder-blocking GAP." It does NOT certify anchor-line accuracy or per-FR completeness — those are
the evidence-quality and completeness lenses' jobs in the parallel intermediate gate (I19: 2
rf-analyst + 2 rf-qa + 1 rf-qa-qualitative). The single MINOR item (spec path drift) does not block
synthesis because it is already resolved in research with a concrete path.

---

## VERDICT: PASS (gap-detection lens)

Research covers all six builder-need focus areas. No CRITICAL or IMPORTANT gaps. One MINOR
doc/code path-drift (Issue #1) is already caught and resolved within the research itself; it is
logged so the builder honors `cases/uc2-*` over the spec's incorrect `evals/uc2-*` paths.

The research correctly draws the structural-vs-content boundary: it captures the
research-only facts (exact SKILL.md/refs anchors, grader.py signatures, the FAIL-pre/PASS-post
prefix-partition mechanism, the count-invariant grader limitation + resolution, Template-02 rules)
while routing the builder to spec/TDD for FR content, acceptance criteria, NFR measurement methods,
DoD, and blocker ordering — all of which I independently verified EXIST in spec.md/tdd.md.

## QA Complete
