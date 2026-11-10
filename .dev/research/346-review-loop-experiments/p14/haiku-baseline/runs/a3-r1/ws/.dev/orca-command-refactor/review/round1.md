review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (review 1 of 3)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`)
- baseline: missing (first review; no `--baseline` given)
- prior report: none
- reviewer model: claude-haiku-5-5
- command: `/sc:spec-panel --mode critique --focus requirements,architecture`; prompt: FIRST-REVIEW from `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full
- Correctness focus not active, so no State Variable Registry is required
- citation key (paths relative to the workspace root): `SPEC` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `README` = `.dev/orca-command-refactor/README.md`; `INV-A` / `INV-B` = `.dev/orca-command-refactor/inventory/commands-a.md` / `commands-b.md`; `CAPS` = `.dev/orca-command-refactor/inventory/orca-capabilities.md`

## Summary

4 blocking findings (F-1 to F-4), 10 Medium findings (M-1 to M-10, follow-up candidates) and 3 minor notes (m-1 to m-3). Verdict FAIL, because F-1 to F-4 are open.

## Coverage

- Read in full: `command.md`, the review-loop prompt file, `README`, `INV-A`, `INV-B`, `CAPS` and `SPEC`.
- Every `INV-A`, `INV-B`, `CAPS`, `README` and `SPEC`-internal citation used below was checked against those files. The `CAPS` lines cited for E1, E2, E4, R1, R3, WC-1, WC-3, WC-5, WC-7, WC-8, WC-10 and WC-12 were confirmed to carry the stated text.
- Not checked: citations to `src/superclaude/...`, `CLAUDE.md`, `tests/`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...` and `/opt/Orca/...`. These are not in the workspace, so each is UNVERIFIED here. The grep result in E5 (`SPEC:25`) is also UNVERIFIED, because the grep cannot be re-run from the workspace.
- Not run: the spec's own commands. No command in `SPEC` section 7 was executed, and no Orca state was touched.

## Findings

Each finding gives the FIRST-REVIEW grading sentence ("An implementer who follows the stated text as written builds X, and X is wrong because Y").

### === REQUIREMENTS ANALYSIS ===

**F-1 [BLOCKING] The brief must carry `--unattended`, but the P0 smoke runs must not.**
- Experts: Wiegers (lead), Adzic, Crispin.
- Text: `SPEC:73` (section 2.3) says each Task's brief states "the exact command line including `--unattended`". `SPEC:158` (P0) runs three commands "as real Orca workers, invoked directly", and `SPEC:194` (AC-0.4) lists them without `--unattended`. The flag is first introduced in P1 (`SPEC:159`), and the WC-4 contract exists only in unattended mode (`SPEC:62`).
- Grading sentence: an implementer who follows `SPEC:73` for the P0 runs passes `--unattended` to commands that do not accept it yet, and an implementer who follows `SPEC:194` omits it, which breaks `SPEC:73`. The two stated texts contradict each other, and the spec does not say which applies in P0.
- Recommendation: state in `SPEC:73` that P0 briefs omit `--unattended`, or move the brief requirement to P1 onward.
- Priority: High.

**F-2 [BLOCKING] AC-0.4 step 3 cannot pass in P0.**
- Experts: Crispin (lead), Adzic.
- Text: `SPEC:194` says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1." The pass condition of step 3 (`SPEC:182`) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path." Both need the P1 contract. The exemption in `SPEC:194` names only step 4.
- Grading sentence: an implementer who runs AC-0.4 as written finds that step 3 has no contract status and no WC-4 path to check in P0, so step 3 cannot pass and the P0 gate cannot close.
- Recommendation: give step 3 a P0 variant that compares the outcome with the command's own report and checks the path of the file the command wrote.
- Priority: High.

**F-3 [BLOCKING] `/sc:load` must name a contract, but its row and its Decisions entry say it writes none.**
- Experts: Wiegers (traceability), Crispin.
- Text: AC-1.1 (`SPEC:195`) requires every command in sections 3.1-3.2 to have a `## Unattended mode` section that names `return-contract.yaml`. `load` is in section 3.2 (`SPEC:112`), with "none (see note)" in the Report column. Its Decisions row (`SPEC:265`) says "a report file would be an unrequested addition." WC-4 (`SPEC:62`) requires the contract "on every outcome".
- Grading sentence: an implementer who follows the `load` row and the Decisions row adds no contract, so AC-1.1 fails for `load`. An implementer who makes AC-1.1 pass adds the report file that `SPEC:265` forbids.
- Recommendation: exclude `load` explicitly from WC-4 and from AC-1.1, in the way section 4 is excluded, or give `load` a contract and remove the Decisions row.
- Priority: High.

**F-4 [BLOCKING] The "no change" verdict for tasklist rests on a nesting depth that the cited evidence contradicts.**
- Experts: Fowler (lead), Nygard, Hohpe.
- Text: `SPEC:122` says tasklist needs no change because "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`."
- Evidence: `INV-B:210` says Stage 10.5 "dispatches N Agent-tool subagents that each run `/sc:reflect`, which itself spawns `root-cause-analyst` + `confidence-calibrator`." So reflect's own agents sit two layers below the worker, not one: the Stage 10.5 subagent is layer 1 and its spawned agents are layer 2. `INV-B:111` says Tier 2 is merged by `sc:adversarial-protocol`, which can add a further layer; its fan-out is not traced in the workspace (UNVERIFIED). `INV-A:14` says that at the depth limit "Claude Code withholds the `Agent` tool". Also, a gate that fires inside such a subagent cannot use `ask`, because WC-7 (`SPEC:65`) forbids subagents from sending lifecycle messages. The only resolution left is "blocked", and Stage 10.5 is not shown to surface it.
- Grading sentence: an implementer who follows `SPEC:122` leaves tasklist unchanged, believing reflect runs one layer down. Its reflect agents are already at layer 2, and any spawn one level deeper than assumed reaches the depth where `INV-A:14` says the Agent tool is withheld. That fan-out is then lost without an error, and the spec has no check for it.
- Recommendation: correct `SPEC:122` to "two layers below the worker; adversarial Mode A depth UNVERIFIED". Re-decide the tasklist verdict, and add a P2 check that a tasklist run keeps its Tier 2 fan-out. Add a rule for gates that fire inside a subagent.
- Priority: High.

**M-1 [MEDIUM] P1 accepts `--unattended` on gated outward commands without saying what it does.**
- Experts: Wiegers, Whittaker.
- Text: `SPEC:159` says the flag is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". `post-release`, `pr-submit` and `task` are gated and push, commit or open PRs (`SPEC:113`, `SPEC:114`, `SPEC:121`). WC-9 (`SPEC:67`) says outward defaults are off under `--unattended`. Their gate conversion is in P4 (`SPEC:162`) and P2 (`SPEC:121`).
- Grading sentence: an implementer who follows P1 must guess what the flag does on a gated command. The no-op reading lets `post-release` still push and open PRs under `--unattended`, which breaks WC-9.
- Recommendation: state that in P1 gated commands treat `--unattended` as blocked, or reject it, until their own row lands.
- Priority: High (safety-relevant), though the grading rule makes it Medium.

**M-2 [MEDIUM] Nobody is assigned to create a fresh output directory on retry.**
- Experts: Whittaker (sequence attack), Hohpe.
- Text: WC-6 (`SPEC:64`) says a command "writes each run into a fresh output directory". WC-4 (`SPEC:62`) and the brief rule (`SPEC:73`) say the coordinator passes the output directory. The first attempt's `return-contract.yaml` sits at the same path.
- Grading sentence: an implementer who follows `SPEC:73` on a retry passes the same `--output`, and nothing in the text stops the command from overwriting the first attempt's contract and report, so the first attempt's output is lost.
- Recommendation: state that a retry gets a new `--output`, and that a command refuses to write into a non-empty output directory unless it is given its resume flag.
- Priority: Medium-high.

**M-3 [MEDIUM] WC-4 states as fact something the spec lists as unverified.**
- Experts: Wiegers (testability).
- Text: `SPEC:62` says "Orca does not check the file, so the coordinator opens it." `SPEC:274` (UNVERIFIED item 3) says "the spec assumes it does not", and `CAPS:79` marks it UNVERIFIED.
- Grading sentence: a reader who trusts WC-4 believes Orca's behaviour is established, but the spec's own UNVERIFIED list says it is not.
- Recommendation: rewrite as "the spec does not rely on Orca checking the file; the coordinator opens it."
- Priority: Low-medium.

**M-4 [MEDIUM] The evidence statement about the direct route conflicts with a cited contract.**
- Experts: Hohpe (evidence), Wiegers.
- Text: `SPEC:43` says "The only end-to-end proof is the PR #329 run ... so it proves the nested route, not the direct route." But `SPEC:23` (E3) cites `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10` as evidence, and `INV-A:13` reads that same contract as `invocation_method: "skill-direct"`, which is a direct-route run.
- Grading sentence: either the P3 run is direct evidence, in which case `SPEC:43` understates the evidence, or it is not, in which case E3 mis-cites it. The text does not say which.
- Recommendation: state which run the P3 contract belongs to, and whether it counts as a direct-route run.
- Priority: Medium.

**M-5 [MEDIUM] The cli-eval gate names "the safety flags" without listing them.**
- Experts: Adzic (examples), Wiegers.
- Text: `SPEC:104` says `run` "requires `--suite` and the safety flags in the brief, else blocked". AC-2.2 (`SPEC:200`) tests only the missing `--suite`. `INV-A:44` refers to "confirmation of the exact invocation and safety flags" without naming them.
- Grading sentence: an implementer cannot tell which flags make the gate pass, so the gate is either always blocked or never blocked.
- Recommendation: list the safety flags in `SPEC:104`, and add a test for a missing safety flag.
- Priority: Medium.

**M-6 [MEDIUM] A `partial` result can unblock dependent Tasks before anyone reads it.**
- Experts: Fowler, Nygard.
- Text: `SPEC:63` and `SPEC:263` map `partial` to `succeeded`. `CAPS:77` says a valid `worker_done` "settles the Task ... automatically", and `CAPS:84-86` shows dependents become startable from `task-list --ready`. `SPEC:73` says the coordinator opens the report "then releases or reuses the worker", but says nothing about reading it before a dependent starts.
- Grading sentence: an implementer who follows `SPEC:73` can start the dependents of a `partial` Task straight from the ready view, and those dependents then run on an incomplete deliverable. The text does not forbid this, so the reader must guess that the report is read first.
- Recommendation: add to `SPEC:73` that the coordinator reads the report and checks `status` before it starts any dependent Task.
- Priority: Medium.

**M-7 [MEDIUM] The AC-C1 and AC-C5 commands are written with `\|`, so the SA-2 check passes whatever the code says.**
- Experts: Whittaker (sentinel collision), Crispin.
- Text: `SPEC:172` (AC-C1) and `SPEC:176` (AC-C5) use `\|`. Inside the single-quoted `grep -E` pattern, `\|` is a literal `|`, so `(orchestration\|worktree\|terminal\|agent)` matches the literal text and nothing else. Outside the quotes, `\|` is passed to the shell as a literal `|`, which `grep` then reads as a file name. The result is that AC-C1 prints nothing regardless of the code.
- Grading sentence: an implementer who runs AC-C1 from the file as written gets an empty result and reports SA-2 and WC-8 as passing, though neither has been checked.
- Recommendation: write both commands unescaped in fenced code blocks. Rendered GFM turns `\|` into `|`, so the rendered view looks correct and the raw file does not.
- Priority: Medium.

**M-8 [MEDIUM] Existing contracts whose status is outside the four-value set have no rule.**
- Experts: Wiegers, Whittaker.
- Text: WC-4 (`SPEC:62`) says "commands that already write a contract keep their fields and add the missing ones." The status set is fixed at `succeeded / partial / failed / blocked` (`SPEC:262`), and WC-5 (`SPEC:63`) maps only those four values. The spec does not say which status values the existing contracts use (UNVERIFIED).
- Grading sentence: a command whose existing contract writes `status: done` produces a value that WC-5 does not map, so `--outcome` is undefined for that worker.
- Recommendation: state that an unmapped status makes the outcome `failed`, and that the command must write one of the four values.
- Priority: Medium.

**M-9 [MEDIUM] Most gates name no flag, although WC-3 and WC-2(b) depend on one.**
- Experts: Wiegers, Adzic.
- Text: WC-3 (`SPEC:61`) says the worker may "re-invoke or resume the command with the answer as a flag". WC-2(b) (`SPEC:60`) resolves a gate by "a value the caller supplied as a flag". Most section 3 rows name no flag for their gate, for example `cleanup` and `improve` per-item approvals (`SPEC:103`, `SPEC:110`) and `tasklist` (`SPEC:122`).
- Grading sentence: an implementer who follows WC-3 has no flag name to pass for these gates, so the answer cannot be given and the gate resolves as blocked or is silently skipped.
- Recommendation: for each gate, name the flag, or state that it has none and resolves as blocked.
- Priority: Medium.

### === ARCHITECTURE ANALYSIS ===

Architecture points raised above and not repeated here: F-4 (nesting depth), M-1 (P1 flag scope), M-6 (`partial` and dependents), and M-2 (retry directories). Two further observations:
- The decision to keep commands free of Orca calls (`SPEC:16`, `SPEC:66`) is coherent with the depth-1 finding (`CAPS:97-101`). I found no contradiction there.
- The phase order (`SPEC:153-162`) is consistent with the section 3 phase column. I checked each command's phase against sections 3.1, 3.2 and 6, and they agree.

### Minor notes

- **m-1** (`SPEC:68`): WC-10 splits waits "longer than 5 minutes", but the heartbeat cadence is "every 5 minutes". An exact 300-second wait may go a full cadence without a heartbeat.
- **m-2** (`SPEC:78-79`): the section 3.1 heading says "ready today", but the same rows need P1 or P2 fixes (for example `SPEC:83`, `SPEC:91`). The heading should say "ready with the listed small fixes".
- **m-3**: most of the spec's `src/`, `CLAUDE.md` and `.dev/evals` citations (for example `SPEC:23`, `SPEC:52`, `SPEC:59`) are outside the workspace and remain UNVERIFIED in this review.

## Guard Condition Boundary Table (mandatory artifact)

Triggered: the spec contains conditional logic (WC-4, WC-5, WC-10, the `--unattended` switch and the gate rules). Completion: each guard below has its input classes listed. Classes with no meaningful value for a guard are left out with a one-line reason. The table does not tabulate every per-command gate row in section 3; those rows are covered by M-5, M-9 and F-3.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 status-to-outcome | SPEC:63 | Zero/Empty: no report file exists | none | failed | "`--outcome failed` ... or no report exists" | OK |
| WC-5 status-to-outcome | SPEC:63 | One/Minimal: `status: partial` | `partial` | succeeded | "`succeeded` ... including `partial`" (SPEC:263) | GAP (M-6: dependents may start before the report is read) |
| WC-5 status-to-outcome | SPEC:63 | Typical: `status: succeeded` | `succeeded` | succeeded | stated | OK |
| WC-5 status-to-outcome | SPEC:63 | Maximum/Overflow: audit with `verdict: FAIL` and `status: succeeded` | `verdict: FAIL` | succeeded | "including an audit whose verdict is FAIL" | OK |
| WC-5 status-to-outcome | SPEC:63 | Sentinel Value Match: a status outside the four values | `done` | undefined | not specified | GAP (M-8) |
| WC-5 status-to-outcome | SPEC:63 | Legitimate Edge: `status: blocked` with a body that says succeeded | `blocked` | failed | "`failed` when the report says `failed` or `blocked`" | OK |
| WC-10 wait split | SPEC:68 | Typical: 180-second tool wait | 180 s | not split | stated | OK |
| WC-10 wait split | SPEC:68 | Legitimate Edge: wait of exactly 300 s | 300 s | not split | "longer than 5 minutes" | GAP (m-1) |
| WC-10 wait split | SPEC:68, SPEC:104 | Maximum: cli-eval eval of 3600 s | 3600 s | split into waits of at most 240 s | `SPEC:104` | OK |
| WC-10 wait split | SPEC:68 | Zero/Empty: no wait | left out: a zero-length wait is not a wait | n/a | n/a | n/a |
| `--unattended` switch | SPEC:51, SPEC:146 | flag absent (standalone) | none | standard behaviour | SA-1 | OK |
| `--unattended` switch | SPEC:159 | flag present on a command with no gate | none | no-op | `SPEC:159` | OK |
| `--unattended` switch | SPEC:73, SPEC:158 | flag present during P0, before it exists | none | undefined | `SPEC:73` requires it; `SPEC:194` omits it | GAP (F-1) |
| `--unattended` switch | SPEC:159, SPEC:67 | flag present on a gated outward command before P2 or P4 | none | undefined (no-op or off) | `SPEC:67` says off | GAP (M-1) |
| WC-4 contract | SPEC:62 | retry with the same output directory | same path | undefined | WC-6 requires a fresh directory (`SPEC:64`) | GAP (M-2) |
| WC-4 contract | SPEC:62, SPEC:112 | command with no report file (`load`) | none written | none written | `SPEC:62` "every outcome"; AC-1.1 `SPEC:195` | GAP (F-3) |
| WC-4 contract | SPEC:92 | pre-creation STOP (`workflow`) | contract written | contract written | `SPEC:92` | OK |

Guards with a GAP status that names a concrete wrong outcome are blocking (F-1, F-3). The other GAP rows are the Medium findings and minor notes listed above.

## Pipeline Dimensional Analysis

Not triggered. The spec's data flow is a coordinator, then one worker per Task, then one report per Task. It has no multi-stage transformation whose output count may differ from its input count. The fan-out that exists is the coordinator's Task DAG (`CAPS:84-92`), which the spec does not count.

## Follow-up candidates (Medium and minor, not blocking)

- M-1 P1 flag scope for gated outward commands (`SPEC:159`, `SPEC:67`)
- M-2 retry output directory (`SPEC:64`, `SPEC:73`)
- M-3 WC-4 presents an unverified fact as settled (`SPEC:62`, `SPEC:274`)
- M-4 P3 run classed as nested-only but cited as direct (`SPEC:43`, `SPEC:23`, `INV-A:13`)
- M-5 cli-eval safety flags undefined (`SPEC:104`, `SPEC:200`)
- M-6 `partial` and dependent Tasks (`SPEC:63`, `SPEC:263`, `SPEC:73`, `CAPS:77`, `CAPS:84-86`)
- M-7 `\|` in AC-C1 and AC-C5 (`SPEC:172`, `SPEC:176`)
- M-8 unmapped status values (`SPEC:62`, `SPEC:262`)
- M-9 gates with no flag name (`SPEC:61`, `SPEC:60`, `SPEC:103`, `SPEC:110`, `SPEC:122`)
- m-1 300-second wait boundary (`SPEC:68`)
- m-2 "ready today" heading (`SPEC:78-79`)
- m-3 citations outside the workspace remain UNVERIFIED

## Reviser brief

Blocking finding ids: F-1, F-2, F-3, F-4.

Restated rule (review-loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revised under this brief.

verdict: FAIL
