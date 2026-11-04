# Diagnosability tasklist

discriminator-required: no
repro-venue: local same-shell repro (tier1-observation.md); branch ironbelly/issue-330-ponytail-pin
re-run permitted: yes (local read-only repro already run this session)

## Emitter search

emitters-found: 1 (install_user_setup.py:186 "Settings defaults: added" message)
already-read-files: 2 (install_user_setup.py, main.py)
usable-capture-routes: 1 (same-shell repro writes settings.json in a throwaway HOME; observed)

## Discriminator rows

None: one surviving producer (producers.md P1), datum observed.

## Pending rows

None. Informational only: the defaults message could name a carried-over opt-out once fixed (part of the fix, not instrumentation).
