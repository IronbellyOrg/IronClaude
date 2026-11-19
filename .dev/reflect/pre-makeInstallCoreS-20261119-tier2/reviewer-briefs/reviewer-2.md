# Reviewer brief 2 (persona: qa; model class: haiku alias)

You are a read-only reviewer for a pre-execution (UC-1) reflection. Judge the PLAN against its SPEC and the real code. You may Read, Grep and Glob; do not run commands or edit anything. Return your card as text; the orchestrator saves it.

Card format to return: a header line `reviewer: 2 persona: qa`, then `## Findings` as one bullet per finding with `severity` (blocking | minor | note), a one-line claim, and `file:line` citations that you Read yourself; then `## Coverage verdict` (does the plan cover every spec requirement, yes/no with reasons); then `## Risks the first run missed` (list, or "none found" with what you checked); then `## Recommendation` (one concrete action: file, change, verifier); then `reviewer_model_self_report: <the model you run as>`. Tag any claim you could not cite as [INFERRED]. A finding that is only wording is a note, not blocking. A zero-finding result is valid if you state what you checked.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## T1 card excerpt

Plan: `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md` (2 tasks: Task 1 replaces install_core's private comparison with `install_keep.same_content`; Task 2 adds a test proving a same-size same-mtime rewrite is reported stale).

Coverage result of the first run: union coverage 1.00 (5 of 5 inferred requirements mapped); parsed coverage null because the spec is one unlabelled prose line, so `coverage_degraded: parsed-sparse` fired. Acceptance in the plan: Task 1 AC1 (no `filecmp` import, no `_same_content`, caller uses `same_content`), AC2 (`uv run pytest tests/cli -q -k install` passes, including `test_skip_without_force_names_only_stale_files`); Task 2 AC1 (new test passes with Task 1 applied and fails with the old comparison, checked through a throwaway pytest plugin that disables `filecmp.clear_cache`), AC2 (`uv run pytest tests/cli/test_how_we_work_install.py -q` and ruff on both files pass).

Questions for you as QA: (1) Is each acceptance check observable and does it fail when it should? (2) Does Task 2's test really reproduce the stale-cache bug (cache key is size plus mtime; the test rewrites with the same size and restores the old mtime)? (3) Are there inputs the spec implies that no task or test covers (for example the OSError path, a missing kept file, the `--force` path)? (4) Is anything in the plan unverifiable?
Context: the plan has since been implemented; judge the plan's design, not today's line numbers.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-19T01:43:08Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-606 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-606

### .dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/source.md:1-1
The spec body (whole file; Read it yourself): "Make install_core._same_content use the fixed install_keep.same_content so it no longer answers from filecmp's stale cache. Files: src/superclaude/cli/install_core.py (lines 121-125, private _same_content; its caller at line 97) and a test in tests/cli for install_core. Source: the troubleshoot report .dev/troubleshoot/test-same-content-20261119/REPORT.md; install_keep.same_content already calls filecmp.clear_cache() first. Acceptance: a same-size same-mtime rewrite is reported as different by install_core; existing tests/cli -k install stay green."

### src/superclaude/cli/install_keep.py:18-26
```python
def same_content(a: Path, b: Path) -> bool:
    """True only when both files are readable and byte-identical."""
    # filecmp caches results by (size, mtime), so a same-size rewrite within one timestamp tick
    # would be answered from the cache; the cache is only a speed-up, so drop it first.
    filecmp.clear_cache()
    try:
        return filecmp.cmp(a, b, shallow=False)
    except OSError:
        return False
```

### tests/cli/test_how_we_work_install.py:118-134
```python
def test_same_size_rewrite_with_old_mtime_is_reported_stale(tmp_path):
    """filecmp caches answers by (size, mtime); a same-size rewrite that keeps
    its old mtime must still be reported, not answered from the cache."""
    target = tmp_path / ".claude"
    shipped = (install_core._get_core_source() / "PRINCIPLES.md").read_bytes()
    kept = target / "PRINCIPLES.md"
    _seed(kept, shipped)
    install_core.install_core_files(target_path=target, force=False)  # primes the cache

    before = kept.stat()
    kept.write_bytes(bytes([shipped[0] ^ 1]) + shipped[1:])  # same length, one byte differs
    os.utime(kept, ns=(before.st_atime_ns, before.st_mtime_ns))

    ok, message = install_core.install_core_files(target_path=target, force=False)

    assert ok, message
    assert "PRINCIPLES.md" in message.split("NOT updated")[1]
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 install_core uses fixed same_content | Task 1 | covered | install_core.py:12, :98 |
| INF-002 no answer from filecmp's stale cache | Task 1, Task 2 | covered | install_keep.py:22 |
| INF-003 a test in tests/cli for install_core | Task 2 | covered | test_how_we_work_install.py:118 |
| INF-004 same-size same-mtime rewrite reported as different | Task 2 | covered | test_how_we_work_install.py:127-134 |
| INF-005 existing tests/cli -k install stay green | Task 1 | covered | plan acceptance, Task 1 |
