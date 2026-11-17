# Panel notes (shadow)
- findings_block_compliance_rate 0.6667 (conservative): all 3 blocks are valid after one bounded re-ask; reviewer 2's first reply had a schema-valid block but cited line numbers counted inside its brief (plan 406 / spec 23 offset), out of range in the real files, so it was re-asked once and counted as a first-parse miss. The tool-measured first parse is not available for that reply (saved as artifacts/reviewer-2-card-first-reply.md).
- Valid blocks after re-ask: 3 of 3. calibration_coverage 15/15 (bare indented calibration mapping; ids equal the block ids).
- Reviewer 1 and 3 cards arrived with the entity-escaped angle brackets of the notification text decoded to < and > when saved (display escaping, no claim edited).
