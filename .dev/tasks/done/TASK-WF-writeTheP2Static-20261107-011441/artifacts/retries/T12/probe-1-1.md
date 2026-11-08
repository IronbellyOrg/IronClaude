60262eab54a984b8c7d8afcfcf04e985a43233f7
family: section-skeleton
defect form: a Contract bullet that does not say "written on every outcome".
command: grep -n -F -e 'written on every' -- src/superclaude/commands/task.md
before-output:
171:- **Contract.** `<report-dir>/return-contract.yaml` is written on every tier, not only on TFEP. `report_path` is `<r
coupled sites: none (one Contract bullet in task.md; the skill sentences name the contract only in passing).
after:
171:- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, and on every tier, not only on TFEP
