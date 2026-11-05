68452bae4a42000ec0997738b027d452c5256ffc
A1 r1-1 note (reviewer) minor tests/unit/test_ccsession_tag.py:2203 ac=T6.AC2 n,n,n,n test_auto_name_two_calls_in_the_same_second_differ asserts at least 2 distinct labels in 3 calls; it leans on the random part (it fails when the part is removed).
A2 r2-1 note tests/unit/test_ccsession_tag.py:2229 ac=scope n,n,n,n three behaviours outside the listed cases have no test that fails when they are removed: the trailing-hyphen strip (ccsession:636), the validate_label fallback (ccsession:653) and the -w check inside the writable test (ccsession:643).
