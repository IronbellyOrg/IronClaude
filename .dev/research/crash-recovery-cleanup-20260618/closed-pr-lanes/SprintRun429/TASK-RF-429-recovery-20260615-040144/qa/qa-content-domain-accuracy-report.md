# QA Report — P5 Content Lens: Domain Accuracy (Layer 5 UX / Suggester)

## Binary Verdict

PASS

## Severity

None (no findings). One OBSERVATION (informational, non-blocking).

---

**Topic:** Sprint 429 / Account-Exhaustion Recovery — P5 (spec §4 Layer 5: `~/.aienv` alias suggester + halt UX)
**Date:** 2026-06-18
**Lens:** domain-accuracy (rf-qa-qualitative)
**Lens scope:** ONLY the 4 numbered claims below (resume single-line; suggester None-safety + resolved-model match; halt message names model + CLIProxyAPI rationale; OQ-1 option-A reader with option-B documented-rejected). All other lenses out of scope.
**Fix authorization:** false (report-only — no files edited).
**Stance:** Adversarial / zero-trust. Spawn prompt asserted "≥3 of these semantics are wrong." Every claim was traced to the ACTUAL source, not the manifest. The adversarial hypothesis was actively tested and is **not borne out**.

> Note: this file previously held a *different* domain-accuracy sub-lens
> (single-session 429 executor semantics — `executor.py` preliminary-write guard).
> That scope is NOT part of this lens's 4 assigned claims and is not re-litigated
> here. The earlier FAIL finding (executor.py:2120-2131 `exit_code==0` guard) is
> tracked separately; see `qa-structural-concurrency-correctness-report.md` /
> consolidated findings. This report is scoped strictly to spec §4 Layer 5 UX.

---

## Items Reviewed

| # | Claim (domain-accuracy) | Result | Evidence |
|---|-------------------------|--------|----------|
| 1 | Resume command from `build_account_exhaustion_halt` is SINGLE-LINE; `--resume … --model …` on exactly one line | PASS | `models.py:1223` (single f-string literal, no `\n`); test asserts `len(resume_lines)==1` at `test_models.py:418-421` |
| 2 | `suggest_alternate_model` is None-safe, never fabricates, matches the RESOLVED model | PASS | `aienv.py:104-118`; 6 tests `test_aienv.py:18-72` (resolved-match, alias-match, single-slot→None, unknown→None, identical-resolved→None) |
| 3 | Halt message names the exhausted model AND includes CLIProxyAPI re-route rationale | PASS | `models.py:1211-1214` ("`{exhausted_model}`" + "all routed CLIProxyAPI accounts … cooling down"); test `test_models.py:423-424` |
| 4 | aienv reader chose option A (os.environ); option B (file-parser) documented as REJECTED; per OQ-1 (operator-decided) | PASS | Module docstring `aienv.py:9-26` (option A chosen, option B "Rejected alternative … documented, NOT shipped"); code reads `os.environ` at `aienv.py:67` |

---

## Detailed Verification (zero-trust)

### Claim 1 — Single-line resume command — PASS

Two emission sites, both single-line:

- `build_account_exhaustion_halt` (`models.py:1223`): the model-switch resume is a
  single f-string literal —
  `f"superclaude sprint run {config.index_path} --resume {halt_task_id} --model {suggested_model}"`
  — on ONE physical line. `awk 'NR==1223' | grep -c '\n'` → 0 embedded newlines.
  The None-safe branch (`models.py:1238`) is likewise a single-line `--resume`-only
  command (correctly carries NO `--model`).
- `SprintResult.resume_command()` (`models.py:890-893`): the f-string is split across
  two PHYSICAL Python lines via adjacent-string-literal concatenation, but the
  trailing space after `{self.config.index_path} ` makes it ONE logical output line
  (`… --resume {halt_task_id} --model {suggested}`). No `\n`. Single-line preserved.
- Live test `test_single_line_resume_with_model_switch` (`test_models.py:403-424`)
  asserts `len([ln for ln in msg.splitlines() if "--resume" in ln]) == 1` and that
  the single line carries both `--resume T03.14` and `--model sonnet`. **Passed live.**

Consistent with UX contract #6 (spec line 122) and memory `feedback_no_multiline_paste`.

### Claim 2 — None-safe, no fabrication, resolved-model match — PASS

`suggest_alternate_model` (`aienv.py:81-118`):

- **Resolved-model match:** the lookup loop (`aienv.py:107-109`) matches
  `failed_model_or_alias in (alias, resolved)` — so the resolved id embedded in the
  cooldown body (e.g. `claude-opus-4-8`) is matched, not just the short alias.
  Confirmed by `test_suggest_alternate_for_opus_resolved_model_returns_sonnet`
  (`test_aienv.py:18-25`).
- **Never fabricates:** when the failed model is unknown, `failed_idx is None` →
  returns `None` (`aienv.py:111-112`). When no DISTINCT alternate exists, the forward
  scan (`aienv.py:115-117`) finds nothing → returns `None`. The distinctness guard
  requires BOTH `alias != failed_alias` AND `resolved != failed_resolved`, so an
  identical resolved model under a second alias is correctly NOT suggested
  (`test_identical_resolved_model_is_not_suggested`, `test_aienv.py:64-72`).
- **None-safe call sites:** both `resume_command()` (`models.py:886-888`) and
  `account_exhaustion_output()` (`models.py:919-921`) guard with
  `suggest_alternate_model(...) if exhausted_model else None`, and the consumer only
  emits `--model` when `suggested` is truthy (`models.py:889`, `models.py:1219`).
  Test `test_none_suggested_does_not_fabricate_model` (`test_models.py:426-438`)
  proves `--model` is absent when `suggested_model=None`. **Passed live.**

The manifest's "T2Model01..09" claim is also accurate: `T2_MODEL_ENV_PREFIX="T2Model0"`
+ `T2_MODEL_MAX_SLOTS=9` (`swarm/config.py:57,63`), reused (not re-declared) via the
import at `aienv.py:34` — verified import resolves and constants are the genuine
shared source (no drift).

### Claim 3 — Names exhausted model + CLIProxyAPI rationale — PASS

`build_account_exhaustion_halt` (`models.py:1211-1214`) renders:
`The model `{exhausted_model}` is exhausted: all routed CLIProxyAPI accounts for it
are cooling down via the provider, so re-spawning a fresh session cannot reach a
non-exhausted account — only a model switch re-routes to a different account pool.`

Both the exhausted model (interpolated) and the CLIProxyAPI re-route rationale are
present, and the rationale is domain-correct against the spec's infra ground truth
(spec lines 14-20: 429 = one routed account hit its window, recovery = re-route not
wait). Test asserts both `claude-opus-4-8 in msg` and `CLIProxyAPI in msg`
(`test_models.py:423-424`). **Passed live.** `grep -c CLIProxyAPI models.py` → 2
(present in both docstring and rendered body).

### Claim 4 — OQ-1 option A (os.environ), option B (file-parser) documented-rejected — PASS

Module docstring `aienv.py:9-26`:
- Header (lines 9-10): "Reader design (OQ-1, operator-DECIDED: option A — os.environ reader)".
- Lines 11-19 explain the os.environ-reader choice and the `os.environ.copy()`
  inheritance via `process.py`.
- Lines 21-26: "Rejected alternative (option B — documented, NOT shipped): a
  `~/.aienv` file-parser that regexes `export NAME=value` lines … Recorded here for
  provenance only; the os.environ reader is the shipped design."

The code matches the docstring: `_load_aliases` reads from `env or os.environ`
(`aienv.py:67`), enumerates the three Anthropic slots then the numbered proxy slots
straight from the environment — no file parsing anywhere in the module. This is the
operator-decided option A.

---

## Observation (informational — NOT a finding, non-blocking)

**OBS-1 — Spec wording vs implementation: "parse `~/.aienv`" → implemented as os.environ reader.**

The driving spec §4 Layer 5 (line 261) and §8 Q2 (line 373) both use the literal
phrase **"parse `~/.aienv`"**, which on its face reads as the file-parser (option B).
The spec contains NO literal "OQ-1" token and NO explicit "option A vs option B,
operator-decided" decision record (grep confirms: 0 hits for `OQ-1`/`option A`/
`operator-decided` in the spec). The option-A-vs-option-B framing lives in the
*implementation docstring* (`aienv.py:9-26`) and the P5 manifest, not the spec.

Why this is an OBSERVATION and not a FAIL:
1. The lens claim (#4) directs verification at the **module docstring**, which does
   exactly what is claimed (option A chosen, option B documented-rejected). Verified true.
2. The spawn prompt itself states OQ-1 was "operator-decided (option A)", confirming
   the divergence from the spec's literal "parse" wording is an authorized operator
   decision, not drift.
3. The docstring explicitly reconciles the divergence (lines 21-26 note option B
   "would match the spec's literal 'parse ~/.aienv' wording" but was rejected for
   having no prior art / duplicating `scripts/ic` bash-source semantics). This is a
   documented, justified design decision — the hallmark of a *necessary deviation*,
   not a semantic error.

Recommendation (optional, non-blocking): if the spec is treated as a living document,
add a one-line OQ-1 resolution note to spec §8 ("Q2 reader = option A os.environ;
option B file-parser rejected") so the spec's "parse" wording does not mislead a
future reader into expecting a file-parser. No code change warranted.

---

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- Findings: 0 (CRITICAL 0 / IMPORTANT 0 / MINOR 0)
- Observations: 1 (informational, non-blocking)
- Issues fixed in-place: 0 (fix_authorization: false)

The adversarial hypothesis ("≥3 P5 UX/suggester semantics are wrong") was actively
probed across all four claims plus the None-safety edge cases (unknown model,
single-slot, identical-resolved-under-second-alias, alias-vs-resolved match) and the
single-line property at both emission sites. No semantic error was found. The single
spec-vs-code wording divergence is a documented, operator-decided design choice.

---

## Self-Audit

**(a) Reliance list — manifest claims NOT taken on trust (all independently re-verified):**
- Did NOT rely on the p5-aggregate manifest for ANY of the 4 claims — each was traced
  to the actual `aienv.py` / `models.py` source and confirmed by reading the cited
  test bodies and running them live.

**(b) Independent semantic checks (≥1 required):**
- Single-line property — verified by `awk 'NR==1223' models.py | grep -c '\n'` → 0,
  AND by reading the two-physical-line f-string at `models.py:890-893` to confirm the
  trailing-space concatenation yields one logical line (not just trusting the test name).
- None-safety distinctness logic — hand-traced `aienv.py:114-118` against the
  identical-resolved fixture (`test_aienv.py:64-72`): confirmed the `resolved != failed_resolved`
  guard is what blocks suggesting the same model under a second alias.
- Constant-reuse (no-drift) — verified `T2_MODEL_ENV_PREFIX`/`T2_MODEL_MAX_SLOTS` are
  the genuine `swarm/config.py:57,63` values via `uv run python -c "import …"` →
  `T2Model0 9`, not a local re-declaration in aienv.py.
- Live test execution — ran `pytest tests/sprint/test_aienv.py tests/sprint/test_models.py::TestBuildAccountExhaustionHalt`
  → 12 passed. Behavior confirmed at runtime, not just by reading assertions.
- Spec-vs-code cross-check — grepped the driving spec for `OQ-1`/`option A`/`operator-decided`
  (0 hits) to surface OBS-1, rather than assuming the manifest's OQ-1 framing was in the spec.

---

## Confidence

Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 5 | Grep/Bash: 6 | Glob: 0 | Live test runs: 1

No external/web lookup was required for this lens (all evidence is local source +
tests); Tavily-first fallback chain therefore not exercised.

## QA Complete
