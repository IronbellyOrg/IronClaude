3939477e29cadc940a1cd304bdf78131bfa8653b
reviewed=367939dd341af696e6a5269861ac1c90978d8949 ref=r3-1
F3.1 sev=blocking trigger=B2 ac=scope at=src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md:84 anchor=src/superclaude/pr_submit/reviewers.py:243 chk=n,y,n,n family=codex-wait-completion-wording fix=In the Codex column of the pending and incomplete rows (augment-poll.md:84 and :87), replace "no completion yet" and "no completion" with "gate state not clean/findings (still polling)" first=A3 origin=new: rows say "no completion yet" / "active but no completion at --timeout", but a completed marker with has_any_findings true, no unresolved Codex root and no Codex formal review on head stays polling
applied tree=76ba1855fafd35ea79d9980d09807e9e6dcb6a00
