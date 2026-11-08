b9af89d68d7c18af63eeb5b0e513b9a01a44cc38
family g3-wrapper-basename
defect form: a wrapper, shell or git word in command position that is compared by its raw text where the design compares by basename
command: grep -nE 'case \$w in|case \$LL_B in' src/superclaude/hooks/scripts/launch-level-guard.sh
before-output:
436:                            case $w in
(the wrapper and shell arms matched the raw word)
coupled sites: probed /usr/bin/git ci, /usr/bin/git push origin f, /usr/bin/env /usr/bin/git ci, nice -n 5 /usr/bin/git ci, /usr/bin/nohup /bin/sh -c "git ci", A=/usr/bin/env git ci: all exit 2; only the wrapper arm was affected
after:
303:    case $w in
436:                            case $w in -*) continue ;; esac
438:                            case $LL_B in
