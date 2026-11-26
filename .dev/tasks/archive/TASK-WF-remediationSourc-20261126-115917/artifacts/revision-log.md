# Revision 1 log

- old package: TASK-WF-remediationSourc-20261126-041454
- new package: TASK-WF-remediationSourc-20261126-115917
- old plan sha256: 2bfcf8fe5b2c8426334e91a31b5bcf18fe8bfef0c07041fbc4e61f04f5c27f6b
- review report: .dev/reflect/pre-TASK-WF-remediationSourc-20261126-041454-20261126041915/adversarial/merged-reflection.md
- finding_counts: {"blocking": 2, "label_high": 1, "medium": 7, "note": 5}

## Fix map

# Fix map (workflow-reviser, surgical route; B1 and B2 blocking, M-a..M-g and N1..N4 ordered by the story)

All 13 ids reported applied (B1, B2, M-a, M-b, M-c, M-d, M-e, M-f, M-g, N1, N2, N3, N4); N5 needs no plan edit. Reviser notes: it first applied M-a, M-c, N2 and N4 in one Edit call (against the one-finding-per-call rule), reverted that exactly and re-applied one call per finding; wall-clock test lines were corrected to the grepped ones (test_cooldown_expires_and_repeats at 1177; CCSESSION_FIRST_BYTE_TIMEOUT="1" at 1204, 1244, 1554, 1752); byte counts are the reviser's own approximate tallies.
