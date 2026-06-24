# Pinned Per-Escape Replay Table (AUTHORITATIVE)

Sources: RELEASE-SPEC §3.1/§8.3 + `research/08-gap-fill-reconciliation.md` (G1 tie-breaker) +
`research/05-replay-targets.md`. The `prefix_parent_sha` column is the **bare checkout target**
(resolved `<fix>^` once at authoring time per G1) — runtime checkout is `git checkout <prefix_parent_sha>`
with **ZERO caret arithmetic**.

| escape_id | fix_sha | prefix_parent_sha (CHECKOUT TARGET, no caret) | wave | §8.3 scenario | OLD=MISS callable | NEW=CATCH impl ref |
|-----------|---------|-----------------------------------------------|------|---------------|-------------------|--------------------|
| E1 | `7601ad25` | `94d5baa0` | H1 | E1 backtest | `_build_file_args` (class `PrdClaudeProcess`, `cli/prd/process.py`) | `runtime-entrypoint-verification.md` |
| E2 | `e97aa4fd` | `10723863` | H3 | E2 backtest | `_check_parallel_instructions` (module-level, `cli/prd/gates.py`) | `unmask-and-sweep.md` |
| E3 | `eb9a2633` | `e97aa4fd` | H3 | E3 backtest | `gate_passed` (module-level, `cli/pipeline/gates.py`) | `unmask-and-sweep.md` |
| E4 | `b97c9960` (**UNMERGED**) | `1b0264f1` | H2 | E4 backtest | `_evaluate_gate` (class `PrdExecutor`, `cli/prd/executor.py`) | `contract-enumeration.md` |
| E5 | `10723863` | `d878bc6d` | H4 | E5 backtest | POST-reflect range selector (`skills/task-builder/SKILL.md`) | `effective-input-proof.md` |

## Checkout rule (G1 — stated prominently)

> Runtime checkout is **`git checkout <prefix_parent_sha>`** — the bare pre-fix PARENT sha, with **NO `^`
> suffix, ever**. Applying `^` to a parent sha (e.g. `94d5baa0^` → `ac80f176`) **double-decrements** and
> replays one commit too early, producing a green-but-meaningless backtest (the escape's bug isn't even
> present at the double-decremented commit). The `prefix_parent_sha` values above are already
> `<fix>^`-resolved; no further caret arithmetic is applied at runtime.

## Cross-check / chain note

E5's fix `10723863` **is** E2's checkout parent; E2's fix `e97aa4fd` **is** E3's checkout parent. The
escapes are interleaved on the same linear history — this is why per-escape parent pinning (not a single
global `^`) is required. No sha is fabricated beyond research/08's authoritative table.

## E4 HEAD-drift caveat

E4's advisory-fatal bug is already **HEALED on HEAD** via `20693bb8`; the spec's `b97c9960` fix remains
**UNMERGED**. Replay E4 against pre-fix parent `1b0264f1` (where the bug IS present), **NOT HEAD**. Frame
E4 as the §8.3 H2 ledger-completeness assertion over BOTH `gate_passed` AND `_evaluate_gate` consumers.

## Shared-ref note (E2 + E3)

E2 and E3 both map to wave H3 and both proxy the same `unmask-and-sweep.md` ref, but assert DISTINCT
facets: E2 = word-boundary `complete` ⊄ `incomplete` classifier; E3 = sibling-heading unmask/sweep
`K_swept == K_true` + WARN/CONTINUE severity. Do not collapse the two.
