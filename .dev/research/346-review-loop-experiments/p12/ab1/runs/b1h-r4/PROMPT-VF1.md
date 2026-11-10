You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf1. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf1/ws is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf1/home. Files under /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab1/runs/b1h-r4/vf1/home are inside the sandbox and may be read; a path written with `~` means the same path under it.

TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
Verify the blocking findings listed below against the candidate .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (sha256 of the file). You see only the candidate and this finding list, not the review report or the reviewer's reasoning. For each finding, find every text it quotes or cites in the candidate yourself, with `grep -nF` or by reading the cited line, and copy what you found; when a finding names two texts that contradict, check both. State whether the quoted text exists as quoted and whether the stated wrong outcome follows from the candidate's text with no further assumption. Confirm a finding only if both hold; otherwise reject it with one sentence that names what is missing. Add no finding, regrade nothing and edit nothing. Write one table row per finding: id, found text, exists yes/no, outcome follows yes/no, confirm or reject, reason. End with one line `confirmed: <ids>`, or `confirmed: none`. Findings: 

Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md B1)
**B1. Output flag value types contradict each other (tdd, spec-panel, AC-2.2).** Expert: Fowler (lead), Wiegers. Severity: MAJOR, blocking.
- Stated texts: WC-4 says the contract goes in `<output-dir>`, "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). The tdd row gives `--output <file>` (spec:90). The AC-2.2 gate-trigger example is `/sc:tdd "auth" --unattended --output <file>` (spec:200). The spec-panel row says "add `--output`" (spec:120).
- Grading sentence: An implementer who follows WC-4 as written writes the contract to `<tdd-file>/return-contract.yaml`, and because a regular file cannot hold a child path, the contract is never written; WC-5 (spec:63) then reports every such tdd run as failed for want of a report.
- Command evidence: `command.md:23` already defines `--output <file>` for spec-panel, and `command.md:460` says "`--report-dir <dir>` only (`--output` is file-valued)". The unattended contract goes under `<report-dir>` (`command.md:461`). So spec:120 would add a directory-valued `--output` where the command already has a file-valued one.
- Stale evidence: INV-B:182 says spec-panel has "no path or `--output` flag" and cites `cmd/spec-panel.md:22`. That is out of date against `command.md:23`, `:459-461`. The spec row at spec:120 inherits the stale claim (spec:11 says only 11 locations were re-read).

### M2

#### M2.a (round1-a.md B2)
**B2. init-lite re-run overwrites its report, which WC-6 forbids.** Expert: Nygard (lead), Fowler. Severity: MAJOR, blocking.
- Stated texts: section 3.1 gives init-lite "Re-run overwrites its marked report" (spec:87). WC-6 says a command either resumes from its on-disk state or "writes each run into a fresh output directory so a re-run starts clean", and that a retry "must not corrupt the first attempt's output" (spec:64). The inventory agrees on the overwrite (INV-A:55).
- Grading sentence: An implementer who follows section 3.1 leaves init-lite as it is, so a `worker-start --retry-of` re-run replaces the first attempt's `context-audit.md`; WC-6 says the retry must not corrupt that output, and the spec names no third option.

### M3

#### M3.a (round1-a.md B3)
**B3. The outcome mapping treats an empty or status-less contract as success.** Expert: Whittaker (FR-2.1 Zero/Empty), Wiegers. Severity: MAJOR, blocking (names a concrete wrong outcome).
- Stated text: `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise (spec:63). Acceptance check step 4 (spec:183) tests `test -s` and a `status` value, but only after `worker_done` has already settled the Task (CAPS:77).
- Grading sentence: An implementer who follows WC-5 as written sends `--outcome succeeded` for a 0-byte `return-contract.yaml` left by a worker killed mid-write, because the file exists and says neither `failed` nor `blocked`; the Task then settles as completed with no content (CAPS:77), and the ready view starts its dependents (CAPS:86).

### M4

#### M4.a (round1-b.md B1)
### B1. Phase 0 acceptance check AC-0.4 cannot pass as written. CRITICAL.
- Location: `SPEC:194` (AC-0.4), `SPEC:182` (7.2 step 3), `SPEC:183` (7.2 step 4), `SPEC:158` (P0 scope).
- Wrong outcome: AC-0.4 says "steps 1-3 and 5-7 pass". Step 3's pass condition requires "its report path is the WC-4 contract path" (`SPEC:182`). P0 writes no WC-4 contract; the contract "arrives in P1" (`SPEC:194`). So step 3 cannot pass in P0. AC-0.4 also redefines step 4 to use "the command's existing report file" (`SPEC:194`), but step 4's pass condition requires a YAML file with `status` in four values and a `command` key (`SPEC:183`). An existing REPORT.md or a `.md` does not satisfy it.
- Grading sentence: an implementer who follows AC-0.4 as written cannot make steps 3 and 4 pass in P0, so the P0 gate is unpassable (`SPEC:158` says P0 tests the decision, and section 1.4 at `SPEC:43` makes that test the gate). Either the implementer declares a pass the check does not support, or the phase never closes.

### M5

#### M5.a (round1-b.md B2)
### B2. Phase 1 lets `--unattended` run with PR posting still on. CRITICAL.
- Location: `SPEC:159` (P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"), `SPEC:160` (P2 converts gates, including auggie-review), `SPEC:100` (auggie-review row: `--unattended` implies `--no-post-pr`, posting only with `--post-pr`), `SPEC:67` (WC-9).
- Wrong outcome: "a no-op where a command has no gate" implies that for a gated command the flag must do something in P1. P1 does not include gate conversion (that is P2). An implementer who follows P1 as written either (a) accepts the flag as a no-op for auggie-review, so `/sc:auggie-review <PR> --unattended` still posts to GitHub by default, or (b) implements the P2 gate inside P1, which P1's scope does not name. Both readings either violate WC-9 or contradict the phase split.
- Grading sentence: an implementer who follows `SPEC:159` as written builds auggie-review that accepts `--unattended` and still posts review comments to the PR, and that is wrong because WC-9 (`SPEC:67`) says a default that posts to GitHub is off under `--unattended`. The phase text and the P2 assignment (`SPEC:160`) contradict each other on this one command.

### M6

#### M6.a (round1-b.md B3)
### B3. Default output path breaks WC-11 for index-repo. MAJOR.
- Location: `SPEC:69` (WC-11: "Default output paths carry a timestamp or the slug the coordinator passes"), `SPEC:86` (index-repo: brief passes "none"; report `PROJECT_INDEX.md`; fix is "State the output location (P1)"), `SPEC:85` (cleanup-audit: fixed output dir, "one audit per worktree at a time (WC-11)"), `INV-A:53` (index-repo has no output parameter, default at repo root).
- Wrong outcome: an implementer who follows `SPEC:86` builds index-repo with the default `PROJECT_INDEX.md` and no output flag, so the coordinator cannot pass a slug. WC-11 says a default output path carries a timestamp or a slug. The 3.1 fix ("state the output location") does not add one. cleanup-audit (`SPEC:85`) cites WC-11 but does not satisfy it either; its fix is a coordinator rule that is absent from the 2.3 brief.
- Grading sentence: an implementer who follows `SPEC:86` writes `PROJECT_INDEX.md` as a fixed default with no slug, and that is wrong because WC-11 (`SPEC:69`) says default output paths carry a timestamp or the slug the coordinator passes; the sentence needs no further assumption.

### M7

#### M7.a (round1-b.md B4)
### B4. The load row contradicts WC-4 and AC-1.1. MAJOR.
- Location: `SPEC:112` (load: "Report (WC-4): none"), `SPEC:265` (Decisions: a report file for load "would be an unrequested addition"), `SPEC:76` (every changed command gains the Unattended section), `SPEC:195` (AC-1.1: every command in 3.1-3.2 has a section "naming return-contract.yaml"), `SPEC:62` (WC-4: changed commands write the contract in unattended mode).
- Wrong outcome: load is listed under "Needs a change" (`SPEC:112`), so WC-4 applies to it, but its row and its Decision say it writes no file. AC-1.1 then requires a section that names a file load never writes.
- Grading sentence: an implementer who follows the load row and the Decision writes no contract, and that is wrong because WC-4 (`SPEC:62`) requires one for every changed command, and AC-1.1 (`SPEC:195`) fails for load without an invented section.

### M8

#### M8.a (round1-c.md B-1)
#### B-1. WC-4 and the adversarial P1 fix name different contract paths (blocking)
- Quotes: WC-4 says the command "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`candidate:62`). The adversarial row says the brief "must pass `--output <dir>`" and the P1 fix is "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" (`candidate:83`).
- Grading sentence: an implementer who follows WC-4 writes adversarial's contract to `<dir>/return-contract.yaml`, while the P1 fix (`candidate:83`) writes the same contract to `<dir>/adversarial/return-contract.yaml`. The coordinator opens the path WC-4 names (`candidate:73`, `candidate:182`), finds no file, and WC-5 maps the run to `failed` ("no report exists", `candidate:63`). The two texts contradict each other, so this is blocking.
- Acceptance check AC-1.4 (`candidate:198`) only asks that adversarial "names one fixed path". It does not say which, so it cannot decide the conflict.
- Evidence of the current state: adversarial real runs wrote the contract in two places (`commands-a.md:60`). The spec's own text carries that (`candidate:83`).

### M9

#### M9.a (round1-c.md B-2)
#### B-2. AC-C1 cannot fail, so the SA-2 gate is non-functional (blocking)
- Quotes: AC-C1 is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' ... \| grep -v ...`, "prints nothing (SA-2, WC-8)" (`candidate:172`). SA-2 says the rule is "a hard requirement on every phase" (`candidate:142`). AC-C1 is listed under "Common checks (every phase)" (`candidate:169`).
- Grading sentence: an implementer who runs AC-C1 as written, after putting `orca-ide worktree list` into a command file, gets empty output and records SA-2 and WC-8 as passed. That command then fails with `runtime_unavailable` outside Orca (`orca-capabilities.md:147`). This is checkable in the sandbox. The pattern inside single quotes is ERE, where `\|` is a literal pipe, so the alternation never matches: `printf 'orca-ide worktree list\n' | grep -nE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` printed nothing and exited 1. The corrected form with `|` matched the same line and exited 0.
- A second defect in the same line: in the raw source, the `\|` before `grep -v` is not a shell pipe. In an unquoted shell `\|` passes a literal `|` argument (run in the sandbox: `echo a \| cat` printed `a | cat`). The second stage therefore fails with an error and never filters. The table-escape convention (`\|` renders as `|` in a GFM table cell) explains the author's intent, but the worker reads the raw source, so the command as written is wrong in both places. The same `\|` shell-pipe form appears in AC-C4 (`candidate:175`), AC-C5 (`candidate:176`) and AC-0.3 (`candidate:193`).

Write your full reply to .dev/orca-command-refactor/review/verify-1.md. Do not edit anything else. Write only your output file.

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
