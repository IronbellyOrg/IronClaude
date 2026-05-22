# Adversarial Debate Transcript (--depth quick, --focus correctness,risk,test-coverage)

**Format**: 3 rounds, FIX-A advocate vs FIX-B advocate, plus a neutral judge.

## Round 1 — Correctness

**FIX-A advocate**: Both fixes close the exact bug. FIX-A is one line; FIX-B is a signature change. Equal correctness for the reported symptom.

**FIX-B advocate**: FIX-A leaves the footgun in the API. Any future CLI surface that imports `resolve_scratch_root` and passes its `--output-dir` to the kwarg recreates the bug. FIX-B is the only structurally correct answer.

**Judge**: Both fixes are correct for the symptom. FIX-B is structurally more defensive but FIX-A + the parity test (already proposed by quality-engineer) achieve equivalent forward-defense at a fraction of the surface area.

**Round 1 winner**: tie on correctness for the symptom; FIX-B wins on API hygiene; FIX-A wins on minimal-change-for-correctness.

## Round 2 — Risk

**FIX-A advocate**: Lowest possible blast radius. The kwarg still exists for the documented legitimate use case (programmatic callers extending the allowlist for sub-path checks). Removing it changes a public-ish API that scratch-roots.md and `test_output_dir_is_call_scoped_not_persistent` explicitly endorse.

**FIX-B advocate**: The "legitimate use case" is precisely the one that the runtime_config pattern at commands.py:1490-1499 already covers more clearly. Keeping the kwarg keeps the trap baited.

**Judge**: FIX-B's risk is non-trivial — `test_output_dir_is_call_scoped_not_persistent` documents an explicit, presumably tested behavior. Invalidating documented behavior to fix a misuse of that behavior is over-reach. Hard to motivate as the *first* response to a live security hole. A follow-up refactor PR can do the API-hygiene work with proper deprecation; the live bug needs FIX-A now.

**Round 2 winner**: FIX-A.

## Round 3 — Test coverage

**FIX-A advocate**: Both fixes need the same regression + parity tests. FIX-B additionally needs to update or delete `test_output_dir_is_call_scoped_not_persistent` and audit every in-tree caller — strictly more test work.

**FIX-B advocate**: Concede.

**Round 3 winner**: FIX-A.

## Final tally
- Correctness: tie (with FIX-B preferable in the abstract, FIX-A preferable in context)
- Risk: FIX-A
- Test coverage: FIX-A

**Selected fix**: **FIX-A**. Open the door for FIX-B as a follow-up refactor task (with proper deprecation cycle) — but the immediate live security hole gets the minimal-surface fix.
