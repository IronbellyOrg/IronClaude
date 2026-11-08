# Tier-1 reflection card (UC-1, pre-execution)

Spec under audit: docs/designs/issue-watcher.md (935 lines). Tasklist under audit: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md (209 items, 10 phases). Card author: orchestrator (inline fallback, `hypothesis_source: inline-fallback`).

## Coverage (deterministic, artifacts/coverage-matrix.yaml)

- Pass 1 (regex `R-/REQ-/SPEC-/T-`): 13 parsed rows, all of them transition ids T-1..T-13 of design section 7.4 (docs/designs/issue-watcher.md:478-490). 12 matched by exact token in the tasklist. T-2 has no exact token in the tasklist.
- Pass 2 (inference): 157 rows submitted, 155 kept (2 dropped because they overlap a parsed span). 133 matched by the containment rule, 22 unmatched.
- Union: 145 of 168 matched, `coverage_pct_union` 0.8631, parsed-only `coverage_pct` 0.9231, `S_dev_density` 0.1369, `coverage_degraded: parsed-sparse` (155 inferred rows against 13 parsed rows).
- The containment rule is lexical: at least 0.6 of a quote's content words must occur inside one task item. A match is weak evidence of real coverage; an unmatch is weak evidence of a gap.
- Structural signals: S_scope 209 items, S_domains 3 (code, tests, docs) which alone forces escalation under rule 4.

## Leads for the reviewers (each is a lead, not a verdict)

1. Unmapped rows to judge by reading both documents: T-2 (docs/designs/issue-watcher.md:479, failed entry backoff), INF-009 (the poller never assigns, comments or moves Project items, :44), INF-016 (non-goals NG-1..NG-5, :70), INF-051 (exit precedence 2, 6, 7, 5, 3, 4, :166), INF-089 (project id compared in Python, never in argv, :558), INF-101 (never-keys list, :718), INF-139 (every recorded prompt matches the D3 regex over a hostile corpus, :880), INF-147 (shared-input exit mapping, :888), INF-151 (sleeping stub ends with gh_timeout, :892). The full list is in artifacts/coverage-summary.yaml.
2. Gate divergence: design section 13 lists `make test` and `uv run ruff format --check src/ tests/` (docs/designs/issue-watcher.md:798,800). The tasklist instead uses a named affected subset, a pinned `uvx --offline ruff@0.15.20` and an xdist run, citing research/06 (DF-05, DF-60). Check that every deviation from the design is declared in the tasklist's Open Questions or Deviations section and that the substitute gates are at least as strict.
3. Section 11 of the design says `cli.py` holds "six verbs" (docs/designs/issue-watcher.md:759) while section 4.1 lists five verb names with `reset` split into two forms (:112-119). Check that the tasklist builds exactly the verbs of section 4.1 and the exit codes of section 4.3.
4. The design's UNVERIFIED shapes (docs/designs/issue-watcher.md:829-847) may enter the tasklist only as `_assumed_shape` fixtures. Check that no item states an unverified gh or Orca reply shape as fact.
5. The tasklist asks one local checkpoint commit before the POST reflect gate and forbids push and PR. Check that the commit allowlist, the BASE capture and the stop rules are internally consistent across Phase 10.

## Grounded checks done by the orchestrator (all held)

- src/superclaude/cli/main.py:559 and :561 show the `reflect_group` import and `main.add_command(reflect_group, name="reflect")`; the design's "two lines after line 561" matches.
- src/superclaude/cli/install_user_setup.py:35 is `_ORCA_CLIS = ("orca-ide", "orca")`; :198 is `def _find_orca() -> str | None:`.
- src/superclaude/cli/swarm/atomic.py:14 is `def write_prepared_bytes(path: Path, data: bytes) -> int:`.
- Makefile:48-50 (`lint: lint-architecture` then `uv run ruff check .`); .github/workflows/test.yml:47 (`-n auto`), :106 (`ruff format --check src/ tests/`), :123 (`make verify-deps`), :131 (`make verify-sync`); pyproject.toml:16 (`requires-python = ">=3.10"`), :54 (`ruff==0.15.20`), :114 (`--strict-markers`).
- Neither src/superclaude/cli/issue_watch nor tests/issue_watch exists yet, so nothing in the tasklist can already be done.

## Risk surface

- Structural: the tasklist has 34 gate-agent items; a gate that reports a finding on a pre-existing skipped test (tests/swarm/test_cli_registration.py:127) could force a false halt unless every gate prompt carves it out.
- Untested invariants: at-most-once launch rests on record-before-launch ordering and five crash points; the tasklist must test each point with five reruns.
- No regression candidate is visible in a pre-execution audit (no diff exists).

## Self-assessed state (not a calibrated score)

Self-reported confidence 0.62: coverage below the 0.90 floor, parsed-sparse labeling, three domains, and no code to ground against beyond the cited anchors. Recommendation: escalate to Tier 2.
