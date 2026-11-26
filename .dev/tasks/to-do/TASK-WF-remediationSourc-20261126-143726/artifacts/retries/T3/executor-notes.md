a9fc1ce2ec233f8373318a94053ad56959ea7755
Disclosures of the T3 run (implementer, not review findings):
- The A1 review prompt was pasted by hand into the reviewer call; the paste has small slips in the line-number prefixes of one evidence file (t3-load-notes.md, around its lines 11 to 13). The saved prompt-1-1.md is the exact text.
- The A2 review ran from the saved prompt through a copy of its text (prompt-2-1.md minus line 1) in a temp file that the reviewer was told to read first, because a second hand paste of 43 KB risked more slips.
- probe-1-1.md was written after the fix edits, not before; its before-outputs say so.
- T3.AC4 and T3.AC5 literal outcomes are not met (see notes.md F2.5 and F2.6). The verdict is derived under the evidence-AC rule (an AC is unmet only for an absent, false or unverifiable evidence row); the load results are reported as measured.
- After the FINAL, on the instruction of the IronFlow session (for Clay), line 78 of the plan was reworded (the same-checkout case of the third pgrep pattern, Augment review comment on PR 908). The plan's sha256 therefore no longer equals the PLAN: pin on line 2 of progress.md; a later /sc:implement resume or archive of this package will report E-PLAN-CHANGED. This was accepted on purpose; the package is not archived (FINAL: issues).
