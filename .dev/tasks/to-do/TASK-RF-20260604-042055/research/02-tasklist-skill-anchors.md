# Research: sc-tasklist-protocol SKILL.md anchors

Status: Complete
Date: 2026-06-04

Scope: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1491 lines) only, in repo `/config/workspace/IronClaude/.claude/worktrees/ReflectInTaskLists/`.
Goal: exact CURRENT line anchors for every edit site of `.dev/proposals/reflect-in-sc-tasklist.md` (§1-§6 + Flag/stage summary). All line numbers below are from a fresh Read/Grep of the current file.

> **Headline drift verdict:** The proposal's checkpoint-invariant citations (#6 @1073, #18 @1113, #19 @1114, #20 @1115) are **STILL ACCURATE** — they did not drift. The 10-stage table is at **1394-1405** (proposal cited `:1394-1405` — accurate). Most other cites are accurate or off by ≤3 lines; corrected below.

---

## Edit Site 1 — Stage 10 end (insertion point for new Stage 10.5 "Pre-Reflect Sign-off")

**Heading:** `### Stage 10: Spot-Check Verification` — **line 1359**.

**Stage 10 body runs 1359-1386.** Its terminal content (the insertion point for a NEW `### Stage 10.5`) is:

- Line **1386**: `**Stage gate**: All findings verified. If any remain `UNRESOLVED`, they are logged but the skill does NOT loop. The `ValidationReport.md` serves as the record for human review.`
- Line **1388**: `---` (horizontal rule closing the Stage 10 section)
- Line **1390**: `## Stage Completion Reporting Contract` (next top-level section)

**→ Insert `### Stage 10.5: Pre-Reflect Sign-off` between line 1386 and the `---` at 1388** (after the Stage 10 gate text, before the section rule). This is the exact spot proposal §1(a) calls "after Stage 10 (the final roadmap re-verification)". (Proposal cited Stage 10 at `:1359-1386` — **accurate**.)

**Fence note (proposal Decision B / Risk 5):** Stage 9 (the file-mutating patch chain) is `### Stage 9: Patch Execution (Delegate to `sc:task`)` at **line 1339**; `sc:task --compliance strict` patch input line `"Execute TASKLIST_ROOT/validation/PatchChecklist.md"` at **1345**; dependency-chain block **1415-1420** (`Stage 9 is blocked by Stage 8` @1419, `Stage 10 is blocked by Stage 9` @1420). All confirmed.

---

## Edit Site 2 — The 10-stage table (proposal: becomes 11)

**Section heading:** `## Stage Completion Reporting Contract` — **line 1390**.
**Lead sentence (update 10→11):** line **1392**: `The skill executes in 10 stages with per-stage validation. ...`

**The table — lines 1394-1405:**

```
1394 | Stage | Name | Validation Criteria |
1395 |-------|------|---------------------|
1396 | 1 | Input Ingest | ... |
...
1400 | 5 | File Emission | tasklist-index.md written; all phase files referenced in index exist on disk; no extra phase files written |
1401 | 6 | Self-Check | All Sprint Compatibility Self-Check assertions pass; no blocking failures |
1402 | 7 | Roadmap Validation | 2N agents completed; findings merged and deduplicated; zero agent failures |
1403 | 8 | Patch Plan Generation | ... |
1404 | 9 | Patch Execution | ... |
1405 | 10 | Spot-Check Verification | All findings from ValidationReport.md re-verified; results appended to report |
```

**→ Add a `| 10.5 | Pre-Reflect Sign-off | ... |` row after line 1405** + update line 1392 "10 stages" → "11 stages". (Proposal cited `:1394-1405` — **accurate**.)

**Companion stage-bookkeeping blocks that ALSO enumerate stages (NOT cited in proposal — FLAGGED as additional edit sites the builder must keep consistent):**
- **Line 1392** — "executes in 10 stages" prose.
- **Line 1424** — `On skill start, create 10 tasks via TaskCreate with dependencies:` → add Stage 10.5 TaskCreate to block **1427-1436**.
- **Dependency block 1444-1449** (`Stage 10: blockedBy Stage 9` @1449) → add `Stage 10.5: blockedBy Stage 10`.
- **Completion-line block 1457-1462** (`Stage 10: "Spot-Check: ..."` @1462) → add a Stage 10.5 completion line.
- **Tool Usage table 1472-1480**: `Task` (Agent) row @ **1479** — Stage 10.5 reuses this primitive (Edit Site 7).

---

## Edit Site 3 — Stage 5 (File Emission): where the templated POST reflect task is appended

**There is NO `### Stage 5` heading.** Stage 5 = "File Emission"; its behavior is specified by the **File Emission Rules** section + the **phase-file templates**, and only *named* "Stage 5" in the stage table (1400) and bookkeeping (1431, 1444, 1457).

The POST reflect task (proposal §1(b): "appended after the end-of-phase checkpoint") is templated at the phase-file tail. Authoritative anchors:

- `### File Emission Rules (Deterministic)` — **line 91**. Phase-file content contract at **line 96**: `phase-1-tasklist.md ... Contains: phase heading, phase goal, tasks (in order), inline checkpoints, end-of-phase checkpoint` — **the list the POST reflect task must be added to.**
- `#### End-of-Phase Checkpoint (Mandatory, Last Task)` — **lines 1011-1027** (Edit Site 5). **The exact template block after which the POST reflect task is appended.** Current rule "No task may appear below it" (line 1021) is what the proposal amends.

**→ Insert the POST-reflect template (proposal §1(b)) as a new sub-section immediately AFTER the End-of-Phase Checkpoint block (after line 1027, before the `---` at 1029),** and amend the content contract at **line 96**. There is no single "Stage 5 emission section" — the builder edits lines 91/96 + 1011-1027.

---

## Edit Site 4 — CHECKPOINT-IS-LAST INVARIANT SET (4 places — ALL FOUND ✓)

All four located + quoted verbatim. **Proposal's cited lines (1073/1113/1114/1115) are STILL CORRECT — no drift.**

### #6 — Self-Check check #6 ("every phase file ends with an end-of-phase checkpoint task")
**Line 1073** (in `## Sprint Compatibility Self-Check (Pre-Write, Mandatory)`, heading @1062):
```
1073 | 6. Every phase file ends with an end-of-phase checkpoint task (per checks 18-20)
```
Note: #6 explicitly delegates to "checks 18-20" — amending #6 structurally requires amending 18/19/20 too (the proposal's "amend all four together" is enforced by this cross-ref).

### #18 — structural check #18 (sprint-scanner tie-in)
**Line 1113** (in `### Structural Quality Gate (Pre-Write, Mandatory)` table, heading @1104, table starts @1106):
```
1113 | 18 | Checkpoint task emission: every checkpoint block in each phase is emitted as a `### T<PP>.<NN> -- Checkpoint:` task heading (never as a sibling `### Checkpoint:` heading) | Cause-2 fix (v3.7 Wave 4): keeps checkpoints visible to the sprint task scanner |
```

### #19 — structural gate #19 ("checkpoint has highest <NN>, no regular task following")
**Line 1114**:
```
1114 | 19 | End-of-phase position: the `### T<PP>.<NN> -- Checkpoint: End of Phase <PP>` task has the highest `<NN>` in its phase, with no regular task following it | Ensures the end-of-phase gate is the last instruction the agent sees |
```
**Core invariant the proposal amends** ("post-reflect may follow the end-of-phase checkpoint").

### #20 — structural gate #20 (`_verify_checkpoints`/`build_manifest` tie-in)
**Line 1115**:
```
1115 | 20 | Checkpoint Report Path presence: every checkpoint task includes a `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<name>.md` line immediately below its metadata table | Lets Wave 2/3 tooling (`_verify_checkpoints`, `build_manifest`) parse the expected file path |
```

**Gate close-line — line 1117:** `If any check 1-20 fails, fix it before writing any output file.` → FLAG: if the builder adds a NEW check for the post-reflect task, line 1117 ("check 1-20") and line 1073 ("per checks 18-20") both need updating.

**RISK ASSESSMENT: ALL 4 INVARIANTS FOUND. None renumbered or removed.** Lowest-risk of the edit clusters — proposal lines are accurate.

---

## Edit Site 5 — End-of-phase checkpoint task DEFINITION + "no regular task after" rule

**Two locations encode the rule (both must be amended for the post-reflect carve-out):**

**(a) The cadence rule** — `### 4.8 Checkpoints (Exact Cadence)` (heading @343), **lines 356-359**:
```
356 - Emit exactly one end-of-phase checkpoint as the **last** task of each phase:
357   - `### T<PP>.<last_num> -- Checkpoint: End of Phase <PP>`
359     the phase. No regular task may appear after the end-of-phase checkpoint.
```
(Proposal cited `:356-359` — **accurate**. Literal rule string "No regular task may appear after the end-of-phase checkpoint" is at **line 359**.)

**(b) The template definition** — `#### End-of-Phase Checkpoint (Mandatory, Last Task)` — **lines 1011-1027**:
```
1011 #### End-of-Phase Checkpoint (Mandatory, Last Task)
1014 **last** numbered task in the phase:
1017 ### T<PP>.<last_num> -- Checkpoint: End of Phase <PP>
1020 `<last_num>` must be strictly greater than every regular task number in the
1021 phase. No task may appear below it. All other checkpoint-task fields ...
```
(Proposal cited `:1011-1027` — **accurate**. Line **1014** "**last** numbered task" + line **1021** "No task may appear below it." are the two literal phrases Decision C1 amends to "the post-reflection task is the sole task permitted to follow it.")

---

## Edit Site 6 — Deterministic signal sources for COMPLEXITY_SCORE (all CONFIRMED emitted/persisted)

| Signal (proposal §4) | Where defined / emitted | Current line(s) | Persisted? |
|---|---|---|---|
| **Tier Distribution per phase** | `#### Phase Files Table` (index) | hdg **703**; tbl **707-711**; rule "Tier Distribution shows count per tier" @ **718** | **YES** — `tasklist-index.md` Phase Files table, col 5. (Cited `:707-718` — accurate.) |
| **Traceability Matrix `R-###→T<PP>.<TT>`** | `#### Traceability Matrix` (index) + §5.7 | index hdg **759**, tbl hdr **765**, rules **768-773**; §5.7 hdg **647** | **YES** — `tasklist-index.md`. (Cited `:759-773`,`:647-653` — accurate.) |
| **Critical Path Override** (auth/security/crypto/models/migrations) | `### 4.11 Critical Path Override (deterministic)` | hdg **425**; paths @ **429**; `Set CPO: Yes` @ **433**; per-task field row @ **876** | **YES** — per-task metadata field. (Cited `:425-435` — accurate.) |
| **Risk: High scoring** | Risk score→label map | `4+ -> High` @ **532**; band block **530-533**; scoring inputs **522-529** | **YES** — per-task `Risk` field. (Cited `:529-531`; the High line is at **532** — minor drift.) |
| **Task count (`n_tasks`)** | Index `Total Tasks` (bundle) + per-phase | bundle @ **682**; per-phase "Task IDs" col @ **707-711**; count by `### T<PP>.<TT>` @ **1182** | **YES** (bundle); per-phase derivable from range col @707 or heading count. |

- **`n_strict`** = read directly from Tier Distribution cell (`STRICT: N`, format @718) — persisted, no inference.
- **`n_R`** = distinct R-### per phase via Traceability Matrix (765) task-ID→phase join — persisted.

**Dropped `multifile` signal (proposal §4 "Dropped signal"):** the ">2 files affected" tier booster — confirmed the file-count is a *transient* tier-scoring input, **NOT persisted** as a per-task flag (no such column in task metadata table @ **862-916** nor in any index registry @ **707-773**). Proposal's drop is **correct + evidence-backed**: no emitted field to read it from.

**Verdict: all 5 COMPLEXITY_SCORE inputs (`n_strict`, `n_tasks`, `n_cpo`, `n_high_risk`, `n_R`) are deterministically emitted/persisted (Phase Files table + Traceability Matrix + per-task metadata). The depth map is computable post-emission with zero inference.**

---

## Edit Site 7 — Stage 7 parallel `Task` fan-out primitive (reused by Stage 10.5)

`### Stage 7: Roadmap Validation (2N Parallel Agents)` — **line 1174**.

- Agent-spawning algorithm: **lines 1178-1193**.
- Key line **1193**: `This produces **2N agents** total, all spawned via the `Task` tool (Agent) and run in parallel.`
- Per-phase fan-out loop `For each of the N phase files:` @ **1180**; task counting by `### T<PP>.<TT>` headings @ **1182**.
- Tool Usage table confirmation — **line 1479**: `| `Task` (Agent) | Spawn 2N parallel validation agents | Roadmap Validation (Stage 7) |`.

**→ Stage 10.5 (proposal §1(a)) reuses THIS `Task` primitive** — "same primitive as Stage 7's 2N fan-out", but one agent per phase (N, not 2N). Builder mirrors the spawn-loop at 1180-1193 + adds a row/note to the Tool Usage table @1479. (Cited `:1174-1226`,`:1479` — accurate.)

---

## Edit Site 8 — `TASKLIST_ROOT/validation/` directory convention

**Anchors:**
- **Line 87** (Section 3 intended-locations list): `- Validation reports: `TASKLIST_ROOT/validation/``
- **Line 120** (Target Directory Layout tree, 110-123): `validation/` listed under TASKLIST_ROOT.
- **Line 700** (index "Artifact Paths" table): `| Validation Reports | `TASKLIST_ROOT/validation/` |`
- Stage 8 writes existing artifacts there: **1257** (`ValidationReport.md`), **1290** (`PatchChecklist.md`); `mkdir -p` @ **1337**.

**→ Proposal adds `reflect-pre/`, `reflect-post/`, `depth-map.yaml` under `validation/`.** Builder extends: layout tree (after line 120), intended-locations note (near line 87), index Artifact Paths table (line 700). Parent convention confirmed at 87/120/700.

---

## Edit Site 9 — `--dry-run` handling

**`--dry-run` / `--no-reflect` / `--no-validate` are ABSENT from the skill** — grep for `dry.?run|no-reflect|no.?validate` = **zero matches**.

- Only flags recognized today: `--spec`, `--output` (argument-hint @ **line 9**: `argument-hint: "<roadmap-path> [--spec <spec-path>] [--output <output-dir>]"`).
- `--spec` handling: `### 4.1a Supplementary TDD Context (conditional on --spec flag)` @ **166**; `### 4.4a Supplementary Task Generation (conditional on --spec flag)` @ **243**; Stage 7 supplementary validation @ **1227-1238**.

**Consequence (proposal §6 + `feedback_dryrun_skips_subskills.md`):** No dry-run surface exists to amend. `--no-reflect` and any "dry-run skips both gates" behavior are NEW. The argument-hint at **line 9** is the single skill-side edit site to add `--no-reflect` (the `commands/tasklist.md` Arguments table is R3's scope). No "dry-run skips sub-skills" text exists in this skill to mirror.

---

## Summary: edit-site → current-line map

| # | Edit site | CURRENT line(s) | Proposal-cited | Drift? |
|---|---|---|---|---|
| 1 | Stage 10 heading / end (insert Stage 10.5 after) | hdg **1359**; gate @1386; `---` @1388 | `:1359-1386` | none ✓ |
| 2 | 10-stage table (→11) | table **1394-1405**; "10 stages" @**1392** | `:1394-1405` | none ✓ |
| 2b | Stage bookkeeping (TaskCreate/deps/completion) | 1424, 1427-1436, 1444-1449, 1457-1462 | (not cited) | NEW sites flagged |
| 3 | Stage 5 emission (append POST task) | contract @**91/96**; emit-after @**1027** | (no `### Stage 5` heading) | clarified ✓ |
| 4a | **Self-Check check #6** | **1073** | `:1073` | **none ✓** |
| 4b | **structural check #18** | **1113** | `:1113` | **none ✓** |
| 4c | **structural gate #19** | **1114** | `:1114` | **none ✓** |
| 4d | **structural gate #20** | **1115** | `:1115` | **none ✓** |
| 4e | gate close-line "check 1-20" | **1117** | (not cited) | NEW flag |
| 5a | "no regular task after checkpoint" rule | **356-359** (string @**359**) | `:356-359` | none ✓ |
| 5b | End-of-Phase Checkpoint template | **1011-1027** (@**1014**,@**1021**) | `:1011-1027` | none ✓ |
| 6a | Tier Distribution per phase | hdg **703**; tbl **707-718** | `:707-718` | none ✓ |
| 6b | Traceability Matrix (R-###→T) | index hdg **759**, tbl **765**; §5.7 @**647** | `:759-773`,`:647-653` | none ✓ |
| 6c | Critical Path Override | hdg **425**; paths @**429**; set @**433**; field @**876** | `:425-435` | none ✓ |
| 6d | Risk High scoring | `4+ -> High` @**532**; band 530-533 | `:529-531` | minor (+~1-3) |
| 6e | task count | `Total Tasks` @**682**; per-phase @707 / count @**1182** | (n/a) | confirmed persisted |
| 6f | dropped `multifile` (NOT persisted) | task meta tbl **862-916** (absent) | `:596-604` (booster) | confirmed not-persisted ✓ |
| 7 | Stage 7 `Task` fan-out (2N) primitive | hdg **1174**; algo 1178-1193; @**1193**; tool tbl @**1479** | `:1174-1226`,`:1479` | none ✓ |
| 8 | `TASKLIST_ROOT/validation/` convention | **87**, **120** (tree), **700** (index tbl) | (parent dir) | confirmed ✓ |
| 9 | `--dry-run` handling | **ABSENT** (0 matches); argument-hint @**9** | (memory-driven) | NEW surface |

### Checkpoint-invariant set status (the 4 critical anchors): ALL FOUND, ZERO DRIFT.
- #6 @ **1073** ✓ · #18 @ **1113** ✓ · #19 @ **1114** ✓ · #20 @ **1115** ✓
- Bonus structural couplings the builder must amend alongside: line **1073** cross-refs "checks 18-20"; line **1117** says "check 1-20" — both need consistency if a 21st check is added.
