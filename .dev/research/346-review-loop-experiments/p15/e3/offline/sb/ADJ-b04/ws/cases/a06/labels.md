## Label A
blocking: no
sentence: P1 scope (line 159) says the WC-4 contract in unattended mode and the --unattended flag apply to every command in 3.1 and 3.2, and line 79 says Phase 1 adds the contract. The 'Small fix: None' cells do not contradict that. Following the rows into a build without the contract needs a guess that the column overrides the scope sentence.
evidence: document.md:62 WC-4; :79; :87 init-lite 'None'; :159 P1 scope; :196 AC-1.2
confidence: high

## Label B
blocking: yes
sentence: An implementer who follows the phase table and the init-lite row never adds a contract to init-lite. L159 says --unattended is accepted by every command in 3.1, and L62 says the command writes return-contract.yaml in unattended mode on every outcome, so init-lite run unattended writes no contract and violates WC-4. This relies only on the stated text, though the phase placement is incomplete.
evidence: L62 WC-4 'In unattended mode the command writes <output-dir>/return-contract.yaml ... on success, failure, blocked and partial outcomes'; L87 init-lite row, Small fix 'None'; L159 P1 scope 'the --unattended flag accepted by every command in sections 3.1 and 3.2'; L158-L162 phase table, which lists init-lite in no phase.
confidence: low
