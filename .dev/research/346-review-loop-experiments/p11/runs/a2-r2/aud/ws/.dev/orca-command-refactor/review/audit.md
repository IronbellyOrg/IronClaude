review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

| Header field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Label | Whole-document audit of the final spec; first review of the full document |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate sha256 | `bbc5da09c16d99c761039d7df263e9ff3629635be3ec1f834b924b06575af75f` |
| Baseline / prior report | none given, so this is a first review (no `--re-review`, no `--baseline`) |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Brief clauses overridden | none |
| Improve step | not run: the brief allows writing only this file, and no revised specification is written |

Citation keys. `SPEC:N` is line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` are lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` under `.dev/orca-command-refactor/`. `README:N` is `.dev/orca-command-refactor/README.md`.

Evidence limit. The three inventory files are the only evidence checkable in this workspace. Every spec citation to `src/superclaude/...` (`cmd/`, `sk/`, `ag/`), `CLAUDE.md`, `EVIDENCE.md`, `install_core.py`, `Makefile`, `pyproject.toml`, `HOW-WE-WORK.md` or the codegraph-migration files is UNVERIFIED here. Such a citation is accepted only as "carried by INV-x:N" when an inventory line quotes it.

## What I covered

- All 285 lines of the candidate.
- Every `INV-A`/`INV-B` line cited in sections 3 and 4 and in the decisions table: each points at the row or note it names, and the verdict split holds. 10 ready + 27 needs-change + 6 coordinator-only = 43 (SPEC:76; INV-A:73; INV-B:278). The per-phase counts also add up (see Quantity Flow).
- The `CAPS` lines cited in sections 1, 2, 8 and 9 and in the UNVERIFIED list. They support the claims, with two small wording overstatements (n-1, n-4).
- The internal consistency of WC-1..WC-12, SA-1..SA-6, the phase table, AC-C1..AC-4.3 and D1..D5.
- Not covered, because it is not checkable here: the truth of any claim that rests only on `cmd/`, `sk/`, `ag/` or repo-file lines.

## Findings at a glance

| Id | Label | Graded | Bucket | Subject |
|---|---|---|---|---|
| F-01 | CRITICAL | blocking | ARCHITECTURE | WC-4 contract path for file-valued `--output` collides across workers |
| F-02 | MAJOR | blocking | REQUIREMENTS | AC-0.4 cannot pass as written; its failure "reopens section 1" |
| M-01 | MAJOR | Medium | ARCHITECTURE | WC-6 "fresh output directory" has no owner and conflicts with the WC-4 fixed path |
| M-02 | MAJOR | Medium | REQUIREMENTS | cli-portify has no stated way past its three approval gates; AC-2.3 cannot pass for it |
| M-03 | MAJOR | Medium | REQUIREMENTS | P1 accepts `--unattended` on gated commands before P2 converts the gates |
| M-04 | MINOR | Medium | REQUIREMENTS | AC-1.1 asserts `load` both has and has no `## Unattended mode` section |
| M-05 | MINOR | Medium | REQUIREMENTS | AC-C1 and SA-2 contradict each other for the contract file and the HOW-WE-WORK Orca section |
| M-06 | MINOR | Medium | REQUIREMENTS | AC-C5 (no removed lines) conflicts with adding a flag to an existing usage line |
| M-07 | MAJOR | Medium | REQUIREMENTS | WC-10 splits waits above 5 min into waits of at most 4 min; the 4-5 min band is undefined |
| M-08 | MAJOR | Medium | ARCHITECTURE | pr-submit poll loop is read differently from the inventories and is not in the re-read list |
| M-09 | MAJOR | Medium | ARCHITECTURE | "keep their fields" versus a fixed four-value `status` set |
| M-10 | MAJOR | Medium | REQUIREMENTS | WC-3 lets any blocked gate be answered by the coordinator, including the implement Ruling |
| M-11 | MAJOR | Medium | REQUIREMENTS | Blocked-to-failed-to-retry cycle is unbounded; coordinator recovery after `blocked` is not specified |
| M-12 | MAJOR | Medium | ARCHITECTURE | tasklist: nesting depth stated safe and remediation auto-accepted without a recorded decision |
| M-13 | MINOR | Medium | ARCHITECTURE | Fixed-path commands rely on coordinator serialization that section 2.3 never assigns |
| M-14 | MINOR | Medium | ARCHITECTURE | Report-location flags are heterogeneous; the contract has no version field |
| M-15 | MINOR | Medium | REQUIREMENTS | SA-3 and WC-4 disagree on when the contract is written |
| M-16 | MINOR | Medium | REQUIREMENTS | `--unattended` with no output flag has no stated command behavior |
| M-17 | MINOR | Medium | REQUIREMENTS | WC-1 "well inside the limit" has no number |
| M-18 | MINOR | Medium | REQUIREMENTS | WC-5 "no report exists" does not cover an empty or unparseable report |
| n-1..n-7 | MINOR | note | mixed | See "Follow-up candidates" |

Two findings are blocking, so the verdict is FAIL.

=== REQUIREMENTS ANALYSIS ===

### F-02 (MAJOR label, blocking). AC-0.4 cannot pass as written
- **Experts.** Crispin (lead), Wiegers, Adzic.
- **Issue.** AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (SPEC:194). Only step 4 is relaxed. Step 3 of the live check still requires that "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (SPEC:182). In P0 no WC-4 contract exists. P0 makes no command edits (SPEC:158), and WC-4 and the `## Unattended mode` sections arrive in P1 (SPEC:159, 79). The three P0 smoke commands also have no WC-4 path today:
  - `/sc:troubleshoot` reports `REPORT.md`, which is not a contract with a `status` (SPEC:91).
  - `/sc:workflow` reports `.dev/tasks/to-do/<id>/return-contract.yaml`, where `<id>` is unknown before dispatch and the `--output-dir` flag is only added in P1 (SPEC:92).
  - `/sc:adversarial` has "filename not fixed", and real runs wrote it at two different depths (SPEC:83; INV-A:35, INV-A:60).
- **Grading sentence.** An implementer or verifier who follows AC-0.4 as written must show, for each of the three P0 smoke runs, a report path equal to the WC-4 contract path and a contract `status` to compare against the outcome. That is impossible before P1, so the acceptance criterion cannot pass and the verifier must either fail it or silently reinterpret it. A failure at this gate "reopens section 1" (SPEC:194), the central decision, on a defect of the check and not of the decision.
- **Recommendation.** Narrow step 3 for P0 only, for example: "its report path is the report file named for that command in section 3.1, and `--outcome` matches the worker's own reading of that report". Keep the full wording from P1 on. Rationale: P0 exists to test the decision with commands as they are today (SPEC:158), so its pass condition must use today's report files. This is a deletion or narrowing of one clause, not a new rule.
- **Priority.** High. **Quality impact.** Testability +2 (about 5 to 7), Consistency +1.

### M-02 (MAJOR label, Medium). cli-portify has no stated path past its approval gates
- **Experts.** Wiegers, Cockburn.
- **Issue.** Under `--unattended` each of cli-portify's three always-on approval gates "resolves as blocked" (SPEC:105; INV-A:45). WC-2 allows three resolutions: a documented default, a caller flag, or blocked (SPEC:60). The row names no default and no approval flag. The inventory had recommended "an explicit auto-approve flag" as an option (INV-A:79). The row adds only `--resume <contract>` and does not say whether resuming past a gate counts as approval. AC-2.3 asks for a happy-path run of every P2 command "with every required flag in the brief" that ends `--outcome succeeded` (SPEC:201), and cli-portify is a P2 command (SPEC:160).
- **Why Medium.** The finding needs a guess: an implementer could read `--resume` as implicit approval and then AC-2.3 passes over several runs. Nothing in the text forces the worse reading, but nothing excludes it either.
- **Recommendation.** One sentence in the row: either the resume flag implies approval of the artifact named in the contract, or a named approve flag exists. Priority Medium.

### M-03 (MAJOR label, Medium). P1 flag acceptance versus P2 gate conversion
- **Experts.** Adzic, Nygard.
- **Issue.** P1 delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (SPEC:159). The coordinator brief template tells the coordinator to put `--unattended` on every worker's command line (SPEC:73, 51). Gate conversion, including WC-9's "outward actions off", is in P2 (SPEC:160). Between P1 and P2, `/sc:auggie-review <PR> --unattended` would be accepted, and since the flag is still a no-op for that command, it would post to GitHub by default and then wait (INV-A:38, INV-A:62; SPEC:100). The phase table says each phase "leaves standalone behaviour unchanged" (SPEC:154), which is true, but it does not say a gated command must refuse the flag until its phase lands. AC-1.2 tests only P1 commands (SPEC:196).
- **Why Medium.** It depends on a coordinator dispatching a P2 command during the P1 window, which the text does not forbid but does not require either.
- **Recommendation.** State that a command accepts `--unattended` only in the phase that gives it a full row (or refuses it before). Priority Medium.

### M-04 (MINOR label, Medium). AC-1.1 and `load`
- AC-1.1 asserts that "the rows naming P1" have a `## Unattended mode` section, and in the same sentence that `load` has none (SPEC:195). The `load` row names P1 (usage line only) (SPEC:112), and section 3 says every changed command "except `load`" gains the section (SPEC:76). P1 also lists `--unattended` "accepted by every command in sections 3.1 and 3.2" (SPEC:159), which includes `load`. A careful reader resolves it, but the test author has to guess. Recommend: say "the rows naming P1 other than `load`". Priority Low.

### M-06 (MINOR label, Medium). AC-C5 and new flags
- SA-4 says edits are additive: "a new `## Unattended mode` section and new flags" (SPEC:149). AC-C5 requires that `git diff -U0 ... | grep -E '^-[^-]'` print nothing for command files without a named defect fix (SPEC:176). A new flag documented in an existing usage or `argument-hint` line changes that line and prints a `-` row. The implementer must know to put every new flag only in the new section. Recommend: say so in SA-4. Priority Low.

### M-07 (MAJOR label, Medium). WC-10 band between 4 and 5 minutes
- **Expert.** Nygard. WC-10 requires a split only for a step that blocks "longer than 5 minutes", and then into waits "of at most 4 minutes" (SPEC:68). The decisions table fixes 4 minutes as a margin under the 5-minute cadence (SPEC:266; CAPS:130). AC-4.3 demands that "no single tool call exceeds 240 s" (SPEC:210). A step that blocks for 4.5 minutes needs no split under WC-10 but fails AC-4.3. Two blocking calls of 4.5 minutes put the gap between heartbeats at about 9 minutes against a 5-minute cadence.
- **Why Medium.** Whether Orca uses heartbeat age at all is UNVERIFIED (CAPS:130, CAPS:182), so no wrong outcome is shown. Recommend: use one threshold (4 minutes) in both places. Priority Medium.

### M-10 (MAJOR label, Medium). WC-3 and the implement Ruling
- **Experts.** Wiegers, Nygard. WC-3 lets a worker whose gate "would resolve as blocked" ask the coordinator once and then "re-invoke or resume the command with the answer as a flag" (SPEC:61). The implement row blocks on `E-HALT-QA` or `E-NO-RULING` (SPEC:109), and D2(a) says the worker "stops ... and ends `failed`" because the Ruling rule rejects "another agent's message" (SPEC:233-234; INV-A:51, INV-A:66). Read alone, WC-3 allows the worker to relay a coordinator answer for the Ruling gate. D2(a) and the implement row do not say that WC-3 does not apply to the Ruling gate.
- **Why Medium.** The skill's own Ruling rule (INV-A:66) still rejects such an answer, so a wrong approval needs the worker to misread that rule. Recommend: one clause in WC-3 excluding the Ruling gate. Priority Medium.

### M-11 (MAJOR label, Medium). Blocked, failed, retry
- **Experts.** Cockburn, Nygard. WC-5 maps `blocked` to `--outcome failed` (SPEC:63). A worker's own failed report "does not" count toward Orca's circuit breaker (CAPS:80), and a failed Task keeps its dependents blocked until a `--retry-of` replacement completes (CAPS:90). The spec never says how the coordinator proceeds after a `blocked` report (answer the question, then start a retry with the answer as a flag), and section 2.3 stops at "releases or reuses the worker" (SPEC:73). Because blocked reports are exempt from the breaker, a coordinator that retries without supplying the answer can cycle without bound.
- **Recommendation.** Add to section 2.3 one sentence: after `blocked`, the coordinator supplies the answer through the flag the row names and starts a `--retry-of` worker, and stops after the same cap Orca uses. Priority Medium.

### M-16, M-17, M-18 (MINOR labels, Medium)
- **M-16.** `--unattended` without any output flag has no stated behavior in the commands. Section 2.3 puts the duty on the coordinator (SPEC:73), but WC-4 and the rows say "add `--output`" without "required" (SPEC:62, 99-107). Recommend: command refuses (blocked) without an output location.
- **M-17.** WC-1 says a fallback must come "well inside" the 60 s limit (SPEC:59). The evidence it cites shows a fallback of 30 s passing and "above about 45 s" failing, on a start whose limit was 45 s (CAPS:49). The text gives no number for the 60 s default. Recommend: state 30 s.
- **M-18.** WC-5 sends "no report exists" to `failed` (SPEC:63). A report file that exists but is empty, unparseable, or has an unlisted `status` is not covered. Step 4 of the live check tests it only on the coordinator side (SPEC:183). Recommend: treat those as "no report".

### M-15 (MINOR label, Medium). SA-3 versus WC-4
- WC-4 says the contract is written "in unattended mode" (SPEC:62). SA-3 says contract and report files are written "only in unattended mode or when the caller passes the new output flag" (SPEC:148). A plain run with only the new output flag writes a contract under SA-3 and none under WC-4. AC-1.3 tests only the no-flag case (SPEC:197). Priority Low.

=== ARCHITECTURE ANALYSIS ===

### F-01 (CRITICAL, blocking). Contract path collides when `--output` is a file
- **Experts.** Fowler (lead), Whittaker, Hohpe.
- **Issue.** WC-4 defines the contract directory as "the brief's `--output-dir` or directory-valued `--output`, or the parent directory of a file-valued `--output` (tdd, init-lite)" and requires the contract at `<contract-dir>/return-contract.yaml` (SPEC:62). The tdd row's brief passes `--output <file>` (SPEC:90), and the TDD default is `docs/[domain]/TDD_[COMPONENT-NAME].md` (INV-B:222), so sibling TDDs in one domain directory are the normal case. Section 2.3 says the brief states "the output directory, so the report path is known before dispatch" and says nothing about it being unique per worker (SPEC:73). WC-11 requires "Two workers in one worktree must never write the same file" (SPEC:69), but it governs default output paths and shared memory, not the contract name.
- **Grading sentence.** An implementer who follows WC-4 as written builds a contract path that is the same for any two file-valued outputs in one directory, and that is wrong because the coordinator then reads one worker's `status` and `report_path` as the other's, defeating the purpose of WC-4 (a per-worker report known before dispatch) and violating WC-11.
- **Whittaker, accumulation attack.** I can break this specification by **Accumulation Attack**. The invariant at **SPEC:62 / 73** (one known contract path per worker) fails when **two file-valued `--output` values share a parent directory**. Concrete attack: W1 runs `/sc:tdd "Login service" --unattended --output docs/auth/TDD_login.md` and W2 runs `/sc:tdd "Session service" --unattended --output docs/auth/TDD_session.md`. Before: `docs/auth/` holds no contract. Both are told `--report-path docs/auth/return-contract.yaml`. W1 finishes and writes `status: succeeded`; W2 fails and writes `status: failed` over it (or the reverse order). After: 2 workers, 1 file; the coordinator reads `failed` for W1 or `succeeded` for W2. The 7.2 check runs one worker at a time (SPEC:180-186), so no acceptance check catches it.
- **Recommendation.** Delete the "parent directory of a file-valued `--output`" clause from WC-4 and instead make the contract directory always the brief-supplied directory, with section 2.3 requiring a distinct directory per worker; or name the file by the output stem. Prefer the deletion plus one sentence in 2.3. Priority High. **Quality impact.** Consistency +1, Completeness +1.

### M-01 (MAJOR label, Medium). "Fresh output directory" has no owner
- **Experts.** Newman, Nygard. WC-6 says a command without a resume flag "writes each run into a fresh output directory" (SPEC:64). WC-4 fixes the contract at the brief's directory, known before dispatch (SPEC:62, 73). If the command creates the fresh directory, the contract is not at the pre-dispatched path. If the coordinator supplies a new directory per attempt, the brief for a `--retry-of` worker must say so, and the text does not. AC-3.2 starts roadmap "fresh" in a directory that already holds `.session-memory.md` and no resume flag (SPEC:205), which would overwrite the earlier attempt's output.
- **Why Medium.** The implementer has two readings and the worse one is only one of them. Recommend: state that the coordinator supplies a new directory per attempt for fresh-dir commands. Priority Medium.

### M-05 (MINOR label, Medium). AC-C1 versus SA-2 and the P0 deliverables
- SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (SPEC:147). AC-C1 scans `src/superclaude/core`, which holds the contract file and `HOW-WE-WORK.md`, with a pass condition of "prints nothing" and no exclusion for either file (SPEC:172). P0 adds the contract file and an Orca section to `HOW-WE-WORK.md` (SPEC:158, 150). If either contains a literal `orca orchestration ...` the common check fails in P0. Recommend: scope AC-C1 to commands, skills and agents, as SA-2 says. Priority Low.

### M-08 (MAJOR label, Medium). pr-submit poll loop
- The spec asserts that pr-submit's 600 s is "a cumulative per-wait budget made of repeated iterations ... not one blocking call" and so needs no wait splitting (SPEC:68, 114). Both inventories describe it as a wait of "up to `--timeout` 600 s per wait" that "must send Orca heartbeats" (INV-B:95, INV-B:299). The spec's re-read list does not include `sk/sc-pr-submit-protocol/SKILL.md:46-64` (SPEC:11), and the spec marks the poll script runtime UNVERIFIED (SPEC:114, 283). The spec therefore overrides its inventory evidence with a citation it did not re-read, and the sources are not checkable here (UNVERIFIED). Because D3's recommendation keeps pr-submit with the coordinator (SPEC:240), the harm is limited to D3(b). Recommend: record the disagreement as a Decisions row. Priority Medium.

### M-09 (MAJOR label, Medium). `status` vocabulary versus "keep their fields"
- WC-4 requires `status` to be one of four values and says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62). The decisions table fixes the four-value set (SPEC:262). The existing contracts of workflow, reflect, brainstorm and adversarial have their own `status` fields (INV-B:272, INV-B:112, INV-A:39, INV-A:35), and no inventory line gives their values. Step 4 of the live check asserts the four values on every command (SPEC:183). If an existing value is, say, `complete`, then "keep" and the check contradict each other, and changing it is not additive (SPEC:149) and may break consumers (SA-6, SPEC:151). Recommend: read the four vocabularies and record the mapping. Priority Medium. UNVERIFIED: the existing value sets.

### M-12 (MAJOR label, Medium). tasklist nesting and remediation
- **Experts.** Fowler, Newman. The tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (SPEC:122, citing INV-A:14). INV-A:14 says up to three layers below the main conversation. The tasklist's Stage 10.5 reflect agent can itself run Tier 2 reviewers and an adversarial merge, so the path can reach that limit. The inventory marks nested spawning UNVERIFIED (INV-B:210, INV-B:314, INV-B:322), and the spec's own UNVERIFIED list (SPEC:271-285) omits it. The row also chooses to pass `--unattended` to each reflect, which per the reflect row means `--remediate` auto-accepts under the headless rule (SPEC:88, 122; INV-B:109), while the inventory's recommended fix was to drop `--remediate` (INV-B:215). No Decisions row records why the larger behavior was chosen. Recommend: add the UNVERIFIED item and a Decisions row. Priority Medium.

### M-13 (MINOR label, Medium). Fixed-path commands
- cleanup-audit (`.claude-audit/`), index-repo (`PROJECT_INDEX.md`) and init-lite (`.dev/superclaude/context-audit.md`) write fixed paths (SPEC:85-87; INV-A:42, INV-A:53, INV-A:55). The spec says one audit per worktree "at a time (WC-11)" (SPEC:85), but WC-11 is a command rule (SPEC:69) and section 2.3 does not give the coordinator a serialization duty (SPEC:73). Recommend: one sentence in 2.3. Priority Low.

### M-14 (MINOR label, Medium). Interface heterogeneity
- **Experts.** Fowler, Newman. Report location is expressed with `--output` (directory or file), `--output-dir`, `--pass`, and per-command fixed paths (SPEC:62, 83-92, 99-125). The contract has no version or schema field, while one existing contract is already versioned ("contract 1.1", INV-B:272). A single directory flag and a `contract_version` field would let the coordinator treat all 37 worker-capable commands alike. Priority Low.

=== ADVERSARIAL ANALYSIS (Whittaker, review order 6) ===

Each finding follows the FR-3 template. F-01 is given above in full.

- I can break this specification by **Sequence Attack**. The invariant at **SPEC:194 (AC-0.4) with SPEC:158-159** fails when **the P0 smoke runs are judged against contract rules that only exist after P1**. Concrete attack: the verifier runs `/sc:troubleshoot` as a worker in P0; it writes `REPORT.md` and no contract; step 3 requires a contract `status` and the WC-4 path; the run is recorded as failed and "reopens section 1". Before: decision stands; after: decision reopened on a check defect. (F-02, MAJOR, blocking.)
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:154 / 159-160** fails when **a gated command receives `--unattended` between P1 and P2**. Concrete attack: after P1, the coordinator dispatches `/sc:auggie-review 123 --unattended`; the flag is accepted as a no-op; the command posts a PR review by default and then ends its turn on the remediation offer (INV-A:38, INV-A:62). Before: no review posted; after: one review and a stalled worker. (M-03, MAJOR, graded Medium.)
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:68 / 210** fails when **a blocking call lasts 4.5 minutes**. WC-10 does not require a split, AC-4.3 requires one, and two such calls leave about 9 minutes between heartbeats. (M-07, MAJOR, graded Medium.)
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:63 / CAPS:80** fails when **blocked workers are retried repeatedly**. A `blocked` report ends `failed` but does not count toward the breaker, so retry number N+1 has the same input and the same outcome, with no cap. (M-11, MAJOR, graded Medium.)
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:63** fails when **the contract file is present but empty**. `test -s` on the coordinator side catches it (SPEC:183), but the worker-side rule "no report exists" (SPEC:63) does not name it. (M-18.)
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:62** fails when **an existing contract already uses `status` with a different value set**. WC-4 says both "keep their fields" and "one of succeeded/partial/failed/blocked". (M-09.)
- I can break this specification by **Zero/Empty Attack** on **SPEC:60 / 99-107**: `--unattended` with no output flag has no command-side rule. (M-16.)

=== GUARD CONDITION BOUNDARY TABLE ===

Trigger met: the spec has thresholds and guards (limits, caps, mode switches, confidence floor). Completed before the synthesis below. Classes left out are named with a one-line reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| contract-dir resolution | SPEC:62 | Zero/Empty | no output flag in the brief | unresolved | none in commands; coordinator "owes" the directory (SPEC:73) | GAP (M-16, Medium) |
| contract-dir resolution | SPEC:62 | One/Minimal | `--output x.md` (bare filename) | parent is `.` | contract at `./return-contract.yaml`, by the literal rule | OK |
| contract-dir resolution | SPEC:62 | Typical | `--output-dir .dev/x/` | the directory | contract at `.dev/x/return-contract.yaml` | OK |
| contract-dir resolution | SPEC:62, 90 | Maximum/Overflow | two workers, file-valued `--output` in one directory | same path for both | not specified; one file overwritten | GAP (F-01, blocking: coordinator reads the wrong status) |
| contract-dir resolution | SPEC:62, 262 | Sentinel Value Match | existing contract `status` value outside the four | fixed set vs "keep their fields" | not specified | GAP (M-09, Medium) |
| contract-dir resolution | SPEC:64, 73 | Legitimate Edge Case | `--retry-of` worker given the same directory | overwrite | "fresh directory" but no owner | GAP (M-01, Medium) |
| wait split (WC-10) | SPEC:68 | Typical | a 2-minute poll | below 5 min | heartbeat between calls | OK |
| wait split (WC-10) | SPEC:68, 104 | Maximum/Overflow | a 3600 s eval | above 5 min | split into waits of at most 4 min | OK |
| wait split (WC-10) | SPEC:68, 210 | Legitimate Edge Case | one call of 4.5 min | not above 5 min, above 240 s | WC-10 none, AC-4.3 fails it | GAP (M-07, Medium) |
| outcome mapping (WC-5) | SPEC:63 | Zero/Empty | report file empty or unparseable | "no report exists"? | not specified | GAP (M-18, Medium) |
| outcome mapping (WC-5) | SPEC:63 | One/Minimal | `status: succeeded`, one artifact | succeeded | `--outcome succeeded` | OK |
| outcome mapping (WC-5) | SPEC:63, 263 | Typical | `status: partial` | succeeded | `--outcome succeeded`, first sentence says partial | OK |
| outcome mapping (WC-5) | SPEC:63 | Sentinel Value Match | `status: blocked` | failed | `--outcome failed` | OK (follow-up path: M-11) |
| outcome mapping (WC-5) | SPEC:63 | Legitimate Edge Case | audit report with verdict FAIL | succeeded | `--outcome succeeded` | OK |
| nested depth (R1/WC-8) | SPEC:33, 66 | Typical | command calls `worker-start` at depth 1 | refused | forbidden for commands | OK |
| nested depth (R1/WC-8) | SPEC:252 | Legitimate Edge Case | user raises the depth (D5 b) | allowed by Orca | spec's non-goal, kept at 1 | OK |
| confidence floor (task row) | SPEC:121 | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| confidence floor (task row) | SPEC:121; INV-B:199 | Legitimate Edge Case | confidence exactly 0.70 | not below 0.70 | proceeds, as the source rule is "< 0.70" | OK |
| tdd topic guard | SPEC:90, 200; INV-B:219 | Zero/Empty | empty prompt | unclear | not specified | GAP (Medium; minor) |
| tdd topic guard | SPEC:90, 200 | Typical | bare topic `auth` | topic-only | blocked (AC-2.2) | OK |
| tdd topic guard | SPEC:90 | Legitimate Edge Case | one-line named component, not a bare topic | between "bare topic" and "precise prompt" | not defined | GAP (Medium; minor) |
| outward default (WC-9) | SPEC:67 | Zero/Empty | no authorizing flag | off | off | OK |
| outward default (WC-9) | SPEC:67, 245 | Typical | flag present and user instruction quoted (D4 a) | on | on | OK |
| outward default (WC-9) | SPEC:100 | Sentinel Value Match | auggie-review `--post-pr`; inventories quote only `--no-post-pr` | flag unverified | "explicit `--post-pr`" | GAP (n-2, minor; UNVERIFIED) |
| retry breaker (WC-6) | SPEC:64; CAPS:80, CAPS:116 | Typical | one or two failed starts | below 3 | retry allowed | OK |
| retry breaker (WC-6) | CAPS:80 | Maximum/Overflow | three consecutive failed starts | breaker trips | Task failed (Orca) | OK |
| retry breaker (WC-6) | SPEC:63; CAPS:80 | Legitimate Edge Case | repeated `blocked` reports | never counted | not specified | GAP (M-11, Medium) |

Classes left out, with the reason. For nested depth: Zero/Empty, One/Minimal, Maximum and Sentinel cannot occur, because the value is an Orca configuration constant that Orca itself clamps to at least 1 (CAPS:100). For the wait split: Zero/Empty and One/Minimal are left out because a wait of zero length cannot starve a heartbeat; Sentinel does not apply. For the confidence floor: Maximum and Sentinel do not apply to a 0..1 score compared with one threshold. For the retry breaker: Zero/Empty and Sentinel do not apply to an attempt counter. Every row has all cells populated, so FR-10 is met and synthesis was not blocked. FR-8 and FR-9: the F-01 and F-02-class GAP rows are graded blocking (concrete wrong outcome); the others are Medium.

=== PIPELINE DIMENSIONAL ANALYSIS (FR-17..FR-21) ===

Trigger met: the coordinator-to-worker-to-report flow has stages where the output count can differ from the input count.

```text
[Inventories: 43 commands] --> [Verdict split] --> [10 ready] [27 needs-change] [6 coordinator-only]   (10+27+6 = 43, conserved)
[27 needs-change] --> [P1: 9] [P2: 11] [P3: 4] [P4: 3]                                                   (27, conserved)
[10 ready]        --> [P1 sections/fixes: 6 = adversarial, cleanup-audit, index-repo, workflow, brainstorm, init-lite]
                      [P2: 4 = reflect, release-split, tdd, troubleshoot]                               (10, conserved)
[Coordinator: N workers] --> [N worker_done, exactly one each (SPEC:63)]
        |--> directory-valued / --output-dir workers --> [N' contract files, N' = N']
        '--> file-valued --output workers (tdd, init-lite) --> [M contract files, M = distinct parent dirs, M <= N]   <-- MISMATCH (F-01)
[Coordinator reads 1 file per report-path]  <-- assumes M = N
```

Counts checked at SPEC:76, 97-125, 159-162 and INV-A:73, INV-B:278. The only count divergence is the contract fan-in; by FR-19 it is CRITICAL, and it is F-01. Scenario: N = 2 tdd workers in `docs/auth/` produce M = 1 contract file while the coordinator reads 2 report paths.

=== EXPERT CONSENSUS AND DISAGREEMENTS ===

- **Consensus.** The decision (Orca coordinates, commands stay the units of work) is well supported by the inventories (SPEC:19-26 against CAPS:97-103, 147-149) and the spec states its own evidence gaps plainly (SPEC:41-45, 271-285). Wiegers, Fowler, Newman and Hightower agree the 10/27/6 split, the phase order and the standalone guarantees (SA-1..SA-6) are sound and testable.
- **Wiegers / Adzic.** Most requirements carry an ID, an owner and evidence. They want concrete sample contract files for success, blocked and partial (none is shown), and a number for WC-1 (M-17).
- **Cockburn.** The primary actor (coordinator) and the person who decides D1..D5 are clear. The blocked-to-resolved scenario lacks its main-success steps after `blocked` (M-11).
- **Fowler / Newman.** The cross-cutting contract is a good move (one installed file, SPEC:52, 264). The path rule in WC-4 is the one structural defect (F-01); the heterogeneous report flags (M-14) and the missing contract version are follow-ups.
- **Nygard / Whittaker.** Failure-mode coverage is good for readiness, depth and stalls. Open: unbounded blocked retries (M-11), the 4-5 minute band (M-07), and nothing about the Orca runtime disappearing mid-run (R2 covers commands, not a running worker; SPEC:34). That last point is a minor note.
- **Crispin / Gregory.** The acceptance suite is thorough but mostly live and single-worker. One gate cannot pass as written (F-02) and no check exercises two parallel workers (F-01).
- **Hightower.** Release and cleanup duties are inherited from Orca (SPEC:73; CAPS:107-113). Contract files written into tracked folders such as `docs/` are a visible side effect worth a line (see F-01 recommendation).
- **Disagreement.** Whittaker would grade M-03 and M-11 blocking; Fowler and Wiegers hold they need a guess about coordinator behavior. Graded Medium under the grading check.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.5
  clarity: 7
  completeness: 7
  testability: 5.5
  consistency: 6.5
critical_issues:
  - {category: architecture, severity: CRITICAL, expert: Fowler/Whittaker, issue: "F-01 contract path collides for file-valued --output", recommendation: "contract directory is always the brief-supplied, per-worker directory"}
  - {category: requirements, severity: MAJOR, expert: Crispin/Wiegers, issue: "F-02 AC-0.4 cannot pass in P0", recommendation: "narrow step 3 to the existing report files for P0"}
expert_consensus:
  - "The coordinator-on-top decision and the evidence behind it hold."
  - "The WC-4 path rule and one acceptance check are the defects that block."
improvement_roadmap:
  immediate: [F-01, F-02]
  short_term: [M-01, M-02, M-03, M-07, M-09, M-10, M-11, M-12]
  long_term: [M-14, contract version field, sample contract files]
adversarial_analysis:
  - {attack: Accumulation, severity: CRITICAL, invariant: "SPEC:62/73", trigger: "two file-valued --output in one directory", trace: "2 workers -> 1 contract file"}
  - {attack: Sequence, severity: MAJOR, invariant: "SPEC:194", trigger: "P0 checked against P1 contract", trace: "no contract exists in P0"}
```

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium: M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08, M-09, M-10, M-11, M-12, M-13, M-14, M-15, M-16, M-17, M-18, plus the two tdd-guard GAP rows.

Minor notes:
- n-1. E2 says the worker "answered" (SPEC:22); the quoted evidence shows only `state: ready, stage: input_accepted` (CAPS:49). Wording overstated.
- n-2. WC-9 and the auggie-review row turn posting back on with "an explicit `--post-pr`" (SPEC:67, 100). The inventories quote only `--no-post-pr` (INV-A:38). Whether `--post-pr` exists is UNVERIFIED.
- n-3. The "prints nothing" pass conditions of AC-C1, AC-C4 and AC-C5 (SPEC:172, 175, 176) also pass vacuously when the command errors (for example an unknown `master` ref). Add an exit-status check.
- n-4. WC-4 states "Orca does not check the file" as fact (SPEC:62); the UNVERIFIED list says it is assumed (SPEC:274; CAPS:79).
- n-5. Section 3.1 is titled "Ready today" and "run as workers now" (SPEC:78-79) while section 1.4 says no command has been run end to end (SPEC:43; INV-B:323). P0 resolves it; the wording could say "ready by reading".
- n-6. With D3(a) recommended (SPEC:240), pr-submit stays with the coordinator, so the effective split is 26 / 7, not 27 / 6 (SPEC:76, 139).
- n-7. `load` is counted among the 27 "needing a change" but its only change is a usage line and it gets no `## Unattended mode` section (SPEC:76, 112).

Per Review Loop bullet 3 the reviewing session asks the user once whether to open an issue for these. This worker's reply channel is limited to one `DONE` line, so the question is not asked and nothing is created; the list is recorded for the coordinator to put to the user.

## Reviser brief

Blocking finding ids: **F-01, F-02**. (Review 1 of 3; the loop may run up to two fix cycles.)

Contract for the reviser (restating Review Loop bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names: F-01 (SPEC:62 WC-4, with at most one sentence in section 2.3, SPEC:73) and F-02 (SPEC:194 AC-0.4, and SPEC:182 only if needed to scope step 3 to P0).
- Add no rule, mechanism or section that a listed finding does not call for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
