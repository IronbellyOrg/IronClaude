# Final acceptance review

status: pass

## Acceptance criteria
Independent reviewer opening: "Result: pass. I found no confirmed blocking finding."

The opening summary reported 22 ACs. The plan has 25 (6+6+4+4+5); the parent requested the truncated tail and explicit complete coverage before recording a FINAL verdict. No approval is inferred from the truncated response alone.

**Limits on this review.** I had no shell and ran nothing, so I did not recompute the plan and source sha256 pins, and I did not diff the diagnostic package. For the diagnostic package I only read `artifacts/diagnostic-preservation.json` (`verified: 61`, no mismatches). I judged test behavior by reading the tests and the saved logs. I did not rerun them.

**Production code** (the user-authorized launcher change plus the two continuations):
- The launcher change is at `src/superclaude/cli/swarm/commands.py:1297-1306`. The child argv now carries `--output <resolved dir> <resolved snapshot>`. The launcher still only stages the snapshot and calls `launch_detached`, and it writes no marker (`:1278-1338`).
- Foreground publication is at `commands.py:2097` (`result_contract = None`), `:2148` (reduce), `:2168` (terminal-state write), then `:2176-2186` (`emit_done_sentinel` with `result_contract.status` and the resolved `return-contract.yaml` path). It is gated on the contract being non-None, an output dir existing, and the policy flag being true.
- Resume publication is at `commands.py:2595` (reduce), `:2608` (terminal-state write), then `:2610-2616` (marker).
- `_emit_killed_done_sentinel` and `kill_cmd` are untouched. I saw no change to `Manifest`, `resume_mode` or the reflect ensemble.

**Task 1**
- **AC1 met.**
  - `foreground-before.txt:1-3` shows the pre-fix failures (`FileNotFoundError` for `done.json`, `:55`).
  - `foreground-after.txt:4` shows `110 passed`, `EXIT: 0`.
  - The first before-run also shows invalid test statuses (`:233`, `got 'failed'`). That is kept history, and the tests were later fixed (`tests/swarm/test_commands_run.py:614`, `timeout`).
- **AC2 met.**
  - `tests/swarm/test_e2e_user_guide.py:117` is the new positive default-on test.
  - `tests/swarm/test_commands_run.py:573-596` asserts the exact three-field marker for spec-file and stdin, enabled and disabled, with a relative `--output`.
  - `foreground-cli-check.txt:29-33` shows `atomic_write` true, `terminal_status` success and an absolute `contract_path`.
- **AC3 met.**
  - Opt-out is covered at `test_commands_run.py:591`. The success, partial and failed cases (3, 2 and 0 successes) run the real reducer and writer at `:599-639`.
  - The disabled case also asserts a terminal state and a contract.
- **AC4 met.**
  - Ordering wrappers are at `:621-639`: the contract exists and no marker exists at terminal write, and at marker time the state is terminal and the status matches the contract.
  - Failure injection for reduce, contract and terminal-write is at `:642-667`.
  - No-output, no-recipe, preflight and transport branches are at `:670-688`.
- **AC5 met.** `foreground-cli-check.txt:2-37` records the UV-launched run with the argv, stdout, stderr, exit 0, the import path in the checkout, `artifact_count` 13 and `PASS`.
- **AC6 met.** `foreground-after.txt:1-6` runs the six required modules: 110 passed.

**Task 2**
- **AC1 met.** `resume-before.txt:47-54` shows 6 failed (missing marker). `resume-after.txt:6-15` shows 82 passed. The fixture asserts that no marker exists first (`tests/swarm/test_resume_crash_recovery.py:567`).
- **AC2 met.**
  - The test at `test_resume_crash_recovery.py:545-640` covers both skip-all (`:608`, `calls == []`) and full redispatch.
  - Mixed skip and redispatch with markers is covered by the existing tests at `:390` and `:426`.
  - It also checks preserved sidecar bytes (`:638`) and 3 unique slot indices (`:627-637`).
- T2.AC3 met. tests/swarm/test_resume_crash_recovery.py:545-547 parameterizes enabled, successes (0, 2, 3) and skip_all. Expected status is derived at :610-616. The real reducer runs, and only dispatch_wave1 and normalize_wave2 are stubbed (:585-586). The disabled policy is injected through a wrapper around preflight.resume_mode (:568-575). Normal manifest tests run default-on (:390, :426). Disabled gives events == ["terminal"] (:609).
- T2.AC4 met. The state wrapper (:590-594) asserts the contract exists and no marker exists at terminal write. The marker wrapper (:596-602) asserts state is terminal and the status matches the contract. Failure cases are at :642-673: reduce, contract, terminal, missing, malformed and mismatch. Each ends with assert not done.json (:673).
- T2.AC5 met. artifacts/resume-cli-check.txt:1-62 has the argv, stdout (skipped=3 redispatched=0), exit 0, and the seed run. Setup is recorded: the seed's prior marker was removed (:43-47). The new marker, state and contract agree (:49-59). It imports the checkout's commands.py (:60).
- T2.AC6 met. artifacts/resume-after.txt:12-17 runs the five required modules: 82 passed, EXIT 0. Production resume change is only commands.py:2610-2616.

Task 3
- T3.AC1 met. tests/swarm/test_tmux_detached.py:276-336. launch_detached is intercepted (:296-301). No marker from the parent (:297, :308). Snapshot policy checked at :313-318. The captured argv is run through the real run_cmd (:320). Marker only when enabled (:322). Status, path and terminal state at :328-335. Both relative and absolute --output are covered. Production: commands.py:1297-1306.
- T3.AC2 met. Live test at :339-398 uses uv run, a fixed 10 s deadline that breaks early if the session dies, and kills only its own session. artifacts/detached-check.txt:81-130 shows tmux_available true, nested false, stdout and stderr, the artifact list, marker success, state terminal and PASS. The earlier FAIL record (:1-30) is kept history.
- T3.AC3 met. artifacts/completion-compatibility.txt:78-87 shows 123 passed, 2 skipped with reasons (:83-84), EXIT 0. Earlier failing runs (:1-63) are kept history.
- T3.AC4 met. The launcher stays launcher-only (commands.py:1278-1338). The only production change is the argv, authorized by the user at 2026-11-23T20:53:20Z. The killed-marker code and the reflect ensemble are untouched.

Task 4
- T4.AC1 met. docs/swarm/README.md:12-13, :119-128; command-reference.md:266-276; user-guide.md:407-413. A grep for only-kill and inline-never phrasing found nothing.
- T4.AC2 met. Three-field row at README.md:113 and command-reference.md:266. "Completion does not guarantee all workers succeeded" is there. The count of 13 (README.md:115) matches foreground-cli-check.txt:35.
- T4.AC3 met. command-reference.md:282 and the README resume note give the effective-policy qualifier. Early errors give no marker. No full-detached-verification claim.
- T4.AC4 met. artifacts/reference-doc-check.txt:222-228: 25 passed, exit 0, claim search and links OK.

Task 5
- T5.AC1 met. monitoring-patterns.md:6-12, :40-52, :80-82.
- T5.AC2 met. observability-procedure.md:23-32, :51, :98-117, :271-273.
- T5.AC3 met. operator-runbook.md:218-228.
- T5.AC4 met. The only hit for the test name is observability-procedure.md:28, which cites the new test_quickstart_emits_done_sentinel. No old-name citation and no only-kill claim remain. artifacts/monitoring-doc-check.txt:1-223.
- T5.AC5 met. artifacts/monitoring-doc-check.txt:224-229: 29 passed, exit 0.

Constraints
- Production edits are limited to the two completion continuations plus the user-authorized launcher argv. The reducer, writer, Manifest, resume_mode and kill paths are unchanged.
- I saw no write to the diagnostic package. artifacts/diagnostic-preservation.json shows verified 61 with no mismatches.
- Python and test runs go through uv. They used --no-project and the existing tool interpreter. The tail-start-line citations in this message are exactly as above.

Reviewer correction: "the plan has 25 ACs (T1 6, T2 6, T3 4, T4 4, T5 5). My opening said 22, which was wrong. All 25 are marked met below or in the part you already have. The result stays pass, with no blocking findings."

## Saved review prompts and notes
Reviewer tail, verbatim:
- artifacts/prompt-template-check.txt:1-9 records a first failure on trailing whitespace before an empty slot. That is whitespace-only, so it is a note. The recheck at :10-19 passed all 8 prompts: T1, T2, T3 (1-1, 2-1, 2-2), T4 (1-1, 2-1) and T5.
- I independently compared retries/T3/prompt-2-2.md with the seven-slot template and it matched outside the slots. I did not read the other seven prompts myself and rely on the script for them.
- There is no superseded-prompts folder, so there is no superseded-prompt judgment.
- The notes files are all-no entries, cited as noted: T3 notes.md:2-3, T4 notes.md:2, T5 notes.md:2-3.
- review-*.md blocking lines: T3 F3.1 is marked resolved (review-2.md:9, operator-review-2.md). T4 F1.1 is resolved (review-2.md:2).
- The T3 dispute halt was closed by operator-review-2.md.

Parent: this tail completes all 25 AC marks, but admits the required direct audit of seven saved prompts was omitted. The same independent reviewer was asked to finish only those missing direct reads and every remaining retry-folder file before this gate can be accepted. No delivery bytes or state digest changed.
## Reviewer's direct audit completion, verbatim

Direct saved-prompt and retry-folder check is done. The result is unchanged: pass, no blocking findings. The script was not used as a substitute. I used targeted greps and line-range Reads. Under retries/ (T1 to T5) I Read every file, except attempt-2.diff, which I read only lines 1-40, and the diff and Task-brief slot bodies, which I did not read in full (see Limits).

PER-PROMPT COMPARISON against the seven-slot closed template in qa.md
Method: for each prompt I confirmed line 1 is the start sha, line 2 is "Review one task for spec compliance.", and the order of the fixed lines. Those are: Task brief, Global constraints, Start sha, Diff against the start snapshot, Delta diff, Earlier blocking findings, Saved-probe re-check hit locations, "Do not trust the implementer's report.", the First-mark paragraph, the four numbered questions, Anchor rule, "Write one line per finding", F<k>.<j> line, "Do not write sev=...", "Inside /sc:implement...", "You are not given an adviser answer...", and "The prior-findings slot above...". I grepped 22 fixed-line anchors in each prompt, and each file returned exactly 22. I Read the tail (from the Delta line through the last line) of T1, T2, T3/1-1, T3/2-1, T4/1-1, T4/2-1 and T5 in full. I Read T3/2-2 in full earlier. Slot contents of Delta, Earlier findings and Saved-probe differ, as the template allows. Whitespace was not treated as a difference.
- T1/prompt-1-1.md (sha 8b15d2ff, tail :244-267): identical to the template outside the slots. Slots 5-7 are empty, as expected on a first review. PASS.
- T2/prompt-1-1.md (sha 260a67c7, tail :220-243): same result. PASS.
- T3/prompt-1-1.md (sha 1e33f422, tail :179-202): same result. PASS.
- T3/prompt-2-1.md (sha 1e33f422, tail :179-202): the Earlier-findings slot (:180) holds F3.1 and the Saved-probe slot (:181) holds the hit locations. Everything else matches. PASS.
- T3/prompt-2-2.md (read in full earlier): PASS. Line 26 of that prompt, the user instruction, sits inside the Global constraints slot.
- T4/prompt-1-1.md (sha 06ccf728, tail :169-192): same result. PASS.
- T4/prompt-2-1.md (sha 06ccf728, Delta slot at :172-195, tail :196-218): the Earlier-findings slot carries F1.1 and the Saved-probe slot carries the table-row locations. The template lines match. PASS.
- T5/prompt-1-1.md (sha 56f171c1, tail :309-332): same result. PASS.
The shas on line 1 match the ledger start lines (progress.md:3, 5, 7, 12, 14). No non-blank line outside the slots is changed, added, removed or reordered in any of the 8 prompts. No whitespace-only differences were noted. No prompt-template issues. There is no superseded-prompts/ folder (the Glob returned nothing), so there are no superseded prompts and nothing needing a README. Every task with a flagged prompt has a later passing one, so the superseded-prompt rule is not triggered.

RETRY-FOLDER READS AND END-STATE CHECKS
- T1: review-1.md (start 8b15d2ff). All 6 ACs met, no findings. Its citation foreground-before.txt:292 is a pointer to the earlier log, not a defect. q0-head is 720cbaf9, a base marker only.
- T2: review-1.md read earlier. All 6 ACs met, no findings. q0-head is 720cbaf9.
- T3:
  - review-1.md has F3.1 blocking and is marked resolved at the end of review-2.md. review-2.md has F3.1 open and then resolved after the user's authorization. Both are history.
  - operator-review-2.md says all ACs are met and F3.1 is resolved. That response was first rejected as paperwork-only, and the fresh respawn is recorded. The notes cover F3.2 and F3.3 as all-no.
  - probe-1-1.md has the "after:" line, which records the launcher change that came with the user's authorization.
  - advice-3-a.md and advice-3-b.md both say "dispute". They each say the fix is outside the plan's scope and needs a ruling, offering option (a), authorize the launcher argv, or option (b), amend the ACs. Neither adviser answer authorized anything. The user's 2026-11-23T20:53:20Z message chose option (a), which is consistent with the ledger.
  - advice-check-3.log records the citation checks and the halt (reason=dispute, no revert, no Ruling). approach-2.md, extras-2.log and attempt-2.diff (lines 1-40) are the failed-attempt record: 2 failed, 119 passed, which was later fixed. These are history, not current defects.
  - notes.md has 2 entries, both all-no, so they are noted.
- T4: review-1.md has F1.1 blocking (table row split by a blank line), resolved in review-2.md (README.md:112-113 and command-reference.md:265-266, which I checked live earlier). probe-1-1.md has its "after:" line. notes.md has one all-no note, F2.1, which was addressed by Task 5.
- T5: review-1.md covers both reviewer responses. The first was rejected as paperwork-only, and the respawn has two all-no notes, F1.1 and F1.2. There is no blocking finding. notes.md matches.
- q0-head of T1 to T5 all hold 720cbaf9. These are base markers, not defects.
No blocking line is left open in any review-*.md. No notes entry has a confirmed yes.

LIMITS
- I did not Read the bodies of the diff and Task-brief slots in the 7 prompts beyond the head and tail; the template comparison covers the fixed lines. The slot contents are not compared with the template by definition.
- I did not recompute any digest or run any test.
- A note appeared that artifacts/final-review.md changed on disk after my last Read. I did not open it, and nothing here depends on it.

Verdict unchanged: pass, with the Medium follow-up for ruff I001 at tests/swarm/test_commands_run.py:602.

Parent: direct outside-slot comparisons now satisfy the prompt comparison. The report's live edits are only persistence of returned sections, not changes to delivery inputs. The reviewer was asked for the remaining attempt-2.diff lines 41-144 before closing the required retry-file read.
Reviewer final confirmation, verbatim:

I read T3/attempt-2.diff lines 41-145 (the file ends at 144; line 145 is an empty phantom line). It changes no end-state finding. The verdict is still pass, with no blocking findings.

- The diff is the test-only A2 version of the two detached tests. It has the same parent-launch and captured-child steps (`requests[0][5:]`, :68) and the same live CLI test (:85-144). It touches only tests/swarm/test_tmux_detached.py, which fits the earlier lines 1-4.
- It is the historical failing attempt. Its parent test has no `monkeypatch.chdir` and no `relative_output` parameter. It has no assertions that the snapshot path is absolute, that `--output` is carried in the argv, or that `return-contract.yaml` exists. Those assertions appear only in the current test_tmux_detached.py:276-336, after the authorized launcher change at commands.py:1297-1306. The current file therefore supersedes this diff.
- The live test is identical to the current one, and the A2-era failure it records was the missing child output (extras-2.log:17-23). That is resolved: detached-check.txt:81-130 shows PASS.
- I found no skip or xfail substitution, no weakened expectation and no delivery-file edit in this diff, which matches approach-2.md.

All files under retries/ have now been Read in full.

## Findings
Reviewer tail:
- Blocking: none. All four checklist answers are no, so there are no anchors.
- Medium follow-up candidate: ruff I001 at tests/swarm/test_commands_run.py:602 (artifacts/final-lint-check.txt:3-26, exit 1). This is a lint extra, not a spec verdict. The formatting of the added tests was not checked.

Reviewer-unverified items: plan and source sha256 pins (no shell to recompute), staging state, and test reruns. Test conclusions come from reading tests and saved logs.

Parent: the import-spacing result is a real, explicitly failed lint extra, not a failed acceptance criterion. Its form-only nature and all-no checklist derive note under qa.md, regardless of the reviewer's Medium label. It is disclosed, not silently repaired in a completed task. The final-lint-check.txt is the actual run of that formatting check, so the incidental phrase "formatting ... was not checked" does not describe the executor's verification.
Parent: helper --print-state recomputed the same a64b4c8e7dc88ac21ffdf379af3ff451aa0b499e997185267921278d79309334 digest before and after the review. SHA-256 values remain 7fcb916baa03f01def2927f7d830f089d393d1c8a14f50ebc769fcd5c8f5db7c for the plan and 5b689aeb3e7bf2db98dedbadb75dec24bf386bb80a0b99085430da9076e0d2eb for source.md. The original 61 diagnostic files were independently rehashed by the executor with zero mismatches. No source/plan edit or gap-acceptance Ruling exists.
Final gate result: pass. The independent reviewer has verified all 25 original ACs, all 8 prompts outside their allowed slots, and all retry-folder files, with no open blocking finding. The bounded missing reads and truncated-report tail were completed by the same independent reviewer without any delivery-file change. No missing behavior was accepted; the user authorized the launcher repair itself.
