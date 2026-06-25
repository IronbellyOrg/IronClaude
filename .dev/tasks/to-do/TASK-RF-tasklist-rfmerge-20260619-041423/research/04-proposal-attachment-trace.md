# Research: Proposal Attachment Trace

**Status:** Complete
**Date:** 2026-06-19
**Researcher:** R04 (Data Flow Tracer)
**Owns:** dynamic in/out data-flow + the single best prose insertion anchor per proposal.

---

## 0. Topology note (read first — resolves the "Stage N" vs "Section N" ambiguity)

The skill mixes two numbering systems and the brief's "Stage 4 / Stage 6 / Stage 7" labels do
not map 1:1 onto literal `### Stage N` headings:

- **Generation logic** (the brief's "Stage 1-6") lives under **prose Sections** — Input Contract
  (SKILL.md:47), Artifact Paths (SKILL.md:61), `### 3.x Source Document Enrichment`
  (SKILL.md:130), `## Deterministic Generation Algorithm` Sections 4.1-4.4b (SKILL.md:151-310),
  `## Deterministic Enrichment` Sections 5.1-5.7 (SKILL.md:444-658), `## Output Templates`
  (SKILL.md:662), and the pre-write `## Sprint Compatibility Self-Check` (SKILL.md:1132-1187).
- **Post-write validation** (the brief's "Stage 6→10.5") lives under literal `### Stage N`
  headings (SKILL.md:1244-1487). The `TaskCreate`/blockedBy ledger (SKILL.md:1564-1602) names
  Stage 1 Input Ingest … Stage 6 Self-Check … Stage 7 Roadmap Validation … Stage 10.5.

Mapping the brief's stage labels to real anchors:

| Brief label | Real SKILL.md anchor |
|---|---|
| Stage 4 Enrichment (P1, P5) | Sections 5.1-5.7 (444-658) for scored data; `### Index File Template` (666-849) for emit surface |
| Stage 6 Self-Check 20-check gate (P4) | `## Sprint Compatibility Self-Check` checks 1-20 (1136-1187) |
| Stage 7 2N validation + merge (P3, P4) | `### Stage 7` (1244-1310), merge prose 1288-1295, retry 1310 |
| Stage 8→9→10 patch chain (P2) | `### Stage 8/9/10` (1312-1456) |
| Stage 10.5 boundary (P2) | `### Stage 10.5` (1460-1487) |

`tasklist/prompts.py` is **mostly off the critical path** for these hooks (see §P4 and §Cross-cutting).

---

## P1 — `## Execution Context` block (Stage 4 / Index emit)

**Goal:** emit a `## Execution Context` block in `tasklist-index.md` derived from roadmap
refs + source areas, deterministically, never inventing file paths.

### Data available at emit time

| Datum | Where it is produced | Shape |
|---|---|---|
| Roadmap text (sole source of truth) | Input Contract, SKILL.md:47-57 | raw markdown string |
| `TASKLIST_ROOT` | Artifact-path resolver, SKILL.md:65-74 | path string (`.dev/releases/current/<seg>/`) — resolved from a roadmap substring or version token, the only "ref" the skill currently extracts from roadmap prose |
| Supplementary TDD `supplementary_context` (`component_inventory`, `api_surface`, etc.) | Section 4.1a, SKILL.md:169-184 (only when `--spec`/auto-wired) | dict of extracted tables; `component_inventory.new` = candidate "source areas" |
| Supplementary PRD `prd_context` | Section 4.1b, SKILL.md:185-197 | dict |
| Auto-wired `tdd_file`/`prd_file` from `.roadmap-state.json` | Section 4.1c, SKILL.md:199-214 | path strings (may be None / may not exist on disk) |
| Roadmap Item Registry (`R-###` → original text) | Section 4.1 (164-167) + emitted table at SKILL.md:739-749 | table |

**Critical constraint already in the skill:** SKILL.md:88-89 ("You must not claim these paths
exist; they are intended locations") and SKILL.md:468, 945, 1107 ("Do not invent code file
paths"). The deterministic emission rule must inherit this — i.e. only surface roadmap-derived
refs and (when present) TDD `component_inventory` component names, **never synthesized repo paths**.

### Deterministic emission rule (maps to the brief's spec)

- **Roadmap refs that "resolve":** the only roadmap-derived resolvable ref the generator currently
  computes is the `TASKLIST_ROOT` segment/version token (SKILL.md:69-72). A second class of "refs"
  is the auto-wired `tdd_file`/`prd_file` whose existence is *checked* at SKILL.md:212 ("If the
  auto-wired file path no longer exists on disk, a warning is emitted and the value is left as
  None"). **This is the existing resolve/None gate the P1 "emit iff ≥1 ref resolves" rule should
  reuse** — a ref "resolves" iff it is non-None after the 4.1c existence check.
- **Source areas:** TDD `component_inventory.new` (SKILL.md:176) is the only source-area-shaped
  data the skill extracts. The degraded "References-only" form (no source areas) is exactly the
  roadmap-only branch already described at SKILL.md:136 ("Without source documents: works from the
  roadmap alone").

### Emit-surface in/out

- **In:** `{TASKLIST_ROOT, resolved tdd_file?, resolved prd_file?, component_inventory.new?,
  R-### registry}`.
- **Out:** a `## Execution Context` markdown block in `tasklist-index.md`.

### Single best insertion anchor

**Heading:** `### Index File Template (\`tasklist-index.md\`)` → insert the `## Execution Context`
sub-section template **between `#### Metadata & Artifact Paths` (ends ~SKILL.md:707) and
`#### Phase Files Table` (SKILL.md:709)**. Best precise line: **after the Artifact-Paths table
row `| Feedback Log | ... |` at SKILL.md:707, before `#### Phase Files Table` at 709.**
Rationale: Execution Context is cross-phase metadata about *where work lands / what it reads*,
so it belongs in the index alongside the other metadata tables, before the per-phase listing.
A one-line pointer must also be added to the File-Emission inventory at SKILL.md:95 (index-file
contents list) so the self-check knows the section exists.

### GAP the builder must resolve

- **The skill does not parse roadmap prose for file/area references** beyond the TASKLIST_ROOT
  token. "Roadmap refs/source-areas" as a first-class extracted list **does not exist today**.
  P1 must either (a) restrict "refs" to the already-computed set (TASKLIST_ROOT + resolved
  tdd/prd + `component_inventory.new`), which is fully deterministic and matches the no-invention
  rule, or (b) add a new deterministic roadmap-ref scanner (more surface, must define a regex as
  tight as the 4.x scanners). Option (a) is the lower-risk reuse and is recommended.
- **No self-check covers a new index sub-section.** Checks 1-8 (SKILL.md:1138-1145) assert the
  Phase Files table + filenames but nothing about Execution Context. If P1 wants the block
  guaranteed-present, a check must be added (overlaps R05's territory — flagged, not owned).

---

## P5 — Tier Calibration Advisory (Stage 4, READ-ONLY)

**Goal:** render a `## Tier Calibration Advisory` that READS `TASKLIST_ROOT/feedback-log.md`
WITHOUT feeding back into the scored tier — proving scored tiers stay a pure function of the roadmap.

### Where scored tiers are computed (confirmed pure)

- **Compliance Tier:** Section 5.3, SKILL.md:544-614. Inputs are 100% derived from *roadmap item
  text* + task-local context (compound phrases 5.3.1 / keyword matches 5.3.2 / file-count + path +
  operation boosters 5.3.3). **No feedback-log input anywhere in 5.3.**
- **Confidence Score:** Section 5.4, SKILL.md:616-629. `Base = max(tier_scores)` (line 622) — a pure
  function of the 5.3 scores. No external state.
- The brief's cited range "546-646" spans 5.3 (544) through 5.6 Sub-Agent Delegation (642-650); the
  scored-tier core is precisely **544-629**.

### feedback-log.md is an OUTPUT template, not an input today

`feedback-log.md` is **emitted** by the generator as an empty collection schema
(`#### Feedback Collection Template`, SKILL.md:820-839; intended path SKILL.md:826). Columns:
`Task ID | Original Tier | Override Tier | Override Reason | Completion Status | Quality Signal |
Time Variance`. It is filled at *execution time* by `/sc:task`, not read during generation.
**Therefore a P5 advisory necessarily reads a feedback-log from a PRIOR run** (the current run's
file is freshly emitted empty), which structurally guarantees the read cannot influence the current
scored tiers. This is the cleanest possible no-feedback proof.

### Advisory in/out

- **In (READ-ONLY):** prior `TASKLIST_ROOT/feedback-log.md` rows (Original Tier vs Override Tier
  deltas, Quality Signal). If absent → advisory renders a "no prior calibration data" degraded line.
- **Out:** a `## Tier Calibration Advisory` block in `tasklist-index.md`. Pure prose; **must not**
  mutate any task's `Tier`/`Confidence` already computed by 5.3/5.4.

### Single best insertion anchor

**Heading:** `### Index File Template` → insert `## Tier Calibration Advisory` template **immediately
after `#### Feedback Collection Template` (ends SKILL.md:839) and before `#### Glossary`
(SKILL.md:841)**. Best precise line: **after SKILL.md:839, before SKILL.md:841.** Rationale: it is
the natural sibling of the Feedback Collection Template (same data source), and placing it there
keeps the "reads feedback-log" coupling visually adjacent to the schema it reads. A guard sentence
must be added stating the advisory is *advisory-only and never alters Section 5.3/5.4 outputs* — the
same "advisory (logged but not blocking)" pattern already used at SKILL.md:1481 and 1547.

### GAP the builder must resolve

- **No existing read of feedback-log during generation.** Must define the read as best-effort
  (file may not exist on first run) and must explicitly fence it out of the 5.3/5.4 compute path so
  no future editor wires it into `tier_scores`. Add a one-line invariant to Section 5.3 header
  (SKILL.md:546) like "tier scores are a pure function of roadmap text; no calibration/feedback
  input." (overlaps R03 field-contract territory — flagged.)

---

## P4 — `gate-results.txt` (Stage 6 → Stage 7 injection)

**Goal:** serialize the Stage-6 20-check gate as plain text to
`TASKLIST_ROOT/validation/gate-results.txt` (present even on all-pass), then inject that text into
the Stage-7 2N validation-agent prompt build.

### Stage 6 gate output (the source)

The "20-check gate" is the `## Sprint Compatibility Self-Check` block, **checks 1-20 at
SKILL.md:1136-1187**, terminated by SKILL.md:1187 ("If any check 1-20 fails, fix it before writing
any output file"). Sub-groups: checks 1-8 Sprint compat (1138-1145), 9-12 Semantic Quality Gate
(1149-1156), 13-20 Structural Quality Gate table (1176-1185). The completion ledger reports it as
"Stage 6: Self-Check: all 17 checks passed" at SKILL.md:1597 — **note the count mismatch (says 17,
the gate is 20); R01/R05 should reconcile, flagged.**

**Current state:** these checks run **in-memory only** — SKILL.md:1134 ("All checks … MUST pass
before any Write() call. Invalid output is never written") and the write-atomicity rule
SKILL.md:1195. **There is NO serialization of the check results to disk today.** That file does not
exist; P4 introduces it.

### Serialization in/out

- **In:** the boolean result of each of checks 1-20 (in-memory at the pre-write gate, ~SKILL.md:1187).
- **Out:** `TASKLIST_ROOT/validation/gate-results.txt`, one line per check
  `CHECK N PASS/FAIL: <check label>` + summary `GATE: PASS (20/20)`. Must be emitted even on all-pass.
  `TASKLIST_ROOT/validation/` already exists by Stage 8 (`mkdir -p`, SKILL.md:1407) but P4 needs it
  earlier — the dir creation must move/duplicate to the Stage-6→7 boundary.

### Stage 7 prompt-build injection site (the exact anchor)

The Stage-7 validation-agent prompt is **inline prose in SKILL.md, NOT a prompts.py function.**
It is the block-quote at **SKILL.md:1265-1286** ("Validation instructions for each agent: > You are
a tasklist validation agent…"), spawned per the algorithm at SKILL.md:1248-1263. The 5 checks the
agent runs (Drift/Contradictions/Omissions/Weakened/Invented) are SKILL.md:1269-1275.

**Exact injection anchor:** add a "Pre-validation gate context" paragraph **inside the agent
instruction block, after the intro line SKILL.md:1267-1268 and before check 1 (Drift) at
SKILL.md:1271** — i.e. inject the contents of `gate-results.txt` so each agent sees which
structural checks already passed. Equivalently, add it to the per-agent spawn payload list at
SKILL.md:1255-1257 / 1259-1261 (the "Spawn Agent A/B with:" bullets) as a 4th bullet:
"the contents of `TASKLIST_ROOT/validation/gate-results.txt`".

### prompts.py is NOT the site (important)

`tasklist/prompts.py:build_tasklist_fidelity_prompt` (prompts.py:17-148) is the **CLI
`superclaude tasklist validate`** surface, a *different pipeline* per the scope note at
SKILL.md:132 — it validates roadmap→tasklist for the CLI, not the skill's Stage-7 2N fan-out.
`build_tasklist_generate_prompt` (prompts.py:151-234) is generation, also not Stage 7. So the
P4 injection lives in **SKILL.md inline prose**, not prompts.py. (If the builder *wants* a reusable
gate-results block it could add a `build_gate_results_block(...)` pure function to prompts.py and
have SKILL.md reference it, but that is optional and adds a new tested symbol — R05 territory.)

### GAP the builder must resolve

- **No on-disk serialization step exists.** A new sub-step must be added at the end of the
  Self-Check section (after SKILL.md:1187) AND the `validation/` dir must be created before
  Stage 7 (currently first created at Stage 8, SKILL.md:1407).
- **Stage gate wording** at SKILL.md:1310 ("All 2N agents completed successfully") and the
  completion contract (SKILL.md:1597-1598) don't mention gate-results.txt; P4 should add it to the
  artifact inventory + the Stage-6 completion line.

---

## P3 — Synthetic-DNSP finding on single-agent failure (Stage 7 merge)

**Goal:** in the Stage-7 orchestrator merge, when ≥1 agent succeeds but some agent failed,
synthesize a HIGH synthetic-DNSP ("Did Not Survive Probe") finding and PROCEED; only zero-success
(all agents fail) escalates with no synth.

### The merge step prose (the anchor)

The orchestrator merge is **`**Orchestrator merge and deduplication**` at SKILL.md:1288-1295**:
1. collect all findings (1292), 2. dedup (1293), 3. sort by severity/phase/task (1294),
4. produce consolidated findings list for Stage 8 (1295).

The current failure handling is a single clause at the **Stage gate, SKILL.md:1310**:
"Zero agent failures (if an agent fails, retry once before reporting error)." So today:
**any** unrecovered agent failure → hard error (no proceed-with-synth, no zero-vs-some distinction).

### Data in/out

- **In:** per-agent return = either a structured findings list (severity/Task ID/Problem/Roadmap
  evidence/Tasklist evidence/Exact fix, SKILL.md:1277-1284) or `"No issues found."` (1286), OR an
  agent failure (post-retry).
- **Out (P3):**
  - **≥1 success, ≥1 failure →** consolidated findings list (1295) PLUS a synthesized HIGH finding
    in the same entry shape (1277-1284), e.g. `Severity: High, Problem: "validation coverage gap —
    agent for tasks X-Y of phase P did not survive its probe (retry exhausted)", Exact fix: "re-run
    Stage 7 for the uncovered task range"`. Then PROCEED to Stage 8.
  - **0 success (all agents failed) →** escalate / all-agents-fail error, **no synth finding**
    (a synth among zero real findings would be meaningless).

### Single best insertion anchor

**Heading:** `### Stage 7: Roadmap Validation` → modify the **retry-and-failure clause at the
Stage gate, SKILL.md:1310**, and add a new numbered step to the merge list **between step 1
"Collects all findings" (SKILL.md:1292) and step 2 "Deduplicates" (SKILL.md:1293)** — a
"1a. Reconcile agent failures: if ≥1 agent succeeded and ≥1 failed (post single retry), synthesize a
HIGH synthetic-DNSP finding covering the failed agent's task range and proceed; if 0 agents
succeeded, escalate all-agents-fail (no synthetic finding)." Best precise line: **insert after
SKILL.md:1292, and replace the gate sentence at SKILL.md:1310.**

### GAP the builder must resolve

- **The retry primitive exists (1310) but is binary (success vs error).** P3 must split the
  post-retry failure path into the some-vs-zero branch; the existing "retry once" stays as the
  per-agent recovery before the merge classifies success.
- **Synthetic finding must carry the standard entry shape** (1277-1284) so it flows untouched
  through dedup/sort (1293-1294) and into the Stage-8 ValidationReport (the HIGH bucket at
  SKILL.md:1341-1349). No new schema needed — reuse confirmed.

---

## P2 — Bounded validation loop (Stage 10 → Stage 9, with Stage-10.5 non-overlap)

**Goal:** after Stage 10 spot-check, if a re-validation surfaces a failing set `F_k`, loop back to
re-patch (Stage 9) under monotonicity/regression/cap stop conditions — without overlapping the
Stage-10.5 pre-reflect boundary.

### Current flow (linear, NO loop)

- **Stage 8** Patch Plan: consolidated findings (from Stage 7) → `ValidationReport.md` +
  `PatchChecklist.md` (SKILL.md:1312-1407). Short-circuit if zero findings (1316-1325).
- **Stage 9** Patch Exec: delegate `PatchChecklist.md` to `sc:task --compliance strict`
  (SKILL.md:1409-1427). Orchestrator does NOT patch itself (1425).
- **Stage 10** Spot-Check: re-verify ONLY the Stage-7 findings, record `RESOLVED`/`UNRESOLVED`
  into a `## Verification Results` table appended to `ValidationReport.md` (SKILL.md:1429-1454).
- **Stage 10 explicitly does NOT loop today:** SKILL.md:1456 "If any remain UNRESOLVED, they are
  logged but the skill does NOT loop. The ValidationReport.md serves as the record for human review."
  **This single sentence is the exact thing P2 replaces.**

### Data in/out for the loop

- **`F_k` (failing set at iteration k):** the brief specifies it = the **full Stage-7
  re-validation** failing set, NOT just the prior UNRESOLVED rows. Stage 10 today only re-reads the
  flagged sections (1437-1439, "Re-verify only the specific findings"). So P2's loop body must run a
  **fresh Stage-7-style 2N validation** (re-using the Stage-7 fan-out primitive, the same one
  Stage 10.5 reuses per SKILL.md:1464) to compute `F_k`, then feed `F_k` back into Stage 8/9.
- **In:** `F_{k-1}` patched phase files. **Out:** `F_k` = new full-revalidation finding set.

### Stop conditions (must be authored explicitly)

- **Monotonicity:** require `|F_k| < |F_{k-1}|` (strictly shrinking) — else stop.
- **Regression guard:** if `F_k` introduces a finding on a task not in `F_{k-1}` (a new break), stop
  and report regression — reuse the Stage-10 "no regression in surrounding context" check at
  SKILL.md:1439 as the seed concept.
- **Cap:** a hard max iteration count (e.g. K_max) so the loop is bounded.

### Single best insertion anchor

**Heading:** `### Stage 10: Spot-Check Verification` → **replace the no-loop Stage gate at
SKILL.md:1456** with the bounded loop-back: "compute `F_k` via a full Stage-7 re-validation; if
`F_k` is non-empty AND `|F_k| < |F_{k-1}|` AND no regression AND `k < K_max`, loop back to Stage 8
(regenerate PatchChecklist for `F_k`) → Stage 9 (re-execute) → Stage 10; otherwise stop (clean,
capped, or regression) and finalize ValidationReport." Best precise line: **replace SKILL.md:1456.**
The blockedBy ledger (Stage 10 blockedBy Stage 9, SKILL.md:1556/1587) already encodes the 8→9→10
dependency the loop rides.

### Stage-10.5 non-overlap boundary (the fence)

This is **already explicitly architected** and P2 must not violate it. SKILL.md:1462 states Stage
10.5 is "fenced after the Stage 8-10 patch chain" precisely because Stage 9 mutates phase files;
a reflect co-located with 8-10 would "race a file mid-patch." Therefore the P2 loop must **fully
converge/terminate (clean | capped | regression) BEFORE Stage 10.5 fans out** — the loop lives
entirely inside the 8↔10 cycle and Stage 10.5 (SKILL.md:1460-1487) runs once, after the loop's final
phase content is settled. Best precise line for the fence note: **add one sentence to Stage 10.5's
opening rationale at SKILL.md:1462** ("…the Stage 8-10 patch chain *including any P2 bounded
loop-back iterations*…").

### GAP the builder must resolve

- **`F_k` requires a full re-validation, but Stage 10 today is a cheap targeted re-read** (1433,
  "not parallelized — the finding list is typically small"). P2 changes Stage 10's character: the
  loop's re-validation must invoke the Stage-7 2N fan-out primitive (SKILL.md:1248-1263), not the
  narrow per-finding read. The builder must decide whether the *first* Stage 10 stays cheap and only
  the loop-back arms the full re-validation (recommended: cheap first pass, full re-validate only if
  UNRESOLVED rows exist) — otherwise every run pays 2N extra agents.
- **No iteration counter / `F_{k-1}` state exists** in the linear flow; P2 introduces loop state
  (k, |F_{k-1}|, regression set) that must be recorded (suggest into `ValidationReport.md`'s
  Verification Results section, SKILL.md:1442-1454, as a per-iteration table).
- **Short-circuit interaction:** Stage 8's zero-finding short-circuit (SKILL.md:1316-1325, 1549)
  skips 9-10 entirely; the loop only exists when Stage 7 found ≥1 issue, so the short-circuit path is
  unaffected — confirm the loop is nested under the non-short-circuit branch.

---

## Cross-cutting findings

1. **prompts.py is largely off-path for P1-P5.** All five hooks attach to **SKILL.md prose**, not to
   the two pure functions in `tasklist/prompts.py`. The fidelity prompt (prompts.py:17-148) serves a
   *different* CLI pipeline (`tasklist validate`) per the scope note SKILL.md:132; the generate
   prompt (prompts.py:151-234) builds the generation instruction but does not carry Stage-7/gate
   logic. Only P4 *optionally* could add a reusable `build_gate_results_block` here (R05 territory).
2. **Two hooks (P1, P5) attach to the same `### Index File Template` region** (666-849), in source
   order: `## Execution Context` after Artifact-Paths (after 707), `## Tier Calibration Advisory`
   after Feedback Collection Template (after 839). They do not collide; both are index-only,
   cross-phase metadata, consistent with the content-boundary rule SKILL.md:104.
3. **Three hooks (P2, P3, P4-injection) attach to the Stage-7→10 validation chain** and all *reuse
   existing primitives*: the Stage-7 2N fan-out (1248-1263), the orchestrator merge (1288-1295), the
   retry clause (1310), the Stage-8 finding schema (1341-1349), the 8→9→10 blockedBy chain
   (1554-1556). Low new-surface risk; the work is mostly prose insertion + replacing two
   "does-not-loop"/"binary-failure" sentences (1456, 1310).
4. **Count-mismatch flag for R01/R05:** SKILL.md:1597 says "all 17 checks passed" but the gate is
   checks 1-20 (1136-1187). P4's `gate-results.txt` must serialize 20, so this stale "17" should be
   corrected as part of P4 (or flagged to R01's static inventory).
5. **Self-check additions for new sections (R05 territory):** P1's `## Execution Context` and P5's
   `## Tier Calibration Advisory` have no presence/format self-check among checks 1-8 (1138-1145);
   if either must be guaranteed-present, a check is needed — flagged, not owned.

---

## Per-proposal anchor summary (one line each)

| Proposal | In → Out (data shape) | Single best insertion anchor (heading + line) | Gap flag |
|---|---|---|---|
| **P1** Execution Context | `{TASKLIST_ROOT, resolved tdd/prd?, component_inventory.new?, R-### registry}` → `## Execution Context` block in index | `### Index File Template` — after Artifact-Paths table (after **SKILL.md:707**), before `#### Phase Files Table` (709) | No roadmap-ref scanner today; reuse 4.1c resolve/None gate (212) |
| **P5** Tier Calibration Advisory | prior `feedback-log.md` rows → `## Tier Calibration Advisory` (READ-ONLY) | `### Index File Template` — after `#### Feedback Collection Template` (after **SKILL.md:839**), before `#### Glossary` (841) | feedback-log is output-only today; must fence out of 5.3/5.4 pure-compute (544-629) |
| **P4** gate-results.txt | checks 1-20 booleans (1187) → `validation/gate-results.txt` → injected into Stage-7 agent prompt | Serialize after **SKILL.md:1187**; inject inside agent block after **SKILL.md:1268**, before Drift check (1271) | No on-disk serialization today; `validation/` dir first made at Stage 8 (1407) |
| **P3** synthetic-DNSP | per-agent {findings \| "No issues" \| failure} → consolidated list + synth HIGH (some-fail) / escalate (zero-success) | `### Stage 7` — new merge step after **SKILL.md:1292**; replace gate sentence **SKILL.md:1310** | Retry clause is binary success/error today; split some-vs-zero branch |
| **P2** bounded loop | `F_{k-1}` patched files → `F_k` (full Stage-7 re-validation set) under monotonic/regression/cap stop | `### Stage 10` — replace no-loop gate **SKILL.md:1456**; fence note added to Stage-10.5 rationale **SKILL.md:1462** | Stage 10 is cheap targeted re-read today, not full re-validation; no iteration state |
