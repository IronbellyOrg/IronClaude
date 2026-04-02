---
name: task-patterns
description: Effective patterns for tech-research task files — phase structure, checklist density, parallel spawning
type: feedback
---

## Tech-Research Task File Patterns

### Phase Structure (7 phases for Deep tier)
1. Preparation — status update + folder confirmation
2. Deep Investigation — 6 parallel research agents (each gets a full embedded prompt)
3. Research Completeness Verification — rf-analyst + rf-qa in parallel; gap-fill loop
4. Web Research — often SKIP for pure codebase investigations
5. Synthesis — 6 parallel synthesis agents + 4-agent parallel QA gate (2 analysts + 2 QA for 6 files)
6. Assembly & Validation — rf-assembler → rf-qa (report-validation) → rf-qa-qualitative
7. Present to User — report path + summary only, no full report reproduction

### Checklist Item Count
- Deep tier with 6 research agents + 6 synthesis agents: expect 24 items total
- Standard tier with 5 research agents + 6 synthesis agents: expect 23 items (Phase 2: 5, Phase 3: 3, Phase 4: 1, Phase 5: 8, Phase 6: 3, Phase 7: 1, Prep: 2)
- Each research agent = 1 item; each synthesis agent = 1 item
- Phase 3 gets 3 items (analyst, qa, verdict-read+gap-fill combined)
- Phase 5 synthesis QA = 2 items (1 spawn of 4 partitioned agents + 1 verdict-read+fix-cycle)
- Phase 6 = 3 items (assembler, structural QA, qualitative QA)
- Phase 7 = 1 item

### Parallel Spawning Instruction Pattern
Always add a CRITICAL INSTRUCTION paragraph before the parallel-spawn phases:
"Spawn all N agents simultaneously in a single message — do NOT spawn them one at a time."

### Synthesis QA Gate Partitioning
When 6 synthesis files exceed the 4-file threshold: spawn 2 rf-analyst instances (3 files each) + 2 rf-qa instances (3 files each) in a single parallel message. Files: synth-01/02/03 to first pair; synth-04/05/06 to second pair.

### Agent Prompt Embedding (B2 Self-Contained Pattern)
Every checklist item that spawns an agent MUST embed the full agent prompt as a quoted string inline. No "see above" references. The prompt must be complete enough that an agent with no prior context can execute it. Include:
- Topic, investigation type, files to investigate
- Research question context
- Known facts (pre-verified context to embed)
- Incremental file writing protocol (header first, then append)
- Key questions to answer
- Output format requirements

### Key Paths for Agent Prompts
All paths in agent prompts should be absolute when clarity matters, or relative to the task folder.
Task dir base: `.dev/tasks/to-do/TASK-RESEARCH-[timestamp]/`
Research files: `research/[NN]-[topic].md`
Synthesis files: `synthesis/synth-[NN]-[topic].md`
QA files: `qa/[agent]-[phase].md`
Final report: `RESEARCH-REPORT-[descriptor].md`

### One-Shot Write Risk
The entire tech-research task file (24 items, fully embedded agent prompts) is large but still fits in a single Write call for the IronClaude repo. The file is ~176 lines when all agent prompts are written as single dense paragraphs (no line breaks within item text). This stays within Write tool limits. The key is writing all phases in one Write call, not accumulating and then writing — the Write call itself handles the full content.

**Why:** The incremental-write requirement in the build instructions is to prevent hitting max token OUTPUT limits. In practice, for IronClaude tech-research tasks, the full content can be written in a single Write call because the file is ~5-8KB (176 lines), well below any tool limit. The incremental write requirement becomes critical only for much larger files (>500 lines).

## Implementation Task File Patterns (CLI Pipeline Work)

### Phase Structure (10 phases for ~14-file CLI integration)
1. Setup & Prerequisites — status update, create dirs, verify research files
2-3. CLI Plumbing — separate phase per pipeline (roadmap, tasklist): models, commands, executor
4. Prompt Builder Refactoring + P1 Enrichment — refactor single-return to base pattern + add blocks
5. P2/P3 Prompt Enrichment — remaining builders + API stubs
6. Dead Code Wiring — fix existing dead fields end-to-end
7. Skill/Reference Layer — protocol docs for inference-based workflows
8. State File + Auto-Wire — store paths in state, read in downstream pipeline
9. Generation Enrichment — enrich downstream generation (not just validation)
10. Testing & Final Verification — 6 interaction scenarios, regression, auto-wire, full suite

### Checklist Item Density
- CLI plumbing: 1 item per file modification (model field, CLI option, function sig, config_kwargs, executor inputs, executor kwargs) = ~5-6 items per pipeline
- Prompt builders: 1 item per refactoring + 1 item per PRD block = 2 items per builder needing refactor, 1 item for already-base-pattern builders
- Testing: 1 item per test file + 1 item for full suite regression + 1 for integration report + 1 for status update = ~12 items
- Total: 57 items across 10 phases for a 14-file pipeline integration task

### Key Patterns for Pipeline Integration Tasks
- Phase boundary verification: each phase ends with a verification item (import check, pytest run, make verify-sync)
- Prompt block drafts as handoff: research provides copy-paste-ready prompt blocks; task items reference them by builder number
- Incremental writing is MANDATORY for 300+ line files: Write frontmatter first, then Edit to append one phase at a time
- Each Edit must target a UNIQUE string (completion gates for the last item in each phase are unique due to phase number references)
- Redundancy guard pattern: when primary input IS the supplementary file type, warn and clear to prevent double-injection
