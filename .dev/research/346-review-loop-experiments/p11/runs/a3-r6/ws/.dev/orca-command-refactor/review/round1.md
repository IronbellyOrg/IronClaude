review: 1 of 3

# Spec-panel review, round 1: Orca worker-contract spec

| Header field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 57763 bytes) |
| candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| baseline | none (first review; neither `--re-review` nor `--baseline` was given) |
| reviewer model actually used | `claude-sonnet-5-5` (Sonnet 5.5) |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full before this review (the hard gate of `cmd:266-268`) |
| date | 2026-11-10 |
| `--unattended` | not passed; no `return-contract.yaml` is written (`cmd:459`) |
| revised spec | none written: first review, brief says do not edit the candidate (`prompts:32`); the Improve step is not run |

Citation keys: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`, as in `spec:7-10`. `README:N` = `.dev/orca-command-refactor/README.md`. `cmd:N` = line N of the sandbox `command.md`. `prompts:N` = line N of the review-loop prompts file. Any citation to a file that is not in the sandbox (source files under `src/`, `CLAUDE.md`, `EVIDENCE.md`, the codegraph README, Orca binaries) is marked UNVERIFIED; the inventories and the spec are the only evidence I could check.

Brief clauses overridden: none. The brief narrowed nothing and widened nothing (`cmd:264`).

## What I covered

- Read in full: the candidate (285 lines), `README.md`, all three inventories, `command.md`, the prompts file.
- Cross-checked every `INV-A`, `INV-B`, `CAPS` and `README` line reference in the candidate (about 120) against the inventory files. All of them point at the text the candidate says they do. I found no wrong inventory line.
- Verified the counts: 21 + 22 = 43 commands; 10 ready, 27 needs-change, 6 coordinator-only. They match `INV-A:73`, `INV-B:278`, the 10 rows at `spec:83-92`, the 27 rows at `spec:99-125` and the 6 rows at `spec:132-137`. Phase membership at `spec:159-162` also sums to 37 worker commands.
- Not covered: whether the cited source lines under `src/superclaude/` say what the inventories claim (not in the sandbox), the Orca binaries, the codegraph-migration README, `EVIDENCE.md` (reachable only through the quotes at `CAPS:49`), and the "11 locations re-read" and "340 citations re-checked" claims at `spec:11` and `spec:285`. All UNVERIFIED here.
- Whole-document review. Focus requirements and architecture; correctness focus was not requested, so no State Variable Registry is produced (`cmd:186-188`).

## Panel (fixed order, `cmd:101-113`, restricted to the selected focus areas and Whittaker)

Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker, Newman, Hohpe. Crispin, Gregory and Hightower are not selected by `--focus requirements,architecture` (`cmd:131-152`).

## Guard Condition Boundary Table (hard gate, completed before synthesis)

Trigger: the spec contains guards, thresholds and sentinels (`cmd:313`). Responsibility: Nygard builds, Crispin's completeness duty is covered by me because Crispin is not on this panel, Whittaker attacks. Classes the guard cannot meet are omitted with a one-line reason under the table (`cmd:317`, `cmd:334`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` switch | spec:51, 227-230 | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1, spec:146) | OK |
| G1 | spec:51, 227-230 | Sentinel Value Match | `--unattended` as quoted text inside a free-text argument, e.g. `/sc:tdd "explain --unattended"` | ambiguous | none: the spec never says the flag is a standalone token (the real command does, `cmd:459`) | GAP (Medium, M-9) |
| G2 report-status mapping (WC-5) | spec:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G2 | spec:63 | Typical | `status: succeeded`/`failed`/`blocked`/`partial` | n/a | mapped (`partial` -> succeeded) | OK |
| G2 | spec:63 | Legitimate Edge Case | report exists but is empty, unparseable, or `status` outside the four values | unspecified | not stated; WC-5 only covers "no report exists" | GAP (Medium, M-6) |
| G3 wait-split (WC-10) | spec:68 | Zero/Empty | no long wait | false | no change | OK |
| G3 | spec:68 | Legitimate Edge Case | one call of 4 min 59 s after 1 min of other work | split rule (> 5 min) false | heartbeat gap reaches 5 min 59 s; rule says split at > 5 min but waits of "at most 4 minutes" | GAP (Minor, N-3) |
| G3 | spec:68 | Maximum/Overflow | cli-eval eval of 3600 s | true | split into <= 4 min waits (spec:104) | OK |
| G4 readiness fallback (WC-1) | spec:59 | Maximum/Overflow | wrapper fallback of 45 s against a 60 s limit | n/a | "well inside" the limit; no number | GAP (Medium, M-10) |
| G5 `ask` resume (WC-3) | spec:61 | Maximum/Overflow | coordinator never answers; worker resumes the same message ID indefinitely | no cap | none: no maximum number of resumes or total wait | GAP (Medium, M-10) |
| G5 | spec:61 | Legitimate Edge Case | a gate with no flag to carry the answer (tdd topic-only, recommend question, cli-portify approvals) | n/a | "re-invoke ... with the answer as a flag" has no flag to use | GAP (Medium, M-1) |
| G6 `<output-dir>` (WC-4) | spec:62, 73 | Zero/Empty | `--unattended` given, no output directory in the brief | true | none: the blocked report has no place to be written | GAP (blocking, REQ-1) |
| G6 | spec:62, 90, 87 | Legitimate Edge Case | `--output` is a file (tdd, init-lite, spec-panel) | `<output-dir>` undefined | none | GAP (blocking, REQ-1) |
| G6 | spec:83, 85, 92 | Legitimate Edge Case | command writes its contract elsewhere (adversarial `<output>/adversarial/`, cleanup-audit fixed `.claude-audit/`, workflow `.dev/tasks/to-do/<id>/`) | path differs from WC-4 | row and WC-4 disagree | GAP (blocking, REQ-1) |
| G6 | spec:62, 64 | One/Minimal | second attempt (`--retry-of`) with the same `<output-dir>` | overwrite vs "fresh dir" | WC-4 and WC-6 contradict | GAP (blocking, ARCH-1) |
| G7 outward-default off (WC-9) | spec:67, 100, 113, 121 | Sentinel Value Match | a command that has no explicit authorization flag (post-release, task commit/push, auggie-review `--post-pr`) | "turn on only through the command's own explicit flag" | the flag does not exist in the inventories | GAP (Medium, M-2) |
| G8 nesting depth (WC-8) | spec:66, 214, 250 | Typical | depth 1 | true | commands never call Orca | OK |
| G8 | spec:250-252 | Maximum/Overflow | depth raised above 1 (D5 b) | false | WC-8 still forbids; D5 recommends keeping 1 | OK |
| G9 additive-edit check (AC-C5, AC-0.3) | spec:176, 193 | Sentinel Value Match | a deleted markdown bullet (`- text` appears in a diff as `-- text`) | regex `^-[^-]` false | deletion not detected | GAP (Medium, M-3) |
| G9 | spec:176 | Zero/Empty | empty diff | prints nothing | pass | OK |

Classes omitted: G1 Maximum (a boolean has none); G2 One/Minimal and Maximum (a status is one of a closed set); G3 One/Minimal (a 1 s call is under the threshold, same as Zero); G4 Zero (a 0 s fallback means no prompt, which WC-1 allows); G6 Maximum (a path has no capacity); G7 Zero/Maximum (an outward default is on or off); G8 Zero (depth 0 is the coordinator, not a worker); G9 Maximum (a diff has no capacity).

FR-10 gate: every guard is enumerated and every cell is populated, so synthesis proceeds. Each GAP is graded by consequence below (FR-8, FR-9, `cmd:332-333`).

## Pipeline Dimensional Analysis (triggered: 4 stages, count differs at stage 2)

The coordinator -> worker -> report flow has more than 2 stages and the count changes when a Task is retried (`CAPS:116`), so the heuristic applies (`cmd:353`).

```text
[Coordinator: T Tasks] --> [worker-start: D dispatches, D >= T (retry-of adds one per retry)]
                                  |
                                  v
                          [worker_done: <= D messages, one per dispatch, zero on stall or consumer_fenced]
                                  |
                                  v
                          [contract file: one per output-dir, WC-4 = <output-dir>/return-contract.yaml]
                                  |
                                  v
                          [coordinator reads: expects one contract per dispatch]  <-- MISMATCH when D > distinct output-dirs
```

Concrete counts: 1 Task, 2 dispatches (attempt 1 ends `blocked`, attempt 2 is `--retry-of`), 1 output directory, 1 contract file. Attempt 2 overwrites attempt 1's file, or goes to a different directory the coordinator was not told. This is ARCH-1 (CRITICAL, FR-19, `cmd:372`).

## === REQUIREMENTS ANALYSIS ===

### REQ-1 (blocking, MAJOR, Wiegers lead, with Adzic): the report-location rule in WC-4 cannot be applied to a dozen of the commands the spec itself lists

Where: `spec:62` (WC-4), `spec:73` (section 2.3), `spec:83`, `spec:85`, `spec:87`, `spec:90`, `spec:92`, `spec:182-183` (live check steps 3-4), `spec:201` (AC-2.3).

Text as written:
- WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and section 2.3 says the output directory is passed "so the report path is known before dispatch".
- `--output` is a file for tdd (`spec:90`: "`--output <file>`; the TDD at `--output`"), init-lite (`spec:87`: "`--output <file>`") and, by the same convention, the `--output` that `spec:120` adds to spec-panel. For these, `<output-dir>` is undefined.
- adversarial's small fix names a different path: `<output>/adversarial/return-contract.yaml` (`spec:83`). cleanup-audit's output directory is fixed at `.claude-audit/` and the brief passes none (`spec:85`). workflow's contract lives in `.dev/tasks/to-do/<id>/`, the brief passes no output directory, and the `<id>` does not exist before the run (`spec:92`, `INV-B:272`). Its "pre-creation STOP" contract, which WC-4 requires "including stops before any other output exists" (`spec:62`, `spec:92`), has no directory at all.
- With no output directory in the brief, the `blocked` outcome of WC-2(c) has nowhere to be written (`spec:60`, `spec:62`).

Grading check: An implementer who follows the stated text as written builds, for `/sc:tdd --output docs/x/TDD_X.md --unattended`, a contract at a path of his own choosing (the file's parent directory, or a sibling file), builds adversarial's contract one level below `<output-dir>`, and builds workflow's pre-creation STOP with no contract; and that is wrong because the coordinator's acceptance steps require the report path to be the WC-4 path known before dispatch (`spec:182`), run `test -s <contract>` on it (`spec:183`), and treat a missing report as `--outcome failed` (`spec:63`), so a correct worker is scored as failed, or the check cannot be evaluated at all.

Corroboration (not evidence for the spec): the `/sc:spec-panel` command definition under review in this sandbox resolved the same problem with a separate directory-valued flag, because "`--output` is file-valued" (`cmd:460`). The spec has no such resolution.

Recommendation (narrowing, no new mechanism): state for every `--output` that is file-valued where the contract goes (for example `<output-file-dir>/return-contract.yaml`, or a sibling of the file), state the exact contract path in each 3.1/3.2 row whose path differs from WC-4 (adversarial, cleanup-audit, workflow), and say what a command does when no directory is given (the `blocked` report goes to a stated default, or the run stops with a chat-only refusal).

### REQ-2 (blocking, MAJOR, Wiegers with Cockburn): the P1 acceptance test contradicts the rows' own phase assignments and the "ready today" rows

Where: `spec:79`, `spec:87` and `spec:84` (3.1 "Small fix: None"), `spec:112` (load), `spec:76` and `spec:95`, `spec:159` (P1 scope), `spec:195` (AC-1.1), `spec:154`.

Text as written:
- P1 delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" and AC-1.1 requires every command in 3.1-3.2 to have a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (`spec:159`, `spec:195`).
- But 3.1 says for the ready commands "The only command changes are the small fixes in the last column" (`spec:79`), and brainstorm and init-lite have "Small fix: None" (`spec:84`, `spec:87`).
- load's row says "Report: none (see note)", "Other required change: none: use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)" (`spec:112`), and the Decisions table says a report file for load "would be an unrequested addition" (`spec:265`). Yet `spec:76` says "Every changed command also gains the `## Unattended mode` section", and load is changed.
- The rows assign implement, post-release and pr-submit to P4, roadmap, save and validate-* to P3, and the gate commands to P2 (`spec:109`, `spec:113`, `spec:114`, `spec:118-119`, `spec:124-125`); yet AC-1.1 is a P1 check over all of 3.1-3.2.

Grading check: An implementer who follows the stated text as written builds, for P1, a test that fails until brainstorm, init-lite, load, implement, post-release, pr-submit, roadmap, save, validate-roadmap and validate-tests each carry a `## Unattended mode` section naming a contract file (or builds the P1 plan and leaves the test red), and that is wrong because the rows say brainstorm, init-lite and load are not to be changed beyond a usage line and the later-phase commands are not to be touched before their phase; the P1 pass condition and the per-row scope cannot both hold.

Secondary consequence (the same text): a P1 `## Unattended mode` section and an accepted `--unattended` on a gate command such as auggie-review, which does not turn off PR posting or the remediation offer until P2 (`spec:100`, `spec:160`), gives a coordinator a switch that looks safe and is not. The spec never says `--unattended` must not be used on a command before its own phase. I grade that part Medium (M-4) because it also needs the assumption that P1 is released and used before P2.

Recommendation: scope AC-1.1 to the commands whose row says P1 (and the 3.1 commands the P1 row names), or delete the clause "accepted by every command in sections 3.1 and 3.2" from `spec:159`; give load and the "None" rows an explicit exemption.

## === ARCHITECTURE ANALYSIS ===

### ARCH-1 (blocking, CRITICAL, Fowler lead, Whittaker attack W2): WC-4 and WC-6 contradict on where a retry writes

Where: `spec:62` (WC-4), `spec:64` (WC-6), `spec:73` (2.3), the "Fresh dir" cells of `spec:88-91` and `spec:99-125`, `CAPS:80`, `CAPS:90`, `CAPS:116`.

Text as written:
- WC-4: the contract is `<output-dir>/return-contract.yaml`, in the directory the coordinator passed, and the path is "known before dispatch" (`spec:62`, `spec:73`).
- WC-6: a retry worker "must not corrupt the first attempt's output"; a command with no resume flag "writes each run into a fresh output directory so a re-run starts clean" (`spec:64`). About 25 rows say "Fresh dir".
- Orca's own model: a worker that ends `failed` (which is what a `blocked` report maps to, `spec:63`) leaves its Task `failed` and its dependents blocked until a `--retry-of` replacement completes it (`CAPS:90`, `CAPS:116`). So a retry after every `blocked` outcome is the normal path the spec designs for. Nothing in section 2.3 or section 7 says the coordinator must pass a new directory on a retry, and no acceptance check exercises `--retry-of`.

Grading check: An implementer who follows the stated text as written builds commands that, when the retry brief repeats the same `--output <dir>`, either write into `<dir>` (overwriting the first attempt's `return-contract.yaml` and artifacts, which WC-6 forbids) or create a new directory (so the contract is not at the path the coordinator knew before dispatch, which WC-4 requires); one of the two requirements must be broken, and the coordinator's step 4 (`test -s <contract>`, `spec:183`) then reads the first attempt's stale `blocked` contract as the retry's result, which is wrong because the retry may have succeeded.

State trace: Task T1, dispatch d1 `--output D` -> `D/return-contract.yaml {status: blocked}`; d2 `--retry-of d1 --output D` -> WC-6 "fresh dir" vs WC-4 "D". If d2 writes `D2/...`, the coordinator reads `D/...` (blocked) and marks a good run failed. Counts: 1 Task, 2 dispatches, 1 expected contract path, 2 real contract files (Quantity Flow Diagram above).

Recommendation (narrowing): in section 2.3 require the coordinator to pass a distinct `<output-dir>` per dispatch (one sentence), and reword WC-6 so "fresh output directory" means "the directory the coordinator passes for that dispatch". Add one retry case to the P2 gate-trigger check (AC-2.2).

## === ADVERSARIAL ANALYSIS (Whittaker, review order 6) ===

Format per `cmd:82`. Severity uses CRITICAL / MAJOR / MINOR; the review-loop grading (blocking vs Medium) is stated in the findings list.

- W1. I can break this specification by **Sentinel Collision Attack**. The invariant at **AC-C5 and AC-0.3 (spec:176, 193): "additive edits only"** fails when **a markdown bullet is deleted**. Concrete attack: before, a command file has `- Will Not: push to origin`; after, the line is removed. `git diff -U0` prints `-- Will Not: push to origin`. The regex `^-[^-]` excludes any line whose second character is `-`, because it is meant to skip the `---` file header. I ran `printf -- '-- item\n- x\n-plain\n' | grep -E '^-[^-]'` in the sandbox: only `- x` and `-plain` printed; `-- item` did not. The check prints nothing, so it passes. Severity MAJOR; review-loop grade Medium (M-3), because the spec's text does not itself build the wrong thing; the check is blind.
- W2. I can break this specification by **Sequence Attack**. The invariant at **WC-4/WC-6 (spec:62, 64)** fails when **a retry follows a blocked attempt**. Concrete attack: see ARCH-1. Severity CRITICAL (blocking).
- W3. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (spec:62)** fails when **the brief omits the output directory, or `--output` is a file**. Concrete attack: `/sc:tdd "<precise prompt>" --unattended --output docs/x/TDD_X.md`; there is no `<output-dir>`; the contract path is undefined; the worker reports `--report-path` to a guess. Severity MAJOR (blocking, REQ-1).
- W4. I can break this specification by **Divergence Attack**. The invariant at **WC-5 (spec:63)** fails when **a report reads `partial`**. Concrete attack: a roadmap run writes only `extraction.md` and reports `partial`; WC-5 sends `--outcome succeeded`; Orca marks the Task completed and a dependent Task becomes startable (`CAPS:90`), consuming a partial roadmap. The body sentence is the only warning (`spec:63`). The spec never says which commands may emit `partial` or what a dependent must check (M-6). Severity MAJOR; Medium.
- W5. I can break this specification by **Accumulation Attack**. The invariant at **WC-3 (spec:61)** fails when **the coordinator never answers**. Concrete attack: the worker times out, resumes the same message ID, times out again, without limit; no heartbeat is sent while blocked in `ask` (`spec:61`, `CAPS:64`), so liveness looks "healthy" forever (`CAPS:52`, `CAPS:129`). Severity MAJOR; Medium (M-10): nothing stated, so the implementer must guess a cap.
- W6. I can break this specification by **Divergence Attack**. The invariant at **WC-9 (spec:67)** fails when **a command has no explicit authorization flag**. Concrete attack: auggie-review is told "posting returns only with an explicit `--post-pr` in the brief" (`spec:100`); the inventories show only `--no-post-pr` (`INV-A:38`, `INV-A:78`), and `--post-pr` appears nowhere in the three inventories (checked by search). Severity MAJOR; Medium (M-2).

## Findings list and grading

Blocking (3). Each passes the grading check written above under its finding.

| Id | Label | Blocking | One-line wrong outcome |
|---|---|---|---|
| REQ-1 | MAJOR | yes | contract path undefined or contradicted for file-valued `--output`, adversarial, cleanup-audit, workflow; the coordinator's checks cannot pass or mis-score a good run |
| REQ-2 | MAJOR | yes | AC-1.1 requires P1 edits that the rows forbid or schedule for later phases |
| ARCH-1 | CRITICAL | yes | WC-4 and WC-6 cannot both hold on a retry; the coordinator reads a stale contract |

### follow-up candidates (Medium and minor; none fails the review, none enters the Reviser brief)

Medium (warnings):
- M-1 (Wiegers): WC-3 says the session "may" ask and re-invoke "with the answer as a flag" (`spec:61`). Several gates have no such flag (tdd topic clarification `spec:90`, recommend `spec:115`, cli-portify approvals `spec:105`). For implement, an answered `ask` would be "another agent's message", which does not count as a Ruling (`INV-A:66`, `spec:109`, `spec:233`); the row and D2 keep the rule, but WC-3 in the shared contract file reads as a general permission. AC-2.2 pins `worker_done --outcome failed` for a gate-trigger run (`spec:200`), which a worker that used WC-3's `ask` would not produce. The implementer must guess which text wins, so Medium.
- M-2 (Nygard): WC-9 turns an outward default on "only through the command's own explicit flag" (`spec:67`), but the inventories show no such flag for auggie-review (`--post-pr`), post-release, task commit/push or pr-submit (`INV-A:38`, `INV-B:79`, `INV-B:204`). The auggie-review row lists "Other required change: none" (`spec:100`) although it needs a new flag. The task row is in P2 (`spec:121`, `spec:160`) while D4 is a user decision that "affects" task (`spec:244`).
- M-3 (Whittaker W1): AC-C5 and AC-0.3 use `grep -E '^-[^-]'` (`spec:176`, `spec:193`) and cannot see a deleted bullet. Use a pattern that skips only the `--- a/...` header line (for example drop lines matching `^--- ` first, then match `^-`). Also, in the raw markdown `\|` inside AC-C1 and AC-C4 is a table escape (`spec:172`, `spec:175`); pasted into a shell it would be a literal pipe in an ERE and AC-C1 would match nothing. State the commands outside a table or say the escape is removed.
- M-4 (Fowler): between P1 and P2 a coordinator can pass `--unattended` to a gate command that still posts or waits (see REQ-2 secondary consequence). Add one sentence: a command's `--unattended` is usable only after its row's phase.
- M-5 (Cockburn): section 1.4 (2) says a command's own `AskUserQuestion` "comes *after* readiness, so it does not fail `worker-start`" (`spec:44`). README:13 states the opposite risk as binding context. For Claude the task is passed on the command line (`CAPS:47`), so the command runs at process start and a first-step question may be what readiness waits behind. The cited support (`CAPS:52`, `CAPS:129`) covers a worker already past `input_accepted`. The requirement WC-2 is unaffected; the evidence statement is stronger than its source. UNVERIFIED either way.
- M-6 (Adzic): WC-5 covers "no report exists" but not an empty, unparseable or out-of-vocabulary report (Guard Table G2), and `partial` has no definition (which commands emit it, what a dependent must check) (`spec:63`, `spec:263`). Also WC-4 says existing contracts "keep their fields" (`spec:62`) while the status set is fixed at four values; the status values of the existing brainstorm, reflect, workflow and adversarial contracts are not in the inventories, so compatibility is UNVERIFIED.
- M-7 (Cockburn): `spec:154` says "Phases 1-3 need no user decision" while `spec:225` says "Phases 0-3 can proceed on the recommendations" and D4 lists auggie-review and task (both P2) as affected (`spec:244`).
- M-8 (Newman): section 4 says of `/sc:git` that "workers make no commits or pushes" and justifies it with `README:31` (`spec:133`). README:31 is a rule for this planning run, not a standing policy, and D4(a) lets a worker push when the user's instruction names it (`spec:245`).
- M-9 (Hohpe): (a) the tasklist row has "Other required change: none" and says its reflect fan-out is inside Claude Code's nesting limit (`spec:122`), but `INV-B:210`, `INV-B:314` and `INV-B:322` mark nested spawning and who answers the remediation offer UNVERIFIED. (b) The row makes Stage 10.5 pass `--unattended` so reflect's headless auto-accept applies; the inventory recommended calling reflect without `--remediate` (`INV-B:215`). Under the spec's choice remediation actually runs inside the tasklist worker, and what happens to the `needs_human_decision` HALT (`INV-B:209`) is not stated. (c) The `--unattended` token is not defined as standalone (Guard Table G1).
- M-10 (Nygard): WC-1 says a prompt must fall back "well inside" the readiness limit with no number (`spec:59`), and WC-3 has no cap on `ask` resumes (Guard Table G4, G5; W5).

Minor notes:
- N-1. SA-3 ("only in unattended mode or when the caller passes the new output flag", `spec:148`) is unclear for commands that already have `--output` (adversarial, reflect, brainstorm): does passing the existing flag now write a contract in a standalone run?
- N-2. WC-11 relies on a "timestamp" for uniqueness (`spec:69`); two workers started in one second collide. cleanup-audit's fixed `.claude-audit/` needs a coordinator-side serialization rule in the brief template (`spec:85`, `spec:73`); the template lists none.
- N-3. WC-10 splits waits above 5 minutes into waits of at most 4 minutes (`spec:68`); a 4 min 59 s call can still exceed a 5-minute heartbeat gap. Use one number.
- N-4. The `explain` row adds Write to a read-only command's tool list (`spec:108`); SA-1 covers prompts and defaults, not tools. State that this widens the standalone tool set.
- N-5. UNVERIFIED citations (not checkable in the sandbox): `spec:11` (11 locations re-read), `spec:25` (E5 grep results), `spec:52` (`install_core.py:4,33`, `:13-24`; `CLAUDE.md:83,408`), `spec:150` (`CLAUDE.md:16,157,334`), `spec:174` and `spec:23` (codegraph README lines), `spec:183` (`pyproject.toml:38`), `spec:285` (340 citations re-read). The spec labels some of these itself; the rest are carried as fact.

The follow-up issue offer (`cmd:260`) is not asked: this run is a single-turn worker with no user in the loop, so the list above is recorded only.

## Quality assessment (standard format, scores 0-10)

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.5
  clarity: 8.0
  completeness: 7.0
  testability: 7.0
  consistency: 7.5
critical_issues:
  - {category: requirements, severity: MAJOR, expert: Wiegers, issue: "REQ-1 report location undefined or contradicted", recommendation: "state the contract path for every row"}
  - {category: requirements, severity: MAJOR, expert: Wiegers, issue: "REQ-2 AC-1.1 contradicts the rows' phases", recommendation: "scope AC-1.1 to P1 rows"}
  - {category: architecture, severity: CRITICAL, expert: Fowler, issue: "ARCH-1 WC-4 vs WC-6 on retry", recommendation: "one output-dir per dispatch"}
expert_consensus:
  - "The decision (Orca on top, commands as workers) is well supported by the inventories; every inventory citation I checked is accurate."
  - "The worker contract's rules are sound; the defects are in the report-location and phasing details."
improvement_roadmap:
  immediate: [REQ-1, REQ-2, ARCH-1]
  short_term: [M-1, M-2, M-3, M-4]
  long_term: [M-5, M-6, M-7, M-8, M-9, M-10]
adversarial_analysis: [W1, W2, W3, W4, W5, W6]
```

Strengths (for balance): the inventory-to-spec traceability is accurate (all checked `INV-*` and `CAPS:*` lines match, counts reconcile), the rejected alternative is argued with checkable Orca facts (`spec:29-39`), the evidence-strength gaps are stated plainly (`spec:41-45`), and the open decisions carry a recommendation each (`spec:224-253`).

## Reviser brief

Blocking finding ids: REQ-1, REQ-2, ARCH-1. Nothing else.

Rules for the reviser (restating `cmd:263`; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave every Medium and minor item above untouched. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
