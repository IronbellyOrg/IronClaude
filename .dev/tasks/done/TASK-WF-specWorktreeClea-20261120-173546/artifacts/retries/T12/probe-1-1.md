44f5941e9fc784d4934bd6650ea57ab811cc7d1a
family: orca-unreadable-fails-open
defect form: an unreadable list of worktrees from the tool is turned into "none listed", which rule 8 reads as not pinned
command: grep -n -E "is_pinned|by_path|treating every worktree" scripts/worktree_cleanup.py
before: 612 (field), 732 (parser), 1741 (rule 8 reads orca.is_pinned only when orca is not None), 2697 (the unreadable case only prints a note)
coupled sites: RuleInputs (needs a known flag), _rule8, assess, find_worktrees, test_verbs.py fallback test

family: exit-code-lookup
defect form: a reason caused by an unreadable fact is not counted as a lookup failure
command: grep -n -E "_lookup_failed|EXIT_FAILED|EXIT_USAGE" scripts/worktree_cleanup.py
before: 2817 (two prefixes only), 2851 (summary), 2973-2976 (archive), 2995-2997 (retire), 2954-2956 (selector)
coupled sites: Decision (needs an unread flag), decide, _summarize, _one_worktree, tests in test_verbs.py

family: out-inside-worktree
defect form: a verb path that can create files under --out skips the check that --out is outside every worktree
command: grep -n -E "_inside_any|RepoLocks\(|\.mkdir\(" scripts/worktree_cleanup.py
before: 2908 (list and prune only), 2793 (the lock creates the folder), 2930 (prune files)
coupled sites: _run_verb, _one_worktree, RepoLocks.acquire

family: exit-code-oserror
defect form: a file operation on the output folder outside a try block
command: grep -n -E "\.mkdir\(|write_text\(|open\(self\.out" scripts/worktree_cleanup.py
before: 2793 (acquire), 2930-2936 (prune files)
coupled sites: RepoLocks.acquire, _apply_removal, _run_verb
after:
676:    """(repo or None, number) from Orca's linkedIssue; anything unreadable is None."""
1310:        return PrLookup(False, None, "gh pr list gave an unreadable reply")
1372:    return Landed("UNKNOWN", "gh pr view", f"{why}: unreadable reply")
1490:    unread: list[str] = []
1493:        unread.append(f"issue lookup failed: {references.unavailable}")
1520:    failures: list[str] = list(unread)
1580:    orca_known: bool = True
1758:    if not i.orca_known:
1784:            unread = reason.startswith(UNREAD_PREFIXES) or after_unknown
1785:            return Decision("kept", number, reason, "", cell, unread)
2572:    """Does an ``orca worktree list --json`` reply hold this worktree? None: unreadable.
2729:    return Found(pairs, notes, failures, orca_known=listed.ok)
2740:    orca_known: bool = True,
2751:        orca_known=orca_known,
2786:        assess(runner, cfg, wt, orca, scan, now, own, found.orca_known)
2828:            self.out.mkdir(parents=True, exist_ok=True)
2868:        if locks.error:
2869:            return "failed", locks.error, ""
2890:        if r["decision"] == "failed" or (r["decision"] == "kept" and e.decision.unread)
2920:def _inside_any(path: Path, found: Found) -> bool:
2942:    if _inside_any(out.expanduser(), found):
2952:                out.mkdir(parents=True, exist_ok=True)
2977:                (out / f"prune-{stamp}.md").write_text(
2980:                (out / f"prune-{stamp}.json").write_text(
3022:        found.orca_known,
3030:            return EXIT_FAILED if d.unread else EXIT_USAGE
3033:                f"error: {locks.error or 'another run holds the lock'}", file=sys.stderr
3053:        return EXIT_FAILED if d.unread else EXIT_USAGE
