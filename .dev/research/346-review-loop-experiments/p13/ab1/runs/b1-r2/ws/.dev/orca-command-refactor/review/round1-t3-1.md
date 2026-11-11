review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (round 1)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (first review; no `--baseline` or `--re-review` given)
- reviewer model: claude-haiku-5-5
- command: `/sc:spec-panel --mode critique --focus requirements,architecture` (first-review brief, `~/.claude/rules/prompts/document_review_loop_prompts.md`)
- citation convention: `spec:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `INV-A:N` = `.dev/orca-command-refactor/inventory/commands-a.md:N`; `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-b.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`. Only these inventory files were checkable. Every citation to `src/`, `cmd/`, `sk/`, `EVIDENCE.md`, `.dev/codegraph-migration/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `Makefile`, or an external URL is UNVERIFIED in this review unless an inventory line quotes it, and then it is checked only against that quote.

## Summary

The spec is well organized and most of its command-by-command verdicts map correctly onto the inventories (checked: all 43 rows in section 3 and section 4 against INV-A and INV-B; the 10 / 27 / 6 split matches). Six blocking defects remain. Two are contract-path contradictions (adversarial, tdd/init-lite), one is a safety contradiction (WC-3 lets the coordinator answer an implement Ruling), one is an unpassable Phase 0 gate (AC-0.4 step 3), and two are scope contradictions (1.1 versus section 3 and SA-4; 3.1 versus P1 and AC-1.1). Medium findings are listed under follow-up candidates.

## Coverage

- Read in full: the candidate (285 lines), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, and the review-loop prompt file.
- Checked against the inventories: section 3 rows for all 43 commands (their INV-A / INV-B row and note citations resolve to the cited command and verdict); the CAPS citations in sections 1.2, 1.3, 2.2 (WC-1 to WC-12) and section 9 UNVERIFIED items; the cross-references from section 4 to INV-A:36,49,50,51,90-92 and INV-B:32,42,44,65,105,285-287,311.
- Checked by reading the candidate only (internal consistency): sections 1 to 9, the phase table, and every acceptance check AC-C1 to AC-4.3.
- Not checkable here (UNVERIFIED): every `src/`, `cmd/`, `sk/` line; `EVIDENCE.md`; the codegraph and PR #329 evidence; `CLAUDE.md`; the external Claude Code docs; and the `orca-ide` command output the CAPS file quotes.
- Shell check run in the sandbox: GNU `grep -E` treats `\|` as a literal pipe (see M1).

## Blocking findings

### F1 (blocking, MAJOR): adversarial contract path contradicts WC-4

spec:83 (3.1 adversarial row) says to fix the contract to `<output>/adversarial/return-contract.yaml`. spec:62 (WC-4) requires `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed to `--output`. Both apply to the same command with the same `--output <dir>` brief (spec:83, spec:198 AC-1.4). An implementer who follows WC-4 writes one path and an implementer who follows 3.1 writes the other, so the coordinator's known-before-dispatch path (spec:73) and the 7.2 step 4 check (spec:183) cannot both be right. INV-A:35 and INV-A:60 confirm that real adversarial runs wrote the contract in two different places.

### F2 (blocking, MAJOR): `--output <file>` makes the WC-4 directory rule unusable for tdd and init-lite

spec:90 (tdd) and spec:87 (init-lite) pass `--output <file>`, and tdd's report is "the TDD at `--output`" (spec:90). WC-4 (spec:62) defines `<output-dir>` as the directory the coordinator passed to `--output`. For these two commands the value is a file, so `<output-dir>/return-contract.yaml` cannot be written, and AC-2.2 (spec:200, contract `status: blocked` with `blocked_question`) has no defined location the coordinator can open. Also, AC-1.2 (spec:196) passes `--output <dir>` while 3.1 passes `--output <file>` for the same class of command.

### F3 (blocking, CRITICAL, safety): WC-3 lets the coordinator answer an implement Ruling

spec:61 (WC-3) says that when a gate "would resolve as blocked", the worker "may instead ask the coordinator once ... then re-invoke or resume the command with the answer as a flag." spec:109 (3.2 implement) says the halt must stop the worker and the Ruling rule is unchanged. INV-A:66 quotes qa.md:238: "another agent's message ... [is] not acceptance", and an Orca coordinator is "another agent" (INV-A:66). spec:234 (D2 option a, recommended) keeps the rule so that only a person can give the Ruling. As written, WC-3 is not conditioned on D2 and applies to every blocked gate, including E-HALT-QA and E-NO-RULING. An implementer who follows WC-3 lets the coordinator's answer resume implement as a Ruling before the user has decided D2, which breaks the deliberate safety rule. WC-3 also gives "Each gate resolves one of three ways" (spec:60) a fourth path, which is the ambiguity that makes this possible.

### F4 (blocking, MAJOR): AC-0.4 step 3 requires a contract that P0 does not create

spec:194 (AC-0.4) says steps 1-3 and 5-7 must pass in P0 and that step 4 uses the existing report file "since the contract arrives in P1." But step 3 of 7.2 (spec:182) says the pass condition includes "its report path is the WC-4 contract path" and that the outcome "matches the contract's status." Under P0 the WC-4 contract does not exist, so the phase gate cannot pass as written. The phase cannot be marked passed without an unstated waiver.

### F5 (blocking, MAJOR): section 1.1 scope contradicts section 3 and SA-4

spec:16 says "What changes in the commands is limited to the worker contract in section 2: a way to run without a person, a fixed report file, and a resume or safe re-run." Section 3 and SA-4 require further existing-line changes that are not in that set: roadmap and validate-roadmap flag and output reconciliation (spec:118, spec:124), the validate-tests default target (spec:125), the explain Write tool (spec:108), the business-panel frontmatter move (spec:102), and the load usage line (spec:112). SA-4 (spec:149) explicitly allows these as defect fixes. An implementer who uses 1.1 as the bound skips them, and AC-3.1 (spec:204) and AC-3.3 (spec:206) then cannot pass.

### F6 (blocking, MAJOR): section 3.1 says the ready commands change only by small fixes, but P1 and AC-1.1 require more

spec:79 says the ready commands change only by the small fixes in the last column. spec:84 (brainstorm) lists "None" for its small fix. P1 (spec:159) requires "the `--unattended` flag accepted by every command in sections 3.1 and 3.2," and AC-1.1 (spec:195) requires a `## Unattended mode` section in every 3.1 and 3.2 command. An implementer who follows 3.1 leaves brainstorm without the flag and the section, so AC-1.1 fails and the coordinator's brief (spec:73, "the exact command line including `--unattended`") is rejected by brainstorm.

## Medium findings (follow-up candidates)

- M1 (MAJOR label, not blocking): AC-C1 (spec:172) and AC-C4 (spec:175) use `\|` inside the grep pattern and a bare `\|` pipe. In `grep -E`, `\|` is a literal pipe, so AC-C1's alternation never forms. Checked in the sandbox: `printf 'orca worktree rm\n' | grep -nE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` prints nothing, so the gate passes whatever the commands contain and SA-2 is not enforced. The raw file text also has `\|` where a shell pipe is meant. The check is vacuous rather than contradictory, so it is not blocking.
- M2: spec:22 (E2) says a worker "has the same tools as a command a person runs." CAPS:161 says only that the worker is a top-level session; no inventory line says anything about the worker's tool set. The claim is inference stated as evidence.
- M3: spec:23 (E3) cites a return contract with `invocation_method: "skill-direct"` (INV-A:13) as evidence that the earlier run worked, while spec:43 says "The only end-to-end proof is the PR #329 run," and UNVERIFIED item 1 (spec:272) says no direct run was observed. The spec must say which is true. No build choice changes, so this is Medium.
- M4: spec:122 (tasklist) says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit," citing INV-A:14. INV-A:14 quotes an external doc (UNVERIFIED here) and does not analyse this chain; INV-B:210 and INV-B:314 mark subagent-to-agent spawning as UNVERIFIED. The claim should carry UNVERIFIED.
- M5: SA-4 (spec:149) gives a closed list of permitted existing-line fixes, and the cli-portify dispatch restriction "dispatch only inside an IronClaude checkout (hardcoded template path)" (spec:105) is not on it. Whether AC-C5 allows that edit is therefore unclear.
- M6: spec:104 (cli-eval) requires "the safety flags in the brief" but never names them. AC-2.2 (spec:200) passes only `--suite`. An implementer must guess the flag set.
- M7: P1 (spec:159) and P2 (spec:160) give no explicit phase that adds a WC-4 contract for release-split, tdd, troubleshoot or init-lite. Their 3.1 rows report a non-contract file (INV-B:37, INV-B:222, INV-B:242; INV-A:55). AC-2.3 step 4 (spec:201 via spec:183) needs a contract. Read literally, P1's "every command in sections 3.1 and 3.2" would cover them, but P1's scope list does not.
- M8: spec:73 requires the report path to be "known before dispatch (WC-4)," but the workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (spec:92), and `<id>` is created at run time (INV-B:272). Workflow has no output flag, so the coordinator cannot give the path in the brief.

## Minor notes

- m1: spec:228 (D1 example) passes `--output .dev/troubleshoot/login/` to `/sc:troubleshoot`. spec:91 lists no output flag for troubleshoot, and INV-B:242 gives a default output directory. The example uses a flag the section 3 row does not name.

## Decisions

- Output path: the coordinator brief names `review/round1.md`, which I wrote. The README output table (`README.md:22-27`) lists `review/spec-panel.md` for task 5. I followed the brief and did not write a second file.
- Severity: a Medium finding is recorded with `severity` MAJOR and `blocking: false`, as the review-loop prompt allows ("a Medium finding goes under follow-up candidates even when its label is MAJOR").
- Blocking test: a finding is blocking only when a stated text contradicts another stated text or breaks a safety or security boundary, or when an acceptance check cannot pass as written. Overstated evidence (M2, M3, M4) and ambiguous scope (M5 to M8) are Medium.
- Layout: the Reviser brief sits above the final `verdict:` line, and `## Findings block` is the last section before it, so both placement rules hold.
- No follow-up issue is created. The loop's question to the user is left to the coordinator.

## Reviser brief

Blocking finding ids: F1, F2, F3, F4, F5, F6.

Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)", "anchor2": "In unattended mode the command writes `<output-dir>/return-contract.yaml`", "refs": ["WC-4", "3.1", "AC-1.4"], "claim": "WC-4 puts adversarial's contract at `<output-dir>/return-contract.yaml` while the 3.1 fix puts it at `<output>/adversarial/return-contract.yaml`, so the coordinator's known path and the 7.2 step 4 check disagree for the same run."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "a precise component prompt, not a bare topic; `--output <file>`", "anchor2": "the directory the coordinator passed (`--output` / `--output-dir`)", "refs": ["WC-4", "3.1", "AC-2.2"], "claim": "For tdd (and init-lite, whose row also passes `--output <file>`) WC-4 cannot write `<output-dir>/return-contract.yaml` because the value is a file, so the blocked contract AC-2.2 requires has no location the coordinator can open."}
{"id": "F3", "severity": "CRITICAL", "blocking": true, "category": "safety", "anchor": "the session may instead ask the coordinator once with the preamble's `ask` command", "anchor2": "stop with the halt recorded in the ledger and the contract as blocked", "refs": ["WC-3", "WC-2", "3.2 implement", "D2"], "claim": "WC-3 lets a coordinator answer a blocked implement Ruling and resume with that answer as a flag, which is the relayed Ruling D2 leaves to the user and qa.md:238 (quoted at INV-A:66) forbids."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file", "anchor2": "its report path is the WC-4 contract path", "refs": ["AC-0.4", "7.2 step 3", "WC-4"], "claim": "AC-0.4 says step 3 passes in P0, but step 3 requires the WC-4 contract path and its status, which P0 does not create, so the P0 gate cannot pass as written."}
{"id": "F5", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "What changes in the commands is limited to the worker contract in section 2", "anchor2": "Existing lines change only where section 3 names a defect fix", "refs": ["1.1", "SA-4", "3", "AC-3.1", "AC-3.3"], "claim": "Reading 1.1 as the scope bound skips the defect fixes section 3 and SA-4 require (roadmap, validate-roadmap, validate-tests, explain, business-panel, load), so AC-3.1 and AC-3.3 cannot pass."}
{"id": "F6", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "The only command changes are the small fixes in the last column.", "anchor2": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["3.1", "P1", "AC-1.1", "SA-1"], "claim": "3.1 gives brainstorm no change, but P1 and AC-1.1 require the --unattended flag and an Unattended mode section for every 3.1 command, so AC-1.1 fails for brainstorm."}
{"id": "M1", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "refs": ["AC-C1", "AC-C4", "SA-2"], "claim": "In grep -E, `\\|` is a literal pipe, so AC-C1 never matches real orca invocations and passes vacuously; AC-C4 has the same escaping."}
{"id": "M2", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "so a command run by a worker has the same tools as a command a person runs.", "refs": ["E2"], "claim": "No inventory line says anything about a worker's tool set; CAPS:161 says only that the worker is top-level, so the claim is inference presented as evidence."}
{"id": "M3", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "The only end-to-end proof is the PR #329 run", "anchor2": "Orca workers invoked `/sc:adversarial`, and that work landed as PR #329.", "refs": ["E3", "1.4", "UNVERIFIED 1"], "claim": "E3 cites a skill-direct return contract as evidence while 1.4 and UNVERIFIED 1 say no direct-route run was observed; the two statements conflict."}
{"id": "M4", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit", "refs": ["3.2 tasklist", "INV-A:14", "INV-B:314"], "claim": "The nesting-limit claim rests on an external doc quote and is stated as fact, while INV-B:210 and INV-B:314 mark subagent-to-agent spawning as UNVERIFIED."}
{"id": "M5", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "dispatch only inside an IronClaude checkout (hardcoded template path)", "anchor2": "Existing lines change only where section 3 names a defect fix", "refs": ["SA-4", "3.2 cli-portify", "AC-C5"], "claim": "The cli-portify checkout restriction changes an existing line but is not on SA-4's closed list of permitted fixes, so AC-C5 cannot be applied to it."}
{"id": "M6", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "`run` requires `--suite` and the safety flags in the brief, else blocked", "refs": ["3.2 cli-eval", "AC-2.2"], "claim": "The safety flags are never named, so an implementer must guess which flags make the run non-blocked."}
{"id": "M7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "The WC-4 contract in unattended mode", "anchor2": "7.2 passes with `--outcome succeeded`", "refs": ["P1", "P2", "AC-2.3", "3.1"], "claim": "No phase row names release-split, tdd, troubleshoot or init-lite as getting a WC-4 contract, yet AC-2.3 step 4 requires one for P2 commands."}
{"id": "M8", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "`.dev/tasks/to-do/<id>/return-contract.yaml`", "anchor2": "so the report path is known before dispatch (WC-4)", "refs": ["3.1 workflow", "WC-4", "2.3"], "claim": "The workflow package id is created at run time and workflow has no output flag, so the coordinator cannot state the contract path before dispatch as 2.3 requires."}
{"id": "m1", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "--unattended --output .dev/troubleshoot/login/", "refs": ["D1", "3.1 troubleshoot"], "claim": "The D1 example passes --output to /sc:troubleshoot, which no section 3 row names as a flag."}
```

verdict: FAIL
