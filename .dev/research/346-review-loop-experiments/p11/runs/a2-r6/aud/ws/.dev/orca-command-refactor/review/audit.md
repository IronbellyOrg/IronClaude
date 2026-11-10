review: 1 of 3

# Spec-panel audit: Orca worker-contract spec (whole-document audit, first review)

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines) |
| Candidate SHA-256 | `5214f80e3dc9557f5cf50e915b26edd24f7757a9ce7975ec766b78482cde7fd6` |
| Re-review / baseline | not given: first review of the full document (`review: 1 of 3`); no baseline hash applies |
| Reviewer model actually used | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full before reviewing) |
| Precedence | No brief clause was overridden. The brief did not widen scope, did not regrade any minor finding, and did not ask to apply findings. |
| Inputs | All readable. `--unattended` was not passed, so person-mode questions and the follow-up question below are recorded, not asked. |

Citation convention: `S:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `CMD:N` = line N of the sandbox `command.md`. Any citation into a file that is not in the sandbox (`src/`, `CLAUDE.md`, `EVIDENCE.md`, installed Orca files, the codegraph run files) is UNVERIFIED here and is only repeated second-hand through an inventory line.

Summary: no blocking finding. 15 Medium findings and 8 minor notes are listed under follow-up candidates. The decision (Orca coordinates, commands stay the units of work) is supported by the inventories. The Mediums are mostly requirements the document never states, plus verification commands that can false-pass.

## What was covered

- The whole candidate was read (S:1-286), plus `README.md`, both inventories and `orca-capabilities.md` in full, `command.md` in full and the loop-prompts file in full.
- About 45 candidate citations that point into the three inventories were checked against the cited inventory lines. All matched, including the count claim (21 + 22 = 43 commands; 10 / 27 / 6 split; per-phase rows). Spot checks: S:21 to CAPS:92 and CAPS:86; S:33 to CAPS:97-103; S:34 to CAPS:147-149; S:35 to CAPS:76 and CAPS:150; S:37 to INV-A:90 and INV-B:285-286; S:44 to CAPS:52 and CAPS:129; S:59 to CAPS:44-45 and the `EVIDENCE.md:39,45,56` quotes at CAPS:49; S:68 to CAPS:130 and INV-B:95; S:83-92 to INV-A:35-55 and INV-B:36-52; S:99-125 to the matching inventory rows.
- Two shell checks were run on patterns the candidate prescribes (see AUD-09). No file was written other than this report.
- Not checkable in the sandbox, so UNVERIFIED: every direct `src/`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `EVIDENCE.md` and codegraph citation (S:11, S:22-23, S:25, S:52, S:62 second half, S:147, S:150, S:183, S:279), the "about 340 citations re-read" claim (S:285), and whether the 43 commands are all the commands that exist.

=== REQUIREMENTS ANALYSIS ===

Panel: Wiegers (lead), Adzic, Cockburn.

### AUD-01 (label MAJOR, graded Medium) Where the contract file goes is undefined for many commands
- Expert: Wiegers, Adzic.
- Issue: WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)" (S:62), and 2.3 says the path is "known before dispatch" (S:73). But:
  - `tdd` and `init-lite` take `--output <file>` (S:87, S:90), so there is no directory.
  - `cleanup-audit` has a fixed output directory and `index-repo` a fixed repo-root file, with no output flag added (S:85, S:86; INV-A:42, INV-A:53).
  - `workflow` writes to `.dev/tasks/to-do/<id>/`, where `<id>` is generated at run time and the brief passes no output flag (S:92; INV-B:272).
  - `adversarial` is to write `<output>/adversarial/return-contract.yaml` (S:83), a different shape from WC-4.
  - AC-1.2 requires `--unattended --output <dir>` for "each P1 command", and the P1 commands include cleanup-audit, index-repo and workflow (S:196, S:159), which have no such flag.
  - The sandbox command definition shows the same problem was met and solved differently: `--output` is file-valued, so a separate `--report-dir` is required (CMD:23, CMD:460).
- Grading check: "An implementer who follows the stated text builds a contract path rule that has no `<output-dir>` for these commands and an AC-1.2 run that passes a flag these commands do not have." This needs the implementer to choose one of several workable readings (add a flag, use the parent directory, add a `--report-dir`), none of which loses data, so it is Medium.
- Recommendation: in WC-4 define the contract location per command class (directory flag, file flag, fixed or generated path) and state in each 3.1 row where its contract goes. Rationale: the coordinator can only read a file whose path it knows before dispatch (S:73).
- Priority: High. Quality impact: Completeness and Testability.

### AUD-02 (label MAJOR, graded Medium) The `--unattended` flag is delivered before its meaning, and which commands are dispatchable per phase is never stated
- Expert: Wiegers, Cockburn.
- Issue: P1 adds the flag to "every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (S:159) and AC-1.1 requires a `## Unattended mode` section in all of them (S:195). The gates only convert in P2 to P4 (S:160-162). 2.3 tells the coordinator to put `--unattended` in every brief (S:73). 3.1 says the ten ready commands run "now" (S:79), and AC-0.4 runs them without the flag (S:194), so before P1 the flag the brief must carry does not exist. After P1, `/sc:auggie-review --unattended` is accepted but still posts to GitHub and offers remediation (S:100), `/sc:implement --unattended` still halts for a Ruling (S:109), and `/sc:pr-submit` gets a section and flag even though D3(a) says it stays with the coordinator (S:114, S:240, S:139). WC-2 and WC-9 say the opposite for any command that accepts the flag (S:60, S:67).
- Grading check: "An implementer who follows the stated text ships P1 with `--unattended` accepted on auggie-review and a coordinator then passes it as 2.3 says, and X (a GitHub post or a stall) is wrong because WC-9 says that default is off under the flag." It needs the assumption that a coordinator dispatches a P2 command before P2 lands, and the document does not forbid it, but also does not allow it. Medium, not blocking.
- Recommendation: add one sentence to section 6 or 2.3: a command is dispatchable under `--unattended` only after its own phase passes its checks; before that the flag is refused, not accepted as a no-op. Also say that a D3(a) outcome removes pr-submit from AC-1.1. Rationale: removes the false-assurance interval at no cost.
- Priority: High. Quality impact: Consistency and Safety.

### AUD-03 (label MAJOR, graded Medium) Phases 1-3 are said to need no user decision, but D1 fixes the mechanism they build
- Expert: Wiegers.
- Issue: S:154 says "Phases 1-3 need no user decision". S:225 says "Phases 0-3 can proceed on the recommendations". D1 (flag versus detecting Orca) decides what P1 implements in about 37 command files (S:227-230), and D5 bounds R1 (S:249-253). The two sentences disagree on whether D1 is open, and the document never says what happens if the user later picks D1(b).
- Grading check: needs a guess about the user's later answer, so Medium.
- Recommendation: state that D1(a) is assumed for P1 and that a different answer reopens P1. Priority: Medium. Quality impact: Consistency.

### AUD-04 (label MAJOR, graded Medium) Several requirements have no acceptance check, and one check contradicts a permission
- Expert: Adzic, Crispin.
- Issue: WC-6 (resume or safe re-run, S:64), WC-12 (`check` before `worker_done`, S:70), WC-3's resume-by-message-ID (S:61) and WC-1 (S:59, covered only indirectly by step 1 of S:180) have no check in section 7. AC-2.2 requires a blocked gate to end `worker_done --outcome failed` (S:200), but WC-3 lets the worker ask the coordinator instead and carry on (S:61); a WC-3-compliant worker then ends `succeeded` and fails AC-2.2 unless the brief forbids `ask`, which 2.3 does not say (S:73).
- Grading check: AC-2.2 can pass because WC-3 says "may"; the finding is a missing requirement, so Medium.
- Recommendation: add one retry check for WC-6 (kill a worker mid-run, `--retry-of`, compare the first attempt's files by hash), a transcript check for WC-12, and say in 2.3 whether the gate-trigger runs forbid `ask`. Priority: Medium. Quality impact: Testability.

### AUD-05 (label MAJOR, graded Medium) The contract schema cannot both keep existing fields and fix the status values, and carries no version
- Expert: Wiegers, Fowler.
- Issue: WC-4 says commands that already write a contract "keep their fields" (S:62), while `status` must be one of four values (S:62-63, S:262). The existing workflow contract has a `status` field and is "contract 1.1" (INV-B:272), but its values are not in any file in the sandbox, so whether they match is UNVERIFIED. The new shared contract has no `contract_version` field, although a versioned one already exists. A later field change would break coordinators silently.
- Grading check: depends on values the document does not give, so Medium.
- Recommendation: require `contract_version`, and say which wins when an existing `status` vocabulary differs (map it, or add a second field). Priority: Medium. Quality impact: Consistency, evolvability.

### AUD-06 (label MAJOR, graded Medium) `--unattended` combined with other inputs is not fully specified
- Expert: Whittaker (FR-2.1 Zero/Empty, FR-2.2 Divergence), Wiegers.
- Issue:
  - No output directory given with `--unattended`: the document says nothing (S:62), while the sandbox command definition refuses before any work (CMD:460).
  - `--unattended` together with `--interactive` is refused for the 3.2 commands that have one (S:103, S:110) but only "never in the brief" for adversarial, brainstorm and release-split (S:83, S:84, S:89), so the command's own behavior with both flags is open.
  - `tasklist` Stage 10.5 passes `--unattended` to reflect (S:122), but the inventory records that `needs_human_decision` items HALT (INV-B:209) and the row does not say how that resolves, which WC-2 requires (S:60).
  - `brainstorm` can hand off to tasklist or task-builder in Wave 4 (INV-A:39); the brainstorm row constrains `--interactive` only (S:84).
  - A topic that contains the text `--unattended` inside quotes: no token rule is given (the command definition has one, CMD:459).
- Grading check: each needs a reading choice or is a requirement never stated. Medium.
- Recommendation: add one sentence per case, or one general rule in WC-2: conflicting person-mode flags are refused, a missing output directory is refused, and nested hand-offs inherit the flag. Priority: Medium. Quality impact: Completeness.

### AUD-07 (label MAJOR, graded Medium) A stale contract from an earlier attempt can be read as the current result
- Expert: Whittaker (FR-2.4 Sequence).
- Issue: WC-6 lets a resume-flag command reuse its directory (S:64). WC-4 writes the contract "on every outcome" (S:62) but nothing says the command removes or overwrites the old file at the start. WC-5 sends `failed` "or no report exists" (S:63). If attempt 2 is killed (context exhausted, stopped by Orca) before it writes, the old `status: succeeded` or `blocked` file is still there and "no report exists" cannot be true. The coordinator opens that file (S:73).
- Grading check: needs a kill-before-write sequence that the document does not exclude; Medium.
- Recommendation: require the command to write `status: running` (or delete the file) as its first step in unattended mode. Priority: Medium. Quality impact: Reliability.

### AUD-08 (label MAJOR, graded Medium) The outward-action default list is incomplete and "paid external run" is undefined
- Expert: Nygard, Wiegers.
- Issue: WC-9 turns off pushes, PRs, posts, installs, provisioning and "paid external run" (S:67). The inventories record other external or tree-leaving actions that the rows do not address: web search through paid APIs in research, review-translation and recommend `--plugin` (INV-B:134, INV-B:144, INV-B:104; S:115-117 mention no switch), and `reflect` writing a tracked memory file and, by default in UC-2, moving a work-unit folder (INV-B:114), where S:88 only suggests `--no-promote` "when the coordinator owns folder moves".
- Grading check: requirement never stated; Medium.
- Recommendation: define the term (name the commands or tools it covers) and add the reflect tracked-file write and default folder move to the 3.1 reflect row. Priority: Medium. Quality impact: Safety, completeness.

### AUD-09 (label MAJOR, graded Medium) Three section-7 verification commands can pass while the rule they check is broken
- Expert: Crispin, Adzic.
- Issue (checked in the sandbox, no file written):
  - AC-C5 (S:176) uses `grep -E '^-[^-]'` to prove edits are additive (SA-4, S:149). A deleted markdown bullet is the diff line `-- text`, and a deleted `---` line is `----`; both start `--` and are not matched. Test: `printf '%s\n' '-- bullet removed' '-plain removed' '-| table row removed' '----' | grep -E '^-[^-]'` printed only `-plain removed` and `-| table row removed`; the bullet and `----` lines were missed. Command files are mostly bullets, so a deleted standalone-behavior bullet passes the gate.
  - AC-C1 (S:172) is written in the file with `\|` inside the `-E` alternation (the raw markdown escape). Pasted as written, `printf 'orca orchestration ask\n' | grep -nE '\borca(-ide)?[[:space:]]+(orchestration\|worktree)\b'` printed nothing (exit 1), while the unescaped form matched. A pasted check passes vacuously.
  - AC-C1 scans `src/superclaude/core` and excludes only ccsession-tag, yet SA-2 allows a mention of the question channel "inside the contract file" (S:147), which lives in `core/` (S:52). A literal `orca orchestration ask` there fails AC-C1.
  - Step 5 of the live check searches the transcript for the string `AskUserQuestion` (S:184). Skill text that quotes it (for example "never AskUserQuestion" in the troubleshoot protocol, INV-B:239) would appear in the transcript and trip the check; the pass condition says "no call", the search says "string".
- Grading check: these are check defects, not a stated rule that does harm by itself, and SA-1 has other checks (AC-1.3, AC-2.5, AC-C3). Medium.
- Recommendation: use `grep -E '^-' | grep -vE '^---'` for deletions in AC-C5 (and flag every deleted line), give the regex without table escapes (in a code block), add the contract file to AC-C1's exclusion, and search the transcript for tool-call records, not the word. Priority: High. Quality impact: Testability.

### AUD-10 (label MAJOR, graded Medium) How a worker actually invokes a command is not specified
- Expert: Cockburn, Adzic.
- Issue: WC-7 and AC-0.4 say the worker runs the command "directly" (S:65, S:194), but Orca delivers the task as the Claude launch prompt (CAPS:47), after a preamble, so the first text is not `/sc:...`. Whether the model uses the Skill tool, reads the command file or types the slash command, and how the brief's flags reach it, is open. This is the gap §1.4(1) admits (S:43) and P0 is meant to close, but the contract text (section 2) and the coordinator brief (S:73) do not carry an invocation rule, so P0 can pass and still leave it unwritten.
- Grading check: requirement never stated; Medium.
- Recommendation: make "the invocation form the P0 smoke runs prove" a P0 output that is written into the brief template. Priority: High. Quality impact: Completeness.

### AUD-11 (label MAJOR, graded Medium) Two evidence claims are stronger than their sources
- Expert: Wiegers, Adzic.
- Issue: (1) §1.4(2) states that a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`" (S:44). CAPS:47 shows Claude receives the task as its launch prompt, so the command starts running while the agent is still starting; whether the "fresh composer" is reached first is not shown anywhere in the inventories. It is an inference and should be marked UNVERIFIED. The design is not harmed, because WC-2 covers both cases (S:44, S:60). (2) E2 says the worker "answered" (S:22); the quoted `EVIDENCE.md:45` text at CAPS:49 only shows `state: ready, stage: input_accepted`.
- Grading check: needs no wrong outcome; the safe design stands either way. Medium (claim strength).
- Recommendation: mark both UNVERIFIED and list the first in the UNVERIFIED items (S:271-285); P0 tests it. Priority: Medium. Quality impact: Accuracy.

### AUD-12 (label MAJOR, graded Medium) The spec-panel row conflicts with the command definition in this sandbox
- Expert: Wiegers.
- Issue: the row says to add `--output`, require `target_release` as a flag, keep the improved-spec step off unless asked, and add a contract (S:120; INV-B:43, INV-B:182). The sandbox `command.md` already has `--output <file>`, `--target-release`, `--report-dir`, `--unattended`, `--improve` and an `## Unattended mode` section (CMD:22-23, CMD:455-465), and that section cites "WC-4" for a different rule (paths git ignores are left out, CMD:461) than S:62. Either the inventory is older than the command, or the numbering differs from the shared contract it points at (`~/.claude/WORKER-CONTRACT.md`, not present in the sandbox home, so UNVERIFIED). Following the row literally would add a second `--output` or turn the file-valued one into a directory, which breaks SA-1 (S:146).
- Grading check: a stale-evidence mismatch whose wrong outcome depends on which file is current; Medium.
- Recommendation: re-read the live command and reconcile the row and the WC numbering with the shared contract before P2. Priority: High. Quality impact: Consistency.

=== ARCHITECTURE ANALYSIS ===

Panel: Fowler (lead), Newman, Hohpe, Nygard, Whittaker.

### AUD-13 (label MAJOR, graded Medium) WC-11 says no two workers write one file, but rows accept fixed shared paths
- Expert: Fowler, Nygard.
- Issue: WC-11 (S:69) is a "must never" owned by the command. The rows then accept fixed paths: `index-repo` writes `PROJECT_INDEX.md` at a repo-root location with no output flag (S:86; INV-A:53), `cleanup-audit` uses a fixed `.claude-audit/` and resolves it with "one audit per worktree at a time" (S:85), `init-lite` defaults to a fixed file (S:87). The second is a coordinator rule that appears only in one row; 2.3 does not list it (S:73). WC-6's "fresh output directory" also cannot be met for a command with a fixed directory (S:64).
- Grading check: needs a reading choice; Medium.
- Recommendation: add to 2.3 a rule that Tasks naming a fixed path must not run in parallel in one worktree, or add an output flag. Priority: Medium. Quality impact: Reliability.

### AUD-14 (label MAJOR, graded Medium) The decision to let a brief authorize outward actions sits uneasily with the rule used to keep implement's Ruling
- Expert: Fowler, Nygard.
- Issue: D2(a) keeps "another agent's message is not acceptance" because "the rule exists to stop an agent approving its own work" (S:233-236). D4(a) lets the coordinator's brief, quoting the user, authorize pushes, PRs and installs in a worker (S:245-247), citing a post-release rule that says "the user pre-authorized them this session" (S:247; INV-B:79). The two reasonings differ and the document does not say why a quoted instruction is enough for a push but not for a Ruling. Both are open for the user (S:224), so nothing is implemented wrongly yet.
- Grading check: pending user decision, no stated text does harm; Medium.
- Recommendation: add one sentence to D4 stating why quoting the user's instruction differs from relaying a Ruling, or align the two. Priority: Medium. Quality impact: Consistency, safety.

### AUD-15 (label MAJOR, graded Medium) The wait-length rule leaves a gap and the check is stricter than the rule
- Expert: Nygard, Whittaker (FR-2.5 Accumulation).
- Issue: WC-10 splits a wait only when it is "longer than 5 minutes" into waits of "at most 4 minutes" (S:68). A single wait of 4.5 minutes is neither required to be split nor within 4 minutes. AC-4.3 demands "no single tool call exceeds 240 s" (S:210), so a 280 s wait that WC-10 allows fails the check. pr-submit's `--poll-interval` is described as a minimum sleep with no maximum (S:68; INV-B:95), so a larger value breaks the 4-minute rule.
- Grading check: only pr-submit is affected and only under D3(b); Medium.
- Recommendation: say "no single blocking tool call longer than 4 minutes" and cap `--poll-interval` in unattended mode. Priority: Low. Quality impact: Consistency.

Architecture notes without a separate id: the design keeps one coordinator and no second orchestrator (S:37, S:128-137), the shared rules live in one installed file (S:52, S:264), standalone behavior is a hard requirement (S:141-151), and Orca state stays out of the commands (S:147). Fowler and Newman find the boundaries clean. Hohpe's message-exchange check: `worker_done` once per Task (S:63), the report is a claim-check the coordinator opens (S:62, S:73), questions resume by message ID (S:61); the missing piece is AUD-07. Nygard's failure-mode check: stall visibility is handled by `agentWait` (S:181); a coordinator policy for a worker that never sends `worker_done` is not stated (note N-06).

## Expert pass (fixed order)

1. Wiegers: requirements are numbered and owner-tagged (S:57-70); gaps are AUD-01, AUD-03, AUD-05, AUD-06, AUD-08, AUD-11, AUD-12.
2. Adzic: examples exist for D1 (S:228) and the live check (S:179-186); missing examples for AUD-01 and AUD-06; check defects in AUD-09.
3. Cockburn: primary actor is the coordinator; the worker's invocation step is missing (AUD-10); the person's actor goals are protected by SA-1..SA-6 (S:146-151).
4. Fowler: boundaries and the single contract file are sound; shared-path conflicts in AUD-13.
5. Nygard: AUD-07, AUD-13, AUD-15; also N-06.
6. Whittaker: attacks below.
7. Newman: contract versioning (AUD-05); phase-by-phase compatibility (AUD-02).
8. Hohpe: stale-message risk (AUD-07); otherwise sound.
9. Crispin: AUD-04, AUD-09; each phase has named, runnable checks (S:166-210), which is a strength.
10. Gregory: the three-amigos question is whether the coordinator author, the command owners and a tester agree on the contract location (AUD-01) and the invocation form (AUD-10).
11. Hightower: observability of a worker is through `worker-show` and the contract only; N-06.

### Whittaker attacks (FR-3 template)

- I can break this specification by **Sequence Attack**. The invariant at **S:62-64 (contract written on every outcome; retry never corrupts the first attempt)** fails when **a resume-flag command reuses its directory and the second attempt dies before writing**. Concrete attack: attempt 1 ends `status: blocked` (file F, state: blocked); the coordinator retries with `--retry-of` and the same directory; attempt 2 is stopped at once; F still says `blocked` (or `succeeded` after an earlier success), no new `worker_done` is sent, and the coordinator opening F reads the old result. (AUD-07)
- I can break this specification by **Divergence Attack**. The invariant at **S:60 (never calls AskUserQuestion under `--unattended`)** fails when **`--unattended` and `--interactive` are both passed to adversarial, brainstorm or release-split**. Concrete attack: before: brief says "never `--interactive`" (S:83); the coordinator's brief template adds both flags by mistake; after: the command honors `--interactive` (INV-A:35: it adds 4 AskUserQuestion checkpoints) and waits at a checkpoint. (AUD-06)
- I can break this specification by **Zero/Empty Attack**. The invariant at **S:62-73 (path known before dispatch)** fails when **the brief passes `--unattended` and no output directory**. Concrete attack: `/sc:analyze src/x --unattended`; the row says "add `--output`" (S:99) but no refusal is specified; the command writes its report to an undefined place and a contract nowhere. (AUD-06)
- I can break this specification by **Accumulation Attack**. The invariant at **S:154 (a phase passes only when every check passes)** fails when **the gate command cannot see the violation**. Concrete attack: a P1 edit deletes the bullet `- Will Not: ...` from a command file; the diff line is `-- Will Not: ...`; AC-C5 prints nothing; the phase passes. (AUD-09)
- I can break this specification by **Sentinel Collision Attack**. The invariant at **S:51 (`--unattended` selects the mode)** fails when **quoted topic text contains the token**. Concrete attack: `/sc:troubleshoot "login fails --unattended"`; the spec gives no token rule, so the command may switch mode. (note N-05)
- Divergence and Sequence also apply to the flag-before-meaning interval (AUD-02): `/sc:auggie-review <PR> --unattended` after P1, before P2.

## Guard Condition Boundary Table

Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack). Guards are the conditional rules the candidate states. Classes not given a row for a guard are listed after the table with their one-line reason (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 `--unattended` switch | S:51, S:60 | Zero/Empty | flag present, no output dir | true | not specified (the sandbox command refuses, CMD:460) | GAP (Medium, AUD-06) |
| G1 `--unattended` switch | S:51, S:62 | Typical | flag plus `--output <dir>` | true | gates resolve per 3.x row, contract written | OK |
| G1 `--unattended` switch | S:51, S:159 | Sentinel Value Match | topic text containing `--unattended` | unspecified | no token rule | GAP (minor, N-05) |
| G1 `--unattended` switch | S:60, S:83-84, S:89 | Legitimate Edge Case | `--unattended` with `--interactive` | true | refused for 3.2 commands (S:103, S:110); unspecified for adversarial, brainstorm, release-split | GAP (Medium, AUD-06) |
| G1 `--unattended` switch | S:159, S:160-162 | Legitimate Edge Case | flag on a command before its phase lands | true | accepted as a no-op by P1; WC-2 and WC-9 say gates and outward defaults are off | GAP (Medium, AUD-02) |
| G2 gate resolution (a)/(b)/(c) | S:60 | Zero/Empty | gate flag given as empty value | (b) false, falls to (c) | blocked, contract with the question | OK |
| G2 gate resolution | S:60 | Typical | documented default exists | (a) true | default used | OK |
| G2 gate resolution | S:122, S:84 | Legitimate Edge Case | gate reached through a hand-off or nested skill (tasklist `needs_human_decision`, brainstorm Wave 4) | unspecified | not specified | GAP (Medium, AUD-06) |
| G3 outcome mapping | S:63 | Zero/Empty | no contract file | true | `--outcome failed` | OK |
| G3 outcome mapping | S:63 | Typical | status `succeeded` or `partial` | true | `--outcome succeeded` | OK |
| G3 outcome mapping | S:62-63 | Legitimate Edge Case | old contract left by a prior attempt | "report exists" true | would read the old status | GAP (Medium, AUD-07) |
| G3 outcome mapping | S:61, S:200 | Legitimate Edge Case | gate blocked, worker uses `ask`, answer arrives | status ends `succeeded` | AC-2.2 expects `failed` | GAP (Medium, AUD-04) |
| G3 outcome mapping | S:62, S:262 | Sentinel Value Match | existing contract with another `status` value | unspecified | "keep their fields" and fixed set conflict | GAP (Medium, AUD-05) |
| G4 wait-length rule | S:68 | Typical | 3-minute wait | false | no split needed | OK |
| G4 wait-length rule | S:68, S:210 | Legitimate Edge Case | wait of 4 to 5 minutes | false | neither clause applies; AC-4.3 fails above 240 s | GAP (Medium, AUD-15) |
| G4 wait-length rule | S:68 | Maximum/Overflow | `--poll-interval` above 4 minutes | true | no cap stated | GAP (Medium, AUD-15) |
| G5 outward default off | S:67, S:100 | Typical | auggie-review PR post default | true | off; returns only with an explicit `--post-pr` | OK |
| G5 outward default off | S:67, S:115-117, S:88 | Legitimate Edge Case | paid web search, tracked-file write, default folder move | unspecified | not listed | GAP (Medium, AUD-08) |
| G5 outward default off | S:67, S:244-247 | Sentinel Value Match | explicit flag in the brief | true | allowed; whose authority counts is open decision D4 | OK (open decision) |
| G6 phase gate | S:154, S:167 | Zero/Empty | phase edits no command (P0) | true | AC-C5 vacuous, others apply | OK |
| G6 phase gate | S:174 | Legitimate Edge Case | baseline suite already failing | true | compare against saved baseline | OK |
| G6 phase gate | S:172, S:176, S:184 | Legitimate Edge Case | gate command cannot detect the violation | false | not addressed | GAP (Medium, AUD-09) |
| G7 resume or fresh run | S:64 | Typical | resume flag given and state on disk | true | resumes | OK |
| G7 resume or fresh run | S:64, S:85-86 | Zero/Empty | retry of a command with a fixed output location and no resume flag | false | a fresh directory is impossible; not specified | GAP (Medium, AUD-13) |
| G7 resume or fresh run | S:64 | Legitimate Edge Case | retry reuses the directory | true | old contract not cleared | GAP (Medium, AUD-07) |
| G8 task confidence below 0.70 | S:121 | Zero/Empty | confidence 0 | true | blocked | OK |
| G8 task confidence below 0.70 | S:121 | Legitimate Edge Case | confidence exactly 0.70 | false | proceeds (the gate is "below 0.70") | OK |
| G9 readiness limit (WC-1) | S:59 | Legitimate Edge Case | startup fallback at 45 s or more | limit missed | requirement says "well inside" without a number; the 45 s figure sits only in the evidence column | GAP (minor, N-07) |

Left out with a reason (FR-10):
- G1: One/Minimal and Maximum/Overflow: a boolean flag has no size.
- G2: One/Minimal: one gate resolves like many; Maximum/Overflow: no capacity; Sentinel: no reserved value.
- G3: One/Minimal and Maximum/Overflow: one outcome per run, no counter.
- G4: Zero/Empty: a zero-length wait needs no split; One/Minimal: below the threshold, same as Typical; Sentinel: no reserved value.
- G5: Zero/Empty: no outward action means nothing to turn off; One/Minimal and Maximum/Overflow: no counter.
- G6: One/Minimal and Maximum/Overflow: a phase either passes all checks or not.
- G7: Maximum/Overflow: the circuit breaker is Orca's (CAPS:116), not a guard in the candidate; Sentinel: none.
- G8: Maximum/Overflow: confidence is capped at 1; Sentinel: none.
- G9: Zero/Empty and One/Minimal: a launch prompt either exists or not; Maximum: the limit is Orca's.

FR-8 and FR-9: every GAP above was graded by its consequence. None names a concrete wrong outcome that an implementer following the stated text produces, or a data-loss or safety-boundary breach; all are Medium or minor and are listed under follow-up candidates. No Specified Behavior cell is blank: unspecified behavior is written as "not specified".

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

The classification funnel in section 3 and the phase plan in section 6 is the one multi-stage count flow. Counts were checked against the inventories and the candidate rows (count conservation holds).

```text
[Source: 43 commands (21 in INV-A:3 + 22 in INV-B:3)] --> [Classify]
   --> [10 ready (S:81-92)]        --> phases: P1 4 (adversarial, cleanup-audit, index-repo, workflow), P2 4 (reflect, release-split, tdd, troubleshoot), none 2 (brainstorm, init-lite)
   --> [27 need a change (S:98-125)] --> phases: P1 9, P2 11, P3 4, P4 3  (= 27)
   --> [6 coordinator-only (S:130-137)]  --> no phase
Phase totals: P1 13, P2 15 (11 + 4), P3 4, P4 3, none 2 = 37 = 10 + 27; plus 6 = 43. No mismatch.
```

Consumers: `AC-1.1` (S:195) counts "every command in 3.1-3.2 except load", which includes the 3 P4 commands in P1 (see AUD-02). No dimensional mismatch.

Advisory only: the candidate has numeric thresholds (60 s, 4 and 5 minutes, 0.70, 240 s) and several state-like files (contracts, ledgers). The panel suggests `--focus correctness` for a later review; it was not activated here, so no State Variable Registry was produced.

## Consensus and disagreements

- Consensus: the decision and the contract shape are sound and well evidenced by the inventories; the document is unusually explicit about evidence gaps (S:41-45) and open decisions (S:224-253).
- Consensus: the main weakness is under-specified edges of the contract (location, flag combinations, stale files) and verification commands that can false-pass.
- Disagreement: Fowler would put `--unattended` acceptance before P1 behind a per-command phase table (AUD-02); Wiegers would accept the current wording with one added sentence. Both agree it is not blocking.

## Follow-up candidates (Medium and minor, none blocking)

Medium (warnings; do not trigger a revision): AUD-01 contract location, AUD-02 flag before meaning and per-phase dispatchability, AUD-03 D1 gating, AUD-04 missing acceptance checks and AC-2.2 versus WC-3, AUD-05 schema versioning and status vocabulary, AUD-06 flag combinations and missing output directory, AUD-07 stale contract, AUD-08 outward-action list, AUD-09 false-passing gate commands, AUD-10 invocation form, AUD-11 evidence strength, AUD-12 spec-panel row versus the command definition, AUD-13 shared fixed paths, AUD-14 D2 versus D4 reasoning, AUD-15 wait-length rule.

Minor notes:
- N-01: S:16 says command changes are "limited to" the contract (unattended mode, report file, resume), but section 3 "Other required change" and SA-4 add defect fixes (S:149).
- N-02: S:195-196 cite "F-01", an id from an earlier review that is not defined in this document.
- N-03: E3 (S:23) cites `invocation_method: "skill-direct"` as support, while §1.4(1) says that run proves only the nested route (S:43); INV-A:13 reads the same field as a direct call. Marked UNVERIFIED (the return-contract file is not in the sandbox).
- N-04: WC-3 says the worker asks "once" (S:61), but cli-portify has three approval gates (S:105); read as once per gate.
- N-05: no rule for how `--unattended` is recognized as a standalone token (CMD:459 has one).
- N-06: no coordinator policy for a worker that never sends `worker_done` beyond "leave the wait only on positive proof" (CAPS:126); no limit on how many workers run at once in one worktree.
- N-07: WC-1 says "well inside" the readiness limit (S:59) without a number; the evidence gives 30 s passing and about 45 s failing (CAPS:49).
- N-08: tdd's "precise component prompt" (S:90) has no test the coordinator can run before dispatch; the blocked path makes it safe.

Per `/sc:spec-panel` Review Loop bullet 3, the session that ran the review asks the user once per loop whether to open an issue for these. This run has no user to ask and was told to write nothing but this report, so the question is left to the coordinator and no issue was created.

## Reviser brief

Blocking finding ids: none. No revision is requested. Reviser contract (restated from the command's Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of any reviser brief and must not be edited from this report.

verdict: PASS
