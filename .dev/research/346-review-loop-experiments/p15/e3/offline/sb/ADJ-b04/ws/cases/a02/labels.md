## Label A
blocking: yes
sentence: An implementer who runs AC-0.4 as written must make step 3 pass ('its report path is the WC-4 contract path' and outcome matches the contract's status), but line 194 says the contract only arrives in P1 and substitutes only step 4. Troubleshoot without --fix writes REPORT.md, so step 3 cannot pass in P0. The spec's own text makes this criterion impossible to pass. Part of the finding (the 'command' key claim for workflow) rests on inventory files not in the document and is unchecked.
evidence: document.md:194 AC-0.4 'steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1'; :182 step 3; :183 step 4; :91 troubleshoot 'REPORT.md'
confidence: low

## Label B
blocking: yes
sentence: AC-0.4 requires steps 1-3 to pass in P0, but step 3 requires the report path to be the WC-4 contract path, and P0 adds no command edits, so the contract does not exist. The acceptance criterion cannot pass as written in P0.
evidence: L194 AC-0.4: 'steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1'; L182 step 3: 'its report path is the WC-4 contract path'; L158 P0: 'no command edits'; L159 P1: 'The WC-4 contract in unattended mode'.
confidence: high
