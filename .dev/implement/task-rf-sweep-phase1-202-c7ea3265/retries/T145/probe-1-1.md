e2c1d51a27ae663ce88d730459052ca77e60abcb
family=stale-design-line-cite
defect form: a DESIGN line number copied from the item text (written against an earlier design layout) cited as if it were the live line; the live DESIGN file has the cited sentence at a different line.
command: grep -n -E 'line 552|DESIGN 552|DESIGN 973|line 973|line 971' -- .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-17-cursor-template-decision.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md ; grep -n -E 'cursor template is not in the set|^\| 5 \| .worker-list. page size' -- docs/designs/orchestrator-mode.md
before-output (state reviewed in review 1):
1.0a-facts.md:54: ...DESIGN line 552 says a cursor template is added only after step 1.0a captures the cursor field...
1.0a-facts.md:56: ...the DESIGN 973 full-page lower bound applies... (prescribed wording)
OQ-17-cursor-template-decision.md:14: > DESIGN line 552 ... quoted sentence
OQ-17-cursor-template-decision.md:25: ...the DESIGN 973 full-page lower bound applies... (quoted from the item text)
readonly-probe.md: no hit
live design: 559 holds "The worker-list cursor template is not in the set"; 995 holds open item 5; 552 is blank; 973 is a different row
coupled sites: the two files above only; the prescribed refusal wording keeps "DESIGN 973" and gets a clarifier.
after:
(552 changed to 559 in both files; "DESIGN 973" kept as prescribed wording and followed by a note that the live line for open item 5 is 995)
