# Pre-Edit Source Evidence

**Task:** TASK-RF-reflect-marker-leak-20260611-175724
**Captured:** 2026-06-11
**Purpose:** Bind the exact edit sites, must-not-edit surfaces, and validation commands extracted from the five research files before any source edit.

## Binding edit sites and constraints

| Reference | Relevant File | Required Action | Must Not Break |
|-----------|---------------|-----------------|----------------|
| R-002 §3/§4 (`02-verification-envelope-surface.md`), research-notes GAP_FILL §6.1.1 anchor | `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §6.1.1 (controls a–h at `:489-502`, verb allowlist at `:494`, after control (h) at `:500`) | Add new control **(i)** after control (h): require every §6.1 step 5.5 verification command to run as `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <validated base command>` after base-command validation passes; strip applies ONLY to non-mutating verification/build/test subprocesses. Update preface `All eight controls are mandatory` → `All nine controls are mandatory`. | Must NOT authorize clearing the marker for reflect audits, reflect gate commands, or auto-run corrective `/task`. Must preserve controls (a)–(h), the per-invocation audit artifact (g), and `--no-verify` (h). Must NOT add `env` as a user-selectable allowlisted verb. |
| R-002 §3 Option A/§4 secondary tweak (`SKILL.md:494`), research-notes GAP_FILL control-(b) clarification | `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §6.1.1 control **(b)** only | Add a one-line clarification that the verb allowlist is checked against the BASE command's first token in `{pytest, ruff, mypy, make, uv, npm, tsc, cargo}`, NOT against the `timeout`/`env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` wrapper prefix added by the protocol. | Must NOT weaken control (c) metacharacter rejection or control (a) template construction. Fixed wrapper must remain protocol-authored, never assembled from untrusted spec/tasklist prose. |
| R-003 §3.2 + research-notes GAP_FILL (LOCATION OVERRIDE) | `tests/cli/reflect/test_marker_suppression.py` | Add source-contract regression test `test_verification_envelope_strips_reflect_wrapper_marker` that reads `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, extracts the §6.1.1 `execute_shell_command` envelope via stable heading anchors, and asserts the envelope contains BOTH `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` and `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`. Include a docstring/comment noting that if the fix later moves into Python a direct unit test must prove marker-present input yields marker-stripped output. | Test MUST live in `test_marker_suppression.py`, NOT `test_no_nesting_guard.py` (GAP_FILL override: `test_no_nesting_guard.py` is staged-modified by the sibling task → collision risk). MUST read source-of-truth `src/superclaude/`, NOT `.claude/` mirrors. |
| R-004 §3/§5 (`04-conventions-contract-template.md`) | `.dev/tasks/.../phase-outputs/plans/contract-carveout-deferral.md` (DEFAULT) — sibling contract `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` is non-default | Follow DEFAULT path: write the deferral artifact documenting the exact deferred §3.2 patch. Only edit the sibling-worktree contract if explicit in-session operator authorization is recorded. | Must NOT edit a sibling worktree owned by a concurrent task without operator authorization. Must NOT change unrelated contract text. |
| R-004 §2 (CLAUDE.md sync rules) | `make sync-dev`, `make verify-sync`, `uv run ruff format --check src/ tests/`, `uv run ruff check src/ tests/`, `uv run pytest tests/cli/reflect/test_marker_suppression.py tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q` | Run all validation commands from worktree root with green/exit-0 results captured to `phase-outputs/test-results/`. | Must NOT stage or edit `.claude/` mirrors directly (gitignored sync-dev output). `make lint` alone is NOT CI parity — ruff format-check is separate. |

## Evidence-only surfaces — MUST NOT receive the marker-strip fix

| File | Why evidence-only | Must Not Break |
|------|-------------------|----------------|
| `src/superclaude/cli/reflect/commands.py` (`:44` constant, `:62-73` group-callback recursion-breaker guard) | R-001 §1/§5: the guard is the correct recursion breaker the leaked verification tests trip on; it must stay. | Exact-string `== "1"` suppression guard must remain unchanged. |
| `src/superclaude/cli/reflect/runner.py` (`:53` constant, `:405-416` audit child, `:440-448` corrective `/task` child) | R-001 §2/§5, R-002 §5: the marker is INTENTIONALLY exported into audit + apply children for nested-gate suppression; removing it breaks recursion suppression. | `env_vars={_WRAPPER_MARKER: "1"}` on audit and `/task` children must remain. |
| `src/superclaude/cli/pipeline/process.py` (`:145-160` `build_env`) | R-001 §3: env-propagation mechanism only; the fix is NOT a marker scrub here. | Do NOT add marker scrubbing in `build_env()` for this task. |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` marker references | research-notes GAP_FILL: those are O2 GATE-EMISSION skip guards, unrelated to the verification-env leak. | OUT OF SCOPE — do NOT edit for the marker-strip fix. |

## Key resolved decisions (from research-notes GAP_FILL_RESOLUTIONS)

- Fix mechanism = **Option C** (skill-body control instruction in §6.1.1), NOT a Python edit. No Python `execute_shell_command` verification runner exists under `cli/reflect/`.
- Regression test home = **`test_marker_suppression.py`** (overrides R-003's `test_no_nesting_guard.py` recommendation).
- Canonical verify command re-proves nested-gate suppression is still intact AND new source-contract presence: `uv run pytest tests/cli/reflect/test_marker_suppression.py tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q`.
- POST gate = end-to-end dogfood AFTER fix + validation; if marker is `1` at gate time, record DEVIATION `dogfood deferred — nested-gate suppression, not proof` and use documented fallback evidence.
- Empirical proof of the bug (R-003 §2): marker-set run → 6 failed / 4 passed; `env -u` marker-unset run → 10 passed.
