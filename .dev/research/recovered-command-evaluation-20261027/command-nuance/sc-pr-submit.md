# /sc:pr-submit: scope x complexity nuance

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Read-only analysis; no command was run.
Sources read in full: CMD = `/home/coder/.claude/commands/sc/pr-submit.md` (90 lines); SKILL = `/home/coder/.claude/skills/sc-pr-submit-protocol/SKILL.md` (246 lines); all 11 refs under `.../sc-pr-submit-protocol/refs/` (cited `refs/<name>`); script headers under `.../scripts/`. Also read, to answer the run-log question: the installed core `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/pr_submit/` (cited `run_log.py`, `fsm.py`; `run_log.py` is byte-identical to `/home/coder/workspaces/IronClaude/src/superclaude/pr_submit/run_log.py`, `fsm.py` is not) and 8 real run logs under `/home/coder/workspaces/Coder/.dev/plans/top9-issues-20261001/*/pr-monitor/`.
The backing protocol skill EXISTS (`~/.claude/skills/sc-pr-submit-protocol/`).

## 1. Status and role
- Does: "Open a PR on the fork and arm an in-session PR-review auto-remediation monitor" (CMD:3). Phase: Commit / Push / PR (the last step of every pipeline). Standalone-invokable, explicit only (CMD:16-20); not retired. It never refers to `/sc:task` or `/sc:tasklist` (grep of CMD and the whole skill folder: no hit).
- Overlaps: `/sc:auggie-review` (sibling; pr-submit also calls it once as a decline fallback, SKILL:196), `/sc:troubleshoot` (called per verified finding, CMD:90), `/code-review` / `bmad-code-review` (local review before the PR), plain `gh pr create` (identical to `--monitor 0` on GitHub).
- Correction to the brief's wording "push with `/sc:pr-submit`": the command OPENS the PR (SKILL:189). It does not push the engineer's branch; the only push it can make is a remediation push at `--monitor 3` (SKILL:195). HOW-WE-WORK has the engineer push first, then run it (`HOW-WE-WORK.md:202-204`).

## 2. Flags
### 2a. The `--monitor` levels: what each does to code, repo, GitHub, disk

`--monitor` is a capability ceiling on ONE state machine, compared at three gates (arm >= 1, edit >= 2, push >= 3) plus one override (`needs_human_decision` halts at any level) (SKILL:26-27; `refs/state-machine.md:58-81`; `fsm.py:139-146`). Default is 2 (CMD:47; `fsm.py:30`). HOW-WE-WORK says "always pass `--monitor 1`" (`HOW-WE-WORK.md:254`).

| Level | What it does (cited) | Product code | Local git | GitHub | Disk |
|---|---|---|---|---|---|
| 0 | Opens the PR on the origin repo and returns; FSM never leaves idle; no polling, no CI wait (SKILL:189, SKILL:198; `refs/state-machine.md:23-25`) | untouched | untouched | PR only | none documented: the run log is initialised in Wave 1, an L1+ wave (SKILL:190; U2) |
| 1 | L0 + arms; polls for the Augment review; re-grades; verifies each finding with the read-only `evidence-validator`; diagnoses via `/sc:troubleshoot`; PROPOSES "fix these? y/n" and applies NO edits; then waits on CI (SKILL:190-193, 198; `fsm.py:41`) | untouched | untouched | PR only (polls are reads: `scripts/poll-augment-review.sh`, `scripts/poll-ci-checks.sh`) | run log + per-round dirs (see 2c); troubleshoot output (U4) |
| 2 (default) | L1 + the skill itself applies the diagnosed edits in the working tree, runs the validation gates, then HALTS before push: "no commit, no push, no reply" (SKILL:194; `refs/state-machine.md:83-94`) | EDITED in working tree | dirty tree, nothing committed | PR only, except possibly the oversized-PR fallback report (U6) | as L1 |
| 3 | L2 + commit/push to the PR head branch, reply on each finding thread, resolve it, post the `auggie review` re-trigger comment, re-poll; up to `--max-rounds` pushes; one silence re-request (SKILL:195, 198; `refs/thread-reply.md`; `refs/review-retrigger.md:24-35`) | EDITED and PUSHED | commits created (mechanism: U1) | commits on the branch, replies, resolved threads, trigger comments, summary comment | as L1 |

Push gate at L3 (all five must hold, recorded in a write-ahead `push_decision` event): ordinal >= 3; validation green; no `needs_human_decision`; `round_counter < max_rounds`; at least one applied edit (`refs/state-machine.md:145-164`). The first push of a run needs `--yes` or an interactive confirm unless non-interactive (`refs/state-machine.md:155-159`). Never pushes to an upstream parent or the default/protected branch (SKILL:225).

Time cost, derived (U13): the attended monitor blocks the session. At L1 the Augment wait and the CI wait each get a fresh `--timeout` clock (SKILL:198), so the worst case is about 2 x `--timeout` (default 20 minutes); each L3 cycle adds another re-review wait.

### 2b. Flags

| Flag | Values | Default | What it changes | Worth using | Avoid |
|---|---|---|---|---|---|
| `--monitor` | 0, 1, 2, 3 | 2 | The ceiling above (CMD:47; `fsm.py:75-77` rejects anything else) | 1 per the guide; 0 when the Augment app is not on the repo (`HOW-WE-WORK.md:205`) | 2 and 3 in this repo: see 2a and U5 (validation gates cannot run as written) |
| `--max-rounds` | int 0..5 | 2 | Cap on remediation cycles; `>= max_rounds` halts (`refs/loop-guard.md:10-28`); parser rejects >5 and <0 (`fsm.py:114-117`) | Only at L3 | Setting it at L0-L2: the counter ticks only at the re-review edge, which exists only after an L3 push (derived from `refs/loop-guard.md:22-23`, SKILL:195) |
| `--poll-interval` | seconds >= 30 | 30 | Sleep between polls; <30 is rejected, not rounded (SKILL:138; `fsm.py:110`) | 60 for long CI (all 8 observed runs used 60) | below 30 (rejected) |
| `--timeout` | seconds | 600 | Per-wait wall clock; the Augment wait and the CI wait each start a fresh clock (SKILL:139, 198). CI "has run longer than 600s" (SKILL:139; `refs/ci-poll.md:32`) | Size to the full CI run; 3600 and 7200 were used in the 8 observed runs | Leaving 600 when CI is a long matrix: ends `terminal_timeout` |
| `--silence-timeout` | seconds >= 30 | 300 | Window with no Augment activity before `terminal_augment_no_response`; clamped to `--timeout` (`fsm.py:112,123`). Only L3 may poke once (`refs/review-retrigger.md:30-35`) | Default | n/a |
| `--base` | branch | repo default branch | PR base (CMD:52) | Only when not targeting the default | n/a |
| `--head` | branch | none | PR head (CMD:53) | Always give it | n/a |
| `--title` / `--body` | text | none | PR title / body (CMD:54) | Always: the PR text is the one thing a checker reads on GitHub at L0/L1 | n/a |
| `--output-dir` | path | `<cwd>/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/` | Where the run log and artifacts go; overrides the default entirely (CMD:55; `run_log.py:282-295`) | When the run log must sit next to a task package | Assuming the default path: 8 of 8 observed logs used an explicit dir (see 2c) |
| `--resume` | path to `monitor-run-<N>.jsonl` | none | Rebuild state from the write-ahead log (CMD:56; SKILL:141) | After a crash or closed session | Expecting the monitor to survive a closed session by itself: it is attended and dies with the session (SKILL:33-35) |
| `--yes` | flag | off | First-push confirm bypass at L3 (`refs/state-machine.md:155-159`; `fsm.py:97`) | n/a | NOT in CMD's argument-hint or Options table, and not in SKILL's Required Input: it exists only in the core parser and one ref (U9) |

**Does not exist** (people may assume): `--fix` and `--depth` on this command (it only hands `--fix` / `--depth deep --fix` to troubleshoot and never `--depth quick --fix`, CMD:85, `refs/severity-routing.md:71-74`); `--repo` (repo is computed from origin and pinned internally, CMD:83; only the helper scripts take `--repo`); `--pr` (CMD:27 and SKILL:136 accept "an existing PR number" but name no flag for it, U10); `--draft`, `--reviewer`, `--label` (not in CMD:8); `--no-post-pr` (belongs to `/sc:auggie-review`; the fallback passes `--depth quick --remediation-offer` and must NOT pass `--no-post-pr`, `refs/auggie-fallback.md:28-35`); any daemon or background option (CMD:85, SKILL:33).

### 2c. Run log: where it lands (the earlier UNVERIFIED item)

- Default: `<cwd>/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/monitor-run-<N>.jsonl`, with `state.snapshot.json` beside it and `validation/round-<N>/`, `troubleshoot/round-<N>/` below (`run_log.py:77-82,285,295,299-300`; `refs/loop-guard.md:61-80`). `cwd` is the directory the command is run from, so in a worktree it is the worktree root (`run_log.py:287-289`). VERIFIED from source, not from a live default run: no `.dev/pr-monitor/pr-*` directory exists anywhere under `/home/coder/workspaces`.
- `--output-dir` replaces the whole default (`run_log.py:289-291`). The 8 real logs sit in `<plan-dir>/pr-monitor/monitor-run-<N>.jsonl` (plan dirs `closeout`, `i263`, `i269`, `cd-ci-exclude`, `orca-worktree-root`, ...), so a checker must glob `**/monitor-run-*.jsonl`, not rely on the default.
- Those 8 logs do NOT match the documented schema: they use key `event` (documented: `event_type`) and have no `schema_version`, `event_id` or `run_id` (grep count 0 in two of them; `refs/loop-guard.md:98-100`). A core `RunLog` writes `schema_version`/`event_id`/`event_type` (seen in a unit-test log, `/tmp/pytest-of-coder/pytest-21/test_rereview_count_and_auggie0/monitor-run-99.jsonl`). So the observed logs were written by hand or by a model following the skill loosely (U8). A checker should read a minimal common core: an `armed` line carrying `monitor`, and a last line whose `status` (or `event_type`) starts with `terminal`.
- Git status of the log: in this worktree `git check-ignore` on a default-shaped path returns not ignored, so a default log would show as untracked; `.dev/pr-monitor/detection-contract.locked.md` IS tracked here (commit `6a8e33f8`) although SKILL:190 calls it a gitignored override. `/home/coder/workspaces/IronClaude/.gitignore:246` ignores the whole `.dev/pr-monitor/`. The observed logs in `/home/coder/workspaces/Coder` are tracked (`git ls-files` lists them). CLAUDE.md requires `.dev/tasks/` staged; it says nothing about `.dev/pr-monitor/` or `.dev/plans/`.

## 3. Scope x complexity matrix
The command does not change WHETHER it runs with complexity: it is the PR step at every scope (existing table rates it REQUIRED in all six). Complexity changes the flag set, mainly `--timeout`, and what to expect from the bot. No file gives a threshold for these bands; all three are JUDGMENT, built from signals that do appear in files.

| Band | Signals (one line) |
|---|---|
| LOW (J) | Few files, one subsystem, no secrets, permissions, user input, paths or infra; CI fits the 600 s default timeout (SKILL:139) |
| MEDIUM (J) | Several files or one large subsystem; CI matrix can exceed 600 s (SKILL:139, `refs/ci-poll.md:32`) |
| HIGH (J) | Multi-subsystem or large diff, where Augment can decline an "abnormally large" PR and trigger the one-shot auggie fallback (`refs/auggie-fallback.md:13-19`, SKILL:196); OR risk paths (secrets, permissions, infra), given this repo's secrets incident (`CLAUDE.md` Secrets discipline) |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | REQUIRED `--monitor 1` (J; `--monitor 0` is fine, see rule below) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1` only when risk-driven (J); size-driven HIGH is N/A, re-scope to B or S |
| B bug fix | REQUIRED `--monitor 1` (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) |
| S single story | REQUIRED `--monitor 1` (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout <CI length>`; `/sc:auggie-review --no-post-pr` first (J) |
| F multi-story feature | N/A (J; a feature with several stories is not LOW) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout 3600` or more (J; 3600 and 7200 were used in observed runs); expect a decline and fallback (J) |
| R multi-feature release | N/A (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J) | REQUIRED `--monitor 1 --timeout 3600` or more (J); expect decline and fallback (J) |
| N new product | N/A (J) | REQUIRED `--monitor 1 --timeout <CI length>` (J; first PR small scaffold) | REQUIRED `--monitor 1 --timeout 3600` or more (J); or `--monitor 0` if the Augment app is not yet on the new repo (`HOW-WE-WORK.md:205`) |

Level choice, all scopes and bands:

| Level | Rating | Why |
|---|---|---|
| `--monitor 0` | OPTIONAL | Guide's own fallback when the app is absent or unsure (`HOW-WE-WORK.md:205`); equal to a plain PR on GitHub |
| `--monitor 1` | REQUIRED as the baseline | Guide: "Always pass `--monitor 1`" (`HOW-WE-WORK.md:254`, step 6 at :204) |
| `--monitor 2` | SKIP (J) | It is the command default, so omitting the flag silently edits code (`HOW-WE-WORK.md:254`); leaves an uncommitted dirty tree; validation gates are repo-specific (U5) |
| `--monitor 3` | SKIP (J) | Autonomous push, reply, resolve on the engineer's identity; the guide never recommends it. Observed use was 8 of 8 runs at `monitor` 3 in `/home/coder/workspaces/Coder` (see 5), so the guide is not what happens in practice |

Flag by complexity: `--timeout` grows with MEDIUM and HIGH (size to CI, not to the diff). `--poll-interval` 60 for MEDIUM/HIGH (J; observed practice). `--max-rounds` and `--silence-timeout` matter only at L3, so they are irrelevant at the recommended level. `--base` only for a non-default target. `--output-dir` only when a checker or task package needs the log in a known place.

## 4. Choose this or the neighbour
| Neighbour | Decision rule by signal | Cited |
|---|---|---|
| plain `gh pr create` / web UI | Same as `--monitor 0` on GitHub. Prefer `/sc:pr-submit` because it pins `--repo` to origin and halts on a misrouted PR (a CLI that defaulted to an upstream parent). Plain `gh` is acceptable when the engineer only wants a PR and no monitor | CMD:83; SKILL:143-146, 189 |
| `/sc:auggie-review` | Different timing. auggie-review runs BEFORE the PR on the local diff (`--diff origin/<main>...HEAD --no-post-pr`); pr-submit runs AFTER the PR exists and waits for the Augment App. For HIGH complexity (large diff) run auggie-review first, because the App may decline an oversized PR. pr-submit calls auggie-review itself once, only on a decline, and only described for L2+ (L1: U3) | `HOW-WE-WORK.md:201`; SKILL:196; `refs/auggie-fallback.md` |
| `/code-review`, `bmad-code-review` | Not replaced. They run locally before the push; pr-submit checks the bot's findings after. `HOW-WE-WORK.md:198-205` lists code-review (step 2) before pr-submit (step 6) | `HOW-WE-WORK.md:198-205` |
| `/sc:troubleshoot` | pr-submit calls it per VERIFIED finding at L1+ for diagnosis; the engineer does not run troubleshoot on bot findings by hand. For a bug that did not come from a PR review, use troubleshoot directly (pipeline "bugs and issues via /sc:troubleshoot") | `refs/troubleshoot-dispatch.md:9-24`; brief ruling 5 |
| `/sc:git` | `/sc:git` commits. pr-submit commits only at L3 (mechanism U1) and never at L0-L2 | SKILL:194-195 |
| `/sc:task`, `/sc:tasklist` | Retired. No relation: pr-submit never calls either (no grep hit) | grep of CMD and skill folder |

## 5. What a scheduled checker can see
Key point: at L0 and L1 the monitor posts nothing to GitHub (polls are reads, replies and re-triggers are L3 only, SKILL:195), so a PR opened with `--monitor 0`, `--monitor 1` or plain `gh pr create` looks the same on GitHub. The Augment review itself is posted by the App on PR-open whatever the engineer did (`refs/review-retrigger.md:3-6`), so a bot review on the PR is not evidence the command ran. The command adds no label, body footer or marker that any file documents (U12).

| Level | On GitHub | On disk | In the session |
|---|---|---|---|
| 0 | The PR (title, body, head, base). Nothing else | Nothing documented (U2) | Command invocation in the transcript only |
| 1 | Same as 0 | Run log and `state.snapshot.json`; `validation/` and `troubleshoot/` round dirs; possibly troubleshoot artifacts (U4) | Transcript shows polling and the `fix these? y/n` proposal (`fsm.py:41`) |
| 2 | Same as 0 (fallback report: U6) | As 1, plus a dirty working tree with modified product files and no new commit | Transcript shows edits and the validation run |
| 3 | After PR-open: new commits on the head branch (at most `max_rounds`, plus one for the fallback, `refs/loop-guard.md:43-47`); reply comments on Augment threads saying fix + SHA + validation, or "no code change applied" (`refs/thread-reply.md:17-20`); threads resolved; `suggestion` blocks on trivial fixes (`:22-28`); issue comments with body `auggie review` (`refs/review-retrigger.md:24`) or one `augment review` silence poke (`:30-35`); one summary comment (`refs/thread-reply.md:85-88`); fresh CI runs per push | As 1, with `push_decision` / `push_initiated` / `push_completed` events when the core RunLog is used (`refs/state-machine.md:155-157`, SKILL:195) | Transcript |

Run-log fields to read, minimal and tolerant of the two shapes (2c): monitor level (`armed.monitor`), final `status` (`terminal_clean`, `terminal_max_rounds`, `terminal_halted`, `terminal_timeout`, `terminal_augment_no_response`, `terminal_failed`, `proposed`, `halt_before_push`, SKILL:159), and counters `round_counter`, `push_count`, `reply_count`, `applied_edits`, `rereview_request_count` (SKILL:155-170). `terminal_augment_no_response` means the App stayed silent (check its trigger mode, allowlist, quota; SKILL:236); it is not a clean review (CMD:58). Observed: all 8 logs end `terminal_clean` or `terminal_max_rounds`; three show `push_count` 1 with `round_counter` 0 (PRs 285, 289, 292).

Locator: glob `**/monitor-run-*.jsonl`, because `--output-dir` moves it (2c). The detection contract file `.dev/pr-monitor/detection-contract.locked.md` is tracked in this repo and is NOT a run log.
Hook: CMD:19 and SKILL:189 describe an `offer-pr-review.sh` hook that mentions `/sc:pr-submit --monitor` after `gh pr create`. It is not present in `/home/coder/.claude/hooks/` and `find /` finds no such file (U7); a checker must not rely on it.

## 6. Expected-step rule
- Expected: exactly once per branch that is shipped, as the last step of the pipeline, at every scope and band (existing table: REQUIRED in all six scopes; unchanged by complexity, only the flags change). Count it as done when a PR exists for the branch AND the engineer either ran the command or the PR is equivalent to `--monitor 0` (plain `gh pr create` or the web UI). Because `--monitor 0` and `--monitor 1` leave no GitHub footprint beyond the PR (section 5), the checker should NOT flag a missing run log or a missing monitor when a PR exists (J).
- Absence is fine: nothing is shipped yet (local-only work); the Augment app is not installed so `--monitor 0` is used (`HOW-WE-WORK.md:205`); a PR opened through the UI. Not skipped steps: `terminal_timeout`, `terminal_augment_no_response`, `halt_before_push`, `proposed` are outcomes, not omissions (SKILL:159). Worth a separate "deviates from guide" note, not a skipped-step flag: `--monitor 2` or `3` (guide says 1, `HOW-WE-WORK.md:254`).

## 7. Proposed changes to command-value-by-phase.md
All proposals; `command-value-by-phase.md` is not edited. Line numbers are from that file as read on 2026-10-27.

| Where | Current text | Proposed text |
|---|---|---|
| Line 167, `/sc:pr-submit` row, T/B/S/F columns | REQUIRED (x4) | REQUIRED (x4), unchanged. Complexity changes flags, not the rating |
| Line 167, R column | REQUIRED | REQUIRED, rating unchanged under the multi-feature definition. Reason: it was already REQUIRED and a multi-feature release is HIGH complexity by definition; what changes is the Notes (below). R re-rated: no rating change |
| Line 167, N column | REQUIRED | REQUIRED, unchanged; add "`--monitor 0` until the Augment app is on the new repo" |
| Line 167, Notes | "Ryan's pipeline step 4. Always pass `--monitor 1` (default is 2, which edits code; 3 pushes). Needs `gh` logged in and the Augment review app; app presence is UNVERIFIED, else `--monitor 0`" | "Ryan's pipeline step 4. Opens the PR; it does not push your branch, push first. Always pass `--monitor 1` (default 2 edits code and leaves a dirty tree; 3 also commits, pushes, replies and resolves threads). At 0 and 1 only the PR appears on GitHub. Size `--timeout` to the CI run (default 600 s, observed CI is longer); on F, R, N expect Augment to decline an oversized PR. Needs `gh` and the Augment app; app presence: indirect evidence only (run log for PR 286 polled `review_present`), else `--monitor 0`" |
| Line 273, checker footprint | "the PR itself; a `run-log.jsonl` exists (`--resume` flag), its location is UNVERIFIED" | "L0/L1: the PR itself, indistinguishable from a plain `gh pr create`. L1+: `monitor-run-<N>.jsonl`; default `<cwd>/.dev/pr-monitor/pr-<N>-<timestamp>/` (`run_log.py:282-295`), but `--output-dir` moves it, so glob `**/monitor-run-*.jsonl`. L3 also: extra commits, replies, resolved threads, `auggie review` comments" |
| Line 288, U4 (Augment app installed) | "Guide says `/sc:pr-submit --monitor 1` needs it; ... result is inconclusive" | Add: "indirect evidence: run log `/home/coder/workspaces/Coder/.dev/plans/top9-issues-20261001/closeout/pr-monitor/monitor-run-286.jsonl` shows an Augment poll reaching `review_present` on 2026-10-02; the tracked `.dev/pr-monitor/detection-contract.locked.md` lists the Augment identities. Still not confirmed in repo Settings" |
| Line 297, U13 | "Post-mode output folder of `/sc:reflect` and location of the `/sc:pr-submit` run log" | Split. pr-submit part answered from source (default path above; `--output-dir` override; observed logs use an explicit dir). Not observed from a live default run |
| Line 256, Release scenario step 3 | "`/sc:pr-submit --monitor 1`" | "`/sc:pr-submit --monitor 1 --timeout 3600`" (J: size to CI) |
| Line 254 and 253 etc., the other scenario rows | `/sc:pr-submit --monitor 1` | unchanged |

## 8. Unverified items
| ID | Item | What was checked / how to resolve |
|---|---|---|
| U1 | Who creates the commit at L3, with what author and message | SKILL:195 names only `git push origin <target_sha>:<target_branch>` and replies citing "commit SHA"; no commit step is written. Resolve by reading `src/superclaude/pr_submit` callers or one L3 run |
| U2 | Whether L0 writes any run log | SKILL:189 says FSM never leaves idle; SKILL:190 initialises the log in Wave 1 (L1+). Not stated for L0 |
| U3 | What L1 does when Augment declines an oversized PR | SKILL:196 labels Wave 6b "L2+"; `refs/state-machine.md:108-111` edges are not ordinal-gated in text |
| U4 | Whether the L1 troubleshoot dispatch, which carries `--fix` (`refs/troubleshoot-dispatch.md:19-24`), triggers troubleshoot's plan route and leaves a `.dev/tasks/to-do/<id>/` package plus `remediation-source.md` in the engineer's repo (`sc-troubleshoot-protocol/refs/remediation-handoff.md:11,75,109`). pr-submit says it uses troubleshoot "for diagnosis" only (`refs/troubleshoot-dispatch.md:44-49`). Matters because CLAUDE.md says `.dev/tasks` is always staged |
| U5 | Whether the validation gates run in this repo: VG-1..VG-5 are `uv run pytest`, `make test`, `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync` (SKILL:205-209); the Coder worktree has no `Makefile`, `pyproject.toml`, `src/` or `tests/`. So predicate 2 of the push gate (validation green) cannot be met as written, which would block an L3 push (derived) unless the model improvises. Observed runs pushed anyway (PRs 285, 289, 292) |
| U6 | Whether the L2+ oversized-PR fallback posts the auggie-review report to the PR: `refs/auggie-fallback.md:35` says the report is auto-posted; SKILL:196 says L2 halts before push/reply and does not mention this post |
| U7 | The `offer-pr-review.sh` hook (CMD:19, SKILL:189) is not installed on this machine (`find /` and `~/.claude/hooks` listing); engineers' machines unknown |
| U8 | Provenance of the 8 observed logs: their shape differs from the documented schema, so they were not written by the core `RunLog`. Not confirmed who or what wrote them |
| U9 | `--yes`: in the core parser (`fsm.py:97`) and `refs/state-machine.md:155-159`, absent from CMD:8,45-56 and SKILL:133-141. Whether the command layer passes it through is unverified |
| U10 | How to attach to an existing PR: CMD:27 and SKILL:136 allow "an existing PR number" but define no flag |
| U11 | Augment app installed on `IronbellyOrg/Coder`: indirect evidence only (observed log for PR 286; tracked contract file). No Settings page or API check done (read-only rule) |
| U12 | Any marker (label, footer, body text) that pr-submit adds to the PR: none documented in CMD, SKILL or refs; a live run would settle it. Also the exact form of the command in the session transcript is unobserved |
| U13 | The 2 x `--timeout` worst-case blocking time is derived from SKILL:198 ("reset wait elapsed"), not stated in any file |
