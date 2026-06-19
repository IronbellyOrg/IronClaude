# Anchor Map — TASK-RF-tasklist-rfmerge-20260619-041423

**Confirmed:** 2026-06-19 (Step 1.4). All anchors located by their VERBATIM line text in the
current source. SKILL.md = `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1631 lines).
phase-template = `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (189 lines).
index-template = `src/superclaude/skills/sc-tasklist-protocol/templates/index-template.md`.

No anchor is DRIFT-UNRESOLVED. Research/01/04/07 absolute numbers vs confirmed current lines noted.

| Anchor Name | Proposal | Verbatim Line Text | Confirmed Current Line | File |
|---|---|---|---|---|
| Phase Files Table heading | P1/P5 index region | `#### Phase Files Table` | 709 | SKILL.md |
| Feedback Collection Template | P5 insert-after anchor | `#### Feedback Collection Template` | 820 | SKILL.md |
| Glossary | P5 insert-before anchor | `#### Glossary` | 841 | SKILL.md |
| Task body Artifacts marker | P1 | `**Artifacts (Intended Paths):**` | 894 | SKILL.md |
| Task body Deliverables marker | P1 | `**Deliverables:**` | 900 | SKILL.md |
| Task body Steps marker | P1 | `**Steps:**` | 904 | SKILL.md |
| Task body Notes marker | P1 | `**Notes:** <optional; max 2 lines; include tier conflict resolution if applicable>` | 927 | SKILL.md |
| Self-Check gate close | P4 serialize anchor | `If any check 1-20 fails, fix it before writing any output file.` | 1187 | SKILL.md |
| Final Output Constraint | P4 emit-before boundary | `## Final Output Constraint` | 1191 | SKILL.md |
| Stage 7 header | P3/P4 | `### Stage 7: Roadmap Validation (2N Parallel Agents)` | 1244 | SKILL.md |
| Agent A spawn | P4 inject (payload) | `3. Spawn **Agent A** with:` | 1254 | SKILL.md |
| Agent B spawn | P4 inject (payload) | `4. Spawn **Agent B** with:` | 1258 | SKILL.md |
| Validation-instructions blockquote intro | P4 inject (prose) | `> You are a tasklist validation agent. You receive a subset of tasks...` | 1267 | SKILL.md |
| Drift check (first dimension) | P4 inject-before | `> 1. **Drift**: ...` | 1271 | SKILL.md |
| Orchestrator merge and deduplication | P3 merge-step anchor | `**Orchestrator merge and deduplication**:` | 1288 | SKILL.md |
| Stage-7 gate / retry clause | P3 gate amend | `**Stage gate**: All 2N agents completed successfully. Findings merged and deduplicated. Zero agent failures (if an agent fails, retry once before reporting error).` | 1310 | SKILL.md |
| Stage 8 header | P3 short-circuit guard | `### Stage 8: Patch Plan Generation` | 1312 | SKILL.md |
| Stage-8 short-circuit rule | P3 short-circuit guard | `**Short-circuit rule**: If Stage 7 produced zero findings across all agents, write a clean ValidationReport.md...` | 1316 | SKILL.md |
| Stage-8 short-circuit "skip Stages 9 and 10" | P3 | `Then skip Stages 9 and 10. The skill is complete.` | 1325 | SKILL.md |
| Stage 9 header | P2 loop-back target | `### Stage 9: Patch Execution (Delegate to ` + "`sc:task`" + `)` | 1409 | SKILL.md |
| Stage 9 mechanism | P2 | `**Mechanism**: Invoke ` + "`sc:task`" + ` via the ` + "`Skill`" + ` tool with:` | 1413 | SKILL.md |
| Stage 9 gate | P2 | `**Stage gate**: ` + "`sc:task`" + ` reports completion. All checklist items addressed.` | 1427 | SKILL.md |
| Stage 10 header | P2 | `### Stage 10: Spot-Check Verification` | 1429 | SKILL.md |
| Stage 10 Verification Results | P2 iteration state | `## Verification Results` (appended to ValidationReport.md) | 1442 | SKILL.md |
| Stage-10 no-loop gate | P2 load-bearing edit | `**Stage gate**: All findings verified. If any remain ` + "`UNRESOLVED`" + `, they are logged but the skill does NOT loop. The ` + "`ValidationReport.md`" + ` serves as the record for human review.` | 1456 | SKILL.md |
| Stage 10.5 header | P2 fence | `### Stage 10.5: Pre-Reflect Sign-off` | 1460 | SKILL.md |
| Stage-10.5 fencing rationale | P2 fence note | `This stage is **fenced after the Stage 8-10 patch chain**:` | 1462 | SKILL.md |
| §5.3 Compliance Tier header | P5 fence | `### 5.3 Compliance Tier Classification (mandatory, deterministic)` | 544 | SKILL.md |
| Stale 17-checks completion string | P4 hygiene fix | `- Stage 6: "Self-Check: all 17 checks passed"` | 1597 | SKILL.md |
| Input-Contract open sentence | --spec §22 (xcut) | `You receive exactly one input: **the roadmap text**.` | 49 | SKILL.md |
| Input-Contract close sentence | --spec §22 (xcut) | `Treat the roadmap as the **only source of truth**.` | 57 | SKILL.md |
| phase-template Artifacts marker | P1 mirror | `**Artifacts (Intended Paths):**` | 49 | phase-template.md |
| phase-template Deliverables marker | P1 mirror | `**Deliverables:**` | 55 | phase-template.md |
| phase-template Steps marker | P1 mirror | `**Steps:**` | 59 | phase-template.md |
| phase-template Notes marker | P1 mirror | `**Notes:** <optional; max 2 lines>` | 82 | phase-template.md |
| index-template Feedback Collection Template | P5 mirror | `### Feedback Collection Template` / `## Feedback Collection Template` | 123 / 125 | index-template.md |
| index-template Feedback Log row | P5 mirror context | `| Feedback Log | ` + "`TASKLIST_ROOT/feedback-log.md`" + ` |` | 48 | index-template.md |

## Drift notes (research absolute # → confirmed current #)

- P1/P5 index region cited `:707/:709` → Phase Files Table confirmed at **709**.
- P5 cited `:820-839/:841` → Feedback Collection Template **820**, Glossary **841** (exact match).
- P1 task body cited `:894-927` → Artifacts **894**, Deliverables **900**, Steps **904**, Notes **927** (exact match).
- P4 serialize cited `:1187` → **1187** (exact). Final Output Constraint **1191** (the emit-before boundary).
- P4 inject cited `:1254-1286` → Agent A **1254**, Agent B **1258**, blockquote intro **1267**, Drift **1271** (within range).
- P3 cited `:1288`/`:1310` → Orchestrator merge **1288**, Stage-7 gate **1310** (exact match).
- P3 Stage-8 short-circuit cited `:1316-1325` → short-circuit rule **1316**, skip line **1325** (exact match).
- P2 Stage-10 no-loop cited `:1456` → **1456** (exact). Stage-10.5 fence cited `:1462` → **1462** (exact).
- P4 hygiene cited `:1597` → **1597** (exact).
- --spec §22 cited `:49`/`:57` → **49**/**57** (exact match). Middle bullet list = lines 50-56.
- P1 mirror cited `:55-82` → Deliverables **55**, Steps **59**, Notes **82** (within range).

## Material determination for P5 (Step 6.3)

**index-template.md DOES carry the Feedback Collection Template** (heading at line 123, literal
`## Feedback Collection Template` at line 125, plus a `Feedback Log` artifact-paths row at line 48).
Therefore Step 6.3's mirror edit IS required: add a matching `## Tier Calibration Advisory`
placeholder shape adjacent to the feedback template in index-template.md.
