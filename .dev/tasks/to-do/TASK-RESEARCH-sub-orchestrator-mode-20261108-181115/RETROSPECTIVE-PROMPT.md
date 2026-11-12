# Retrospective Prompt

Paste the prompt below into a separate session. This is an investigation handoff, not permission to edit the framework or resume the subordinate-coordinator feature.

---

Review how the issue-444 research session became disproportionately expensive and slow, identify the concrete causes in our instructions and execution, and recommend the smallest changes that prevent recurrence without weakening evidence, security or honest completion.

## Objective and authorization

The original request was: “Run the tech research without switching model tiers.” The agreed deliverable was a decision report about subordinate coordinators for the proposed orchestrator command, explicitly not an implementation plan or implementation. Later the user requested a process diagnosis, Ponytail's fastest complete finish, and this retrospective handoff.

Investigate the process. Do not implement subordinate coordination, modify skills/agents/hooks, commit, push, publish private evidence or open issues. Proposed framework changes require a separate approved implementation request. Do not automatically invoke the same large research/task pipeline you are evaluating. Start with direct read-only inspection. Use no additional reviewers unless genuinely necessary and authorized. Do not change model tiers.

## Evidence locations

Use this worktree if it still exists; otherwise locate the preserved task package in the current checkout before proceeding:

`/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test`

Task package, relative to that checkout:

`.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/`

Read its BUILD-REQUEST.md, task Markdown, execution/phase logs, research notes, inventories, consolidated findings, original returned reports, synthesis and final report if present. Detect the actual completion state; do not assume the state when this prompt was written is final. The retrospective prompt itself is a handoff, not an independently validated incident report.

Session transcript:

`/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-fix-flaky-parallel-thread-test/952cee73-732b-4629-bd21-afa7a36058dd.jsonl`

Completed-agent transcripts, where still available:

`/tmp/claude-1000/-home-coder-workspaces-worktrees-IronClaude-fix-flaky-parallel-thread-test/952cee73-732b-4629-bd21-afa7a36058dd/tasks/`

Parse these selectively and read bounded excerpts. Never dump the whole session or every agent transcript into context. Distinguish human messages from hook reminders, automatic task notifications, compacted summaries and agent quotations. Summaries provide leads, not proof of user approval.

Read the actual runtime instructions under `~/.claude/skills/{tech-research,task-builder,task}/`, `~/.claude/agents/rf-*.md`, global/project instructions, applicable hooks and permissions. Compare with their canonical source under `src/superclaude/skills/`, `src/superclaude/agents/` and `src/superclaude/core/`; relevant plugin/project mirrors are distribution surfaces, not extra sources of truth. Determine which version actually governed this session before blaming current source. Inspect routing guidance rather than assuming research automatically selected implementation-level machinery.

## Questions to answer with evidence

1. Reconstruct the critical path from the user's request to actual delivery or the latest checkpoint. Count research, synthesis, review, fix, verification, assembly and bookkeeping work separately. Identify useful work versus repeated checking of unchanged evidence.
2. Explain the multiplication of task-encoded reviews, executor phase-boundary reviews, final-document lenses, fidelity/anti-omission reviews and post-completion validation. Are their criteria actually independent? Does composing individually capped gates leave total review work effectively unbounded? Do not claim an infinite single fix loop if the record shows many finite gates.
3. Trace why a decision-only investigation produced a 122-item task. Separate routing choice, skill requirements, generated-task additions, executor requirements and discretionary parent choices. Identify the first point where a smaller complete process could have been selected lawfully.
4. Diagnose the agent write restriction. Definitions advertised write tools but running agents reported a higher-priority no-write rule. Locate the actual source if retained; otherwise mark it unresolved. The user approved inline findings with parent persistence. Do not propose swapping agents or bypassing permissions as the fix.
5. Evaluate duplicated complete JSON returns and separately authored compressed Markdown indexes. The parent acknowledged joining ordinary words and adding avoidable work. Measure repeated bytes/lines and review-size amplification where possible. Could one canonical readable artifact plus immutable evidence replace parallel authored representations? Would parent-owned deterministic serialization be safe and sufficient?
6. Check partitioning: reviewers had assigned output subsets yet often consumed all twelve complete research pairs and selected primary sources. Separate necessary trace work from overlapping blanket “verify every claim exhaustively” obligations. Evaluate finding quotas, arbitrary minimum agent floors, recursive review of review artifacts and line/file-count scaling.
7. Trace historical-search expansion, the user-approved current-source narrowing and repeated treatment of superseded originals. Were controlling corrections and scope decisions propagated once, or rediscovered by each reviewer? Do not reopen the excluded historical audit.
8. Classify actual corrections by value. Guard-scope and external-statistic corrections were substantive; missing bookkeeping and formatting need separate analysis. Did wording-only findings ever trigger blocking machinery contrary to the stated severity rule? Verify, do not assume. Distinguish a source defect from an unmet adoption prerequisite and from an incomplete research deliverable.
9. Examine resume behavior, repeated freshness reads, per-item checkbox edits, required header stubs, manual evidence extraction and context handoffs. Include the continuation after the user requested efficiency, not just early mistakes. Identify premature “all returned PASS” summaries versus on-disk accepted reports. Evaluate whether proceed/stop rules prevented responding efficiently to the user's changed priority.
10. Check branch and staging hygiene. The research was accumulated on an existing documentation branch with unrelated commits and other untracked work. No literal Git lock was established as the delay's cause. Identify what actually happened before any recommendation about isolation or publishing.
11. Examine environmental drift during long-running research. The later boundary reviews found the installed Orca build/default had changed and an old hashed bundle disappeared. Read the actual evidence/correction and distinguish a valid new defect from an originally false observation. Would an explicit versioned input snapshot and targeted freshness refresh prevent repeated whole-investigation checks? Do not propose freezing or downgrading the user's installation, silently treating old observations as current, or dropping factual validation.

## Quantification and uncertainty

Use observed timestamps, tool calls, agent counts, output sizes and meaningful correction counts. Separate active execution from the long user pauses. Do not translate aggregate input/cached/subagent token counters into billed cost without the necessary usage semantics and pricing evidence. Report unknown costs honestly. Show your counting method, exclusions and uncertainty; do not spend more reproducing a precise total than the decision needs.

## Deliverables and stopping rule

Produce one concise retrospective with:

- A short timeline and the causal chain from instructions to behavior to overhead.
- Verified root causes, contributing conditions and symptoms separately, each with exact source/transcript evidence and confidence.
- A compact table of useful review findings versus redundant or presentation-only work.
- Ranked proposed changes: exact canonical skill/agent/hook or mechanism affected, smallest behavioral change, failure prevented, safety retained, and one concrete regression/evaluation case per proposal.
- A proposed bounded research process: one declared review owner per criterion, a total work/review budget, reuse of unchanged verified evidence, targeted rechecking of changed claims, explicit finish/stop conditions and truthful unresolved findings. Treat these as candidates, not preselected answers.
- The first minimal change worth implementing, any independent follow-ups, and what should deliberately remain unchanged.

Do not solve process bloat by adding another mandatory panel, generic coordinator layer, nested task package or large policy document. Consider deletion and consolidation first, but justify every change against the evidence. Retain validation of decision-driving claims, human authority, permission boundaries, artifact preservation and blocking-defect handling.

Stop at the retrospective and proposed changes. Do not modify the framework or launch implementation. If a required safety check conflicts with the proposed efficiency improvement, explain the conflict rather than silently waiving the check.

## Repository constraints

Use UV for Python operations. Do not expose tokens, profiles or private transcript contents to external services. GitHub interactions, if needed and authorized, must explicitly target IronbellyOrg/IronClaude, never the upstream project. Do not stage generated `.claude/` mirrors. Preserve all original research and review evidence. Follow current task-folder staging rules without treating staging as permission to commit.
