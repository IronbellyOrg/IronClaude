## Label A
blocking: yes
sentence: An implementer who runs AC-0.4 as written in P0 requires steps 1-3 to pass, but step 3 demands the report path be the WC-4 contract path while the same row says the contract arrives in P1 (and P0 has no command edits), so step 3 cannot pass and the P0 gate cannot be passed. AC-0.4 amends step 4 only, not step 3.
evidence: L182 'its report path is the WC-4 contract path'; L194 'steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1'; L158 'P0 ... (no command edits)'
confidence: low

## Label B
blocking: yes
sentence: An implementer who runs AC-0.4 in P0 as written must make step 3 pass, which requires its report path to be the WC-4 contract path, but line 194 says the contract arrives in P1 and P0 has no command edits (line 158), so AC-0.4 cannot pass in P0 as written and the two stated texts contradict.
evidence: AC-0.4 line 194 'steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1'; step 3 line 182 'its report path is the WC-4 contract path'; P0 line 158 '(no command edits)'
confidence: high
