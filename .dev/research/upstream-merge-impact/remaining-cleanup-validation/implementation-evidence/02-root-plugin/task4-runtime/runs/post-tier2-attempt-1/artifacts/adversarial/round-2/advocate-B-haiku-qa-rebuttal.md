<!-- Round 2 rebuttal (sequential, 2nd; saw A's rebuttal). Advocate for Variant B. Native Task worker (general-purpose), model slot: haiku, persona: qa. agentId a64980251869bbd7d. Persisted verbatim by the top-level pipeline driver. -->
## Response to criticisms

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

## Updated assessment of Variant A

A’s Round 2 is better than A’s card. It adopts the str / non-str split, concedes the `name == ""` elimination of Necessary, concedes the three-way gap and X-002, and ties bare `status: done` to a real reporting gap. Those concessions should be merged.

What still stands on the card, and should be kept, is `severity: LOW`, navigable hunk refs, the shared-`greet` coupling note, the “narrow or amend” path, and a recommendation aimed at `t1-card.md` with an approving-artifact verifier.

What the rebuttal does not repair is the card. T-102 is still “implemented (static only)” with D-1 off in another section. The recommendation still offers whole-item “no-deviation.” Gap 1 still bundles “nothing ran” with importability and asks whether static presence suffices for done, the question A now calls misframed. The rebuttal’s X-001 defense splits `[x]` from `status: done` inside a single tasklist, and “content requirement satisfied statically” conflicts with the import caveat in the same rebuttal.

## New evidence

Snapshot root: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime/runs/post-tier2-attempt-1/artifacts/reviewer-snapshot/root/`.

- `completed.md:2` is `status: done` and `:8` is `[x]` plus “implements … tests.” Same record. The status line was already cited in Round 1; A’s concession on it is correct; the checkbox exemption is new and does not hold.
- No `__init__.py` and no `conftest.py` under that snapshot root. `tests/test_greeting.py:1` imports `src.greeting`. Import failure stays `[INFERRED]`.
- `interaction-effects.yaml` is 13 lines. The load-bearing sentence is `:12` (guard edit hits the R-001 path; both requirement paths “covered … (statically)”). `:14-21` is not in the file. The tests behind that sentence are `"Ada"` and `""` only.
- `fixtures/project/proposed.md:7` is “Reject an empty name using ValueError.” It does not approve falsy broadening. It is outside the snapshot.
- Re-read this round: `changes.patch:6-9` is `src/greeting.py:1-4`. A did not re-read the patch. Identity still holds, and it still does not cover `tests/test_greeting.py`.

## Shared assumptions

- **A-002: QUALIFY (unchanged).** For `str`, `not name` iff `name == ""`. Whitespace is truthy under both. The extra behavior is non-str falsy rejection, which is Drift (LOW) unless an approving artifact exists, not no-deviation and not Necessary. A now adopts this. Neither card states it.
- **A-005: QUALIFY (unchanged).** Cases are on disk at `tests/test_greeting.py:4-5` and `:8-13`. Reject executor authorship. The file is outside `changes.patch:1-9`, `in_supplied_diff: false`, `in_scope_flag: false` (`task-to-work-map.yaml:30-31`), and the repo has git init only (`task-to-work-map.yaml:36`). `execution.log:4` is a self-report. B’s token is the less authored wording; both verdicts still treat the file as T-103 work.
- **A-006: QUALIFY (unchanged for me; A moved from ACCEPT to QUALIFY).** `proposed.md:7` does not authorize the broadening, so “not Authorized” survives. Completeness of the search was never shown, and neither card states the scope.
- **A-007: ACCEPT (unchanged), `src/greeting.py` only.** `changes.patch:6-9` matches `src/greeting.py:1-4`. It does not extend to `tests/test_greeting.py`.

## Updated per-point positions

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
