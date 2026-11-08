# Gate 3 fix verification (structural, rf-qa), fix cycle 1

Status: Complete
Provenance note: the rf-qa verifier could not write `qa/qa-fix-verification.md` because a freshness hook rejected every Write to that path (stale read entry for a file that does not exist). This file was written by the executor from the verifier's returned message, unedited in substance, so the verdict and findings exist on disk. Date: 2026-11-07.

## Items Reviewed

| # | Finding | Result | Evidence (report lines) |
|---|---|---|---|
| 1 | three contradiction markers | PASS | `[CONTRADICTION` count 0; issue-type field verified (336/808/2009); option letters follow the binding lettering (764/895/905/909, 743/1050/1901); nine revisit conditions identical in 5.15 and Section 6 (954-966 vs 1313-1327); 7.8 and 8 cite that list |
| 2 | false "no Python calls orca" | PASS | corrected at 341/513/685/1551; `resolve_orca` in step 3.4; `install_user_setup.py:198-263` and `_ORCA_CLIS` line 35 accurate |
| 3 | decision-label collision | PASS | D1-D3 owner decisions (129-139, 583, 635, 1520-1522, 1838-1840); Qn only as open-question rows |
| 4 | Phase 4 read rules | PASS | one rule at 1613 matched by SC-7/SC-13, step 1.5, test 4.5, checklist |
| 5 | title/body reach the poller | PASS | `--jq` mandatory in the Project discovery call (1618), SC-5 (625), hostile-fixture test (1639); gh `queries.go` 558-566 and 673-678 verified |
| 6 | candidate cap starvation | PARTIAL | `is:open` and cap-after-local-skip present (1618, 1661); residual defect NEW-1 |
| 7 | launch timeout duplicate session | PASS | timeout maps to `unknown` (1592), `launch_cwd` stored (1650), tests 1707-1708; Q3 quotes the `orca agent launch --help` retry rule (verified by running it) |
| 8 | gate list sync-dev | PASS | `make sync-dev` before pytest, `make verify-sync` after (1732, 1407, 1541, 636, 1823); `test.yml:32-38`, Makefile 109/166 verified; `.claude/skills` and `.claude/commands` absent |
| 9 | orphaned gap G15 | PASS | step 1.6 and Q36 (697, 1538, 1886, 1970, 2124) |
| 10 | wrong cross-references | PASS | step pointers fixed; step 7.6 has 11 checks and step 1.10 lists the same 12 Q-numbers (1542, 1746) |
| 11 | false carry claim | PASS | Q34/Q35 (1884-1885); softened intro (754); sources verified |
| 12 | idempotency key | PASS | one rule, `(repository, issue number)` with approval event id as an attribute (881, 1650, 1669, 1987) |

Structure: sections 1 to 10 in order, Table of Contents (12-98) matches headings, no placeholders.

## New blocking findings (introduced by the fixes or residual)

- **NEW-1 (residual of finding 6), IMPORTANT, blocking:** the cap can starve new issues again after the lease expires. Step 3 (1661) drops `launched` entries before the cap, but `may_dispatch` (1650) and the "Second cycle" test (1702) expect a `launched` entry to be retried or abandoned after the lease. Reading 1 (`launched` always dropped): the retry/abandon path is dead code. Reading 2 (`launched` dropped only inside the lease): after 60 minutes handled issues with a claim marker come back, are skipped at step 6 (1664) and consume cap slots, which is the original starvation. Fix: when step 6 finds a marker, move the entry to a terminal state (for example `claimed`) that step 3 always drops; give the "Many already-handled candidates" test (1709) an entry older than the lease.
- **NEW-2 (introduced by fix 2), IMPORTANT, blocking:** the PATH-stub end-to-end test can reach a real Orca. `resolve_orca` (1592) tries `orca-ide` then `orca` using the real `shutil.which`; steps 6.1/6.2 (1728-1729) stub only `orca`, `gh` and `git`. On this host `which -a orca-ide` returns `/home/coder/.local/bin/orca-ide`, so the test would probe, and possibly launch through, the real binary, breaking the "nothing runs live" rule (1466). On a host with no Orca the unit tests would raise `E-ORCA-NOT-FOUND` because the plan never says how `shutil.which` is faked. Fix: inject the candidate names or the lookup function into `resolve_orca`; make the e2e stub every candidate name (or restrict PATH to the stub directory) and monkeypatch the lookup in unit tests.

## Minor notes (not rechecked)

- Unescaped `|` inside code spans breaks table column counts at lines 691, 838, 847, 935, 1128 (pre-existing) and 1556 (new, `cwd: Path | None`); escape as `\|`.
- `str(int(number))` at 603, 624, 694, 1361 conflicts with the stricter `type(number) is int` in step 3.2 (1590).
- Design-doc default IDs `D1..` (1529, 1541) collide with owner decisions D1-D3; the label rule at 139 names D1-D3 while 9.1 also has D4-D6.
- A `pending` entry gets a fresh launch after the lease (1650), conflicting with "never retry as a fresh launch" (1584).

Confidence: verified 16/16. Sections 6.2 to 6.4 tables were only structurally checked.

Open blocking findings: 2 (NEW-1, NEW-2); before this cycle: 12.

VERDICT: FAIL
