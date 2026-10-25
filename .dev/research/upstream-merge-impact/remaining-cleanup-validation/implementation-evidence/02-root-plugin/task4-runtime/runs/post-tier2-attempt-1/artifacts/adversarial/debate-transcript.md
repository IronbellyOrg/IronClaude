# Adversarial Debate Transcript

<!-- Assembled by the neutral sc:debate-orchestrator (Skill sc:sc-adversarial-protocol, Mode A). The orchestrator did not debate. Round 1, Round 2 and Round 2.5 were dispatched and persisted by the top-level pipeline driver. The round statements below are embedded verbatim from round-1/ and round-2/; only the heading levels were demoted to fit this document. Assembled 2026-10-24T20:12:49Z. -->

## Metadata
- Depth: standard
- Rounds completed: 2 debate rounds + Round 2.5 probe. Round 1 ran in parallel and Round 2 sequentially (A first, then B, with B seeing A's rebuttal). Round 2.5 was the invariant probe (single independent fault-finder, opus).
- Round 3: skipped (log: "Round 3 skipped: depth=standard")
- Convergence achieved: 83.3% diff-point agreement (25/30). The final status is **BLOCKED_BY_INVARIANTS**; see Convergence Assessment.
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2
  - Variant A (`variant-1-original.md`, reviewer 1) advocate: `sonnet:analyzer`. R1 agentId a44abd3634a7e5ae6, R2 agentId aacae5a74ec340cb7.
  - Variant B (`variant-2-original.md`, reviewer 2) advocate: `haiku:qa`. R1 agentId acb3a713412dd27cb, R2 agentId a64980251869bbd7d.
  - Fault-finder (Round 2.5): opus, agentId a78bf335f88ed2257, not an advocate.
- Diff points debated: 30 = S-001..S-008 (8) + C-001..C-015 (15) + X-001..X-003 (3) + promoted [SHARED-ASSUMPTION] A-002, A-005, A-006, A-007 (4)
- Shared-assumption response check: both advocates gave ACCEPT/QUALIFY/REJECT for A-002, A-005, A-006 and A-007 in both rounds. No `[OMISSION]` flags.

## Round 1: Advocate Statements

### Variant A Advocate (sonnet:analyzer)

Source: `round-1/advocate-A-sonnet-analyzer.md` (verbatim).

<!-- Round 1 statement. Advocate for Variant A (variant-1-original.md). Native Task worker (general-purpose), model slot: sonnet, persona: analyzer. agentId a44abd3634a7e5ae6. Persisted verbatim by the top-level pipeline driver. -->
#### Position summary
Variant A is the better-calibrated card for a deviation audit. It classifies D-1 as Drift but keeps the "adherent/no deviation" alternative open, it keeps every T-103 verdict inside what `spec.md`, `execution.log` and `invocations.yaml` support, and its one citation defect is small and doesn't change any verdict. Variant B has real strengths: a coverage statement, a drift link on the T-102 verdict, a correct critique of T1's G-2 citation, and more concrete test remediations. But its headline T-103 "overclaim" finding rests on a reading the evidence contradicts, and its Drift reasoning conflates "a narrower guard would suffice" with the Necessary test.

#### Steelman of Variant B
- **Coverage section.** B alone includes `coverage_audit` (variant-2:9). Its claim that `spec.md:1-3` is non-normative is correct (`spec.md:3` reads "synthetic audit input").
- **Linked T-102 verdict.** B's `statically_met_with_drift` (variant-2:7) ties D-1 to the T-102 verdict. A's plain "implemented (static only)" (variant-1:7) leaves the verdict and the deviation unlinked.
- **Correct G-2 critique.** B correctly notes that `execution.log:5` ("No test execution is claimed") does not prove tool unavailability. Only `invocations.yaml:3` does.
- **More actionable remediations.** B's tests/diff recommendations are concrete: replace the try/except, regenerate the diff, make `src` importable.
- **Per-gap flags.** `decision_needed_by_user` is a boolean on each gap, and a cleaner separation of the three gaps.
- **Unhedged classification.** The Drift call is decisive, which some consumers prefer.
- **Extra risks.** B surfaces risks A omits: whitespace input, non-string input, and any-ValueError acceptance.

#### Strengths claimed
1. **D-1 is calibrated and its elimination test is faithful.**
   - A runs the full four-class test: no approving artifact (Authorized fails), no forcing constraint (Necessary fails), no contradiction (not Regression) (variant-1:16).
   - It adds the counter-view that `not name` is a common idiom and might be no deviation. That is correct, because `spec.md:9` only requires rejecting an empty name and `greet('')` raises (`greeting.py:2-3`).
   - The `severity: LOW` field is defensible given that only non-str falsy inputs are affected.
2. **The T-103 verdict is bounded by the evidence.**
   - A's "implemented on disk, unrun, outside supplied diff" (variant-1:8) matches `task-to-work-map.yaml:30-32` (`in_supplied_diff: false`, `implemented_statically`).
   - It matches `execution.log:4`, which says the tests were created, and `execution.log:5`, which says no run is claimed.
   - R-003 (`spec.md:12`) says tests "MUST exercise the ordinary greeting and empty-input rejection". It does not say they must pass or have been run.
3. **A's recommendations target the root cause.**
   - Its first recommendation (variant-1:27) is aimed at the T1 card itself, with the rule-level verifier "every 'authorized' item cites an explicit approving artifact". The upstream error, which `t1-card.md:5-6` shows, is T1 calling D-1 authorized because it was mapped to a task.
   - Its guard remediation offers two paths: narrow the guard, or record a rationale or spec amendment (variant-1:28). B offers only the narrowing path.
4. **A's gaps name concrete hunk refs and use decision questions.**
   - A gives `hunk_ref` values (`tests/test_greeting.py:1`, and the tests file "outside changes.patch"), where B uses `none` three times.
   - `decision_needed_by_user` in A is a stated question, e.g. "whether static presence suffices for T-103 done".
5. **A raises shared-function coupling.** It notes that T-101 and T-102 share one function body. This is supported by `interaction-effects.yaml:5-7` and `:12` ("changing the guard at line 2 affects the R-001 path"), even though A's line range is wrong (see Concessions).
6. **Every other citation resolves.** The diff analysis (C-014) found no other defects in A's per-task, D-1 and gap citations.

#### Weaknesses identified in Variant B
1. **The completion "overclaim" misreads its own evidence.**
   - B says `completed.md:8` `[x]` and `tasklist_completion_pct 1.0` "overclaim acceptance" (variant-2:8).
   - `task-to-work-map.yaml:33` annotates the figure itself: "3/3 statically verified on disk". `completed.md:8` says T-103 "implements R-003 both ordinary and empty-input tests", and `execution.log:4` confirms the tests exist.
   - `spec.md:12` does not require a passing run, so "R-003 not accepted absent execution" (variant-2:23) imports a requirement the spec does not contain.
   - The map's own annotation also says the number is static, so it is not an acceptance pass either.
2. **B contradicts itself.**
   - The same T-103 verdict says "exercise is statically visible" (variant-2:8) and that completion is an overclaim.
   - If exercise is statically visible, R-003 as written is met statically. That is also why B's verdict is `static_cases_present...`.
3. **The Necessary test is misapplied.**
   - B's Necessary elimination is "`name == ""` would have sufficed" (variant-2:16).
   - Necessary under the protocol needs a documented forcing rationale. Whether a narrower alternative exists is not part of that test.
   - For `str` input `not name` is identical to `name == ""` (A-002). B's counterfactual therefore points only at non-str falsy values, and B never states that.
4. **Drift is stated without hedging.** `spec.md:9` does not forbid the idiom, and `greet('')` raises. B offers no no-deviation outcome (X-003). B's own recommendation hedges: "stop calling falsy broadening authorized".
5. **Some risks are unrelated to the guard.**
   - The whitespace risk concerns a behavior `not name` does not change. It is carried forward from `t1-card.md:24`, and B marks it [INFERRED].
   - The any-ValueError risk is explicitly "not required by spec", so B concedes it is not a spec issue.
6. **Recommendations mirror T1's.**
   - B's recommendations 2-4 closely match `t1-card.md` recs 1-3 (try/except to a raises-style assertion, regenerate the diff, make `src` importable). This is carry-forward and anchoring, not independent audit.
   - Recommendation 1 is filed under `src/greeting.py` but is really a reclassification of the T1 card.
7. **G-2 critique omits `invocations.yaml:3`.**
   - B's critique is correct on `execution.log:5`, but it never mentions `invocations.yaml:3`, which does record `tool-unavailable`.
   - Presenting it as a "citation defect" without noting the supporting line overstates it, because T1's conclusion was true and only the citation was weak.
8. **Weaker gap hygiene.**
   - B gives `hunk_ref: none` three times.
   - All three `decision_needed_by_user` values are booleans, so no decision question is stated. Gap 1 says `true` but does not say what is to be decided.

#### Concessions
- **Out-of-range citation.** A's `interaction-effects.yaml:14-21` is out of range. The file has 13 lines and the relevant content is at `:5-7` and `:12`. The claim itself is true, only the pointer is wrong.
- **Verdict not linked to D-1.** A's T-102 verdict does not link D-1 (C-002). B is better here.
- **No coverage section.** A has none (S-001), and B's `coverage_audit` is accurate.
- **Gap 1 conflates two questions.** A folds "no execution" and "import/packaging" into one gap. B's three-way split is cleaner.
- **Free-text verdict labels.** A's labels are less machine-friendly (S-003).
- **Thinner remediation.** A's test remediation is a single item, and B's concrete remediations (explicit assertion, `conftest`/`pythonpath`) add value.
- **Smaller points B gets right.** B's G-2 critique of `execution.log:5` is right. The whitespace risk, which A omits, is a legitimate note even though it is unrelated to the guard.
- **Calibration.** The calibrator scored B (0.84) above A (0.82), so I make no claim of overall superiority beyond the specific points above.

#### Shared assumptions

**A-002: QUALIFY (accept the equivalence, reject how B uses it).**
- For `str`, `not name` equals `name == ""`, because the empty string is the only falsy `str`. The broadening therefore only affects `None`, `0`, `[]` and `False`, where `spec.md:9` is silent and `greet` has no type contract.
- That supports A's hedge and D-1 at LOW severity, and an unspecified-input note is a plausible reading.
- It undercuts B's "`name == ""` would have sufficed -> not Necessary" and B's unhedged Drift. Drift remains defensible: an unrationalised behavioral broadening that the spec neither authorizes nor contradicts.
- The `t1-card.md` rationale (line 6) already named None, 0, [] and False, so neither variant discovered anything new here.

**A-005: QUALIFY.**
- Executor authorship of the untracked tests file rests only on `execution.log:4` plus the map's "log-declared path" rule (`task-to-work-map.yaml:35`).
- A pairs the T-103 verdict with the provenance gap ("outside supplied diff", gap 2). B's verdict does not condition on its own gap 1. A's wording carries the caveat, so A is less exposed to the assumption.
- Both cards should state it explicitly.
- `spec.md:12` is about the tests' existence and content, not their authorship, so a T-103 verdict "present on disk" survives even if authorship is unproven.

**A-006: ACCEPT.**
- I read `fixtures/project/proposed.md`. Line 7, "Reject an empty name using ValueError", does not authorize falsy broadening. No artifact in `spec.md`, `completed.md`, `execution.log`, `proposed.md` or the map approves it either.
- Neither card states its search scope, which is a minor omission in both.

**A-007: ACCEPT.**
- `changes.patch:6-9` is identical to `src/greeting.py:1-4` (the patch is the only hunk).
- Interchangeable citation is therefore sound.
- It would matter only if the file were edited after the diff, and nothing shows that.

#### Per-point positions

| point | superior approach (A / B / equal) | one-line reason |
|---|---|---|
| S-001 | B | `coverage_audit` is accurate (`spec.md:3` non-normative) and A has none. |
| S-002 | A | A's `severity: LOW` is justified by the narrow impact (str-equivalent). |
| S-003 | equal | Both labels are vocabulary only. B's tokens are tidier, A's is more readable. |
| S-004 | A | A gives real hunk refs for the gaps and B gives `none`. |
| S-005 | A | A states the decision question as a string. B's booleans carry no content. |
| S-006 | B | B's three-way split is cleaner than A's merged gap 1. |
| S-007 | equal | Path formatting is cosmetic. B's bare names are consistent and A's single full path is clearer. |
| S-008 | equal | A is concise and targets the root cause. B is more granular but partly mirrors T1. |
| C-001 | equal | The T-101 verdicts are substantively the same. |
| C-002 | B | Only B links D-1 into the T-102 verdict. |
| C-003 | A | The `[x]` and 1.0 "overclaim" is contradicted by `task-to-work-map.yaml:33` ("statically verified") and `spec.md:12`. |
| C-004 | A | A's hedge is correct, since `spec.md:9` is met for `''`. |
| C-005 | A | A applies the real forcing-constraint test. B's counterfactual is not the Necessary criterion. |
| C-006 | equal | Both identify the gap and agree on the need for user input. |
| C-007 | equal | B is cleaner on `execution.log:5` but omits `invocations.yaml:3`. A's merge is acceptable. |
| C-008 | equal | Both mark the import risk [INFERRED]. |
| C-009 | B | B lists more boundary risks, though the whitespace one is orthogonal to the guard. |
| C-010 | A | A keeps its verification risk to what is shown. B's "must not become runtime clearance" is rhetorical. |
| C-011 | A | A raises the coupling risk, which `interaction-effects.yaml:5-7,12` supports (line range wrong). |
| C-012 | A | A also offers the rationale or spec-amendment path and a rule-level verifier. |
| C-013 | B | B's remediations are more concrete, though they mostly mirror T1's. |
| C-014 | B | A has one out-of-range citation (`interaction-effects.yaml:14-21`). B's all resolve, but B's G-2 omits `invocations.yaml:3`. |
| C-015 | equal | The calibrated scores (0.82 vs 0.84) are close and inversely ordered against self-report. |
| X-001 | A | Open static-presence framing is correct. The `spec.md:12` text and the map's annotation do not support B's "overclaim". |
| X-002 | A | A's user-decision framing is consistent with its caveated verdict. B's `false` fits its stance but conflicts with its own `[x]` complaint. |
| X-003 | A | "No deviation" remains admissible for str-equivalent input. B forecloses it without justification. |
| A-002 | A | The equivalence holds and favors A's hedge over B's Necessary test. |
| A-005 | A | A's verdict wording carries the provenance caveat. B's verdict does not. |
| A-006 | equal | Both accept it, since `proposed.md:7` does not authorize the broadening. Neither states its scope. |
| A-007 | equal | `changes.patch:6-9` matches `greeting.py:1-4`. |

### Variant B Advocate (haiku:qa)

Source: `round-1/advocate-B-haiku-qa.md` (verbatim).

<!-- Round 1 statement. Advocate for Variant B (variant-2-original.md). Native Task worker (general-purpose), model slot: haiku, persona: qa. agentId acb3a713412dd27cb. Persisted verbatim by the top-level pipeline driver. -->
#### Position summary

Variant B is the stronger audit where a QA gate matters: it ties the T-102 verdict to the guard drift, treats `completed.md`’s `[x]` and `tasklist_completion_pct: 1.0` as an acceptance overclaim while `verification_ran` is false, and splits grounding gaps so only diff provenance is a user decision. A’s no-deviation counter-view, LOW severity, shared-function coupling note, and “narrow or amend the spec” fix should be merged in; they do not justify A’s clean T-102 verdict or its open waiver of R-003.

#### Steelman of Variant A

A’s strongest point is the D-1 counter-view (rationale, variant-1-original.md:16; U-009 / X-003). R-002 only says the greet function “MUST reject an empty name with ValueError” (`spec.md:9`). For that input, `if not name` (`src/greeting.py:2`) does raise, and `tests/test_greeting.py:10` calls `greet("")`. For a `str`, `not name` is true exactly when `name == ""`. Calling the idiom Drift without saying that it may be adherent inside the spec’s named domain can over-classify a predicate that meets every stated case.

A also gets several concrete things right. It stamps D-1 `severity: LOW` (variant-1-original.md:15), which matches “does not contradict R-002 for `""`.” It aims a recommendation at the bad upstream class, not only at the snippet: reclassify T1’s authorized label, with the verifier “every 'authorized' item cites an explicit approving artifact” (variant-1-original.md:27), against `t1-card.md:19-20` (“mapped to T-102, so it is not Drift”). It offers a real alternative to narrowing: “record rationale/spec amendment for rejecting all falsy input” (variant-1-original.md:28), and its verifier is behavioral (`greet('')` raises, `greet('Ada') == 'Hello, Ada!'`), which is the right check on a function `interaction-effects.yaml:5-12` marks `genuinely_shared` by T-101 and T-102. The coupling risk itself is real: “changing the guard at line 2 affects the R-001 path” (`interaction-effects.yaml:12`). A’s grounding-gap `hunk_ref`s name `tests/test_greeting.py:1` and the out-of-diff file instead of `none`, and its risk line cites `invocations.yaml:2-3`, including `verification_skip_reason: tool-unavailable`. “Extra falsy handling untested” is the actual D-1 delta (`None`, `0`, `[]`, `False`), which B’s risk list never names.

#### Strengths claimed

1. **T-102 verdict carries D-1 (C-002).** B’s verdict is `statically_met_with_drift` with “broadening = D-1” (variant-2-original.md:7). A’s T-102 line is “implemented (static only)” (variant-1-original.md:7) even though the implementing line is `if not name`. A per-task reader of A accepts R-002 as clean.

2. **Acceptance is not a checkbox (C-003, X-001, U-002).** `completed.md:2` is `status: done` and `completed.md:8` is `[x] T-103`. `task-to-work-map.yaml:33` is `tasklist_completion_pct: 1.0`. `invocations.yaml:2` is `verification_ran: false` and `invocations: []` is line 4. `execution.log:5` says “No test execution is claimed.” R-003 (`spec.md:12`) says tests “MUST exercise” the two cases. B is the card that says the `[x]` and the 1.0 “overclaim acceptance” (variant-2-original.md:8) and that “completion 1.0 is not an acceptance pass” (variant-2-original.md:23). The map comment “3/3 statically verified on disk” discloses static scope; the tasklist `[x]` does not. A stops at “implemented on disk, unrun.”

3. **Necessary is eliminated by a counterfactual, not a slogan (C-005).** B: “no inline rationale and `name == \"\"` would have sufficed -> not Necessary” (variant-2-original.md:16). Nothing in `spec.md:9`, `completed.md:7` (“empty-name rejection”), `execution.log:3` (“empty names raise ValueError”), or `proposed.md:7` (“Reject an empty name using ValueError.”) forces a falsy predicate. A’s “no documented forcing constraint” is the same conclusion with the alternative left implicit.

4. **Four-class chain is explicit and matches the taxonomy.** Same rationale line: no approving artifact, so not Authorized; narrower check would have sufficed, so not Necessary; “no contradiction for `''`”, so not Regression; “unstated broadening with no rationale”, so Drift. That is the required order. T1’s “mapped to a task, therefore not Drift” (`t1-card.md:20`) is the move both cards reject; B is the one that refuses to put “no-deviation” on the recommendation list as a way to drop the extra behavior.

5. **Gap split and decision discipline (S-006, C-007, X-002).** B’s three gaps (variant-2-original.md:19-21) are three different failures: test file absent from `changes.patch:1-9` (user decision true; `task-to-work-map.yaml:35-36`, git init only, no HEAD); no runner output (decision false, “unrun != contradiction”); packaging/`src.greeting` import (decision false, “[INFERRED] … not observed”). A folds execution and import into one gap whose `decision_needed_by_user` is “whether static presence suffices for T-103 done” (variant-1-original.md:19). A yes-answer would close an unobserved import failure. Policy (is an out-of-diff file acceptable?) is the only user decision; pass/fail is a missing log.

6. **Coverage control (S-001, U-001).** B’s `coverage_audit` states no requirement-bearing span is missing and that `spec.md:1-3` is non-normative. `spec.md:3` is “synthetic audit input, not shipped product code.” R-001..R-003 (`spec.md:5-12`) are the whole normative span. A has no coverage section.

7. **Edge cases A dropped (C-009).** `"   "` is truthy, so `src/greeting.py:2` does not raise and line 4 returns a greeting; R-002 says “empty”, not blank. Truthy non-strings are interpolated at line 4; the spec has no type rule. `tests/test_greeting.py:8-13` does `except ValueError: return`, so any `ValueError` passes, and B notes the spec does not require the message. Those are failure scenarios, correctly not upgraded to Regression.

8. **T1 G-2 citation defect (U-003).** `t1-card.md:33` uses `execution.log:5` as if it showed the tool was unavailable. Line 5 is only “No test execution is claimed.” B flags that (variant-2-original.md:20). B’s other half, “exercise is statically visible,” matches the calls at `tests/test_greeting.py:4-5` and `:10`. Held next to “R-003 not accepted absent execution,” the right reading is: calls are in source; pass/fail is not.

9. **Citation that was checked resolves; A’s unique risk citation does not (C-014).** `interaction-effects.yaml` is 13 lines. A cites `:14-21` (variant-1-original.md:23). The edge is `:4-12`. B’s cited lines (`spec.md:6` and `:9` and `:12`, `t1-card.md:19-20`, G-2 text at `:33-34`, `task-to-work-map.yaml:30-31` and `:33`, `invocations.yaml:2-4`) match the files.

10. **Remediation matches distinct test failures (C-013).** B asks for an explicit `ValueError` assertion, a diff that includes the tests or a widened scope, and a root `conftest.py` or `pythonpath`, each with its own verifier (variant-2-original.md:30-32). A’s single “run suite with real pytest” (variant-1-original.md:29) is necessary and would not tighten `except ValueError` or put T-103 in the supplied diff. A green log would leave both holes.

#### Weaknesses identified in Variant A

1. **Per-task T-102 erases the only deviation (C-002).** Verdict text “implemented (static only)” plus evidence `src/greeting.py:2-3` (variant-1-original.md:7) tells a consumer the guard is just the implementation. D-1 sits in another section, and recommendation 1 then offers “or no-deviation” (variant-1-original.md:27), so the broadening can vanish without an approving artifact. That is the same disappearance T1 achieved via “mapped, therefore not Drift.”

2. **R-003 is left as a user preference (X-001, C-003).** “implemented on disk, unrun, outside supplied diff” (variant-1-original.md:8) does not challenge `completed.md:8`. The gap question “whether static presence suffices for T-103 done” treats `spec.md:12` (“MUST exercise”) as waivable by the reader of the card. With `verification_ran: false`, static presence is not acceptance. A waiver would itself need an approving artifact; it should not be the default question.

3. **Out-of-range coupling citation (C-014).** The shared-function claim is right (`interaction-effects.yaml:7` `genuinely_shared: true`; `:12` guard vs R-001 path) and the line range `:14-21` is not in the file. The one risk A alone adds is the one risk whose citation does not resolve.

4. **Two failure modes, one gap (C-007, S-006).** “No test execution; no src/__init__.py / conftest / pytest config” (variant-1-original.md:19) mixes “nothing ran” with “plain pytest may not collect `from src.greeting import greet`” (`tests/test_greeting.py:1`). A’s own `why_not_classifiable` says import/pass is “not statically decidable.” Pairing that with a user question about static sufficiency lets one answer close both. Provenance, which really is a user call (`task-to-work-map.yaml:35-36`), is a separate gap, so the schema is inconsistent: every gap is a question, and none can say “no decision, get a log.”

5. **Blank-string and weak-assertion holes are missing (C-009).** “extra falsy handling untested” and “only exercises `''`” (variant-1-original.md:23-25) cover `None`/`0`/`[]`/`False` and the single literal. They do not cover `greet("   ")` taking the return path at `src/greeting.py:4`, truthy non-strings, or `except ValueError` accepting any message. T1 already had the whitespace candidate (`t1-card.md:38`). A dropped it. Running the current suite, which is A’s only test recommendation, would greenwash `tests/test_greeting.py:8-13`.

6. **Necessary test does not show the spec-exact alternative (C-005).** “no documented forcing constraint (Necessary fails)” (variant-1-original.md:16) is fair and incomplete. A defender can say the idiom *is* the empty check. B’s `name == ""` counterfactual closes that. A also never states the str-equivalence it needs for the counter-view, so “could be read as adherent” floats free of the values where the guards differ.

7. **No coverage statement (S-001).** On a 12-line spec the miss is small. A still never records that `spec.md:1-3` is non-normative or that R-001..R-003 are the full requirement span, which is the control that would show a missing MUST.

#### Concessions

1. **B’s “exercise is statically visible” collides with the spec’s verb (C-003).** `spec.md:12` says tests “MUST exercise.” B says T1’s “cannot confirm tests exercise the code” (`t1-card.md:34`) is “too broad: exercise is statically visible” (variant-2-original.md:8) and also “R-003 not accepted absent execution” (variant-2-original.md:23). Those are compatible only if “exercise” means “the calls are written down.” B does not say that. As written, it reuses R-003’s verb for source text. The fix is to split the sentence: calls are visible at `tests/test_greeting.py:4-5` and `:10`; pass/fail is not; G-2 should not pretend `execution.log:5` proves tool unavailability.

2. **B omits `invocations.yaml:3` (C-014).** The execution.log critique is true and incomplete. `invocations.yaml:3` does record `verification_skip_reason: tool-unavailable` and that the orchestrator did not substitute Bash. That is an orchestrator surface choice, not a pytest result. B cites `:2-4` in the T-103 evidence line but the gap text (variant-2-original.md:20) never mentions line 3, so it can be read as denying evidence that is there.

3. **Unhedged Drift over-claims inside the str domain (C-004, X-003).** B offers no adherent reading. For `str`, `not name` and `name == ""` match, `greet("")` raises either way, and that is not a Regression and may be no deviation. The counter-view belongs in the rationale, scoped to `str`. It does not belong as a recommended reclassification that drops `None`/`0`/`[]`/`False`.

4. **No severity (S-002).** If the class stays Drift, LOW is right: the specified `""` path raises, and `greet("Ada")` is unaffected. B’s record can be read as an unqualified defect.

5. **`hunk_ref: none` and a bare boolean lose the question (S-004, S-005).** A’s refs point at the import line and the out-of-diff file. B’s `decision_needed_by_user: true` (variant-2-original.md:19) does not state the decision (is omission from the supplied diff acceptable?). The boolean is the right type; the question text still has to live somewhere.

6. **Coupling is under-weighted (C-011).** B only says “interaction-effects coverage is static only” (variant-2-original.md:27). `interaction-effects.yaml:12` is a cross-requirement failure mode: a guard edit is on the R-001 path. A broken line range does not make that finding optional.

7. **The guard recommendation is the weaker fix (C-012).** “narrow line 2 … or stop calling falsy broadening authorized” (variant-2-original.md:29) mixes a code edit with a labeling instruction. Narrowing `if not name` to `name == ""` changes `None` from `ValueError` to `f"Hello, {None}!"` (`src/greeting.py:4`) with no new test. A’s “or record rationale/spec amendment” keeps that behavior only if it is chosen on purpose, and A’s verifier actually calls `greet('')` and `greet('Ada')`. B’s verifier is another static re-read of `src/greeting.py:2-3` vs `spec.md:9`.

8. **Risks B raises are not in B’s test recommendations.** Whitespace and truthy non-strings are not fixed by narrowing to `name == ""` (both predicates treat them as non-empty). B never asks for tests for `"   "`, `None`, or `42`. T1 did (`t1-card.md:48`). Flagging an edge and not asking for a case is a QA hole in B, not a point against the risks being real.

9. **A-005 applies to B too.** `static_cases_present_runtime_unproven` still treats `tests/test_greeting.py` as T-103 work. Authorship evidence is `execution.log:4` plus an untracked file (`task-to-work-map.yaml:35-36`). B conditions the gap, not the verdict, on that fact.

#### Shared assumptions

**A-002 — QUALIFY.** Accept the equivalence as a Python fact: for `str`, `not name` is true iff the string is empty. `"   "` is truthy under both predicates, so whitespace is not the broadening. The broadening bites for non-str falsy values (`None`, `0`, `[]`, `False`). Reject using that fact as a silent premise that the broadening is in-domain divergence, and reject using it to collapse D-1 to no-deviation. `spec.md:9` states no type contract; `src/greeting.py:1` is `def greet(name)` with no annotation. The audit sentence neither card wrote: str-domain behavior meets R-002 and is not Regression; rejection of non-str falsy values is unspecified extra behavior, hence Drift unless an approving artifact exists, not “no deviation” and not Necessary.

**A-005 — QUALIFY.** Accept on-disk case presence: `tests/test_greeting.py:4-5` and `:8-13` contain the two R-003 cases. Reject executor authorship. The file is outside `changes.patch:1-9`, `in_supplied_diff: false` and `in_scope_flag: false` (`task-to-work-map.yaml:30-31`), and the repo “has git init only: no HEAD” (`task-to-work-map.yaml:36`). `execution.log:4` is a self-report. Both verdicts credit the file anyway. Credit “cases present on disk,” keep the provenance gap’s user decision, and do not let the verdict say the executor implemented T-103.

**A-006 — QUALIFY.** Do not accept “the snapshot is the complete authorization search.” `fixtures/project/proposed.md` is outside the snapshot. Its line 7, “Reject an empty name using ValueError.”, does not approve falsy broadening, nor do `spec.md:9`, `completed.md:7`, or `execution.log:3`. The conclusion “not Authorized” survives the omitted file. The method claim does not: search scope must include the plan artifact, and neither card states that scope.

**A-007 — ACCEPT.** On-disk `src/greeting.py:1-4` matches `changes.patch:6-9` (same four lines; patch prefixes only). Interchangeable citation is valid for this file. It does not extend to `tests/test_greeting.py`, which the patch does not contain.

#### Per-point positions

| point | superior approach (A / B / equal) | one-line reason |
|---|---|---|
| S-001 | B | B records a coverage span and correctly marks `spec.md:1-3` non-normative; A has no coverage section. |
| S-002 | A | LOW severity is the right metadata for a non-contradicting broadening; B omits it. |
| S-003 | B | B’s tokens distinguish clean static, drift, and runtime-unproven; A uses “implemented (static only)” for both T-101 and T-102. |
| S-004 | A | Concrete hunk refs to the import line and the out-of-diff test file are navigable; `none` is not. |
| S-005 | B | A boolean can say “no user decision”; A’s always-a-question string cannot. |
| S-006 | B | Provenance, unrun tests, and inferred import are separate failures and must not share one decision. |
| S-007 | equal | Both are readable against the snapshot root; neither prefixes paths consistently. |
| S-008 | B | B’s four items track the guard, the weak assertion, the missing hunk, and importability separately. |
| C-001 | equal | Both correctly limit T-101 to static evidence; B’s extra `spec.md:6` and `execution.log:5` cites do not change the verdict. |
| C-002 | B | Only B’s T-102 verdict carries D-1; A’s “implemented (static only)” reads as a clean R-002. |
| C-003 | B | B challenges `completed.md:8` and completion 1.0; A describes the file as implemented on disk and leaves the checkbox standing. |
| C-004 | B | Both land on Drift; A’s “or no-deviation” hedge drops non-str falsy behavior the empty-string idiom does not justify. |
| C-005 | B | B shows `name == ""` would have met R-002, so the wider predicate was not forced; A only says no forcing constraint was documented. |
| C-006 | equal | Both correctly leave out-of-diff test provenance as a user decision given git-init-only and no HEAD. |
| C-007 | B | Unrun is not a contradiction and not a user opinion; A asks whether static presence suffices and folds the import question in. |
| C-008 | B | B keeps the inferred `src.greeting` import failure unobserved and decision-free instead of bundling it with acceptance. |
| C-009 | B | B adds blank-string, truthy non-string, and any-`ValueError` holes; A alone notes untested falsy inputs, which D-1 already is. |
| C-010 | B | B refuses to treat completion 1.0 as an acceptance pass; A only reports that the verification triangle did not run. |
| C-011 | A | Shared `greet` means a guard change hits R-001 (`interaction-effects.yaml:12`); B never raises that coupling. |
| C-012 | A | A’s “narrow or amend the spec” plus a `greet('')`/`greet('Ada')` verifier beats B’s label change and a static re-read that would turn `None` into `"Hello, None!"`. |
| C-013 | B | B separately fixes the assertion, the missing test hunk, and importability; A only says to run pytest. |
| C-014 | B | A cites `interaction-effects.yaml:14-21` in a 13-line file; B’s checked cites resolve, though it under-mentions `invocations.yaml:3`. |
| C-015 | equal | Calibration inverts self-report (B 0.76/0.84, A 0.80/0.82); neither self-score is evidence. |
| X-001 | B | Static cases plus an unrun file do not discharge “MUST exercise” or a tasklist `[x]`. |
| X-002 | B | Only diff-scope policy needs a user; runtime pass/fail needs a saved pytest log. |
| X-003 | equal | No-deviation is admissible for `str`/`""` only; Drift remains the right class for unrationalised non-str falsy rejection. Neither card states that split. |
| A-002 | equal | Neither card states the str-equivalence; it qualifies D-1, it does not license either card’s silent use of it. |
| A-005 | B | B’s verdict name credits cases present, not “implemented”; both still treat an untracked out-of-diff file as T-103 work. |
| A-006 | equal | `proposed.md:7` does not authorize falsy broadening, but it sits outside the snapshot, so completeness was never shown. |
| A-007 | equal | `src/greeting.py:1-4` matches `changes.patch:6-9`; both cards were right to treat those cites as the same text. |

## Round 2: Rebuttals

### Variant A Rebuttal (sonnet:analyzer, sequential 1st)

Source: `round-2/advocate-A-sonnet-analyzer-rebuttal.md` (verbatim).

<!-- Round 2 rebuttal (sequential, 1st). Advocate for Variant A. Native Task worker (general-purpose), model slot: sonnet, persona: analyzer. agentId aacae5a74ec340cb7. Persisted verbatim by the top-level pipeline driver. Driver note: "from src.graph import greet" below is the advocate's typo; tests/test_greeting.py:1 reads "from src.greeting import greet". -->
#### Response to criticisms

**1. C-003 / X-001: R-003 and the `[x]` (B's weaknesses 1 and 2)**

I'm splitting this into what I hold and what I concede.

*What I hold.* `spec.md:12` is "Tests MUST exercise the ordinary greeting and empty-input rejection." That sets a requirement on what the tests contain. It does not require a pass or a run.
- `tests/test_greeting.py:4-5` calls `greet("Ada")` and asserts the exact string.
- `tests/test_greeting.py:8-13` calls `greet("")` and fails if no ValueError is raised.
- `completed.md:8` says T-103 "implements R-003 both ordinary and empty-input tests". That is a claim about implementation, and the static evidence supports it.
- `execution.log:5` says "inspect these files independently", which invites static inspection.
- `task-to-work-map.yaml:33` carries the comment "3/3 statically verified on disk".

So B's "overclaim acceptance" attributes an acceptance claim to a checkbox that does not make one. A's "implemented on disk, unrun" is accurate, and I keep X-001.

*What I concede.* B's U-002 has a real residual.
- `completed.md:2` is a bare `status: done`, with no static-only qualifier.
- A reader of `completed.md` alone would take that as acceptance while `invocations.yaml:2` says `verification_ran: false`.
- A's risks say "all verdicts static", but A never ties that to the `done` status. B does, in "completion 1.0 is not an acceptance pass".
- My own gap question, "whether static presence suffices for T-103 done", is somewhat misframed. R-003's text does not need a waiver. The real question is the meaning of `done`.
- A further caution for me: static "exercise" depends on `from src.graph import greet` resolving (`tests/test_greeting.py:1`). That is an [INFERRED] import risk, not an observed failure, but it means "exercise" is not purely static.

On C-003 as a whole, B surfaced something useful that A omitted, so I move it to equal. I keep X-001 for A on the narrow question of whether R-003 is discharged.

**2. C-004 / X-003: the hedge versus unhedged Drift (B's weaknesses 5 and 6)**

I accept B's split proposal and think it is the correct resolution.
- For `str`, `not name` is true exactly when `name == ""`. `greet("")` raises, so R-002 is met and this is no deviation.
- For `None`, `0`, `[]` and `False`, the spec is silent and `greet` has no annotation (`src/greeting.py:1`). Rejecting them is extra, unrationalised behaviour with no approving artifact, which is Drift (LOW).

B is right that my hedge is unscoped. "Could be read as adherent/no deviation" and "Reclassify D-1 ... Drift (LOW) or no-deviation" (variant-1:16, :27) do not say where no-deviation applies.

B also made a concession (its concession 7) that is a fair hit on its own recommendation. Narrowing to `name == ""` would turn `greet(None)` into `"Hello, None!"` (`src/greeting.py:4`). A's "or record rationale/spec amendment" path and its `greet('')` / `greet('Ada')` verifier handle that better than B's static re-read.

Where this leaves the two cards:
- A kept the no-deviation reading visible and set severity LOW. That is closer to the correct split, so I keep C-004 for A.
- Neither card states the str-versus-non-str scoping, so X-003 is equal.

**3. C-005: what the Necessary test requires (B's weakness 6)**

I concede this point. In R1 I said B's counterfactual is "not part of that test". That was too strong.

"Necessary" means the deviation was needed to implement the requirement. "No documented forcing constraint" shows only that none was recorded. A deviation can be necessary and undocumented. Showing that the spec-exact `name == ""` satisfies `spec.md:9`, `tests/test_greeting.py:10`, `completed.md:7` and `execution.log:3` is the stronger elimination, because it rules out necessity on the merits.

B's counterfactual does have a limit. For `str` it is an identity, so it bites only for non-str falsy values. B never says that (A-002), but the conclusion is sound. C-005 moves to B.

**4. C-007 / X-002: whether runtime pass/fail needs a user decision (B's weakness 4)**

I concede this to B.
- `invocations.yaml:3` shows the skip was an orchestrator surface choice. The orchestrator "did not substitute Bash", and `tool-unavailable` describes one tool, not the repository.
- The missing pytest log is therefore closable by an orchestrator re-run. It is not a policy question.
- The only real user decisions are provenance of the out-of-diff test file (`task-to-work-map.yaml:35-36`) and what `done` means.
- A's single string, "whether static presence suffices for T-103 done", bundles the execution gap and the import gap. The string field cannot say "no decision, get a log". B's gap 2 and gap 3 with `false` express that correctly.

C-007 and X-002 move to B. B's omission of `invocations.yaml:3` stands, but it does not change the decision flag.

**5. S-003, S-005, S-008**

- **S-003.** B's snake_case tokens separate `statically_met` from `statically_met_with_drift`. A gives T-101 and T-102 the same label. Some of that is C-002 counted a second time, but the tokens are also more machine-mergeable. I move this to B.
- **S-005.** The diff analysis calls this an interface-type difference. A's string field can state a question but cannot say "none". B's boolean can say "no", but `true` loses the question (B's concession 5). Neither dominates, so I move to equal.
- **S-008.** B's four items are granular. Their mirroring of `t1-card.md` recs 1-3 is anchoring, but that does not make them worse recommendations. A's rec 1 targets the T1 card with a rule-level verifier, which B lacks. I keep equal.

**6. C-009 (B's weakness 5)**

B is right that A dropped whitespace, truthy non-str, and any-ValueError. That is why I conceded C-009 in R1, and I keep it for B. Two caveats stand:
- Whitespace and non-str inputs are not changed by the guard (`" "` is truthy under both predicates).
- B never asks for tests covering them (B's concession 8).

**7. C-010**

I move to equal. B's "completion 1.0 is not an acceptance pass" is accurate, and the map's own comment ("statically verified") supports it. A's "verification triangle did not run" covers the same ground less sharply. B's "must not become runtime clearance" is still emphasis rather than evidence, but that no longer decides the point.

**8. C-013**

B is better. The explicit assertion, the diff scope and importability are separate fixes, and a green pytest log would not close any of them. A's single "run pytest" is necessary but thin. Position unchanged.

**9. C-014 / C-011 / C-012**

- **C-014.** `interaction-effects.yaml` is 13 lines. A cited `:14-21`; the claim is at `:4-12`, with `:12` the load-bearing note. A's citation is defective. B wins on citations, as in R1.
- **C-011.** A raised the coupling risk and B did not. The defective range does not remove the finding (B's concession 6), so A wins.
- **C-012.** I keep A, based on B's concession 7.

#### Updated assessment of Variant B

B's stronger points are the Necessary counterfactual, the three-way gap split with correct decision flags, `coverage_audit`, linking D-1 into the T-102 verdict, and surfacing the `status: done` and completion-1.0 semantics.

B's weaker points:
- B's "R-003 not accepted absent execution" reads a pass or run requirement into `spec.md:12`.
- B's "exercise is statically visible" sits in tension with that line, and B concedes the tension (its concession 1).
- B's Drift is unhedged, which B also concedes (its concession 3).
- B's guard fix omits the `None` side effect.
- B flags edge cases without asking for tests.

My R1 claim that B "misreads its own evidence" was overstated. B misattributes acceptance to the checkbox, but it identifies a real reporting gap.

#### New evidence

- `completed.md:2` carries a bare `status: done` with no static-only qualifier. This supports B's overclaim point in a limited form.
- `completed.md:8` says "implements ... tests", not "passes". This supports A's reading of the `[x]`.
- `execution.log:5` says "inspect these files independently". It invites static inspection and does not claim a run.
- `invocations.yaml:3` shows the missing run was an orchestrator surface choice, so the runtime gap needs no user decision (X-002).
- `interaction-effects.yaml:12` says "Both paths are covered by the T-103 tests (statically)". The tests cover only `""` and `"Ada"`. Narrowing the guard would change `None` behaviour with no test catching it, which weakens B's guard fix.
- `tests/test_greeting.py:1` imports `src.greeting`, and there is no `__init__.py` or conftest in the snapshot. Plain-pytest importability is [INFERRED] and unobserved, so "exercise" depends on an unverified import.
- I have not re-read `changes.patch` this round. For A-007, I rely on the diff analysis's verification plus `task-to-work-map.yaml:6` (a four-line new-file hunk, which matches `src/greeting.py`'s four lines).

#### Shared assumptions

- **A-002: QUALIFY (changed in substance, same label).** I now adopt B's formulation.
  - The str domain meets R-002 and is no deviation.
  - Rejecting non-str falsy values is unspecified extra behaviour, which is Drift (LOW) unless an approving artifact exists.
  - Neither card states this.
- **A-005: QUALIFY (unchanged label).** B's token `static_cases_present_runtime_unproven` is more authorship-neutral than A's "implemented". A's "outside supplied diff" carries the provenance caveat, but "implemented" still implies authorship. Neither verdict is conditioned on its own provenance gap.
- **A-006: QUALIFY (changed from ACCEPT).** The conclusion holds, because `proposed.md:7` does not authorize the broadening. B is right that completeness of the search scope was never shown, and neither card states it.
- **A-007: ACCEPT (unchanged), limited to `src/greeting.py`.** It does not extend to `tests/test_greeting.py`, which is outside the patch.

#### Updated per-point positions

| point | superior (A / B / equal) | changed from R1? | one-line reason |
|---|---|---|---|
| S-001 | B | n | `coverage_audit` is accurate; A has no coverage section. |
| S-002 | A | n | `severity: LOW` fits a str-equivalent broadening; B has none. |
| S-003 | B | y | B's tokens distinguish the clean, drift and unproven states and are mergeable. |
| S-004 | A | n | A's hunk refs are navigable; B uses `none` three times. |
| S-005 | equal | y | A's string cannot say "none"; B's `true` loses the question. |
| S-006 | B | n | Provenance, unrun tests and import are separate failures. |
| S-007 | equal | n | Path formatting is cosmetic. |
| S-008 | equal | n | B is more granular, but its items mirror T1; A's rec 1 is root-cause. |
| C-001 | equal | n | The T-101 verdicts are substantively the same. |
| C-002 | B | n | Only B's T-102 verdict carries D-1. |
| C-003 | equal | y | R-003's text is met statically, but B surfaced the `status: done` semantics gap that A did not. |
| C-004 | A | n | A keeps the no-deviation reading open and sets LOW; neither scopes it to str. |
| C-005 | B | y | The `name == ""` counterfactual is a stronger Necessary elimination than "no documented constraint". |
| C-006 | equal | n | Both flag provenance as a user decision. |
| C-007 | B | y | `invocations.yaml:3` shows the gap is closable by a re-run, and B separates it cleanly. |
| C-008 | equal | n | Both mark the import risk [INFERRED]; the bundling is S-006. |
| C-009 | B | n | B adds whitespace, non-str and any-ValueError risks; A only notes untested falsy input. |
| C-010 | equal | y | B's "not an acceptance pass" is accurate; A's "all verdicts static" covers the same ground. |
| C-011 | A | n | `interaction-effects.yaml:12` supports the coupling risk, despite A's wrong line range. |
| C-012 | A | n | A's rationale/amendment path and behavioural verifier beat B's static re-read, which risks `"Hello, None!"`. |
| C-013 | B | n | B's three fixes are distinct and concrete. |
| C-014 | B | n | A's `interaction-effects.yaml:14-21` is out of range in a 13-line file. |
| C-015 | equal | n | Calibrated and self-reported scores are inversely ordered; neither is evidence. |
| X-001 | A | n | `spec.md:12` and `completed.md:8` do not require a run, so the `[x]` is not an acceptance claim (with the `status: done` caveat). |
| X-002 | B | y | Runtime pass/fail needs a saved log; only provenance and the meaning of `done` need a user. |
| X-003 | equal | y | No-deviation is admissible for str only and Drift for non-str falsy; neither card states the split. |
| A-002 | equal | y | The equivalence holds; neither card states it, and B's split is the right resolution. |
| A-005 | equal | y | B's token is more authorship-neutral, while A's wording carries the provenance caveat. |
| A-006 | equal | y | The conclusion holds, but neither card states the search scope. |
| A-007 | equal | n | `src/greeting.py` matches the patch; this does not extend to the tests file. |

### Variant B Rebuttal (haiku:qa, sequential 2nd, saw A's rebuttal)

Source: `round-2/advocate-B-haiku-qa-rebuttal.md` (verbatim).

<!-- Round 2 rebuttal (sequential, 2nd; saw A's rebuttal). Advocate for Variant B. Native Task worker (general-purpose), model slot: haiku, persona: qa. agentId a64980251869bbd7d. Persisted verbatim by the top-level pipeline driver. -->
#### Response to criticisms

**X-001.** A is right about the spec sentence and about two annotations, and wrong to save the checkbox.

`spec.md:12` says tests “MUST exercise” the ordinary greeting and the empty-input rejection. It does not say “MUST pass” or “MUST have been run.” `completed.md:8` says “implements R-003 both ordinary and empty-input tests,” not “passes.” `task-to-work-map.yaml:33` annotates `1.0` with “3/3 statically verified on disk.” `execution.log:5` says no execution is claimed and tells the reader to inspect the files. I withdraw the gloss that R-003 imports a green pytest log, and I withdraw treating that annotated `1.0` as a hidden acceptance pass. “R-003 not accepted absent execution” (`variant-2-original.md:23`) over-reads the spec. The tension with “exercise is statically visible” (`variant-2-original.md:8`) is real; the calls are on disk at `tests/test_greeting.py:4-5` and `:10`.

That does not make the `[x]` a non-claim, and it does not discharge “exercise.”

`completed.md` is one completion record: `status: done` at line 2, then `[x]` on lines 6–8. A concedes the status line and exempts the checkbox because the words after it do not say “pass.” The mark is the claim; the words are the label. The same reading would empty T-101 and T-102’s `[x]` as well. A reader who, as A says, would take `completed.md` alone as acceptance does not stop at the frontmatter. `invocations.yaml:2` is `verification_ran: false`. The overclaim that survives is that this tasklist marks T-103 done with no static-only qualifier. It is not a claim that the map’s commented percentage secretly means a run.

A’s own import caveat blocks “satisfied statically.” `tests/test_greeting.py:1` is `from src.greeting import greet`. The snapshot has no `src/__init__.py` and no `conftest.py`. A says exercise depends on that import and is therefore not purely static, then still says the content requirement is satisfied. Call expressions are present. That they exercise `greet` is not shown. `execution.log:5` says the opposite of a run. B’s token `static_cases_present_runtime_unproven` matches that. A’s “implemented on disk, unrun” matches the file and is silent on the tasklist.

A also narrowed X-001 after abandoning it. A now says its gap question (“whether static presence suffices for T-103 done”) is misframed, that R-003 needs no waiver, and that “the real question is the meaning of `done`.” That real question is the one B answers and the one A moved to B under X-002. It cannot be reused to keep X-001. On the bundled conflict, B stays ahead: the tasklist mark is an overclaim; the spec does not require a recorded pass; the cases are present and unproven. A wins only the withdrawn pass-requirement slice.

**C-004.** A now adopts the split, and the split is right. For `str`, `not name` is true exactly when `name == ""`, and `greet("")` raises, so that input is not a deviation and not a Regression. For `None`, `0`, `[]`, and `False`, `spec.md:9` is silent and `src/greeting.py:1` has no annotation, so rejecting them is extra and is Drift (LOW) unless something approves it. Nothing in `spec.md:9`, `completed.md:7`, `execution.log:3`, or `fixtures/project/proposed.md:7` does.

“Closer” does not follow. The split is not “D-1 may be reclassified as no-deviation.” A’s recommendation (`variant-1-original.md:27`) is one label for the whole item: “Drift (LOW) or no-deviation.” The second option drops `None`/`0`/`[]`/`False`. A admits the hedge at `variant-1-original.md:16` and `:27` is unscoped. B’s chain (`variant-2-original.md:16`) already has the split’s shape: “no contradiction for `''` -> not Regression; unstated broadening with no rationale -> Drift.” Drift’s object is the broadening, not the empty string. Missing pieces are the explicit non-str domain and `severity` (S-002, still A’s). An unscoped binary is not nearer the split than that chain. C-004 stays B. X-003 stays equal: neither card writes the domain.

**S-002.** Concede, unchanged. If the class is Drift, LOW is the right field, because `""` still raises and `greet("Ada")` is unchanged. B has no severity. A’s reason “str-equivalent broadening” is the wrong justification: the str case is equivalent, and the broadening is the non-str part. The field still belongs to A.

**S-004.** Concede, unchanged. A’s hunk refs are navigable; `none` three times is not. Qualification only: gap 1’s ref `tests/test_greeting.py:1` is the import, not the missing log, and `changes.patch:1-9` still has no test hunk. That mis-point does not make `none` better.

**C-011.** Concede, unchanged. `interaction-effects.yaml:7` is `genuinely_shared: true` and `:12` says changing the guard at line 2 affects the R-001 path. The file is 13 lines; A’s `:14-21` does not exist. The bad range is C-014, not a reason to drop the finding. B never raised the coupling.

**C-012.** Concede, unchanged, with a limit on why A wins. Narrowing `if not name` to `name == ""` turns `greet(None)` from `ValueError` into `f"Hello, {None}!"` at `src/greeting.py:4`. The tests call only `"Ada"` and `""`. `interaction-effects.yaml:12` says both requirement paths are covered statically; it does not mention `None`. A’s “or record rationale/spec amendment” (`variant-1-original.md:28`) is the branch that keeps the broad behavior only on purpose. B’s first branch does not.

A’s verifier does not earn the point. `greet('')` raises and `greet('Ada') == 'Hello, Ada!'` under both predicates, so it cannot see the `None` change. The superiority is the amendment option, not those two asserts. B’s other branch, “stop calling falsy broadening authorized,” does not change `None` either, and it is a label fix filed under `src/greeting.py`. The same `:12` note, which says the coverage is static, is what B’s “must not become runtime clearance” is aimed at; it supports that risk and does not rescue the untested narrowing.

**S-008.** Move to equal. B’s four items are finer (guard, assertion, diff, import). A’s first item targets `t1-card.md` with a rule-level verifier B does not have. B’s items 2–4 do mirror `t1-card.md:45-47`. A is right that mirroring does not make them worse recommendations, and it also does not make the set the better organization once A’s upstream target is counted. Granularity is already scored at C-013.

**S-005 (A moved this to equal).** Keep B. The point is the field’s type. `decision_needed_by_user` is a predicate; a boolean can be false, and A’s string cannot. A’s extra words on gap 1 are the question A now calls misframed. B’s `true` on the provenance gap still does not restate the question; that text is in the sibling fields (`variant-2-original.md:19`). That hole was concession 5. It does not equalize the interface.

**C-005.** A’s concession is right; the limit A adds is also right. `name == ""` is an identity for `str` and differs only on non-str falsy values. The card never says that. The elimination still holds: a documented forcing constraint is missing, and the spec-exact check meets `spec.md:9`, `tests/test_greeting.py:10`, `completed.md:7`, and `execution.log:3`. Point stays B.

**C-007 / X-002.** Accepted. `invocations.yaml:3` is an orchestrator surface choice, not a pytest result. The missing log is closable by a re-run. B’s omission of line 3 remains a citation gap, not a reason to put a user in front of pass/fail.

**C-008.** Move to equal. Both mark the import `[INFERRED]` and unobserved. Keeping it as its own decision-free gap is S-006 and C-007, already B.

**C-009.** Keep B. The whitespace, truthy non-str, and any-`ValueError` holes are real, and A dropped them. A’s caveats are right and do not move the point: `"   "` and truthy non-strings are non-empty under both predicates, and B still does not ask for tests for them (concession 8).

**C-010.** Move to equal. “completion 1.0 is not an acceptance pass” is sharper than “all verdicts static,” but the percentage’s own comment already says static, and the R-003 half of B’s risk over-reads the spec. A’s `invocations.yaml:2-3` line is the cleaner evidence sentence. The tasklist finding is carried at C-003 / X-001, not here.

**C-003.** Stays B, on narrower grounds than Round 1. Only B’s T-103 verdict flags the tasklist against `verification_ran: false`. The spec-requires-a-run half is withdrawn above. A’s verdict describes the file and leaves `completed.md:8` standing.

**A-005.** Keep B. `static_cases_present_runtime_unproven` does not say the executor authored the file. “implemented … outside supplied diff” still says implemented. The location caveat does not cancel the verb. Both still fail to condition the verdict on the provenance gap, which is why the assumption stays QUALIFY rather than why the verdicts are equal.

#### Updated assessment of Variant A

A’s Round 2 is better than A’s card. It adopts the str / non-str split, concedes the `name == ""` elimination of Necessary, concedes the three-way gap and X-002, and ties bare `status: done` to a real reporting gap. Those concessions should be merged.

What still stands on the card, and should be kept, is `severity: LOW`, navigable hunk refs, the shared-`greet` coupling note, the “narrow or amend” path, and a recommendation aimed at `t1-card.md` with an approving-artifact verifier.

What the rebuttal does not repair is the card. T-102 is still “implemented (static only)” with D-1 off in another section. The recommendation still offers whole-item “no-deviation.” Gap 1 still bundles “nothing ran” with importability and asks whether static presence suffices for done, the question A now calls misframed. The rebuttal’s X-001 defense splits `[x]` from `status: done` inside a single tasklist, and “content requirement satisfied statically” conflicts with the import caveat in the same rebuttal.

#### New evidence

Snapshot root: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/`.

- `completed.md:2` is `status: done` and `:8` is `[x]` plus “implements … tests.” Same record. The status line was already cited in Round 1; A’s concession on it is correct; the checkbox exemption is new and does not hold.
- No `__init__.py` and no `conftest.py` under that snapshot root. `tests/test_greeting.py:1` imports `src.greeting`. Import failure stays `[INFERRED]`.
- `interaction-effects.yaml` is 13 lines. The load-bearing sentence is `:12` (guard edit hits the R-001 path; both requirement paths “covered … (statically)”). `:14-21` is not in the file. The tests behind that sentence are `"Ada"` and `""` only.
- `fixtures/project/proposed.md:7` is “Reject an empty name using ValueError.” It does not approve falsy broadening. It is outside the snapshot.
- Re-read this round: `changes.patch:6-9` is `src/greeting.py:1-4`. A did not re-read the patch. Identity still holds, and it still does not cover `tests/test_greeting.py`.

#### Shared assumptions

- **A-002: QUALIFY (unchanged).** For `str`, `not name` iff `name == ""`. Whitespace is truthy under both. The extra behavior is non-str falsy rejection, which is Drift (LOW) unless an approving artifact exists, not no-deviation and not Necessary. A now adopts this. Neither card states it.
- **A-005: QUALIFY (unchanged).** Cases are on disk at `tests/test_greeting.py:4-5` and `:8-13`. Reject executor authorship. The file is outside `changes.patch:1-9`, `in_supplied_diff: false`, `in_scope_flag: false` (`task-to-work-map.yaml:30-31`), and the repo has git init only (`task-to-work-map.yaml:36`). `execution.log:4` is a self-report. B’s token is the less authored wording; both verdicts still treat the file as T-103 work.
- **A-006: QUALIFY (unchanged for me; A moved from ACCEPT to QUALIFY).** `proposed.md:7` does not authorize the broadening, so “not Authorized” survives. Completeness of the search was never shown, and neither card states the scope.
- **A-007: ACCEPT (unchanged), `src/greeting.py` only.** `changes.patch:6-9` matches `src/greeting.py:1-4`. It does not extend to `tests/test_greeting.py`.

#### Updated per-point positions

| point | superior (A / B / equal) | changed from R1? | one-line reason |
|---|---|---|---|
| S-001 | B | n | `coverage_audit` is accurate; A has no coverage section. |
| S-002 | A | n | LOW is the right field because `""` is not contradicted; B has none. |
| S-003 | B | n | A now agrees the tokens separate clean, drift, and unproven. |
| S-004 | A | n | Navigable refs beat `none`; the import-line mis-point does not flip it. |
| S-005 | B | n | A boolean can say false; A’s string cannot, and its question is the one A now calls misframed. |
| S-006 | B | n | Provenance, unrun tests, and inferred import are separate failures. |
| S-007 | equal | n | Path formatting is cosmetic. |
| S-008 | equal | y | B is finer-grained; A’s `t1-card.md` target is the root-cause item; mirroring is not incorrectness. |
| C-001 | equal | n | T-101 verdicts are the same substance. |
| C-002 | B | n | Only B’s T-102 verdict carries D-1. |
| C-003 | B | n | Only B flags the tasklist against `verification_ran: false`; the spec-requires-a-run half is withdrawn. |
| C-004 | B | n | Unscoped “or no-deviation” collapses D-1; B already separates `''` from the broadening. |
| C-005 | B | n | A conceded; `name == ""` meets the stated requirement and bites only off `str`. |
| C-006 | equal | n | Both leave out-of-diff provenance as a user decision. |
| C-007 | B | n | A conceded; `invocations.yaml:3` makes the gap a re-run, not a policy question. |
| C-008 | equal | y | Both mark the import `[INFERRED]`; the split is already scored at S-006 and C-007. |
| C-009 | B | n | Blank, truthy non-str, and any-`ValueError` stand; they are not fixed by the guard, and B still requests no tests. |
| C-010 | equal | y | The 1.0 sentence is sharper, but the map comment already says static, and B’s R-003 half over-reads the spec. |
| C-011 | A | n | `:12` shows the guard edit hits R-001; the bad `:14-21` range does not remove it. |
| C-012 | A | n | Amendment-or-narrow beats an untested narrowing; A’s `greet('')`/`greet('Ada')` verifier is also `None`-blind. |
| C-013 | B | n | Assertion, diff scope, and importability are separate; a green log closes none of them. |
| C-014 | B | n | `:14-21` is outside a 13-line file; B’s cites resolve; `invocations.yaml:3` stays under-mentioned. |
| C-015 | equal | n | Calibration inverts self-report; neither score is evidence. |
| X-001 | B | n | No pass requirement in `spec.md:12`; `status: done` and `[x]` are still one completion claim against `verification_ran: false`. |
| X-002 | B | n | A conceded; only provenance and the meaning of done need a user. |
| X-003 | equal | n | No-deviation for `str` only, Drift for non-str falsy; neither card states that. |
| A-002 | equal | n | The equivalence holds and neither card writes it; A now adopts the split. |
| A-005 | B | n | B’s token does not say “implemented”; “outside supplied diff” does not cancel A’s verb. |
| A-006 | equal | n | `proposed.md:7` does not authorize; the search scope is still unstated. |
| A-007 | equal | n | `src/greeting.py:1-4` matches `changes.patch:6-9`; the tests file is outside the patch. |

## Round 2.5: Invariant Probe

An independent fault-finder (opus) probed the post-Round-2 consensus. The assembled findings are in `invariant-probe.md`, and the raw output is `round-2-5/fault-finder-opus-raw.md`. Result: 15 findings, 8 ADDRESSED and 7 UNADDRESSED. The only HIGH UNADDRESSED finding is INV-014. The MEDIUM UNADDRESSED findings are INV-001, INV-007 and INV-012.

## Round 3: Final Arguments

Not executed. Round 3 skipped: depth=standard. Round 3 requires `--depth deep`.

## Scoring Matrix

### Confidence calibration rules applied (deterministic)

These implement `scoring_matrix.confidence_calibration` (SKILL.md) and the caller's directive. With N=2, both advocates agreeing counts as unanimous. 90-100 is used only where the losing advocate conceded. 100% is never assigned. A split is unresolved at 50%.

| Rule | Condition | Confidence |
|------|-----------|-----------|
| U1 | Unanimous winner, stable R1→R2, and the losing advocate's concession is unqualified | 95% |
| U2 | Unanimous winner reached in R2 by the loser's concession, or a qualified/limited concession | 90% |
| T1 | Unanimous "equal" (tie), stable R1→R2. No loser exists to concede, so it stays below 90. | 80% |
| T2 | Unanimous "equal" reached in R2 by a position move | 75% |
| SPLIT | R2 positions differ (no majority with N=2) | 50%, winner = Unresolved |
| Adj −5 | An UNADDRESSED Round 2.5 finding directly challenges the point's evidence or premise (applied at most once per point; not applied to SPLIT points, which are already at the floor) | −5 |

| Diff Point | Winner | Confidence | Rule | Evidence Summary |
|------------|--------|------------|------|------------------|
| S-001 | Variant B | 95% | U1 | Both advocates hold B in R1 and R2; A conceded outright that it has no coverage section. B's `coverage_audit` is accurate (`spec.md:3` is non-normative). |
| S-002 | Variant A | 90% | U2 | Both hold A; B conceded that LOW is the right severity, but said A's 'str-equivalent' justification is the wrong reason (qualified concession). |
| S-003 | Variant B | 90% | U2 | A moved from equal to B in R2 (concession). B's snake_case tokens separate clean, drift and runtime-unproven states, where A gives T-101 and T-102 the same label. |
| S-004 | Variant A | 90% | U2 | Both hold A. B conceded that the navigable hunk refs beat `none`×3, with the qualification that gap 1's ref points at the import line, not the missing log. |
| S-005 | Unresolved | 50% | SPLIT | R2: A says equal (A's string cannot say 'none'; B's `true` loses the question), B says B (a boolean can be false). No majority, so the point is unresolved. |
| S-006 | Variant B | 95% | U1 | Both hold B in both rounds; A conceded that its gap 1 conflates two questions. Provenance, unrun tests and the inferred import are separate failures. |
| S-007 | Tie (equal) | 80% | T1 | Both say equal in both rounds: path formatting is cosmetic. |
| S-008 | Tie (equal) | 75% | T2 | B moved to equal in R2. B's items are finer-grained, A's rec 1 targets the T1 card at root cause, and granularity is already scored at C-013. |
| C-001 | Tie (equal) | 80% | T1 | Both say equal in both rounds: the T-101 verdicts are substantively identical. |
| C-002 | Variant B | 95% | U1 | Both hold B; A conceded in R1 and R2 that only B's T-102 verdict carries D-1. |
| C-003 | Unresolved | 50% | SPLIT | R2: A says equal (the R-003 text is met statically, but B surfaced the `status: done` semantics), B says B (only B flags the tasklist against `verification_ran: false`). Unresolved; also impugned by HIGH INV-014. |
| C-004 | Unresolved | 50% | SPLIT | R2: A says A (the hedge plus LOW is closer to the str/non-str split), B says B (the unscoped 'or no-deviation' collapses D-1). Both adopt the same split substantively but disagree on which card is closer. Unresolved. |
| C-005 | Variant B | 90% | U2 | A conceded in R2 that the `name == ""` counterfactual is the stronger Necessary elimination, noting the limit that it bites only on non-str falsy values. B accepts the limit. |
| C-006 | Tie (equal) | 80% | T1 | Both say equal in both rounds: out-of-diff provenance is a user decision (`task-to-work-map.yaml:35-36`). |
| C-007 | Variant B | 85% | U2 -5 | A conceded in R2 that `invocations.yaml:3` makes the runtime gap a re-run, not a policy question. −5 because UNADDRESSED MEDIUM INV-001 (the re-run needs surface approval) and INV-012 (the run is environment-dependent) challenge that premise. |
| C-008 | Tie (equal) | 70% | T2 -5 | B moved to equal in R2: both mark the import risk [INFERRED]. −5 because INV-007 and INV-009 note that the shared evidence ('no conftest in snapshot') cannot be shown by the snapshot. |
| C-009 | Variant B | 90% | U2 | Both hold B. A conceded the whitespace, non-str and any-ValueError risks with two caveats: they are orthogonal to the guard, and B requests no tests for them. |
| C-010 | Tie (equal) | 70% | T2 -5 | Both moved to equal in R2: B's 'not an acceptance pass' is sharper, but the map comment already says static and B's R-003 half over-reads `spec.md:12`. −5 because of HIGH INV-014 (the R-003 sufficiency is unresolved). |
| C-011 | Variant A | 95% | U1 | Both hold A; B conceded plainly that `interaction-effects.yaml:12` supports the coupling risk despite A's bad line range. |
| C-012 | Variant A | 90% | U2 | Both hold A. B conceded, limited to A's 'record rationale/spec amendment' branch: A's `greet('')`/`greet('Ada')` verifier is also blind to `None`. |
| C-013 | Variant B | 90% | U1 -5 | Both hold B; A conceded that B's three distinct remediations are better. −5 because UNADDRESSED MEDIUM INV-012 shows that B's 'pytest from project root' verifiers are environment-dependent. |
| C-014 | Variant B | 95% | U1 | Both hold B; A conceded that `interaction-effects.yaml:14-21` is out of range in a 13-line file. B's checked citations resolve, though it under-mentions `invocations.yaml:3`. |
| C-015 | Tie (equal) | 80% | T1 | Both say equal in both rounds: calibration inverts self-report, and neither score is evidence. |
| X-001 | Unresolved | 50% | SPLIT | R2: A says A (`spec.md:12` and `completed.md:8` require no run), B says B (`status: done` and `[x]` are one completion claim against `verification_ran: false`). Unresolved; directly impugned by HIGH INV-014. |
| X-002 | Variant B | 85% | U2 -5 | A conceded in R2: runtime pass/fail needs a saved log, and only provenance and the meaning of `done` need a user. −5 because UNADDRESSED MEDIUM INV-001 says closing it needs surface approval. |
| X-003 | Tie (equal) | 70% | T2 -5 | A moved to equal in R2: no-deviation applies to `str` only, Drift to non-str falsy values, and neither card states the split. −5 because INV-011 says 'no Regression' completeness is uncited. |
| A-002 | Tie (equal) | 70% | T2 -5 | A moved to equal in R2 and adopted B's formulation (str domain meets R-002; non-str falsy rejection is Drift LOW). −5 because INV-004 says the 'None, 0, [], False' list is not exhaustive. |
| A-005 | Unresolved | 50% | SPLIT | R2: A says equal (A's wording carries the provenance caveat, B's token is authorship-neutral), B says B (`implemented` still asserts authorship). Unresolved; also bears on INV-014 and INV-015. |
| A-006 | Tie (equal) | 80% | T1 | Both say equal in both rounds: `proposed.md:7` does not authorize the broadening, but the search scope is unstated (A moved ACCEPT→QUALIFY on the assumption, not the point). |
| A-007 | Tie (equal) | 80% | T1 | Both say equal in both rounds: `src/greeting.py:1-4` equals `changes.patch:6-9`, which does not extend to the tests file (INV-003 adds manifest-hash support). |

**Debate tally** (input to the Step 3 tiebreaker): Variant A won 4 points, Variant B won 10, 11 agreed ties, 5 unresolved.

## Per-Point Tracking

Positions are taken from each advocate's per-point table (R1 "Per-point positions", R2 "Updated per-point positions"). `agreed` reflects the final round (R2), and `winner` is null when not agreed.

| point_id | taxonomy_level | A R1 | B R1 | R1 agreed | A R2 | B R2 | agreed | winner |
|----------|----------------|------|------|-----------|------|------|--------|--------|
| S-001 | L2 | B | B | yes | B | B | true | Variant B |
| S-002 | L2 | A | A | yes | A | A | true | Variant A |
| S-003 | L1 | equal | B | no | B | B | true | Variant B |
| S-004 | L2 | A | A | yes | A | A | true | Variant A |
| S-005 | L2 | A | B | no | equal | B | false | null |
| S-006 | L2 | B | B | yes | B | B | true | Variant B |
| S-007 | L1 | equal | equal | yes | equal | equal | true | Tie (equal) |
| S-008 | L2 | equal | B | no | equal | equal | true | Tie (equal) |
| C-001 | L2 | equal | equal | yes | equal | equal | true | Tie (equal) |
| C-002 | L3 | B | B | yes | B | B | true | Variant B |
| C-003 | L2 | A | B | no | equal | B | false | null |
| C-004 | L3 | A | B | no | A | B | false | null |
| C-005 | L3 | A | B | no | B | B | true | Variant B |
| C-006 | L2 | equal | equal | yes | equal | equal | true | Tie (equal) |
| C-007 | L2 | equal | B | no | B | B | true | Variant B |
| C-008 | L2 | equal | B | no | equal | equal | true | Tie (equal) |
| C-009 | L3 | B | B | yes | B | B | true | Variant B |
| C-010 | L2 | A | B | no | equal | equal | true | Tie (equal) |
| C-011 | L2 | A | A | yes | A | A | true | Variant A |
| C-012 | L3 | A | A | yes | A | A | true | Variant A |
| C-013 | L2 | B | B | yes | B | B | true | Variant B |
| C-014 | L2 | B | B | yes | B | B | true | Variant B |
| C-015 | L2 | equal | equal | yes | equal | equal | true | Tie (equal) |
| X-001 | L2 | A | B | no | A | B | false | null |
| X-002 | L2 | A | B | no | B | B | true | Variant B |
| X-003 | L3 | A | equal | no | equal | equal | true | Tie (equal) |
| A-002 | L3 | A | equal | no | equal | equal | true | Tie (equal) |
| A-005 | L2 | A | B | no | equal | B | false | null |
| A-006 | L2 | equal | equal | yes | equal | equal | true | Tie (equal) |
| A-007 | L2 | equal | equal | yes | equal | equal | true | Tie (equal) |

Round-by-round alignment: R1 = 16/30 = 53.3% (below threshold). R2 = 25/30 = 83.3%. No point flipped between A and B across rounds; every move was toward "equal" or to the other side by concession. No oscillation. Termination: max rounds reached for depth=standard. The stable-majority condition was not met because R1 was below threshold.

## Convergence Assessment

### Diff-point agreement
- Formula: convergence = agreed_points / total_diff_points
- Denominator used: **30**. total_diff_points = count(S-NNN) 8 + count(C-NNN) 15 + count(X-NNN) 3 + count(A-NNN promoted [SHARED-ASSUMPTION]) 4 = 30.
  - Why: per `shared_assumption_extraction.promotion_to_diff_points`, only UNSTATED assumptions become synthetic diff points. Diff-analysis promoted exactly A-002, A-005, A-006 and A-007. A-001, A-003, A-004, A-008 and A-009 are STATED, were not promoted, and were not debated as points, so they are excluded.
  - U-NNN (unique contributions, 11) are not diff points and are excluded per `total_diff_points_calculation`.
  - Sensitivity (non-normative): counting all 9 A-NNN rows would give 25/35 = 71.4%. That reading contradicts the promotion rule and is not used.
- Points resolved: 25 of 30
- Alignment: 83.3%
- Threshold: 80%
- Diff-point gate: PASS (83.3% ≥ 80%)

### Taxonomy coverage gate (AD-5)
| Level | Points debated | Agreed | Covered (>0 addressed) |
|-------|----------------|--------|------------------------|
| L1 surface | 2 (S-003, S-007) | 2 | yes |
| L2 structural | 21 | 17 | yes |
| L3 state-mechanics | 7 (C-002, C-004, C-005, C-009, C-012, X-003, A-002) | 6 | yes |

Levels come from the diff-analysis.md `Level` column (auto-tagged in Step 1). A-001 is L3 in diff-analysis but was not promoted, so it is not counted here. All three levels were addressed by both advocates in R1 and R2. Gate: **PASS**. No forced round was triggered.

### Invariant probe gate (AD-1)
- count(HIGH ∧ UNADDRESSED) = **1** → gate **BLOCKS**

```
CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-014
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

- INV-014 (sufficiency_challenge): neither the "T-103 implemented" nor the "R-003 met" verdict is conditioned on the tests actually being collected. Under plain `pytest`, with no `conftest`, `__init__` or `pythonpath`, collection of `from src.greeting import greet` is predicted to fail. Neither verdict names which pytest invocation or environment counts.

```
WARNING: 3 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-007, INV-012
These items do not block convergence but should be reviewed.
```

- INV-001: "closable by re-run" ignores that the skipped surface needs approval (C-007, X-002).
- INV-007: row agreement is not verification of the row's evidence (C-008).
- INV-012: a pytest run from the fixture root is environment-dependent, because the ancestor `pyproject.toml` becomes rootdir and the `pytest11` plugin may autoload (C-007, C-013).
- LOW UNADDRESSED (INV-004, INV-009, INV-011): no action per gate algorithm.

### Final status
- Status: **BLOCKED_BY_INVARIANTS**. Agreement is 83.3% ≥ 80% and all taxonomy levels are covered, but one HIGH-severity UNADDRESSED invariant (INV-014) remains.
- Convergence is **not** declared.
- Unresolved points: S-005, C-003, C-004, X-001, A-005
- Blocking invariants: INV-014
- Downstream note: per the error-handling matrix, a non-converged debate proceeds to Step 3 force-select by score and must document the non-convergence. INV-014 should be carried into the refactor plan as an explicit condition on any T-103/R-003 verdict, or acknowledged by the user as accepted risk.
