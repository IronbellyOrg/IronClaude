# D-P2-24, option B (alternative): nest what can be nested, record only what cannot

1. release-split Part 4 calls `sc:analyze` nested with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`sc:analyze` accepts the flag since P1), lists its contract in `artifacts`, and falls back to inline verification only if the call fails. release-split's nested list becomes brainstorm, adversarial, analyze (and `EXPECTED_NESTING`, the spec row and the tests change accordingly).
2. reflect Wave 1B keeps skipping `tech-research` (it cannot be nested: no Unattended mode), recorded in the contract.

Claimed strengths: follows spec section 2.1 literally (a callee that accepts the flag gets the flag); keeps the stronger verification.
Claimed weakness: one more nested directory, a nested-list change in the test pin and the spec, and a heavier run; the spec row for release-split names no analyze call.

## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.
