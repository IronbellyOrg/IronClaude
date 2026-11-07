3bdba3a8d32771fe9567b7e8c94c5e410584c782
family: gate-sentence-pins
defect form: a command's UNATTENDED_EXPECT entry does not list the plan's gate sentences (Constraints, "Gate sentences") in its phrases.
command: grep -n -F -e 'is refused' -e 'listed as not applied' -- tests/skills/test_worker_contract.py src/superclaude/commands/improve.md
before-output:
tests/skills/test_worker_contract.py:50:        ["Passing neither, or both, is refused before any work"],
src/superclaude/commands/improve.md:102:- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
src/superclaude/commands/improve.md:104:- **Person-mode flags.** `--interactive` is refused before any work (contract `worker_status: failed`, the flag in `reason`). `--force` is refused too, because it widens what is applied without confirmation.
src/superclaude/commands/improve.md:105:- **Gates.** Under `--unattended` only the items outside the "Approval Required" list and outside the "Explicitly Will NOT (without `--force` flag)" list are applied: every item under "Approval Required" is listed as not applied, and so is every item of the second list. `--force` is refused, so that second list is never lifted. There is no other gate.
coupled sites: tests/skills/test_worker_contract.py cleanup entry (Task 2, complete): same omission; outside this task's touched files, listed here, not edited (Task 20 builds P2_GATES from the same sentences and the cleanup entry is completed there).
after:
tests/skills/test_worker_contract.py:50:        ["Passing neither, or both, is refused before any work"],
tests/skills/test_worker_contract.py:414:            'every item under "Approval Required" is listed as not applied',
tests/skills/test_worker_contract.py:415:            "`--force` is refused",
src/superclaude/commands/improve.md:102:- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
src/superclaude/commands/improve.md:104:- **Person-mode flags.** `--interactive` is refused before any work (contract `worker_status: failed`, the flag in `reason`). `--force` is refused too, because it widens what is applied without confirmation.
src/superclaude/commands/improve.md:105:- **Gates.** Under `--unattended` only the items outside the "Approval Required" list and outside the "Explicitly Will NOT (without `--force` flag)" list are applied: every item under "Approval Required" is listed as not applied, and so is every item of the second list. `--force` is refused, so that second list is never lifted. There is no other gate.
