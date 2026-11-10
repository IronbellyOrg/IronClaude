## Label A
blocking: yes
sentence: An implementer who follows the load row and Decisions row builds no contract for load, and that is wrong because WC-4 requires a contract on every outcome and AC-1.1 requires every 3.1-3.2 command, load included, to have an Unattended mode section naming return-contract.yaml; making AC-1.1 pass means adding the report file L265 rejects.
evidence: L112 load row: Report 'none (see note)', in 3.2; L195 AC-1.1 'every command in sections 3.1-3.2'; L62 WC-4; L265 'a report file would be an unrequested addition'
confidence: low

## Label B
blocking: yes
sentence: An implementer who follows the load row and the Decisions row adds no return-contract.yaml, so AC-1.1, which requires every section 3.2 command to name return-contract.yaml, fails for load; an implementer who makes AC-1.1 pass must add the report file that the Decisions row forbids, so the acceptance criterion cannot pass without breaking a stated text.
evidence: L62 (WC-4: contract 'written on success, failure, blocked and partial outcomes'); L92 (workflow row: WC-4 'every outcome'); L112 (load row: Report column 'none (see note)'); L195 (AC-1.1 requires every 3.1-3.2 command to name return-contract.yaml); L265 (Decisions: 'a report file would be an unrequested addition')
confidence: high
