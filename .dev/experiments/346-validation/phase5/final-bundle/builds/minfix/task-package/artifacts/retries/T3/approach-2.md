Implementer claims (not verified by review):
- Built check --enforce as one in-memory revert pass: failing findings (OVER, MINOR-EDIT), depends closure, unattributed hunks, cycle-cap order, moved-unit partner closure, then one atomic write and a re-check.
- Text is rebuilt from units plus the separators between them; a reverted part emits baseline units, a kept part revised units.
- A2 changed the separator rule (borrow the break before a dropped run when the unit continued a line), added the baseline tail, a depends closure over entries whose hunks are unattributed (claimant set, entry unset), and a gap rule (an unowned deleted unit makes its gap unattributed).
- A whole-baseline restore remains as a labelled safety net (reason=raw-size by design, reason=recheck otherwise); the property test asserts reason=recheck never occurs; 10,000 extra fuzz cases on PROP_BASE showed none.
- Believed T3.AC1-AC4 met; the reviewer found the separator rule still wrong next to tables and the depends closure blind to entries whose quote is not in the baseline.
