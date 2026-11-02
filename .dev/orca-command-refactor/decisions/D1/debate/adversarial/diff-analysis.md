# Diff Analysis: D1 option-argument comparison (how a command knows it runs without a person)

## Metadata
- Generated: 2026-11-02T15:37:10Z
- Step: 1 (diff analysis), /sc:adversarial Mode A
- Decision: D1, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:328-331`
- Variants compared: 3 (V1 option a, V2 option b, V3 option c)
- Total differences found: 36 (S + C + X + U)
- Categories: structural (7), content (13), contradictions (7), unique (9), shared assumptions (9: UNSTATED 4, STATED 4, CONTRADICTED 1)
- Taxonomy tags across S, C, X, A (36 points): L3 19, L2 14, L1 3

## Structural Differences

Variant key: V1 = `variant-1-original.md` (option a, flag), V2 = `variant-2-original.md` (option b, detect Orca), V3 = `variant-3-original.md` (option c, flag plus worker-session guard). `SPEC:N` and `CAPS:N` as defined in the variants; `V1:N` = line N of variant 1, and so on.

| # | Area | V1 (a) | V2 (b) | V3 (c) | Severity | Tag |
|---|------|--------|--------|--------|----------|-----|
| S-001 | Opening section | Goes straight to Safety; no "case for" section | "Strongest case for it" section before Safety | "Why a third option" section that critiques (a) and (b) before its own case | Low | L1 |
| S-002 | Advocacy posture | Advocates its option and names one "Known weakness" (V1:19) | Advocates (b) in its first section, then argues against its own environment route in Safety and Reliability (V2:13, V2:17-19); never states which route it recommends | Advocates (c) as a strict superset of (a); no self-critique | Medium | L2 |
| S-003 | Commitment to one mechanism | One mechanism (standalone token) | Two sub-mechanisms (environment variable, preamble) offered as alternatives; never picks one (V2:3) | One mechanism in commands plus a second check owned by the worker session | High | L2 |
| S-004 | Where the switch logic lives | Command files plus `WORKER-CONTRACT.md` | Every command file (detection text per command, V2:25) | Command files (as V1) plus one rule in the worker-session part of `WORKER-CONTRACT.md` (V3:23) | High | L3 |
| S-005 | Citation keys | `SPEC`, `CAPS` only | Adds `[G] N` = line N of `orca-ide skills get orchestration` output, which a reviewer can only re-read by running Orca | Same `[G]` key as V2 | Low | L1 |
| S-006 | Relation to other options | Stand-alone; mentions (b) only as a misfire risk | Stand-alone; compares itself to (a) on non-Orca callers (V2:18) | Defined by reference to (a) ("exactly as in option (a)", V3:3) and framed as a fix for both (a) and (b) | Medium | L2 |
| S-007 | Day-to-day section depth | Two bullets, covers person and coordinator | One bullet, mostly a restated risk | One bullet, covers person and coordinator | Low | L1 |

## Content Differences

| # | Topic | V1 (a) approach | V2 (b) approach | V3 (c) approach | Severity | Tag |
|---|-------|-----------------|-----------------|-----------------|----------|-----|
| C-001 | Safety for people (SA-1) | A person's run cannot switch: person never types the flag; quoted text never counts (V1:8, `SPEC:55`, AC-2.8 `SPEC:269`) | Environment route is unsafe (would drop `/sc:cleanup --interactive` prompts in a person's Orca tab, V2:13); preamble route is "safer" because a person's session has no preamble (V2:14) | Same as (a): no command reads environment or conversation (V3:11) | High | L3 |
| C-002 | Outward defaults for people (WC-9) | Explicit: flag turns outward defaults off only under the flag, so a person in Orca keeps auggie-review posting (V1:10) | Mentions loss of "outward defaults" only as a side effect of the environment misfire (V2:13) | Not discussed beyond "same as (a)" | Medium | L3 |
| C-003 | Reliability / testability | "Deterministic and checkable by text"; AC-1.1 and 7.2 checks (V1:13); but admits the parse is applied by the model reading a rule (V1:22) | "Not mechanically testable: there is no token to grep"; a wrong model guess is invisible until a stall or a missing prompt (V2:17); preamble and task share one command line, hard to separate in tests (V2:14) | "Deterministic: a string check on the brief's command line" testable with one extra 7.2 run (V3:16); admits the rule is "prose read by a model" (V3:17) | High | L3 |
| C-004 | Forgotten-flag stall | Named as the known weakness; caught only after the fact by the brief template and the 7.2 step-3 stall proof (V1:19, `SPEC:238`) | Removes "that whole failure class" because there is no flag to forget (V2:9) | Turns the stall into an immediate `worker_done --outcome failed` with reason `brief lacks --unattended` (V3:3, V3:12, V3:20) | High | L3 |
| C-005 | Caller-neutrality (SA-2, non-goal 1) | Flag names the condition, not the tool; serves `claude -p`, CI, other orchestrators (V1:14, `SPEC:54`, `SPEC:361`) | Concedes (b) ties every command to Orca, conflicts with non-goal 1 and SA-2, and does nothing for `claude -p`/CI (V2:18) | Command side identical to (a); the Orca-aware check sits in the worker session, which already has Orca duties (V3:8, WC-3/5/7/12) | High | L2 |
| C-006 | Coordinator day-to-day | Copies the command line from the brief template; must remember the flag (V1:18-19) | No flag to remember; shorter briefs (V2:10, V2:22) | Must still write the flag, but a miss produces a named failure instead of a stall to diagnose with `worker-read` (V3:20) | Medium | L2 |
| C-007 | Implementation cost | One shared parse rule and refusal list in the contract file, plus a short `## Unattended mode` section per command (V1:22) | "Low per brief, higher per command": detection text naming Orca in each command; AC-C1 exception needed (V2:25) | All of (a)'s cost plus one sentence in `WORKER-CONTRACT.md` and one live check (V3:23) | Medium | L2 |
| C-008 | Reversibility | Cheap: detection can be added later as an extra trigger (V1:23) | Expensive: undoing means touching every command again (V2:25) | Guard removable with a one-line change (V3:23) | Low | L2 |
| C-009 | `ORCA_TERMINAL_HANDLE` evidence | Cites the 2026-11-02 observation (variable set, handle not among 11 `worker-list` handles) as proof detection misfires; resolves UNVERIFIED item 13 (V1:9) | Cites the same observation against its own environment route (V2:13) | Cites the same observation against (b) (V3:8) | Medium | L3 |
| C-010 | Orca's own definition of a worker | Not used | Orca's role table defines a worker by a live preamble with Task and Dispatch IDs (V2:8, `[G]` 38/41, `CAPS:148`) | Uses the same definition to justify putting the check in the worker session (V3:8) | Medium | L3 |
| C-011 | Coordinator-only commands run by a worker | Not addressed | Not addressed | Guard also refuses the six section-4 commands (V3:3, V3:13) | Medium | L3 |
| C-012 | Repo precedent for headless detection | Not addressed | `/sc:reflect` detects `claude --print` with no TTY; would not fire for an Orca worker (V2:19) | Not addressed | Low | L2 |
| C-013 | Phase gating of the flag | Flag accepted only after a command's gates are converted (V1:15, `SPEC:187-195`) | Not addressed | Not addressed; guard behaviour for commands not yet accepting the flag is unstated (see X-005) | Medium | L3 |

## Contradictions

| # | Point of conflict | Side A (quoted) | Side B (quoted) | How to falsify | Impact | Tag |
|---|-------------------|-----------------|-----------------|----------------|--------|-----|
| X-001 | Can preamble recognition be trusted? (V2 vs V3) | V2:14: preamble detection "relies on the model noticing prose in its context ... hard to tell apart in a test"; V2:17: "a wrong guess by the model is invisible" | V3:8: the worker session is where "detection is already authoritative"; "Orca itself tells that session it is a worker through the preamble" | Both rest on the same mechanism (a model reading the preamble). A 7.2-style run where the worker session must state its Task/Dispatch IDs before running the command shows whether recognition is reliable | High | L3 |
| X-002 | Does (b) remove the forgotten-switch failure class? (V2 intra-variant) | V2:9: "Detection removes that whole failure class" | V2:17: "a wrong guess by the model is invisible until a run stalls or a prompt disappears" | A missed detection reproduces exactly the stall V2:9 says is removed; a single worker run where the model does not act on the preamble falsifies V2:9 | High | L3 |
| X-003 | Is the flag switch "deterministic"? (V1 and V3 intra-variant; V2 cross-variant) | V1:13: "Deterministic and checkable by text"; V3:16: "Deterministic: a string check on the brief's command line" | V1:22: "the 'parse' is applied by the model reading the rule, not by code"; V3:17: "The worker rule is prose read by a model" | Text checks (grep of briefs and command files) are deterministic; the runtime switch is not. AC-2.8 (`SPEC:269`) is a manual check, which confirms the runtime part is not mechanically proven | Medium | L3 |
| X-004 | Can detection be added later "cheaply"? (V1 intra-variant, and V1 vs V2) | V1:23: "if detection ever becomes reliable, it can be added as an extra trigger without removing the flag" | V1:14 relies on SA-2 / caller-neutrality, and V2:18 notes non-goal 1 forbids "Orca-specific branching" in commands (`SPEC:314`); V2:25: "Undoing it later means touching every command again" | Adding Orca detection to commands later breaks the SA-2 constraint V1 itself cites, so it is not a cheap add-on unless SA-2 changes | Medium | L2 |
| X-005 | Does V3's guard refuse legitimate flagless worker briefs? (V3 vs spec plan it inherits) | V3:3: "if the command line in its Task has no standalone `--unattended` ... it does not run it"; V3:23: add "one live check in P0 or P1" | `SPEC:181` and `SPEC:191`: P0 smoke runs are dispatched as real workers with "each command's existing flags" and no `--unattended`; `SPEC:197`: `/sc:load` "never gains the flag" yet is used inside a worker's brief; `SPEC:187` gates the flag per phase | If the guard ships in P0 (where `WORKER-CONTRACT.md` is written, `SPEC:181`), AC-0.4 smoke runs are refused. V3 must exempt pre-conversion briefs or ship the guard after P0 | High | L3 |
| X-006 | Does (b) shorten briefs and avoid new flags on 35 commands? (V2 vs spec) | V2:10: "Shorter briefs and no new flag on 35 commands" | `SPEC:57` and WC-4 (`SPEC:68`): under unattended mode every brief must still pass exactly one report directory (`--report-dir` is a new flag on many commands) | The `--unattended` token is the only flag (b) removes; `--report-dir` and section-3 required flags remain in every brief | Medium | L2 |
| X-007 | Does the forgotten flag have to be caught "after the fact"? (V1 vs V3) | V1:19: the brief template and 7.2 step-3 stall proof "catch it, but only after the fact" | V3:12: "A wrong brief fails fast and visibly instead of stalling" | Not a factual conflict on (a) itself; V3 adds a mechanism V1 does not consider. Falsifiable by the V3:16 live run (flag omitted: pass = `worker_done --outcome failed`, no `agentWait`) | Low | L2 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | States plainly that the flag "parse" is done by the model reading a rule, not by code, and that this is why the quoted-argument rule exists (V1:22) | High |
| U-002 | V1 | Links D1 to WC-9: under (a) a person working in Orca can never lose auggie-review's posting default (V1:10, `SPEC:73`, `SPEC:169`) | Medium |
| U-003 | V1 | Phase gating: a command accepts the flag only after its gates are converted, so the flag never promises behaviour the command lacks (V1:15, `SPEC:187-195`) | Medium |
| U-004 | V2 | Grounds worker identity in Orca's own role table (live preamble with Task and Dispatch IDs = worker; no preamble = ordinary agent) (V2:8, `CAPS:148`) | High |
| U-005 | V2 | Splits (b) into environment and preamble routes with different safety profiles (V2:13-14) | Medium |
| U-006 | V2 | Shows the repo's only headless precedent (`claude --print`, no TTY) would not fire for an Orca worker (V2:19, `SPEC:391`) | Medium |
| U-007 | V3 | Moves the Orca-aware check to the worker session, which is already Orca-aware and outside SA-2's scope, turning a silent stall into a named `worker_done --outcome failed` (V3:3, V3:8, V3:12) | High |
| U-008 | V3 | The same guard blocks the six coordinator-only commands from running as workers, which today only section 4 prose forbids (V3:13, `SPEC:151`) | Medium |
| U-009 | V3 | Concrete live check for the forgotten flag: one extra 7.2 run with the flag omitted; pass = `worker_done --outcome failed`, no contract, no `agentWait` (V3:16) | Medium |

## Shared Assumptions

| # | Agreement point | Precondition it depends on | Classification | Promoted | Tag |
|---|-----------------|---------------------------|----------------|----------|-----|
| A-001 | The 2026-11-02 observation shows `ORCA_TERMINAL_HANDLE` is set in Orca terminals that are not dispatched workers, so the environment route misfires on people (V1:9, V2:13, V3:8) | (i) `worker-list --json` returned every live worker (no paging, run, terminal-state or remote filtering; `CAPS:127` says it returns "at most 100 local rows" and `CAPS:128` that remote workers need `--include-remote`); (ii) the observing session was a person-started or coordinator tab, not a worker; (iii) `agentTerminalHandle` values use the same format as `ORCA_TERMINAL_HANDLE`. None of the three variants states these. Re-check by this agent: the variable is set in this subagent's environment (`term_feb70160-...`); `worker-list` was not re-run (Orca commands are out of bounds for this step) | UNSTATED | [SHARED-ASSUMPTION] | L3 |
| A-002 | A stall on a prompt is silent: Orca reports a waiting worker as "healthy, not failed" (V1:19, V2:9, V3:7) | `CAPS:52`, `CAPS:129` quote `[H:worker-show]` line 16 directly | STATED | no | L3 |
| A-003 | A person never types `--unattended` as a standalone token (V1:8; V3:11 inherits; V2 does not dispute) | No person copies a coordinator brief's command line into their own session, and no doc or routing guide shows the flag to people. `SPEC:329` states "a person never types it" as a design intent, not an enforced guard | UNSTATED (precondition) | [SHARED-ASSUMPTION] | L3 |
| A-004 | The model correctly applies text rules at runtime (the flag parse rule under (a)/(c); preamble recognition under (b)/(c)) | V1:22 and V3:17 state the rules are model-applied; V1:13 and V3:16 also call them "deterministic"; V2:14/17 says model recognition is unreliable. The variants disagree on how far this holds (X-001, X-003) | CONTRADICTED | no | L3 |
| A-005 | Every legitimate worker brief carries `--unattended` (V3's guard depends on it; V1:18 implies it via the brief template) | Contradicted by the spec's own plan: P0 smoke runs use no flag (`SPEC:181,191`); `/sc:load` never gains the flag (`SPEC:197`); unconverted commands cannot accept it (`SPEC:187`). No variant states the assumption | UNSTATED | [SHARED-ASSUMPTION] | L3 |
| A-006 | SA-2 and non-goal 1 are fixed constraints that D1 must respect (V1:14, V2:18 concedes, V3:8) | `SPEC:170`, `SPEC:314` | STATED | no | L2 |
| A-007 | Non-Orca headless callers (`claude -p`, CI, other orchestrators) are a real requirement to weigh (V1:14, V2:18; V3 inherits from (a)) | `SPEC:54` says the mode "serves any caller"; no variant shows such a caller is in this project's scope or planned. AC-1.3 uses `claude -p` only for file-creation checks | STATED | no | L2 |
| A-008 | A `worker_done --outcome failed` with a reason reaches the coordinator sooner than a stall is proven (V3:12, V3:20; V1:19 implicitly agrees by calling the stall check "after the fact") | The coordinator's `check --wait --types "worker_done,..."` loop (`SPEC:238`) returns on `worker_done` promptly, while the stall proof needs a timed-out wait plus a transcript read | STATED | no | L3 |
| A-009 | The coordinator writes every brief from the `WORKER-CONTRACT.md` template (V1:18; V3 relies on the template to normally include the flag; V2 relies on it for report directory) | `SPEC:58`, `SPEC:79` describe the template; nothing enforces its use | UNSTATED (precondition) | [SHARED-ASSUMPTION] | L2 |

Promoted [SHARED-ASSUMPTION] points for the debate: A-001, A-003, A-005, A-009. A-004 is CONTRADICTED and is carried by X-001 and X-003.

## Citation spot-check

Six decision-critical citations re-read on 2026-11-02. `[G]` lines were not re-read (that needs `orca-ide`, out of bounds here); they are judged through the CAPS lines that quote them.

| # | Cited by | Citation | What it actually says (short quote) | Verdict |
|---|----------|----------|-------------------------------------|---------|
| 1 | V1:9, V2:13, V3:8 | `SPEC:330` | "whether it is also set in a person's own Orca tab is UNVERIFIED, and if it is, prompts would vanish for a person working in Orca, breaking SA-1; preamble detection depends on the model reading prose and cannot be tested mechanically" | CONFIRMED |
| 2 | V1:19, V2:9, V3:7 | `CAPS:52` | "observation.agentWait names a worker parked on a prompt only a human can answer ... A waiting worker is healthy, not failed." | CONFIRMED |
| 3 | V2:8 | `CAPS:148` | "`[G]` line 41: 'No live preamble and no explicit supervision \| Ordinary terminal agent' ... only a session that received a preamble with Task and Dispatch IDs is (`[G]` line 38)" | CONFIRMED |
| 4 | V3:12 | `CAPS:73` | "`[G]` lines 88-90: '... explicit `--outcome succeeded` or `--outcome failed`. Never encode failure only in prose.'" | CONFIRMED |
| 5 | V2:14 | `CAPS:47` (claim: "the worker preamble arrives on the same command line as the task") | "For Claude the task is passed on the command line, not typed" (`promptInjectionMode: 'argv'`). The line says nothing about the preamble | OVERSTATED |
| 6 | V2:25 | `SPEC:205-212` (claim: "AC-C1's grep would need an exception") | The AC-C1 pattern is `\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b`, case-sensitive lowercase. A check of `ORCA_TERMINAL_HANDLE` or of preamble prose would not match it, so AC-C1 needs no exception. The real conflict is SA-2's text at `SPEC:170` ("The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file"), which V2:18 already cites | WRONG (for AC-C1; the underlying SA-2 point stands) |

Additional notes, not counted above:
- V3:8 cites `[G]` lines 78-82 for "Orca itself tells that session it is a worker through the preamble". `CAPS:61` quotes `[G]` lines 80-82 as the rule to use the preamble's `ask` command, not as an identity statement; the identity rule is `[G]` lines 38 and 41 (`CAPS:148`). Likely OVERSTATED range; not re-read.
- V2:18 `CLAUDE.md:74`: "Commands, skills, agents, hooks and core files are copied to `~/.claude/` ... and then run in OTHER projects". CONFIRMED.
- V2:19 `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:239-242`: "`--print` mode is the headless signal". CONFIRMED.
- `ORCA_TERMINAL_HANDLE` evidence: partly reproduced. The variable is set in this analysis subagent's environment (2026-11-02T15:37Z). The `worker-list` half of the observation was not re-run.

## Summary
- Total structural differences: 7
- Total content differences: 13
- Total contradictions: 7
- Total unique contributions: 9
- Total shared assumptions surfaced: 9 (UNSTATED 4, STATED 4, CONTRADICTED 1); promoted [SHARED-ASSUMPTION] points: A-001, A-003, A-005, A-009
- Citation spot-check: 6 checked; 4 CONFIRMED, 1 OVERSTATED (V2 on `CAPS:47`), 1 WRONG (V2 on AC-C1, `SPEC:205-212`)
- Highest-severity items: S-003, S-004, C-001, C-003, C-004, C-005, X-001, X-002, X-005
- Points the debate must settle first (all L3): X-005 (V3's guard refuses the spec's own flagless P0 smoke runs and `/sc:load` briefs unless exempted); X-001 and X-002 (whether a model reliably recognizes the preamble, which both (b) and (c) lean on); A-001 (whether the `ORCA_TERMINAL_HANDLE` observation really shows the variable in a person's own tab).
- All three variants agree that the environment-variable route is unsafe for people; the live dispute is between (a) and (c), and whether (b)'s preamble route survives X-002.

### Similarity check
Comparable items: 28 claim bullets/paragraphs across the three variants (V1 10, V2 10, V3 8). Differences (S + C + X): 27, about 96% of comparable items. That is far above the 10% threshold, so the variants are not near-duplicates and a full debate is warranted.
