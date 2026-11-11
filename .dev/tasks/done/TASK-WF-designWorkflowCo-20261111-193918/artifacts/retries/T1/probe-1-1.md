4656192e2213410d16af9164aeaa61915737960f
family: table-tool-omission
defect form: a tool the task text lists for a step is missing from that step's table row
command: grep -n -F -e codegraph_files -- src/superclaude/skills/sc-workflow-protocol/SKILL.md src/superclaude/commands/workflow.md
before-output:
(no hits)
coupled sites: src/superclaude/skills/sc-workflow-protocol/SKILL.md:36 (Wave 1 table row); the Wave 1 step-0 one-liner; the command file table (Task 2)
after:
src/superclaude/skills/sc-workflow-protocol/SKILL.md:36:| Wave 1 | Resolve the files and symbols the source names; outli
