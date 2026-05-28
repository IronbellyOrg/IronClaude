# Bucket C — task-builder skill content digest

## Files read
| Path | Lines | Status |
|------|-------|--------|
| `src/superclaude/skills/task-builder/SKILL.md` | 1709 | read in full (4 chunks) |

## Files expected but absent
Verified via `ls`: only `SKILL.md` exists in the skill directory.
- `src/superclaude/skills/task-builder/refs/**` — **absent**
- `src/superclaude/skills/task-builder/rules/**` — **absent**
- `src/superclaude/skills/task-builder/templates/**` — **absent**
- `src/superclaude/skills/task-builder/scripts/**` — **absent**

## Skill purpose and trigger
- **Produces:** MDTM task file at `${TASK_DIR}${TASK_ID}.md` plus research artifacts and QA reports — SKILL.md:6–13; output schema SKILL.md:1409–1485.
- **Trigger phrases:** "build a task file for…", "create a task for…", "rf task builder", "create an MDTM task for…", BUILD-REQUEST*.md reference — SKILL.md:3.
- **Inputs:** GOAL (mandatory), WHY, WHERE, optional `BUILD_REQUEST` .md path — SKILL.md:30–47.

## Execution model
- **Single stage (Stage A only):** explicitly "no Stage B — the user reviews the task file and executes it with `/task [path]`" — SKILL.md:12, SKILL.md:141.
- **13 numbered steps (A.1–A.11 with A.8.5 and A.10.5):** SKILL.md:143–157.
- **Not single-pass; not interview-driven; is agent-team-orchestrated:** "spawns parallel researcher agents via the Agent tool, runs rf-analyst + rf-qa quality gates… then spawns the `rf-task-builder` agent" — SKILL.md:10. Skill is the orchestrator, NOT the builder — SKILL.md:80–82.
- **Delegates to:** `general-purpose` researchers (SKILL.md:398, 664), `rf-analyst` (SKILL.md:582), `rf-qa` (SKILL.md:614, 876), `rf-qa-qualitative` (SKILL.md:927), `rf-task-builder` (SKILL.md:719). Listed in Naming Conventions table SKILL.md:1690–1697.
- **Parallel research model:** "ALL researchers for a track spawned in the SAME message for parallel execution… Multi-track: ALL researchers across ALL tracks in one message" — SKILL.md:400–401; SKILL.md:1673–1677.
- **Handoff patterns:** Orchestrator-mediated with 3 explicit flows — RESEARCH_NEEDED (max 2), MALFORMED (max 2), NEED_USER_INPUT (deferred to Open Questions) — SKILL.md:852–870. Separate retry counters: SKILL.md:1550.

## Output artifacts
- **Path convention:** `.dev/tasks/to-do/TASK-RF-YYYYMMDD-HHMMSS/` — SKILL.md:107–116; multi-track `TASK-RF-track-T-YYYYMMDD-HHMMSS/` — SKILL.md:131.
- **File format:** MDTM (Template 01 generic, Template 02 complex) — SKILL.md:228–238; templates external at `.claude/templates/workflow/0[1|2]_mdtm_template_[generic|complex]_task.md` — SKILL.md:544, 1420.
- **Frontmatter fields:** `id, title, description, status, type, priority, created_date, updated_date, assigned_to, template_schema_doc, estimation, task_type, related_docs, tags` — SKILL.md:1410–1429.
- **Checklist-item schema:** `context + action + output + verification + completion gate` (the "B2 self-contained item pattern") — SKILL.md:1452–1457; SKILL.md:900, 1495.
- **Templates used:** generic (01) vs complex (02), selected per-track via signal table — SKILL.md:230–238, SKILL.md:378–391.

## Self-contained item invariant
- **Definition (quote):** "Checklist items are self-contained (context + action + output + verification + completion gate)" — SKILL.md:900; restated SKILL.md:1495, SKILL.md:1515.
- **Every item MUST embed:** Context (executor's needed knowledge), Action (exactly what to do), Output (what gets created/modified), Verification (how to confirm), Completion gate (when done) — SKILL.md:1453–1457.
- **Per-item references required:** "Evidence-based: items reference specific file paths, not vague descriptions" — SKILL.md:902, SKILL.md:1518. Agent prompts "fully embedded in each spawning item" — not "see SKILL.md" — SKILL.md:1498, 1517.
- **Acceptance criteria:** verification clause with "ensuring..." and "measurable criteria" — SKILL.md:1522.

## Evidence binding
- **Tasks bound to evidence via:** research files in `${TASK_DIR}research/[NN]-[topic].md` (SKILL.md:124, 1600), referenced by builder which "only works from verified research files, not from memory or inference" — SKILL.md:21.
- **File paths + line numbers + function/class names required:** "Every finding must cite actual file paths, line numbers, function names, class names. No assumptions, no inferences, no guessing" — SKILL.md:452–454, SKILL.md:1530.
- **"Unverified" marker rule:** "If you can't verify it, mark 'Unverified.'" — SKILL.md:454, SKILL.md:1213. Doc-claim tagging: `[CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]` — SKILL.md:519–522, 1150–1153.

## Persistent artifacts
- **Contents of `.dev/tasks/`:** task file, `research-notes.md`, `research/*.md`, `qa/*.md` (analyst-completeness, qa-research-gate, qa-task-validation, qa-qualitative-review) — SKILL.md:120–129, 1597–1607.
- **Incremental write (not atomic):** "INCREMENTAL TASK FILE WRITING (MANDATORY — NEVER ONE-SHOT)" — SKILL.md:819–832; researcher protocol SKILL.md:437–449, 1196–1209; rule #8 SKILL.md:1542.
- **Preservation rule:** "Preserve research artifacts… persist after the task file is built. They serve as the evidence trail. Do NOT delete intermediate files" — SKILL.md:1536, SKILL.md:1608.

## Zero-trust QA
- **QA stages on own output (3 gates):** research gate (A.8, rf-analyst + rf-qa parallel), task structural validation (A.10, rf-qa task-integrity), task qualitative validation (A.10.5, rf-qa-qualitative) — SKILL.md:18, 574–654, 872–916, 923–1000.
- **Pre-write validation gates:** A.5 mandatory self-review of research notes BEFORE spawning researchers — SKILL.md:351–373.
- **Adversarial stance (quote):** "Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked." — SKILL.md:621, 878, 895, 929, 958, 1291, 1308, 1386. "Zero tolerance — if you can't verify it, it fails." — SKILL.md:1340.
- **Enumerated checks:**
  - Research-gate 9-item analyst checklist — SKILL.md:594–602, 1266–1274.
  - Research-gate 10-item QA checklist — SKILL.md:1323–1333.
  - Research-gate 5-item QA prompt — SKILL.md:627–632.
  - Task-integrity 9-item validation — SKILL.md:898–906, 1389–1398.
  - Task-file validation checklist (15 items) — SKILL.md:1491–1507.
  - Qualitative review "15-item Task File Qualitative Review checklist from agent definition" — SKILL.md:961.
  - Task File Content Rules table (8 rule pairs) — SKILL.md:1513–1523.

## Determinism status
- **No explicit determinism claim.** Skill describes default tier, default single-track, and "default Template 02 when uncertain" — SKILL.md:88, 226, 238 — but never asserts deterministic outputs.
- **Explicit non-determinism:** Agent research is exploratory; tier scales researcher count 3–8 (SKILL.md:90–94); "Scenario B → Researchers do broad exploration to figure out what exists and determine reasonable defaults" — SKILL.md:201. Web research is conditional on tier + gate gaps — SKILL.md:658–662.

## Traceability
- **Traceability matrix:** absent. No matrix structure described.
- **Roadmap-item-to-task chains:** absent. The skill never references "roadmap" — it works from a GOAL/BUILD_REQUEST, not a roadmap.
- **Deliverable IDs:** Only `TASK_ID` (`TASK-RF-YYYYMMDD-HHMMSS`) — SKILL.md:111–115. No per-checklist-item IDs beyond template's `1.1`/`1.2` numbering — SKILL.md:1452, 1459.

## Tier classification
- **Tier table:** Quick / Standard / Deep tied to file count and researcher count (3 / 4–5 / 6–8) and web-agent budget (0 / 0–1 / 1–2) — SKILL.md:90–94.
- **Algorithm:** rule-based, not numeric: "Default Standard… 'thorough/comprehensive/deep dive' → always Deep… Quick only for <5 files, single concern… multi-track defaults to Deep" — SKILL.md:96–101; restated SKILL.md:1546.
- **No complexity-scoring algorithm.** No weighted formula, no point system.

## Quality gates
- **Pre-write gates:** A.5 self-review (7 questions) BEFORE spawning researchers — SKILL.md:357–363; A.8 analyst+QA research gate before builder — SKILL.md:574–654.
- **Mid-pipeline gates:** A.10 task-integrity (9 checks) — SKILL.md:898–906; A.10.5 qualitative (15-item checklist) — SKILL.md:961.
- **Enumeration of distinct gate checks across skill (deduped, approximate count):**
  - A.5 sufficiency: 7 — SKILL.md:357–363.
  - A.8 analyst: 9 — SKILL.md:594–602.
  - A.8 QA (in-prompt): 5 — SKILL.md:627–632; or 10 in agent template — SKILL.md:1323–1333.
  - A.10 task integrity: 9 — SKILL.md:898–906.
  - A.10.5 qualitative: 15 (agent-side checklist, referenced not enumerated here).
  - A.10/Task File Validation Checklist (skill-side mirror): 15 — SKILL.md:1493–1507.
- **Comparison to sc:tasklist's 17:** task-builder has more gate *stages* (4 vs sc:tasklist's typical pre-write) but does NOT enumerate a single 17-check list. The closest parallels are the 15-item validation checklist (SKILL.md:1491–1507) and 18 Critical Rules (SKILL.md:1526–1564).

## Agent delegation
- **Subagents spawned:** `general-purpose` (researchers + gap-fill + web), `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-task-builder` — SKILL.md:398, 583, 614, 664, 720, 877, 927; Naming Conventions table SKILL.md:1690–1697.
- **Retry budgets:**
  - Scope-discovery gap-fill: max 2 rounds — SKILL.md:371.
  - Research-gate gap-fill: max 3 rounds — SKILL.md:651.
  - RESEARCH_NEEDED: max 2 rounds — SKILL.md:859.
  - MALFORMED: max 2 rounds — SKILL.md:865.
  - Counters tracked independently (potential 4 total builder invocations) — SKILL.md:870, 1550.
- **Failure handling:** "After max rounds, proceed with what's available and note remaining gaps in AMBIGUITIES_FOR_USER" — SKILL.md:371; "After 3 rounds, proceed with remaining gaps as Open Questions in the task file" — SKILL.md:652; multi-track isolation: "Failure in one track MUST NOT prevent other tracks from completing" — SKILL.md:1548, 1681.

## Invariants the skill protects (G6 candidate list)

1. **Self-contained item** — "Checklist items are self-contained (context + action + output + verification + completion gate)" — SKILL.md:900; rule #14 "Task file actionability… each item must be self-contained" — SKILL.md:1554.
2. **Evidence-bound item** — Critical Rule #2: "Evidence-based claims only. Every finding must cite actual file paths, line numbers, function names" — SKILL.md:1530; "items reference specific file paths, not vague descriptions" — SKILL.md:902; "No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings" — SKILL.md:903, 1502.
3. **Persistent `.dev/tasks/` artifact** — "Preserve research artifacts… persist after the task file is built… Do NOT delete intermediate files" — SKILL.md:1536; "Research and QA report files persist after the task file is built — they serve as the evidence trail" — SKILL.md:1608.
4. **Zero-trust QA** — Rule #7: "Quality gates are mandatory. rf-analyst + rf-qa MUST be spawned at the research gate. Do not skip verification to save time" — SKILL.md:1540; adversarial-stance phrase repeated 8× across the file.
5. **Parallel research** — "ALL researchers for a track spawned in the SAME message for parallel execution… Multi-track: ALL researchers across ALL tracks in one message" — SKILL.md:400–401; "Parallel spawning instructions included for research/QA phases" — SKILL.md:1499.

**Other invariants declared (with cite):**
- **Granularity / no batch items** — Rule A3 "Complete Granular Breakdown": "individual items per file/component… NOT batch items like 'document all 14 handlers'" — SKILL.md:431–434, 901, 1517.
- **Codebase as source of truth** — Rule #1 SKILL.md:1528; code > docs > web — SKILL.md:706, 1167.
- **No one-shotting** — Rule #8 SKILL.md:1542; incremental writing protocol SKILL.md:437–449, 819–832.
- **Anti-orphaning** — Rule #15: completion items inside final phase — SKILL.md:1556, 1505.
- **No team infrastructure** — Rule #13: never use TeamCreate/SendMessage/TaskCreate — SKILL.md:1552; ESCALATION blocks override agent defaults — SKILL.md:456, 674, 804, 890.
- **Multi-track isolation** — Rule #11 SKILL.md:1548.
- **Partitioning thresholds** — Rule #9: >6 research files → multiple analyst/QA instances — SKILL.md:643, 1544.
- **BUILD_REQUEST field encoding invariants** — Rules #16/17/18 require QA gates, validation, and testing items in generated task file when BUILD_REQUEST specifies them — SKILL.md:1558–1562. MALFORMED if omitted.

## Where the skill is explicitly silent
- **Traceability matrix** — silent. Does not address roadmap-to-task or matrix structure.
- **Roadmap input** — silent. Skill works from GOAL/BUILD_REQUEST, not roadmaps.
- **Numeric complexity scoring** — silent. Uses rule-based tier selection only.
- **Deliverable ID schema beyond TASK_ID** — silent. No per-item IDs beyond `1.1`/`1.2` template numbering.
- **CLI/programmatic mode** — silent. Skill is invoked via `/task-builder [request]` (SKILL.md:80) or by other skills spawning the builder agent (SKILL.md:81–82); no Python CLI integration described.
- **Deterministic output guarantee** — silent (not actively excluded; just never claimed).
- **Sprint/sprint-bundle output format** — silent. Output is a single MDTM file per track, not a sprint bundle.

Coverage map vs G6 candidates:
| Invariant | Status |
|-----------|--------|
| Self-contained item | covered — SKILL.md:900, 1495, 1554 |
| Evidence-bound item | covered — SKILL.md:1530, 902, 1502 |
| Persistent `.dev/tasks/` artifact | covered — SKILL.md:1536, 1608 |
| Zero-trust QA | covered — SKILL.md:1540, adversarial stance ×8 |
| Parallel research | covered — SKILL.md:400–401, 1499 |
| Granularity / no batch items | covered — SKILL.md:1517 |
| Traceability matrix | silent — does not address |
| Numeric complexity score | silent — does not address |
| Roadmap-as-input | silent — does not address |
| Sprint-bundle output | silent — does not address |
| Per-item deliverable IDs | silent — does not address |
| CLI/programmatic execution | silent — does not address |
| Deterministic output | silent — does not address |

## evidence_status:
`complete`
