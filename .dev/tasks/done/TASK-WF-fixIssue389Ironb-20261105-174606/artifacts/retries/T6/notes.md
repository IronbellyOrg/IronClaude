5efc9ab849dd911f2092df60dd0dbfab363e36a4
A1 r1-1 F1.1 minor tests/unit/test_ccsession_tag.py:1308 ac=scope n,n,n,n the refresh-note test sets CCSESSION_MODELS_REFRESH=1 where the brief says leave it unset; the test module's autouse fixture sets it to 0, so it cannot stay unset, and 1 equals the launcher default; the test fails on the unfixed launcher (artifacts/t6-unfixed-check.log)
