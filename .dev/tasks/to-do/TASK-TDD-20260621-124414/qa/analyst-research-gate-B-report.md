# Research Completeness Verification (Partition B of 2)

**Topic:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep (TDD research gate)
**Date:** 2026-06-21
**Files analyzed:** 3 (assigned subset)
**Depth tier:** Heavyweight
**fix_authorization:** false (report-only; no edits made to research files)

**Assigned files:**
- `research/04-eval-path-integration.md`
- `research/05-reuse-and-boundaries.md`
- `research/06-skill-prose-demotion.md`

**Reference read:** `research-notes.md` (planned scope / SUGGESTED_PHASES / REUSE_AUDIT).

> [PARTITION NOTE: Cross-file checks (contradiction detection, cross-reference, coverage audit
> against full scope) are applied ONLY within this assigned subset {04,05,06} plus research-notes.md.
> Full cross-file analysis vs files 00–03 + web research requires merging this report with partition A.]

---

## Verdict: PASS — 0 Critical, 0 Important, 4 Minor

All three files are Complete, evidence-dense, and meet Heavyweight depth. File 05's two special-attention
checks both PASS: all 6 reuse verdicts carry grounded `file:line` neighbours, and the reflect→audit import
boundary is presented as three explicitly-weighable options (A/B/C) with a recommended-but-not-silent choice.
The 4 Minor issues are documentation-hygiene nits that do not block synthesis.

**Independent verification performed:** I re-read the live source for the highest-leverage citations in each
file (grader.py:191/318/448-449, reachability.py:591/460, filetype_rules.py:143-144, runner.py:8-9/14-17,
SKILL.md:465/487/491/721-730/669-672, evals.json ids 37-41, the absence of any `cli/audit` import-ban in
reflect modules). Every checked citation matched the file's claim. Details under each section.

---

## 1. Coverage Audit (assigned subset vs SUGGESTED_PHASES rows 04/05/06)

The research-notes.md SUGGESTED_PHASES table assigns each of files 04/05/06 a topic + a list of files to
investigate + target synthesis sections. I audited whether each assigned investigation surface is actually
covered in the corresponding file.

| Phase / Scope item (from research-notes) | Covered By | Status |
|------------------------------------------|-----------|--------|
| 04: grader.py `check_yaml_list_len_eq` + dispatcher | 04 §1 (dispatcher, grader.py:318), §2 (checker, grader.py:191) | COVERED |
| 04: grader-extensions.md | 04 §2 (extensions:135-166), Stale-Doc #1/#2/#3 | COVERED |
| 04: evals.json | 04 §3 (registry shape, ids 37-41, case_dir vs case_file) | COVERED |
| 04: cases/uc2-* (5 dirs) | 04 §3 (all 5 cases enumerated with assertion focus) | COVERED |
| 04 → §15 testing, §4 metrics (target synth) | 04 §4.1/4.2 (Option A oracle / Option B materialize) | COVERED |
| 05: cli/audit/reachability.py | 05 §5 (reachability.py:374/591-624/460/26-33) | COVERED |
| 05: cli/audit/dependency_graph.py | 05 §2 (dependency_graph.py:1-14/5-8/27-39/24) | COVERED |
| 05: cli/audit/dynamic_imports.py | 05 §4 (dynamic_imports.py:1-13/24-39) | COVERED |
| 05: cli/audit/filetype_rules.py | 05 §3 (filetype_rules.py:105-107/110-131/143-144) | COVERED |
| 05: cli/audit/wiring_gate.py | 05 §1 (wiring_gate.py:164 `_safe_parse`) | COVERED |
| 05: cli/audit/dead_code.py | 05 §1 (dead_code.py:37-49), §4 (dead_code.py:30-35/155-163) | COVERED |
| 05: reflect import-ban docstrings | 05 §7 (runner.py:8-9, config.py:7-10, models.py:8-12, __init__.py) | COVERED |
| 05 → §6.4 decisions / §18 deps / §21 alternatives | 05 §7 (3-option boundary), G2 (§18 deps flag) | COVERED |
| 06: SKILL §6.1 4b/4b′ | 06 §1 (lines 465/466/487/489 verbatim) | COVERED |
| 06: SKILL line 491 contract-emission | 06 §4 (line 491 verbatim) | COVERED |
| 06: SKILL §9.1 emission comment | 06 §4 (lines 721-730 verbatim) | COVERED |
| 06 → §6 arch / §19 migration / §3 non-goals | 06 §2 (demote), §3 (preserve), §5 (no version bump) | COVERED |

**Coverage result: 17/17 assigned scope items COVERED. No gaps.** Each file investigated exactly the surfaces
its SUGGESTED_PHASES row named, plus adjacent surfaces (e.g. 06 pulled in §5.3/§9.3 to anchor the
preserve-boundary). No assigned file/directory was left uninvestigated within this partition.

---

## 2. Evidence Quality

Each file uses an explicit per-claim tagging discipline (`[CODE-VERIFIED]` / `[INFERRED]`) and anchors claims
to `file:line`. I spot-verified the load-bearing citations against live source (results in the right column).

| Research File | Evidenced Claims | Unsupported Claims | Independent spot-check | Quality |
|--------------|------------------|--------------------|------------------------|---------|
| 04-eval-path-integration | High — every §1–§4 claim carries grader.py / evals.json line anchors | 0 architectural claims left bare; `[INFERRED]` items honestly flagged (materializer step, LLM-run characterization, Option A/B design) | grader.py:191 def, :318 dispatcher, :448-449 bucketing, evals.json ids 37-41, 5 uc2 dirs — ALL MATCH | Strong |
| 05-reuse-and-boundaries | High — all 6 verdicts + 3 boundary options carry `file:line` neighbours | 0 | reachability.py:591/460, filetype_rules.py:143-144, runner.py:8-9/14-17, absence of cli/audit ban — ALL MATCH | Strong |
| 06-skill-prose-demotion | High — all four target blocks quoted verbatim with exact line anchors | 0; recommendations explicitly labelled "Recommended replacement framing" not asserted fact | SKILL.md:465/466/487/491, 721-730 comment, contract_version 1.6.0 at :672 — ALL MATCH | Strong |

**Notable rigor in file 04 §2:** the "self-consistency-only caveat" correctly identifies that
`check_yaml_list_len_eq` compares two operands both emitted by the same producer, so a coherent fabrication
passes. This is the precise motivation for the deterministic module and is evidence-grounded
(grader.py:191-210), not hand-waved. This is the strongest single analytical insight across the three files.

**Notable rigor in file 05 §5:** correctly distinguishes that `_bfs_reachable` is itself *unbounded* (no depth
param) — so the depth=1 contract must be enforced by the caller, not the BFS internal. Verified against
reachability.py:591-624 (the BFS signature takes `graph, start, target`, no depth). This is a non-obvious
correction beyond the reuse-audit.yaml citation and materially affects the §6.4 design.

No file contains a vague "the system uses X architecture" claim without a path. Evidence quality is uniformly
Strong across the partition.

---

## 3. Documentation Staleness

All three files have a dedicated "Stale Documentation Found" section and tag doc-sourced claims. Critically,
each doc-vs-code discrepancy is reported with the CODE as authoritative (not the stale doc as current fact),
which is exactly the discipline this check enforces.

| Discrepancy reported | Source | File's tag / handling | Status |
|----------------------|--------|------------------------|--------|
| grader-extensions.md:25 "10 groups" vs 11 dispatcher branches | 04 Stale #1 | Labelled accounting note; authoritative count 11/19 pinned to grader.py + evals.json | OK (code-authoritative) |
| grader-extensions.md:43 `check_citation_resolves` sketch missing `is_absolute()` remap | 04 Stale #2 | Shipped grader.py:126-129 declared "more correct"; doc sketch flagged illustrative | OK (code-authoritative) |
| FR-RSR path itself | 04 Stale #3 | Declared byte-consistent grader.py:191-210 vs extensions:146-165 | OK (no staleness) |
| reuse-audit.yaml:591 cite vs BFS span :591-624 + unbounded | 05 Stale (refinement) | Added precision, not staleness; verified live | OK |
| reuse-audit.yaml filetype_rules:110 vs inverted-default at :143-144 | 05 Stale (refinement) | Pinned exact load-bearing line | OK |
| SKILL line 487 "LLM-free" self-label vs 491/§9.1 LLM-emit instruction | 06 Stale (wording) | Correctly framed as *aspirational-not-literal* tension that FR-DRS resolves | OK |
| TASK-prompt line numbers (~465/487/491/721-735) off by 1-2 | 06 Stale (prompt drift) | Corrected to exact 465/466/487/489/491/721-730 (731-736 = field defs); verified live | OK |

**No doc-sourced architectural claim is presented as current fact without a `[CODE-VERIFIED]` cross-check.**
No `[CODE-CONTRADICTED]` claim is reported as a current fact. File 06's handling of the "LLM-free" label
tension (line 487 self-describes the tagger as deterministic while 491 instructs the LLM to emit) is
particularly well-handled: it is surfaced as the *exact* discrepancy FR-DRS exists to close, not buried.

Staleness check: PASS for all three files.

---

## 4. Completeness (Status / Summary / Gaps / Key Takeaways per file)

The RF research-file structure expects each file to be Complete with a Summary, a Gaps and Questions section,
and synthesized takeaways. None of the three files carries an explicit `Status: Complete` line — but all three
carry a full Summary, a Gaps and Questions section, and a Stale Documentation section, which together
constitute a finished investigation. The absence of a literal `Status:` field is a Minor format nit
(M1 below), not an incomplete investigation.

| Research File | Status line | Summary | Gaps Section | Synthesized takeaways | Rating |
|--------------|-------------|---------|--------------|-----------------------|--------|
| 04-eval-path-integration | absent (M1) | Y (§Summary + per-case roll-up) | Y (5 gaps Q1–Q5) | Y (Option A/B §15 path) | Complete |
| 05-reuse-and-boundaries | absent (M1) | Y (§Summary, all 6 verdicts) | Y (G1–G4) | Y (3-option recommendation) | Complete |
| 06-skill-prose-demotion | absent (M1) | Y (§Summary + boundary-in-one-sentence) | Y (G1–G4) | Y (demote/preserve table) | Complete |

All three have Summary + Gaps + takeaways. **Completeness: PASS** (with M1 format nit).

---

## 5. Cross-Reference Check (within partition + to research-notes)

The three files reference each other's domains and external phases. I verified each cross-reference points at
a real, correctly-scoped target.

- **04 → 05/01:** "deterministic module ... where will it live" (04 G1) defers the module-home question; 05 §7
  answers the *import-boundary* half (reflect-local copy), and 04 correctly does NOT claim to resolve it.
  Consistent — no contradiction, clean hand-off.
- **04 → 02/03:** 04 §4.2 Option B materialization "would live in the runner/materializer" and explicitly
  flags (G2) that the materializer step "was not found this turn" and defers to research 02/03. Honest scope
  boundary; matches research-notes assigning the runner/commands.py to phase 02.
- **05 → 02 (OQ-DRS.1):** 05 G3 correctly defers the referrer-engine choice (Serena/LSP vs AST) to research 02
  as "an engine choice, not a reuse choice." Matches research-notes OQ-DRS.1 ownership.
- **05 → research-notes PATTERNS:** 05 §7 Option B cites the "callable interfaces" decoupling precedent
  (sprint executor avoids TurnLedger import) directly from research-notes PATTERNS_AND_CONVENTIONS. Accurate.
- **06 → 02/03 (OQ-DRS.2):** 06 G1 is the strongest cross-reference — it correctly identifies that the
  demotion prose cannot be *fully* demoted unless the bare `claude -p /sc:reflect` path is covered, which
  depends on the invocation-site decision owned by research 02. It flags that the demotion wording must be
  *conditional*. This is a genuine, correctly-attributed downstream dependency, not a gap in 06 itself.
- **06 → 04:** 06 §4 references "enforced by the grader's schema assertion (research 04)" — consistent with
  04's Option A oracle-assertion proposal.

All cross-references are consistent and correctly scoped. **Cross-reference check: PASS.** No file claims to
resolve something another file owns; the OQ-DRS.1/2/3 open questions are uniformly deferred to their correct
owners and to TDD §22.

---

## 6. Contradiction Detection (within partition {04,05,06} + research-notes)

I compared claims about shared components across the three files. The shared touchpoints are: (a) the
deterministic module's determinism property, (b) the count invariant, (c) the contract field set / version,
(d) the dynamic-dispatch→DEGRADE rule, (e) the reuse posture for reachability.

| Shared topic | File 04 | File 05 | File 06 | Verdict |
|--------------|---------|---------|---------|---------|
| Module is deterministic / LLM-free | §4.2 "identical input→identical output" | (n/a) | §1 "FR-DRS makes a Python module the literal executor" | CONSISTENT |
| Count invariant `len(unreached_surfaces)==runtime_surface_unreached` | §2 (grader checks it) | §6 (module computes it by construction) | §2 D4 / §4 (module-computed invariant) | CONSISTENT — complementary roles (compute vs check) |
| Contract field set / version | §3 (6 fields, names exact) | (n/a) | §5 (NO field change, NO bump from 1.6.0) | CONSISTENT |
| Dynamic-dispatch → DEGRADE not UNREACHED/Regression | §3 case 39 (DEGRADE) | §5 mismatch #1 (reachability says UNREACHABLE; runtime-surface needs DEGRADE) | §3 P4 (dynamic→DEGRADE soundness floor) | CONSISTENT across all three |
| Reuse of reachability.py | (n/a) | §5 reuse-by-import, adapt, depth=1 | (n/a) | No conflict (only 05 covers it) |

**No contradictions found.** The three files agree on every shared claim. The count-invariant treatment is a
good example of *complementary, non-contradictory* coverage: 04 frames it as what the grader checks, 05 as
what the module computes, 06 as what migrates from "LLM emission rule" to "Python invariant + test oracle" —
three views of one invariant, mutually consistent.

One **alignment worth noting (not a contradiction):** 06 §5 firmly recommends "keep 1.6.0, no bump" while
acknowledging a single flip condition (a semantic tightening on the bare-skill path). 04 and research-notes
both treat the field set as stable. No file argues for a version bump. Aligned.

**Contradiction detection: PASS.**

---

## 7. Compiled Gaps (deduplicated, severity-rated)

All gaps are sourced from the files' own Gaps/Questions sections plus my verification pass. None are Critical
or Important — they are downstream design decisions correctly deferred to later phases, or doc-hygiene nits.

### Critical Gaps (block synthesis)
None.

### Important Gaps (affect quality)
None. The two highest-stakes open items — the module's home/invocation site (04 G1, 06 G1, OQ-DRS.2) and the
import boundary (05 §7) — are NOT gaps in the research; they are correctly surfaced *as decisions for TDD
§6.4/§21/§22*, which is exactly where the research is supposed to route them. Surfacing a decision is the
research deliverable, not a gap in it.

### Minor Gaps / Issues (must still be fixed — doc hygiene, non-blocking)
- **M1 — Missing literal `Status: Complete` line.** None of 04/05/06 carries an explicit `Status:` field.
  All are substantively complete (Summary + Gaps + takeaways present). Fix: add a `Status: Complete` line for
  RF-format conformance. Source: structural check §4. (Owner: research agents / cosmetic.)
- **M2 — File 04 line-count overstatement.** 04 line 12 states grader.py is "519 lines"; live `wc -l` = 518.
  Off by one (trailing-newline counting). Harmless but a factual nit in a file that otherwise prides itself on
  exactness. Fix: change 519→518. Source: my `wc -l` verification.
- **M3 — File 04 G2 (materializer step) genuinely unverified.** 04 honestly flags that the `evals.json` →
  `eval_metadata.json` materializer "was not found this turn," which leaves Option B's "runner materializes
  contract.yaml" hook location unconfirmed. This is correctly tagged `[INFERRED]` and deferred — but the TDD
  §15 (Option B path) will need this resolved by research 02/03 or a follow-up grep before relying on it.
  Not a defect in 04; a carried dependency. Source: 04 G2.
- **M4 — File 04 §1 routing-fragility note (grader.py:448-449) is advisory, not actioned.** 04 G3 correctly
  warns that a future oracle assertion (Option A) using a non-`target` key would be silently dropped from both
  config buckets. This is a real downstream risk for the §15 Option A design but is flagged, not resolved.
  The TDD §15 must either mandate Option A assertions carry a `target` key or extend the bucketing logic.
  Source: 04 §1 + G3 (verified bucketing logic at grader.py:448-449).

All four are Minor. None blocks synthesis or assembly.

---

## 8. File 05 Special-Attention Checks (per spawn prompt)

The spawn prompt specifically directs: (a) confirm all 6 component reuse verdicts carry grounded `file:line`
neighbours, and (b) confirm the reflect→audit import boundary is presented as three weighable options, not a
silent choice. Both PASS.

### 8a. Six reuse verdicts — grounded `file:line` neighbours

| # | Component | Verdict (+ S_reuse) | Grounded neighbour(s) | Independently verified |
|---|-----------|---------------------|------------------------|------------------------|
| 1 | surface-tagger | distinct (0.37) | wiring_gate.py:164, filetype_rules.py:1-13, dead_code.py:37-49 | (not re-spot-checked; consistent with reuse-audit.yaml) |
| 2 | referrer-finder | distinct/shape-divergent (0.67) | dependency_graph.py:1-14/5-8/27-39/24 | (consistent) |
| 3 | partitioner | distinct (0.57) | filetype_rules.py:105-107/110-131/**143-144** | **VERIFIED** :143-144 = "Default to source for unknown / return FileType.SOURCE" |
| 4 | degrade-oracle | distinct (0.68) | dynamic_imports.py:1-13/24-39, dead_code.py:30-35/155-163 | (consistent) |
| 5 | entrypoint-rootwalk | **reuse-by-import** (0.81) | reachability.py:374/**591-624**/**460**/26-33 | **VERIFIED** :591 = `_bfs_reachable(graph,start,target...)`, :460 = `if depth > 50` |
| 6 | ledger-writer | distinct (0.56) | ensemble.py:500-509, contract.py:65-71, runner.py:58-67/70 | (consistent) |

**All 6 verdicts carry grounded `file:line` neighbours.** The two I independently spot-checked (partitioner's
inverted-default at filetype_rules.py:143-144, and the rootwalk's `_bfs_reachable` at reachability.py:591 +
depth>50 at :460) matched exactly. The "distinct vs reuse-by-import" gradient is well-justified: only the BFS
internal (strongest, 0.81) earns reuse-by-import, and even that is qualified "adapt, do NOT drop-in" with two
CODE-VERIFIED domain mismatches (dynamic-dispatch→UNREACHABLE-vs-DEGRADE, depth>50-vs-depth=1). 8a: PASS.

### 8b. Reflect→audit import boundary — three weighable options

File 05 §7 presents the boundary as a genuine three-way decision:
- **Option A** — import `cli/audit` directly (pro: zero new BFS code / con: couples product path to
  cleanup-audit semantics whose defaults are inverted; reaches into a private `_bfs_reachable`).
- **Option B** — extract a boundary-neutral shared `graph_bfs` helper (pro: no coupling, matches callable-
  decoupling precedent / con: refactor touches cli/audit, larger diff).
- **Option C** — reflect-local copy of the ~30-line BFS (pro: zero coupling, mirrors the `_IndentDumper`
  copy-over-import precedent at runner.py:14-17 / con: ~30 lines duplicated, drift risk low).

Each option has an explicit pro **and** con. The file states a **recommendation (Option C for v1, Option B
long-term, Option A to be avoided)** but explicitly frames it as "for the TDD to ratify, not a silent
choice" (§7 heading and closing). The mechanical premise — that the reflect import-ban names ONLY `cli/sprint`
and `cli/roadmap`, so a `cli/audit` import is *mechanically legal* and the decision is coupling-quality not
legality — I **independently verified**: grep for `cli/audit`/`cli.audit` across all reflect modules returns
nothing, and runner.py:8-9 / config.py:7-10 / models.py:8-12 ban only sprint+roadmap. The Option C
recommendation is anchored to a real in-repo precedent (runner.py:14-17 "copied locally (lower coupling than
importing the private symbol)") which I verified verbatim.

**8b: PASS.** The boundary is a properly-weighable three-option decision with a recommended-not-silent
resolution, exactly as the spawn prompt and research-notes REUSE_AUDIT require ("surface it as a Key Design
Decision (§6.4) + Alternative (§21) + Open Question (§22), NOT a silent choice"). File 05 G1 reiterates this
explicitly.

---

## 9. Depth Assessment (vs Heavyweight tier)

**Expected (Heavyweight):** code-traced data/control flow, symbol-level evidence, integration-point mapping,
pattern analysis, alternatives weighed, open questions routed to TDD sections.

| File | Depth elements present | Achieved |
|------|------------------------|----------|
| 04 | Dispatcher control-flow trace, per-case assertion mapping (5 cases × shapes), self-consistency-vs-correctness analysis, two wiring options with grader-conformance | Deep |
| 05 | 6 component fingerprints with prior-art neighbours, S_reuse scoring, 2 CODE-VERIFIED domain mismatches on the rootwalk, 3-option boundary with precedent citation | Deep |
| 06 | Verbatim quotation of 4 target blocks, sentence-level demote/preserve table (D1-D6 / P1-P6), version-rule mapping (patch/minor/major), conditional-demotion dependency on OQ-DRS.2 | Deep |

**Actual depth achieved: Heavyweight-conformant across all three.** The investigations go beyond file-level
understanding into symbol-level reduction precedence, BFS-boundedness nuance, and sentence-level prose surgery.
**Missing depth elements: None.** The only genuinely-unverified surface (the eval_metadata materializer, M3) is
honestly flagged rather than fabricated — which is correct Heavyweight discipline, not a depth shortfall.

---

## 10. Recommendations

1. **PASS this partition to synthesis.** No Critical or Important gaps. Files 04/05/06 are evidence-dense,
   internally consistent, and Heavyweight-deep.
2. **Carry M1 (add `Status: Complete`) and M2 (519→518) as cosmetic fixes** — optional, non-blocking; can be
   batched whenever the research files are next touched. fix_authorization is false, so no edits were made.
3. **Route the two load-bearing decisions to the TDD, not back to research:** the invocation-site/module-home
   (OQ-DRS.2; 04 G1 + 06 G1) and the import boundary (05 §7) belong in TDD §6.4 / §21 / §22. The research has
   done its job by surfacing them as weighable options.
4. **Flag M3 + M4 for the TDD §15 author:** before relying on Option B (runner-materializes) the materializer
   location must be confirmed (M3); for Option A, oracle assertions must carry a `target` key or extend the
   grader bucketing (M4, grader.py:448-449). These are design constraints the synthesis §15 must respect.
5. **Merge note for the orchestrator:** this is Partition B. Cross-file contradiction/coverage checks vs files
   00–03 + web research were out of scope here. Merge with Partition A's findings (take more-severe rating on
   any shared item) before issuing the gate-wide verdict.

---

## Summary

- Files passed: 3 / 3
- Critical gaps: 0
- Important gaps: 0
- Minor issues: 4 (M1 missing Status line, M2 519-vs-518 count, M3 unverified materializer [carried dep],
  M4 routing-fragility advisory)
- File 05 special checks: 6/6 reuse verdicts grounded (PASS); 3-option import boundary, recommended-not-silent (PASS)
- Depth: Heavyweight-conformant, all three
- Independent citation spot-checks: all matched live source
- **Partition B verdict: PASS**
