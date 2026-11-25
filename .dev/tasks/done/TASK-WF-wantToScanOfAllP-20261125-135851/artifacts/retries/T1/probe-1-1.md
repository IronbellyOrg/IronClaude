263bc652fd715afe06e128bc71ab65a7d1ba3fb0
family goal-wording-incomplete: GOAL shorter than the corrected wording of the Constraints
command: grep -n -E -e 'owner goal|decisions are made|demands to the coordinator' -- .dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/tools/plan_common.py
before:
29:    "owner goal: the dashboard replaces talking to the coordinator sessions directly; it is the one place "
coupled sites: none other in plan_common.py (L726 states a different rule); render.py line 137 repeats the wording and is Task 2
after:
29:    "owner goal: the dashboard replaces talking to the coordinator sessions directly; it is the one place "
31:    "and answers start going through the dashboard to the coordinator); decisions are made there, with as "
33:    "fails, demands to the coordinator for more context, a better explanation, a debate of several "
