**F-1 [BLOCKING] The brief must carry `--unattended`, but the P0 smoke runs must not.**
- Experts: Wiegers (lead), Adzic, Crispin.
- Text: `SPEC:73` (section 2.3) says each Task's brief states "the exact command line including `--unattended`". `SPEC:158` (P0) runs three commands "as real Orca workers, invoked directly", and `SPEC:194` (AC-0.4) lists them without `--unattended`. The flag is first introduced in P1 (`SPEC:159`), and the WC-4 contract exists only in unattended mode (`SPEC:62`).
- Grading sentence: an implementer who follows `SPEC:73` for the P0 runs passes `--unattended` to commands that do not accept it yet, and an implementer who follows `SPEC:194` omits it, which breaks `SPEC:73`. The two stated texts contradict each other, and the spec does not say which applies in P0.
- Recommendation: state in `SPEC:73` that P0 briefs omit `--unattended`, or move the brief requirement to P1 onward.
- Priority: High.
