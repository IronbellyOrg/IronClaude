7987ab62e0024258b9bd4ad4197ddcc89dbbee48
## family doc-claim-vs-code (F4.1)
defect form: the note says what the sc-fix-audit skill covers more broadly than SKILL.md does
command: grep -n -F -e 'SKILL.md' -e 'on success' -e 'on failure' -- docs/designs/spec-panel-ponytail.md
before:
32:What each step prints, on success and on failure, is listed in the `sc-fix-audit` skill (`~/.claude/skills/sc-fix-audit/SKILL.md`); this note does not repeat it.
62:| `src/superclaude/skills/sc-fix-audit/SKILL.md` | New: carrier skill with the four steps |
coupled sites: none in the note (the pointer sentence is the only claim about SKILL.md content); src/superclaude/skills/sc-fix-audit/SKILL.md:37 (out of T9 scope, not edited)
after (doc-claim-vs-code F4.1):
after: 60:| `src/superclaude/skills/sc-fix-audit/SKILL.md` | New: carrier skill with the four steps |
