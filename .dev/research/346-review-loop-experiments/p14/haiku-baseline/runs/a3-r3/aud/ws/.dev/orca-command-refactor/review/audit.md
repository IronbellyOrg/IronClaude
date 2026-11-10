review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

| Field | Value |
|---|---|
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (296 lines, 60320 bytes) |
| candidate sha256 | `90517bb8b39156a6ae96df698dafb7e24324de3cb8682a343273a1cbd2cce875` |
| baseline | none given; neither `--re-review` nor `--baseline` was passed, so this is a first review of the full document (no `baseline: missing` note applies) |
| reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| command run | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| review date | 2026-11-10 |
| input type | specification; not a TDD and not a PRD, so Behavioral Flow steps 6a-6d do not apply |
| prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` lines 27-32, read in full before the review |
| panel (review order) | Wiegers (requirements lead), Adzic, Cockburn, Fowler (architecture lead), Nygard, Whittaker (always active), Newman, Hohpe, Crispin (boundary-table completeness only) |
| Improve step | not run: no `--improve` was passed, and the brief forbids editing anything but this file |
| brief clauses overridden | none |

Citation keys: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `cmdmd:N` = line N of the `/sc:spec-panel` command definition supplied with this task (outside the workspace, so used only to compare, never as workspace evidence). `README:N` = `.dev/orca-command-refactor/README.md`.

## Coverage statement

Read in full: the README, the three inventories, the whole candidate, the command definition and the review-loop prompts file. Spot-checked about 60 of the candidate's `INV-A`, `INV-B` and `CAPS` citations against those files (WC-1 to WC-12, R1-R5, E1-E5, section 1.4, the section 3 and section 4 evidence cells, the section 7 `CAPS` references, D1-D5). All matched the cited line's content. Checked arithmetic: 43 = 10 + 27 + 6 (`spec:76`, `INV-A:73`, `INV-B:278`); the 3.1, 3.2 and section 4 tables hold 10, 27 and 6 rows; the phase column of each row agrees with the section 6 lists (12 + 15 + 4 + 3 = 34 edited, plus 3 unedited ready, plus 6 coordinator-only = 43).

Not checkable in this sandbox, therefore UNVERIFIED: every citation into `src/superclaude/commands/`, `src/superclaude/skills/`, `src/superclaude/cli/install_core.py`, `CLAUDE.md`, `HOW-WE-WORK.md`, `pyproject.toml`, `Makefile` and `.dev/codegraph-migration/` (the spec carries most of them from the inventories, `spec:11`); the E5 grep results (`spec:25`); the "11 re-read locations" and "about 340 citations" statements (`spec:11`, `spec:295`). The Orca-side facts are only as good as the numbered command output in `CAPS`, which cannot be re-run here.

## Grading check applied

Each blocking finding carries the sentence required by the FIRST-REVIEW prompt: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding that needed a guess about which of two readings the text allows, or that is a requirement the spec never states, is Medium and is listed under follow-up candidates whatever its expert label.

=== REQUIREMENTS ANALYSIS ===

### B-1  AC-1.1 cannot pass: it demands the `## Unattended mode` section in commands the spec itself assigns to later phases, leaves unchanged, or gives no contract
- **Severity**: CRITICAL, blocking. **Expert**: Wiegers (testability), with Whittaker (sequence attack) and Crispin (criterion coverage). **Priority**: High. **Quality-impact estimate**: Testability 8 to 4, Consistency 7 to 5 if left.
- **Stated texts that contradict**:
  1. `spec:205` (AC-1.1, a Phase 1 check): the test asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". Sections 3.1 and 3.2 hold 37 commands (10 + 27).
  2. `spec:159` (Phase 1 scope) repeats the 37: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". Its command column lists only 12 (analyze, build, business-panel, design, document, explain, index, test, load, plus fixes to adversarial, cleanup-audit, index-repo).
  3. `spec:154` and `spec:162`: "Later phases do not start until the earlier phase's checks in section 7 pass" and Phase 4 (implement, post-release, pr-submit) "waits for answers to D2-D4".
  4. `spec:250`: under D3 option (a), the recommended one, "no pr-submit changes in Phase 4".
  5. `spec:84`, `spec:87`, `spec:92`: brainstorm, init-lite and workflow have small fix "None" and are not in any phase list. `spec:112`: `/sc:load` has "Report: none" and is to be used "as a step inside another worker's brief, not as its own Task", so a section naming `return-contract.yaml` in `load` names a file it never writes.
- **Count mismatch (see Quantity Flow Diagram)**: the criterion covers 37 commands; the phases edit 34 in total, only 12 of them in Phase 1; 3 are never edited.
- **Grading sentence**: An implementer who follows AC-1.1 as written builds a Phase 1 that must add the section to implement, post-release and pr-submit (Phase 4, blocked on user decisions D2-D4 and, under D3 (a), not to be changed), to brainstorm, init-lite and workflow (rows say "None"), and to `load` (no contract), and X is wrong because the check can only pass if the implementer edits Phase 4 commands before the user decides, or edits commands the spec says to leave alone; otherwise Phase 1 never passes and, by `spec:154`, Phases 2-4 never start.
- **Recommendation** (narrow, do not add): restrict AC-1.1 and the Phase 1 sentence at `spec:159` to the commands that each phase's rows actually edit, and drop `load`, `brainstorm`, `init-lite` and `workflow` from the "names `return-contract.yaml`" assertion (or state the assertion per phase). Rationale: the per-row Phase column (`spec:83-125`) is already the authoritative assignment and is internally consistent; only the acceptance text over-reaches.

=== ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking grade. The decision itself (Orca coordinates, commands stay the units of work, `spec:13-39`) is consistent with the inventories: R1 to R5 each trace to a `CAPS` line that supports them (`CAPS:97-103`, `CAPS:145-150`, `INV-A:90`), and WC-7 and WC-8 do not depend on the unverified subagent questions (`spec:45`, `CAPS:159-160`). The architecture items below are Medium or minor.

## Follow-up candidates (Medium: warnings, never trigger a revision)

Each of these needs a guess about which reading the text allows, or states a requirement the spec never states.

### M-1  Contract location is undefined when the output flag is a file, or when no output location is passed
- **Expert**: Wiegers; Whittaker (zero/empty attack). **Priority**: High. **Impact**: Completeness -1.
- `spec:62` defines the contract as `<output-dir>/return-contract.yaml`, with `<output-dir>` "the directory the coordinator passed (`--output` / `--output-dir`)". The spec's own rows use file-valued `--output` for tdd (`spec:90`, `spec:210`) and init-lite (`spec:87`); only workflow gets the [B1] carve-out. AC-2.2 (`spec:210`) expects a `status: blocked` contract from `/sc:tdd "auth" --unattended --output <file>`, but no stated rule says where that contract goes. WC-4 also says the contract is written "on every outcome", yet nothing says what happens when `--unattended` arrives with no output location at all (compare `cmdmd:460`, which refuses before any work and prints in chat only). Boundary rows GC-3 below.
- Recommendation: one sentence stating the contract path for file-valued `--output` and the behaviour when no location is given. Not blocking because the implementer must pick between two plausible paths (guess).

### M-2  WC-6 "fresh output directory" conflicts with WC-4 "known before dispatch" unless the coordinator supplies the fresh directory, which the spec never says
- **Expert**: Nygard; Fowler. **Priority**: Medium.
- `spec:64`: a command with no resume "writes each run into a fresh output directory so a re-run starts clean". `spec:62` and `spec:73`: the contract is at a path the coordinator passes before dispatch. A command that creates its own fresh subdirectory moves the contract off the known path; a command that writes in place overwrites the first attempt's contract, which WC-6 forbids. The brief contents list (`spec:73`) has no "pass a new directory per attempt" item. Most section 3.2 rows say "fresh dir" (`spec:99-125`), so this affects about 20 commands.
- Related collision risk (UNVERIFIED, depends on how callers pass `--output`): the [B1] fix moves adversarial's contract to `<output>/return-contract.yaml` (`spec:83`), while callers that nest adversarial (brainstorm Wave 3, `INV-A:39`; release-split Part 2, `INV-B:121`; reflect Tier 2, `INV-B:111`; troubleshoot Tier 2, `INV-B:241`) write their own `<output>/return-contract.yaml` (`INV-A:39`, `INV-B:112`). If a caller passes its own directory to the nested run, both write one path. `INV-A:60` shows nested runs already produced `.../adversarial/adversarial/return-contract.yaml`, so the nesting depth of callers' output directories varies.

### M-3  "Ready today, None" rows do not meet WC-4's field list, and the status vocabulary of existing contracts is not mapped
- **Expert**: Wiegers (traceability); Newman (versioning). **Priority**: Medium.
- `spec:62` requires `status` (four values), `command`, `report_path`, `artifacts`, and `blocked_question` when blocked, and says commands with a contract "keep their fields and add the missing ones". `spec:79` says the worker reports the named file "until Phase 1 adds the contract", but Phase 1 (`spec:159`) lists no edit for brainstorm, reflect, workflow, release-split or troubleshoot. Workflow's contract carries `status`, `plan_path`, `reflect_report_path` (`INV-B:272`); its status values and whether it carries `command` are not stated. `spec:193` (step 4 of the live check) asserts `d['command']` and a four-value `status`, which the existing contracts may not satisfy. The shared contract also has no schema-version field although workflow's carries "contract 1.1" (`INV-B:272`).

### M-4  The worker-session rules (WC-3, WC-5, WC-7, WC-12) have no stated delivery path to the worker for commands that are not edited
- **Expert**: Fowler (single responsibility, interface); Hohpe (message pattern). **Priority**: Medium.
- Eleven of the twelve WC items name the "worker session" or the command as owner (`spec:57-70`). The command-side route is the `## Unattended mode` section that points at the installed contract (`spec:52`). Brainstorm, init-lite and workflow are never edited (M-3, B-1), and section 2.3 (`spec:73`) lists what the brief must contain (command line, output directory, authorizations, worktree) but not "read `~/.claude/WORKER-CONTRACT.md` and apply WC-5 outcome mapping". The brief template is deferred to Phase 0 (`spec:158`). Without it, nothing tells the worker to map `blocked`/`partial` to `--outcome` as WC-5 requires.

### M-5  WC-2 (c) "blocked, then stop" and WC-3 "ask the coordinator once" are both allowed for the same gate, and the acceptance check expects only the first
- **Expert**: Cockburn (primary actor, goal); Hohpe. **Priority**: Medium.
- `spec:60` (c) says the command writes `status: blocked` and stops; `spec:61` lets the worker session instead `ask`, wait, and re-invoke with the answer "as a flag". `spec:210` (AC-2.2) passes only on `--outcome failed` with a blocked contract. A run that took the `ask` route and succeeded would fail AC-2.2, and many gates have no flag that carries a free-text answer (for example the `cli-portify` approval gates, `spec:105`). Neither route has a rule for choosing, and the spec does not say the brief selects it.

### M-6  Interim window between P1 and P2: `--unattended` is accepted before its gates are resolved
- **Expert**: Whittaker (sequence attack). **Priority**: Medium.
- `spec:159` has Phase 1 add `--unattended` to every 3.1/3.2 command ("a no-op where a command has no gate"), while gate resolutions for auggie-review, cleanup, improve, cli-eval, task and others land in Phase 2 (`spec:160`). After Phase 1 and before Phase 2, a coordinator briefed from the section 3 table passes `--unattended` to a command whose gate or default outward action (auggie-review PR posting, `spec:100`, `INV-A:38`) is still live. The spec does not say what the flag does for a command with a gate before its phase lands.

### M-7  Phase 1 gives `/sc:explain` a Write tool for every run, not only unattended ones
- **Expert**: Nygard; Fowler. **Priority**: Medium.
- `spec:108`: "add Write to its tools (only Read/Grep/Glob, TodoWrite, Task today)" (`INV-A:48`). A tool added to the command's tool list applies in standalone runs too, which SA-1 and SA-3 (`spec:146`, `spec:148`) say must stay as today, and `spec:154` says Phases 1-3 need no user decision. No sentence restricts Write to the unattended output path. This widens a read-only command's authority; I grade it Medium because the text does not say the widening is unconditional.

### M-8  `/sc:tasklist`: the Stage 10.5 HALT is unresolved, and the nesting claim is stated as settled where the inventories mark it UNVERIFIED
- **Expert**: Nygard; Newman. **Priority**: Medium.
- `spec:122` resolves Stage 10.5 by passing `--unattended` to each reflect "so the headless rule applies". `INV-B:209` records that Stage 10.5 also says `needs_human_decision` items HALT (`SKILL.md:1631`) and that who answers inside a subagent is UNVERIFIED; the headless rule "skips the gates" for reflect (`INV-B:109`) while the tasklist text HALTs. The spec does not say which wins. The same row says the fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`", but `INV-B:210` and `INV-B:322` mark nested spawning there UNVERIFIED and `INV-A:112` marks availability of tools in nested subagents UNVERIFIED.

### M-9  `/sc:roadmap` writes memory through `/sc:save` each wave, and WC-11 is not applied to it
- **Expert**: Nygard; Whittaker (accumulation). **Priority**: Medium (UNVERIFIED which keys are written).
- `INV-B:154`: roadmap "writes memory through `sc:save` at every wave"; `INV-B:165`: the single-owner keys are "overwritten whole on each save". `spec:69` (WC-11) says single-owner shared files are not written in unattended mode, and `spec:119` fixes `/sc:save` only. The roadmap row (`spec:118`) does not say its nested saves use per-session keys, so two workers in one worktree can still clobber `pm_context`, `last_session`, `next_actions`.

### M-10  No bound on blocked-then-retry cycles
- **Expert**: Whittaker (accumulation attack); Nygard. **Priority**: Medium.
- A `blocked` result is reported as `--outcome failed` (`spec:63`), and `CAPS:80` says a worker's own failed report does not count toward the three-failure circuit breaker. WC-3 and section 2.3 imply the coordinator answers and retries with `--retry-of`. Nothing caps how many block-and-retry rounds a Task may go through.

### M-11  auggie-review names a `--post-pr` flag that no evidence shows exists
- **Expert**: Wiegers (testability). **Priority**: Low-Medium.
- `spec:100` and `spec:254` say posting returns "only with an explicit `--post-pr`". `INV-A:38` lists `--no-post-pr` (C:52) and the default-on posting (C:51) but no positive `--post-pr` flag. Precedence between `--unattended`, `--no-post-pr` and a new flag is not stated. Passing AC-2.4 (`spec:212`) does not need the flag.

### M-12  AC-0.4 gives no status to compare for `/sc:troubleshoot` and `/sc:adversarial`
- **Expert**: Crispin; Adzic. **Priority**: Medium.
- `spec:204` says Step 3 passes when `--outcome` "matches the status that the command's own report states". Troubleshoot's report is `REPORT.md` and it writes `return-contract.yaml` only for `--caller task-unified` (`INV-B:242`); adversarial's contract varies in name and location (`INV-A:60`). Only workflow's `status` key is named. For two of the three smoke runs the pass condition is therefore not defined, although the spec says a failure "reopens section 1".

### M-13  `--unattended` parsing rule is unspecified, and coordinator-only commands have no defined behaviour when it is passed
- **Expert**: Whittaker (sentinel collision attack). **Priority**: Low-Medium.
- D1 (`spec:238`) says the flag "cannot misfire on a person", but several commands take quoted free text (troubleshoot symptom, tdd prompt, spec content). The spec does not say the token counts only as a standalone argument outside quotes (`cmdmd:459` does). Section 4 (`spec:128`) says those six get no mode; it does not say what a run that receives the flag does.

### M-14  Plugin mirror has no acceptance check
- **Expert**: Newman (compatibility); Crispin. **Priority**: Low-Medium.
- UNVERIFIED #8 (`spec:289`) admits the update rule for `plugins/superclaude/commands/` was not read and leaves it to each phase plan. Section 7 has no check for it (`AC-C2`, `spec:183`, covers `.claude/` sync only).

### M-15  Requirements with no acceptance check
- **Expert**: Wiegers; Crispin. **Priority**: Low-Medium.
- Traceability: WC-1 (launch prompt), WC-3 (ask route), WC-6 (retry safety), WC-12 (`check` and `consumer_fenced`) have no AC in section 7. WC-2 and WC-4 to WC-5 and WC-7 to WC-10 are exercised through the 7.2 live check; WC-11 only through AC-3.4 (`spec:217`, save only). WC-10's "heartbeat every 5 minutes" is hard-coded from the dispatch preamble, which `spec:68` and `CAPS:130` say is not a guide value, and pr-submit's poll-iteration runtime is UNVERIFIED (`spec:293`).

## Minor notes (never fail the review)

- **N-1**: E3 (`spec:23`) cites `invocation_method: "skill-direct"` as support, while section 1.4 (`spec:43`) says the same run "proves the nested route, not the direct route". Both can be true (brief said one thing, worker did another) but the spec does not reconcile them (`INV-A:13`, `CAPS:156`).
- **N-2**: `spec:67` and `spec:133` cite `README:31` as the basis for "outward actions need the user's authorization in this repo". `README:31` is a rule "for every worker in this run", not a general repository policy.
- **N-3**: Non-goal 8 (`spec:230`) limits scope to defects that stop a command working as a worker, but the plan fixes the `load` usage line (`spec:112`) and the business-panel frontmatter (`spec:102`, effect UNVERIFIED, `INV-A:120`).
- **N-4**: AC-C5 (`spec:186`) fails on any removed line, and SA-4 (`spec:149`) allows "new flags". Adding a flag by editing an existing Usage line removes a line. `cmdmd:22-23` shows the additive way (a second Usage line); the spec does not say so.
- **N-5**: SA-2 (`spec:147`) says the only allowed Orca mention "in a changed command" is "inside the contract file"; the contract file is not a command.
- **N-6**: The pr-submit top-level rule is cited at `SKILL.md:37-39` (source, via the inventories) and at `:47-49` (installed copy, `CAPS:161`). The ten-line difference suggests the installed and source copies differ; the spec does not note it (UNVERIFIED either way).
- **N-7**: WC-4 names the output flags `--output` / `--output-dir`; `cmdmd:460` uses `--report-dir` for spec-panel (with `--output` file-valued) and already carries `--unattended`, which supports the [B4] hedge (`spec:120`, `spec:296`) but shows flag names vary.
- **N-8**: SA-1 (`spec:146`, output paths unchanged without `--unattended`) and the adversarial contract move (`spec:83`) disagree; SA-4 (`spec:149`) names the adversarial fix as an allowed exception, so the text is reconcilable.

=== MANDATORY OUTPUT ARTIFACTS ===

### Guard Condition Boundary Table (Nygard builds, Crispin validates completeness, Whittaker attacks)

Triggered: the spec contains thresholds, boolean guards and sentinels. One row per applicable input class. Status GAP means a finding: blocking only when it names a concrete wrong outcome or a security, data-loss or safety-boundary risk (FR-8, FR-9). Classes left out are listed below the table with their one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GC-1 readiness limit | spec:59, CAPS:44-45 | Zero/Empty | no startup prompt | pass | WC-1 allows it | OK |
| GC-1 readiness limit | spec:59, CAPS:49 | Typical | prompt with 30 s fallback | pass (34 s observed) | within the 60 s default | OK |
| GC-1 readiness limit | spec:59, CAPS:49 | Maximum/Overflow | fallback of 50 s | fails | requirement says only "well inside"; the ~45 s ceiling is in evidence only (CAPS:49), not in the text | GAP (Medium, M-15 area) |
| GC-1 readiness limit | spec:59, CAPS:45 | Legitimate Edge Case | `--timeout-ms` raised for one start | limit raised | WC-1 cites the flag; it does not say a raised limit relaxes the fallback rule | OK |
| GC-2 `--unattended` | spec:146 | Zero/Empty | flag absent | false | SA-1: today's behaviour | OK |
| GC-2 `--unattended` | spec:51, spec:60 | Typical | standalone token present | true | unattended mode | OK |
| GC-2 `--unattended` | spec:238 | Sentinel Value Match | token inside quoted text, e.g. `"login fails --unattended"` | ambiguous | spec silent (cmdmd:459 defines the rule) | GAP (Medium, M-13) |
| GC-2 `--unattended` | spec:128 | Legitimate Edge Case | flag passed to a section 4 command | n/a | no behaviour stated | GAP (Medium, M-13) |
| GC-2 `--unattended` | spec:159-160 | Legitimate Edge Case | flag passed after P1, gate lands in P2 | accepted, gate live | no behaviour stated | GAP (Medium, M-6) |
| GC-3 contract path | spec:62, spec:73 | Zero/Empty | `--unattended`, no output location | no path | spec silent | GAP (Medium, M-1) |
| GC-3 contract path | spec:62 | Typical | directory passed | true | `<dir>/return-contract.yaml` | OK |
| GC-3 contract path | spec:62, spec:90 | Legitimate Edge Case | `--output` is a file (tdd, init-lite) | no directory | spec silent; only workflow has a carve-out | GAP (Medium, M-1) |
| GC-3 contract path | spec:62, spec:64 | Legitimate Edge Case | directory already holds a contract (retry) | overwrite or fresh | WC-4 fixed path vs WC-6 fresh directory | GAP (Medium, M-2) |
| GC-3 contract path | spec:83 | Sentinel Value Match | nested adversarial writes the same `<output>/return-contract.yaml` as its caller | collision | spec silent (UNVERIFIED) | GAP (Medium, M-2) |
| GC-4 outcome map | spec:63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| GC-4 outcome map | spec:63 | Typical | `succeeded` | true | `--outcome succeeded` | OK |
| GC-4 outcome map | spec:63, spec:273 | Sentinel Value Match | `partial`; audit verdict FAIL | succeeded | maps to `succeeded`, body states it | OK |
| GC-4 outcome map | spec:62-63 | Legitimate Edge Case | status outside the four values (existing contracts) | unmapped | spec silent | GAP (Medium, M-3) |
| GC-4 outcome map | spec:60-61 | Legitimate Edge Case | `blocked` with a live preamble | failed or ask | two readings | GAP (Medium, M-5) |
| GC-5 wait and heartbeat | spec:68 | Typical | wait of 2 min | pass | worker heartbeats between waits | OK |
| GC-5 wait and heartbeat | spec:68, spec:276 | One/Minimal | wait of exactly 4 min | pass | allowed, margin under 5 min | OK |
| GC-5 wait and heartbeat | spec:68, spec:293 | Maximum/Overflow | single call over 5 min the command cannot split (pr-submit poll runtime, long evals) | breaks cadence | "confirm" only; runtime UNVERIFIED | GAP (Medium, M-15) |
| GC-5 wait and heartbeat | spec:68, CAPS:130 | Legitimate Edge Case | preamble cadence differs from 5 min | mismatch | cadence hard-coded | GAP (minor) |
| GC-6 nesting depth | spec:66, CAPS:97 | Zero/Empty | depth 0 coordinator | may start workers | coordinator only | OK |
| GC-6 nesting depth | spec:66, CAPS:97 | Typical | depth 1 worker calls `worker-start` | refused | WC-8 forbids the call | OK |
| GC-6 nesting depth | spec:262 | Legitimate Edge Case | user raises depth (D5 b) | allowed by Orca | WC-8 still forbids | OK |
| GC-7 task confidence | spec:121 | Zero/Empty | 0.0 | below 0.70 | blocked | OK |
| GC-7 task confidence | spec:121, INV-B:199 | Legitimate Edge Case | exactly 0.70 | not below | proceeds | OK |
| GC-7 task confidence | spec:121 | Typical | 0.85 | not below | proceeds | OK |
| GC-8 phase gate | spec:154, spec:205 | Typical | P1-edited command | passes AC-1.1 | per-row phase column | OK |
| GC-8 phase gate | spec:154, spec:162, spec:205 | Maximum/Overflow | P4 command (implement, post-release, pr-submit) | AC-1.1 fails | P1 test needs a P4 edit; P4 cannot start | GAP (blocking, B-1) |
| GC-8 phase gate | spec:84, spec:87, spec:92, spec:205 | Zero/Empty | command with "None" (brainstorm, init-lite, workflow) | AC-1.1 fails | not edited, yet asserted | GAP (blocking, B-1) |
| GC-8 phase gate | spec:112, spec:205 | Legitimate Edge Case | `load` (no contract) | AC-1.1 fails | section must name a file it never writes | GAP (blocking, B-1) |
| GC-8 phase gate | spec:250, spec:205 | Legitimate Edge Case | pr-submit under D3 (a) | AC-1.1 fails | "no pr-submit changes" | GAP (blocking, B-1) |
| GC-9 block-retry loop | spec:61, CAPS:116 | Typical | one block, one retry with the answer | pass | WC-3, `--retry-of` | OK |
| GC-9 block-retry loop | spec:63, CAPS:80 | Maximum/Overflow | repeated `blocked` rounds | breaker never trips | no cap stated | GAP (Medium, M-10) |
| GC-9 block-retry loop | spec:61, CAPS:60 | Legitimate Edge Case | `ask` timeout | pending | resume same message ID | OK |
| GC-10 pr-submit `--monitor` | spec:114, INV-B:89 | Legitimate Edge Case | `--monitor 1` | y/n gate | refused under `--unattended` | OK |

Classes left out: GC-1 One/Minimal (a 1 s prompt is covered by Typical) and Sentinel (no sentinel value in the guard); GC-2 One/Minimal and Maximum (a boolean flag has no count; repeating it changes nothing); GC-3 Maximum and One/Minimal (one file per directory, no capacity notion); GC-4 One/Minimal and Maximum (outcome is a single value per run); GC-5 Zero/Empty (a zero-length wait is no wait) and Sentinel (the 600 s budget is cumulative, `spec:68`); GC-6 Maximum and Sentinel (depth is a single integer; a malformed setting falls back to 1, `CAPS:100`); GC-7 Maximum and Sentinel (confidence is a bounded score); GC-8 One/Minimal (covered by Typical) and Sentinel (no sentinel); GC-9 Zero/Empty and Sentinel (no blocked rounds means no loop); GC-10 other `--monitor` values (`INV-B:89` reports a y/n gate only at ordinal 1).

Downstream propagation: the GAP rows feed `sc:adversarial` AD-1 as priority invariant candidates; the ten Medium GAP rows are the M-1 to M-15 items above.

### Quantity Flow Diagram (pipeline: inventory to verdict to phase to acceptance check)

```text
[Commands in cmd/: 43] --> [Verdict split] --> [ready 10] [needs change 27] [coordinator-only 6]
        (INV-A:73 5+13+3 ; INV-B:278 5+14+3 ; spec:76)
[ready 10]  --> edited: adversarial, cleanup-audit, index-repo (P1); reflect, release-split, tdd, troubleshoot (P2) = 7
            --> never edited ("None"): brainstorm, init-lite, workflow = 3
[needs change 27] --> P1: 9 (analyze, build, business-panel, design, document, explain, index, test, load)
                  --> P2: 11   --> P3: 4   --> P4: 3 (implement, post-release, pr-submit)
Edited by phase: P1 = 9 + 3 = 12 ; P2 = 11 + 4 = 15 ; P3 = 4 ; P4 = 3 ; total edited = 34
Consumer A: section 6 phase lists               expects 34 edited (12 in P1)   consistent
Consumer B: AC-1.1 and P1 scope (spec:205,159)  expects 37 with a section in P1  <-- MISMATCH (37 vs 12 in P1, 34 overall)
Consumer C: AC-1.1 "naming return-contract.yaml" expects a contract for all 37    <-- MISMATCH (load writes none)
```

The only count divergence is at the acceptance check, and it is the cause of B-1. The 43 / 10 / 27 / 6 partition is conserved.

## Expert consensus

- Wiegers, Adzic and Cockburn: the requirement set is mostly testable, with owners stated per row (`spec:57-70`), concrete examples (D1, `spec:238`) and a live check (`spec:188-196`). The one criterion that cannot pass is AC-1.1.
- Fowler, Newman, Hohpe and Nygard: the layering is sound and the rejected alternative is argued from Orca facts, not preference. Open points are delivery of the worker-session rules (M-4), contract identity and versioning (M-1 to M-3), and unbounded retry (M-10).
- Whittaker: the sequence and zero/empty attacks produced the Medium items; the only provable contradiction is B-1.
- Disagreement: none between experts on grading; Crispin would raise M-1 to blocking if AC-2.2 were the only tdd check, but the text still lets the implementer choose a path, so it stays Medium.

## Follow-up candidates (list)

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, M-14, M-15. Minor: N-1 to N-8. Issue question: not asked, because this worker has no user channel; no issue was created, and the session that ran the loop should ask the user once.

## Reviser brief

Blocking finding ids to repair: **B-1** only.

The reviser reads this report, not the command. Rules: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award a PASS. For B-1 the text to change is `spec:205` (AC-1.1) and the sentence at `spec:159`, narrowed to the commands each phase's rows edit and excluding commands with no contract.

verdict: FAIL
