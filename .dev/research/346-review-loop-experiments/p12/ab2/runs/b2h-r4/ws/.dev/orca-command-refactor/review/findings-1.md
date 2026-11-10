### B-1
### B-1 (BLOCKING): section 3 says ready commands change only by their small fixes, but P1 and AC-1.1 require every one of them to change
- Issue: `spec:79` says "The only command changes are the small fixes in the last column" for the ten ready commands. `spec:159` (P1) requires the `--unattended` flag "accepted by every command in sections 3.1 and 3.2", and `spec:195` (AC-1.1) requires a `## Unattended mode` section in every 3.1 command. Brainstorm (`spec:84`) and init-lite (`spec:87`) have no fix, so an implementer following `spec:79` leaves them untouched and fails P1 and AC-1.1. Following P1 and AC-1.1 adds a change that `spec:79` denies.
- Sentence: "An implementer who follows `spec:79` leaves brainstorm and init-lite unchanged, and that is wrong because `spec:195` requires them to carry a `## Unattended mode` section."
- Severity: MAJOR, blocking (two stated texts contradict).

### B-2
### B-2 (BLOCKING): the P0 acceptance check cannot pass for a command whose report is not a YAML contract
- Issue: `spec:194` (AC-0.4) runs the 7.2 live check on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` and says "step 4 uses the command's existing report file, since the contract arrives in P1". Step 4 (`spec:183`) asserts `yaml.safe_load(...)` with `d['status']` in four values and `d['command']`. Troubleshoot writes `REPORT.md` and `audit.log`, not YAML (`INV-B:49`; `spec:91`). Adversarial's contract filename is not fixed (`INV-A:60`). So step 4 fails by construction for troubleshoot and cannot be checked for adversarial.
- Sentence: "An implementer who runs AC-0.4 step 4 on `/sc:troubleshoot` parses `REPORT.md` as YAML, and that is wrong because `REPORT.md` has no `status` field and the check fails."
- Severity: MAJOR, blocking (acceptance criterion cannot pass as written).

### B-3
### B-3 (BLOCKING): the contract location rule (WC-4) conflicts with the per-command rows, so the coordinator cannot know the path before dispatch
- Issue: `spec:62` says the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed", and it must be "known before dispatch". Three rows break this: adversarial (`spec:83`) is to be changed to `<output>/adversarial/return-contract.yaml`, which is not `<output-dir>/return-contract.yaml`; workflow (`spec:92`) writes `.dev/tasks/to-do/<id>/return-contract.yaml`, not into a passed directory; tdd (`spec:90`) and init-lite (`spec:87`) take `--output <file>`, which is a file, not a directory. The inventory records that real adversarial runs wrote the contract in two different places (`INV-A:60`). WC-4's "keep their fields" wording does not say the location is kept.
- Sentence: "An implementer who writes the adversarial contract at `<output>/return-contract.yaml`, as `spec:62` says, breaks the path that `spec:83` requires; and one who follows `spec:83` breaks `spec:62`."
- Severity: MAJOR, blocking (two stated paths contradict, and the coordinator's brief depends on the path).

### B-4
### B-4 (BLOCKING): `--unattended` auto-accepts reflect remediation, which lets the worker approve its own corrective work
- Issue: `spec:88` (P2 for reflect) says "Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt". Headless auto-accept "skips the gates" for auto-fixable registers (INV-B:109, citing `remediation-handoff.md:239-247`, UNVERIFIED here). `spec:122` (tasklist) passes `--unattended` to every reflect at Stage 10.5, so the same auto-accept applies inside tasklist. The spec's own safety rule for implement (D2, `spec:236`) says the rule "exists to stop an agent approving its own work". The inventory recommended removing the nested remediation offer at Stage 10.5 (`INV-B:295`); the spec does not disposition that recommendation. SA-6 (`spec:151`) keeps the headless rule for `claude --print`; it does not require the unattended path to reuse it.
- Sentence: "An implementer who follows `spec:88` runs `/sc:workflow` or `task-builder` corrective work from a worker with no person approving it, and that is wrong because the spec treats agent self-approval as a safety boundary in D2 (`spec:236`)."
- Severity: MAJOR, blocking (safety-boundary risk; the grading rule names it).

### B-5
### B-5 (BLOCKING): WC-5 maps an empty, truncated or unrecognised contract to `succeeded`
- Issue: `spec:63` sends `--outcome failed` "when the report says `failed` or `blocked`, or no report exists" and `--outcome succeeded` "otherwise". A contract that exists but is empty, truncated (killed mid-write), unparseable, or has a `status` outside the four values in `spec:262` falls into "otherwise". The literal text therefore reports a crashed run as succeeded. Orca settles the Task on `succeeded` and then starts dependents (CAPS:76-77, CAPS:84-88).
- Whittaker, FR-2.1 (Zero/Empty): "I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (spec:63)** fails when **the contract exists with zero bytes or a truncated body**. Concrete attack: the command is killed after creating `return-contract.yaml`; the file exists, the status is absent, the branch falls to 'otherwise', `worker_done --outcome succeeded` is sent, the Task settles `completed`, and a dependent Task runs on no output." Trace: before = crashed run; after = Task `completed`.
- Sentence: "An implementer who follows `spec:63` as written sends `succeeded` for an empty contract, and that is wrong because the run did not finish."
- Severity: MAJOR, blocking (concrete wrong outcome from the literal text).
