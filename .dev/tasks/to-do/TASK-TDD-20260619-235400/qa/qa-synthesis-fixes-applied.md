# QA Report — Synthesis-Gate Fix Cycle (S1/S2/S3 applied in-place)

**Topic:** FR-RH2 Headless Ensemble Fix — TDD synthesis
**Date:** 2026-06-20
**Phase:** synthesis-gate (fix-cycle)
**Fix authorization:** true
**Agent:** rf-qa (adversarial stance; every citation re-verified against shipped source)

---

## Overall Verdict: FIXED (3/3 applied, each code-grounded)

All three findings from `qa-consolidated-findings-synthesis.md` were fixed in-place
with surgical Edits. No file was rewritten. Each Edit returned success. Internal
"(Dn)" directive labels were left untouched (assembler scope).

---

## S1 (IMPORTANT) — synth-06 §12.4 5xx retry mislabelled "Immediate"

**File:** `synthesis/synth-06-error-security.md` §12.4 (Retry & Recovery Strategies)

**Source verification (`src/superclaude/cli/swarm/dispatch.py`):**
- `dispatch.py:46` + `:224-225` — `RetryPolicy` §7 defaults: `on_5xx=True`,
  `on_5xx_backoff_sec=2`, `on_4xx=False`, `on_timeout=False`.
- `dispatch.py:124` — `_DEFAULT_TIMEOUT_SEC = 180`; applied at `:244`.
- `dispatch.py:202-273` — `_send_with_retry`: 5xx path sleeps the configured
  backoff at `:269-271` (`backoff = max(0, retry.on_5xx_backoff_sec)`;
  `if backoff > 0: sleep_fn(backoff)`) **before** the single retry `_send_once`
  at `:273`. Backoff sleep is excluded from `elapsed_ms` (comment `:264-268`).

**What was wrong:** the §12.4 row said the 5xx retry was an
"**Immediate** single retry" — contradicting the `on_5xx_backoff_sec=2` source
and synth-08 §17.2 (which correctly says `+2s backoff`).

**Fix applied (2 Edits):**
1. §12.4 intro prose — now states "once, with a 2s backoff," cites
   `dispatch.py:202-273`, the `:224-225` defaults, the `:269-271` backoff sleep,
   and `_DEFAULT_TIMEOUT_SEC = 180` at `dispatch.py:124`/`:244`. Added explicit
   "This matches synth-08 §17.2."
2. §12.4 retry-matrix row — 5xx row changed from "Immediate single retry" to
   "Retry once with **2s backoff** (`on_5xx_backoff_sec=2`)" + budget cell now
   reads "Single retry after a 2s backoff sleep (`dispatch.py:269-271`); per-call
   budget 180s (`elapsed_ms` excludes the backoff sleep)."

**Consistency:** synth-06 §12.4 now agrees with synth-08 §17.2 line 49
(`on_5xx_backoff_sec=2`) and §17.2 worst-case row (`+2s` backoff). ✔

---

## S2 (MINOR) — synth-08 §19.6 wrong file+line for the sanctioned tmux subprocess

**File:** `synthesis/synth-08-perf-deps-migration.md` §19.6 (NFR-7 / OI-2 reconciliation)

**Source verification (grep `subprocess.run` across `reflect/` + `swarm/`):**
- The sanctioned `--tmux` `subprocess.run` is in **`src/superclaude/cli/reflect/commands.py`**,
  function `_launch_tmux` (def at `:311`):
  - `reflect/commands.py:320` — `subprocess.run(["tmux", "new-session", "-d", "-s", name, …])`
    (the launch; this is the legitimate sanctioned call).
  - `reflect/commands.py:325` — `subprocess.run(["tmux", "attach-session", "-t", name])`.
  - `reflect/commands.py:327` — `subprocess.run(["tmux", "kill-session", "-t", name], check=False)`.
- The no-nest ban scope is correct: `grep subprocess src/superclaude/cli/reflect/runner.py`
  and `…/ensemble.py` shows **no raw `subprocess.run`** — runner.py only has docstring
  mentions + `ClaudeProcess`; ensemble.py does not exist yet. So the ban scoped to
  `{runner.py, ensemble.py}` genuinely does not touch `reflect/commands.py:320`.

**What was wrong:** synth-08 cited `commands.py:267-274` (and `commands.py:267`) —
wrong on BOTH count: (a) bare `commands.py` is ambiguous (implies `swarm/commands.py`);
(b) lines 267-274 of `reflect/commands.py` are `_session_name`/`_write_exit_sentinel`,
not subprocess calls at all. The real call site is `reflect/commands.py:320`.

**Fix applied (2 Edits):**
1. §19.6 bullet — now reads "`reflect/commands.py` keeps a legitimate `--tmux`
   `subprocess.run` in `_launch_tmux` (`reflect/commands.py:320`, the
   `subprocess.run(["tmux", "new-session", -d, …])` launch; the same function also
   runs `tmux attach-session`/`kill-session` at `reflect/commands.py:325,327`)."
2. §19.6 recorded-amendment text — citation corrected to
   "`reflect/commands.py` retains its sanctioned `--tmux` `subprocess.run` in
   `_launch_tmux` (`reflect/commands.py:320`)."

**Substantive claim unchanged:** the raw-subprocess ban remains scoped to
`{runner.py, ensemble.py}` so the legit tmux call elsewhere is unaffected — correct,
only the line/file reference was fixed. ✔

---

## S3 (MINOR) — synth-09 §22 Q6 glossed the FR-RH2.7 tension

**File:** `synthesis/synth-09-risks-alternatives-ops.md` §22 Open Questions, Q6
(the `ensemble-empty` M==0 slug open question)

**Source verification:**
- `spec.md:303` (FR-RH2.7) — "`derive_verdict` and the `Verdict` exit-code map
  (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are unchanged."
- `spec.md:171,368,438` — `derive_verdict (contract.py, UNCHANGED)` /
  `verdict_map_unchanged`. So adding a new M==0 branch inside `derive_verdict`
  modifies the path FR-RH2.7 pins as unchanged.
- synth-06 §12 D3 Option A (synth-06 line 45) already flags this exactly:
  Option A "is a *deliberate, recorded* amendment to the verdict layer and must
  be called out against FR-RH2.7's 'unchanged' claim."

**What was wrong:** synth-09 Q6 option (ii) ("add `ensemble-empty` as a new reason
slug under the existing `BLOCKED` verdict") was framed as a no-cost slug label
("the slug is a reason label, not a verdict"), without noting that implementing it
requires a new `derive_verdict` M==0 branch — i.e. a modification to the
verdict-derivation path that FR-RH2.7 says stays unchanged. synth-06 emphasised
this tension; synth-09 did not — an inconsistency between the two synth files.

**Fix applied (1 Edit):** Q6 resolution rewritten so:
- Option (i) is labelled **Option B (preserves FR-RH2.7 literally)** — maps M==0
  onto an existing BLOCKED trigger, `derive_verdict` not touched.
- Option (ii) is labelled **Option A (deliberate, recorded scope call)** — adds a
  new M==0 branch in `derive_verdict`, explicitly noted as modifying the
  verdict-derivation path, "must be called out as a deliberate amendment against
  FR-RH2.7's '`derive_verdict` unchanged' claim … NOT a no-cost slug rename,"
  with a direct cross-ref to synth-06 §12 D3 Option A and to spec §FR-RH2.7 (L303).
- Closing line now requires any `derive_verdict` change be "an acknowledged
  FR-RH2.7 amendment, not a silent one."

**Consistency:** synth-09 Q6 now mirrors synth-06 §12 D3 Option A's emphasis. ✔

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| S1 | synth-06 §12.4 5xx backoff correctness | FIXED | `dispatch.py:46,124,202-273,224-225,269-271`; 2 Edits; now matches synth-08 §17.2 |
| S2 | synth-08 §19.6 sanctioned-tmux line cite | FIXED | `reflect/commands.py:311(def),320,325,327`; runner.py/ensemble.py have no raw subprocess; 2 Edits |
| S3 | synth-09 Q6 FR-RH2.7 tension alignment | FIXED | `spec.md:303,171,368,438`; synth-06 D3 Option A (L45); 1 Edit |

## Confidence

Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 4 (consolidated findings + synth-06 + synth-08 + synth-09) |
Grep: 0 (folded into Bash greps) | Glob: 0 |
Bash: 4 (dispatch.py retry grep; cross-package subprocess grep; reflect/commands.py
context + line confirm; spec FR-RH2.7 grep) |
Edit: 5 (S1×2, S2×2, S3×1) — each returned success.

tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
(no external lookups required — all three findings are intrinsically local source-truth checks).

## Notes for downstream (assembler / Step 5.20 re-verify)

- S4 + S5 remain ASSEMBLY directives (not synth-file edits) per the consolidated
  findings — strip bare "(Dn)" labels and renumber synth-03 §6.6/§6.7. Not in this
  fix scope.
- The cosmetic off-by-one citation nits (S6 bucket) were left as-is per the fix plan
  ("Cosmetic nits left as-is").
- Internal "(Dn)" directive labels were deliberately NOT touched.

## QA Complete
