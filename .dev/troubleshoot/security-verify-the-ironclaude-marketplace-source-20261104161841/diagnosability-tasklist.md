# Diagnosability tasklist

discriminator-required: no
repro-venue: local same-shell repro (tier1-observation.md); branch ironbelly/issue-330-ponytail-pin
re-run permitted: yes

## Emitter search

emitters-found: 1 (install_user_setup.py:376/:380 plugin-step message)
already-read-files: 2 (install_user_setup.py, main.py)
usable-capture-routes: 1 (same-shell repro with a fake claude CLI records every command)

## Discriminator rows

None: P1 and P2 are two independent defects, each observed directly (case 1, case 2), not competing explanations of one value.

## Pending rows

None.
