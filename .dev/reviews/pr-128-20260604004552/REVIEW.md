# Code Review: PR #128 — `feat(cli): add superclaude init-lite --context-optimized`

**Target**: PR #128 (`IronbellyOrg/IronClaude`)
**Reviewer**: /sc:auggie-review (depth=standard, focus=all)
**Generated**: 2026-06-04 00:50 UTC
**Source PR**: https://github.com/IronbellyOrg/IronClaude/pull/128
**Base ↔ Head**: `master` ↔ `feat/init-lite` (head `f2d274d0`)
**Stats**: 15 files, ~1383 diff lines, 6 findings reported (2 dropped/folded during grounding)

---

## Summary

**Verdict: 🟢 Approve with comments** (0 critical, 0 high, 1 medium, 4 low, 1 nit).

`init-lite` is a clean, well-tested, safety-conscious feature. The static safety gates are real and enforced in code: `_is_protected_context_path` (init_lite.py:199) resolves symlinks before comparison, so `CLAUDE.md` / `.mcp.json` / `.claude/**` are genuinely unwritable under every flag; `--dry-run` returns before any write; `--force` is correctly scoped to init-lite-owned `.dev/superclaude/` targets via `_is_init_lite_owned` (init_lite.py:114). The test suite (17 tests) exercises most invariants directly.

The one finding worth acting on before merge is **non-atomic file writes** (M1): the new code uses bare `Path.write_text()` where the rest of the repo uses a tempfile + `os.replace()` convention. This is both a consistency gap and a (narrow, local-only) TOCTOU symlink-swap window. The remaining items are Low/Nit polish and test-hardening that can land in this PR or a follow-up.

> Note on threat model: this is a single-user local dev CLI operating on the operator's own working tree. The security-flavored findings all require an attacker who *already* has write access to your project filesystem; they are defense-in-depth, not externally-exploitable holes. Graded accordingly.

## Findings

### 🟡 Medium (fix in this PR if cheap, otherwise follow-up)

#### M1. Non-atomic `write_text` diverges from the repo's atomic-write convention and opens a TOCTOU window
- **File**: `src/superclaude/cli/init_lite.py:242` (and `:257` in `_write_scaffold`)
- **Category**: architecture / security (latent)
- **Source**: auggie (folds Auggie finding #1 + cross-cutting #1)
- **Evidence**:
  ```python
  out_path.parent.mkdir(parents=True, exist_ok=True)
  out_path.write_text(content, encoding="utf-8")   # line 242
  ```
- **Why this matters**: The repo has an established atomic-write pattern used by every other module that writes files — `install_hooks.py:433` (`_atomic_write_json`: tempfile + `os.replace`), `roadmap/executor.py:585,603` (`os.replace`). `init_lite.py` rolls its own direct `write_text`. Beyond inconsistency, this opens a TOCTOU: `_write_report` checks `out_path.exists()` / reads the marker at lines 230–231, then writes at line 242. Between those two points an attacker with local FS write access could replace `out_path` with a symlink to a protected file; `write_text` follows the symlink and writes through it. `os.replace` onto the path would instead atomically replace the *link itself*, closing the window.
- **Recommendation**: Add a small `_atomic_write(path: Path, content: str)` helper (tempfile in the same dir + `os.replace`), and use it in both `_write_report` (line 242) and `_write_scaffold` (line 257). This unifies with the repo convention and removes the TOCTOU.
- **Cross-refs**: `src/superclaude/cli/install_hooks.py:433`, `src/superclaude/cli/roadmap/executor.py:585`

### 🟢 Low (nice-to-have)

#### L1. Surface discovery follows symlinks (no `is_symlink` guard)
- **File**: `src/superclaude/cli/init_lite.py:66` (`_add_surface`, reached from the `rglob`/`glob` loops at 98–108)
- **Category**: security (latent), read-only
- **Why this matters**: `_add_surface` gates on `path.is_file()`, which follows symlinks. A symlink planted at e.g. `.claude/skills/evil/SKILL.md → /etc/passwd` would be `stat()`-ed and its **size** recorded in the report (content is never read, only `st_size`). Minor information disclosure, and only if an attacker can already plant files under your `.claude/`. The repo guards against exactly this in `eval/disk_budget.py:436` (`if entry.is_symlink(): ...`).
- **Recommendation**: In `_add_surface`, add `if path.is_symlink(): return` before the `is_file()` check, matching the `disk_budget.py` policy.

#### L2. `--output` / `--project-root` are unconfined trusted operator input (undocumented trust boundary)
- **File**: `src/superclaude/cli/init_lite.py:314,318`
- **Category**: security (latent) / docs
- **Source**: auggie (folds Auggie finding #2 + cross-cutting #2; Auggie's "symlink confuses ownership" mechanism does **not** hold — `_is_init_lite_owned` calls `resolve()`, so an escaping symlink resolves *outside* the owned root and is correctly classified not-owned)
- **Why this matters**: `--output` may target any non-protected location (this is by design — it's a documented flag), and `--project-root` will happily walk `/etc` or `~/.ssh` if pointed there (read-only size disclosure). Writes to context inputs are still blocked by `_is_protected_context_path`. The real gap is that the "read-only / safe" framing in the PR body and SKILL.md doesn't state that these two flags are *trusted operator input*, not sandboxed.
- **Recommendation**: Add a one-line trust-boundary note to `init_lite_command`'s docstring and SKILL.md §4. If the tool is ever exposed to untrusted input, add allowlist validation like `eval/config.py:resolve_scratch_root`.

#### L3. Test gap: no symlink-`--output` and no malicious-`--project-root` coverage
- **File**: `tests/cli/test_init_lite.py` (suite-level)
- **Category**: tests
- **Source**: auggie (folds findings #5 + #6)
- **Why this matters**: The suite covers direct-path protection well (`test_force_refuses_to_write_protected_context_inputs:366`, `test_claude_md_bytes_never_change:244`, `test_existing_claude_dir_is_not_written:309`) but never exercises a symlink `--output → CLAUDE.md` (which `_is_protected_context_path`'s `resolve()` *should* catch) or a `--project-root` pointed outside the project. These would lock in the safety claims the PR makes.
- **Recommendation**: Add (1) a test creating `tmp/.dev/superclaude/evil → tmp/CLAUDE.md` and asserting `--output evil` is refused; (2) a `--project-root` test asserting graceful behavior on a root with no read access / outside `tmp_path`.

#### L4. Command-doc `--force` row is less precise than the skill/code
- **File**: `src/superclaude/commands/init-lite.md:35`
- **Category**: docs
- **Why this matters**: The command table says `--force` "Overwrite init-lite-owned generated artifacts under `.dev/superclaude/` only; never context inputs." The skill (`SKILL.md:63`) and code (`init_lite.py:232–233`) are more precise: `--force` specifically enables overwriting **marker-less** owned files (marked reports overwrite without `--force`). Not a contradiction, just less precise — a reader of the command file alone won't learn the marker exemption.
- **Recommendation**: Align `init-lite.md:35` wording with `SKILL.md:63` (mention the marker-less nuance).

### 💬 Nit

#### N1. Installer e2e test could use `force=False` for a stronger guard
- **File**: `tests/unit/test_cli_install.py:244`
- **Note**: Auggie flagged `test_install_all_skills_keeps_protocol_skills_standalone` (uses `force=True`) as a vacuous regression guard. **This overstates it** — the actual regression (protocol skills wrongly classified command-backed) is robustly guarded by `test_new_init_lite_protocol_is_not_command_backed:200`, `test_sample_existing_protocol_skills_not_command_backed:206`, and `test_no_available_protocol_skill_is_command_backed:231`, none vacuous. The e2e test is a complementary "installs standalone" check. Optionally switch it to `force=False` + an idempotent re-run for marginally stronger end-to-end coverage; not required.

## Architectural / Cross-Cutting Observations

- **Atomic-write convention** — folded into M1 above. The single highest-value action: adopt the repo's `tempfile + os.replace` pattern in the two `init_lite.py` write sites.
- **Safety design is otherwise sound** — `resolve()`-based protected-path and ownership checks are the right approach; `--dry-run` short-circuits correctly; flag semantics between command/skill/code agree except for the L4 precision nit.

## Audit

- Auggie chunks: 1 (succeeded: 1, retried: 0, skipped: 0)
- Auggie raw findings: 8 findings + 2 cross-cutting → after grounding/dedupe: 1 medium, 4 low, 1 nit
- Dropped during grounding: 1 (Auggie finding #4 "weight boundary off-by-one" — false positive; docstring `init_lite.py:55` matches code exactly)
- Folded (dedupe): #1+cross-cutting#1 → M1; #2+cross-cutting#2 → L2; #5+#6 → L3
- Corrected: #8 severity (Medium→Nit) — premise that the guard is vacuous is false at suite level
- Persona cross-check: disabled (standard depth)
- Recommendation: **Approve with comments** (no merge blockers)

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 0 medium: 1 low: 4 nit: 1
dropped: 1
auggie_chunks: 1
duration_sec: 137
-->
