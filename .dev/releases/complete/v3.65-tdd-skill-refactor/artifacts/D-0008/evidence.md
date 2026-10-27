# D-0008 Evidence: refs/agent-prompts.md Extraction

## Task: T02.01

## Source
- File: `src/superclaude/skills/tdd/SKILL.md`
- Line range: 525-942 (current 1387-line version)
- Blocks: B15-B22 per fidelity index

## Deliverable
- Path: `src/superclaude/skills/tdd/refs/agent-prompts.md`
- Line count: 418 lines

## Verification

### 8 Agent Prompts Present (SC-11)
1. Codebase Research Agent Prompt
2. Web Research Agent Prompt
3. Synthesis Agent Prompt
4. Research Analyst Agent Prompt (rf-analyst -- Completeness Verification)
5. Research QA Agent Prompt (rf-qa -- Research Gate)
6. Synthesis QA Agent Prompt (rf-qa -- Synthesis Gate)
7. Report Validation QA Agent Prompt (rf-qa -- Report Validation)
8. Assembly Agent Prompt (rf-assembler -- TDD Assembly)

### Zero Drift Confirmation
- `diff` between `sed -n '525,942p' SKILL.md` and `refs/agent-prompts.md`: **zero differences**

### Checksum Markers
- **B15 first 10 words**: "## Agent Prompt Templates These templates are provided to the"
- **B15 last 10 words**: "the actual source code of X verifies X exists. ```"
- **B22 first 10 words**: "### Assembly Agent Prompt (rf-assembler -- TDD Assembly) ``` Assemble"
- **B22 last 10 words**: "should be candidates for archival (the TDD replaces them) ```"

All markers match fidelity index.

### Sentinel Check
- `{{`: 0 matches
- `<placeholder>`: 0 matches
- `TODO`: 0 matches
- `FIXME`: 0 matches

## Verdict: PASS
