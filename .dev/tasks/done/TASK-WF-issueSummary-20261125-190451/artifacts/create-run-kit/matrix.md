# Controlled create-run matrix (issue 834): 10 scenarios x 3 depths = 30 rows

Status: prepared, not filled. Every row below starts with the Result marker that says an owner run is required. A row is filled only by a person who ran it as README-run.md says, from the row's own `rows/<row id>/gh-calls.log` and the session transcript.

Scenarios:

- S01 empty notes (both lists hold only `- None`): 0 questions.
- S02 additions only, including an `Assumption:` line: 0 questions.
- S03 reversed choice: 1 question.
- S04 dropped requirement: 1 question.
- S05 changed flag: 1 question.
- S06 user-stated fact contradicted by verified code: 1 question.
- S07 two contradictions at once: 1 question naming both.
- S08 additions plus one contradiction: 1 question, and the additions stay in the body.
- S09 a worker disagrees with a user-supplied flag and the issue is filed with the user's flag: 0 questions; the pushback comment is posted at standard and deep depth only.
- S10 an addition that is the only evidence of a contradiction: 1 question; the answer "keep my wording" removes only that content, every other addition stays.

Row pass rule (README-run.md, section "Reading a row"): zero REFUSED lines in the row's log, exactly one CREATE line, exactly one FIELD-POST line, the number of COMMENT lines in "Calls expected", the observed question count equal to the expected one, every addition present in the posted body, and no offer to approve the full body.

| Row | Scenario | Depth | Drafting worker | Expected questions | Observed questions | Answer given | Calls expected | Calls observed (from the log) | Additions kept in the posted body | Pushback comment (expected / observed) | Fake issue number | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01-quick | empty notes | quick | issue-worker-t3 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900001 | not run: owner run required |
| S01-standard | empty notes | standard | issue-worker-t2 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900002 | not run: owner run required |
| S01-deep | empty notes | deep | issue-worker-t1 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900003 | not run: owner run required |
| S02-quick | additions only | quick | issue-worker-t3 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900004 | not run: owner run required |
| S02-standard | additions only | standard | issue-worker-t2 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900005 | not run: owner run required |
| S02-deep | additions only | deep | issue-worker-t1 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900006 | not run: owner run required |
| S03-quick | reversed choice | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900007 | not run: owner run required |
| S03-standard | reversed choice | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900008 | not run: owner run required |
| S03-deep | reversed choice | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900009 | not run: owner run required |
| S04-quick | dropped requirement | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900010 | not run: owner run required |
| S04-standard | dropped requirement | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900011 | not run: owner run required |
| S04-deep | dropped requirement | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900012 | not run: owner run required |
| S05-quick | changed flag | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900013 | not run: owner run required |
| S05-standard | changed flag | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900014 | not run: owner run required |
| S05-deep | changed flag | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900015 | not run: owner run required |
| S06-quick | user-stated fact contradicted by verified code | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900016 | not run: owner run required |
| S06-standard | user-stated fact contradicted by verified code | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900017 | not run: owner run required |
| S06-deep | user-stated fact contradicted by verified code | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900018 | not run: owner run required |
| S07-quick | two contradictions at once | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900019 | not run: owner run required |
| S07-standard | two contradictions at once | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900020 | not run: owner run required |
| S07-deep | two contradictions at once | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900021 | not run: owner run required |
| S08-quick | additions plus one contradiction | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900022 | not run: owner run required |
| S08-standard | additions plus one contradiction | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900023 | not run: owner run required |
| S08-deep | additions plus one contradiction | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900024 | not run: owner run required |
| S09-quick | worker disagrees with a user-supplied flag | quick | issue-worker-t3 | 0 | to fill | n/a | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900025 | not run: owner run required |
| S09-standard | worker disagrees with a user-supplied flag | standard | issue-worker-t2 | 0 | to fill | n/a | 1 create, 1 field POST, 1 comment | to fill | to fill | yes / to fill | 900026 | not run: owner run required |
| S09-deep | worker disagrees with a user-supplied flag | deep | issue-worker-t1 | 0 | to fill | n/a | 1 create, 1 field POST, 1 comment | to fill | to fill | yes / to fill | 900027 | not run: owner run required |
| S10-quick | addition that is the only evidence of a contradiction | quick | issue-worker-t3 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900028 | not run: owner run required |
| S10-standard | addition that is the only evidence of a contradiction | standard | issue-worker-t2 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900029 | not run: owner run required |
| S10-deep | addition that is the only evidence of a contradiction | deep | issue-worker-t1 | 1 | to fill | keep my wording | 1 create, 1 field POST, 0 comments | to fill | to fill | no / to fill | 900030 | not run: owner run required |
