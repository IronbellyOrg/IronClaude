RUBRIC v1 (frozen; a change is a new version and starts a new loop)
BLOCKING needs B1, B2 and B3.
B1 Quote: the finding quotes the offending text verbatim (a substring of the spec under review) and marks the defective words (span).
   For an omission, quote the requirement or guard whose promised behavior is incomplete.
B2 Outcome: it states a concrete wrong outcome: a named reader, implementer or test that follows the quoted text exactly and produces a
   specific wrong result; or two quoted texts that cannot both hold; or a check that cannot pass or always passes, with the input that shows it.
B3 Kind, one of: (a) contradiction between two quoted texts; (b) a claim about a source that the source's quoted text contradicts; (c) an
   acceptance check that cannot pass or passes vacuously; (d) one text with two readings that lead to different observable results, both named;
   (e) a step that loses data or takes an unsafe action.
CRITICAL is BLOCKING under (e) or in a requirement the spec calls core; the verdict does not tell them apart.
MINOR is everything else: wording, missing example, moved line number or citation drift, style, a gap whose intended behaviour is inferable
   from nearby text, a suggestion to add a rule, mechanism or section.
Never a reason to be blocking: experts agree; experts disagree; the section is important; the finding was found late; a Boundary Table row says
   GAP or blank (such a row is a candidate and must meet B1-B3).
Q2 (re-reviews, recorded as data, never demotes): given the baseline text shown, could a reader of the baseline already produce the same wrong outcome? same | different | na.
