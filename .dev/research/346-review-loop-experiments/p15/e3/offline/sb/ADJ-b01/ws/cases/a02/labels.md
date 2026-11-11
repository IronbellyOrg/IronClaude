## Label A
blocking: no
sentence: Fails: the cited SPCMD text and the git-ignored rule do not exist in the document; the file-valued --output for tdd and init-lite leaves the contract location unstated rather than contradicting WC-4, and AC-1.2's P1 commands include no file-valued --output command, so the wrong outcome needs a guess.
evidence: line 62 WC-4; line 87 init-lite '--output <file>'; line 90 tdd '--output <file>'; line 196 AC-1.2 applies to P1 commands; no 'SPCMD' or 'report-dir' anywhere in the document
confidence: high

## Label B
blocking: yes
sentence: An implementer who follows WC-4 as written treats --output as the directory the coordinator passed, but the tdd and init-lite rows define --output as a file, so applying WC-4 to tdd writes the contract into a path that is a file, and the stated rules cannot both be met for those commands.
evidence: L62 WC-4: '<output-dir> is the directory the coordinator passed (--output / --output-dir)'; L90 tdd row: 'a precise component prompt ... --output <file>'; L87 init-lite row: '--output <file>'; L83 adversarial row and L84 brainstorm row: '--output <dir>'; L120 spec-panel row: 'add --output' with no type.
confidence: low
