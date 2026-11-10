## Label A
blocking: no
sentence: Lines 73 and 79 differ on whether the brief shows --unattended, but the claimed harm (the P0 smoke run not exercising the contract) is not a failure: AC-0.4 (line 194) already uses existing report files, and how a command treats an unknown flag is a guess.
evidence: line 73 'including --unattended'; line 158 'no command edits'; line 159; line 79 'the stated flags'; line 194
confidence: low

## Label B
blocking: yes
sentence: An implementer who follows section 2.3 ('the exact command line including --unattended') writes --unattended into the P0 smoke-run briefs for /sc:troubleshoot and /sc:workflow, while P0 makes no command edits and the flag is added only in P1, so the P0 run that AC-0.4 requires does not exercise the stated contract; the two stated texts disagree on whether P0 briefs carry the flag.
evidence: spec:73 (2.3: each brief 'states the exact command line including --unattended'); spec:158 (P0 'no command edits'); spec:159 (P1 adds the flag); spec:79 and spec:81-92 (3.1 ready commands run 'if the brief uses the stated flags', none listing --unattended); spec:180 and spec:194 (AC-0.4 builds the brief 'per section 2.3')
confidence: medium
