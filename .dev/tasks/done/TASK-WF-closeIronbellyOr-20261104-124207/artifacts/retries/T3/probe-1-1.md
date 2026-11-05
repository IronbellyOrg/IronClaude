235bb29732e5681bbc6e23842700f369c166175e
family=ledger-off-wording
form: required wording from the Task 3 instruction/AC missing or paraphrased
command: grep -n -F -e ledger -- docs/getting-started/installation.md
before:
  393:and after every turn writes a ledger row to
  396:ledger stays local unless you set Ponytail's webhook option. `/ponytail band off`
  397:hides the band; the `git grep`, the Edit/Write watch and the ledger keep
  398:running. The ledger is on by default: set Ponytail's `ledger` option to off in
coupled: CHANGELOG.md [Unreleased] (Task 4) repeats the same sentence
family=optout-incomplete
form: required wording from the Task 3 instruction/AC missing or paraphrased
command: grep -n -F -e uninstall -e settings.local.json -e 'wins over' -- docs/getting-started/installation.md
before:
  168:- Clean uninstall
  495:pipx uninstall superclaude
  498:pip uninstall superclaude
  507:There is no `superclaude uninstall` command. Uninstalling the package removes only the Python package and the `superclaude` command. Everything `superclaude install` copied into your home folder stays where it is:
  516:Remove those by hand if you want them gone. Run `superclaude install --list` before uninstalling to see which core files, commands, agents, skills and templates are installed, and which codegraph paths are owned. To remove codegraph, run:
coupled: CHANGELOG.md [Unreleased] (Task 4) repeats the same sentence
family=statusline-note-incomplete
form: required wording from the Task 3 instruction/AC missing or paraphrased
command: grep -n -F -e 'changes no settings' -e 'mention the offer' -- docs/getting-started/installation.md
before:
  387:sees the note in its context and may mention the offer in its reply. The
coupled: CHANGELOG.md [Unreleased] (Task 4) repeats the same sentence
after (family=ledger-off-wording):
  393:and after every turn writes a ledger row to
  396:ledger stays local unless you set Ponytail's webhook option. `/ponytail band off`
  397:hides the band; the `git grep`, the Edit/Write watch and the ledger keep
  398:running. The ledger is on by default: set Ponytail's `ledger` option to `false`
after (family=optout-incomplete):
  168:- Clean uninstall
  416:as `true`. Do not only run `claude plugin uninstall` either: the next
  418:`false` for it. A project `.claude/settings.json` that enables it wins over your
  420:that project's `.claude/settings.local.json`.
  500:pipx uninstall superclaude
  503:pip uninstall superclaude
  512:There is no `superclaude uninstall` command. Uninstalling the package removes only the Python package and the `superclaude` command. Everything `superclaude install` copied into your home folder stays where it is:
  521:Remove those by hand if you want them gone. Run `superclaude install --list` before uninstalling to see which core files, commands, agents, skills and templates are installed, and which codegraph paths are owned. To remove codegraph, run:
after (family=statusline-note-incomplete):
  387:sees the note in its context and may mention the offer in its reply; the note
  388:itself changes no settings. The installer never sets `statusLine`; to skip the note, set your own `statusLine`
