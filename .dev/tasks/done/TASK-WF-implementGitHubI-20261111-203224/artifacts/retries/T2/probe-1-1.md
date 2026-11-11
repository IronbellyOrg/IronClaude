036104cb53a1f9f190105bbdb612c01d8875e262
family ac2-phrase-outside-subsection
defect form: a required phrase sits outside the subsection that must contain it
search: grep -n -F -e 're-invocation keeps every token' -- src/superclaude/core/WORKER-CONTRACT.md
before:
22:  A command invoked by another command, through the Skill
216:Whether a `Command:` line carries `--unattended` is deci
coupled sites: line 216 pointer sentence; line 22 brief guard sentence (unchanged, keeps its own copy of the phrase)
after:
22:  A command invoked by another command, through the Skill
228:A WC-3 re-invocation keeps every token of the `Command:`
