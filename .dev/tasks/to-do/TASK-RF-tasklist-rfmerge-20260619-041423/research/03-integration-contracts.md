# Research: Integration Contracts

**Status:** Complete
**Date:** 2026-06-19
**Researcher:** R03 (Integration Points)
**Focus:** EXACT existing contracts the RFMerger P1–P5 proposals must REUSE. Forking ANY of these is a HALT condition. Every field cites `file:line` against `src/superclaude/` as of 2026-06-19.

**Files of record:**
- `src/superclaude/skills/task-builder/SKILL.md` (P3 DM-003, P1 Execution Context, P2 PR-02)
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (Stage 9 delegate, Stage 10.5 reflect, tier algorithm)
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (reflect-remediation finding-set boundary)
- `src/superclaude/skills/sc-task-protocol/SKILL.md` + `src/superclaude/commands/task.md` (sc:task tier)
- `src/superclaude/cli/sprint/config.py` (sprint parser conventions)

---

## §0. HALT-condition summary (read first)

Any P-proposal that REDEFINES, RENAMES, FORKS, or PARALLEL-IMPLEMENTS any of the contracts below — instead of REUSING the existing surface verbatim — is a contract-fork HALT. The five reuse obligations:

| Proposal | MUST reuse (no fork) | Anchor |
|---|---|---|
| P3 | DM-003 synthetic-dnsp emission contract (8 fields, fixed values, closed exhaust vocab, R-122 Path A/B/C, strictly-additive merge, HIGH non-overridable) | task-builder SKILL.md:873–911 |
| P1 | `## Execution Context` 3-subfield contract + "no file:line in header" rule + TB-Add-7 | task-builder SKILL.md:1066–1071, 1231, 1389 |
| P2 | PR-02 Retry Monotonicity (regression > monotonicity, F-set = dedup-key cardinality, byte-exact halt strings, 4-step ordering) | task-builder SKILL.md:1261–1305 |
| P2 (disjointness) | Stage 10.5 reflect-pre finding set must be PROVEN disjoint from P2's bounded patch loop | sc-tasklist SKILL.md:1460–1481; sc-reflect SKILL.md |
| (all) | Stage 9 delegates patching to `sc:task` (tier `STRICT > EXEMPT > LIGHT > STANDARD`); `sc:task-unified` is NOT a real name | sc-tasklist SKILL.md:1409–1427, 414/548/1206 |

---

## §1. P3 — DM-003 synthetic-dnsp emission contract (task-builder SKILL.md:873–911)

The contract P3 in sc:tasklist MUST conform to lives in the **"DNSP Synthetic Finding Protocol (PR-03 — paradigm-neutral, the BASE proposal of this release)"** block, task-builder SKILL.md:873. PR-03 is described there as the **BASE proposal** — so sc:tasklist's P3 is a CONSUMER/MIRROR of this contract, never an independent re-spec.

### 1.1 The 8-field emission record (verbatim, SKILL.md:877–883)

When a partition agent (rf-analyst / rf-qa / rf-qa-qualitative) **exhausts its escalation ladder (WebSearch → /rf:opinion → team-lead)** AND **fails the existing single retry** (Bucket A "retry once before reporting error" baseline), the orchestrator synthesizes a HIGH-severity finding (SKILL.md:875):

| Field | Fixed/Dynamic | Exact value / rule | Line | Reject symbol |
|---|---|---|---|---|
| `severity` | FIXED | literal `HIGH` (case-sensitive) | 877 | `DM-003-fixed-field-invariant-violation` (R-113/R-114, :885) |
| `source` | FIXED | literal `synthetic-dnsp` (case-sensitive) | 878 | `DM-003-fixed-field-invariant-violation` (:885) |
| `affected_range` | DYNAMIC | the failed agent's `assigned_files` slice **copied byte-for-byte verbatim** — no normalization/canonicalization/ordering/whitespace edits (`assigned_phases` for rf-qa-qualitative) | 879, 887 | `DM-003-dynamic-field-invariant-violation` (R-115/R-116, :887) |
| `evidence` | DYNAMIC | canonical wire value = spawn-log path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`; if unavailable, MUST substitute stub `<!-- evidence-absence: no-spawn-log: <reason> -->` (e.g. `no-spawn-log: tmpfs-cleared`, `no-spawn-log: orchestrator-write-failed`). NEVER blank/whitespace-only | 880, 887 | `DM-003-dynamic-field-invariant-violation` (:887) |
| `recommendation` | FIXED | literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix). The earlier `on this range` extension was a pre-T06.01 drift, removed by T06.05 | 881, 889 | `DM-003-recommendation-invariant-violation` (R-117, :889) |
| `dedup_key` | DYNAMIC (shape-pinned) | 2-element YAML list `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`. MUST be a 2-element list; 2nd element MUST be from the closed vocab below | 882, 889 | `DM-003-dedup-key-shape-violation` (R-118, :889) |
| `found_n_times` | DYNAMIC (counter) | int, default `1` on first emission; increments by exactly `1` on each within-cycle dedup-key collapse. MUST be positive int ≥1; first emission MUST be `1` | 883, 889 | `DM-003-found-n-times-invariant-violation` (R-119, :889) |

**Note:** the protocol enumerates the record as 7 named YAML fields (`severity`, `source`, `affected_range`, `evidence`, `recommendation`, `dedup_key`, `found_n_times`) at SKILL.md:877–883. `dedup_key` is itself a 2-tuple, so the literal field count is 7; the task brief's "8 fields" counts the dedup_key 2-tuple's two elements separately. Verified: SKILL.md:877–883.

### 1.2 Closed exhaust-point vocabulary (SKILL.md:882, 891)

`escalation_ladder_exhaust_point` (the 2nd `dedup_key` element) MUST be drawn from the closed set:
`{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (SKILL.md:882, restated :889, :891).
Free-form descriptions, paraphrases, or NL summaries (`"second retry"`, `"gap-fill round 2"`, `"after WebSearch exhaustion"`, `"escalation-ladder rung 3"`) are ALL rejected → `API-003-exhaust-point-vocabulary-violation` (R-120/R-121, SKILL.md:891).

### 1.3 Emission wire-shape (API-003-M6, SKILL.md:891)

The synthetic-dnsp finding MUST be a **structured Markdown block written into the partition agent's normal output stream** — the same stdout/report channel real findings use. NO separate signalling channel, sideband API, structured-result frame, or out-of-band metadata transport (SKILL.md:891). Consumed downstream by the merge step at §A.8 (Research Quality Gate merge) and §A.10 (Task File Validation merge); the merge treats it as a real finding for the existing **"any gap regardless of severity = FAIL"** gating rule (SKILL.md:891, gate rule at :861).

### 1.4 All-agents-fail Path A/B/C precedence (R-122, SKILL.md:897)

The emitter MUST gate on partition-cohort **success count BEFORE any per-partition emission attempt**, routing the cohort down exactly ONE of three mutually-exclusive paths:

- **Path A (zero-partitions-succeeded):** success count = `0` → existing `rf-team-lead's Fix Cycles rule` fix-cycle escalation fires; **NO synthetic emits** (a HIGH synthetic for every partition is informationally equivalent to escalation and adds noise — SKILL.md:895). At §A.8/§A.10 merge, the merge step is SKIPPED and the fix-cycle rule activates instead.
- **Path B (≥1-success AND ≥1-exhaust):** synthetic-dnsp emits **ALONGSIDE real findings** — one synthetic block per exhausted partition; **strictly additive, never replaces real findings**.
- **Path C (all-partitions-succeeded):** no synthetic; normal merge.

Mutually exclusive: a cohort that satisfies >1 path's precondition OR none (e.g. zero successes AND zero exhausts — every partition must terminate in success-or-exhaust) is a contract violation → `R-122-guard-precedence-violation` (SKILL.md:897).
**Byte-stability pin:** the `rf-team-lead's Fix Cycles rule` line MUST be byte-stable across the M6 landing — COMP-006-M6 preservation gate, sha256 `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` (SKILL.md:897). Path A activation MUST only route control to the existing fix-cycle escalation — never replace/short-circuit/modify it.

### 1.5 Strictly-additive merge + HIGH non-overridable (R-126, SKILL.md:901, 911)

- **Strictly additive:** post-merge real-finding count MUST equal pre-merge real-finding count **plus** synthetic count (SKILL.md:901, :911(a)). Any merge that drops/coalesces/filters real findings to make room for synthetic findings (incl. on severity-bucket collision) → `R-126-real-findings-replacement-violation` (:901).
- **HIGH non-overridable across the merge step:** no merge-time normalization, severity-downgrade transform, severity-coalesce rule, or operator-overridable severity flag may lower synthetic-dnsp severity below HIGH (SKILL.md:901, :911(b)). Merge-step override → `R-126-severity-override-violation` (distinct from the per-emission `DM-003-fixed-field-invariant-violation`: DM-003 = emission boundary; R-126 = merge/cohort layer).
- **Gate treatment:** a present synthetic-dnsp record causes **FAIL** until an operator manually reviews per the fixed `recommendation` literal; the gap-fill cycle MUST NOT attempt to auto-resolve synthetic-dnsp records (SKILL.md:911).
- **INV-021 N-1 cohort concurrency (R-125, SKILL.md:901):** when one partition's ladder exhausts, the remaining N-1 siblings MUST continue executing concurrently to their own success-or-exhaust terminal state BEFORE the exhausted partition's synthesis composes and BEFORE the §A.8/§A.10 merge runs. Serialization → `INV-021-cohort-serialization-violation`.

### 1.6 Dedup composition with PR-02 (INV-012, SKILL.md:899, 903)

- **Within-cycle collapse (R-123, :899):** two synthetic findings in the SAME retry cycle for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple collapse to one record with `found_n_times` incremented by exactly `1`. → `INV-012-within-cycle-collapse-violation`.
- **Cross-cycle composition (R-124, INV-012 non-regression, :899):** same `dedup_key` re-emitted on cycle `n+1` after cycle `n` is a **DEDUP case, NOT a regression** — contributes `1` (not `2`) to `|F_{n+1}|`. Cross-cycle collapse runs BEFORE the PR-02 monotonicity comparison (Step 2 of the 4-step ordering rule). MUST NOT trip Step 1 (regression) because `dedup_key ∈ FAIL_n ⟹ dedup_key ∉ PASS_n`. → `INV-012-cross-cycle-composition-violation`.

### 1.7 Symmetric application surfaces (SKILL.md:905–909)

The protocol applies symmetrically to: **A.8** research-gate partition spawns (rf-analyst + rf-qa); **A.10** task-integrity partition spawns (rf-qa, when partitioning invoked); **A.10.5** qualitative partition spawns (rf-qa-qualitative).

### 1.8 task-builder-specific vs Stage-7-validation reuse boundary (REQUESTED ANALYSIS)

The DM-003 contract is engineered around the **partition-cohort** model: N partition agents each own an `assigned_files` (or `assigned_phases`) slice and run an escalation ladder, with the cohort traversing exactly one R-122 path.

- **Reusable by the narrower sc:tasklist Stage-7-validation-agent case (the field-level wire contract):** the 7-field record shape, fixed `severity: HIGH` / `source: synthetic-dnsp`, the fixed `recommendation` literal, the 2-tuple `dedup_key` shape, the closed exhaust-point vocab, the API-003-M6 "normal output stream Markdown block" wire-shape, the strictly-additive merge semantics, and the HIGH-non-overridable invariant. These are surface-agnostic — they describe HOW a single exhausted agent encodes a synthetic finding and how the merge step preserves it.
- **task-builder-specific (the partition-cohort machinery) — sc:tasklist Stage-7 must MAP, not COPY:** R-122's three-path cohort-success-count gate, INV-021 N-1 cohort concurrency, `assigned_files` vs `assigned_phases` partition-slice semantics, and the §A.8/§A.10/§A.10.5 spawn-surface enumeration. sc:tasklist's Stage 7 fans out **2N validation agents** (one pair per phase file — see sc-tasklist SKILL.md:1464 "the same Task (Agent) primitive Stage 7 uses for its 2N validation fan-out") rather than partition cohorts over file slices. P3 in sc:tasklist therefore reuses the per-agent **emission/merge wire contract verbatim** but must define `affected_range` against its OWN cohort unit (the Stage-7 validation agent's assigned phase/finding slice) and apply the R-122 path gate against its OWN cohort-success count. This is a REUSE-of-contract / MAP-of-cohort split, not a fork: forking the field values, vocab, or merge semantics is the HALT condition; re-binding `affected_range`/cohort to Stage-7's fan-out unit is the legitimate adaptation.

### 1.9 Typed `StageError` for zero-success — DOES NOT EXIST (CONFIRMED)

`grep -rn "StageError" src/superclaude/skills/task-builder/ src/superclaude/skills/sc-tasklist-protocol/` returns **zero matches** (run 2026-06-19). A broader grep over `src/superclaude/` for `StageError` also returns nothing. **CONFIRMED: no typed `StageError` exists in current source.** The existing zero-success behavior is the **R-122 Path A** prose route (orchestrator escalates per the existing retry-then-Open-Questions / `rf-team-lead's Fix Cycles rule` flow — task-builder SKILL.md:895–897), NOT a typed exception. **Implementation-time decision flag for P3:** if a P-proposal wants a typed `StageError` for the zero-success / all-agents-fail case, that is a NEW implementation-time decision (no prior art to reuse) and must be designed against the existing Path A prose contract — it cannot claim to "reuse" an existing type.

---

## §2. P1 — `## Execution Context` contract (task-builder SKILL.md:1066–1071, 1231, 1389)

This is the surface P1 must REUSE so the two surfaces (P1 enrichment + existing Execution Context block) do not collide.

### 2.1 The required section + 3 sub-fields (EXECUTION_CONTEXT_INSTRUCTION, SKILL.md:1066–1071)

The builder MUST populate the `## Execution Context` section present in the MDTM template, **immediately after Prerequisites & Dependencies** (SKILL.md:1066). The three sub-bullets, with their EXACT discipline (SKILL.md:1067–1069):

- **References:** BUILD_REQUEST GOAL verbatim; WHY summary; related-doc IDs (`R-001`, `R-002`, …) — SKILL.md:1067.
- **Source areas:** named modules/packages identified in research — **NEVER specific file:line paths** (e.g. `"rf-qa agent prompts"`, `"task-builder skill body"`) — SKILL.md:1068.
- **Key constraints:** top 1-3 invariants from QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS / TESTING_REQUIREMENTS or research findings — SKILL.md:1069.

**Degradation rule:** Omit any sub-bullet lacking data. If GOAL is the only signal, emit **References only** (SKILL.md:1070, restated :1231 "degrades to References-only").

### 2.2 The "no file:line in the block header" rule (SKILL.md:1071, 1231, 1389)

- `## Execution Context` block header carries **NO specific `path.py:NN` references — those belong in per-item Context fields** (SKILL.md:1071).
- Restated at the build STEP: STEP 5a — "Do NOT include specific file:line paths in the block header" (SKILL.md:1231).
- **Structurally enforced by TB-Add-7** (SKILL.md:1389): *"Execution Context source areas reappear in items: every 'Source areas:' entry in the `## Execution Context` block reappears in at least one item's Context field; the block itself contains NO specific file:line references. INACTIVE if no Execution Context block exists."* TB-Add-7 is one of the imported sc:tasklist 17-point pre-write gate checks (SKILL.md:1383, CB-3 per-check classification).
- **Companion TB-Add-8** (SKILL.md:1390): per-item Context evidence binding — every item Context field referencing a code surface includes a `file:line` citation OR an `<!-- evidence-absence: ... -->` comment. "Structurally proves PR-01's 'no specific paths' rule is confined to the header (INV-015 scope-confinement)."

### 2.3 P1 non-collision obligation

P1's enrichment must write its References/Source areas/Key constraints into the SAME `## Execution Context` block surface (these exact sub-field names), preserve the **header-has-no-file:line / items-carry-file:line** split (TB-Add-7 ⇄ TB-Add-8, INV-015), and degrade to References-only when only GOAL is present. Forking a parallel "execution context" surface with different sub-field names, or putting file:line in the header, collides with TB-Add-7/TB-Add-8 and is a HALT. **Line numbers confirmed current: SKILL.md:1066–1071, 1231, 1383, 1389–1390 (read 2026-06-19).**

---

## §3. P2 — PR-02 Retry Monotonicity semantics (task-builder SKILL.md:1261–1305)

P2's bounded patch loop MUST reuse PR-02 (FR-CONV.5) — the "halt-guards wrapper layered ON TOP of every existing fix-cycle loop" (SKILL.md:1265). PR-02 introduces **NO new retry loop and NO new stage** — it adds two stop conditions evaluated BEFORE the existing iteration cap fires (SKILL.md:1265).

### 3.1 The two guards (SKILL.md:1267–1268)

1. **Monotonicity guard (SKILL.md:1267):** record remaining gate failures `F_n` at end of cycle `n`. If `F_{n+1} >= F_n` (count did NOT strictly shrink) → HALT and emit `[HALT-MONOTONICITY] |F|=<n>`. Fires only on strict non-shrink; `F_{n+1} = F_n - 1` (slow convergence) continues. Consulted ONLY when `|F_n| > 0` AND only after the regression check passed.
2. **Regression detection (SKILL.md:1268):** record items that PASSED at end of each cycle. If any item PASS at cycle `n` is FAIL at cycle `n+1` → HALT immediately and emit the regression halt string. Fires only on previously-PASS items.

### 3.2 Precedence: regression > monotonicity (SKILL.md:1270)

"Regression detection ALWAYS runs BEFORE the monotonicity check on every cycle transition `n → n+1`. When both conditions would trigger in the same cycle, the regression halt-message is emitted and the monotonicity check is NOT consulted on the regressed item." (SKILL.md:1270; the halt-precedence is also pinned at :1261, FR-CONV.5 / API-004.)

### 3.3 Byte-exact halt strings (API-004 wire ABI, M5 contract freeze, SKILL.md:1278–1283)

| Signal | Wire string (byte-exact) | Substitution |
|---|---|---|
| Monotonicity halt | `[HALT-MONOTONICITY] |F|=<n>` | `<n>` ← integer cardinality `|F_{n+1}|` at the cycle the guard fires |
| Regression halt | `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` | `X.Y` ← regressed item id; `N` ← prior-PASS cycle number |

Note the em-dash `—` in the regression string (not a hyphen) — byte-exact (SKILL.md:1268, 1283).

### 3.4 F-set definition (item identity = dedup-key, cardinality post-dedup, SKILL.md:1285–1292)

`F_n` is the SET of FAIL-verdict items at end of cycle `n`. Membership by dedup-key:
- Ordinary checklist items: dedup-key = item ID (e.g. `3.2`) — SKILL.md:1289.
- synthetic-dnsp findings (PR-03): dedup-key = `(assigned_files_range, escalation_ladder_exhaust_point)` — SKILL.md:1290.
`|F_n|` = cardinality of `F_n` AFTER dedup-key deduplication (SKILL.md:1292).

### 3.5 4-step ordering rule (strict, SKILL.md:1294–1303)

On every transition `n → n+1`, run in this exact order, EXIT on first match — `regression → monotonicity → hard-cap → proceed`:
1. **Regression check** → emit regression halt; do NOT consult subsequent steps (SKILL.md:1298).
2. **Monotonicity check:** if `|F_n| > 0` AND `|F_{n+1}| >= |F_n|` → emit monotonicity halt (SKILL.md:1299).
3. **Hard-cap check:** per-gate caps (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3; global 3-cycle backstop at `rf-team-lead's Fix Cycles rule`) → HALT per gate's escalation path (SKILL.md:1300).
4. **Proceed:** re-spawn fix cycle for `n+1` (SKILL.md:1301).
**Strict ordering invariant (SKILL.md:1303):** regression ALWAYS exits before monotonicity; monotonicity before hard-cap; hard-cap before proceed. Producers MUST NOT reorder/skip; consumers verify ordering by emission order in the execution log.

### 3.6 Full-set re-validation + independent counters (SKILL.md:1272, 1305)

- **Independent counters (SKILL.md:1272):** each retry counter (RESEARCH_NEEDED, MALFORMED, research-gate gap-fill, A.10, A.10.5, per-gate cycles) keeps its OWN `F_n` and PASS-set history. NEVER collapsed.
- **Regression non-emission invariant (SKILL.md:1305):** a regression halt MUST NOT fire for any item whose dedup-key was in `F_n` (FAIL_n) — the Step-1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is the ONLY regression trigger; cross-cycle dedup is excluded by construction. Consumers verify `grep -c "Regression detected on Item" <execution-log>` returns `0` for any cross-cycle same-dedup_key transition (TEST-022 at T05.14 / D-0065).

**P2 reuse obligation:** P2's bounded patch loop reuses (a) the F-set = post-dedup cardinality definition, (b) `|F_{k}| < |F_{k-1}|` strict-shrink monotonicity, (c) regression-precedence-over-monotonicity, (d) the byte-exact API-004 halt strings, and (e) the 4-step ordering. Full-set re-validation is implicit in the F-set semantics: `F_n` is recorded "at the end of each cycle" over the whole gate's item set, and regression detection requires re-evaluating PASS-set membership across the full set each cycle. A P2 loop that re-validates only the patched subset (not the full set) would be unable to detect regressions in previously-PASS items and would FORK PR-02. **Line numbers confirmed current: SKILL.md:1261–1305 (read 2026-06-19).**

---

## §4. Stage 10.5 reflect boundary — P2 non-overlap obligation

### 4.1 What Stage 10.5 operates on (sc-tasklist SKILL.md:1460–1481)

Stage 10.5 ("Pre-Reflect Sign-off") fans out **one `/sc:reflect --mode pre --remediate` agent per phase file in parallel** AFTER Stage 10 (final roadmap re-verification) completes (sc-tasklist SKILL.md:1460–1462). Each agent validates a generated **phase tasklist against its driving spec** — a coverage/best-practice audit of the FINAL, validated phase content, **before any execution spend** (SKILL.md:1462, 1466).

- **Finding set:** reflect mode=pre (UC-1) input is "a *proposed* tasklist/strategy plus its driving spec/PRD/objectives doc" → output is "a coverage matrix, a best-practice compliance grade, and a gap registry" (sc-reflect SKILL.md:39). It operates on **spec-coverage gaps / unmapped requirements**, NOT on QA-gate fix-cycle failures.
- `--mode pre` requires `--spec` (sc-reflect SKILL.md:108); UC-1 builds the spec→tasklist coverage map (SKILL.md:144, 300, 577).
- **`--remediate` behavior (sc-reflect SKILL.md:337–350):** Wave 6 runs ONLY when `--remediate` accepted (Tier 3). Reflect **AUTHORS but NEVER runs `/task`** (SKILL.md:339, 348 — the §"Will Not" invariant). It emits `remediation_task_path` (the authored corrective MDTM path) or `null` (SKILL.md:348, 757). Under headless `--print`, `--remediate` auto-accepts for AUTO-FIXABLE registers (Drift/Necessary only); HUMAN-REQUIRED registers (any Regression or `needs_human_decision: true`) author nothing auto-runnable and emit `remediation_task_path: null` (SKILL.md:339).

### 4.2 Why Stage 10.5 is fenced (sc-tasklist SKILL.md:1462, 1477)

Stage 10.5 is "fenced after the Stage 8-10 patch chain: Stage 9 mutates the phase files via `sc:task --compliance strict`, so a pre-reflect co-located with Stages 8-10 would race a file mid-patch" (SKILL.md:1462). It runs **non-blocking / advisory-blocking**: PARTIAL/FAIL records the verdict but the bundle STILL SHIPS (audit-first); `--remediate` only *offers* Tier-3 task-builder remediation and NEVER auto-mutates the phase file; any `needs_human_decision` item HALTs (SKILL.md:1477, citing `feedback_human_decision_items_must_halt`).

### 4.3 P2 disjointness proof obligation

For P2's bounded patch loop to be PROVEN disjoint from Stage 10.5's finding set (no finding remediated by both):
- **P2 (PR-02) operates on:** QA-gate / fix-cycle **FAIL-verdict items** (`F_n`) within the generation+validation patch chain (Stages 7→9), identified by dedup-key (item ID or synthetic-dnsp 2-tuple). Source: task-builder SKILL.md:1285–1292.
- **Stage 10.5 reflect-pre operates on:** **spec-coverage gaps / unmapped requirements** (UC-1 coverage matrix + gap registry), computed AFTER the Stage 8-10 patch chain finalizes, against the driving spec — NOT against QA-gate verdicts. Source: sc-reflect SKILL.md:39, 300; sc-tasklist SKILL.md:1462.
- **Disjointness lever:** the two sets live at different stages (P2 inside Stages 7-9 patch loop; reflect-pre at Stage 10.5 AFTER Stage 10), against different reference docs (P2 vs QA-gate verdicts; reflect-pre vs spec), with different remediation ownership (P2 patches inline via the fix-cycle; reflect-pre AUTHORS a corrective MDTM but NEVER auto-mutates — sc-reflect SKILL.md:339/348). A finding cannot be in both unless P2 were to re-run a spec-coverage audit (it does not — it consumes QA-gate F-sets). P2 MUST NOT widen its loop to spec-coverage gaps, and Stage 10.5 MUST stay fenced after the patch chain; that fence + the distinct finding-source is the disjointness guarantee.

---

## §5. sc:task delegate + tier algorithm

### 5.1 Stage 9 delegates to `sc:task` (sc-tasklist SKILL.md:1409–1427)

Stage 9 ("Patch Execution (Delegate to `sc:task`)") invokes `sc:task` via the **Skill tool** with input `"Execute TASKLIST_ROOT/validation/PatchChecklist.md"` and `--compliance strict` (SKILL.md:1413–1416). `sc:task` handles reading the checklist, applying edits to each phase file, tracing changes for compliance, and tier-appropriate verification (SKILL.md:1418–1423). "The orchestrator does NOT apply patches itself. Separation of concerns: the tasklist-protocol generates and validates; `sc:task` executes edits." (SKILL.md:1425). Stage gate at :1427. Confirmed in the stage tables: SKILL.md:1539, 1572, 1600 (`sc:task --compliance strict`).

### 5.2 Tier algorithm `STRICT > EXEMPT > LIGHT > STANDARD` (CONFIRMED)

The priority order appears verbatim **three times** in sc-tasklist SKILL.md:
- `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)` — SKILL.md:414
- `**Priority order:** STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)` — SKILL.md:548
- `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)` — SKILL.md:1206

Each task receives a Compliance Tier computed deterministically via the `/sc:task` classification algorithm (sc-tasklist SKILL.md:546; tiers STRICT/STANDARD/LIGHT/EXEMPT at :41). The sc:task execution semantics per tier are at sc-task-protocol SKILL.md: STANDARD/LIGHT/EXEMPT execution at :100–118, verification table at :124–129 (STRICT→sub-agent quality-engineer; STANDARD→direct test exec; LIGHT/EXEMPT→skip), Critical-Path Override (`auth/ security/ crypto/ models/ migrations/` → CRITICAL regardless of tier) at :131, Trivial-Path Override (`*.md docs/ *test*.py` may skip) at :133.

### 5.3 `sc:task-unified` is NOT a current name (CONFIRMED)

`grep -rn "sc:task-unified\|sc-task-unified\|task-unified" src/superclaude/` (run 2026-06-19) returns matches ONLY for the string `task-unified` as a **`--caller` value** in the troubleshoot↔task-protocol TFEP wire contract (troubleshoot.md:60/69; sc-task-protocol SKILL.md:217/241/270/271; troubleshoot SKILL.md:148/471/479/481; report-template.md:158). There is **NO skill, command, or skill-name `sc:task-unified` / `sc-task-unified`**. The unified-task SKILL is named `sc-task-protocol` (skill name `sc:task-protocol`), invoked as `sc:task`. **CONFIRMED: `sc:task-unified` is not a real invocation name** — `task-unified` exists only as the `--caller` identity string passed to `/sc:troubleshoot` so it emits a `return-contract.yaml` adapter. P-proposals MUST delegate to `sc:task`, never `sc:task-unified`.

---

## §6. Sprint parser conventions (NFR-RFMERGE.4) — src/superclaude/cli/sprint/config.py

Quoted verbatim (read 2026-06-19).

### 6.1 Phase filename regex — `PHASE_FILE_PATTERN` (config.py:20–32)

```python
PHASE_FILE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:phase-(\d+)-tasklist\.md"
    r"|phase-(\d+)r-tasklist\.md"
    r"|p(\d+)-tasklist\.md"
    r"|phase_(\d+)_tasklist\.md"
    r"|tasklist-p(\d+)\.md)(?![A-Za-z0-9])",
    re.IGNORECASE,
)
```

Canonical accepted filenames (config.py:15–19 comment + the alternation): `phase-1-tasklist.md`, `p1-tasklist.md`, `phase_1_tasklist.md`, `tasklist-p1.md`, PLUS the v4.3.0 rerun-bundle variant `phase-Nr-tasklist.md` (config.py:22–27: trailing `r` marks a rerun-bundle tasklist; captured digits are still the phase number). Case-insensitive (`re.IGNORECASE`). The canonical generator-emitted name P-proposals should target is `phase-<N>-tasklist.md` (matches `phase-(\d+)-tasklist\.md`; also the form used at sc-tasklist SKILL.md:1470 `--tasklist TASKLIST_ROOT/phase-<P>-tasklist.md`).

### 6.2 Task heading regex — `_TASK_ID_HEADING_RE` (config.py:34–40)

```python
_TASK_ID_HEADING_RE = re.compile(
    r"^###\s+T\d{2}\.\d{2}\b",
    re.MULTILINE,
)
```

Matches canonical task headings `### T<PP>.<TT>` — exactly two digits, dot, two digits (config.py:34, 37–40). Used by `count_tasks_in_file` (config.py:43–55) to pre-scan total task count (TUI dual progress bar, F3). Missing/unreadable files return 0 (config.py:51–54). **Implication for P-proposals:** generated task headings MUST be `### T<PP>.<TT>` with zero-padded two-digit phase + two-digit task (e.g. `### T06.05`); a non-padded `### T6.5` would NOT match and the task would be invisible to the sprint pre-scan.

### 6.3 Execution Mode enum {claude, python, skip} (config.py:116–124, 131, 143)

In `discover_phases`, the optional markdown-table "Execution Mode" column is parsed (config.py:73–124). The allowed set is enforced literally (config.py:116):

```python
allowed = {"claude", "python", "skip"}
if raw_mode not in allowed:
    raise click.ClickException(
        f"Unknown execution mode '{raw_mode}' for file '{filename}'. "
        f"Allowed: claude, python, skip"
    )
```

Mode is lowercased before comparison (config.py:115 `.strip().lower()`). Default when the column is absent / a phase is discovered without a mode entry: `"claude"` (config.py:124, 131, 143). **Implication:** if P-proposals emit an Execution Mode column, every value MUST be one of `claude` / `python` / `skip` (case-insensitive) or the sprint CLI raises `click.ClickException` at discovery.

---

## §7. Summary — REUSE map (every contract is a no-fork obligation)

1. **P3 → DM-003** (task-builder SKILL.md:873–911): reuse the 7-field record (8 incl. dedup_key tuple elements), fixed `severity: HIGH` / `source: synthetic-dnsp`, fixed `recommendation` literal `Manual review required — partition agent failed twice`, 2-tuple `dedup_key` with closed exhaust vocab `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`, `found_n_times` (default 1, +1 per within-cycle collapse), R-122 Path A/B/C cohort-success gate, strictly-additive merge, HIGH-non-overridable (R-126), API-003-M6 normal-output-stream wire-shape. Narrower Stage-7 case reuses the per-agent wire/merge contract verbatim but MAPS `affected_range`/cohort to its own 2N fan-out unit (not a fork). **No typed `StageError` exists — new implementation-time decision (CONFIRMED via grep).**
2. **P1 → `## Execution Context`** (task-builder SKILL.md:1066–1071, 1231, 1389): reuse References / Source areas / Key constraints sub-fields, the no-file:line-in-header rule, References-only degradation, TB-Add-7 ⇄ TB-Add-8 (INV-015).
3. **P2 → PR-02** (task-builder SKILL.md:1261–1305): reuse regression > monotonicity precedence, F-set = post-dedup cardinality, `|F_{k}| < |F_{k-1}|` strict-shrink, byte-exact API-004 halt strings, 4-step ordering, full-set re-validation.
4. **P2 disjointness** (sc-tasklist SKILL.md:1460–1481; sc-reflect SKILL.md:39, 339): Stage 10.5 reflect-pre operates on spec-coverage gaps post-Stage-10, AUTHORS-not-runs remediation; P2 operates on QA-gate F-sets inside Stages 7-9. Distinct stage + distinct finding-source + distinct remediation-ownership = disjoint.
5. **Stage 9 / sc:task** (sc-tasklist SKILL.md:1409–1427): patching delegates to `sc:task --compliance strict`; tier `STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4)` (SKILL.md:414/548/1206). `sc:task-unified` is NOT a real name — `task-unified` is only a TFEP `--caller` string (CONFIRMED via grep).
6. **Sprint parser** (config.py): `PHASE_FILE_PATTERN` (config.py:20–32) accepts `phase-N-tasklist.md` etc.; `_TASK_ID_HEADING_RE = ^###\s+T\d{2}\.\d{2}\b` (config.py:37–40) requires zero-padded `### T<PP>.<TT>`; Execution Mode ∈ `{claude, python, skip}` default `claude` (config.py:116–124).

**No "Unverified" items** — every field above cites a current file:line confirmed by Read/grep on 2026-06-19.
