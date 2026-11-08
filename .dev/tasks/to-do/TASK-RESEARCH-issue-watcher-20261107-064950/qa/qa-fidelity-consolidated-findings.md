# Consolidated fidelity findings (Gate 4, fix cycle 1)

Sources: `qa/qa-source-fidelity-report-1.md` (VERDICT: PASS, 6 minor notes) and `qa/qa-source-fidelity-report-2.md` (VERDICT: FAIL, 1 blocking, 5 minor). Consolidated 2026-11-07 by the executor. Report under review: `RESEARCH-REPORT-issue-watcher.md`.

Count line: total findings 12 (1 blocking, 11 minor), blocking 1.

| # | Finding | Location in report | Severity | Blocking | Originating agent(s) | Proposed fix |
|---|---|---|---|---|---|---|
| 1 | Phase 4's five-filter table, row 4 (report line ~1612) says `status:Backlog` "is documented for UI filtering only". The cited gh manual page and the local `gh project item-list --help` both show status filters used with `--query` on that same command (`assignee:octocat -status:Done`, `label:bug -status:Done`); research file 01 line ~152 recorded this example and the report dropped it. The conclusion does not change (whether the API host accepts `status:Backlog` and the JSON schema stay [UNVERIFIED], Q8), but the "UI filtering only" wording is false against the cited page. | Section 8 Phase 4 filter table row 4 (~1612); optionally the option-A cell for R4 in the Requirement Scoring table (~1265) | IMPORTANT | yes | fidelity agent 2 | Replace the "UI filtering only" clause with: the gh manual for `gh project item-list --query` shows status filters in its examples (`assignee:octocat -status:Done`); whether the API accepts exactly `status:Backlog`, and the JSON schema, remain [UNVERIFIED] (Q8); align the R4 option-A cell wording if it repeats the claim. Read the cited page text or `gh project item-list --help` before editing. |
| 2 to 12 | Minor notes (not fixed): `WORKER-CONTRACT.md:112` paraphrase; step 4.5 write-token rule "modelled on" `assert_no_retrigger_call`; line-count drift (`origin_repo.py` 195, `planning_status` :10, `identify()` to 248, `bug_report.yml` line 28, `install_orca_skills` to 278); detail omissions (`E-WORKER-NO-OUTPUT`, ClickUp `page_cap`, `launch-job-identity.sh` notes); `which -a orca-ide` also lists `/usr/bin/orca-ide` and `/bin/orca-ide`; "the only follow-up A needs in the Coder repo" is stronger than the research supports; earlier sections still show `str(int(number))`. | various | MINOR | no | both agents | notes only |

Consolidated verdict: FAIL (1 blocking finding). Minor findings remain notes.
