# O2 — sc-tasklist-protocol POST Gate Edit Surface

Status: Complete

Topic: Replace per-phase terminal `/sc:reflect --mode post` SPAWN DIRECTIVE with a FLAT Bash shell-out
`superclaude reflect run <ABS_PHASE_FILE> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>`,
wrapped in `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard. PRE gate (Stage 10.5 `--mode pre`) stays INTACT.
`--no-reflect` gating toggle KEPT.

Files in scope (branch reflect/wrapper-gate-wiring):
- src/superclaude/skills/sc-tasklist-protocol/SKILL.md (1617 lines)
- src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md (174 lines)

Authoritative shapes from contract (`reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md`):
- O2 invocation (§2): `superclaude reflect run <ABS_PHASE_FILE_PATH> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>`
- `--base <sha>` is a SINGLE ref (NOT `base..HEAD` range). `--no-promote` REQUIRED (no per-phase adapter, §5).
- Skip guard (§3.2): `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then echo "..."; exit 0; fi`
- Forbidden: `--reflect …` dial, `--max-turns`, `base..HEAD` range. `--depth` accepts only `standard|deep`.
- Frontmatter (§6): per-phase `start_commit` (git SHA) + `executor_model_class` (model alias e.g. `sonnet`).
  Canonical path = explicit `--base <sha>` on the gate line. `reflect_post:` written BACK by wrapper — leave room.

---

## SURFACE 1 — SKILL.md "Post-Execution Reflection Task (Terminal …)" section (THE primary O2 block)

**Location:** SKILL.md lines 1036–1083 (intro prose 1036–1038; fenced template block 1040–1083).

### 1a. Intro prose — lines 1036–1038 (VERBATIM)

```markdown
#### Post-Execution Reflection Task (Terminal — when reflect gating is enabled)

When reflect gating is enabled (default; disabled by `--no-reflect`), append exactly ONE fixed terminal task to each phase file, AFTER the End-of-Phase Checkpoint above. This is the sole task permitted to follow the end-of-phase checkpoint (per the amended checkpoint-is-last invariant set — Self-Check #6 and structural checks #18/#19/#20). It uses the standard Sprint-CLI task shape (metadata table + body sections), is Tier EXEMPT (reflect is the auditor, not itself tier-verified, so it is exempt from the artifact-referencing Acceptance-Criteria minimum), and carries a `**Reflect Report Path:**` (not a Checkpoint Report Path). `<phase-commit-range>` is a placeholder the Sprint executor resolves at execution time — never a fabricated SHA. The spawn directive uses `/sc:reflect` (never the `sc:task` execution command).
```

**What changes for O2:** Rewrite the last two sentences. The `<phase-commit-range>` placeholder is REPLACED by an explicit `--base <PHASE_N_START_SHA>` resolved from the per-phase start SHA the generator persists (no longer "Sprint executor resolves a git RANGE at execution time" — the contract uses a SINGLE base ref vs working tree). "The spawn directive uses `/sc:reflect`" becomes "the gate is a FLAT Bash shell-out `superclaude reflect run … --no-promote --base <sha>`, wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard." Keep the "Tier EXEMPT" / "Reflect Report Path (not Checkpoint)" / "sole task after checkpoint" framing.

### 1b. Fenced task template — lines 1040–1083 (VERBATIM)

```markdown
### T<PP>.<final> -- Post-Execution Reflection: sc:reflect --mode post

| Field | Value |
|---|---|
| Roadmap Item IDs | <all R-### in this phase, comma-separated> |
| Why | Independent post-execution deviation audit of every task in Phase <PP>, in a fresh session, after all phase work completes. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT  (* reflect is the auditor; it is not itself tier-verified *) |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification (reflect IS the verification) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | Required (fresh-session reflect ensemble) |
| Deliverable IDs | D-RF<PP> |

**Reflect Report Path:** `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md`

**Spawn Directive (fresh session):** Spawn a NEW agent/session and run:
`/sc:reflect --mode post --remediate --tasklist TASKLIST_ROOT/phase-<PP>-tasklist.md --diff <phase-commit-range> --depth <DETERMINISTIC_DEPTH_for_phase_PP> --tier <DETERMINISTIC_TIER_for_phase_PP> --executor-model <EXECUTOR_CLASS> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`
(The reflect agent uses the default subagent model; `--executor-model` is the reflect-native exclusion flag naming the class that ran the phase's work, so reflect removes it from the reviewer pool — it does not select a model. Never the `sc:task` execution command.)

**Steps:**
1. **[VERIFICATION]** Resolve `<phase-commit-range>` = the git range covering all of Phase <PP>'s task commits.
2. **[VERIFICATION]** Spawn a fresh session and invoke the Spawn Directive above (reflect audits the committed diff — cross-session-safe).
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface its deviation counts (authorized/necessary/drift/regression).

**Acceptance Criteria:** (exactly 4 bullets)
- File `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` exists with a deviation-taxonomy summary.
- Zero `regression`-class deviations, OR a `--remediate` Tier-3 task was authored for each.
- Reflect ran with executor-disjoint reviewers (the `<EXECUTOR_CLASS>` passed via `--executor-model` was excluded from the reviewer pool).
- Report includes the per-task verdict matrix for Phase <PP>.

**Validation:**
- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** all regular + checkpoint tasks in Phase <PP>.
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately).
```

**What changes for O2 (line-by-line):**
- **L1041 heading** `### T<PP>.<final> -- Post-Execution Reflection: sc:reflect --mode post` → drop the `sc:reflect --mode post` suffix (gate is now a `superclaude reflect run` shell-out). Recommend keeping the `-- Post-Execution Reflection` prefix so structural check #18 needs no edit.
- **L1062–1064 Spawn Directive** — THE core replacement. The `/sc:reflect --mode post --remediate … --diff <phase-commit-range> --depth <DET_DEPTH> --tier <DET_TIER> --executor-model <CLASS> --output …` line is REPLACED by the flat shell-out wrapped in the skip guard:
  ```bash
  if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then
    echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0
  fi
  superclaude reflect run <ABS_PHASE_FILE> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>
  ```
  Contract fixes `--depth deep` (no `<DETERMINISTIC_DEPTH>`), DROPS `--tier`, and drops `--remediate`/`--tasklist`/`--diff`/`--output`/`--executor-model` from the gate line (executor-model now flows via frontmatter `executor_model_class`, not a hand-written CLI flag). The L1064 parenthetical about `--executor-model` being a CLI flag becomes obsolete for the gate line.
- **L1066–1068 Steps** — Step 1 "Resolve `<phase-commit-range>` = the git RANGE covering all of Phase <PP>'s task commits" is now wrong: contract uses a SINGLE `--base <sha>` (phase START sha) vs the working tree, NOT a range. Rewrite to "the gate passes `--base <PHASE_N_START_SHA>` (persisted at phase-build time); the wrapper diffs that base ref against the working tree." Step 2 "Spawn a fresh session and invoke the Spawn Directive" → "the gate runs `superclaude reflect run …` (the wrapper spawns the reflect ensemble internally)."
- **L1073 Acceptance Criteria** — "OR a `--remediate` Tier-3 task was authored" — `--remediate` is gone; the wrapper's `--fix` auto-fix loop is the new mechanism. Reword to the wrapper exit-code contract (exit 0 = clean OR auto-fixed-and-verified; exit 10/11/2 = gate FAILS).
- **L1074 Acceptance Criteria** — "the `<EXECUTOR_CLASS>` passed via `--executor-model`" → now sourced from frontmatter `executor_model_class`; reword.

---

## SURFACE 2 — phase-template.md mirror block (kept in sync with Surface 1)

**Location:** phase-template.md lines 117–174 (end-of-phase checkpoint 117–125; POST section 127–174).
This file is a "Read-only reference extracted from SKILL.md … This file exists for human review; the skill uses its own inline copy" (template L3). It MUST be edited in lock-step with Surface 1.

### 2a. POST section intro — lines 127–129 (VERBATIM)

```markdown
## Terminal Post-Execution Reflection Task (when reflect gating is enabled)

> Mirror of the SKILL.md Section 6B inline copy — kept in sync for human review. When reflect gating is enabled, the generator appends exactly ONE fixed terminal task per phase file, AFTER the end-of-phase checkpoint. It uses the standard Sprint-CLI task shape, is Tier EXEMPT (reflect is the auditor, so it is **exempt from the artifact-referencing Acceptance-Criteria minimum**), carries a `**Reflect Report Path:**` (not a Checkpoint Report Path), and its `<phase-commit-range>` is resolved by the Sprint executor at run time (never a fabricated SHA). The spawn directive uses `/sc:reflect` (never the `sc:task` execution command).
```

### 2b. Fenced template — lines 131–174 (VERBATIM)

```markdown
### T<PP>.<final> -- Post-Execution Reflection: sc:reflect --mode post

| Field | Value |
|---|---|
| Roadmap Item IDs | <all R-### in this phase, comma-separated> |
| Why | Independent post-execution deviation audit of every task in Phase <PP>, in a fresh session, after all phase work completes. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT  (* reflect is the auditor; it is not itself tier-verified *) |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification (reflect IS the verification) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | Required (fresh-session reflect ensemble) |
| Deliverable IDs | D-RF<PP> |

**Reflect Report Path:** `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md`

**Spawn Directive (fresh session):** Spawn a NEW agent/session and run:
`/sc:reflect --mode post --remediate --tasklist TASKLIST_ROOT/phase-<PP>-tasklist.md --diff <phase-commit-range> --depth <DETERMINISTIC_DEPTH_for_phase_PP> --tier <DETERMINISTIC_TIER_for_phase_PP> --executor-model <EXECUTOR_CLASS> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`
(The reflect agent uses the default subagent model; `--executor-model` is the reflect-native exclusion flag naming the class that ran the phase's work — it does not select a model. Never the `sc:task` execution command.)

**Steps:**
1. **[VERIFICATION]** Resolve `<phase-commit-range>` = the git range covering all of Phase <PP>'s task commits.
2. **[VERIFICATION]** Spawn a fresh session and invoke the Spawn Directive above (reflect audits the committed diff — cross-session-safe).
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface its deviation counts (authorized/necessary/drift/regression).

**Acceptance Criteria:** (exactly 4 bullets)
- File `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` exists with a deviation-taxonomy summary.
- Zero `regression`-class deviations, OR a `--remediate` Tier-3 task was authored for each.
- Reflect ran with executor-disjoint reviewers (the `<EXECUTOR_CLASS>` passed via `--executor-model` was excluded from the reviewer pool).
- Report includes the per-task verdict matrix for Phase <PP>.

**Validation:**
- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** all regular + checkpoint tasks in Phase <PP>.
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately).
```

**What changes for O2:** IDENTICAL transformation to Surface 1 (mirror). L132 heading, L153–155 Spawn Directive → flat shell-out + skip guard, L158–159 Steps (range→`--base <sha>`), L164/L165 Acceptance Criteria (`--remediate`→`--fix`; `--executor-model` flag→frontmatter). Also update the L129 mirror-note prose (`<phase-commit-range>` resolved by Sprint executor / "spawn directive uses `/sc:reflect`") to match.

---

## SURFACE 3 — Checkpoint-is-last invariant + "sole task permitted to follow checkpoint"

These lines assert the ORDERING contract (post-reflection is the absolute last task after the end-of-phase checkpoint). They reference the post-reflection task but DO NOT name `sc:reflect`/`--mode post`, so they survive UNCHANGED. The task remains a task body in the phase file, so the "task" framing stays accurate.

### SKILL.md L1018–1034 — End-of-Phase Checkpoint section (VERBATIM, ordering lines)

```markdown
#### End-of-Phase Checkpoint (Mandatory, Last Task)

Every phase file MUST end with an end-of-phase checkpoint, emitted as the
last numbered **checkpoint** in the phase:

### T<PP>.<last_num> -- Checkpoint: End of Phase <PP>

`<last_num>` must be strictly greater than every regular task number in the
phase. No regular task may appear below it; when reflect gating is enabled (default), the templated post-reflection task is the sole task permitted to follow it and is the absolute last task. All other checkpoint-task fields
(metadata table, Checkpoint Report Path, Purpose, Verification, Exit
Criteria, Steps, Acceptance Criteria, Validation, Dependencies, Rollback)
are required exactly as in the inline-checkpoint template above; the
checkpoint report path is fixed at
`TASKLIST_ROOT/checkpoints/CP-P<PP>-END.md` and the Deliverable ID is
`D-CP<PP>`.
```
**Change:** None required (no `sc:reflect`/`--mode post` token). "templated post-reflection task is the sole task permitted to follow it and is the absolute last task" stays true. KEEP.

### phase-template.md L117–125 — End-of-Phase Checkpoint (VERBATIM)

```markdown
## End-of-Phase Checkpoint (Mandatory)

Every phase file MUST end with an end-of-phase checkpoint as its last *checkpoint*:

### Checkpoint: End of Phase <N>

This checkpoint serves as the gate for the next phase and must include all standard checkpoint fields. When reflect gating is enabled (the default; disabled by `--no-reflect`), the templated post-execution reflection task below is the **sole** task permitted to follow this checkpoint and is the absolute last task in the file.
```
**Change:** None required. KEEP.

---

## SURFACE 4 — Structural checks #18/#19/#20, Self-Check #6 (+ every `sc:reflect`/`--mode post` assertion)

### 4a. Self-Check #6 — IS structural check #6 (line 1129). There is NO separate numbered "Self-Check #6".

The intro prose at L1038 says "per the amended checkpoint-is-last invariant set — **Self-Check #6** and structural checks #18/#19/#20". "Self-Check #6" = item 6 of the "Sprint Compatibility Self-Check (Pre-Write, Mandatory)" list (heading at L1118). That item 6 is at **L1129** (VERBATIM):

```markdown
6. Every phase file ends with an end-of-phase checkpoint task — the last *checkpoint* in the phase (per checks 18-20); when reflect gating is enabled (default), the templated post-reflection task is the sole task permitted to follow that checkpoint and is the absolute last task in the file
```
**Change:** None required (no `sc:reflect`/`--mode post`/spawn-directive token). KEEP. (The "Self-Check #6" cross-reference at L1038 also stays valid.)

### 4b. Structural checks #18 / #19 / #20 — L1169 / L1170 / L1171 (VERBATIM)

```markdown
| 18 | Checkpoint task emission: every checkpoint block in each phase is emitted as a `### T<PP>.<NN> -- Checkpoint:` task heading (never as a sibling `### Checkpoint:` heading); when reflect gating is enabled, the post-reflection task is likewise emitted as its own `### T<PP>.<NN> -- Post-Execution Reflection:` task heading (scanner-visible, not a checkpoint) | Cause-2 fix (v3.7 Wave 4): keeps checkpoints visible to the sprint task scanner |
| 19 | End-of-phase position: the `### T<PP>.<NN> -- Checkpoint: End of Phase <PP>` task is the last *checkpoint* in its phase, with no **regular** task following it; when reflect gating is enabled, the templated post-reflection task is the sole task permitted to follow it and holds the highest `<NN>` in the phase | Ensures the end-of-phase gate is the last instruction before the (optional) post-execution reflection |
| 20 | Checkpoint Report Path presence: every checkpoint task includes a `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<name>.md` line immediately below its metadata table (the post-reflection task is NOT a checkpoint task and instead carries a `**Reflect Report Path:**` line — it is exempt from this check) | Lets Wave 2/3 tooling (`_verify_checkpoints`, `build_manifest`) parse the expected file path |
```

**FLAG — check #18 asserts the heading shape `### T<PP>.<NN> -- Post-Execution Reflection:`.** If the O2 rewrite changes the task HEADING (Surface 1 L1041 / 2b L132 currently `… -- Post-Execution Reflection: sc:reflect --mode post`), check #18's asserted heading PREFIX `### T<PP>.<NN> -- Post-Execution Reflection:` must stay CONSISTENT. Recommendation: keep the heading prefix `-- Post-Execution Reflection` (drop only the `: sc:reflect --mode post` suffix) so check #18 needs no edit. If the rewrite alters the prefix, #18 MUST be updated.
- **#19, #20:** structurally about position / Reflect-Report-Path — no `sc:reflect` token; KEEP. The `**Reflect Report Path:**` line referenced in #20 is RETAINED in the new block, so #20 stays valid.

### 4c. Other lines literally asserting `sc:reflect` / `--mode post` / `/sc:reflect`

- **L1041** (Surface 1 heading) and **L132** (Surface 2b heading): `… Post-Execution Reflection: sc:reflect --mode post` — CHANGE (see Surface 1/2).
- **L1063, L154** (spawn directive lines): `/sc:reflect --mode post --remediate …` — CHANGE to shell-out (see Surface 1/2). These are the ONLY lines emitting the old POST invocation.
- **L1038, L129** (intro prose): "The spawn directive uses `/sc:reflect`" — CHANGE.
- **No standalone numbered structural/self-check literally string-matches `sc:reflect`/`--mode post`** beyond #18's heading-prefix assertion (4b). The structural/self-check layer is mostly ordering/heading-shape, not invocation-text — so the gate-shape rewrite is low-risk to the check battery PROVIDED the heading prefix is preserved.

---

## SURFACE 5 — `argument-hint` + `--no-reflect` handling (confirm KEEP)

### `argument-hint` — SKILL.md L9 (VERBATIM)

```yaml
argument-hint: "<roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]"
```
**Confirmed:** `--no-reflect` here is the GATING ON/OFF TOGGLE (it gates BOTH the Stage 10.5 PRE fan-out and the terminal POST task emission). It is NOT the abandoned `--reflect <none|0|1|2|auto>` dial (that dial took a value; this is a bare boolean disable). **KEEP unchanged.** There is NO `--reflect` value-dial anywhere in either file (grep confirmed: every `--reflect`-prefixed token is `--no-reflect`, `reflect-pre`, `reflect-post`, `reflect_pre`, or `/sc:reflect`).

### `--no-reflect` handling sites (all KEEP — toggle semantics):
- **L96** — index/bundle description: "(when reflect gating is enabled — the default) a terminal post-execution reflection task as the absolute last task". KEEP (still true; the task body changes, not its presence).
- **L725** — "Pre-Reflect Sign-off … Shown as `SKIPPED` (or omitted) when `--no-reflect` is set." KEEP (PRE gate, intact).
- **L1028, L1038, L1129** — "disabled by `--no-reflect`" gating prose. KEEP.
- **L1465** (Stage 10.5) — "**Skip when disabled.** If `--no-reflect` is set (or `--dry-run`), skip this stage entirely (under `--dry-run`, print "would run N pre-reflects + template N post-reflect tasks" …)." KEEP — the `--dry-run` message "template N post-reflect tasks" stays accurate (POST task still templated, different body).
- **phase-template L125, L127, L129** — "disabled by `--no-reflect`" gating prose. KEEP.

**Conclusion:** `--no-reflect` is the gating toggle and is KEPT exactly. No `--reflect` dial exists to remove.

---

## SURFACE 6 — Per-phase frontmatter / metadata: where `executor_model_class` + per-phase start SHA live

**KEY STRUCTURAL FINDING:** Phase files have NO YAML frontmatter today. A phase file STARTS with a level-1 heading `# Phase N -- <Phase Name>` (SKILL.md L859–863; template L11–17; structural check #5 at L1128 asserts "Every phase file starts with `# Phase N -- <Name>` (level 1 heading…)"). The phase file is "a self-contained execution unit … It does NOT contain registries, traceability matrices, templates, or completion protocol instructions" (L855 / template L7). So **there is no existing frontmatter slot** for `start_commit` / `executor_model_class`.

**Implication for O2:** The generator must ADD a place to persist per-phase `start_commit` and `executor_model_class`. Two contract-compatible options:
1. **Add a YAML frontmatter block** at the top of each phase file (before the `# Phase N` heading) — but this COLLIDES with structural check #5 ("starts with `# Phase N`") and Sprint CLI TUI display-name extraction (L863) unless check #5 is amended to allow leading frontmatter. FLAG: check #5 (L1128) would need updating if frontmatter is prepended.
2. **Inject the value directly onto the gate line** — the contract's canonical path: explicit `--base <PHASE_N_START_SHA>` on the `superclaude reflect run` line (precedence `--base` > frontmatter `start_commit` > `git merge-base HEAD master`, contract §6). This sidesteps frontmatter entirely for the base SHA. `executor_model_class`, however, the wrapper reads from frontmatter (contract §6 row 3) — so SOME per-phase metadata persistence is still needed for `executor_model_class`, OR it must be surfaced another way.

### How `<phase-commit-range>` / `<phase-N-start-sha>` is resolved TODAY (placeholder semantics)

Today there is NO per-phase start-SHA persistence at all. The current model is a RANGE placeholder the Sprint executor fills at run time:
- **L1038 / template L129:** "`<phase-commit-range>` is a placeholder the Sprint executor resolves at execution time — never a fabricated SHA."
- **L1067 / template L158 (Step 1):** "Resolve `<phase-commit-range>` = the git range covering all of Phase <PP>'s task commits."
- **L1063 / template L154 (spawn directive):** passed as `--diff <phase-commit-range>`.

So the generator NEVER writes a SHA today; it emits a `<phase-commit-range>` placeholder and the Sprint executor computes the range. **O2 must change this**: persist the per-phase START sha (single ref, not a range) at build/emit time and pass it as `--base <PHASE_N_START_SHA>`. The "git range" framing (Step 1, L1067/L158) is obsolete — contract uses a single base ref vs working tree. The exact token `<phase-N-start-sha>` does NOT exist in either file today (today's placeholder is the RANGE token `<phase-commit-range>`).

**Quote — the only `<EXECUTOR_CLASS>` plumbing today:** L1063/L154 pass `--executor-model <EXECUTOR_CLASS>` as a CLI flag on the spawn directive; L1064/L155 explain it as "the reflect-native exclusion flag naming the class that ran the phase's work." Contract §6 moves this to frontmatter `executor_model_class`. FLAG: there is currently NO field/frontmatter persisting `executor_model_class` per phase — it is only a `<EXECUTOR_CLASS>` placeholder on the directive line. The generator must add persistence (or redefine the wrapper resolution).

---

## SURFACE 7 — Full grep sweep (every line + 1-line context)

### SKILL.md

| Line | Token | Context | O2 disposition |
|------|-------|---------|----------------|
| 9 | `--no-reflect` | argument-hint | KEEP (gating toggle) |
| 87 | `reflect-pre`/`reflect-post` | validation dir paths incl `reflect-post/` + `depth-map.yaml` | KEEP (POST output dir still used) |
| 96 | reflect | "terminal post-execution reflection task as the absolute last task" | KEEP (presence true) |
| 121,123 | `reflect-pre`/`reflect-post` | dir tree listing | KEEP |
| 283,291 | reflect(s) | "reflects stakeholder_priorities" — unrelated English | NO CHANGE |
| 350-363 | checkpoint | checkpoint cadence rules | KEEP |
| 725 | `--no-reflect` | "Shown as SKIPPED … when --no-reflect is set" | KEEP |
| 1020-1034 | checkpoint | End-of-Phase Checkpoint section (Surface 3) | KEEP |
| 1028 | `--no-reflect` | "disabled by --no-reflect … sole task permitted to follow" | KEEP |
| 1036 | reflect | `#### Post-Execution Reflection Task` heading | CHANGE (Surface 1a) |
| 1038 | `--no-reflect`,`/sc:reflect`,Self-Check #6 | intro prose | CHANGE (Surface 1a) |
| 1041 | `sc:reflect --mode post` | task heading | CHANGE (Surface 1b) |
| 1060 | reflect | Reflect Report Path | KEEP (path retained) |
| 1063 | `/sc:reflect --mode post --remediate … --diff … --depth … --tier … --executor-model …` | **spawn directive** | **CHANGE → shell-out** |
| 1064 | reflect,`--executor-model` | directive explainer | CHANGE (Surface 1b) |
| 1067 | reflect/`<phase-commit-range>` | Step 1 "git range" | CHANGE (range→--base sha) |
| 1068 | reflect | Step 2 "Spawn fresh session … committed diff" | CHANGE |
| 1072-1075 | reflect,`--remediate`,`--executor-model` | Acceptance Criteria | CHANGE (Surface 1b) |
| 1129 | `--no-reflect` | Self-Check #6 (=struct #6) | KEEP (Surface 4a) |
| 1169 | `Post-Execution Reflection:` | struct check #18 heading-shape | KEEP* (FLAG — heading-prefix must match; Surface 4b) |
| 1170 | reflect | struct check #19 position | KEEP (Surface 4b) |
| 1171 | reflect/Reflect Report Path | struct check #20 | KEEP (Surface 4b) |
| 1257,1260,1290 | reflect(ed) | drift rubric / "reflected in" English | NO CHANGE |
| 1448 | `/sc:reflect --mode pre --remediate` | **Stage 10.5 PRE fan-out** | **KEEP INTACT** (PRE gate stays) |
| 1452 | reflect/`--depth`/`--tier` | PRE depth/tier resolve | KEEP (PRE) |
| 1455-1460 | `/sc:reflect --mode pre --remediate … --depth … --tier …` | PRE invocation block | KEEP (PRE) |
| 1463 | reflect/`reflect_pre` | PRE verdict handling | KEEP (PRE) |
| 1465 | `--no-reflect`,reflect,"template N post-reflect tasks" | Stage 10.5 skip prose | KEEP (toggle) |
| 1467 | reflect | PRE stage gate | KEEP |
| 1471-1507 | reflect/`--depth`/`--tier`/`DETERMINISTIC` | **Per-Phase Reflect Depth (COMPLEXITY_SCORE → depth/tier)** | KEEP for PRE; see FLAG below |
| 1478 | "post-reflect task" | n_tasks excludes post-reflect | KEEP |
| 1522-1605 | Self-Check / Pre-Reflect | stage-reporting contract (1522,1527,1555,1560,1583,1588,1605) | KEEP (PRE) |

### phase-template.md

| Line | Token | Context | O2 disposition |
|------|-------|---------|----------------|
| 108,114,119 | checkpoint | checkpoint path/name rules | KEEP |
| 125 | `--no-reflect` | end-of-phase checkpoint ordering | KEEP (Surface 3) |
| 127 | reflect | POST section heading | CHANGE (Surface 2a) |
| 129 | `--no-reflect`,`/sc:reflect`,`<phase-commit-range>` | mirror-note prose | CHANGE (Surface 2a) |
| 132 | `sc:reflect --mode post` | task heading | CHANGE (Surface 2b) |
| 141,145,148,151 | reflect | EXEMPT row / Reflect Report Path | KEEP (retained) |
| 154 | `/sc:reflect --mode post --remediate … --diff … --depth … --tier … --executor-model …` | **spawn directive** | **CHANGE → shell-out** |
| 155 | reflect/`--executor-model` | directive explainer | CHANGE (Surface 2b) |
| 158 | `<phase-commit-range>` | Step 1 "git range" | CHANGE |
| 159 | reflect | Step 2 | CHANGE |
| 163-166 | reflect/`--remediate`/`--executor-model` | Acceptance Criteria | CHANGE (Surface 2b) |
| 170,172,173 | reflect | Validation/Dependencies/Rollback | KEEP |

### FLAG — `--tier` / `DETERMINISTIC_DEPTH` / `DETERMINISTIC_TIER` plumbing the flat O2 shell-out makes OBSOLETE *for the POST gate only*

The contract's O2 line is FIXED `--depth deep` with NO `--tier`. So for the POST gate, these placeholders are obsolete:
- **L1063 / template L154** `--depth <DETERMINISTIC_DEPTH_for_phase_PP> --tier <DETERMINISTIC_TIER_for_phase_PP>` → becomes literal `--depth deep`, `--tier` dropped.

BUT the COMPLEXITY_SCORE → depth/tier machinery (L1471–1507) and the Stage 10.5 PRE invocation (L1455–1460) STILL use `<DETERMINISTIC_DEPTH_for_phase_P>` / `<DETERMINISTIC_TIER_for_phase_P>` for the **PRE** gate. **The PRE gate is explicitly OUT OF SCOPE (stays intact).** Therefore:
- DO NOT delete the COMPLEXITY_SCORE section (L1471–1507) — PRE still needs it.
- The depth/tier determinism becomes POST-irrelevant: the POST gate no longer reads COMPLEXITY_SCORE. Optional one-line clarifying note: "COMPLEXITY_SCORE drives the PRE gate's `--depth`/`--tier` only; the POST gate is fixed `--depth deep`." Not required for correctness.
- `--tier` exists ONLY on the PRE line (L1459) and the obsolete POST directive (L1063/L154). After O2, `--tier` survives only on PRE. The flat POST shell-out removes the only POST `--tier`/`<DETERMINISTIC_*>` usage.

### Tokens with ZERO hits (confirmed absent)
`superclaude reflect run` (0 — to be ADDED by O2), `start_commit` (0 — to be ADDED per contract §6), `executor_model_class` (0 — only `<EXECUTOR_CLASS>` placeholder via `--executor-model` exists today), bare `--reflect` value-dial (0 — abandoned dial never present), `--base` (0 — to be ADDED), `<phase-N-start-sha>` exact token (0 — today's placeholder is `<phase-commit-range>`, a RANGE), `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` (0 — to be ADDED), `--no-promote` (0 — to be ADDED).

---

## Summary of edit surface (O2)

| # | File:lines | Block | Action |
|---|-----------|-------|--------|
| 1 | SKILL.md 1036–1038 | POST intro prose | CHANGE: range→`--base sha`, `/sc:reflect`→shell-out, mention skip guard |
| 2 | SKILL.md 1041 | POST task heading | CHANGE: drop `: sc:reflect --mode post` suffix (keep `-- Post-Execution Reflection` prefix for check #18) |
| 3 | SKILL.md 1062–1064 | **Spawn Directive** | **CHANGE → flat `superclaude reflect run <abs> --depth deep --fix --no-promote --base <sha>` + skip guard** |
| 4 | SKILL.md 1066–1075 | Steps + Acceptance Criteria | CHANGE: range→base ref; `--remediate`→`--fix`/exit-codes; `--executor-model` flag→frontmatter |
| 5 | phase-template.md 127–174 | mirror block | CHANGE: identical to #1–4 (kept in sync) |
| 6 | SKILL.md 1018–1034, 1129; template 117–125 | checkpoint-is-last invariant + Self-Check #6 | KEEP (no invocation token) |
| 7 | SKILL.md 1169–1171 | struct checks #18/#19/#20 | KEEP — FLAG #18 heading-prefix must match new heading |
| 8 | SKILL.md 9 | argument-hint `--no-reflect` | KEEP (gating toggle, not the dial) |
| 9 | SKILL.md 1128 (check #5 "starts with `# Phase N`") | structural check | FLAG: if frontmatter is prepended for `executor_model_class`/`start_commit`, check #5 must be amended |
| 10 | SKILL.md 1471–1507 (COMPLEXITY_SCORE), 1455–1460 (PRE invocation) | PRE depth/tier | KEEP INTACT (PRE out of scope); POST no longer consumes it |

**Per-phase metadata gap (Surface 6):** phase files have NO frontmatter today. Canonical O2 path = explicit `--base <PHASE_N_START_SHA>` on the gate line (sidesteps frontmatter for the SHA). `executor_model_class` (contract §6) still needs a persistence slot — decide between prepended frontmatter (collides with check #5) vs another mechanism. The current `<phase-commit-range>` RANGE placeholder + `--diff` is fully replaced by a single `--base` ref vs working tree.
