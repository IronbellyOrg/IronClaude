review: 1 of 3

# Spec review, round 1: Orca worker contract (critique; focus: requirements, architecture)

candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
candidate sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
baseline: none (first review of the full document)
prompt: FIRST-REVIEW of `~/.claude/rules/prompts/document_review_loop_prompts.md` (sha256 ed219181156e47e6d70120730063e0b00081482d8a78b3d2633da188574ca829)
reviewer model used: claude-haiku-5-5
panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker active in every panel review
format: markdown, critique mode

## Run status (read before using the verdict)

- **One reviewer, not three.** The FIRST-REVIEW prompt calls for three fresh-context first reviews, the MERGE rule, and a VERIFY pass in a fresh context. This worker cannot start fresh-context reviewers or verifiers, so none of those ran. Every finding below is one reviewer's finding and is unverified. The coordinator must run two more first reviews, merge them, and run the VERIFY prompt over the blocking ids before the Reviser brief is used. Per the VERIFY rule, a reply with no `confirmed:` line confirms every finding.
- **Covered.** Read in full: the candidate (`spec`, 285 lines), `.dev/orca-command-refactor/README.md` (`README:N`), `command.md`, the review prompt file, and the three inventories: `inventory/commands-a.md` (`INV-A:N`, 120 lines), `inventory/commands-b.md` (`INV-B:N`, 323 lines), `inventory/orca-capabilities.md` (`CAPS:N`, 188 lines). I checked a sample of the candidate's citations into the inventories and CAPS against those files; the ones I checked matched, for example spec:65 against INV-A:95 and CAPS:159-161, spec:61 against CAPS:58-61, spec:59 against CAPS:44-45, and spec:76 against INV-A:76-83 and INV-B:292 (the last via spec:79's inventory references). I did not check the "43 commands in cmd/" count against the repository (see M11).
- **UNVERIFIED.** Every citation to a repository file outside `.dev/orca-command-refactor/` (for example `CLAUDE.md`, `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`) is UNVERIFIED, because this sandbox holds only the workspace copy. So is every guide-output line (`[G]`, `[H:...]`) the inventories quote; I checked those only as the inventories copied them. No blocking finding rests on an UNVERIFIED citation.
- **Citation keys.** `spec:N` = candidate line N; `INV-A:N`, `INV-B:N`, `CAPS:N`, `README:N` = the workspace files above.

## Mandatory artifact: Guard Condition Boundary Table

Triggered: the candidate has conditional logic (WC-2 gate resolution, WC-3 ask, WC-5 outcome mapping, WC-6 resume, WC-10 wait limit, WC-12 fence). The table below is complete under FR-10: every guard is listed, and the input classes not used are named with a reason. Each GAP row is a finding below (FR-8).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 failed or blocked test | spec:63 | Zero/Empty | 0-byte `return-contract.yaml` | neither failed nor blocked | "succeeded otherwise": a file that names no status maps to succeeded | GAP (M1) |
| WC-5 | spec:63 | Sentinel Value Match | `status: done` (outside the four values in spec:262) | neither | "succeeded otherwise" | GAP (M1) |
| WC-5 | spec:63 | One/Minimal | `status: succeeded` only | not failed or blocked | succeeded | OK |
| WC-5 | spec:63, spec:263 | Typical | `status: partial` | not failed or blocked | succeeded | OK (consequence in M2) |
| WC-5 with 7.2 step 3 | spec:63, spec:182 | Legitimate Edge Case: no file | no contract | no report exists | failed | OK |
| WC-4 with WC-6 | spec:62, spec:64 | Legitimate Edge Case: answered or retried run | re-run into a fresh directory | contract path changes | not stated | GAP (M3) |
| WC-2 flag | spec:60, spec:159 | Typical: flag absent in a section 3.1 brief | no `--unattended` | plain behaviour | section 2.3 requires the flag (spec:73) | GAP (B2) |
| WC-2 flag | spec:60, spec:146 | Zero/Empty flag | no `--unattended` | plain behaviour (SA-1) | stated | OK |
| WC-3 ask | spec:61, spec:200 | Legitimate Edge Case: ask timeout | timeout | resume or re-invoke ("or") | "may"; AC-2.2 needs one fixed outcome | GAP (M4) |
| WC-9 outward flag | spec:67 | Zero/Empty | no outward flag | outward default off | stated | OK |
| WC-9 with WC-2 | spec:88, spec:60, spec:67 | Legitimate Edge Case: `--remediate` under unattended | auto-accept | remediation runs | not classed as outward (WC-9) or blocked (WC-2) | GAP (M6) |
| WC-10 wait limit | spec:68 | Maximum/Overflow | one tool call of 6 minutes | must split into waits of at most 4 minutes | named only for cli-eval (spec:104) and pr-submit (spec:114) | GAP (M8) |
| WC-1 readiness | spec:59, CAPS:44-45 | Maximum/Overflow | 60 s readiness with an unanswered prompt | fails at `agent_readiness` | fallback is required to fire below the limit | OK |
| WC-12 fence | spec:70 | One/Minimal | `check` returns `consumer_fenced` | stop, no `worker_done` | stated | OK |

Input classes left out, one line each: Maximum/Overflow for WC-5 and WC-12 (no count is involved). Pipeline Dimensional Analysis is not triggered: the candidate's stages are control flow (Tasks, waves, settlement; spec:44-46, CAPS:92), not data whose count changes between stages.

## Findings: blocking

### B1. The SA-2 exception, AC-C1 and the P0 Orca sections contradict each other

- **Sentence.** An implementer who follows SA-2 (spec:147), which allows Orca to be named "as an example of a caller's question channel inside the contract file", and names `orca orchestration ask` in `src/superclaude/core/WORKER-CONTRACT.md`, builds a file that AC-C1 (spec:172) rejects. AC-C1 greps `src/superclaude/core` and exempts only `skills/ccsession-tag/`, so the common check fails in P0 (spec:158, spec:170).
- The same grep also rejects the Orca section P0 adds to `HOW-WE-WORK.md` (spec:158; SA-5 at spec:150). SA-2's exception covers only the contract file, so the routing guide has no permitted form at all.
- **Expert.** Wiegers (testability of the common checks); Whittaker (FR-2.3 sentinel collision: the exemption is a permitted token the check cannot tell from a violation).
- **Recommendation.** Make AC-C1 exempt the contract file and the routing-guide section by path, or state one rule that covers both core files and matches AC-C1.
- **Priority.** High. **Quality impact.** P0 cannot pass its common check, so no phase after P0 can start.

### B2. The ready tier (section 3.1) says no command changes, but section 2.3, P0, P1 and AC-1.1 require them

- **Sentence.** An implementer who follows section 3.1 ("These run as workers now", "The only command changes are the small fixes", spec:79) and runs the ten ready commands without `--unattended` builds workers that do not match section 2.3 (the brief must carry `--unattended`, spec:73) or the P0 check (spec:180 step 1 and spec:194, AC-0.4).
- P1 (spec:159) adds the `--unattended` flag to every command in sections 3.1 and 3.2. AC-1.1 (spec:195) requires every command in 3.1 and 3.2 to have a `## Unattended mode` section naming `return-contract.yaml`. Section 3 says changed commands gain that section (spec:76). Brainstorm (spec:84) and init-lite (spec:87) list the small fix as "None", so AC-1.1 cannot pass for them as the tables are written.
- P0 is "no command edits" (spec:158), yet its smoke runs follow 7.2 (spec:194), and 7.2 needs the flag.
- **Expert.** Wiegers (traceability from section 2.3 to section 3.1); Fowler (interface drift between phase and table).
- **Recommendation.** Either give the ready tier the `--unattended` flag and section in P0 and say so in 3.1, or define P0 smoke runs without the flag and say which checks then apply.
- **Priority.** High. **Quality impact.** The phase gate for P0 and P1 cannot be run from the text.

### B3. The fixed contract path in WC-4 does not fit the ready commands, so AC-0.4 and AC-1.2 cannot pass for them

- **Sentence.** An implementer who follows WC-4 (spec:62: `<output-dir>/return-contract.yaml`, known before dispatch) and the section 3.1 row for workflow (spec:92) finds that the workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (INV-B:272), where `<id>` is made by the command. The coordinator cannot know the path before dispatch, and no phase gives workflow an output directory. AC-0.4 step 3 (spec:182, spec:194) requires "the WC-4 contract path", so it cannot pass for workflow.
- cleanup-audit (spec:85; INV-A:42) writes `.claude-audit/pass<N>-summary.md` into a fixed directory and writes no contract. index-repo (spec:86; INV-A:53) writes `PROJECT_INDEX.md` and takes no output flag. The candidate adds neither a contract nor an output flag to either, yet AC-1.2 (spec:196) runs step 4 (spec:183) on every P1 command with `--unattended --output <dir>`, and P1 (spec:159) lists both.
- The two path rules also disagree for adversarial. spec:83 fixes its contract at `<output>/adversarial/return-contract.yaml`, while WC-4 (spec:62) puts the contract directly in `<output-dir>`. init-lite takes `--output <file>` (spec:87), so its "output directory" is a file, and WC-4 needs a directory.
- **Expert.** Adzic and Wiegers (acceptance criteria that cannot be satisfied by the rule they test); Newman (contract location as a service interface).
- **Recommendation.** Add an output directory and a contract write to workflow, cleanup-audit and index-repo, or move AC-0.4 and AC-1.2 to the commands that have one. Fix one path rule for adversarial and init-lite.
- **Priority.** High. **Quality impact.** The coordinator cannot read a contract at the path the brief names for these commands.

## Findings: Medium (follow-up candidates; not blocking; not in the Reviser brief)

- **M1. A zero-byte or status-less contract maps to success (WC-5).** Expert: Whittaker (FR-2.1, FR-2.3). spec:63 maps any report that does not say failed or blocked to `--outcome succeeded`. WC-4 (spec:62) writes a contract on every outcome, so a crash during the write leaves an empty file, and the Task then settles completed (CAPS:77). The wrong outcome needs no guess. Quality impact: a false success starts dependents. Recommendation: map an empty, unparseable, or unknown-status contract to `failed`. The `test -s` in 7.2 step 4 (spec:183) catches this only after `worker_done` has been sent.
- **M2. Partial output is settled as success, and nothing gates dependents on status.** Expert: Hohpe, Nygard. spec:63 and spec:263 map `partial` to succeeded. The Task settles completed (CAPS:77) and dependents appear in the ready view (CAPS:85). Orca does not start them (CAPS:92), but spec:73 only says the coordinator opens the report, not that it must wait for `succeeded` before starting a dependent. A coordinator that starts dependents from the ready view builds on partial output. Medium because it needs a coordinator that skips the read. Recommendation: state that dependents wait for a status of `succeeded`, or map `partial` to `failed`.
- **M3. An answered re-run may leave the coordinator with a stale blocked contract (sequence).** Expert: Fowler, Nygard. spec:61 lets the worker "re-invoke or resume the command with the answer as a flag". spec:62 fixes the report path before dispatch, and spec:64 says a command with no resume flag writes each run into a fresh output directory. A re-invoked run then writes elsewhere. The coordinator opens the pre-dispatch path and reads the first attempt's `status: blocked`, for a run that finished. Recommendation: say that the answered run writes to the same contract path and overwrites the blocked file, or that the coordinator re-reads after any `ask`. `--retry-of` (CAPS:116) has the same shape.
- **M4. The ask path is optional, so AC-2.2 is not a fixed gate (Adzic; sequence).** spec:61 says the worker "may" ask, and AC-2.2 (spec:200) expects `worker_done --outcome failed` with `status: blocked`. A conforming worker that takes the ask path ends differently, and step 2 (spec:181, `agentWait` never non-null) may also fail while it waits. Recommendation: pick one behaviour for blocked gates in the acceptance check, or make AC-2.2 accept both.
- **M5. The "ready today" label is asserted, not run (Wiegers, traceability).** spec:79 says the ten commands "run as workers now". spec:43 (section 1.4, gap 1) says no command has run end to end, and INV-B:323 says the verdicts come from reading. Several commands the table lists as ready are also rows in P2 (spec:160): reflect, release-split, tdd and troubleshoot. Troubleshoot's `--fix` offer (spec:91) and reflect's `--remediate` offer (spec:88) are gates the brief must keep off, and the P0 smoke run uses troubleshoot (spec:194). Recommendation: label the tier "ready, pending the P0 smoke run", and reconcile the P2 entries with it.
- **M6. Remediation auto-accept under unattended mode is not classified (Nygard, safety).** spec:88 says `--remediate` under `--unattended` should "follow the existing headless auto-accept rule". WC-2 (spec:60) lists only a default, a flag value, or blocked. WC-9 (spec:67) limits the rule to outward actions. So an auto-accepted remediation, which per spec:88 hands off to sc:workflow or task-builder, is neither blocked nor outward, and the candidate does not say whether it may edit product code (UNVERIFIED: the handoff reference is outside the sandbox). Recommendation: classify the auto-accept under WC-2 explicitly, or make `--remediate` resolve as blocked under `--unattended`.
- **M7. The nesting claim for tasklist is not computed, and a silent loss of the Agent tool is not covered (Newman, Nygard).** spec:122 says tasklist's reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, INV-A:14". INV-B:210 says Stage 10.5 dispatches N subagents, each of which runs reflect, and reflect Tier 2 runs adversarial (INV-A:35: 2-10 generator agents). That chain reaches depth 3 or deeper below the worker. INV-A:14 says that at the limit the Agent tool is withheld silently. spec:45 (section 1.4, point 3) says the limit is unproven, and WC-7 (spec:65) and the acceptance checks do not cover a silent loss. Recommendation: remove the claim or compute the depth; have the contract record how many fan-out agents actually ran; add a check.
- **M8. Several requirements have no acceptance check, and WC-10 is applied to two commands only (Wiegers, traceability).** WC-1 (spec:59), WC-6 (spec:64), WC-11 (spec:69, only save at AC-3.4, spec:207), WC-12 (spec:70) and SA-6 (spec:151) have no check that covers every command they bind. WC-10 (spec:68) is named only for cli-eval (spec:104) and pr-submit (spec:114). The candidate does not say whether other commands block one tool call for more than five minutes (for example cleanup-audit's waves, INV-A:42). Recommendation: add a requirement-to-check table, and an audit of long waits for each command.
- **M9. AC-C1 is case-sensitive and misses the uppercase form the guides use (Whittaker, FR-2.3).** spec:172 greps without `-i`. The guide text the candidate quotes writes `ORCA orchestration ask` (CAPS:60). A contract that uses that form passes AC-C1 while naming Orca. Recommendation: add `-i`, and match `orca-ide` too.
- **M10. The worker rules depend on an installed file with no precondition check (Newman, Hohpe).** spec:52 places the contract at `~/.claude/WORKER-CONTRACT.md`, installed by `superclaude install`, and each Unattended section points there. The candidate states no precondition. AC-1.1 (spec:195) is a static test of source, not of the installed file. A worker in a checkout with an older install gets no rules, and gates stall, which WC-2 exists to prevent. Recommendation: have the brief template check that the file is present, record its absence as blocked, and add a check.
- **M11. The "43 commands" total is not shown to be complete (Wiegers, scope).** spec:75 says "The 43 commands in `cmd/`". Each inventory lists its scope by hand (`INV-A:3`, `INV-B:3`), and neither shows a directory listing. The skill listing in this session also names `sc:graph`, `sc:impact` and `sc:issue`, which neither scope list contains. UNVERIFIED against the repository. Recommendation: list `src/superclaude/commands/`, reconcile against the 43, and classify any extra commands.

## Findings: minor notes (not graded above Medium; not in the Reviser brief)

- **N1.** spec:139 and spec:268 call `load` and `recommend` coordinator-side helpers (INV-B:65, INV-B:105 say the same), yet spec:105, spec:115 and phases spec:159-160 give them worker rows and work. Decide one.
- **N2.** WC-4 (spec:62) states as fact that Orca does not check the report file. UNVERIFIED item 3 (spec:274) says the spec assumes it. Mark the assumption in WC-4.
- **N3.** SA-5 (spec:150) updates both mirrored routing-guide copies. AC-0.2 (spec:192) checks one `cmp` and "the level-table test". Name both checks.
- **N4.** Non-goal 8 (spec:220) limits fixes to defects that stop a worker, but P3 (spec:161) fixes roadmap drift and the validate-tests target "regardless of Orca". Say which rule P3 follows.
- **N5.** P0 (spec:158) writes install-visible core files before AC-0.4 (spec:194) tests the decision, and spec:194 says a failure "reopens section 1". Consider running AC-0.4 before the core writes.
- **N6.** The cli-portify template path is hard-coded to the checkout (spec:105; INV-A:68). Section 5 keeps standalone behaviour unchanged, which is true, but the row should say the command still works only inside an IronClaude checkout.

## Coordinator actions

1. Run two more FIRST-REVIEW reviews with the first-review brief, then the MERGE rule.
2. Run the VERIFY prompt over B1, B2 and B3 and the merged blocking list, in a fresh context that sees only the candidate and the list.
3. Once, ask the user whether to open an issue for M1-M11 and N1-N6. This worker created none.

## Decisions

| Decision | Options | Rationale |
|---|---|---|
| Blocking grade | FIRST-REVIEW categories only, or command.md's broader "concrete wrong outcome" test | The FIRST-REVIEW categories apply, because the brief names that prompt. Under them M1 (false success) is Medium, not blocking: it is a wrong outcome but not a contradiction, a data-loss or safety risk, or a failed acceptance check. |
| Number of reviewers | Run three reviewers, or record one | No fresh-context reviewer tool is available here, so one reviewer is recorded and the run status says so. |
| Verdict | Withhold, or record FAIL | FAIL is recorded because a blocking finding is open. It stays FAIL until a VERIFY reply says otherwise. |
| Guard table | Full table, or "not triggered" | Triggered (conditional logic is present), so the full table is given. |

## Reviser brief

Blocking finding ids: **B1, B2, B3**. Do not start a revision until the VERIFY reply confirms these ids (this report confirms nothing itself).

Restated rule (section 6 of the review command, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on every added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not to be edited. No brief narrowed or widened the scope of this review.

verdict: FAIL
