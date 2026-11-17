### Variant B Rebuttal (Round 2)

Slot C-10 (pr-review-wire-format-and-slot), Round 2, standard depth; focus correctness, risk, test-coverage. Code state: HEAD 50d4d2b9d, branch ironbelly/shadow-runs. Nothing was run: no pytest, no script, no model call. Tags: [CODE-VERIFIED] = I read that file and line myself in this Round 2 session; [RELIED] = taken from A's Round 2, diff-analysis or my Round 1 and not re-read now; [UNVERIFIED] = not settled by reading. Paths are relative to the repository root. This file cites nothing from the run-1 task folder or the run-1 queued file. "C10-R" is A's Round 2 resolution; "C10-R-B" is C10-R plus the amendments named in section 6.

## 1. Responses to A's section 2, "What B still gets wrong", items 1 to 5

### 1.1 Zero-token rule on `severity_router.py` and the home of the converter

The fact is right. `CORE_PURE_FILES` lists `severity_router.py` (`tests/pr_submit/test_static_grep.py:37-55`, entry at `:48`). `test_tn50_core_pure_no_gh_git_tokens` applies `\bgh\b|\bgit\b` to every line of every listed file with no comment or docstring exemption (`:136-147`). [CODE-VERIFIED] A function added to the router must keep those two words out of its code and its docstrings.

The argument does not separate the two homes, for two reasons.
1. A's own condition 2 puts a T-N50-style check on the new module. Then the hunk parser has the same vocabulary limit in the new module. The only way the new module escapes the rule is to stay uncovered, and A rejects that. A parser needs no such word anyway: it reads `@@ -a,b +c,d @@` and `+++ b/<path>` lines, not the `diff --git` header.
2. A `finding_from_v2` docstring or body fails the suite only if it uses the words `git` or `gh`. That is a style constraint, not a placement driver. The router's own docstring already complies (`severity_router.py:10-13`). [CODE-VERIFIED]

What I concede, and on different grounds: my Round 1 said the reader "is a rename" and that T1 (parity) "fails if the reader needs any logic beyond renaming". That falsifier has fired. Under C10-R the converter does a `(reviewer_id, id)` join (X-001), a severity maximum, a severity table, a diff-range computation and per-cluster error handling. Logic of that size does not belong in the router that the FSM and the tests import (`tests/pr_submit/test_cosmos_protocol.py:51` pins `core.finding_from_comment is severity_router.finding_from_comment`). So I accept a new module. C-003 goes to A on size and import fan-in, not on purity.

One dispute: A treats "no existing test edited" as a goal. INV-E names `Finding`, `Severity`, the FSM and the fork-only checks, not test files. Appending the new module to `CORE_PURE_FILES` is one additive list entry and keeps one definition of "core-pure"; a second copy of the token scan in a new test file can drift from the first. I propose the append (AM-5). If the owner prefers zero edits to existing tests, a new test file is acceptable; the stake is low.

### 1.2 Representative is the most confident member, not the most severe

Confirmed. `_cluster` picks `rep = min(group, key=(-confidence, order))`, with a missing confidence ranked below every calibrated one (`src/superclaude/cli/review/cluster.py:338-344`). `claim` is the representative's claim and `blocking_any` is over all members (`:374-375`). [CODE-VERIFIED] I accept: severity must be taken over the joined members, not from the representative alone.

Two facts make this worse for the PR path than A states.
- `pr_submit` has no calibration step at all (Grep `calibrat` over `src/superclaude/pr_submit`: 0 matches). The only source of a per-finding confidence is a `calibration:` block in a reviewer card (`src/superclaude/cli/review/cluster_cmd.py:1-6, 28-40`), and whether the PR panel card carries one is the template's decision [UNVERIFIED]. With no calibration every member has `finding_confidence = None`, every member sorts on `order`, and the representative is the lowest `(ordinal, position)` member. In the default PR path "most confident" means "first reviewer". The claim text then comes from whichever reviewer has the lowest ordinal.
- The member dicts that `cluster_v2` returns carry no `claim` (`cluster.py:354-365`), so the claims of the non-representative members are recoverable only through the join.

Taking the severity maximum is necessary but not sufficient. See D1: it pairs a maximum severity with the representative's category and claim, which can produce a wrong outcome.

### 1.3 `original_line` is useless for panel findings

Confirmed. Producers are the bot paths only: `classifier.py:449`, `reviewers.py:295, :309`. The one consumer of the value is `dedup_groups`, and only when `line` is None (`reviewers.py:438`). The SKILL and the routing ref call it "only a verification hint" (`SKILL.md:226`; `refs/severity-routing.md:48-50`). The field itself is `models.py:192`; the validator reads it at `severity_router.py:73, :116`. A Grep of `src/superclaude` for `original_line|originalLine` finds no other reader of the value. [CODE-VERIFIED] A panel `Finding` always has an integer `line` (`is_groundable`, `fsm.py:364-372`), so `original_line` is never read. I drop it from my hybrid.

### 1.4 Harness injection versus the converter setting the keys on its own dict

Conceded. After `parse_block` the harness holds the dict in memory; writing `in_diff` and `reviewer` into it and building a `Finding` from it is the same operation as the converter building its own dict, and it additionally mutates a record the kernel handed out. If the keys were written back into a findings-v2 block and re-parsed, the unknown-key acceptance (confirmed in section 3 (a)) would be load-bearing and unpinned. The converter owning the keys removes that. The only residual difference was my T0 test, and T0 is only needed if keys are ever promoted. I withdraw "the harness injects them into the line".

### 1.5 Open items C-008 and A-006

I accept A's defaults (report-only first release; thread-less rule on promotion). A-006 is moot in the first release because panel findings never enter `verified`. C-008 is not fully closed by "report-only": see D5, where a report-only panel with blocking findings sits beside a `terminal_clean` status. That needs one mechanical wording rule, not an owner decision.

<!-- end section 1 -->

## 2. Response to each row of A's section 4 (the 11 remaining differences)

| # | Dimension | A's position | My response | Evidence and reason | My conf. |
|---|-----------|--------------|-------------|---------------------|----------|
| 1 | Where the converter lives | New pure module | ACCEPT, on different grounds | The zero-token rule does not separate the homes once the new module is covered (section 1.1). The reason is size: join, maximum, table, ranges; my "rename" premise failed. Append the module to `CORE_PURE_FILES` (AM-5). | 70 |
| 2 | What it reads | Cluster output plus records joined on `(reviewer_id, id)`; severity and category from the joined lines | ACCEPT the join; REFINE the aggregation | Path, line and `blocking_any` from the cluster are right (`cluster.py:354-367, :375`). Severity as a maximum is right. But category and claim from the representative with a cluster-wide maximum severity pairs data from different defects (D1). The cluster is built on span proximity alone (`cluster.py:161-181`). AM-1 and AM-2. | 65 |
| 3 | Who sets `in_diff` and `reviewer` | Converter, on its own output dict | ACCEPT; REFINE the missing-ranges case | Same operation as injection (section 1.4). A's "absent ranges means nothing converts" loses findings; router step 4 is already dormant for bots, and `in_diff` defaults to True (`severity_router.py:112, :178`). Degrade, do not drop (D4, AM-3). | 70 |
| 4 | Promote the four keys? | No; keep a trigger; drop `original_line` | ACCEPT | Section 1.3 and 1.4. The trigger list (M3 nonzero, second consumer, M2) is the right one. | 80 |
| 5 | `confidence` | Unset | ACCEPT | `remap_severity` drops a tier on `"low"` (`severity_router.py:173-175`); a `disputed`-derived value would lower a CRITICAL. | 85 |
| 6 | `incomplete` rule | Any requested reviewer not `complete`, as requested ids minus `complete_reviewers` | ACCEPT; REFINE | Computing from requested ids is right: a reviewer with no record is invisible to `cluster_v2` (`cluster.py:414-418`). The clause "every cluster was dropped" is vacuously true for a panel with zero clusters, so a clean panel would read `incomplete` (D3, AM-4). | 75 |
| 7 | `body` | Representative's `claim` verbatim | ACCEPT | `fix_key` hashes `path`, `line`, `body` (`models.py:196-207`). | 90 |
| 8 | Thread-less findings | One PR conversation follow-up; callbacks skip findings with no integer `comment_id` | ACCEPT as the promotion default | `fsm.py:1203-1205` passes `verified` unfiltered; precedent `refs/thread-reply.md:92-101`. Moot in the first release (nothing enters `verified`). | 70 |
| 9 | Bots silent or clean while the panel has findings | Report-only first release | ACCEPT; ADD one rule | `terminal_clean` is assigned at eight sites in `fsm.py` and is not read from the panel. A report-only panel with a blocking cluster beside `status: terminal_clean` is a misleading report (D5). The `panel` field must carry `blocking_clusters` and the summary may not say "clean" while it is above 0. | 65 |
| 10 | Severity table | CRITICAL to `critical`; MAJOR with `blocking_any` to `medium`; else `low` | ACCEPT as the PR module's default; STRIKE one claim | The table feeds the router; it does not decide the tier. Category ceilings and the `in_diff` drop lower a CRITICAL after the table (D2). "Never lowers a CRITICAL" cannot be claimed for the pipeline output. | 55 |
| 11 | Cadence | Once per head SHA; the field records the reviewed SHA | ACCEPT | Mirrors the bot gate's binding (`SKILL.md:103-112`); cost unmeasured (GQ-177). | 65 |

<!-- end section 2 -->

## 3. Verification of the code facts A reported in its section 3

Result: I confirm every one of A's checked facts. I contradict two small scope claims and add four details. All reads were done in this session.

| Item | A's claim | My result |
|------|-----------|-----------|
| (a) unknown keys | `check_finding` never iterates keys and rejects only `calibrated_confidence`; `parse_block` appends the whole object; no test pins acceptance | CONFIRMED. The only key-level rejection is `findings_v2.py:96-97`; the line's `lens` is read at `:140-145`; `parse_block` appends `obj` after `setdefault("refs", [])` (`:288-290`). The module docstring says a v1-valid line "with other keys may be rejected" (`:3-5`), so acceptance is a property of the code, not a promise. My Grep of `tests/review/test_review_findings*.py` for `unknown\|extra key\|other keys\|additional` returns no match, so no test pins acceptance in those files. Scope of that claim: those files only, not every caller of `parse_block`. |
| (b) quorum evaluator | exists, wrong shape | CONFIRMED. `QuorumState` (`src/superclaude/cli/reflect/fallback.py:75-82`) and `evaluate_quorum(workers, *, allow_single_vendor)` (`:161-179`) count `status == "success"` workers and require `reviewer_count >= 2`, `model_class_diversity == "full"` and multi-vendor or `allow_single_vendor`. Statuses are swarm statuses (`:40`). My Grep of `src/superclaude/pr_submit` for `cli.review\|cli.reflect\|findings_v2\|cluster_v2\|superclaude.cli`: 0 matches, so adopting it would add the first `pr_submit` dependency on `cli.swarm`. |
| (c) bot-gate batch drop | `try: [finding_from_comment(raw) ...] except ValueError: review_state = "polling"; findings = []` | CONFIRMED at `SKILL.md:118-124` (Augment) and `:143-149` (Codex). It is right for bots (the next poll re-reads GitHub) and wrong for a panel (no re-poll). Per-cluster `try` is the correct rule. Add: a dropped cluster must list its `cluster_id` and the reviewer-stated severity, so a dropped CRITICAL is visible by name, not only counted. |
| (d) purity list and fences | `severity_router.py` is listed; a new module needs no edit; one `python` fence pinned | CONFIRMED: list `test_static_grep.py:37-55`, scan `:136-147`, anthropic-import glob `:150-159`. Fence pins: `test_merge_guard_protocol.py:533` (`text.count("```python") == 1`), `test_codex_reviews.py:687-688` (`len(blocks) == 1`), `test_cosmos_protocol.py:35-36` (same, `exec`s the block), `test_conflict_sync_protocol.py:532-536` (`len(fences) == 1`). Addition: `test_merge_guard_protocol.py:87-90` bans a `python` fence and `src/superclaude` only in the merge-guard ref, not in other refs; I did not search `tests/` outside `tests/pr_submit` for a repo-wide ref scan [UNVERIFIED]. |
| (e) join | `(reviewer_id, id)`; unique; `cluster_v2` does not mutate | CONFIRMED. Member keys `cluster.py:356-358`; representative `:373`; duplicate `reviewer_id` skipped `:235-247`; duplicate finding id skipped `:269-276`; validity rule `:218-223` (list block, or dict with `state == "complete"`). `parse_block` also rejects duplicate ids (`findings_v2.py:101-102`). The converter must use the same validity rule or it will join to findings that `cluster_v2` ignored. |
| Found 1: categories | six core values vs 18 router values; one out-of-set category invalidates a reviewer's block | CONFIRMED. `CATEGORIES` is `contradiction, unpassable-check, data-loss, safety, missing-requirement, other` (`src/superclaude/cli/review/findings.py:15-22`); the router table has 18 other values, no overlap (`severity_router.py:34-53`). `check_finding` rejects a category outside the set (`findings_v2.py:109-110`); `parse_block` sets `invalid` on any one error (`:299-303`); `cluster_v2` then skips the whole block (`cluster.py:218-223, :256`). SCOPE CONTRADICTION: A's condition 5 asks for category, severity and lens parameters. For the PR path only the category set needs a parameter. `SEVERITIES` (CRITICAL, MAJOR, MINOR, `findings.py:14`) is reusable as is, and `lens` may be None (`findings_v2.py:88, :140-145`), in which case `annotate` takes the first citation as primary (`cluster.py:133-134`). |
| Found 2: reviewer default | `Finding.reviewer` defaults to `"augment"` | CONFIRMED at `severity_router.py:118`. |
| Found 3: FSM hands the verified list unfiltered | `fsm.py:1203-1205`; callbacks default to `_noop` | CONFIRMED (`fsm.py:1203-1205`; `RunConfig.do_reply`, `do_resolve` at `:945-946`). The fallback path computes `fallback_only` from integer `comment_id`s (`:1064-1074`). |
| Found 4: thread-less precedent | one PR conversation follow-up, no inline reply, no resolve | CONFIRMED at `refs/thread-reply.md:92-101`. |
| `SKILL.md:175-178` | panel findings would join `decision["used"]` | CONFIRMED: `decision["outcome"]` and the findings of `decision["used"]` go to the FSM (`SKILL.md:175-178`). |
| `fsm.py` `terminal_clean` | eight assignment sites | CONFIRMED by Grep: lines 241, 805, 872, 1026, 1085, 1120, 1145, 1253 (others are comments); not traced, as A says. |
| Router has no hunk handling | Grep count 0 | CONFIRMED. A Grep of `severity_router.py` for `hunk\|@@\|changed_ranges\|diff --git\|patch` hits only the substring in "dispatched" (`:58, :207`). `fsm.py` has 20 matches, all fix-hunk text per diff-analysis [RELIED]. |
| `claim` limits | at most 300 flattened characters | CONFIRMED (`findings_v2.py:111`), with a detail A does not state: `_check_flat(..., lo=None, hi=300)` has no minimum (`findings.py:79-87`), so an empty claim passes the core and then raises `ValueError` in `finding_from_comment` (`severity_router.py:69-71`). The per-cluster `try` covers it. |

<!-- end section 3 -->

## 4. New defects in C10-R

Severity here follows the repo rule: a defect is HIGH when it yields a wrong outcome an implementer would produce or loses a safety-relevant finding; MEDIUM when it is a real weakness that does not by itself produce a wrong outcome in the first release.

### D1 (HIGH): the cluster collapse mixes different defects, then C10-R pairs a maximum severity with the wrong category and claim

Mechanism, all [CODE-VERIFIED]:
- `same_defect_v2` compares only deviation class, `refs_norm` and citation spans (`cluster.py:161-181`). It never compares `category` or claim text. The span test is `c1.line_start <= c2.line_end + 3 and c2.line_start <= c1.line_end + 3` on the same path (`:170-179`, `SPAN_TOLERANCE = 3` at `:72`).
- The refs test passes when both `refs_norm` lists are empty (`:167-169`). `refs_norm` takes tokens such as `FR-12` or `P1` from `refs`, `anchor`, `anchor2` and the claim text (`src/superclaude/cli/review/findings.py:321-337`). A PR finding about code has no requirement ids, so in the normal case both lists are empty.
- Clusters are union-find components, so adjacency chains (`cluster.py:302-320`; `chained` is only a flag, `:324-326`).
- `_cluster` keeps one claim, the representative's (`:374`), and the member dicts carry no claim (`:354-365`).

Failure example. Reviewer R1 emits `F1`: category `style`, MINOR, citation `a.py` lines 40-40, claim "rename this variable". Reviewer R2 emits `F1`: category `security`, CRITICAL, citation `a.py` lines 42-42, claim "token compared with ==". No refs, no requirement tokens. Both resolve against the snapshot, `|42-40| <= 3`, refs both empty: one cluster. With no calibration the representative is R1's finding (lowest ordinal, `:338-344`). C10-R then gives severity = maximum over members = CRITICAL; category from the representative = `style`; body = "rename this variable". `remap_severity` clamps `style` to a ceiling of LOW (`severity_router.py:52, :136-143, :171`), so the Finding is Low and report-only. The CRITICAL security defect is demoted to Low, and its text is nowhere in the Finding. If instead the category is taken from the maximum member, the Finding is CRITICAL with the body "rename this variable". Either way the output is wrong. A per-line reader keeps both: `dedup_groups` groups by exact `(path, line)` and keeps every finding (`reviewers.py:430-440`), so lines 40 and 42 stay two Findings and each routes on its own category.

This is a defect of "cluster first, one Finding per cluster" itself, which I conceded in Round 1 (C-001) too quickly, and it is in my Round 1 hybrid as well. A's value-add (merge near-duplicates) is real for same-category duplicates; it is wrong for cross-category adjacency.

Amendment AM-1: one Finding per (cluster, category) pair. Group the joined members of a cluster by their own source-line category; within a group the representative rule, the severity maximum and `blocking_any` apply. A `chained` cluster (`cluster.py:324-326`) emits one Finding per member. Test: the example above as a golden fixture; expected two Findings, `style` Low and `security` Critical.

### D2 (MEDIUM): "a CRITICAL is never lowered" does not hold through the router

A's section 4 row 10 and its C-009 evidence say the adapter table "never lowers a CRITICAL". The table maps CRITICAL to the hint `critical`; `remap_severity` then applies, after it, the category ceiling (`performance` HIGH, `docs` MEDIUM, `dead-code` LOW, `naming` and `style` LOW: `severity_router.py:34-53`, clamp at `:171` and `:197`) and the `in_diff is False` drop (`:178-189`). So a reviewer's CRITICAL with category `docs` leaves the router as Medium, and a CRITICAL outside the diff in a `correctness` category leaves it at High. These are the router's rubric, shared with both bots, and I do not propose to fork them. The claim must go, and the information must not be lost: `Finding` has no slot for the reviewer's severity (`models.py:179-194`).

Amendment AM-2: the converter returns, per Finding, a small side record `{cluster_id, reviewer_severity_max, blocking_any, disputed, reviewers}` used only by the summary and the `panel` field. The summary shows the reviewer's tier beside the routed tier. No change to the router.

### D3 (MEDIUM): the clause "every cluster was dropped" is vacuously true for a panel with zero clusters

C10-R's standing rule (section 5 condition 4) makes the panel `incomplete` "when every cluster was dropped". For a complete panel that found nothing, the set of clusters is empty and "every cluster dropped" is true under `all(...)`. A clean panel would read `incomplete`, and the first release would never show a clean panel. The opposite error is as bad: a rule written as "dropped count equals cluster count" must not treat 0 = 0 as a drop.

Amendment AM-4: `incomplete` for drops only when there is at least one cluster and all were dropped. Test: three-output standing test gains a "complete, zero findings, `present`" case.

### D4 (MEDIUM): fail-closed on missing `changed_ranges` loses findings in the wrong direction

W3 and condition 2 say that with no `changed_ranges` the converter "converts nothing" and the panel is `incomplete`. Dropping a panel's CRITICAL because a diff parser failed is the unsafe direction. The router's own default is the conservative one: `Finding.in_diff` defaults to True (`severity_router.py:112`; `models.py:185`), so step 4 does not lower anything, and for both bots step 4 is already dormant because nothing produces `in_diff` (`classifier.py:443-456` per diff-analysis [RELIED]). `is_groundable` (`fsm.py:364-372`) drops findings that cannot be located; a missing diff is a different condition and the finding is located.

Amendment AM-3: with no ranges, convert with `in_diff` left unset (True), mark the panel `incomplete` with reason `ranges_missing`, and say in the summary that the diff-locality step was skipped. Test: fixture with absent ranges expects Findings present and standing `incomplete`.

### D5 (MEDIUM, INV-I sibling): a `present` panel with blocking clusters beside `terminal_clean`

C10-R keeps INV-I for `absent` and `incomplete` (no "clean" wording). It does not cover `present` with `blocking_any` clusters while the bots are clean. In the first release those findings are report-only and never reach the FSM, so `status` can be `terminal_clean` (assigned at eight sites, `fsm.py:241, :805, :872, :1026, :1085, :1120, :1145, :1253`; the enum is documented unchanged at `SKILL.md:259, :277`) while the same run's `panel` field lists a CRITICAL. A reader of the Output Contract sees `terminal_clean` and `panel: present`.

Amendment AM-4 (second half): the `panel` field carries `blocking_clusters`; the run summary must not use the word "clean" for the run while `blocking_clusters > 0` or the panel is not `present`. This is prose plus a test on the summary template; the owner decision on whether such findings may drive a push (C-008, A-005) stays open.

### D6 (LOW): the converter's invocation path is unspecified

`SKILL.md` may not take a second `python` fence (four pins, section 3 (d)); the converter has no CLI entry; `from superclaude.pr_submit import ...` would need an edit to the package `__init__.py` exports (existing Python module, contradicting "zero edits to existing modules"). A's condition 6 allows a new ref. Resolution: the pre-step ref imports by full module path (`superclaude.pr_submit.<new module>`) and keeps its own fence; add a new test that pins the ref's existence and the absence of a second fence in `SKILL.md`. Residual: `test_merge_guard_protocol.py:87-90` bans `python` fences only in the merge-guard ref; a repo-wide ref scan outside `tests/pr_submit` was not searched [UNVERIFIED].

### D7 (LOW): M2 is unmeasurable as written, and cluster scope depends on `snapshot_file_list`

- A says reviewer-stated `in_diff` is "only compared" (M2). The converter drops the key, and no key is requested from reviewers unless the C-07 template asks for an optional `in_diff`. Without that, M2 has nothing to compare. Add the optional line key to the template as an ignored, logged field, or retire M2.
- `cluster_v2` treats a citation as `resolved` only when its path is in the snapshot list (`cluster.py:115`) and only resolved citations cluster (`:170-179`). If the PR snapshot list is the diff's file list, a `role: source` citation to an unchanged file is `unresolved`, has no fingerprint (`:143-147`) and never merges with the same finding from another reviewer; it still converts, because `_citation` keeps its integer lines (`:104-116`). Condition 1 should say "the PR head's file tree", not "the PR's files" (AM-6).

<!-- end section 4 -->

## 5. What I concede and what I still dispute: my Round 1 hybrid against C10-R

Conceded (C10-R is better than my Round 1 hybrid on each):
1. Placement. A new module, not `finding_from_v2` in the router. My "thin rename" premise and the T1 falsifier failed (section 1.1).
2. Who sets the PR keys and where. The converter sets `in_diff` and `reviewer` on its own output dict; the findings-v2 record is never mutated; T0 is dropped unless keys are promoted (section 1.4).
3. `original_line` is dropped (section 1.3).
4. Severity aggregation as a maximum over joined members, not the representative's value (section 1.2).
5. `confidence` unset, the severity table owned by the PR module, `body` the representative's claim verbatim, cadence once per head SHA with the SHA in the field.
6. Defaults for the two items I left open: report-only first release (C-008) and a thread-less rule on promotion (A-006).
7. My Round 1 claim that the harness-injection path "keeps the T0 dependency" was a cost with no purchaser; withdrawn.

Still disputed, or refined, with evidence:
1. "Cluster first, one Finding per cluster" is not safe as written (D1). It is my own Round 1 hybrid's defect too. Same-category near-duplicates are where clustering helps; cross-category adjacency must not collapse.
2. The zero-token rule as the reason for a new module (section 1.1). Right module, wrong reason.
3. "Never lowers a CRITICAL" (D2). The router's ceilings and `in_diff` step lower it; the tier shown must be both.
4. Fail-closed on missing ranges (D4). Degrade, do not drop.
5. The `incomplete` drop clause is vacuous on an empty cluster set (D3).
6. INV-I is only half covered: `present` with blocking clusters beside `terminal_clean` (D5).
7. "No existing test edited" as a goal (section 1.1; AM-5). A one-line additive append keeps one purity definition.
8. FX-5 scope for the PR path is the category set only (section 3, Found 1).

Where my Round 1 position still stands and A has not answered it: nothing material. The wire-format axis (per-line reader as an alternative to an adapter) is now a question of what the converter reads, and A's join answers it. The slot axis was conceded in Round 1 and stays conceded.

<!-- end section 5 -->

## 6. The single resolution I propose: C10-R with six named amendments (C10-R-B)

I endorse C10-R as A's Round 2 section 5 states it, with amendments AM-1 to AM-6 and the conditions below. If A accepts the amendments, A and I name the same resolution. If A rejects AM-1 to AM-4, the labels in the table of section 8 stay equal but the resolution is not the same one, because C-001, C-002, C-006, S-004 and S-008 then carry different contents.

Amendments:
- AM-1 (D1, HIGH before promotion). One Finding per (cluster, category). Group joined members by the category on their own source line; apply representative, severity maximum and `blocking_any` inside each group. A `chained` cluster emits one Finding per member. Golden fixture: adjacent `style` MINOR and `security` CRITICAL findings from two reviewers give two Findings.
- AM-2 (D2). The converter returns a side record per Finding: `{cluster_id, reviewer_severity_max, blocking_any, disputed, reviewers}`. The summary shows reviewer tier and routed tier. Delete "never lowers a CRITICAL" from the table rationale; add a table test that states the expected routed tier for each of the three table outputs with and without a ceiling category.
- AM-3 (D4). Missing `changed_ranges`: convert with `in_diff` unset, standing `incomplete` with reason `ranges_missing`; never drop.
- AM-4 (D3, D5). Standing rule: `present` when every requested reviewer is `complete` and no cluster set was lost; `incomplete` when any requested reviewer (requested ids minus `complete_reviewers`) is not complete, when ranges are missing, or when there is at least one cluster and all were dropped; `absent` when no panel ran for this head SHA. Zero clusters with every requested reviewer complete is `present`. The field carries the reviewed SHA, `blocking_clusters`, the finding count, and the dropped list as `(cluster_id, reviewer_severity, reason)`. The run summary may not say "clean" while the panel is not `present` or `blocking_clusters > 0`.
- AM-5 (section 1.1). Append the new module to `CORE_PURE_FILES` (one additive entry) instead of a duplicate token test; either is acceptable to me, the append is preferred.
- AM-6 (D7, section 3 Found 1). The PR prerequisite from FX-5 is the category set only (severity set and lens reuse today's values); `snapshot_file_list` is the PR head's file tree, not the diff's file list.

Conditions kept from C10-R, unchanged: first release is report-only (condition 1); converter is pure with per-cluster `try` and no import of `cli/review`, `cli/reflect` or `cli/swarm` (condition 2); `body` is the representative's claim verbatim, `reviewer = "panel"` set by code, `confidence` and `original_line` unset (condition 3, with `category` now per AM-1); no second `python` fence in `SKILL.md`, no `src/superclaude/` path in installed prose, all other new tests are new files (condition 6); thread-less rule on promotion (condition 7); models named as "requested" until C-08.

Tests and measurements, on top of A's list: the AM-1 golden fixture; the zero-cluster `present` case (AM-4); the missing-ranges case (AM-3); the table test with ceiling categories (AM-2); a test that a dropped CRITICAL is named in the dropped list; M4 (new): share of clusters whose joined members span more than one category, which measures how often D1 would have fired; M2 only if the C-07 template carries an optional `in_diff` key (D7).

Invariants this resolution leaves open (id, severity):
- INV-G, HIGH: mutually blind, mechanically read-only reviewers; launch path is C-07; neither C10-R nor C10-R-B changes it.
- INV-I, HIGH: reporting-only. The three-output test pins the field, not the FSM; `terminal_clean` is set at eight sites and nobody has traced them (`fsm.py:241, :805, :872, :1026, :1085, :1120, :1145, :1253`).
- INV-007 (R-C03), HIGH: `requested` collapsing when slots are dropped without `skipped_slots`; AM-4 depends on the pre-step passing the dispatched set.
- INV-003 (R-C01), HIGH, [UNVERIFIED by me]: a repair step versus pins in `tests/review/test_review_findings.py`. In a PR one bad line (for example an over-long claim, `findings_v2.py:111`, or a category outside the set, `:109-110`) invalidates a reviewer's whole block (`:299-303`), which `cluster_v2` then ignores (`cluster.py:218-223, :256`). C-06 owns it.
- INV-L (new), HIGH before promotion, MEDIUM in the report-only release: cluster-level conversion must not collapse distinct defects (D1); closed by AM-1 plus the fixture, open until they exist.
- INV-J, MEDIUM: which tier is blocking and what routes `--fix` (`SKILL.md:305`, not re-read by me).
- INV-K, MEDIUM: the thread-less skip is callback or prose behaviour, not FSM behaviour, and is unpinned until a test is written.
- INV-M (new), MEDIUM: routed tier versus reviewer tier (D2); closed by AM-2.
- INV-F, MEDIUM: open until the prose exists; check `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`.
- Not open: INV-E, HIGH (no edit to `Finding`, `Severity`, the FSM, `reviewers.py`; one additive list entry in an existing test file under AM-5), INV-A, INV-B, INV-C (no key is added to a line or re-parsed), INV-D.
- Unmeasured: per-round cost (GQ-177, OQ-18).

What would change my mind: a fixture run showing that M4 is zero on realistic PR panels (then AM-1 costs code for nothing and may be simplified to a fixture-only guard); or a decision that the first release has no summary at all (then D2, D5 shrink to wording).

<!-- end section 6 -->

## 7. Shared-assumption responses A-001 to A-013 (Round 2)

| A-NNN | Response | One sentence |
|-------|----------|--------------|
| A-001 | ACCEPT | `SKILL.md:47-49` requires the main orchestrating session and forbids an Agent-tool subagent, so the panel pre-step is a main-session step [CODE-VERIFIED]. |
| A-002 | ACCEPT | A Grep of `src/superclaude/pr_submit` for `cli.review`, `cli.reflect`, `findings_v2`, `cluster_v2` and `superclaude.cli` returns 0 matches, and `calibrat` returns 0, so the PR path has no ledger, no kernel import and no calibration step. |
| A-003 | ACCEPT, narrowed | No PR profile exists, but only the category set needs a parameter: `check_finding` has no set parameters (`findings_v2.py:84-90`), the category sets share no value (`findings.py:15-22`, `severity_router.py:34-53`), while severity and `lens=None` work today (`findings.py:14`, `findings_v2.py:140-145`). |
| A-004 | REJECT | After conversion a `Finding` is also read for `in_diff` and `verification_status` (`fsm.py:902-906`), for `fix_key` over path, line and body (`models.py:196-207`) and for ids in reply and resolve (`fsm.py:1064-1074, :1203-1205`). |
| A-005 | QUALIFY | Panel findings entering Wave 2-4 is an owner decision; C10-R-B keeps the first release report-only and adds the "not clean" wording rule for blocking clusters (D5). |
| A-006 | REJECT | The FSM hands the whole verified list to `do_reply` and `do_resolve` unfiltered (`fsm.py:1203-1205`), so a thread-less panel finding needs a callback-level skip and a summary-only rule (`refs/thread-reply.md:92-101`) on promotion. |
| A-007 | QUALIFY | `fix_key` is stable within a run only when `body` is the claim verbatim (`models.py:196-207`) and the claim is taken from a stable representative, which in the uncalibrated PR path is the lowest-ordinal member (`cluster.py:338-344`); across a re-run after a push the identity is new by design. |
| A-008 | ACCEPT | A panel result is valid only for the head SHA it reviewed, modelled on the bot gate's `expected_head` and `pushed_sha` binding (`SKILL.md:103-112`). |
| A-009 | ACCEPT | Per-round cost is unmeasured (GQ-177, OQ-18); M1 is needed under either design before a per-round panel. |
| A-010 | QUALIFY | `dedup_groups` merges only equal `(path, line or original_line)` and keeps every finding (`reviewers.py:430-440`); `cluster_v2` bounds panel-internal duplicates but also merges distinct defects by span proximity (D1), so clustering is a cost control for same-category duplicates only. |
| A-011 | ACCEPT | Independence stays "requested, not served" until C-08 records `model_observed`; a PR report names models as "requested". |
| A-012 | ACCEPT | `finding_from_comment` validates and does not map (it reads none of `citations`, `claim`, `blocking`, `severity`, `severity_router.py:61-119`), so the converter is the mapper and no second typed validator is written. |
| A-013 | REJECT | No quorum rule exists in `cli/review` or `pr_submit` (0 matches for `quorum` or `min(2`), `evaluate_quorum` is the wrong shape (`cli/reflect/fallback.py:161-179`), and the strict rule "any requested reviewer not `complete`" needs none. |

<!-- end section 7 -->

## 8. Updated per-point table (every point; `changed` marks a movement from my Round 1 table)

"Hybrid" means C10-R-B of section 6 (C10-R plus AM-1 to AM-6) unless the sentence says otherwise. A-labelled rows: "A" is Variant A as originally written; "B" is Variant B as originally written.

| Point | Superior approach (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence |
|-------|-----------------------------------------------|--------------|------------------------|
| S-001 | Hybrid | 70 `changed` (from 55) | A's two-stage topology keeps the one `python` gate and its pins untouched (`test_codex_reviews.py:687-688`), and B's SHA binding closes the staleness gap; panel findings join `decision["used"]` (`SKILL.md:175-178`) only on promotion. |
| S-002 | Hybrid | 85 | The axes separate: slot and field to A, reader logic to B, and the converter owns the PR facts; both advocates now agree. |
| S-003 | A | 75 | C10-R-B adds one module, one field and prose, while B as written edits five functions in `reviewers.py` (`:47-78, :276, :395-424`) and three prose copies. |
| S-004 | Hybrid | 70 `changed` (from A 65) | A sibling `panel` field (A) with the value derived by B's strict rule from requested ids minus `complete_reviewers` (`cluster.py:414-418`); it avoids the `merge_wait` guards at `reviewers.py:412, :420`. |
| S-005 | Neither | 50 | Document spine does not bear on correctness. |
| S-006 | B | 55 | A's "preserved by construction" overlooked its own Output Contract field and unpinned prose (X-004), though INV-E now holds with zero edits to `reviewers.py`. |
| S-007 | Hybrid | 75 `changed` (from 70) | U-001 on fixtures that hold source blocks, T1, T3, T4, M1 to M3, plus the AM-1 to AM-4 fixtures and M4; T0 only on promotion. |
| S-008 | Hybrid | 60 `changed` (from A 55) | A dropped its quorum floor (no home, W5); B's C-06 over-limit dependency (`findings_v2.py:111`) and the R-C03 INV-007 note both stay. |
| S-009 | B | 55 | A numbered, tagged evidence table with a "Limits" section is easier to audit than inline tags. |
| S-010 | B | 55 | B carried five further objections with OPEN marks; A covered fewer. |
| C-001 | Hybrid | 60 `changed` (from 65) | Cluster for grouping and support, one Finding per (cluster, category) with chained clusters per member; cluster-only collapse mixes defects because `same_defect_v2` ignores category and claim (`cluster.py:161-181`, D1). |
| C-002 | Hybrid | 60 `changed` (from A 65) | The converter computes `in_diff` from `changed_ranges` and degrades to unset when ranges are missing; no producer exists for the bots (`classifier.py:443-456` per diff-analysis) and `pr_submit` has no hunk parser (Grep). |
| C-003 | A | 60 `changed` (from B 55) | A new module because the converter's logic is no longer a rename (section 1.1); the zero-token rule (`test_static_grep.py:48, :136-147`) applies equally to a covered new module. |
| C-004 | A | 85 | All five two-name functions stay untouched (`reviewers.py:47-78, :276, :395-424`), and B's own hybrid drops them. |
| C-005 | A | 70 `changed` (from 65) | Both hybrids use one sibling `panel` field beside `reviewers` (`SKILL.md:271`), unpinned in either until a new test exists (X-004). |
| C-006 | Hybrid | 70 `changed` (from A 60) | B's strict rule computed from requested ids; A's inputs from `cluster_v2` (`cluster.py:414-418`); no quorum helper, no floor; AM-4 fixes the empty-set case. |
| C-007 | Hybrid | 65 `changed` (from B 60) | B's head-SHA binding adopted (`SKILL.md:103-112`); A's once-per-head cadence kept because per-round cost is unmeasured. |
| C-008 | Neither | 65 `changed` (from 60) | Still an owner decision; the default is report-only plus the "not clean while `blocking_clusters > 0`" wording rule (D5). |
| C-009 | A | 55 | An adapter-owned table reaches `critical`, `medium` and `low` without a fifth key; it does not decide the tier, because ceilings and the `in_diff` drop act after it (`severity_router.py:171, :178-197`, D2). |
| C-010 | Hybrid | 75 `changed` (from 55) | `confidence` unset: a `disputed`-derived "low" would lower a tier (`severity_router.py:173-175`), and three meanings exist already (`findings_v2.py:178-182`, `cluster.py:39-44`). |
| C-011 | Neither | 65 `changed` (from 60) | Neither hybrid adds a key to the line or re-parses an extended line; the shared core takes only the decided category parameter (AM-6). |
| C-012 | Neither | 60 | Both end in a slot-less `Finding` (`models.py:179-194`); the AM-2 side record carries what the summary needs; M3 asks whether later waves need more. |
| C-013 | Neither | 75 | `verify-citations` writes an advisory sidecar both designs can read (X-007) [RELIED, `verify_cmd.py` not re-read]. |
| C-014 | Hybrid | 60 `changed` (from B 55) | Parity of the converter's output dict against `finding_from_comment` plus golden fixtures that hold source blocks; the `(reviewer_id, id)` join makes them cheap (`cluster.py:356-358, :373`). |
| C-015 | A | 55 | Per-consumer converters match B's own admission that the `/task` gate uses none of the four PR keys; a prediction [UNVERIFIED]. |
| C-016 | A | 85 `changed` (from 75) | `Finding.reviewer` defaults to `"augment"` when absent (`severity_router.py:118`), so code must always set `"panel"`; both advocates agree. |
| X-001 | B | 90 | The cluster record has no severity or category (`cluster.py:352-378`); the repair is the `(reviewer_id, id)` join, with path and line already on the member (`:363`). |
| X-002 | B | 60 | `reviewer_activity` is a literal two-key dict not read from `REVIEWERS` (`reviewers.py:73-78` [CODE-VERIFIED]); A's pin claim holds only for a B that edits it; both are bound by the one-fence pins. |
| X-003 | B | 90 | 47 `test_*.py` files, not 50 [RELIED on diff-analysis Glob]. |
| X-004 | Neither | 85 | No test pins the `reviewers` row (the contract slicer checks only the `merge_guard` row, `test_merge_guard_protocol.py:498-508` [RELIED]), so an added key or field is equally unpinned. |
| X-005 | Neither | 65 `changed` (from A 65) | B10 holds only for an A without a `panel` field, and a present panel beside `terminal_clean` is its own gap (D5); `terminal_clean` is assigned at eight sites, none traced. |
| X-006 | A | 70 | The bots have no producer of `in_diff` or `confidence` (`classifier.py:443-456` per diff-analysis); `auggie-reviewer.md:54-67` carries two of B's four keys [RELIED]. |
| X-007 | Neither | 75 | `Finding` has no slot for citation flags in either design (`models.py:179-194`), so both read the same sidecar. |
| X-008 | A | 70 | With the panel excluded from re-triggers, only the name-agnostic absent fold is reusable, and A can emit it too [RELIED]. |
| X-009 | Hybrid | 70 `changed` (from A 70) | No quorum rule exists (0 matches in `cli/review` and `pr_submit`), `evaluate_quorum` is the wrong shape (`fallback.py:161-179`), and the strict rule needs none. |
| X-010 | Neither | 65 `changed` (from 60) | `pr_submit` has no hunk parser (Grep), so both designs need new diff-aware code; AM-3 makes `changed_ranges` a degrade-not-drop input. |
| A-001 | Neither | 90 `changed` (from 80) | Shared and verified at `SKILL.md:47-49`. |
| A-002 | Neither | 90 `changed` (from 80) | `pr_submit` has zero imports of `cli.review`, `cli.reflect`, `findings_v2`, `cluster_v2` or `superclaude.cli`, and no `calibrat` (Grep). |
| A-003 | Neither | 85 | Both need a PR profile; the minimum is a category-set parameter (`findings_v2.py:84-90, :109-110`; `findings.py:15-22`). |
| A-004 | Neither | 70 | False for both: `in_diff`, `verification_status`, `fix_key` and comment ids are read (`fsm.py:902-906`, `models.py:196-207`). |
| A-005 | Neither | 70 `changed` (from 65) | Both treat Wave 2-4 entry as given; the first release is report-only and which tier blocks is open (INV-J). |
| A-006 | Neither | 80 `changed` (from 75) | The FSM hands thread-less findings to the callbacks unfiltered (`fsm.py:1203-1205`); the default is a callback-level skip plus a summary-only rule on promotion (INV-K). |
| A-007 | Hybrid | 70 `changed` (from Neither 60) | `body` as the claim verbatim keeps `fix_key` stable within a run (`models.py:196-207`); the representative is the first reviewer in the uncalibrated path (`cluster.py:338-344`). |
| A-008 | Hybrid | 70 `changed` (from B 60) | The `panel` field carries the reviewed SHA, as the bot gate does (`SKILL.md:103-112`); no automatic re-run in the first release. |
| A-009 | Neither | 90 `changed` (from 85) | Cost is unmeasured for both (GQ-177); M1 serves both. |
| A-010 | Hybrid | 60 | Exact-line dedup is correct but costly (`reviewers.py:430-440`); `cluster_v2` bounds same-category duplicates only (D1). |
| A-011 | Neither | 90 `changed` (from 85) | Carried from R-C03; identical in both. |
| A-012 | Neither | 85 `changed` (from 80) | `finding_from_comment` is the validation seam (`severity_router.py:61-119`); the converter module is the mapper. |
| A-013 | Hybrid | 70 `changed` (from Neither 70) | The strict rule "any requested reviewer not `complete`" needs no quorum rule; none exists in `cli/review` or `pr_submit` (0 matches). |

Agreement with A on the winner per point: the labels in this table equal A's Round 2 table on all 49 points (S 10, C 16, X 10, A 13). The contents behind five labels differ: C-001, C-002, C-006, S-004 and S-008 name "Hybrid", and my Hybrid carries AM-1 to AM-6. C-003 and C-009 carry the same label for different reasons (sections 1.1 and 4 D2). Confidence differs from A's by 5 or more points on S-001 (70 against 65), S-006 (55 against 60), C-003 (60 against 65), C-009 (55 against 60) and X-002 (60 against 70).

Status: Complete
<!-- end of round2-advocate-B.md -->
