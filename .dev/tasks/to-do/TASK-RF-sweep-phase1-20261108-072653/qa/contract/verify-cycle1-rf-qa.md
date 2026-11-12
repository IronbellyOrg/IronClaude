# Verify report, contract gate cycle 1 (rf-qa, T275)

**Date:** 2026-11-12
**Phase:** fix-cycle verification (fix_authorization: false)
**Fix cycle:** 1
**Inputs:** `consolidated-findings-cycle0.md` (F_0 = CON-F1, CON-F2), `fix-log-cycle1.md`, `cycle-ledger.md` (82 cycle-0 PASS ids), live files named in the prompt.

## Method

Judged against the live files, not the fix log. Read now: `src/superclaude/core/WORKER-CONTRACT.md` (whole file), `src/superclaude/commands/sweep.md`, `tests/commands/test_sweep_command.py`, `tests/skills/test_worker_contract.py` (write-verb section), the consolidated findings, fix log, cycle ledger, OQ-3 addendum, the seven cycle-0 reports, and the saved results `step-1.17-checks.md`, `r7-check.md`, `phase12-validation.md`. Ran read-only: `git diff`, `grep`, `cmp`, `md5sum`, `diff`, `sha256sum -c`, `uv run pytest`, `uv run ruff`. No repository file was written except this report. Private copies lived under `/tmp/ironclaude-batch.*` and were removed by an exit trap. No mutation experiment was run (see the note under the Checks table).

Change set proved from disk. The executor saved pre-fix copies under `.dev/implement/task-rf-sweep-phase1-202-c7ea3265/work/T274/before/`. Compared with the live files:

- `sweep.md`: `diff` shows exactly one changed line, line 20.
- `WORKER-CONTRACT.md`: the only differing words on line 277 are `wake,` becoming `wake or wait timeout,`. Four diff lines in total.
- `docs/designs/orchestrator-mode.md`: the same word change on line 679 and nothing else.
- `step-1.17-checks.md`: 0 removed lines; the new section "Re-run after the cycle-1 fix" is appended at line 76 to the end.
- `sha256sum -c` over `protected-before.sha256`: 63 of 63 files OK. The list covers `tests/skills/test_worker_contract.py`, the developer guide, both OQ records, `r7-check.md`, `phase12-validation.md`, `step-1.19-pytest.txt`, `sc-sweep-protocol/SKILL.md` and `src/superclaude/cli/sweep/*.py`.
- Whole-contract compare against `HEAD`: lines 1-273 except line 23 are identical, and line 275 to the end of HEAD equals line 279 to the end now. Lines 110 and 151 are identical to HEAD.

## Findings

### CON-F1 (MAJOR): RESOLVED

Defect was `sweep.md` giving the coordinator an uncapped "on every wake" cadence against WC-16 and contract line 110.

- `src/superclaude/commands/sweep.md:20` now reads: "Explicit only: the coordinator runs `/sc:sweep` inside its liveness sweep pass, at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`), or a person types it. Nothing starts it automatically."
- It carries the 5-minute cap and names WC-16, matching `src/superclaude/core/WORKER-CONTRACT.md:277` ("at most once every 5 minutes ... runs `/sc:sweep`", "in the same pass") and `:110` ("at most once every 5 minutes"). "inside its liveness sweep pass" agrees with WC-16's "is not a second pass".
- `grep -n 'every wake'` over `sweep.md`, `src/superclaude/skills/sc-sweep-protocol/`, `src/superclaude/core/HOW-WE-WORK.md` and the developer guide finds no cadence text there; the only hits in the checked files are contract `:110` and `:277`, which carry the cap.
- Wording constraints of the command tests hold for the whole file, not just line 20 (see "Command-test wording constraints" below).

### CON-F2 (MAJOR): RESOLVED

Defect was WC-16 tying the pass to "every coordinator wake" while line 110 runs the sweep after "every wake or timeout".

- `src/superclaude/core/WORKER-CONTRACT.md:277` now says "When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake or wait timeout, at most once every 5 minutes, the coordinator runs "The sweep." ... unchanged and, in the same pass, runs `/sc:sweep`". A quiet timeout is now named as a trigger, so `/sc:sweep` runs when all workers are silent. This agrees with `:110` ("After every wake or timeout") and the 300000 ms wait at `:101`.
- The pinned phrase `On every coordinator wake` is still a substring: `grep -c` on the contract gives 1 (line 277). `tests/skills/test_worker_contract.py` passes: 742 passed on the file alone, 2641 passed on `tests/skills tests/core tests/commands tests/recommend`.
- Contract and DESIGN stayed in step: `sed -n 275,277p` of the contract and `sed -n 677,679p` of `docs/designs/orchestrator-mode.md` are `cmp`-identical (1855 bytes each, 16 more than the cycle-0 figure of 1839, which is exactly the 16 characters " or wait timeout"). `md5sum` of contract line 277 equals that of DESIGN line 679 (`58262e3f5b38d2c18dc4af7bd9eb8442`).
- The change is the one the owner approved in `phase-outputs/plans/OQ-3-addendum-wc16-wait-timeout-decision.md` (status RESOLVED, "Approve both fixes"), and nothing outside the three approved places changed.

### Command-test wording constraints (the new `sweep.md` sentence)

Held. Evidence, all on the live file:

- `tests/commands/test_sweep_command.py:34-36` defines `_FORBIDDEN_ADVICE` (stop, retry, release, merge, removal); the test using it, `test_sweep_skill_has_no_stop_retry_release_merge_removal_advice` (`:167`), reads the skill, not the command file. Even so, `grep -niE 'stop|retry|release|merge|removal'` over the whole of `sweep.md` prints nothing, and `grep -nP '\x{2014}|\x{2013}'` (em dash, en dash) prints nothing.
- The command-file tests (`:106-165`) still hold: `allowed-tools` literal unchanged; `## Activation` block unchanged; `## Unattended mode` count 0 and `--unattended` count 0; `src/superclaude/` count 0.
- The write-verb audit regex (`tests/skills/test_worker_contract.py:1959-1962`, scans `src/superclaude/commands`) has no hit in `sweep.md`; `test_every_write_verb_hit_is_classified` passes in the full run.
- `uv run pytest tests/skills tests/core tests/commands tests/recommend -q`: 2641 passed. `uv run ruff check tests/skills/test_worker_contract.py`: All checks passed. `uv run ruff format --check`: 1 file already formatted.

## Checks

All 82 ids of the cycle-0 PASS set, in the order of `cycle-ledger.md`. "Unchanged" below means the file is in `protected-before.sha256` and its hash still matches (63 of 63 OK), or the pre-fix copy under `work/T274/before/` differs from the live file only in the words named in the Method section. Five rows (`qa-test-pins-report:C9`, `qa-test-pins-report:C12`, `qa-r7-guide-report:C12`, `qa-master-contract-report:C1`, `qa-master-contract-report:C3`) rest partly on cycle-0 scratch runs (mutations on `/tmp` copies, the master test file run against the new contract); those cannot be re-run, so each cell says what the check relied on and confirms from disk that the fix changed none of it. Every other row was re-read or re-run now.

| Check id | Result |
|---|---|
| qa-contract-rule-report:C1 | PASS. `cmp` of contract `:275-277` and DESIGN `:677-679`: IDENTICAL, 1855 bytes each (cycle-0 figure 1839, plus the 16 characters of " or wait timeout"). DESIGN fence still at `:676` and `:680`. |
| qa-contract-rule-report:C2 | PASS (in substance). Baseline `revisions/.../baseline/design.md` against live DESIGN differs in section 8 on one line only, `:679`, by the owner-approved words (OQ-3 addendum). The cycle-0 wording "empty diff" and "1839 bytes" moved by exactly that approved edit; the claim that the fenced text is the approved text holds, and OQ-3's cited span `:674-680` still matches (`:674` "Final text.", `:676-680` fence). |
| qa-contract-rule-report:C3 | PASS. Hunk `@@ -274,0 +275,4 @@` unchanged; headings at `:271`, `:275`, `:279` (re-run of step 1.17 check 1); HEAD from line 275 to the end equals the live file from line 279 to the end, so blank-line framing is unchanged. |
| qa-contract-rule-report:C4 | PASS. `grep -c '^### WC-16'` is 1 and `grep -c 'WC-16'` is 1; the heading line did not change (only line 277 differs from the pre-fix copy). |
| qa-contract-rule-report:C5 | PASS. Words containing "lock" in lines 275-277: one, `blocked`. |
| qa-contract-rule-report:C6 | PASS. Code spans in 275-277: `### Liveness supervision` (1), `/sc:sweep` (6), `worktree ps --agent-wait` (1). Spans starting `uv`, `make` or `bash`: 0. `superclaude sweep`: 0. |
| qa-contract-rule-report:C7 | PASS. Line 23 is identical to the pre-fix copy; hunk `@@ -23 +23 @@`; the list order equals DESIGN `:705` (full-line `diff` after stripping the quote marker: equal). |
| qa-contract-rule-report:C8 | PASS. `git diff HEAD --numstat` for the contract: 5 added, 1 deleted (as before the fix); only the line-23 and `-274,0 +275,4` hunks. Lines 110 and 151 identical to HEAD. `WC-14` at `:63`, `:124`, `:213`, `:293` (same four lines as the cycle-0 record, `:289` having moved to `:293` by the 4 inserted lines). |
| qa-contract-rule-report:C9 | PASS. Counts in lines 275-277: `WC-16. Coordinator loop` 1, `On every coordinator wake` 1, `it is never posted` 1, `It never stops watching on its own` 1. |
| qa-contract-rule-report:C10 | PASS. `tests/skills/test_worker_contract.py` hash matches the protected list; numstat 14 added, 3 deleted, the cycle-0 figures. |
| qa-contract-rule-report:C11 | PASS. Re-run now: contract test file 742 passed; `tests/skills tests/core tests/commands tests/recommend` 2641 passed; `ruff check` All checks passed; `ruff format --check` 1 file already formatted. |
| qa-contract-rule-report:C12 | PASS. `step-1.19-pytest.txt` (hash matches) ends `742 passed`, equal to the live file run. `phase12-validation.md` (hash matches) says 2008 passed for `tests/skills tests/core`; the live four-directory run gives 2641, and the fix log gives 633 for `tests/commands tests/recommend`, and 2008 + 633 = 2641. Write-verb regex over `sweep.md`: no hit after the new sentence. |
| qa-contract-rule-report:C13 | PASS. Guide `:991` unchanged (hash matches); its order equals contract line 23: agent, git, help, issue, pm, spawn, sweep, swarm-wizard, pr-submit. |
| qa-contract-rule-report:C14 | PASS. OQ-1 and OQ-3 records unchanged (hashes match); the OQ-3 addendum (RESOLVED) adds the one approved wording change. WC-16 still says `/sc:sweep` does not run the `worktree ps --agent-wait` listing (span present once). |
| qa-contract-rule-report:C15 | PASS. `git ls-files` lists only `src/superclaude/core/WORKER-CONTRACT.md` and an old spec under `.dev/orca-command-refactor/`; no `plugins/` copy of `sweep.md`. |
| qa-test-pins-report:C1 | PASS. Test file hash unchanged; same 14 and 3 numstat, so still five edits. |
| qa-test-pins-report:C2 | PASS. Test file unchanged, so the `WC-16` entry, position and four phrases are as reviewed. |
| qa-test-pins-report:C3 | PASS. Each of the four phrases occurs once in contract lines 275-277; heading line 275 carries the ident. |
| qa-test-pins-report:C4 | PASS. Test file unchanged (the `RULE_PHRASES` keys are as reviewed). |
| qa-test-pins-report:C5 | PASS. Test file unchanged; contract line 23 equals DESIGN `:705`. |
| qa-test-pins-report:C6 | PASS. Test file unchanged (the `NEVER_AS_WORKER` tuple is as reviewed). |
| qa-test-pins-report:C7 | PASS. Test file unchanged; `grep` finds no `names_all_seven` or "seven commands" in contract, test or guide. |
| qa-test-pins-report:C8 | PASS. Test file unchanged; `sweep.md` has 0 `## Unattended mode` and 0 `--unattended`. |
| qa-test-pins-report:C9 | PASS. Relied on the file diff and a cycle-0 scratch run of the master test file. Not re-runnable; confirmed from disk that the test file and line 23 are unchanged and the live file still collects and passes 742. |
| qa-test-pins-report:C10 | PASS (in substance). Log content unchanged (hash matches) and shows the entries the check quoted, footer `742 passed`. The log's timestamp (07:13:46) is now older than the contract file (13:35) only because of the owner-approved edit; the same pins pass in the live re-run. |
| qa-test-pins-report:C11 | PASS. Re-run now: 742 passed on the file, 2641 on four directories, ruff check and format clean. |
| qa-test-pins-report:C12 | PASS. Scratch mutations cannot be re-run. Nothing they relied on changed: test file, its helpers, line 23 and every pinned phrase are as before, and `On every coordinator wake` is still contained in the longer new text. |
| qa-test-pins-report:C13 | PASS. `step-1.17-checks.md` gate lines unchanged; OQ-3 record unchanged; `phase12-validation.md` and `r7-check.md` unchanged (hashes match). |
| qa-r7-guide-report:C1 | PASS. Guide `:991` and contract `:23` are single list lines, both read now. |
| qa-r7-guide-report:C2 | PASS. Nine commands in each. |
| qa-r7-guide-report:C3 | PASS. Same order in both (printed side by side). |
| qa-r7-guide-report:C4 | PASS. Guide hash unchanged. |
| qa-r7-guide-report:C5 | PASS. Contract line 23 identical to the pre-fix copy. |
| qa-r7-guide-report:C6 | PASS. Order equals DESIGN `:705`; R7 row `:721` still says "same order as section 8". |
| qa-r7-guide-report:C7 | PASS. Guide numstat 1 and 1. |
| qa-r7-guide-report:C8 | PASS. `r7-check.md` unchanged (hash matches) and its quoted contract line 23 equals the live line. |
| qa-r7-guide-report:C9 | PASS. `r7-check.md` unchanged. |
| qa-r7-guide-report:C10 | PASS. Test file unchanged. |
| qa-r7-guide-report:C11 | PASS. Re-run now (see qa-contract-rule-report:C11). |
| qa-r7-guide-report:C12 | PASS. Scratch mutation (swap order) cannot be re-run; line 23, the pin phrase and the test file are unchanged, so nothing it relied on moved. |
| qa-r7-guide-report:C13 | PASS. Guide unchanged; no new copy of the list. |
| qa-r7-guide-report:C14 | PASS. OQ-3 record unchanged (RESOLVED); OQ-1 unchanged. |
| qa-coordinator-cadence-report:C1 | PASS. `md5sum` of contract `:277` equals that of DESIGN `:679` (`58262e3f5b38d2c18dc4af7bd9eb8442`). Both changed together. |
| qa-coordinator-cadence-report:C2 | PASS. "at most once every 5 minutes" is in `:277` and `:110`. |
| qa-coordinator-cadence-report:C3 | PASS. `:277` still says "unchanged", "an added read: it does not replace that sweep, it is not a second pass, and it does not update heartbeat records or run the `worktree ps --agent-wait` listing". Only four trigger words changed. |
| qa-coordinator-cadence-report:C5 | PASS. The L1 carve-out sentence is untouched; `:110` and `:151` identical to HEAD. |
| qa-coordinator-cadence-report:C6 | PASS. Line 23 unchanged and equal to DESIGN `:705`. |
| qa-coordinator-cadence-report:C8 | PASS. `worktree ps --agent-wait` still named at `:110` and `:277`; OQ-1 record and `src/superclaude/cli/sweep/probes.py` and `classify.py` unchanged (hashes match). |
| qa-coordinator-cadence-report:C9 | PASS. OQ-3 approved WC-16 (RESOLVED); the addendum approves the one wording change; the contract diff still has two hunks, WC-14 and WC-15 untouched. |
| qa-coordinator-cadence-report:C11 | PASS. Re-run now: 742, 2641, ruff clean. |
| qa-coordinator-cadence-report:C13 | PASS. Guide unchanged; no cadence text in it. |
| qa-coordinator-cadence-report:C14 | PASS. `:277` still gives no stall-proof or action power to `/sc:sweep` ("recommends nothing", "A missing heartbeat is absence, never death"); WC-10 and "Never on silence" unchanged. |
| qa-reader-clarity-report:C1 | PASS. `cmp` identical (see qa-contract-rule-report:C1). |
| qa-reader-clarity-report:C2 | PASS. Same nine commands in the same order in contract `:23` and guide `:991`. |
| qa-reader-clarity-report:C3 | PASS. Contract `:20` case 3 unchanged; `:23` still lists `/sc:sweep`, so the guard refuses a `Command: /sc:sweep` line. |
| qa-reader-clarity-report:C10 | PASS. "added read, not a replacement, not a second pass" unchanged and consistent with `:110` and `:151`. |
| qa-reader-clarity-report:C11 | PASS. "recommends nothing" and "dated local file; it is never posted" sentences unchanged. |
| qa-reader-clarity-report:C12 | PASS. 742 passed; ruff clean. |
| qa-reader-clarity-report:C13 | PASS. OQ-1 and OQ-3 records unchanged; addendum consistent with WC-16. |
| qa-reader-clarity-report:C14 | PASS. WC-14 and WC-15 lines identical to HEAD; the new text reuses neither id. |
| qa-conventions-report:C1 | PASS. Heading `### WC-16. Coordinator loop` unchanged, same form as `### WC-6.`. |
| qa-conventions-report:C6 | PASS. Pin tuple unchanged (test file hash matches). |
| qa-conventions-report:C8 | PASS. `ruff format --check`: 1 file already formatted. |
| qa-conventions-report:C11 | PASS. Re-run now: `ruff check` clean; 742 passed. |
| qa-conventions-report:C12 | PASS. Guide and contract line 23 both unchanged, same set and order. |
| qa-conventions-report:C13 | PASS. `grep -cF` of contract `:277` as a pattern against DESIGN gives 1 match. |
| qa-conventions-report:C14 | PASS. No "seven commands" or `names_all_seven` hit in contract, test or guide. |
| qa-master-contract-report:C1 | PASS. Relied on an AST scan and a mutation run (cycle-0 scratch, not re-runnable). Test file unchanged (hash matches); heading line 275 carries ident and first phrase; the pytest run passes. |
| qa-master-contract-report:C2 | PASS. Lines 275-277 hold 0 `--setup` or `--run-hooks` flags and no `uv`, `make`, `bash` span; the repo-setup test passes in the run. |
| qa-master-contract-report:C3 | PASS. Contract line 23 and the test file are unchanged; the list and rename tests pass. The mutation part is a cycle-0 scratch run, not re-runnable; its inputs are unchanged. |
| qa-master-contract-report:C4 | PASS. `sweep.md` has 0 `## Unattended mode` headings and 0 `--unattended`; the `"sweep" not in UNATTENDED_COMMANDS` assertion is in the unchanged test file. |
| qa-master-contract-report:C5 | PASS. Test file unchanged; `UNATTENDED_EXPECT` not in the diff. |
| qa-master-contract-report:C6 | PASS. `commands` is an audit root, so `sweep.md` is scanned: the write-verb regex has no hit in it after the new sentence; the classification table is in the unchanged test file; the audit tests pass in the run. |
| qa-master-contract-report:C7 | PASS. Lines 110 and 151 identical to HEAD; HEAD lines 1-273 except 23 equal the live lines; HEAD from 275 equals live from 279. |
| qa-master-contract-report:C8 | PASS. `WC-14` at `:63`, `:124`, `:213`, `:293`; no `### WC-14` heading. |
| qa-master-contract-report:C9 | PASS. WC-9 (`:41-45`) is in the identical range; the only "lock" substring in 275-277 is `blocked`. |
| qa-master-contract-report:C10 | PASS. `cmp` identical (1855 bytes each); heading `### WC-16`; placement after the fan-in paragraph and before the worked example; OQ-3 RESOLVED plus the addendum RESOLVED. |
| qa-master-contract-report:C11 | PASS. Line 23 equals DESIGN `:705` word for word (full-line `diff` equal); OQ-1 consistent. |
| qa-master-contract-report:C12 | PASS. Guide `:991` unchanged and in the same order as `:23`; no stale copy of the old list wording. |
| qa-master-contract-report:C13 | PASS. Test file unchanged: five design pins only. |
| qa-master-contract-report:C14 | PASS. Runs repeated now: 742, 2641, ruff check and format clean. |
| qa-master-contract-report:C15 | PASS. The WC-16 escalation list and the other sentences are unchanged; the trigger now agrees with `:110` ("wake or timeout"), so the cycle-0 ambiguity noted in F1 of that report is closed. |

The three cycle-0 checks that were FAIL because of the two F_0 findings (`qa-coordinator-cadence-report:C4`, `qa-coordinator-cadence-report:C7`, `qa-reader-clarity-report:C4`) are not in the 82 and are not rated here; on the live files their claims now hold (WC-16 trigger "wake or wait timeout" against `:110`; no other coordinator-facing text with a different cadence).

Count: 82 PASS, 0 FAIL.

## New findings

No new BLOCKING or MAJOR finding. The fix introduced no contradiction I could find: the cap and the "wake or wait timeout" trigger agree across `sweep.md:20`, contract `:277` and `:110`, DESIGN `:679`, and the tests pass.

Notes (minor, never fail the gate, not rechecked later):

| Id | file:line | Note |
|---|---|---|
| N1 | `docs/designs/orchestrator-mode.md:716` (DESIGN row R2) | R2 still words the future routing-guide bullet as "on every wake, at most once every 5 minutes". It is not live text: `src/superclaude/core/HOW-WE-WORK.md` has 0 `sc:sweep` hits, and the owner's approval (OQ-3 addendum, "Scope of this approval") left R2 alone on purpose. When the step that applies R2 runs, the bullet will be narrower than WC-16 (no timeout). Align it then, with the owner's say. |
| N2 | `.claude/commands/sc/sweep.md` | The project copy does not exist yet: `make sync-dev` has not run (the fix log says a later plan step does it). `make verify-sync` needs it later. Not a defect of this fix. |
| N3 | `phase-outputs/test-results/step-1.17-checks.md:84` | Check 5 as written reports FAIL, because the contract diff against HEAD now also holds the line-23 hunk. The file says so and records two passing adjusted comparisons; my own `cmp` of lines 275-277 against the DESIGN block is identical. Recorded, not blocking. |
| N4 | cycle-0 CON-F3 to CON-F20 | The 18 MINOR findings were left as notes by design and were not rechecked. |

## Verdict

- Confidence: Verified: 85/85 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The 85 are CON-F1, CON-F2, the command-test wording check and the 82 check ids. Five of the 82 rest partly on cycle-0 scratch runs and were confirmed from unchanged inputs, as said above the table.
- Tool engagement: Read: 19 | Grep: 3 | Glob: 0 | Bash: 6 (four batched read-only scripts with about 70 `grep`, `diff`, `cmp`, `md5sum` and `sed` commands, one `sha256sum -c` over 63 files, one pytest and ruff run). Read plus Grep plus Glob (22) is below the 85 items, so the minimum-engagement rule flags this review as suspect on its face; the per-item evidence is in the Bash batches and is cited per row. Edit and Write touched this report only. Web: none.
- Not run: no live Orca command; no mutation experiment; no `make sync-dev` or `make verify-sync`.

Verdict: PASS
Blocking count: 0
