66f369dd3f39c96c30a26fe974e68d3669b2d070
A3 r3-1 F3.1 blocking-accepted CHANGELOG.md:22 ac=T10.AC1 n,y,n,n the hint is cut at the first "; " that has @LIMIT@ after it (the entry said "that last part"). Fixed after review 3 in CHANGELOG, README and D08; NOT re-reviewed (coordinator ruling for task 10).
A3 r3-1 F3.2 blocking-accepted CHANGELOG.md:22 ac=T10.AC1 n,y,n,n a pasted block whose first line is blank is read as an empty answer (exit 0), not as text for Claude (exit 3). Fixed in CHANGELOG, README, the ccsession help text and test_ask_a_blank_line_means_enter; NOT re-reviewed.
A3 r3-1 F3.3 blocking-accepted CHANGELOG.md:13 ac=T10.AC1 n,y,n,n a limit such as 1.5 or 30s waits for ever (only whole numbers are limits). Fixed in CHANGELOG, README and D08; NOT re-reviewed.
A1 note: D08 cites ccsession line numbers that were already off before #315; the header now says to search the quoted text or the function name.
