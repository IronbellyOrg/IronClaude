# Final repair probes

## Blocking FIFO open

Defect: data-file validation opens a FIFO read-only before checking its type; both installer conflict detection and owned-hook status use this function.

Probe: `grep -n -E '_l2_data_ok|O_RDONLY.*O_NOFOLLOW' src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`

Before: shared validator at 1186, blocking open at 1190, callers at 1243 and 1382. Bounded runtime regressions reproduced two 5-second TimeoutExpired failures (install_l2 and l2_status) in artifacts/fifo-before.log. Coupled sites: descriptor open, existing fstat regular-file/uid/mode checks, both callers, FIFO inode/directory-preservation assertions.

After: shared validator now includes O_NONBLOCK with O_RDONLY and O_NOFOLLOW. Regular-file/uid/mode checks and both callers are unchanged. artifacts/fifo-after.log records 3 passing FIFO tests (the two new data-path cases plus an existing hook-path case). Both new cases return conflict/data-file-differs within the subprocess timeout and preserve the FIFO and every hook directory entry. Installation may change the directory's own mtime through its existing temporary publication; status leaves even that unchanged. First post-fix run rejected promptly but failed the overly strict installer directory-mtime assertion; only that fixture expectation was corrected. Full required suite: 822 passed, 3 skipped in artifacts/final-repairs-tests.log.

## Malformed delivery paths

Defect: notes@ references at the end of eight files= fields are parsed as part of the last pathname instead of evidence tokens. Coupled records: T2, T4, T5, T6, T7, T8, T9 and T10; preserve all other fields, notes and original final result.

Before: progress-before-final-repairs.md preserves the exact ledger. The previous helper manifest has 24 real paths and 8 absent annotated names; final-review.md lists all eight. Authorization permits correcting those fields; it does not waive either final finding.

After: exactly eight note relocations verified against the preserved ledger; prior verdicts, citations, history Ruling and original FINAL unchanged. Corrected manifest has 32 actual files with no absent annotated names. artifacts/verify-delivery-repair.py used disposable copies and the real archive helper's digest function to mutate and restore each formerly omitted file; all eight byte changes changed the digest, and every restoration restored it (artifacts/delivery-repair-check.log). Live delivery bytes were never modified by this probe.
