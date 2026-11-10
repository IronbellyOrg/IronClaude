## Label A
blocking: no
sentence: Fails: WC-4 puts the contract in the coordinator-passed output directory, and P1 adds output flags for commands that lack one (line 159) while line 79 says ready commands report their existing file until P1; the workflow row's package path is today's state, so which path wins after P1 needs a guess, and the outcome does not follow without assuming no output flag is added.
evidence: line 62 WC-4; line 92 workflow row 'Brief must pass --handoff none', report today '.dev/tasks/to-do/<id>/return-contract.yaml'; line 79 'until Phase 1 adds the contract'; line 159 'output flags for commands that lack one'
confidence: low

## Label B
blocking: yes
sentence: An implementer who follows WC-4 as written writes the contract to <output-dir>/return-contract.yaml with the path known before dispatch, but the workflow row passes only --handoff none with no output directory and names a per-run package path, and the adversarial fix names a subdirectory <output>/adversarial/return-contract.yaml that WC-4 does not state, so the stated rules give two different paths and the workflow one cannot be known before dispatch.
evidence: L62 WC-4: 'the command writes <output-dir>/return-contract.yaml'; L73 (2.3): 'so the report path is known before dispatch (WC-4)'; L83 adversarial row: 'Fix the contract filename to <output>/adversarial/return-contract.yaml'; L92 workflow row: brief '--handoff none', contract '.dev/tasks/to-do/<id>/return-contract.yaml'.
confidence: high
