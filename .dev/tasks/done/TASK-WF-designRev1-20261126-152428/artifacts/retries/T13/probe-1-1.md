256f8cf05c9304e648363a0a43b19b5cca8fda4d
## Family r1-workflow-claim (review r1-1, finding F1.1)
defect form: a claim about push-triggered workflows that the audit record contradicts
command: grep -n -F -e 'push trigger' -e 'on: push' -e 'throwaway branch' -- .dev/issues/837/apply-runbook.md
before:
  124:R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of the target repositor
  211:R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of the target repositor
  369:| Scratch ruleset or throwaway branch survives | R1 | List `zz-selftest-*` rulesets and branches; delete; the real create wa
coupled sites: the R1 paragraph of each of the three repos

## Family variables-not-filled (review r1-1, finding F1.2)
defect form: a placeholder where the task asks for the filled value
command: grep -n -E -e '^FILE=' -e '^PARENT_OWNER=' -e '^BRANCH=' -- .dev/issues/837/apply-runbook.md
before:
  106:PARENT_OWNER=seakee
  107:BRANCH=main
  108:FILE=<protect-main-mirror.json when ahead_by is 0 and Clay's acceptance is quoted, otherwise protect-main.json>
  193:PARENT_OWNER=stablyai
  194:BRANCH=main
  195:FILE=<protect-main-mirror.json when ahead_by is 0 and Clay's acceptance is quoted, otherwise protect-main.json>
  280:BRANCH=main
  281:FILE=<protect-main.json>
coupled sites: the variable block of each repo, the part two intro paragraph that names the ledger-decided file, R3 and R6 which read FILE
after:
 family r1-workflow-claim:
  124:R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of 
  211:R1. Scratch self-test for each role the ledger says `APPLY`, before the snapshot, in a scratch clone of 
  369:| Scratch ruleset or throwaway branch survives | R1 | List `zz-selftest-*` rulesets and branches; delete
 family variables-not-filled:
  106:PARENT_OWNER=seakee
  107:BRANCH=main
  108:FILE=protect-main-mirror.json   # the ledger candidate while ahead_by is 0 and Clay's written acceptance
  193:PARENT_OWNER=stablyai
  194:BRANCH=main
  195:FILE=protect-main-mirror.json   # the ledger candidate while ahead_by is 0 and Clay's written acceptance
  280:BRANCH=main
  281:FILE=protect-main.json
