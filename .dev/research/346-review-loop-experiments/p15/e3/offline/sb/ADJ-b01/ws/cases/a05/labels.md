## Label A
blocking: no
sentence: The 4 to 5 minute gap is real arithmetic, but the harm (6.5 minutes without a heartbeat) needs the assumption that the worker does not heartbeat between calls and that Orca acts on heartbeat age, which the document marks unverified; the Monitor point is a missing requirement.
evidence: L68 WC-10 'sends a heartbeat every 5 minutes while working ... longer than 5 minutes ... waits of at most 4 minutes'; L104 'split the eval wait into waits of at most 4 minutes'
confidence: low

## Label B
blocking: no
sentence: An implementer who follows WC-10 may run one unsplit tool call of about 4.5 minutes, and the heartbeat gap exceeds 5 minutes only if 'every 5 minutes' is read as cumulative since the last heartbeat and as requiring a heartbeat during a blocking call. The text states neither reading, so the outcome needs an assumption.
evidence: document.md:68 WC-10 'sends a heartbeat every 5 minutes while working ... must be split into waits of at most 4 minutes' (a call of 5 minutes or less is not split); document.md:114 pr-submit row; document.md:104 cli-eval row
confidence: low
