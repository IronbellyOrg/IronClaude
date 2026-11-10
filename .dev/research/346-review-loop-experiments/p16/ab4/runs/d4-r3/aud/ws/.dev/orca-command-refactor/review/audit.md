review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

| Header | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| scope | Labelled whole-document audit of the final spec. First review of the whole document (no `--re-review`, no `--baseline` given, so no `baseline: missing` note applies). |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| candidate sha256 | `cbaee912425ccadcbc06bd6c2dd562fc87afea9b7b20dc55342bb7c482b347f0` (59637 bytes) |
| baseline sha256 | not applicable (first review) |
| reviewer model | claude-sonnet-5-5 |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; `~` is the sandbox home) |
| binding context read | `.dev/orca-command-refactor/README.md` (read first, in full) |
| evidence checked | `inventory/commands-a.md` (INV-A), `inventory/commands-b.md` (INV-B), `inventory/orca-capabilities.md` (CAPS). Same shorthand as the spec. |
| citation rule | Spec lines are cited as `spec:N`. Any citation into `src/`, `tests/`, `CLAUDE.md`, `.dev/evals/`, `.dev/codegraph-migration/`, `orca-ide` output, `pyproject.toml`, or `Makefile` that I could not check inside the workspace is marked UNVERIFIED. |

## What I covered

- All of `spec:1-286`: sections 1 to 9, the Decisions table, and the UNVERIFIED list.
- Every `INV-A:N`, `INV-B:N` and `CAPS:N` citation I met (about 60 distinct ones) was opened against the inventory line. All land on the stated content. I found no wrong inventory or capability line number.
- The section 3 command rows were compared with the inventory rows for 37 commands. The 10 / 27 / 6 split reconciles: 5 + 5 ready, 13 + 14 needs-change, 3 + 3 coordinator-only (`INV-A:73`, `INV-B:278`, `spec:76`).
- Not covered: the source files themselves (`cmd/*.md`, `sk/**`) and the live Orca guides. They are outside the sandbox, so every `src/...` line the spec cites beyond what the inventories quote is UNVERIFIED here. This includes the 11 locations that `spec:11` says were re-read.

## Panel (fixed order, focus requirements + architecture; Whittaker is always active)

Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard (architecture); Whittaker (adversarial); Newman, Hohpe (architecture). Crispin, Gregory and Hightower are not engaged because the focus did not select them.

## Grading note

Each finding is graded by consequence under the FIRST-REVIEW grading check. Only F-01 meets it. Everything labelled MAJOR in the experts' wording but needing an assumed reading is Medium and sits under `follow-up candidates`.

=== REQUIREMENTS ANALYSIS ===

### F-01 (blocking, MAJOR) Phase 1 gives every command `--unattended` before the gate and outward-default changes that the flag promises

Experts: Wiegers (lead), Nygard, Whittaker (FR-2.4 Sequence Attack).

Grading sentence: an implementer who follows the stated text as written builds a Phase 1 in which gated commands accept `--unattended` and still prompt or post, and that is wrong because WC-2 and WC-9 say that under `--unattended` no prompt remains and every outward default is off.

Stated texts that meet:

- `spec:159` (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". Its rationale is "No person gate is involved".
- `spec:195` (AC-1.1) asserts the `## Unattended mode` section on every command in 3.1 and 3.2 except load. That includes the P2 and P4 commands.
- `spec:196` (AC-1.2) runs the live check only on P1 commands. `spec:203` (AC-2.4, the auggie-review posting check) only exists in P2.
- `spec:60` (WC-2): under `--unattended` the command never calls `AskUserQuestion`, never ends on a chat question. `spec:67` (WC-9): under `--unattended` any default that pushes, posts, installs or provisions is off.
- `spec:73` (2.3): the coordinator's brief states the exact command line "including `--unattended`".
- `spec:100`, `spec:121`, `spec:113`, `spec:114` (rows for auggie-review, task, post-release, pr-submit): the gate and outward-default changes are in P2 or P4. Their baseline is a default that posts to GitHub with no confirmation (`INV-A:38`, citing `cmd/auggie-review.md:51-54`, UNVERIFIED in the workspace), a TFEP report that is committed (`INV-B:204`), and installs/VM/commit/PR behind chat confirmations (`INV-B:79`).

State trace (auggie-review, Whittaker FR-2.4):

1. Before: P1 merged, P2 not started. `/sc:auggie-review` has the section and accepts `--unattended`. Posting is still the default, and the remediation offer is still a plain chat wait (`INV-A:62`).
2. The contract file from P0 (`spec:158`) and the brief template (`spec:73`) tell the coordinator to pass `--unattended` and that outward actions are off (`spec:67`).
3. The coordinator dispatches `/sc:auggie-review <PR> --unattended`.
4. After: review comments are posted to the PR (an outward action WC-9 says is off), and then the session ends its turn waiting on a reply nobody sends (a WC-2 stall with no `worker_done`, the exact failure `spec:44` calls invisible).

Nothing in the document marks the flag as not yet effective for these commands. P1 acceptance does not catch it, because the P1 checks never run a gated command. The same trace applies to `/sc:task` (commit/push EXEMPT keywords, `spec:121`), `/sc:post-release` and `/sc:implement`.

Same root cause, second symptom: `spec:241` (D3 recommendation (a)) says "no pr-submit changes in Phase 4", and `spec:139` keeps pr-submit a worker candidate only if D3 is accepted. But P1 (`spec:159`) and AC-1.1 (`spec:195`) already require pr-submit to carry the section and the flag. Two stated texts cannot both hold under the recommended D3.

Recommendation: narrow P1 and AC-1.1 so that a command gains `--unattended` in the phase that makes the flag true for it (P1 for gate-free commands, P2 for the gated ones, P4 for the three decision-gated ones). If a command must accept the flag earlier, it should refuse it with a stated message until its phase lands. Prefer this deletion/narrowing to adding a mechanism. Priority High. Quality impact: removes the only state in which the contract's safety promise is false.

### M-01 (Medium) Contract location is undefined for several commands and for the empty-anchor case

Experts: Wiegers, Whittaker (FR-2.1 Zero/Empty Attack). A requirement the document never states.

- `spec:62` (WC-4): default location is the directory the coordinator passed. The exceptions list names adversarial, workflow, implement, cleanup-audit, index-repo, research, recommend, review-translation, task, save. cli-eval has no output flag (`INV-A:44`, outputs are fixed `.dev/eval-workspaces/...` and `.dev/eval-runs/...`) and is not on the list. `spec:104` gives no location. Yet `spec:200` (AC-2.2) uses `/sc:cli-eval run --unattended` with no `--suite` as its example and expects a contract and a path "WC-4 gives" (`spec:182`, step 3). WC-4 gives none.
- `spec:105` (cli-portify) copies the inventory gap into the spec ("file location unnamed"). A tasklist, roadmap, validate-roadmap and validate-tests row also names a report but no placing rule.
- `spec:92` (workflow) requires a contract for pre-creation STOPs (`spec:198`, AC-1.4), but the contract lives in `.dev/tasks/to-do/<id>/` and `<id>` is created by the run, so before creation there is no directory.
- Zero attack: `--unattended` without `--output` for the rows that say "add `--output`" (`spec:99-107`, `spec:123`) is not specified (blocked, or a timestamped default?). `spec:69` (WC-11) says default paths carry a timestamp, but not for the contract.

The coordinator can still learn the path from `worker_done --report-path`, which is why this is Medium and not blocking. Priority Medium.

### M-02 (Medium) Section 3.1 says "ready" commands change only by small fixes; P1 and AC-1.1 change every one of them

`spec:79`: "The only command changes are the small fixes in the last column." Rows `spec:84` (brainstorm) and `spec:87` (init-lite) say "None". But `spec:76`, `spec:159` and `spec:195` give all of them the `## Unattended mode` section, and WC-4 gives all of them the new contract fields. Several 3.1 commands have no contract today (init-lite, troubleshoot, tdd, release-split write a REPORT or a document, `INV-B:112`, `:122`, `:242`). The P1 command list at `spec:159` names 13 commands and omits brainstorm and init-lite. Count: 9 (P1 3.2 rows) + 4 (P1 ready fixes) + 15 (P2) + 4 (P3) + 3 (P4) = 35 named; with brainstorm and init-lite that is 37. They are covered only by the "every command" prose. Priority Medium.

### M-03 (Medium) Fixed `status` set vs "keep their fields" for existing contracts

`spec:62` fixes `status` to `succeeded|partial|failed|blocked` and says commands that already write a contract "keep their fields and add the missing ones". `spec:264` records the choice of a fixed set over each command's own statuses. The existing contracts' `status` vocabularies are not stated anywhere in the spec or inventories (workflow's is in `refs/return-contract.md:3-19`, UNVERIFIED; adversarial, reflect, brainstorm also write one). If an existing `status` uses other values, "keep" and "fixed set" conflict, and the AC-1 YAML check (`spec:183`) fails. Also, WC-5 (`spec:63`) defines `failed` for "no report exists" but not for a report that exists and is empty, unparseable, or has a value outside the set. Priority Medium.

### M-04 (Medium) "Fresh output directory" on retry conflicts with a coordinator-supplied directory, and `roadmap` unattended start overwrites state

- `spec:64` (WC-6): a command with no resume "writes each run into a fresh output directory". `spec:62` (WC-4) and `spec:73` (2.3) have the coordinator pass the directory. A retry brief with the same `--output` writes into the old directory. Nothing in 2.3 says to pass a new directory per attempt, and the contract has no run identifier or timestamp, so a stale contract from attempt 1 is indistinguishable if attempt 2 dies before rewriting it (WC-5 reads the file to choose the outcome, `spec:63`).
- `spec:118` (roadmap) and `spec:206` (AC-3.2): with an existing `.session-memory.md` and no resume flag the command "starts fresh". The spec does not say whether the earlier `roadmap.md` and `.session-memory.md` in the same directory are overwritten, which conflicts with WC-6's "must not corrupt the first attempt's output".

Priority Medium.

### M-05 (Medium) A claim used to downgrade a risk is stated as fact, not marked UNVERIFIED

`spec:44` (1.4 gap 2): a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`". For Claude the task is passed on the command line (`CAPS:47`), so the command starts running while Orca waits for the fresh composer or an idle TUI. Whether an immediate first-step question still lets readiness pass is not shown by `CAPS:52` or `CAPS:129` (those are about a worker already at `input_accepted`). `README.md:36` requires unverified items to be marked UNVERIFIED, and it is not in the UNVERIFIED list (`spec:272-286`). Practical effect is small because WC-2 forbids prompts, but AC-2.2 deliberately provokes gate-trigger runs and reads the result by `agentWait` (`spec:181`). Priority Low to Medium.

### M-06 (Medium) `--unattended` token has no parse rule; free-text arguments can collide with it

Whittaker FR-2.3 Sentinel Collision Attack. `spec:229` (D1) says the flag "cannot misfire on a person". But many commands take free text (`/sc:tdd "…"`, `/sc:troubleshoot "…"`, `/sc:research`, `/sc:task`, `/sc:brainstorm`, `/sc:recommend`). A prompt containing the string `--unattended`, or a pasted command line, would switch off the gates for a person. The spec defines the switch as a flag but never says it must be a standalone argument token outside quoted content. Concrete attack: `/sc:troubleshoot "login fails when run with --unattended" ` reads as unattended mode in a person's session and violates SA-1 (`spec:146`). Priority Medium.

=== ARCHITECTURE ANALYSIS ===

### M-07 (Medium) SA-2 permits an Orca mention that AC-C1 would fail on, in the spec's own P0 deliverables

Experts: Fowler, Newman.

- `spec:147` (SA-2): "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file."
- `spec:158` (P0) adds `core/WORKER-CONTRACT.md` and an Orca section in `core/HOW-WE-WORK.md`. WC-3 (`spec:61`) names the preamble's `ask` command.
- `spec:172` (AC-C1) greps `src/superclaude/core` as well, excluding only `skills/ccsession-tag/`, and requires the output to be empty. A line such as `orca orchestration ask` in either P0 file prints a match, so P0 fails its own common check. This only happens if the author writes the command in that form, which the text neither requires nor forbids, hence Medium. `E5` (`spec:25`) shows the baseline is zero mentions in core.

Recommendation: exclude the two named P0 files from AC-C1, or forbid command-form Orca text in them. Priority Medium.

### M-08 (Medium) Phase and decision wording disagree on what needs a user decision

`spec:154`: "Phases 1-3 need no user decision". But D4 (`spec:245`) covers auggie-review `--post-pr` and task `commit`/`push`, both P2 rows (`spec:100`, `spec:121`), and D1 selects the switch every phase uses (`spec:228`). `spec:226` says "Phases 0-3 can proceed on the recommendations", which is a different statement. Priority Low to Medium.

### M-09 (Medium) WC-3 lets the worker `ask` instead of ending `blocked`, but the acceptance checks and D2 assume `failed`

- `spec:61` (WC-3): "may instead ask the coordinator once". It is not a carve-out for implement. `spec:238` (D2) and `spec:209` (AC-4.1) expect an implement halt to end `failed` with no relayed Ruling unless D2(b). `spec:200` (AC-2.2) expects `--outcome failed` for every blocked gate.
- "Once" is undefined for a command with several gates (cli-portify has three, `spec:105`; task has two, `spec:121`). Each re-invocation can block again.
- A relayed answer "as a flag" (WC-3) cannot carry an implement Ruling, so the generic route is silent on the one place where relaying is a stated safety rule (`INV-A:66`, `INV-A:81`).

Priority Medium.

### M-10 (Medium) `--post-pr` is relied on but not evidenced; WC-9 assumes every outward default has an explicit enabling flag

`spec:100`: posting "returns only with an explicit `--post-pr` in the brief". The evidence has only `--no-post-pr` (`INV-A:38`, citing `cmd/auggie-review.md:52`, UNVERIFIED in the workspace). `spec:67` (WC-9) says outward defaults turn on "only through the command's own explicit flag", but task's `commit`/`push` are EXEMPT keywords, not flags (`INV-B:204`), and post-release's gates are conversational (`INV-B:79`). D4(a) (`spec:246`) depends on these flags existing. The spec does not say they are new flags to add. Priority Medium.

### M-11 (Medium) tasklist row asserts nested-spawn safety that the inventories leave UNVERIFIED, and leaves the reflect HALT unresolved

`spec:122`: the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". `INV-A:14` gives the limit (three layers). It does not show that reflect inside a tasklist subagent keeps its own spawns: reflect Tier 2 reviewers sit at depth 2, and its adversarial merge advocates at depth 3. `INV-B:210`, `INV-B:314` item 1 and `INV-B:322` item 8 all call nested spawning and the nested remediation answer UNVERIFIED. The row also passes `--unattended` to each reflect so "the headless rule applies", but `INV-B:209` says `needs_human_decision` items HALT, and the row does not say how that HALT resolves under WC-2. Priority Medium.

### M-12 (Medium) WC-10 cannot be met for blocking Agent-tool calls

Hohpe/Nygard. `spec:68`: a step that blocks a single tool call for more than 5 minutes "must be split into waits of at most 4 minutes". The examples are a poll wait and an eval. A `Task` call that fans out a wave (cleanup-audit waves of 7-8 agents, `INV-A:42`; tdd research agents, `INV-B:221`) blocks for as long as the agents run, and the command cannot split it. Liveness loss is benign by `CAPS:125` ("absence never authorizes stop"), so this is Medium. The spec should say so or exempt Agent-tool calls.

## Guard Condition Boundary Table

Trigger: the spec contains threshold and conditional guards. The six classes are a menu. A class that cannot occur is left out with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit (60 s) | WC-1, `spec:59` | Typical | start at 34 s | pass | `state: ready` (`CAPS:49`) | OK |
| readiness limit (60 s) | WC-1, `spec:59` | Maximum/Overflow | fallback above ~45 s | fail | fails `agent_readiness` (`CAPS:49`) | OK |
| readiness limit | `spec:44` | Legitimate Edge Case | command asks first-step question (argv launch) | unknown | claimed not to fail readiness; no evidence | GAP (M-05, Medium) |
| nesting depth 1 | R1, WC-8, `spec:33`, `spec:66` | One/Minimal | worker calls `worker-start` | refused | `nested_worker_depth_exceeded` (`CAPS:99`) | OK |
| nesting depth 1 | WC-8, `spec:66` | Legitimate Edge Case | worker calls `task-create` | unknown | forbidden either way; Orca behavior UNVERIFIED (`CAPS:103`) | OK (stated as UNVERIFIED) |
| `--unattended` switch | `spec:51`, D1 `spec:229` | Zero/Empty | no `--output` given | not stated | nothing for the 12 "add `--output`" rows | GAP (M-01, Medium) |
| `--unattended` switch | `spec:51`, D1 `spec:229` | Sentinel Value Match | token inside quoted free text | not stated | no parse rule | GAP (M-06, Medium) |
| `--unattended` switch | P1 `spec:159` | Legitimate Edge Case | gated command, gate not yet converted | flag accepted | gate and outward default unchanged | GAP (F-01, blocking: concrete wrong outcome and a safety-boundary risk) |
| contract `status` set | WC-4/WC-5, `spec:62-63` | Sentinel Value Match | existing contract uses another status vocabulary | not stated | "keep their fields" vs fixed set | GAP (M-03, Medium) |
| contract `status` set | WC-5, `spec:63` | Zero/Empty | report exists but empty or unparseable | not stated | only "no report exists" is defined | GAP (M-03, Medium) |
| contract path | WC-4, `spec:62` | Zero/Empty | cli-eval, cli-portify, workflow pre-creation STOP | not stated | no location | GAP (M-01, Medium) |
| fresh dir / retry | WC-6, `spec:64` | Legitimate Edge Case | retry with same `--output` | not stated | stale contract can be read; roadmap start-fresh overwrite | GAP (M-04, Medium) |
| confidence < 0.70 (task) | `spec:121` | Zero/Empty | confidence 0.0 | true | blocked | OK |
| confidence < 0.70 (task) | `spec:121` | Legitimate Edge Case | exactly 0.70 | false | proceeds ("below 0.70" only) | OK |
| heartbeat wait <= 4 min | WC-10, `spec:68` | Maximum/Overflow | blocking `Task` fan-out > 5 min | not satisfiable | not addressed | GAP (M-12, Medium) |
| `ask` once | WC-3, `spec:61` | One/Minimal | single gate | one ask | defined | OK |
| `ask` once | WC-3, `spec:61` | Maximum/Overflow | cli-portify, three gates | second ask | "once" undefined | GAP (M-09, Medium) |
| PR/review count unchanged | AC-2.4, `spec:203` | Maximum/Overflow | more than 30 reviews or comments on the PR | count stays 30 | `--jq length` without `--paginate` counts the first page only | GAP (N-02, minor) |

Classes left out: Zero/Empty and One/Minimal for the 60 s limit (a non-positive `--timeout-ms` falls back to 60 s, `CAPS:44`, which is outside this spec's behavior); Sentinel Value Match for depth (no sentinel).

FR-8 and FR-9 applied: the GAPs that name a concrete wrong outcome or a safety-boundary risk are blocking (one: F-01). The others are Medium.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

The classification and rollout is a two-stage count flow. Counts reconcile, with one divergence at the last stage.

```text
[Source: 43 commands (21 A + 22 B)] --> [Stage 1: split coordinator-only] --> [37 worker-capable (43 - 6)]
                                                                               |
                                                                               v
                                         [Stage 2: readiness verdict] --> [10 ready + 27 needs change = 37]
                                                                               |
                                                                               v
                                         [Stage 3: phase assignment (section 6)]
                                           P1 13 named (9 gate-free incl. load + 4 ready fixes)
                                           P2 15 | P3 4 | P4 3                        = 35 named
                                           brainstorm, init-lite: no phase row        =  2   (covered only by prose)
                                                                               |
                                                                               v
   [Consumer: P1 prose "every command in 3.1 and 3.2"]   expects 37   (spec:159)
   [Consumer: AC-1.1 section check]                       expects 36   (37 minus load, spec:195)
   [Consumer: P1 command list]                            lists 13     (spec:159)   <-- MISMATCH (M-02)
```

Totals reconcile (43, 37, 10/27/6, 15 P2 rows in section 3 equal 15 in the section 6 list). The mismatch is between what P1 names, what P1 says in prose, and what AC-1.1 checks (13 / 37 / 36). It adds to F-01 (acceptance of the flag by commands whose phase has not landed).

=== ADVERSARIAL ANALYSIS (Whittaker) ===

- **FR-2.4 Sequence Attack**: F-01 (P1 flag before P2/P4 gate conversion). Trace in F-01.
- **FR-2.1 Zero/Empty Attack**: M-01 (no `--output`; cli-eval with no `--suite` has no contract anchor).
- **FR-2.3 Sentinel Collision Attack**: M-06 (`--unattended` inside quoted text); M-03 (existing `status` values collide with the fixed set).
- **FR-2.2 Divergence Attack**: M-09 (WC-3 "ask" branch vs "blocked ends failed" branch both apply to the same gate).
- **FR-2.5 Accumulation Attack**: M-09 (repeated gates against "ask once"); N-02 (page-limited counts).

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review: "1 of 3"
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.5
  clarity: 8
  completeness: 7
  testability: 7.5
  consistency: 7
critical_issues:
  - {category: phasing, severity: MAJOR, expert: Wiegers, issue: "F-01 flag accepted before gate conversion", recommendation: "accept per phase or refuse until effective"}
expert_consensus:
  - "The decision (Orca on top, commands as workers) is well evidenced and the evidence limits are stated plainly (spec:41-45)."
  - "Inventory counts and citations reconcile; the contract rules WC-1 to WC-12 are testable by section 7."
  - "The one real defect is sequencing of the flag against the safety rules it promises."
improvement_roadmap:
  immediate: [F-01]
  short_term: [M-01, M-02, M-03, M-04, M-06, M-07]
  long_term: [M-05, M-08, M-09, M-10, M-11, M-12]
```

## Follow-up candidates (Medium and minor; none triggers a revision, none appears in the Reviser brief)

Medium: M-01 contract location undefined for cli-eval, cli-portify, workflow pre-creation stops, and when no `--output` is given. M-02 section 3.1 intro vs P1 and AC-1.1. M-03 fixed `status` set vs existing contracts, and invalid/empty reports. M-04 fresh directory on retry, stale contract, roadmap overwrite. M-05 readiness claim not marked UNVERIFIED. M-06 `--unattended` parse rule. M-07 SA-2 vs AC-C1 on P0 files. M-08 "no user decision" for P1-P3. M-09 WC-3 `ask` vs `failed` expectations and "once". M-10 `--post-pr` and explicit enabling flags. M-11 tasklist nesting claim and reflect HALT. M-12 WC-10 vs blocking Agent calls.

Minor notes:

- N-01 `spec:67` and `spec:133` cite `README.md:31` ("No git commits, pushes, PRs...") as grounds for a lasting product rule. That line is a rule for the workers of this planning run (`README.md:29-31`), not repository policy.
- N-02 `spec:203` (AC-2.4): `gh api ... --jq length` without `--paginate` counts only the first page (30), so the "unchanged" check passes vacuously on a busy PR.
- N-03 `spec:194` (AC-0.4) says the no-Agent-tool-wrapper fact is "verified in the step-5 transcript", but step 5 (`spec:184`) only searches for `AskUserQuestion`.
- N-04 `spec:253` (D5 (b)) calls R1 "protection against runaway fan-out". R1 (`spec:33`) is a refusal rule, not a fan-out guard.
- N-05 `spec:111` (index row) tells the command to state that knowledge-base mode "does not wait", while the same row says whether it does is UNVERIFIED.
- N-06 `spec:22` (E2) says the worker "answered". `CAPS:49` quotes only `state: ready, stage: input_accepted`. UNVERIFIED in the workspace.
- N-07 `spec:198` (AC-1.4): a `grep -n` cannot show that adversarial "names one fixed path". It shows only matching lines.
- N-08 `spec:159` says P1 has "No person gate", but its list includes business-panel, explain and test, whose rows add refusals under `--unattended` (`spec:102`, `spec:108`, `spec:123`).
- N-09 `spec:159` lists `load` in P1 as accepting the flag, while `spec:76` and `spec:112` say load has no section and no contract.
- N-10 The `spec:133` rationale for `/sc:git` ("need the user's authorization in this repo") leans on N-01.
- N-11 `spec:1-286` carry UNVERIFIED-in-workspace citations to `src/` files and to `.dev/codegraph-migration/*`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `CLAUDE.md`, `pyproject.toml`, `Makefile`. I checked them only through the inventory lines that quote them.

The session that ran this review asks the user once whether to open an issue for the follow-up candidates and creates none without an answer. This is not an `--unattended` run, so the list is also recorded here.

## Brief clauses overridden

None. The brief narrowed nothing and widened nothing.

## Reviser brief

Blocking finding ids: **F-01** only.

Restated reviser contract (the reviser reads this report, not the command):

- Revise only text that F-01 names: `spec:159` (P1 scope), `spec:195` (AC-1.1), and if needed `spec:241` and `spec:139` (D3 and pr-submit).
- Add no rule, mechanism or section that F-01 does not call for. Each added paragraph or table cites F-01.
- Prefer deleting or narrowing to adding. Report the byte size of the spec before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M-xx, N-xx) alone.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
