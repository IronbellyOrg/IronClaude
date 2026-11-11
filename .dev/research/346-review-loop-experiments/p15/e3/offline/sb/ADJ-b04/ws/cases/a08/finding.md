### F-09 (MINOR, MEDIUM): the Phase 0 runs and section 3.1 briefs omit `--unattended`, which section 2.3 requires

- Location: line 73 (2.3: each brief states "the exact command line including `--unattended`"); line 79 and 81-92 (3.1 "Brief must pass" columns, no `--unattended`); line 158 and line 194 (P0 smoke runs without it); line 184 (7.2 step 5: transcript search for `AskUserQuestion`).
- Issue: P0 is the only evidence for the decision (line 43), and it runs the commands in attended mode, because the flag does not exist until P1. The spec does not say so. Step 5 then tests the wrong mode.
- Recommendation: state that P0 runs are attended, and that the unattended behaviour of each ready command is first tested in P1 (AC-1.2).
- Expert: Adzic.
