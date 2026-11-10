## Label A
blocking: no
sentence: R15 explicitly states that deleting a user deletes the documents they own, and the notes (L27) say a document has exactly one owner. Following the text builds exactly the stated behaviour; calling it wrong because teams lose data is a design preference not shown by any contradicting text, so the sentence needs an outside assumption.
evidence: L24 'R15. When a user is deleted, the documents they own are deleted with them.'; L27 'A document has exactly one owner... Teams share documents by adding people to the document'
confidence: low

## Label B
blocking: yes
sentence: An implementer following R15 (line 24) builds user deletion that deletes every document the user owns; per line 27 teams share documents by adding people rather than by folder, so a team's shared document owned by the deleted user is deleted and the team loses its data, which is data loss caused directly by a stated text.
evidence: R15 line 24 'When a user is deleted, the documents they own are deleted with them.'; line 27 'A document has exactly one owner, the user who created it. Teams share documents by adding people to the document, not by sharing a folder.'
confidence: high
