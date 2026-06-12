# QA Domain Report — E4 HEAD-Drift + E3/E4 Dual-Evaluator Framing

**Topic:** E4 HEAD-drift handling and E3/E4 dual-evaluator framing
**Date:** 2026-06-12
**Phase:** doc-qualitative (domain-correctness, adversarial)
**Fix authorization:** false (report-only — NO source file modified)
**Stance:** ADVERSARIAL — assumed ≥3 errors; verified every claim against git + source.

---

## Overall Verdict: **PASS**

All four DOMAIN concerns are correct against git ground truth and the RELEASE-SPEC §8.3 oracle. No
CRITICAL or IMPORTANT domain defect found. Three OBSERVATIONS (one MINOR doc-tension, two
non-defects that survived adversarial probing) are recorded below for completeness — none changes
the verdict.

---

## Concern-by-Concern Verdict

| # | Domain Concern | Verdict | Decisive Evidence |
|---|----------------|---------|-------------------|
| 1 | E4 replays against `1b0264f1` (bug present), NOT HEAD (healed via `20693bb8`); pins parent + documents HEAD-drift caveat | **PASS** | git ancestry + test pin + docstring/skip-reason |
| 2 | E4 framed as H2 ledger-completeness over BOTH `gate_passed` AND `_evaluate_gate` | **PASS** | §8.3 verbatim match; NEW=CATCH ref assertions |
| 3 | E3 (`gate_passed`) and E4 (`_evaluate_gate`) modeled as two SEPARATE consumers of the same advisory mechanism | **PASS** | git commits `eb9a2633` (E3) + `b97c9960` (E4) |
| 4 | E4 OLD=MISS handles class-bound `_evaluate_gate` (SimpleNamespace self / unbound call) and genuinely returns False despite advisory | **PASS** | pre-fix body at `1b0264f1` exec-traced |

---

## Concern 1 — HEAD-drift pinning — PASS

**Claim:** E4 replays against `1b0264f1` (bug present), NOT HEAD (healed via `20693bb8`); the fix
`b97c9960` is unmerged; the test pins the parent and documents the caveat.

**Verified (git, in `/config/workspace/IronClaude`):**

- `git rev-parse b97c9960^` → `1b0264f13eda…` — **`1b0264f1` IS the true pre-fix parent of `b97c9960`.**
- `git merge-base --is-ancestor b97c9960 HEAD` → **NO** (unmerged; lives only on
  `remotes/origin/fix/prd-executor-advisory-gate`, confirmed via `git branch -a --contains`).
- `git merge-base --is-ancestor 20693bb8 HEAD` → **YES** — HEAD healed via the sibling commit
  `20693bb8` "fix(prd): honor advisory semantic-check flag in executor._evaluate_gate".
- `git merge-base --is-ancestor 1b0264f1 HEAD` → **YES** (parent is reachable, so the worktree
  checkout target is valid).
- HEAD `executor.py:859` → `if getattr(check, "advisory", False):` confirms the heal is live on HEAD
  (so replaying current code would NOT reproduce the bug — exactly why the pin matters).

**Test-side pinning (`test_backtest_e4.py`):**

- L34–36: `_E4 = escape_by_id("E4")` with inline comment `prefix_parent_sha == 1b0264f1 (NOT HEAD)`.
- `git_replay.py:52–54`: `ReplayEscape("E4", "b97c9960", "1b0264f1", "H2")` with comment
  `fix UNMERGED; replay against parent`.
- L38–45 `pytestmark` skip-reason explicitly states "Pinned to the pre-fix parent, NOT HEAD (HEAD
  already healed via 20693bb8)."
- L14–17 module docstring carries the "E4 HEAD-DRIFT (critical)" caveat verbatim.
- L76 test docstring repeats "Replayed against the pinned pre-fix parent, NOT HEAD (HEAD already
  healed via 20693bb8)."

The pin is the BARE parent sha (no `^`), consistent with the G1 checkout rule in `git_replay.py:8–10`
and `:44–47`. **No drift defect.**

---

## Concern 2 — H2 ledger over BOTH consumers — PASS

**Claim:** E4 is framed as the §8.3 H2 ledger-completeness assertion over BOTH `gate_passed` AND
`_evaluate_gate`.

**Verified against RELEASE-SPEC §8.3 (read verbatim):**

> E4 backtest | Run advisory check through PRD `_evaluate_gate` with H2 ledger | **H2 FAIL until both
> `gate_passed` and `_evaluate_gate` consumers classified**

- `EscapeResult(escape_id="E4", wave="H2", …)` at `test_backtest_e4.py:85` — correct wave.
- NEW=CATCH proxy `test_backtest_e4_new_gate_catches_via_contract_enumeration_ref` (L94–104) asserts
  the H2 `contract-enumeration.md` ref contains BOTH `"gate_passed"` AND `"_evaluate_gate"` (L102–104)
  plus `"ledger"` / empty-ledger=FAIL (L99–101). This is a faithful proxy for the §8.3 "both
  consumers classified" oracle.
- The proxy is `@requires_impl_ref("contract-enumeration.md")` (L94) and the ref does **not** exist
  yet (`find … contract-enumeration.md` → 0 hits; greenfield per spec §1.2 G1-halt). The guard
  (`_impl_guard.py:43–57`) correctly **SKIPS** (not fails) until the ref lands — appropriate for an
  implementation-halted G1 spec. The OLD=MISS half (L73–91) runs unconditionally.

**No framing defect.** Note: the spec §3.1 E4 row also names two further ledger consumers ("trailing
gate, remediation dispatch"); the NEW=CATCH proxy asserts only the two CODE-VERIFIED ones. See
Observation O-2.

---

## Concern 3 — E3/E4 = two separate consumers of the same advisory mechanism — PASS

**Claim:** E3 (`gate_passed`) and E4 (`_evaluate_gate`) are the two SEPARATE consumers of the SAME
advisory mechanism; E4 exists because E3's fix was verified against the wrong consumer.

**Verified against the actual git commits:**

- E3 fix `eb9a2633` "fix(prd): make parallel-instructions gate advisory (warn, don't halt) (#155)" —
  `git show --stat`: touches `cli/pipeline/gates.py` (+16), `cli/pipeline/models.py` (+9 → adds
  `SemanticCheck.advisory`), `cli/prd/gates.py` (+13). **This is the commit that INTRODUCED the
  advisory mechanism in `gate_passed`.**
- E4 fix `b97c9960` "fix(prd): honor advisory checks in the executor's `_evaluate_gate`" — mirrors the
  same advisory branch into `PrdExecutor._evaluate_gate` (the live PRD path that never calls
  `gate_passed`). The commit message (research/05 L218–220) states verbatim: "PR #155 added
  advisory-check handling to `pipeline.gates.gate_passed`, but the PRD executor never calls
  `gate_passed`."

So the test files' framing (E3 = `gate_passed` consumer, E4 = `_evaluate_gate` consumer, both of the
SAME `SemanticCheck.advisory` mechanism, E4 existing because E3 hardened the wrong consumer) is
**consistent with git reality and with §8.3's E4 wording.** `test_backtest_e3.py:11` and
`test_backtest_e4.py:3` cross-reference each other as the "dual-evaluator pair," matching
research/05 §summary L304–308. **No defect.**

This is the most adversarially-suspicious framing in the set (see Observation O-1 for the spec-§3.1
narrative tension that does NOT rise to a defect).

---

## Concern 4 — class-bound `_evaluate_gate` invocation genuinely returns False — PASS

**Claim:** The OLD=MISS snippet correctly handles the class-bound `_evaluate_gate` (SimpleNamespace
self / unbound call) and genuinely shows it returns False despite the advisory flag.

**Verified by reading the pre-fix body at `1b0264f1`
(`git show 1b0264f1:src/superclaude/cli/prd/executor.py`, lines 825–862):**

```
def _evaluate_gate(self, step_id, gate, content) -> bool:
    if gate.min_lines > 0: …                      # skipped: snippet sets min_lines=0
    if gate.semantic_checks:
        for check in gate.semantic_checks:
            result = check.check_fn(content)
            if result is not True:                # advisory NEVER read at the parent
                msg = result if isinstance(result, str) else check.failure_message
                self._diagnostics.record_gate_failure(step_id, msg, gate.enforcement_tier)
                self._logger.log_gate_result(step_id, False, msg)
                return False                       # ← OLD=MISS witness
    …
    return True
```

**Snippet (`test_backtest_e4.py:49–70`) traced against that body:**

- L53 `_fn = E.PrdExecutor._evaluate_gate` — unbound function; invoked at L64 as
  `_fn(_self, "build-task-file", _gate, "content…")`. Signature `(self, step_id, gate, content)`
  matches the pre-fix definition exactly. **Class-bound handling correct.**
- L54–57 `_self = SimpleNamespace(_diagnostics=…record_gate_failure…, _logger=…log_gate_result…)` —
  provides exactly and only the two attributes the failing branch touches. **No AttributeError;
  stubs match the real attribute access (`self._diagnostics.record_gate_failure`,
  `self._logger.log_gate_result`).**
- L58–62 `_chk.check_fn = lambda c: "parallel_instructions failed"` returns a **string** →
  `result is not True` is True → enters the failing branch → `return False`. `advisory=True` (L61) is
  set but the pre-fix loop never reads it. **Genuinely reproduces "halts despite advisory."**
- L63 `_gate = SimpleNamespace(min_lines=0, …, semantic_checks=[_chk])` — `min_lines=0` skips the
  line-count branch; content is 2 lines via `chr(10)` joins. Clean.
- L68 `"halted_despite_advisory": (_ret is False)` — the assertion at L79 checks this is `True`.

The `json` reference at L65 resolves: `run_prefix_replay_snippet` prepends a prelude
`import sys, json` (`replay_executor.py:220–221`) before exec'ing the snippet in a fresh subprocess
whose `sys.path[0]` is the checked-out parent's `src/` (`:218–233`). **Not a NameError.** This
adversarial trap (snippet uses `json.dumps` with no in-snippet `import json`) is CLEAN.

**No defect.** The replay is a genuine in-process invocation of the real pre-fix callable, not theatre.

---

## Observations (do NOT change the PASS verdict)

### O-1 (MINOR — doc/narrative tension, not a code defect)

The test files frame E3's mechanism as the **advisory-severity escape in `gate_passed`**
(`test_backtest_e3.py:1–14`). The RELEASE-SPEC **§3.1 mechanism column** instead describes E3 as
"Single reported heading fixed while same-token sibling headings remained unswept" (the
**unmask-and-sweep** escape), and the §8.3 E3 row is "Replay Task-Log/Findings sibling-heading
artifact … `K_swept == K_true`."

Resolution: this is a known spec-internal layering, NOT a test error. The E3 *fix commit* `eb9a2633`
genuinely does BOTH — it adds the advisory mechanism (the OLD=MISS half the snippet replays) AND is
the wave-H3 sweep escape (the NEW=CATCH `unmask-and-sweep.md` proxy the test asserts, L103–113).
`test_backtest_e3.py:11–14` explicitly reconciles this: "E3 and E2 both proxy `unmask-and-sweep.md`
but assert DISTINCT facets: E3 = sweep + WARN/CONTINUE severity." So the E3 OLD=MISS (advisory) and
E3 NEW=CATCH (sweep) describe two facets of one commit. The framing is internally coherent and
matches §8.3; the only residual is that a reader comparing §3.1's E3 *mechanism* prose to the test's
OLD=MISS docstring could see surface dissonance. MINOR, documentation-clarity only.

### O-2 (informational — ledger consumer set is a 2-of-4 subset)

The §3.1 E4 evidence-card column requires the H2 ledger classify FOUR live consumers: "generic gate,
PRD evaluator, **trailing gate, remediation dispatch**" (research/04 §4.3 L175–176 flags only 2 of 4
are CODE-VERIFIED). The NEW=CATCH proxy (`test_backtest_e4.py:102–104`) asserts only `gate_passed`
and `_evaluate_gate`. This is **faithful to §8.3** (which names exactly those two) but is a strict
subset of §3.1's four. Not a defect for these tests — the §8.3 oracle is the one the test maps to
("Maps 1:1 to §8.3 'E4'", L18) — but the impl tasklist that authors `contract-enumeration.md` should
ensure the ledger ref itself enumerates all four consumers, else the H2 ledger-completeness gate
under-counts. Out of scope for this domain QA (the ref is greenfield); flagged for the impl author.

### O-3 (non-defect — adversarial trap cleared)

The E4 wave is `H2` while E3 is `H3` (`test_backtest_e4.py:85` vs `test_backtest_e3.py:94`), even
though the two are the "dual-evaluator pair." This is CORRECT, not a contradiction: per spec §3.1 the
advisory dual-evaluator gap (E4) closes under H1/H2 (the runtime-entrypoint + consumer-ledger waves),
whereas the sibling-heading sweep facet (E3) closes under H3 (the unmask/sweep classifier wave). The
pair-ness is about the shared `SemanticCheck.advisory` mechanism, not a shared closing wave. Both
wave tags match `git_replay.py:51–53` and §3.1/§8.3. CLEAN.

---

## Self-Audit

**(a) Reliance list — items where I relied on prior research instead of re-deriving:**

- Relied on research/05's per-escape fix↔parent SHA table only as a *starting hypothesis* — I
  re-verified the E4 row (`b97c9960^ == 1b0264f1`, ancestry of HEAD) directly via git.

**(b) Independent semantic checks (≥1 required):**

- E4 pre-fix `_evaluate_gate` body re-read at the pinned parent via
  `git show 1b0264f1:src/superclaude/cli/prd/executor.py` (lines 825–862) and exec-traced against the
  snippet — confirmed `return False` on the advisory check; NOT taken on the research's word.
- `b97c9960` ancestry, `20693bb8` ancestry, `1b0264f1 == b97c9960^`, and branch-containment of
  `b97c9960` re-run live with `git merge-base --is-ancestor` / `git branch -a --contains` — confirmed
  unmerged + HEAD-healed independently.
- E3 mechanism re-derived from `git show eb9a2633` (commit message + `--stat`) — confirmed it is the
  commit that introduced `SemanticCheck.advisory`, grounding the dual-consumer framing in git, not in
  the research narrative.
- `json` NameError trap re-checked by reading the actual prelude in `replay_executor.py:218–233` —
  not assumed.
- Pre-fix `GateCriteria` / `SemanticCheck` / `gate_passed` shapes re-read at `e97aa4fd` to confirm the
  E3 snippet's constructor + call match the parent's dataclass fields.

---

## Confidence

- **Confidence:** Verified: 4/4 concerns | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 7
- Tool-engagement note: 4 source/research Reads + replay_executor Read; 7 Bash invocations each
  mapped to a specific claim (json prelude, E4 ancestry block, git_replay SHAs, pre-fix
  `_evaluate_gate` body, E3/E4 wave tags, E3 fix commit, spec §3.1/§8.3 verbatim, HEAD heal + branch
  containment). No padding calls.
- Web research performed: none (all checks local git + source).

## QA Complete
