review: 3 of 3

# Spec-panel re-review, round 3: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md` (no `--unattended`, no `--iterations`; with `--re-review` the Improve step is skipped and no revised specification is written)
- review number: PRIOR `review/round2.md:1` says `review: 2 of 3`, so N = 3. PRIOR's last line (`round2.md:149`) is `verdict: FAIL`, but the "do not review" halt applies only to a prior at `review: 3`, so the review runs.
- roles (fixed by the RE-REVIEW prompt table): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v2.md`; PRIOR = `.dev/orca-command-refactor/review/round2.md`.
- sha256 candidate: `de92cfbd1e91f7c9b127746790c558a078c2ca7c0cfa873d862dfcbd0dab1bb9` (58026 bytes, 285 lines)
- sha256 baseline: `5082997e7df1eb90f5c3852b329722d02c4c86bb728e0f29c56b6b9bb7dfa478` (57803 bytes, 285 lines); equals the candidate hash recorded at `round2.md:9`, so the baseline is the file round 2 reviewed
- sha256 prior: `902739a1d42fe4091a8982eb173620dd44ab92c27d1e8b1e21b49bb95b9dfd97`
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:36-49` (read in full first), with the Review Loop section of the command (`command.md:256-264`).
- citation keys: `S:N` = line N of the candidate (all lines other than 62 and 200 are identical in the baseline); `B:N` = line N of the baseline; `INV-A:N`, `INV-B:N` = line N of `inventory/commands-a.md`, `commands-b.md`; `R2:N` = line N of PRIOR; `REV2:N` = line N of `review/revise2.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Every line cited was read in this sandbox. Paths outside the workspace (`cmd/*`, `sk/*`, Orca guides) are UNVERIFIED here and are used only through an inventory line.
- brief clauses overridden: none.
- issue question (Review Loop bullet 3): this worker cannot ask the user, so it asks nothing and creates no issue; the follow-up candidates below are recorded for the coordinator.
- verification block: PRIOR carries a verification line (`R2:2`) naming B-2 as confirmed and no rejected id. `verify-2.md` ends `confirmed: B-2`. B-2 therefore counts as a prior blocking finding.

## Step 1: evidence block

Command run: `diff -w BASELINE CANDIDATE`. It prints two hunks (`62c62`, `200c200`); a plain `diff` prints the same two, so there is no whitespace-only change. Changed lines, copied verbatim (the `B:`/`S:` prefixes are mine; the long WC-4 row is quoted up to the end of the changed sentence and the rest of the row is identical on both sides):

BEFORE (baseline), lines starting `<`:

~~~text
B:62  | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: ... [rest of row identical]
B:200 | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
~~~

AFTER (candidate), lines starting `>`:

~~~text
S:62  | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`), or, for a command whose `--output` is a file (init-lite, tdd), that file's parent directory, which the coordinator dedicates to this one run (B-2). It follows the return-contract pattern several commands already use and carries at least: ... [rest of row identical]
S:200 | P2 | AC-2.2 | Gate-trigger run per P2 command: a 7.2 live check with input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file>` with a bare topic, so the contract is read from the parent directory of `<file>` (WC-4, B-2); `/sc:cli-eval run --unattended` with no `--suite`) | `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`; step 2 never shows `agentWait` |
~~~

Net change: two pure insertions, 148 bytes in S:62 and 75 bytes in S:200, 57803 to 58026 bytes (`wc -c`), which equals `REV2:9-13,21`. Nothing was deleted.

## Prior blocking findings

| id | prior state | re-check against AFTER text only | state |
|---|---|---|---|
| B-1 | resolved in round 2 (`R2:42`) | Not edited by this diff. AFTER S:76 still reads "Every changed command except `load` (B-1) also gains the `## Unattended mode` section" and AFTER S:195 still reads "every command in sections 3.1-3.2 except `load` (B-1)"; S:112 ("none (see note)") and S:265 ("a report file would be an unrequested addition") agree with both. It does not fail again. | resolved |
| B-2 | blocking, confirmed (`R2:2`, `R2:43`, `R2:147`) | The defect was that WC-4 defined `<output-dir>` as the `--output` value while the init-lite row (S:87, "`--output <file>`") and the tdd row (S:90, "`--output <file>`", "the TDD at `--output`") pass a file, so the contract path would sit beneath a regular file. AFTER S:62 now says that for a command whose `--output` is a file (init-lite, tdd) the contract goes in "that file's parent directory, which the coordinator dedicates to this one run". S:87 and S:90 are unchanged and now agree with it. AFTER S:200 says the AC-2.2 tdd contract "is read from the parent directory of `<file>`". Step 4 of 7.2 (S:183, `test -s <contract>`) and step 3 (S:182, "its report path is the WC-4 contract path") take the path from WC-4, so a tdd run with `--output docs/auth/TDD.md` has the contract `docs/auth/return-contract.yaml`, which can be created and read. The two contradicting texts no longer contradict, and AC-2.2 can pass as written. The inventories agree on the file meaning (`INV-B:222`, `INV-B:225`, `INV-A:55`). | resolved |

## Findings table

| id | grade | origin | expert | one line | location |
|---|---|---|---|---|---|
| B-1 | blocking, resolved | unchanged | Wiegers | still resolved; S:76 and S:195 untouched | S:76, S:195 |
| B-2 | blocking, resolved | changed | Fowler | WC-4 now names the parent directory for a file-valued `--output` | S:62, S:87, S:90, S:183, S:200 |
| M-16 | Medium | changed | Fowler | the file-valued list "(init-lite, tdd)" is closed, while S:120 adds an `--output` to spec-panel and S:99, S:106, S:107, S:111 add one to others with no stated shape | S:62, S:120, S:196 |
| M-17 | Medium | changed | Nygard | "the coordinator dedicates [the parent directory] to this one run" is stated only in WC-4; the brief rule (S:73) and the tdd/init-lite rows do not repeat it, and a bare file name has the worktree root as parent | S:62, S:73, S:87, S:90 |
| M-15 | Medium | unchanged | Adzic | carried from round 2: AC-1.2 "each P1 command" includes `load`, which writes no contract | S:196, S:159, S:112 |
| N-6 | minor | changed | Wiegers | carried and extended: review ids `(B-1)`, now also `(B-2)` and `(WC-4, B-2)`, sit inside normative sentences and an acceptance criterion; the spec defines no B-2 | S:62, S:76, S:195, S:200 |
| N-7 | minor | unchanged | Wiegers | carried: S:52 has no `load` exception, S:76 does | S:52, S:76 |

No new blocking finding. The round-1 Medium and minor list (`R2:140`) is unchanged text and was not re-graded.

## === REQUIREMENTS ANALYSIS ===

### B-2 (resolved)
Wiegers: the repair is the one-sentence option round 2 asked for ("Narrowest repair", `R2:77`): a rule in WC-4 for the file-valued case, with the init-lite and tdd rows and AC-2.2 made to agree. The rows at S:87 and S:90 needed no edit because they already said `--output <file>`. The reviser stayed in scope: only text B-2 names was touched (S:62 and S:200, both in B-2's brief at `R2:147`), each addition carries `(B-2)`, no flag, mechanism or section was added, and 223 bytes were added and 0 deleted (`REV2:13,21`), which I reproduced with `wc -c`.

### M-16 (MAJOR label, Medium, priority Low, Adzic), origin=changed
Texts: the new WC-4 clause covers "a command whose `--output` is a file (init-lite, tdd)". The spec also gives other commands an output flag it does not shape: spec-panel "add `--output`; contract" (S:120), and analyze, design, document, index "add an output path; contract" (S:99, S:106, S:107, S:111). AC-1.2 (S:196) runs P1 commands with `--output <dir>`, while AC-2.2 (S:200) runs tdd with `--output <file>`.
Why Medium and not blocking: the sentence "an implementer builds the spec-panel contract at `<--output>/return-contract.yaml`, and X is wrong because `--output` is a file there" needs the guess that the implementer defines the new flag as a file; the spec states no such meaning, so it is a requirement the document never states (an unspecified edge case) and not a stated text that does harm. The first clause of WC-4 (`<output-dir>`) covers the directory reading. Recommendation (follow-up, not a revision): say in S:62 that a newly added flag is directory-valued, or list the file-valued commands as "every command whose `--output` is a file", not a closed list.

### M-17 (Medium, priority Low, Nygard), origin=changed
Texts: S:62, "that file's parent directory, which the coordinator dedicates to this one run (B-2)"; S:73, "the output directory, so the report path is known before dispatch (WC-4)"; S:87 and S:90 repeat only `--output <file>`.
Why Medium: the dedication duty is in WC-4, which an implementer of the contract reads, so a stated text does not do harm. The harm appears only if the coordinator passes a file in a shared directory (for example two tdd workers both writing into `docs/auth/`, or a bare `TDD.md` whose parent is the worktree root); then both runs write one `return-contract.yaml`, which WC-11 (S:69, "Two workers in one worktree must never write the same file") forbids. That needs a coordinator that ignores WC-4, so it is a guess and not a contradiction. Recommendation: one clause in S:73 ("for a file-valued `--output`, the file sits in its own directory").

### M-15 (carried, unchanged text)
`load` and AC-1.2: S:196 "each P1 command", S:159 lists "load (usage line only)", S:112 says no contract. Not touched by the diff and not re-graded; still Medium.

### Adzic scenarios (state traces, changed behaviour only)
1. Given `/sc:tdd "auth" --unattended --output docs/auth/TDD.md` with a bare topic: before the edit, contract path `docs/auth/TDD.md/return-contract.yaml` (cannot be created); after, `docs/auth/return-contract.yaml`, `status: blocked`, `blocked_question` non-empty, `worker_done --outcome failed`; 7.2 steps 3 and 4 read it. OK.
2. Degenerate input: `--output TDD.md` (no directory part). After: parent is `.`, so the contract is `./return-contract.yaml` in the worktree root; the "dedicated to this one run" condition does not hold, and a second run overwrites it. Not wrong under the text if the coordinator follows WC-4; see M-17.
3. Given `/sc:init-lite --unattended --output .dev/superclaude/context-audit.md`: contract `.dev/superclaude/return-contract.yaml`; consistent with S:87. OK.

## === ARCHITECTURE ANALYSIS ===

### Fowler / Newman / Hohpe / Nygard on the changed lines
The edit gives WC-4 one extra resolution rule for `<output-dir>`; the contract schema, status values, `worker_done --report-path` hand-off (S:62) and 7.2 steps are unchanged. The contract's location is still known before dispatch (the parent of a known file), which keeps the WC-4 title claim true. The interface stays segregated: one path rule in WC-4, referenced by the rows and AC-2.2 and not duplicated in S:87 or S:90. The one weak point is the closed list of file-valued commands (M-16) and the dedication duty living in one place (M-17). Both are Medium. No architecture finding is blocking.

## === ADVERSARIAL ANALYSIS (Whittaker, changed lines and prior blockers only) ===

1. I can break this specification by **Zero/Empty Attack**. The invariant at **S:62 (contract is in the parent directory of a file-valued `--output`)** fails when **`--output` has no directory part**. Concrete attack: `/sc:tdd "x" --unattended --output TDD.md`; parent = `.` (worktree root); before: no contract anywhere reachable; after: `./return-contract.yaml`, shared by any later run in the same worktree. The text still gives a defined path; the collision needs a coordinator that breaks the "dedicated" clause. Medium (M-17).
2. I can break this specification by **Divergence Attack**. The invariant at **S:62 (two readings of `<output-dir>`)** fails when **a newly added `--output` is file-valued but not in the list**. Concrete attack: spec-panel gets `--output report.md` (S:120); first clause says `report.md/return-contract.yaml`; second clause does not apply because spec-panel is not listed. Not a stated-text contradiction because S:120 never says the new flag is a file. Medium (M-16).
3. I can break this specification by **Sequence Attack** on the 7.2 steps. The invariant at **S:182-183 (path from WC-4)** fails when **a tdd run is blocked before the parent directory exists**. Concrete attack: `--output new/dir/TDD.md`, blocked at the topic gate; WC-4 says the contract is written on stops before any other output (S:62), so the command creates the parent; the spec says nothing about creating it. Inferrable from "written on every outcome"; Minor, no id.
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:62, S:200 (`B-2` as a normative tag)** fails when **a test author greps for an id**. Concrete attack: the spec defines no B-2, so the tag has no target. Minor (N-6).

## Guard Condition Boundary Table (changed lines only; Nygard builds, Crispin validates, Whittaker attacks)

Guard on the changed lines: "a command whose `--output` is a file (init-lite, tdd)" in S:62, and its use in S:200.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| file-valued `--output` | S:62 | Typical | tdd `--output docs/auth/TDD.md` | true | contract at `docs/auth/return-contract.yaml`; S:90, S:200 agree | OK |
| file-valued `--output` | S:62 | Legitimate Edge Case | init-lite `--output .dev/superclaude/context-audit.md` | true | contract in `.dev/superclaude/`; S:87 agrees | OK |
| file-valued `--output` | S:62, S:196 | Typical | directory-valued `--output <dir>` (adversarial, brainstorm, P1 commands) | false | contract at `<dir>/return-contract.yaml` | OK |
| file-valued `--output` | S:62 | Zero/Empty | bare file name, no directory part | true | parent is the worktree root; "dedicated to this one run" cannot hold; no further behaviour stated | GAP (M-17) |
| file-valued `--output` | S:62, S:120 | Sentinel Value Match | a newly added `--output` (spec-panel, S:120) not in the closed list | not stated | no rule says which reading applies | GAP (M-16) |
| file-valued `--output` | S:62 | One/Minimal | `--output` omitted | n/a | S:87 and S:90 require the brief to pass `--output`; WC-4 and S:73 require the output directory in the brief | OK |

Classes left out: Maximum/Overflow (the path is not input-sized). FR-8/FR-9 grading: each GAP names no wrong outcome that follows without assuming which reading or which coordinator behaviour applies, so both are Medium. The table is complete for the changed lines (FR-10 met).

## Quantity Flow Diagram (the changed lines move no count)

~~~text
[Source: 43 commands (INV-A 21 + INV-B 22; S:76)]
   --> [verdict split] --> 10 (3.1) + 27 (3.2) + 6 (section 4) = 43      (conserved, unchanged by this diff)
   --> [Consumer: WC-4 contract path]
         directory-valued --output : N commands, path <dir>/return-contract.yaml
         file-valued --output      : 2 listed (init-lite, tdd), path <parent>/return-contract.yaml   (S:62)
         newly added --output      : spec-panel + the S:99/106/107/111 commands, shape not stated    <-- M-16
   --> [Consumer: AC-1.1 section test] 36 expected (37 - load)   (S:195, unchanged)
   --> [Consumer: AC-1.2 "each P1 command"] 13 listed, load among them                              <-- M-15 (carried)
~~~

The 2-command gap (brainstorm and init-lite in no phase list) is unchanged text from round 1 and round 2 (`R2:117`); not re-graded.

## Minor notes

- N-6 (extended): `(B-2)` in S:62 and `(WC-4, B-2)` in S:200 add a review id to normative text, as `(B-1)` already does in S:76 and S:195. Replace each with a pointer to S:62 or delete the id once the review is closed.
- N-7 (carried): S:52 has no `load` exception; S:76 carries it.

## Self-check before the verdict

Commands run in the workspace:
- `grep -nFxf` of each AFTER line (without `>`) against the candidate: found at S:62 and S:200.
- the same for each BEFORE line (without `<`) against the baseline: found at B:62 and B:200.
- the BEFORE lines against the candidate and the AFTER lines against the baseline: no match in either, so the roles are not swapped.
- `wc -l`: 285 lines in each file; `wc -c`: 57803 (baseline) and 58026 (candidate); `diff` prints 4 changed lines (two hunks).

The AFTER text is consistent with the init-lite row (S:87), the tdd row (S:90), step 3 and 4 of 7.2 (S:182-183), AC-2.2's expected result (S:200), WC-11 (S:69) read together with the "dedicates" clause, and the inventories (`INV-B:222,225`, `INV-A:55`). It is not fully consistent with the spec's own newly added output flags (S:99, S:106, S:107, S:111, S:120), recorded as M-16 (Medium, not blocking).

## Coverage

scoped PASS: changed lines + prior blockers

Whole-document assurance is not claimed. Covered: the two changed lines (S:62, S:200) and everything that cites or depends on them (S:69, S:73, S:87, S:90, S:99, S:106, S:107, S:111, S:112, S:120, S:159, S:182-185, S:195-196); the reviser report (`revise2.md`) for scope and byte accounting; both prior blocking findings (B-1 still resolved, B-2 now resolved) re-read against the AFTER text; the verification trail for B-2 (`verify-2.md`); the Guard Condition Boundary Table for guards on changed lines only; the quantity flow for counts the edit moves; the README (`README:1-38`). Not covered: unchanged text outside the prior blockers; the round-1 Medium and minor findings and M-15, N-7 were carried and not re-graded (their texts are unchanged). This run found no severe defect in older text and records none as newly discovered.

## Follow-up candidates (Medium and minor; none triggers a revision)

M-16, M-17, M-15, N-6 and N-7 above, plus the round-1 Medium and minor list at `round1.md:182-183` as carried in `R2:140` (unchanged text, not re-checked). Open an issue for them only if the user says so; this run recorded the list and asked nothing.

No Reviser brief is written: at `review: 3` with no open blocking finding there is nothing to revise, and a fourth review does not start.

verdict: PASS
