# Qualitative Scoring, Pass 2 (reverse order: V5, V4, V3, V2, V1)

## Metadata
- Step: 3 (hybrid scoring, qualitative layer) of `/sc:adversarial`, git-ownership debate.
- Evaluator: independent (not an advocate). `scoring-pass-1.md` was not read.
- Date: 2026-11-02.
- Order: within each criterion, variants are scored V5 (E), V4 (D), V3 (C), V2 (B), V1 (A).
- Inputs scored: `variant-5-original.md` to `variant-1-original.md`, as written. Short form below: `V5:17` = line 17 of `variant-5-original.md`.
- Correctness evidence used: `diff-analysis.md`, `debate-transcript.md` (Rounds 1-2, scoring matrix, orchestrator verification), `invariant-probe.md`, and the advocate concession lists in `round1-advocate-*.md` / `round2-advocate-*.md`.
- Method: Claim-Evidence-Verdict, binary, no partial credit. MET needs a quoted line or named section. If no evidence was found, the searched sections are listed.

## Reading rules applied to every variant
- **Requirements R1-R7** (Completeness 1): R1 parallel correctness (index lock, shared worktree, HEAD during retries); R2 safety, authorization and audit trail; R3 recovery when a worker **or** the git owner crashes; R4 coordinator context load; R5 PR-rule fit; R6 day-to-day use; R7 implementation cost. All seven must be present.
- **Factual errors** (Correctness 1): a claim the debate showed false or overbroad counts against the variant. "Workers never run mutating git" was shown false in `round2-advocate-a.md:60` (N3: `/sc:implement` workers write refs and restore files), so it counts against every variant that states it, not only V1.
- **Collection boundaries** (Invariant 1): MET needs the empty case (no grant, no contract, nothing to commit) plus at least one of single or maximum. Every variant states the single-writer case, so that alone does not discriminate.
- **Probability and impact** (Risk 1): needs both stated for at least 3 risks. A weaknesses list without likelihood does not qualify.

## Dimension 1: Completeness

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1. Covers R1-R7 | V5 | R1-R7 covered | Sections "Correctness under parallel workers" (index lock, HEAD, shared refs, V5:16-20), "Safety and authorization" with "Audit trail" (V5:22-25), "Recovery" for worker and coordinator crash (V5:27-29), "Context load" (V5:31-32), "Fit with repo PR rules" (V5:34-35), "How a person works day to day" (V5:37-38), "Implementation cost" (V5:40-41) | MET (1) |
| 1. Covers R1-R7 | V4 | R3 not fully covered | "Recovery" covers only the subagent crash and the coordinator crash: "A subagent crash returns an error to the coordinator ... A coordinator crash kills the subagent too" (V4:26). No evidence found for a worker crash; searched Proposal, What D buys, What D costs, Correctness, Recovery. Safety has no section of its own (folded into What D costs, V4:18-19) | NOT MET (0) |
| 1. Covers R1-R7 | V3 | R1-R7 covered | Correctness (V3:21-22) plus Staying in sync (HEAD, V3:17-19); Safety with "The audit trail is the clearest" (V3:24-27); Recovery for git session and worker crash (V3:32-34); Context load (V3:36-37); Fit (V3:39-40); Day to day (V3:42-43); Cost (V3:45-46) | MET (1) |
| 1. Covers R1-R7 | V2 | R1-R7 covered | Correctness incl. shared-worktree limit and HEAD (V2:10-15); Safety with "Audit trail" (V2:17-22); Recovery (V2:24-26; the worker is the git owner here); Context load (V2:28-29); Fit (V2:31-32); Day to day (V2:34-35); Cost (V2:37-38) | MET (1) |
| 1. Covers R1-R7 | V1 | R1-R7 covered | Correctness (V1:10-14); Safety with "Audit trail" (V1:16-21); Recovery for worker and coordinator crash (V1:23-25); Context load (V1:27-28); Fit (V1:30-31); Day to day (V1:33-34); Cost (V1:36-37) | MET (1) |
| 2. Edge cases and failure scenarios | V5 | Met | "Worker crash mid-commit: a stale lock affects only its own worktree" (V5:28); "two implement runs in two worktrees must use different slugs ... UNVERIFIED for two runs of the same plan" (V5:19); "never inside a parallel batch" (V5:13) | MET (1) |
| 2. Edge cases and failure scenarios | V4 | Met | "Two git subagents in one worktree hit `index.lock`" (V4:20); "the subagent's report returns in the same confident register whether right or wrong" (V4:18); subagent crash (V4:26) | MET (1) |
| 2. Edge cases and failure scenarios | V3 | Met | "A failed `worker-start` still owns its terminal and must be released" (V3:33); without retention "C degrades to 'a fresh git worker per action'" (V3:50); loop Task rejected (V3:14) | MET (1) |
| 2. Edge cases and failure scenarios | V2 | Met | "a `git add -A` sweeps the other worker's files, and any commit moves the shared HEAD" (V2:14); "a parallel batch never gets a retry ladder" (V2:15); stale lock after crash (V2:25) | MET (1) |
| 2. Edge cases and failure scenarios | V1 | Met | "A worker that ran `git add -A` would commit other workers' half-written files" (V1:12); "Coordinator crash mid-commit: a stale `index.lock` may remain" (V1:25) | MET (1) |
| 3. Dependencies and prerequisites | V5 | Met | Worker commit needs "(1) the brief quotes the user's instruction ... (2) the worker is the only writer ... (3) ... only between tasks" (V5:13); "the per-task commit step inside `/sc:implement` stays #326's feature (K3 ...), and until it exists a worker commits only through steps its brief adds" (V5:41) | MET (1) |
| 3. Dependencies and prerequisites | V4 | Met | "Low: one agent definition (or a prompt template) for 'commit these paths', plus the A wording in the spec" (V4:38); frontmatter tool restriction named as the mechanism (V4:12) | MET (1) |
| 3. Dependencies and prerequisites | V3 | Met | "C needs the user to request retention once at run start" (V3:13); "pr-submit there is D3 (b) and needs the section 3 pr-submit row" (V3:25); "until #326 delivers an unattended `/sc:git`" (V3:27) | MET (1) |
| 3. Dependencies and prerequisites | V2 | Met | "implement-side commits are a deliberate protocol change (#326 K3 ...)" (V2:19); "Pushes and PRs from workers need D3 (b) and the section 3 pr-submit row" (V2:21); "the coordinator needs a worktree-per-worker placement rule and a merge step" (V2:38) | MET (1) |
| 3. Dependencies and prerequisites | V1 | Met | "per-task commits wait for #326's own protocol change (`EVAL:63`, K3)" (V1:14); actions happen "each only when the user's own instruction names that action" (V1:8) | MET (1) |
| 4. Success / completion criteria | V5 | Not met | No evidence found. Searched The proposal, Correctness, Safety, Recovery, Day to day, Cost. Contract SHAs (V5:13) are a record, not a definition of done for the design | NOT MET (0) |
| 4. Success / completion criteria | V4 | Not met | No evidence found. Searched Proposal ("report the SHA", V4:8, is a subagent output, not a success criterion), What D buys, What D costs, Recovery, Cost | NOT MET (0) |
| 4. Success / completion criteria | V3 | Not met | No evidence found. Searched Proposal, Orca mechanics, Correctness, Safety, Cost. "a contract shape for git results (SHAs, branch, PR URL)" (V3:46) is an output shape, not a criterion | NOT MET (0) |
| 4. Success / completion criteria | V2 | Not met | No evidence found. Searched Proposal, Correctness, Safety, Recovery, Day to day, Cost | NOT MET (0) |
| 4. Success / completion criteria | V1 | Not met | No evidence found. Searched Proposal, Correctness, Safety, Day to day ("shows the commit and PR link", V1:34, describes the flow), Self-check (verifies a git fact, not the design) | NOT MET (0) |
| 5. Explicit out of scope | V5 | Met | "Commands: none in this spec's phases; the per-task commit step inside `/sc:implement` stays #326's feature" (V5:41) | MET (1) |
| 5. Explicit out of scope | V4 | Met | "D covers local commits and branch work only; outward actions fall back to A" (V4:17) | MET (1) |
| 5. Explicit out of scope | V3 | Met | "The git session runs plain git and `/sc:pr-submit` until #326 delivers an unattended `/sc:git`" (V3:27); "A single never-ending Task is not an option" (V3:14) | MET (1) |
| 5. Explicit out of scope | V2 | Not met | No evidence found. Searched Proposal (allows commit, push and PR, V2:8), Correctness, Safety, Cost, Weaknesses. B names gaps ("Merges still need a single owner", V2:44) but declares nothing out of scope | NOT MET (0) |
| 5. Explicit out of scope | V1 | Met | "Under A, per-task commits wait for #326's own protocol change" (V1:14); "No command changes" (V1:37) | MET (1) |

## Dimension 2: Correctness

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1. No factual errors | V5 | Not met | Two overclaims. (a) "the retry Task (WC-6) checks for it first" (V5:28): E's own advocate conceded "no command has that step today" (`round1-advocate-e.md:63`, concession 3). (b) "linked worktrees have separate index files ... so no two git writers share a lock" (V5:17): refs and `packed-refs` live in the common directory, so ref locks are shared (`invariant-probe.md:13`, INV-005) | NOT MET (0) |
| 1. No factual errors | V4 | Not met | "Workers never run mutating git" (V4:8) is the claim shown inaccurate in `round2-advocate-a.md:60` (N3). The narrow-tool claim (V4:12) lists `Bash, Read` as a restriction while Bash stays unrestricted (X-005, `diff-analysis.md:48`; D conceded, `round2-advocate-d.md:20`). The permission-prompt claim (V4:18) "was too broad" (`round1-advocate-d.md:53`, D concession 3) | NOT MET (0) |
| 1. No factual errors | V3 | Not met | "Other workers never run mutating git" (V3:8): inaccurate for `/sc:implement` workers (N3, `round2-advocate-a.md:60`). V3 also omits that C conflicts with `SPEC:156` ("workers make no commits or pushes"), which its own advocate conceded (`debate-transcript.md:332`) | NOT MET (0) |
| 1. No factual errors | V2 | Met | No debate-verified false claim found. Checked V2 against B's concessions (`round1-advocate-b.md:58-63`): they concede design weaknesses and one omission (shared refs, concession 5), not a false statement. V2's index/HEAD separation claim (V2:11) matches GITDEMO; its stale-lock step is correctly called absent ("a step no command has today", V2:25) | MET (1) |
| 1. No factual errors | V1 | Not met | "Workers never run a mutating git command" (V1:8) is inaccurate: `/sc:implement` writes refs and restores files (`round2-advocate-a.md:60`, N3, conceded by A's own advocate) | NOT MET (0) |
| 2. Feasible under stated constraints | V5 | Met | Outward actions stay where the spec already puts them ("matching D3 (a) (`SPEC:341`)", V5:23); the worker row is conditional and its K3 dependency is stated (V5:41). All five advocates accepted E's table as the merge form (`debate-transcript.md:1291`) | MET (1) |
| 2. Feasible under stated constraints | V4 | Met | Scope is limited to what is feasible: "D covers local commits and branch work only; outward actions fall back to A" (V4:17), respecting pr-submit's top-level rule (V4:17) | MET (1) |
| 2. Feasible under stated constraints | V3 | Not met | V3 "conflicts with the spec's D3 recommendation (a) (`SPEC:341`)" (V3:40); retention needs a user request (V3:13); how reuse injects the next Task is "UNVERIFIED" (V3:37). Its core mechanism is unproven and conflicts with the current spec | NOT MET (0) |
| 2. Feasible under stated constraints | V2 | Not met | "All of it is new behaviour in commands, against the spec's additive-edits rule for P1-P3 (`SPEC:172`)" (V2:38); "Unsafe in the default shared worktree" (V2:41) | NOT MET (0) |
| 2. Feasible under stated constraints | V1 | Met | "No command changes: WC-9 already turns every outward default off in workers (`SPEC:73`)" (V1:37); matches spec D3 (V1:20) | MET (1) |
| 3. Terminology consistent | V5 | Met | "coordinator", "worker", "only writer", "quiescent point" used the same way in the table (V5:12-14) and Correctness (V5:17-18) | MET (1) |
| 3. Terminology consistent | V4 | Met | "subagent", "coordinator's main chat", "Agent-tool subagent" used consistently (V4:8, 17, 29) | MET (1) |
| 3. Terminology consistent | V3 | Met | "git session", "Task", "Dispatch", "retention" used consistently (V3:8-15, 33) | MET (1) |
| 3. Terminology consistent | V2 | Met | "committing worker", "one worker per worktree", "brief" used consistently (V2:11-14, 18) | MET (1) |
| 3. Terminology consistent | V1 | Met | "coordinator", "settled contracts", "explicit paths" used consistently (V1:8, 12, 24) | MET (1) |
| 4. No internal contradictions | V5 | Met | Table rows reconcile: row 1 (merge into a shared branch) is bounded by row 5, "Anything mutating git in a worktree shared with other running workers: Nobody but the coordinator at a quiescent point" (V5:14). No contradiction found across Proposal, Correctness, Safety, Recovery | MET (1) |
| 4. No internal contradictions | V4 | Not met | Claims "A narrow tool list" as a benefit, then "Whether the frontmatter can restrict Bash to git subcommands only is UNVERIFIED" (V4:12); the diff analysis classes this as an intra-variant contradiction (X-005, `diff-analysis.md:48`) | NOT MET (0) |
| 4. No internal contradictions | V3 | Met | Spec conflicts are stated as conflicts (V3:40, 51) and retention degradation is acknowledged (V3:50). No contradiction found | MET (1) |
| 4. No internal contradictions | V2 | Met | "The coordinator only plans, reads contracts and merges results" (V2:8) agrees with "B still needs A for merges" (V2:29). No contradiction found | MET (1) |
| 4. No internal contradictions | V1 | Met | The honest limit (V1:14) and weakness 3 (V1:42) are concessions, not contradictions. No contradiction found | MET (1) |
| 5. Claims supported | V5 | Met | Claims carry citations: `SKILL.md:114`, `refs/retry.md:41`, `SKILL.md:97`, `SKILL.md:113` (V5:18-19); `CLAUDE.md:37`, `HWW:282` (V5:24) | MET (1) |
| 5. Claims supported | V4 | Met | `src/superclaude/agents/reflect-reviewer.md:5` (V4:12); `SKILL.md:47-49,82-84` (V4:17); AGENT-TOOL key defined (V4:5) | MET (1) |
| 5. Claims supported | V3 | Met | `[G:cl] 46-55`, `[G:rc] 108`, `[G:rc] 157`, `[G] 80-82,91-93` (V3:11-14) | MET (1) |
| 5. Claims supported | V2 | Met | GITDEMO and issue #326 owner comment (V2:11); `retry.md:41`, `SKILL.md:114` (V2:12); `managed-workspace.md:63,67` (V2:19) | MET (1) |
| 5. Claims supported | V1 | Met | GITDEMO with a Self-check procedure (V1:11, 45-46); `retry.md:41,44` (V1:13); `CLAUDE.md:37,50`, `HWW:282` (V1:17) | MET (1) |

## Dimension 3: Structure

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1. Logical ordering | V5 | Met | Proposal table, then Correctness, Safety, Recovery, Context load, Fit, Day to day, Cost, Weaknesses (V5:7-47) | MET (1) |
| 1. Logical ordering | V4 | Met | Proposal, What D buys, What D costs, Correctness, Recovery, Context load, Fit, Day to day, Cost, Weaknesses (V4:7-43) | MET (1) |
| 1. Logical ordering | V3 | Met | Proposal, Orca mechanics, Staying in sync, Correctness, Safety, Relation to #326, Recovery, Context, Fit, Day to day, Cost, Weaknesses (V3:7-52) | MET (1) |
| 1. Logical ordering | V2 | Met | Proposal, Correctness, Safety, Recovery, Context, Fit, Day to day, Cost, Weaknesses (V2:7-44) | MET (1) |
| 1. Logical ordering | V1 | Met | Proposal, Correctness, Safety, Recovery, Context, Fit, Day to day, Cost, Weaknesses, Self-check (V1:7-46) | MET (1) |
| 2. Consistent hierarchy | V5 | Met | One H1, `##` sections, bold-led bullets inside (V5:16-20) | MET (1) |
| 2. Consistent hierarchy | V4 | Met | One H1, `##` sections, bold-led bullets in buys/costs (V4:10-20) | MET (1) |
| 2. Consistent hierarchy | V3 | Met | One H1, `##` sections, bold-led bullets (V3:10-19) | MET (1) |
| 2. Consistent hierarchy | V2 | Met | One H1, `##` sections, bold-led bullets (V2:10-15) | MET (1) |
| 2. Consistent hierarchy | V1 | Met | One H1, `##` sections, bold-led bullets (V1:10-14, 23-25) | MET (1) |
| 3. Separation of concerns | V5 | Met | Each requirement has its own section; ownership rules isolated in the table (V5:7-14) | MET (1) |
| 3. Separation of concerns | V4 | Not met | "What D costs" (V4:16-20) mixes PR-rule fit (top-level-only commands), authorization (one more hop), audit (no Orca record) and parallel correctness (subagents collide). Safety has no section of its own | NOT MET (0) |
| 3. Separation of concerns | V3 | Met | Orca mechanics (V3:10-15), sync (V3:17-19) and safety (V3:24-27) are separate sections | MET (1) |
| 3. Separation of concerns | V2 | Met | One section per concern (V2:10-38) | MET (1) |
| 3. Separation of concerns | V1 | Met | One section per concern plus a separate evidence appendix (V1:10-46) | MET (1) |
| 4. Navigation aids | V5 | Met | "Citation keys: as in `option-a.md` (`SPEC`, `CAPS`, ...)" (V5:5); cross-refs to D4, F3, WC-9 (V5:10-11, 23) | MET (1) |
| 4. Navigation aids | V4 | Met | Citation keys plus a new `AGENT-TOOL` key defined (V4:5) | MET (1) |
| 4. Navigation aids | V3 | Met | Citation keys (V3:5); `[G:cl]`, `[G:rc]` line refs throughout (V3:11-14) | MET (1) |
| 4. Navigation aids | V2 | Met | Citation keys (V2:5); `EVAL:52`, F2 cross-refs (V2:11) | MET (1) |
| 4. Navigation aids | V1 | Met | Full citation-key definitions (V1:5) and a Self-check appendix (V1:45-46) | MET (1) |
| 5. Position-paper conventions (brief's topics as sections) | V5 | Met | Sections for parallel correctness, safety and authorization, recovery, context load, PR-rule fit, day to day, implementation cost, weaknesses (V5:16-47) | MET (1) |
| 5. Position-paper conventions | V4 | Not met | No "Safety and authorization" section; searched all `##` headings (V4:7-40). Authorization appears only as a bullet under "What D costs" (V4:18) | NOT MET (0) |
| 5. Position-paper conventions | V3 | Met | All brief topics are headings (V3:21, 24, 32, 36, 39, 42, 45, 48) | MET (1) |
| 5. Position-paper conventions | V2 | Met | All brief topics are headings (V2:10, 17, 24, 28, 31, 34, 37, 40) | MET (1) |
| 5. Position-paper conventions | V1 | Met | All brief topics are headings (V1:10, 16, 23, 27, 30, 33, 36, 39) | MET (1) |

## Dimension 4: Clarity

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1. Unambiguous language | V5 | Met | Each row states owner and condition; "quiescent point" is defined in place: "no worker running in that worktree" (V5:12) | MET (1) |
| 1. Unambiguous language | V4 | Met | Role stated literally: "stage these exact paths and commit with a conventional message; report the SHA" (V4:8) | MET (1) |
| 1. Unambiguous language | V3 | Met | Example Tasks stated literally: "stage these paths, commit with this message", "push branch X" (V3:8) | MET (1) |
| 1. Unambiguous language | V2 | Met | Allowed actions enumerated: "local commit only; or commit plus push; or a PR through `/sc:pr-submit` under D3 (b)" (V2:8) | MET (1) |
| 1. Unambiguous language | V1 | Met | "Workers never run a mutating git command ... The coordinator ... stages explicit paths, commits, ..." (V1:8) | MET (1) |
| 2. Concrete | V5 | Met | Example instruction: "run the plan in its own worktree, commit after each task, and open a PR when it passes" (V5:38) | MET (1) |
| 2. Concrete | V4 | Met | Concrete frontmatter example: "A git agent could list only `Bash, Read`" (V4:12) | MET (1) |
| 2. Concrete | V3 | Met | Exact verbs: "`worker-show --dispatch <id>` then `worker-start --task <next_task_id> --terminal <agent_terminal_handle>`" (V3:11) | MET (1) |
| 2. Concrete | V2 | Met | Exact paths: "`.git/worktrees/<name>/index` and `.../HEAD`" (V2:11) | MET (1) |
| 2. Concrete | V1 | Met | Exact git error text quoted (V1:11) and the GITDEMO procedure (V1:46) | MET (1) |
| 3. Each section has a clear purpose | V5 | Met | Section headings match their content; no off-topic section found (V5:16-47) | MET (1) |
| 3. Each section has a clear purpose | V4 | Met | "What D buys" and "What D costs" each state a single purpose (V4:10, 16) | MET (1) |
| 3. Each section has a clear purpose | V3 | Met | "How Orca can keep it alive (verified mechanics)" and "Relation to #326's central relay" have stated purposes (V3:10, 29) | MET (1) |
| 3. Each section has a clear purpose | V2 | Met | Headings match content (V2:10-44) | MET (1) |
| 3. Each section has a clear purpose | V1 | Met | Headings match content; Self-check states what was run (V1:45-46) | MET (1) |
| 4. Terms and acronyms defined on first use | V5 | Not met | WC-9, WC-11, WC-6, D3 (a), D4 (a), K3, F3 used undefined (V5:10-11, 23, 28, 41); citation keys deferred to `option-a.md` (V5:5) | NOT MET (0) |
| 4. Terms and acronyms defined on first use | V4 | Not met | `AGENT-TOOL` is defined (V4:5), but "Task or Dispatch" (V4:19), "quiescent points" (V4:14) and "the A wording" (V4:38) are used undefined; other citation keys deferred to `option-a.md` (V4:5) | NOT MET (0) |
| 4. Terms and acronyms defined on first use | V3 | Not met | Dispatch, D3 (b), D4 (a), SA-2, WC-8, WC-6 used undefined (V3:11, 25-26, 30, 33); keys deferred to `option-a.md` (V3:5) | NOT MET (0) |
| 4. Terms and acronyms defined on first use | V2 | Not met | D3 (b), D4 (a), WC-11, F2, K3, WC-6 used undefined (V2:8, 11, 19, 25); keys deferred to `option-a.md` (V2:5) | NOT MET (0) |
| 4. Terms and acronyms defined on first use | V1 | Not met | Citation keys are defined (V1:5), but WC-9, D3, D4, K3 and `worker_done` are used undefined (V1:14, 20, 37) | NOT MET (0) |
| 5. Actionable next steps / decision points | V5 | Met | "Spec: wording in WC-9, WC-11, section 2.3, the `/sc:git` row and D4 (this file's table)" (V5:41) | MET (1) |
| 5. Actionable next steps / decision points | V4 | Met | "one agent definition (or a prompt template) for 'commit these paths', plus the A wording in the spec" (V4:38) | MET (1) |
| 5. Actionable next steps / decision points | V3 | Met | "a git-action brief template, a contract shape for git results ..., a retention step, quiescence rules, and pr-submit's P4 changes" (V3:46) | MET (1) |
| 5. Actionable next steps / decision points | V2 | Met | "Every committing command needs a commit step, a stale-lock rule and a contract field for SHAs; implement needs K3; the coordinator needs a worktree-per-worker placement rule" (V2:38) | MET (1) |
| 5. Actionable next steps / decision points | V1 | Met | "The spec needs only wording in section 2.3 (coordinator duties) and the `/sc:git` row" (V1:37) | MET (1) |

## Dimension 5: Risk Coverage

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1. At least 3 risks with probability and impact | V5 | Not met | Three risks listed (V5:44-46) with no likelihood or impact stated. No evidence found in Weaknesses, Correctness, Recovery | NOT MET (0) |
| 1. At least 3 risks with probability and impact | V4 | Not met | Three weaknesses (V4:41-43) and four costs (V4:17-20), none with likelihood. Searched both sections | NOT MET (0) |
| 1. At least 3 risks with probability and impact | V3 | Not met | Four weaknesses (V3:49-52), no likelihood. Searched Weaknesses, Recovery | NOT MET (0) |
| 1. At least 3 risks with probability and impact | V2 | Not met | Four weaknesses (V2:41-44), no likelihood. Searched Weaknesses, Correctness | NOT MET (0) |
| 1. At least 3 risks with probability and impact | V1 | Not met | Four weaknesses (V1:40-43), no likelihood. Searched Weaknesses, Context load | NOT MET (0) |
| 2. Mitigation for each identified risk | V5 | Not met | Weaknesses 1-3 (V5:44-46) have no mitigation. Weakness 2 states only that "the coordinator's later review catches it" | NOT MET (0) |
| 2. Mitigation for each identified risk | V4 | Not met | Collision has one ("the coordinator must run them one at a time", V4:20); weaknesses 1-3 (V4:41-43) have none | NOT MET (0) |
| 2. Mitigation for each identified risk | V3 | Not met | Weaknesses 1-4 (V3:49-52) have no mitigation | NOT MET (0) |
| 2. Mitigation for each identified risk | V2 | Not met | Shared-worktree risk mitigated ("B forces a worktree per committing worker", V2:14); weaknesses 2-4 (V2:42-44) have none | NOT MET (0) |
| 2. Mitigation for each identified risk | V1 | Not met | Context load has "Mitigation: messages queue durably" (V1:28); weaknesses 1, 3 and 4 (V1:40-43) have none | NOT MET (0) |
| 3. Failure modes and recovery procedures | V5 | Met | "Recovery": stale lock confined to its worktree, retry Task, earlier commits survive; coordinator crash as A (V5:27-29) | MET (1) |
| 3. Failure modes and recovery procedures | V4 | Met | "A subagent crash returns an error to the coordinator, which inspects `git status` itself" (V4:26) | MET (1) |
| 3. Failure modes and recovery procedures | V3 | Met | "clears a stale lock only after proving no git process runs, and re-issues the action as a new Task (WC-6 ...)" (V3:33) | MET (1) |
| 3. Failure modes and recovery procedures | V2 | Met | "The retry is a new Task (WC-6 ...) in the same worktree, which must first clear the stale lock" (V2:25) | MET (1) |
| 3. Failure modes and recovery procedures | V1 | Met | "inspects with `git status` and removes the stale lock only after proving no git process runs" (V1:25) | MET (1) |
| 4. External dependencies and their failure scenarios | V5 | Met | Dependency on #326 K3, with the fallback when it is absent: "until it exists a worker commits only through steps its brief adds after the command finishes" (V5:41) | MET (1) |
| 4. External dependencies and their failure scenarios | V4 | Met | Claude Code Agent tool: tool restriction "UNVERIFIED" (V4:12); subagent report "returns in the same confident register whether right or wrong"; permission mode inherited (V4:18) | MET (1) |
| 4. External dependencies and their failure scenarios | V3 | Met | Orca retention: "without it the session is released after each action and C degrades" (V3:50); "A failed `worker-start` still owns its terminal" (V3:33); readiness start 60 s (V3:49) | MET (1) |
| 4. External dependencies and their failure scenarios | V2 | Met | `/sc:git` has "no unattended mode", so "Workers would run plain `git`" (V2:20); K3 needed before implement commits (V2:19) | MET (1) |
| 4. External dependencies and their failure scenarios | V1 | Met | Orca message durability during pr-submit waits: "messages queue durably ... `check` replays the oldest delivery until acknowledged" (V1:28); Run state durable in Orca after a crash (V1:25) | MET (1) |
| 5. Monitoring / validation mechanism | V5 | Met | "worker commits are listed by SHA in contracts" (V5:25); wrong paths are caught by "the coordinator's later review" (V5:45) | MET (1) |
| 5. Monitoring / validation mechanism | V4 | Met | On error, the coordinator "inspects `git status` itself" (V4:26); the subagent reports the SHA (V4:8) | MET (1) |
| 5. Monitoring / validation mechanism | V3 | Met | "Orca reports liveness (`CAPS:122-126`)" (V3:33); one `worker_done` and contract per action (V3:26) | MET (1) |
| 5. Monitoring / validation mechanism | V2 | Not met | No detection step found. The SHA in the contract (V2:22) is a record nobody is said to check; the stale-lock check is stated as missing ("a step no command has today", V2:25). Searched Correctness, Safety, Recovery, Context load | NOT MET (0) |
| 5. Monitoring / validation mechanism | V1 | Met | The coordinator stages "only the paths named in settled contracts" (V1:12) and inspects with `git status` after a crash (V1:25); claims validated by the GITDEMO Self-check (V1:46) | MET (1) |

## Dimension 6: Invariant & Edge Case Coverage

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1. Collection boundaries (empty, single, maximum) | V5 | Met | Empty grant: "Without that instruction nothing is committed" (V5:38); single: "the worker is the only writer in its worktree" (V5:13) | MET (1) |
| 1. Collection boundaries | V4 | Not met | Single and two-writer cases only ("one subagent at a time", V4:14; "Two git subagents ... hit `index.lock`", V4:20). No empty case found; searched Proposal, buys, costs, Correctness, Recovery | NOT MET (0) |
| 1. Collection boundaries | V3 | Not met | Maximum one active Dispatch per terminal (V3:12). No empty case (no action, nothing to commit, no contract); searched Proposal, mechanics, sync, Correctness, Recovery | NOT MET (0) |
| 1. Collection boundaries | V2 | Not met | Single committing worker per worktree (V2:14). No empty case; searched Proposal, Correctness, Safety, Recovery | NOT MET (0) |
| 1. Collection boundaries | V1 | Met | Empty: the coordinator "decides from the contract (or its absence, `SPEC:69`) whether to stage them" (V1:24); single: "only one session ever takes that lock in a given worktree" (V1:11) | MET (1) |
| 2. State interactions across component boundaries | V5 | Met | "refs are shared across linked worktrees ... two implement runs in two worktrees must use different slugs" (V5:19); separate HEAD per worktree versus implement's ladder (V5:18) | MET (1) |
| 2. State interactions across component boundaries | V4 | Met | Subagent commits against the coordinator's worktree, "never while an `/sc:implement` worker runs in the same worktree (`retry.md:41,44`)" (V4:23) | MET (1) |
| 2. State interactions across component boundaries | V3 | Met | "a commit moves HEAD and halts that worker's retry ladder" (V3:18); per-worktree index and HEAD via `git -C` (V3:19) | MET (1) |
| 2. State interactions across component boundaries | V2 | Met | "any commit moves the shared HEAD, which halts every running `/sc:implement` task in that worktree with `head-moved`" (V2:14) | MET (1) |
| 2. State interactions across component boundaries | V1 | Met | "the only thing that can move HEAD is the coordinator ... never commit in a worktree while an `/sc:implement` worker in that worktree is running" (V1:13) | MET (1) |
| 3. Guard condition gaps | V5 | Met | Slug guard gap: "UNVERIFIED for two runs of the same plan in two worktrees" (V5:19); raw-git gap: "A worker running raw git can still make a mistake inside its own worktree" (V5:45) | MET (1) |
| 3. Guard condition gaps | V4 | Met | "Whether the frontmatter can restrict Bash to git subcommands only is UNVERIFIED" (V4:12) | MET (1) |
| 3. Guard condition gaps | V3 | Met | Retention guard: allowed "only when the user explicitly wants the settled terminal kept live" (V3:13), with the degraded case (V3:50); final release "UNVERIFIED" (V3:13) | MET (1) |
| 3. Guard condition gaps | V2 | Met | Implement's guard: acceptance never "authorizes commit, PR, merge or release" (V2:19); missing stale-lock guard (V2:25) | MET (1) |
| 3. Guard condition gaps | V1 | Met | Orca's ownership guard: a coordinator that stages and prepares PRs "is doing owner work unless the user's plan names it as owner" (V1:42) | MET (1) |
| 4. Count divergence (off-by-one, ranges) | V5 | Met | Task versus batch boundary: per-task commits "only between tasks and never inside a parallel batch" (V5:13); "a parallel batch has no ladder anyway" (V5:18) | MET (1) |
| 4. Count divergence | V4 | Not met | No evidence found. Searched Proposal, buys, costs, Correctness, Recovery, Context load. V4 never treats one run versus N tasks or any range | NOT MET (0) |
| 4. Count divergence | V3 | Met | One `worker_done` per run versus N tasks: "the coordinator still sees only the run's end" (V3:52); 600 s wait budget (V3:22) | MET (1) |
| 4. Count divergence | V2 | Met | "in-run commits must wait for a batch's last `complete` line too" (V2:15); only the worker sees each task's end (V2:12) | MET (1) |
| 4. Count divergence | V1 | Met | "the coordinator learns only of the whole run's `worker_done` (`[G] 88-90`), not of each task inside it" (V1:14); "waits of up to 600 s per wait budget" (V1:28) | MET (1) |
| 5. Interaction effects when components combine | V5 | Met | Worker-commit lane plus coordinator lane plus implement ladder: "The coordinator never commits in a worktree while an implement worker runs there" (V5:18) | MET (1) |
| 5. Interaction effects when components combine | V4 | Met | pr-submit plus subagent: "Top-level-only commands cannot run there" (V4:17) | MET (1) |
| 5. Interaction effects when components combine | V3 | Met | pr-submit loop in the git session lets "the coordinator keep processing other workers' messages meanwhile" (V3:22) | MET (1) |
| 5. Interaction effects when components combine | V2 | Met | Shared worktree plus `git add -A` plus implement ladder (V2:14) | MET (1) |
| 5. Interaction effects when components combine | V1 | Met | pr-submit loop plus worker messages: "during which the coordinator does not react to other workers" (V1:28) | MET (1) |

## Summary: MET counts per dimension

| Dimension | V5 (E) | V4 (D) | V3 (C) | V2 (B) | V1 (A) |
|---|---|---|---|---|---|
| Completeness | 4 | 3 | 4 | 3 | 4 |
| Correctness | 4 | 3 | 3 | 4 | 4 |
| Structure | 5 | 3 | 5 | 5 | 5 |
| Clarity | 4 | 4 | 4 | 4 | 4 |
| Risk Coverage | 3 | 3 | 3 | 2 | 3 |
| Invariant & Edge Case Coverage | 5 | 3 | 4 | 4 | 5 |
| **Total /30** | **25** | **19** | **23** | **22** | **25** |

Criteria no variant met: Completeness 4 (success criteria), Clarity 4 (terms defined on first use), Risk 1 (probability and impact), Risk 2 (a mitigation for every risk).

## Edge-case floor check

| Variant | Invariant & Edge Case score | Floor (0/5 makes it ineligible as base) |
|---|---|---|
| V5 (E) | 5/5 | Eligible |
| V4 (D) | 3/5 | Eligible |
| V3 (C) | 4/5 | Eligible |
| V2 (B) | 4/5 | Eligible |
| V1 (A) | 5/5 | Eligible |

No variant is excluded by the floor. V5 and V1 tie on the qualitative layer (25/30). They differ in where they lose points. V5 loses on two factual overclaims (the retry step that no command has, and "no two git writers share a lock"). V1 loses on its "workers never run a mutating git command" claim. The tie should be settled by the quantitative layer and the debate scoring matrix, not by this pass.
