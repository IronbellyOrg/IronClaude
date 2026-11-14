95162a1cf2b65d545c6281bf311be8527fc97d23
A1 r1-1 F1.1 note tests/sweep/test_probes_allowlist.py:1319-1325 ac=scope amiss:n,false:n,harm:n,constraint:n The test test_ledger_over_the_limit_is_read_as_head_and_tail says "head and tail" while the behaviour (DESIGN line 62) searches the tail; a naming nit.
A1 r1-1 F1.2 note tests/sweep/test_probes_allowlist.py:463 ac=scope amiss:n,false:n,harm:n,constraint:n The FR-021 forbidden-verb scan exempts the name dispatch file-wide; it could be limited to _get(show, "dispatch", ...) lookups. The runtime refusal test already covers the argv side.
