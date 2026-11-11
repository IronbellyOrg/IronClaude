review: 2 of 3

# Spec-panel re-review, round 2: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` (no `--unattended`, no `--iterations`; with `--re-review` the Improve step is skipped and no revised specification is written)
- review number: PRIOR `review/round1.md:1` says `review: 1 of 3`, so N = 2. PRIOR's last line (`round1.md:192`) is `verdict: FAIL`, so the "do not review at review 3" check does not apply.
- roles (fixed by the RE-REVIEW prompt table): CANDIDATE = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; BASELINE = `.dev/orca-command-refactor/specs/history/spec-v1.md`; PRIOR = `.dev/orca-command-refactor/review/round1.md`.
- sha256 candidate: `5082997e7df1eb90f5c3852b329722d02c4c86bb728e0f29c56b6b9bb7dfa478` (57803 bytes, 285 lines)
- sha256 baseline: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes, 285 lines); equals the candidate hash recorded at `round1.md:7`, so the baseline is the file round 1 reviewed
- sha256 prior: `b154a5eb9df56fe508ede197d315e5300ad7cefeceefcbe706f8b333e2972625`
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: RE-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:36-49` (read in full first, with the Review Loop section of the command)
- citation keys: `S:N` = line N of the candidate (lines other than 76 and 195 are identical in the baseline); `B:N` = line N of the baseline; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `R1:N` = line N of PRIOR; `README:N` = `.dev/orca-command-refactor/README.md`. Every line cited below was read in this sandbox. Any path outside the workspace (`cmd/*`, `sk/*`, `CLAUDE.md`, `EVIDENCE.md`, Orca guides) is UNVERIFIED here and is used only through an inventory line.
- brief clauses overridden: none.
- issue question (Review Loop bullet 3): this worker cannot ask the user, so it asks nothing and creates no issue; the follow-up candidates below are recorded for the coordinator.

## Step 1: evidence block

Command run: `diff -w BASELINE CANDIDATE`. It prints two hunks (`76c76`, `195c195`). A plain `diff` without `-w` prints the same two hunks, so there is no whitespace-only change to ignore. Changed lines, copied verbatim:

BEFORE (baseline), lines starting `<`:

~~~text
B:76  The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
B:195 | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
~~~

AFTER (candidate), lines starting `>`:

~~~text
S:76  The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command except `load` (B-1) also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
S:195 | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load` (B-1) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
~~~

(The `B:`/`S:` line-number prefixes are mine, not part of the lines.) Net change: two insertions of ` except `load` (B-1)`, 20 bytes each, 57763 to 57803 bytes (`wc -c`); this equals `revise1.md:13-15`. Nothing was deleted.

## Prior blocking findings

| id | prior state | re-check against AFTER text only | state |
|---|---|---|---|
| B-1 | blocking, confirmed (`round1.md:2`, `verify-1.md:7-9`) | The defect was that AC-1.1 required a `## Unattended mode` section on every 3.1-3.2 command, `/sc:load` included, while the load row (S:112: Report "none (see note)", Phase "P1 (usage line only)") and the Decision (S:265: "a report file would be an unrequested addition. Only its usage-line defect is fixed.") say load gets no contract. AFTER S:195 now reads "every command in sections 3.1-3.2 except `load` (B-1)", and AFTER S:76 reads "Every changed command except `load` (B-1) also gains the section". S:112 and S:265 are unchanged and now agree with S:195. AC-1.1 passes whether or not load has the section, so the criterion can be passed with the load row as written. | resolved |
| B-2 | blocking (`round1.md:23`, `round1.md:190`) | Not edited: `diff -w` shows no change to S:62, S:73, S:87, S:90, S:183 or S:200. WC-4 at S:62 still reads "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; the init-lite row at S:87 still reads "Brief must pass: `--output <file>`"; the tdd row at S:90 still reads "`--output <file>`" and "the TDD at `--output`"; AC-2.2 at S:200 still runs `/sc:tdd "auth" --unattended --output <file>` and expects "contract `status: blocked` with a non-empty `blocked_question`". The inventories agree that tdd's `--output` is the TDD file (`INV-B:47`, `INV-B:222`) and init-lite's is a file (`INV-A:55`). The reviser did not touch it (`revise1.md:4`: "B-2 is not in IDS and is not touched"). | open |

Process note for the coordinator (not a finding): B-2 never went through the VERIFY step. `findings-1.md:1-4` holds only B-1 and `verify-1.md:9` ends `confirmed: B-1`. The verification line at `round1.md:2` says the Reviser brief "is narrowed to the confirmed ids" and lists no rejected id, yet `round1.md:188-190` still lists B-2 as a blocking finding. No verification block rejects B-2, so it is not a `noted, unactioned` id; the reviser left it unrevised, and a deferred finding counts as open (Review Loop bullet 5). I therefore carry B-2 as open. I re-checked its quoted texts and the stated wrong outcome myself (table above and the grading sentence below), but that is not a fresh-context verification. Before the next revision, the coordinator should run the VERIFY prompt on B-2.

Corroboration only, not used for grading: the definition of this very command (`command.md:460`) says "`--report-dir <dir>` only (`--output` is file-valued)", i.e. the command treats a file-valued `--output` and a separate report directory as different flags, which is the distinction WC-4 lacks.

## Findings table

| id | grade | origin | expert | one line | location |
|---|---|---|---|---|---|
| B-1 | blocking, resolved | changed | Wiegers | AC-1.1 vs the load row and Decision; fixed by the `except `load`` clause | S:195, S:76, S:112, S:265 |
| B-2 | blocking, open | unchanged (prior) | Fowler | WC-4 defines `<output-dir>` as the `--output` value, but tdd and init-lite pass a file | S:62, S:87, S:90, S:200, S:183 |
| M-15 | Medium | unchanged | Adzic | AC-1.2 runs the live check on "each P1 command", and S:159 lists `load` as one; load writes no contract, so step 4 cannot pass for it | S:196, S:159, S:183, S:112, S:195 |
| N-6 | minor | changed | Wiegers | the review id `(B-1)` sits inside two normative sentences, so a test author meets an id the spec never defines | S:76, S:195 |
| N-7 | minor | unchanged | Wiegers | S:52 "Each changed command adds a short `## Unattended mode` section" has no `load` exception; S:76 carries it | S:52, S:76 |

## === REQUIREMENTS ANALYSIS ===

### B-1 (resolved)
Wiegers: the narrowing is the one-clause option round 1 preferred (`round1.md:49`). The two sentences that scoped the section to all 3.1-3.2 commands (S:76, S:195) now name the exception; the texts that supported the exception (S:112, S:265, `INV-B:65`: "writes no file, so a worker has nothing to report") were left alone. SA-4 (S:149) already lists the load usage line as the one named defect fix, so the additivity rule is consistent with AFTER. The reviser stayed in scope: only text B-1 names (S:76 and S:195 are both cited in B-1's body, `round1.md:47`), each addition carries `(B-1)`, bytes added 40 and deleted 0 per `revise1.md:13-22`, which I reproduced with `wc -c`.

### M-15 (MAJOR label, Medium, priority Low, Adzic), origin=unchanged, quotes the changed line
Texts: the changed AC-1.1 at S:195, "every command in sections 3.1-3.2 except `load` (B-1)", sets that load has no section and no contract (S:112 "none (see note)"). The neighbouring AC-1.2 at S:196 reads "7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass", and P1 at S:159 lists "load (usage line only)" in its Commands column. Step 4 of 7.2 (S:183) runs `test -s <contract>`, and step 3 (S:182) needs "its report path is the WC-4 contract path". For load there is no contract.
Why Medium and not blocking: the sentence "an implementer builds AC-1.2 against load and step 4 fails" needs the guess that "each P1 command" includes a command whose own row says "use it as a step inside another worker's brief, not as its own Task" (S:112); both readings are allowed. It surfaces only because the changed line made load's missing contract explicit. Same family: WC-4 (S:62) says "In unattended mode the command writes" the contract, and S:159 has load accept `--unattended`.
Recommendation (follow-up, not a revision): one clause "except `load`" in AC-1.2, or say that a load run needs no contract.

### Adzic scenarios (state traces, changed behaviour only)
1. Given the AC-1.1 test and the 36 commands other than load: each must have a section naming both strings; load may or may not. Before: 37 required, load fails. After: 36 required, load free. OK.
2. Given `/sc:load --unattended` run as P1's last command (S:159): no gate, no contract (S:112); AC-1.2 step 4 fails. See M-15.

## === ARCHITECTURE ANALYSIS ===

### B-2 (open, blocking, priority High, Fowler)
Texts as in the prior-findings table above. Grading sentence (FIRST-REVIEW form, re-applied to the AFTER text): An implementer who follows the stated text as written takes `<output-dir>` to be the value of `--output`, which for tdd is the TDD file (S:90), so the contract path is `<TDD file>/return-contract.yaml`, a path beneath a regular file that cannot be created, and X is wrong because AC-2.2 (S:200) and step 4 of 7.2 (S:183) then cannot read the contract that WC-4 says is written on every outcome, including blocked. WC-4 (S:62) says the `--output` value is a directory; S:87 and S:90 say it is a file. Two stated texts contradict, and an acceptance criterion cannot pass as written. The grade holds; no further assumption is needed.
Narrowest repair: in WC-4, say where the contract goes when `--output` is a file (a named sibling directory or a separate report-directory flag), one sentence, and make the init-lite and tdd rows and AC-2.2 agree with it.

### Newman / Hohpe / Nygard on the changed lines
The edit changes only a documentation scope and a test assertion. It adds no interface, no message path and no failure mode. No finding.

## === ADVERSARIAL ANALYSIS (Whittaker, changed lines and prior blockers only) ===

1. I can break this specification by **Sentinel Collision Attack**. The invariant at **S:195 (exempt command is named `load`)** fails when **a command name merely contains or equals the sentinel in some other role**. Concrete attack: the test exempts by name; the 43 commands (`INV-A:3`, `INV-B:3`) include no other name containing `load`, so before: 36 commands asserted; after a future `/sc:upload`-style command with a substring test: asserted 35. Not a defect today. Minor, no id (nothing wrong in the current text).
2. I can break this specification by **Divergence Attack**. The invariant at **S:76 and S:195 (load has no section, but still accepts `--unattended`, S:159)** fails when **a person or coordinator passes `--unattended` to load**. Concrete attack: before: `/sc:load --unattended` is not a documented form; after: S:159 says it is accepted as a no-op, WC-4 says unattended commands write a contract, S:112 says none. The three texts disagree about load's output. Graded Medium (M-15), because the spec says load is not dispatched as a Task.
3. I can break this specification by **Zero/Empty Attack** on the open blocker. The invariant at **S:62 (contract written on every outcome)** fails when **`--output` is a file**. Concrete attack: `/sc:tdd "auth" --unattended --output docs/auth/TDD.md`; contract path `docs/auth/TDD.md/return-contract.yaml`; before write: `docs/auth/TDD.md` is a file or absent; after: no contract. Open, B-2.

## Guard Condition Boundary Table (changed lines only; Nygard builds, Crispin validates, Whittaker attacks)

Guard on the changed lines: the exemption "except `load`" in S:76 and S:195. Input = the command under the AC-1.1 test.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| except-`load` exemption | S:195 | Typical | `analyze` (3.2, not load) | false | section required, names both strings | OK |
| except-`load` exemption | S:195, S:76 | Legitimate Edge Case | `load` | true | no section required; S:112 and S:265 agree | OK |
| except-`load` exemption | S:195 | Sentinel Value Match | any other command name containing `load` | false | none exists in `INV-A:3`, `INV-B:3`; exact name `load` is exempt | OK |
| except-`load` exemption | S:195 | Legitimate Edge Case | a section-4 command (guard false) | false | no section allowed (second clause of S:195) | OK |
| except-`load` exemption | S:159, S:62, S:196 | Legitimate Edge Case | `load` run with `--unattended` | true | AC-1.1 silent on a contract; WC-4 says write one; row S:112 says none; AC-1.2 says run the live check | GAP (M-15) |

Classes left out: Zero/Empty (the exemption set has exactly one member, so an empty list cannot occur), One/Minimal (same as Typical for a name match), Maximum/Overflow (not input-sized). FR-8/FR-9 grading: the one GAP names no wrong outcome that follows without assuming which reading of "each P1 command" the implementer picks, so it is Medium. The table is complete for the changed lines (FR-10 met).

## Quantity Flow Diagram (the changed lines alter an expected count)

~~~text
[Source: 43 commands (INV-A 21 + INV-B 22; S:76)]
   --> [verdict split] --> 10 (3.1, S:81-92) + 27 (3.2, S:98-125) + 6 (section 4, S:130-137) = 43      (conserved)
   --> [Consumer: AC-1.1 section test]
         before the edit: expects 37 (3.1 + 3.2)   -- load fails                     <-- MISMATCH (B-1)
         after the edit:  expects 36 (37 - load)   -- load exempt (S:195)            (resolved)
   --> [Consumer: phase Commands lists S:159-162]
         P1 9 + 4 fixes = 13 (load among them)  P2 15  P3 4  P4 3  = 35 listed
         sections owed by phase lists = 35 - load = 34 versus 36 expected             <-- 2 short: brainstorm, init-lite (in no list)
   --> [Consumer: section-4 clause] expects 0 of 6
   --> [Consumer: AC-1.2 "each P1 command" (S:196)] 13 listed, load among them, expects a contract from all   <-- M-15
~~~

The 2-command gap (brainstorm and init-lite appear in no phase list, S:84, S:87) is the same count round 1 recorded as a Medium (`round1.md:30`) and the edit neither adds nor removes it; it stays an unchanged follow-up. The arithmetic checks out: P1 13 (S:159), P2 15 (S:160), P3 4 (S:161), P4 3 (S:162).

## Minor notes

- N-6: `(B-1)` inside S:76 and S:195 is a review id in normative text. The spec defines no B-1; the test author sees a bare id. Replace with a pointer to S:112 or delete the id when the finding is closed.
- N-7: S:52 states that each changed command adds the section, and load is a changed command (usage line). The reviser noted this (`revise1.md:37`). S:76 carries the exception and a specific sentence outranks a general one, so no implementer is misled; it is a note.

## Self-check before the verdict

Commands run in the workspace:
- `grep -nFxf` of each AFTER line (without `>`) against the candidate: found at S:76 and S:195.
- the same for each BEFORE line (without `<`) against the baseline: found at B:76 and B:195.
- the BEFORE lines against the candidate and the AFTER lines against the baseline: no match in either, so the roles are not swapped.
- `wc -l`: 285 lines in each file; `wc -c`: 57803 and 57763.

The AFTER text is consistent with SA-4 (S:149), the load row (S:112), the Decision (S:265), the P1 scope sentence (S:159) and `INV-B:65`. It is not fully consistent with AC-1.2 and WC-4 for a load run, recorded as M-15 (Medium, not blocking).

## Coverage

Whole-document assurance is not claimed. Covered: the two changed lines (S:76, S:195) and everything that cites or depends on them (S:52, S:62, S:112, S:149, S:159-162, S:182-183, S:196, S:265, `INV-B:65`, `INV-B:31`); the reviser report (`revise1.md`) for scope and byte accounting; both prior blocking findings (B-1 resolved, B-2 open) re-read against the AFTER text; the Guard Condition Boundary Table for guards on changed lines only; the quantity flow for counts that the edit moves; the whole README and the verification trail (`findings-1.md`, `verify-1.md`). Not covered: unchanged text outside the prior blockers; the round-1 Medium and minor findings were not re-graded (their texts are unchanged). Round-1 lines are not re-listed because none is a prior blocking finding.

## Follow-up candidates (Medium and minor; none triggers a revision)

M-15, N-6 and N-7 above, plus the round-1 Medium and minor list at `round1.md:182-183` (unchanged text, not re-checked). Open an issue for them only if the user says so; this run recorded the list and asked nothing.

## Reviser brief

Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone, including M-15, N-6 and N-7. Return the candidate once and do not award yourself a PASS. This is review 2 of 3: one fix cycle remains after this one, and the loop escalates to the user if B-2 is still open at review 3.

Blocking findings:
- B-2. Texts: WC-4 at S:62, "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; the init-lite row at S:87, "Brief must pass: `--output <file>`"; the tdd row at S:90, "`--output <file>`" and "the TDD at `--output`"; AC-2.2 at S:200, "`/sc:tdd "auth" --unattended --output <file>`" expecting "contract `status: blocked` with a non-empty `blocked_question`". Wrong outcome: an implementer who follows the stated text as written writes the tdd contract at `<--output value>/return-contract.yaml`, a path beneath the TDD file that cannot be created, and AC-2.2 step 4 (S:183) cannot read a contract. WC-4 says `--output` is a directory; the tdd and init-lite rows say it is a file.

verdict: FAIL
