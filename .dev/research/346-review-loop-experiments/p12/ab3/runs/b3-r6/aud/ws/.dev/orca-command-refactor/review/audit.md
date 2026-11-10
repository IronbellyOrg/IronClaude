review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit of the final spec; no `--re-review`, no `--baseline`, so this is a first review)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `361193fc0635fb15c8c62bef7845f79c10650c2ce1378fb6cefbbb9b882a7ae8` (285 lines)
- baseline: none given (first review, nothing to diff)
- reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5)
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (lines 1-55). No brief clause was overridden.
- citation shorthand: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## Coverage (what was and was not checked)

Covered: the whole candidate (all sections 1-9, the Decisions table and the UNVERIFIED list), read against README and the three inventories.

Checked and found as cited:
- Every `INV-A:` / `INV-B:` line reference in sections 1.2, 3.1, 3.2, 4 and Decisions was resolved against the inventory files. Each lands on the row or note the spec attributes to it (for example `INV-A:35`, `INV-A:106`, `INV-B:272`, `INV-B:320`).
- Every `CAPS:` line reference was resolved the same way (for example `CAPS:49`, `CAPS:90`, `CAPS:130`, `CAPS:176-188`). No wrong line was found.
- The command counts (43 = 21 + 22; 10 ready / 27 needs-change / 6 coordinator-only) match the inventories (`INV-A:73`, `INV-B:278`) and the rows of SPEC:81-92, 97-125, 130-137. The phase lists at SPEC:159-162 cover all 27 needs-change commands exactly once.
- One mechanical claim was run: the regex in SPEC:176 and SPEC:193 (see M-1).

UNVERIFIED in this sandbox (no file inside the workspace to check): every citation of `src/superclaude/...` (`cmd/`, `sk/`, `ag/`), `CLAUDE.md:N`, `pyproject.toml:38`, `Makefile:68-74`, `install_core.py`, `EVIDENCE.md:N`, `.dev/codegraph-migration/...`, and the Orca-guide / Orca-JS line numbers. Where such a citation is only a pass-through of an inventory claim, the inventory line was checked instead (see above). The spec's own claims of "about 340 citations re-read" (SPEC:285) and "11 locations re-read" (SPEC:11) are also UNVERIFIED here.

Not covered: the correctness of the inventories' source readings themselves (out of scope for a spec audit and not checkable here); the Orca CLI behaviour (read from `CAPS:` only).

Panel: Wiegers, Adzic, Cockburn (requirements focus); Fowler, Newman, Hohpe, Nygard (architecture focus); Whittaker (active in every review). Review order is the command's fixed order.

## Grading summary

No finding passed the grading check for blocking. Each finding below needs a guess that an implementer picks the worse of two readings the text allows, or is a requirement the document never states, so each is Medium (a warning under `follow-up candidates`) or minor. Open blocking findings: 0.

Quality (0-10): clarity 8, completeness 7, testability 7, consistency 7. The decision (Orca on top, commands as units) is well supported and the evidence gaps are stated plainly (SPEC:41-45). The weaknesses are in the acceptance checks and in undefined edges of the new `--unattended` mode.

## === REQUIREMENTS ANALYSIS ===

### M-1 Additive-edit check cannot see deleted bullet lines (Medium, Wiegers, priority High, quality impact -1 testability)
- Where: SPEC:176 (AC-C5) and SPEC:193 (AC-0.3): `git diff -U0 ... | grep -E '^-[^-]'`, "prints nothing: edits are additive".
- Defect: a removed or rewritten markdown bullet (`- Will Not: ...`) appears in the diff as `-- Will Not: ...`, whose second character is `-`, so the regex skips it. Verified with a two-file experiment in the sandbox: changing `- Will Not: push` to `- Will Not: push or pull` printed nothing, while a changed table row (`| a | b |`) was printed. SA-4 (SPEC:149) and SA-1 (SPEC:146) are therefore not enforced for bullet lines.
- Why Medium, not blocking: the sentence "an implementer builds X and X is wrong" needs the assumption that the command files contain bullet lines that a phase will rewrite. The inventories quote such lists (for example the "Will Not" lists at `INV-A:35`, `INV-A:49`), but the files are not in the workspace (UNVERIFIED).
- Recommendation: replace the pass condition with a check that counts removed lines, for example `git diff --numstat master...HEAD -- <file>` with deleted-count 0, or `git diff -U0 ... | grep -E '^-' | grep -vE '^---'`.

### M-2 `--unattended` detection is undefined for free-text arguments (Medium, Wiegers/Whittaker sentinel-collision attack, priority High)
- Where: SPEC:51 (mode "when its caller passes `--unattended`"), SPEC:228 ("It is testable by grep and cannot misfire on a person"), SPEC:146 (SA-1 hard requirement).
- Attack: I can break this specification by **Sentinel Collision**. The invariant at SPEC:228 (the flag cannot misfire on a person) fails when a person's free-text argument contains the string `--unattended` (for example a `/sc:tdd` or `/sc:task` prompt about this very feature, or `/sc:spec-panel` run on this spec). Concrete attack: before = person runs `/sc:tdd "design the --unattended flag for X"` expecting the clarification prompt; after = a command that matches the substring switches to unattended mode and resolves the topic-only gate as `blocked` (SPEC:90) with no prompt, breaking SA-1.
- Why Medium: the spec never says how the token is matched; whether an implementer picks substring or standalone-token matching is a guess.
- Recommendation: state in section 2.1 that the mode applies only when `--unattended` is a standalone argument token outside any quoted argument, and add one assertion for it to AC-1.1.

### M-3 Interaction of `--unattended` and the new output flag is not specified (Medium, Adzic/Whittaker zero-attack and divergence attack, priority Medium)
- Where: SPEC:62 (WC-4: contract written "in unattended mode"), SPEC:148 (SA-3: files written "only in unattended mode or when the caller passes the new output flag"), SPEC:197 (AC-1.3 covers only "no `--unattended` and no new output flag").
- Zero/empty attack: `--unattended` with no output flag. Rows such as analyze (SPEC:99) say "add `--output`", but nothing says whether the command refuses, picks a default directory, or writes nowhere. The coordinator is only told to pass the path (SPEC:73); the command side is silent.
- Divergence attack: output flag without `--unattended`. SA-3 allows the contract; WC-4 says unattended mode only. Both readings pass AC-1.3.
- Why Medium: a requirement the document never states (an undefined state), not a stated text that does harm.
- Recommendation: add one sentence to section 2.1 or WC-4 fixing both cases (for example: `--unattended` without an output path is refused as `blocked`; the contract is written whenever `--unattended` is passed and never otherwise) and one AC-1.3 variant for each.

### M-4 No rule against a stale contract file (Medium, Whittaker sequence attack, priority Medium)
- Where: SPEC:61 (WC-3: after an answer the session re-invokes the command), SPEC:62-63 (WC-4/WC-5: "no report exists" means failed), SPEC:64 (WC-6).
- Attack: **Sequence**. After a `blocked` run the contract sits in the output directory. The session asks, gets an answer and re-invokes the command into the same directory; if the second run dies before it writes (context exhaustion, kill), the old `status: blocked` file is still there. WC-5's "or no report exists" never triggers, and the coordinator reads a stale blocked question as the current result. Nothing requires the command to delete or overwrite the contract at start.
- Why Medium: requires the second run to die early; the text does not state what happens.
- Recommendation: require the command to write (or truncate to) `status: running` at start, or require WC-5 to compare the contract's mtime with the dispatch start.

### M-5 Contracts of the ten "ready" commands: when do they get the WC-4 fields? (Medium, Wiegers, priority Medium)
- Where: SPEC:79 ("the worker reports the named file until Phase 1 adds the contract"), SPEC:76 ("the P1 small fixes to ready commands ... add none"), SPEC:159 (P1 scope: eight no-gate commands plus small fixes), SPEC:62 ("Commands that already write a contract keep their fields and add the missing ones"), SPEC:183 (check requires `status` in the four-value set and a non-empty `command`).
- Defect: SPEC:79 says Phase 1 adds the contract for the ready commands; SPEC:76 and SPEC:159 say it does not. Brainstorm, workflow and init-lite appear in no phase scope at all, and adversarial, reflect, release-split, tdd and troubleshoot get only a filename or gate fix. The existing contracts' `status` vocabularies and the presence of `command` / `artifacts` are not recorded anywhere in the inventories (`INV-B:272` lists workflow's fields as `status`, `plan_path`, `reflect_report_path`). So the 7.2 step 4 check (SPEC:183) cannot pass for those commands as written, and WC-5 cannot map their status.
- Why Medium: it needs the guess that the checks are meant to apply to them; AC-0.4 (SPEC:194) deliberately exempts P0, and no AC runs 7.2 on them later.
- Recommendation: replace "until Phase 1 adds the contract" with the real rule, and either list an explicit phase for adding `command` / `artifacts` / the four-value status to each existing contract or state that WC-5 reads the existing vocabularies.

### M-6 Whether the worker may use `ask` after a `blocked` stop is left open, but the acceptance checks assume it does not (Medium, Cockburn/Hohpe, priority Medium)
- Where: SPEC:61 (WC-3: "may instead ask the coordinator once"), SPEC:60 (WC-2 (c): stop), SPEC:73 (brief contents do not mention it), SPEC:200 (AC-2.2: `worker_done --outcome failed`, `agentWait` never shown).
- Defect: with `ask` allowed the same input yields a parked worker and a later `succeeded` outcome; with it forbidden it yields `failed`. AC-2.2 passes only under the second reading, and the coordinator brief (SPEC:73) is the only place the choice could be made.
- Recommendation: add "whether the worker may `ask` on a blocked gate" to the SPEC:73 brief list, and let AC-2.2 state which reading it tests.

### M-7 Fixed output locations of ready commands under WC-11 are handled for one command only (Medium, Wiegers/Fowler, priority Low)
- Where: SPEC:69 (WC-11), SPEC:85 (cleanup-audit flagged), SPEC:86 (index-repo: only "state the output location"), SPEC:88 (reflect).
- Defect: index-repo writes `PROJECT_INDEX.md` / `PROJECT_INDEX.json` at a fixed location (`INV-A:53`), and reflect UC-2 moves the work-unit folder by default and writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (`INV-B:114`). Two workers in one worktree can collide on either, and a retry worker (WC-6) can overwrite the first attempt. SPEC:88 offers `--no-promote` only "when the coordinator owns folder moves", and the memory file is not mentioned.
- Recommendation: add the same one-audit-per-worktree note to the index-repo row and list the reflect memory file in the reflect row (or in WC-11).

### M-8 AC-1.1's negative assertion collides with AC-C3 in later phases (Medium, Adzic, priority Low)
- Where: SPEC:195 (the test asserts "no other command ... has one yet"), SPEC:174 (AC-C3: no test that passed in the baseline may fail), SPEC:199 (AC-2.1: the test "gains" assertions).
- Defect: once P2 adds `## Unattended mode` to other commands, the P1 negative assertion fails, and AC-C3 forbids a baseline-passing test from failing. The spec says the test gains assertions, not that the P1 one is replaced.
- Recommendation: state in AC-1.1 that the "none elsewhere yet" assertion is per-phase (a phase-to-command map in the test), or drop it.

### M-9 Minor consistency gaps (minor notes, no effect on the verdict)
- n-1: SPEC:16 says command changes are "limited to" the worker contract, but the rows add other changes (SPEC:102, 108, 118, 124, 125); SA-4 (SPEC:149) and non-goal 8 (SPEC:220) already cover them. Reword SPEC:16.
- n-2: P1 is titled "commands with no gate" and "No person gate is involved" (SPEC:159), but its rows include refusal resolutions (business-panel `--mode socratic`, explain `--format interactive`, test `--watch`; SPEC:102, 108, 123).
- n-3: SPEC:45 says "has no proven limit, but no proof of none either"; the intended meaning is "no limit was found, and none is proven absent" (`CAPS:155`).
- n-4: WC-10 splits waits only above 5 minutes (SPEC:68) but AC-4.3 fails any single call above 240 s (SPEC:210) and the pr-submit row asks for iterations under 4 minutes (SPEC:114). Pick one threshold.
- n-5: E3 (SPEC:23) cites `invocation_method: "skill-direct"` as support, while section 1.4 (1) says the PR #329 run proved only the nested route (SPEC:43). Say in E3 that the evidence is for the nested route.
- n-6: WC-9 (SPEC:67) lets the brief authorize an outward action through "the command's own explicit flag", while D4 (a) (SPEC:245) requires the coordinator to quote the user's own instruction. State that D4 (a) tightens WC-9, or mirror it in WC-9.
- n-7: the acceptance check at SPEC:183 relies on PyYAML as a "declared dependency" (`pyproject.toml:38`, UNVERIFIED); the dependency list in the project instructions names only pytest, click and rich.

## === ARCHITECTURE ANALYSIS ===

### M-10 `--unattended` is not propagated to nested invocations, except tasklist to reflect (Medium, Fowler/Newman, priority Medium)
- Where: SPEC:122 (tasklist passes `--unattended` to each reflect), SPEC:90 (tdd nested `/task`), SPEC:121 (task, whose TFEP calls troubleshoot, `INV-B:201`), SPEC:104 (cli-eval create runs spec-panel and adversarial, `INV-A:44`), SPEC:89 (release-split runs brainstorm and adversarial, `INV-B:121`).
- Defect: WC-2 (SPEC:60) says a command under `--unattended` never blocks on a person, but a command that calls another gate-bearing command is covered only where a row happens to say so. Nested calls are not a stated requirement, and the order of changes inside a phase is not stated either: tasklist depends on reflect accepting the flag (both P2, SPEC:160).
- Why Medium: a requirement never stated; the rows that matter today are individually handled.
- Recommendation: add one line to WC-2 ("a command run with `--unattended` passes it to every command it invokes that accepts it, and refuses to invoke one that does not and may gate") and order reflect before tasklist inside P2.

### M-11 The tasklist row asserts nested spawning is safe, against its own inventory (Medium, Nygard/Newman, priority Medium)
- Where: SPEC:122 ("inside Claude Code's nesting limit, `INV-A:14`"), SPEC:268 (inventory verdicts kept), SPEC:271-285 (UNVERIFIED list).
- Defect: `INV-B:210` and `INV-B:314` mark nested spawning from Stage 10.5 as UNVERIFIED, and `INV-B:215` recommended running the reflect fan-out at the worker's top level. The spec instead cites `INV-A:14` (a general statement from fetched documentation, which is not repo evidence) as if it settled the question for reflect's Tier 2 (reviewers, calibrators, adversarial advocates below one subagent). The item is not in the spec's UNVERIFIED list and the departure from `INV-B:215` is not recorded in Decisions.
- Concrete wrong outcome risk: if the Agent tool is withheld at depth, Stage 10.5 degrades silently in a run nobody watches.
- Recommendation: carry the item into the UNVERIFIED list and add an AC (a P2 live run of tasklist without `--no-reflect`), or follow `INV-B:215` (reflect at top level).

### M-12 "AskUserQuestion comes after readiness" is stated as fact (Medium, Nygard, priority Medium)
- Where: SPEC:44 ("A command's own `AskUserQuestion` or chat question comes after readiness, so it does not fail `worker-start`").
- Defect: `CAPS:47` records that Claude receives its task on the command line, so the command runs from the first turn. A first-turn `AskUserQuestion` dialog could occupy the screen before Orca sees a fresh input box, the same shape as the `EVIDENCE.md:39` failure (`CAPS:49`). `CAPS:52` and `CAPS:129` support only that a worker waiting after `input_accepted` is healthy. The claim is not in the UNVERIFIED list. It matters in phases before P2, where gate commands are briefed without `--unattended` (SPEC:154).
- Recommendation: mark the claim UNVERIFIED and add a P0 smoke run of one gate-bearing command with a deliberately gated input, or state the claim as "after `input_accepted`".

### M-13 Roadmap acceptance check overwrites state in the same directory (Medium, Nygard, priority Low)
- Where: SPEC:205 (AC-3.2: existing `<dir>/.session-memory.md`, no resume flag, "starts fresh"), SPEC:64 (WC-6: a retry must not corrupt the first attempt's output), SPEC:118.
- Defect: "starts fresh" in the same `<dir>` overwrites the first attempt's partial roadmap, which WC-6 forbids for commands without the resume flag (fresh directory) and which a coordinator that forgets the flag on a retry will trigger.
- Recommendation: AC-3.2 should expect a new directory (or a refusal) when state exists and no resume flag is given.

### M-14 AC-C1 conflicts with what P0 must write (Medium, Fowler, priority Medium)
- Where: SPEC:172 (AC-C1: nothing under `src/superclaude/{commands,skills,agents,core}` may match `orca(-ide) (orchestration|worktree|terminal|agent)`, one exemption), SPEC:147 (SA-2 allows a mention of Orca inside the contract file), SPEC:158 (P0 adds a coordinator brief template and an Orca section to `HOW-WE-WORK.md`; both live under `core/`).
- Defect: the exemption covers only `skills/ccsession-tag/`. A brief template or routing-guide section that names the Orca commands the coordinator runs (the template lists the section 7.2 command forms) matches the pattern, so P0 can fail the check that every phase must pass (SPEC:169).
- Why Medium: it depends on how those files are worded (the spec does not require the literal command forms).
- Recommendation: exempt `core/WORKER-CONTRACT.md` and the new routing-guide section explicitly, or state that they must avoid those literal forms.

### M-15 AC-C1 as written in the file is not the command that was meant (Medium, Fowler, priority Low)
- Where: SPEC:172. The cell holds `(orchestration\|worktree\|terminal\|agent)` and `\| grep -v`; the backslashes are table-cell escapes. A reader who copies the raw file text into a shell gets a regular expression whose `\|` is a literal pipe, which matches nothing, so the check passes vacuously.
- Recommendation: put the command in a fenced block below the table, or note that `\|` must be unescaped.

## Mandatory output artifacts

### Guard Condition Boundary Table
Triggered: the spec contains conditional logic, thresholds and sentinels (mode switch, wait threshold, outcome mapping, readiness limit, depth fence). Classes left out are named with a one-line reason; all other cells are populated. Status GAP rows map to the findings above; none names a concrete wrong outcome without a further guess, so none is blocking (FR-8/FR-9 grading).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 `--unattended` mode switch | SPEC:51, 62, 148 | Zero/Empty | `--unattended` with no output path | true | unspecified (refuse, default dir or write nowhere) | GAP (M-3) |
| G1 | SPEC:228 | One/Minimal | `"--unattended"` inside a quoted prompt | ambiguous | unspecified (substring or token match) | GAP (M-2) |
| G1 | SPEC:51 | Typical | standalone token, output path given | true | gates resolve per row; contract written | OK |
| G1 | SPEC:148 vs 62 | Legitimate Edge Case | output flag given, no `--unattended` | false | SA-3 allows the contract, WC-4 does not | GAP (M-3) |
| G1 | n/a | Maximum/Overflow | left out: a boolean flag has no capacity | n/a | n/a | n/a |
| G2 wait split (WC-10) | SPEC:68 | One/Minimal | one 1-minute wait | false (no split) | not split | OK |
| G2 | SPEC:68 | Typical | 10-minute poll wait | true | split into waits of at most 4 minutes | OK |
| G2 | SPEC:68, 210 | Legitimate Edge Case | single call of 4 to 5 minutes (270 s) | false | allowed by WC-10, failed by AC-4.3 (240 s) | GAP (n-4) |
| G2 | SPEC:68 | Maximum/Overflow | eval of 3600 s (`INV-A:65`) | true | split into 4-minute waits | OK |
| G2 | n/a | Zero/Empty, Sentinel | left out: a zero-length wait needs no split; no sentinel value exists | n/a | n/a | n/a |
| G3 outcome mapping (WC-5) | SPEC:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G3 | SPEC:63, 183 | One/Minimal | empty or unparseable file | unspecified | WC-5 silent; only the AC step 4 rejects it | GAP (M-5) |
| G3 | SPEC:63 | Typical | `status: succeeded` | false | `--outcome succeeded` | OK |
| G3 | SPEC:63, 263 | Legitimate Edge Case | `partial`, or audit verdict FAIL | false | `--outcome succeeded`, body states status | OK |
| G3 | SPEC:62-63 | Sentinel Value Match | `status` outside the four values (existing contracts), or stale `blocked` file | unspecified | unspecified | GAP (M-4, M-5) |
| G3 | n/a | Maximum/Overflow | left out: a status value has no capacity | n/a | n/a | n/a |
| G4 readiness limit (WC-1) | SPEC:59 | Typical | launch fallback of 30 s | false | start passes (34 s observed, `CAPS:49`) | OK |
| G4 | SPEC:59 | Legitimate Edge Case | fallback above about 45 s | true | start fails (`CAPS:49`) | OK |
| G4 | SPEC:59 | Maximum/Overflow | `--timeout-ms` above the accepted bound | unspecified | bound UNVERIFIED (`CAPS:176`); WC-1 does not depend on it | OK |
| G4 | SPEC:44 | One/Minimal | command's own first-turn `AskUserQuestion` | unspecified | claimed to be after readiness (UNVERIFIED) | GAP (M-12) |
| G4 | n/a | Zero/Empty, Sentinel | left out: a zero timeout is replaced by the 60 s default (`CAPS:44`); no sentinel value exists | n/a | n/a | n/a |
| G5 nesting depth (WC-8) | SPEC:66, 33 | Typical | coordinator starts a worker (depth 1) | false | allowed | OK |
| G5 | SPEC:66 | Legitimate Edge Case | command attempts `worker-start` from a worker | true | forbidden; Orca refuses at depth 1 (`CAPS:99`) | OK |
| G5 | SPEC:252 | Maximum/Overflow | depth raised by the user (D5 (b)) | false | WC-8 still forbids the call | OK |
| G5 | n/a | Zero/Empty, One/Minimal, Sentinel | left out: depth is a fixed small integer setting (malformed values fall back to 1, `CAPS:100`) | n/a | n/a | n/a |

### Whittaker attack summary
- Zero/Empty Attack: M-3 (no output path), G3 empty contract file.
- Divergence Attack: M-3 (SA-3 vs WC-4), n-4 (5-minute rule vs 240 s check).
- Sentinel Collision Attack: M-2 (`--unattended` inside user text), M-5 (status vocabulary), M-4 (stale `blocked` file).
- Sequence Attack: M-4 (blocked, ask, re-invoke, crash), M-13 (state overwritten without a resume flag).
- Accumulation Attack: none found. The counters the spec uses (three-failure circuit breaker, heartbeat cadence, one `worker_done`) are defined by Orca (`CAPS:80`, `CAPS:73`) and the spec states their limits (SPEC:63, 68).

### Pipeline Dimensional Analysis
Not triggered. The spec describes a coordinator, Task, worker and report flow, not a data pipeline whose stage counts diverge. The fan-out counts of individual commands (for example 2N validators in tasklist) are facts of the cited commands, not designed here, and only the nesting claim of M-11 touches them. No Quantity Flow Diagram.

### State Variable Registry
Not required: `--focus correctness` was not requested. Advisory only (not forced): the spec introduces several mutable states (contract `status`, Task and Dispatch status, the single-owner memory keys at SPEC:69), which meets the auto-suggestion threshold for `--focus correctness`. A later review could use it.

## Follow-up candidates (Medium and minor; never trigger a revision)

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-10, M-11, M-12, M-13, M-14, M-15 (Medium); n-1 to n-7 (minor).

Question for the user: open an issue for these follow-up candidates? This run was a non-interactive worker run and could not ask; no issue was created.

## Reviser brief

No blocking finding is open, so no finding id is listed and nothing needs revising. Standing rules for any later reviser, restated from the command: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id. Medium and minor findings must not be edited under this brief, including through "apply all findings".

verdict: PASS
