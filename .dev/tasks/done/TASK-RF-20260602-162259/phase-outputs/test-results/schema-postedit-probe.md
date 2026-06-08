# On-Disk Schema Post-Edit Probe (Step 4.7)

**Captured:** 2026-06-02 17:59
**Verdict: PASS** — bug closed.

Reads the same on-disk JSON the runtime (`tool_writer.load_schema`) validates against:

| step | re.match(pattern, "M1-D01") |
|------|------------------------------|
| extract | True |
| extract_tdd | True |
| generate | True |
| merge | True |

`merge == generate`: **True**.

All four schemas now contain the MD arm and accept `M1-D01`. The merge≡generate invariant is preserved.
