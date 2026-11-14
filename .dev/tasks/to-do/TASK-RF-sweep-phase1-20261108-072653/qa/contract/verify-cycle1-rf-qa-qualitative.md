# Verify, contract gate cycle 1 (rf-qa-qualitative)

Date: 2026-11-12. Verifier: rf-qa-qualitative, `fix_authorization: false`. Inputs: consolidated-findings-cycle0.md, fix-log-cycle1.md, cycle-ledger.md, OQ-3 addendum, live files.

## Findings

Judged from the live files, read now (2026-11-12). Files changed since the fix began (`find -newermt '2026-11-12 13:30'` over `src`, `tests`, `docs`, the task folder and `.claude`): `WORKER-CONTRACT.md`, `sweep.md`, `docs/designs/orchestrator-mode.md`, `step-1.17-checks.md`, the OQ-3 addendum, the fix log, and QA/prompt files. Nothing else in `src`, `tests`, `docs` or `.claude` moved. A word diff of DESIGN line 679 against the baseline copy (`revisions/chat-output-exception-20261109-133150/baseline/design.md`) shows one change: `wake,` became `wake or wait timeout,`. The contract diff against HEAD still has only two hunks (`@@ -23 +23 @@` and `@@ -274,0 +275,4 @@`).

### CON-F1 (MAJOR): RESOLVED

- `src/superclaude/commands/sweep.md:20` now reads "Explicit only: the coordinator runs `/sc:sweep` inside its liveness sweep pass, at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`), or a person types it. Nothing starts it automatically."
- `grep -n 'every wake' src/superclaude/commands/sweep.md` prints nothing (exit 1). The line carries the 5-minute cap, ties the run to the liveness sweep pass, and points at WC-16 by installed path (no `src/superclaude` path). The line holds no stop, retry, release, merge or removal word (0 matches) and no em dash.
- The two cadences are now one: contract `:110` ("After every wake or timeout, at most once every 5 minutes"), WC-16 `:277` and `sweep.md:20` all say once per 5 minutes inside the sweep pass.
- Not done and not required by this finding: `.claude/commands/sc/sweep.md` does not exist yet (`make sync-dev` is a later plan step).

### CON-F2 (MAJOR): RESOLVED

- `src/superclaude/core/WORKER-CONTRACT.md:277` now reads "When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake or wait timeout, at most once every 5 minutes, the coordinator runs "The sweep." ..." so an expired wait is named as a trigger beside a wake, matching `:110` ("wake or timeout").
- The pinned phrase `On every coordinator wake` is still a substring: `grep -c` on the contract is 1, pin at `tests/skills/test_worker_contract.py:177`; the gate test run passes (see Gate runs).
- Contract `:275-277` and DESIGN `:677-679` are byte-identical (`cmp` IDENTICAL; `md5sum` of both extracts `1ae51dc52343c621f9cfc70a56c826ac`; line 277 against line 679 alone also IDENTICAL, 1826 bytes each; no trailing whitespace or CR in `:275-277`).
- Lines 110 and 151 of the contract are unchanged from HEAD (`diff` SAME_110_151).

### New findings

No new BLOCKING or MAJOR finding. Three MINOR notes (never fail the gate, not rechecked):

- N1 (MINOR) `docs/designs/orchestrator-mode.md:716` (row R2) still prescribes the CLAUDE.md bullet "The coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, beside "The sweep."". The owner's addendum limited the change to three places, so R2 was left as is, and no live file carries that bullet (`grep 'runs `/sc:sweep`' src/superclaude` hits only `WORKER-CONTRACT.md:277` and `sweep.md:20`). Effect: if R2 is applied as written, a third coordinator-facing text will say "every wake" and bring back the wake-only reading of CON-F2. Fix when R2 is applied: write "on every wake or wait timeout".
- N2 (MINOR) `step-1.17-checks.md:84` records check 5 as FAIL as written (the line-23 hunk added after the first run); the same file records the two adjusted comparisons as identical. The record is honest and the claim it guards (contract paragraph equals DESIGN block) holds on disk now. A reader who re-runs check 5 unchanged will see "differ".
- N3 (MINOR) `sweep.md:20` says "its liveness sweep pass"; the contract calls the same thing "The sweep." under "Liveness supervision". The WC-16 pointer in the same sentence resolves it, so it does not mislead.

## Checks

82 ids, the cycle-0 PASS set. Basis: live re-checks (cmp, grep, git diff, tests) for claims about the contract, DESIGN block, `sweep.md` and pins; for saved artifacts and scratch runs of the cycle-0 agents, the on-disk mtimes show that the guide, the test file, `step-1.19-pytest.txt`, `r7-check.md`, `phase12-validation.md`, OQ-1, the original OQ-3, research/07 and the cycle-0 reports were not touched after 07:27 on 2026-11-12, before the fix (13:35). "Scratch" below means a /tmp experiment that cannot be re-run.

| Check id | Result |
|---|---|
| qa-contract-rule-report:C1 | PASS. Contract `:275-277` and DESIGN `:677-679` still byte-identical (cmp, md5 equal); both changed together. |
| qa-contract-rule-report:C2 | PASS. DESIGN differs from the baseline copy only by "or wait timeout" on line 679, approved in the OQ-3 addendum; the original OQ-3 record and its `:674-680` span are untouched, and the stated 1839-byte size is now 16 bytes more, a count that moved, not a false claim. |
| qa-contract-rule-report:C3 | PASS. Headings still at 271, 275, 279; blank-line framing unchanged (diff hunk `@@ -274,0 +275,4 @@`). |
| qa-contract-rule-report:C4 | PASS. One `### WC-16. Coordinator loop` heading at 275; ident and phrase on one line. |
| qa-contract-rule-report:C5 | PASS. Only `lock` word in line 277 is "blocked"; the new words add none. |
| qa-contract-rule-report:C6 | PASS. Code spans in line 277: `### Liveness supervision`, `/sc:sweep` x6, `worktree ps --agent-wait`; none starts `uv`, `make` or `bash`. |
| qa-contract-rule-report:C7 | PASS. Line 23 hunk `@@ -23 +23 @@` unchanged by the fix; order agent, git, help, issue, pm, spawn, sweep, swarm-wizard, pr-submit. |
| qa-contract-rule-report:C8 | PASS. Only two hunks against HEAD; lines 110 and 151 equal HEAD (diff SAME_110_151); WC-14 lines still 63, 124, 213, 293. |
| qa-contract-rule-report:C9 | PASS. `grep -c 'On every coordinator wake'` is 1; the other three phrases are covered by the passing pin test. |
| qa-contract-rule-report:C10 | PASS. Test file unchanged since 07:13; its five edits stand. |
| qa-contract-rule-report:C11 | PASS. Re-run: 2641 passed over `tests/skills tests/core tests/commands tests/recommend`; ruff check and format check clean. |
| qa-contract-rule-report:C12 | PASS. `step-1.19-pytest.txt` unchanged (742 passed); the pin phrase is still a substring, so the saved result still holds. |
| qa-contract-rule-report:C13 | PASS. Guide `:991` unchanged and lists the nine commands in the order of contract `:23`. |
| qa-contract-rule-report:C14 | PASS. Original OQ-3 and OQ-1 unchanged; the OQ-3 addendum covers the wording change. WC-16 still says `/sc:sweep` does not run `worktree ps --agent-wait`. |
| qa-contract-rule-report:C15 | PASS. Only `WORKER-CONTRACT.md` under `src` holds the contract; no `.claude` copy exists; the old wording survives nowhere live. |
| qa-test-pins-report:C1 | PASS. Test file untouched by the fix (mtime 07:13:39). |
| qa-test-pins-report:C2 | PASS. `"WC-16"` entry unchanged; its four phrases are still in the contract. |
| qa-test-pins-report:C3 | PASS. Heading at 275 and the phrase `On every coordinator wake` (count 1) still present. |
| qa-test-pins-report:C4 | PASS. File unchanged; one `WC-14` key. |
| qa-test-pins-report:C5 | PASS. `never-as-worker` phrase equals contract `:23` (line unchanged); `test_contract_states_rule` passes in the run. |
| qa-test-pins-report:C6 | PASS. `NEVER_AS_WORKER` unchanged; its removal tests pass. |
| qa-test-pins-report:C7 | PASS. Rename unchanged; no `names_all_seven` hit in `src`, the test file or the guide. |
| qa-test-pins-report:C8 | PASS. Assertion line unchanged; `sweep.md` still has 0 `## Unattended mode` headings. |
| qa-test-pins-report:C9 | PASS. Test file unchanged. The scratch run of the master test file against the new contract cannot be re-run; the contract change is 16 bytes inside one sentence and does not touch the `never-as-worker` line, so its result stands. |
| qa-test-pins-report:C10 | PASS. `step-1.19-pytest.txt` mtime 07:13:46, unchanged, still shows 742 passed. |
| qa-test-pins-report:C11 | PASS. Re-run now: pytest 2641 passed, ruff check clean, ruff format clean. |
| qa-test-pins-report:C12 | PASS. Scratch mutations cannot be re-run; they relied on the test file and on the four WC-16 phrases, none of which the fix changed (the pinned phrase is still a substring). |
| qa-test-pins-report:C13 | PASS. `step-1.17-checks.md` gained an appended section only (first run text intact); `r7-check.md` and `phase12-validation.md` unchanged. |
| qa-r7-guide-report:C1 | PASS. Guide `:991` and contract `:23` read now; each a single list line. |
| qa-r7-guide-report:C2 | PASS. Same nine commands in both. |
| qa-r7-guide-report:C3 | PASS. Same order in both (checked on `:23` and `:991` now). |
| qa-r7-guide-report:C4 | PASS. Guide file unchanged since 07:14. |
| qa-r7-guide-report:C5 | PASS. Contract line 23 hunk unchanged; the D3 wording difference is as at HEAD. |
| qa-r7-guide-report:C6 | PASS. `/sc:sweep` still between `/sc:spawn` and `/sc:swarm-wizard`, as DESIGN `:705` says; DESIGN changed only on line 679. |
| qa-r7-guide-report:C7 | PASS. Guide diff is 2 lines changed (1 insertion, 1 deletion). |
| qa-r7-guide-report:C8 | PASS. `r7-check.md` unchanged and its quotes still equal the live lines. |
| qa-r7-guide-report:C9 | PASS. `r7-check.md` unchanged (the F1 note stays a note). |
| qa-r7-guide-report:C10 | PASS. Test pins unchanged and passing. |
| qa-r7-guide-report:C11 | PASS. Re-run now: tests pass, ruff clean. |
| qa-r7-guide-report:C12 | PASS. Scratch swap-order mutation cannot be re-run; it relied on line 23 and the pin, both untouched. |
| qa-r7-guide-report:C13 | PASS. No other guide location repeats the list; the fix touched none. |
| qa-r7-guide-report:C14 | PASS. OQ-3 RESOLVED stands; the addendum is additive; OQ-1 unchanged. |
| qa-coordinator-cadence-report:C1 | PASS. md5 of contract `:275-277` equals md5 of DESIGN `:677-679` (`1ae51dc52343c621f9cfc70a56c826ac`); the text is "wake or wait timeout" in both. |
| qa-coordinator-cadence-report:C2 | PASS. WC-16 cadence "at most once every 5 minutes" equals line 110's cap. |
| qa-coordinator-cadence-report:C3 | PASS. WC-16 still says `/sc:sweep` is added beside the sweep, "unchanged", not a replacement, not a second pass. |
| qa-coordinator-cadence-report:C5 | PASS. L1 carve-out sentence unchanged; lines 110 and 151 equal HEAD. |
| qa-coordinator-cadence-report:C6 | PASS. Line 23 equals DESIGN `:705` word for word; one line. |
| qa-coordinator-cadence-report:C8 | PASS. `--agent-wait` mentions at `:110` and `:277` unchanged in substance and agree with OQ-1. |
| qa-coordinator-cadence-report:C9 | PASS. Contract diff still two hunks; WC-14 and WC-15 untouched; the addendum approves the one new edit. |
| qa-coordinator-cadence-report:C11 | PASS. Re-run now: 2641 passed, ruff clean. |
| qa-coordinator-cadence-report:C13 | PASS. Guide diff adds only `/sc:sweep`; no cadence text. |
| qa-coordinator-cadence-report:C14 | PASS. WC-16 still says "A missing heartbeat is absence, never death" and "`/sc:sweep` recommends nothing"; "Never on silence" lines 182-192 untouched. |
| qa-reader-clarity-report:C1 | PASS. WC-16 paragraph equals DESIGN paragraph (line 277 vs 679 cmp IDENTICAL). |
| qa-reader-clarity-report:C2 | PASS. Line 23 and guide `:991` name the same nine in the same order. |
| qa-reader-clarity-report:C3 | PASS. Line 23 and guard case 3 (`:20`) unchanged; `/sc:sweep` still refused. |
| qa-reader-clarity-report:C10 | PASS. The "added read, not a second pass" sentence is unchanged and consistent with `:110` and `:151`. |
| qa-reader-clarity-report:C11 | PASS. "recommends nothing" and "dated local file; never posted" sentences unchanged. |
| qa-reader-clarity-report:C12 | PASS. Test pins and contract agree; tests and ruff re-run clean. |
| qa-reader-clarity-report:C13 | PASS. OQ-1 and the original OQ-3 unchanged; WC-16 id and the no-`--agent-wait` rule stand. |
| qa-reader-clarity-report:C14 | PASS. WC-14 and WC-15 lines unchanged (63, 124, 213, 293). |
| qa-conventions-report:C1 | PASS. Heading form `### WC-16. Coordinator loop` unchanged. |
| qa-conventions-report:C6 | PASS. Pin tuple shape unchanged (test file untouched). |
| qa-conventions-report:C8 | PASS. `never-as-worker` pin string layout unchanged; ruff format clean. |
| qa-conventions-report:C11 | PASS. Re-run: ruff check and format check clean; pytest passes (contract tests inside the 2641). |
| qa-conventions-report:C12 | PASS. Guide `:991` wording equals contract `:23` wording (both read now). |
| qa-conventions-report:C13 | PASS. WC-16 paragraph found in DESIGN: line 277 and line 679 identical, one match. |
| qa-conventions-report:C14 | PASS. `grep -i 'seven commands\|names_all_seven'` over core, `sweep.md`, the test file and the guide: no hit. |
| qa-master-contract-report:C1 | PASS. `"WC-16"` key and `_check_rule` unchanged; heading line 275 carries ident and phrase; contract tests pass. |
| qa-master-contract-report:C2 | PASS. The new words add no `--setup`, `--run-hooks` or launcher code span (code spans listed above); repo-setup check passes in the run. |
| qa-master-contract-report:C3 | PASS. Line 23 unchanged; `NEVER_AS_WORKER` check passes. |
| qa-master-contract-report:C4 | PASS. `sweep.md` still has 0 `## Unattended mode` headings (grep -c 0), after the line-20 edit. |
| qa-master-contract-report:C5 | PASS. Test file unchanged; `UNATTENDED_EXPECT` untouched. |
| qa-master-contract-report:C6 | PASS. `sweep.md:20` has no write verb (0 matches for stop, retry, release, merge, remov); the write-verb audit tests pass in the 2641. |
| qa-master-contract-report:C7 | PASS. Lines 110 and 151 equal HEAD; the only contract differences against HEAD are the line-23 hunk and the 4 lines at 275-278 (git diff hunks). Scratch rewording mutations cannot be re-run; they relied on lines 110 and 151, unchanged. |
| qa-master-contract-report:C8 | PASS. WC-14 lines 63, 124, 213, 293 unchanged. |
| qa-master-contract-report:C9 | PASS. WC-9 untouched; the only added words are "or wait timeout"; no lock text. |
| qa-master-contract-report:C10 | PASS. `sed -n 275,277p` of the contract equals `sed -n 677,679p` of DESIGN (cmp IDENTICAL); original OQ-3 RESOLVED and the addendum RESOLVED. |
| qa-master-contract-report:C11 | PASS. Line 23 equals DESIGN `:705`; OQ-1 consistent. |
| qa-master-contract-report:C12 | PASS. Guide edit unchanged; no other stale copy of the list. |
| qa-master-contract-report:C13 | PASS. Test file diff scope unchanged (five pins). |
| qa-master-contract-report:C14 | PASS. Re-run: 2641 passed over `tests/skills tests/core tests/commands tests/recommend`; ruff check and format check clean. |
| qa-master-contract-report:C15 | PASS. WC-16 still matches the escalation lines it maps to and WC-10; the wait-timeout words make it agree with `:110` and `:101`. |

## Passage re-read

**WC-16 (contract `:277`) read as a coordinator.** The paragraph gives this order: keep watching until every Task is settled and every result inspected; when a wait expires, re-arm it; "On every coordinator wake or wait timeout, at most once every 5 minutes" run "The sweep." unchanged and, in the same pass, `/sc:sweep`, and read its report before acting. An expired wait is now named as a trigger, so a coordinator does not read a quiet timeout as "no wake, skip the read". Re-arming and sweeping are two things that both happen after a timeout, and the sentence order does not suggest one replaces the other. The cap is stated once and is the same cap as line 110. No misleading passage found in the changed words. (Unchanged MINOR notes from cycle 0, such as "Phase 1 adds this duty, not a scheduler", stay as notes.)

**`sweep.md:20` read as the coordinator who loads that file.** "Explicit only: the coordinator runs `/sc:sweep` inside its liveness sweep pass, at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`), or a person types it." One cadence: inside the sweep pass, at most once per 5 minutes, with a pointer to WC-16 for the triggers. The line does not itself say "wake or wait timeout", so a reader who stops at `sweep.md` learns the cap and the placement but takes the trigger from WC-16 or line 110; it cannot read it as "on every heartbeat", which was the cycle-0 defect. It does not tell the reader that an expired wait is not a trigger. See N3 (wording of "liveness sweep pass") in Findings.

**Do the two passages give one cadence?** Yes: inside the liveness sweep pass, at most once every 5 minutes, on a wake or a wait timeout (contract `:110`, `:277`, `sweep.md:20`). The one remaining place that still says "every wake" is DESIGN row R2 (`:716`), a design prescription outside the approved scope; see N1.

## Gate runs

- `uv run pytest tests/skills tests/core tests/commands tests/recommend -q`: 2641 passed in 57.88s.
- `uv run ruff check tests/skills/test_worker_contract.py`: All checks passed.
- `uv run ruff format --check tests/skills/test_worker_contract.py`: 1 file already formatted.
- Two read-only batches under `/tmp/ironclaude-batch.*` (removed on exit): cmp, grep, sed, md5sum and git diff over the live files. One line in the second batch (the "whole-file vs HEAD" check) failed on a sed expression and printed a false SAME_REST; I did not use it. The two-hunk `git diff -U0` output is the evidence for "nothing else changed in the contract".
- Not run: the sha256 check of the 63 protected files (the baseline taken at the T274 start is not in the files I was given). Substitute evidence: `find -newermt '2026-11-12 13:30'` lists only the three allowed source files, `step-1.17-checks.md` and the OQ-3 addendum among the non-report files; nothing in `src`, `tests`, `docs` or `.claude` besides the three allowed files changed.
- No live Orca command, no repository file edited, no scratch mutation run. Tools: Read 9 | Bash 6 | Grep 0 (grep ran inside Bash) | Write/Edit: this report only.

## Verdict

CON-F1 RESOLVED, CON-F2 RESOLVED. All 82 check ids of the cycle-0 PASS set still PASS (0 FAIL). No new BLOCKING or MAJOR finding; three MINOR notes (N1 to N3).

Confidence: Verified: 82/82 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (scratch-run checks are verified by the unchanged-input argument stated in the Checks section).

Verdict: PASS
Blocking count: 0
