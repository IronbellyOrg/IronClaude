# Cross-Validation Report — RFMerger P1–P5 Build (Partition A)

**Date:** 2026-06-19
**Analysis type:** completeness-verification / cross-validation lens
**Partition:** A of N — source-mapping/contract/citation cluster
**Assigned files (4):**
- R01: 01-skill-stage-map.md
- R03: 03-integration-contracts.md
- R04: 04-proposal-attachment-trace.md
- R07: 07-citation-crossval-and-spec.md

**Lens focus:** Cross-validate claims BETWEEN these 4 files. Flag contradictions, conflicting line numbers, divergent descriptions of the same attachment point/contract. Adversarial — find divergence.

[PARTITION NOTE: Cross-file checks limited to assigned subset (R01/R03/R04/R07). Full cross-file analysis requires merging all partition reports.]

---

## Q1 — Do R01, R04, R07 agree on CURRENT line anchors for each P1–P5 attachment point?

Cross-check of the anchor each file pins for the same physical edit site. Sources cited from BOTH sides.

### P1 — `## Execution Context` block (attach surface)

| Aspect | R01 | R04 | Verdict |
|---|---|---|---|
| Where P1 EMITS | **per-task body** of the Phase File Template, `SKILL.md:894-927` (Steps :904, Notes :927); mirror `templates/phase-template.md:55-82` (R01:58-64) | **Index file** — `## Execution Context` in `tasklist-index.md`, after Artifact-Paths table (after `SKILL.md:707`), before `#### Phase Files Table` (709) (R04:80-87) | **CONTRADICTION (material).** R01 = phase-file task body (`SKILL.md:894-927`). R04 = index file (after `SKILL.md:707`). Different files AND different line regions for the SAME proposal. See Q5. |

**R07 is silent on the P1 sc-tasklist emit site** (it verifies the task-builder source contract at `task-builder/SKILL.md:1066-1071`, not the sc-tasklist emit anchor). Q1-P1 is an R01-vs-R04 disagreement.

### P5 — `## Tier Calibration Advisory` (attach surface)

| Aspect | R01 | R04 | R07 | Verdict |
|---|---|---|---|---|
| Emit surface | Index file, after `#### Feedback Collection Template` (`SKILL.md:820-839`) before `#### Glossary` (`SKILL.md:841`) (R01:69) | Index file, **after `SKILL.md:839`, before `SKILL.md:841`** (R04:137-139) | feedback template region present (R07) | **AGREE.** Both R01 and R04 land P5 after Feedback Collection Template (ends 839), before Glossary (841). Identical anchor. |
| Tier-scoring core (must NOT mutate) | §5.3 `SKILL.md:544`; priority `:548`; §5.4 `:616-629` (R01:68,75) | §5.3 `544-629` core; confidence `:622` (R04:110-116) | §5.3 heading at **544**; body `544-648` (R07:36) | **AGREE.** All three converge on 544 as §5.3 start. No conflict. |

### P4 — gate-results.txt emit (Stage 6 end) + Stage 7 inject

| Aspect | R01 | R04 | R07 | Verdict |
|---|---|---|---|---|
| Stage-6 gate close anchor | `SKILL.md:1187` ("If any check 1-20 fails…"); emit after, before `## Final Output Constraint` 1191 (R01:93-95) | `SKILL.md:1187`; serialize after 1187 (R04:164,209,372) | Gate body `1132-1187`, ends at **1187** (R07:29) | **AGREE.** All three: gate closes at `SKILL.md:1187`; P4 emit attaches after 1187. |
| Stage-7 inject anchor | spawn payload `SKILL.md:1254-1262`; instructions `1265-1286`; augment after `:1267` (R01:108-115) | inject after intro line `1267-1268`, before Drift `1271`; or spawn bullets `1255-1261` (R04:190-195) | (not separately pinned) | **AGREE** (R01 vs R04). Both name spawn payload (`1254-1262`/`1255-1261`) + instruction intro (`~1267-1268`). Consistent paragraph. |

### P3 — synthetic-dnsp on Stage-7 agent failure (orchestrator merge)

| Aspect | R01 | R04 | Verdict |
|---|---|---|---|
| Merge-step anchor | `**Orchestrator merge and deduplication**` `SKILL.md:1288-1295`; insert between steps 1 (`1292`) and 4 (`1295`) (R01:118-123) | merge `1288-1295`; insert after step 1 `1292`, before step 2 `1293` (R04:226-229,251-255) | **AGREE.** Both: merge block `1288-1295`; new step immediately after `1292`. R04 more precise; no conflict. |
| Retry/gate clause | `SKILL.md:1310` ("retry once before reporting error") (R01:120) | `SKILL.md:1310` (replace gate sentence) (R04:230-232,255) | **AGREE.** Both pin `SKILL.md:1310`. |

R07 verifies the task-builder DM-003 contract at `873-911`, not the sc-tasklist merge anchor — silent here (correct division of labor, not a contradiction).

### P2 — bounded patch loop (Stage 10 origin → Stage 9 target)

| Aspect | R01 | R04 | R07 | Verdict |
|---|---|---|---|---|
| Loop ORIGIN (no-loop sentence) | `SKILL.md:1456` ("…the skill does NOT loop…") (R01:153-155) | `SKILL.md:1456` (replace no-loop gate) (R04:282-284,305-309) | (Stage 9 `1409-1427`, 10.5 `1460-1481` confirmed; 1456 not separately pinned) | **AGREE.** Both pin `SKILL.md:1456` as the no-loop sentence P2 replaces. |
| Loop TARGET (Stage 9) | `SKILL.md:1413`/`:1427` (R01:141,156) | Stage 8 regen → Stage 9 `1409-1427` (R04:307-309) | Stage 9 `1409-1427` present (R07:33) | **AGREE.** All consistent (`:1413`/`:1427` ⊂ `1409-1427`). |
| Stage 10.5 fence | `SKILL.md:1462` race-avoidance (R01:163) | `SKILL.md:1462` fence note (R04:315-322) | Stage 10.5 `1460-1481` fenced (R07:32) | **AGREE.** All three: fence at `SKILL.md:1462`. |

### Q1 VERDICT
- **P1: CONTRADICTION** — R01 (phase-file task body `SKILL.md:894-927`) vs R04 (index file after `SKILL.md:707`). Material; both cannot be right. Escalated to Q5.
- **P2, P3, P4, P5: AGREE** — every pinned anchor matches across the files that pin it.

---

## Q2 — Do R03 and R07 agree on the task-builder DM-003 contract location (873–911) and field set?

| Aspect | R03 | R07 | Verdict |
|---|---|---|---|
| Contract location | task-builder `SKILL.md:873–911` (heading at 873) (R03:23,31,33) | `task-builder/SKILL.md:873-911`; heading at 873 (R07:20) | **AGREE.** Identical range and heading line. |
| PR-03 = BASE proposal | "PR-03 is the BASE proposal of this release" (R03:33) | heading reads "DNSP Synthetic Finding Protocol (PR-03 …)" (R07:20) | **AGREE.** |
| Emitter field rows | `severity` 877, `source` 878, `affected_range` 879, `evidence` 880, `recommendation` 881, `dedup_key` 882, `found_n_times` 883 (R03:41-47) | fields at 877-883: severity/source/affected_range/evidence/recommendation/dedup_key/found_n_times (R07:20) | **AGREE.** Same 7 named fields, same 877-883 block. |
| Reject-symbol lines | R-113/R-114 :885; R-115/R-116 :887; R-117/R-118/R-119 :889; R-120/R-121 :891 (R03:41-47,55) | R-113/R-114 at 885; R-115/R-116 at 887; R-117/R-118/R-119 at 889; R-120/R-121 at 891 (R07:20) | **AGREE.** Every reject-symbol line number matches exactly. |
| A.8 merge step | strictly-additive merge + R-126 at :901, :911; gate FAIL treatment at :911 (R03:74-76) | "A.8 merge step R-127 at 911" (R07:20) | **MINOR NOTE (not a contradiction).** Both place a merge/gate clause at line 911. R03 labels the merge invariants R-126; R07 labels the A.8 merge step "R-127". These are different rule symbols at the same region (911), not conflicting line numbers — R-126 (HIGH-non-overridable/additive) and R-127 (A.8 pick-up wiring) are distinct rules. No line-number conflict; symbol labels are complementary, not divergent. |

### Field-COUNT reconciliation (7 vs 8)
- R03 explicitly addresses this: "the protocol enumerates the record as **7 named YAML fields** … `dedup_key` is itself a 2-tuple, so the literal field count is 7; the task brief's '8 fields' counts the dedup_key 2-tuple's two elements separately" (R03:48-49).
- R07 lists exactly 7 named fields (R07:20).
- **AGREE.** Both report 7 named fields; the "8" in the build brief is the dedup_key tuple counted as two. No divergence — R03 reconciles it openly and R07's enumeration corroborates.

### Q2 VERDICT
**AGREE.** R03 and R07 fully concur on the DM-003 contract location (`873–911`), the 7-field set (877-883), every reject-symbol line, and the 7-vs-8 reconciliation. The only nuance is the R-126 (R03) vs R-127 (R07) symbol label at line 911 — both are real rules at that region (merge invariants vs A.8 pick-up), not a conflict. No contradiction.

---

## Q3 — Do R01/R04 agree the Stage-7 prompt is inline prose vs prompts.py? (R04 says inline prose, not prompts.py)

| Claim | R01 | R04 | Verdict |
|---|---|---|---|
| Stage-7 validation-agent prompt is **inline prose in SKILL.md** | Stage-7 instructions are the inline block-quote `SKILL.md:1265-1286` ("validation instructions block"); spawn payload `1254-1262` (R01:104,109,114) | "The Stage-7 validation-agent prompt is **inline prose in SKILL.md, NOT a prompts.py function**" — block-quote `SKILL.md:1265-1286` (R04:185-188) | **AGREE.** Both treat the Stage-7 agent prompt as inline SKILL.md prose at `1265-1286`. |
| `prompts.py` is OFF the Stage-7 path | "P1-P5 attach to the **skill protocol** … NOT these CLI modules"; `build_tasklist_fidelity_prompt`=CLI validate, `build_tasklist_generate_prompt`=skill generation, neither is Stage 7 (R01:203,209,214) | "`prompts.py` is NOT the site"; fidelity prompt = CLI `tasklist validate` (different pipeline, scope note `SKILL.md:132`); generate prompt = generation, "also not Stage 7" (R04:198-205,343) | **AGREE.** Both: the two `prompts.py` builders serve CLI-validate + skill-generate respectively; NEITHER carries Stage-7 fan-out logic. |
| Scope note that forks CLI-validate vs skill-generate | `SKILL.md:130-132` scope note (R01:203) | `SKILL.md:132` scope note (R04:201,346) | **AGREE.** Both cite the §3.x scope note at 130/132 as the fork point. (R07 independently confirms 130-132 = "Source Document Enrichment scope note", NOT an sc:task anchor — R07:35,161 — corroborating R01/R04's framing.) |

### Q3 VERDICT
**AGREE — R01 concurs with R04.** Both files independently conclude the Stage-7 validation-agent prompt is inline SKILL.md prose (`1265-1286`), and that `tasklist/prompts.py` is off the Stage-7 critical path (its two builders are CLI-validate and skill-generate, neither Stage 7). R07's scope-note confirmation (130-132) reinforces this. No contradiction.

---

## Q4 — Do all agree that NO typed StageError and NO sc:task-unified exist in current source?

### StageError

| File | Claim | Evidence |
|---|---|---|
| R03 | "no typed `StageError` exists in current source" | `grep -rn "StageError" src/superclaude/skills/task-builder/ src/superclaude/skills/sc-tasklist-protocol/` → **zero matches**; broader grep over `src/superclaude/` also nothing (R03:95-97) |
| R07 | "typed `StageError` … **ABSENT**" | "0 hits anywhere in `src/superclaude/`"; if spec/TDD assumes one it is `[UNVERIFIED]/non-existent` (R07:146) |
| R01 | (does not assert) | R01 is the static stage map; does not grep for StageError — silent, not contradictory |
| R04 | (does not assert) | R04 is data-flow; silent, not contradictory |

**AGREE (R03 + R07; R01/R04 silent).** Both files that investigated it independently confirm zero matches. R03 adds the implementation note that a typed StageError for zero-success would be a NEW decision (no prior art); R07 adds it should not be authored as an import/raise. Consistent — no contradiction.

### sc:task-unified

| File | Claim | Evidence |
|---|---|---|
| R03 | "`sc:task-unified` is NOT a current name … CONFIRMED" | `grep -rn "sc:task-unified\|sc-task-unified\|task-unified" src/superclaude/` → matches ONLY for `task-unified` as a `--caller` value in the troubleshoot↔task-protocol TFEP wire contract (troubleshoot.md:60/69; sc-task-protocol SKILL.md:217/241/270/271; etc.). No skill/command/skill-name `sc:task-unified` (R03:213-215) |
| R07 | "`sc:task-unified` … **ABSENT** … Fully retired. The unified-task surface is now `sc:task`" | "0 hits anywhere in `src/superclaude/`" (R07:142) |

**AGREE on the operative conclusion** (sc:task-unified is NOT a real invocation name; delegate to `sc:task`). 

**Sub-nuance worth surfacing (NOT a contradiction, but a phrasing divergence the builder should note):**
- R07 says the literal string `sc:task-unified` has **"0 hits anywhere in `src/superclaude/`"** (R07:142). This is scoped to the exact hyphenated token `sc:task-unified`.
- R03 says `grep` for the alternation `sc:task-unified\|sc-task-unified\|task-unified` returns matches — but ONLY for the bare substring `task-unified` as a `--caller` value (R03:215).
- These RECONCILE: the full token `sc:task-unified` = 0 hits (R07 correct); the bare substring `task-unified` does appear as a TFEP `--caller` identity (R03 correct). R07's "fully retired" + R03's "`task-unified` exists only as a `--caller` string" are the same finding stated at two granularities. **No contradiction**, but the builder must understand `task-unified` (the `--caller` string) is live while `sc:task-unified` (the invocation name) is not.

### Q4 VERDICT
**AGREE.** Both StageError and sc:task-unified are confirmed absent as typed-error/invocation-name by the two files that grepped (R03, R07); R01/R04 are silent (not contradictory). The only nuance is granularity: `task-unified` survives as a `--caller` wire string (R03), while the `sc:task-unified` token is 0-hit (R07) — complementary, not divergent.

---

## Q5 — Any conflicting claim about where P1/P5 attach (Stage 4 task-body vs index-level section)?

This is the one MATERIAL CONTRADICTION in the partition. P5 is clean; **P1 diverges between R01 and R04.**

### P5 — NO conflict
- R01: P5 advisory is "an **index-level section** (cross-phase, advisory). Cleanest home is the index file" after Feedback Collection Template `820-839` (R01:69).
- R04: P5 `## Tier Calibration Advisory` → "a … block in `tasklist-index.md`", after `839` before `841` (R04:132,137-139).
- **AGREE.** Both place P5 in the index file at the same anchor (after Feedback Collection Template, before Glossary). No conflict.

### P1 — CONTRADICTION (CRITICAL for the builder)

| | R01 | R04 |
|---|---|---|
| Target FILE | Phase file (`phase-N-tasklist.md`) | Index file (`tasklist-index.md`) |
| Target SURFACE | per-**task** body in Phase File Template | cross-phase **index** metadata block |
| Anchor | `SKILL.md:894-927` (insert near `**Steps:**` :904 / after `**Notes:**` :927); mirror `templates/phase-template.md:55-82` (R01:57-64,222) | after Artifact-Paths table `SKILL.md:707`, before `#### Phase Files Table` :709 (R04:80-87,370) |
| Granularity | **per-task** ("each task's `**Steps:**`… carries the task's resolved context") (R01:65) | **per-index / cross-phase** ("Execution Context is cross-phase metadata about where work lands") (R04:84-85) |
| Rationale cited | task-level context so F1 executor needs no re-derivation; Minimum Task Specificity Rule `1110-1128` (R01:65) | index-level because it is "cross-phase metadata", sibling to other index metadata tables (R04:84-85) |

**Root of the divergence:** R01 and R04 interpret "Context-Armed Steps" at two different altitudes:
- **R01** reads P1 literally as arming each **task's Steps block** with resolved context → necessarily a **per-task, phase-file** edit (`SKILL.md:894-927` + `phase-template.md:55-82`).
- **R04** reads P1 as a single cross-phase `## Execution Context` block that belongs in the **index** alongside metadata (`SKILL.md:707`).

**Corroborating third signal (R03, task-builder contract):** R03 §2 pins the REUSE surface to the task-builder `## Execution Context` block at `task-builder/SKILL.md:1066-1071`, which is described as "immediately after Prerequisites & Dependencies" — i.e. a **section in the MDTM task file body** (task-level/per-file), with per-item Context fields carrying file:line (TB-Add-7 ⇄ TB-Add-8) (R03:107-120). R07 confirms this contract is present and stable at `1066-1071`/`1231`/`1389` (R07:21-23).

**Analyst read of the conflict:** The task-builder precedent R03/R07 anchor (`## Execution Context` as a **task-file body section**, with a header that carries NO file:line and per-item Context fields that DO) is structurally closer to **R01's phase-file/task-body placement** than to R04's index-level block. R04's "index metadata block after :707" does not have an obvious home for the per-item Context evidence binding that TB-Add-8 requires. HOWEVER — sc:tasklist's index has no per-item surface at all, and a single cross-phase Execution Context block (R04) is a legitimate ADAPTATION of the task-builder section to sc:tasklist's index-centric output. **Neither is provably wrong from the source alone; they are genuinely different design choices for the SAME proposal, and they cannot both ship.** This MUST be resolved by the builder (or escalated as a design decision) before P1 is authored — shipping both anchors would emit the block in two different files.

### Q5 VERDICT
- **P5: NO conflict** (both index-level, same anchor 839/841).
- **P1: CONTRADICTION (material, unresolved).** R01 = phase-file per-task body (`SKILL.md:894-927`, mirror `phase-template.md:55-82`). R04 = index-level block (after `SKILL.md:707`). The task-builder reuse contract (R03/R07, `1066-1071` = task-file body section) leans toward R01's altitude but does not settle the sc:tasklist adaptation. Builder MUST pick one before authoring P1.

---

## Q-extra — The 17-vs-20 stray at `SKILL.md:1597` (build brief called this out explicitly)

Cross-check of the stale check-count inconsistency across all files that touch it.

| File | Claim | Anchors |
|---|---|---|
| R01 | "CONFIRMED — real stale-count inconsistency." Gate says **1-20** at `SKILL.md:1187`; Stage-6 completion message says **17** at `SKILL.md:1597`. "17" is stale; fix to 20 as P4-adjacent cleanup (R01:188-197) | `1187` (1-20, correct) vs `1597` (17, stale) |
| R04 | "Count-mismatch flag … `SKILL.md:1597` says 'all 17 checks passed' but the gate is checks 1-20 (1136-1187). P4's gate-results.txt must serialize 20, so this stale '17' should be corrected as part of P4" (R04:166-168,357-359) | same: `1597` (17) vs `1136-1187` gate (20) |
| R07 | "**CONFIRMED STALE at 1597** … contradicts the gate's own 'check 1-20' at 1187. Confirmed by grep: only two count tokens exist — `1187: check 1-20` and `1597: all 17 checks`." Tagged **[CODE-CONTRADICTED]**. Fix 17→20 (R07:31,165) | `1597` (17) vs `1187` (1-20) |

**AGREE (3-way, unanimous).** R01, R04, R07 all independently confirm: the authoritative gate is **20 checks** (`SKILL.md:1187`, "check 1-20"), and `SKILL.md:1597` ("all 17 checks passed") is **stale/wrong**. R07 adds the grep-proof that exactly two count tokens exist in the region (1187=20, 1597=17), so there is no third conflicting count hiding. All three recommend fixing 17→20 as a bounded P4-adjacent hygiene item. **No divergence** — this is a clean, triply-corroborated finding, not a contradiction between researchers (the contradiction is internal to the SKILL.md source, which all three correctly surface).

---

## Cross-File Consistency Summary

| Cross-check | Files | Result |
|---|---|---|
| Q1 P1 anchor | R01 vs R04 | **CONTRADICTION** (phase-body vs index) |
| Q1 P2/P3/P4/P5 anchors | R01/R04/R07 | AGREE |
| Q2 DM-003 location + field set | R03 vs R07 | AGREE (R-126/R-127 label nuance at 911, not a conflict) |
| Q3 Stage-7 prompt = inline prose | R01 vs R04 (R07 corroborates scope note) | AGREE |
| Q4 StageError absent | R03 + R07 (R01/R04 silent) | AGREE |
| Q4 sc:task-unified absent | R03 + R07 | AGREE (granularity nuance: `task-unified` `--caller` live) |
| Q5 P5 attach point | R01 vs R04 | AGREE (index-level) |
| Q5 P1 attach point | R01 vs R04 | **CONTRADICTION** (same as Q1 P1) |
| Q-extra 17-vs-20 at :1597 | R01/R04/R07 | AGREE (unanimous; internal source bug, not researcher conflict) |

### Contradictions found (count: 1 material)
1. **[MATERIAL] P1 `## Execution Context` attachment surface — R01 vs R04.**
   - R01 (`01-skill-stage-map.md:57-64`): phase-file per-task body, `SKILL.md:894-927`, mirror `templates/phase-template.md:55-82`.
   - R04 (`04-proposal-attachment-trace.md:80-87`): index-level block, after `SKILL.md:707`, before `#### Phase Files Table` (709).
   - Same proposal, two different files + two different line regions. Both cannot ship. Task-builder reuse contract (R03 §2 / R07 §1a, `task-builder/SKILL.md:1066-1071` = task-file body section) is structurally closer to R01's task-body altitude, but the sc:tasklist index-centric adaptation (R04) is not provably wrong. **Requires builder decision before P1 is authored.** Recommend the builder reconcile by checking whether sc:tasklist's output even has a per-task body surface to host the Context-Armed Steps (it does — Phase File Template `SKILL.md:894-927`), which favors R01; if a single cross-phase summary block is intended instead, R04's index anchor applies. Do NOT author P1 against both anchors.

### Non-divergence nuances surfaced (NOT contradictions, builder should note)
- Q2: R-126 (R03) vs R-127 (R07) symbol label at `task-builder/SKILL.md:911` — distinct rules at the same region, complementary.
- Q4: `task-unified` survives as a TFEP `--caller` string (R03) while `sc:task-unified` token = 0 hits (R07) — same finding at two granularities.
- Field count 7-vs-8: 7 named YAML fields; "8" counts the dedup_key 2-tuple's elements separately (R03 reconciles; R07 corroborates).

---

## VERDICT: FAIL

**1 material contradiction found** between assigned partition files:

- **P1 attachment-point contradiction (R01 vs R04):** R01 anchors P1's `## Execution Context` to the phase-file per-task body (`SKILL.md:894-927`); R04 anchors it to the index file (after `SKILL.md:707`). This is a genuine divergence on WHERE the same proposal attaches, not a line-number drift. It MUST be resolved before P1 is authored, or the build will emit the block in the wrong file (or both).

All other cross-checks PASS / AGREE:
- DM-003 contract location + 7-field set (R03 ⇔ R07): consistent.
- Stage-7 prompt = inline SKILL.md prose, prompts.py off-path (R01 ⇔ R04, R07 corroborates): consistent.
- StageError + sc:task-unified absent (R03 ⇔ R07): consistent.
- P5 index-level attach (R01 ⇔ R04): consistent.
- 17-vs-20 stale count at `:1597` (R01/R04/R07): unanimously confirmed as an internal SKILL.md bug to fix (17→20), not a researcher disagreement.

[PARTITION NOTE: This FAIL reflects the assigned subset (R01/R03/R04/R07) only. Other partitions may surface additional contradictions; the orchestrator should merge before the final gate verdict. The single P1 contradiction is the actionable blocker from this partition.]

**Status:** Complete
