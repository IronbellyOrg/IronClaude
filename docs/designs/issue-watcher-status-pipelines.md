# Issue watcher: per-status commands, launch levels and completion

**Status:** design note, decided 2026-11-19 (Task 6 of the zero-setup plan `TASK-WF-requirements-20261119-143917-2`). It records the owner's decisions of 2026-11-18 and 2026-11-19 (requirements R23, R24, R25, R29, R31, R32, R33, R34 and R35) and fixes every interface that Tasks 7 to 14 implement. Where a line of code or text is named, it was read on 2026-11-19.

Terms: the **Status** is the Project 2 single-select field `Status`; the **Pipeline** is its single-select field `Pipeline` (`None`, `Worktree`, `Full`, `Full Submit`); the **stage** is the word the watcher derives from the Status (`research`, `spec`, `plan`, `debug`); the **level** is the launch level derived from the Pipeline (`none`, `worktree`, `full`, `full submit`). The **approval** is the issue field `Approved` set to `Yes` (R35, `docs/designs/issue-watcher.md`).

## 1. What acts and what does not (R22, Task 1)

Only an issue whose one live Project item has Status `Research`, `Spec`, `Plan` or `Debug` acts (`predicates.ALLOWED_STATUSES`). `Backlog`, `Ready`, `In progress`, `In review`, `Done`, an empty Status and any status added to the board later never act. **Ready triggers nothing**: no command, no launch.

The Pipeline picks the level: `None` or empty is level `none`, `Worktree` is `worktree`, `Full` is `full`, `Full Submit` is `full submit`. The ship gate of Task 8 was opened by a reviewed commit (2026-11-25), so every level launches; if `GOVERNED_LEVELS_ALLOWED` is set back to `False`, only level `none` launches and every other level ends `level_gated`.

## 2. The decision table

All four Status pipelines end at **`In review`** (owner, 2026-11-19; held in one named table in `complete.py`, Task 12). Only a `succeeded` outcome moves the Status.

| Status | Command at the stage | Runs as the coordinator's worker? (level `none`) | Level `none` | Level `worktree` | Level `full` | Level `full submit` | End Status |
|---|---|---|---|---|---|---|---|
| Research | `/sc:research` | Yes: `src/superclaude/commands/research.md:117` has `## Unattended mode` | worker runs it unattended and reports | agent runs it, writes the report in the issue's worktree, halts, no commit | as `worktree` plus one local commit of the report on the issue branch | as `full` plus push of that branch to `origin` and `/sc:pr-submit --monitor 3` | In review |
| Spec | `/sc:design` when the issue is well defined, else `/sc:brainstorm` with a handoff to `/sc:design` for high complexity or scope | Yes: `design.md:117` and `brainstorm.md:148` | as above | as above | as above | as above | In review |
| Plan | `/sc:workflow` | Yes: `workflow.md:80` | as above; stops before `/sc:implement` and `/task` | as above | as above | as above | In review |
| Debug | `/sc:troubleshoot` | Yes: `troubleshoot.md:169` | worker runs it **without `--fix`** | agent runs it **without `--fix`** (propose next steps, halt) | agent runs it **with `--fix`** (a remediation tasklist package, never an applied code change) | as `full` plus push and PR | In review |
| Ready | none | not applicable | nothing | nothing | nothing | nothing | unchanged |

None of the five commands is on the never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep`, `/sc:swarm-wizard`, and `/sc:pr-submit` while decision D3 holds). Each has an `## Unattended mode` section at the line shown, so no alternative is needed. `/sc:pr-submit` is never a worker command: at level `full submit` the launched agent runs it in its own top-level session, as D3 allows.

**Debug at level `none`.** The coordinator's worker runs `/sc:troubleshoot` without `--fix`, because a level `none` worker stops before any code change; code-affecting remediation starts only at `full` and `full submit`. The worker brief is used only at level `none`; at the other levels the launched agent runs the command from its launch prompt, so the brief has no level slot.

**What `--fix` does.** `src/superclaude/commands/troubleshoot.md:54`: `--fix` offers the Tier 3 remediation chain (`/sc:workflow` produces a tasklist package; the user runs `/sc:implement`); code changes never auto-apply. At `full` the agent therefore leaves a remediation package, not a code change.

## 3. The launch prompt (decision 1)

The watcher sends one of these prompts to `orca agent launch --prompt`. The stage is derived from the Status read by `_revalidate`; the level from the Pipeline.

| Level | Prompt for stage `research` (the others replace the last word) |
|---|---|
| none | `/sc:issue --claim <N> --pipeline none --stage research` |
| worktree | `/sc:issue --claim <N> --pipeline worktree --stage research` |
| full | `/sc:issue --claim <N> --pipeline full --stage research` |
| full submit | `/sc:issue --claim <N> --pipeline full --submit --stage research` |

Stages: `research`, `spec`, `plan`, `debug`. `--stage` is a new claim-only option of `/sc:issue` (Task 10); `--submit` stays valid only after `--pipeline full`. The launch-level guard has no prompt allow-list, so the pin is the pattern in `launch.py`, which replaces `PROMPT_PATTERN` (line 33):

```
^/sc:issue --claim [1-9][0-9]{0,8} --pipeline (?:none|worktree|full(?: --submit)?) --stage (?:research|spec|plan|debug)$
```

`build_claim_prompt` (line 84) takes the issue number, the stage and the level and raises `ValueError` for any input that does not match, so no other text reaches `--prompt`. `launch_argv` (line 95) and `retry_argv` (line 119) keep refusing a prompt that does not fullmatch the pattern. The prompt is built from the item that `_revalidate` rereads (Task 7), so a Status or Pipeline moved between examine and launch cannot launch the old command.

## 4. Which session runs the Status command (decision 3)

- **Level `none`.** The watcher's claim session assigns the issue, posts its two marked comments and writes `.dev/issues/<N>/issue-summary.md` and `next-steps.md`; it creates no worktree and starts no agent. The coordinator then reads the claim's stage, creates the worktree and starts one worker from the worker brief, whose `Command:` line carries the stage's command (section 7).
- **Levels `worktree`, `full`, `full submit`.** `/sc:issue --claim` creates the worktree and launches an agent in it. The stage command enters the agent's `launch-prompt.md` (written by the claim from `templates/next-steps.md`, Task 10): its first step is the stage command in the form of the table above, its last step is writing `.dev/issues/<N>/result.md`, and it states that only the coordinator writes to an issue, a label or a Project (section 8). The agent runs the command from that prompt.

## 5. How the Status and Pipeline reach the coordinator (decision 4)

A `--pipeline none` claim writes no worktree record. The watcher stores the stage and the level in the claim's `.dev/issues/<N>/next-steps.md` header lines (`stage: <word>` and `level: <word>`) next to the existing summary, and the coordinator reads them there, in the checkout that ran the claim, with the `claimed` entry of `dispatch.json` read-only. The coordinator never trusts a Status it remembers: it rereads the Project item through `stage-status` at each gate, which also reads the approval and the plan reply.

## 6. "Well defined" for Spec (decision 5)

The claim worker that writes `issue-summary.md` judges it, from the Complexity issue field and the summary text: `Simple` or `Medium` with a stated acceptance criterion is well defined (`/sc:design`); anything else, or `Complex`, is not (`/sc:brainstorm`, with a handoff to `/sc:design` for high complexity or scope). It records the verdict and the reason in one line of `issue-summary.md` (`spec-route: design|brainstorm — <reason>`). No code judges it and no issue text reaches the brief.

## 7. The worker brief (levels `none` only)

`src/superclaude/cli/issue_pipeline/templates/worker-brief.txt` and `brief.py` carry one row per allowed Status instead of one row per complexity. The brief's `Command:` line is the command of the Status (the table), built from a closed template; the issue number is a validated integer and the Status a closed set, so no issue text reaches the brief. The brief states that `In review` fails the project check, so after the coordinator's move to `In review` a relaunch needs the owner to move the Status back to an allowed value (section 9). `brief.py` keeps the closed-set checks and refuses a bad Status, issue number or nonce with a closed reason. The Debug row at `none` has no `--fix`.

## 8. The approval record (decision 6, R19, R29, R35)

"Automatic approval record" of R19 means the **claim-time approval already kept in `dispatch.json`** (`approver_id`, `approval_event_id`, `approved_at`, now taken from the `Approved` field event) plus the **adoption row** (`adopt-create`). It is not the plan-hash approval row. The plan-hash row (`approval_record.py`, `record_create`) is created only from a worker's `ask` that carries the plan hash (WC-17, R29). A claim-time event is refused as plan approval in `src/superclaude/cli/issue_pipeline/stage_predicates.py` (rule `label-before-plan`, lines 161 to 170, through `stage-status`), because `approval_record.record_create` cannot tell the two events apart and is not changed. The coordinator calls `record-create` only with evidence that `stage-status` reports as accepted. Task 11 tests this where it is enforced, in `tests/issue_pipeline/test_stage_predicates.py` and `test_stage_status.py`.

## 9. The completion update (R24, decision 7)

Only the coordinator writes to an issue, a label or a Project item, and only under that issue's grant row (`WORKER-CONTRACT.md` lines 241 to 243 and 300). An agent launched at any level and every worker reports through its result file and never runs `issue-pipeline complete`.

- **How the coordinator learns a run finished.** At level `none`: the worker's `worker_done` contract. At the other levels: the result file `.dev/issues/<N>/result.md` in the issue's worktree, noticed by the `/sc:sweep` report the coordinator already reads at each wake (WC-16).
- **Closed format of `result.md`.** Three lines, no free text: `outcome: succeeded|failed|blocked|partial`, `artifacts: <repo-relative paths, comma separated, may be empty>`, `pull_request: <number or none>`. The coordinator reads only these three keys; nothing else of the file is posted. The run id (the approval event id) is not in the file: the agent cannot know it and must not choose it, so the coordinator takes it from the issue's entry in `dispatch.json` (Task 10 amended this from four lines).
- **The result comment.** One comment per run, carrying the per-run marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->` and the outcome word, the artifact paths and the pull request number. The marker never contains the claim marker. The approval event id keys it, so a run started on a later approval has a different id; a marker already written by the coordinator's own login for the same run suppresses a second comment (idempotency).
- **Only `succeeded` moves the Status**, with a compare-and-set: the Status moves only from `Research`, `Spec`, `Plan` or `Debug`; any other current Status (for example a person moved it to `Done`) posts the comment and returns `status_moved_by_person` without a move. A `failed`, `blocked` or `partial` outcome posts the comment only. The end Status comes from one table keyed by the allowed Status (all four `In review`), so an exception is a one-line change. The read then write is not atomic; the module says so.
- **Effect on the approval.** The coordinator's own comment never voids an approval (comments by the watcher's own login are skipped, `predicates.py` `unchanged_since`). Its move to `In review` no longer voids the approval (R36 withdrew R31, 2026-11-20); `In review` still fails `project_check`, so a relaunch needs the owner to move the Status back to an allowed value. The same holds for the coordinator's mirror of the Status at line 298 of the duties.

## 10. The Full Submit push rule (decision 8)

`WORKER-CONTRACT.md` line 245 gets this sentence in place of the current one: "At Full Submit the launched agent pushes only its own feature branch to origin and opens the pull request through /sc:pr-submit; the owner's Pipeline value plus an approval in the `Approved` field is the go for that issue only. The coordinator never pushes worker commits on that basis; for every other push the rule above stands." Task 11 applies it and tests that no coordinator push grant is tied to the Pipeline.

## 11. Which sessions the guard governs (decision 10)

Governed means a session with a record in the launch-level store: the agents launched at `worktree`, `full` and `full submit`, and bound workers. Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design; it reads untrusted issue text under the launch login. The counted marker login is the **workspace's single `gh` login**, shared by the watcher, the coordinator and launched agents; the guard (Task 13) is a text check on `gh` commands and cannot tell them apart by login, so the complete control is a token without issues or projects write for launched agents (a Coder row, Task 27).

## 12. Files that change in Tasks 7 to 14 (by path)

| Task | Files |
|---|---|
| 7 | `src/superclaude/cli/issue_watch/launch.py`, `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/predicates.py`, and the seven test files `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_crash_injection.py`, `test_cycle.py`, `test_launch.py`, `test_no_text.py`, `test_security_invariants.py` |
| 8 | `src/superclaude/cli/issue_watch/launch.py`, `cycle.py`, `audit.py`, `tests/hooks/test_launch_level_observations.py`, `tests/issue_watch/test_cycle.py`, `test_audit.py` |
| 9 | `src/superclaude/cli/issue_watch/predicates.py`, `cycle.py`, `cli.py`, tests under `tests/issue_watch/` |
| 10 | `src/superclaude/commands/issue.md`, `src/superclaude/skills/sc-issue-protocol/SKILL.md`, `refs/claim.md`, `templates/next-steps.md`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, and the docs that quote the old prompt |
| 11 | `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt`, `brief.py`, `tests/skills/test_worker_contract.py`, `tests/issue_pipeline/test_brief.py`, `test_stage_predicates.py`, `test_stage_status.py` |
| 12 | `src/superclaude/cli/issue_pipeline/complete.py` (new), `tests/issue_pipeline/test_complete.py` (new), `tests/issue_watch/test_security_invariants.py` |
| 13 | `src/superclaude/hooks/scripts/launch-level-guard.sh`, `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, the guard and issue-worktree tests |
| 14 | `src/superclaude/cli/issue_pipeline/cli.py`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/issue_pipeline/test_complete_cli.py` (new), `tests/skills/test_worker_contract.py` |

## 13. Ship-gate note (Task 8)

`docs/designs/sc-issue-launch-level-hook.md` line 201 limits observation item 1 to `full` and `--submit`, while `refs/claim.md` line 133 asks for an observation of item 1 before any governed claim. One boolean, `GOVERNED_LEVELS_ALLOWED`, follows the stricter text (no governed level launches until the observations pass). Owner decision 2026-11-24 and 25: one boolean for all levels, and the gate also waits for OB-CTX. The gate was opened on 2026-11-25 after OB-H1 items 1 and 5, OB-H2, OB-H3 and OB-CTX passed; what was not observed is listed in `docs/designs/sc-issue-launch-level-hook.md` section 19.8. A per-level split is not built.
