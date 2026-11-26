20a5b4889a1482fde59eefb34342aebd4e734312

## family hash-list-incomplete
defect form: the hash list covers fewer files than a run reads
command: grep -n -E -e "templates/|origin_repo|analyze|adversarial" .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness-feasibility.md
before:
119:| fetch URL | `origin` keeps the GitHub fetch URL `https://github.com/IronbellyOrg/IronClaude`, because `scripts/origin_repo.py` needs a GitHub-form fetch U
168:origin_repo.py
183:1abf40eeee2342401b85b042f858f6aaa88aaa5ebc97c80eb750e8912f9c5967  src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md  seeded-equals-src=yes  
184:61c89e9dd6065f69503c6998f6854f8acb640f9517d12e2cdc3656205f9094e1  src/superclaude/skills/sc-issue-protocol/templates/flags-decision.md  seeded-equals-src=ye
185:3ae8241bb81bfae9ebb3d88f5e80789f1ce6392da613d9416d7998bb586349b0  src/superclaude/skills/sc-issue-protocol/templates/create-review-comment.md  seeded-equals
192:The installed copy differs from `src/` for `SKILL.md`, `refs/create.md`, `templates/draft-notes.md`, the three workers and `commands/issue.md`; the seeded h
coupled sites: the sentence after the hash list that calls it the expectation for read-files.txt; section 8 (not shown); plan Task 5 and Task 6 acceptance lines that compare with this list

## family no-answer-unevidenced
defect form: a behaviour is stated that no run recorded
command: grep -n -i -E -e "no answer|waits at the question" .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness-feasibility.md
before:
74:I couldn't ask the question because there's no AskUserQuestion tool in this session. Nothing was sent to you, so I have no answer to print.
109:Answer supplied: yes. The first option of the question screen is selected with Enter. The shipped rule lists "keep my wording" as the first choice (`src/superclaude/skills/sc-issue-protocol/refs/c
coupled sites: section 8 Answer line that says a question screen that could not be answered is recorded unanswered

## family stop-rule-narrowed
defect form: the fork-activity stop rule is narrower than the plan constraint
command: grep -n -i -E -e "attributed|marker|stops the matrix|stop conditions" .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness-feasibility.md
before:
159:The fork is not quiet: another session created an issue and a comment during the minutes of this task, so "any change in fork activity" cannot be the stop rule on its own. Decision (this answers t
226:- Write controls: section 4, plus the fake `gh` and the attributed fork-activity check of Task 5.
227:- Stop conditions (unchanged from the plan, with the two refinements found here): an unknown `gh` call (Claude Code's own `gh auth token` is a known start-up read), an uninterceptable write, an at
coupled sites: the Decided block line in .dev/issues/834/issue-summary.md about the fork-activity rule (not staged); plan Task 5 and Tasks 6 to 8 text that name the stop file

after: hash-list-incomplete
22 matching lines (the section 6 list now holds all 30 files)
after: no-answer-unevidenced
74:I couldn't ask the question because there's no AskUserQuestion tool in this session. Nothing was sent to you, so I ha
109:Answer supplied: yes. The first option of the question screen is selected with Enter. The shipped rule lists "keep m
after: stop-rule-narrowed
159:The fork is not quiet: another session created an issue and a comment during the minutes of this task, so "any chang
247:- Write controls: section 4, plus the fake `gh` and the attributed fork-activity check of Task 5.
248:- Stop conditions (the plan's, with the two refinements found here): an unknown `gh` call (Claude Code's own `gh aut
