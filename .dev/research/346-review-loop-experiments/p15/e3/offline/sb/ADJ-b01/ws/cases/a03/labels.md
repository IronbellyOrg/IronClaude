## Label A
blocking: no
sentence: An implementer who follows the stated text builds P1 so that every 3.1/3.2 command accepts --unattended and has the section, but this is wrong only if the section must carry gate resolution P1 does not deliver; the text does not say that, so the outcome needs a guess about what the P1 section contains.
evidence: L159 'flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)'; L195 AC-1.1 only asserts a section naming return-contract.yaml and WORKER-CONTRACT.md; L160-162 gate conversion in P2-P4
confidence: low

## Label B
blocking: no
sentence: An implementer who follows P1 as written accepts --unattended on tdd while the topic-only clarification is still live. That is wrong only if WC-2 is read as binding in P1, which the spec does not state; the P1 row makes the flag a no-op where a gate is unconverted, so the outcome needs a phase-timing assumption.
evidence: document.md:159 P1 scope 'the --unattended flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)'; document.md:60 WC-2 'never calls AskUserQuestion'; document.md:90 tdd row 'topic-only clarification ... (P2)'; document.md:154 'Each phase is independently useful'; document.md:195 AC-1.1
confidence: low
