review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines)
- Candidate sha256: `b72ae0165828ae31e6e86c4c17ddcc94a378f90648e36bc5398fab3017942e03`
- Baseline: none given (not a re-review). No `--re-review`, no `--baseline`; this is a first review of the full document.
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`. Iterations: one review, no Improve step, no revised specification written.
- Citation key: `S:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` in the workspace. `README:N` = `.dev/orca-command-refactor/README.md`. Any cited path outside those five files (src/, CLAUDE.md, EVIDENCE.md, the codegraph README, `~/.claude`) is UNVERIFIED here; I checked it only through the inventory line that quotes it.

## Coverage

Read in full: the candidate, README, `orca-capabilities.md` lines 40-189, `commands-a.md` lines 1-120, `commands-b.md` lines 28-52, 56-75, 86-125, 176-215, 265-323. Not read: the remaining per-command notes of `commands-b.md` (lines 1-27, 126-175, 216-264). Every `CAPS:` citation in the spec's sections 1, 2 and the UNVERIFIED list was matched to its line (all matched). The `INV-A`/`INV-B` citations in section 3 and 4 were matched where the inventory line was read (all matched). Not covered: the live repo, the 11 "re-read" locations of S:11, and the 340 citations of S:285; these are UNVERIFIED here.

## Quality scores (0-10)

Clarity 7, Completeness 7, Testability 6, Consistency 5.

## REQUIREMENTS ANALYSIS

### F-01 (CRITICAL, blocking) P1 and AC-1.1 contradict D3 (a), section 4 and the "P4 waits for D2-D4" rule (expert: Wiegers, Nygard)
- Grading sentence: an implementer who follows the stated text as written adds an `## Unattended mode` section and a `--unattended` flag to `/sc:pr-submit`, `/sc:post-release` and `/sc:implement` in Phase 1, and that is wrong because the same document says those three change only in Phase 4 after the user answers D2-D4, and recommends that pr-submit get no change at all.
- Texts in conflict:
  - S:159: Phase 1 scope is "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", and S:195 (AC-1.1) requires every command in 3.1-3.2 except `/sc:load` to have the section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`. Sections 3.1-3.2 include implement (S:109), post-release (S:113) and pr-submit (S:114), each tagged phase P4.
  - S:154: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
  - S:240 (D3 (a), recommended): "no pr-submit changes in Phase 4". S:128 and S:139: coordinator-only commands "get no `--unattended` mode"; pr-submit "stays a worker candidate only if the user accepts" D3.
  - S:52: the section is added by "each changed command".
- Concrete trace: D3 answered (a) (the recommendation, on which S:225 says Phases 0-3 proceed). P1 ships. AC-1.1 passes only if pr-submit has the section, so pr-submit has been edited; D3 (a) says it is not edited. Both cannot hold. The same applies to implement (D2) and post-release (D4).
- Recommendation: restrict P1 scope and AC-1.1 to the commands whose section-3 phase is P1-P3, and exempt the three P4 commands (and pr-submit under D3 (a)) by name, as S:195 already does for `/sc:load`.
- Priority: High.

### F-02 (CRITICAL, blocking) AC-2.3 cannot pass for `/sc:cli-portify` (expert: Wiegers, Adzic)
- Grading sentence: an implementer who follows the stated text builds a cli-portify whose three approval gates always end the run as blocked, and that is wrong against AC-2.3, which demands a happy-path run with "every required flag in the brief" ending `--outcome succeeded`; no flag exists that satisfies the gates, so the acceptance criterion cannot pass.
- Texts: S:105 says each of the three approval gates "resolves as blocked" and lists no flag, input or pre-approval that lets a run pass them. S:61 (WC-3) says `ask` never answers cli-portify approval gates. S:200-201 (AC-2.2, AC-2.3) require a happy-path run per P2 command; cli-portify is P2 (S:160). The `--resume` flag S:105 adds only reuses `resume_phase`/`resume_substep`; it carries no approval.
- Concrete trace: brief `/sc:cli-portify <workflow> --unattended --output <dir>`. Phase 1 and 2 finish, the review gate after them (INV-A:45, `sk/sc-cli-portify-protocol/SKILL.md:69`) resolves blocked, contract `status: blocked`, `worker_done --outcome failed`. Re-running with `--resume <contract>` reaches the same gate again. Phase 3 is never reached.
- Recommendation: either name an explicit pre-approval input for these gates in the cli-portify row, or declare cli-portify a "blocked-by-design" command and exempt it from AC-2.3 (the same way D2 (a) makes implement end `failed`).
- Priority: High.

### F-03 (Medium) Output directory missing: where does a `blocked` contract go?
- WC-4 says the contract is written "on every outcome" at `<output-dir>/return-contract.yaml` (S:62). Rows for post-release, document and explain say the command requires an explicit output and resolves "else blocked" (S:107, S:108, S:113). If the output is the missing item, the specified location does not exist. An implementer must guess a fallback path. Not stated: what happens when the brief omits the output directory. Follow-up: state the fallback (for example, refuse in chat only, as the installed `/sc:spec-panel` Unattended-mode section does, which is outside the evidence set and UNVERIFIED here).

### F-04 (Medium) Section 2.3 puts `--unattended` in every brief, but P0 and the "ready today" table run commands that do not accept it yet
- S:73 requires "the exact command line including `--unattended`". S:79 says the 3.1 commands run "now" with the stated flags and S:194 (AC-0.4) lists P0 command lines without `--unattended`; the flag arrives in P1 (S:159). An implementer writing the brief template (S:158) from S:73 passes an unsupported flag in P0. It depends on how an unknown flag is treated, which the document does not say. Follow-up: say that 3.1 commands are briefed without `--unattended` until P1.

### F-05 (Medium) SA-3 and WC-4 disagree on when the contract file is written
- WC-4 writes the contract "in unattended mode" (S:62). SA-3 writes it "only in unattended mode or when the caller passes the new output flag" (S:148). AC-1.3 (S:197) tests only the case with neither. A run with the output flag and no `--unattended` is left open. Follow-up: pick one trigger.

### F-06 (Medium) `/sc:save` per-session keys are written but nothing reads them
- S:119 has save write only `<key>-<session-or-timestamp>.md`. `/sc:load` reads `<key>.md` (INV-B:63) and `/sc:pm` reads fixed keys (INV-B:73). The spec's own AC-3.4 (S:207) only checks that two new files appear. Result: the saved state is never loaded. This is a missing requirement (no merge/read-back rule), not a stated text that does harm. Follow-up: say who reads the per-session files.

### F-07 (Medium) `/sc:tasklist` row asserts nesting is safe and changes the inventory's remedy without a check
- INV-B:215 says to drop `--remediate` and run the per-phase reflect at the worker's top level, and INV-B:210, INV-B:314 mark subagent-to-agent nesting UNVERIFIED. S:122 instead passes `--unattended` to each reflect and says the fan-out is "inside Claude Code's nesting limit, `INV-A:14`". INV-A:14 states a three-layer rule for Claude Code but does not trace tasklist's depth (worker, reflect subagent, Tier 2 reviewers, adversarial advocates). UNVERIFIED that the depth fits. Also S:122 turns reflect's `--remediate` into auto-accept (S:88, S:151) inside tasklist, so a corrective package may be generated per phase without anyone asking. Follow-up: add a depth count and an acceptance check, or adopt the inventory's remedy.

### F-08 (Medium) Section 3.1 says the only command changes are small fixes, but P1 and AC-1.1 touch every 3.1 command
- S:79 ("The only command changes are the small fixes") versus S:159 and S:195 (the section in all 3.1 commands, including brainstorm and init-lite whose "Small fix" cell is "None", S:84, S:87). Overlaps F-01; listed separately because it affects commands outside the P4 set.

## ARCHITECTURE ANALYSIS

The central decision (Orca coordinates, commands stay units of work, S:16, S:29-37) is supported by lines I could check: CAPS:97-103 (depth 1), CAPS:147-149 (no Orca outside), CAPS:76 and CAPS:150 (worker_done bound to the dispatched pane), CAPS:155-161 (subagents). The gaps it states in S:41-45 match CAPS:52, 129, 155-160, 186-187. No finding against the decision itself.

### F-09 (Medium) AC-C1 and SA-2 may contradict the P0 deliverables
- AC-C1 (S:172) greps `src/superclaude/core` for `orca ... (orchestration|worktree|terminal|agent)` and requires no output. P0 adds `WORKER-CONTRACT.md` (a core file, S:52) with a coordinator brief template and an Orca section in `HOW-WE-WORK.md` (S:158). SA-2 allows an Orca mention "in a changed command" as a caller's question-channel example (S:147), but says nothing about core files. Whether the new text contains the grep phrase is not stated; if it does, P0 fails its own common check. Follow-up: exempt `WORKER-CONTRACT.md` and the new HOW-WE-WORK section in AC-C1, or forbid the phrase there.

### F-10 (Medium) Brief-supplied output location is missing for several "ready today" commands
- WC-4 needs the report path known before dispatch (S:62, S:73), yet the "Brief must pass" cells for troubleshoot, reflect and release-split name no output flag while their reports sit in `<output>` or `REPORT.md` (S:88, S:89, S:91; INV-B:36, 37, 49). The coordinator cannot know `report_path` for these before dispatch. Follow-up: add the output flag to the brief cell.

### F-11 (Medium) Section 3.2 "Unattended-mode gate resolution" for the tasklist/reflect HALT
- INV-B:209 records that Stage 10.5 `needs_human_decision` items HALT. S:122 does not say how a HALT resolves under `--unattended` (blocked per WC-2 (c)) and relies on reflect's headless rule, which S:151 says is keyed on `claude --print` (S:280, UNVERIFIED item 9: assumed not applicable to Orca workers). So the headless rule may not fire for the worker even when `--unattended` is passed, unless reflect's own change (S:88) lands first. Order: reflect is P2 as is tasklist; no ordering stated. Follow-up: state that tasklist depends on the reflect change.

### N-01 (MINOR) Provenance statements disagree
- S:11 says every other section-3 line was "carried from the inventories without a second read", S:285 says a validator re-read about 340 citations in this spec. Both can be true for different passes but the reader cannot tell which lines were rechecked.

### N-02 (MINOR) `--unattended` token inside quoted task text
- Nothing says that the string `--unattended` inside a quoted topic or prompt does not switch the mode on. The installed spec-panel text restricts it to a standalone token (outside the evidence set, UNVERIFIED). Add one line to WORKER-CONTRACT.md.

### N-03 (MINOR) AC-C5 versus new flags on one-line Usage lines
- S:176 forbids any removed line; S:149 allows new flags. Adding a flag to a single Usage line removes that line in the diff. State that a second Usage line is used, or exempt Usage lines.

### N-04 (MINOR) S:51 says unattended mode is "the only command-side change besides report files and resume"; section 3 also requires wait splitting (S:104), tool additions (S:108), frontmatter and interface reconciliation (S:102, S:118, S:124-125).

## Whittaker adversarial findings

I can break this specification by **Sequence Attack**. The invariant at **S:154 and S:159 (Phases 1-3 need no user decision; P1 adds the section to every 3.1-3.2 command)** fails when **D3 is answered (a)**. Concrete attack: before: pr-submit has no Unattended-mode section, D3 unanswered. Step 1: P1 is executed per S:159 and AC-1.1 runs (S:195). After: pr-submit carries the section, which S:240 says must not exist. See F-01.

I can break this specification by **Zero/Empty Attack**. The invariant at **S:62 (WC-4, contract on every outcome)** fails when **the brief's output directory is empty or absent**. Concrete attack: post-release row S:113 resolves "else blocked"; contract path `<output-dir>/return-contract.yaml` has no directory. See F-03.

I can break this specification by **Divergence Attack**. The invariant at **S:148 (SA-3)** fails when **the caller passes the output flag but not `--unattended`**. WC-4 writes no file, SA-3 permits one. See F-05.

I can break this specification by **Accumulation Attack**. The invariant at **S:68 (WC-10, heartbeat every 5 minutes, waits at most 4 minutes)** fails when **a command sums several 4-minute waits**. No limit on total run time is set; S:282 (UNVERIFIED item 11) assumes Orca has none. Not graded: it is a stated assumption, not a wrong outcome (Medium at most, no new finding).

## Guard Condition Boundary Table

Guards found: WC-10 wait size; WC-5 outcome mapping; WC-4 output-directory presence; task confidence below 0.70 (S:121); pr-submit `--monitor 1` (S:114); Orca depth limit 1 (S:33). Classes left out: Maximum/Overflow for confidence and `--monitor` (a bounded 0-1 value and a 0-3 ordinal, no overflow case); Sentinel Value Match for WC-5 (no sentinel is used).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 output dir present | S:62 | Zero/Empty | no output flag in brief | false | not specified where a `blocked` contract goes (S:107, S:113 say "else blocked") | GAP (F-03, Medium) |
| WC-4 output dir present | S:62 | Typical | `--output <dir>` | true | contract at `<dir>/return-contract.yaml` | OK |
| WC-4 output dir present | S:62 | Legitimate Edge Case | flag takes a file (tdd, init-lite) | true | brief gives fresh dir, contract beside file | OK |
| WC-10 wait size | S:68 | Typical | wait of 3 minutes | true (no split) | heartbeat between waits | OK |
| WC-10 wait size | S:68 | Maximum/Overflow | single call of 3600 s (cli-eval) | false | split into waits of at most 4 minutes (S:104) | OK |
| WC-10 wait size | S:68 | Legitimate Edge Case | exactly 5 minutes | true | rule says "longer than 5 minutes" must be split, and splits at "at most 4"; exactly 4-5 minutes unspecified | GAP (minor, inferable) |
| WC-5 outcome | S:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| WC-5 outcome | S:63 | Legitimate Edge Case | `partial` | true | `succeeded`, body states status | OK |
| WC-5 outcome | S:63 | Legitimate Edge Case | audit verdict FAIL | true | `succeeded` | OK |
| task confidence <0.70 | S:121 | Typical | 0.60 | true | blocked | OK |
| task confidence <0.70 | S:121 | Legitimate Edge Case | exactly 0.70 | false | proceeds (inferred from "below 0.70") | OK |
| pr-submit `--monitor 1` | S:114 | Typical | `--monitor 1 --unattended` | true | refused | OK |
| depth limit | S:33 | One/Minimal | depth 1 worker calls `worker-start` | true | refused `nested_worker_depth_exceeded` (call-site enforcement UNVERIFIED, CAPS:103) | OK (UNVERIFIED) |
| cli-portify approval gate | S:105 | Typical | brief with every flag | true | blocked, no flag passes it | GAP (F-02, blocking) |
| P1 section guard | S:195 | Legitimate Edge Case | command is a P4 command or pr-submit under D3 (a) | true | section required (AC-1.1) and forbidden (S:240) | GAP (F-01, blocking) |

## Follow-up candidates (Medium and minor, not blocking)

F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11 (Medium); N-01, N-02, N-03, N-04 (minor). The session that ran this review asks the user once whether to open an issue for them; none is created here.

## Panel consensus and disagreement

- Consensus: the coordinator-on-top decision is well evidenced for the facts checkable here, and the stated gaps (S:41-45) are honest.
- Disagreement: Nygard would grade F-09 and F-11 higher (a self-failing P0 check; an unordered dependency). I graded them Medium because each needs a guess about text that is not yet written.

## Reviser brief

Blocking finding ids: F-01, F-02. Restated rules for the reviser (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
