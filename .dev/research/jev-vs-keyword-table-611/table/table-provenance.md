# Table provenance (a form to fill in)

**This is a form to be completed by the person or session that applied the table. It is not evidence until it is filled in, and it holds no
prompt, label or answer.**

Fill every line. Leave nothing blank; write `none` or `not applicable` where that is the truth.

- Method (one of: a person reading the prose, or executing the skill): `<fill in>`
- Source revision, the commit (`git rev-parse HEAD`): `<fill in>`
- Source revision, the blob of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` at that time (`git hash-object <that file>`): `<fill in>`
- Who applied the table (a name, or a session id): `<fill in>`
- Date applied (UTC): `<fill in>`
- The applier was a different person or session from the labeller (yes or no): `<fill in>`
- The applier received prompts only, with no label and no Jev answer (yes or no): `<fill in>`
- Gate 1 had passed before the table was applied (yes or no, and the time of the `gate1` event): `<fill in>`

## Only when the method was executing the skill

A source-table assertion is not proof of what ran. Record which copy of the skill executed (the lesson in
`docs/memory/reflect/deviation-patterns-issue-610.md`):

- The copy that was loaded (the installed `~/.claude/skills/...` path or the project `.claude/skills/...` path): `<fill in>`
- The SHA-256 of that copy: `<fill in>`
- The actual tool-loading trace or transcript that shows it loaded (a path): `<fill in>`
