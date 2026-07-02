# Agent C — Why Tier-2 `/sc:reflect` Missed F1–F4: the Deviation-Taxonomy + Verification-Triangle Blindspot

**Scope:** Post-execution reflect audit of `TASK-RF-detection-contract-20260701-164700` (return contract `156f28292b4d`) returned **PASS / regression 0 / tier 2 / non-degraded** yet Augment caught 4 real correctness bugs (F1–F4) on PR #209. This report establishes the miss concretely and traces the two *structural* reasons reflect could not have found them.

The 4 bugs (all in `src/superclaude/pr_submit/contract_setup/`, all 100% spec-conformant — the merged requirements/design never define the micro-decisions they get wrong):
- **F1** `diagnosis.py` — file-vs-dir evidence guard (`probe_evidence` treated as file; spec never says it must be a file).
- **F2** `candidate.py` — app-slug bucket.
- **F3** `questions.py` — `probe_pr` operator answer silently ignored (default derived via `_evidence_attr('pr_number')` reading a nonexistent `answers.pr_number`).
- **F4** `candidate.py` — `_path_resolves()` all-None quirk (a key missing on every element collapsed to "resolved," falsely allowing lockability).

Fix commits: `f6a32e9a` (F1/F2) and `21d4b8e0` (F3/F4) on `dc507305..21d4b8e0`.

---

## 1. Did ANY reviewer or the adversarial pass mention anything near F1–F4? — NO. Concrete miss.

The three swarm slots and the adversarial merge produced **zero** findings touching the logic of `diagnosis.py`, `candidate.py`, or `questions.py`. Every finding was about the task file's own **completion bookkeeping**, not code correctness.

**Slot 00 (kimi-k2.7-code):** never produced a review. `t2-swarm/reflect-review-00-kimi-k2.7-code.meta.json` exists but there is **no** `reflect-review-00-...final.md`; `return-contract.yaml:5` records `reviewer_count: 2`. So the ensemble degraded to 2 live reviewers (one of which truncated — see below), yet the top-level contract reports `degraded_components: []` and `status: success`.

**Slot 01 (qwen3.6-plus)** — the only complete review. Its 5 findings (`reflect-review-01-qwen3.6-plus.final.md:15-38`) are entirely gate/state bookkeeping:
- F#1 "Frontmatter/Execution State Drift" (`status: 🟠 Doing` vs Summary `Completion Date: 2026-07-02`)
- F#2 "Hard Gate Bypass Risk (Step 5.6)" — post-reflect wrapper `[ ]`
- F#3 "QA Protocol Deviation (Step 5.3)" — the `7`→`6` doc-count fix
- F#4 "Broad Test Run vs. Scoped Verdict Discrepancy"
- F#5 "Unresolved Decision State in Frontmatter" — `reflect_post: ""`

Its "Suspect-Source Files" table (`:58-65`) even *names* `diagnosis.py` and `candidate.py`'s sibling `validation.py`/`lockgate.py` — but only as **"elevated scrutiny recommended"** for *downstream* scoring, with risk vectors tied to phase-QA fix cycles, never an actual read of the shipped logic. The reviewer flagged the neighborhood and walked past the bugs.

**Slot 02 (glm-5.2)** — **truncated at 19 lines**, cuts off mid-sentence at `**Completion Date:** ` (`reflect-review-02-glm-5.2.final.md:20`; corroborated by `diff-analysis.md:7` "TRUNCATED — cuts off mid-sentence"). It produced exactly one partial finding (F-001, the same frontmatter drift) before dying. Zero code findings.

**Adversarial pass (`t2-adversarial/`):** The debate had nothing correctness-shaped to debate. `debate-transcript.md:10` declares a **"Degenerate-input notice"** (Variant 2 is a fragment) and substitutes "ground-truth adjudication" — but that adjudication (`debate-transcript.md:47-61`) only re-verifies the *bookkeeping* claims already made (status Doing, reflect_post empty, 5.6 unchecked). `invariant-probe.md` probes exactly one assumption family: whether running Step 5.6 alone greens "Done" (INV-001..004). **Not one invariant, diff-analysis row, or debate turn examined `_path_resolves`, `_evidence_attr`, or the evidence file/dir guard.** The consolidated verdict (`reflect-review-consolidated.md:19`) is "CONDITIONAL FAIL — completion gates unresolved," with `**changed-file test set passes**` cited as the *positive* correctness signal.

**Conclusion of §1:** The entire Tier-2 budget was spent auditing whether the *task marked itself done correctly*, and unanimously (86% convergence) concluded "not yet — run the wrapper." The shipped code's behavior was never the object of review.

---

## 2. Structural root cause: the deviation taxonomy measures *against the driving spec*, and the spec is silent on F1–F4.

Reflect UC-2 does not ask "is this code correct?" It asks "does every divergence from the driving spec/tasklist classify cleanly?" The taxonomy is explicitly, definitionally spec-relative:

> "Reflection's defining contribution beyond a generic verification protocol is *classifying* every divergence between expected and actual work into a concrete, decision-driving category." — `refs/deviation-taxonomy.md:5`

> "The **gold-standard reference** for 'what was expected' is the **driving spec/tasklist** (the artifact the agent was instructed to fulfil)". — `refs/deviation-taxonomy.md:7`

All four classes anchor on the spec as the oracle of "expected":
- **Authorized** — "a scope addition ... approved by an authoritative artifact" (`:28`).
- **Necessary** — "does NOT contradict any acceptance criterion in the spec" (`:49`).
- **Drift** — "A silent change not in the original spec/tasklist" whose distinguishing test is "Does NOT contradict any acceptance criterion" (`:58,64`).
- **Regression** — "A change that *contradicts* an acceptance criterion, an explicit constraint in the spec, or a previously-passing test" (`:75`).

F1–F4 are **spec-conformant**: the merged requirements never say `probe_evidence` must be a file (F1), never define `_path_resolves` all-None semantics (F4), never specify the `probe_pr` answer plumbing (F3), never pin the app-slug bucket (F2). So each bug produces **zero divergence-from-spec** to classify. Under a taxonomy whose four buckets are all "distance from spec," a bug that faithfully implements a spec that never contemplated the case is **invisible** — it lands in none of Authorized/Necessary/Drift/Regression because there is nothing for it to diverge *from*. Reflect asks "did they build what the spec said?"; it does **not** ask "is what they built correct where the spec was silent?" The taxonomy is a conformance auditor, and F1–F4 are conformance-clean correctness bugs.

Note the SKILL even rejected a standalone `deviation-classifier` agent on the grounds that "deviation classification *is* mechanical mapping (the §10 taxonomy is the classifier)" (`SKILL.md:656`). That is exactly the point: a *mechanical spec-diff mapper* has no seat for an open-ended "is this logic wrong?" judgement. There is no correctness/oracle lens anywhere in the pipeline.

---

## 3. The verification-triangle double failure.

Reflect's one non-spec-relative correctness surface is the §6.1 step 5.5 verification triangle — it runs the tests as ground truth and feeds the Regression detector:

> "Step 5.5 ... is the **verification triangle** — `get_diagnostics_for_file` + `summarize_changes` + `execute_shell_command` (step 5.5, does it pass)." — `SKILL.md:525`

> Regression detection: "A test that previously passed now fails after the diff — detected by the default-on §6.1 step 5.5 verification triangle (`execute_shell_command`), not the task-log self-report. ... When verification is unavailable, this degrades to the task-log claim with a Grounding Gap entry." — `refs/deviation-taxonomy.md:80`

**(a) The triangle never ran.** The return contract records:
```
verification_ran: false                        (return-contract.yaml:18)
verification_skip_reason: tool-unavailable     (:19)
```
Per `SKILL.md:525`, step 5.5 "runs only when `execute_shell_command_available` is true ... otherwise it skips with the matching `verification_skip_reason` and degrades §10.4 Regression detection to the task-log claim." So `regression: 0` (`return-contract.yaml:12`) and `regression_present: false` (`:23`) were derived **without executing a single test** — from the task log's own self-report that its changed-file set passes. The one correctness gate reflect owns was **off**, and — critically — the contract still reports `status: success` and `degraded_components: []` (`:2,28`). The skip was silent: a "tool-unavailable" verification degrade did not lower the headline verdict.

**(b) The triangle would have passed anyway — the tests encoded the bug.** Even a fully-armed triangle would not have caught F4. The fix commit `21d4b8e0` states verbatim: *"Updated the severity-path test that pinned the old behavior (a review with no severity now correctly resolves to `comments[].severity`, not `reviews[].severity`)."* The pre-fix `_path_resolves` all-None quirk was **asserted as correct** by `tests/pr_submit/test_contract_setup_validation.py`. So `pytest` on the author's own suite would have exited 0 and the exit-code mapping (`refs/deviation-taxonomy.md:107`, "`pytest` exit 0 → clean") would have confirmed `regression_present: false`. The oracle and the bug were written by the same author in the same task, so the oracle ratified the bug. Green tests here are a **tautology**, not evidence.

The double failure: reflect skipped its only correctness gate (a), and the gate was a rigged oracle that would have greened the bug regardless (b).

---

## 4. Was `regression: 0` unearned? Yes — reflect's regression lens is structurally blind to first-implementation bugs.

`refs/deviation-taxonomy.md:75` defines Regression as work that "*undoes or violates a documented commitment*" — "contradicts an acceptance criterion, an explicit constraint ... **or a previously-passing test**." Every prong is **differential**: it measures the new state against a *prior* committed state (a criterion previously stated, a test previously green). The gold-standard reference is literally "**verified test-suite state pre/post**" (`:83`).

`contract_setup/` is a **brand-new package** in this task. There is no "previously-passing test" for `_path_resolves` or `_evidence_attr` — they never existed before. A first-implementation bug cannot regress a baseline it has no baseline for. By construction, F1–F4 are **outside the Regression class's domain of definition**: not "checked and found clean," but "unmeasurable, because Regression is a delta and there is no `t-1` term." `deviation_count_by_class.regression: 0` (`return-contract.yaml:12`) is therefore **vacuously true, not earned** — it is the correct answer to a question ("did anything regress from before?") that is orthogonal to the one that mattered ("is this new code correct?"). Reflect's regression lens can only catch bugs that *break something that used to work*; it is congenitally blind to *shipping something that never worked*.

---

## 5. Recommended reflect-protocol changes (2–3).

**R1 — Add a spec-independent "correctness/oracle" reviewer lens (highest value).** The taxonomy's four classes are all spec-relative; add a fifth *review objective* (not a fifth deviation class) to the `reflect-reviewer` brief: *"Ignore the spec for this pass. Read each new/changed function and ask: given its own signatures, callers, and data shapes, does it do the obviously-correct thing on edge inputs (empty list, all-None, missing key, file-vs-dir, an operator answer that must be threaded through)? Report logic bugs even where the spec is silent."* This is exactly the class of reasoning Augment applied to F1–F4. It slots into the existing heterogeneous-reviewer fan-out without new tooling. Frame as reliability/correctness coverage.

**R2 — Treat `verification_skip_reason: tool-unavailable` as a first-class STATUS DEGRADE, not a silent pass.** Today the contract emitted `verification_ran: false` + `status: success` + `degraded_components: []`. When the sole non-spec correctness gate is unavailable, the run should append `"verification:tool-unavailable"` to `degraded_components`, and any `regression: 0` derived without an executed triangle must be stamped `regression_evidence: task-log-self-report` (a Grounding Gap) so the PASS is visibly *unverified*. A headline PASS should never be reachable while the only correctness gate is off.

**R3 — Do not trust in-repo tests as the oracle when the same author wrote them in the same task.** F4 proves author-written tests can encode the bug. When the changed diff **adds or modifies the very tests** that the triangle would run (detectable: test files appear in the audited diff), down-weight a green triangle to "self-consistent, not independently verified" and require either R1's spec-independent read or an adversarial "would this test still pass if the intended behavior were the *opposite*?" mutation probe before crediting `regression_present: false`.

---

### Top recommendation

**R1: add a spec-independent correctness/oracle reviewer lens.** The root cause is not a bug in reflect's machinery — every gate behaved as specified — it is that *every* gate (deviation taxonomy, Regression class, verification triangle) measures conformance-to-spec or delta-from-baseline, and F1–F4 are conformance-clean, baseline-free correctness bugs. Only an oracle that reads the code on its own terms, spec set aside, closes that structural blindspot; R2/R3 stop the run from *claiming* a verified PASS while that lens is absent or rigged.
