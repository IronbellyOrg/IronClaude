# QA Report — Structural Escape Mapping (per-escape §8.3 differential)

**Topic:** E1–E5 per-escape OLD=MISS / NEW=CATCH runners vs RELEASE-SPEC §8.3
**Date:** 2026-06-12
**Phase:** task-integrity (structural escape-mapping verification)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — no source file modified)
**Stance:** ADVERSARIAL — assumed >=5 errors; verified every claim against source.

---

## Overall Verdict: PASS (with 1 documented prompt-vs-spec discrepancy — see Finding D1)

The 5 per-escape runners are internally correct and self-consistent against the
git_replay registry, the _impl_guard ref-resolver, and research/05 + research/04.
Every one of the 5 VERIFY criteria as literally stated in the spawn prompt holds.

The adversarial search surfaced **one substantive discrepancy** and several
**near-miss traps that the code correctly avoids** (documented below as evidence
the review was not theatre). The discrepancy (D1) is between the **spawn prompt's
asserted mapping** and the spec's §3.1 Traceability Matrix — NOT an error in the
test files. Because the VERIFY criteria pin the mapping to §8.3 (not §3.1), and
the runners match §8.3 + the registry exactly, the binary verdict is PASS, but D1
is surfaced per Critical Rule 6 (never resolve a cross-source contradiction silently).

---

## VERIFY Criterion 1 — Each E1–E5 has BOTH an OLD=MISS test AND a NEW=CATCH proxy

| Escape | OLD=MISS test | NEW=CATCH proxy | Result |
|--------|---------------|-----------------|--------|
| E1 | `test_backtest_e1_old_protocol_misses_local_path_file` (e1:58) | `test_backtest_e1_new_gate_catches_via_h1_ref` (e1:79, `@requires_impl_ref`) | PASS |
| E2 | `test_backtest_e2_old_protocol_misses_final_phase_false_positive` (e2:69) | `test_backtest_e2_new_gate_catches_via_unmask_and_sweep_ref` (e2:91) | PASS |
| E3 | `test_backtest_e3_old_protocol_misses_advisory_severity` (e3:82) | `test_backtest_e3_new_gate_catches_via_unmask_and_sweep_ref` (e3:104) | PASS |
| E4 | `test_backtest_e4_old_protocol_misses_second_consumer` (e4:73) | `test_backtest_e4_new_gate_catches_via_contract_enumeration_ref` (e4:95) | PASS |
| E5 | `test_backtest_e5_old_protocol_misses_wrong_diff_surface` (e5:43) | `test_backtest_e5_new_gate_catches_via_effective_input_ref` (e5:68) | PASS |

Each OLD=MISS asserts `verdict == VERDICT_MISS and negative_witness is True`
(e1:75, e2:87, e3:100, e4:91, e5:64). Each NEW=CATCH is guarded by
`@requires_impl_ref(<ref>)` and reads the ref text. **Criterion 1: PASS.**

---

## VERIFY Criterion 2 — 1:1 wave mapping E1→H1, E2→H3, E3→H3, E4→H2, E5→H4

The `wave=` field passed into each `EscapeResult` AND the registry record both encode the wave.

| Escape | `EscapeResult(wave=…)` in OLD=MISS | Registry `REPLAY_ESCAPES` wave | Prompt-required | Result |
|--------|-----------------------------------|--------------------------------|-----------------|--------|
| E1 | `wave="H1"` (e1:69) | `"H1"` (git_replay:49) | H1 | PASS |
| E2 | `wave="H3"` (e2:81) | `"H3"` (git_replay:50) | H3 | PASS |
| E3 | `wave="H3"` (e3:94) | `"H3"` (git_replay:51) | H3 | PASS |
| E4 | `wave="H2"` (e4:85) | `"H2"` (git_replay:53) | H2 | PASS |
| E5 | `wave="H4"` (e5:58) | `"H4"` (git_replay:55) | H4 | PASS |

Every test-file `wave=` matches the registry, matches research/05 line 25 table,
and matches the prompt-required mapping. **Criterion 2 (as literally stated): PASS.**

### ⚠ Finding D1 (IMPORTANT, prompt-vs-spec, NOT a test-file error)

The spawn prompt and §8.3 use mapping **E1→H1, E4→H2**. But research/04 §1
(CONTRACT A = spec **§3.1 Traceability Matrix**, reproduced verbatim, lines 38/41)
gives a DIFFERENT "Closing Wave(s)" column:
- §3.1 **E1 → "H1, H2"** (not H1 alone)
- §3.1 **E4 → "H1, H2"** (not H2 alone)

So the spec internally carries TWO wave columns: §3.1 (multi-wave closure sets)
vs §8.3 (the single primary backtest wave each replay drives). The test files +
registry + research/05 all consistently use the **§8.3 single-wave** numbers,
which is the correct choice for a per-escape backtest runner (each replay drives
ONE gate). This is a real cross-source nuance the harness author must not confuse,
but it is NOT a defect in the 5 runners — they match the §8.3 column the prompt
pinned. Surfaced per Critical Rule 6. Recommendation: add a one-line comment in
git_replay.py noting "wave = §8.3 primary backtest wave; §3.1 lists broader
closure sets (E1/E4 also touch H1+H2)" so a future reader does not read the
single wave as contradicting §3.1.

---

## VERIFY Criterion 3 — Each OLD=MISS checks out the correct BARE parent sha, NO `^`

Each runner references `_E{n}.prefix_parent_sha`, which resolves via
`escape_by_id` → `REPLAY_ESCAPES` (git_replay:48–56). No test passes a literal
SHA or appends `^`; the checkout target is the bare registry value, passed
verbatim through `checkout_worktree`/`run_prefix_replay_snippet`.

| Escape | Prompt-required parent | Registry `prefix_parent_sha` | `^` present? | Result |
|--------|------------------------|------------------------------|--------------|--------|
| E1 | `94d5baa0` | `"94d5baa0"` (git_replay:49) | NO | PASS |
| E2 | `10723863` | `"10723863"` (git_replay:50) | NO | PASS |
| E3 | `e97aa4fd` | `"e97aa4fd"` (git_replay:51) | NO | PASS |
| E4 | `1b0264f1` | `"1b0264f1"` (git_replay:53) | NO | PASS |
| E5 | `d878bc6d` | `"d878bc6d"` (git_replay:55) | NO | PASS |

**No-`^` enforcement (independently confirmed):**
- git_replay docstring G1 CHECKOUT RULE (git_replay:8–13) explicitly forbids a
  runtime `^` ("double-decrements … 94d5baa0^ → ac80f176 … Never apply `^` at runtime").
- `checkout_worktree` passes `commitish` UNCHANGED (git_replay:160–161, 187–194:
  `["git","worktree","add","--detach",str(wt),commitish]` — no `^` concatenation).
- E1–E4 `_E{n}_SNIPPET` paths call `run_prefix_replay_snippet(_E{n}.prefix_parent_sha, …)`
  (e1:60, e2:71, e3:84, e4:78) — bare attribute, no `+ "^"`.
- E5 calls `checkout_worktree(_E5.prefix_parent_sha)` (e5:45) — bare, no `^`.
- skipif `missing_replay_commits([_E{n}.prefix_parent_sha])` (e1:27, e2:36, e3:33,
  e4:39, e5:35) also uses the bare value.

Cross-checked the 5 SHAs against research/05 line 21–25 table and research/04 §1:
all 5 match (E1 94d5baa0, E2 10723863, E3 e97aa4fd, E4 1b0264f1, E5 d878bc6d).
**Criterion 3: PASS.**

### Near-miss trap CORRECTLY AVOIDED (E2/E3/E5 interleave)
research/05 note + git_replay:45–47 flag that the history interleaves: E5's FIX
(`10723863`) is E2's PARENT, and E2's FIX (`e97aa4fd`) is E3's PARENT. An author
could easily have mis-pinned E2's parent to a fix sha. Verified the registry
keeps them distinct and correct: E2.parent=10723863 (=E5.fix, correct as a
parent), E3.parent=e97aa4fd (=E2.fix, correct as a parent). The interleave is
real and the pinning is right — not an error.

---

## VERIFY Criterion 4 — E4 base pinned to `1b0264f1` (NOT HEAD)

- Registry: `ReplayEscape("E4", "b97c9960", "1b0264f1", "H2")` — fix b97c9960
  UNMERGED, checkout target is the parent `1b0264f1` (git_replay:52–54).
- e4 replay uses `_E4.prefix_parent_sha` (= 1b0264f1) at e4:78, NOT `HEAD`.
- e4 module comment HEAD-DRIFT (e4:14–18) documents the load-bearing reason:
  the advisory-fatal bug is ALREADY HEALED on HEAD via `20693bb8`; the spec's
  `b97c9960` is unmerged; so replaying against HEAD would NOT reproduce the bug.
  This exactly matches research/04 §4.2 (lines 164–173) + checklist item 11
  (line 213): "literal E4 negative witness must replay against a pre-`20693bb8`
  tree." `1b0264f1` is pre-`20693bb8`, so the pinning is correct.
- skipif reason string (e4:42–44) explicitly states "Pinned to the pre-fix
  parent, NOT HEAD (HEAD already healed via 20693bb8)."

No occurrence of `HEAD` as the E4 checkout/replay target anywhere in e4.
**Criterion 4: PASS.** (This is the single highest-risk trap in the set; the
runner handles it correctly and documents it.)

---

## VERIFY Criterion 5 — Each NEW=CATCH gates on the correct ref AND asserts the DISTINCT facet

### Ref-gating (the `@requires_impl_ref(<ref>)` + the file read target)

| Escape | Prompt-required ref | `@requires_impl_ref(...)` | `HARDENING_REFS / "<ref>"` read | Result |
|--------|---------------------|---------------------------|---------------------------------|--------|
| E1 | runtime-entrypoint-verification.md | e1:78 | e1:81 | PASS |
| E2 | unmask-and-sweep.md | e2:90 | e2:93 | PASS |
| E3 | unmask-and-sweep.md | e3:103 | e3:106 | PASS |
| E4 | contract-enumeration.md | e4:94 | e4:97 | PASS |
| E5 | effective-input-proof.md | e5:67 | e5:70 | PASS |

`HARDENING_REFS` resolves to
`src/superclaude/skills/sc-troubleshoot-protocol/refs/` (_impl_guard:23–25),
which matches research/04 §0 line 23 (the 6 greenfield refs). All 5 ref
filenames are members of that 6-ref greenfield set. **Ref-gating: PASS.**

### Distinct-facet assertions (E2 word-boundary vs E3 sweep — the key disambiguation)

E2 and E3 BOTH proxy `unmask-and-sweep.md` (same ref) but must assert DIFFERENT facets:

**E2 = word-boundary facet (e2:95–100):**
- asserts `"incomplete" in low and "complete" in low` (e2:95)
- asserts `"word-boundary" in low or "word boundary" in low or "\\b" in text` (e2:98)
- This is the `complete` !=> `incomplete` word-boundary grammar — matches
  research/05 §E2(d) + §8.3 E2 ("complete vs incomplete discrimination").

**E3 = sweep + WARN/CONTINUE facet (e3:108–112):**
- asserts `"k_swept" in low or "swept" in low` (e3:108) — the K_swept==K_true sweep
- asserts `"warn" in low or "advisory" in low or "continue" in low` (e3:111) — severity
- This is the unmask/sweep coverage + severity-by-consumer rule — matches
  research/05 §E3(d) + §8.3 E3 ("K_swept==K_true … WARN/CONTINUE rather than HALT").

The two assertion sets are DISJOINT (E2 keys on word-boundary/`\b`; E3 keys on
swept/warn/continue). The runners' own docstrings call this out (e2:16–17,
e3:13–14: "assert DISTINCT facets"). **Distinct-facet: PASS.**

**Criterion 5: PASS** (ref-gating + distinct facets both hold).

---

## Additional adversarial cross-checks (OLD=MISS body asserts the §8.3 facet)

Beyond the 5 stated criteria, I verified each OLD=MISS body actually reproduces
the §8.3 escape mechanism (so the negative witness is not theatre):

- **E1** asserts `emits_local_file` (`--file` in argv AND local `_spec` path in
  argv) (e1:62, snippet e1:53) — the local-path-as-cloud-file escape. MATCH §8.3 E1.
- **E2** asserts `halted` AND `"Phase 5 missing parallel" in result` (e2:72–78) on
  a sequential completion final phase. NOTE: the runner's prose at e2:6/e2:114 in
  research/05 uses "Phase 7" as the example, but the e2 FIXTURE uses Phase 5
  (e2:55) — these are consistent (the fixture's max digit phase is 5). The
  digit-heading trap (e2:9–13) is correctly handled: fixture uses CONCRETE DIGIT
  headings so the pre-fix `Phase \d+` matcher collects them. MATCH §8.3 E2.
- **E3** asserts `halted` AND `"Semantic check 'parallel_instructions' failed" in
  reason` (e3:85–91) with a dynamically-tagged advisory check that the pre-fix
  gate ignores (snippet e3:60–62). MATCH §8.3 E3.
- **E4** asserts `halted_despite_advisory` (`_ret is False`) on an advisory-tagged
  check through the LIVE `_evaluate_gate` path (e4:79, snippet e4:58–68). MATCH §8.3 E4.
- **E5** asserts the two-dot `"<BASE>..HEAD" in text` source selector is present
  AND the fix's `"Do NOT use \`start_commit..HEAD\`"` prohibition is ABSENT at the
  parent (e5:48–55). MATCH §8.3 E5 (wrong-surface vacuous PASS).

All 5 OLD=MISS bodies reproduce the correct escape mechanism. No theatre.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | OLD=MISS + NEW=CATCH per E1–E5 | PASS | e1:58/79, e2:69/91, e3:82/104, e4:73/95, e5:43/68 |
| 2 | Wave map E1→H1,E2→H3,E3→H3,E4→H2,E5→H4 | PASS | EscapeResult wave= e1:69,e2:81,e3:94,e4:85,e5:58 + registry git_replay:49–55 |
| 3 | Bare parent sha, no `^` | PASS | git_replay:49–55 + checkout_worktree:187–194 + e1:60,e5:45 |
| 4 | E4 pinned 1b0264f1 not HEAD | PASS | git_replay:52–54 + e4:36/78 + skipif e4:42–44 |
| 5 | Ref-gating + distinct facets (E2 word-bdry vs E3 sweep) | PASS | e1:78–81,e2:90–100,e3:103–112,e4:94–97,e5:67–70 |
| D1 | §8.3 (single-wave) vs §3.1 (E1/E4 multi-wave) | NOTED | research/04 §1 lines 38/41 vs §8.3 / prompt |

## Summary
- Checks passed: 5 / 5 stated VERIFY criteria (+5 adversarial OLD=MISS body cross-checks)
- Checks failed: 0
- Critical issues: 0
- IMPORTANT findings: 1 (D1 — prompt/§8.3-vs-§3.1 wave-column nuance; NOT a test defect)
- Issues fixed in-place: 0 (report-only; fix_authorization=false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| D1 | IMPORTANT (advisory) | git_replay.py:48–56 | `wave` encodes §8.3 single primary wave; spec §3.1 lists E1+E4 as "H1, H2" multi-wave closure sets. No code defect, but a future reader could misread the single wave as contradicting §3.1. | Add 1-line comment: "wave = §8.3 primary backtest wave; §3.1 broader closure sets (E1/E4 also touch H1+H2)." Out of scope for this report (fix_authorization=false). |

## Actions Taken
None — report-only, no source file modified.

## Recommendations
- Binary verdict is PASS; the 5 runners may proceed.
- Optionally apply the D1 one-line clarifying comment (separate, authorized change)
  to pre-empt a §8.3-vs-§3.1 reader confusion. Non-blocking.

---

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 1
  (Read: 5 test files + research/05 + research/04 + git_replay + _impl_guard
  [9 Reads incl. report read-back]; Bash: 1 directory listing. No web research
  performed — all verification was source-truth-local, so no Tavily/WebSearch line.)
- Every VERIFY criterion checked with a specific file:line citation above.
- No UNCHECKED items. No UNVERIFIABLE items.
- Tool-engagement >= checklist items (9 Reads + 1 Bash vs 5 criteria): not suspect.

## QA Complete
