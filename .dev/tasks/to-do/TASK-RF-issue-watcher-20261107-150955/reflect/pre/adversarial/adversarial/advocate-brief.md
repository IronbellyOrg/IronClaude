# Advocate brief (shared by all advocates; input to the Task tool, not a report)

Root: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher
ADV = <root>/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/pre/adversarial/adversarial

## What is being debated
Three reviewer cards audit one pre-execution task file against one design:
- Task file (209 items): <root>/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- Design: <root>/docs/designs/issue-watcher.md
- Deviation authority: <root>/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md and the task file's Open Questions list. A deviation declared there is NOT a defect.
- Variant 1 (reviewer 1, analyzer, sonnet, calibrated confidence 0.75): ADV/variant-1-original.md
- Variant 2 (reviewer 2, qa, haiku, calibrated confidence 0.85): ADV/variant-2-original.md
- Variant 3 (reviewer 3, refactorer, opus, calibrated confidence 0.85): ADV/variant-3-original.md
- Diff analysis (28 debate points S/C/X/A plus 5 unique U points): ADV/diff-analysis.md

The debate is weighted by CALIBRATED confidence, not self-reported confidence.

## Binary severity (decide from evidence, not from the reviewer's label)
- blocking: a worker following the task file would produce wrong code, run an impossible command, deadlock, break a stated constraint, leave a required behaviour untested or unbuilt, or take an unsafe action; also a false claim or a missing required deliverable.
- minor: cosmetic, wording, a moved line number on a true claim, a nit.
- DROP: the cited text does not exist at or near the cited line, or the "defect" is a declared deviation, or the claim is false on reading the task file.

## Verification rule
You MAY Read the task file, the design, research/06 and any repo file cited (read-only) to verify cited lines. Verify before you argue. A finding whose cited text does not exist is dropped.

## Hard rules
- Read-only everywhere except your one output file named in your prompt. Never edit the task file, the design, the variants or anything under .claude/. Never run git. Do not spawn sub-agents.
- STEELMAN each opposing variant before critiquing it. Cite file:line for every claim. Label speculation. Concede honestly.
- Focus areas: correctness, coverage, deviation-classification.

## Point questions (answer every one; the token in CAPS or the listed value is your Verdict)
- S-001: Format the merged register should follow: YAML | MARKDOWN
- S-002: Coverage unit set the merged coverage_resolution should draw on: V1 | V2 | V3 | UNION
- S-003: Severity scale for the merge: BINARY | GRADED
- S-004: Category vocabulary for the merge: ENUM (coverage_gap/contradiction/unexecutable_item/wrong_citation/gate_weakness/sequencing/other) | DEVIATION-TAXONOMY
- C-001 (R1-003), C-002 (R1-004), C-003 (R1-005), C-004 (R3-003), C-005 (R3-004), C-006 (R3-005), C-007 (R3-006), C-008 (R3-007), C-009 (R3-008): VALID-BLOCKING | VALID-MINOR | DROP
- C-010: Most accurate overall verdict after evidence: V1 | V2 | V3 | OTHER (say which findings are blocking)
- C-011: Should coverage judgements a card itself marks "not re-read / not line-verified" carry less weight than line-verified ones? YES | NO
- X-001 (R1-002 + R3-001, one defect): VALID-BLOCKING | VALID-MINOR | DROP
- X-002 (R1-001; T-2): verdict VALID-BLOCKING | VALID-MINOR | DROP, Secondary = T-2 coverage covered | partially_covered | not_covered
- X-003 (INF-123), X-004 (INF-155), X-005 (INF-016): covered | partially_covered | not_covered
- X-006 (R2-002; INF-146/AC-14): VALID-BLOCKING | VALID-MINOR | DROP, Secondary = INF-146 coverage
- X-007 (R2-001; AC-6/INF-138): VALID-BLOCKING | VALID-MINOR | DROP, Secondary = AC-6 coverage
- X-008 (R3-002; lint gates): VALID-BLOCKING | VALID-MINOR | DROP
- X-009: Are Variant 3's "automatic mapping is wrong" corrections right (the items exist)? YES | NO
- A-001, A-002, A-003, A-004 (shared assumptions): ACCEPT | REJECT | QUALIFY (mandatory; an omission is flagged)

## Output file format (markdown)
## Advocate: Variant N (<model>:<persona>)
### Position Summary
### Steelman: Variant X   (one per opposing variant)
### Key Strengths Claimed
### Weaknesses in Variant X   (one per opposing variant)
### Concessions
### Shared Assumption Responses   (A-001..A-004, each ACCEPT/REJECT/QUALIFY + one line)
### Point Positions
| Point | Verdict | Secondary | Evidence (path:line - verbatim excerpt, at most 25 words) | Conceded to |
One row per point, all 28: S-001..S-004, C-001..C-011, X-001..X-009, A-001..A-004.
