d95df19b94c424a6b43ad5253478c032ab263523
family=scope-addition (covers F1.1)
defect form: a sentence in the new Wave 2 item that adds behaviour about later STOPs, which the plan's Constraints rule out.
command: grep -n -F -e 'later STOP' src/superclaude/skills/sc-issue-protocol/refs/claim.md
before-output: refs/claim.md:44 (the new item 5) is the only line that contains the phrase.
coupled sites: refs/claim.md:150 (Final output item 4) states the held-line rule for the normal end; it does not mention later STOPs and stays as is.
after-output: 0 hits (expected 0)
