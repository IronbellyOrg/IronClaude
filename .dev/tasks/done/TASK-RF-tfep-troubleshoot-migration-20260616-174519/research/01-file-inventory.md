# R1 — File Inventory & Edit-Anchor Map

- **Topic**: Exact edit-anchor map for replacing `/sc:forensic` with `/sc:troubleshoot` inside the TFEP of the SuperClaude task pipeline
- **Scope** (read-only, main repo):
  - `/config/workspace/IronClaude/src/superclaude/skills/sc-task-protocol/SKILL.md` (396 lines total)
  - `/config/workspace/IronClaude/src/superclaude/commands/task.md` (187 lines total)
- **Status**: Complete
- **Date**: 2026-06-16
- **Researcher**: R1 (File Inventory). R2=troubleshoot surface, R3=repo-wide cross-refs/sync/report-template, R4=MDTM template. No overlap with those.

---

## A. `sc-task-protocol/SKILL.md` — Section 4.5 TFEP structural map

The entire TFEP feature lives in a single contiguous block: **lines 133–261**. Section ends at line 261; line 262 is blank and line 263 begins `### 5. Feedback Collection` (the next sibling section). All "forensic" / "return-contract.yaml" / "context.yaml" strings in the file are confined to this block (verified: grep for those strings outside 133–261 returns nothing).

| Sub-section | Heading line | Body line range |
|---|---|---|
| `### 4.5 Test Failure Escalation Protocol (TFEP)` | **133** | 133–261 (whole section) |
| intro `**CRITICAL**:` paragraph | — | 135 |
| `#### TFEP Prohibition Rules (VIOLATION-level)` | **137** | 137–151 (incl. Permitted Exceptions 145–149, Valid Adversarial Outcome 151) |
| `#### Test Baseline Snapshot (Pre-Implementation)` | **153** | 153–162 |
| `#### Escalation Trigger Detection` | **164** | 164–179 (MUST-escalate list 166–170; "Escalation gradient" sub-block 172–179) |
| `#### TFEP Execution Flow` | **181** | 181–235 |
| — Step 1: Halt and freeze | **185** | 185–188 |
| — Step 2: Construct failure context | **190** | 190–203 |
| — Step 3: Invoke forensic | **205** | 205–213 |
| — Step 4: Consume forensic results | **215** | 215–222 |
| — Step 5: Tasklist insertion | **224** | 224–229 |
| — Step 6: Resume | **231** | 231–235 |
| `#### TFEP Incident Reporting` | **237** | 237–253 (fenced template 241–251; "committed to git" line 253) |
| `#### Escalation Budget` | **255** | 255–261 (fenced block 257–261) |

Note on naming vs. prompt: the prompt referenced "TFEP Execution Flow steps 1-6" — confirmed there are exactly 6 labeled Steps (1–6) at lines 185/190/205/215/224/231, each `**Step N: ...**` headed, with a continuous 1–15 numbered-list running across them.

---

## B. Rename worklist — every `forensic` / `/sc:forensic` / `return-contract.yaml` / `context.yaml` occurrence

Each row = literal string + line + surrounding sentence. This is the authoritative rename worklist for changes #1 (terminology), #3-implied (command swap), #5 (consume troubleshoot output).

### "forensic" (bare term — terminology rename, change #1 "diagnostic escalation")

| Line | Surrounding text (verbatim) |
|---|---|
| 172 | `**Escalation gradient (within-TFEP, for future forensic integration):**` |
| 205 | `**Step 3: Invoke forensic**` (Step heading) |
| 206 | `5. Determine the forensic tier based on escalation count:` |
| 213 | `7. The forensic pipeline runs autonomously through all its phases and returns a structured return contract.` |
| 215 | `**Step 4: Consume forensic results**` (Step heading) |
| 216 | `8. Read the forensic return contract from ` ``` `{output_dir}/return-contract.yaml` ``` `.` |
| 250 | `- **Forensic artifacts**: {path to output_dir}` (incident-report template field) |
| 253 | `This report is committed to git alongside other forensic artifacts.` |

### "/sc:forensic" (command invocation — swap to `/sc:troubleshoot`; R2 owns the exact troubleshoot flag/contract surface)

| Line | Surrounding text (verbatim) |
|---|---|
| 212 | `6. Invoke: ` `/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick` |
| 258 | `1st TFEP trigger  → /sc:forensic --tier light --intent triage    (~5-8K tokens)` (Escalation Budget fenced block) |
| 259 | `2nd TFEP trigger  → /sc:forensic --tier standard                 (~15-20K tokens)` (Escalation Budget fenced block) |

### "return-contract.yaml" (output-consumption contract — change #5)

| Line | Surrounding text (verbatim) |
|---|---|
| 216 | `8. Read the forensic return contract from ` ``` `{output_dir}/return-contract.yaml` ``` `.` |

Also relevant to #5 (return-contract field reads, no literal "return-contract.yaml" but reads from it):
- Line 213: "...returns a structured return contract."
- Line 225: `10. Read ` `` `tasklist_insertion_path` `` ` from the return contract.`

### "context.yaml" (input package path — change #5)

| Line | Surrounding text (verbatim) |
|---|---|
| 203 | `4. Write context to ` `` `{output_dir}/context.yaml` `` `.` |

(Note: line 191 builds a `failure_context` YAML package and line 212 passes `--context {context_path}`; the literal filename `context.yaml` appears only at line 203.)

---

## C. Specific anchors called out by the change list

### Change #6 — Preserve TFEP freeze semantics (freeze-semantics text)
`**Step 1: Halt and freeze**` heading at **line 185**; freeze body is **lines 185–188**:
- 187: `1. **STOP** testing immediately.`
- 188: `2. **FREEZE** implementation — no further code changes permitted.`
This block contains NO forensic/troubleshoot terminology and must be left semantically intact through the migration.

### Change #7 — Update incident reporting
- Incident-report fenced template: **lines 241–251**.
- "Forensic artifacts" template field: **line 250** → `- **Forensic artifacts**: {path to output_dir}`.
- "committed to git alongside other forensic artifacts" sentence: **line 253**.

### Change #8 — Update escalation-budget language
- `#### Escalation Budget` heading: **line 255**.
- Fenced block: **lines 257–261** (opening ``` ``` ``` at 257, closing at 261):
  - 258: `1st TFEP trigger  → /sc:forensic --tier light --intent triage    (~5-8K tokens)`
  - 259: `2nd TFEP trigger  → /sc:forensic --tier standard                 (~15-20K tokens)`
  - 260: `3rd TFEP trigger  → FULL STOP. Report to user. Do not attempt further fixes.`

### Change #4 — Remediation ownership decision
The remediation-ownership logic is **Step 5: Tasklist insertion (lines 224–229)** plus the contract-driven branch in **Step 4 (lines 215–222)**:
- 219: `- If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.`
- 220–222: status branches (`success` → Step 5; `partial`/escalation → re-loop Step 3; `failed` → halt).
- 225: `10. Read ` `` `tasklist_insertion_path` `` ` from the return contract.`
- 226–229: insert `## Failure Remediation Plan (Adjudicated)` block before existing test/verification tasks, append-not-replace.
These are the lines where "who owns the remediation" (task-protocol vs. troubleshoot) is decided; any ownership change edits this Step 4/Step 5 pair.

### `diagnostic_backend:` clean insertion point
There is currently **no** `diagnostic_backend:` / `backend:` declaration anywhere in the file (grep confirms zero hits). Cleanest insertion candidates:
- **Front of TFEP section**: after the `**CRITICAL**:` intro paragraph (line 135), i.e. a new declaration line/block inserted at **line 136** (blank line) before `#### TFEP Prohibition Rules` at 137. This puts a single authoritative `diagnostic_backend:` knob at the top of the protocol the way `**Trivial Path Override**` sits inline elsewhere (e.g. line 131).
- **Alternatively, at point of use**: immediately before `**Step 3: Invoke forensic**` (line 205), since that is the only step that names the backend command. Inserting at line 204 (blank) keeps the declaration adjacent to its consumer.
The section-top option (~line 136) is the cleaner single-source-of-truth location; the Step-3-adjacent option (~line 204) is the lower-blast-radius location. No existing YAML-style declaration block exists in 4.5 to extend, so this is a net-new line either way.

---

## D. `commands/task.md` — anchors in scope

| Item | Line | Verbatim |
|---|---|---|
| `--no-escalation` flag row mentioning "structured forensic analysis" | **48** | `| `` `--no-escalation` `` ` | `false` | Bypass TFEP (Test Failure Escalation Protocol) triggers. When set, agents may fix test failures directly without structured forensic analysis. **WARNING**: Using `--no-escalation` voids TFEP protection against ad-hoc fixes. |` |

Boundaries-list lines naming TFEP / forensic (section `## Boundaries`, lines 163–187):
| Line | Verbatim |
|---|---|
| 175 | `- Enforce TFEP (Test Failure Escalation Protocol) when test failures meet escalation thresholds` |
| 176 | `- Block ad-hoc fixes when pre-existing tests fail during task execution` |
| 186 | `- Allow ad-hoc code fixes in response to test failures without TFEP workflow (unless `--no-escalation` is set)` |

Other TFEP mentions in task.md (context, not necessarily edits): line 44 (flag list, `--no-escalation` named), line 161 (Activation note: "...TFEP escalation protocol..."). The only "forensic" string in task.md is on **line 48**. No `/sc:forensic`, `return-contract.yaml`, or `context.yaml` strings appear in task.md (grep confirms).

---

## E. Summary for the tasklist builder

- **All TFEP edits in SKILL.md are confined to lines 133–261** — a single contiguous section. Changes #1, #4, #5, #6, #7, #8 all land here; no scattered edits elsewhere in the 396-line file.
- **Rename worklist = 11 line-anchored occurrences** in SKILL.md: forensic ×8 (172, 205, 206, 213, 215, 216, 250, 253), /sc:forensic ×3 invocation sites (212, 258, 259), context.yaml ×1 (203), return-contract.yaml ×1 (216). The forensic#216 line and forensic#212/258/259 lines overlap the command-swap and term-rename concerns — edit once, satisfy both.
- **Freeze semantics (change #6) = lines 185–188**, terminology-clean today; preserve verbatim except any heading-word rename.
- **Incident reporting (change #7) = template 241–251 (field at 250) + sentence at 253.**
- **Escalation budget (change #8) = heading 255 + fenced block 257–261** (forensic invocations at 258–259).
- **Remediation ownership (change #4) = Step 4 branches 215–222 + Step 5 insertion 224–229.**
- **`diagnostic_backend:` insertion = net-new line; recommend section-top ~line 136 (single source of truth) or Step-3-adjacent ~line 204 (point of use).** No existing declaration to extend.
- **task.md = 2 edit clusters: line 48 ("structured forensic analysis") + Boundaries lines 175/176/186 + Activation line 161.** Only one literal "forensic" (line 48).
