review: 1 of 3

# /sc:spec-panel critique, round 1

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (repo-relative; 286 lines as read)
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Mode: critique, first review (no `--re-review`, so `baseline: missing` does not apply)
- Focus: requirements, architecture (panel leads: Wiegers, Fowler; support: Adzic, Cockburn, Newman, Hohpe, Nygard)
- Reviewer model: claude-haiku-5-5
- Evidence base: the candidate, `.dev/orca-command-refactor/README.md`, and the three inventories under `.dev/orca-command-refactor/inventory/`. Every other path cited inside the spec (`src/`, `.dev/codegraph-migration/`, `.dev/evals/`, `CLAUDE.md`, `~/.claude/`, `/opt/Orca/`) is not in the workspace. I check it only where an inventory quotes it, against that quote, and otherwise mark it UNVERIFIED.
- Rules read: `command.md` in full; `home/.claude/rules/prompts/document_review_loop_prompts.md` (FIRST-REVIEW prompt) in full.

Citation shorthand: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of the three inventories; `README:N` = `.dev/orca-command-refactor/README.md`.

Coverage: all 12 WC rules (SPEC:59-70), section 2.3 (SPEC:73), section 3.1 and 3.2 tables (SPEC:81-125), section 4 (SPEC:127-139), section 5 SA-1 to SA-6 (SPEC:144-151), phases (SPEC:158-162), acceptance checks AC-C1 to AC-C5 and AC-0.1 to AC-4.3 (SPEC:172-210), decisions D1 to D5 (SPEC:228-253), the Decisions table (SPEC:258-269), and UNVERIFIED items 1 to 14 (SPEC:272-285). Section 1 evidence (SPEC:21-26) and its rejected alternative (SPEC:31-37) were checked against CAPS:92, CAPS:97-103, CAPS:145-151 and CAPS:161.

Verified by reviewer: the AC-C1 grep fault (finding M1) was tested read-only with a piped sample. The escaped-pipe pattern from SPEC:172 matches nothing (exit 1). The same pattern with plain `|` alternation matches the sample (exit 0).

## Mandatory output artifacts

### Guard Condition Boundary Table (triggered: the candidate has threshold, status-value and presence guards in WC-1, WC-4, WC-5, WC-6, WC-10, WC-12, section 3 gate rows, and AC-7.2 steps 2 and 4)

Rows are the input classes that apply to each guard. Classes that cannot occur are left out with a reason. The FR-8 and FR-9 status rule grades each GAP as blocking or Medium. Only B1 is blocking. All GAP rows here are Medium because each needs a guess about the implementer's reading, which is the Medium test in the review-loop prompt.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome: report says `failed` or `blocked` | SPEC:63 | Blocked | `status: blocked` | true | `--outcome failed` | OK |
| WC-5 outcome: no report exists | SPEC:63 | Zero/Empty | no file | true | `--outcome failed` | OK |
| WC-5 outcome: report says `succeeded` or `partial` | SPEC:63 | Typical / One | `status: partial` | false | `--outcome succeeded` | OK |
| WC-5 outcome: report exists, `status` key missing or value outside the four | SPEC:63 | Malformed | empty or `status: done` | not stated | not stated (contract is undefined; not "no report") | GAP (M8) |
| WC-6 resume: resume flag given, on-disk state missing | SPEC:64 | Sentinel | flag set, no state | not stated | not stated | GAP (M9) |
| WC-6 resume: no resume flag | SPEC:64 | Typical | flag absent | false | fresh output dir | OK |
| WC-10 long-wait split: tool call longer than 5 min | SPEC:68 | Max | 5 min 30 s | true | split into waits of at most 4 min | OK |
| WC-10 long-wait split: call of exactly 5 min | SPEC:68 | Boundary | 5 min 0 s | false ("longer than") | no split; heartbeat cadence is also 5 min (SPEC:68, CAPS:130) | GAP (minor, note N2) |
| WC-12 ownership fence: `check` returns `consumer_fenced` | SPEC:70 | Sentinel | `consumer_fenced` | true | stop, no `worker_done` | OK |
| WC-12 ownership fence: `check` returns empty | SPEC:70 | Zero/Empty | empty | false | continue (CAPS:51 says empty never means replaced) | OK |
| WC-12: `check` returns any other error | SPEC:70 | Legitimate edge | unknown error | not stated | not stated | GAP (minor, note N3) |
| WC-1 readiness: prompt before input box | SPEC:59 | Max | prompt present at 60 s | true | prompt must fall back "well inside" 60 s | GAP (minor; "well inside" is not a number) |
| WC-2 gate resolution: gate with no documented default and no flag | SPEC:60 | Legitimate edge | gate not in section 3 row | not stated | not stated | GAP (minor; section 3 claims to list every gate) |
| AC-7.2 step 2: `agentWait` absent | SPEC:181 | Zero/Empty | field absent | "pass" by the stated rule | Pass only if `agentWait` never non-null; absent means Orca never looked (CAPS:129) | GAP (M6) |
| AC-7.2 step 4: `status` outside the four values | SPEC:183 | Sentinel | `status: ok` | false | assert fails | OK |
| Section 3 gate rows (`--unattended` refusals, e.g. `--mode socratic`) | SPEC:102, 104, 114, 120 | Sentinel | flag set with refused value | true | refused or blocked | OK |

Pipeline Dimensional Analysis (FR-17): not triggered. The candidate describes task dispatch and report files, not a multi-stage data flow whose counts change. No count-divergence stage exists to annotate.

State Variable Registry (FR-15.1): not triggered. Focus is requirements and architecture, not correctness.

## Findings

### Blocking

**B1. Two stated rules contradict each other on whether Phase 0 briefs carry `--unattended`.** Expert: Wiegers (requirements consistency); Fowler (interface contract).
- Section 2.3 says each Task brief "states the exact command line including `--unattended`" (SPEC:73). Acceptance check AC-0.4 builds its brief "per section 2.3" (SPEC:180, SPEC:194).
- Phase 0 makes "no command edits" (SPEC:158), and the `--unattended` flag is added only in P1 (SPEC:159). The ready-today table says briefs pass "the stated flags", and its brief column lists no `--unattended` (SPEC:79, SPEC:81-92). So the flag is required by one rule and absent from the phase that runs the same commands.
- Sentence that holds with no further assumption: an implementer who follows section 2.3 writes `--unattended` into the P0 brief for `/sc:troubleshoot` or `/sc:workflow`, neither of which implements it until P1. The P0 smoke run then does not exercise the worker contract that AC-0.4 claims to test, and the section 1.4 gap 1 test (SPEC:43) is not performed.
- Recommendation: state in section 2.3 that `--unattended` is required from P1, and that P0 briefs omit it; or move the AC-0.4 brief rule to P1. Either change makes the two rules agree.
- Priority: High. Blocking under the two-rules-contradict class.

### Medium (follow-up candidates)

**M1. AC-C1 cannot fail, so it does not enforce SA-2 or WC-8.** Expert: Adzic (acceptance examples must be able to fail).
- SPEC:172 writes `(orchestration\|worktree\|terminal\|agent)` inside `grep -E`. In ERE, `\|` is a literal `|`, not alternation. The pattern matches nothing, so the check prints nothing and passes whether or not a command calls Orca. Reviewer test (read-only, piped sample): escaped form exit 1; plain-alternation form exit 0 on the same input.
- Recommendation: change `\|` to `|` in SPEC:172, and add a check that the pattern matches a planted sample.
- Priority: High, because it is the only mechanical gate for SA-2 and WC-8. Graded Medium here, because the defect is in a check and no stated text causes harm by itself.

**M2. Section 1.4 and E3 disagree on whether a direct-route run exists.** Expert: Wiegers (evidence consistency).
- E3 cites the codegraph return contract with `invocation_method: "skill-direct"` as proof the work landed (SPEC:23). INV-A:13 reads the same contract as "Proven as a direct Orca-worker skill call".
- Section 1.4 item 1 says the only end-to-end proof is the PR #329 run, whose brief used an Agent-tool subagent, so it "proves the nested route, not the direct route" (SPEC:43). UNVERIFIED item 1 says no direct run was observed (SPEC:272).
- The spec's own E3 contradicts this. Either the direct-route evidence is weaker than the spec says (a single contract, not an end-to-end worker transcript), or the section should cite it. The claim and its strength need to match.
- Recommendation: cite the skill-direct contract in section 1.4 as direct-route evidence, with its limit (no transcript read, INV-B:323 applies only to this task), and keep UNVERIFIED item 1 for the transcript check.
- Priority: Medium.

**M3. Section 3.2 says the tasklist reflect fan-out needs no change, which relies on a nesting-limit claim the inventories mark UNVERIFIED.** Expert: Fowler (architecture: nesting depth).
- The tasklist row says "Other required change: none (its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, INV-A:14)" (SPEC:122).
- INV-B:210 says nested spawning is "UNVERIFIED whether nested spawning works" and treats it as subagent-to-agent nesting. INV-B:314 and INV-B:322 flag the same question as unverified. INV-B:295 recommends removing "a nested fan-out or remediation offer that runs inside subagents".
- The spec cites only INV-A:14 and omits the conflict. Neither the UNVERIFIED list (SPEC:272-285) nor section 9 mentions this row.
- Recommendation: add the open question to UNVERIFIED, and either make Stage 10.5 run without `--remediate` in unattended mode or justify the no-change verdict against INV-B:295.
- Priority: Medium.

**M4. The D1 example uses an `--output` flag that no inventory evidences for troubleshoot.** Expert: Cockburn (worked examples).
- D1 example: `/sc:troubleshoot "login fails" --unattended --output .dev/troubleshoot/login/` (SPEC:228).
- The troubleshoot row in section 3.1 lists "no `--fix`" as its only brief flag (SPEC:91). INV-B:242 names only the default output directory (`.dev/troubleshoot/<slug>-<timestamp>/`) and no output flag.
- Recommendation: drop `--output` from the example, or cite the flag.
- Priority: Medium.

**M5. `/sc:tdd` is listed as ready today, but the nested `/task` runs commit and push immediately, and WC-9 forbids that under unattended mode.** Expert: Adzic (outward-action examples).
- WC-9 says no push, PR, post, install or paid run is default under `--unattended` (SPEC:67).
- INV-B:204 says the task command's EXEMPT keywords `commit` and `push` "run immediately with no skill". INV-B:221 says tdd runs `/task`. INV-B:224 lists tdd's outward actions as none.
- Sentence needing one assumption: if a generated task file contains a `commit` or `push` item, a tdd worker in the ready-today set commits or pushes with no gate. The assumption (that generated tasks contain such items) is UNVERIFIED by this reviewer.
- Recommendation: add `tdd` to the section 3.2 gate list with a commit and push refusal under `--unattended`, or state why generated task files cannot contain them.
- Priority: Medium.

**M6. AC-7.2 step 2 passes when Orca never looked.** Expert: Adzic (acceptance rule).
- Pass rule: `observation.agentWait` "is never non-null" (SPEC:181). CAPS:129 quotes `worker-show`: "Null means Orca looked and found no wait. An absent field means it never looked."
- An absent field satisfies "never non-null", so a run that Orca never observed passes the stall check. The check then cannot detect the stall it exists to catch.
- Recommendation: require `agentWait` to be present and null on each poll; treat absent as a fail.
- Priority: Medium.

**M7. The research row pins `--strategy planning` on a persona file the inventory did not verify.** Expert: Cockburn (behavior under the pin).
- SPEC:116 says `--unattended` pins `--strategy planning`, citing `src/superclaude/agents/deep-research-agent.md:40-56`, which INV-B:127-135 read.
- INV-B:316 (UNVERIFIED item 3) says it is not known whether the frontmatter persona loads that file at run time. The spec does not mention this, and the pin depends on it.
- Recommendation: add the UNVERIFIED item to section 9 or the UNVERIFIED list, or pin the strategy in the brief as well.
- Priority: Medium.

**M8. WC-5 has no outcome for a report that exists but has a missing or unknown `status`.** Expert: Nygard (failure modes; blank behavior rule).
- WC-5 maps `failed` or `blocked`, no report, and "otherwise" to `succeeded` (SPEC:63). A malformed contract falls under "otherwise", so a worker may send `succeeded` for a report it could not read.
- Recommendation: add "missing or unrecognized `status`: `--outcome failed` and `blocked` in the body".
- Priority: Medium.

**M9. WC-6 has no rule for a resume flag whose on-disk state is absent.** Expert: Nygard.
- WC-6 says a command resumes "when given its resume flag" (SPEC:64). Nothing says what happens if the state is missing: fail, or start fresh in the same directory, which would collide with WC-6's own rule against corrupting prior output.
- Recommendation: state that a missing state with a resume flag is `blocked`.
- Priority: Medium.

**M10. The count of "27 needing a change" includes `/sc:pr-submit`, which D3 recommends keeping coordinator-only.** Expert: Wiegers (internal consistency).
- The 27 includes pr-submit (SPEC:114, SPEC:76). D3 recommends coordinator-only (SPEC:239-242). Section 4 says pr-submit is a worker candidate "only if the user accepts open decision D3" (SPEC:139).
- Recommendation: move pr-submit to a conditional row with the count stated as 26 plus one conditional.
- Priority: Low to medium.

**M11. The reflect row is ready today, but its default Wave 7 moves a folder and writes a tracked docs file in the shared worktree.** Expert: Hohpe (shared-state writes).
- SPEC:88 lists reflect as ready with only `--no-promote` as an option. INV-B:110-114 says Wave 7 moves the validated work-unit folder by default and writes `docs/memory/reflect/deviation-patterns-<slug>.md`.
- WC-11 covers writes to one file by two workers (SPEC:69). It does not cover a folder move or a tracked-file write from a ready-today command.
- Recommendation: make `--no-promote` required in the reflect brief, and list the tracked file under the artifacts WC-4 must name.
- Priority: Medium.

**M12. The E2 claim that the worker "answered" is not in the cited line.** Expert: Wiegers.
- SPEC:22 says EVIDENCE.md:45 shows "state: ready, stage: input_accepted and answered". INV-quoted text from that line (CAPS:49) shows only `state: ready, stage: input_accepted`. "Answered" is not in the quote.
- Recommendation: remove "and answered" or cite where the answer is shown.
- Priority: Low.

### Minor notes (not blocking, not Medium)

- N1. Section 1.2 E4 relies on CAPS:155 for "not counted by Orca's nesting limit" (SPEC:24). CAPS:155 cites the depth fence correctly but says Orca's limit on subagents is UNVERIFIED. The claim should say "the depth fence counts only Orca dispatches (CAPS:97-99)".
- N2. WC-10 "longer than 5 minutes" and "heartbeat every 5 minutes" meet at exactly 5 minutes (SPEC:68). Say "5 minutes or longer".
- N3. WC-12 says nothing about a `check` that errors (SPEC:70).
- N4. WC-1 "well inside the readiness limit" has no number (SPEC:59). Give one, such as 30 s, which EVIDENCE.md:45 used per CAPS:49.
- N5. The spec's UNVERIFIED list (SPEC:272-285) is referenced correctly from the body, except that M3, M5 and M7 are not in it.
- N6. Several section 3 rows cite `src/` and `.dev/codegraph-migration/` paths not in the workspace. I checked them only through the inventories' quotes. Where a row has no inventory quote, it is UNVERIFIED here.

## Expert summary

- Wiegers (requirements): B1, M2, M10, M12. The core requirements (WC-1 to WC-12) are clear and testable, except for WC-5 and WC-6 gaps (M8, M9).
- Adzic (acceptance examples): M1, M5, M6. Two acceptance checks cannot fail or pass by absence.
- Cockburn (use cases and actors): M4, M7. Worked examples and pins need evidence.
- Fowler (architecture and interfaces): B1, M3. The unattended flag contract and the nested fan-out assumption need one owner each.
- Newman, Hohpe (service boundaries and shared state): M11. Reflect's default writes break the parallel-safe rule's intent.
- Nygard (failure modes): M8, M9. Missing or malformed state has no defined outcome.

## Overall quality (0 to 10)

- Clarity: 7. Precise rule IDs and citations; some rules repeat each other.
- Completeness: 6. Phase 0 and the reflect and tdd rows have open gaps.
- Testability: 5. AC-C1 and AC-7.2 step 2 cannot detect what they target.
- Consistency: 5. B1 and M10 conflict with the body; M2 conflicts with E3.

## Reviser brief

Revise only the blocking finding B1, and restate the rules: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph cites its finding id; prefer deleting or narrowing; report byte size before and after with bytes added and deleted per finding id. Medium and minor findings are not in this brief and do not trigger a revision.

Blocking ids for revision: B1.

## Follow-up candidates (Medium and minor; recorded, not acted on)

Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12 (M12 is Low).
Minor: N1 to N6.

No issue has been opened. The coordinator decides whether to open issues for these; this run is not `--unattended`, so the interactive question belongs to the session that ran the review.

## Items not checked

- Every citation to a file outside `.dev/orca-command-refactor/` (see N6) is UNVERIFIED except where an inventory quote was compared.
- Nothing was run against Orca, GitHub or the repository. The only command executed was the read-only grep test for M1, plus `sha256sum`.

verdict: FAIL
