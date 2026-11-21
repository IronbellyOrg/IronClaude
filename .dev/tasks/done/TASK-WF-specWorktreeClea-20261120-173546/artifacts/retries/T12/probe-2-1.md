44f5941e9fc784d4934bd6650ea57ab811cc7d1a
family: exit-code-recheck
defect form: a step of the removal that cannot read a fact returns status kept, so the verbs count it as a plain verdict and not as a lookup failure
command: grep -n -E "RemovalResult\(\"kept\"" scripts/worktree_cleanup.py
before: the re-check after the terminals are closed returns kept for an unreadable git status, an unknown relation to the pull request, a failed process scan, and for a changed worktree; _apply_removal passes the status through; _summarize and retire read only the decision made before the removal
coupled sites: remove_worktree, _apply_removal, _summarize, _one_worktree (retire exit code), tests in test_removal.py that pin the kept status for a change made while terminals closed
after (attempt 3):
2408:        return RemovalResult("failed" if first.unread else "kept", first.reason)
2411:        return RemovalResult(
2422:            return RemovalResult("failed", saved.reason, tuple(steps))
2437:            return RemovalResult(
2449:    unreadable = ""
2451:        unreadable = "the folder could not be read"
2453:        unreadable = "git status could not be read"
2455:        unreadable = "HEAD could not be read"
2460:                unreadable = "a saved file could not be read"
2462:    if unreadable:
2463:        return RemovalResult(
2465:            f"re-check failed: {unreadable} after the terminals were closed",
2478:    if after.relation == "unknown":
2479:        return RemovalResult(
2481:            f"re-check failed: {after.reason}",
2485:    if changed or after.relation not in ("same", "ancestor"):
2486:        return RemovalResult(
2494:        return RemovalResult(
2501:        return RemovalResult(
2517:            return RemovalResult(
2534:        return RemovalResult(
2546:        return RemovalResult("failed", problem, tuple(steps), branch_note, verified)
2548:    return RemovalResult("removed", "", tuple(steps), branch_note, verified)
