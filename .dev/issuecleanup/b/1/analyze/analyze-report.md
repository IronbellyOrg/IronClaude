# Analyze report: src/superclaude/skills/sc-closeout-protocol (architecture, quick)

Master f2894fc44, 2026-11-24. Read-only run for issues 782, 783, 784 (round 2).
Codegraph: index_state=fresh, checked_at=2026-11-24T22:13:31Z; degraded: none (used for readiness only; findings from Grep/Read/ls).

## Layout of the pattern skill (what C1 to C3 copy)

- `SKILL.md` (124 lines): `## Files of this skill` table (line 28), `## Waves` (57), `## Return contract` (69), `## Error handling` table (73-95), Will Do / Will Not Do.
- `refs/` settle.md, done-check.md, result.md; `templates/` four files; `scripts/` three files. Stub-first via templates.
- Activation section is in the command file `src/superclaude/commands/closeout.md:85`, not in SKILL.md; STOP rules at `closeout.md:40`.
- Tests: `tests/skills/test_closeout_protocol.py:3213` (stop codes two-way), `:3301` (result template parses).

## Findings

| # | Severity | Finding |
|---|---|---|
| 1 | Medium | No `sc-coordinator-protocol`, no `commands/coordinator.md`, no `tests/coordinator/` on master (ls: no such file). C1 to C3 are all unbuilt. |
| 2 | Medium | Activation lives in the command file; C1's "test reads SKILL.md for an Activation section" has no model on master. |
| 3 | Low | Error-handling table has two columns (scenario, behavior); C2's three columns (code, when, what next) are a small extension. |
| 4 | Low | Return contract is a YAML block printed last with `status` words; C3 can copy `templates/result.md`. |
| 5 | Low | `E-NO-GRANT` has no hit in `src/` or `tests/`. |

## Recommendations

Copy the pattern; put Activation and its test in a command file; scope the stop-code test to the skill's files.
