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
- Each research agent = 1 item; each synthesis agent = 1 item
- Phase 3 gets 4 items (analyst, qa, verdict-read, gap-fill)
- Phase 5 synthesis QA = 1 item (spawns 4 agents internally)
- Phase 6 = 3 items (assembler, structural QA, qualitative QA + final status update = 4)
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
