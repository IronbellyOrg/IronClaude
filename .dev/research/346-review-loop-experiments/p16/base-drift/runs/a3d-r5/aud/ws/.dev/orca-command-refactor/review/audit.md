review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `fb9100899806def3c0456f91fd02f9793207fcb28f4789f5ae6d358a15a2ce5f`
- baseline: none (first review; neither `--re-review` nor `--baseline` was given)
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`
- panel: Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, plus Whittaker (always active). Crispin, Gregory and Hightower are outside the two requested focus areas and were not used.
- citation shorthand: `spec:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` under `.dev/orca-command-refactor/`; `README:N` = `.dev/orca-command-refactor/README.md`; `cmd:N` = line N of the `/sc:spec-panel` definition.

## Coverage statement

Covered: the whole document (spec:1-285), all of sections 1-9, Decisions and UNVERIFIED.

Checked against files inside the sandbox: about 70 inventory citations (`INV-A`, `INV-B`, `CAPS`, `README`), sampled across sections 1, 2, 3, 4, 5, 8, 9 and the UNVERIFIED list. All matched what the spec says they hold. The 10 / 27 / 6 split reconciles with the two inventories (INV-A:73, INV-B:278). The phase assignment of each section 3 row reconciles with the section 6 phase table (9 P1 + 11 P2 + 4 P3 + 3 P4 = 27 in 3.2; 4 P1 fixes + 4 P2 in 3.1).

UNVERIFIED (not checkable in this sandbox, taken as stated): every `src/superclaude/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `tests/` and `~/.claude/` citation; `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`; `.dev/codegraph-migration/...`; the `orca-data.json` and `/opt/Orca` citations (only their quotations in `CAPS` were read). Section 3 rows that cite only `cmd/` or `sk/` lines are therefore checked through the inventory lines that carry the same fact, not through the source file.

The spec does not define `F-1`, `F-2`, `F-3` (see M-9), and the files `review/spec-panel.md` and `review/disposition.md` named in `README:21-26` are not in the sandbox. The audit was done on the candidate and the inventories only.

Mandatory artifacts: the Guard Condition Boundary Table is triggered (the spec has thresholds, flag guards and status guards) and is completed below before synthesis. `--focus correctness` is not active, so no State Variable Registry is produced. Pipeline Dimensional Analysis is triggered by the phased rollout (a staged pipeline whose per-stage command count differs from its input), so a Quantity Flow Diagram is produced.

## Guard Condition Boundary Table

Classes left out are named in the "Input Condition" cell as `omitted: <reason>`.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| unattended switch (`--unattended` standalone token) | spec:51, spec:229 | Zero/Empty (flag absent) | no flag | false | SA-1: behaviour as today (spec:146) | OK |
| unattended switch | spec:51, spec:62 | One/Minimal (flag present, no output directory) | `--unattended` only | true | none: WC-4 needs `<output-dir>` "the coordinator passed" and says the contract is written "including stops before any other output exists", with no directory to write to | GAP (M-2) |
| unattended switch | spec:51 | Typical | `--unattended --output <dir>` | true | WC-2, WC-4 apply | OK |
| unattended switch | spec:51 | Sentinel Value Match (token inside quoted prompt text or as another flag's value) | `"explain the --unattended flag"` | unspecified | none; the spec does not say how the token is recognised | GAP (M-13) |
| unattended switch | spec:51 | omitted: Maximum/Overflow, a boolean flag has no capacity | | | | |
| outcome mapping (WC-5) | spec:63 | Zero/Empty (no report file) | no file | `failed` | `--outcome failed` | OK |
| outcome mapping | spec:63, spec:183 | One/Minimal (report exists, `status` missing, unparseable, or outside the four values) | `status: success` | unspecified | none; step 4 asserts membership but WC-5 does not say what the worker sends | GAP (M-11) |
| outcome mapping | spec:63 | Typical (`succeeded`) | `succeeded` | `succeeded` | `--outcome succeeded` | OK |
| outcome mapping | spec:63 | Legitimate Edge Case (audit verdict FAIL, run `partial`) | `partial` | `succeeded` | succeeded, first body sentence names the status | OK |
| wait size (WC-10) | spec:68 | Typical | wait of 4 min | within | heartbeat between waits | OK |
| wait size | spec:68, spec:65 | Maximum/Overflow (one Agent-tool call that blocks the parent for more than 5 min) | 10 subagents, 12 min | exceeds | none; WC-7 keeps fan-out "as it is" while WC-10 says a single tool call over 5 min "must be split" | GAP (M-4) |
| wait size | spec:68 | omitted: Zero/Empty, a command with no wait has nothing to split | | | | |
| retry / re-run (WC-6) | spec:64 | Zero/Empty (no earlier output) | none | n/a | normal run | OK |
| retry / re-run | spec:64, spec:62, spec:73 | Typical (retry with the same brief, command has no resume flag) | same `--output <dir>` | unspecified | WC-6 says the command writes "a fresh output directory"; WC-4 and 2.3 fix the report path to the passed directory | GAP (M-1) |
| pr-submit `--monitor` | spec:114 | Typical | `--monitor 3` | allowed | runs; operator HALTs resolve as blocked | OK |
| pr-submit `--monitor` | spec:114 | Legitimate Edge Case | `--monitor 1` | refused | refused under `--unattended` | OK |
| pr-submit `--monitor` | spec:114 | One/Minimal | `--monitor 0` or `2` | allowed | not stated; INV-B:89 says only `--monitor 1` has a y/n gate, so no gate is open | OK (inferred) |
| task confidence | spec:121 | Typical | 0.50 | below 0.70 | blocked | OK |
| task confidence | spec:121 | Legitimate Edge Case | exactly 0.70 | not below | proceeds (row says "below 0.70") | OK |

## Quantity Flow Diagram

```text
[Commands in cmd/: 43] --> [split: 6 coordinator-only (section 4)] --> [37 worker candidates: 10 ready (3.1) + 27 change (3.2)]
                                                                          |
                                                                          v
                                                          [minus load (no section) = 36; minus 3 P4 commands = 33]
                                                                          |
                              AC-1.1 (spec:195): all 33 hold "## Unattended mode" at the end of P1   <-- MISMATCH
                                                                          |
                              Phase table (spec:159): P1 command column names 12 commands
                              (8 in 3.2 + 4 fixes in 3.1); the other 21 are assigned to
                              P2 (15, of which 4 are in 3.1), P3 (4), or nothing (brainstorm, init-lite)
```

The mismatch (33 required against 12 assigned) is the origin of finding B-2.

=== REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL, blocking) Phase 0 acceptance check cannot pass as written, and its failure "reopens section 1"
Experts: Wiegers, Adzic, Whittaker (Sequence Attack).

Location: spec:182 (live check step 3), spec:194 (AC-0.4), spec:158 (P0 "no command edits"), spec:79 (3.1 intro), spec:62 (WC-4).

Grading sentence: An implementer who follows AC-0.4 as written runs live-check steps 1-3 on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` before any command edit, and step 3 requires that "its `--outcome` matches the contract's `status` under WC-5" and that "its report path is the WC-4 contract path"; no WC-4 contract exists in P0 (P0 makes no command edit, and spec:79 says the worker "reports the named file until Phase 1 adds the contract"), so step 3 cannot pass, and AC-0.4 says a failure there "reopens section 1", the core decision.

I can break this specification by **Sequence Attack**. The invariant at **AC-0.4 / step 3** fails when **the check is run in the order the phases require (P0 before P1)**. Concrete attack: before P1, troubleshoot writes `REPORT.md`, workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml`, adversarial writes a contract at an unfixed path (INV-A:35). None is `<output-dir>/return-contract.yaml`. Step 3's second and third conditions evaluate false for all three runs. AC-0.4 exempts only step 4, not step 3.

Recommendation (narrowing, not adding): in AC-0.4, make step 3's report-path and status conditions read "the command's existing report file" in the same way step 4 already does.

### M-2 (Medium) `--unattended` with no output directory is undefined
Experts: Wiegers, Whittaker (Zero/Empty Attack). Location: spec:62, spec:73, many 3.2 rows "add `--output`".
WC-4 requires a contract on every outcome "including stops before any other output exists" at the directory "the coordinator passed", but nothing says what a command does when `--unattended` arrives without one. The only mention is section 2.3, which says the brief carries it. No row except `document` and `post-release` says "require an explicit output". Missing requirement, not a stated text that does harm.

### M-1 (Medium) WC-6 "fresh output directory" and WC-4 "the directory the coordinator passed" can both be built, and they differ
Experts: Wiegers, Fowler. Location: spec:64, spec:62, spec:73; about 20 rows say "fresh dir".
Reading A: the command creates a new subdirectory under the passed directory (the contract is then not at `<output-dir>/return-contract.yaml`, and the step 3 check fails). Reading B: the coordinator passes a new directory per dispatch (then the owner column "Command" for WC-6 is wrong). A `worker-start --retry-of` reuses the same Task spec (CAPS:116), so the same brief and the same directory. Needs a choice of reading, so Medium.

### M-3 (Medium) File-valued `--output` puts the contract in a source directory shared by workers
Experts: Wiegers, Whittaker (Accumulation Attack). Location: spec:62 ("parent directory of a file-valued `--output`"), spec:69 (WC-11), spec:87 (init-lite), spec:90 (tdd).
For `tdd` the default location is `docs/[domain]/TDD_[COMPONENT-NAME].md` (INV-B:222). Two TDD workers for one domain write the same `return-contract.yaml`, which WC-11 forbids, and the contract lands in a tracked docs directory. The coordinator can avoid it by choosing directories, but the spec states the rule and not the avoidance.

### M-11 (Medium, UNVERIFIED) "Keep their fields" against the fixed four-value `status`
Experts: Wiegers, Newman. Location: spec:62, spec:183, spec:262.
WC-4 says commands that already write a contract "keep their fields and add the missing ones", and live-check step 4 asserts `status` is one of four values. Whether the existing `workflow`, `brainstorm`, `reflect` and `adversarial` contracts already use those four values is not shown in the inventories (INV-B:272 names the `status` field, not its values). If they differ, the two texts conflict and step 4 fails for a correct existing contract. Not decidable from the files in the sandbox.

### M-12 (Medium) Workflow's contract location is not known before dispatch, and the pre-creation case has no location
Experts: Cockburn, Fowler. Location: spec:92, spec:62.
The workflow row keeps `.dev/tasks/to-do/<id>/return-contract.yaml` and adds "write the contract for pre-creation STOPs too". A pre-creation stop has no `<id>` directory (INV-B:272 "Not written for pre-creation STOPs"). WC-4 requires the path to be known before dispatch. How `<id>` is formed was not read (UNVERIFIED).

### M-13 (Medium) How the `--unattended` token is recognised is not stated
Experts: Whittaker (Sentinel Collision Attack). Location: spec:51, spec:229 (D1 says "testable by grep").
A prompt that quotes the word (for example a `/sc:tdd` topic about the flag) would switch the mode on, with the gates and outward defaults off. The `/sc:spec-panel` definition solves it ("standalone argument token outside any quoted argument", cmd:459); the spec does not require it.

=== ARCHITECTURE ANALYSIS ===

### B-2 (CRITICAL, blocking) Phase 1 gives every worker command the `--unattended` section before the phases that convert their gates
Experts: Fowler (lead, count annotation), Whittaker (Divergence Attack), Nygard.

Location: spec:159 (P1 scope "accepted by every command in sections 3.1 and 3.2 except the P4 commands"), spec:195 (AC-1.1), spec:100 (auggie-review row, Phase P2), spec:118 (roadmap row, P3), spec:160 (P2), INV-A:38, INV-A:78.

Grading sentence: An implementer who follows P1 and AC-1.1 as written makes `/sc:auggie-review` accept `--unattended` and write a section naming `return-contract.yaml` and the contract path, while its gate conversion (`--no-post-pr`, `--no-remediation-offer`) is a P2 row, so after P1 `/sc:auggie-review <PR> --unattended` still posts a review and inline comments to GitHub with no prompt (INV-A:38) and then waits on a remediation offer, which is the outward action and the stall that WC-2 and WC-9 say the flag removes, and AC-1.1 passes.

I can break this specification by **Divergence Attack**. The invariant at **spec:159 / spec:195** fails when **a gated command's phase (P2 or P3 in its own row) is later than the phase that adds its `--unattended` flag (P1)**. Concrete attack: P1 merged, P2 not yet. The coordinator's brief template (P0) says `--unattended` implies no person and no outward default; it runs `/sc:auggie-review 123 --unattended --output d/`; the command posts to PR 123 and ends its turn on the remediation offer; no `worker_done` arrives. The same applies to `roadmap` (the "Resume? [Y/n]" prompt stays until P3), `cli-eval`, `cli-portify`, `task`, `cleanup`, `improve` and the other 11 P2 / P3 commands in 3.2. Count: AC-1.1 requires 33 commands to hold the section after P1; the P1 command column lists 12 (see the Quantity Flow Diagram).

The spec already sees the hazard for P4 and fixes it there (spec:159 and spec:195, "F-2": those commands get the flag in P4). The same reason applies to every command whose gate row is not P1.

Recommendation (narrowing): in P1 and AC-1.1, give each command its `## Unattended mode` section and flag in the phase named in its own section 3 row, as already done for the P4 commands.

### M-4 (Medium) WC-10 and WC-7 disagree about Agent-tool calls that block the parent
Experts: Nygard, Hohpe, Whittaker (Accumulation Attack). Location: spec:68, spec:65, spec:24 (E4); INV-A:42 (7-8 concurrent agents per wave), INV-B:47 (2-10+ agents).
WC-10: a step that blocks one tool call for more than 5 minutes "must be split". WC-7: fan-out "stays as it is". A synchronous Agent-tool wave is one tool call that can block the top-level session for longer than 5 minutes, so the worker cannot send the 5-minute heartbeat. Whether Orca uses heartbeat age is UNVERIFIED (CAPS:130, CAPS:182), which is why this is Medium and the spec's checks (AC-4.3) test only pr-submit. The P0 smoke runs (troubleshoot Tier 2, adversarial) will break WC-10 by design.

### M-5 (Medium) SA-2 allows an Orca mention in the contract file; AC-C1 greps `src/superclaude/core`, where that file lives
Experts: Fowler, Wiegers. Location: spec:147, spec:172, spec:52, spec:158 (P0 adds an Orca section to `HOW-WE-WORK.md`, also in `core/`).
SA-2 permits "an example of a caller's question channel inside the contract file"; AC-C1 prints any `orca orchestration|worktree|terminal|agent` match under `core/` and requires nothing. An example written as `orca orchestration ask` fails the gate the spec makes mandatory for every phase. Passable if the author avoids that wording, but the two texts do not say so.

### M-6 (Medium) cli-portify: a coordinator-passed `--resume` counts as the approval of a human gate; the spec treats the same class of gate differently in D2
Experts: Cockburn, Fowler, Nygard. Location: spec:105 (F-3), spec:160 (P2 "touch no safety rule"), spec:236 (D2 rationale "the rule exists to stop an agent approving its own work"); INV-A:45 ("Present final spec to user for approval before delivering").
D2 keeps the implement Ruling rule so an agent cannot approve. For cli-portify the spec decides that the resume flag is approval, with no decision item, and states P2 touches no safety rule. The output stays under the chosen output directory, so no outward action; the finding is the inconsistency and the missing decision. Same issue for `task` (spec:121 keeps the confidence rule blocked; that row is consistent).

### M-14 (Medium) WC-3 lets any blocked worker `ask` and re-invoke with the answer, including implement's Ruling
Experts: Nygard, Cockburn. Location: spec:61, spec:109, spec:234-236; `INV-A:66` (a coordinator reply is not a Ruling).
Under D2(a) the answer must not count. WC-3 does not exclude implement, so a worker may `ask`, receive the person's words relayed by the coordinator, re-invoke, and be refused again with `E-NO-RULING`. A loop, not a wrong state; resolve by one sentence excluding Ruling-type gates from WC-3.

### M-7 (Medium) pr-submit's own "Will Not: run headless" is not addressed
Experts: Newman, Cockburn. Location: spec:114, spec:241, spec:162; INV-B:90 (`cmd/pr-submit.md:85`, `SKILL.md:225`).
If D3(b) is chosen, the `## Unattended mode` section sits beside a stated Will Not that says the command does not run headless. AC-C5 (additive edits) would flag the removal. Only matters if D3(b) is chosen.

### M-10 (Medium) No rule says `--unattended` reaches the commands a command invokes
Experts: Hohpe, Fowler. Location: spec:122 (only tasklist passes it to reflect); INV-A:44 (cli-eval create runs `/sc:spec-panel` and adversarial), INV-B:47 (tdd runs `/task`), INV-B:33.
Each nested invocation with a gate needs its own row; there is no general sentence. Nested gates that exist today: spec-panel TDD `target_release` (INV-B:179) and `/task` "ask the user" (INV-B:219).

### M-8 (Medium) AC-2.4 counts only the first page of `gh api`
Experts: Whittaker (Accumulation Attack). Location: spec:202.
`gh api repos/.../pulls/<PR>/reviews --jq length` and `.../comments --jq length` return at most one page (30 by default). On a PR with 30 or more review comments both counts are 30 before and after, so a post that happened is not seen. Add `--paginate`.

### M-9 (Medium) `F-1`, `F-2`, `F-3` are used as authority and never defined
Experts: Wiegers. Location: spec:62, spec:105, spec:159, spec:195.
The ids refer to a review that is not part of this document. The sentences they sit in are readable on their own, so no behaviour depends on them; a reader of the spec alone cannot tell what they point to.

## Minor notes

- m-1: README:31 ("No git commits, pushes, PRs or GitHub comments") is a rule for the workers of the planning run; the spec cites it as general evidence in WC-9 (spec:67) and for `/sc:git` (spec:133). The repo's own `CLAUDE.md` rules are the stronger citation (UNVERIFIED here).
- m-2: E3 (spec:23) cites `invocation_method: "skill-direct"` as support while 1.4(1) (spec:43) says the earlier run used an Agent-tool subagent and proves only the nested route. The spec states the gap; E3 should carry the same caveat.
- m-3: The P1 rationale "No person gate is involved" (spec:159) sits beside P1 rows that refuse `--mode socratic`, `--format interactive` and `--watch` (spec:102, 108, 123).
- m-4: AC-C5 (spec:176) requires no removed lines in command files; adding `[--unattended]` to a Usage line removes the old line. Adding a new line avoids it. Say so.
- m-5: Step 5 of the live check (spec:184) searches the transcript for the string `AskUserQuestion`; a tool list or prose mention gives a false fail.

## Follow-up candidates (Medium and minor; never trigger a revision)

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12, M-13, M-14; m-1 to m-5.
No issue was created. The question "open an issue for these follow-up candidates?" is left to the session that owns this loop (one question per loop); this run was not able to ask it.

## Brief clauses overridden

None. The brief did not widen scope, did not grade a minor finding as blocking and did not ask for "apply all findings".

## Reviser brief

Blocking finding ids: B-1, B-2.

Restated contract (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id. Leave every Medium and minor finding alone. Do not award yourself a PASS.

- B-1: narrow step 3 of the live check in section 7.2, or the AC-0.4 pass condition, so that in P0 the report path and status are those of the command's existing report file (as step 4 already does).
- B-2: narrow the P1 scope sentence (spec:159) and AC-1.1 (spec:195) so each command's `## Unattended mode` section and flag are added in the phase named in its own section 3 row, as already done for the P4 commands.

verdict: FAIL
