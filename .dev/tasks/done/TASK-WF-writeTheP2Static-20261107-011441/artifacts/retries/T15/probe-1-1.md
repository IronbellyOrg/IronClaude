ea47de70c2734af993ca9288b2cf2c255abcb5fa
family: nested-call-site-coverage
defect form: a call site of the nested workflow command in the reflect skill or its ref that does not carry the --unattended arguments.
command: grep -n -F -e 'sc:workflow-protocol' -e 'nested/workflow-' -- src/superclaude/skills/sc-reflect-protocol/SKILL.md src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md
before-output:
src/superclaude/skills/sc-reflect-protocol/SKILL.md:322:- `--remediate` (depth `standard` default, or `quick`)
src/superclaude/skills/sc-reflect-protocol/SKILL.md:339:- **Phase A — Build the plan:** write `remediation-s
src/superclaude/skills/sc-reflect-protocol/SKILL.md:586:| `sc:workflow-protocol` (skill, not agent) | 6 | UC-2
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:14:| `--remediate` (depth `standard`, t
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:16:| headless `claude --print` + `--rem
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:74:3. Invoke `Skill sc:workflow-protoco
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:75:   Under `--unattended` (shared rule
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:301:| `sc:workflow-protocol` returns no
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:302:| `sc:workflow-protocol` unavailabl
coupled sites: the ref step 3 (carries the arguments after Task 15), SKILL.md Phase A bullet, the SKILL.md agent-map row and the Failure modes row (describe the call, not instruct it).
after:
src/superclaude/skills/sc-reflect-protocol/SKILL.md:322:- `--remediate` (depth `standard` default, or `quick`)
src/superclaude/skills/sc-reflect-protocol/SKILL.md:339:- **Phase A — Build the plan:** write `remediation-s
src/superclaude/skills/sc-reflect-protocol/SKILL.md:340:  Under `--unattended` (shared rules: `~/.claude/WORKE
src/superclaude/skills/sc-reflect-protocol/SKILL.md:587:| `sc:workflow-protocol` (skill, not agent) | 6 | UC-2
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:14:| `--remediate` (depth `standard`, t
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:16:| headless `claude --print` + `--rem
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:74:3. Invoke `Skill sc:workflow-protoco
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:75:   Under `--unattended` (shared rule
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:301:| `sc:workflow-protocol` returns no
src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:302:| `sc:workflow-protocol` unavailabl
