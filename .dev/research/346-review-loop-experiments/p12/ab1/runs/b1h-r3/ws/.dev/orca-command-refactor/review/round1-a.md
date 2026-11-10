review: 1 of 3

# Spec-panel critique: Orca worker contract spec (review 1 of 3)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (no `--re-review` and no `--baseline`; first review of the full document)
- reviewer model: claude-haiku-5-5
- scope: requirements and architecture focus; Whittaker adversarial probing (always active); Guard Condition Boundary Table (triggered by the spec's conditional logic, see its section below); Pipeline Dimensional Analysis (not triggered, see its section)
- coordinator steps not run here: this worker is one reviewer. The three first reviews, the MERGE rule, and the VERIFY prompt (fresh context, candidate plus finding list only) belong to the coordinator. The blocking findings below are unverified until that VERIFY pass runs.

## Citation legend
- `spec:N` = line N of the candidate file above (checked by reading it).
- `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/orca-capabilities.md`.
- `INV-A:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`; `INV-B:N` = line N of `.dev/orca-command-refactor/inventory/commands-b.md`.
- `src/...`, `.dev/codegraph-migration/...`, `.dev/evals/...` and `~/.claude/...` paths named in the spec are outside this sandbox. Any claim that rests only on them is marked UNVERIFIED.

## Summary
- Blocking findings: 7 (B1 to B7). Verdict FAIL.
- Non-blocking findings: 20 (M1 to M20), all graded Medium or lower; the heading label on some (M6, M11, M14, M16 to M20) reads MINOR. None of them is in the Reviser brief.
- Quality metrics (0-10): Clarity 6, Completeness 6, Testability 5, Consistency 4. The consistency score is low because the standalone-behaviour rule (SA-1) and the contract rules contradict several rows.
- The disposition counts reconcile: 43 = 21 + 22 = 10 ready + 27 needing change + 6 coordinator-only (spec:75-76, spec:83-92, spec:99-125, spec:132-137); per inventory, A is 5/13/3 (INV-A:73) and B is 5/14/3 (INV-B:278). This tally was checked and holds.

---

=== REQUIREMENTS ANALYSIS ===

### B1 (CRITICAL, blocking). The standalone-behaviour rule is contradicted by two rows
- Issue: SA-1 says that without `--unattended` every prompt and default stays as it is today (spec:146). The roadmap row replaces the default-on "Resume? [Y/n]" prompt with an explicit flag and says "resume only when passed" with no `--unattended` qualifier (spec:118). The save row says to write only per-session keys and never the single-owner keys, again with no qualifier (spec:119). WC-11 limits the single-owner exclusion to unattended mode (spec:69), so the two texts disagree. SA-4 allows only defect fixes outside additive edits (spec:149). The roadmap and save changes are not named as defect fixes there (only "roadmap and validate-roadmap drift" is named).
- Grading sentence: An implementer who follows the roadmap row as written builds `/sc:roadmap` that starts fresh without asking when an earlier session exists, and that is wrong because SA-1 (spec:146) requires the prompt to stay for a person in a plain session.
- Second instance: an implementer who follows the save row builds `/sc:save` that stops writing `pm_context`, `last_session` and `next_actions` in a plain session, which breaks `/sc:load` and `/sc:pm` resume (spec:119 against spec:146).
- Expert: Wiegers (traceability and contradictions). Priority: High. Impact: High (every standalone user of two commands).
- Recommendation: gate both changes on `--unattended`, or name them as SA-4 defect fixes and state that the standalone behaviour is preserved (for example, keep the prompt and make only the worker path resume-by-flag).

### B2 (CRITICAL, blocking). WC-3 lets a coordinator answer any gate, which contradicts the spec's own three-way rule and the implement Ruling rule
- Issue: WC-2 says each gate resolves one of three ways (a default, a flag, or blocked) (spec:60). WC-3 adds a fourth path: the worker may ask the coordinator and then "re-invoke or resume the command with the answer as a flag" (spec:61). The implement row blocks on a halt and keeps the Ruling rule (spec:109). D2(a) recommends keeping that rule because another agent's message is not acceptance (spec:234), and the spec cites that rule as `refs/qa.md:238` (spec:109, CAPS and INV-A:66). D4(a) says outward authorization needs the user's own words, but WC-3 needs no quoting (spec:245 against spec:61).
- Attack (Whittaker, sentinel collision, see section below): a free-text coordinator answer is turned into a flag. WC-3 does not say which flag a free answer maps to.
- Grading sentence: An implementer who follows WC-3 as written asks the coordinator at the implement Ruling gate, resumes with the coordinator's reply as the Ruling flag, and the halt is cleared; that is wrong because `refs/qa.md:238` (cited at spec:109) says another agent's message is not acceptance, and WC-3 has no exception for it.
- Expert: Nygard (failure and control path), Wiegers (contradicting rules). Priority: High. Impact: High (safety rule).
- Recommendation: exclude safety and authorization gates from WC-3 (implement Ruling, post-release and pr-submit authorizations, cli-eval safety flags), and say which flag a coordinator answer maps to, or drop the relay for these gates until D2 and D4 are decided.

### B3 (MAJOR, blocking). WC-5 reports a FAIL audit as `succeeded`, and no contract field carries the verdict
- Issue: WC-5 says `--outcome succeeded` for "an audit whose verdict is FAIL" (spec:63). WC-4 lists the contract fields `status`, `command`, `report_path`, `artifacts` and `blocked_question` and has no verdict field (spec:62). The verdict is therefore only in the body of `worker_done`, which WC-5 requires as prose ("The first sentence of the body states the report's status and verdict", spec:63). The spec cites the Orca rule "Never encode failure only in prose" (CAPS:73, from `[G]` lines 88-90). The spec breaks that rule for audits.
- Grading sentence: An implementer who follows WC-5 builds a coordinator that unblocks dependent Tasks when `worker_done --outcome succeeded` arrives, and that is wrong because the audit's FAIL verdict is only in prose and the coordinator's gate cannot read it (spec:63 with spec:62; CAPS:73).
- Expert: Fowler (interface), Whittaker (divergence attack, see section below). Priority: High. Impact: High (dependents run after a failed audit).
- Recommendation: add `verdict` to the WC-4 contract (required for audit-type commands), and make the coordinator gate on it, not on prose. Keep `succeeded` only for the run, not for the audit result.

### B4 (MAJOR, blocking). A contract with a missing or unrecognised `status` is reported as `succeeded`
- Issue: WC-5 maps "`--outcome succeeded` otherwise" (spec:63). WC-4 requires `status` to be one of four values (spec:62). The spec does not say what happens when `status` is absent, misspelled, or holds another value (for example a command's own legacy status word, INV-B:272 for workflow).
- Attack (Whittaker, zero/empty, see section below): a worker writes a contract with no `status` key because its command predates the contract. The rule yields `succeeded`.
- Grading sentence: An implementer who follows the "otherwise" rule in WC-5 reports `worker_done --outcome succeeded` for a contract with no `status`, and that is wrong because WC-4 makes `status` required (spec:62), so a missing status is a failed contract.
- Expert: Whittaker (lead on this attack), Wiegers. Priority: High. Impact: Medium-high.
- Recommendation: map missing, unparseable or unknown `status` to `failed`, and say so in WC-5.

### B5 (CRITICAL, blocking). Two contract paths for the same adversarial output
- Issue: WC-4 says the contract is `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (spec:62). The adversarial row fixes the path as `<output>/adversarial/return-contract.yaml` (spec:83). The coordinator "knows the report path before dispatch" and opens it (spec:73), so the two rows give it different files.
- Grading sentence: An implementer who follows WC-4 writes the adversarial contract at `<output>/return-contract.yaml`, and the coordinator following the row opens `<output>/adversarial/return-contract.yaml`, finds nothing, and per WC-5 records the worker as `failed` ("no report exists", spec:63) when the run succeeded; the two texts contradict each other (spec:62 against spec:83).
- Expert: Fowler (interface contract). Priority: High. Impact: Medium (false failures, and the wrong file may be read later).
- Recommendation: choose one rule (either the WC-4 path or an explicit per-command subdirectory listed in WC-4), and make section 3 use only that rule.

### B6 (MAJOR, blocking). Acceptance check AC-C1 cannot pass once P0 lands
- Issue: AC-C1 greps `src/superclaude/core` as well as commands, skills and agents (spec:172). It excludes only `ccsession-tag` (spec:172). SA-2 allows Orca text in the contract file as "an example of a caller's question channel" (spec:147). SA-5 requires an Orca section in `HOW-WE-WORK.md`, which is also under core (spec:150), and P0 adds the contract to core (spec:158). An Orca section or a contract example of the form `orca orchestration ask` would therefore match AC-C1 in P0 while the spec says it is allowed.
- Grading sentence: An implementer who writes the P0 files as SA-2 and SA-5 allow runs AC-C1 as written and gets matches in `src/superclaude/core`, so the common check fails although the content is permitted; the check cannot pass as written (spec:172 against spec:147, spec:150, spec:158).
- Expert: Crispin (testability). Priority: High. Impact: Medium (blocks P0 gate; forces ad hoc exceptions).
- Recommendation: exclude `src/superclaude/core/WORKER-CONTRACT.md` and the routing-guide Orca section from AC-C1 by name, and keep the command and skill scope.

### B7 (MAJOR, blocking). AC-0.4 step 4 cannot pass for the P0 ready commands
- Issue: step 4 requires a YAML file with `status` in four values and a `command` key (spec:183). AC-0.4 says step 4 "uses the command's existing report file" (spec:194). The existing workflow contract, as listed at INV-B:272, has `status`, `plan_path` and `reflect_report_path`, and no `command` key. The existing troubleshoot report is `REPORT.md`, which is markdown (INV-B:49). The check as written fails for both.
- Grading sentence: An implementer who runs step 4 on `/sc:workflow --handoff none` as written hits `assert d['command']` against a contract that has no `command` key (INV-B:272), so P0 cannot pass its own acceptance check; the spec says the same check applies (spec:183 against spec:194).
- Expert: Crispin. Priority: High (blocks the phase that tests the decision). Impact: Medium.
- Recommendation: define step 4 for each P0 command separately: for workflow, check `status` only and state that `command` arrives in P1; for troubleshoot, check that `REPORT.md` exists and is non-empty.

---

=== ARCHITECTURE ANALYSIS ===

### M1 (MAJOR, Medium). The evidence on direct-route runs conflicts within the spec
- Issue: E3 cites a direct run, `invocation_method: "skill-direct"` in a return contract, as evidence (spec:23). Section 1.4 says the only proof is the PR #329 run, which used an Agent-tool subagent, and that "it proves the nested route, not the direct route" (spec:43). INV-A:13 also reads the `skill-direct` contract as direct. The 3.1 "ready" verdict for adversarial rests on "proven in PR #329 run" (spec:83, INV-A:35). Both claims cannot hold.
- Expert: Wiegers (evidence). Priority: Medium. Impact: Medium (the "ready today" list depends on it).
- Recommendation: either cite the `skill-direct` contract as direct evidence and drop the "no direct-route run exists" statement, or mark it UNVERIFIED and remove "proven" from the adversarial row.

### M2 (MAJOR, Medium). Scope is understated: section 1.1 says commands change only through the contract
- Issue: section 1.1 says "What changes in the commands is limited to the worker contract in section 2" (spec:16). Section 3 adds a new `--resume` flag to cli-portify (spec:105), tool additions to explain (spec:108), frontmatter moves in business-panel (spec:102), a roadmap flag-surface change (spec:118), and a validate-tests target change (spec:125). The reader is misled about the size of the change.
- Expert: Fowler (interface surface). Priority: Medium. Impact: Medium (review scope).
- Recommendation: restate 1.1 to cover interface drift and defect fixes, citing SA-4 (spec:149).

### M3 (MAJOR, Medium). Certainty overstated for the report-path behaviour
- Issue: WC-4 says "Orca does not check the file, so the coordinator opens it" (spec:62). CAPS:79 says Orca's handling of the file is UNVERIFIED, and UNVERIFIED #3 says "the spec assumes it does not" (spec:274). The design works either way (the coordinator opens the file), but the requirement states as fact what the spec later calls an assumption.
- Expert: Wiegers. Priority: Low-Medium. Impact: Low.
- Recommendation: write "Orca's handling of the file is UNVERIFIED; the design does not depend on it" in WC-4.

### M4 (MAJOR, Medium). The live check asks for two timings that cannot both run
- Issue: step 2 needs `worker-show` at least once every 5 minutes while the worker runs (spec:181). Step 3 is a single `check --wait` with `--timeout-ms 900000` (spec:182), a 15-minute blocking wait. The step order does not say how the coordinator runs the 5-minute polls during a 15-minute block.
- Expert: Crispin. Priority: Medium. Impact: Low (test procedure).
- Recommendation: use `check --wait` with a timeout under 5 minutes in a loop with `worker-show` between calls.

### M5 (MAJOR, Medium). Split threshold for long waits differs between WC-10 and AC-4.3
- Issue: WC-10 splits a step only when it blocks "for longer than 5 minutes" and sets the split size at 4 minutes (spec:68). A 4.5-minute single call is therefore allowed by the first sentence. AC-4.3 requires "no single tool call exceeds 240 s" (spec:210), which is 4 minutes. The two texts disagree in the 4-to-5-minute band. The heartbeat cadence is also hard-coded as "every 5 minutes" (spec:68), while CAPS:130 says the cadence comes from the dispatch preamble, not from a guide.
- Attack (Whittaker, divergence): a 270-second poll passes WC-10 and fails AC-4.3.
- Expert: Whittaker, Nygard (heartbeat). Priority: Medium. Impact: Low.
- Recommendation: use one threshold (240 s) in WC-10, and read the heartbeat cadence from the preamble.

### M6 (MINOR, Medium). AC-C1 escapes its alternation in the raw file
- Issue: the raw text of AC-C1 writes `\|` inside the ERE alternation and before `grep -v` (spec:172). The markdown table escape renders this as `|`, but a copy of the raw text into a shell gives a literal `|` in the regex (ERE `\|` is a literal pipe) and a file argument `|` for the first grep, so the check matches nothing.
- Expert: Crispin. Priority: Medium. Impact: Medium (SA-2 check silently passes).
- Recommendation: write the command in a code block with plain `|` and `-E` alternation, and test it on a file with a known `orca orchestration` line.

### M7 (MAJOR, Medium). Tasklist and reflect: an unrecorded reversal and an unverified nesting claim
- Issue: the tasklist row says "Other required change: none", and that the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit", citing INV-A:14 (spec:122). INV-A:14 cites documentation not available here (UNVERIFIED). INV-B:314 marks whether a subagent can spawn agents as UNVERIFIED. INV-B:295 recommends dropping `--remediate` from Stage 10.5; the spec does not record the reversal. Under `--unattended`, the reflect row makes `--remediate` follow the headless auto-accept rule (spec:88), so Stage 10.5 would accept remediation without a person. That auto-accept policy is not in the Decisions table or among D1 to D5, and it differs from troubleshoot's Tier 3 rule that needs an explicit user acceptance (INV-B:239, UNVERIFIED for the nesting question).
- Expert: Nygard (failure modes of nested spawning), Cockburn (who accepts remediation). Priority: Medium. Impact: Medium.
- Recommendation: record the reversal in Decisions and add an entry in D-list. Add the nested-spawn question to UNVERIFIED, or drop `--remediate` from Stage 10.5 as INV-B:295 recommends.

### M8 (MAJOR, Medium). Contract versioning and vocabulary are not set for commands that already have a contract
- Issue: WC-4 says commands with a contract "keep their fields and add the missing ones" (spec:62). It fixes a four-value status vocabulary and no version field. INV-B:272 names the workflow contract as "contract 1.1". Its status values are not listed in the inventory (UNVERIFIED against the source file). A coordinator cannot tell which contract version it has read, and adding fields to 1.1 while changing the status vocabulary breaks compatibility without a bump.
- Expert: Newman (evolution and compatibility). Priority: Medium. Impact: Medium.
- Recommendation: add a `contract_version` field in WC-4, and state how a 1.1 contract is read (its existing status values mapped to the four-value set).

### M9 (MAJOR, Medium). Two channels for one question: `blocked_question` and a pending `ask`
- Issue: WC-2(c) writes the question into the contract as `blocked_question` (spec:60, spec:62). WC-3 sends the same question through `ask` (spec:61). The spec does not say which one the coordinator answers, or whether both are sent.
- Expert: Hohpe (message channels). Priority: Medium. Impact: Low-Medium (duplicate or lost questions).
- Recommendation: pick one channel per gate. A blocked outcome with `blocked_question` is the default, and `ask` is used only where WC-3 allows it.

### M10 (MAJOR, Medium). Cli-portify keeps an installed-skill path to src/
- Issue: the cli-portify skill reads `src/superclaude/examples/release-spec-template.md` (INV-A:45, INV-A:68). CLAUDE.md forbids a primitive from naming a `src/superclaude/...` path. P2 edits cli-portify (spec:160) and the row only limits the command to an IronClaude checkout (spec:105). The spec neither fixes the path nor records it as an exception.
- Expert: Fowler (dependency direction). Priority: Medium. Impact: Medium (breaks installed use).
- Recommendation: fix the lookup in P2 using the installed path, or list the exception with its reason.

### M11 (MINOR, Medium). Layering: worker-side `ask` is wired into command text
- Issue: SA-2 says commands carry no Orca call, and the only allowed mention is in the contract file (spec:147). WC-3 places the `ask` in the worker session, which is the right layer. The coordinator brief template (P0, spec:158) is not specified, so the wiring between brief, contract and `ask` is not testable.
- Expert: Fowler. Priority: Low. Impact: Low.
- Recommendation: specify the brief template fields in P0, or move it to a test fixture.

---

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Each attack uses the template: "I can break this specification by **[attack]**. The invariant at **[location]** fails when **[condition]**. Concrete attack: **[scenario]**."

- B2 (sentinel collision, FR-2.3): I can break this specification by **sentinel collision**. The invariant at **spec:61 (WC-3, "answer as a flag")** fails when **the coordinator's reply is free text that matches a flag name or a yes/no token**. Concrete attack: troubleshoot's `--fix` gate (INV-B:49) blocks with "[yes / no]"; the coordinator replies "yes"; the worker re-invokes with "yes" as the flag, which the spec does not map to `--fix`; a reply of "--fix" turns remediation on. Before: `--fix` off. After: `--fix` on, with no person's acceptance. Severity: CRITICAL (see B2).
- B3 (divergence, FR-2.2): I can break this specification by **divergence between outcome and verdict**. The invariant at **spec:63 (WC-5)** fails when **the audit verdict is FAIL and status is succeeded**. Concrete attack: a reflect run writes `status: succeeded` with a FAIL verdict in REPORT.md; the outcome is `succeeded`; the coordinator unblocks the next Task. Before: dependents wait. After: dependents run on a failed audit. Severity: MAJOR (see B3).
- B4 (zero/empty, FR-2.1): I can break this specification by **zero-value status**. The invariant at **spec:63 ("otherwise succeeded")** fails when **the contract has no `status` key**. Concrete attack: a command predating the contract writes `{command: ...}` only; WC-5 yields `succeeded`. Before: a missing status is a failure. After: `worker_done --outcome succeeded`. Severity: MAJOR (see B4).
- M9 (accumulation, FR-2.5): I can break this specification by **unbounded ask loop**. The invariant at **spec:61 (WC-3)** fails when **the coordinator never answers and the timeout is repeatedly resumed**. Concrete attack: the worker resumes the same message ID at each timeout with no cap; `agentWait` is null (healthy, CAPS:52) so no alarm fires; the Task stays dispatched indefinitely. Before: a bounded wait. After: an unbounded wait. Severity: MAJOR (see M9 and the Nygard note below).

---

=== EXPERT NOTES (by expert) ===

- Wiegers: B1 (contradictions), M1 (evidence), M3 (certainty). Acceptance coverage (M12) below.
- Adzic: the examples in AC-2.2 (spec:200) are good Given/When/Then cases for the two gate types. Missing an example for the WC-3 relay path (see B2) and for a contract with no `status` (see B4).
- Cockburn: no use case covers the coordinator's next step after a blocked worker. Section 2.3 (spec:72-73) says only "the coordinator opens the report file, then releases or reuses the worker". Blocked, failed and partial outcomes each need a stated next action. See M12.
- Fowler (lead): B5 (path), M2 (scope), M10 (installed path), M11 (brief template).
- Newman: M8 (contract versioning).
- Hohpe: M9 (two channels).
- Nygard: B2 (control path), M5 (heartbeat cadence), M7 (nesting and auto-accept), M9 (unbounded wait).
- Whittaker: the four attacks above.
- Crispin: B6, B7, M4, M6, and M13 below.

### M12 (MAJOR, Medium). Requirements without an acceptance check, and no next step for `blocked`
- Issue: WC-1 (spec:59), WC-3 (spec:61), WC-6 (spec:64) and WC-12 (spec:70) have no entry in section 7 (spec:172-210). WC-7 is checked only in AC-0.4 (spec:194). The coordinator's next step after `blocked` (re-dispatch with `--retry-of`, answer, or stop) is not stated, and WC-6's fresh directory means a re-run discards the partial output.
- Expert: Wiegers (traceability), Cockburn (use case). Priority: Medium. Impact: Medium.
- Recommendation: add one check per uncovered WC row, and a next-step table for blocked, failed and partial outcomes.

### M13 (MAJOR, Medium). Standalone regression is sampled, not tested
- Issue: SA-1 applies "on every phase" (spec:146, spec:142). The only checks are AC-1.3 on two commands (spec:197) and a manual check on two commands (spec:203). Thirty-odd commands change under P1 to P3, and none has an automated standalone test.
- Expert: Crispin. Priority: Medium. Impact: Medium.
- Recommendation: add a static test that runs each changed command's default path against a golden snapshot of its prompts and defaults, or a per-command check of its `## Unattended mode` gate.

### M14 (MINOR, Medium). Partial plus a blocked question
- Issue: WC-5 maps `partial` to `succeeded` (spec:63). WC-4 lets a contract carry `status: partial` and `blocked_question` together (spec:62). The spec does not say which wins. This is a legitimate edge case that the outcome rule does not cover.
- Expert: Whittaker (edge). Priority: Low. Impact: Low.
- Recommendation: state that a `blocked_question` makes the outcome `failed` regardless of status.

### M15 (MAJOR, Medium). A follow-up from the coordinator has no defined effect beyond stopping on `consumer_fenced`
- Issue: WC-12 says a worker runs `check` at checkpoints and stops only on `consumer_fenced` (spec:70). It does not say what a normal follow-up does (incorporate, reply, ignore). FR-9 applies: the behaviour for a follow-up is blank.
- Expert: Wiegers. Priority: Medium. Impact: Medium.
- Recommendation: state that a follow-up is answered in the worker's report, or is queued for the next Task.

### M16 (MINOR, Medium). Output directory not writable
- Issue: WC-4 says the contract is written "including stops before any other output exists" (spec:62). It does not say what happens if `<output-dir>` cannot be created or written. WC-5 then reports `failed` ("no report exists", spec:63), which is the safe direction, but the spec should say so.
- Expert: Nygard. Priority: Low. Impact: Low.
- Recommendation: state the fallback (`failed`, with the reason in the worker_done body).

### M17 (MINOR, Medium). `--unattended` quoted in specification text
- Issue: D1 makes the flag the switch (spec:228). The spec does not say whether a flag inside quoted content counts. The command.md rule (quoted content is not a flag) applies only to spec-panel. A quoted spec that mentions `--unattended` would switch the mode on in a command that reads it.
- Expert: Whittaker (sentinel). Priority: Low. Impact: Low-Medium.
- Recommendation: state the quoting rule for every command, or pass the switch only from the brief's argument list.

### M18 (MINOR, Medium). The `--retry-of` path discards the blocked run's answer
- Issue: after a blocked outcome, the coordinator re-dispatches with `--retry-of` (CAPS:116). WC-6 writes each run into a fresh directory, so the answer that resolved the gate is not carried over unless the brief repeats it. This is an interaction of WC-3, WC-6 and the retry path, and the spec does not state it.
- Expert: Cockburn (use case), Whittaker (sequence). Priority: Low. Impact: Low.
- Recommendation: state that a retry brief carries the answer as an explicit flag, and that the fresh directory is the one the coordinator names.

### M19 (MINOR). The brief template has no content
- Issue: P0 proposes "a coordinator brief template listing the section 3.1 flags" (spec:158), and section 2.3 lists its contents (spec:73). The template itself is not drafted, so it cannot be checked.
- Expert: Fowler. Priority: Low.
- Recommendation: include the template in P0 as a fixture that the test file checks.

### M20 (MINOR). `pr-submit` is classed two ways
- Issue: section 3.2 counts pr-submit among the 27 needing change (spec:114). D3(a) recommends coordinator-only (spec:240), and section 4 lists the six coordinator-only commands without it (spec:132-137, spec:139). The count is unaffected, but the disposition is unclear.
- Expert: Wiegers. Priority: Low.
- Recommendation: mark pr-submit as "needs change if D3(b) is chosen; otherwise coordinator-only" in both places.

---

=== GUARD CONDITION BOUNDARY TABLE ===

Trigger: the spec has conditional logic, threshold checks and boolean guards (spec:61, 63, 68, 70). The table is therefore produced. Responsibility: Nygard (lead), Crispin (completeness), Whittaker (attacks). Rows cover the input classes that apply to each guard. Classes left out are listed below the table with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--outcome` rule (WC-5) | spec:63 | Zero/Empty | no contract, no report | `failed` | "no report exists" gives `failed` | OK |
| `--outcome` rule (WC-5) | spec:63 | One/Minimal | `status: partial`, no question | `succeeded` | "including `partial`" gives `succeeded` | OK (see M14 for partial plus question) |
| `--outcome` rule (WC-5) | spec:63 | Typical | `status: succeeded` | `succeeded` | stated | OK |
| `--outcome` rule (WC-5) | spec:63 | Sentinel Value Match | `status` absent, or not one of four values | unset | "`succeeded` otherwise" gives `succeeded` (B4) | GAP (B4, blocking) |
| `--outcome` rule (WC-5) | spec:63 | Legitimate Edge Case | `status: succeeded`, audit verdict FAIL | `succeeded` | no verdict field exists (B3) | GAP (B3, blocking) |
| `--outcome` rule (WC-5) | spec:63 | Legitimate Edge Case | `status: partial` with `blocked_question` set | unset | rule does not cover it (M14) | GAP (M14, Medium) |
| `--unattended` switch (WC-2) | spec:60, spec:51 | Zero/Empty | flag absent | standalone | SA-1 (spec:146) | OK |
| `--unattended` switch (WC-2) | spec:60 | One/Minimal | flag alone on a gated command | gate blocked | row says blocked (spec:97-125) | OK |
| `--unattended` switch (WC-2) | spec:60 | Typical | flag plus required flags | proceeds | section 3 rows | OK |
| `--unattended` switch (WC-2) | spec:228 (D1) | Sentinel Value Match | flag inside quoted spec text | unset | not stated (M17) | GAP (M17, Medium) |
| `--unattended` switch (WC-2) | spec:60 | Legitimate Edge Case | command with no gate (analyze) | no-op | stated at spec:159 | OK |
| Contract path (WC-4) | spec:62 | Typical | `<output-dir>/return-contract.yaml` | written | stated | OK |
| Contract path (WC-4) | spec:83 | Legitimate Edge Case | adversarial, `<output>/adversarial/...` | written at other path | contradicts WC-4 (B5) | GAP (B5, blocking) |
| Contract path (WC-4) | spec:62 | Zero/Empty | output dir cannot be created | contract cannot be written | not stated (M16); `failed` by WC-5 | GAP (M16, Medium) |
| Wait threshold (WC-10) | spec:68 | Legitimate Edge Case | single call of 4.5 minutes | split? | WC-10 allows; AC-4.3 forbids (M5) | GAP (M5, Medium) |
| Wait threshold (WC-10) | spec:68 | One/Minimal | single call of 4 minutes | no split | stated | OK |
| `consumer_fenced` (WC-12) | spec:70 | Zero/Empty | `check` returns empty | continue | CAPS:67: empty is not fencing | OK |
| `consumer_fenced` (WC-12) | spec:70 | Typical | normal follow-up returned | effect unset | not stated (M15) | GAP (M15, Medium) |
| `consumer_fenced` (WC-12) | spec:70 | Sentinel Value Match | `consumer_fenced` returned | stop, no `worker_done` | stated | OK |
| `ask` timeout (WC-3) | spec:61 | Zero/Empty | timeout omitted | default unknown | UNVERIFIED (spec:281, CAPS:68) | GAP (UNVERIFIED, Medium via M9) |
| `ask` timeout (WC-3) | spec:61 | Maximum/Overflow | repeated timeouts, no reply | resume without cap | not stated (M9) | GAP (M9, Medium) |

Classes left out with reason:
- `--unattended` switch: Maximum/Overflow (boolean, no numeric bound).
- Wait threshold: Sentinel Value Match (no sentinel value in a numeric threshold).
- `consumer_fenced`: Legitimate Edge Case (fencing after `worker_done` is covered by the idle rule in CAPS:77-80, not a spec row).
- Contract path: Maximum/Overflow (a path has no numeric bound).
- Section 7 (acceptance) guards are not tabled; they are covered by B6 and B7.

Completeness (FR-10): every guard is enumerated; every cell is populated; GAP rows are carried into the findings above. FR-8 and FR-9 apply to each GAP row; the blocking ones are B3, B4, B5, and the Medium ones are M5, M9, M14, M15, M16, M17.

=== PIPELINE DIMENSIONAL ANALYSIS ===

Not triggered as a data pipeline. The spec's flows are classification and report hand-off, not stages that filter, aggregate or fan out records. The one count-bearing flow is the disposition tally, which conserves: 43 = 21 + 22 (spec:76); 10 + 27 + 6 = 43 (spec:75-76, spec:83-92, spec:99-125, spec:132-137); 5 + 13 + 3 = 21 and 5 + 14 + 3 = 22 (INV-A:73, INV-B:278). No Quantity Flow Diagram is required.

---

=== CONSENSUS AND DISAGREEMENTS ===

- Consensus: the top-level-session rule and the "Orca on top, commands as workers" decision are sound (spec:16-17; the inventories agree, INV-A:95, INV-B:24).
- Consensus: the standalone rule and the file-based contract are the right shape. The defects are in how rows apply them.
- Disagreement (not resolved by this review): whether a coordinator answer may ever resolve a gate (B2). The spec leaves this to D2 and D4, but WC-3 applies generally. The coordinator's VERIFY pass should confirm that B2 is blocking as written.

=== REVISER BRIEF ===

Blocking findings: B1, B2, B3, B4, B5, B6, B7.

Restatement of the review loop's reviser contract (bullet 6): revise only the text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not revised by this brief.

=== FOLLOW-UP CANDIDATES (Medium and minor; not in the reviser brief; the session that ran the review asks the user once per loop whether to open issues for these, and this worker creates none) ===

- M1 evidence conflict on direct-route runs (spec:23, spec:43, spec:83)
- M2 scope understated in section 1.1 (spec:16)
- M3 report-path certainty overstated (spec:62, spec:274)
- M4 live-check timing (spec:181-182)
- M5 long-wait threshold and heartbeat cadence (spec:68, spec:210)
- M6 raw-text escape in AC-C1 (spec:172)
- M7 tasklist and reflect reversal and auto-accept (spec:88, spec:122, INV-B:295, INV-B:314)
- M8 contract versioning (spec:62, INV-B:272)
- M9 two channels for one question, and unbounded ask (spec:60-62)
- M10 cli-portify installed-path lookup (spec:105, INV-A:45)
- M11 brief template not specified (spec:158)
- M12 acceptance coverage for WC-1, WC-3, WC-6, WC-12; no next step for blocked (spec:59-70, spec:172-210)
- M13 standalone regression sampled, not tested (spec:146, spec:197, spec:203)
- M14 partial plus blocked question (spec:62-63)
- M15 follow-up effect unspecified (spec:70)
- M16 output directory not writable (spec:62-63)
- M17 quoted `--unattended` (spec:228)
- M18 retry path and answer carry-over (CAPS:116, spec:64)
- M19 brief template has no content (spec:158)
- M20 pr-submit classed two ways (spec:114, spec:132-139, spec:240)

Minor items (listed above under their MINOR labels): M6, M11, M14, M16, M17, M18, M19, M20.

---

=== BLOCKING FINDINGS (for the VERIFY prompt) ===

- B1 (spec:118, spec:119 against spec:146, spec:149)
- B2 (spec:61 against spec:60, spec:109, spec:234, spec:245)
- B3 (spec:63 with spec:62; CAPS:73)
- B4 (spec:63 with spec:62; INV-B:272)
- B5 (spec:62 against spec:83)
- B6 (spec:172 against spec:147, spec:150, spec:158)
- B7 (spec:183 and spec:194; INV-B:272, INV-B:49)

Verification has not been run. The coordinator must brief a fresh-context verifier with the candidate and this list only.

## Coverage
- Read in full: the candidate spec (`spec:1-286`), the shared README, the two command inventories, the Orca capabilities inventory, the review-loop prompts file (`~/.claude/rules/prompts/document_review_loop_prompts.md` as mapped into the sandbox home), and command.md.
- Checked against the inventories: all inventory line citations used in the findings (INV-A:13, 14, 35, 45, 49, 51, 62, 66, 68, 73, 76-83, 95, 97; INV-B:24, 46, 49, 210, 272, 278, 295, 301, 310, 314; CAPS:52, 58-61, 63, 64, 66-68, 73, 79, 80, 116, 129, 130) were read and match the quoted text.
- Not checked: every `src/...`, `.dev/codegraph-migration/...` and `.dev/evals/...` citation in the spec (outside the sandbox), so any claim resting on them is UNVERIFIED. The exact status vocabulary of the workflow contract (M8) and the exact `command` field of that contract (B7) are UNVERIFIED against source.

verdict: FAIL
