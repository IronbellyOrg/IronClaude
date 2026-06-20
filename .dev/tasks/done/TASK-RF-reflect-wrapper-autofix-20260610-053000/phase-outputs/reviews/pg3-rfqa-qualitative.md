# QA Report — Operational Qualitative Review (Phase 3: commands.py)

**Topic:** reflect-wrapper auto-fix evolution — Phase 3 (commands.py surface)
**Date:** 2026-06-10
**Phase:** doc-qualitative (operational lens, adapted to a CLI-surface review)
**Fix cycle:** N/A (report-only)
**Reviewer:** rf-qa-qualitative (ADVERSARIAL STANCE, fix_authorization: false)

**Scope:** `src/superclaude/cli/reflect/commands.py` only — flags, promote flip,
recursion-breaker, base/tmux forwarding. The runner.py auto-fix loop, contract.py
classifier, models.py auto-fix bookkeeping, and SKILL.md gate-emission deltas are
Phases 4–5 (not yet implemented) and are correctly NOT failed here.

---

## Overall Verdict: PASS

---

## The four load-bearing questions — empirically answered

### 1. Does the guard ACTUALLY exit 0 BEFORE Click rejects the non-existent tasklist arg? — YES

The recursion breaker is placed in the `@click.group("reflect")` **group callback**
(`commands.py:62-73`), NOT inside `run()`'s body. Click invokes group callbacks
during command parsing, BEFORE the `run` subcommand's
`@click.argument("tasklist", type=click.Path(exists=True, ...))` validation fires.

**Empirical proof (CliRunner):**
`reflect run /tmp/nonexistent-since-moved-file-xyz.md` with
`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` →
**exit_code = 0**, output `reflect-wrapper recursion breaker: nested gate suppressed`,
no exception. With the marker absent, the SAME missing path → exit 2 (Click usage
rejection). This proves the guard pre-empts path validation — the load-bearing FR-2
behavior. Code comment at lines 62-68 correctly documents the rationale ("an in-body
check cannot pre-empt Click's parse-time path validation"). Matches contract §3.1 and
merged-requirements FR-2 verbatim ("immediately exits 0 ... before any audit").

### 2. Is the truthiness spec-literal (only '1' suppresses)? — YES

`os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1"` (line 69).

**Empirical matrix (missing-path probe; suppressed = recursion-breaker message present):**

| marker value | exit | suppressed |
|---|---|---|
| `'1'` | 0 | YES |
| `'0'` | 2 | no |
| `''` | 2 | no |
| `'2'` | 2 | no |
| `' 1 '` | 0 | YES (strip) |
| `'01'` | 2 | no |
| `'true'` / `'TRUE'` / `'yes'` | 2 | no |
| ABSENT | 2 | no |

Only `'1'` (and `' 1 '` via `.strip()`) suppresses; `'0'`/`''`/`'2'`/absent and all
non-`1` strings run normally. Matches spec §1, FR-2, contract §3 ("exactly the string
'1'. Absent/empty/any-other-value ⇒ not suppressed"). The `.strip()` whitespace
tolerance is a reasonable defense, NOT a spec violation — the contract specifies the
*value* `"1"`, and `' 1 '.strip() == '1'`.

### 3. Does the promote default match O1 `--depth deep --fix --promote` working WITHOUT explicitly passing `--promote`? — YES

`--promote/--no-promote` declared with `default=True` (`commands.py:89-94`).

**Empirical proof (resolve_config kwargs captured via monkeypatch):**
- O1-minus-explicit-promote `reflect run <file> --depth deep --fix` → `promote=True`
- Full O1 `--depth deep --fix --promote` → `promote=True` (identical)

The O1 invocation shape works correctly WITHOUT explicitly passing `--promote`.
Matches FR-5 ("default flips to `--promote`") and contract §5. The `--fix` CLI default
is `False` (the generator emits `--fix`), consistent with the spec phrasing "gate
default `--fix`" — the *gate caller* supplies it, not the intrinsic CLI default.

### 4. Does the wrapper correctly LEAVE O2 `--no-promote` forcing to the generator (no wrapper-side O2 logic)? — YES

`grep -niE "O1|O2|per-phase|phase.detect|adapter"` over commands.py finds these
strings ONLY in help text (line 93) — there is ZERO O1/O2 detection or phase-forcing
logic. The wrapper is a pure flag forwarder: passing `--no-promote` → `promote=False`
(captured empirically). The generator owns the O2 decision per FR-5 / contract §5; the
phrase "the wrapper forces `--no-promote`" is realized by the *generator emitting it*,
not by wrapper-side branching. Correct — no wrapper-side O2 logic.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Recursion breaker pre-empts Click path validation | PASS | CliRunner: missing-path + marker=1 → exit 0 (not usage error) |
| 2 | Truthiness spec-literal (only '1') | PASS | 10-value matrix; only '1'/' 1 ' suppress |
| 3 | Promote default flip to True | PASS | `default=True`; O1-minus-promote threads promote=True |
| 4 | No wrapper-side O2 logic | PASS | grep: O1/O2 only in help text; pure forwarder |
| 5 | `--base` threaded + tmux-forwarded (single ref) | PASS | base_override='abc123' captured; inner argv `--base` only when present |
| 6 | `--max-fix-iterations` default 2 (FR-3) | PASS | captured max_fix_iterations=2 |
| 7 | tmux inner-cmd explicit promote both directions (FR-5 footgun) | PASS | promote=False→`--no-promote`; promote=True→`--promote` |
| 8 | NFR-1 thinness (no sprint/roadmap import, no async) | PASS | grep empty; async count 0 |
| 9 | Exit-code wiring consistent (pass0/halt10/degr11/block2) | PASS | models.py Verdict.exit_code matches; _BLOCKED_EXIT=2 |
| 10 | Config-STOP sidecar path doesn't crash | PASS | forced ValueError → exit 2 + wrapper-result.yaml written |
| 11 | Referenced symbols exist (Verdict, write_sidecar, ReflectResult fields) | PASS | all present; auto-fix fields defaulted so hand-built site valid |
| 12 | main.py registration | PASS | main.py:442 `add_command(reflect_group, name="reflect")` |

---

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

---

## One observation (NOT a Phase-3 failure)

**Test `tests/cli/reflect/test_no_nesting_guard.py::test_layer_a_wrapper_branch_is_bash_shellout` FAILS** — but this is OUT OF Phase-3 scope and not a commands.py defect.

It asserts against the **task-builder SKILL.md source**
(`src/superclaude/skills/task-builder/SKILL.md`), searching for the marker
`**Mode \`2\` / \`auto-resolved-2\` (§6.3, DEFAULT) — wrapper shell-out, remediate:**`.
That heading belongs to the **abandoned `--reflect` dial** (merged-requirements §0:
"PR #157 closed... Not carried forward"). Confirmed: `auto-resolved-2`,
`POST_REFLECT_MODE`, and `--reflect` are entirely ABSENT (grep count 0) from the
current SKILL.md. The SKILL.md gate-emission deltas are explicitly Phase 4–5 work.
This is pre-existing dial-era residue, reconciled when the SKILL.md gate emission
lands; it does not touch the commands.py surface. The other 40 reflect tests pass
(41 collected, 40 passed, 1 failed).

---

## Confidence

**Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
**Tool engagement:** Read: 4 | Grep: 5 | Glob: 0 | Bash: 8

---

## Self-Audit

1. **Factual claims verified against source:** All four load-bearing questions were
   verified by *executing* the CliRunner against the real `reflect_group`, not by
   reading code alone. The parse-vs-callback order (highest-risk claim) was proven by
   observing exit 0 vs exit 2 under marker toggling against a non-existent path.
   Promote/base/iteration threading was verified by monkeypatching `resolve_config` to
   capture actual kwargs. The config-STOP sidecar path was verified by forcing a
   ValueError and observing exit 2 + the written `wrapper-result.yaml`.
2. **Files read:** `commands.py` (full), `merged-requirements.md` (full),
   `reflect-wrapper-contract.md` (full), `models.py` (ReflectResult/Verdict); plus
   grep/exec against `main.py`, `runner.py`, `config.py`, `SKILL.md`,
   `test_no_nesting_guard.py`.
3. **Not a zero-issue rubber-stamp:** I surfaced a failing test and adversarially
   traced it to abandoned-dial residue rather than ignoring or mis-attributing it. The
   `.strip()` whitespace tolerance was specifically probed (`' 1 '`, `'01'`) to confirm
   it does not widen the truthiness contract beyond the spec-literal `"1"`.
4. **Web research:** None performed — all verification was local-file / empirical-
   execution bound. Tavily-first rule not triggered (no external lookup required).

---

## Recommendations

- Phase 3 (commands.py) is operationally sound and may proceed.
- **Do not** fix `test_no_nesting_guard.py` in Phase 3 — it is coupled to the Phase
  4–5 SKILL.md gate-emission template. Flag it in the Phase 4/5 task so its failure is
  not mistaken for a wrapper regression; the test marker must be updated to match the
  new contract-conformant Mode emission (or the test re-scoped) when that lands.

## QA Complete
