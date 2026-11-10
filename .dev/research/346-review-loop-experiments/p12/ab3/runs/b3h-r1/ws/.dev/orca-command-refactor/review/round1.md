review: 1 of 3

# /sc:spec-panel critique report, round 1 (first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy, read in full)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (repo-relative), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review). Prior report: none.
- Reviewer model: claude-haiku-5-5 (Haiku 5.5), fresh context, no prior round seen.
- Panel: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Newman, Hohpe, Nygard; Whittaker (adversarial, active in every review).
- Mode of working: planning spec review only. Nothing edited. Only this file written.

## Coverage and verification limits

- Read in full: the candidate (`specs/orca-worker-contract-spec.md:1-286`), `README.md:1-39`, `inventory/commands-a.md:1-121`, `inventory/commands-b.md:1-324`, `inventory/orca-capabilities.md:1-189`, and the sandbox copies of `command.md` and the review-loop prompts file.
- Every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in the candidate was checked against the matching inventory line, and the spec's own line references (WC-, SA-, AC-, D-, §) were checked against the candidate. Mismatches are noted in the findings.
- UNVERIFIED for this review: every citation that points outside `.dev/orca-command-refactor/` (for example `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/skills/...`, Orca's `/opt/Orca/...` files, `EVIDENCE.md`, `pyproject.toml`, `Makefile`). The sandbox holds none of them, so I neither confirm nor refute those claims. Where a finding depends on one, the finding says so.
- The Orca facts are taken from the inventory's quoted command output (`CAPS:N`), not from a live Orca run.

## Summary

- Blocking findings (verdict-relevant): F-01 to F-06.
- Medium findings (follow-up candidates, not blocking): F-07 to F-15.
- Minor notes: m-01 to m-03.
- Verdict: FAIL, because F-01 to F-06 are open.

## Quality scores (0-10, advisory)

| Dimension | Score | Reason |
|---|---|---|
| Clarity | 6 | Phase, row and WC rules are well structured; several rules contradict each other across sections (F-01, F-03, F-07). |
| Completeness | 6 | Good coverage of 43 commands; no rule for worker-start failure (F-12) or for gate answers (F-08). |
| Testability | 5 | Most AC are runnable; AC-0.4 cannot pass in P0 (F-04); AC-C1 greps a directory that holds allowed content (F-05). |
| Consistency | 4 | Contract path, output flag names, and standalone-file rules disagree across WC-4, SA-3, §3.1 and §3.2 (F-01, F-02, F-03). |

## Findings

### === REQUIREMENTS ANALYSIS ===

#### F-03 (BLOCKING) SA-3 contradicts the §3.1 contract fixes for standalone runs
- **Issue.** SA-3 says "A standalone default run writes the same files it writes today" (`specs/orca-worker-contract-spec.md:148`). §3.1 then changes files that standalone runs write: adversarial "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" (`:83`), and workflow "Write the contract for pre-creation STOPs" (`:92`). Inventory A says the adversarial contract "MUST be written on every run" (`inventory/commands-a.md:35`), so a standalone adversarial run already writes a contract at a varying path, and a standalone workflow pre-creation STOP writes none (`inventory/commands-b.md:272`).
- **Grading check.** An implementer who follows SA-3 literally leaves the standalone adversarial and workflow file set unchanged, and follows §3.1 changes it, so the two texts cannot both hold. Blocking by contradiction.
- **Expert.** Wiegers (traceability between SA-3 and §3.1 rows), Fowler (contract boundary).
- **Recommendation.** Either exempt these two fixes from SA-3 by name with the reason (a documented defect that is already a standalone output), or gate the new paths behind `--unattended` / the new output flag. Restate SA-3 to list the exceptions.
- **Priority.** High. **Quality impact.** Medium: a standalone user sees the contract file move or appear.

#### F-07 (MEDIUM) P1 accepts `--unattended` on gated and outward commands before their rules exist
- **Issue.** P1 scope says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (`specs/orca-worker-contract-spec.md:159`). Gated commands (for example tdd, reflect, troubleshoot at `:90`, `:88`, `:91`) and outward-default commands (post-release, `:113`; pr-submit, `:114`; task commit/push, `:121`) get the flag in P1 but their gate and WC-9 rules are only added in P2 or P4 (`:160`, `:162`). The no-op claim holds only for gate-free commands.
- **Grading check.** An implementer who follows P1 literally accepts `--unattended` on post-release, and post-release's confirmations (`inventory/commands-b.md:33`) still prompt until P4, so the worker stalls. Stall, not outward action, so Medium.
- **Expert.** Hohpe (phase boundary and integration), Wiegers.
- **Recommendation.** Limit P1's flag acceptance to command rows with no gate and no outward default, or make a gated command under `--unattended` in P1 resolve as blocked, not silently ignore the flag.

#### F-08 (MEDIUM) The ask-and-resume path (WC-3) has no answer flags for most gates
- **Issue.** WC-3 says the worker may ask the coordinator and then "re-invoke or resume the command with the answer as a flag" (`:61`). §3 names an answer flag for only a few gates (spec-panel `target_release`, `:120`; cli-eval `--suite`, `:104`; tasklist/roadmap resume flags). For the other gates (for example troubleshoot `--fix`, review-translation phase 1 context, task confidence, research strategy) no flag is named, so the ask path has no defined re-entry.
- **Grading check.** An implementer cannot build the re-entry for, say, review-translation from the text; it needs a guess about the flag name and semantics. Medium.
- **Expert.** Wiegers (requirement incompleteness), Cockburn (actor and goal for the answer).
- **Recommendation.** Add a per-gate "answer input" column to §3 or state that a gate without an answer flag resolves as blocked, not asked.

#### F-12 (MEDIUM) No rule for a failed worker start
- **Issue.** WC-1 covers readiness only (`:59`). If `worker-start` fails at `agent_readiness` (60 s default), the spec gives no worker or coordinator action. The inventory of Orca facts says a failed start must not be relaunched and its receipt read (`inventory/orca-capabilities.md:46`), and a failed start still owns a terminal to be released (`inventory/orca-capabilities.md:112`). The spec's WC-6 covers only `--retry-of` of an existing attempt.
- **Grading check.** An implementer following the spec relaunches on failure and can reach the three-failure circuit breaker (`inventory/orca-capabilities.md:80`). Medium.
- **Expert.** Nygard (failure modes).
- **Recommendation.** Add WC-1a: on a failed start, read the receipt's `failedStage`, do not relaunch with a new Dispatch, release the owned terminal, and record the attempt.

#### F-13 (MEDIUM) §7.2 step 2 and AC-2.2 fail a legitimate `ask`, and their premise is unverified
- **Issue.** Step 2 passes only if `observation.agentWait` is never non-null (`specs/orca-worker-contract-spec.md:181`). AC-2.2 expects "step 2 never shows agentWait" for a gate-trigger run (`:200`). WC-3 explicitly lets a worker park on `ask` (`:61`), and the inventory says agentWait names a worker parked on a prompt only a human can answer (`inventory/orca-capabilities.md:129`). Whether an open `ask` sets agentWait is not stated (UNVERIFIED in the inventory, `inventory/orca-capabilities.md:52,129`).
- **Grading check.** A run that uses WC-3 correctly fails step 2 if agentWait covers asks, and passes AC-2.2 only if the worker blocks instead of asking. The criterion contradicts WC-3 under one reading. Medium.
- **Expert.** Adzic (testable example).
- **Recommendation.** Allow a non-null agentWait whose reason is an open `ask` in step 2, or check the open-question record directly.

#### F-14 (MEDIUM) No ordering between writing the contract and sending `worker_done`
- **Issue.** WC-4 requires the contract on every outcome (`:62`) and WC-5 requires exactly one `worker_done` (`:63`), but neither orders them. §2.3 says the coordinator opens the file after `worker_done` (`:73`). If the worker sends `worker_done` before the contract is flushed, the coordinator reads a missing or empty file. Step 4 runs after `worker_done` (`:183`), so the test would also fail on a correct late write.
- **Attack (Whittaker).** I can break this specification by **sequence reordering**. The invariant at **WC-4 / WC-5 (`:62-63`)** fails when **worker_done is sent first**. Concrete attack: the worker sends `worker_done --report-path <contract>` while its shell is still writing the YAML; the coordinator's `check` returns, `test -s` reads a zero-byte file, and the outcome is recorded with no report.
- **Grading check.** Needs a guess about flush timing, so Medium.
- **Expert.** Hohpe (sequencing), Whittaker.
- **Recommendation.** Require the contract to be written and closed before `worker_done`, and have step 4 run before the check returns.

#### F-02 (BLOCKING) The spec-panel output flag conflicts with its own `--unattended` contract
- **Issue.** §3.2 says spec-panel gets "add `--output`; contract" (`specs/orca-worker-contract-spec.md:120`), and WC-4 names `--output` / `--output-dir` (`:62`). The spec-panel command already defines its unattended mode: "`--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work" (`command.md:460`), with the contract at `<report-dir>/return-contract.yaml` (`command.md:461`). A coordinator brief written from WC-4 for spec-panel would pass `--output` and get a refusal.
- **Grading check.** An implementer who follows §3.2 builds an `--output` flag that the command refuses under `--unattended`. Blocking: the two texts name different flags for the same contract, and the worker fails immediately.
- **Expert.** Fowler (interface), Wiegers (traceability).
- **Recommendation.** Make WC-4 name the flag per command ("`--report-dir` for spec-panel; `--output` otherwise") or adopt one name for all commands, and update §3.2's spec-panel row to match `command.md:459-461`.

#### F-06 (BLOCKING) Fixed-path commands clobber output under concurrent or retried workers
- **Issue.** WC-11 says two workers in one worktree must never write the same file, and default output paths must carry a timestamp or a coordinator slug (`specs/orca-worker-contract-spec.md:69`). WC-6 says a retry must not corrupt the first attempt's output (`:64`). §3.1 lists commands with fixed paths as ready: index-repo writes `PROJECT_INDEX.md` with the location implied (`:86`); init-lite "Re-run overwrites its marked report" (`:87`); cleanup-audit has a fixed output directory, which the spec itself says allows "one audit per worktree at a time" (`:85`). §2.3 (`:73`) gives the coordinator no rule to serialise such Tasks.
- **Grading check.** An implementer who dispatches two index-repo workers in one worktree, or retries init-lite with `--retry-of`, overwrites the earlier file. That is data loss under a stated MUST, so blocking.
- **Expert.** Nygard (recovery), Newman (shared state), Whittaker (sentinel and shared-file collision).
- **Recommendation.** Give each fixed-path command a per-run subdirectory under the coordinator's `--output`, or add a §2.3 rule that Tasks writing a fixed path are serialised and listed in the brief. Restate WC-11 to name them.

### === ARCHITECTURE ANALYSIS ===

#### F-01 (BLOCKING) WC-4's contract path cannot be derived for file-valued `--output` commands
- **Issue.** WC-4 says the command writes `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory the coordinator passed, so the report path is known before dispatch (`specs/orca-worker-contract-spec.md:62`). §3.1 gives `--output <file>` for init-lite (`:87`) and tdd (`:90`, "the TDD at `--output`"). For those commands the directory is not given and the contract path is undefined. §3 also names no default when `--output` is absent under `--unattended`.
- **Grading check.** Two stated texts contradict: WC-4 (a directory is always given, the path is known) and §3.1 (`--output` is a file). An implementer cannot place the contract for init-lite or tdd. Blocking.
- **Expert.** Fowler (interface boundary), Newman (contract evolution).
- **Recommendation.** Define the contract location for file-valued outputs, for example `<dirname(output)>/return-contract.yaml`, and require a directory default for every unattended command. Update §3.1 rows (`:87`, `:90`) to match.

#### F-04 (BLOCKING) AC-0.4 requires a contract path that P0 cannot produce
- **Issue.** AC-0.4 says steps 1-3 and 5-7 must pass and step 4 uses the existing report file, "since the contract arrives in P1" (`specs/orca-worker-contract-spec.md:194`). Step 3's pass condition is "its report path is the WC-4 contract path" (`:182`). In P0 `/sc:troubleshoot` writes `REPORT.md` (`inventory/commands-b.md:49`) and no WC-4 file exists, so step 3 cannot pass. The AC waives step 4 only.
- **Grading check.** An acceptance criterion cannot pass as written. Blocking.
- **Expert.** Adzic (acceptance example), Cockburn (phase goal).
- **Recommendation.** In AC-0.4, waive step 3's report-path condition for P0 as well, or check the command's existing report path against `worker_done --report-path`.

#### F-05 (BLOCKING) AC-C1 scans a directory that holds content the spec allows to name Orca
- **Issue.** AC-C1 greps `src/superclaude/core` as well as commands, skills and agents (`specs/orca-worker-contract-spec.md:172`). SA-2 permits the contract file to name Orca's question channel (`:147`), and P0 adds an Orca section to `HOW-WE-WORK.md` in `core` (`:158`). The grep therefore fails on allowed content. The pattern is also written with `\|` alternation inside `grep -E`, which the table cell's escaping makes ambiguous: copied literally, `\|` in ERE is a literal pipe and the alternation silently matches nothing.
- **Grading check.** The check cannot pass on the deliverable SA-2 permits, and as written it can pass vacuously. Blocking.
- **Expert.** Nygard (gate reliability), Fowler (boundary).
- **Recommendation.** Exclude `WORKER-CONTRACT.md` from AC-C1 by name, state that the HOW-WE-WORK section must not contain `orca` commands, and write the pattern as `(orchestration|worktree|terminal|agent)` in ERE with the code block not escaped.

#### F-11 (MEDIUM) The tasklist verdict relies on an unverified nesting premise and misstates depth
- **Issue.** §3.2 says tasklist's "reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit" (`specs/orca-worker-contract-spec.md:122`, citing INV-A:14). Stage 10.5 runs N subagents, and each runs reflect, which spawns its own agents (`inventory/commands-b.md:210`). The actual depth is at least two layers below the worker. The inventory marks whether a subagent can spawn agents as UNVERIFIED (`inventory/commands-b.md:314`, item 1; `inventory/commands-b.md:320`). INV-A:14 says the fan-out loses its Agent tool at the depth limit, so the premise is not established.
- **Grading check.** The verdict "ready for this row" needs the unverified premise. Medium.
- **Expert.** Newman (service decomposition), Fowler.
- **Recommendation.** Say "UNVERIFIED: nested spawn under a worker" and add a P2 acceptance check for tasklist that runs Stage 10.5 under a worker, or move the per-phase reflect to the coordinator.

#### F-09 (MEDIUM) A FAIL-verdict audit reports `succeeded`, and dependents then release
- **Issue.** WC-5 maps an audit whose verdict is FAIL to `--outcome succeeded` (`specs/orca-worker-contract-spec.md:63`), and the decisions table repeats this for `partial` (`:263`). In Orca a successful `worker_done` settles the Task (`inventory/orca-capabilities.md:77`), and only a failed Task keeps dependents blocked (`inventory/orca-capabilities.md:90`). §2.3 does not require the coordinator to check the verdict before it releases dependents (`:73`).
- **Attack (Whittaker).** I can break this specification by **divergence**. The invariant at **WC-5 (`:63`)** fails when **the audit verdict is FAIL but status is succeeded**. Concrete attack: an adversarial or reflect audit writes `status: succeeded`, `verdict: FAIL`; the Task settles; the `--deps` dependent (for example an implement Task) becomes ready and runs on a failed audit.
- **Grading check.** Needs the guess that the coordinator reads only `status`. Medium.
- **Expert.** Nygard, Hohpe (integration).
- **Recommendation.** Add a `verdict` field to the contract, and map a FAIL verdict to `failed` or require the coordinator's brief to gate dependents on it.

#### F-10 (MEDIUM) WC-9 covers outward actions only, not local code changes under `--unattended`
- **Issue.** WC-9 turns off defaults that push, post, install, provision or call paid runs (`specs/orca-worker-contract-spec.md:67`). §3.1 makes reflect's `--remediate` follow the headless auto-accept rule under `--unattended` (`:88`), and that rule leads into sc:workflow / task-builder remediation (`inventory/commands-b.md:36`), which can change code. No requirement says whether such a local edit is allowed without a person.
- **Grading check.** Needs an assumption about whether code edits count as outward. Medium.
- **Expert.** Cockburn (goal and actor of the auto-accept), Wiegers.
- **Recommendation.** Decide in writing whether unattended runs may edit product code; if not, `--remediate` resolves as blocked under `--unattended`.

#### F-15 (MEDIUM) The central rejection rests on a rule whose enforcing call sites are UNVERIFIED
- **Issue.** §1.3 R1 says the command-calls-Orca alternative "cannot run as a worker at the current setting" (`specs/orca-worker-contract-spec.md:33`). The cited refusal text and depth 1 are verified (`inventory/orca-capabilities.md:97-101`), but the same entry says which call sites enforce it is UNVERIFIED and whether a depth-1 worker may call `task-create` is UNVERIFIED (`inventory/orca-capabilities.md:103`).
- **Grading check.** A reader cannot tell whether the alternative is blocked outright or only refused at worker-start. Medium.
- **Expert.** Fowler (rejected alternatives), Hohpe.
- **Recommendation.** Write R1 as "refused at worker-start and dispatch (presumed); UNVERIFIED for task-create", and keep the decision.

## Guard Condition Boundary Table

Triggered: the spec contains conditional rules (readiness limit, outcome mapping, contract-on-every-outcome, wait split, gate resolution, standalone rule, outward flags). Completeness: every guard below lists its input classes; a class left out has a one-line reason. Status GAP findings are numbered to the findings above.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit | WC-1, `:59` | Typical: prompt-free start | ready in 30 s | ready | `state: ready` (7.2 step 1, `:180`) | OK |
| readiness limit | WC-1, `:59` | Maximum/Overflow: prompt unanswered past limit | elapsed > 60 s | fail at agent_readiness | no worker or coordinator action stated | GAP (F-12) |
| readiness limit | WC-1, `:59` | Sentinel: `--timeout-ms` absent or invalid | none / 0 | default 60 s | WC-1 names the default | OK |
| readiness limit | WC-1, `:59` | Zero/Empty, One/Minimal | n/a | n/a | the limit is a timer, so no count applies; the rule is the same as Typical | omitted |
| outcome mapping | WC-5, `:63` | Zero/Empty: no report file | `report=absent` | `failed` | stated | OK |
| outcome mapping | WC-5, `:63` | One/Minimal: `status: partial` | `partial` | `succeeded` | stated (`:263`) | OK |
| outcome mapping | WC-5, `:63` | Typical: `status: succeeded` | `succeeded` | `succeeded` | stated | OK |
| outcome mapping | WC-5, `:63` | Sentinel: `status: blocked` | `blocked` | `failed` | stated | OK |
| outcome mapping | WC-5, `:63` | Legitimate edge: audit verdict FAIL, status succeeded | `verdict: FAIL` | `succeeded` | dependents released by Orca (`inventory/orca-capabilities.md:77,90`) | GAP (F-09) |
| outcome mapping | WC-4, `:62` | Unknown status string (for example `done`) | not in enum | undefined | the 7.2 step 4 test rejects it, but the runtime rule is not stated | GAP (F-09, Medium) |
| outcome mapping | WC-5, `:63` | Maximum/Overflow | n/a | n/a | enum has four values, not a count | omitted |
| contract path | WC-4, `:62` | Typical: directory `--output <dir>` | `<dir>` | `<dir>/return-contract.yaml` | stated | OK |
| contract path | WC-4, `:62` | Zero/Empty: `--output` absent under `--unattended` | none | path undefined | no default stated | GAP (F-01) |
| contract path | WC-4, `:62` | Sentinel: file-valued `--output <file>` (init-lite `:87`, tdd `:90`) | `<file>` | path undefined | contradicts "directory" | GAP (F-01) |
| contract path | WC-4, `:62` | Legitimate edge: fixed sub-path (adversarial `:83`) | `<output>/adversarial/` | differs from WC-4 literal path | §3.1 row only | GAP (F-03) |
| contract path | WC-4, `:62` | One/Minimal: `--output` flag name (`--output` vs `--report-dir`) | `--report-dir` | refused under spec-panel's rule | `command.md:460` | GAP (F-02) |
| retry safety | WC-6, `:64` | Typical: fresh output dir | new dir | no overwrite | stated | OK |
| retry safety | WC-6, `:64` | Legitimate edge: retry into existing marked report (init-lite `:87`) | existing file | overwrite of first attempt | WC-6 forbids corrupting it | GAP (F-06) |
| retry safety | WC-11, `:69` | Legitimate edge: two Tasks, one fixed file (index-repo `:86`) | two workers | second write clobbers first | no serialisation rule (§2.3 `:73`) | GAP (F-06) |
| standalone | SA-3, `:148` | Typical: no `--unattended`, no new output flag | no flags | same files as today | adversarial contract path changes (`:83`); workflow STOP contract added (`:92`) | GAP (F-03) |
| standalone | SA-3, `:148` | Sentinel: `--output` given, no `--unattended` | output flag set | new files allowed | SA-3 permits | OK |
| gate resolution | WC-2, `:60` | Zero/Empty: required gate flag absent | none | `blocked` (c) | stated as general rule | OK |
| gate resolution | WC-2, `:60` | Sentinel: `--unattended` and `--interactive` together | both set | conflict | only some rows say "refused" (`:104`, `:110`) | GAP (m-01) |
| gate resolution | WC-2, `:60` | Typical: documented default exists | default | (a) | per-row (`:99-125`) | OK |
| gate resolution | WC-2, `:60` | One/Minimal, Maximum | n/a | n/a | a gate is a yes/no, so no count applies | omitted |
| wait split | WC-10, `:68` | Typical: wait 2 min | 120 s | single call ok | stated | OK |
| wait split | WC-10, `:68` | Boundary: one poll-plus-sleep iteration near 4 min | 240 s | ok | runtime of pr-submit poll UNVERIFIED (`:114`) | GAP (Medium) |
| wait split | WC-10, `:68` | Maximum: pr-submit 600 s cumulative budget in one call | 600 s | exceeds 240 s | budget is cumulative (`:114`) | GAP (Medium) |
| ask and resume | WC-3, `:61` | Typical: answer before timeout | answered | resume with answer as flag | no answer flag for most gates | GAP (F-08) |
| ask and resume | WC-3, `:61` | Zero/Empty: ask timeout omitted | none | default timeout | UNVERIFIED default (`inventory/orca-capabilities.md:68`), but WC-3 needs no value | OK |
| outward flag | WC-9, `:67` | Typical: flag absent | none | off | stated | OK |
| outward flag | WC-9, `:67` | Legitimate edge: brief passes flag, user did not authorise | flag set | on | D4 (`:244-247`) is open | GAP (F-10, D4) |
| depth | WC-8, `:66` | Typical: command calls `worker-start` at depth 1 | call | refused | forbidden by WC-8 and CAPS:97-101 | OK |

Pipeline Dimensional Analysis: not triggered. The spec describes no multi-stage data flow whose counts change. The count-changing fan-outs (for example tasklist's 2N validators, `inventory/commands-b.md:211`) sit in the inventories, not in the candidate.

## Findings: wording and minor notes

- **m-01 (minor).** WC-2 (`:60`) gives no general rule for a command passed both `--unattended` and `--interactive`. Only some rows say "refused". Add one sentence.
- **m-02 (minor).** §1.4 (`:42`) says "The evidence supports the decision", while gap 1 (`:43`) says no command has run end to end as a worker. Say "supports the decision as a hypothesis to test in P0".
- **m-03 (minor).** Non-goal 3 (`specs/orca-worker-contract-spec.md:215`) cites `CAPS:12-13` for the coordinator following Orca's guide, but those lines are the source-key table, not the guide's coordinator text. Cite the guide lines (`CAPS:9-14`, the `[G:coordinator-loop]` entries) instead.

## Follow-up candidates (Medium and minor, not blocking)

F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-15, m-01, m-02, m-03. The session that ran this review asks the user once whether to open an issue for them; none is created without the user's answer.

## Decisions made by this reviewer

| Decision | Options | Rationale |
|---|---|---|
| Finding ids | Sequential by bucket vs by severity | Ids assigned in order of discovery within each bucket, so the re-review table can cite them. |
| Grading of F-03 | Medium vs blocking | Blocking: SA-3 and §3.1 are two stated texts that contradict each other. The consequence is small, but the grading check requires blocking for a contradiction. |
| Grading of F-06 | Medium vs blocking | Blocking: WC-11 forbids the outcome and §3.1 lists the commands as ready with no serialisation rule, so data loss is the stated outcome. |
| Guard table | Omit vs full | Included: the candidate contains conditional rules, so the mandatory table applies (FR-8 to FR-10). |

## Reviser brief

Blocking finding ids: F-01, F-02, F-03, F-04, F-05, F-06.

Restated rule (review-loop bullet 6): the reviser revises only text a blocking finding names; adds no rule, mechanism or section no blocking finding calls for; cites the finding id on each added paragraph or table; prefers deleting or narrowing to adding; and reports the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings are not part of this brief and must not be edited.

verdict: FAIL
