# Diff Analysis: Recommendation Position Comparison

## Metadata
- Generated: 2026-11-11T21:05:00Z
- Variants compared: 2 (Variant A = position-a-keep-subagents.md, Variant B = position-b-orca-orchestrator.md)
- Total differences found: 17 debate points (S 2, C 9, X 2, A 4) plus 6 unique contributions (not in the convergence denominator)
- Categories: structural (2), content (9), contradictions (2), unique (6), shared assumptions (4)
- Taxonomy tags (AD-5): L1 = S-001, S-002; L2 = C-001..C-004, C-007, A-001, A-003, A-004; L3 = C-005, C-006, C-008, C-009, X-001, X-002, A-002

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Presentation and evidence style (L1) | Claim, 6 numbered case points, closing section. Cites repo file:line in points 1, 2, 4 and 6 (for example `SKILL.md:1021-1028`, `:240`). | Same skeleton. Cites no repo file:line; leans on Orca CLI help and general argument. | Low |
| S-002 | Closing section (L1) | "What to do instead": concrete alternative actions, including two doc defects. | "Mitigation of known costs": answers to the costs A raises. | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Unit of work per proposer (L2) | One-shot Task, text in and text out (`max_turns: 5`); a full session is "far more machinery than the work needs". | A full worker session can search and research while writing, so S1 and S2 could merge. | Medium |
| C-002 | Blast radius of the change (L2) | S2-S5 live in the 2985-line shared adversarial skill used by roadmap, troubleshoot, reflect and spec-panel; brainstorm owns only S1. | Stage it: S2 only, behind `--runtime orca`, default stays Task; scoring, merge and contract untouched. | Medium |
| C-003 | Portability and dual paths (L2) | Installed primitives run in projects without Orca, so two dispatch paths must be maintained forever. | Probe `orca --version` and the Orca worktree, fall back to Task. | Medium |
| C-004 | Route to cross-family model diversity (L2) | Already available without Orca: `sc-bare-review` dispatches to external models through an OpenAI-compatible proxy. | Orca `--agent codex\|cursor\|opencode --model <id>` gives different model families. | High |
| C-005 | Token budget guard (L3) | Hard-kill at 1.25 x estimate and `token_usage.wave_3` depend on the Task usage report. | Accept coarser telemetry from transcript size or word count. | Medium |
| C-006 | Parent context and protocol state (L3) | Not addressed as a problem; results return inline. | Workers write files so the parent holds only paths, protecting state (domain, strategy, agent-spec) from compaction on deep runs. | Medium |
| C-007 | Observability, control and partial retry (L2) | Silent on benefits; names Orca operational risk (receipt is not proof of work). | Live view, `worker-stop`, `--retry-of`, steering one worker without killing the run. | Low |
| C-008 | Resumability (L3) | Silent. | A separate process survives a parent crash, so `--resume-from` could reattach to finished proposals. | Medium |
| C-009 | Completion checking and failure modes (L3) | Orca failure modes are known and real (`turn_started` receipt is not proof; resumes need screen checks). | Worker contract: prompt file in, one result file out, `worker_done`; verify the file on disk, never the signal alone. | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Can a failed Task agent be retried alone today? (L3) | Implied yes: Task returns results inline and failures are handled by the skill. | "S2 to S3 failures today can only be retried whole" (point 3). The skill text says otherwise: `failure_handling` retries the single failed advocate once, then proceeds with N-1 (`SKILL.md:1065-1072`), and the error matrix does the same for any agent failure. B's claim is false for S2 and S3. | Medium |
| X-002 | Does the staged plan deliver the stated context benefit? (L3) | Not addressed. | Point 2 promises the parent holds only paths, but point 6 stages S2 only. Debate transcripts, scoring and merge still run in the parent context because `Skill sc-adversarial-protocol` runs in-session; the S2 proposals are also read by the parent in diff analysis. B's benefit 2 does not follow from B's plan 6. | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|-----------------|
| U-001 | A | Found two real spec defects independent of this decision: SKILL.md token thresholds (500K/650K, 80K per proposal) disagree with `refs/agent-spec-builder.md` (250K/350K, 8K per proposal); the command file says "5-wave" and lists six steps. | Medium |
| U-002 | A | Names `sc-bare-review` as a no-Orca route to cross-family diversity. | High |
| U-003 | B | Staged rollout: S2 first, flag-gated, default unchanged. | Medium |
| U-004 | B | Worker contract: prompt file in, single result file out, verify on disk. | High |
| U-005 | B | Resume of finished proposals as a new capability. | Medium |
| U-006 | B | Merge enrichment into the proposer so each proposer researches for itself. | Low |

## Shared Assumptions

Scan of the verified repo text (not only the two variants) found four assumptions both variants rely on without stating:

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | The unit to spawn is the individual proposer or advocate. Neither considers spawning the whole of Wave 3 as ONE worker. `/sc:adversarial` already has `--unattended` plus `--report-dir` and writes `return-contract.yaml` on every outcome (adversarial command file, "Unattended mode"). | Both reason per agent (S2-S5). | UNSTATED | High | Promoted |
| A-002 | Context pressure comes from Task agents. In fact `Skill sc-adversarial-protocol` runs inside the calling session, so all debate, scoring and merge text passes through that context whatever replaces the Task calls. | Both discuss Task results and parent context only. | UNSTATED | High | Promoted |
| A-003 | Cost is measured in tokens and maintenance effort. Neither estimates wall-clock latency, worker start-up time or money for the Orca path. | Neither quantifies. | UNSTATED | Medium | Promoted |
| A-004 | The Orca spawning would live inside the brainstorm skill. The repo's own contract forbids that: `~/.claude/WORKER-CONTRACT.md` WC-8 ("A command never calls `worker-start`, `dispatch` or `task-create`"), WC-13 (the worker session never does either) and WC-7 (a command's own Agent-tool fan-out "stays as it is"). Orca fan-out belongs to a coordinator session the person opened; its fan-in rule even names "N workers, then `/sc:adversarial --compare`". The installed `~/.claude/commands/sc/brainstorm.md` already has an `## Unattended mode` section (7 matches); the `src/superclaude/commands/brainstorm.md` on this branch has none (0 matches), so the source copy here lags the installed one. Whether master has it is UNVERIFIED. | A: "every Orca path needs a Task fallback" and B's whole plan assume in-skill spawning. | CONTRADICTED | High | Promoted; flagged for debate |

## Summary
- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 2
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: C-004, A-001, A-002, A-004

Additional evidence note: `~/.claude/WORKER-CONTRACT.md` WC-10 records that a command's own Agent-tool fan-out can hold a worker session longer than the heartbeat cadence with no way to heartbeat; "that gap is accepted". `superclaude swarm run --lens bare-review` is an existing CLI fan-out engine (help text verified); that it supports a proposal-generation lens is UNVERIFIED.
