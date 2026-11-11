# Adjudication of findings X1-X22

Inputs read: `.dev/orca-command-refactor/README.md`, `specs/orca-worker-contract-spec.md` (all 285 lines), `review/adj-input.md`, and the cited lines of the three inventories. Spec line numbers below refer to `specs/orca-worker-contract-spec.md`.

Test applied to each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is confirmed only if that sentence holds with no further assumption.

Limit: source files under `src/superclaude/` and Orca itself are not in this workspace, so any claim about them is UNVERIFIED here. No verdict below depends on one.

Result: 1 confirmed (X5), 1 unsure (X18), 20 rejected.

## Confirmed

### X5: confirmed
An implementer who follows the P1 row as written (spec:159) edits the 13 commands in its Commands column, and that is wrong because AC-1.1 (spec:195) fails P1 unless every command in sections 3.1-3.2 (37) has a `## Unattended mode` section naming `return-contract.yaml`.

The other reading fails too. An implementer who follows the P1 Scope cell and AC-1.1 writes that section in all 37 during P1. Section 2.1 (spec:52) says the section lists the command's own gate resolutions and report file. That is wrong for three reasons:
- implement, post-release and pr-submit are P4 rows (spec:109,113,114) whose gate resolutions depend on D2-D4, while spec:154 says Phases 1-3 need no user decision.
- pr-submit must get the section in P1 even though D3 (a), the recommended answer, makes it coordinator-only (spec:139,240).
- load must name `return-contract.yaml` although its row says it writes no report (spec:112).

Either reading produces a P1 that cannot both pass its check and stay inside its stated bounds. No assumption is needed; the texts conflict directly.

## Unsure

### X18: unsure
Step 3 of 7.2 (spec:182) blocks in `check --wait` for up to 900000 ms, and step 2 (spec:181) requires a `worker-show` at least every 5 minutes "while it runs". A coordinator that runs the steps one call at a time cannot satisfy both. The sentence holds only if the coordinator cannot run the two calls concurrently (for example a background wait), and nothing in the workspace settles that. The 900000 value is Orca's own guide line (`CAPS:63`). A one-line fix removes the doubt: a wait timeout of at most 240000 ms in a loop, or a statement that step 2 runs alongside step 3.

## Rejected

### X1: rejected
Section 1.1 (spec:16) is a summary sentence. SA-4 (spec:149) and the section 3 rows enumerate the defect fixes explicitly, so the implementer builds from those. Nothing wrong is built; the summary is loose wording.

### X2: rejected
The reflect row (spec:88) reuses a rule that already exists for `claude --print` and is limited to auto-fixable registers (`INV-B:109`). The brief column also says not to pass `--remediate`. D2 concerns the `/sc:implement` Ruling rule, not reflect's remediation handoff. Calling the auto-accept wrong needs the added premise that it counts as the self-approval D2 guards against.

### X3: rejected
The troubleshoot row's "Brief must pass" cell (spec:91) omits the `--depth deep` short-input STOP that exists today (`INV-B:239`), so "ready today" is slightly overstated. A stall needs a brief that combines `--depth deep` with a symptom under 10 words, which no stated text prescribes; AC-0.4 uses a real symptom with no depth flag. Worth a one-cell wording fix, not a blocker.

### X4: rejected
- Core files: P0 must add Orca prose to core files, but nothing requires that prose to contain a lowercase `orca orchestration|worktree|terminal|agent` invocation. The spec's own examples write `ORCA orchestration ...`, which the case-sensitive pattern does not match. AC-C1 (spec:172) is therefore a satisfiable constraint.
- Pipes: `\|` inside a table code span is the standard GFM escape for `|`. The same escape appears in AC-C4, AC-C5 and AC-0.3. The check fails only if the implementer pastes the raw table source into a shell.

### X6: rejected
`CAPS:155` itself is headed "Agent-tool subagents are not Orca workers, so the depth limit does not count them", so E4 matches its source. The remaining UNVERIFIED part (whether Orca limits subagents some other way) is stated at spec:45, and the design does not depend on it.

### X7: rejected
P0 adds the file to `KNOWN_CORE_FILES` (spec:158, AC-0.1), so it installs with the commands. The failure needs a partial or stale install, which is an added assumption.

### X8: rejected
AC-1.3 (spec:197) tests SA-3, that no `return-contract.yaml` appears without the flag. A print-mode run tests that validly. Interactive behaviour is covered separately by the manual check AC-2.5.

### X9: rejected
WC-7 (spec:65) says a command's own Agent-tool fan-out stays as it is. WC-8's splitting applies only to fan-out that needs Orca records, and D5 (a) repeats the rule. The cleanup-audit and tdd case is covered: their fan-out stays internal.

### X10: rejected
The rows at spec:100 and spec:104 are in "Needs a change", so the stated flag behaviour is what the implementer builds whether or not the flag exists today. `INV-A:44` names `--suite` and the safety flags for cli-eval; `INV-A:38` shows `--no-post-pr` against a default-on posting option. The "premise and 43-command scope need a re-check" part names no wrong build.

### X11: rejected
"None" sits in the "Other required change" column. The `--post-pr` / `--no-post-pr` behaviour is the row's gate-resolution cell, which is itself the required change. The two cells do not contradict.

### X12: rejected
The spec already records this as UNVERIFIED item 8 (spec:279) and assigns it: "Each phase's plan must resolve this before editing." It is a known open item with an owner, not a hidden gap.

### X13: rejected
P4's scope is "Apply the answers to D2-D4" (spec:162). If the answer to D3 is (a), applying it means no pr-submit change, which matches spec:240 and AC-4.3's "If D3 allows".

### X14: rejected
The tdd row (spec:90) names the nested `/task` "ask the user" lines (`sk/task/SKILL.md:49,114`) as resolving to blocked, so the outcome is required. Only the pass-down mechanism is left to the implementer, which is an under-specified detail, not a wrong build.

### X15: rejected
The misfire needs a person to paste and run a coordinator brief containing `--unattended`. That is an explicit opt-in by the person, and an added assumption.

### X16: rejected
The gap is in coordinator behaviour after a `blocked` or `partial` report. Section 2.3 (spec:73) has the coordinator open the report before acting, WC-3 and WC-6 cover the question and retry routes, and a coordinator program is non-goal 3. Nothing a command or contract implementer builds is wrong.

### X17: rejected
Missing acceptance coverage for some requirements is a test-coverage gap. It does not make an implementer build anything wrong, and several of the named items (WC-1, WC-3, WC-12) are owned by launch setup or the worker session, not by command edits.

### X19: rejected
The claim at spec:44 follows `CAPS:52` ("once `input_accepted`, a worker waiting ... is healthy") and `EVIDENCE.md:45` as quoted there. It is an evidence-strength point. Step 1 of the 7.2 live check in AC-0.4 and AC-2.2 tests it before anything depends on it.

### X20: rejected
The misfire needs a command that parses `--unattended` out of quoted prompt text. Nothing in the spec says to build that, so it is an added assumption about parsing.

### X21: rejected
Section 4 (spec:128) says these six are never dispatched and get no unattended mode, and AC-1.1 asserts they have no section. A wait happens only if a coordinator violates the spec by dispatching one.

### X22: rejected
AC-4.3 (spec:210) applies only to pr-submit. The pr-submit row (spec:114) already requires each iteration to stay under 4 minutes, which equals the 240 s limit. The 4-to-5-minute gap in WC-10's general wording never reaches a check that would fail.

```adj-v1
{"x": "X1", "verdict": "rejected", "reason": "Section 1.1 is a loose summary; SA-4 and section 3 enumerate the defect fixes, so nothing wrong is built."}
{"x": "X2", "verdict": "rejected", "reason": "The reflect row reuses an existing headless rule limited to auto-fixable registers, and calling it forbidden self-approval needs an added premise because D2 covers only the implement Ruling."}
{"x": "X3", "verdict": "rejected", "reason": "The troubleshoot brief cell omits the deep short-input STOP, but a stall needs a brief combining --depth deep with a symptom under 10 words, which no stated text prescribes."}
{"x": "X4", "verdict": "rejected", "reason": "P0's Orca prose need not contain the lowercase invocation pattern AC-C1 scans for, and the escaped pipes are standard table escaping that fails only if raw source is pasted."}
{"x": "X5", "verdict": "confirmed", "reason": "Following P1's 13-command list fails AC-1.1, which demands the section in all 37, while satisfying AC-1.1 forces D2-D4-dependent sections for the P4 commands and a contract mention in load during P1."}
{"x": "X6", "verdict": "rejected", "reason": "CAPS:155 states the same thing E4 does, the spec marks the remaining doubt UNVERIFIED in 1.4, and the design does not depend on it."}
{"x": "X7", "verdict": "rejected", "reason": "P0 installs the contract file through KNOWN_CORE_FILES, so the failure needs an assumed partial or stale install."}
{"x": "X8", "verdict": "rejected", "reason": "AC-1.3 tests only that no contract file appears without the flag, which a print-mode run tests validly; prompts are covered by AC-2.5."}
{"x": "X9", "verdict": "rejected", "reason": "WC-7 says a command's own Agent-tool fan-out stays as it is, so cleanup-audit and tdd fan-out is covered and is not split."}
{"x": "X10", "verdict": "rejected", "reason": "Both rows sit in the needs-a-change table, so the flag behaviour is what gets built whether or not the flags exist today, and the re-check request names no wrong build."}
{"x": "X11", "verdict": "rejected", "reason": "The 'none' is in the other-required-change column while the post-pr behaviour is the row's gate-resolution change, so the cells do not conflict."}
{"x": "X12", "verdict": "rejected", "reason": "The plugin mirror is already recorded as UNVERIFIED item 8 with the instruction that each phase plan resolves it before editing."}
{"x": "X13", "verdict": "rejected", "reason": "P4 applies the answers to D2-D4, so under D3 (a) it makes no pr-submit change, consistent with the decision text and AC-4.3."}
{"x": "X14", "verdict": "rejected", "reason": "The tdd row names the nested task ask-the-user lines as resolving to blocked, leaving only the pass-down mechanism to the implementer."}
{"x": "X15", "verdict": "rejected", "reason": "The misfire needs a person to paste and run a brief containing --unattended, which is an explicit opt-in and an added assumption."}
{"x": "X16", "verdict": "rejected", "reason": "This is a gap in coordinator guidance, which is a stated non-goal, and nothing a command or contract implementer builds from the text is wrong."}
{"x": "X17", "verdict": "rejected", "reason": "Missing acceptance checks are a coverage gap that does not cause a wrong build."}
{"x": "X18", "verdict": "unsure", "reason": "A coordinator running the steps one call at a time cannot poll every 5 minutes during a 15-minute blocking wait, but the conflict holds only if it cannot run the two calls concurrently, which the workspace does not settle."}
{"x": "X19", "verdict": "rejected", "reason": "The claim follows CAPS:52 and is an evidence-strength point that step 1 of the 7.2 live check tests in AC-0.4 and AC-2.2."}
{"x": "X20", "verdict": "rejected", "reason": "The misfire needs a command that parses the flag out of quoted prompt text, which the spec does not tell anyone to build."}
{"x": "X21", "verdict": "rejected", "reason": "Section 4 commands are never dispatched and get no unattended mode, so a wait needs a coordinator that violates the spec."}
{"x": "X22", "verdict": "rejected", "reason": "AC-4.3 applies only to pr-submit, whose row already requires each iteration under 4 minutes, so the WC-10 wording gap never reaches a failing check."}
```
