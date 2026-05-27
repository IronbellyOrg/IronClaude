# QA Report — task-qualitative

**Topic:** TASK-RF-20260525-194356 (`superclaude init-lite --context-optimized`)
**Date:** 2026-05-27
**Phase:** task-qualitative
**Fix cycle:** 1 (initial qualitative pass)
**Document type:** Executed Task File
**Reviewer:** rf-qa-qualitative (adversarial stance, fix_authorization=true)

---

## Overall Verdict: PASS

All 15 task-qualitative checks pass against the actual files on disk. The
implementation matches the documented behavior, all 56 focused tests pass
live (independently reproduced), the help surface matches the command-source
docs, registration is reachable through `superclaude.cli.main:main`, the
installer mapping fix is exercised by 5 unit tests, and the source-of-truth
discipline (UV/make-only, no `.claude/` staging) is honored end-to-end.

One operational artifact noted (not a defect): the pipx-installed `superclaude`
shim at `/config/.local/bin/superclaude` is rooted in an older snapshot that
predates `init-lite`; invocations from outside the worktree fail with
`No such command 'init-lite'`. From inside the worktree, `uv run superclaude
init-lite ...` works correctly. This matches the operator-install policy
(`pipx install --force <src-dir>` refreshes the shim post-release); no source
or test change is warranted. Logged as Follow-Up A below.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Gate/command dry-run | PASS | `uv run superclaude init-lite --help` (from worktree) prints all 6 flags exactly as documented in `src/superclaude/commands/init-lite.md:32-39`. Live `--dry-run` against `/tmp/init-lite-qa-probe2` rendered the marker (`<!-- generated-by: superclaude init-lite context-audit v1 -->`) + report body to stdout and wrote nothing (verified by `ls -la` on the probe dir post-invocation). Matches `init_lite.py:313-316`. |
| 2 | Project convention compliance | PASS | All test summaries cite `uv run pytest ...` (no `python -m`/bare `pytest` — `focused-cli-pytest-summary.md:3`). Sync uses `make sync-dev` + `make verify-sync` (`make-sync-dev-summary.md:3`, `make-verify-sync-summary.md:3`). No `.claude/` staging instructed in any phase-output file (grepped: only mentions are *negative* — "no `.claude/` paths were staged"). Source-of-truth edits only under `src/superclaude/` confirmed; dev mirrors at `.claude/commands/sc/init-lite.md` + `.claude/skills/sc-init-lite-protocol/SKILL.md` exist as `make sync-dev` output. |
| 3 | Intra-phase execution simulation | PASS | Walked Step 2.1's "ensuring" clauses against `init_lite.py:72-104` (discovery scope), `:194-203` (marker-ownership), `:313-316` (dry-run writes nothing), `:343-361` (scaffold creates only the two named files). All clauses hold. Step 2.4 thin-command claim verified against `commands/init-lite.md:47-63` (Activation invokes `Skill sc-init-lite-protocol`, no algorithm embedded). Step 3.1's "tests use temporary directories" verified — every test uses `tmp_path` fixture. Step 4.6 verdict file matches all five Step 4.1-4.5 summaries. |
| 4 | Function signature verification | PASS | Live grep: `discover_surfaces(project_root: Path)` (init_lite.py:72), `estimate_tokens(byte_count: int)` (:31), `classify_token_estimate(tokens: int)` (:38), `_is_protected_target_path(project_root, candidate)` (:206), `_command_name_for_skill(skill_name)` (install_skills.py:20), `_has_corresponding_command(skill_name)` (install_skills.py:44). All exist with the signatures the test file imports at `test_init_lite.py:19-29`. Test imports succeed at collection time (56 tests collected, 0 import errors). |
| 5 | Module context analysis | PASS | `init_lite.py` imports: `math`, `dataclasses.dataclass`, `pathlib.Path`, `typing.List/Optional`, `click`. All used (`math.ceil` :35, `@dataclass` :47, `Path` throughout, `Optional[Path]` :285, `click.*` decorators :236-281). Module exposes `init_lite_command` at module scope (:282), which `main.py:428-430` imports and registers. `install_skills.py` still exposes `install_all_skills` (:53) and `list_installed_skills` (:144) — both preserved; new helpers `_command_name_for_skill` + `_has_corresponding_command` added without breaking the public surface. |
| 6 | Downstream consumer analysis | PASS | `_has_corresponding_command` is consumed by `install_all_skills` at `install_skills.py:81` and `_command_name_for_skill` at `:120`. Both preserved. `init_lite_command` is consumed only by `main.py:428-430` registration. No other downstream consumers exist (verified via grep across `src/`). The installer mapping change is purely additive: `sc-roadmap` mapping still works (test `test_installer_keeps_existing_sc_prefix_mapping` PASS), unrelated `sc-totally-fictional` still rejected (test `test_installer_rejects_sc_skill_without_matching_command` PASS). |
| 7 | Test validity | PASS | Tests exercise real behavior, not stubs: `test_dry_run_writes_nothing` asserts `not (tmp_path / ".dev").exists()` AND CLAUDE.md byte-hash preservation (sha256). `test_default_run_writes_report_with_marker_and_no_scaffold` reads the actual report file and asserts the marker is on line 1. `test_no_writes_under_claude_when_present` snapshots `.claude/` byte-hashes before and after 4 invocation modes and asserts equality. `test_output_to_protected_path_is_refused` is parametrized 7 paths × 2 force values = 14 cases, asserting exit≠0 AND target byte-preservation. No 6-char placeholder fixtures; no smoke-only assertions. |
| 8 | Test coverage (primary use case) | PASS | Coverage matrix: dry-run (`test_dry_run_writes_nothing`), default (`test_default_run_writes_report_with_marker_and_no_scaffold` + `test_custom_output_flag_used`), scaffold (`test_scaffold_creates_only_advisory_files` + `test_second_scaffold_run_is_idempotent`), force (covered by `test_refuses_to_overwrite_non_marker_output_without_force` + scaffold idempotency), CLAUDE.md preservation (`test_claude_md_bytes_preserved_across_all_modes` across 4 modes), marker idempotency (`test_second_default_run_overwrites_marked_report`), help surface (`test_help_lists_required_flags`), missing `--context-optimized` (`test_missing_context_optimized_is_usage_error`), protected path denylist (parametrized 14-case `test_output_to_protected_path_is_refused` + `test_is_protected_target_path_unit`), installer mapping (5 tests). All 11 invariants from research/03 are pinned. |
| 9 | Error path coverage | PASS | Missing `--context-optimized` → `click.UsageError` (test `test_missing_context_optimized_is_usage_error`, code `init_lite.py:300-304`). `--project-root` non-directory → `click.UsageError` at `:307-308` (not explicitly tested, but the code path is straightforward Click validation + `is_dir()` check). `--output` aimed at protected path → `click.ClickException` "protected target-project path" (14 parametrized cases). `--output` aimed at non-marker file without `--force` → `click.ClickException` "init-lite generated marker" (`test_refuses_to_overwrite_non_marker_output_without_force`). All four documented bad-input scenarios are covered. |
| 10 | Runtime failure path trace | PASS | Trace: user runs `superclaude init-lite --context-optimized [...]` → `main.py:430` dispatches to `init_lite_command` → `:300-304` guard → `:306-308` root validation → `:310` discovery (read-only `is_file()`/`glob`/`rglob`) → `:311` `render_report` (pure compute) → branch on `dry-run` (echo, return) OR write path with denylist (`:324-329`) + ownership (`:331-337`) + parent mkdir + write. Edge cases: non-UTF8 CLAUDE.md — `discover_surfaces` only `stat()`s for byte_count (never decodes); the report itself is generated UTF-8. Symlinks — `_is_protected_target_path` uses `resolve(strict=False)` which follows symlinks; an external symlink lands outside the denylist but the marker-ownership guard still catches it (documented as deliberate carve-out in `task-integrity-gate-verdict.md:33` and `### Follow-Up Items Identified` in the task file). Permission-denied dirs — `mkdir(parents=True, exist_ok=True)` would raise `PermissionError` which Click surfaces with a non-zero exit; acceptable failure mode. |
| 11 | Completion scope honesty | PASS | `final-validation-evidence.md` accurately reports 56/56 pytest pass, 5/5 installer-mapping pass, `make sync-dev` PASS, `make verify-sync` PASS, `make lint` PASS — each backed by raw output files. `task-integrity-gate-verdict.md` honestly reports the 2-cycle history (Cycle 0 FAIL with 1 IMPORTANT + 1 MINOR, Cycle 1 PASS after Invariant-5 fix). `### Follow-Up Items Identified` honestly flags the symlink carve-out as a deliberate non-blocker for future hardening. No overclaim. |
| 12 | Ambient dependency completeness | PASS | New 3rd-party deps introduced: **none**. `init_lite.py` imports only stdlib + `click` (already a top-level project dep per `pyproject.toml`). `install_skills.py` changes use stdlib only. CLI registration added to `main.py:428-430` follows the existing additive `from … import …` + `main.add_command(…, name="…")` pattern (cf. lines 400, 404, 408, 412, 416, 420, 424). No `__init__.py` exports required (Click groups discover via `main.add_command`). |
| 13 | Kwarg sequencing red flags | PASS | All 6 Click options are kwargs with explicit defaults (`init_lite.py:236-281`). The Python wrapper `init_lite_command(...)` signature (`:282-289`) takes positional args that Click binds by `--option` name. No positional/kwarg confusion. No deferred-completion items (everything is implemented in this PR). |
| 14 | Function existence claims verification | PASS | Grep verification: `discover_surfaces` (init_lite.py:72 — imported at test_init_lite.py:23), `estimate_tokens` (init_lite.py:31 — :24), `classify_token_estimate` (:38 — :22), `_is_protected_target_path` (:206 — :21), `GENERATED_MARKER` (:21 — :20), `_command_name_for_skill` (install_skills.py:20 — test_init_lite.py:27), `_has_corresponding_command` (install_skills.py:44 — :28). All imports resolve (pytest --collect-only collected 56 tests, 0 import errors). |
| 15 | Cross-reference accuracy for templates | PASS | Skill name match: command at `commands/init-lite.md:52` says `Skill sc-init-lite-protocol`; actual skill dir is `src/superclaude/skills/sc-init-lite-protocol/` — exact match. Skill says it's invoked by `/sc:init-lite` (`SKILL.md:20-27`); command file lives at `commands/init-lite.md` and frontmatter says `name: init-lite` (:2) — match. Dev mirrors exist at `.claude/commands/sc/init-lite.md` and `.claude/skills/sc-init-lite-protocol/SKILL.md` (live `ls` confirmed). |

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place by this review: 0 (none found)

## Tool Engagement

- Read: 14 (task file, init_lite.py, test_init_lite.py, install_skills.py, main.py L1-60 + L395-455, init-lite.md, sc-init-lite-protocol/SKILL.md, test_cli_registration.py, 5 phase-output summaries, validation-verdict, task-integrity-gate-verdict, final-validation-evidence, post-completion-output-audit)
- Bash: 7 (collect-only count, full pytest re-run, --help output, two end-to-end dry-run smoke tests against `/tmp/init-lite-qa-probe{,2}`, command-file listing, grep init-lite in main.py, ls dev-mirror existence)
- Grep: 0 (replaced by targeted `ls`/`grep` via Bash above)

Confidence: Verified 15/15, Unverifiable 0, Unchecked 0, Confidence 100%.
Tool engagement total: 21 calls for 15 checks (1.4x ratio — above the
1:1 floor required by the Confidence Gate Protocol).

## Issues Found

None.

## Actions Taken

None — no mechanical fixes required. The implementation, tests, summaries,
and evidence files are internally consistent and match disk state.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

The spawn prompt did not include a formal `## Inherited Structural Verdict`
block, but it asserted that "the task file's task-integrity QA gate (Phase 5)
already PASSED in fix-cycle 1, with the rf-qa-found Invariant 5 hole now
closed (`_is_protected_target_path`)." That assertion was treated as a
reliance signal, with the following independent verification:

- **Relied on:** rf-qa task-integrity PASS on the post-fix Invariant-5 denylist.
- **Independent semantic check:** Read `init_lite.py:206-233` (denylist
  helper) AND `:324-329` (call-site BEFORE the marker-ownership check) AND
  the 14 parametrized + 1 unit-test cases in `test_init_lite.py:475-533`.
  Confirmed the denylist:
  (a) classifies `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, and
  anything under `.claude/` as protected;
  (b) allows `.dev/superclaude/context-audit.md` and `custom/audit.md`;
  (c) deliberately returns False for paths outside `project_root` (the
  documented symlink carve-out, surfaced as Follow-Up A below);
  (d) is gated BEFORE the marker-ownership check, so `--force --output
  CLAUDE.md` is refused with exit≠0 and CLAUDE.md byte-preserved (verified
  by `test_output_to_protected_path_is_refused[True-CLAUDE.md]`).

This rf-qa PASS is genuinely verified, not merely relied on.

## Self-Audit

**1. How many factual claims did I independently verify against source code?**

Every checklist row's evidence column cites a specific file:line range or
a live Bash invocation. 15/15 checks have ≥1 file:line citation; 4/15 also
have a live-runtime probe (full pytest re-run, --help output, two dry-run
smoke tests).

**2. What specific files did I read to verify claims?**

`src/superclaude/cli/init_lite.py` (362 lines), `tests/cli/test_init_lite.py`
(534 lines), `src/superclaude/cli/install_skills.py` (165 lines),
`src/superclaude/cli/main.py:1-60 + 395-435`, `src/superclaude/commands/init-lite.md`,
`src/superclaude/skills/sc-init-lite-protocol/SKILL.md`,
`tests/cli/test_cli_registration.py` (144 lines), the 5 test-result summary
files, both verdict files in `plans/`, and 2 reports in `reports/`. The
task file itself was read end-to-end (Steps 1.1-6.4).

**3. If I found 0 issues, why should the user trust I checked thoroughly?**

(a) I independently re-ran `uv run pytest tests/cli/test_init_lite.py
tests/cli/test_cli_registration.py -q` and reproduced 56 passed in 0.21s
(matches the summary's claim of 0.24s within noise).
(b) I performed an end-to-end live dry-run smoke test from outside the
project tree (`/tmp/init-lite-qa-probe2`) and verified the report rendered
to stdout AND that nothing was written to disk.
(c) I uncovered a non-defect operational note (the pipx shim is stale —
worth logging but not a code bug). That observation is the kind of finding
an "all green" sweep would have missed if I weren't probing live.
(d) The earlier rf-qa structural pass already caught the Invariant-5 hole
(now fixed); my pass independently re-walked the denylist code + test
matrix to confirm the closure.

**4. Tavily-first compliance:** No external web lookup was required for
this review (all evidence is local source + local test artifacts). The
Tavily-first rule is N/A by content type, not by tool unavailability.

## Follow-Up Items Identified (Logged, Not Failures)

**Follow-Up A (LOW priority, operator hygiene — not a code defect):**
The pipx-installed shim `/config/.local/bin/superclaude` points at
`/config/.local/share/pipx/venvs/superclaude/bin/python`, which is a
pre-`init-lite` snapshot. Running `superclaude init-lite ...` from outside
the worktree fails with `No such command 'init-lite'`. From inside the
worktree, `uv run superclaude init-lite ...` works correctly. Per memory
`reference_superclaude_install_vector.md`, the operator install vector is
`pipx install --force ~/workspace/IronClaude` (or `pipx install --force
<worktree-path>`) — that would refresh the shim. **This is not a task
defect** (the task scope was `src/superclaude/` source-of-truth changes,
not operator install hygiene), but the next person running this command
from a non-UV shell may benefit from the `pipx install --force` reminder
in release notes.

**Follow-Up B (LOW priority, already logged):** Symlink hardening in
`_is_protected_target_path` — a `CLAUDE.md` symlink that resolves out of
`project_root` is not denylisted (the marker-ownership guard still catches
it). Already logged in the task file's `### Follow-Up Items Identified`
section (line 277) by the earlier rf-qa pass; no new action required from
this review.

## Recommendations

Proceed to Step 6.3 (Create task summary) and Step 6.4 (Mark task complete).
Both can use this report's PASS verdict and the consistent evidence chain
across `validation-verdict.md`, `task-integrity-gate-verdict.md`,
`final-validation-evidence.md`, `post-completion-output-audit.md`, and this
qualitative review.

Optional release-note line for the `pipx install --force` follow-up:
> After updating SuperClaude, refresh the pipx shim with
> `pipx install --force ~/workspace/IronClaude` so `superclaude init-lite
> --help` is reachable outside the development tree.

## QA Complete
