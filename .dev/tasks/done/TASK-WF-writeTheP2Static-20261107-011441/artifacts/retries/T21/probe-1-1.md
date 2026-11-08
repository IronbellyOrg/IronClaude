f328099e253f3285c5dbd993bf892467c0520883
family: evidence-header
defect form: an evidence file whose first line names a command that is not the command that produced its output.
command: grep -n -m2 -e '^\$ ' -e '^# ' -- ac-c2.txt ac-c6-depth-setting.txt ac-c5.txt mirror-check.txt unmirrored-plugin-copies.txt static-checks-log.txt (in the artifacts folder)
before-output:
ac-c2.txt:1:$ make sync-dev
ac-c2.txt:10:$ make verify-sync
ac-c6-depth-setting.txt:1:$ grep -ho nestedWorkerMaxDepth <profiles>/*/orca-data.json   (AC-C6)
ac-c5.txt:1:# AC-C5 (Check ADDITIVE): added/deleted lines per command file. master = merge base of master and HEAD (the plan's literal command); HEAD = the P2 start.
ac-c5.txt:2:# Local master is behind HEAD, so the master column cannot see edits to lines P1 added; the HEAD column does.
unmirrored-plugin-copies.txt:1:# plugin command copies left unmirrored by this plan: plugin copy compared with its source before this plan (HEAD) and now
unmirrored-plugin-copies.txt:17:# whole-folder comparison of the two pinned mirror folders (a difference here that is not in mirror-check.txt predates this plan)
coupled sites: ac-c5.txt header comment and unmirrored-plugin-copies.txt header comment describe their own commands (checked by hand: they match the script lines); only ac-c6-depth-setting.txt misstates its command.

family: report-wording
defect form: a report sentence that says where a change lives and names a place that does not hold it.
command: grep -n -e 'resume point' -e 'skill.s ' -- p2-static-report.md
before-output:
53:- D-P2-25 (new, awaiting approval): release-split Part 3 can call `/sc:design`, `/sc:workflow` or `/sc:tasklist`, a call site no plan decision or spec row names. Under `--unattended` the section an
69:- cli-portify's `{work_dir}` stays undefined in the skill (as the plan says). The new delivery-gate resume point (`resume_phase: 4`, `resume_substep: "delivery"`) was added to the skill's resume po
after:
ac-c2.txt:1:$ make sync-dev
ac-c2.txt:10:$ make verify-sync
ac-c6-depth-setting.txt:1:$ grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json   (AC-C6, spec section 7.1)
ac-c5.txt:1:# AC-C5 (Check ADDITIVE): added/deleted lines per command file. master = merge base of master and HEAD (the plan's literal command); HEAD = the P2 start.
ac-c5.txt:2:# Local master is behind HEAD, so the master column cannot see edits to lines P1 added; the HEAD column does.
unmirrored-plugin-copies.txt:1:# plugin command copies left unmirrored by this plan: plugin copy compared with its source before this plan (HEAD) and now
unmirrored-plugin-copies.txt:17:# whole-folder comparison of the two pinned mirror folders (a difference here that is not in mirror-check.txt predates this plan)

after (report-wording):
53:- D-P2-25 (new, awaiting approval): release-split Part 3 can call `/sc:design`, `/sc:workflow` or `/sc:tasklist`, a call site no plan decision or spec row names. Under `--unattended` the section and skill make Part 3 write the specs inline (the skill's own 
69:- cli-portify's `{work_dir}` stays undefined in the skill (as the plan says). The new delivery-gate resume point (`resume_phase: 4`, `resume_substep: "delivery"`) was added to the skill's "Resume under `--unattended`" paragraph (`src/superclaude/skills/sc-c
