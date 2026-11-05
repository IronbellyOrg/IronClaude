# Scoring Pass 1: qualitative layer (input order)

- Step: 3 (hybrid scoring, qualitative layer), pass 1 of the /sc:adversarial git-ownership debate.
- Evaluator: independent, not an advocate. Date: 2026-11-02.
- Order: variants in input order 1, 2, 3, 4, 5 within every criterion.
- Objects scored: the original files as written (`variant-1-original.md` .. `variant-5-original.md`). `V<n>:L` = line L of `variant-<n>-original.md`.
- Correctness evidence used: `diff-analysis.md` (X-005, A-001..A-005), `debate-transcript.md` (orchestrator verification, Round 2 tables), `round2-advocate-a.md` N3, `round2-advocate-e.md` E11 and E14, `invariant-probe.md` (INV-005).
- Method: Claim-Evidence-Verdict for every criterion and variant. MET = 1, NOT MET = 0, no partial credit. No specific evidence for MET means NOT MET.
- Source requirements: R1 parallel correctness (index locks, shared worktrees, HEAD during retries); R2 safety and authorization (approver, audit trail); R3 recovery after a worker or git-owner crash; R4 coordinator context load; R5 fit with repo PR rules; R6 day-to-day use; R7 implementation cost.

## Dimension 1: Completeness

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| C1 covers R1-R7 | 1 | Met | Sections for each: Correctness (V1:10-14, lock, shared worktree, HEAD), Safety incl. "Audit trail" (V1:16-21), Recovery for worker and coordinator crash (V1:23-25), Context load (V1:27), PR rules (V1:30), Day to day (V1:33), Cost (V1:36) | MET (1) |
| C1 covers R1-R7 | 2 | Met | Correctness (V2:10-15, lock, sweep, HEAD), Safety incl. "Audit trail" (V2:17-22), Recovery of the git owner (worker) crash (V2:24-26), Context (V2:28), PR (V2:31), Day to day (V2:34), Cost (V2:37) | MET (1) |
| C1 covers R1-R7 | 3 | Met | Sync and Correctness (V3:17-22, quiescence, HEAD, serialization), Safety with audit (V3:24-27), Recovery for git session and worker crash (V3:32-34), Context (V3:36), PR (V3:39), Day to day (V3:42), Cost (V3:45) | MET (1) |
| C1 covers R1-R7 | 4 | Met | Lock and HEAD (V4:14,20,23), authorization hop and audit ("No Orca record", V4:18-19), Recovery (V4:26), Context (V4:29), PR (V4:32), Day to day (V4:35), Cost (V4:38) | MET (1) |
| C1 covers R1-R7 | 5 | Met | Correctness lock/HEAD/refs (V5:16-20), Safety and audit (V5:22-25), Recovery (V5:27-29), Context (V5:32), PR (V5:35), Day to day (V5:38), Cost (V5:41) | MET (1) |
| C2 edge cases and failure scenarios | 1 | Met | Stale `index.lock` after coordinator crash (V1:25); worker crash with partial files or absent contract (V1:24) | MET (1) |
| C2 edge cases and failure scenarios | 2 | Met | Shared-worktree failure ("contend for `index.lock` ... `git add -A` sweeps ... halts every running `/sc:implement` task", V2:14); parallel batch has no ladder (V2:15); crash mid-commit (V2:25) | MET (1) |
| C2 edge cases and failure scenarios | 3 | Met | "A failed `worker-start` still owns its terminal and must be released" (V3:33); no retention means degradation to a fresh worker per action (V3:50) | MET (1) |
| C2 edge cases and failure scenarios | 4 | Met | "Two git subagents in one worktree hit `index.lock`" (V4:20); subagent crash and coordinator crash (V4:26) | MET (1) |
| C2 edge cases and failure scenarios | 5 | Met | Two implement runs sharing refs across worktrees (V5:19); worker crash mid-commit (V5:28); parallel batch exclusion (V5:13) | MET (1) |
| C3 dependencies and prerequisites | 1 | Met | Per-task commits "wait for #326's own protocol change (`EVAL:63`, K3)" (V1:14); spec needs "wording in section 2.3 ... and the `/sc:git` row" (V1:37) | MET (1) |
| C3 dependencies and prerequisites | 2 | Met | "implement-side commits are a deliberate protocol change (#326 K3)" (V2:19); PRs "need D3 (b) and the section 3 pr-submit row" (V2:21); worktree per worker (V2:14) | MET (1) |
| C3 dependencies and prerequisites | 3 | Met | "C needs the user to request retention once at run start" (V3:13); D3 (b) for PRs (V3:25); cost list incl. brief template, contract shape, P4 changes (V3:46) | MET (1) |
| C3 dependencies and prerequisites | 4 | Met | "one agent definition (or a prompt template) ... plus the A wording in the spec" (V4:38); Bash restriction prerequisite UNVERIFIED (V4:12) | MET (1) |
| C3 dependencies and prerequisites | 5 | Met | Spec wording list and dependence on K3: "until it exists a worker commits only through steps its brief adds after the command finishes" (V5:41); per-row conditions (V5:10-14) | MET (1) |
| C4 success/completion criteria | 1 | Not met | No evidence found. Searched The proposal, Safety ("the commits themselves are the durable record", V1:21, is an audit statement), Day to day (V1:34, narrative only), Cost. No completion record or checkable result is defined for a coordinator git action | NOT MET (0) |
| C4 success/completion criteria | 2 | Met | "the worker's contract lists the commit SHA" (V2:22); "a contract field for SHAs" (V2:38) | MET (1) |
| C4 success/completion criteria | 3 | Met | "Each action therefore gets its own Task, Dispatch, `worker_done` and outcome" (V3:11); "a contract shape for git results (SHAs, branch, PR URL)" (V3:46) | MET (1) |
| C4 success/completion criteria | 4 | Met | Subagent role ends with "report the SHA" (V4:8) | MET (1) |
| C4 success/completion criteria | 5 | Met | Worker row: "lists each SHA in its contract's `artifacts`" (V5:13) | MET (1) |
| C5 explicit out of scope | 1 | Met | "Honest limit. A cannot honour #326's 'commit after each task' inside one `/sc:implement` run" (V1:14) | MET (1) |
| C5 explicit out of scope | 2 | Met | Merges excluded from workers: "It still owns merging branches back ... (so B still needs A for merges)" (V2:29); "B is never complete on its own" (V2:44) | MET (1) |
| C5 explicit out of scope | 3 | Met | "A single never-ending Task is not an option" (V3:14); "It does not solve per-task commits inside `/sc:implement`" (V3:52) | MET (1) |
| C5 explicit out of scope | 4 | Met | "D covers local commits and branch work only; outward actions fall back to A" (V4:17) | MET (1) |
| C5 explicit out of scope | 5 | Met | "Commands: none in this spec's phases; the per-task commit step inside `/sc:implement` stays #326's feature" (V5:41) | MET (1) |

Subtotals: V1 4/5, V2 5/5, V3 5/5, V4 5/5, V5 5/5.

## Dimension 2: Correctness

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| K1 no factual errors | 1 | Not met | "Workers never run a mutating git command" (V1:8) and "the worker made no git call" (V1:24). Shown inaccurate in `round2-advocate-a.md` N3: `/sc:implement` writes refs (`SKILL.md:113,116`), uses a private `GIT_INDEX_FILE` and runs `git restore --worktree` (`refs/retry.md:398`) | NOT MET (0) |
| K1 no factual errors | 2 | Met | Checked claims hold under the debate: HEAD baseline per task (V2:12, `SKILL.md:114`), shared-worktree lock/sweep/HEAD (V2:14), parallel batch without ladder (V2:15), missing stale-lock step stated honestly (V2:25). No B variant claim was shown false in Round 2 (B9 retracts a Round 1 statement, not variant text) | MET (1) |
| K1 no factual errors | 3 | Met | Orca mechanics cited and verified (V3:11-14; transcript line 23 confirms `worker-retain --help`); unverified points labelled (V3:13, V3:37). Round 2 concessions C4, C10 concern judgement (retention purpose, audit ranking), not false statements in the variant | MET (1) |
| K1 no factual errors | 4 | Not met | "A narrow tool list ... A git agent could list only `Bash, Read`" (V4:12) offered as a benefit. X-005 (`diff-analysis.md:48`) and D's own Round 2 D2 concede the original `tools:` mechanism cannot restrict Bash | NOT MET (0) |
| K1 no factual errors | 5 | Not met | Row 5 "Anything mutating git in a worktree shared with other running workers: Nobody but the coordinator" (V5:14) conceded "false as written for `/sc:implement`" (`round2-advocate-e.md` E14); "the retry Task (WC-6) checks for it first" (V5:28) conceded as overclaim (E11); "no two git writers share a lock" (V5:17) is overbroad for shared refs (INV-005) | NOT MET (0) |
| K2 approach feasible under stated constraints | 1 | Met | Uses existing defaults: "WC-9 already turns every outward default off in workers" (V1:37); pr-submit runs top-level, which the coordinator is (V1:18) | MET (1) |
| K2 approach feasible under stated constraints | 2 | Not met | Variant states it is unsafe in the default layout ("Unsafe in the default shared worktree", V2:41) and its changes run "against the spec's additive-edits rule for P1-P3 (`SPEC:172`)" (V2:38) | NOT MET (0) |
| K2 approach feasible under stated constraints | 3 | Not met | The long-lived session rests on user-requested retention (V3:13), unverified release semantics (V3:13) and unverified reuse injection into a running session (V3:37), and needs D3 (b), which conflicts with the spec's recommendation (V3:40). Round 2 C4: advocate withdrew the long-lived session | NOT MET (0) |
| K2 approach feasible under stated constraints | 4 | Met | Subagent-run local commits are feasible within constraints; PR work is explicitly returned to the main chat to satisfy `SKILL.md:47-49` (V4:17) | MET (1) |
| K2 approach feasible under stated constraints | 5 | Met | Stays inside D3 (a) and WC-9 (V5:23); no command changes in spec phases (V5:41); worker row dormant until K3, stated (V5:41) | MET (1) |
| K3 terminology consistent | 1 | Met | "coordinator", "worker", "outward", "settled contracts" used with one meaning throughout (V1:8,12,24) | MET (1) |
| K3 terminology consistent | 2 | Met | "committing worker", "shared worktree", "brief" used consistently (V2:8,14,18) | MET (1) |
| K3 terminology consistent | 3 | Met | "git session" used for the one dedicated worker throughout (V3:8,18,22,33) | MET (1) |
| K3 terminology consistent | 4 | Met | "subagent", "main chat", "outward actions" used consistently (V4:8,17,29) | MET (1) |
| K3 terminology consistent | 5 | Met | "outward action", "sole writer", "quiescent point" used consistently across table and prose (V5:10-14,17-18) | MET (1) |
| K4 no internal contradictions | 1 | Met | Limits are stated as limits (V1:14, V1:42) rather than contradicted; lock claim (V1:11) consistent with crash case (V1:25) | MET (1) |
| K4 no internal contradictions | 2 | Met | "The coordinator only plans, reads contracts and merges results" (V2:8) consistent with "It still owns merging branches back" (V2:29) | MET (1) |
| K4 no internal contradictions | 3 | Met | "long-lived" (title) reconciled with one Task per action and "A single never-ending Task is not an option" (V3:11,14) | MET (1) |
| K4 no internal contradictions | 4 | Not met | Diff point X-005 is an intra-variant contradiction: narrow tool list as a benefit (V4:12) versus "Whether the frontmatter can restrict Bash to git subcommands only is UNVERIFIED" in the same bullet | NOT MET (0) |
| K4 no internal contradictions | 5 | Met | Table rows 3 and 5 and correctness text agree that the coordinator commits shared worktrees only at quiescent points (V5:12,14,18). The row-5 problem is a factual error, scored under K1 | MET (1) |
| K5 claims supported | 1 | Met | Path:line citations on each point; GITDEMO procedure recorded (V1:46) | MET (1) |
| K5 claims supported | 2 | Met | Citations on each point (V2:11-15,18-21); #326 comment source named (V2:11) | MET (1) |
| K5 claims supported | 3 | Met | Orca reference lines cited for every mechanic (V3:11-15); UNVERIFIED marks where unsupported (V3:13,37) | MET (1) |
| K5 claims supported | 4 | Met | Citations for each cost (V4:17-20); the weak tool claim is labelled UNVERIFIED with the grep basis (V4:12) | MET (1) |
| K5 claims supported | 5 | Met | Citations on each row and bullet (V5:11-13,17-19,23-24); UNVERIFIED mark on the same-plan case (V5:19) | MET (1) |

Subtotals: V1 4/5, V2 4/5, V3 4/5, V4 3/5, V5 4/5.

## Dimension 3: Structure

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| S1 logical ordering | 1 | Met | Proposal, then correctness, safety, recovery, context, PR fit, day to day, cost, weaknesses, self-check (V1:7-45) | MET (1) |
| S1 logical ordering | 2 | Met | Same order: proposal through weaknesses (V2:7-40) | MET (1) |
| S1 logical ordering | 3 | Met | Proposal, then mechanics that make it possible, sync, correctness, safety, #326 relation, recovery, context, PR, day to day, cost, weaknesses (V3:7-48) | MET (1) |
| S1 logical ordering | 4 | Met | Proposal, benefits, costs, then correctness through weaknesses (V4:7-40) | MET (1) |
| S1 logical ordering | 5 | Met | Ownership table first, then correctness through weaknesses (V5:7-43) | MET (1) |
| S2 consistent hierarchy | 1 | Met | One H1, H2 per topic, bullets beneath (V1:1-45) | MET (1) |
| S2 consistent hierarchy | 2 | Met | One H1, H2 per topic, bullets beneath | MET (1) |
| S2 consistent hierarchy | 3 | Met | One H1, H2 per topic, bullets beneath | MET (1) |
| S2 consistent hierarchy | 4 | Met | One H1, H2 per topic, bullets beneath | MET (1) |
| S2 consistent hierarchy | 5 | Met | One H1, H2 per topic, table and bullets beneath | MET (1) |
| S3 separation of concerns | 1 | Met | Correctness, authorization, recovery and context kept in separate sections (V1:10,16,23,27) | MET (1) |
| S3 separation of concerns | 2 | Met | Separate sections per concern (V2:10,17,24,28) | MET (1) |
| S3 separation of concerns | 3 | Met | Mechanics (V3:10) and sync (V3:17) are separated from correctness (V3:21) and safety (V3:24) | MET (1) |
| S3 separation of concerns | 4 | Not met | "What D costs" (V4:16-20) mixes PR-rule fit, authorization hop, audit record and lock collisions in one list; there is no Safety section, and "Correctness" (V4:22-23) is one line deferring to A | NOT MET (0) |
| S3 separation of concerns | 5 | Met | Ownership table (V5:8-14) separated from correctness, safety and recovery sections (V5:16,22,27) | MET (1) |
| S4 navigation aids | 1 | Met | Full citation-key legend (V1:5) and a Self-check section for GITDEMO (V1:45-46) | MET (1) |
| S4 navigation aids | 2 | Met | Citation keys by cross-reference "as in `option-a.md`" (V2:5) | MET (1) |
| S4 navigation aids | 3 | Met | Citation keys by cross-reference (V3:5) | MET (1) |
| S4 navigation aids | 4 | Met | Citation keys by cross-reference plus its own `AGENT-TOOL` key (V4:5) | MET (1) |
| S4 navigation aids | 5 | Met | Citation keys by cross-reference (V5:5) | MET (1) |
| S5 position-paper conventions (required topics as sections) | 1 | Met | All seven topics are H2 headings (V1:10,16,23,27,30,33,36) | MET (1) |
| S5 position-paper conventions (required topics as sections) | 2 | Met | All seven topics are H2 headings (V2:10,17,24,28,31,34,37) | MET (1) |
| S5 position-paper conventions (required topics as sections) | 3 | Met | All seven topics are H2 headings (V3:21,24,32,36,39,42,45) | MET (1) |
| S5 position-paper conventions (required topics as sections) | 4 | Not met | No "Safety and authorization" heading; R2 content sits under "What D costs" (V4:16). Searched all H2 headings (V4:7,10,16,22,25,28,31,34,37,40) | NOT MET (0) |
| S5 position-paper conventions (required topics as sections) | 5 | Met | All seven topics are H2 headings (V5:16,22,27,31,34,37,40) | MET (1) |

Subtotals: V1 5/5, V2 5/5, V3 5/5, V4 3/5, V5 5/5.

## Dimension 4: Clarity

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| L1 unambiguous language | 1 | Met | Ownership stated without options: the coordinator "stages explicit paths, commits, creates and removes branches and worktrees, pushes, opens PRs ..., each only when the user's own instruction names that action" (V1:8) | MET (1) |
| L1 unambiguous language | 2 | Not met | The proposal leaves the scope open: "The brief states which git actions are allowed (local commit only; or commit plus push; or a PR through `/sc:pr-submit` under D3 (b))" with "for example" triggers (V2:8). It does not say which level B proposes | NOT MET (0) |
| L1 unambiguous language | 3 | Met | "Every git or GitHub action is a small Task the coordinator gives it ... Other workers never run mutating git" (V3:8) | MET (1) |
| L1 unambiguous language | 4 | Met | Split stated plainly: local commits by the subagent, "outward actions fall back to A" (V4:17) | MET (1) |
| L1 unambiguous language | 5 | Met | Per-action owner and condition table (V5:8-14) | MET (1) |
| L2 concrete | 1 | Met | Exact error text and file paths (V1:11), named retry rule (V1:13) | MET (1) |
| L2 concrete | 2 | Met | Concrete paths and lock behaviour (V2:11,14) | MET (1) |
| L2 concrete | 3 | Met | Exact Orca verbs `worker-show --dispatch`, `worker-start --task ... --terminal` (V3:11) | MET (1) |
| L2 concrete | 4 | Met | Concrete subagent role text and frontmatter example (V4:8,12) | MET (1) |
| L2 concrete | 5 | Met | Concrete ref path `refs/superclaude/implement/<slug>/T<id>` (V5:19) and row conditions (V5:13) | MET (1) |
| L3 each section has a clear purpose | 1 | Met | Each H2 maps to one requirement or to weaknesses/self-check | MET (1) |
| L3 each section has a clear purpose | 2 | Met | Each H2 maps to one requirement or to weaknesses | MET (1) |
| L3 each section has a clear purpose | 3 | Met | Extra sections have stated purposes: Orca mechanics (V3:10), sync (V3:17), #326 relay (V3:29) | MET (1) |
| L3 each section has a clear purpose | 4 | Met | "What D buys" and "What D costs" are labelled by purpose (V4:10,16) | MET (1) |
| L3 each section has a clear purpose | 5 | Met | Each H2 maps to one requirement; the table is the proposal (V5:7) | MET (1) |
| L4 terms defined on first use | 1 | Not met | Citation keys defined (V1:5), but spec IDs used undefined: "K3" (V1:14), "D4 option (b)" (V1:20), "WC-9" (V1:37) | NOT MET (0) |
| L4 terms defined on first use | 2 | Not met | "D4 (a)" (V2:8), "WC-11", "F2" (V2:11), "K3" (V2:19) undefined | NOT MET (0) |
| L4 terms defined on first use | 3 | Not met | "D3 (b)" (V3:25), "SA-2, WC-8" (V3:30), "P4" (V3:46) undefined | NOT MET (0) |
| L4 terms defined on first use | 4 | Not met | `AGENT-TOOL` defined (V4:5), but "quiescent points" (V4:14) and "Task or Dispatch" (V4:19) used without definition | NOT MET (0) |
| L4 terms defined on first use | 5 | Not met | "Quiescent point" is defined in the table (V5:12), but "D4" (V5:10), "F3" (V5:11), "WC-9", "WC-11" (V5:41) are undefined | NOT MET (0) |
| L5 actionable next steps or decision points | 1 | Met | "The spec needs only wording in section 2.3 (coordinator duties) and the `/sc:git` row" (V1:37) | MET (1) |
| L5 actionable next steps or decision points | 2 | Met | Concrete change list: commit step, stale-lock rule, SHA field, K3, placement rule, merge step (V2:38) | MET (1) |
| L5 actionable next steps or decision points | 3 | Met | Change list (V3:46) and a user decision at run start (retention, V3:13) | MET (1) |
| L5 actionable next steps or decision points | 4 | Met | "one agent definition (or a prompt template) ... plus the A wording" (V4:38) | MET (1) |
| L5 actionable next steps or decision points | 5 | Met | Named spec edits: "wording in WC-9, WC-11, section 2.3, the `/sc:git` row and D4" (V5:41) | MET (1) |

Subtotals: V1 4/5, V2 3/5, V3 4/5, V4 4/5, V5 4/5.

## Dimension 5: Risk Coverage

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| R1 at least 3 risks with probability and impact | 1 | Not met | Four weaknesses listed (V1:40-43) with no probability or impact rating. Searched Weaknesses, Context load, Recovery | NOT MET (0) |
| R1 at least 3 risks with probability and impact | 2 | Not met | Four weaknesses (V2:41-44), no probability or impact rating | NOT MET (0) |
| R1 at least 3 risks with probability and impact | 3 | Not met | Four weaknesses (V3:49-52), no probability or impact rating | NOT MET (0) |
| R1 at least 3 risks with probability and impact | 4 | Not met | Three weaknesses (V4:41-43), no probability or impact rating | NOT MET (0) |
| R1 at least 3 risks with probability and impact | 5 | Not met | Three weaknesses (V5:44-46), no probability or impact rating | NOT MET (0) |
| R2 mitigation for each risk | 1 | Not met | Context growth has a mitigation (V1:28), but weakness 4, "the coordinator must commit in each worktree" (V1:43), has none | NOT MET (0) |
| R2 mitigation for each risk | 2 | Not met | Weakness 3, outward actions multiplied across sessions (V2:43), has no mitigation | NOT MET (0) |
| R2 mitigation for each risk | 3 | Not met | Weakness 1, extra hop and 60 s readiness start (V3:49), and weakness 3, D3 (b) (V3:51), have no mitigation | NOT MET (0) |
| R2 mitigation for each risk | 4 | Not met | Weakness 2, "adds a hop for authorization without adding an audit record" (V4:42), has no mitigation | NOT MET (0) |
| R2 mitigation for each risk | 5 | Not met | Weakness 1, "two rule sets to state and test" (V5:44), has no mitigation | NOT MET (0) |
| R3 failure modes and recovery procedures | 1 | Met | Coordinator crash: "inspects with `git status` and removes the stale lock only after proving no git process runs" (V1:25) | MET (1) |
| R3 failure modes and recovery procedures | 2 | Met | Stale lock confined to the worker's worktree; retry is a new Task (V2:25) | MET (1) |
| R3 failure modes and recovery procedures | 3 | Met | Inspect, clear lock after proof, re-issue as new Task; release a failed `worker-start` terminal (V3:33) | MET (1) |
| R3 failure modes and recovery procedures | 4 | Met | Subagent crash returns an error; coordinator inspects `git status`; coordinator crash recovers as A (V4:26) | MET (1) |
| R3 failure modes and recovery procedures | 5 | Met | Worker crash: lock only in its worktree, earlier commits survive; coordinator crash as A (V5:28-29) | MET (1) |
| R4 external dependencies and their failure scenarios | 1 | Not met | Relies on Orca durability ("The Run's state is durable in Orca", V1:25; queueing, V1:28) but gives no Orca or GitHub failure scenario. Searched Recovery, Context load, PR fit | NOT MET (0) |
| R4 external dependencies and their failure scenarios | 2 | Not met | No evidence found. Searched Safety, Recovery, PR fit (V2:17-32); no Orca, GitHub or pr-submit failure scenario | NOT MET (0) |
| R4 external dependencies and their failure scenarios | 3 | Met | Orca failure paths: "A failed `worker-start` still owns its terminal and must be released" (V3:33); second Dispatch rejected with `runtime_error` (V3:12); retention not granted (V3:50) | MET (1) |
| R4 external dependencies and their failure scenarios | 4 | Met | Agent tool failure scenario: the subagent's report "returns in the same confident register whether right or wrong" (V4:18) | MET (1) |
| R4 external dependencies and their failure scenarios | 5 | Not met | No evidence found. Searched Safety, Recovery, PR fit (V5:22-35); no Orca, GitHub or pr-submit failure scenario | NOT MET (0) |
| R5 monitoring or validation mechanism | 1 | Met | `git status` inspection and proof that no git process runs before lock removal (V1:25) | MET (1) |
| R5 monitoring or validation mechanism | 2 | Not met | No detection mechanism; recovery says the lock "must first" be cleared without saying how a live lock is distinguished (V2:25). Searched Recovery, Safety | NOT MET (0) |
| R5 monitoring or validation mechanism | 3 | Met | "Orca reports liveness (`CAPS:122-126`)" (V3:33) | MET (1) |
| R5 monitoring or validation mechanism | 4 | Met | Subagent Bash calls still raise a permission prompt to the person, since subagents inherit the parent's mode (V4:18) | MET (1) |
| R5 monitoring or validation mechanism | 5 | Met | Worker SHAs listed in contracts (V5:25); wrong-path mistakes caught by "the coordinator's later review" (V5:45) | MET (1) |

Subtotals: V1 2/5, V2 1/5, V3 3/5, V4 3/5, V5 2/5.

## Dimension 6: Invariant & Edge Case Coverage

| Criterion | Variant | Claim | Evidence | Verdict |
|---|---|---|---|---|
| I1 collection boundaries (empty, single, maximum) | 1 | Met | Empty case: staging decided from the contract "(or its absence, `SPEC:69`)" (V1:24); single writer per index (V1:11) | MET (1) |
| I1 collection boundaries (empty, single, maximum) | 2 | Met | Single versus several committers per worktree: "Strongest case: one worker per worktree" vs "Two workers committing in one worktree" (V2:11,14) | MET (1) |
| I1 collection boundaries (empty, single, maximum) | 3 | Met | Maximum one active Dispatch per terminal (V3:12) | MET (1) |
| I1 collection boundaries (empty, single, maximum) | 4 | Met | "one subagent at a time"; two subagents collide (V4:14,20) | MET (1) |
| I1 collection boundaries (empty, single, maximum) | 5 | Met | Empty grant: "Without that instruction nothing is committed" (V5:38); two runs of one plan (V5:19) | MET (1) |
| I2 state interactions across component boundaries | 1 | Met | Coordinator commit moves HEAD that a worker's retry ladder checks (V1:13) | MET (1) |
| I2 state interactions across component boundaries | 2 | Met | Task-start HEAD baseline versus in-run commit (V2:12); shared HEAD halting other tasks (V2:14) | MET (1) |
| I2 state interactions across component boundaries | 3 | Met | Git-session commit moves HEAD under a running implement worker (V3:18) | MET (1) |
| I2 state interactions across component boundaries | 4 | Met | Subagent commit versus running implement worker in the same worktree (V4:23) | MET (1) |
| I2 state interactions across component boundaries | 5 | Met | Per-worktree HEAD versus shared refs across linked worktrees (V5:18-19) | MET (1) |
| I3 guard condition gaps | 1 | Not met | Guards are stated (V1:13, V1:25) but no gap in them is identified; how quiescence is known is not discussed (later raised as A-003, `diff-analysis.md:71`). Searched Correctness, Recovery, Weaknesses | NOT MET (0) |
| I3 guard condition gaps | 2 | Met | Stale-lock clearing is "a step no command has today" (V2:25) | MET (1) |
| I3 guard condition gaps | 3 | Met | Release of a reused terminal UNVERIFIED (V3:13); without retention "C degrades" (V3:50) | MET (1) |
| I3 guard condition gaps | 4 | Met | Bash-to-git restriction UNVERIFIED (V4:12) | MET (1) |
| I3 guard condition gaps | 5 | Met | Slug guard "UNVERIFIED for two runs of the same plan in two worktrees" (V5:19); wrong-path commits pass until later review (V5:45) | MET (1) |
| I4 count divergence (off-by-one, ranges) | 1 | Met | One `worker_done` per run versus N tasks inside it, so per-task commits cannot be timed (V1:14) | MET (1) |
| I4 count divergence (off-by-one, ranges) | 2 | Met | Batch boundary: "in-run commits must wait for a batch's last `complete` line too" (V2:15) | MET (1) |
| I4 count divergence (off-by-one, ranges) | 3 | Met | Coordinator "still sees only the run's end" (V3:52); 60 s start versus seconds-long actions (V3:49) | MET (1) |
| I4 count divergence (off-by-one, ranges) | 4 | Not met | No evidence found. Searched all sections; no off-by-one, range or event-count mismatch is discussed | NOT MET (0) |
| I4 count divergence (off-by-one, ranges) | 5 | Met | "only between tasks and never inside a parallel batch" (V5:13) | MET (1) |
| I5 interaction effects when components combine | 1 | Met | pr-submit loop blocks the coordinator from reacting to workers (V1:28) | MET (1) |
| I5 interaction effects when components combine | 2 | Met | Two committers in one worktree: lock, sweep, HEAD halt (V2:14) | MET (1) |
| I5 interaction effects when components combine | 3 | Met | Git session at quiescent points with implement workers; pr-submit loop overlapping coordinator work (V3:18,22) | MET (1) |
| I5 interaction effects when components combine | 4 | Met | pr-submit rule forcing outward actions back to the main chat (V4:17); parallel subagents colliding (V4:20) | MET (1) |
| I5 interaction effects when components combine | 5 | Met | Two implement runs combining on shared refs (V5:19) | MET (1) |

Subtotals: V1 4/5, V2 5/5, V3 5/5, V4 4/5, V5 5/5.

## Summary

| Dimension | V1 (A) | V2 (B) | V3 (C) | V4 (D) | V5 (E) |
|---|---|---|---|---|---|
| Completeness | 4 | 5 | 5 | 5 | 5 |
| Correctness | 4 | 4 | 4 | 3 | 4 |
| Structure | 5 | 5 | 5 | 3 | 5 |
| Clarity | 4 | 3 | 4 | 4 | 4 |
| Risk Coverage | 2 | 1 | 3 | 3 | 2 |
| Invariant & Edge Case Coverage | 4 | 5 | 5 | 4 | 5 |
| **Total /30** | **23** | **23** | **26** | **22** | **25** |

## Edge-case floor check

| Variant | Invariant & Edge Case score | Floor (0/5 makes it ineligible as base) |
|---|---|---|
| V1 (A) | 4/5 | Eligible |
| V2 (B) | 5/5 | Eligible |
| V3 (C) | 5/5 | Eligible |
| V4 (D) | 4/5 | Eligible |
| V5 (E) | 5/5 | Eligible |

No variant falls below the floor.

Notes for the pass-2 comparison: no criterion carries partial credit. Three verdicts lean on debate findings rather than the variant text alone: V1 K1 (N3), V4 K1 (X-005) and V5 K1 (E11, E14, INV-005). V3's feasibility verdict (K2) rests on the variant's own UNVERIFIED marks and the Round 2 withdrawal (C4).
