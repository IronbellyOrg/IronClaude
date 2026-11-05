40950c4008013a396f395a09d8206bc392d6458a
family=claim-broader-than-evidence
defect form: a sentence states how a value is produced ("built from", "passes", "are", "stay") in terms narrower than the code paths that produce it
command: grep -n -E "built from|passes|are built|use the alias|stay" docs/reference/model-aliases.md
before:
60:- **Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line 114) are built from the model text the user passes (`src/superclaude/cli/
coupled sites: the Roadmap names bullet (line 60); the other Known consequences bullets are not edited
after:
60:- **Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md
