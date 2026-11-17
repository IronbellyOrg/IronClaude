# Debate transcript — shadow12 Wave 4 (Mode A compare, 3 cards, zero findings)

Participants: advocate for reviewer-1 (analyzer, sonnet), advocate for reviewer-2 (qa, haiku), advocate for reviewer-3 (refactorer, opus). Judge: inline orchestrator (claude-gw-tier3 alias; distinct from all three debater classes — no class collision).

Round 1 (advocate opening, each):
- R1 advocate: my card found no contradiction, unpassable check or missing requirement; spec coverage maps all six fence pairs to Task 1/Task 2 with identical line numbers and the same fallback rule; evidence artifacts corroborate every AC (fence-after none at L280-281, headings outside at L20/142/157/181, Appendix B inside at L259, Appendix C outside at L268, dash rc=1, baseline cmp rc=0). I rejected the orchestrator's C-05 hypothesis: the AC requires EVERY `### Example N:` heading outside any fence, so a future fenced Example heading would fail the check, not pass it.
- R2 advocate: my card audited all 9 coverage rows against the full spec body verbatim; no requirement-bearing span is absent from the matrix; every AC is mechanically checkable from recorded evidence. The matrix's source-line numbering quirk (cites L7 for a span that sits elsewhere) is a citation-formatting note, not a missing requirement.
- R3 advocate: my card checked the process design (baseline-by-copy, byte-exact script copy, superseded-prompt archival) and residue on HEAD; C-04/C-06/C-07 all resolved as non-defects with the move covered three ways (ARCHIVE ruling, README old-to-new mapping, closing FINAL citing only live artifacts).

Round 2 (cross-examination):
- R1->R2: did you verify the guide-diff twelve-line claim yourself? R2: no, it rests on the hunk text and the ledger; the orchestrator re-read guide-diff.txt (12 lone-fence changed lines) during Wave 1 grounding. Accepted as grounded by orchestrator evidence.
- R2->R3: the t1-notes/t2-notes files are absent though the plan says to record moved line numbers there. R3: the notes files are conditional ("if a line number has moved" — at execution time none had), so their absence is conformant, not a defect. No dispute.
- R3->R1: the FINAL: issues evidence paths dangle after the move. R1: traceable via README + ARCHIVE ruling; not filed. No dispute.

Round 3 (judge): no contested findings exist; all three cards are zero-finding with stated check scopes. Nothing to merge beyond the empty set. Convergence trivially 1.0. The one candidate claim (C-05 generic Example-heading AC, orchestrator-raised) was rebutted by R1 with the AC's own wording and is dropped. debate_skipped_similar: false (the debate ran; the variants are identical in verdict but the transcript records the cross-examination).
