3939477e29cadc940a1cd304bdf78131bfa8653b
## family codex-wait-completion-wording
defect form: a Codex wait-outcome condition phrased as "no completion" where the code tests the gate state (polling), which also covers a completed marker whose promised findings are not yet visible
command: grep -rn -i "no completion" src/superclaude/skills/sc-pr-submit-protocol/ src/superclaude/commands/pr-submit.md
before:
refs/detection-contract.md:100 (gate-state rule "no completion or an invalid selection -> polling": accurate, not the defect form)
refs/augment-poll.md:84 (pending row, Codex column)
refs/augment-poll.md:87 (incomplete row, Codex column)
coupled sites: design section 6 table rows (specification, not edited)
after:
src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:100:`codex_priority` and the mapped `severity_hint`. Gate state: no completion or an invalid selection →
