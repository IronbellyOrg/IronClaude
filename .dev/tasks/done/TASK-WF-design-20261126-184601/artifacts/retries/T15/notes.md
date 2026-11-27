38e580ab0116ad929f13070c37b4cc2cec1b104f
A1 r1-1 F1.1 minor src/superclaude/skills/sc-git-protocol/scripts/vcs_plan.py:1980 ac=T15.AC1 n,n,n,n when HEAD is still the parent every exit from 2 to 128 maps to commit-error while the AC names exit 128 only; no test covers exit codes 2 to 127 (fix: narrow commit-error to 128 and send other statuses to uncertain, or document the wider mapping).
A1 r1-1 F1.2 minor src/superclaude/skills/sc-git-protocol/scripts/vcs.py:71 ac=T15.AC1 n,n,n,n the verify docstring omits two refusal reasons the code can return: sidecar-mismatch and not-a-repo.
