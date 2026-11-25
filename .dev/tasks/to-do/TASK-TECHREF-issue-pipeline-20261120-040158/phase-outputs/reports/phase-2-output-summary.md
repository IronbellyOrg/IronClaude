# Phase 2 output summary

**Total:** 6 research files found (expected 6), 3,021 lines total, none MISSING. All Status: Complete. Snapshot fingerprint after Phase 2: sha256 f20de643086d06b8c8cffb981676a619719094036d6fa386953b4bc777d49b74 (identical to before).

| File | Lines | Status | CODE-VERIFIED count | CODE-CONTRADICTED count | UNVERIFIED count | Has test-pin table | Has Defect Candidates section |
|---|---|---|---|---|---|---|---|
| 01-watcher-decision-engine.md | 656 | Complete | 23 | 15 | 10 | yes (section 11) | yes |
| 02-watcher-io-github-launch-record.md | 473 | Complete | 5 | 3 | 14 | yes | yes |
| 03-watcher-operator-surface-and-setup.md | 497 | Complete | 114 | 18 | 30 | yes | yes |
| 04-claim-flow-and-orca-worktree.md | 497 | Complete | 8 | 14 | 15 | yes | yes |
| 05-guard-stack-and-ccsession.md | 500 | Complete | 2 | 2 | 3 | yes (section 11 "Test pins") | yes |
| 06-coordinator-text-and-removed-code.md | 398 | Complete | 3 | 6 | 14 | yes | yes |

Counts are literal-string counts (grep -o) of `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, and `[UNVERIFIED` (prefix) per file. Files may use other verification wording (for example OBSERVED-BY-GREP, READ-ONLY-READING) alongside the three tags, so low CODE-VERIFIED counts in files 02, 04, 05, 06 do not mean low verification.

Extra artefact: research/05-guard-run-sandbox/ (guard observation run, 44 payloads; HOME set inside the task folder; scripts run-guard-observation.sh, run-guard-extra.sh, observation-output.txt).
