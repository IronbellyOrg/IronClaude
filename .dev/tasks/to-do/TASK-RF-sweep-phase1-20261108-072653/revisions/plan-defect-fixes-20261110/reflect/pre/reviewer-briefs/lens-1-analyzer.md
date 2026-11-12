# Lens 1 (persona: analyzer): authority, ordering and resume safety in Phase 7

Read first: the common brief (same folder, common.md). Your slice: items 7.10 to 7.37 and Phase 7 preamble (TL:1139-1145 region), plus every item they consume or produce.

Focus on the F-03, F-04, F-05, F-09 fixes and everything that depends on them:
1. Item 7.10 (TL:1208-1213): trace the full lifecycle: first run with authorization, first run without, a run that fails a bounded check after the style edit, a resumed run, and the Branch 1/Branch 2 meaning now that this item replaces the Phase 7 preamble branches. Can the executor follow it literally? Does the result file section `## Execution authorization (verbatim)` get written before the style edit, can it be duplicated or overwritten on resume, does 7.20 check it with a command that can pass and fail correctly?
2. The embedded addendum clauses in the 7.10 Action: compare each with ADD:13-21 sentence by sentence; flag any change of meaning, omission that 11.4 pins, or text that would make the style rule broader or narrower than the addendum.
3. Item 7.20 and 7.30/7.34: the new F-08 count (STYLE qualifier lines), the F-04 check, the F-07 sha256 guard (order of the pre-spawn record and post-return re-run, where the sums are written, can the fix agent overwrite them?). Can a correct run fail any of them?
4. The retry-restore hazard for the design append (ADD:45; TL:1210 stop sentence): does any new text route to a retry of ticked 7.10?
5. Does any new text create a dependency cycle, an item that needs an output of a later item, or a check that runs before its input exists?
