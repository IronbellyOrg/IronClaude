For each case decide, using before.md, after.md and finding.md (the whole documents are authoritative; packet.json is a convenience extract):
resolved: yes if after.md no longer produces the wrong outcome the finding describes, anywhere in the document; else no.
obligation_preserved: yes if after.md still requires what the finding's protected requirement (the text the finding says must hold) requires, in any words or place; no if it was deleted, weakened or made optional; n/a only if the finding itself was wrong about that requirement.
new_conflict: yes if a text added or changed in after.md contradicts another requirement of after.md; else no.
closure_correct: yes only if resolved = yes, obligation_preserved is yes or n/a, and new_conflict = no.
Write one JSON line per case to labels.jsonl: {"case_id", "resolved", "obligation_preserved", "new_conflict", "closure_correct", "evidence": "<quotes from after.md>", "confidence": "high|low"}.
Judge only from the documents. Do not guess what the author intended.

Cases in this sandbox: sm-03, sm-04, sm-05, sm-06, sm-10, sm-15, sm-18, sm-20, sm-26, sm-32
