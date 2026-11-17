0efb510d1c8e6ece4cde589ce2b6d19e43fb5f7a
family label-as-grade (failing review r1-1)
- defect form: a label (CRITICAL, IMPORTANT) used to define or floor a grade
- search command: grep -n -E "CRITICAL or IMPORTANT|IMPORTANT or CRITICAL|blocking \(CRITICAL" -- src/superclaude/agents/rf-qa-qualitative.md
- before-output: src/superclaude/agents/rf-qa-qualitative.md:593 and src/superclaude/agents/rf-qa-qualitative.md:796
- coupled sites: src/superclaude/agents/rf-qa-qualitative.md:593 (the axes paragraph that cites Critical Rule 6), src/superclaude/agents/rf-qa-qualitative.md:796 (fix cycle step 2), the sibling agent src/superclaude/agents/rf-qa.md (no hit: line 389 was reworded in Task 4)
family stale-rule6-floor (failing review r1-1)
- defect form: text that still states the old Rule 6 floor
- search command: grep -n -i -E "remain IMPORTANT|by default|IMPORTANT floor" -- src/superclaude/agents/rf-qa-qualitative.md
- before-output: src/superclaude/agents/rf-qa-qualitative.md:593
- coupled sites: src/superclaude/agents/rf-qa-qualitative.md:593 only (the three relay lines of the task were fixed)
after:
(no hits above means both families are gone)
