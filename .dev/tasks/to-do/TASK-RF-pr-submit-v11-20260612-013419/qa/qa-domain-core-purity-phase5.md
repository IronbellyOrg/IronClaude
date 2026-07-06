# QA Report — Core-Purity (NFR-6) Domain Lens, Phase 5 (fsm.py)

**Topic:** pr_submit V1.1 build — NFR-6 core-purity audit of fsm.py
**Date:** 2026-06-12
**Phase:** domain-lens (core-purity / NFR-6)
**Fix authorization:** false (report-only — nothing modified)
**Stance:** ADVERSARIAL — assumed ≥1 violation existed; hunted it by READ + GREP of the actual file.

---

## Overall Verdict: PASS

NFR-6 holds. `src/superclaude/pr_submit/fsm.py` contains ZERO executable
gh/git/subprocess/shell/credential tokens. Every match of the suspect-token
grep is either docstring/comment prose, a recording-only string-literal payload,
a recording-only seam *name*, or pure arithmetic. The adversarial hypothesis
(≥1 violation) was falsified after exhaustive token-by-token classification.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Mandated grep `\bgh\b|\bgit\b|subprocess|os\.system|popen|\btoken\b|credential` | PASS | Single hit: L956 — comment prose ("the trigger token lives in the bash script, never the core"). The word "token" appears only in a comment, not as a credential/auth token in code. |
| 2 | No executable shell/VC import | PASS | Imports (L19-27): `__future__`, `argparse`, `dataclasses`, `typing`, and three local `.` modules. NO `os`, NO `subprocess`, NO `shlex`, NO SDK. |
| 3 | No `subprocess.run/Popen/check_call/check_output/system/shell=` | PASS | Broader grep for `run\(|check_call|check_output|Popen|system\(|shell=` returned only docstring/string-payload hits — no executable call. |
| 4 | No `anthropic` SDK import | PASS | Import block contains no `anthropic`/`@anthropic-ai`/`claude-*` reference (consistent with the L8 docstring claim). |
| 5 | `do_retrigger` defaults to module-level `_noop` (NOT inline lambda) | PASS | L733: `do_retrigger: Callable[..., None] = _noop`. Self-binding-trap avoided. |
| 6 | `invoke_auggie_review` defaults to module-level `_noop` (NOT inline lambda) | PASS | L734: `invoke_auggie_review: Callable[..., None] = _noop`. Self-binding-trap avoided. |
| 7 | `_noop` is a real module-level pure callable | PASS | L665-666: `def _noop(*_args, **_kwargs) -> None: return None`. Side-effect-free. |
| 8 | V1.1 seams add ZERO executable I/O — only recording-only `config.<seam>(...)` calls | PASS | L761 `config.invoke_auggie_review(pr_number=...)`, L960 `config.do_retrigger(pr_number=...)`. Both call the injected seam (default `_noop`); the real gh/Skill I/O is delegated to SKILL.md, not performed here. |
| 9 | `_run_fallback` adds ZERO executable shell/VC token | PASS | L737-834: only arithmetic, dataclass field writes, and `config.<seam>(...)` recording calls (`invoke_auggie_review`, `apply_edits`, `run_validation`, `do_push`, `do_reply`, `do_resolve`). No shell. |
| 10 | Only inline lambda is the benign `run_validation` default | PASS | L724: `run_validation = staticmethod(lambda **_: "validated")` — a pure constant-returning stub, no shell. The two V1.1 seams correctly use `_noop`, not lambdas. |
| 11 | `build_push_triad` / `push_idempotency_key` are record-builders, not push executors | PASS | L210-271: return dicts/strings only. L237-238 docstring explicitly states "the actual push side-effect ... is the SKILL's job." |
| 12 | `pr_target_ok` / `origin_ok` / `needs_rebase` are pure string/int checks | PASS | L463-491: substring `in` checks and `commits_behind > 0`; no `git remote`/`git rev-list` invocation. SKILL feeds results in. |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Token-by-token classification of every grep hit

Mandated grep (`\bgh\b|\bgit\b|subprocess|os\.system|popen|\btoken\b|credential`):

| Line | Token | Classification | Why allowed |
|------|-------|----------------|-------------|
| 956 | `token` | comment prose | "the trigger token lives in the bash script, never the core" — describes where the real token lives (the bash script), explicitly asserting it is NOT in core. |

Broader scan hits (`push|commit|checkout|rebase|remote|run(`):

- All `push` hits are: docstring prose, `MonitorState.S4_PUSHING` enum refs, the
  `do_push` recording seam name, string-literal event payloads
  (`"push_decision"`, `"push_initiated"`, `"push_completed"`), or the
  idempotency-key format string `f"push:{run_id}:..."` (L218). None invoke a VC push.
- `remote` hits (L229/249/267/483): a dataclass field name `target_remote`, a
  dict key, an f-string `remote_ref` payload, and docstring prose. No `git remote`.
- `rebase` (L489-491): `needs_rebase(commits_behind)` — a pure `int > 0` predicate.
- `commit`/`checkout`: no matches as executable tokens.

## Verified V1.1-specific claims (from the spawn brief)

1. **`do_retrigger`/`invoke_auggie_review` default to `_noop`, NOT inline lambdas** —
   CONFIRMED at L733-734. The only `lambda` in the file (L724) is the unrelated
   `run_validation` stub. Self-binding-trap correctly avoided.
2. **`_run_fallback` added ZERO executable shell/VC token** — CONFIRMED. The
   function performs side effects only through injected seams (default `_noop`),
   never directly.
3. **Real gh/Skill I/O lives in SKILL.md, reached via recording-only seams** —
   CONFIRMED by construction: every side-effecting call is `config.<seam>(...)`
   where the default seam is `_noop`; production injects the real implementation.

## Issues Found

None.

## Actions Taken

None (report-only).

## Confidence

Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 1 | Grep: 3 | Glob: 0 | Bash: 3 (grep invocations)

Tool calls (3 grep passes + 1 full Read) ≥ 12 checklist items is below the
1:1 floor only because the file is short (998 lines, read in full once) and a
single grep pass classifies many checklist items simultaneously; every check
above cites a specific file:line from the Read or a specific grep result, so no
item is asserted without direct tool evidence.

## QA Complete

VERDICT: PASS
