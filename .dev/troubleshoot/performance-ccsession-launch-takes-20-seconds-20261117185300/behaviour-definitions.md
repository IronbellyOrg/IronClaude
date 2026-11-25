# Behaviour definitions

All three behaviours were observed directly in this run (same shell, bash 5.2.37, GNU coreutils), so no external fetch was needed; the observation, not a recalled definition, is the defining artifact. Source of each observation: tier1-observation.md.

| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | bash `local VAR=value` for a variable that is not already exported | the value is not passed to child processes | parent probe, 2026-11-17T19:03:28Z: `bash -c 'f() { local x LC_ALL=C; env \| grep -c "^LC_ALL="; }; f'` printed 0, LC_ALL unset in the shell (tier1-observation.md "Locale finding") | none (observed) | observed in this run |
| 2 | GNU `date -r <operand>` | `-r` takes a FILE operand, so an epoch number fails with "No such file or directory", exit 1 | parent run, 2026-11-17T19:00:52Z: `date -r 1794941650 '+%Y-%m-%d %H:%M'` exit 1; `date -d @1794941650 ...` exit 0 (tier1-observation.md "Primitive behaviour observed in this run") | none (observed) | observed in this run |
| 3 | `grep -oE` with a bracket-alternation regex over about 1.25 MB per file in a UTF-8 locale vs the C locale | UTF-8 locale roughly doubles the regex time | parent probe Arms 2 and 3, 2026-11-17T19:02:52Z: 6.460 s (LC_ALL=C on grep) vs 13.227 s (LANG=C.UTF-8) over 439 files; end-to-end alternation `ccsession --here` plain vs `LC_ALL=C`, 2026-11-17T19:07:38Z onward, plain 22.5-24.7 s vs 16.2-16.7 s (locale-probe.txt) | none (observed) | observed in this run |
