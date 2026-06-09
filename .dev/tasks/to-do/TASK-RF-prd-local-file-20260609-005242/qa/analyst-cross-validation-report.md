# Analyst Cross-Validation Report — ADVERSARIAL Gate

**Lens:** Cross-validation (independent re-verification against actual source; research files NOT trusted).
**Repo:** /config/workspace/IronClaude (read-only).
**Research dir:** `.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/research/`
**Date:** 2026-06-09

---

## Method

Re-opened every cited source file independently and confirmed each line-number/snippet/behavioral
claim. Grep-confirmed reference scope for the three constants and `_build_file_args`. Checked R1/R2/R3
for mutual contradictions.

---

## 1. `src/superclaude/cli/prd/process.py`

| Claim | Source verification | Verdict |
|---|---|---|
| Two `--file` emissions at :199 and :204 | `grep '"--file"'` returns exactly :199 (`file_args.extend(["--file", str(ref_path)])`) and :204 (`file_args.extend(["--file", spec_path])`) | MATCH |
| `_build_file_args` declared :169 (`@staticmethod`) / :170 (`def`), `return` :206 | Read confirms `@staticmethod` :169, `def _build_file_args` :170, `return file_args` :206 | MATCH |
| Branch A (refs>50KB) :191-199 | Read confirms loop :191-199 | MATCH |
| Branch B (spec) :201-204 | Read confirms `if base_step in _SPEC_FILE_STEPS:` :201, emit :204 | MATCH |
| Call site :155, `extra_args=file_args` :166 | Read confirms `file_args = self._build_file_args(config, step_id)` :155; `extra_args=file_args` :166 | MATCH |
| `_PHASE_ALLOWED_REFS` def :95, sole use :191 | grep returns exactly :95 (def) and :191 (use). No other refs. | MATCH |
| `_FILE_SIZE_THRESHOLD` def :115, sole use :198 | grep returns exactly :115 (def) and :198 (use). No other refs. | MATCH |
| `_SPEC_FILE_STEPS` def :121, code use :201, docstring :180 | grep returns :121 (def), :180 (docstring inside method), :201 (code use). All in-method except def. | MATCH |
| All three constants referenced ONLY inside `_build_file_args` | CONFIRMED: every non-definition reference (:191, :198, :201, plus docstring :180) lies within the method body (:170-206). Zero external/test references. | MATCH |
| `base_step` normalization local at :187 | Read confirms :187 `base_step = step_id.rsplit("-", 1)[0] if step_id[-1:].isdigit() else step_id` | MATCH |
| Module docstring :3-5 "phase-aware ``--file`` arg scoping"; :11 GAP-003 line | Read confirms :4 "phase-aware ``--file`` arg scoping", :11 "GAP-003: Phase-aware ``--file`` arg scoping." | MATCH |
| Class docstring :133 "Phase-aware ``--file`` arg construction (GAP-003)" | Read confirms :133 | MATCH |

## 2. `src/superclaude/cli/pipeline/process.py` (base)

| Claim | Source verification | Verdict |
|---|---|---|
| `self.extra_args = extra_args or []` at :63; param default `None` at :48 | Read confirms :63 and :48 (`extra_args: list[str] | None = None`) | MATCH |
| `cmd.extend(self.extra_args)` at :94; only `--file` source is extra_args | Read confirms :94 `cmd.extend(self.extra_args)`; build_command :79-95 has no other `--file` source | MATCH |
| `env = os.environ.copy()` at :107; pops CLAUDECODE :108, CLAUDE_CODE_ENTRYPOINT :109 | Read confirms :107 `env = os.environ.copy()`, :108-109 pops, :110-111 conditional update | MATCH |

## 3. `src/superclaude/cli/prd/prompts.py`

| Claim | Source verification | Verdict |
|---|---|---|
| `_authoritative_specs_block(spec_paths: list[str] | None) -> str` at :120 | Read confirms :120 exact signature | MATCH |
| Empty-input early return `if not spec_paths: return ""` at :130-131 | Read confirms :130-131 | MATCH |
| Non-empty body :132-138 (paths-only, leading `\n\n`, "MUST Read each one IN FULL") | Read confirms :132-138; substring "You MUST Read each one IN FULL before" at :135 | MATCH |
| `_TRUNCATION_MARKER` at :34 (em-dash) | Read confirms :34 `"\n\n[TRUNCATED — file exceeds 50KB inline limit]"` (`—`) | MATCH |
| `_read_file(path, max_bytes=50_000)` at :42-47; truncates `content[:max_bytes] + marker` | Read confirms :42-47 exactly | MATCH |
| `_read_required` guarded variant at :91-95 | grep confirms def at :91 | MATCH |
| Call site A invocation :247-249, interpolation `{specs_block}` at :257 | Read confirms :247-249 and :257 (`{ctx}{specs_block}`) | MATCH |
| Call site B invocation :919, interpolation :927; investigation signature :904-911 (`spec_paths=None`) | Read confirms :919, :927 (`Product root: {product_root}{specs_block}`), signature :904-911 | MATCH |

## 4. `tests/cli/prd/test_spec_flag.py`

| Claim | Source verification | Verdict |
|---|---|---|
| `TestSpecFileAttach` exists around :459-515 | `class TestSpecFileAttach:` at :477; section banner :459-462; `_spec_config` helper :465-474; class body ends :515. R1/R3 cite ":459-515" as the surrounding block (banner→last test) — accurate as a region label. | MATCH |
| Asserts on `--file` / `_build_file_args` | :485/:487 `args == ["--file", str(a), "--file", str(b)]`; :495/:497-498 `"--file" in args` + `str(spec) in args`; :506/:510/:515 `_build_file_args(...) == []` | MATCH |
| Injection tests bind NON-EXISTENT paths | `TestScopeDiscoverySpecInjection.test_block_present_with_exact_paths` (:251) binds `/abs/SPEC_A.md`, `/abs/SPEC_B.md` (:255-256), never created on disk; byte-identity test derives `block = _authoritative_specs_block(["/abs/SPEC.md"])` at :306 | MATCH |
| `"MUST Read each one IN FULL"` assertion | Confirmed at :265 | MATCH |
| `test_helper_empty_returns_empty_string` at :310-312 (locks `==""` for `[]` and `None`) | Read confirms :310-312 | MATCH |
| Imports `_authoritative_specs_block` (:36) + `_render_investigation_prompt` (:37); `PrdClaudeProcess` (:34) | grep confirms all imports | MATCH |

## 5. `tests/cli/prd/test_prompts.py` (R2 secondary)

| Claim | Source verification | Verdict |
|---|---|---|
| `TestReadFileTruncation.test_read_file_truncation_at_50kb` at :249-277; marker hardcoded :253 | Read confirms class :249, test :252, marker literal :253 | MATCH |

---

## Cross-File Contradiction Check (R1 vs R2 vs R3)

- **`--file` emission count.** R1 §7 and R3 §2 both assert exactly 2 emissions at :199/:204; R2 §5 corroborates the no-`--file` sibling convention. Consistent.
- **Removal vs replacement.** R1 removes the `--file` mechanism (delete `_build_file_args` + 3 constants); R2 adds the inline replacement (upgrade `_authoritative_specs_block` to embed content via `_read_file`). These are COMPLEMENTARY halves of one change, not contradictory — R1 owns process.py argv, R2 owns prompts.py content delivery. No conflict.
- **`_build_file_args` reference set.** R1 §4 and R3 §2 both list the identical production+test reference set (process.py :155/:170 + test_spec_flag.py :461/:485/:495/:506/:510/:515). My grep reproduces this set exactly. Consistent.
- **`TestSpecFileAttach` line label.** R1 (":477 start"), R2 (n/a), R3 (":459-515") — R1 cites the `class` line, R3 cites the banner→last-test region. Both accurate; no contradiction (different anchoring conventions, both verifiable).
- **`_read_file` missing-path behavior.** R2 §2 flags that `_read_file` raises `FileNotFoundError` on absent paths and that injection-test fixtures bind non-existent paths — internally consistent and confirmed against source (:42-44 calls `read_text` directly; tests bind `/abs/SPEC*.md`). This is a correctly-surfaced design risk, not an error.
- **Empty-input contract.** R2 (:130-131) and R3 (§2, `test_helper_empty_returns_empty_string` :310-312) agree the `== ""` contract must be preserved. Consistent.

No discrepancies, no contradictions, no wrong line numbers, no mischaracterized behavior found.

---

## Discrepancy List

None.

---

VERDICT: PASS
