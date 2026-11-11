## Label A
blocking: no
sentence: Section 2.3 (line 73) and 7.2 step 1 say the brief carries --unattended, while AC-0.4 (line 194) and P0 (line 158, no command edits; 3.1 says ready commands run with 'the stated flags', which exclude --unattended) list the P0 commands without it. Which text governs P0 needs a guess (general rule versus the specific P0 and 3.1 text), and an unknown flag's effect is not stated, so the outcome does not follow without assumption.
evidence: line 73: "the exact command line including `--unattended`"; line 158: "(no command edits)"; line 79: "run as workers now if the brief uses the stated flags"; line 159: "the `--unattended` flag accepted by every command"; line 194 AC-0.4 commands without the flag
confidence: low

## Label B
blocking: yes
sentence: An implementer who follows L73 for the P0 runs puts --unattended in the brief for /sc:troubleshoot, /sc:workflow and /sc:adversarial. P0 makes no command edits (L158) and L159 says the flag arrives in P1, so the command does not accept it. An implementer who follows L194 omits the flag, which breaks L73. The two stated texts contradict each other, and the document does not say that P0 briefs omit it.
evidence: L73 (section 2.3): 'the exact command line including --unattended'. L158 (P0): 'Then run three ready commands as real Orca workers, invoked directly'; 'no command edits'. L159 (P1): 'the --unattended flag accepted by every command'. L194 (AC-0.4): '/sc:troubleshoot ... /sc:workflow ... --handoff none, /sc:adversarial --compare ... --output <dir>' with no --unattended.
confidence: high
