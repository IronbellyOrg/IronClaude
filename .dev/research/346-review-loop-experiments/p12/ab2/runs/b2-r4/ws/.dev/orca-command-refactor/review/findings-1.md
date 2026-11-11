### F-1
### F-1 (blocking, CRITICAL). WC-4's contract path rule contradicts the briefs and fixes that the spec itself gives
- Stated texts that disagree:
  - SPEC:62: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - SPEC:73: "the output directory, so the report path is known before dispatch (WC-4)".
  - SPEC:87 and SPEC:90: init-lite and tdd briefs pass "`--output <file>`" (a file). SPEC:200 (AC-2.2) runs `/sc:tdd "auth" --unattended --output <file>` and requires "contract `status: blocked` with a non-empty `blocked_question`".
  - SPEC:83: adversarial contract fixed to `<output>/adversarial/return-contract.yaml`, but WC-4 says `<output-dir>/return-contract.yaml`.
  - SPEC:92: workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, and the row passes no output directory. INV-B:272 says that contract is not written for pre-creation stops (`refs/return-contract.md:39`), so the spec's own fix "Write the contract for pre-creation STOPs too" (SPEC:92) has no `<id>` directory to write it into.
  - SPEC:182 and SPEC:183: step 3 requires "its report path is the WC-4 contract path"; step 4 runs `test -s <contract>`.

### F-2
### F-2 (blocking, MAJOR with concrete wrong outcome). AC-1.1 and the P1 scope require a contract for `/sc:load`, which the spec says gets none
- Stated texts that disagree:
  - SPEC:159 (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; same row: "The WC-4 contract in unattended mode".
  - SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - SPEC:76: "Every changed command also gains the `## Unattended mode` section".
  - SPEC:112 (load row): report "none (see note)"; "use it as a step inside another worker's brief, not as its own Task".
  - SPEC:265 (Decision): "a report file would be an unrequested addition".
  - SPEC:154: "Later phases do not start until the earlier phase's checks in section 7 pass."
