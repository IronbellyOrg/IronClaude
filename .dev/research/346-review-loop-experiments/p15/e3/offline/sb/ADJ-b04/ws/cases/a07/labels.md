## Label A
blocking: no
sentence: An implementer who follows the cleanup-audit row (line 85) is told 'output dir is fixed, so one audit per worktree at a time (WC-11)', so the text itself states the one-at-a-time restriction; the claimed double dispatch needs a coordinator that ignores the row, which is an extra assumption. The mis-citation of WC-11 is a weak point but does not force a wrong build.
evidence: L85: "output dir is fixed, so one audit per worktree at a time (WC-11)"; L69: "Default output paths carry a timestamp or the slug the coordinator passes"; the cited `commands-a.md:42` is not in the document
confidence: low

## Label B
blocking: no
sentence: Fails: an implementer who follows the cleanup-audit row (line 85, 'one audit per worktree at a time') is told not to dispatch two audit workers into one worktree, so the double-dispatch needs the coordinator to ignore a stated rule. The gap is a missing enforcement in the brief, not a contradiction that yields a determinate wrong build.
evidence: Line 85: 'output dir is fixed, so one audit per worktree at a time (WC-11)'. Line 69 (WC-11): 'Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes'. Line 73 (section 2.3) lists brief contents with no concurrency rule.
confidence: low
