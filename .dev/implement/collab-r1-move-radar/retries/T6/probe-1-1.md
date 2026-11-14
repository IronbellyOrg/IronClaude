b6de60bca78d4bd884af1b3721cebe4d62c50bb9
## family killswitch-empty (from r1-1)
defect form: a launch switch read with the :- default form, so a set-but-empty value is taken as the default instead of being refused
command: grep -n -e 'PANEL_COLLAB' -e 'NOFALLBACK' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh
before:
36:COLLAB=${PANEL_COLLAB:-1}
41:case ${NOFALLBACK:-1} in 1) ;; *) refuse "NOFALLBACK must be unset or 1";; esac
coupled sites: run-reviewer.sh refuses unless NOFALLBACK=1 (${NOFALLBACK:-} = 1, an empty value is already refused there); no other tool reads PANEL_COLLAB; tests/test_launch.py test_preflight_refusals needs empty-value cases
after (killswitch-empty):
36:COLLAB=${PANEL_COLLAB-1}  # unset-only default: a set-but-empty value is refused by the case below
41:case ${NOFALLBACK-1} in 1) ;; *) refuse "NOFALLBACK must be unset or 1";; esac
