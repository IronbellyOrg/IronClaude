40950c4008013a396f395a09d8206bc392d6458a 21b2a5a1e64473e5cefee60bcaabd8a355b46c84
F1.1 resolved
F1.3 resolved
F1.4 resolved
F1.5 resolved
F3.1 resolved
F3.2 resolved
F4.1 resolved
T6.AC1 met: T6.AC1@docs/reference/model-aliases.md:5-61, docs/reference/model-aliases.md:26-28, docs/reference/model-aliases.md:33-35, docs/reference/README.md:22
T6.AC2 met: T6.AC2@.dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/artifacts/t6-test.log:18-25 (13 passed; grep exit 1)
F4.2 sev=blocking trigger=B2 ac=T6.AC1 at=docs/reference/model-aliases.md:60 anchor=src/superclaude/cli/roadmap/executor.py:3475-3481 chk=n,y,n,n family=claim-broader-than-evidence fix=add "or, on --resume without --agents, from the agents saved in .roadmap-state.json (executor.py lines 3475-3481)" before "otherwise from the default specs" first=A4 origin=fix-induced: The sentence says the model text comes from --agents when given "and otherwise from the default specs opus and sonnet". On --resume without --agents, execute_roadmap (executor.py:3673-3678) calls _restore_from_state, which replaces the agents with those saved in .roadmap-state.json, so the "otherwise" is not exhaustive. The conclusion still holds because the step-id text is still alias text. Same pattern as F4.1.
F4.3 sev=minor trigger=none ac=T6.AC1 at=docs/reference/model-aliases.md:60 anchor=none chk=n,n,n,n family=implied-not-stated fix=end the bullet with "so the step ids and the best_model values (src/superclaude/cli/recommend/best_model.py lines 77-124, chosen from these lists) stay as they are" first=A4 origin=new: Not blocking. The brief asks the page to say that roadmap step ids and recommend best_model values stay unchanged; the closing "so their names stay as they are" grammatically refers only to the eval model lists, and best_model is never named.
F4.2 resolved
