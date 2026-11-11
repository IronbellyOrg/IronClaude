### B1
### B1 (= M8, open). The load row gives a contract that WC-4 does not allow, and the phase rows say the contract is not added
- Origin: changed (spec:112 is on a changed line; spec:268 is on a changed line).
- Issue, three conflicting texts:
  1. WC-4 says the contract "carries at least" `status`, `command`, `report_path` (if any), `artifacts` (every other file written) and, when blocked, `blocked_question` (spec:62). The load row writes "status-only contract ... (`status`, `command`; no `report_path`, as WC-4 allows)" (spec:112). `artifacts` is required by WC-4 and is absent from the row, so the row contradicts WC-4 on a field WC-4 does not make optional.
  2. The Decisions row says the status-only contract "meets WC-4 and AC-1.1" (spec:268). Point 1 shows it does not meet WC-4.
  3. The load row keeps "P1 (usage line only)" (spec:112, Phase column), and the P1 scope lists "load (usage line only)" (spec:159). An implementer who follows P1 adds no Unattended-mode section and no contract for load, so AC-1.1 (spec:196), which requires such a section for every command in 3.1 and 3.2, fails for load.
- Sentence that holds with no further assumption: an implementer who follows the load row writes a contract with `status` and `command` only, and WC-4 (spec:62) says it must also carry `artifacts`; an implementer who follows the P1 phase text adds nothing for load, and AC-1.1 (spec:196) then fails.
