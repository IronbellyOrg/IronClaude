review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (round 1)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none (first review; no `--re-review`, no `--baseline`)
- prior report: none
- reviewer model: claude-haiku-5-5, one reviewer, one context
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`)

Citation key: `spec:N` = candidate line N. `INV-A:N` = `inventory/commands-a.md` line N. `INV-B:N` = `inventory/commands-b.md` line N. `CAPS:N` = `inventory/orca-capabilities.md` line N. Anything cited to a file outside the workspace (`src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `~/.claude/...`) could not be checked here and is UNVERIFIED.

## 1. Coverage and method

- Read in full: `command.md`, `.dev/orca-command-refactor/README.md`, the FIRST-REVIEW prompt file, the candidate, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`.
- Inventory citations: every `INV-A`, `INV-B` and `CAPS` citation that a finding below depends on was opened and read against the claim. The rest of the candidate's inventory citations (about 60 lines in total) were sampled. No mismatch was found. The candidate's counts were recomputed: 21 + 22 = 43 commands; 10 ready + 27 needs-change + 6 coordinator-only = 43; phases P1 9 + P2 11 + P3 4 + P4 3 = 27 needs-change rows, and the ready set splits as 8 with fixes + 2 unchanged = 10. All consistent.
- Behavioural check run in the sandbox: the grep alternation in AC-C1 (finding B4). The escaped form `\|` printed 0 matches on a line containing `orca orchestration ask`; the unescaped form printed 1.
- Not run: the FIRST-REVIEW prompt asks for three reviewers in fresh contexts and the MERGE rule. This sandbox has one worker and no fresh-context reviewer, so this file is one first review. The coordinator must run two more first reviews and the MERGE rule before this round is complete.
- Not run: the VERIFY prompt (fresh verifier, candidate plus finding list only). The blocking findings below are pending it. A reply with no `confirmed:` line confirms all of them.
- Mandatory output artifacts: Guard Condition Boundary Table triggered (section 3.1). Pipeline Dimensional Analysis triggered in its count form (section 3.2). State Variable Registry not triggered, because the correctness focus is not active.
- Focus checked: requirements (WC-1 to WC-12, SA-1 to SA-6, AC-C1 to AC-4.3, D1 to D5) and architecture (coordinator/worker split, rejected alternative, phase order, coordinator-side obligations).

## 2. Blocking findings

### B1. Contract directory is undefined for file-valued or fixed-path commands (requirements, WC-4)

- Evidence: WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" and requires the path known before dispatch (`spec:62`; `spec:73`).
- `/sc:tdd` takes `--output <file>` (`spec:90`; `INV-B:222`). `/sc:init-lite` takes `--output <file>` (`spec:87`; `INV-A:55`). The AC-2.2 gate-trigger example passes `--output <file>` to tdd (`spec:200`).
- `/sc:cleanup-audit` writes a fixed `.claude-audit/` with no output flag (`spec:85`; `INV-A:42`). `/sc:index-repo` writes `PROJECT_INDEX.md` with "brief must pass: none" (`spec:86`; `INV-A:53`).
- Grading sentence: the stated text defines `<output-dir>` as a directory, and the tdd row passes a file, so the text contradicts itself. An implementer following WC-4 cannot say where `return-contract.yaml` goes for `/sc:tdd --output <file>`. The coordinator then cannot open the contract at the path it was given, and AC-2.2 step 4 (`spec:183`, `spec:200`) reads a file the spec never names.
- Recommendation: define the directory for file-valued output (for example its parent directory), or add a `--contract-dir` flag. Add an output-directory flag to cleanup-audit and index-repo before they count as ready.

### B2. AC-0.4 step 4 cannot pass for the P0 smoke commands (acceptance)

- Evidence: AC-0.4 uses "the command's existing report file" for step 4 (`spec:194`). Step 4 loads YAML and asserts `status` and `command` keys (`spec:183`).
- `/sc:troubleshoot` writes `REPORT.md` as `report_path`. Its return contract exists only with `--caller task-unified` (`spec:91`; `INV-B:242`). `/sc:adversarial` names no contract filename (`spec:83`; `INV-A:35`, `INV-A:60`). Both are in the P0 smoke set (`spec:158`).
- Grading sentence: an implementer who runs step 4 on `REPORT.md` gets a markdown file with no `status` or `command` keys, so step 4 fails on the first P0 troubleshoot run and P0 cannot close as written.
- Recommendation: state, for each P0 command, which file step 4 checks. Apply the YAML assertions only where a YAML contract exists.

### B3. Section 3.1 says ready commands change only in one column, which contradicts P1 and AC-1.1 (requirements)

- Evidence: `spec:79` says the ten ready commands "run as workers now" and "The only command changes are the small fixes in the last column." `spec:52` says each changed command "adds a short `## Unattended mode` section." P1 requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (`spec:159`). AC-1.1 requires every command in 3.1 to 3.2 to have the section (`spec:195`).
- Grading sentence: an implementer following `spec:79` leaves the ten ready commands without the `## Unattended mode` section and without the flag. AC-1.1 then fails in P1. The two stated texts contradict each other.
- Recommendation: change `spec:79` to say the ready commands also gain the section and the flag in P1, in addition to their small fixes.

### B4. AC-C1 matches nothing as written, and it cannot pass P0 as scoped (acceptance, SA-2)

- Evidence: AC-C1 (`spec:172`) writes its alternation as `(orchestration\|worktree\|terminal\|agent)` inside `grep -E`. In `grep -E`, `\|` is a literal pipe, so the pattern never matches an Orca subcommand. The sandbox check in section 1 confirms this. The `\` is a GFM table escape, so the rendered page looks correct and the raw text does not work.
- AC-C1 scans `src/superclaude/core`, and its only exclusion is `ccsession-tag` (`spec:172`). P0 writes `src/superclaude/core/WORKER-CONTRACT.md` and adds an Orca section to `src/superclaude/core/HOW-WE-WORK.md` (`spec:158`). SA-2 allows an Orca mention "inside the contract file" (`spec:147`). AC-C1 has no exemption for it.
- Grading sentence: an implementer who copies AC-C1 as written gets a check that passes any command calling `orca orchestration`, so SA-2 (a hard requirement, `spec:142`) is not enforced. An implementer who fixes the escaping, and writes the routing-guide section with any `orca orchestration` text as P0 asks, fails AC-C1 in P0. The stated texts contradict each other.
- Recommendation: write the alternation unescaped. Exempt `WORKER-CONTRACT.md` and the `HOW-WE-WORK.md` section by name, or keep that section free of subcommand text. See also M11.

## 3. Mandatory output artifacts

### 3.1 Guard Condition Boundary Table

Triggered: the candidate contains conditional logic and thresholds (WC-1, WC-2 to WC-5, WC-10, WC-12, D1, D4). Guards WC-7 and WC-8 are prohibitions with no input condition and are left out for that reason. D2 is a decision, not a guard. Status `GAP` rows map to findings. FR-8 and FR-9 gaps are blocking only where they name a wrong outcome; the grade is in the Finding column.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 outcome from `status` | `spec:63`, `spec:182`, `spec:263` | Zero/Empty | report absent | failed | failed ("no report exists", `spec:63`) | OK |
| G1 | `spec:63` | Zero/Empty | report present, 0 bytes | not matched | unspecified | GAP (M6) |
| G1 | `spec:63`, `spec:62` | One/Minimal | `status` present, `command` absent | matched | unspecified; `spec:62` requires `command` | GAP (M6) |
| G1 | `spec:63` | Typical | `status: succeeded` | matched | `--outcome succeeded` | OK |
| G1 | `spec:63` | Maximum/Overflow | `status: PASS` (outside the four values) | not matched | unspecified | GAP (M6, M10) |
| G1 | `spec:63`, `spec:263` | Sentinel Value Match | `status: partial` | matched | `--outcome succeeded`; dependents released (`CAPS:77`, `CAPS:86`) | GAP (M3) |
| G1 | `spec:63`, `spec:200` | Legitimate Edge Case | `status: blocked`, empty `blocked_question` | matched | `failed`; `spec:200` requires a non-empty question | GAP (M6) |
| G2 ask wait | `spec:61`, `spec:64` | Zero/Empty | no question asked | n/a | n/a | OK |
| G2 | `spec:61` | Typical | `ask` times out | resume same message ID | `CAPS:60` | OK |
| G2 | `spec:61` | Maximum/Overflow | coordinator never answers | wait | no bound stated; default timeout UNVERIFIED (`CAPS:68`) | GAP (M1) |
| G2 | `spec:61` | Sentinel Value Match | answer arrives after the command already stopped as blocked | no pause point | unspecified | GAP (M1) |
| G2 | `spec:61` | Legitimate Edge Case | session holds no preamble | `ask` unavailable | blocked | OK |
| G3 contract directory | `spec:62`, `spec:73` | Zero/Empty | no output flag (analyze, build, design before P1) | n/a | unspecified | GAP (B1) |
| G3 | `spec:62`, `spec:90`, `spec:87` | One/Minimal | `--output` names a file | directory undefined | unspecified | GAP (B1) |
| G3 | `spec:62` | Typical | `--output <dir>` | contract at `<dir>/return-contract.yaml` | `spec:62` | OK |
| G3 | `spec:62`, `spec:63` | Maximum/Overflow | output directory unwritable | no contract | WC-5 maps "no report" to failed | OK |
| G3 | `spec:85`, `spec:86` | Sentinel Value Match | fixed default path (`.claude-audit/`, `PROJECT_INDEX.md`) | collides with a second worker | unspecified | GAP (M4) |
| G3 | `spec:62` | Legitimate Edge Case | relative `--output` | resolved against which cwd | unspecified | GAP (N1) |
| G4 wait length | `spec:68`, `spec:181`, `spec:210` | Zero/Empty | no tool call | none | n/a | OK |
| G4 | `spec:68` | Typical | single call 60 to 240 s | no split | `spec:68` | OK |
| G4 | `spec:68` | Maximum/Overflow | single call over 5 min | must split into at most 4 min | stated; enforced only by the live checks in section 7.2 | OK |
| G4 | `spec:68`, `spec:283` | Sentinel Value Match | pr-submit poll iteration | runtime unknown | UNVERIFIED item 12 | GAP (M12) |
| G4 | `spec:68` | Legitimate Edge Case | heartbeat while in `ask` | none sent | `CAPS:64` | OK |
| G5 unattended switch | `spec:51`, `spec:60`, `spec:228` | Zero/Empty | flag absent | standalone | SA-1 | OK |
| G5 | `spec:51` | One/Minimal | flag present, required flag absent | unspecified | unspecified | GAP (M7) |
| G5 | `spec:51` | Typical | all required flags present | unattended | `spec:60` | OK |
| G5 | `spec:51`, `spec:104` | Maximum/Overflow | `--unattended` with `--interactive` | unspecified for commands that do not refuse it | unspecified | GAP (M7) |
| G5 | `spec:51` | Sentinel Value Match | flag text inside a quoted argument | unspecified | unspecified | GAP (M7) |
| G5 | `spec:90`, `spec:104` | Legitimate Edge Case | "precise component prompt" (tdd), "safety flags" (cli-eval) | not testable | no test or flag set named | GAP (M7) |
| G6 readiness | `spec:59` | Zero/Empty | no launch prompt | ready | `spec:59` | OK |
| G6 | `spec:59` | Typical | launch prompt with fallback under the limit | ready | `spec:59`; evidence outside workspace (UNVERIFIED) | OK |
| G6 | `spec:59` | Maximum/Overflow | prompt blocks past 60 s | `agent_readiness` failure | `CAPS:44` | OK |
| G6 | `spec:59` | Sentinel Value Match | fallback set at 50 to 60 s | unspecified | "well inside" has no number | GAP (N1) |
| G7 outward switch | `spec:67`, `spec:245` | Zero/Empty | no outward flag | off | `spec:67` | OK |
| G7 | `spec:67`, `spec:245` | Typical | flag in brief quoting the user | on | D4(a) | OK |
| G7 | `spec:67` | Sentinel Value Match | flag in brief not quoted from the user | on | command cannot check the quote | GAP (N2) |
| G7 | `spec:67`, `spec:122` | Legitimate Edge Case | auto-accepted reflect remediation | unspecified | unspecified | GAP (M5) |
| G8 fence | `spec:70` | Zero/Empty | empty `check` | continue | `CAPS:67` | OK |
| G8 | `spec:70` | Typical | no fence | continue | OK |
| G8 | `spec:70` | Sentinel Value Match | `consumer_fenced` | stop, no `worker_done` | `CAPS:67` | OK |

Completeness (FR-10): every guard above has its input classes listed or left out with a reason. The conditionals are WC-1, WC-2 (its three-way resolution is covered by G5 and G2), WC-3, WC-4, WC-5, WC-9, WC-10, WC-12 and D1. The rows cover them. No guard is left out without a stated reason.

### 3.2 Pipeline Dimensional Analysis (count form)

Trigger: the candidate's classification is a multi-stage flow in which counts are re-partitioned, and the WC-4 to WC-5 status mapping reduces the count of values. Stage counts below.

```text
[INV-A 21 commands (INV-A:3)] + [INV-B 22 commands (INV-B:3)] = 43            (spec:75)
   |  verdict split
   v
[ready 10 (spec:83-92)] + [needs-change 27 (spec:97-125)] + [coord-only 6 (spec:132-137)] = 43   N=M, OK
   |  phase assignment (spec:158-162)
   v
ready 10 = 8 with fixes (P1 4 + P2 4) + 2 unchanged (brainstorm, init-lite)                   OK
needs-change 27 = P1 9 + P2 11 + P3 4 + P4 3                                                 OK
   |  recommended D3(a) (spec:240): pr-submit leaves the worker set
   v
worker set 36 = ready 10 + needs-change 26;  coord-only 7 = 6 + pr-submit                   MISMATCH (M2)
   |  status mapping: WC-4 four values (spec:62) -> WC-5 two outcomes (spec:63)
   v
4 statuses -> 2 outcomes: {succeeded, partial} -> succeeded; {failed, blocked} -> failed     COUNT-REDUCING at partial (M3)
   |  consumers of the outcome: Orca settles the Task on worker_done (CAPS:77), and the ready view releases dependents (CAPS:86)
   v
dependents of a partial run are released on "succeeded"; spec:73 gives no rule about them   MISMATCH (M3)
```

The count mismatch M2 is a classification inconsistency, not a data-flow count divergence with a consumer, so FR-19 does not apply to it. M3 is a count-reducing divergence with a consumer. FR-19 labels such a mismatch CRITICAL. This review grades by consequence instead (review rule 2), and it is Medium because `spec:263` calls a partial deliverable "usable". The coordinator should decide whether dependents may run.

### 3.3 State Variable Registry

Not triggered: `--focus correctness` is not active.

## 4. Medium and minor findings (follow-up candidates, not in the Reviser brief)

- **M1 (requirements and architecture, WC-3).** WC-3 says a session "may instead ask the coordinator once", then "re-invoke or resume the command with the answer as a flag" (`spec:61`). No command has a pause point between its steps. No section 3 row names an answer flag (`spec:81-92`, `spec:97-125`). A re-invoked command that runs in a fresh directory (WC-6, `spec:64`) repeats its work. No bound is set on waiting, and the default `ask` timeout is UNVERIFIED (`CAPS:68`). Grade: undefined mechanism, so Medium under rule 2.
- **M2 (requirements, classification).** `spec:75` and the table at `spec:114` count pr-submit among the 27 needs-change commands. `spec:139` and D3(a) (`spec:240`) recommend it not run as a worker. Under the recommended design the worker set is 26 needs-change and 7 coordinator-only, not 27 and 6 as stated. Section 6 still lists pr-submit in P4 (`spec:162`).
- **M3 (architecture, outcome mapping).** `partial` maps to `succeeded` (`spec:63`, decision at `spec:263`). Orca settles the Task on a valid `worker_done` (`CAPS:77`), and the ready view then starts dependents (`CAPS:84-86`). Section 2.3 says the coordinator opens the report and releases the worker (`spec:73`) but gives no rule about dependents. The decision row calls partial output usable, so the wrong outcome depends on a further assumption. Medium, with a request for an explicit coordinator rule.
- **M4 (architecture, WC-11).** WC-11 forbids two workers in one worktree writing the same file (`spec:69`). Orca's default is a shared worktree (`CAPS:115`). The ready set includes commands with fixed paths: adversarial's contract filename (`spec:83`), cleanup-audit's `.claude-audit/` (`spec:85`, which says "one audit per worktree at a time", a scheduling rule not in section 2.3, `spec:73`), index-repo's `PROJECT_INDEX.md` (`spec:86`), and reflect's default-on folder move (`spec:88`; `INV-B:114`). Two workers collide on these.
- **M5 (architecture, Stage 10.5 and WC-9).** Stage 10.5 passes `--unattended` to each reflect (`spec:122`). The reflect fix auto-accepts remediation under `--unattended` (`spec:88`; SA-6 at `spec:151`). UNVERIFIED item 9 concedes Orca may not look headless to reflect (`spec:280`; `INV-B:109`). WC-9 (`spec:67`) does not say whether an auto-accepted handoff that creates a workflow or task-builder package (`INV-B:36`) is an outward action.
- **M6 (requirements, WC-5 edge cases).** WC-5 maps only "no report exists" (`spec:63`). AC-7.2 step 4 requires a non-empty file (`spec:183`). AC-2.2 requires a non-empty `blocked_question` (`spec:200`). Undefined: an empty file, a contract with no `command` (`spec:62`), a status outside the four values, and `blocked` with an empty question.
- **M7 (requirements, unattended rules).** The candidate does not say what happens when `--unattended` is present but a required flag is absent (for example analyze before P1, `spec:99`), when `--unattended` is combined with `--interactive` (refused only in some rows, `spec:103`, `spec:110`, `spec:118`), or when the flag text sits inside a quoted argument. Two gate conditions cannot be tested as written: tdd's "precise component prompt" (`spec:90`) and cli-eval's "safety flags" (`spec:104`), which name no flag set.
- **M8 (architecture, shared file).** Each unattended section points to `~/.claude/WORKER-CONTRACT.md` (`spec:52`). The candidate has no fail-closed rule for a missing file, such as a user who has not re-run `superclaude install`.
- **M9 (requirements, roadmap).** The `[Y/n]` resume prompt "is replaced by the explicit resume flag" (`spec:118`). SA-1 says every prompt stays without `--unattended` (`spec:146`). The row sits in the unattended column, but the text should say the change applies only under `--unattended`.
- **M10 (requirements, UNVERIFIED).** WC-4 says commands that already write a contract "keep their fields" (`spec:62`), and `spec:262` fixes four status values. The existing status values of reflect, workflow, brainstorm and adversarial contracts are not in the inventories, so the mapping is not stated. UNVERIFIED here.
- **M11 (acceptance, AC-C1 scope).** Even when repaired, AC-C1's alternation (`spec:172`) omits `orca status`, `orca open` and `orca-cli`, and the uppercase `ORCA` form the candidate itself uses (`spec:180`). SA-2 forbids any `orca` or `orca-ide` call, not only four subcommands.
- **M12 (open, UNVERIFIED).** The pr-submit poll-iteration runtime is unknown (`spec:283`), and AC-4.3 depends on it (`spec:210`).
- **N1 (minor).** "Well inside the readiness limit" (`spec:59`) has no number. The relative `--output` path (G3) is resolved against an unstated working directory.
- **N2 (minor).** Under G7, D4 requires the user's instruction to be quoted in the brief (`spec:245`), but the command cannot check the quote. Note it in the brief template.
- **N3 (minor).** Item 14 in the UNVERIFIED list (`spec:285`) is a log of an earlier citation check, not an open question. Move it to a changelog.

## 5. Checks that passed

- Inventory citations behind B1 to B4 and M1 to M11 match their inventory lines (section 1).
- Count arithmetic in section 3 and section 6 is consistent (section 3.2).
- The CAPS citations for the readiness limit, `ask`, `worker_done`, depth 1, release, and liveness match their lines.
- The rejected alternative (`spec:28-39`) relies on `CAPS:97-103`, which says what it claims.

## 6. Reviser brief

Blocking finding ids: B1, B2, B3, B4.

Restated rule (review-loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
