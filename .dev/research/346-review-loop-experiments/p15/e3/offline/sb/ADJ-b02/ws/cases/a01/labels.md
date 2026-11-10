## Label A
blocking: yes
sentence: An implementer who follows WC-4 as written builds the contract at '<--output value>/return-contract.yaml', and this is wrong because tdd and init-lite pass --output as a file (line 87, 90) while AC-2.2 runs '/sc:tdd ... --output <file>' and requires a contract with status: blocked, so the path cannot exist. WC-4 also says the path is 'known before dispatch' while workflow's path uses a generated <id> (line 92). The quotes exist as cited. Some doubt remains because a parent-directory reading is possible.
evidence: document.md:62 'the directory the coordinator passed (--output / --output-dir)' 'known before dispatch'; :87,:90 '--output <file>'; :200 AC-2.2 '/sc:tdd "auth" --unattended --output <file>' 'contract status: blocked'; :92 workflow '.dev/tasks/to-do/<id>/return-contract.yaml'
confidence: low

## Label B
blocking: yes
sentence: An implementer who follows WC-4 writes the contract at <output-dir>/return-contract.yaml, where --output is the directory passed. For tdd and init-lite, AC-2.2 passes --output <file>, so the required path would sit under a file and cannot exist, and AC-2.2 with step 3 cannot pass. For adversarial, the row at L83 names a different path than WC-4.
evidence: L62 WC-4: '<output-dir>/return-contract.yaml, where <output-dir> is the directory the coordinator passed (--output / --output-dir)'; L87 and L90: '--output <file>'; L200 AC-2.2: '/sc:tdd "auth" --unattended --output <file>'; L182 step 3: 'its report path is the WC-4 contract path'; L83: '<output>/adversarial/return-contract.yaml'.
confidence: high
