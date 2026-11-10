You are the adjudicator. For each case in disputes.json two independent labelers disagreed or were unsure. Decide the final label yourself from the documents in cases/<case_id>/ (before.md, after.md, finding.md; the whole documents are authoritative). The two earlier labels and their evidence are in disputes.json: weigh the evidence, do not count votes, and check every quote against the documents.
For each case decide, using before.md, after.md and finding.md (the whole documents are authoritative; packet.json is a convenience extract):
resolved: yes if after.md no longer produces the wrong outcome the finding describes, anywhere in the document; else no.
obligation_preserved: yes if after.md still requires what the finding's protected requirement (the text the finding says must hold) requires, in any words or place; no if it was deleted, weakened or made optional; n/a only if the finding itself was wrong about that requirement.
new_conflict: yes if a text added or changed in after.md contradicts another requirement of after.md; else no.
closure_correct: yes only if resolved = yes, obligation_preserved is yes or n/a, and new_conflict = no.
If a field cannot be settled from the documents, write "undecidable" for that field.
Write one JSON line per case to adjudications.jsonl: {"case_id", "resolved", "obligation_preserved", "new_conflict", "closure_correct", "reason": "<one sentence>"}.
Judge only from the documents. Do not guess what the author intended.

Cases in this sandbox: sm-01, sm-15, sm-16, sm-19, sm-21, sm-22, sm-23, sm-24, sm-29, sm-30
