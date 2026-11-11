# Revise 1

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place). Baseline: .dev/orca-command-refactor/specs/history/spec-v1.md, sha256 d3cdbe57...5200d. Revised sha256 cbaee912425ccadcbc06bd6c2dd562fc87afea9b7b20dc55342bb7c482b347f0.
Brief: REVISE prompt; ids M1, M2, M3, M4, M5, M6 (review/round1.md Reviser brief, confirmed in review/verify-1.md). Minor and Medium findings left alone. No PASS awarded. Line numbers are in the revised spec; the inventory source lines behind the tdd/workflow/research rows are not in the sandbox (UNVERIFIED); every edit rests on the spec's own text.

## Byte accounting

Size before: 57763 bytes. Size after: 59637 bytes. Net +1874.
Each edit replaced a fragment; deleted = old fragment bytes, added = new fragment bytes.

Some edits serve more than one id, so the exact ledger is per edit; it sums to the totals above:

| # | Edit | Findings | Deleted | Added | Net |
|---|---|---|---|---|---|
| 1 | WC-4 text (62) | M1, M2, M3 | 247 | 736 | +489 |
| 2 | Section 2.3 brief sentence (73) | M3, M4 | 73 | 205 | +132 |
| 3 | Section 3 intro (76) | M1, M5 | 148 | 255 | +107 |
| 4 | load row (112) | M5 | 86 | 147 | +61 |
| 5 | workflow row (92) | M3 | 73 | 158 | +85 |
| 6 | 7.2 step 3 (182) | M4 | 102 | 306 | +204 |
| 7 | AC-0.4 (194) | M4 | 105 | 134 | +29 |
| 8 | AC-1.1 (195) | M5 | 172 | 198 | +26 |
| 9 | AC-1.2 (196) | M5 | 70 | 87 | +17 |
| 10 | AC-2.2 and new AC-2.2b (200-201) | M6 | 355 | 1079 | +724 |
| | Total | | 1431 | 3305 | +1874 |

Per finding, counting a shared edit in full for each id it serves (so the column over-counts the total): M1 edits 1, 3 net +596; M2 edit 1 net +489; M3 edits 1, 2, 5 net +706; M4 edits 2, 6, 7 net +365; M5 edits 3, 4, 8, 9 net +211; M6 edit 10 net +724.

## Dispositions

| Id | Disposition | Where | What changed |
|---|---|---|---|
| M1 | Applied | spec:62 (WC-4), spec:76 | WC-4 no longer defines the contract as `<output-dir>/return-contract.yaml` where the dir is the `--output` value. One rule: the contract goes in the passed directory, or in the directory containing the file when `--output` is a file; rows that name another location (adversarial `<output>/adversarial/`, spec:83; workflow, spec:92) override it, and that path is the one AC-1.4 (spec:198) pins. Section 3 "Contract" definition (spec:76) points to WC-4 instead of repeating the directory form. Narrowed wording, no new flag, as the finding recommended. |
| M2 | Applied | spec:62; spec:200 | Same WC-4 rule covers the tdd (spec:90) and init-lite (spec:87) `--output <file>` rows: contract at `<directory of file>/return-contract.yaml`. AC-2.2 now names that path for the `/sc:tdd ... --output <file>` run, so `<contract>` in 7.2 step 4 (spec:183) is defined. |
| M3 | Applied | spec:62, spec:73, spec:92 | Removed the unconditional "known before dispatch" claim from WC-4's title and from the brief paragraph. WC-4 now says the path is known before dispatch only when the row builds it from brief values, otherwise the coordinator reads it from `worker_done --report-path` (finding's second option); the rows it lists as overriding are adversarial, workflow, implement, cleanup-audit, index-repo, and research, recommend, review-translation, task, save (no placing flag). The workflow row (spec:92) states `<id>` is made by the run. No output flag added to any command, so spec:159 (P1) is unchanged. |
| M4 | Applied | spec:73, spec:182, spec:194 | Step 3 now reads in P0 as: `--outcome` matches the command's own verdict in its existing report, and the report path is the existing report file named in 3.1 (same relaxation step 4 already had). The P0 brief omits `--unattended` (it arrives in P1). AC-0.4 states step 3 is read that way. |
| M5 | Applied | spec:76, spec:112, spec:195, spec:196 | load is excluded by name from the `## Unattended mode` section requirement (spec:76), from AC-1.1 (which now asserts load has none) and from AC-1.2. The load row says it has no contract and no such section. spec:159 still lists load in P1 for the usage-line fix only. |
| M6 | Applied | spec:200, spec:201 | AC-2.2 limited to the nine P2 commands whose row has a blocked resolution: cli-eval, cli-portify, recommend, review-translation, spec-panel, task, release-split, tdd, troubleshoot (rows spec:104, 105, 115, 117, 120, 121, 89, 90, 91). Narrower than the finding's list: cleanup and improve are moved out of the blocked check because their rows (spec:103, 110) say `--interactive` is "refused" without stating that the refusal writes `status: blocked`, and asserting it would add a rule. New AC-2.2b checks the default of auggie-review, cleanup, improve, research, tasklist and reflect (rows spec:100, 103, 110, 116, 122, 88); auggie-review posting stays with AC-2.4 (spec:202). |

No finding rejected.

## Decisions
- M6: cleanup and improve placed under AC-2.2b rather than the blocked list (decision; options: keep them in AC-2.2 for the refused `--interactive`, or move them; rationale: the rows do not state a blocked status for the refusal, and the brief forbids adding rules).
- M3: chose "read from `worker_done`" over adding flags (rationale: deleting or narrowing is preferred; adding flags would extend P1 scope that no finding asked for).
