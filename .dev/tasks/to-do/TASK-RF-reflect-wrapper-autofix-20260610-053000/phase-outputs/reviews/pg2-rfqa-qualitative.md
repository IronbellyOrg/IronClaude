# QA Report — Operational Qualitative Review (reflect-wrapper auto-fix: base precedence + new fields)

**Topic:** reflect-wrapper AUTO-FIX evolution — FR-6 base precedence + spec-literal field names + single-ref diff invariant
**Date:** 2026-06-10
**Phase:** doc-qualitative (operational lens, code-vs-spec fidelity)
**Fix cycle:** N/A
**Stance:** ADVERSARIAL — report only, fix nothing

---

## Overall Verdict: FAIL

The three questions asked have nuanced answers, and the adversarial trace surfaced one
CRITICAL end-to-end wiring gap that makes the FR-6 `--base` precedence **unreachable from
the CLI** despite being correctly implemented in `config.py`.

---

## The three questions, answered with evidence

### Q1 — Does the base-precedence chain ACTUALLY implement `--base > frontmatter start_commit > git merge-base HEAD master`?

**In `config.py`: YES, all three branches are correct and were runtime-verified.**
**End-to-end from the CLI: NO — the top branch (`--base`) is unreachable (see CRITICAL-1).**

`_resolve_base` (config.py:81-105) implements first-match-wins precedence exactly as the
spec §FR-6 / §9 worked chain states. Runtime trace (`uv run python`, all four branches):

| Branch | Input | Returned | Spec branch |
|--------|-------|----------|-------------|
| B1 | `base_override='SHA_OVERRIDE'`, fm `start_commit='aaa'` | `SHA_OVERRIDE` | `--base` wins (highest) |
| B2 | `base_override=None`, fm `start_commit='fm_sha'` | `fm_sha` | frontmatter `start_commit` |
| B2b | `base_override='   '` (whitespace), fm `start_commit='fm_sha'` | `fm_sha` | empty override correctly falls through (the `.strip()` truthiness guard at config.py:97 is right) |
| B3 | `base_override=None`, fm `{}` | `e97aa4fd2a9d` | `git merge-base HEAD master` |
| (none) | all empty + git failure | raises `ValueError("base-unresolved")` | matches docstring + spec fail-closed |

The precedence ORDER, the empty-override fall-through, the `master` default
(`_DEFAULT_BASE_BRANCH = "master"`, config.py:44), and the fail-closed terminal `ValueError`
are all spec-faithful. **This part of the implementation is correct.**

### Q2 — Are the new field NAMES spec-literal (not paraphrased)?

**YES — all six are byte-exact against spec §9 and contract §6.**

Verified by grep across the package. Every name the spawn prompt enumerated exists verbatim:

| Spec/contract name | Location | Match |
|--------------------|----------|-------|
| `base_override` | models.py:84 (`ReflectConfig`), config.py:139/183/237 | exact |
| `fix` | models.py:85, config.py:140/238 | exact |
| `max_fix_iterations` | models.py:86, config.py:141/239 | exact |
| `fix_iterations` | models.py:114 (`ReflectResult`) | exact |
| `fix_converged` | models.py:115 | exact |
| `remediation_task_path` | models.py:116 | exact |

No paraphrasing (no `base_ref`, `auto_fix`, `fix_count`, `remediation_path`, etc.). Defaults
match spec: `max_fix_iterations` default `2` (spec FR-3 "default 2"), `fix_iterations: int = 0`,
`fix_converged: bool = False`, `remediation_task_path: str | None = None`. The dataclass
field-ordering comments (models.py:82-83, 112-113) correctly note the append-after-non-defaults
rule and the 5-construction-site default requirement — these are accurate and load-bearing.

### Q3 — Would a `--base <sha>..HEAD` range value silently corrupt the single-ref diff invariant?

**Mechanically the verbatim-single-ref STORE property is preserved; but the wrapper does NOT
REJECT a range value — it passes `..HEAD` through verbatim to `--diff`.** This is
spec-CONSISTENT for `config.py` in isolation (the spec defines "de-range" as
"no `..` parsing/splitting is performed", not "reject ranges"), but it is an operational
soft spot — see IMPORTANT-1.

Trace: `base_override='abc..HEAD'` → `_resolve_base` returns `'abc..HEAD'` verbatim (no split,
no rejection) → stored as `config.base` → runner.py:344 emits `parts += ["--diff", config.base]`
verbatim. So a range value would reach reflect's `--diff` as `abc..HEAD`, which IS a commit
range, defeating the working-tree-diff intent the spec FR-6 / contract §2 protect.

The spec's actual invariant ("no `..` parsing/splitting") IS satisfied — the code never splits a
range and never downgrades to unconditional merge-base. The corruption-prevention for range
values is **delegated to the generator contract** (contract §2 "Flags the generators MUST NOT
emit: … any `<base>..HEAD` range form for `--base`"). That delegation is a legitimate design
choice, but it means the wrapper trusts its caller rather than enforcing the invariant itself.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | commands.py:57-144 (`run` command + options) | The FR-6 `--base` flag, plus `--fix/--no-fix` and `--max-fix-iterations`, are **NOT exposed as Click options and NOT passed to `resolve_config`**. `run()` calls `resolve_config(...)` (commands.py:132-144) with no `base_override`, `fix`, or `max_fix_iterations` args, so they fall through to the defaults `base_override=None`, `fix=False`, `max_fix_iterations=2`. **Result: the top precedence branch (`--base`) is dead code from the CLI** — a user/generator running `superclaude reflect run <f> --base <sha>` would hit a Click "no such option" error, and the O1/O2 invocation shapes in spec §4 and contract §2 (`--fix --promote`, `--no-promote --base <SHA>`) would FAIL at the command line. | Add `@click.option("--base", "base_override", default=None)`, `@click.option("--fix/--no-fix", default=...)`, and `@click.option("--max-fix-iterations", type=int, default=2)`; add the params to `run(...)`; thread them into the `resolve_config(...)` call. (Spec §9 lists `commands.py` as the surface that "add[s] `--fix/--no-fix`, `--max-fix-iterations`, `--base`" — this is unimplemented.) |
| 2 | IMPORTANT | config.py:81-105 + runner.py:344 | No range-form rejection on `base_override`. A `<sha>..HEAD` value is stored and emitted to `--diff` verbatim, silently converting the working-tree diff into a commit range (the exact failure #153 / F3 de-range was created to prevent). The invariant is currently enforced only by trust in the generator contract (§2), not by the wrapper. | Add a guard in `_resolve_base` (or `resolve_config`) that raises `ValueError("base-must-be-single-ref")` when `base_override` contains `".."`. Fail-closed (blocked/exit 2) is the correct posture given the rest of the package. This makes the spec's single-ref invariant defensively enforced rather than caller-trusted. |
| 3 | MINOR | commands.py:31, 129 (`_DEFAULT_MODEL` / `ANTHROPIC_MODEL`) vs `commands.py` docstring | Out-of-scope-for-this-review but observed during the end-to-end trace: the promote default in `commands.py:73` is still `default=False` (`--no-promote`), but spec FR-5 / contract §5 flip the default to `--promote`. Like CRITICAL-1, this is a `commands.py` gap, not a `models.py`/`config.py` gap — flagging so the merge step does not assume the field-layer correctness implies the CLI-layer correctness. | Flip `--promote/--no-promote` default to `True` per FR-5; covered by the same `commands.py` remediation as CRITICAL-1. |

---

## Scope note (why findings land in `commands.py` though the assigned files were `models.py`+`config.py`)

The spawn prompt scoped the files to `models.py`, `config.py`, spec, and contract, but the
question "does the precedence chain ACTUALLY implement `--base > … > merge-base`?" is an
**end-to-end operational question** that cannot be answered honestly without tracing whether
`--base` reaches `_resolve_base`. It does not. Reporting `config.py` as PASS in isolation while
the CLI cannot deliver a `--base` value would be a false PASS that lets a broken gate reach the
generators (who depend on the exact `--base <SHA>` O2 invocation shape, contract §2/§8). The
field-layer and resolution-layer are correct; the **command-layer wiring that makes them
reachable is absent.**

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on no inherited structural verdict (none provided in spawn prompt); performed standalone verification.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Precedence ORDER correctness — verified by runtime trace of `_resolve_base` across all 4 branches (`uv run python`, B1/B2/B2b/B3 + ValueError path), not by reading the docstring.
- Field-name spec-literalness — verified by `grep -rn` of all six names across the package (models.py:84-116, config.py:139-239) against spec §9 + contract §6 tokens.
- End-to-end `--base` reachability — verified by `grep -n '"--base"' commands.py` (zero hits) + reading `run()`'s `resolve_config(...)` call site (commands.py:132-144) confirming the three new args are not threaded.
- Range-corruption behavior — verified by runtime trace (`base_override='abc..HEAD'` returns `'abc..HEAD'`) + reading runner.py:344 `--diff` emission, not by assuming the docstring's "de-range" claim covers rejection.

## Confidence

**Confidence:** Verified: 3/3 questions + 3 findings | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 5 | Grep: 4 | Glob: 0 | Bash: 4 (incl. 2 runtime traces)

All four tool-engagement calls map to specific verifications (file reads of the 4 named files +
commands.py for the wiring trace; greps for field names, range guards, command options; two
`uv run python` runtime traces of `_resolve_base`). No padding.

## Recommendations

1. **Block the gate until CRITICAL-1 is fixed** — `commands.py` must expose `--base`,
   `--fix/--no-fix`, `--max-fix-iterations` and thread them into `resolve_config`, and flip the
   `--promote` default (MINOR-3). Without this, the spec §4 / contract §2 invocation shapes
   error at the CLI and the FR-6 precedence top branch is dead code.
2. **Harden IMPORTANT-1** — add a `".." in base_override` → `ValueError` guard so the single-ref
   diff invariant is enforced by the wrapper, not merely trusted to the generator contract.
3. After fixes, re-run this review WITH `commands.py` formally in scope and add an integration
   test asserting `superclaude reflect run <f> --base <sha>` resolves B1.

## QA Complete
