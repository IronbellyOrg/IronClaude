review: 1 of 3

# Spec-panel critique: Orca worker contract spec (review 1 of 3)

- Command: `/sc:spec-panel --mode critique --focus requirements,architecture`, FIRST-REVIEW prompt from `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before this review).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 286 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Baseline: none (first review; `baseline: missing` does not apply).
- Reviewer model: claude-haiku-5-5, one reviewer. `superclaude` is not installed in the sandbox, so `superclaude review panel resolve` and `review merge` did not run and no ledger was written.
- Coverage: the whole candidate (lines 1-286) was read. Inventory citations in the findings were checked against the inventory text read in this run (`CAPS`, `INV-A`, `INV-B`). Every anchor quoted below was verified byte-exact against the candidate with `grep -F`. Citations to `cmd/`, `sk/`, `refs/`, `.dev/evals/`, `.dev/codegraph-migration/`, `src/` and the README-listed evidence files are not in the sandbox and are UNVERIFIED here; where a finding rests on one, the finding says so.
- Citation keys: `spec:N` = candidate line N; `CAPS:N` = `inventory/orca-capabilities.md` line N; `INV-A:N` = `inventory/commands-a.md`; `INV-B:N` = `inventory/commands-b.md`; `README:N` = `README.md`.
- Panel for focus requirements + architecture (per command.md lines 91-106 and the Focus Areas section): Wiegers (lead), Adzic, Cockburn; Fowler (lead), Newman, Hohpe, Nygard; Whittaker (active in every panel review). Crispin, Gregory and Hightower do not run for these focus areas.

**Verdict: FAIL.** Four blocking findings are open (F1-F4). Twelve Medium findings are listed under follow-up candidates and do not block.

## Summary

The spec is internally well organized. Its inventory-derived counts check out (10 ready, 27 needs-change, 6 coordinator-only sum to 43; the per-inventory splits 5/13/3 and 5/14/3 match `INV-A:73` and `INV-B:278`), and the Orca facts it relies on match the quoted `CAPS` lines. The blocking problems are four places where the spec contradicts itself: the outcome rule that defaults to success (F1), the flag that a brief must carry before the flag exists (F2), the evidence base for the direct route (F3), and an acceptance check that claims a proof its steps do not perform (F4).

## Requirements analysis (Wiegers, Adzic, Cockburn; Whittaker attacks)

**F1. CRITICAL, blocking.** Expert: Whittaker (FR-2.1 Zero/Empty, FR-2.3 Sentinel Collision), Wiegers.
- Issue: WC-5 maps `failed` and `blocked` to `--outcome failed`, then says `--outcome succeeded` "otherwise" (`spec:63`). "Otherwise" catches a contract whose `status` is absent, misspelled (`Partial`) or empty, and sends success. Section 2.2 only defines a four-value vocabulary (`spec:262`), which does not close the "otherwise" branch.
- Grading sentence: an implementer who follows WC-5 as written sends `--outcome succeeded` for a contract whose status is absent or misspelled, and that is wrong because a valid `worker_done` settles the Task automatically (`CAPS:77`), so the coordinator treats undelivered work as completed.
- Attack: contract `status: Partial` gives `succeeded`; contract present but `status` line missing gives `succeeded`; no contract gives `failed` (`spec:63`) but an empty file, which `test -s` in `spec:183` would reject, is not addressed by WC-5.
- Recommendation: send `succeeded` only for the literal values `succeeded` and `partial`. Every other case, including a missing or unreadable contract, an empty file, or an unknown `status`, sends `failed` and names the reason in the body.
- Priority: High. Quality impact: high (silent false success on the coordinator side).

**F2. MAJOR, blocking.** Expert: Wiegers, Cockburn.
- Issue: section 2.3 requires every brief to state "the exact command line including `--unattended`" (`spec:73`). Phase P0 runs three ready commands "invoked directly" (`spec:158`), and AC-0.4 uses `/sc:troubleshoot "<real symptom>"` with no flag (`spec:194`). The `--unattended` flag is added only in P1 (`spec:159`), and the ready-today table lists no such flag (`spec:81-92`).
- Grading sentence: an implementer who follows section 2.3 as written puts `--unattended` in the P0 brief, while AC-0.4 runs the command without it, so the two stated texts give different command lines for the same P0 run.
- Recommendation: state in section 2.3 that `--unattended` applies from the phase that adds it, and that P0 briefs use the section 3.1 flags only. Alternatively move the flag requirement into P1.
- Priority: High. Quality impact: high (the P0 evidence would not test the contract the spec defines).

**F3. MAJOR, blocking.** Expert: Wiegers (traceability of evidence), Fowler.
- Issue: section 1.4 says "The only end-to-end proof is the PR #329 run" (`spec:43`) and UNVERIFIED item 1 says no direct-route run was observed (`spec:272`). But E3 cites a return contract with `invocation_method: "skill-direct"` as evidence that Orca workers ran `/sc:adversarial` (`spec:23`, citing `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10`). `INV-A:13` quotes the same contract as a direct-route worker run. A direct-route run on record therefore contradicts "the only" end-to-end proof and "no such run was observed".
- Grading sentence: an implementer who reads section 1.4 as written concludes no direct-route worker run is on record, while E3 cites one, so the decision's evidence base disagrees with itself and the reader cannot tell whether Phase 0 is testing a new route or repeating a proven one.
- Caveat: the cited contract is UNVERIFIED here (not in the sandbox). The contradiction is between two texts of the spec and the inventory quote, so it holds without reading that file.
- Recommendation: either cite the P3 run as the direct-route precedent and reword section 1.4 and UNVERIFIED item 1 to say it is a single prior run not checked in this review, or drop the direct-route claim from E3.
- Priority: High. Quality impact: high (the decision's strength is stated inconsistently).

**F4. MAJOR, blocking.** Expert: Adzic (Given/When/Then, acceptance criteria), Cockburn.
- Issue: AC-0.4 says the no-wrapper rule (WC-7) is "verified in the step-5 transcript" (`spec:194`). Step 5 searches the transcript only for `AskUserQuestion` (`spec:184`). No step checks whether the command ran inside an Agent-tool subagent.
- Grading sentence: an implementer who runs AC-0.4 as written passes steps 1-3 and 5-7 and then records the check as passed, although nothing in the criterion tests WC-7, so the one rule that section 1.4 names as P0's purpose is never checked.
- Recommendation: add an explicit step with a pass condition, for example: the first tool call that runs the command is the command itself (no Agent or Task tool call before it), read from the step-5 transcript.
- Priority: High. Quality impact: high (this is the only test of the direct-route decision).

**F9. MEDIUM (follow-up).** Expert: Wiegers (traceability), Whittaker. The reflect ready verdict ignores default-on writes that INV-B names: a folder move in Wave 7 and a tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` (`INV-B:114`). The spec lists only `--no-promote` (`spec:88`), and WC-11 (`spec:69`) bans two workers writing the same file. A slug collision between two reflect workers would clobber the tracked file. Recommendation: name the tracked file in section 3.1 and say whether the brief must pass a unique slug. Quality impact: medium.

**F10. MEDIUM (follow-up).** Expert: Whittaker (FR-2.5 Accumulation). WC-3 resumes a timed-out `ask` by message ID and "never creates a duplicate" (`spec:61`), with no upper bound or abandonment rule. The default ask timeout is UNVERIFIED (`CAPS:68`; `spec:281`). A worker waiting on an unanswered question has no stated exit. Recommendation: state a bound (for example one hour) after which the worker writes `status: blocked` with the pending question and ends. Quality impact: medium.

**F14. MEDIUM (follow-up).** Expert: Adzic (measurability of checks). AC-C1 (`spec:172`) escapes its alternation as `\|` inside a single-quoted `grep -E` pattern. Read from the raw Markdown, `\|` is a literal pipe in `grep -E`, so the pattern matches nothing and the check passes on any tree. The rendered table shows the intended alternation, so the defect depends on which text is copied. Recommendation: write the alternation without the escape in the source and add a positive control (the check must match a known-bad fixture). Quality impact: medium (a guard against SA-2 could pass vacuously).

**F16. MEDIUM (follow-up).** Expert: Cockburn (every row has an acceptance check). Several section 3 "other required change" entries have no acceptance check in section 7.3: the cli-portify hardcoded template path (`spec:105`), the business-panel frontmatter move (`spec:102`) and the load usage line (`spec:112`). AC-3.3 covers validate-tests only (`spec:206`). Recommendation: add one check per entry or state why none is needed. Quality impact: low to medium.

## Architecture analysis (Fowler, Newman, Hohpe, Nygard)

**F5. MEDIUM (follow-up).** Expert: Fowler (interface and ownership). WC-4 says the contract is written in "the directory the coordinator passed" (`spec:62`). WC-6 says a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean" (`spec:64`). Section 2.3 gives the brief the directory, but no rule says who creates a new one on retry. Under one reading the command creates a subdirectory, which takes the contract away from the path the coordinator recorded; under the other the coordinator must always pass a fresh path, which the spec never says. Recommendation: state that the coordinator creates a new `--output` for every `--retry-of` attempt, and that the command writes only inside it. Quality impact: medium.

**F6. MEDIUM (follow-up).** Expert: Nygard (failure modes, timing). WC-1 requires any prompt to "fall back on its own well inside the readiness limit (default 60 s)" (`spec:59`). The same line cites the evidence that the 45-second limit failed and that a fallback above about 45 seconds fails again ("above about 45 s it fails again", `spec:59`). "Well inside" is not a number. A fallback at 50 seconds satisfies the text and fails the cited evidence. Recommendation: replace "well inside" with a number, for example a fallback of at most 30 seconds, and cite the evidence for it. Quality impact: medium.

**F7. MEDIUM (follow-up).** Expert: Newman (service boundaries), Fowler (nesting). The tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (`spec:122`). Section 1.4 item 3 says the fan-out has "no proven limit, but no proof of none either" (`spec:45`). `INV-B:210` marks nested spawning as UNVERIFIED, and `INV-B:314` repeats it. The claim in `spec:122` also omits that reflect spawns its own agents, which adds a second layer. Recommendation: reword the row to "UNVERIFIED; needs an AC-2 run" and add a tasklist check to Phase 2. Quality impact: medium.

**F8. MEDIUM (follow-up).** Expert: Nygard (unclassified gates), Wiegers. The troubleshoot row calls it ready with no `--fix` (`spec:91`). The inventory says read-only probes run "under an execution gate" (`INV-B:243`, citing `cmd/troubleshoot.md:101`), but the same inventory's gate column names only `--fix` (`INV-B:49`). WC-2 (`spec:60`) requires every gate to be listed in section 3, so an unlisted execution gate has no resolution. Recommendation: have P0's first run confirm the gate is absent, or list it in section 3. Quality impact: medium (the P0 smoke test could stall on it).

**F11. MEDIUM (follow-up).** Expert: Hohpe (message delivery). WC-5 requires `worker_done` "exactly once" (`spec:63`), but no rule covers a `worker_done` send that fails or times out. The inventory notes that every orchestration mutation accepts `--retry-request <id>` (`CAPS:117`), which the spec does not mention. Without it, a retry can duplicate or drop the completion. Recommendation: require the worker to send `worker_done` with a `--retry-request` id and to check the outcome with `request-show` before retrying. Quality impact: medium.

**F12. MEDIUM (follow-up).** Expert: Nygard (liveness). Section 2.3 covers only the happy path after `worker_done` (`spec:73`). AC-2 and section 7.2 detect a stall through `agentWait` alone (`spec:181`). The inventory says absence never authorizes retry or release (`CAPS:125`) and that a stall needs positive proof: exited liveness, or a transcript whose final turn sent no `worker_done` (`CAPS:126`). The spec has no rule for a worker that is neither waiting on a question nor finished. Recommendation: add a coordinator rule that uses the `CAPS:126` proof before any retry or release. Quality impact: medium.

**F13. MEDIUM (follow-up).** Expert: Fowler (interface closure). WC-4 says the contract "carries at least:" a set of fields (`spec:62`). The schema is open, has no version field, and has no rule for extra fields from commands that already write a contract (workflow, reflect, brainstorm). AC-0.4's check reads only `status` and `command` (`spec:183`). A coordinator cannot validate a contract against a fixed interface. Recommendation: add `contract_version` and close the field list, with per-command extensions named in an `extensions` block. Quality impact: medium.

**F15. MEDIUM (follow-up).** Expert: Whittaker (FR-2.4 Sequence), Hohpe. WC-5 maps an audit with a FAIL verdict to `succeeded` (`spec:63`), so Orca settles the Task as completed (`CAPS:77`). A dependent Task whose dependency is `completed` becomes ready (`CAPS:86`, `CAPS:88`). The spec relies on the coordinator reading the report before it starts a dependent (`spec:73`), and nothing enforces that order. Recommendation: map a FAIL verdict to `failed` for the Task, or add a rule that dependents wait for the coordinator's read of the contract. Quality impact: medium to high.

## Guard Condition Boundary Table (mandatory: the spec has guard conditions)

Every guard in the spec is enumerated (seven guards). Input classes with no meaning for a guard are left out with a one-line reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | spec:63 | Zero/Empty | no contract, or empty file | no contract: true; empty file: not stated | "no report exists" gives failed; empty file not addressed | GAP (F1) |
| WC-5 outcome mapping | spec:63 | One/Minimal | `status: partial` | true | succeeded | OK |
| WC-5 outcome mapping | spec:63 | Typical | `status: succeeded` | true | succeeded | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status` absent, `Partial`, `done` | falls to "otherwise" | succeeded | GAP (F1) |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | audit verdict FAIL with status succeeded | true | succeeded; Task settles completed | GAP (F15) |
| WC-1 readiness fallback | spec:59 | Typical | fallback 30 s | true | passes (cited evidence) | OK |
| WC-1 readiness fallback | spec:59 | Boundary | fallback 45-60 s | ambiguous | "well inside" undefined | GAP (F6) |
| WC-2 gate resolution | spec:60 | Legitimate Edge Case | gate not listed in section 3 (troubleshoot execution gate) | true | no resolution stated | GAP (F8) |
| WC-3 ask timeout | spec:61 | Zero/Empty | flag omitted | default unknown (`CAPS:68`) | resume the same ID, no bound | GAP (F10) |
| WC-3 ask timeout | spec:61 | Maximum/Overflow | question never answered | true | no abandonment rule | GAP (F10) |
| WC-6 retry-of | spec:64 | Legitimate Edge Case | retry with the first attempt's directory | true | fresh dir or resume; who creates the dir not stated | GAP (F5) |
| WC-10 wait split | spec:68 | Boundary | single tool call at 4 min vs 5 min heartbeat | 4 < 5 | split into waits of at most 4 min | OK |
| WC-12 consumer_fenced | spec:70 | Sentinel Value Match | check returns `consumer_fenced` | true | stop, no `worker_done` | OK |

Left out, with the one-line reason: WC-1 Zero/Empty (no fallback means no prompt, which WC-1's first clause already forbids); WC-10 and WC-12 Zero/Empty and Maximum (the guard takes no count or quantity input); WC-6 Typical (no fixed value in the text).

Pipeline Dimensional Analysis: not triggered. The spec describes no multi-stage data flow whose item count changes; the outcome mapping changes a status, not a count. No Quantity Flow Diagram is required.

Auto-suggestion (advisory, not forced): `--focus correctness` would fit. The spec has numeric thresholds (`spec:59`, `spec:68`, `spec:182`) and a four-state outcome mapping (`spec:63`). Its mandatory correctness outputs (State Variable Registry) are not produced here because the focus was not requested.

## Follow-up candidates (Medium and minor; not blocking; not revised)

- F5 (WC-4/WC-6 directory ownership), F6 (WC-1 "well inside"), F7 (tasklist nesting claim), F8 (troubleshoot execution gate), F9 (reflect default writes), F10 (unbounded ask), F11 (lost `worker_done` send), F12 (stall handling), F13 (open contract schema), F14 (AC-C1 escaped pipe), F15 (FAIL audit settles completed), F16 (section 3 entries without acceptance checks).
- Minor notes: UNVERIFIED items 3, 5 and 10 (`spec:274`, `spec:276`, `spec:281`) are correctly flagged; the spec's own UNVERIFIED list is accurate about what it could not check.
- Per the review loop, the session that ran this review asks the user once whether to open an issue for these. This worker creates none.

## Process notes

- Layout: the prompt asks for the Reviser brief just above the final `verdict:` line and for the Findings block to be the last section. Both cannot hold, so the Reviser brief sits directly above the Findings block and `verdict: FAIL` is the last line.
- Panel: one reviewer; `superclaude review panel` not run (not installed).
- Scope check: the spec's `src/superclaude/...` references are maintainer-facing (for example the proposed `src/superclaude/core/WORKER-CONTRACT.md`, `spec:52`). The CLAUDE.md rule allows that form, so no finding is raised on it. The installed-path lines in the spec's `## Unattended mode` wording point to `~/.claude/WORKER-CONTRACT.md` (`spec:52`), which is the form the rule requires.
- Nothing outside the output file was written. The candidate was not edited and no further review was started.

## Reviser brief

Blocking finding ids: F1, F2, F3, F4.

Restated rule (review loop step 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not in this brief and must not be revised.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "other", "anchor": "--outcome succeeded` otherwise, including `partial`", "refs": ["WC-5", "CAPS:77"], "claim": "An absent, misspelled or empty contract status is sent as --outcome succeeded, so the coordinator treats undelivered work as completed."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "the exact command line including `--unattended` and every flag section 3 lists as required", "anchor2": "7.2 live check on `/sc:troubleshoot", "refs": ["2.3", "AC-0.4", "P0"], "claim": "Section 2.3 requires --unattended in every brief, but P0 and AC-0.4 run the ready commands without it because the flag does not exist until P1."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "The only end-to-end proof is the PR #329 run", "anchor2": "invocation_method: \"skill-direct\"", "refs": ["1.4", "E3", "UNVERIFIED-1"], "claim": "Section 1.4 says PR #329 is the only end-to-end proof and no direct-route run was observed, while E3 cites a skill-direct worker contract."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "verified in the step-5 transcript", "anchor2": "search the transcript for `AskUserQuestion`", "refs": ["AC-0.4", "7.2 step 5", "WC-7"], "claim": "AC-0.4 claims the no-wrapper rule is verified in step 5, but step 5 checks only for AskUserQuestion, so WC-7 is never tested."}
{"id": "F5", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "anchor": "is the directory the coordinator passed", "anchor2": "writes each run into a fresh output directory so a re-run starts clean", "refs": ["WC-4", "WC-6", "2.3"], "claim": "Nothing says who creates the fresh output directory on retry, so the contract path the coordinator recorded can be lost."}
{"id": "F6", "severity": "MEDIUM", "blocking": false, "category": "other", "anchor": "well inside the readiness limit (default 60 s)", "anchor2": "above about 45 s it fails again", "refs": ["WC-1"], "claim": "'Well inside' has no number, and the cited evidence fails above about 45 seconds."}
{"id": "F7", "severity": "MEDIUM", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker", "refs": ["tasklist row", "1.4-3", "INV-B:210"], "claim": "The tasklist row states the nesting limit is respected, while section 1.4 says no limit is proven and the inventory marks it UNVERIFIED."}
{"id": "F8", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "anchor": "Under `--unattended`, the `--depth deep` short-input STOP", "anchor2": "no `--fix` | `REPORT.md`", "refs": ["WC-2", "troubleshoot row"], "claim": "The troubleshoot row is ready, but an execution gate the inventory mentions has no WC-2 resolution."}
{"id": "F9", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "anchor": "`--no-promote` when the coordinator owns folder moves", "refs": ["reflect row", "WC-11", "INV-B:114"], "claim": "The reflect row omits a default-on tracked file write and folder move that two workers could collide on."}
{"id": "F10", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "anchor": "On an `ask` timeout it resumes the same message ID and never creates a duplicate.", "refs": ["WC-3", "CAPS:68"], "claim": "A timed-out ask resumes indefinitely, with no bound or abandonment rule."}
{"id": "F11", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "anchor": "The worker sends `worker_done` exactly once from its own top-level session.", "refs": ["WC-5", "CAPS:117"], "claim": "No rule covers a failed or timed-out worker_done send, so completion can be lost or duplicated."}
{"id": "F12", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "anchor": "After `worker_done`, the coordinator opens the report file", "refs": ["2.3", "7.2 step 2", "CAPS:125-126"], "claim": "No coordinator rule handles a worker that neither waits on a question nor finishes."}
{"id": "F13", "severity": "MEDIUM", "blocking": false, "category": "other", "anchor": "carries at least: `status`", "refs": ["WC-4", "AC-0.4"], "claim": "The contract schema is open and unversioned, so a coordinator cannot validate it against a fixed interface."}
{"id": "F14", "severity": "MEDIUM", "blocking": false, "category": "unpassable-check", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "refs": ["AC-C1", "SA-2"], "claim": "Read raw, the escaped alternation makes the grep match nothing, so AC-C1 passes on any tree."}
{"id": "F15", "severity": "MEDIUM", "blocking": false, "category": "other", "anchor": "including an audit whose verdict is FAIL (the audit itself succeeded)", "refs": ["WC-5", "2.3", "CAPS:77"], "claim": "A FAIL-verdict audit settles its Task as completed, and dependents can start before the coordinator reads the report."}
{"id": "F16", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "anchor": "dispatch only inside an IronClaude checkout (hardcoded template path)", "refs": ["section 3.2 cli-portify", "section 7.3"], "claim": "Some section 3 other-required-change entries have no acceptance check."}
```

verdict: FAIL
