# Research: Repeated pre-implementation reviews of the Orca tracking plan

**Investigation type:** Historical source tracing and document analysis  
**Scope:** Session `ac2cd1fd-60f6-4b7c-942c-93026ea8edce`, planning incident only  
**Status:** Complete, with explicit verification limits below  
**Date:** 2026-10-23  
**Requested output path, not written:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/01-session-ac2cd1fd.md`


**Persistence note:** Main session transcribed the dedicated analyst return verbatim from its on-disk transcript because that agent cannot write reports. This does not claim producer-authored disk delivery.

## 1. Finding

The repeated reviews did not uncover twenty newly introduced regressions after sixteen successful fixes. They uncovered a mixture:

- Some corrections introduced demonstrable new plan defects.
- Several earlier findings were only partially corrected.
- Some important omissions already existed in the original plan.
- Several later findings demanded stronger tests than the driving specification itself listed.
- The specification contained conflicting instructions that the original plan copied without resolving.
- One later item duplicated other findings, and another explicitly described a note rather than a defect.

There were **two full pre-implementation reflection runs and one targeted independent review**, not three full review cycles. Both full runs reported `partial`; the targeted review reported `PARTIAL` for both selected findings. The final plan passed a structural quality check but was explicitly **not reviewed again**.

No production implementation was performed in this selected session. Its physical JSONL file has 954 lines. Its last substantive planning result is line 946; the live task folder contains implementation artifacts from subsequent activity, which I excluded from this incident.

### Evidence locations

The following absolute-path keys are used below.

| Key | Absolute path |
|---|---|
| Session | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl` |
| Plan | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/TASK-WF-designSpec-20261022-132541.md` |
| Source | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/source.md` |
| Requirements | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/brainstorms/20261022T011827Z-orca-upstream-tracking/merged-requirements.md` |
| First report | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/REPORT.md` |
| First merged findings | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/adversarial/merged-verdict.yaml` |
| First coverage matrix | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/artifacts/coverage-matrix.yaml` |
| Second report | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/REPORT.md` |
| Second merged findings | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml` |
| Second citation validation | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/artifacts/evidence-validation.yaml` |
| Targeted verdict | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v3-targeted-20261022155651/verdict.yaml` |
| Workflow inventory test | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.github/contract-tests/test-50-candidate-attribution.sh` |
| Existing workflow-shape test | `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.github/contract-tests/test-66-orca-publish-gate.sh` |

References such as “Plan v2:207” describe the historical version reconstructed from the logged write, **not the current file at that line**. The current on-disk plan is byte-identical to the reconstructed final v4.

**Key takeaways**

- This is a mixed-cause planning loop, not evidence that every correction created another regression.
- Exact historical plan contents are recoverable from the actual JSONL writes and edits.
- Report and finding counts require correction before reuse.

## 2. Chronological event chain

All timestamps below are UTC on 2026-10-22. These are actual events, excluding command templates, injected skill text, hook instructions, and task-notification boilerplate.

| JSONL line | Timestamp | Actual event |
|---|---|---|
| 15 and 37 | 13:25:22.131; 13:25:25.236 | Workflow command appears in the transcript. These are not two completed workflow runs. |
| 58 | 13:25:27.503 | Actual workflow skill invocation. |
| 141 | 13:31:04.606 | Writes original plan, version 1. |
| 150/151 and 163/164 | 13:31:11.613; 13:31:22.708 | Initial wording-cleanup attempt at Raw150 was blocked at Raw151 and did not apply; retry at Raw163 succeeded at Raw164. Reviewed v1 hash matches the first review snapshot. |
| 152 | 13:31:15.974 | Structural plan checks: headings, acceptance-criteria presence, forbidden patterns, dependencies. |
| 170 | 13:31:26.392 | First actual pre-implementation reflection invocation. |
| 194-454 | 13:32:10.279-14:03:52.502 | Thirteen actual agent dispatches: coverage, calibration, two reviewers, adversarial rounds, invariant probe, merge, citation validation. |
| 499 | 14:09:01.093 | Reports sixteen findings, thirteen rated important and three minor. Reflection status is `partial`, with two unsupported citations dropped but no finding dropped. |
| 511 | 15:06:19.930 | User authorizes applying the sixteen findings and rerunning the pre-review. |
| 544 | 15:08:38.839 | **Whole-file Write**, not an Edit, creates plan v2. |
| 558 | 15:08:48.329 | Second actual pre-implementation reflection invocation. |
| 574-789 | 15:09:10.536-15:40:32.555 | Another thirteen actual agent dispatches following the full review sequence. |
| 821 | 15:45:18.570 | Reports twenty numbered items. Status remains `partial`; two high-severity items block the adversarial merge. Recommends a targeted next review rather than a third full run. |
| 824 | 15:50:41.590 | User: “apply 01-20 as plan version 3”. |
| 841 | 15:53:15.796 | Whole-file Write creates plan v3. |
| 843/849 | 15:53:19.603 onward | Structural gate passes. It checks shape and backward dependencies, not the semantic correctness of every change. |
| 856 | 15:53:35.506 | Reports v3 and recommends checking only the two blockers. |
| 858 | 15:54:59.545 | User explicitly authorizes that narrowed review. |
| 862 | 15:55:10.904 | One fresh reviewer is dispatched for the validation-before-use and up-to-date-state findings only. |
| 874 | 15:56:35.717 | Reviewer returns `PARTIAL` for both, with additional omissions and contradictions. |
| 877 | 15:56:51.622 | Orchestrator persists a condensed targeted verdict. |
| 885 | 15:57:00.384 | Recommends a small correction “without another review”. |
| 889 | 16:04:39.868 | User: “make the small edit”. |
| 906-934 | 16:05:13.461-16:05:39.849 | Fifteen actual targeted Edit calls create version 4. |
| 943/944 | 16:05:46.068 onward | Structural gate passes: seven phases, fifteen tasks, acceptance criteria present, no prohibited formatting. |
| 946 | 16:05:53.370 | Explicit final disclosure: “NOT CHECKED: v4 has had no review since this edit.” Recommends implementation. |

Elapsed invocation-to-result time was approximately 37 minutes 35 seconds for the first full review and 36 minutes 30 seconds for the second. The targeted reviewer returned about 85 seconds after dispatch. These are observed wall-clock intervals, not token costs or summed agent runtime.

### Count corrections

The second report says “13 of the 16” findings fixed, three partial. Its detailed `prior_fix_check` instead marks:

- **Fourteen fixed:** first findings 1-3, 5-8, 10-16.
- **Two partial:** toolchain/diagnosis testing and PR-body rendering/old values.

The second report’s own fixed list omits the repository-self-check finding even though the detailed merged artifact marks it fixed. Do not repeat “13 fixed, 3 partial” as a verified result.

Likewise, twenty numbered second-round items are not twenty independent defects:

- The sufficiency item repeats the validation-order and missing-state problems.
- The concurrency item explicitly says it is “a note, not a defect”.

**Key takeaways**

- The user authorized each plan amendment and the reduction in review scope.
- Final termination was not a clean independent review result.
- Structural gate success was reported separately from the absence of a final semantic review.

## 3. Findings that demonstrably arose from earlier corrections

These are **plan-level** introduced defects or contradictions. No runtime regression is claimed.

### 3.1 Moving the four-asset requirement into early detection

**Original criterion.** Source:316 defines “release exists” as a published, non-draft release listing the Debian package. Source:245 separately makes the pin-writing script refuse a release missing any of four assets.

**First finding and proposal.** First merged findings:22-30 says rollback validation is missing from detection and recommends using the pin writer’s four-asset rule, or explicitly accepting late failure. Its invariant probe also advocates harmonizing the predicates.

**Actual v2 edit.** JSONL:544 inserts a constraint calling this a case “the source leaves open”. Plan v2:171 and :186-187 require all four assets during pin/rollback detection.

**Next finding.** Second merged findings:75-83 identifies that this changes specified behavior. A package release with `LICENSE.orca` rather than `LICENSE` now fails in detection, instead of reaching the pin-writing job and failing there by release name.

**Classification:** Introduced behavioral divergence in the plan, directly caused by an earlier recommendation. The “pin equals current means no operation” part of the same item was subsequently withdrawn as a contradiction because Source:136 permits that decision.

**Actual v3 correction.** JSONL:841 restores Debian-package-only detection and keeps the four-asset refusal in the pin writer. Current Plan:29, :180, :196 describe the distinction explicitly.

**Why the first review missed it:** The first review did not merely miss this later divergence; it proposed the stronger early predicate. Its objective was eliminating late refusal, but it did not preserve the specification’s distinction between release existence and pin-writer eligibility.

### 3.2 Choosing a different source for the old lockfile digest

**Original criterion.** Requirements:302 names the recipe’s lockfile digest as the old value for PR field 9.

**First finding and proposal.** First merged findings:85-93 correctly notices that old values must be captured before the pin writer rewrites files. It offers capture from main “or from P provenance”.

**Actual v2 edit.** JSONL:544, historical Plan v2:209, explicitly captures the old lock digest from the currently deployed package’s provenance, without declaring a change to the field’s contract.

**Next finding.** Second merged findings:57-65 identifies the changed source and also finds that old commit, patch hash, package digest, patch digests, and Electron version still lack complete declared sources.

**Classification:** Mixed. The explicit field-9 source substitution is introduced by the correction. The other unspecified old values are an incomplete correction of the original old-value problem.

**Actual v3 correction.** JSONL:841; current Plan:220 takes field 9 from the recipe on main and enumerates the other old values from the deployed release’s provenance.

**Why the first review missed it:** It allowed two alternative sources without resolving that the governing field table chose one. The first probe already understood that rollback separates the deployed recipe and deployed package; the resulting recommendation still left the source choice open.

### 3.3 Requiring an inventory test before registering the new workflow

**Original criterion.** Source:281 requires the new workflow to be registered in the automation inventory. The actual test, Workflow inventory test:599-628, compares the real workflow-file set against registered/excluded entries and fails on any unlisted file.

**First finding and proposal.** First merged findings:103-111 adds local reader tests, including this inventory test, to the workflow-test task.

**Actual v2 edit.** JSONL:544 adds “same result as on the base commit” for test-50 to Task 13. Route registration remains Task 14.

**Next finding.** Second merged findings:120-128 identifies an unsatisfiable intermediate acceptance criterion: the new workflow already exists, but the entry needed for the test is scheduled later.

**Classification:** Introduced acceptance-order defect.

**Actual v3 correction.** JSONL:841 moves registration to Task 13 and workflow checks to Task 14. Current Plan:234-260 preserves that order.

**Why the first review missed it:** It recommended a broader regression check without tracing when that check’s required new inventory entry would exist. The relevant test was already being cited in the original route task, so this was a dependency interaction created by the recommendation.

### 3.4 Creating a renderer test boundary that excluded what the tests needed

**Original criterion.** Source:345-359 separates collectors, sanitization, object construction, rendering, and the oversized-body fallback.

**First finding and proposal.** First merged findings:85-93 asks for an extracted renderer region and fixture tests for caps, fallbacks, unavailable fields, and rollback text.

**Actual v2 edit.** JSONL:544 creates an extracted renderer that reads only a JSON object, with collectors outside it, while requiring extracted-region tests for caps and release filtering without assigning where those operations live.

**Next finding.** Second merged findings:66-74 says the tests could be vacuous or impossible if caps/filtering happen in collectors outside the tested region.

**Classification:** Newly introduced ambiguity in the correction, plus an unresolved original integration-testing gap. Testing the sanitizer alone still does not prove collectors invoke it.

**Actual v3 correction.** JSONL:841 explicitly assigns sanitization to collectors and caps, field-17 filtering, rollback text, title, and oversized-body handling to the renderer. Current Plan:224-225 and :251-259 encode those boundaries.

**Why the first review missed it:** Its proposed extraction solved “no renderer test” without defining the boundary between the extractor’s input and the operations it was supposed to test.

### 3.5 Naming a fetch remote without establishing that remote

**Original criterion.** The patch-check task must fetch upstream source and the recipe base commit.

**Original plan.** Historical v1:191 says “shallow fetch of T and the base commit”, without a remote name.

**Actual v2 edit.** JSONL:544, historical v2:208, adds `git fetch ... origin ...` while spelling out the missing diagnosis procedure.

**Next finding.** Second merged findings:201-209 notes that no scratch repository or upstream remote has been established. In the repository checkout, `origin` is not the intended upstream source.

**Classification:** Introduced concrete plan instruction error, refining a pre-existing underspecification.

**Actual v3 correction.** JSONL:841; current Plan:218 requires a scratch repository and explicitly adds the upstream repository before fetching.

**Why the first review missed it:** It was introduced while expanding the procedure requested by the first review. The earlier text had not named the wrong remote.

**Key takeaways**

- Several later problems have a visible correction-to-defect chain.
- These cases concern preservation of behavior and dependency ordering, not simply missing prose.
- The first review’s proposed fixes were not themselves consistently checked against the whole specification.

## 4. Complete second-round finding trace

The table covers every numbered item in the second merged review. “v3 changed” means the logged whole-file write contains the specified correction, not that a later full review proved it complete.

| Later item, plain-English meaning | Classification and validity | Earlier chain, actual correction, and observed outcome |
|---|---|---|
| **Validation happens after external calls (N-01)** | Pre-existing newly discovered ordering defect, not proven introduced by v2. Valid as a plan omission. | Source:469 requires checks before arguments reach `gh`. Original v1:163 performs checks inside the network-free decision script, while v1:190 fetches before calling it. First findings 2 and 8 add more checks inside that same late stage. V2 makes the candidate derivation explicit but retains the earlier ordering. V3 adds fetch-level checks. Targeted review still finds additional unchecked tag sources; v4 expands the rule. Second merged findings:39-47. |
| **The agreed changes are insufficient (N-02)** | Duplicate/meta-finding, not another independent defect or regression. | It rests on the validation-order and missing-state findings, plus incomplete old-value and pinned-output coverage. It should not inflate the count of distinct root causes. Second merged findings:48-56. |
| **Old PR values have incomplete or conflicting sources (N-03)** | Introduced field-9 contract change plus unresolved original old-value gaps. Valid, with the qualification that provenance could be a better engineering source if explicitly approved. | First finding 9 → pre-edit capture proposal → v2 chooses provenance for field 9 and lists only three old values → later source-contract conflict and remaining missing values → v3 enumerates sources. See §3.2. |
| **Renderer/sanitizer tests can pass without checking integration (N-04)** | Newly underspecified extraction boundary plus incomplete original fix. Valid test-design issue, not proof that deployed code is unsafe. | First finding 9 → renderer extraction → v2 leaves tested-region contents unclear → v3 assigns operations and adds collector-pipe checks/mutations. See §3.4. |
| **Early four-asset check changes the specified failure path (N-05)** | Introduced specification divergence. Valid; “pin equals current is forbidden” subclaim was withdrawn. | First findings 2 and 8 → stronger early predicate → v2 blocks earlier and calls it unspecified scope → v3 restores source behavior. See §3.1. |
| **Candidate branch and pinned resolver output are not guarded by failing tests (N-06)** | Pre-existing newly discovered test gaps and output ambiguity. Not a v2 regression. | Source:160 conditionally supplies commit but passes resolver version directly; Source:183 rejects only one environment variable being set. Original v1:132 and v2:133 do not explicitly say pinned mode emits no version. Original test cases mainly cover default extraction and input rejection. V3 adds candidate-mode part (f), resolver extraction, empty-version behavior, and mutations. Current Plan:121, :137, :159, :164. Second merged findings:84-92. |
| **Dispatch flags and manual target selection are untested (N-07)** | Pre-existing newly discovered test-strength/assignment gap. Valid risk, not observed faulty dispatch. | Original v1:191 refers to the exact source command, but v1:204 only checks that dispatch is conditioned on “needs build”. The first toolchain/diagnosis fix does not execute dispatch. V3 adds an extracted dispatch region and asserts all three flags; makes manual target assignment explicit. Current Plan:217-218, :250, :259. Second merged findings:93-101. |
| **Repository failure versus outage precedence lacks a conflicting fixture (N-08)** | Unresolved old issue, with stronger fixture demand. Valid test omission. | First findings 6 and 15 add repository checks and an individual bad-digest case. V2 does not combine a bad repository and failed metadata fetch. V3 adds that combined case, non-latest fetch error distinction, and an ordering mutation. Current Plan:198 and :205. Does not resolve the separate “no upstream call before self-check” contradiction. Second merged findings:102-110. |
| **Release-pruning credentials and environment wiring are not asserted (N-09)** | Pre-existing newly discovered test gap. | Source:167 defines distinct release and PR tokens and the fresh-main checkout. Original plan delegates the environment to the source but its shape checks do not assert those mappings. V3 enumerates them and adds mutations. Current Plan:140, :157, :164. Second merged findings:111-119. |
| **Inventory test scheduled before route registration (N-10)** | Introduced acceptance-order defect. Valid and directly supported by actual test code. | First finding 11 → add reader tests → v2 puts test-50 in Task 13 with route registration still Task 14 → v3 reorders them. See §3.3. |
| **Manual upstream-tag runs lack release metadata and rejection fixtures (N-11)** | Pre-existing newly discovered interface/test gap. | Source:312 requires shape, non-prerelease, non-draft status. Original v1:163 reads latest-release metadata in forward mode but gives no explicit manual-tag metadata fetch; v1:175 lacks these rejection cases. V3 introduces the target metadata-file distinction and the missing cases. Current Plan:177, :195, :217, :248. Second merged findings:129-137. |
| **Current pin can stop the weekly patch check (N-12)** | Pre-existing omission aggravated by inconsistent source instructions. Valid missing reconciliation, not proof v2 would certainly skip the job. | Source:382 sends current candidate to “Noop”; Source:142 and :402 require a nonempty “up to date” state and patch-check execution. Both v1:163/:175 and v2:170/:185 say only “noop”. V3 introduces the state and mutations, but the targeted review finds the planned text mutation ill-defined. V4 uses the exact generic condition. Second merged findings:138-146; targeted verdict:11-21. |
| **Workflow-shape assertion mechanism is unspecified (N-13)** | Changed review precision/test scope, not demonstrated functional regression. Valid executability clarification. | The source itself calls for text checks; original plan repeats them. During review, a proposed YAML-parsed assertion conflicts with the existing text-level convention and undeclared dependency. The merged item rejects that proposal and asks for a named mechanism. V3 chooses the existing regular-expression job slicing and adds per-guard mutation requirements. Current Plan:24. Second merged findings:147-155 and :241. |
| **Toolchain and diagnosis logic are not executed by tests (N-14)** | Unresolved old finding, not new. | First finding 4 demands a procedure and fixtures. V2 adds procedure and rendering-from-diagnosis fixtures, not execution of the probe/parser. V3 explicitly accepts owner-run live acceptance as the only coverage. Current Plan:218 and :268. This is a declared test-coverage limit, not an automated fix. Second merged findings:156-164. |
| **Rollback compare direction is not asserted (N-15)** | Incomplete new renderer-test fix; stronger test specificity, not a newly wrong link. | Source:361 supplies direction. V1 delegates rollback rendering to the source. V2’s new renderer fixture checks heading/sentence but not the link. V3 adds the exact link and reversal mutation. Current Plan:225, :253, :259. Second merged findings:165-173. |
| **Concurrency key verification remains limited (N-16)** | Explicit non-defect note after calibration. Do not count as a fresh bug. | First finding 16 requests external support verification. V2 records documented support and pairing with non-cancellation. The second merge says this satisfies the first concern and withdraws the suggestion to remove the key. V3 clarifies the oracle and old-linter caveat. Second merged findings:174-182 and :235-237. I did not independently research current GitHub syntax. |
| **No recorded baseline for “same result as base” (N-17)** | Introduced acceptance-executability gap associated with the new reader checks; a known local-failure comparison also existed in v2 constraints. | First finding 11 → v2 adds baseline comparisons without a capture task → v3 captures named test outcomes before editing. Current Plan:27, :35, :47, :150, :260. Second merged findings:183-191. |
| **Logs could be accidentally staged (N-18)** | Pre-existing advisory hygiene risk, not behavioral defect. | Original v1 already writes acceptance logs under an untracked artifacts path. V3 clarifies the package-relative directory and “never stage”. The citation validator rejects a proposed claim that the package lies outside the worktree. Current Plan:28. Second merged findings:192-200; second citation validation:14. |
| **Patch fetch names an unestablished/wrong remote (N-19)** | Introduced concrete instruction error atop earlier missing detail. | First finding 4 → v2 adds explicit `origin` fetch → later reviewer requires scratch/upstream setup → v3 supplies it. See §3.5. |
| **PR head must be defined by mode before rechecking (N-20)** | Incomplete old fix plus source inconsistency, not wholly new. | First finding 3 fixes the open-only rollback exception. V2 adds it but retains a branch placeholder and broad “same candidate” wording. Source:115 says “all modes”, whereas Source:454 gives rollback its own head rule. V3 names the per-mode head and adds a case that a merged forward PR does not block rollback. The validator narrows the finding because closed/merged rollback handling was already present. Current Plan:197 and :222; second citation validation:15. |

### Why the original review did not catch these particular issues

Verified evidence supports four case-specific explanations.

1. **Coverage was credited without proving the state needed by downstream wiring.**  
   First coverage matrix:1749-1757 quotes the requirement that the patch check run for the “up to date” state. It initially matches Task 10 by containment at ratio `0.714`, then assigns semantic coverage to Tasks 12 and 13. Neither original task actually names that state. The missing-state defect was therefore present in a requirement that the matrix treated as covered.

2. **The first matrix omitted some security/order clauses entirely.**  
   The second merged findings:223-227 explicitly records the before-use security clause and before-upstream-call clause among missed spans. The original matrix contains tag-validation rows but not the complete temporal constraint. A check existing somewhere was not the same as checking before the fetch that used it.

3. **The specification’s test table itself left holes.**  
   Source:479 lists “noop for current candidate” rather than asserting the named state. It omits the individual patch-digest mismatch that the behavior section requires at Source:400. The first QA reviewer’s self-audit says they checked every listed test-table case. Matching that list did not establish that every behavioral requirement had an effective test.

4. **Some later defects did not exist until the correction was written.**  
   The inventory-test ordering, explicit old-lock source substitution, renderer boundary, and explicit remote instruction have before/after evidence. No explanation of an initial “miss” is needed for text introduced later.

For the remaining newly noticed test-strength issues, the exact reason the first reviewers overlooked them is **unknown**. The record supports omissions and differing focus, not a proven cognitive cause such as context exhaustion.

**Key takeaways**

- Validation existence, validation timing, and validation coverage were repeatedly conflated.
- The original coverage matrix visibly over-credited at least one later blocking requirement.
- Copying the source’s test inventory preserved omissions and contradictions already present in that source.

## 5. What the targeted third review added

The full return is preserved at Session:874. The shorter on-disk targeted verdict omits some per-site detail, so the JSONL notification is necessary for the complete evidence.

| Targeted observation | Historical classification | Actual v4 response |
|---|---|---|
| PR collectors still use intermediate upstream release tags without the required filter. | Pre-existing omission, newly discovered by tracing all tag sources. V3 fixed the primary target paths, not this secondary source. Requirements:297 and Source:346 already require filtering. | Edit at Session:926 adds filtering before calls/links; :932 adds structural checking; :934 adds a filter-removal mutation. Current Plan:224, :251, :259. |
| The bad-value error prints untrusted text inside a workflow command. | Introduced explicit unsafe instruction in v3:217, which says the error names the bad value. This is a plan-level injection risk, not an observed exploit. | Session:908 and :922 change errors to name only the failed input; :928 and :934 add output/mutation checks. Current Plan:23, :217, :248, :259. |
| Annotated tags are followed through an upstream-controlled URL without checking it first. | Pre-existing, inherited from Source:158, which explicitly instructs following `object.url`. This is tension with Source:469, not a v3 regression. | Session:912 requires a 40-hex object digest and a fixed tag-object endpoint instead of the raw URL. Current Plan:137. No separate final independent verification observed. |
| No fetch-level malformed rollback input case. | Incomplete validation-before-use correction. A decision-script test after fetching is not a fetch-level guard test. | Session:928 adds the missing case. Current Plan:248. |
| No mutation for the candidate-version check. | Incomplete v3 testing promise. The new global “one mutation per guard” rule makes this more conspicuous, but missing mutation does not prove the existing bad-input test ineffective. | Session:934 adds ordering mutation. Current Plan:259. |
| No mutation removing the build resolver’s tag check. | Incomplete v3 testing promise; the existing malformed-tag fixture already requires an empty call log. | Session:914 adds the mutation. Current Plan:164. |
| Downstream jobs rely on successful detection without saying so explicitly. | Documentation clarification, not established faulty wiring: `needs: detect` already exists. | Session:908 makes the dependency explicit. Current Plan:23. |
| Planned mutation “remove up_to_date from the condition” has no meaning when the source condition is simply nonempty state. | Introduced v3 acceptance-instruction defect. Source:129 names a generic condition, not a state list. | Session:924 and :930 require the exact source condition; :934 changes mutation to narrowing execution to “needs build”. Current Plan:218, :251, :259. |
| Pin/rollback no-operation cases have an unspecified state value. | Incomplete missing-state correction, with a source scope tension. | Session:910 and :916-920 make those modes emit the “up to date” state and empty target. Current Plan:29, :180, :196-197. |
| No test or named live check evaluates the up-to-date week through the positive control. | Unresolved verification limit. | V4 retains text-level guard checks and a general statement that live checks cover expression evaluation. It does not add the exact runtime scenario requested by the targeted reviewer. |
| Fetches still precede the repository self-check despite the “before any upstream call” rule. | Pre-existing specification contradiction, unresolved. | V4 preserves a decision-stage check before reading fetched files, but fetch still precedes that decision. Current Plan:178 versus :217. |

### Narrowing overstatements in the targeted return

The detailed reviewer also marks some deterministic derivations and downstream uses as not independently tested. Those observations do **not** establish separate functional defects:

- A value derived from an already checked version is not automatically an unchecked-input defect.
- An absent extra mutation is not proof that an existing malformed-input fixture cannot catch removal of the guard.
- The handoff uses a version produced by the build path; the return does not demonstrate that an arbitrary untrusted value can reach that point.
- Existing job dependency syntax is evidence of dependency wiring even when an explanatory sentence is absent.

These should be retained as test/documentation limitations unless a concrete invalid path is shown, rather than counted as newly introduced bugs.

**Key takeaways**

- The targeted reviewer found two genuinely new correction defects: unsafe bad-value wording and an ill-defined condition mutation.
- It also found pre-existing paths outside the primary validation fix.
- The final edit improved the plan but did not close every verification limit or reconcile the self-check ordering contradiction.

## 6. Why the loop continued, and why it stopped

### Verified continuation mechanisms

**Different review passes were answering different questions.** Initial gaps concerned coverage and assignment. Corrections then introduced more precise collectors, extraction regions, acceptance checks, and order constraints. Later reviewers could inspect those newly concrete interfaces and find defects that were previously underspecified rather than concretely wrong.

**Local fixes crossed component boundaries.** Early release validation changed which job failed and what recovery applied. Capturing old values crossed the deployed-package/recipe boundary. Adding a reader test crossed workflow creation and inventory registration. These are specific dependencies visible in the artifacts.

**The source was not a consistent single acceptance contract.** Examples:

- Source:382 says current candidate goes to “Noop”; Source:142/:402 requires a named state that still runs patch checks.
- Source:285 makes the decision script consume pre-fetched files; Source:402 says the repository self-check precedes any upstream call.
- Source:158 says follow the annotated tag URL; Source:469 requires upstream values to be checked before use.
- Requirements:302 defines field 9 from recipe state even though rollback can separate recipe and deployed-package state.

**Stronger tests accumulated across rounds.** Several later findings asked for mutation checks or execution scenarios absent from Source:477-479. Some were useful corrections; they were not all evidence of lost original requirements.

### Verified stopping mechanism

At Session:821 and :856, the orchestrator argued for reviewing only the two blocking fixes, citing the repeated cost and increasingly detailed test-strength findings. The user explicitly accepted that narrowed review at :858.

After both targeted results were still partial, Session:885 recommended a small edit “without another review”, relying on future per-task implementation review. The user authorized the edit at :889.

Session:946 then disclosed:

> “NOT CHECKED: v4 has had no review since this edit.”

The loop therefore stopped by **authorized reduction of review scope and deferral of enforcement to implementation**, not by observed convergence to a clean independent pre-review.

**Key takeaways**

- Cost and review-scope decisions are explicit in the record.
- There is no basis to describe final v4 as independently approved.
- The structural gate could pass all four versions because the contested problems were primarily semantic and cross-task.

## 7. Evidence integrity and hashes

Historical plan versions were reconstructed in memory from actual `Write` and `Edit` payloads, without writing extracted files. The first two reconstructed hashes match the review snapshots, and the final reconstructed hash matches the live plan.

| Source | SHA-256 |
|---|---|
| Selected JSONL | `bff72993f9c75b6c1565326ed3298964b99bf5ae0ddcae20a38a12d4e5e12a89` |
| Driving source | `32211523717c4740cbd82123b69d960b9e9e5b61ee99c7e1b42b675432e83b2b` |
| Companion requirements | `08f9c06e87c614d4980e4b1227876c06d34d268ef16bab0f1fa86f717f466e60` |
| Reviewed plan v1 | `ebc03d4586a29b7436632bd40008a731f94f33a021f242fc7cb98068bd685ab5` |
| Plan v2, Session:544 | `d3a12ef9e187e8edbfa584926c81be75a5bb6792a3013de237bf19cb0d5e8940` |
| Plan v3, Session:841 | `cbfb606a9d9669c66aaa01c7df1ff6a480a11374ecdf9ffda386e39b34af78f8` |
| Final/live plan v4 | `94af0cdac984ba7661ab1919d38ee670a87ab9f3c18b88dcf240f2b807b9e18b` |
| First report | `ff7ba8697a03e296a255a45a21375373624e71137a9a32de0226dc6f1689b423` |
| Second report | `52a2e253e0158658724a79c17335cd85c21db052a01d7c0a3b2cd6609d4550c8` |
| Persisted targeted verdict | `a675acc8f66dcf7831538717ae35e55caa865a6db99aa0b085fb9974a12e4fd0` |

**Key Takeaways**

- First and second `input-snapshot.yaml` files contain the same source hash. Thus changing specification content is not an explanation for the additional findings between those two runs.

## Gaps and Questions

- No runtime implementation regression is established by this planning session. The findings concern instructions, acceptance design, and specification fidelity.
- Later implementation artifacts now exist under the task package. Their presence does not prove this planning session executed anything.
- The second report’s closure count is internally inconsistent; the detailed checklist supports fourteen fixed and two partial.
- The final plan was not independently reviewed after the fifteen edits.
- The repository-self-check-before-fetch contradiction remained unresolved.
- The precise runtime test for an up-to-date week reaching the positive control remained absent.
- The exact reason a reviewer overlooked each otherwise pre-existing test gap cannot be recovered. I have not substituted speculation for that missing evidence.
- I did not independently verify present-day GitHub concurrency documentation; the historical review resolved that issue and explicitly treated the remaining item as a note.
- No task execution, production code edits, tests, commits, or report-file writes were performed for this investigation.

## Stale Documentation Found

No current-architecture staleness claim is established by this investigation. The relevant issues are **internally conflicting design instructions**, an inaccurate review closure count, and a condensed targeted verdict that omits details retained in the JSONL return.


<!-- phase3-correction: orca-plan-original-repair-ledger -->
## Complete original-repair accounting supplement

Historical v2 anchors below refer to the logged whole-file Write, not current plan lines.

## Evidence keys

- **Session:** `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl`
- **Original findings:** `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-20261022133138/REPORT.md`
- **Next-review checklist:** `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml`
- **Plan:** `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/TASK-WF-designSpec-20261022-132541.md`

**Key Takeaways**

- **Historical line convention:** Every “v2:N” anchor below means line N of the complete plan content in **Session:544**, the actual whole-file Write at `2026-10-22T15:08:38.839Z`. **Session:545**, at `15:08:38.938Z`, confirms that write succeeded. These are historical plan lines, not current-file line numbers.

## A. All sixteen first-round repairs

| Original finding | Original shortfall and suggested fix | Actual logged v2 amendment | Next review’s result and qualification |
|---|---|---|---|
| **Rollback choices lack asset filtering (M-01)** | Original findings:31 says PR field 17 could advertise releases missing required assets. Add four-asset filtering and a missing-`LICENSE` fixture. | Session:544, **v2:209** adds the field-17 four-asset filter; **:223** adds the missing-`LICENSE` renderer fixture; **:229** requires removing the filter to make that test fail. | **Fixed**, next-review checklist:22. Qualified there by the renderer-region placement ambiguity, later finding N-04. The filtering requirement was added successfully even though its testing boundary still needed correction. |
| **Rollback input validation happens too late (M-02)** | Original findings:32 says detection/decision lacks rollback format and release-existence checks. Add early checks and malformed/missing-release cases, using the same four-asset rule as the pin writer. | Session:544, **v2:171** adds the rollback format, current-version no-operation, and four-asset release checks; **:187** adds malformed, missing-release, missing-`LICENSE`, and rollback PR-state cases. | **Fixed**, next-review checklist:23. However, following the suggested four-asset rule introduced the early-failure specification divergence later identified as N-05. Validation inside the decision script also did not solve validation-before-fetch ordering. |
| **Closed rollback PR incorrectly prevents another rollback (M-03)** | Original findings:33 says the re-check loses the exception that rollback PRs count only while open. Add the exception and a check. | Session:544, **v2:209** explicitly says a closed or merged rollback PR does not count; **:171/:187** carry the open-only rollback rule and cases; **:221** adds the corresponding workflow text check. | **Fixed**, next-review checklist:24. Qualified by later N-20: the queried branch still needed definition by mode. This does not negate the successful closed/merged exception amendment. |
| **Toolchain probe and patch diagnosis lack procedure/tests (M-04)** | Original findings:34 asks for the companion requirements’ comparison and diagnosis procedures, plus fixtures. | Session:544, **v2:208** spells out toolchain comparisons, cumulative application, pristine-target checks, three-way/reject diagnostics, and conflict counting. **:191** adds diagnosis-rendering cases naming both toolchain edit sites and patch-status details. | **Partial**, next-review checklist:25. Procedure and rendering checks were added, but tests still did not execute the actual probe/diagnosis logic. Later N-07 addresses dispatch testing; N-14 retains the probe/parser coverage gap. |
| **Nobody computes the patch digest/candidate identifier (M-05)** | Original findings:35 says the decision script takes the shortened patch digest as input but no task computes it. Assign computation and verify the known tree’s value. | Session:544, **v2:207** assigns the ordered four-patch SHA-256 computation, first twelve hex characters, and forward candidate derivation. **:221** adds the extracted-fetch check for `6b8a326a74bb`. | **Fixed**, next-review checklist:26. This is a successful non-recurring repair. Later validation-order concerns about using the derived candidate do not mean its computation remained missing. |
| **Individual patch-digest mismatch has no fixture (M-06)** | Original findings:36 says repository validation implements individual patch checks but the test list omits that failure. Add the fixture. | Session:544, **v2:188** adds “one changed patch sha” with no latest-release input read, alongside the other repository-failure cases. | **Fixed**, next-review checklist:27. Later N-08 asks for the stronger combined case of bad repository state plus failed upstream metadata. The individual mismatch fixture itself was added. |
| **Runner and timeout requirements cover only detection (M-07)** | Original findings:37 asks to apply the small runner and fifteen-minute timeout to every monitor job and assert them. | Session:544, **v2:206** says “Every job” has the required runner and timeout. **:221** adds checks that every job lists them. | **Fixed**, next-review checklist:28. Successful non-recurring repair; no later finding establishes that these requirements disappeared or remained unassigned. |
| **Pin input validation and target derivation are missing (M-08)** | Original findings:38 asks for early candidate-version format checks, explicit upstream-target derivation, and input cases; it also identifies absent release/current-version handling. | Session:544, **v2:171** defines the full version regex, candidate from input, upstream target derivation, current-version no-operation, release checks, and per-mode PR handling. **:186** adds malformed pin, current pin, and missing-`LICENSE` cases. | **Fixed**, next-review checklist:29. Qualified by N-01’s fetch-before-check issue and N-05’s stricter-than-source release predicate. The requested decision-stage validation and derivation were present. |
| **PR renderer is untested and reads old values after rewriting (M-09)** | Original findings:39 asks for a marked renderer, fixture tests, and capture of old values before the pin writer edits files. | Session:544, **v2:209** moves named old-value capture before pinning and adds the renderer markers. **:223** adds unavailable-data, caps, oversized-body, rollback-text, asset-filter, and differing-version fixtures. | **Partial**, next-review checklist:30. Remaining problems were the renderer boundary and the chosen old lockfile source, later N-04 and N-03. See the main report’s detailed chains. |
| **Companion specification is not named (M-10)** | Original findings:40 says pin locations and the eighteen PR fields live in a companion document the plan never names. Identify the file and sections in the source and relevant tasks. | Session:544, **v2:14** names the companion path and sections; **:100** explicitly directs the pin-writer task to its pin-location table; **:203** directs the workflow task to its PR-field contract. | **Fixed**, next-review checklist:31. Successful non-recurring repair of discoverability. Later disputes over particular field definitions do not mean the companion source remained unnamed. |
| **Other tests reading the contract workflow are not run (M-11)** | Original findings:41 asks for additional local reader tests. The detailed first-round merged recommendation specifically names test-50, test-51, test-53, and test-54. | Session:544, **v2:146** adds those four readers to Task 8; **:230** adds them to Task 13, each compared with the base result. | **Fixed**, next-review checklist:32, **with qualifications**: no captured baseline yet, and test-50 is scheduled before the new route registration. These become N-17 and N-10. A later advisory also expands the reader list. The top-level first report’s broader test list should not be mistaken for the narrower detailed merged recommendation actually applied. |
| **No explicit stop between the two PRs (M-12)** | Original findings:42 asks for a stop after PR 1 and a fresh branch from updated main only after the owner merges it. | Session:544, **v2:20** strengthens the global delivery rule; **:158** says “STOP here” and wait for merge; **:166** requires confirmation of merged state and a new branch from updated main before Task 10. | **Fixed**, next-review checklist:33. Successful non-recurring repair. It is more than a dependency-line edit: it creates an explicit executor stopping instruction. |
| **Workflow tasks omit their test-creation dependency (M-13)** | Original findings:43 asks Tasks 8 and 9 to depend on Task 7, which creates the test they wire/assert. | Session:544, **v2:128** changes Task 8 dependencies to Tasks 1, 4, and 7; **:150** changes Task 9 dependencies to Tasks 5, 7, and 8. | **Fixed**, next-review checklist:34. Successful dependency repair. Separate warning that the executor follows source order does not invalidate corrected dependency metadata. |
| **Original versus changed line references are unclear (M-14)** | Original findings:44 asks Task 1 to identify its line references as pre-edit. | Session:544, **v2:34** states: “All line numbers below are pre-edit (today’s file); edit from the bottom up or re-locate by content.” | **Fixed**, next-review checklist:35. Successful non-recurring clarity repair, not evidence of a code defect. |
| **Repository self-check coverage in pin/rollback modes is unspecified (M-15)** | Original findings:45 narrows this to mode coverage: run repository checks in every mode and add pin/rollback cases. | Session:544, **v2:169** requires the repository self-check first in every mode before reading fetched upstream files; **:188** adds repository-check failures in pin and rollback modes. | **Fixed**, next-review checklist:36. This is the item omitted from the second report’s fixed-item summary, producing its bad count. The distinct requirement that no upstream call occur before checking the repository remains contradictory in the source and unresolved by this amendment. |
| **Concurrency syntax lacks demonstrated support (M-16)** | Original findings:46 asks to verify the concurrency key before relying on it. | Session:544, **v2:136** records the historical documentation finding and explicitly pairs queueing with non-cancellation; **:143** requires that pairing in concurrency blocks. The monitor acceptance also checks the pairing at **:214**. | **Fixed**, next-review checklist:37. Calibration expressly corrects an earlier “partial” assessment. Later N-16 is retained as a minor tooling note, explicitly not a defect. I have not independently verified current GitHub documentation. |

### Closure count supported by the detailed evidence

The next-review checklist marks **fourteen fixed and two partial**. The two partial repairs are the toolchain/diagnosis coverage and PR-renderer/old-value findings (M-04 and M-09). The second report’s “thirteen fixed, three partial” summary is not supported by its own detailed checklist.

**Key Takeaways**

- “Fixed” here means **the next reviewer accepted that original finding’s plan amendment**, not that runtime behavior was tested or every interaction introduced by the amendment was correct.

## B. Correction to the initial cleanup timeline

The original report’s timeline entry grouping Session:150 and :163 as cleanup must be qualified as follows.

| JSONL line | Timestamp, UTC | Verified event |
|---|---|---|
| **150** | `2026-10-22T13:31:11.613Z` | Attempted Edit replaces the “placeholder-free section boundary” wording. **This attempt did not apply.** |
| **151** | `2026-10-22T13:31:11.880Z` | Freshness hook blocks the Edit: “You have not Read [the plan] in this session.” It instructs a Read and retry. |
| **163** | `2026-10-22T13:31:22.708Z` | Retried Edit replaces that single wording line. |
| **164** | `2026-10-22T13:31:22.803Z` | Tool confirms the plan “has been updated successfully.” |

**Key Takeaways**

- The reviewed v1 contains the successful retry’s wording. The blocked attempt must not be counted as a successful mutation.

## Summary

The repeated planning reviews were driven by a real mixture of incomplete fixes, new defects introduced by fix proposals, pre-existing omissions, and inconsistent source instructions. Several correction-induced failures have direct before/after proof, especially early release eligibility, old-value sourcing, inventory-test ordering, renderer extraction, and remote setup. Other later findings strengthened tests rather than identifying newly wrong behavior, and the twenty-item count includes a duplicate sufficiency finding and an explicit non-defect note. The final version passed structural checks but was not independently re-reviewed; the user authorized that stopping point after a targeted review still returned partial results.

**Recommended action:** Persist this evidence under the assigned research path and classify this incident as **mixed-cause review churn with an explicitly unreviewed final amendment**, not “twenty regressions caused by sixteen fixes”.

## Resume traceability supplement (2026-10-23)

**Key Takeaways**

- A bounded metadata-only extraction from the exact original Session path above verified all six requested primary transition identifiers, with input/output count six and non-null timestamp/UUID guards. This completes identifier presentation without redoing or changing the historical analysis, finding classifications or source corrections.

| Physical JSONL line | Original timestamp (UTC) | Original message UUID |
|---:|---|---|
| 499 | 2026-10-22T14:09:01.093Z | 5a85c9dd-6036-4e83-9090-eb47eb714e87 |
| 544 | 2026-10-22T15:08:38.839Z | 1ba7509f-fbb1-401f-bba7-c20d545ef750 |
| 821 | 2026-10-22T15:45:18.570Z | 4cd51382-4df1-438d-b1ca-0ed88726c2e2 |
| 841 | 2026-10-22T15:53:15.796Z | 91fa90dd-de48-4891-b7a2-b16222c653f1 |
| 874 | 2026-10-22T15:56:35.717Z | caa3960d-ce1a-4be9-94fa-ee6d9dac8820 |
| 946 | 2026-10-22T16:05:53.370Z | 176a2869-58dd-4804-9d6a-e345d82afae6 |

**Key Takeaways**

- The six transition identifiers retain their original JSONL record numbers, timestamps and UUIDs.
