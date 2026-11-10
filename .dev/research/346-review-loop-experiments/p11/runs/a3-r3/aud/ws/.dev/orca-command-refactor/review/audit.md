review: 1 of 3

# /sc:spec-panel audit: Orca worker-contract spec

| Header field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Kind of run | Labelled whole-document audit of the final spec. A first review of the whole document, per the FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full before reviewing). |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate sha256 | `0af4c9147b1078d164edae3da1719df0954c532ee06138e07f894bc91e1ab096` |
| Baseline / prior | not given (no `--re-review`, no `--baseline`); `--iterations` not given, so one review whatever the Iteration themes say (`command.md:261`) |
| Reviewer model actually used | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Date | 2026-11-10 |
| Brief clauses overridden | none |

Citation shorthand (the spec's own): `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = line N of `.dev/orca-command-refactor/README.md`. `command.md:N` = the command definition given to this audit.

## Coverage (what was and was not checked)

- Read in full: the candidate, `README.md`, all three inventories, `command.md`, the review-loop prompts file.
- Checked against a file inside the workspace: every `INV-A:N`, `INV-B:N`, `CAPS:N` and `README:N` citation in section 3, 4, 1 and 8 of the candidate that I sampled (all rows of 3.1, 3.2 and 4; E1-E6; R1-R5; WC-1 to WC-12 evidence cells). Every inventory line cited points at the content the spec says. The 10 / 27 / 6 split, the 21 + 22 = 43 total and the phase counts conserve (see the Quantity Flow Diagram).
- UNVERIFIED (no such file in the sandbox): every `cmd/`, `sk/`, `ag/` path:line, `CLAUDE.md:N`, `src/superclaude/core/...`, `.dev/codegraph-migration/...`, `.dev/evals/.../EVIDENCE.md` (read only where the capabilities inventory quotes it, `CAPS:49,52`), `Makefile`, `pyproject.toml`, `install_core.py`. SPEC:25 (the `grep -rlni orca` result) and SPEC:285 (the 340-citation check) are also UNVERIFIED here. I used the inventories' restatement of those lines and nothing else.
- Not run: no command, no Orca call, no test.
- Improve step: not run. This is a first-review critique, the spec-panel boundary forbids modifying a specification without consent (`command.md:479`), and the brief assigns only this file. No revised specification was written.
- Follow-up issue question (`command.md:260`): not asked. This worker may reply only `DONE <path>`, so the coordinator's session should ask the user once whether to open an issue for the follow-up candidates below. No issue was created.

## Verdict summary

Two blocking findings (F-1, F-2). Thirteen Medium warnings and seven minor notes are listed under follow-up candidates and do not fail the review.

| Metric (0-10) | Score | Why |
|---|---|---|
| Clarity | 7 | Section 1 and the per-command tables are precise; WC-4 and section 6 P1 are the exceptions. |
| Completeness | 6 | Every command has a row; several rows leave the answer path, the report path or the retry bound unstated. |
| Testability | 6 | Strong per-phase checks; WC-1, WC-3, WC-6 and WC-12 have none, and two checks cannot pass as written. |
| Consistency | 5 | Two cross-section contradictions (F-1, F-2). |

Panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (always active, review order 6); Crispin (boundary-table completeness). Gregory and Hightower were not selected by the two focus areas and have no findings.

---

=== REQUIREMENTS ANALYSIS ===

### F-1 [CRITICAL, blocking] Phase 1 gives 36 commands the `--unattended` flag but only 14 get their gate and outward-action rules there

- Expert: Wiegers (lead), Adzic (scenario), Whittaker (sequence attack). Priority: High. Quality impact: Consistency -2, safety boundary.
- Locations: `SPEC:159` (P1 row), `SPEC:195` (AC-1.1), `SPEC:154` and `SPEC:225` (Phases 1-3 need no user decision), `SPEC:60` (WC-2), `SPEC:67` (WC-9), `SPEC:100`, `SPEC:113`, `SPEC:114`, `SPEC:109` (rows assigned to P2 and P4), `SPEC:240` (D3 recommendation), `SPEC:73` (the brief always passes `--unattended`).
- Grading sentence: An implementer who follows section 6 P1 and AC-1.1 as written gives every command in 3.1 and 3.2 except `/sc:load` the `--unattended` flag and the `## Unattended mode` section in Phase 1, while the rows for auggie-review, cleanup, task, post-release, pr-submit, implement and 15 others schedule their gate and outward-action resolutions for P2 to P4; that is wrong because WC-2 and WC-9 define `--unattended` as "never blocks on a person" and "every outward default is off", so a coordinator that follows `SPEC:73` and passes `--unattended` after P1 gets a command that still posts or still waits.
- Scenario (Adzic, with state trace):
  - Given P1 is complete, so AC-1.1 passes and `/sc:auggie-review` accepts `--unattended`, with the `--no-post-pr` implication still a P2 item (`SPEC:100`).
  - When the coordinator briefs `/sc:auggie-review 123 --unattended --output-dir D` (`SPEC:73`).
  - Then the command still posts `gh pr review --comment` plus inline comments with "No confirmation prompt" (`INV-A:38`), which `SPEC:67` says must be off. Before: 0 comments on the PR. After: review and inline comments posted.
  - Same trace for `/sc:post-release <v> --unattended` (VM, install, commit and PR confirmations remain, `INV-B:79,84`) and for `/sc:pr-submit --unattended`, which D3(a) (`SPEC:240`, "no pr-submit changes in Phase 4") may leave as a coordinator-only command, yet P1 has already changed it.
- Quantity check (FR-19): 36 commands flagged after P1, 14 behaviour-complete (8 no-gate P1 commands, 4 ready commands with P1 fixes, brainstorm, init-lite), 22 pending (15 P2, 4 P3, 3 P4). See the diagram below.
- Why the other reading does not rescue it: if "P1 writes each section with its full gate rules", the P2, P3 and P4 columns of `SPEC:97-125` and the claim that Phase 4 waits for D2-D4 (`SPEC:154`) no longer describe anything.
- Recommendation (narrow, no new rule): make the P1 scope and AC-1.1 match the rows. A command accepts `--unattended` and gets its section in the phase named in its own row (3.1 rows: P1 for the 10, with the P2 fixes landing in P2; 3.2 rows: the Phase column). Rationale: the flag then never exists without the behaviour WC-2 and WC-9 promise, and pr-submit, post-release and implement stay untouched until D2-D4 are answered.

### F-2 [MAJOR, blocking] WC-4's contract path contradicts the rows and AC-1.2 that depend on it

- Expert: Wiegers (traceability), Fowler (interface consistency). Priority: High. Quality impact: Consistency -2, Testability -1.
- Locations: `SPEC:62` (WC-4), `SPEC:76` ("Contract means `<output-dir>/return-contract.yaml`"), `SPEC:73` (report path known before dispatch), `SPEC:83` and `SPEC:198` (adversarial), `SPEC:92` (workflow), `SPEC:85`, `SPEC:86` (cleanup-audit, index-repo), `SPEC:87`, `SPEC:90` (init-lite and tdd), `SPEC:196` (AC-1.2), `SPEC:182` (7.2 step 3).
- Contradicting texts:
  - WC-4: the file is `<output-dir>/return-contract.yaml`, `<output-dir>` is the directory the coordinator passed with `--output` or `--output-dir`, and the path is known before dispatch.
  - adversarial row: the contract moves to `<output>/adversarial/return-contract.yaml` (`SPEC:83`); AC-1.4 requires "one fixed path" (`SPEC:198`). That is not `<output>/return-contract.yaml`.
  - workflow row: `.dev/tasks/to-do/<id>/return-contract.yaml` (`SPEC:92`); `<id>` is minted by the run (`INV-B:272`) and the brief passes only `--handoff none`, so the path cannot be "known before dispatch".
  - cleanup-audit has a fixed output directory (`SPEC:85`, `INV-A:42`) and index-repo has no output flag at all ("State the output location", `SPEC:86`, `INV-A:53`), yet AC-1.2 (`SPEC:196`) runs every P1 command, including these two, "with `--unattended --output <dir>`".
  - init-lite and tdd take `--output <file>` (`SPEC:87`, `SPEC:90`), so "the directory the coordinator passed" is a file; the supplied command definition says the same for spec-panel: "`--output` is file-valued" (`command.md:460`).
- Grading sentence: An implementer who follows WC-4 and 7.2 step 3 (`SPEC:182`: the worker's report path is "the WC-4 contract path") builds a worker that opens `<output>/return-contract.yaml` after a successful `/sc:adversarial` run, finds nothing because the row wrote it under `adversarial/`, and by WC-5 ("no report exists") sends `--outcome failed` for a run that succeeded; and AC-1.2 cannot pass for index-repo or cleanup-audit because they have no `--output <dir>` to pass.
- Recommendation (narrow): drop the "`--output` / `--output-dir`" equivalence from WC-4 and have WC-4 say the contract path is the one the command's row names. Add that exact path to every row of 3.1 and 3.2 (the column already exists as "Report"), and make AC-1.2 and 7.2 step 3 use that column. Rationale: one place defines each path, and the checks stop asking for flags that do not exist.

---

=== ARCHITECTURE ANALYSIS ===

No architecture finding is blocking. The decision in section 1 (Orca on top, commands as units of work) is supported by `CAPS:97-103,145-150,155-161` and by `INV-A:90`, `INV-B:285-286`; the decomposition (one shared contract document, one short section per command, coordinator-owned fan-out) is sound, and the standalone-unchanged rule (SA-1 to SA-6) is the right boundary.

---

## Medium warnings (follow-up candidates, never blocking)

Each Medium finding fails the grading check because the sentence needs a guess, or because the document never states the requirement.

| Id | Expert | Location | Issue | Recommendation and rationale | Priority | Impact |
|---|---|---|---|---|---|---|
| F-3 | Newman, Nygard | `SPEC:62,261,262` | The contract has no version field, no Task or Dispatch id and no run stamp, and WC-4 says commands that already write a contract "keep their fields" while `status` must be one of four values; the existing contracts' status values are not in the inventories (only `failed` is, `INV-B:272`). A retry or a re-run into the same `<output-dir>` leaves the first attempt's contract in place until it is overwritten; a worker that dies before writing leaves a stale `succeeded`, and 7.2 step 4 (`SPEC:183`, `test -s`) passes it. | Add `contract_version` and the dispatch id to the "at least" fields, and say a command removes or replaces an existing contract at start. Say how an existing `status` value maps to the four. | Medium | Consistency, evolution |
| F-4 | Whittaker (divergence) | `SPEC:63,103,105,121` | `partial` maps to `succeeded` and `blocked` to `failed` (WC-5), but a run can be both: cleanup lists deferred "Approval Required" items (`SPEC:103`), cli-portify stops at a gate after writing artifacts (`SPEC:105`), task stops at a TFEP stop (`SPEC:121`). No precedence rule exists, so the same state yields `succeeded` in one command and `failed` in another. | One line: if a run produced a usable deliverable and stopped on a gate, the status is `blocked`. | Medium | Consistency |
| F-5 | Adzic, Cockburn | `SPEC:61,105,113,117,201` | WC-2 (b) and WC-3 let a blocked gate be answered "as a flag", but the rows name no flag for the cli-portify approvals (three gates, `INV-A:45`), the review-translation Phase 1 confirmation, or post-release's pre-tag choice. WC-3 also says the session asks "once", while cli-portify has three gates. AC-2.3 (`SPEC:201`, a happy path with `--outcome succeeded` for every P2 command) cannot pass for cli-portify, whose only unattended outcome is `blocked`. `INV-A:79` offered an auto-approve flag; the spec chose blocked without saying how a worker gets past the gate. | Name, per such row, the flag or the resume rule that records the approval, or state that these commands end `blocked` by design and exempt them from AC-2.3. | Medium | Completeness |
| F-6 | Crispin | `SPEC:59,61,64,68,70,181,182,184` | Traceability from requirement to check: WC-1, WC-3, WC-6 and WC-12 have no acceptance check; WC-10 is checked only for pr-submit (AC-4.3), not for cli-eval, the command P2 names for it (`SPEC:160`); WC-11 only for save (AC-3.4). The chat-question stall that WC-2 forbids (`INV-A:62`) shows neither as `agentWait` (7.2 step 2) nor as an `AskUserQuestion` call (step 5), and step 3 ("until `worker_done` arrives") has no deadline, so an unconverted gate hangs the check instead of failing it. | Add a deadline to step 3 that fails the check, and one check each for WC-6 (retry into a used directory) and WC-10 on cli-eval. | Medium | Testability |
| F-7 | Wiegers | `SPEC:59,67,68`, `SPEC:210` | Thresholds are unquantified or disagree. WC-1 says "well inside" the 60 s limit while its own evidence says a fallback "above about 45 s" fails (`SPEC:59`), and `CAPS:49` shows the 45 s was the limit given in that test, not the default. WC-9 turns off "a paid external run" without defining it; web search is default-on in research, review-translation and recommend `--plugin` (`INV-B:134,144`) and cli-eval `run` executes real evals (`INV-A:44`). WC-10 triggers on a call longer than 5 minutes, yet AC-4.3 forbids any call over 240 s. | State a number for WC-1 (below the shortest observed passing limit), list what WC-9 counts as paid, and use one threshold in WC-10 and AC-4.3. | Medium | Testability |
| F-8 | Nygard, Whittaker | `SPEC:118,205`, `INV-B:153-154` | The roadmap row replaces the "[Y/n]" resume prompt with "resume only when the flag is passed". Today the default is to offer resume of an existing `.session-memory.md`; the new default starts fresh over it, and the skill writes memory at every wave (`INV-B:154`). Whether the old file is kept or overwritten is not stated, so an unattended run can destroy the state a person would have resumed. AC-3.2 (`SPEC:205`) checks only that it "starts fresh". | State that a fresh unattended run moves the old session file aside, or refuses (blocked) when one exists. | Medium | Data safety |
| F-9 | Nygard, Fowler | `SPEC:122`, `INV-B:209-210` | The tasklist row passes `--unattended` to each reflect "so the headless rule applies" but does not resolve the Stage 10.5 `needs_human_decision` HALT that `INV-B:209` records, so a person-blocking step remains inside a subagent (WC-2). It also says the fan-out "runs one layer below the worker, inside Claude Code's nesting limit (`INV-A:14`)": the reflect subagent is layer 1, its agents are layer 2 and a Tier 2 adversarial round is layer 3; `INV-B:210` marks nested spawning UNVERIFIED and `INV-A:14` says the Agent tool is withheld at the limit. | Resolve the HALT as `blocked`, and mark the depth claim UNVERIFIED or count the layers. | Medium | Completeness |
| F-10 | Cockburn, Fowler | `SPEC:16,52,65,73,180` | The spec never says how the worker starts the command. Orca delivers the Task text as launch input with the preamble in front (`CAPS:47`), so the text does not begin with `/sc:`. Section 2.3 says the brief states "the exact command line", WC-7 says the worker "runs the command directly", and the only precedent run used a skill call from an Agent-tool subagent (`SPEC:43`, `CAPS:156`). Slash command, Skill tool call or reading the command file are three different behaviours. | Say in 2.3 which of the three the worker uses, and have AC-0.4 record it. | Medium | Clarity |
| F-11 | Whittaker (accumulation), Nygard | `SPEC:69,85,86,104`, `INV-A:42,44,53` | WC-11 says two workers in one worktree "must never write the same file". cleanup-audit keeps a fixed `.claude-audit/` and `progress.json`, index-repo a fixed `PROJECT_INDEX.md`, cli-eval fixed `.dev/eval-workspaces/cli-eval/` paths. The cleanup-audit row answers "one audit per worktree at a time (WC-11)", but section 2.3 and the brief template do not tell the coordinator to serialise them, and no check covers it. | Add the serialisation rule to 2.3 for the commands whose paths stay fixed. | Medium | Data safety |
| F-12 | Whittaker (sentinel collision) | `SPEC:51,228`, `command.md:459` | D1 recommends a `--unattended` flag as "testable by grep" that "cannot misfire on a person". It can misfire on prompt text: `/sc:research "how does --unattended work"`, `/sc:tdd` or `/sc:troubleshoot` on a topic that quotes the flag, or `/sc:analyze` on this very spec. The spec does not say the flag is recognised only as a standalone token outside quoted arguments. The supplied command definition resolves exactly this for spec-panel (`command.md:459`), which shows the gap is real. | Add that one sentence to 2.1. | Medium | Safety of default |
| F-13 | Whittaker (zero/empty), Nygard | `SPEC:62,52`, `SPEC:63` | WC-4 requires the contract "including stops before any other output exists", but not what happens when the output directory is missing, empty or unwritable, nor when `~/.claude/WORKER-CONTRACT.md` is absent (a dev checkout not yet installed). A zero-byte contract is "a report" for `test -s` failing but not for "no report exists" in WC-5. | Say: directory cannot be created or contract file unreadable means the command prints the refusal in chat and the worker ends `failed`; an empty or unparseable contract counts as no report. | Medium | Reliability |
| F-14 | Nygard, Hohpe | `SPEC:61,63,64`, `CAPS:80,117` | No bound on loops. A command that always ends `blocked` makes the worker report `failed`; Orca's circuit breaker does not count "a worker's own `failed` report" (`CAPS:80`), so a coordinator can retry it without limit. WC-3 resumes an `ask` without a limit. WC-5 says `worker_done` is sent "exactly once" but not what to do when that call fails or times out, where Orca offers `--retry-request` (`CAPS:117`). | Add a retry ceiling to 2.3, and say a failed `worker_done` is retried with the same request id. | Medium | Reliability |
| F-15 | Fowler, Crispin | `SPEC:158,172`, `SPEC:147` | AC-C1 (`SPEC:172`) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and must print nothing, but P0 adds `WORKER-CONTRACT.md` and "an Orca section" to `HOW-WE-WORK.md`, both in `core/` (`SPEC:158`), and SA-2 allows an Orca mention in the contract file (`SPEC:147`). If either file writes a command in the form the pattern matches, P0 fails its own common check. | Exempt the two P0 files in AC-C1 or say they name commands without the `orca <verb>` form. | Medium | Testability |

## Minor notes

| Id | Location | Note |
|---|---|---|
| N-1 | `SPEC:16` | Section 1.1 says what changes in the commands "is limited to" the section 2 contract; section 3 and SA-4 (`SPEC:149`) also list drift fixes, a new Write tool for explain, wait splitting and a frontmatter move. |
| N-2 | `SPEC:67,133` | `README:31` ("No git commits, pushes...") is a rule for this planning run's workers, not repository policy; it is cited as the evidence for WC-9 and for the git row. `SPEC:133` also cites `cmd/git.md:90` (UNVERIFIED here), which is the better source. |
| N-3 | `SPEC:23` vs `SPEC:43` | E3 cites `invocation_method: "skill-direct"` as support, while 1.4 (1) says the precedent proves only the Agent-tool route. The two cells read as disagreeing; E3 could say "via an Agent-tool subagent". |
| N-4 | `SPEC:202` | AC-2.4 counts reviews with `gh api .../reviews --jq length`; without `--paginate` the count stops at one page, so "unchanged" can hold when a post landed on a long PR. |
| N-5 | `SPEC:114` vs `SPEC:68` | The pr-submit row requires each poll-plus-sleep iteration under 4 minutes; WC-10 and AC-4.3 limit one tool call to 4 minutes (240 s). Harmless but two statements of one limit. |
| N-6 | `SPEC:108,102` vs `SPEC:146` | Adding Write to explain's tools and moving business-panel's frontmatter (effect on loading UNVERIFIED, `SPEC:278`) can alter standalone behaviour, which SA-1 forbids. |
| N-7 | `command.md:22-23,455-465` | The command definition supplied to this audit already has `--unattended`, `--report-dir`, `--output` (file-valued), `--target-release` and a `~/.claude/WORKER-CONTRACT.md` pointer for spec-panel, while the spec's spec-panel row says to "add `--output`" (`SPEC:120`) and WC-4 uses `--output` / `--output-dir`. This is not spec evidence, so it is not graded; the coordinator should check whether the spec describes the current command. |

---

## Guard Condition Boundary Table

Trigger met: the spec contains thresholds, boolean guards and sentinel comparisons. Constructed by Nygard, completeness-validated by Crispin, attacked by Whittaker. Classes left out are named in the line under each guard. FR-8/FR-9 grading: a GAP is blocking only with a concrete wrong outcome (here only G1/F-2 and G11/F-1 qualify), otherwise Medium.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 contract exists (`no report exists`) | `SPEC:63` | Zero/Empty | no file; zero-byte file | not found; found | no file: `--outcome failed`. Zero-byte file: not stated (AC step 4 uses `test -s`, `SPEC:183`) | GAP (F-13, Medium) |
| G1 | `SPEC:63`, `SPEC:83` | Legitimate Edge Case | adversarial writes `<output>/adversarial/return-contract.yaml` | not found at WC-4 path | worker sends `failed` for a successful run | GAP (F-2, blocking) |
| G1 | `SPEC:62`, `SPEC:63` | Sentinel Value Match | stale contract from an earlier attempt in the same directory | found | treated as this run's report | GAP (F-3, Medium) |
| G2 `status` in {succeeded, partial, failed, blocked} | `SPEC:62`, `SPEC:63` | One/Minimal | `succeeded` | true | `--outcome succeeded` | OK |
| G2 | `SPEC:63` | Typical | `blocked` | true | `--outcome failed`, first sentence states the status | OK |
| G2 | `SPEC:63` | Legitimate Edge Case | partial work plus a gate stop | both `partial` and `blocked` apply | not stated | GAP (F-4, Medium) |
| G2 | `SPEC:62` | Sentinel Value Match | existing contract uses another status word | false | "keep their fields" vs fixed set, not reconciled | GAP (F-3, Medium) |
| G3 `--unattended` present (D1) | `SPEC:51,228` | Zero/Empty | flag absent | false | today's behaviour (SA-1) | OK |
| G3 | `SPEC:51,228` | Typical | standalone token | true | unattended mode | OK |
| G3 | `SPEC:228` | Sentinel Value Match | the string inside a quoted topic | true by naive grep | not stated | GAP (F-12, Medium) |
| G3 | `SPEC:128`, `SPEC:112` | Legitimate Edge Case | flag passed to a section-4 command or to `/sc:load` | n/a | "get no mode" / exempt, result of passing it not stated | GAP (minor, no wrong outcome inferable) |
| G3 | `SPEC:159`, `SPEC:195` | Maximum/Overflow | flag on all 36 commands after P1, behaviour on 14 | true on 22 commands whose rules are pending | not stated | GAP (F-1, blocking) |
| G4 wait length (WC-10) | `SPEC:68`, `SPEC:210` | Typical | 4 min tool call | no split needed | allowed | OK |
| G4 | `SPEC:68` vs `SPEC:210` | Legitimate Edge Case | 4.5 min call | WC-10 trigger (>5 min) false; AC-4.3 limit (240 s) exceeded | contradicts | GAP (F-7, Medium) |
| G4 | `SPEC:68` | Maximum/Overflow | call over 5 min | split into waits of at most 4 min | stated | OK |
| G5 readiness fallback (WC-1) | `SPEC:59` | Typical | 30 s fallback | passes | stated (evidence) | OK |
| G5 | `SPEC:59` | Legitimate Edge Case | fallback 46-59 s under the default 60 s limit | "well inside" undefined | not stated | GAP (F-7, Medium) |
| G5 | `SPEC:59` | Maximum/Overflow | fallback over 60 s | fails at `agent_readiness` | stated | OK |
| G6 `ask` wait (WC-3) | `SPEC:61`, `SPEC:281` | Zero/Empty | `--timeout-ms` omitted | default unknown | UNVERIFIED #10, resume by id | OK (acknowledged) |
| G6 | `SPEC:61` | Maximum/Overflow | coordinator never answers; resumes repeat | wait continues | no ceiling | GAP (F-14, Medium) |
| G7 retry via `--retry-of` (WC-6) | `SPEC:64`, `CAPS:80` | Maximum/Overflow | repeated `blocked` -> `failed` reports | breaker does not count them | no ceiling | GAP (F-14, Medium) |
| G8 `check` result (WC-12) | `SPEC:70` | Typical / Legitimate Edge Case | empty check; `consumer_fenced` | continue; stop without `worker_done` | stated | OK |
| G9 nesting depth (WC-8, R1) | `SPEC:33,66` | Typical / Maximum | depth 1; depth raised to 2 or more (D5 b) | refused; allowed by Orca | WC-8 forbids either way | OK |
| G10 confidence below 0.70 (task) | `SPEC:121` | Legitimate Edge Case | exactly 0.70 | false | continues per the command (`INV-B:199`) | OK |
| G11 `--monitor` ordinal (pr-submit) | `SPEC:114` | Typical | 1 refused, 3 default | true / false | stated | OK |
| G11 | `SPEC:114` | Legitimate Edge Case | `--monitor 0` and `2` | not stated | not stated; D3(a) may make it moot | GAP (Medium, P4 pending D3) |
| G12 output directory (WC-4) | `SPEC:62` | Zero/Empty | directory missing, empty path, unwritable | not stated | not stated | GAP (F-13, Medium) |

Classes left out: G2 and G4 have no Maximum/Overflow capacity beyond the rows shown (enumerated values, no collection); G5 has no sentinel (a time value); G8, G9 and G10 have no Zero/Empty (the value always exists or is an enumeration).

## Pipeline Dimensional Analysis (FR-17 to FR-19) and Quantity Flow Diagram

Triggered: the spec is a multi-stage partition of a command set into rollout phases, and the count at the flag stage differs from the count at the behaviour stage. Fowler annotated the counts; Whittaker attacked the divergence point.

```text
[43 commands: INV-A 21 + INV-B 22, SPEC:76]
   --> [Split] --> [10 ready (3.1)] [27 need change (3.2)] [6 coordinator-only (4)]   (10+27+6 = 43, conserved)
[37 = 10 + 27]
   --> [P1: flag + section] --> [36 flagged (load exempt)]  <-- consumer AC-1.1 expects 36 sections (SPEC:195)
                                  |
                                  v
                    [behaviour complete at P1: 14]  = 8 P1 no-gate commands + 4 ready-command fixes + brainstorm + init-lite
                    [behaviour pending: 22]         = P2 15 + P3 4 + P4 3        <-- MISMATCH (N=36, M=14), see F-1
[Phase counts]  P1 9 + P2 11 + P3 4 + P4 3 = 27 needs-change (conserved); ready fixes 4 (P1) + 4 (P2) + 2 (none) = 10 (conserved)
[Contract paths] 36 commands expected to write `<output-dir>/return-contract.yaml` (WC-4)
                 vs rows naming another path (adversarial, workflow) or no directory flag (cleanup-audit, index-repo, init-lite, tdd)  <-- MISMATCH, see F-2
```

## Adversarial analysis (Whittaker, FR-3 template)

- I can break this specification by **Sequence Attack**. The invariant at **SPEC:60,67 (WC-2, WC-9) against SPEC:159 (P1)** fails when **P1 is complete and a later phase has not started**. Concrete attack: before, auggie-review has no `--unattended`; P1 adds it, AC-1.1 passes; the coordinator briefs `--unattended`; after, the command posts to the PR (F-1).
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:62 (one contract path) against SPEC:83 (adversarial path)** fails when **the command's row names a different directory**. Concrete attack: adversarial writes `D/adversarial/return-contract.yaml`; the worker opens `D/return-contract.yaml`, finds nothing; WC-5 sends `--outcome failed` for a success (F-2). A second divergence: a run that is both `partial` and `blocked` maps to opposite Orca outcomes (F-4).
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62 ("written on every outcome")** fails when **the output directory cannot be created, or the contract is zero bytes**. Concrete attack: `--output-dir` points at a read-only path; the command cannot write the file it must write on every outcome, and the spec gives no outcome for that case (F-13).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:51,228 (the flag is the only switch)** fails when **user text contains the sentinel**. Concrete attack: `/sc:research "what does --unattended do"` turns a person's run unattended and drops its prompts (F-12). A second collision: an old contract with `status: completed` meets the fixed four-value set (F-3).
- I can break this specification by **Accumulation Attack**. The invariants at **SPEC:64 (retry) and SPEC:69 (parallel-safe writes)** fail when **repeats or parallel runs accumulate**. Concrete attack: a gate that always blocks gives 3, 4, 5 failed reports with no breaker trip (`CAPS:80`); two cleanup-audit workers in one worktree both write `.claude-audit/progress.json` (F-14, F-11).

## Consensus and disagreements

- Consensus: the "Orca on top" decision, the six coordinator-only commands, the 10 / 27 / 6 split and the SA-1 to SA-6 standalone rules are well supported by the inventories (Wiegers, Fowler, Cockburn agree).
- Consensus: the per-phase checks are strong (Crispin); the gaps are in the requirement-to-check trace (F-6) and in two checks that cannot pass (F-2, AC-2.3 in F-5).
- Disagreement (not blocking): Nygard rates the unbounded-retry gap (F-14) higher than Fowler, who treats it as a coordinator concern outside the command contract. Left as Medium.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Newman, Hohpe, Nygard, Whittaker, Crispin]
  focus_areas: [requirements, architecture]
quality_assessment: {overall_score: 6, clarity: 7, completeness: 6, testability: 6, consistency: 5}
critical_issues:
  - {id: F-1, category: requirements, severity: CRITICAL, expert: Wiegers, issue: "P1 flags 36 commands, 14 behaviour-complete", recommendation: "Match flag and section to each row's phase"}
  - {id: F-2, category: requirements, severity: MAJOR, expert: Wiegers, issue: "WC-4 path contradicts rows and AC-1.2", recommendation: "Per-row contract path; WC-4 and AC-1.2 use it"}
expert_consensus: ["Decision and split are well supported", "Checks are strong but two cannot pass"]
improvement_roadmap:
  immediate: [F-1, F-2]
  short_term: [F-3, F-4, F-5, F-6, F-10, F-12, F-13]
  long_term: [F-7, F-8, F-9, F-11, F-14, F-15]
adversarial_analysis: [F-1, F-2, F-4, F-11, F-12, F-13, F-14]
```

## Follow-up candidates

Medium warnings: F-3 to F-15. Minor notes: N-1 to N-7. None is blocking, none triggers a revision, and none appears in the Reviser brief. The coordinator's session asks the user once whether to open an issue for them.

## Reviser brief

Blocking finding ids: F-1, F-2.

Rules for the reviser (restated from the command, because the reviser reads this report and not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the file before and after, and the bytes added and deleted per finding id; leave minor and Medium findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
