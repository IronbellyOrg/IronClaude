## Prior blocking findings (re-check)

| Prior id | Status | Evidence (AFTER text) |
|---|---|---|
| F1 | resolved | F1's text lives in FR-82, which this pass rewrote. AFTER FR-82 still reads "The only code that may write is `issue_watch/repo_init.py` (only `gh label create` for the trigger label, after the owner's chat OK) and the coordinator-only `issue_pipeline/complete.py` (FR-83); `github.py` and the cycle never", and its check still reads "planb `test_security_invariants.py:1059-1079` unchanged (it names both writers and keeps `github.py` and `cycle.py` read-only)". Verified in planb: the scan at lines 1059 to 1076 has `_WRITER_MODULES = {"complete.py", "repo_init.py"}` and asserts both are writers, so `repo_init.py` must stay a writer, which FR-82's new "separate step of `repo_init.py`" keeps. FR-83, SEC-07 (four names), step 6, S9 and L-08 still carry the second writer. Not regressed. |

Review 2 reported no other blocking finding, so there is nothing else to re-check as blocking.

### Review-1 Medium findings the owner asked to have confirmed (not blocking; graded by the same rule)

| Id | Status | What was checked | Residual |
|---|---|---|---|
| F4 | resolved in substance | The one rule is in Q04 (section 2), 3.1, FR-32, SEC-01 ("A push go never covers a merge, and a merge go never covers a push"), SEC-15 (line 245 wording, R25 amendment, wait on OA-7), SEC-22, section 8 rules, 13.2 probe row, OA-7, L-07, Appendix A. No leftover "a typed go precedes every push" remains (grep). It matches the Q04 verdict item by item, and the verdict's fence text matches `SKILL.md:262, 342 to 346`. | H1, H2, H3, H4 |
| F6 | resolved in substance | FR-84 states, for lines 296, 298, 300: one adoption record (the FR-29 file), approval from the owner's chat words through `check-approval`, no label or Status mirror, and the SEC-07 grant in place of "that issue's grant row". FR-29 agrees on file name, exclusive create and timing (record before `worker-start`, ack after the record). L-07, S8 and Appendix A carry it; 12.4 lists it. The quoted phrases exist in the installed contract. | H8, N16, N17, N18 |
| F10 | resolved in substance | The label check only reads in FR-82, FR-23, L-08 and OA-28b; creation needs a per-repo chat OK in FR-82, S17 and 10.4; X-18 records that OAG3's class-level cover is not adopted and why (a standing GitHub write outside SEC-07). The circularity is gone: the throwaway repo's label is made on a named OK or by hand before the six checks. | H5, H6, N20 |
| F14 | resolved | FR-07 now names both grants and the true fixture line (`conftest.py:286`, verified) and adds `test_fixtures_carry_no_refused_grant`. | H7 |
