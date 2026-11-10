# Verification 2: N-1 against the candidate spec

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `97f56a6e69838dc9f80dfae9d1e8e0aa95413656b2559e687870566b2996ca6a` (285 lines)

## Texts located in the candidate

- `spec:63` (WC-5): "`--outcome failed` when the report says `failed` or `blocked`, or when the contract is missing, zero bytes, truncated, unparseable, lacks `status`, or has a `status` outside the four values (B-5: the default is `failed`)". WC-5 has no phase qualifier.
- `spec:79`: "These run as workers now if the brief uses the stated flags; the worker reports the named file until Phase 1 adds the contract."
- `spec:91` (troubleshoot row): "`REPORT.md` (`report_path`)".
- `spec:182` (7.2 step 3): "its `--outcome` matches the contract's `status` under WC-5".
- `spec:194` (AC-0.4): "step 4 uses the command's existing report file, since the contract arrives in P1".
- Phase table `spec:158` (P0): "no command edits"; the P0 deliverable writes `WORKER-CONTRACT.md` (section 2 rules), so WC-5 is a P0 rule. The P1 row (`spec:159`) lists "The WC-4 contract in unattended mode" as P1 work.
- Not in the workspace, so unverified: `CAPS:73`, `CAPS:76-77`, `CAPS:80`, `INV-B:49`, and the baseline wording "no report exists". The sandbox has no baseline or git history, so the "changed" origin cannot be checked. Neither point is needed to decide the outcome below.

## Table

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| N-1 | `spec:63`: "or when the contract is missing ... (B-5: the default is `failed`)"; `spec:79`: "the worker reports the named file until Phase 1 adds the contract"; `spec:91`: "`REPORT.md` (`report_path`)"; `spec:182`: "its `--outcome` matches the contract's `status` under WC-5"; `spec:194`: "step 4 uses the command's existing report file, since the contract arrives in P1" | yes (all five quoted texts match the candidate; the `spec:79` paraphrase "no contract exists until P1" is a fair reading of its "until Phase 1 adds the contract") | yes: WC-5 has no phase scope and maps a missing contract to `failed`. `spec:79` and `spec:194` place the contract in P1, so in P0 the contract is missing. A P0 run that completes and writes `REPORT.md` therefore gets `--outcome failed` under the literal WC-5 text, and `spec:182` step 3 has no contract `status` to match, so AC-0.4 cannot pass as written | confirm | Every quoted text exists, and the wrong outcome follows from `spec:63` applied in P0, where `spec:79` and `spec:194` say there is no contract. The baseline and origin claims are unverified, but the outcome does not depend on them. The `CAPS:73` citation is unverified and not needed. |

confirmed: N-1
