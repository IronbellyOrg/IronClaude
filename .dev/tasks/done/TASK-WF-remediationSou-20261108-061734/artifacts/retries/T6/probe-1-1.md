442543b745467e98bd00c2fca0d4c2b8ee157e0c

## family=stale-1s-wording (from review r6-1)

Defect form: a stale "1 s (asserted)" wording survives at a named update site, contradicting the new 3.5 s assert.

Search command (read-only): grep -n -e "under 1 s" -e "1 s (asserted)" tests/hooks/test_launch_level_guard.py

before-output (touched files + AC-named files):
- tests/hooks/test_launch_level_guard.py:1276:     # T-SPD-5: governed full-submit session, each run under 1 s (asserted).

Coupled sites: none (the only remaining "under 1 s" hit in the file; header and _spd_markdown already reworded).

after:
- grep -n "under 1 s" tests/hooks/test_launch_level_guard.py -> no matches. The comment at :1276-1277 now reads "each run under LARGE_LIMIT_S (3.5 s, asserted; 1 s design target reported)."
