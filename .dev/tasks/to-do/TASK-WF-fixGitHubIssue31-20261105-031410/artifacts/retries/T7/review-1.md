8e0aa4769daecdba07cac3080bf79ea32da9019b tree=60f575652cc92a42ff60d36e2fab7416b0e45c51
AC marks (reviewer, summary): T7.AC1 met tests/unit/test_ccsession_tag.py:2548-2738,1700,1797 and ./artifacts/t7-orca-tests.log (85 passed); T7.AC2 met ./artifacts/launch-paths.md:5-31
F7.1 sev=minor ac=scope at=tests/unit/test_ccsession_tag.py:1797 chk=n,n,n,n family=typed-ahead-assert: the typed-ahead test never checks that the typed text stays waiting for Claude (the behaviour is right; reviewer confirmed with a stdin-reading fake Claude).
F7.2 sev=minor ac=T7.AC1 at=tests/unit/test_ccsession_tag.py:2631 chk=n,n,n,n family=weak-extra-assert: the 245/246-byte CCSESSION_NAME test asserts the topic only, not the arguments.
F7.3 sev=minor ac=scope at=tests/unit/test_ccsession_tag.py:2697 chk=n,n,n,n family=stale-record: the terminal and no-terminal runs of the print-mode and Claude --name tests share one record.json (also :2666).
