## Label A
blocking: no
sentence: The problem needs a brief that uses --depth deep with a short input or a bare tdd topic, which the document never states; the stated flags are followed as written and the unflagged prompts are listed in the same rows with the P2 fix, so this is a missing restriction on inputs, not a contradiction.
evidence: L79 'run as workers now if the brief uses the stated flags'; L90 tdd 'a precise component prompt, not a bare topic' and 'nested /task ... resolve as blocked (P2)'; L91 troubleshoot 'no --fix' and '--depth deep short-input STOP ... (P2)'
confidence: high

## Label B
blocking: no
sentence: An implementer who follows section 3.1 with only the stated flags, and uses a bare topic for tdd or --depth deep with a short input for troubleshoot, gets a prompt that stalls the worker. The stall is real, but WC-2 (line 60) governs only --unattended runs, and no acceptance check (AC-0.4, AC-1.2) covers tdd or troubleshoot's deep path, so the text forces no impossible criterion and the stall is not a stated-text contradiction of the blocking kind.
evidence: line 79 (section 3.1: 'These run as workers now if the brief uses the stated flags'); line 90 (tdd row: nested '/task' ask-the-user lines resolve as blocked only 'Under --unattended (P2)'); line 91 (troubleshoot row: '--depth deep short-input STOP ... (P2)'); line 60 (WC-2: 'Under --unattended the command never calls AskUserQuestion'); line 194 (AC-0.4 covers troubleshoot without --fix)
confidence: low
