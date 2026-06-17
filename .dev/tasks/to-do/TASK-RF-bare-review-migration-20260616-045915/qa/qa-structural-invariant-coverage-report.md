# QA Report — Phase Gate 4: Structural Invariant-Coverage Lens

**Topic:** sc-bare-review M8/M9 migration — rebuilt CLI-vs-frozen-golden parity gate
**Date:** 2026-06-16
**Phase:** report-validation (invariant-coverage lens of PG4)
**Fix authorization:** FALSE (report only — no files modified)
**Adversarial stance:** Assumed ≥3 of 5 invariants were dropped. Hunted for absence, weakening, and false-CLI-driving.

---

## Overall Verdict: PASS

All 5 substantive invariants are PRESENT, CLI-driven against the live CLI's on-disk
outputs / nested contract, and exercised across all 3 scenarios (all-success,
partial-with-timeout, salvage-promoted). The live suite runs green (16 passed).
The FR-028 salvage divergence is adjudicated **(a) acceptable** — see adjudication below.

---

## Per-Invariant Present/Absent Table

| # | Invariant | Present | CLI-driven? | Real (not weakened)? | Evidence (file:line) |
|---|-----------|---------|-------------|----------------------|----------------------|
| 1 | Per-reviewer `.md` byte-equality vs frozen golden | PRESENT | YES — reads on-disk `bare-review-*.final.md` | YES — full multiset string equality `sorted(cli_bodies) == sorted(golden)`, NOT substring | test L284-291 (read live `.final.md`), L329 (`assert sorted(cli_bodies)==sorted(golden)`); `<<TARGET>>`/`<<OUTPUT_DIR>>` sentinel norm L279-282 applied symmetrically to both sides |
| 2 | Aggregate IMM-5 status from CLI contract | PRESENT | YES — live `return-contract.yaml` `status` | YES | test L362-366; live contract emits `status` (verified live dump: `status=success`); expected success/partial/success L213-217 |
| 3 | Per-slot status set + M/N counts from CLI contract | PRESENT | YES — `output_files[].status`, `workers_succeeded`, `workers_requested` | YES | test L394-406; live contract carries `workers_succeeded`/`workers_requested` (verified live dump), `output_files[].status` (live dump shows per-slot `status`) |
| 4 | `suspect:true` + adversarial handoff FROM CLI contract | PRESENT | YES — `caller_metadata.suspect` + `recommended_next_command` | YES — asserts CLI-emitted contract surface, NOT the lens template | test L436-448; live dump: `caller_metadata={'suspect':True,'tier':'T2'}`, `recommended_next_command` contains `/sc:adversarial … --suspect-source …`. Closes the old gate's lens-template asymmetry (research §1.4, §4.7-4) |
| 5 | `output_files` length == requested workers (3) | PRESENT | YES — `len(output_files)` | YES | test L475-478; live dump: `output_files` len 3 |

**Coverage matrix (invariant × scenario):** every invariant is `@pytest.mark.parametrize`'d over
all 3 SCENARIOS (test L306-310, L341-345, L374-378, L414-418, L456-460) → 15 parametrized cases +
1 injection-guard test = **16 tests, all PASS** (live run below).

---

## Adversarial Findings — what I tried to break, and the outcome

### F1 — Live contract uses DIFFERENT field names than the golden contract.yaml (NOT a defect)
The frozen golden `return-contract.yaml` uses **`reviewers_requested`/`reviewers_succeeded`** and a
**top-level `suspect:`** (e.g. `golden/all-success/return-contract.yaml:6-7`, and `suspect: true` at
top level). The **live CLI** emits a **nested schema**: `workers_requested`/`workers_succeeded` and
`caller_metadata.suspect` (verified by live runtime dump). The test asserts invariants 2–5 against the
**LIVE** contract's nested keys (`workers_*`, `caller_metadata.suspect`) — which exist and are correct
— and **never compares the contract.yaml to the golden**. Only the per-reviewer `.md` bodies are
golden-compared (invariant 1). This is internally consistent and exactly what the module docstring
claims ("the live CLI `return-contract.yaml` (nested schema) is parsed", test L41-43).
**Note for the record:** the spawn prompt and research §4.7-3 name `reviewers_succeeded`/
`reviewers_requested`; the actual live contract (and therefore the correct assertion) uses
`workers_succeeded`/`workers_requested`. The test got the live names right. **Not a coverage hole.**

### F2 — Invariant 1 could have been a weakened substring check (it is NOT)
Confirmed real equality: `assert sorted(cli_bodies) == sorted(golden)` (test L329) is a full
list-of-strings multiset comparison. Sentinel normalization (`<<TARGET>>`, `<<OUTPUT_DIR>>`, test
L279-282) is applied symmetrically to both sides, so it cannot mask a real divergence (the absolute
target/output paths are the only non-portable fields). Live body dump confirms the sentinel is actually
present post-normalization (`target: "<<TARGET>>"`).

### F3 — Invariant 4 could have asserted only the lens template (it does NOT)
The OLD gate's documented asymmetry (research §1.4, §4.7-4) was that the new side checked
`LENSES["bare-review"].suspect` / `recommended_next_command_template` rather than a CLI contract.
The rebuilt gate asserts `contract["caller_metadata"]["suspect"]` and `contract["recommended_next_command"]`
(test L436, L440) — the consumer-visible CLI-emitted surface. Asymmetry CLOSED.

### F4 — Driving the CLI for real (not a library shortcut)
`_run_cli` (test L226-291) calls `runner.invoke(swarm_group, ["run","--lens","bare-review", … "--transport","stub"])`
(L256-271), monkeypatches `commands._resolve_run_transport` → fixture-fed `StubTransport` (L240-247)
and `recipes.bare_review_v1.iso_now` → `FIXED_GENERATED` (L250-253), then reads on-disk artifacts.
Zero `t2_normalize`/`LEGACY_SCRIPT`/`importlib`/`skipif` in executable code (only docstring prose at
L13-46) — the gate genuinely survives WS-C deletion. **This is a true end-to-end CLI gate.**

---

## FR-028 Adjudication (the documented divergence PG4 must assess)

**STANCE: (a) ACCEPTABLE.** Driving `salvage-promoted` as three plain-success reviewers (CLI emits
`success`/M=3, body byte-identical to golden) — rather than scripting a real `parse_error` slot and
asserting the divergent `partial`/M=2 — is a **sound invariant-coverage choice for a parity-vs-golden
gate.** Justification with evidence:

1. **A parity-vs-golden gate's contract is "match the golden," full stop.** The frozen golden for
   `salvage-promoted` is `status: success`, `reviewers_succeeded: 3`, 3 bodies
   (`golden/salvage-promoted/return-contract.yaml:2,6-7`; 3 `.md` files on disk). The gate's job is to
   prove the live CLI reproduces that golden. Baking the FR-028 *gap* into the gate (asserting
   `partial`/M=2) would make the gate assert a NON-golden outcome — defeating its own purpose. The
   task log explicitly records that the subagent's intermediate attempt to assert `partial`/M=2 was
   **correctly rejected** (task file L751).

2. **The root cause is a genuine, separately-tracked SOURCE concern — not a test gap.** Verified
   independently: `normalize_wave2` forwards ONE shared `recipe_args` to every worker with no
   per-worker `status` (`src/superclaude/cli/swarm/normalize.py:548-558`), while the recipe reads
   `args.get("status","success")` (`recipes/bare_review_v1.py:249`) and only enters its §7.4 salvage
   branch when `status == "parse_error"` (`bare_review_v1.py:278-286`). So on the CLI path the recipe
   ALWAYS sees `status="success"` and the `parse_error→success` promotion is **structurally
   unreachable**. This is the same shared-`recipe_args` root cause as PG2's C2. It is documented inline
   (test L175-212), as a HIGH-priority Follow-Up (task file L790), and the fix
   (`args = {**recipe_args, "status": worker.status}`) touches the SHARED resume path + all lenses —
   correctly OUT of scope for this test-only WS-B step, and flagged for its own corrective task with
   full-suite QA.

3. **The body byte-equality (invariant 1) is genuinely preserved, not faked.** Verified: the rendered
   frontmatter contains NO `salvaged` field (`bare_review_v1.py` frontmatter dict L295-307 — grep for
   `salvaged` returns no frontmatter key), and the `salvaged` flag affects only the returned
   `NormalizedResult.salvaged`, never `text`. So a salvage-promoted body and a plain-success body of the
   same raw input are **byte-identical by construction**. Driving salvage-as-success does NOT lose
   body-render coverage — invariant 1 still proves the salvage fixture renders byte-for-byte to golden.

4. **The salvage-flag logic itself is NOT left uncovered.** The recipe's §7.4 `parse_error→success`
   branch (`bare_review_v1.py:278-286`) remains unit-tested in `tests/swarm/test_recipe_bare_review.py`
   (task file L751, L790). The parity gate is the wrong layer to exercise it given the CLI path can't
   reach it.

**Why this is NOT a coverage hole that must block:** the gate correctly asserts golden parity; the
FR-028 contract-promotion gap is a *source* divergence (un-reachable promotion via shared
`recipe_args`), surfaced, root-caused, inline-documented, recipe-unit-tested, and tracked as a
HIGH-priority follow-up with the correct (shared-path) scope. Forcing the gate to assert the divergent
`partial`/M=2 would corrupt a parity gate into asserting a non-golden outcome. The honest, auditable
choice was made.

---

## Live Verification (tool evidence)

```
uv run pytest tests/swarm/test_bare_review_parity.py -v
→ 16 passed in 0.35s
```
(15 parametrized invariant cases across 3 scenarios + 1 injection-guard test; all green.)

Live contract runtime dump (all-success) confirmed nested keys exist:
`status`, `workers_requested=3`, `workers_succeeded=3`, `output_files` (len 3, each with `status`),
`caller_metadata={'suspect':True,'tier':'T2'}`, `recommended_next_command` containing
`/sc:adversarial … --suspect-source …`. Live body[0] head shows `target: "<<TARGET>>"` (sentinel
normalization exercised).

---

## Summary
- Invariants present & CLI-driven: **5 / 5**
- Scenarios covered per invariant: **3 / 3**
- Checks failed: **0**
- Critical issues: **0**
- FR-028 adjudication: **(a) acceptable** — does NOT block
- Issues fixed in-place: 0 (fix_authorization=FALSE)

## Confidence
**Verified:** 5/5 invariants + FR-028 root cause + golden tree + live contract schema + live test run.
Confidence: **100%** (Verified: 8/8 sub-claims | Unverifiable: 0 | Unchecked: 0).
**Tool engagement:** Read: 2 | Grep: 6 | Glob: 0 | Bash: 6 (incl. live pytest run + live contract dump).
Tool calls ≥ checklist items; each call mapped to a specific invariant/claim. No web research required
(no external/URL/standards-bound claims in scope) — Tavily-first rule not triggered.

## QA Complete
