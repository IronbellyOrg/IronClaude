# QA Report — Source-Document Fidelity (Partition 3)

**Topic:** Orchestrator mode Phase 1 (issue #339)
**Date:** 2026-11-07
**Phase:** source-fidelity
**Fix cycle:** N/A
**Report under review:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/RESEARCH-REPORT-orchestrator-mode.md`
**Fix authorization:** false (report only)

[PARTITION NOTE: Cross-file checks limited to assigned sources: `src/superclaude/cli/main.py`, `src/superclaude/cli/recommend/`, `src/superclaude/cli/reflect/`, cited tests in `tests/cli/` and `tests/recommend/`, `src/superclaude/commands/{reflect,issue,recommend,help}.md`, `Makefile`, `pyproject.toml`, `docs/designs/sc-issue-command.md`.]

## Source-Document Fidelity Report

### Fidelity Findings

| # | Type | Source File | Report Section | Finding | Severity |
|---|------|-------------|----------------|---------|----------|
| 1 | Characterization distortion | `src/superclaude/cli/reflect/config.py`, `src/superclaude/cli/reflect/commands.py`, `src/superclaude/cli/reflect/runner.py` | S2 "CLI structure" (report L193); S6 comparison row K-4 (L1063, tagged [CODE-VERIFIED]) | The report says reflect has "One subprocess seam, `_git` in `config.py:64-78`" and that the precedent is a "single `_git` seam". That is false for the package. `commands.py:570-577` calls `subprocess.run` directly (`tmux new-session`, `attach-session`, `kill-session`), and `runner.py` starts the child through `ClaudeProcess`, which the tests stub separately (`conftest.py:98-138`). Only `config.py` has a single seam. The cited use site is also wrong: `config.py:158-159` is a docstring line ("Lives in `config.py` (the subprocess-owning module)"), not a `_git` call. The real calls are at `:104`, `:127`, `:130`, `:137`, `:181`, `:189`, `:194`, `:202`, `:222` and `:312`. Fix: say "`config.py` routes all of its git calls through one `_git` seam; `commands.py` (tmux) and `runner.py` (`ClaudeProcess`) start processes outside it", and cite `:104` (or `:127-137`) for the use. | IMPORTANT |
| 2 | Characterization distortion / internal contradiction | `tests/cli/reflect/test_contract_status_cli.py` | Executive summary (L1150); S6 A1 Risk row (L953); K-4 row (L1063); X-3 (L1427) | `test_contract_status_cli.py:44-66` patches `ReflectRunner`, `resolve_config` and `ClaudeProcess` with `side_effect=AssertionError`. That proves `contract-status` never reaches the audit entry points (docstring `:44-52`). It does not prove filesystem read-only behaviour. The only write check is one lock path (`:121-139`, `_LOCK_REL` at `:41`). Even so, L1150 says "local-filesystem read-only behaviour is proved with the `side_effect=AssertionError` pattern", and L1063 says the "read-only proof in `isolated_filesystem`" is "already proven" [CODE-VERIFIED]. Step 1.11 (L1218) contradicts both: it says filesystem read-only behaviour is proved by a snapshot diff, that "the snapshot diff has no cited in-repo precedent", and that "That precedent patches entry points only". Fix: in L1150, L953 and L1063, say that the AssertionError pattern covers the subprocess and entry-point half only, and that the filesystem half is the new snapshot diff from step 1.11, with no precedent. | IMPORTANT |
| 3 | Wrong attribution (behaviour) | `src/superclaude/cli/reflect/commands.py`, `src/superclaude/cli/recommend/commands.py` | S8 step 1.6 (L1208) | Step 1.6 gives "1 internal error, `[sweep ...]` prefix on stderr (reflect pattern, scope-03)". Reflect does not do this. It prints `Error: {exc}` to stderr and exits `_BLOCKED_EXIT` (2) on a config STOP (`reflect/commands.py:389-428`), and its verdict line is `reflect: <verdict> (<reason>)` (`:478`). The `[name ...]` stderr prefix with `sys.exit(1)` belongs to recommend (`recommend/commands.py:73-74`; 13 `[recommend ...]` prefixes). Section 2 attributes it correctly (L196, `recommend/commands.py:73-75`), so the plan contradicts the report's own Section 2. Fix: change "(reflect pattern, scope-03)" to "(recommend pattern, `recommend/commands.py:73-74`)". | IMPORTANT |
| 4 | Detail imprecision | `src/superclaude/cli/main.py` | S2 "CLI structure" (L186) | The report lists init-lite among the "registered groups". `main.py:555-557` registers `init_lite_command`, which is a command, not a group. The other ten names are correct, and no `sweep` exists (verified at `:519-561`). | MINOR |
| 5 | Citation imprecision | `src/superclaude/cli/recommend/commands.py` | S2 (L196) | "Click option conventions follow `:34-48`". Lines 34-48 hold the `@click.group("recommend")` decorator and its docstring and contain no `@click.option`. The first option convention is at `:57-64`. The `:73-75` citation (stderr prefix and exit 1) is correct. | MINOR |
| 6 | Citation imprecision | `tests/cli/reflect/conftest.py` | K-4 row (L1063) | `conftest.py:58-80` is cited for the "read-only proof in `isolated_filesystem`". conftest has no `isolated_filesystem`. It appears in `test_contract_status_cli.py:90`, `:109` and `:133`. The `patch_git` claim for `:58-80` is correct (`monkeypatch.setattr(config_mod, "_git", _fake_git)` at `:74`). | MINOR |
| 7 | Citation imprecision | `tests/cli/reflect/test_contract_status_cli.py` | S4 SC-1 row (L438) | The subprocess-half precedent is cited as "`test_contract_status_cli.py:44-66` pattern (`scope-03:99`)". Elsewhere the report uses `scope-03:99` as the NB-4 argv allowlist (L206, L1446), not the AssertionError pattern. | MINOR |
| 8 | Omission (counter-precedent) | `src/superclaude/commands/help.md` | S9 contradiction resolution P6-01 (L1567) | The resolution says "the cited precedents use the space form". That is true of `sc-swarm-wizard-protocol/SKILL.md:7` and `sc-crash-recovery/SKILL.md:4`. But the assigned source `help.md:6` uses the colon form (`Bash(find:*)`, `Bash(git rev-parse:*)`), so both forms are live in the repo. The decision still holds; the resolution just does not mention the counter-example. | MINOR |
| 9 | Count imprecision | `docs/designs/sc-issue-command.md` | S2 (L233) | "20 headings": the file has 20 numbered `##` sections (`:11` to `:467`) plus the H1 title at `:1`, which makes 21 headings. "20 sections" would be exact. | MINOR |

### Claims verified against source (phantom-finding check: no phantom found)

| Report claim | Source evidence | Result |
|---|---|---|
| Root Click group `main.py:18-26`; deferred registration `:519-561`; `__main__` guard `:564-565`; `# noqa: E402,I001  # intentional: ...` comment at `:559`; insert after `:561` (steps 1.7, SC-10) | `main.py:18-26`, `:519-561`, `:559`, `:564-565` read | Exact |
| Lazy `__getattr__` in `recommend/__init__.py:12-20`; eager imports in `reflect/__init__.py:17-30` | Both files read in full | Exact |
| `contract.py:7`, `:397` "No Click, no subprocess" | `contract.py:7` ("No Click, no subprocess, ...") and `:397` ("PURE: no Click, no subprocess, no I/O") | Exact |
| `_git(cwd: Path, *args: str) -> str` raises `SubprocessError`/`OSError` with `check=True`, `timeout=10`; `_resolve_base` catches both and raises `ValueError("base-unresolved: ...")` at `:103-109` | `config.py:64-78`, `:103-109` | Exact |
| `patch_git` fixture at `conftest.py:58-80`; `FIXTURES_DIR` at `:17` | `conftest.py:17`, `:58-80` | Exact |
| `side_effect=AssertionError` patches at `test_contract_status_cli.py:44-66`; `isolated_filesystem` docstring `:18-22` | Lines 44-66 patch three entry points; `:18-22` names `isolated_filesystem` | Exact (but see finding 2 on what the test proves) |
| `tests/recommend/test_cli_registration.py:1-39` is a CliRunner registration test | 39 lines plus a trailing blank; three `CliRunner` `--help` tests | Exact |
| `_POST_REFRESH_ADDITIONS` at `test_routing_refresh.py:33`; asserted at `:647-648`; Activation regex `:38-40`; `> Skill` parse `:472` | All four ranges read | Exact |
| `EXPECTED_TOP_LEVEL_COMMANDS` at `tests/cli/test_cli_registration.py:31-49` | `:31-49` | Exact |
| Frontmatter `issue.md:1-9`, bare `name: issue`; Activation `reflect.md:146-151` ("**MANDATORY**: Before executing any protocol steps, invoke: > Skill sc:reflect-protocol"); `issue.md:87-93` has the same form | Read | Exact; step 1.14 Activation text matches the source form |
| `recommend.md:2` is `name: sc:recommend` (not bare); its Activation uses `> Skill sc-recommend` (not an identical form) | `recommend.md:2`, `:52-56` | Exact |
| `allowed-tools` set in 14 of 46 command files | Grep: 14 files; Glob: 47 `.md` minus `README.md` = 46 | Exact |
| `[CODE-CONTRADICTED]` recommend docstring says `python -m`, but there is no `__main__.py` | `recommend/commands.py:41` (`uv run python -m superclaude.cli.recommend`); Glob of `cli/recommend/` shows no `__main__.py` | Exact |
| lint-architecture Checks 1 `:368-383`, 2 `:385-396`, 3/4 `:398-411`, 6 `:413-427`, 8 `:429-439`, 9 `:441-451`, 11 `:467-476`; target spans `Makefile:362-489`; Check 11 scans `src/superclaude/cli/` against `contracts/__init__.py` | Makefile grep + reads at `:362-381`, `:464-491` | Exact |
| Ruff pinned `ruff==0.15.20` at `pyproject.toml:54`; anthropic ban `:203-206` | pyproject grep | Exact |
| sc-issue "No CLI (`src/superclaude/cli/`) code: the only program is the skill's own script." at `:384`; scripts at `:362-363`; script tests at `:395-396`; run line `:402` | `sc-issue-command.md:346-407` read | Verbatim quote exact |

### Checklist results

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Semantic coverage of CLI registration, lazy import, config and test patterns | PASS (with defects) | All four patterns are covered in S2 and carried into steps 1.1, 1.4, 1.7, 1.8, 1.11 and 1.13. Coverage is complete; characterization defects are findings 1-3 |
| 2 | Detail preservation (`_git`, line numbers, `side_effect=AssertionError`, frontmatter, Activation block) | FAIL | `_git` signature and raise behaviour preserved exactly; the `:158-159` use site is wrong (finding 1); the AssertionError proof is overstated (finding 2); frontmatter and Activation preserved exactly |
| 3 | Phantom findings (at least 5 claims verified) | PASS | 16 claim groups verified above; no fabricated path, function or line |
| 4 | Characterization accuracy | FAIL | Findings 1, 2 and 3 (single seam, read-only proof, reflect error pattern) |
| 5 | No aspirational claims | FAIL | L1063 tags "already proven ... read-only proof" [CODE-VERIFIED], but the source only proves that the entry points are never called (finding 2). The new sweep design items are labelled "plan decision, new design", which is correct |

## Summary

- Findings: 9 (CRITICAL: 0, IMPORTANT: 3, MINOR: 6)
- Blocking findings: 1 (reflect is not a single-seam package; wrong `:158-159` use site), 2 (the AssertionError precedent is presented as a filesystem read-only proof, which contradicts step 1.11), 3 (step 1.6 attributes recommend's `[name ...]` + exit 1 pattern to reflect, which uses `Error:` + exit 2)
- None of the three changes the recommendation (A1 still meets K-4 with its own seams and the new snapshot diff), but each is a false statement about the code and two are tagged [CODE-VERIFIED].
- MINOR findings 4-9 are notes and need no fix pass.
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 31 | Grep: 14 | Glob: 2 | Bash: 0 (no web research; no tests or builds run)

Verdict: FAIL
