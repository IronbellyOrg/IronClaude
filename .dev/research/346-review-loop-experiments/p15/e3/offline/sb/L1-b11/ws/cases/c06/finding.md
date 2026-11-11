### F-4. MAJOR label, graded Medium. Phase 1 ships `--unattended` on commands whose gates and outward defaults are only converted in Phases 2 to 4.
- Experts: Whittaker (Sequence), Adzic.
- Locations: `SPEC:159` (P1: flag accepted by "every command in sections 3.1 and 3.2"); `SPEC:160-162` (P2 to P4 convert the gates); `SPEC:67` (WC-9: under `--unattended` outward defaults are off); `SPEC:79` ("The only command changes are the small fixes").
- Grading check: needs a guess that a coordinator dispatches such a command between phases. The window is real: after P1, `/sc:auggie-review <PR> --unattended` is accepted yet still posts to GitHub without a prompt (`SPEC:100`, `INV-A:38`) until P2. The text also contradicts itself on whether a ready command changes (`SPEC:79` versus `SPEC:159`).
- Recommendation: either accept `--unattended` only on a command once its gates are converted, or state that the flag means nothing until the command's own phase.
- Priority: Medium. Quality impact: Consistency +1.
