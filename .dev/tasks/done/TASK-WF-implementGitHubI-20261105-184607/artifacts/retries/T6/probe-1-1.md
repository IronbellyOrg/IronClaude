b5d0068933eded0e9a9ec2821380406c3fe00bb8
family: docs-orca-warning-condition
defect form: delivered text says ccsession-orca prints the "not a valid session name" warning under a bad CCSESSION_PERMISSIONS without the condition that CCSESSION_NAME is set (ccsession-orca:131 guards it).
command: grep -n -F -e "not a valid session name" -e "ignoring it" -- src/superclaude/skills/ccsession-tag/README.md src/superclaude/skills/ccsession-tag/ccsession src/superclaude/skills/ccsession-tag/ccsession.env.example
before:
src/superclaude/skills/ccsession-tag/README.md:517:| `CCSESSION_PERMISSIONS=default` | Start Claude without `--dangerously-skip-permissions`: only `--allowedToo
coupled sites: none other than README.md:517; the --help usage entry in ccsession (lines 99-108) and the plan's changelog bullet (Task 9) do not mention the warning.
after:
src/superclaude/skills/ccsession-tag/README.md:517:| `CCSESSION_PERMISSIONS=default` | Start Claude without `--dangerously-skip-permissions`: only `--allowedToo
