# Ledger errata

The ledger (`../progress.md`) is append-only, so a wrong pointer in an already written line is corrected here instead.

| Ledger line | Token as written | Correct pointer | Note |
|---|---|---|---|
| `T2: complete ...` | `T2.AC2@./artifacts/t2-pytest.log:45` | `./artifacts/t2-pytest.log:43` | The log has 44 lines; line 43 is the outcome line `32 passed in 0.14s` and line 44 is `rc=0`. The executor copied the reviewer's line number without checking it. The other T2.AC2 token (`tests/skills/test_clickup_claim.py:148-156`) is unaffected. |
| `T4: complete ...` | `T4.AC2@./artifacts/t4-template-checks.txt:70` | `./artifacts/t4-template-checks.txt:75` | Line 70 is one of the heading lines of the check (`55:## Alternatives Considered`, still heading-order evidence); the `grep -il clickup` outcome `rc=1 (1 = no match)` is line 75. The other T4.AC2 token (`issue-bug-complex.md:77`) is unaffected. |
