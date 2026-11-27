a9fc1ce2ec233f8373318a94053ad56959ea7755
# probe-1-1 for the A1 review of T3 (written AFTER the fix edits, not before; disclosed, not hidden)
family=load-check-not-met
defect form: the notes call an AC's load check met or leave its unmet state unsaid
command: grep -n -E -e "NOT met" -e "rc. 0" -- .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-load-notes.md
coupled sites: .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-load-summary.json, .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-wholefile-summary.json (the rc values the notes quote)
before-output: (not captured before the fix; the review quoted notes lines 5 and 11 saying 'Not caused by this change' and 'NOT met' for AC5 only)
after:
after: 6:  T3.AC4 is therefore NOT met: its wording needs "0 failed process-runs of 32" and 3 of 32 failed.
after: 12:- By the plan's rule it is recorded by name, run alone unloaded (passes), counts as a failed run; no run is repeated until it passes. The literal "all 20 res
family=missing-evidence-row
defect form: a claim in the notes has no log row under ./artifacts/
command: grep -n -E -e "alone and unloaded" -e "basetemp" -- .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-load-notes.md
coupled sites: .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-143726/artifacts/t3-orca-isolation.log
before-output: (not captured before the fix; no t3-orca-isolation.log existed)
after: 11:- The one failure in every run is `test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier` (`--model` where `--name` expected). Cause found: the har
