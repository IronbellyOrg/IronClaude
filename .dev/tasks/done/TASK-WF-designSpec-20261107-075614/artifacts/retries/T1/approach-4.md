69f360d58d89456f559ad3de21ea75027cd72bb0
Implementer claims (not evidence):
- Kept the accepted base record, gate table, O1, O2 and O4 unchanged; rebuilt O3 in two layers: the unedited scan output (Layer 1) and hand-written rule cards (Layer 2).
- Changed the scan: removed the path filter, made Pass B one line per reader tagged PIN or RULE, added --rule-names, and counted comprehensions as loops (45 RULE readers).
- Wrote 45 rule cards, 9 write-verb key cards and 5 folder-wide cards; the card names equal the scan's RULE names (empty diff).
- Believed the reader list complete; it follows only module-level constants and loop variables, so function-local variables are not followed.
- Wrote in the intro that the file filter uses six tokens; the script filters test files by the substring pr-submit.
