review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (taken with `sha256sum`; equals the spec hash recorded in lint-1.md line 1)
- baseline: none given (first review of the full document)
- prior report: none
- reviewer model used: claude-sonnet-5-5
- lint: `.dev/orca-command-refactor/review/lint-1.md` read first (sha256 `6a70e9a1255ee5d4652078e22f1d02b3383feeb5af682b9017b29610cb1b420a`). It says "Checks: REF. Findings: 0." (lint-1.md:3) and "No findings." (lint-1.md:5). There is no lint id to confirm or dismiss.
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-33`.
- citation key: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`, numbered as the file reader numbers them. Any `cmd/`, `sk/`, `CLAUDE.md`, `src/`, `.dev/codegraph-migration/`, `EVIDENCE.md` or `HOW-WE-WORK.md` line that I could reach only through the spec or an inventory is marked UNVERIFIED.

## What was covered

- Read in full: the candidate (285 lines), README.md, all three inventories, lint-1.md, the review-loop prompt file, and the command definition.
- Checked every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in the candidate (about 90 distinct ones) against the inventory files. All found the cited content. No wrong inventory line.
- Reconciled the arithmetic. INV-A 5 ready + 13 needs-change + 3 coordinator-only = 21 (INV-A:73). INV-B 5 + 14 + 3 = 22 (INV-B:278). These match SPEC:76's 10 / 27 / 6 = 43. The section 3.1 table lists 10 commands (SPEC:83-92), section 3.2 lists 27 (SPEC:99-125), section 4 lists 6 (SPEC:132-137). Phase membership adds up: P1 9, P2 15 (11 from 3.2 plus reflect, release-split, tdd, troubleshoot from 3.1), P3 4, P4 3; P1+P2(3.2 part)+P3+P4 = 9+11+4+3 = 27 (SPEC:159-162).
- Not checkable here, so UNVERIFIED: every `cmd/`, `sk/`, `src/superclaude/cli/install_core.py`, `CLAUDE.md`, `HOW-WE-WORK.md`, `Makefile`, `pyproject.toml`, `.dev/codegraph-migration/` and `EVIDENCE.md` citation that the inventories do not quote. This includes the E5 grep result (SPEC:25), the 11 re-read locations (SPEC:11) and every `CLAUDE.md:N` line.
- Experts, in the fixed order: Wiegers, Adzic, Cockburn (requirements), Fowler, Nygard, Whittaker (always active), Newman, Hohpe (architecture). Crispin, Gregory and Hightower are outside the two focus areas and were not run.
- Not triggered: Pipeline Dimensional Analysis (no multi-stage data flow with diverging counts; the 43 = 10+27+6 split reconciles above). State Variable Registry (only under `--focus correctness`).
- Modes: critique only. No `--re-review`, so the Improve step ran as a report, not as an edited specification, and the candidate was not edited.

## Grading

Each blocking finding carries the grading sentence required by the FIRST-REVIEW prompt (`document_review_loop_prompts.md:32`). Anything that needs a guess about which of two readings an implementer picks, or that is a requirement the document never states, is Medium and sits under `follow-up candidates`.

=== REQUIREMENTS ANALYSIS ===

### F-1 (CRITICAL, blocking): the report-file rule has no path for commands whose `--output` is a file or whose output location is fixed

- Experts: Wiegers (lead), Adzic, Whittaker (Sentinel Collision: one name, `--output`, carries two meanings).
- Issue: WC-4 says the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" and that the path is "known before dispatch" (SPEC:62; repeated in SPEC:73). Other stated text hands the same flag a file:
  - tdd: "`--output <file>`; the TDD at `--output`" (SPEC:90; INV-B:222).
  - init-lite: "`--output <file>`" (SPEC:87; INV-A:55).
  - spec-panel: "add `--output`" to a command that has none (SPEC:120; INV-B:182), with a review document as the deliverable.
  - cleanup-audit: "output dir is fixed" `.claude-audit/` (SPEC:85; INV-A:42) and index-repo: `PROJECT_INDEX.md` at an implied location (SPEC:86; INV-A:53) have no caller-chosen directory at all.
  - The acceptance check for the blocked path uses exactly the file-valued form: `/sc:tdd "auth" --unattended --output <file>` must end with "contract `status: blocked` with a non-empty `blocked_question`" (SPEC:200), and step 4 of the live check does `test -s <contract>` on it (SPEC:183).
- Grading sentence: an implementer who follows the stated text as written builds, for `/sc:tdd "auth" --unattended --output docs/x/TDD_FOO.md`, a contract at `docs/x/TDD_FOO.md/return-contract.yaml`, and that is wrong because that path lies under a regular file and cannot be created, so the blocked contract that SPEC:200 requires cannot exist and the coordinator has no report path. Two stated texts contradict (SPEC:62 against SPEC:87, SPEC:90).
- Recommendation: state one rule for where the contract goes when `--output` is a file or the output location is fixed (for example, the brief names the contract path explicitly, or the contract sits beside the named file under a stated filename), and list that path in the rows for tdd, init-lite, spec-panel, cleanup-audit and index-repo. Narrow rather than add: one sentence in WC-4 plus the five row cells. Corroboration, not repo evidence: the command definition given to this review resolves the same clash with a separate `--report-dir` and keeps `--output` file-valued (command.md:460-461), which suggests the spec's single-flag rule is the unfinished part.
- Priority: High. Quality-impact estimate: completeness +1.5 and testability +1.0 on the 0-10 scale.

### F-2 (MAJOR, blocking): acceptance check AC-1.1 cannot pass for `/sc:load` without reversing a stated decision

- Experts: Wiegers (testability), Cockburn.
- Issue: AC-1.1 asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (SPEC:195). `/sc:load` is a section 3.2 row (SPEC:112) whose Report cell is "none (see note)" and Resume cell is "n/a", with the note "use it as a step inside another worker's brief, not as its own Task". The Decisions table says "a report file would be an unrequested addition. Only its usage-line defect is fixed" (SPEC:265), and SA-4 lists the load usage line as its only change (SPEC:149); P1 lists "load (usage line only)" (SPEC:159). The same P1 row also says the `--unattended` flag is accepted by "every command in sections 3.1 and 3.2" (SPEC:159), which includes load.
- Grading sentence: an implementer who follows the stated text as written either adds an `## Unattended mode` section that names `return-contract.yaml` to `/sc:load`, which writes the report file SPEC:265 says must not exist, or leaves load alone and fails AC-1.1, so the check and the decision cannot both hold. A stated text that an acceptance criterion cannot pass.
- Recommendation: narrow AC-1.1 to the commands that produce a contract (3.1 plus 3.2 minus `/sc:load`), and drop `load` from the "accepted by every command" clause in SPEC:159. Two edits, no new text.
- Priority: High. Quality-impact estimate: testability +0.8, consistency +0.5.

=== ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking. The central decision (Orca on top, commands unchanged as workers) is supported by CAPS:97-101 (depth 1), CAPS:147-149 (standalone and outside-Orca behaviour), CAPS:76 and CAPS:150 (`worker_done` bound to the dispatched pane) and INV-A:90 / INV-B:285-286 (competing orchestrators). The spec states its own evidence gap openly (SPEC:42-45, UNVERIFIED items 1-13 at SPEC:272-284). The medium findings below are listed under `follow-up candidates`.

### Guard Condition Boundary Table (Nygard lead, Crispin completeness, Whittaker attack)

Guards found in the spec: WC-1 readiness fallback, WC-2 three-way gate resolution, WC-4 `<output-dir>` rule, WC-5 status-to-outcome map, WC-10 wait split, WC-8 depth limit. Input classes omitted per guard are named in the line after each group.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 status map | SPEC:63 | Zero/Empty | no report file | maps to failed | `--outcome failed` "or no report exists" | OK |
| WC-5 status map | SPEC:63 | Typical | `succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 status map | SPEC:63 | Legitimate Edge Case | `partial` | succeeded | maps to succeeded, body says partial (SPEC:263) | OK |
| WC-5 status map | SPEC:63 | Sentinel Value Match | existing command contract with its own status word (SPEC:62 "keep their fields") | unknown | not specified (see M-5) | GAP (Medium) |
| WC-4 output path | SPEC:62 | Zero/Empty | command has no output flag or fixed dir (cleanup-audit, index-repo) | unknown | not specified | GAP (blocking via F-1) |
| WC-4 output path | SPEC:62 | Legitimate Edge Case | `--output` is a file (tdd, init-lite, spec-panel) | unknown | contradicts SPEC:87, SPEC:90 | GAP (blocking via F-1) |
| WC-4 output path | SPEC:62 | Typical | `--output <dir>` on analyze | dir | `<dir>/return-contract.yaml` | OK |
| WC-4 pre-creation stop | SPEC:62, SPEC:92 | Zero/Empty | workflow stops before its package id exists | unknown | "write the contract for pre-creation STOPs too" with no stated location (see M-6) | GAP (Medium) |
| WC-10 wait split | SPEC:68 | Typical | single call 3 min | no split | heartbeat between waits | OK |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | call longer than 5 min | split | waits of at most 4 min | OK |
| WC-10 wait split | SPEC:68 | Legitimate Edge Case | call of 4 to 5 min | no split required | allowed by WC-10, but AC-4.3 fails any call over 240 s (SPEC:210) | GAP (Medium, see M-9) |
| WC-2 gate resolution | SPEC:60 | Zero/Empty | flag supplied with an empty value | unknown | not specified | GAP (Medium, minor) |
| WC-2 gate resolution | SPEC:60 | Typical | no default, no flag | blocked | contract `status: blocked` plus question | OK |
| WC-1 readiness | SPEC:59 | Typical | fallback 30 s | passes | evidence at CAPS:49 | OK |
| WC-1 readiness | SPEC:59 | Maximum/Overflow | fallback above about 45 s | fails | same evidence (CAPS:49) | OK |
| WC-1 readiness | SPEC:59 | Legitimate Edge Case | fallback 31 to 45 s | "well inside" undefined | not a number | GAP (minor) |
| WC-8 depth | SPEC:66 | Typical | depth 1 | `worker-start` refused | WC-8 forbids the call | OK |
| WC-8 depth | SPEC:66 | Legitimate Edge Case | user raises depth (D5 option b, SPEC:252) | allowed by Orca | WC-8 still forbids, D5(b) contradicts it | GAP (minor: D5(b) is a user choice, not a default) |

Omitted classes (one line each): WC-5 "One/Minimal" and "Maximum" do not apply (a status is one of a closed set); WC-4 "Maximum/Overflow" does not apply (no size bound); WC-2 "Maximum" and "Sentinel" do not apply (gate counts are per command, no magic value); WC-8 "Zero/Empty" and "Sentinel" do not apply (depth is a setting where non-numbers fall back to 1, CAPS:100). FR-8/FR-9 grading: the two GAP rows on WC-4 output path name a concrete wrong outcome (F-1) and are blocking; every other GAP row is Medium or minor and listed below.

### Whittaker adversarial analysis

- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:62 (WC-4)** fails when **`--output` names a file**. Concrete attack: coordinator briefs `/sc:tdd "auth" --unattended --output docs/x/TDD_FOO.md`. Before: no contract. WC-4 says write `<--output>/return-contract.yaml`. After: the write targets a path below a regular file and fails, so there is no report and `worker_done --report-path` has nothing to carry. This is F-1.
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:67 (WC-9) and SPEC:159-160 (P1 and P2)** fails when **P1 ships before P2**. Concrete attack: after P1, `--unattended` is accepted by every command in 3.1 and 3.2 (SPEC:159). A coordinator following the P0 brief template passes `--unattended` to `/sc:auggie-review <PR>`. State trace: P1 done, P2 not done, so the auggie-review posting default and remediation offer are still on (SPEC:100 puts their removal in P2). Result: a review is posted to GitHub and the session ends its turn on a chat offer. Graded Medium (M-1) because the spec never says a coordinator may dispatch a gate command in that window.
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:64 (WC-6) against SPEC:62 and SPEC:73** fails when **a Task is retried**. Concrete attack: the Task spec holds one fixed `--output <dir>`. `worker-start --retry-of` reuses the Task. A "fresh dir" command (22 rows, for example analyze at SPEC:99) writes attempt 2 into the same directory as attempt 1, so attempt 1's output is overwritten or mixed, which WC-6 says must not happen. Graded Medium (M-2): the spec does not say who creates the fresh directory.
- Divergence Attack on **SPEC:148 (SA-3) against SPEC:62 (WC-4)**: SA-3 says contract and report files are written "only in unattended mode or when the caller passes the new output flag"; WC-4 says "In unattended mode". A person running `/sc:analyze x --output out/` without `--unattended` either gets a contract or does not. Graded Medium (M-3).

## Synthesis

The decision, the Orca facts and the per-command table are sound and well sourced. The two blocking problems are both local: one rule in WC-4 (where the contract file goes) that two other stated texts contradict, and one acceptance check (AC-1.1) that cannot pass for `/sc:load` as the spec itself decides. Nothing in the architecture needs rework. Expert consensus: keep the design, fix WC-4's path rule and AC-1.1, leave the Medium items for the follow-up pass.

## follow-up candidates

Medium (warnings; none triggers a revision, none appears in the Reviser brief):

- M-1: P1 accepts `--unattended` on every command in 3.1 and 3.2 (SPEC:159), while gate conversion and WC-9's "outward defaults are off" land in P2 (SPEC:160, SPEC:67, SPEC:100). In between, `--unattended` on auggie-review or cleanup would not do what WC-2 and WC-9 promise. The spec never says gate commands must not be dispatched before P2, and AC-1.1 asks for an `## Unattended mode` section on every command in P1 (SPEC:195) though 2.1 says each section lists that command's gate resolutions (SPEC:52). Missing requirement.
- M-2: WC-6's "fresh output directory" (SPEC:64) cannot be met when the brief fixes one `--output` (SPEC:62, SPEC:73). AC-3.2 relies on "starts fresh" in a directory that already holds `.session-memory.md` (SPEC:205), which is the corruption WC-6 forbids. Missing requirement (who creates the fresh directory).
- M-3: SA-3 (SPEC:148) says new files appear "in unattended mode or when the caller passes the new output flag"; WC-4 says "In unattended mode" (SPEC:62). AC-1.3 only tests neither flag set (SPEC:197).
- M-4: AC-C1 (SPEC:172) fails on any `orca orchestration ...` text under `src/superclaude/core`. P0 adds an Orca section to HOW-WE-WORK.md and a new WORKER-CONTRACT.md there (SPEC:158), and SA-2 allows an Orca mention "inside the contract file" (SPEC:147). The two do not agree on what is allowed in `core`. Which wording an implementer writes decides whether AC-C1 passes. Also, the table cell escapes the pipes as `\|` (SPEC:172), which a copied `grep -E` reads as a literal bar.
- M-5: WC-4 says commands with a contract "keep their fields" (SPEC:62) while the live check asserts `status` is one of `succeeded|partial|failed|blocked` (SPEC:183) and the Decisions row picks a fixed set (SPEC:262). The existing status words of workflow, brainstorm, reflect and adversarial are not given in the inventories (INV-B:272, INV-A:97, INV-B:112, INV-A:35 name the files, not the words), so whether those contracts pass the check is UNVERIFIED.
- M-6: workflow's contract is written "for pre-creation STOPs too" (SPEC:92) but its location today is inside a package whose id does not exist yet (INV-B:272; SPEC:92), so the path is not "known before dispatch" (SPEC:62).
- M-7: roadmap "writes memory through `sc:save` at every wave" (INV-B:154), and parallel save clobbers single-owner keys (INV-B:165; SPEC:119). The roadmap row (SPEC:118) does not say roadmap uses per-session keys under `--unattended`, so WC-11 (SPEC:69) is not met for it.
- M-8: P2 rows already encode D4 option (a) (auggie-review `--post-pr` returns "only with an explicit `--post-pr` in the brief", SPEC:100; task commit and push "refused unless authorized", SPEC:121), while SPEC:154 says phases 1-3 need no user decision and D4 is still open (SPEC:244-247). Under D4(b) those rows would differ.
- M-9: WC-10 requires splitting only above 5 minutes into waits of at most 4 minutes (SPEC:68), while AC-4.3 fails any single call over 240 s (SPEC:210). A 4 to 5 minute call passes WC-10 and fails AC-4.3.
- M-10: an unrelated primitive may already call Orca. The reviewer's session skill list describes `sc:issue` as creating an Orca worktree, which would contradict E5's "no command, skill, agent or core file calls Orca today" (SPEC:25) and make AC-C1 fail on its first run. This is not a workspace file, so it is UNVERIFIED; it also suggests the "43 commands in `cmd/`" scope (SPEC:76) may not include commands the reviewer's list shows (graph, impact, issue). Check with `ls src/superclaude/commands | wc -l`.

Minor (notes):

- n-1: SPEC:79 says the only command changes for the 10 ready commands are the small fixes in the last column, while P1 adds the flag and an `## Unattended mode` section to all of them (SPEC:159, SPEC:195).
- n-2: SPEC:154 says phases 1-3 need no user decision, but D1 (the flag choice that every phase relies on) is open (SPEC:227-230). SPEC:225 says phases 0-3 may proceed on recommendations, which resolves it in practice.
- n-3: UNVERIFIED item 14 (SPEC:285) is a claim that a validator checked about 340 citations, not an unverified item. That check is not in the workspace, so it is not confirmed here.
- n-4: AC-C5 (SPEC:176) rejects any removed line, but adding `--unattended` to an existing Usage line removes the old line. It passes only if the flag is added as a new line.
- n-5: WC-2 has no stated behavior for a flag supplied with an empty value (Guard Condition Boundary Table, WC-2 row).
- n-6: the WC-1 readiness fallback has no number ("well inside", SPEC:59).
- n-7: user question on follow-ups not asked. This worker run is non-interactive, so no issue was opened for the follow-up list.

## Brief clauses overridden

None. The brief narrowed nothing and widened nothing.

## Reviser brief

Blocking finding ids: F-1, F-2.

Reviser contract (restated from the Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone.

- F-1: SPEC:62 (WC-4) against SPEC:85-87, SPEC:90, SPEC:120, SPEC:200.
- F-2: SPEC:195 (AC-1.1) against SPEC:112, SPEC:159, SPEC:265.

verdict: FAIL
