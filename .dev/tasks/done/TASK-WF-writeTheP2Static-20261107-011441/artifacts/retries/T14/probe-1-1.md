0403d1f44280976c2cede916e71d0c23a4d6ab3e
family: builder-unattended-handoff
defect form: text says the builder is told the caller is unattended, with no step that tells it.
command: grep -n -F -e 'told the caller' -e 'BUILD_REQUEST as the prompt' -e 'caller runs under' -- src/superclaude/commands/tdd.md src/superclaude/skills/tdd/SKILL.md src/superclaude/skills/task-builder/SKILL.md
before-output:
src/superclaude/commands/tdd.md:168:- **Gates.** Under `--unattended` a bare topic resolves as blocked (a topi
src/superclaude/skills/tdd/SKILL.md:389:Use the Agent tool with `subagent_type: "rf-task-builder"` and `mode: 
src/superclaude/skills/task-builder/SKILL.md:410:Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRAC
coupled sites: tdd.md Gates bullet; task-builder/SKILL.md paragraph; no other builder spawn in the tdd skill.
after:
src/superclaude/commands/tdd.md:168:- **Gates.** Under `--unattended` a bare topic resolves as blocked (a topi
src/superclaude/skills/tdd/SKILL.md:389:Use the Agent tool with `subagent_type: "rf-task-builder"` and `mode: 
src/superclaude/skills/tdd/SKILL.md:391:Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) ad
src/superclaude/skills/task-builder/SKILL.md:410:Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRAC
