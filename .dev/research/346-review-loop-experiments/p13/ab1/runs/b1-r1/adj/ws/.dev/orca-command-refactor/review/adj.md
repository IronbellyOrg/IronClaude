# Adjudication of findings X1-X16

Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited as `SPEC:N`).
Inventories: `inventory/commands-a.md` (`INV-A:N`), `inventory/commands-b.md` (`INV-B:N`), `inventory/orca-capabilities.md` (`CAPS:N`).

Test applied to each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is confirmed only when that sentence holds with no further assumption.

Limits: only the README, the spec and the three inventories exist in this workspace. Every `src/`, `EVIDENCE.md`, `CLAUDE.md` and Orca source citation in the spec is UNVERIFIED here. Nothing was run.

Result: 3 confirmed (X7, X10, X11), 10 rejected, 3 unsure (X9, X13, X14). X10 and X11 are one defect; X9 and X13 are one question.

## Confirmed

### X7: confirmed
Sentence: An implementer who follows WC-4 as written writes the contract to `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory passed as `--output` / `--output-dir` (`SPEC:62`, repeated at `SPEC:76`), and that is wrong because the spec's own rows give `/sc:tdd` and `/sc:init-lite` a file-valued `--output <file>` (`SPEC:87`, `SPEC:90`), so the path is a child of a file and cannot exist.

It holds without assumption:
- AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and requires a contract with `status: blocked` (`SPEC:200`). No stated location exists for that file.
- The adversarial row fixes a different path, `<output>/adversarial/return-contract.yaml` (`SPEC:83`), while 7.2 step 3 requires "the WC-4 contract path" (`SPEC:182`).
- The workflow row puts the contract at `.dev/tasks/to-do/<id>/return-contract.yaml` (`SPEC:92`) and the brief passes only `--handoff none`. Section 2.3 requires the report path to be known before dispatch (`SPEC:73`).

Putting the contract beside the file (in its parent directory) would be a reasonable fix, but the spec does not say it.

### X11: confirmed
Sentence: An implementer who follows the load row and the Decisions table as written changes only load's usage line and gives it no report file (`SPEC:112`, `SPEC:159`, `SPEC:265`), and that is wrong because AC-1.1 asserts that every command in sections 3.1-3.2, which includes load, has a `## Unattended mode` section naming `return-contract.yaml` (`SPEC:195`), so the P1 test fails.

The reverse reading fails too: following AC-1.1 gives load a section naming a contract the row says it never writes. `SPEC:76` ("every changed command also gains the section") and the P1 scope ("`--unattended` accepted by every command in sections 3.1 and 3.2", `SPEC:159`) conflict with "usage line only" in the same way.

### X10: confirmed (same defect as X11)
The AC-1.1 against load row / Decisions conflict holds exactly as in X11.

The finding's extra consequence does not hold as written. WC-5 maps "no report exists" to `failed` (`SPEC:63`) only for a worker's own Task, and the load row says load is never its own Task (`SPEC:112`). The verdict rests on the AC-1.1 conflict alone.

## Unsure

### X9 and X13: unsure
Sentence attempted: An implementer who follows the cli-eval row builds a gate that requires "`--suite` and the safety flags in the brief, else blocked" (`SPEC:104`), and it is wrong because the set of safety flags is undefined.

- True part: the spec never lists the flags, and AC-2.2 exercises only the missing-`--suite` case (`SPEC:200`).
- Why not confirmed: the row cites `sk/sc-cli-eval-protocol/SKILL.md:128-153`, and `INV-A:44` says the run pipeline confirms "the exact invocation and safety flags (S:135-146)". The term points at an existing definition in the command's own skill.
- Why not rejected: that file is not in the workspace, so whether those lines give a determinate set that can be "required in the brief" is UNVERIFIED.

### X14: unsure
Sentence attempted: An implementer who follows the tasklist row makes no nesting change ("none", `SPEC:122`), and that is wrong because the nested reflect fan-out fails.

- True part: the row's support is `INV-A:14`, a quote from an external docs URL. `INV-B:211` marks nested spawning for this exact case UNVERIFIED, and `INV-B:215` recommended running the reflect fan-out at the worker's top level. The spec's UNVERIFIED list (`SPEC:271-285`) omits it.
- Why not confirmed: the row is wrong only if nesting actually fails, which cannot be decided from the workspace. The AC-2.3 happy-path run (`SPEC:201`) would expose it.

## Rejected

### X1: rejected
- The reflect row tells the brief to pass no `--remediate` (`SPEC:88`). Auto-accept is reached only through tasklist Stage 10.5 (`SPEC:122`).
- WC-9 covers outward actions only: push, PR, GitHub post, install, provision, paid run (`SPEC:67`). Calling the remediation an action that needs brief authorization requires assuming what it does. `INV-B:109` limits the existing auto-accept to auto-fixable registers.
- The trigger is not changed. SA-6 keeps the `claude --print` rule and adds `--unattended` as a second way in (`SPEC:151`).

### X2: rejected
- WC-1 is owned by "Launch setup, not commands" (`SPEC:59`), so no command change is built from it.
- A check exists: 7.2 step 1 passes only on `state: ready` (`SPEC:180`).
- The evidence cell carries the numbers: 60 s default, passes with a 30 s fallback, fails above about 45 s.

### X3: rejected
- True part: the inventories quote `EVIDENCE.md:45` only as "worker-start returned after 34s, `state: ready, stage: input_accepted`" (`CAPS:49`, `INV-A:13`), so "and answered" in E2 (`SPEC:22`) is unsupported by the quoted text and UNVERIFIED here.
- It is a parenthetical in an evidence cell. Nothing is built from it, and E2's claim (a worker is a top-level session) also rests on `CAPS:161`.

### X4: rejected
- E3 claims only that Orca workers invoked `/sc:adversarial` and the work landed (`SPEC:23`).
- Section 1.4(1) narrows that claim itself: it proved the nested route, not the direct one (`SPEC:43`). P0 smoke runs AC-0.4 are scheduled to close the gap (`SPEC:194`).
- This is a disclosed limit, not two opposite uses, and no build step depends on it.

### X5: rejected
- The pr-submit row is the operative text: confirm each poll-plus-sleep iteration stays under 4 minutes (`SPEC:114`). WC-10 requires a split if one does not (`SPEC:68`), and AC-4.3 checks 240 s (`SPEC:210`).
- "Wait splitting" in D3(b) (`SPEC:241`) is a loose label for that row and yields the same build.
- The difference from `INV-B:95` is a stated re-reading with its own citation and an UNVERIFIED item (`SPEC:283`).
- It applies only under the non-recommended option D3(b).

### X6: rejected
The re-read and validator claims (`SPEC:11`, `SPEC:285`) cannot be reproduced from this workspace, which is true. That is a provenance limit. No implementer builds anything from those sentences.

### X8: rejected
The row states the count: "one layer below the worker" (`SPEC:122`), against the three-layer limit quoted at `INV-A:14`. The claim that no layer count is given is false as written. Whether the nesting works is X14.

### X12: rejected
- WC-10 has a trigger (over 5 minutes) and a target (at most 4 minutes) (`SPEC:68`). AC-4.3 applies only to pr-submit (`SPEC:210`).
- The pr-submit row already requires each iteration under 4 minutes (`SPEC:114`, `SPEC:283`), so an implementer following the row meets AC-4.3.
- The 4 to 5 minute gap in WC-10's general wording produces no wrong build for any command the spec checks.

### X15: rejected
- AC-C1 sits in a markdown table cell (`SPEC:172`), where `\|` is the escape for a literal pipe.
- The same cell writes the shell pipe before `grep -v` as `\|`, and AC-C4 and AC-C5 do the same (`SPEC:175-176`). Read raw, those commands would not run at all, so the backslashes are table escaping, not regex text.
- The rendered command uses plain `|` alternation and matches Orca calls.

### X16: rejected
- R1 itself says the call-site enforcement was not traced and is presumed, marked UNVERIFIED (`SPEC:33`, from `CAPS:103`). The limit is disclosed in place.
- The depth-1 rule and the refusal code are quoted at `CAPS:97-99`.
- R2-R5 reject the alternative independently, and WC-8 forbids the calls either way (`SPEC:66`).
- The finding misreads UNVERIFIED item 5, which is about `task-create` (`SPEC:276`).

```adj-v1
{"x": "X1", "verdict": "rejected", "reason": "The brief passes no --remediate, WC-9 covers only outward actions, and SA-6 keeps the claude --print trigger and adds the flag beside it, so the defect needs an assumption about what remediation edits."}
{"x": "X2", "verdict": "rejected", "reason": "WC-1 is owned by launch setup, is checked by 7.2 step 1 (state: ready), and its evidence cell gives the 30 s and 45 s numbers, so no command is built wrongly from it."}
{"x": "X3", "verdict": "rejected", "reason": "The word 'answered' is unsupported by the quoted EVIDENCE.md:45 text, but it is an evidence-cell parenthetical that nothing is built from, and E2 also rests on CAPS:161."}
{"x": "X4", "verdict": "rejected", "reason": "E3 claims only that workers invoked the command, and section 1.4(1) discloses that the run proved the nested route and schedules AC-0.4 to close the gap, so nothing is built from a contradiction."}
{"x": "X5", "verdict": "rejected", "reason": "The pr-submit row, WC-10 and AC-4.3 agree on iterations under 4 minutes with a split if needed, and D3(b)'s 'wait splitting' is a loose label for that row under a non-recommended option."}
{"x": "X6", "verdict": "rejected", "reason": "The re-read and validator claims are unreproducible here, which is a provenance limit and not text an implementer builds from."}
{"x": "X7", "verdict": "confirmed", "reason": "WC-4 puts the contract at <output-dir>/return-contract.yaml under the passed directory, but tdd and init-lite take --output <file> and AC-2.2 requires a contract from that tdd run, so the stated path cannot exist; adversarial and workflow rows also fix other paths."}
{"x": "X8", "verdict": "rejected", "reason": "The row does state the count, one layer below the worker against the three-layer limit at INV-A:14, so the claim is false as written."}
{"x": "X9", "verdict": "unsure", "reason": "The spec never lists the safety flags, but the row cites SKILL.md:128-153 where INV-A:44 says they are confirmed, and that file is not in the workspace to check whether the set is determinate."}
{"x": "X10", "verdict": "confirmed", "reason": "AC-1.1 requires load to have an Unattended mode section naming return-contract.yaml while its row and the Decisions table give it a usage-line fix only and no report, so the P1 test cannot pass; the WC-5 consequence does not hold because load is never its own Task."}
{"x": "X11", "verdict": "confirmed", "reason": "Following the load row and Decisions table (usage line only, no report file) fails AC-1.1, which asserts every section 3.1-3.2 command has an Unattended mode section naming return-contract.yaml."}
{"x": "X12", "verdict": "rejected", "reason": "AC-4.3 applies only to pr-submit, whose own row already requires each iteration under 4 minutes, so the 4 to 5 minute gap in WC-10's general wording produces no wrong build."}
{"x": "X13", "verdict": "unsure", "reason": "Same question as X9: the flags are not listed in the spec, and whether the cited SKILL.md:135-146 defines a determinate set cannot be checked in this workspace."}
{"x": "X14", "verdict": "unsure", "reason": "The 'none' change rests on an external docs quote while INV-B:211 marks nested spawning UNVERIFIED and INV-B:215 recommended top-level fan-out, but the row is wrong only if nesting actually fails, which cannot be decided here."}
{"x": "X15", "verdict": "rejected", "reason": "The backslash-pipe is markdown table-cell escaping, as the same cell's shell pipe before grep -v and AC-C4 and AC-C5 show, so the rendered regex uses real alternation."}
{"x": "X16", "verdict": "rejected", "reason": "R1 itself marks the call-site enforcement as untraced and UNVERIFIED, the depth rule and refusal code are quoted at CAPS:97-99, and R2-R5 and WC-8 stand without it."}
```
