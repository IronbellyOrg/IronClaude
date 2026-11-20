<!-- Stub of the done-check verdict. Copy it to done-verdict.md in the private temporary directory that the evidence step names, then fill it in place. Keep the keys in this order, one line each. Every list line is one line. Replace every angle-bracket placeholder: a placeholder left in is refused. Place kinds for checked: issue_body, issue_comments, target_pr, linked_pr, other_pr, later_stage, remaining_item, timeline. A target_pr or linked_pr line names the number as PR #<n>; an other_pr line says PR #<n> or none found. Every verdict lists at least issue_body, issue_comments, target_pr and other_pr. Sources for criteria: fix_approach, test_plan, acceptance, done_when, other. Delivered words: delivered, partly, not_delivered, unknown. Cite pull requests and files only as the evidence file holds them. unsettled and question are for unclear_escalate only. -->
verdict: <done | not_done | unclear_escalate>
issue: <owner>/<repo>#<N>
pr: <PR>
checked:
- [issue_body] <the number or name read> | <what was found there, one line>
- [issue_comments] <the number or name read> | <what was found there, one line>
- [target_pr] PR #<n> | <what was found there, one line>
- [other_pr] PR #<n> or none found | <what was found there, one line>
criteria:
- [<fix_approach | test_plan | acceptance | done_when | other>] <the issue's own criterion, short> | <delivered | partly | not_delivered | unknown> | <PR #<n>: <file>, <file>; PR #<m>: <file>, or none>
unsettled: <only with unclear_escalate: what could not be settled after the investigation>
question: <only with unclear_escalate: the one question for a person>
reason: <one plain sentence, at most 40 words, that the closing note quotes>
