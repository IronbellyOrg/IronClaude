# Final repair plan

## Authorization and scope

User, 2026-11-09: "I am authorizing the two repairs proceed". This reopens only the installer/status FIFO defect and malformed delivery-file fields found by the independent final review. The pinned plan and source snapshot stay unchanged. Previous final review, task verdicts, notes and scoped history acceptance are preserved. No push or pull request. IR7_REFUSE stays False; commit E must stay last and separate.

Auggie codebase-retrieval is not available in this session. Codegraph confirms the shared validator has two callers: install_l2 and _l2_entry_verdict (status). Live source and tests were read before edits.

## Repair steps and acceptance criteria

1. Add a bounded, real FIFO regression for fresh installation and owned-hook status, preserving the pre-existing FIFO and leaving no private install directory. Observe the current implementation time out before changing it, then change the shared descriptor open to nonblocking without dropping O_NOFOLLOW or fstat validation. Both entry points must return conflict promptly and leave the original FIFO untouched.
2. Preserve the pre-repair ledger verbatim in a separate artifact. Correct exactly eight completion records by moving trailing notes@ references into their evidence fields; do not change task verdicts, AC lists, evidence citations, notes text, or the recorded history-count Ruling. All actual delivery files must be present in the helper manifest; independently show each formerly omitted file changes the state digest when changed (using disposable copies, never live delivery files).
3. Run focused tests, lint and component sync, then the required eight-file regression suite once. Save new results separately so the previous test evidence remains intact. Keep test_install_l2 regressions bounded with subprocess timeouts. Never edit the protected #440 guard test.
4. Request a fresh independent repair review, then a fresh managed FINAL with a new state manifest covering every real delivery file. No archive unless the new FINAL passes with the state unchanged. Keep the original failed final review and FINAL ledger line as history.

## Commit placement

The user explicitly selected "Insert repair commit (Recommended)" on 2026-11-09, approving one dedicated repair commit immediately before E and the resulting seven-entry history check. The full comparison from A's parent remains required. Preserve a backup ref of old E (77a4c70fcdc2f92550bd7c79fb4b5911dcb07100), construct the repair tree on D using a private index, and construct replayed E with the final staged tree. Atomically advance only the current branch from old E to new E; no hard reset, stash, discarded work, push or PR. The repair commit changes only the shared validator and its FIFO regression. E retains only its original refusal-related product diff relative to the repair parent; task records include the authorized ledger correction and provenance. Executed with delivery bytes preserved: dedicated repair 805c5bee6010e820eaba6eff8325a501313d34ad, replayed E fa6b7b8ff326ca9f92724c91926f4590985dbd26. Old E is retained at refs/superclaude/repairs/issue-441/pre-final-fixes. Seven-entry order and empty full protected-test diff verified. E's only product changes relative to its repair parent are the original refusal code and tests; the FIFO fix is already in the parent.

## Evidence

- artifacts/fifo-before.log: both new regressions timed out after 5 seconds before the source fix.
- artifacts/fifo-after.log: 3 FIFO-focused checks pass after the fix.
- artifacts/final-repairs-tests.log: required eight-file suite passes, 822 passed and 3 skipped.
- artifacts/delivery-repair-check.log: exactly eight note relocations, 32 real delivery paths, all eight formerly omitted byte changes affect the real helper digest in disposable copies.
- Ruff and make sync-dev/make verify-sync pass. The protected guard test and pinned plan/source remain unchanged.
- Independent repair review passed with no findings (artifacts/repair-review.json): both original final-review defects resolved, original T6/T7/T12 criteria rechecked, count-only exception retained. Fresh managed FINAL remains required; repair review is not archive approval.
- Renewed T6/T7 completion evidence and T12 blocked/Ruling/unchanged-complete records were appended under direct user authorization. Every repair evidence file in files= uses its repository-relative path (package-relative ./artifacts tokens are deliberately skipped by the helper), so the fresh FINAL state covers those bytes too. Historical failed FINAL and old ledger snapshot remain preserved.
