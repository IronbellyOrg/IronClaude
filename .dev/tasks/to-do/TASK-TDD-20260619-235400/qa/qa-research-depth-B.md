# QA Report — Research Depth Review (Heavyweight TDD), Partition B

**Topic:** ReflectHardening FR-RH2 — swarm/reflect ensemble re-wiring
**Date:** 2026-06-20
**Phase:** report-qualitative (research-depth gate, adversarial stance)
**Fix cycle:** N/A (`fix_authorization: false`, report-only)
**Partition:** B of N (assigned files 05, 06, 07, 08, web-01)

---

## Overall Verdict: PASS

All five assigned research files clear the Heavyweight-TDD depth bar. The four
named depth criteria (ResultContract field enumeration, LensEntry shape,
mock-gap mechanics, adversarial-handoff actionability) are each satisfied at the
"a TDD author could write the design section without re-opening the source"
level, and every load-bearing citation I spot-checked against live source was
exact. Web-01 is genuinely supplementary, not padding. I went in expecting
"structurally complete but shallow" and could not sustain that charge against
the evidence.

---

## Items Reviewed

| # | Depth criterion | Result | Evidence |
|---|-----------------|--------|----------|
| 1 | ResultContract / return-contract.yaml field enumeration substantive (every field + type) | PASS | File 05 §3 enumerates all 19 fields with name+type+default+semantics; nested ContractTarget (4 sub-fields) + WorkerResult (DM-013, §4, 13 fields) + DoneSentinel (DM-017, §5, 3 fields) + Artifacts (DM-018) each broken out. Verified against `models.py` L997-1015 (19 fields exact), L876 frozen dataclass, INV-005 deferral L982-986. |
| 2 | LensEntry shape fully specified (all fields, suspect/tier/next-command convention, validator assertions) | PASS | File 06 §1 enumerates all 14 LensEntry fields; §2 gives the bare_review literal byte-for-byte; §4 enumerates all 6 validator assertions with RULE ids + helper line refs; ResolvedLensEntry 9-field subset called out. Verified `models.py` L707-720 (14 fields exact incl. `normalizer_strategy`), `bare_review.py` L40-75 (every value exact). |
| 3 | Mock-gap mechanics concrete (HOW conftest ClaudeProcess mock copies canned fixture) | PASS | File 07 §3 traces `make_claude_process_stub` build-time `read_bytes` → `_wait()` closure `write_bytes(fixture_bytes)` → `mock.wait.side_effect = _wait`, names the exact gap ("byte-for-byte copy of a hand-authored fixture"). Verified `conftest.py` L98-138 line-exact; `pass.yaml` L4 `tier_reached: 2` confirmed. |
| 4 | Adversarial handoff actionable (HOW ensemble.py hands final_path artifacts to /sc:adversarial Mode A) | PASS | File 08 §1.3 + §4.3 give the literal `succeeded_final_paths` filter, `suspect_files`/`compare_files` construction, and the 5-step in-process handoff. Verified `commands.py` L2066-2081 line-exact. The `--suspect-source` undocumented-in-adversarial-SKILL gap is correctly surfaced as `[CODE-CONTRADICTED]` (grep: 0 `suspect` hits confirmed). |
| 5 | web-01 genuinely supplementary (not padding) | PASS | Explicit scope-note "LIGHT supplementary grounding for §21 + §6 ONLY… codebase is source of truth"; each finding tagged HIGH/MEDIUM with a URL and a one-line relevance tie to a specific TDD section; backend disclosed (Tavily MCP); honest open-question about no second-backend cross-check. Informs the in-process-vs-subprocess design decision, does not invent requirements. |

---

## Summary

- Checks passed: 5 / 5 (the four named depth criteria + web-01 supplementary test)
- Checks failed: 0
- Critical issues: 0
- Independent code verifications performed: 8 source reads/greps (see Self-Audit)
- Issues fixed in-place: 0 (report-only)

---

## Why this is NOT "structurally complete but shallow"

The adversarial charge I was asked to prove is that the research could be a
well-formatted skeleton — field tables present but hollow, mechanics named but
not traced. I tested that charge on the highest-risk surfaces and it failed:

1. **The field tables carry semantics, not just names.** File 05's ResultContract
   table doesn't stop at `merged_path: Optional[str]` — it states the null
   condition (`mode≠normalize+merge OR M<2`), distinguishes the *rendered*
   `recommended_next_command` from JobSpec's *unrendered* `*_template`, and flags
   the INV-005 emitter-vs-dataclass enforcement seam (verified at `models.py`
   L982-986). A shallow file would list the type and move on; this one explains
   why the type is what it is.

2. **The mock-gap is traced as a causal chain, not asserted.** File 07 doesn't
   say "the mock copies a fixture" — it walks build-time eager `read_bytes`
   (L117-119) → the `_wait()` closure that does the `mkdir`+`write_bytes`
   (L127-131) → the `side_effect` wiring (L133), then connects it to the exact
   fixture constant (`pass.yaml` L4 `tier_reached: 2`) and draws the
   representational-bias conclusion ("the test and the thing-under-test share the
   same fabricated witness"). That is the depth a Heavyweight TDD's
   test-strategy section needs to justify FR-RH2.5's StubTransport boundary.

3. **The handoff is given as copy-pasteable mechanics with the real precedent
   line-cited.** File 08 §1.3 reproduces the `succeeded_final_paths` list
   comprehension and the `setdefault` substitutions, then §4.3 turns them into a
   numbered 5-step ensemble.py procedure, AND honestly flags the load-bearing
   contradiction that `--suspect-source` is emitted by the swarm side but not
   parsed by `/sc:adversarial` (verified: 0 hits). A shallow file would have
   copied the "recommended next command" string and assumed Mode A consumes it.

4. **The "to-be-built" honesty is correct, not a depth dodge.** All four
   substantive files correctly tag `ensemble.py` and
   `test_ensemble_stub_integration.py` as not-yet-existing (verified: both absent
   from the tree) and frame their prescriptions as design targets grounded in
   shipped precedents (`bare_review.py`, `commands.py` L2066-2081,
   `test_commands_run.py` L507-568 — the last verified to contain `results=3` +
   `worker_done`×3). This is exactly the right posture for TDD-feeding research:
   distinguish what exists from what the TDD must specify, without leaving the
   "what to specify" hollow.

---

## Minor observations (non-blocking, not findings against the verdict)

These are surfaced for the TDD author's benefit; none rises to even MINOR
severity against the depth criteria, because each is already explicitly flagged
*by the research itself* in a Gaps section.

- **O1 — Recipe binding for `reflect-review` is an open dependency.** File 06
  Gaps correctly flags that validator assertions 2 & 6 (`recipe_name`,
  `normalizer_strategy`) require a *registered* recipe, and that `recipes/` was
  out of read scope. The TDD must pin the recipe binding; the research already
  says so. (Depth-neutral: the file is honest about its own boundary rather than
  bluffing a recipe name.)
- **O2 — OI-1 reflect-side field table completes in synth-04.** File 05 §7 builds
  the swarm→reflect correspondence table by reading `reflect/contract.py`
  directly because `02-reflect-contract-verdict.md` is a stub. This is a
  cross-file dependency the orchestrator should confirm lands in synthesis; it is
  not a depth deficiency in file 05 (which over-delivers by sourcing the reflect
  fields itself).
- **O3 — `ensemble.py` API surface names are inferred.** Files 07/08 infer
  witness field names (`reviewer_count`, diversity) from `derive_verdict`'s
  existing triggers and explicitly tag them `[UNVERIFIED]` pending the TDD's
  canonical naming. Correct labeling; the TDD owns the final names.

[PARTITION NOTE: Cross-file checks limited to assigned subset (05, 06, 07, 08,
web-01). The OI-1 join (file 05 §7) and the reflect-side contract table
(`02-reflect-contract-verdict.md`, synth-04) fall outside this partition; full
cross-file correspondence verification requires merging all partition reports.]

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** Eight
   distinct verifications: (a) `models.py` L876/L997-1015 — ResultContract is a
   19-field frozen dataclass, field names/types/defaults match file 05's table;
   (b) `models.py` L636/L707-720 — LensEntry is a 14-field dataclass including
   `normalizer_strategy`, matching file 06; (c) `merge.py` full file —
   `mechanical_merge` 8-LOC body + boundary docstring match file 05 §2 verbatim;
   (d) `conftest.py` L98-138 — `make_claude_process_stub` `_wait()` fixture-copy
   mechanics match file 07 §3 line-exact; (e) `pass.yaml` — L4 `tier_reached: 2`
   and the cited diversity/merge fields confirmed; (f) `bare_review.py` L40-75 —
   every LensEntry literal value matches file 06 §2; (g) `commands.py`
   L2066-2081 — the `succeeded_final_paths`/`suspect_files`/`compare_files`
   handoff matches file 08 §1.3 line-exact; (h) absence checks — `ensemble.py`,
   `test_ensemble_stub_integration.py` confirmed absent; `suspect-source` 0 hits
   in adversarial SKILL; `test_commands_run.py` L507 `results=3`+`worker_done`×3
   confirmed present.
2. **What specific files read to verify claims?**
   `src/superclaude/cli/swarm/models.py` (two ranges),
   `src/superclaude/cli/swarm/merge.py`,
   `src/superclaude/cli/swarm/lenses/bare_review.py`,
   `tests/cli/reflect/conftest.py`,
   `tests/cli/reflect/fixtures/pass.yaml`,
   `src/superclaude/cli/swarm/commands.py` (L2055-2089), plus greps over
   `src/superclaude/cli/reflect/`, `tests/cli/reflect/`,
   `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`, and
   `tests/swarm/test_commands_run.py`.
3. **If I found 0 blocking issues, why trust that I checked thoroughly?**
   Because I did not take the research's `[CODE-VERIFIED]` tags on faith — I
   independently re-derived the four highest-risk claims (the 19-field count, the
   mock-gap `_wait()` chain, the bare_review literal, the commands.py handoff)
   from live source, and I actively tried to falsify the `--suspect-source` and
   `ensemble.py`-exists claims via grep/ls (both confirmed the research's own
   contradiction/absence flags). The research survived adversarial verification;
   the PASS is earned, not granted. Every PASS row above cites a specific file
   and line range I read this session.
4. **Web research / Tavily?** No web research performed during *this QA review* —
   all verification was local-source-bound. (The reviewed file web-01 itself
   discloses Tavily MCP as its backend; I verified its internal honesty markers,
   not its external URLs, which is appropriate for a depth/supplementary-relevance
   judgment.)

### Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 3 | Glob: 0 | Bash: 3
- Tool-engagement count (≥11 read/grep/bash calls) exceeds the 5 depth-criteria
  items — not suspect-low.

---

## Recommendations

- **Proceed to TDD authoring.** Partition B's research depth is sufficient for a
  Heavyweight TDD. The four named criteria are met at design-actionable depth.
- Carry observations O1 (recipe binding), O2 (OI-1/synth-04 reflect-side table),
  and O3 (canonical `ensemble.py` field names) into the TDD's Open Questions /
  Gaps section — they are real downstream dependencies that the research has
  already and correctly flagged, and the TDD must close them rather than inherit
  them silently.
- Orchestrator: merge this partition report with the other partition(s) before a
  global research-depth verdict; the OI-1 cross-file join is out of B's scope.

## QA Complete
