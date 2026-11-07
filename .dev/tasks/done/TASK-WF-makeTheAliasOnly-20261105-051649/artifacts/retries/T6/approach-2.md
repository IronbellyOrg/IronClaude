40950c4008013a396f395a09d8206bc392d6458a
Implementer claims (not facts):
- Wrote docs/reference/model-aliases.md with the four sections the brief lists and added the README row; verified the Claude Code resolution order against the sub-agents docs and the sprint behaviour against aienv.py.
- Fixed two reported present-tense or universal statements (outside-workspace meaning, the intro "never") in one fix pass and one repair; believed the remaining statements true.
- Each review since found another universal statement ("pick models by the plain aliases", "any --model value is an alias") that live source contradicts at the edges: the retry-ladder slot variables, the sprint slot ids, and the Auggie --model default.
