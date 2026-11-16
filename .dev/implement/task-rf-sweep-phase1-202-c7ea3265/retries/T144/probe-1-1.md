d173296087168f5733efe0d51866ce41427d4f9f
family=extra-command
defect form: an Orca call recorded in the probe file whose arguments are outside the uses the item allows (the item permits a fake Run id for template 2 only).
command: grep -n -E '^Command' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md | grep -n 'orca-ide'
before-output (state reviewed in review 1):
Orca commands recorded: 8 templates with the real Run or Dispatch ids; plus line 942: task-list --run run_000000000000 --json (fake Run id on template 5).
coupled sites: the header paragraph ("wrote nothing outside this task package", "none of the forbidden commands"), the line-942 command label, the compliance record line ("the eight templates only, plus the extra read named in section 8"), and the final summary disclosure.
after:
(the call cannot be undone; the fix records it as Deviation D1 in a last section, labels line 942 as D1, rewrites the compliance record line, and the header names D1 and the /tmp scratch location)
