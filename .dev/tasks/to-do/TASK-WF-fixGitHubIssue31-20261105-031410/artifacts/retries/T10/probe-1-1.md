66f369dd3f39c96c30a26fe974e68d3669b2d070
family changelog-claim-vs-source
defect form: a changelog or guide sentence states a behaviour or a place (a file, a caller, an old default) that the live source or git show HEAD contradicts at an edge
search: grep -n -i -E 'every|never|only|all |still|used to|no longer|default|included|both' CHANGELOG.md | sed -n 1,40p
before-output: lines 11-27 of the new entry (every caller gets it; Coder New Terminal hook included; still start untagged; README and D08 describe)
coupled sites: the sentence naming the Coder New Terminal hook (cannot be checked from this repo: removed, replaced by a statement about any caller that relied on the old default); the CCSESSION_NAME exception (CHANGELOG changed bullet, added bullet and D08 Step 11); the limit-shown claim (CHANGELOG, D08 Step 8); the line-number note (D08 header)
after: each of those sites was re-read against ccsession, ccsession-orca and git show HEAD before the edit
second pass (review r2-1): three more edge claims (the @LIMIT@ rule, "still start untagged", header line-number history). Search: grep -n -E 'LIMIT|shows the limit|show the limit|still start|still starts' CHANGELOG.md docs/testing/v5.0.0/user/D08-ccsession.md
after: CHANGELOG lines 13, 22 and 26 and D08 lines 5 and 266 now state the exact rule; the same search finds no other site.
third pass (review r3-1, executor, no fourth review run): the exact first-"; " cut, the blank-first-line paste and the whole-number rule were fixed in CHANGELOG lines 13 and 22, D08 line 266, README (four sites) and the ccsession help text; test_ask_a_blank_line_means_enter now also covers a paste starting with a blank line.
