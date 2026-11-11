You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r4/vf1-clean. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r4/vf1-clean/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r4/vf1-clean/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1-r4/vf1-clean/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md F1)
### F1 (blocking, Wiegers / Adzic): AC-1.1 requires a contract-naming `## Unattended mode` section on `/sc:load`, which the spec says gets no report
- Texts that conflict:
  - AC-1.1 (SPEC:195): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `/sc:load` is in section 3.2 and its Report cell is "none (see note)", Resume "n/a", and "use it as a step inside another worker's brief, not as its own Task" (SPEC:112).
  - Decisions (SPEC:265): "a report file would be an unrequested addition".
  - WC-4 (SPEC:62) makes the contract the thing an unattended command writes; P1 scope for load is "usage line only" (SPEC:159).
- Grading sentence: An implementer who follows SPEC:112 and SPEC:265 gives `/sc:load` only a usage-line fix and no contract section, and that implementation fails AC-1.1 at SPEC:195. Following AC-1.1 instead makes the implementer add a contract-naming section to a command the spec says writes no report, which contradicts SPEC:265. Both builds are wrong because the spec says both are right.

#### M1.b (round1-b.md B1)
### B1 (CRITICAL, blocking): `/sc:load` is both given no report and required to have one

Grading sentence: an implementer who follows the stated text as written builds a `/sc:load` that satisfies the section 3.2 row (no report, "usage line only") and then fails AC-1.1; or builds the `## Unattended mode` section naming `return-contract.yaml` that AC-1.1 demands and breaks the row and the Decision. Either way the P1 acceptance check cannot pass without breaking another stated text.

Conflicting texts:
- SPEC:112: load row, Report (WC-4) = "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task", phase "P1 (usage line only)".
- SPEC:265: Decision "`/sc:load` handling": "a report file would be an unrequested addition. Only its usage-line defect is fixed."
- SPEC:76 and SPEC:159: every command in 3.2 gets the `## Unattended mode` section and accepts `--unattended` in P1.
- SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
- Supporting inventory: INV-B:65 (load writes no file; if dispatched it would need a context-summary file).


### M2

#### M2.a (round1-a.md F2)
### F2 (blocking, Adzic / Wiegers): AC-0.4 step 3 cannot pass in P0 for the commands it names
- Texts: AC-0.4 (SPEC:194) says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 of the live check (SPEC:182) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Facts the spec itself states: in P0 no command has the WC-4 contract or `--unattended` (the contract is added in P1, SPEC:159; SPEC:79 says the worker "reports the named file until Phase 1 adds the contract"). The `/sc:troubleshoot` row names `REPORT.md` as its report (SPEC:91). The inventory confirms troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (`INV-B:242`), so it has no contract `status` to match.
- Grading sentence: An implementer who runs AC-0.4 as written on `/sc:troubleshoot "<symptom>"` finds no contract file, so "the contract's `status`" and "the WC-4 contract path" in step 3 do not exist, and the check cannot pass. The same holds for `/sc:adversarial`, whose contract filename is not fixed until P1 (SPEC:83; `INV-A:60`). AC-0.4 exempts only step 4, not step 3.

#### M2.b (round1-c.md F2)
### F2 (blocking) - Adzic, Crispin - AC-0.4 cannot pass as written
Grading sentence: an implementer who runs AC-0.4 as written on `/sc:troubleshoot` and `/sc:adversarial` builds a P0 whose step 3 can never pass, because step 3 requires the report path to be "the WC-4 contract path" and the spec says that contract does not exist until P1.

Quoted texts:
1. Spec:182 (7.2 step 3): "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
2. Spec:194 (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
3. Spec:62 (WC-4): the contract is `<output-dir>/return-contract.yaml`; spec:91: troubleshoot's report today is `REPORT.md`; spec:83: adversarial's contract filename "not fixed" and the fix is P1 (spec:159, spec:198).

Attack (state trace): P0 smoke run of troubleshoot. Before: no `return-contract.yaml`. Worker sends `worker_done --report-path REPORT.md`. Step 3 pass condition: "report path is the WC-4 contract path" -> false; "outcome matches the contract's status" -> there is no contract to match. AC-0.4 declares steps 1-3 must pass. The text relaxes only step 4. The gate that decides whether section 1 stands (spec:194, "a failure here reopens section 1") therefore fails or is applied by guess.


### M3

#### M3.a (round1-b.md B2)
### B2 (CRITICAL, blocking): the single report path rule cannot be met by commands whose `--output` is a file or that have no output directory

Grading sentence: an implementer who follows WC-4 as written puts the contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is the value of `--output`; for `/sc:tdd` and `/sc:init-lite` the brief passes `--output <file>`, so the implementer builds a path under a file (or must guess a directory), and the acceptance check `test -s <contract>` has no defined path to test.

Conflicting texts:
- SPEC:62 (WC-4): contract is `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", "known before dispatch".
- SPEC:87: init-lite "Brief must pass `--output <file>`". SPEC:90: tdd "`--output <file>`", report "the TDD at `--output`". SPEC:200 (AC-2.2): `/sc:tdd "auth" --unattended --output <file>` must produce a contract with `status: blocked`.
- SPEC:183 (7.2 step 4): `test -s <contract>` and parse it; SPEC:182: report path "is the WC-4 contract path".
- SPEC:83: adversarial contract is fixed at `<output>/adversarial/return-contract.yaml` (a sub-directory), unlike the `<output>/return-contract.yaml` of brainstorm and reflect (SPEC:84, 88). SPEC:85 and SPEC:86: cleanup-audit and index-repo have a fixed or implied output location and no directory flag.
- SPEC:120: spec-panel gets "add `--output`" with no statement whether it is a file or a directory.
- Evidence the question is real: `CMD:460` (the spec-panel definition in the sandbox) resolves the same problem with a separate `--report-dir` because "`--output` is file-valued".


### M4

#### M4.a (round1-b.md B3)
### B3 (CRITICAL, blocking): P1 makes `--unattended` accepted by every command, including those whose unattended gate behaviour arrives only in P2 or P4

Grading sentence: an implementer who follows SPEC:159 builds `--unattended` (and the `## Unattended mode` section) on `auggie-review`, `task`, `post-release`, `pr-submit` and `implement` in P1 with no gate resolution, so `/sc:auggie-review <PR> --unattended` still posts to the PR and `/sc:post-release --unattended` still installs or provisions; that contradicts WC-9 and WC-2, which define `--unattended` as "outward defaults off" and "no person-blocking step".

Conflicting texts:
- SPEC:159 (P1): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
- SPEC:67 (WC-9) and SPEC:60 (WC-2): under `--unattended` outward defaults are off and no gate blocks on a person.
- SPEC:100, 121 (auggie-review, task: P2), SPEC:113, 114, 109 (post-release, pr-submit, implement: P4), SPEC:162, 154 (P4 waits for D2-D4), SPEC:195 (AC-1.1 requires the section on all of them in P1).
- SPEC:138-139 and 114/241 and 240: under D3 option (a), pr-submit is not a worker, yet P1 and AC-1.1 add the flag and section to it.
- Evidence of the outward default: SPEC:67 cites `cmd/auggie-review.md:51-54` (UNVERIFIED here); INV-A:78 states it.


### M5

#### M5.a (round1-c.md F1)
### F1 (blocking) - Wiegers, Cockburn - AC-1.1 contradicts D3(a), the P4 deferral and "Phases 1-3 need no user decision"
Grading sentence: an implementer who follows the stated text as written builds a P1 that adds an `## Unattended mode` section, a `--unattended` flag and a passing test for `pr-submit`, `implement` and `post-release`, and that is wrong because the same document says those three commands' unattended behaviour waits for user decisions D2-D4 in P4, and under the recommended D3(a) pr-submit gets no change at all.

Quoted texts:
1. Spec:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
2. Spec:195 (AC-1.1, a P1 check): "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
3. Spec:154 and spec:225: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
4. Spec:240 (D3(a), the recommendation): "no pr-submit changes in Phase 4"; spec:139: "`/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3".
5. Spec:109, spec:113, spec:114, spec:162: implement, post-release and pr-submit are rows of section 3.2 with phase P4 and gates that D2 to D4 decide.

Attack (Whittaker, sequence attack): run the phases in the spec's order. After P1, AC-1.1 passes only if pr-submit, implement and post-release each carry the section. pr-submit has real gates (`--monitor 1` y/n, operator HALTs, `INV-B:34`, `INV-B:89`), so a "no-op" flag is not available for it (the text at 159 allows a no-op only "where a command has no gate"). Under D3(a) the section must not exist, so AC-1.1 fails by construction for the recommended path. Under D3(b) it is P4 work done in P1 before the user decided. Two stated texts contradict (AC-1.1 against D3(a) and against 154/225), and an acceptance criterion cannot pass on the recommended path.

Evidence check: inventory confirms pr-submit has default-off gates only at `--monitor 1` and halts handed to "the operator" (`INV-B:89`), and implement's halt cannot be unblocked by another agent (`INV-A:66`; the Ruling rule at `refs/qa.md:238` is quoted in `commands-a.md` notes and is UNVERIFIED against the source here).

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
