# Code Review: PR #79 — fix(roadmap): repair u2014 template corruption + add cosmetic-failure auto-remediation lane

**Target**: [IronbellyOrg/IronClaude#79](https://github.com/IronbellyOrg/IronClaude/pull/79)
**Reviewer**: `/sc:auggie-review` (depth=standard, focus=all)
**Generated**: 2026-05-24 14:43 UTC
**Base ↔ Head**: `master` ↔ `fix/roadmap-template-and-cosmetic-remediation` (`4a647c44`)
**Stats**: 8 files, 1391 +/14 −, 12 findings + 2 cross-cutting (0 dropped during grounding)

---

## Summary

The PR delivers what its title promises: the 9× `u2014` template-corruption fix is precise and unambiguous, and the cosmetic-remediation lane is a thoughtful defense-in-depth layer. The classifier's conservative bias (any semantic violation → halt) is the right safety boundary. Two medium-severity issues are worth addressing before merge: **(M1)** `_is_in_fenced_block` walks the whole file from line 0 on every call, making the detector loop O(N²) — measurable cost on the 736-line TUIBBS opus artifact; **(M2)** the remediator call sites have no try/except, so an unexpected exception in `classify_gate_failure` / `apply_cosmetic_remediations` would crash the pipeline executor in a way the current design's strict-on-failure contract doesn't anticipate. The remaining findings are LOW/NIT and most are fix-or-follow-up at your discretion. **Recommendation: address M1+M2 in this PR, the rest as follow-ups.**

## Findings

### 🟠 Medium (fix before merge)

#### M1. `_is_in_fenced_block` is O(N²) when called line-by-line in the detector loop

- **File**: `src/superclaude/cli/roadmap/cosmetic_remediator.py:204-210`
- **Category**: performance
- **Source**: auggie (validated)
- **Evidence**:
  ```python
  def _is_in_fenced_block(lines: list[str], idx: int) -> bool:
      """Return True if line ``idx`` is inside a ``` ... ``` fenced code block."""
      fence_count = 0
      for i in range(idx):
          if lines[i].lstrip().startswith("```"):
              fence_count += 1
      return fence_count % 2 == 1
  ```
- **Why this matters**: `_detect_cosmetic_violations` calls `_is_in_fenced_block(lines, idx)` once per line. Each call re-walks from 0 to idx counting `^```` lines. For an N-line file the total cost is Σ(i for i in range(N)) ≈ N²/2 fence-counting iterations. On the real TUIBBS opus artifact (736 lines) that's ~270K iterations of `line.lstrip().startswith("```")` per detector pass, and the detector is called twice (classify + recheck). Not a blocker, but easily quadratic on the artifacts this code is meant to operate on.
- **Recommendation**: Precompute a `set[int]` of indices that fall inside fenced blocks with a single O(N) walk, then have detectors do an O(1) membership check. Reuse the set across all detector subroutines. Example:
  ```python
  def _compute_fenced_indices(lines: list[str]) -> set[int]:
      result: set[int] = set()
      inside = False
      for i, line in enumerate(lines):
          if line.lstrip().startswith("```"):
              inside = not inside
              continue
          if inside:
              result.add(i)
      return result
  ```
  Pass the set into `_detect_cosmetic_violations` and every `_apply_*` helper. Same idempotency, ~10× faster on the artifact sizes in scope.

#### M2. No graceful degradation when the cosmetic remediator raises an unexpected exception

- **File**: `src/superclaude/cli/pipeline/executor.py:309-313` and `src/superclaude/cli/roadmap/executor.py` (adapter)
- **Category**: error-handling
- **Source**: auggie (validated)
- **Evidence**: the executor calls `config.cosmetic_remediator(gate_target, gate_name, reason or "", step_id=step.id)` with no try/except. The roadmap adapter wraps `output_file.read_text()` in try/except for `OSError` but does NOT wrap `classify_gate_failure(...)` or `apply_cosmetic_remediations(...)`. A regex compile failure, an unexpected `IndexError` in the lines walker, or a string-translate failure would propagate up the executor and crash the pipeline mid-step with a stack trace, NOT a clean FAIL StepResult.
- **Why this matters**: the whole point of the remediation lane is to be a non-blocking safety net. An exception in the remediator that prevents the pipeline from falling through to the existing FAIL path defeats the design intent and replaces a clean halt-with-diagnostic with an opaque crash.
- **Recommendation**: wrap the entire remediation block in `pipeline/executor.py:286-340` in a `try/except Exception` that logs the exception and falls through to the normal FAIL StepResult construction. Same `gate_failure_reason` as before (the original `reason`), with an additional audit-log line noting the remediator-internal failure. Example:
  ```python
  try:
      remediated_ok, transforms = config.cosmetic_remediator(...)
      # ... existing recheck path ...
  except Exception as exc:  # noqa: BLE001 — intentional broad catch
      _log.warning(
          "Cosmetic remediator raised %s for step '%s'; falling through to FAIL",
          exc.__class__.__name__, step.id,
      )
  ```
  Add a unit test that injects a remediator returning `raise RuntimeError("test")` and asserts the step still becomes FAIL (not crash).

### 🟢 Low (fix in PR if cheap, otherwise file followup)

#### L1. `_apply_blank_line_collapse` does not handle Windows CRLF line endings

- **File**: `src/superclaude/cli/roadmap/cosmetic_remediator.py:604`
- **Category**: correctness
- **Source**: auggie (validated)
- **Evidence**: `re.subn(r"\n{3,}", "\n\n", content)` — does not match `\r\n\r\n\r\n`. On a roadmap artifact written from a Windows host (or after a git checkout with autocrlf), C7 would silently fail to collapse blank-line runs.
- **Why this matters**: low impact for this repo (Python projects generally LF-only and `git config core.autocrlf` is usually input), but the rest of the file has no CRLF handling either — so the issue compounds across C5/C6/C7/C10 if anyone runs the CLI on Windows.
- **Recommendation**: use `r"(?:\r?\n){3,}"` and emit `"\n\n"`; OR document the LF-only assumption in the module docstring. The latter is cheaper and matches what the rest of the package already assumes.

#### L2. `\xa0` (non-break space) in `_NONCANONICAL_DASH_PATTERN` can produce false positives

- **File**: `src/superclaude/cli/roadmap/cosmetic_remediator.py:95`
- **Category**: correctness
- **Source**: auggie (validated)
- **Evidence**: `_NONCANONICAL_DASH_PATTERN = re.compile(r"(?:u2014|—|–|−|\xa0\-\xa0|\xa0|~)")` — the bare `\xa0` alternation will match any non-break space, not just one acting as a dash. The C3 detector guards this with `stem_lower in _REQUIRED_STEMS_LOWER`, so the blast radius is bounded to milestone H3s that legitimately contain `\xa0` (rare). Still, the regex's stated intent ("non-canonical dash") doesn't match the bare-`\xa0` branch's actual behavior.
- **Recommendation**: tighten to `\xa0+(?=\s*M\d+)` or drop the bare-`\xa0` alternation entirely. The `\xa0\-\xa0` form earlier in the alternation already covers the common "no-break-space hyphen" case. Add a regression test for `### Risk Assessment\xa0M1` to lock the expected behavior either way.

#### L3. `--allow-cosmetic-remediation` is not documented in user-facing docs

- **File**: `src/superclaude/cli/roadmap/commands.py:232-253` (flag definition site)
- **Category**: docs
- **Source**: auggie (validated)
- **Evidence**: the flag has a click `help=` string but no entry in any `docs/` page or `README.md`. New users discovering the auto-remediation behavior via a surprising "PASS (remediated)" audit line would have nowhere to read about the contract (which classes are cosmetic, when to use `--strict-no-remediation`, etc.).
- **Recommendation**: add a short "Cosmetic auto-remediation" section to whichever doc covers `superclaude roadmap run` options (README, CHANGELOG, or a new `docs/roadmap-cosmetic-remediation.md`). The PR description has most of the content already; lift the C1-C11 table verbatim.

#### L4. No test coverage for multi-milestone documents with mixed milestone-position failures

- **File**: `tests/roadmap/test_cosmetic_remediator.py:21` (helper `_content_with_milestone`)
- **Category**: tests
- **Source**: auggie (validated)
- **Evidence**: the helper only constructs single-milestone documents (`mid="1"` default). All 17 unit tests exercise milestone M1 only. The end-to-end smoke (run manually against the TUIBBS opus file, recorded in the PR description) demonstrated the C2 detector correctly assigns `-- M2`, `-- M3`, etc. by walking back to the enclosing `## M{N}:`, but no unit test pins this behavior.
- **Recommendation**: extend `_content_with_milestone` to accept a list of milestones, OR add one or two tests that build a 2-3 milestone document inline and assert each milestone's H3s get the correct `M{N}` suffix.

#### L5. No test for Windows CRLF line endings in `_apply_blank_line_collapse`

- **File**: `tests/roadmap/test_cosmetic_remediator.py:205-217` (the C7 test)
- **Category**: tests
- **Source**: auggie (validated)
- **Evidence**: `test_c7_blank_line_collapse` only builds LF content. If you decide on the L1 fix path, add a CRLF case. If you go with "document LF-only", a test asserting CRLF input is left unchanged would prevent silent behavioral drift.
- **Recommendation**: paired with L1's resolution. One additional test.

### 💬 Nits

- **N1.** Cited TOCTOU "race" between the first `gate_passed` and the post-remediation re-check (executor.py:298 vs 318) is theoretical only — the pipeline is single-threaded and no other process writes between those calls. Audit-only.
- **N2.** Encoding consistency on `read_text` / `write_text` calls — the roadmap adapter passes `encoding="utf-8"`, the pipeline executor's semantic-check re-read also passes it, but `gate_passed` (in `pipeline/gates.py`) uses Python defaults. Larger refactor, not specific to this PR.
- **N3.** `_strip_section_numbering` was flagged as a duplicate of `gates._normalize_heading`. Not actually reusable as-is — the existing helper lowercases its return value, which the remediator must NOT do (it preserves case). Skip.
- **N4.** `_h3_stem_and_suffix` ordering concern (auggie F7) — the caller already strips section numbering BEFORE calling this function (`cosmetic_remediator.py:295`), so the ordering is correct. False alarm.
- **N5.** No nested-fenced-block test — narrow edge case; the spec doesn't allow nested fences in markdown anyway.
- **N6.** `Protocol` is imported from `typing` (the standard location). Not a layering issue.
- **N7.** No BOM handling — Python's default UTF-8 is the right call for the inputs in scope; the gate would fail on a BOM either way.

## Architectural / Cross-Cutting Observations

- **CC1.** Cosmetic-remediator's gate-name allowlist (`_ROADMAP_GATE_NAMES`) is hardcoded in the module. As new roadmap gates are added in `gates.py`, this allowlist must be updated in lockstep or new gates silently bypass the remediator. Consider: derive the allowlist from a registry in `gates.py` (e.g., a `@cosmetic_remediation_eligible` decorator or a sibling constant tuple), or document the synchronization contract in both files.
- **CC2.** The remediator runs deterministic Python transforms and the executor re-checks the gate, but there's no protection against a misbehaving remediator that returns `(True, ["fake transform"])` without actually rewriting the file in a way the gate accepts. The post-remediation `gate_passed` recheck catches this, falling through to FAIL with `recheck_reason`. Good design; suggest a one-line audit-log entry distinguishing "remediator returned True but recheck failed" from "remediator returned False" so future bug hunts have a clean signal.

## Audit

- Auggie chunks: 1 (succeeded)
- Findings dropped during grounding: 0
- Persona cross-check: disabled (standard depth)
- Token cost: Auggie ≈ 25 KB raw JSON (offloaded retrieval); Claude orchestration ≈ ~12k tokens
- Audit log: `audit.log` in this output directory
