# D-P2-22, option B (alternative): keep one deleted line and add a correcting line beside the stale one

Keep the check strict where possible: delete only the "Nested invocations" bullet (line 75, which becomes false), so workflow.md shows exactly one deleted line, and leave the P1 "Contract" bullet (line 72, with its `.dev/reflect/` wording) untouched, adding a new line after it that says that under `--unattended` the reflect files are in `<report-dir>/nested/reflect-<n>/`. The stale sentence then stays in the file beside the correction.

Variant B2 (zero deletions): keep both old lines and add two new lines that override them ("Under P2 ... instead"). Check ADDITIVE needs no exemption at all, at the price of two sentences that contradict their neighbours.

Claimed strengths: the additive rule holds (B2) or needs a one-line exemption (B); history of the P1 text stays visible.
Claimed weakness: a worker reading the section meets a false sentence and a correcting sentence; the P1 test phrases that pin the old wording must be kept or edited.

## How to judge (the same for every decision)

Read the cited files in the working tree (they hold uncommitted P2 edits) before arguing. Judge each option on: (1) is the command or skill text true and unambiguous when a worker runs it under `--unattended`; (2) does it respect the spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` section 2.1 (nested propagation: a step whose callee does not accept `--unattended` is made gate-free or skipped and recorded), WC-4 (report and contract), WC-9 (no commit, push or staging by a worker; the coordinator owns outward actions) and WC-11 (parallel-safe writes), and SA-1/SA-4 (a standalone run behaves as today; edits to command files are additive unless a named defect fix); (3) size of the change and risk to existing pinned tests (`tests/skills/test_worker_contract.py`, the Check ADDITIVE rule, the write-verb classification table); (4) what a coordinator and the owner gain or lose. End with one recommended option and the one-sentence reason.
