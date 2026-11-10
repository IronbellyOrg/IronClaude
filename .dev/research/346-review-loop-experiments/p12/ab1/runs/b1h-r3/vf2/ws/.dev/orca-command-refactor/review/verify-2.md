# Verification 2: B1 against the candidate spec

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (288 lines)
sha256: `bddecb0d53d012639197cb333a623b97ec5dd535120f7fee296fb97a980e41db`

## Texts found in the candidate

| Ref | Line | Text as it stands in the candidate |
|---|---|---|
| WC-4 | 62 | "It follows the return-contract pattern several commands already use and carries at least: `status` (one of ...), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`." |
| Load row | 112 | "load \| no gate \| status-only contract under `--unattended` (`status`, `command`; no `report_path`, as WC-4 allows) [M8] \| n/a \| none: use it as a step inside another worker's brief, not as its own Task; ... \| `cmd/load.md:22,42-43,52,82`; `INV-B:31,57-65` \| P1 (usage line only)" |
| Decisions row | 268 | "`/sc:load` handling \| Add a report file; use it only inside another worker's brief \| ... Under `--unattended` it writes a status-only contract with no report file [M8], which meets WC-4 and AC-1.1 without adding a report. Only its usage-line defect is fixed." |
| P1 phase row | 159 | "**P1. Report files and commands with no gate** \| The WC-4 contract in unattended mode; the `--unattended` flag accepted by every command in sections 3.1 and 3.2 ...; ... \| analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow \| ..." |
| AC-1.1 | 196 | "P1 \| AC-1.1 \| `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` ... \| passes" |

Supporting structure checked: `load` sits in the 3.2 table ("Needs a change (27)", starts line 94), so AC-1.1 covers it. Section 2.1 (line 51) and the lead-in of section 3 (line 76) say every changed command gains an `## Unattended mode` section. P1 is the only phase that lists `load`.

## Findings

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| B1 | WC-4 (line 62) lists `artifacts` (every other file written) with no "if any" qualifier, unlike `report_path` and `blocked_question`. The load row (line 112) writes the contract with `status` and `command` only. The Decisions row (line 268) says that contract "meets WC-4 and AC-1.1". The P1 row (line 159) and load row (line 112) say `load` gets only "(usage line only)" in P1. AC-1.1 (line 196) requires a `## Unattended mode` section for every command in 3.1-3.2, and `load` is in 3.2. | yes (all five texts match the quoted wording; the only elision is "..." in the load row and P1 row) | yes | confirm | (a) WC-4 says the contract "carries at least" `status`, `command`, `artifacts`, so the load row's contract, which omits `artifacts`, does not meet WC-4 and the text gives no basis for omitting it when no other file is written. (b) Point 2 (line 268) contradicts this, as the finding says. (c) Following the P1 text for `load` adds only the usage-line fix, so no `## Unattended mode` section is added, and AC-1.1 fails for a 3.2 command. The "(usage line only)" qualifier is what limits P1 for `load`; no other text in the candidate adds a section for it in another phase. |

Note on the wording of the wrong outcome: the finding's sentence "WC-4 says it must also carry `artifacts`" follows from the text of WC-4 (line 62) with no added assumption. The reading that `artifacts` may be empty when no other file is written is not stated in the candidate, so it does not rescue the load row.

confirmed: B1
