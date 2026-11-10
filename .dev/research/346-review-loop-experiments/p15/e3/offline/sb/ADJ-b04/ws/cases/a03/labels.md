## Label A
blocking: no
sentence: The contradicting text is in command.md, not in the document; the document cannot confirm the claim, and the quoted INV-B:43 text is not in the document.
evidence: line 120 spec-panel row 'add --output; contract'; line 52 / 62 WC-4
confidence: high

## Label B
blocking: yes
sentence: An implementer who follows AC-0.4 runs /sc:troubleshoot in P0 and must pass step 3, whose condition requires the outcome to match 'the contract's status' and the report path to be the WC-4 contract path; P0 makes no command edits and the WC-4 contract arrives only in P1, so step 3 cannot pass as written while AC-0.4 requires it.
evidence: spec:158 ('P0 ... (no command edits)'); spec:182 (step 3: 'its --outcome matches the contract's status under WC-5; its report path is the WC-4 contract path'); spec:194 (AC-0.4 relaxes only step 4: 'step 4 uses the command's existing report file, since the contract arrives in P1'); spec:62 (WC-4 path)
confidence: high
