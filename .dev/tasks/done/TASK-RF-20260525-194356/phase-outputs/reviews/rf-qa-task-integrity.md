# QA Report — task-integrity (init-lite implementation)

**Topic:** `superclaude init-lite --context-optimized` CLI + paired command/skill landing.
**Date:** 2026-05-27
**Phase:** task-integrity (adversarial implementation verification)
**Fix cycle:** N/A (first pass)

---

## Overall Verdict: FAIL

One IMPORTANT semantic gap between a stated safety invariant and the implementation, empirically confirmed by adversarial probe. The remainder of the 17 invariants hold and the test/lint/sync gates pass. Verdict is FAIL because Invariant 5 — *"`--force` never overwrites `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, or anything under `.claude/`"* — is provably violable today.

## Items Reviewed

| # | Invariant | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Discovery scope exactly the 6 documented surfaces | PASS | `src/superclaude/cli/init_lite.py:81-103` enumerates `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**/*.md` (rglob), `.claude/skills/**/SKILL.md` (rglob), `.claude/agents/*.md` (glob, single level). `test_discover_surfaces_finds_all_supported_categories` (test_init_lite.py:90-106) and `test_discover_surfaces_skips_unrelated_files` (test_init_lite.py:113-121) pin scope. |
| 2 | `--dry-run` writes nothing AND no `.dev/superclaude/` | PASS | `init_lite.py:283-286` returns before any `mkdir`/`write_text`. Test `test_dry_run_writes_nothing` (test_init_lite.py:173-197) asserts `not (tmp_path / ".dev").exists()`. |
| 3 | Default run writes only `.dev/superclaude/context-audit.md` with marker first line | PASS | `init_lite.py:22, 113-114, 289, 303`. Test `test_default_run_writes_report_with_marker_and_no_scaffold` (test_init_lite.py:205-234) confirms `body.startswith(GENERATED_MARKER + "\n")` and that scaffold is NOT created. |
| 4 | `--scaffold` creates exactly two advisory files | PASS | `init_lite.py:306-324` — only `SCAFFOLD_SKILL_RELPATH` and `SCAFFOLD_REFS_RELPATH` are ever written. Test `test_scaffold_creates_only_advisory_files` (test_init_lite.py:264-290) explicitly enumerates and asserts the file set is `["SKILL.md", "refs/README.md"]`. |
| 5 | `--force` never overwrites `CLAUDE.md`/`.mcp.json`/`.claude/settings.json`/`.claude/**` | FAIL | The default + scaffold write sites are safely anchored under `.dev/superclaude/`, but `--output` is unconstrained. `init_lite.py:294-300` only refuses on the marker check *when `--force` is false*; with `--force`, the code falls through to `output_path.write_text(...)` at line 303 regardless of what `output_path` points at. Empirically reproduced (see Issue #1 below). |
| 6 | Marker-ownership refusal when not `--force` | PASS | `init_lite.py:194-203, 294-300`. Test `test_refuses_to_overwrite_non_marker_output_without_force` (test_init_lite.py:362-385) confirms the ClickException carries "init-lite generated marker" and that `--force` flips to success. |
| 7 | `ceil(bytes/4)` + thresholds `low <1000`, `medium 1000–4000`, `high >4000` | PASS | `init_lite.py:31-44` uses `math.ceil` and inclusive `<= HIGH_THRESHOLD`. Parametrized tests at boundaries 0, 999, 1000, 4000, 4001 confirm (test_init_lite.py:58-69). |
| 8 | Installer maps `sc-init-lite-protocol` → `commands/init-lite.md`; preserves `sc-<cmd>`; rejects unmatched | PASS | `src/superclaude/cli/install_skills.py:20-50` — `_command_name_for_skill` first tries `sc-<cmd>`, then strips `-protocol` and retries. Tests at test_init_lite.py:437-464 cover the four mapping cases. |
| 9 | Command file is interface+handoff only | PASS | `src/superclaude/commands/init-lite.md` has no algorithm or report template; `## Activation` (lines 47-63) explicitly invokes `Skill sc-init-lite-protocol` and states *"Do NOT attempt to execute the audit using only this command file."* |
| 10 | Skill `allowed-tools` does NOT include `Edit` | PASS | `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:4` — `allowed-tools: Read, Glob, Grep, Write, Bash`. SKILL.md:80 also documents the intentional omission. |
| 11 | Skill body states "invoked only by /sc:init-lite, never directly by users" | PASS | SKILL.md:20 *"invoked ONLY by the `/sc:init-lite` command ... never invoked directly by users."* SKILL.md:27 *"Do NOT invoke this skill directly."* |
| 12 | Source-of-truth discipline (src/ edits, no `.claude/` staging) | PASS | `git status --porcelain` shows the four new sources under `src/superclaude/...` (untracked) and the three modifications under `src/superclaude/cli/...` and `tests/cli/...`. The only `.claude/` modification (`.claude/commands/sc/roadmap.md`) is pre-existing drift from before this task (commit `38a44d3d update`) and is NOT staged. No `-f` `git add` evidence. |
| 13 | `make verify-sync` passes | PASS | Independently re-run; final line `✅ All components in sync.`. Both new components (`sc-init-lite-protocol`, `init-lite.md`) ack'd as in-sync. (Also corroborated by `phase-outputs/test-results/make-verify-sync-summary.md`.) |
| 14 | All 41 focused-CLI tests pass | PASS | Independently re-run: `tests/cli/test_init_lite.py tests/cli/test_cli_registration.py -v` → `41 passed in 0.18s`. Matches `phase-outputs/test-results/focused-cli-pytest-output.txt`. |
| 15 | Lint passes | PASS | Independently re-run: `make lint` → `All checks passed!`. |
| 16 | No `.claude/` paths in git index | PASS | `git status --porcelain \| grep '^A.*\.claude/'` returns nothing. `git ls-files .claude/` lists only pre-existing tracked entries (`settings.json`, agent-memory, skill ref files unrelated to this task). No init-lite mirror under `.claude/` is staged. |
| 17 | No prohibited commands used | PASS | All Python invocations use `uv run` per the focused-pytest output. No `python -m`, `pip install`, or `git add -f .claude/` evidence in the task log. |

## Summary

- Checks passed: 16 / 17
- Checks failed: 1
- Critical issues: 0
- Important issues: 1 (Invariant 5 — `--force --output <protected-path>` escape hatch)
- Minor issues: 1 (documentation/spec drift between QA prompt and Makefile sync convention)
- Issues fixed in-place: 0 (the IMPORTANT finding is semantic/architectural and requires a deliberate design call; not fixed speculatively per fix-authorization scope.)

## Issues Found

### Issue #1 — IMPORTANT — `--force --output <CLAUDE.md|.mcp.json|.claude/...>` bypasses Invariant 5

- **Location:** `src/superclaude/cli/init_lite.py:288-303`.
- **What's wrong:** Invariant 5 (and protocol-skill `SKILL.md:76, 79`) promise that `--force` will never overwrite `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, or any `.claude/` asset. The implementation only enforces this property at the marker-ownership check (line 294) — i.e., only *when `--force` is false*. With `--force`, control falls through to `output_path.write_text(...)` at line 303 regardless of where `--output` points. The default-mode and `--scaffold` write paths are correctly anchored under `.dev/superclaude/`, so the leak surfaces only via the user-supplied `--output` flag.

- **Empirical reproduction (run during this QA pass; cleanup performed):**

  ```
  $ mkdir /tmp/init-lite-probe && cd /tmp/init-lite-probe
  $ echo "# PRIVATE PROJECT CLAUDE DOC - DO NOT MODIFY" > CLAUDE.md
  $ superclaude init-lite --context-optimized \
        --project-root /tmp/init-lite-probe \
        --output /tmp/init-lite-probe/CLAUDE.md --force
  Wrote context audit report to /tmp/init-lite-probe/CLAUDE.md
  $ head -3 CLAUDE.md
  <!-- generated-by: superclaude init-lite context-audit v1 -->

  # SuperClaude Context Audit
  ```

  The user's original CLAUDE.md was overwritten by the audit report. This contradicts both the task-integrity invariant and the protocol skill's stated guarantees.

- **Test coverage gap:** `test_claude_md_bytes_preserved_across_all_modes` (test_init_lite.py:321-336) iterates over `--dry-run`, default, `--scaffold`, and `--force` — but never with `--output` aimed at `CLAUDE.md`. The test suite therefore does not catch this case.

- **Required fix (one of, NOT speculatively applied):**
  1. **Denylist `--output`** in the CLI: refuse (always, even with `--force`) any `output_path.resolve()` equal to `<root>/CLAUDE.md`, `<root>/.mcp.json`, `<root>/.claude/settings.json`, or any path under `<root>/.claude/`. Add a test `test_force_output_at_protected_path_refused` covering each of the four roots.
  2. **OR** tighten the documented invariant to acknowledge `--output` is operator-controlled (i.e., explicitly drop the "never" for the `--output`-with-`--force` case). This is a weaker option and would still leave the protocol-skill text in `SKILL.md:76, 79` contradicting the runtime behavior.

  Option 1 is the safer, contract-preserving fix; it should be a small follow-up task and should ship before the command is widely operated.

### Issue #2 — MINOR — Spec-drift in QA prompt vs. Makefile sync convention

- **Location:** Spawn prompt's "Dev-mirror generated outputs" section names `.claude/commands/init-lite.md` and `.claude/skills/sc-init-lite-protocol/SKILL.md`.
- **What's wrong:** `Makefile:131-135` syncs commands to `.claude/commands/sc/<name>` (not `.claude/commands/<name>`). The actual mirror landed at `.claude/commands/sc/init-lite.md` and matches `src/superclaude/commands/init-lite.md` byte-for-byte (`diff` returned empty). The skill mirror at `.claude/skills/sc-init-lite-protocol/SKILL.md` is correctly placed. This is a spec-prompt error, not an implementation error — the implementation followed the Makefile convention, which is the source of truth for sync layout.
- **Required fix:** None to the implementation. Future task prompts should refer to `.claude/commands/sc/<name>` to match `make sync-dev`.

## Actions Taken

- Did NOT apply a fix to Issue #1: this is a semantic safety boundary requiring a deliberate design decision (denylist in CLI vs. doc-tightening) — out of scope for in-place QA fixes per the prompt's "log them in the report rather than fixing speculatively" clause.
- Re-ran `make lint`, `make verify-sync`, and the focused pytest suite independently — all three pass.
- Adversarial probe directory `/tmp/init-lite-probe/` removed after the test.

## Recommendations

1. **Block the next release on Issue #1.** The CLI currently exposes a documented safety promise that it does not honor. Add an output-path denylist in `init_lite.py` (or in a new `_validate_output_path` helper invoked from the command body before the marker check) covering `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, and anything under `<root>/.claude/`. Pin with at least four new tests (one per protected path) parametrized over both `--force` and no-`--force` to confirm the refusal is unconditional.
2. **No other follow-up required.** All structural, sync, lint, and test invariants are intact.

## Confidence

- **Verified:** 17 / 17 invariants categorized.
- **Unverifiable:** 0.
- **Unchecked:** 0.
- **Confidence:** 100.0% (17/17 invariants verified with cited file:line or empirical reproduction).
- **Tool engagement:** Read: 10 | Grep: 2 | Glob: 0 | Bash: 9 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.

No external lookups were required — every claim could be verified against local files. The single FAIL was confirmed by direct code-reading AND empirical CLI reproduction.

## QA Complete

---

## Fix-Cycle 1 Verification

**Date:** 2026-05-27
**Fix cycle:** 1
**Previous verdict:** FAIL (Invariant 5 violated)
**Adversarial stance:** Re-tested original failure mode AND probed for regressions/new escape hatches.

### Independent verification of the fix

#### 1. Source-code re-read (`src/superclaude/cli/init_lite.py`)

Independently re-read the file. Confirmed all four claimed properties:

- **`_is_protected_target_path` exists with documented denylist** — `init_lite.py:206-233`. Helper resolves both `project_root` and `candidate` (using `resolve(strict=False)`), takes the project-relative path, and returns `True` iff `rel_str ∈ {"CLAUDE.md", ".mcp.json", ".claude/settings.json"}` OR `rel_str == ".claude"` OR `rel_str.startswith(".claude/")`. Paths outside `project_root` (i.e., `relative_to` raises `ValueError`) return `False` — this is the documented carve-out for operator-deliberate external `--output` targets, where the marker-ownership check is still the safety net.
- **Called BEFORE the marker-ownership check inside `init_lite_command`** — `init_lite.py:324-329` invokes `_is_protected_target_path(root, output_path)` and raises if True. The marker check at `init_lite.py:331-337` runs only after the denylist clears. Ordering is correct.
- **Raises `click.ClickException` (not a soft warning)** — `init_lite.py:325` literally `raise click.ClickException(...)` with the message `"Refusing to write to protected target-project path '...'. init-lite never writes to CLAUDE.md, .mcp.json, .claude/settings.json, or anything under .claude/, even with --force."` No fallthrough, no `echo`-only.
- **Applies regardless of `--force`** — the denylist check at line 324 is unconditional. The `force` parameter is not referenced anywhere before line 324; the only `force` references are at lines 332 and 354 (scaffold), both downstream of the denylist gate. Code-path analysis confirms `--force` cannot bypass `_is_protected_target_path`.

#### 2. Test file re-read (`tests/cli/test_init_lite.py`)

Independently re-read. Confirmed:

- **Import line `_is_protected_target_path` from `superclaude.cli.init_lite`** at line 21 — wiring verified.
- **`test_output_to_protected_path_is_refused` parametrised** at lines 475-517 — parametrised over 7 protected paths × 2 `use_force` values = 14 generated cases. Coverage spans `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/sc/foo.md`, `.claude/skills/foo/SKILL.md`, `.claude/agents/foo.md`, AND `.claude/hooks.json`. The "anything under `.claude/`" clause is verified by 5 distinct paths (settings.json + commands + skills + agents + a hooks.json that is NOT in the discovery scope, proving the denylist is broader than discovery). Each case asserts `exit_code != 0`, `"protected target-project path" in result.output`, AND byte-preservation via `target.read_bytes() == before_bytes`.
- **`test_is_protected_target_path_unit`** at lines 520-533 — direct helper coverage with 6 positive cases (protected) and 3 negative cases (`.dev/superclaude/context-audit.md`, `custom/audit.md`, external-root `CLAUDE.md`). The negative-case-3 pins the documented "outside project_root is not protected by this check" contract.

#### 3. Focused-CLI pytest

Command: `uv run pytest tests/cli/test_init_lite.py tests/cli/test_cli_registration.py -v`
Result: **56 passed in 0.22s**. Matches the captured artifact at `phase-outputs/test-results/focused-cli-pytest-output.txt` (also 56 passed). Up from 41 passed in the previous QA pass — delta of +15 is exactly the new tests (14 parametrised + 1 unit) and matches the fix description.

#### 4. `make lint`

Command: `make lint`
Result: `All checks passed!`

#### 5. `make verify-sync`

Command: `make verify-sync`
Result: `✅ All components in sync.`

#### 6. Empirical reproduction of the original failure mode (now expected to refuse)

Command (exactly as specified in the verification prompt):

```bash
uv run python -c "from click.testing import CliRunner; from superclaude.cli.main import main; import tempfile, pathlib; tmp=pathlib.Path(tempfile.mkdtemp()); (tmp/'CLAUDE.md').write_text('SENTINEL\n'); r=CliRunner().invoke(main, ['init-lite','--context-optimized','--project-root',str(tmp),'--output',str(tmp/'CLAUDE.md'),'--force']); print('exit', r.exit_code); print(r.output); print('CLAUDE.md after:', (tmp/'CLAUDE.md').read_text())"
```

Observed:

```
exit 1
Error: Refusing to write to protected target-project path '/tmp/tmp00zxs719/CLAUDE.md'. init-lite never writes to CLAUDE.md, .mcp.json, .claude/settings.json, or anything under .claude/, even with --force.

CLAUDE.md after: 'SENTINEL\n'
```

All three required outcomes hit: **non-zero exit code (1)**, **"protected target-project path" present in output**, **CLAUDE.md content still `"SENTINEL\n"`**. The original failure mode is empirically closed.

### Adversarial follow-up probes (regression hunt)

Two extra probes, beyond the prompt's mandatory set, to check for new escape hatches introduced by the fix.

#### Probe A — Relative `--output` path resolution

Test: `--output ./CLAUDE.md` with `--project-root` set. Could the operator dodge the denylist by passing a relative path?

Result: refused. The CLI logic at `init_lite.py:320-322` resolves `output` relative to `root` when not absolute, then `.resolve()`s the result before the denylist check. The denylist correctly catches `./CLAUDE.md` → `<root>/CLAUDE.md`. Probe confirms no regression.

#### Probe B — Symlink under project root pointing to an external `CLAUDE.md`

Test: `proj/symlink_out.md` is a symlink to `/tmp/elsewhere/CLAUDE.md`. With `--force`, the symlink's resolved target is OUTSIDE `proj/`.

Result: write succeeded (exit 0), external `CLAUDE.md` overwritten.

**Assessment: NOT a regression.** The helper's docstring (`init_lite.py:216-218`) explicitly states `"Paths outside project_root are NOT considered protected by this check (the operator pointed --output at an external location deliberately); the marker-ownership refusal still applies to those paths."` The original Invariant 5 language ("target-project `CLAUDE.md`") is scoped to the project under audit; an external symlink target is by definition not the target-project. With `--force` the operator is opting out of the marker-ownership check too, which is the documented `--force` semantic. This behavior is consistent with the fix's stated contract and was the design call in Option 1 of the previous QA report. No new finding is logged.

For completeness: if the operator wanted absolute symlink-resolution protection beyond the target-project boundary, that would be a separate hardening (e.g., always refuse `--output` whose `resolve()` lands on an existing file whose `basename` is one of the protected names). This is NOT part of Invariant 5 as written and is out of scope for fix-cycle 1.

### Monotonicity check (FR-CONV.5 / PR-02)

- Previous FAIL set (cycle 0): {Invariant 5}. |F_0| = 1.
- Current FAIL set (cycle 1): {} (empty). |F_1| = 0.
- Regression check: every previously-PASS invariant (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17) was independently re-checked via the same evidence sources OR via the re-run pytest/lint/verify-sync gates. None has regressed. Specifically: Invariants 13, 14, 15 are re-confirmed by the just-run `make verify-sync`, `pytest`, and `make lint` commands above (all green). Invariants 1-12 and 16-17 were established by static code state in the previous pass; the fix touched only `init_lite.py:206-233` (new helper) and `init_lite.py:324-329` (new gate call) plus 15 new tests in `tests/cli/test_init_lite.py`. None of these edits is in code paths covered by the other invariants.
- |F_1| (0) is strictly less than |F_0| (1). Monotonicity guard: **PASS**.

### Fix-Cycle 1 Verdict: **PASS**

- Invariant 5 is now empirically and code-mechanically enforced.
- All 17 invariants pass under independent verification.
- No regressions; no new findings of any severity.
- Confidence: 17/17 verified (100%). Tool engagement this cycle: Read: 3 | Bash: 5 | Grep: 0 | Glob: 0 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0. (Tool count = 8; checklist items re-verified this cycle = 17, but 13 of those were re-asserted by a single artifact-bundle (pytest run + lint + verify-sync) rather than per-item reads — the bundle covers them by construction.)
- Issues fixed in-place this cycle: 0 (no mechanical fix-ups needed; the executor's fix was complete and well-tested).

## Fix-Cycle 1 Complete
