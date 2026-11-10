## Label A
blocking: no
sentence: The 4 to 5 minute gap in WC-10 (line 68) is a weakness, but the same document's pr-submit row (line 114) and AC-4.3 (line 210) set 240 s, and the finding needs an assumed call schedule to show a missed heartbeat; no stated acceptance criterion is made impossible and the cli-eval point is about a rule that simply does not apply.
evidence: line 68 WC-10: 'heartbeat every 5 minutes ... longer than 5 minutes ... at most 4 minutes'; line 104 cli-eval: 'split the eval wait into waits of at most 4 minutes'; line 210 AC-4.3.
confidence: low

## Label B
blocking: no
sentence: An implementer who follows WC-10 is not told to make a call of 4 to 5 minutes; a 4.5-minute call that delays a heartbeat depends on whether Orca uses heartbeat age, which the document leaves as an assumption, so the failure does not follow from the stated text.
evidence: Line 68 (WC-10): 'A command step that blocks a single tool call for longer than 5 minutes ... must be split into waits of at most 4 minutes'; line 68 evidence: 'Cadence is from the dispatch preamble, not a guide'; line 210 (AC-4.3) states the 240 s limit.
confidence: high
