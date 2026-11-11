review: 1 of 3

# Merged first review (coordinator; MERGE rule over three independent first reviews)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d

sources:
- .dev/orca-command-refactor/review/round1-a.md verdict FAIL sha256 85c0cdc8639c07cdcfcfecf761b9d6f4462d07daf4a60368241530fe756123e8
- .dev/orca-command-refactor/review/round1-b.md verdict FAIL sha256 51a19315af8e3382faf6ba675061fc671df61dbec79d35e8b8dd3eb8ddd77e2a
- .dev/orca-command-refactor/review/round1-c.md verdict FAIL sha256 5efe1dab5b50b30f950e5c74fa0b6b5dc3f5c999b4cff65ea2d385f9172020ed

> verification (coordinator, VERIFY step VF1; verifier reply .dev/orca-command-refactor/review/verify-1.md): confirmed blocking ids: M2, M4, M6, M7, M8, M9. Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: M1 (verifier: The file-versus-directory contradiction between WC-4 and the tdd row is real. The stated outcome (contract written to `<tdd-file>/return-contract.yaml`, never written, WC-5 reports failed) needs the implementer to read a file-valued `--output` as a directory, which the candidate does not say. The `command.md:23` and `:459-461` evidence and `INV-B:182` are outside the workspace and UNVERIFIED.); M3 (verifier: WC-5 is the worker's own rule and runs only before the worker sends `worker_done`. A worker killed mid-write sends no `worker_done`, so the stated `--outcome succeeded` cannot come from that worker. The candidate has no text where a surviving worker reads a 0-byte file and sends succeeded. The settling and dependent-start effects depend on CAPS text that cannot be checked here.); M5 (verifier: The contradiction is real: the no-op qualifier covers only gate-less commands, and auggie-review sits in section 3.2 with a gate resolution. But line 159 does not say what the flag does for auggie-review in P1, so "still posts to GitHub" needs an unstated choice that P1 leaves the command unchanged. AC-1.2 (line 196) covers only P1 commands, and the posting check AC-2.4 (line 202) runs after P2.). The Reviser brief below is narrowed to the confirmed ids.

## Blocking findings (merged, confirmed)

### M2

#### M2.a, from round1-a.md B2: *B2. init-lite re-run overwrites its report, which WC-6 forbids.** Expert: Nygard (lead), Fowler. Severity: MAJOR, blocking.
- Stated texts: section 3.1 gives init-lite "Re-run overwrites its marked report" (spec:87). WC-6 says a command either resumes from its on-disk state or "writes each run into a fresh output directory so a re-run starts clean", and that a retry "must not corrupt the first attempt's output" (spec:64). The inventory agrees on the overwrite (INV-A:55).
- Grading sentence: An implementer who follows section 3.1 leaves init-lite as it is, so a `worker-start --retry-of` re-run replaces the first attempt's `context-audit.md`; WC-6 says the retry must not corrupt that output, and the spec names no third option.
- Recommendation: give init-lite a fresh output directory per run (its report path is the only state), or state in WC-6 that overwrite is an allowed mode with its reason. The first keeps WC-6 unchanged.
- Priority: High. Quality impact: loses the first attempt's report on every retry.

### M4

#### M4.a, from round1-b.md B1: B1. Phase 0 acceptance check AC-0.4 cannot pass as written. CRITICAL.
- Location: `SPEC:194` (AC-0.4), `SPEC:182` (7.2 step 3), `SPEC:183` (7.2 step 4), `SPEC:158` (P0 scope).
- Expert: Adzic (examples), Crispin (test completeness), Wiegers (testability).
- Wrong outcome: AC-0.4 says "steps 1-3 and 5-7 pass". Step 3's pass condition requires "its report path is the WC-4 contract path" (`SPEC:182`). P0 writes no WC-4 contract; the contract "arrives in P1" (`SPEC:194`). So step 3 cannot pass in P0. AC-0.4 also redefines step 4 to use "the command's existing report file" (`SPEC:194`), but step 4's pass condition requires a YAML file with `status` in four values and a `command` key (`SPEC:183`). An existing REPORT.md or a `.md` does not satisfy it.
- Grading sentence: an implementer who follows AC-0.4 as written cannot make steps 3 and 4 pass in P0, so the P0 gate is unpassable (`SPEC:158` says P0 tests the decision, and section 1.4 at `SPEC:43` makes that test the gate). Either the implementer declares a pass the check does not support, or the phase never closes.
- Recommendation: restate AC-0.4 for P0 with its own pass conditions: step 3 checks `worker_done` exactly once and its `--outcome` against the existing report's first-sentence status; step 4 is dropped in P0 and run first in P1. Delete the sentence that calls step 4 "uses the command's existing report file".
- Priority: High. Quality impact: high (the spec's gate on its central decision).

### M6

#### M6.a, from round1-b.md B3: B3. Default output path breaks WC-11 for index-repo. MAJOR.
- Location: `SPEC:69` (WC-11: "Default output paths carry a timestamp or the slug the coordinator passes"), `SPEC:86` (index-repo: brief passes "none"; report `PROJECT_INDEX.md`; fix is "State the output location (P1)"), `SPEC:85` (cleanup-audit: fixed output dir, "one audit per worktree at a time (WC-11)"), `INV-A:53` (index-repo has no output parameter, default at repo root).
- Expert: Fowler (interfaces), Hohpe (shared channel), Newman (evolution).
- Wrong outcome: an implementer who follows `SPEC:86` builds index-repo with the default `PROJECT_INDEX.md` and no output flag, so the coordinator cannot pass a slug. WC-11 says a default output path carries a timestamp or a slug. The 3.1 fix ("state the output location") does not add one. cleanup-audit (`SPEC:85`) cites WC-11 but does not satisfy it either; its fix is a coordinator rule that is absent from the 2.3 brief.
- Grading sentence: an implementer who follows `SPEC:86` writes `PROJECT_INDEX.md` as a fixed default with no slug, and that is wrong because WC-11 (`SPEC:69`) says default output paths carry a timestamp or the slug the coordinator passes; the sentence needs no further assumption.
- Recommendation: give index-repo an `--output` flag (P1) and add it to the brief column, or move index-repo to needs-change. For cleanup-audit, add "one audit per worktree" to the 2.3 brief rules as a coordinator obligation.
- Priority: Medium-High. Quality impact: medium (overwrite of a shared index).

### M7

#### M7.a, from round1-b.md B4: B4. The load row contradicts WC-4 and AC-1.1. MAJOR.
- Location: `SPEC:112` (load: "Report (WC-4): none"), `SPEC:265` (Decisions: a report file for load "would be an unrequested addition"), `SPEC:76` (every changed command gains the Unattended section), `SPEC:195` (AC-1.1: every command in 3.1-3.2 has a section "naming return-contract.yaml"), `SPEC:62` (WC-4: changed commands write the contract in unattended mode).
- Expert: Wiegers (traceability), Crispin (acceptance check).
- Wrong outcome: load is listed under "Needs a change" (`SPEC:112`), so WC-4 applies to it, but its row and its Decision say it writes no file. AC-1.1 then requires a section that names a file load never writes.
- Grading sentence: an implementer who follows the load row and the Decision writes no contract, and that is wrong because WC-4 (`SPEC:62`) requires one for every changed command, and AC-1.1 (`SPEC:195`) fails for load without an invented section.
- Recommendation: remove load from the section 3.2 table and from AC-1.1 (it is a context loader, `SPEC:265`), or give it a contract that reports "loaded: <keys>". Pick one.
- Priority: Medium-High (small consequence, since `SPEC:112` also says load is not dispatched as its own Task). Quality impact: low to medium.

### M8

#### M8.a, from round1-c.md B-1: B-1. WC-4 and the adversarial P1 fix name different contract paths (blocking)
- Expert: Wiegers (testability), with Fowler.
- Quotes: WC-4 says the command "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`candidate:62`). The adversarial row says the brief "must pass `--output <dir>`" and the P1 fix is "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" (`candidate:83`).
- Grading sentence: an implementer who follows WC-4 writes adversarial's contract to `<dir>/return-contract.yaml`, while the P1 fix (`candidate:83`) writes the same contract to `<dir>/adversarial/return-contract.yaml`. The coordinator opens the path WC-4 names (`candidate:73`, `candidate:182`), finds no file, and WC-5 maps the run to `failed` ("no report exists", `candidate:63`). The two texts contradict each other, so this is blocking.
- Acceptance check AC-1.4 (`candidate:198`) only asks that adversarial "names one fixed path". It does not say which, so it cannot decide the conflict.
- Evidence of the current state: adversarial real runs wrote the contract in two places (`commands-a.md:60`). The spec's own text carries that (`candidate:83`).
- Recommendation: choose one rule and make the other text follow it. The narrowest change is to replace the literal in WC-4 with "the fixed path named for each command in section 3", then put the exact path for each command in the section 3 rows, and make AC-1.4 check that path. Add no new mechanism.
- Priority: High. Quality impact: high. Without a fix, every adversarial worker fails at the coordinator's read step, or the coordinator reads a stale file.

### M9

#### M9.a, from round1-c.md B-2: B-2. AC-C1 cannot fail, so the SA-2 gate is non-functional (blocking)
- Expert: Adzic (acceptance checks as examples), with Wiegers.
- Quotes: AC-C1 is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' ... \| grep -v ...`, "prints nothing (SA-2, WC-8)" (`candidate:172`). SA-2 says the rule is "a hard requirement on every phase" (`candidate:142`). AC-C1 is listed under "Common checks (every phase)" (`candidate:169`).
- Grading sentence: an implementer who runs AC-C1 as written, after putting `orca-ide worktree list` into a command file, gets empty output and records SA-2 and WC-8 as passed. That command then fails with `runtime_unavailable` outside Orca (`orca-capabilities.md:147`). This is checkable in the sandbox. The pattern inside single quotes is ERE, where `\|` is a literal pipe, so the alternation never matches: `printf 'orca-ide worktree list\n' | grep -nE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` printed nothing and exited 1. The corrected form with `|` matched the same line and exited 0.
- A second defect in the same line: in the raw source, the `\|` before `grep -v` is not a shell pipe. In an unquoted shell `\|` passes a literal `|` argument (run in the sandbox: `echo a \| cat` printed `a | cat`). The second stage therefore fails with an error and never filters. The table-escape convention (`\|` renders as `|` in a GFM table cell) explains the author's intent, but the worker reads the raw source, so the command as written is wrong in both places. The same `\|` shell-pipe form appears in AC-C4 (`candidate:175`), AC-C5 (`candidate:176`) and AC-0.3 (`candidate:193`).
- Recommendation: write the pipes and the alternation as plain `|` inside each code span, and move each check out of the table cell into a fenced block, so the raw text and the rendered text agree. Add a positive control to AC-C1: the check must match a planted line (for example `orca-ide worktree list`) before it is trusted.
- Priority: High. Quality impact: high for SA-2 and WC-8, which are the only mechanical gates for them.

## Noted, unactioned (verifier rejected; not prior blocking findings)

### M1 (verifier: The file-versus-directory contradiction between WC-4 and the tdd row is real. The stated outcome (contract written to `<tdd-file>/return-contract.yaml`, never written, WC-5 reports failed) needs the implementer to read a file-valued `--output` as a directory, which the candidate does not say. The `command.md:23` and `:459-461` evidence and `INV-B:182` are outside the workspace and UNVERIFIED.)

#### M1.a, from round1-a.md B1: *B1. Output flag value types contradict each other (tdd, spec-panel, AC-2.2).** Expert: Fowler (lead), Wiegers. Severity: MAJOR, blocking.
- Stated texts: WC-4 says the contract goes in `<output-dir>`, "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). The tdd row gives `--output <file>` (spec:90). The AC-2.2 gate-trigger example is `/sc:tdd "auth" --unattended --output <file>` (spec:200). The spec-panel row says "add `--output`" (spec:120).
- Grading sentence: An implementer who follows WC-4 as written writes the contract to `<tdd-file>/return-contract.yaml`, and because a regular file cannot hold a child path, the contract is never written; WC-5 (spec:63) then reports every such tdd run as failed for want of a report.
- Command evidence: `command.md:23` already defines `--output <file>` for spec-panel, and `command.md:460` says "`--report-dir <dir>` only (`--output` is file-valued)". The unattended contract goes under `<report-dir>` (`command.md:461`). So spec:120 would add a directory-valued `--output` where the command already has a file-valued one.
- Stale evidence: INV-B:182 says spec-panel has "no path or `--output` flag" and cites `cmd/spec-panel.md:22`. That is out of date against `command.md:23`, `:459-461`. The spec row at spec:120 inherits the stale claim (spec:11 says only 11 locations were re-read).
- Recommendation: WC-4 must name the contract location per flag type. For file-valued outputs, the contract goes beside the file or in a named `--report-dir`. spec-panel should use its existing `--report-dir` and not a new `--output`. Fix spec:90, spec:120 and AC-2.2 (spec:200) to match.
- Priority: High. Quality impact: every tdd and spec-panel worker run.

### M3 (verifier: WC-5 is the worker's own rule and runs only before the worker sends `worker_done`. A worker killed mid-write sends no `worker_done`, so the stated `--outcome succeeded` cannot come from that worker. The candidate has no text where a surviving worker reads a 0-byte file and sends succeeded. The settling and dependent-start effects depend on CAPS text that cannot be checked here.)

#### M3.a, from round1-a.md B3: *B3. The outcome mapping treats an empty or status-less contract as success.** Expert: Whittaker (FR-2.1 Zero/Empty), Wiegers. Severity: MAJOR, blocking (names a concrete wrong outcome).
- Stated text: `--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise (spec:63). Acceptance check step 4 (spec:183) tests `test -s` and a `status` value, but only after `worker_done` has already settled the Task (CAPS:77).
- Grading sentence: An implementer who follows WC-5 as written sends `--outcome succeeded` for a 0-byte `return-contract.yaml` left by a worker killed mid-write, because the file exists and says neither `failed` nor `blocked`; the Task then settles as completed with no content (CAPS:77), and the ready view starts its dependents (CAPS:86).
- Recommendation: `succeeded` only when the contract parses and has `status` in {`succeeded`, `partial`}; every other state (missing, empty, unparseable, no `status`) maps to `failed`. Also move the `test -s` check into the worker's own mapping.
- Priority: High. Quality impact: silent success on crashed workers.

### M5 (verifier: The contradiction is real: the no-op qualifier covers only gate-less commands, and auggie-review sits in section 3.2 with a gate resolution. But line 159 does not say what the flag does for auggie-review in P1, so "still posts to GitHub" needs an unstated choice that P1 leaves the command unchanged. AC-1.2 (line 196) covers only P1 commands, and the posting check AC-2.4 (line 202) runs after P2.)

#### M5.a, from round1-b.md B2: B2. Phase 1 lets `--unattended` run with PR posting still on. CRITICAL.
- Location: `SPEC:159` (P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"), `SPEC:160` (P2 converts gates, including auggie-review), `SPEC:100` (auggie-review row: `--unattended` implies `--no-post-pr`, posting only with `--post-pr`), `SPEC:67` (WC-9).
- Expert: Fowler (interface and phase boundary), Nygard (safety under partial rollout), Cockburn (actor: the coordinator's brief).
- Wrong outcome: "a no-op where a command has no gate" implies that for a gated command the flag must do something in P1. P1 does not include gate conversion (that is P2). An implementer who follows P1 as written either (a) accepts the flag as a no-op for auggie-review, so `/sc:auggie-review <PR> --unattended` still posts to GitHub by default, or (b) implements the P2 gate inside P1, which P1's scope does not name. Both readings either violate WC-9 or contradict the phase split.
- Grading sentence: an implementer who follows `SPEC:159` as written builds auggie-review that accepts `--unattended` and still posts review comments to the PR, and that is wrong because WC-9 (`SPEC:67`) says a default that posts to GitHub is off under `--unattended`. The phase text and the P2 assignment (`SPEC:160`) contradict each other on this one command.
- Recommendation: either move auggie-review's flag acceptance to P2, or make P1 reject `--unattended` for any command whose gate is not yet converted (fail closed). State which in `SPEC:159`. Add an AC-1 check that auggie-review under `--unattended` posts nothing in P1.
- Priority: High. Quality impact: high (outward action).

## Follow-up candidates

Listed in the three source reports above; not merged.

## Reviser brief

Blocking finding ids: M2, M4, M6, M7, M8, M9.
Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
