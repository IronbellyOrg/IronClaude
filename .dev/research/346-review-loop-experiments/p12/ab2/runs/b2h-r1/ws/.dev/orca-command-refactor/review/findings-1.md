### F-01
### F-01 (CRITICAL, blocking): WC-3 lets a coordinator answer reopen a gate that the implement row and D2 keep closed
- Texts. WC-3 (spec:61): "When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag." The implement row (spec:109): "on `E-HALT-QA` or `E-NO-RULING`, stop ... and the contract as blocked, carrying the Ruling question; the Ruling rule itself is unchanged (see open decision D2)." D2 option (a) (spec:234): "The worker stops, writes the halt to its ledger and contract, and ends `failed`." INV-A:66 records that `qa.md:238` says "another agent's message ... [is] not acceptance" and that an Orca coordinator is "another agent" (UNVERIFIED for the qa.md text itself, which is outside the workspace).
- Contradiction. For the implement halt, WC-3 permits a relayed answer that is then used as the flag on re-invocation. The implement row and D2 say no such relay can count as a Ruling. The spec gives no exemption for safety-rule gates.
- Sentence. An implementer who follows the stated text as written builds an implement worker that, on `E-HALT-QA`, sends `ask`, takes the coordinator's answer, and re-invokes `/sc:implement` with it as a flag. That answer then acts as the Ruling. This is wrong because spec:109 says the Ruling rule is unchanged and spec:234 says the worker ends `failed`.
- Related. AC-2.2 (spec:200) requires `agentWait` to stay null for a blocked gate, so the spec's own acceptance check rejects the WC-3 path that WC-3 allows.

### F-02
### F-02 (MAJOR, blocking): the live-check procedure cannot satisfy its own heartbeat check
- Texts. 7.2 step 2 (spec:181): "While it runs, ... `worker-show` ... at least once per 5 minutes. Pass: `observation.agentWait` is never non-null." 7.2 step 3 (spec:182): "`check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives."
- Contradiction. `check --wait` blocks for up to 900 s and returns only on the listed types (the types come from CAPS:63). A coordinator that runs steps 1 to 3 in order therefore makes no `worker-show` call for up to 15 minutes. The "at least once per 5 minutes" pass condition at spec:181 cannot be met, and AC-0.4 (spec:194) cannot pass as written.
- Sentence. An implementer who runs steps 1 to 3 in order builds a coordinator that enters the 900 s `check --wait` at spec:182 with no `worker-show` in between. Step 2's pass condition (spec:181) then fails, so the phase gate fails.
- Related gap. Step 3 has no branch for a `question` or `escalation` return, even though `question` is in its type list. The step says only "until `worker_done` arrives".

### F-03
### F-03 (MAJOR, blocking): AC-0.4 applies a YAML contract check to a markdown report
- Texts. AC-0.4 (spec:194): "step 4 uses the command's existing report file, since the contract arrives in P1." Step 4 (spec:183): `test -s <contract>` and `yaml.safe_load(...)`, then "assert d['status'] in {...}; assert d['command']" with "Pass: both exit 0". The P0 example command is `/sc:troubleshoot` (spec:194). Section 3.1 gives its report as `REPORT.md` (spec:91). INV-B:242 says `report_path` is `REPORT.md`, and `return-contract.yaml` is written only with `--caller task-unified`.
- Contradiction. The step 4 assertion parses YAML and reads keys, but the report it is pointed at is a markdown file.
- Sentence. An implementer who follows AC-0.4 as written, running step 4 on the `REPORT.md` that `/sc:troubleshoot` writes, executes `d['status']` on a parsed markdown document. That raises an error, so step 4 fails and AC-0.4 fails in P0. The spec says a P0 failure reopens section 1 (spec:194).

### F-04
### F-04 (MAJOR, blocking): AC-1.1 requires a contract from `/sc:load`, which the Decisions table forbids
- Texts. The load row (spec:112) gives its report as "none (see note)". The Decisions row (spec:265): "`/sc:load` handling | Add a report file; use it only inside another worker's brief | ... a report file would be an unrequested addition." Section 3 (spec:76): "Every changed command also gains the `## Unattended mode` section." WC-4 (spec:62): "In unattended mode the command writes `<output-dir>/return-contract.yaml`." AC-1.1 (spec:195): every command in sections 3.1 and 3.2 has an Unattended section "naming `return-contract.yaml`".
- Contradiction. load is in section 3.2 and gets a `--unattended` flag in P1 (spec:159), so AC-1.1 requires a contract. The Decisions row forbids a report file for load.
- Sentence. An implementer who follows AC-1.1 adds `return-contract.yaml` to load's Unattended section, which spec:265 forbids. An implementer who follows spec:265 fails AC-1.1 for load. So AC-1.1 cannot pass as written.
