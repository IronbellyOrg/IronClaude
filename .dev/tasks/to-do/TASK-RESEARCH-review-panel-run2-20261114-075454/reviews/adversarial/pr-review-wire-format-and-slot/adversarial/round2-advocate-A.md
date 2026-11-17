### Variant A Rebuttal (Round 2)

Slot C-10 (pr-review-wire-format-and-slot), Round 2, standard depth; focus correctness, risk, test-coverage. Code state: HEAD 50d4d2b9d, branch ironbelly/shadow-runs. Nothing was run; no test, no pytest. Tags: [CODE-VERIFIED] = I read that file:line myself in this Round 2 session; [UNVERIFIED] = carried from a document or a Round 1 file and not re-read now; [RELIED] = taken from diff-analysis.md or a Round 1 file and not re-checked. Paths are relative to the repository root. This file cites nothing from the run-1 task folder or the run-1 queued file.

## 1. Responses to B's Round 1 criticisms of A

### 1.1 B's Weaknesses 1-8

| # | B's criticism of A | My response | Evidence |
|---|--------------------|-------------|----------|
| W1 | A section 3.5 says the cluster record holds what the adapter reads; it does not hold severity or category (X-001), so A needs source blocks and is "B's reader in an extra module". | CONCEDE the claim, REBUT the inference. The cluster record has no severity and no category. But each member already carries `primary_citation` with `path`, `line_start`, `line_end`, `status` (`cluster.py:354-367`, built by `annotate` at `:148-154`), and the cluster carries the representative's verbatim `claim` and `blocking_any` (`:374-375`). So path, line, body and blocking need no join; only `severity` (and `category`) need the source line, joined on `(reviewer_id, id)` (item (e) below). No edit to `cluster.py`. The converter is therefore "B's reader plus A's grouping": I accept that sentence as the shape of the resolution. | `cluster.py:352-378` [CODE-VERIFIED] |
| W2 | A's `confidence` from `disputed` is a fourth meaning of `confidence`. | CONCEDE, and the evidence is worse for A than B stated. The router drops one tier on `confidence == "low"` (`severity_router.py:173-175`). A `disputed`-derived "low" would lower a CRITICAL whose only support is one reviewer, which contradicts R-C02's "a CRITICAL is never lowered" (A's original section 5, C-02 paragraph). Decision: `confidence` is left unset (None) in the first release. | `severity_router.py:173-175`; `cluster.py:347-351` [CODE-VERIFIED] |
| W3 | A's primary producer of `in_diff` assumes a hunk list the pre-step "already holds"; `pr_submit` has no hunk parser. | CONCEDE that it is a premise and new code. `severity_router.py` has no `@@`, `diff` or hunk handling (Grep count 0), and B's own grep found only fix-hunk text in `fsm.py`. Position: it becomes a stated precondition. The panel cannot review a PR without the diff text, so the main session holds it [UNVERIFIED how it retains it]; the converter takes `changed_ranges` as an input and, when it is absent, converts nothing and reports the panel `incomplete` (fail-closed, same family as `is_groundable`, `fsm.py:364-372`). B's M2 fallback needs the same parser, so this is not a differentiator. | `severity_router.py` Grep [CODE-VERIFIED]; `fsm.py:364-372` [CODE-VERIFIED] |
| W4 | "Zero edits" is true of existing code only; the sibling Output Contract field and pre-step prose are as unpinned as B's third key. | CONCEDE. Restated claim: zero edits to existing `pr_submit` Python modules and to existing tests; two prose files (`SKILL.md` Output Contract, `commands/pr-submit.md`) gain one `panel` row/sentence, unpinned until a new test is written. B is right that INV-E is "preserved by construction" only for `Finding`, `Severity`, FSM. | `SKILL.md:255-275` [CODE-VERIFIED] |
| W5 | A's quorum rule has no home; a helper in the core contradicts "no change to `cluster.py`", a helper in the adapter turns the mapper into a policy holder. | CONCEDE and drop the rule. I withdraw the `min(2, requested)` floor from A's Round 1 hybrid. I adopt B's stricter rule (any requested reviewer not `complete` means the panel is `incomplete`; section 4 row 6). It needs no new helper and no unmeasured parameter. | `cluster.py:414-418` [CODE-VERIFIED]; grep `quorum\|min\(2` over `cli/review` and `pr_submit`: 0 matches [CODE-VERIFIED] |
| W6 | A's "put a support count or second citation in `body`" changes `fix_key` between rounds (identity bug). | CONCEDE. `fix_key = sha256(path, line, body)` (`models.py:196-207`). `body` is the representative's `claim` verbatim and nothing else; `cluster["claim"]` is exactly that string (`cluster.py:294, 374`). | `models.py:196-207` [CODE-VERIFIED] |
| W7 | A leaves staleness and re-run open; bots are SHA- and watermark-bound. | CONCEDE and adopt. The bot gate binds to `expected_head` and `pushed_sha` (`SKILL.md:103-112`). The panel field carries the SHA it reviewed; a result is valid only for that SHA; no automatic re-run after a fix push in the first release (cost unmeasured, GQ-177). | `SKILL.md:103-112` [CODE-VERIFIED] |
| W8 | "One adapter per consumer" is a linear cost model. | ACKNOWLEDGED, not contested. B did not press it and neither do I: it is the accepted cost of A. | n/a |

### 1.2 B's concessions and what they leave

- B concessions 1 (X-008), 2 (X-009/A-013), 3 (X-006), 4 (C-004), 5 (X-005/B10), 6 (C-001), 7 (C-002/C-016/C-010) and 9 (C-003/X-010 hunk parser) are accepted as stated and I now rely on them. Net effect: B conceded the slot axis (S-002 to S-004, C-004, C-005) and the producer of the PR-local keys.
- B concession 2 names a quorum evaluator in `cli/reflect/fallback.py:76-82, 161-178`. It exists, but it is not a usable rule for the PR panel (item (b) below). B's replacement rule ("any reviewer not `complete`") is the right one and I take it.
- B concessions 8 and 10 (C-008/O3; A-006) leave two items open that I now close with defaults (section 4 rows 8 and 9; section 5 conditions 1 and 7), each flagged as owner-decidable.
- B concession 7 ("the defensible core of B is the reader, not the four keys") is the sentence that makes the two hybrids nearly one design; section 4 lists exactly what remains.

### 1.3 B's per-point disagreements with my Round 1 table

| Point | B said | I said (R1) | Now | Why |
|-------|--------|-------------|-----|-----|
| S-001 | Hybrid 55 | A 60 | Hybrid 65 (`changed`) | B's SHA binding is needed; A's topology stands. |
| S-004 | A 65 | Hybrid 65 | Hybrid 70 (`changed`) | Sibling field (A) with B's derivation of the value. |
| C-001 | Hybrid 65 | A 70 | Hybrid 75 (`changed`) | Cluster first, then one `Finding` per cluster; content from the representative member. |
| C-002 | A 65 | Hybrid 55 | Hybrid 60 (`changed`) | Harness-computed, fail-closed when ranges are absent; reviewer-stated values only compared (M2). |
| C-003 | B 55 | A 70 | A 65 (`changed`) | B's point that `severity_router.py` is already on the purity list is real, but the zero-token rule makes it the worse home for a hunk parser (item (d)). |
| C-005 | A 65 | Hybrid 60 | A 70 (`changed`) | Both hybrids use a sibling field. |
| C-006 | A 60 | Hybrid 55 | Hybrid 70 (`changed`) | Strict rule from B, inputs from `requested` and `complete_reviewers`. |
| C-010 | Hybrid 55 (omit key) | A 65 | Hybrid 75 (`changed`) | I concede; see W2. |
| C-011 | Neither 60 | A 60 | Neither 65 (`changed`) | Neither hybrid adds a key to the line format. |
| C-012 | Neither 60 | A 55 | Neither 60 (`changed`) | Body is the claim verbatim; value of dropped fields is M3's question. |
| C-014 | B 55 | A 55 | Hybrid 60 (`changed`) | A parity test on the converter's output dict plus golden fixtures that hold source blocks. |
| X-005 | A 65 | Neither 70 | Neither 70 | B10 is not a separator once the `panel` field exists; I have not traced `terminal_clean`. |

<!-- end section 1 -->

## 2. Updated assessment of Variant B after B's defence

What B got right and I now rely on:
1. The converter must read the source line, not the cluster record (X-001). B found this; I missed it.
2. The `incomplete` rule "any requested reviewer not `complete`" is stricter, simpler and needs no unmeasured parameter. It is better than my `min(2, requested)` floor.
3. `body` must be the claim verbatim (A-007, O4) and the panel result must be bound to the head SHA it reviewed (A-008).
4. Test and measurement set: T1 (parity), T3 (status pin), T4 (grounding), M1 (cost), M2 (reviewer-stated versus hunk-computed `in_diff`), M3 (does any later wave read `quote`, a second citation or `blocking`). I adopt all of them. T0 (unknown keys) is a defensible pin but is only needed if keys are promoted (item (a)).
5. The slot axis: B's own B13 and concession 4 make the third `REVIEWERS` name the costlier option, and B dropped it.

What B still gets wrong or has not shown:
1. The "reader placed next to `finding_from_comment`" claim. `severity_router.py` is on the zero-token list (`tests/pr_submit/test_static_grep.py:48`, check at `:136-147` scans every line including comments and docstrings for `\bgh\b|\bgit\b`). A hunk parser (needed by both hybrids, W3) naturally mentions diff headers; a new module is the safer home (item (d)). This is a moderate point, not a decisive one.
2. B's hybrid reads "the `representative` source line" only. The representative is chosen by calibrated confidence then order (`cluster.py:338-344`), not by severity. A cluster of {MAJOR (representative), CRITICAL (other member)} would lose the CRITICAL. R-C02's floor says a CRITICAL is never lowered, and `blocking_any` is already "any member" (`:375`). The converter must take severity as the maximum over the joined members and take the claim and citation from the representative. B's hybrid does not say this.
3. `original_line` is carried by both hybrids and is useless for panel findings. It has producers only for bot comments (`classifier.py:449`, `reviewers.py:295-309`) and one consumer, the `dedup_groups` fallback when `line` is None (`reviewers.py:438`). A panel finding always has an integer `line` (`is_groundable` drops it otherwise, `fsm.py:364-372`), so `original_line` is never read. I drop it from my hybrid and ask B to drop it from theirs.
4. B's mitigation for model-emitted keys ("the harness injects them into the line") only helps if the harness writes the keys after `parse_block`, in memory. Then there is no difference from the converter setting them on the dict, and "injecting into the line" mutates a record the kernel hands out. If it writes them back to a findings-v2 block and re-parses, B's T0 hole (item (a)) is live. Either way the keys-on-the-line step has no purpose once the converter owns them.
5. B's own residual open items (C-008, A-006) are still not closed in B's hybrid. I close them with defaults in sections 4 and 5.

Net: after Round 1, B and A agree on the slot, on who computes the PR facts, on the `confidence` and `body` rules and on the measurements. Remaining differences are placement, the exact reader input, severity aggregation and two defaults; section 4 settles each.

<!-- end section 2 -->

## 3. New evidence: the five contested code facts, plus what I found on the way

### (a) Do `parse_block` and `check_finding` keep unknown keys on a findings-v2 line, and does a test pin it? Result: B is right on both counts.

- `check_finding` never iterates the keys of `obj`; the only key-level rejection is `calibrated_confidence` (`src/superclaude/cli/review/findings_v2.py:96-97`). `parse_block` then appends the whole object after `obj.setdefault("refs", [])` (`:288-290`), so an extra key survives into `res["findings"]`. [CODE-VERIFIED]
- The module docstring reserves the opposite: "A findings-v1-valid line with other keys may be rejected" (`:3-5`). Acceptance is a property of the code today, not a stated promise. [CODE-VERIFIED]
- No test pins acceptance. `test_v1_line_passes_v2_unchanged` uses only lines whose keys are all in `V1_FIELDS` (`tests/review/test_review_findings_v2.py:69-81`, assertion at `:72`); `test_check_finding_never_raises` varies `V1_FIELDS`, `V2_FIELDS` and the citation keys only (`:372-401`); the other `base(...)` overrides set known keys or `calibrated_confidence` (`:128-172, :205, :330-350`); the `unknown key` pins in `tests/review/test_review_panel.py:33, :65` are for panel-config objects. [CODE-VERIFIED for those files; I did not read every test that calls `parse_block`, so "no test anywhere" is not shown, only "none in `test_review_findings*.py` and none by name or phrase in `tests/review` and `tests/cli/reflect`".]
- Engagement: the hole is live for B as originally written (reviewer-emitted keys). It is not live for either hybrid as long as the PR facts are set on the converter's output dict after `parse_block` and `cluster_v2` and are never written back into a findings-v2 block that is re-parsed. `annotate` and `_members` read only named keys (`cluster.py:126-154, :288-297`), so extra keys do not disturb clustering either. T0 stays a cheap insurance test if keys are ever promoted (promotion trigger in section 5).

### (b) Is there a quorum evaluator at `cli/reflect/fallback.py:76-82, 161-178`? Result: yes, but it is not usable for the PR panel.

- `QuorumState` (`:75-82`) and `evaluate_quorum(workers: list[WorkerResult], *, allow_single_vendor)` (`:161-179`) exist. It counts workers whose `status == "success"` (`:166`) and requires `reviewer_count >= 2`, `model_class_diversity == "full"` and multi-vendor or `allow_single_vendor` (`:169-173`). [CODE-VERIFIED]
- It works on swarm `WorkerResult` records and statuses (`"success"`, `"timeout"`, `"proxy_error"`, `"parse_error"`, `:40`), not on findings-v2 completion states (`complete`, `truncated`, `invalid`, `failed`, `timed_out`, `findings_v2.py:40`) and not on `cluster_v2` output. The module imports `superclaude.cli.swarm.*` (`:15-28`). The names `evaluate_quorum` and `QuorumState` appear in no other file under `src/superclaude`. [CODE-VERIFIED]
- `pr_submit` has zero imports of `cli.review`, `cli.reflect`, `findings_v2`, `cluster_v2` or any `superclaude.cli` module (Grep, 0 matches). Reusing this evaluator would add the first `pr_submit` to `cli.swarm` dependency and would impose a model-class diversity requirement that the PR panel has not decided (independence is "requested, not served" until C-08). The `quorum` and `min(2` patterns have 0 matches in `cli/review` and `pr_submit`. [CODE-VERIFIED]
- Consequence: B's concession stands (no review-kernel quorum rule exists), B's own replacement rule needs no evaluator, and I adopt it.

### (c) Does the bot-gate pattern at `SKILL.md:118-124` and `:143-149` drop a whole batch on a `ValueError`, and would B's reader need it? Result: yes it drops the batch; neither hybrid needs it, and copying it would be a defect.

- Both blocks read: `try: ... findings = [finding_from_comment(raw) for raw in selected] ... except ValueError: review_state = "polling"; findings = []` (`SKILL.md:118-124` Augment, `:143-149` Codex). One bad root discards that reviewer's whole batch and the gate retries on the next poll. [CODE-VERIFIED]
- That is correct for the bots, because a bot batch is re-read from GitHub on the next poll. The panel has no re-poll: a dropped batch would be a silent loss, which breaks INV-I.
- What can raise in the converter? `finding_from_comment` raises for a non-object, empty `path` or `body`, non-positive-integer locations, non-text hint/category/confidence/reviewer, non-bool `in_diff` (`severity_router.py:67-82`). After `check_finding`, `path` is a non-empty repo-relative string and `line_start` a positive integer (`findings_v2.py:59-81`), `claim` is a string of at most 300 flattened characters (`:111`), and `category` is in the allowed set (`:109-110`). `reviewer`, `in_diff`, `severity_hint` and `confidence` are set by converter code, not by a model. So no model-typed field can reach the `ValueError` branches under either hybrid; only the converter's own bugs or an empty/whitespace claim can. For original B (reviewer-emitted `in_diff`, `reviewer`), a string-typed `in_diff` passes the core silently (item (a)) and would raise here.
- Rule for both hybrids: convert per cluster, catch `ValueError` per cluster, collect `(cluster_id, reason)` into a `dropped` list that is reported in the `panel` field and the summary; never wrap the batch in one `try`. Test: three clusters with one malformed gives two `Finding`s and one reported drop.

### (d) Is `severity_router.py` on the static-purity list, and does adding a module require editing that file? Result: yes it is listed; no, a new module needs no edit.

- `CORE_PURE_FILES` names `fsm.py`, `severity_router.py` (`tests/pr_submit/test_static_grep.py:48`), `loop_guard.py`, `ci.py`, `conflicts.py`, `merge_guard.py` and four skill refs (`:37-55`). `test_tn50_core_pure_no_gh_git_tokens` reads each listed file line by line and fails on any `\bgh\b` or `\bgit\b`, with no comment or docstring exemption (`:136-147`). `test_tn41_core_never_imports_anthropic` is the only test that globs every `PR_SUBMIT_PKG/*.py` (`:150-159`). [CODE-VERIFIED]
- So: a new module is outside T-N50 by default (no edit needed for the suite to pass, but also no purity coverage); covering it means appending it to `CORE_PURE_FILES` (an additive edit to an existing test file) or a new test file that applies the same token check (no existing test edited). A function added to `severity_router.py` stays under T-N50, so its code and docstrings must avoid the words `git` and `gh`; a hunk parser that quotes `diff --git` headers would fail the suite.
- Also pinned and binding on both hybrids: SKILL.md may contain exactly one ```python fence (`tests/pr_submit/test_merge_guard_protocol.py:533`, `tests/pr_submit/test_codex_reviews.py:687-688`, `tests/pr_submit/test_cosmos_protocol.py:35-36`; `test_conflict_sync_protocol.py:534` filters lines starting with ```python, assertion not read). The existing merge step is a ```text fence (`SKILL.md:160-173`). Any pre-step code must therefore be described in prose or ```text fences, or live in a new ref; it must not add a ```python fence to SKILL.md. [CODE-VERIFIED]
- `tests/pr_submit/test_cosmos_protocol.py:51` pins `core.finding_from_comment is severity_router.finding_from_comment`; a sibling function or module does not touch it. [CODE-VERIFIED]

### (e) How does a cluster `representative: {reviewer_id, id}` (`cluster.py:373`) join back to the source line? Result: a well-defined key join, with three conditions.

- A reviewer record is `(reviewer_id, ordinal, findings_v2_block, calibration_map)` (`cluster.py:3-4, :202`); the block is a `parse_block` result or a bare list (`:218-223`). Each member carries `reviewer_id` and `id` (`:356-358`); the representative is `{reviewer_id, id}` (`:373`). The join is `lookup[(reviewer_id, id)]` over the findings of the valid records. [CODE-VERIFIED]
- Uniqueness: `_records` skips a duplicate `reviewer_id` (`:235-247`) and `_members` skips a duplicate finding `id` within a reviewer (`:258-277`), so each `(reviewer_id, id)` names at most one clustered finding; `parse_block` already rejects duplicate ids (`findings_v2.py:101-102`). The converter must build its lookup the same way: valid records only (a list block, or a dict with `state == "complete"`, `:218-223`), first occurrence wins.
- `cluster_v2` does not change its inputs (`:3-4`), so the same record objects can be passed to both calls with no drift. If a lookup misses (records changed between the two calls), skip the cluster and count it in `dropped`; never guess.
- What the join is needed for: only `severity` and `category` (and a quote if ever wanted). `path`, `line`, `claim` and `blocking_any` come straight from the cluster (`:354-367, :374-375`). Severity is the maximum over all joined members, not the representative's, because the representative is the most confident member, not the most severe (`:338-344`).
- Conditions: (1) `snapshot_file_list` must list the PR head's files, because only `resolved` citations cluster (`:170-179`) and a citation to a file missing from the list is `unresolved`; (2) a member whose `primary_citation` is `malformed` has `line_start None` (`:112-113`), so the converter drops that cluster and counts it; (3) `annotate` falls back to the first citation when the lens has no `PRIMARY_ROLES` entry (`:133-134`), so the PR template must say the first citation is the defect location (a template-content matter, slot C-07).

### Found on the way

1. Category vocabularies do not overlap. The core `CATEGORIES` is six review values (`src/superclaude/cli/review/findings.py:15-22`); the router's table has 18 PR values (`severity_router.py:34-53`). `check_finding` rejects a category outside the core set (`findings_v2.py:109-110`), and `parse_block` marks the whole block `invalid` on any one error (`:301-302`), after which `cluster_v2` ignores the block (`cluster.py:218-223, :256`). Until the decided FX-5 parameterisation lands, one PR-category line removes a reviewer's entire block. FX-5 is prerequisite work for both hybrids (A-003).
2. `Finding.reviewer` defaults to `"augment"` when absent (`severity_router.py:118`), so a converter that forgets to set it labels a panel finding as Augment. It must always set `reviewer = "panel"`.
3. `fsm.py` passes the whole verified list to `do_reply` and `do_resolve` with no filter (`:1203-1205`; the fallback path computes `fallback_only` from integer `comment_id`s, `:1064-1074`); both callables are supplied by the caller and default to `_noop` (`:945-946`). A thread-less panel finding would reach them. [CODE-VERIFIED]
4. The existing precedent for findings without a thread: one PR conversation follow-up on the issue-comments surface, no inline reply, no GraphQL resolution (`src/superclaude/skills/sc-pr-submit-protocol/refs/thread-reply.md:92-99`). [CODE-VERIFIED]

<!-- end section 3 -->

## 4. The two hybrids: what they share and where they still differ

Shared, no dispute left: the panel runs as a main-session pre-step before the snapshot gate (`SKILL.md:47-49`); no `panel` entry in `REVIEWERS`, no third pair in `merge_wait`, `reviewers.py` and the python gate untouched; panel standing is a sibling Output Contract field with values `present | absent | incomplete`, bound to the head SHA it reviewed and never read as clean (INV-I); `Finding`, `Severity`, the FSM and the fork-only checks are not edited; `reviewer = "panel"` is set by code, not by a model; `finding_from_comment` is the single validation seam (`severity_router.py:61-119`); `cluster_v2` runs first; FX-5 vocabulary parameters on `check_finding` are prerequisite work for both; M1 (cost) is needed before a per-round panel.

Where they still differ, each with my position:

| # | Dimension | A-prime (my Round 1 file) | B's reader on A's slot (B Round 1 file) | My position now | Conf. | Reason |
|---|-----------|---------------------------|------------------------------------------|-----------------|-------|--------|
| 1 | Where the converter lives | New pure module on the `pr_submit` side | `finding_from_v2` in `severity_router.py` beside `finding_from_comment` | New pure module | 65 | `severity_router.py` is under the zero-token rule (`test_static_grep.py:48, :136-147`) and a hunk parser needs diff-header vocabulary; the FSM and 47 test files lean on the router. Cost I accept: the module has no purity coverage until a new test is written (no existing test edited). B's argument that the router is already covered is true and is the one real point for B. |
| 2 | What it reads | Cluster output plus the same reviewer records, joined on `(reviewer_id, id)` | The source line chosen through `representative`, content from the line | Cluster output plus records; path, line, claim, blocking from the cluster, severity and category from the joined lines | 75 | Representative is the most confident member, not the most severe (`cluster.py:338-344`); taking its severity alone can lower a CRITICAL member (item (e)). The two hybrids converge on "join via representative" for content. |
| 3 | Who sets `in_diff` (and `reviewer`) | Converter sets them on the dict it passes to `finding_from_comment` | Harness injects them into the v2 line | Converter sets them on its own output dict; the v2 record is never mutated | 70 | In-memory injection after `parse_block` is the same operation under another name; mutating a kernel-owned record adds a drift risk and, if written back and re-parsed, engages the unknown-key hole (item (a)). `in_diff` needs `changed_ranges`; absent ranges means nothing converts and the panel is `incomplete`. |
| 4 | Are the four keys ever promoted to the line format? | Only on a trigger: M3 nonzero, a second consumer needs the same per-finding key, or M2 shows reviewer-stated `in_diff` is more accurate | In B's hybrid the harness writes them onto the line; promotion is not argued | No promotion now; keep the trigger | 75 | With the converter owning the keys, promotion has no consumer. `original_line` is dropped outright: its only reader for a finding is the `dedup_groups` fallback when `line` is None (`reviewers.py:438`), and a panel finding always has a line. T0 is added only at promotion. |
| 5 | `confidence` | R1: from cluster facts or None | Drop until a threshold is measured | Unset (None); router step 3 stays dormant for the panel as it is for both bots | 85 | A `disputed`-derived "low" would lower a CRITICAL (`severity_router.py:173-175`), contradicting R-C02; `self_confidence`, calibrated support and the router text are three existing meanings (`findings_v2.py:178-182`, `cluster.py:39-44`). |
| 6 | The `incomplete` rule | `invalid_reviewers` / `valid_blocks` floor with `min(2, requested)` | Any reviewer not `complete` | Any requested reviewer not `complete` (B's rule), computed against the dispatched set | 80 | Needs no helper and no unmeasured parameter; `incomplete` only labels, it does not stop valid reviewers' findings from being reported. It must be computed as `requested_ids minus complete_reviewers`, not from `invalid_reviewers` alone, because a reviewer that never produced a record is invisible to `cluster_v2` (`cluster.py:414-418`); this is R-C03's HIGH INV-007 and is the pre-step's job. Values: `present` (all requested complete), `incomplete` (some not, or `changed_ranges` missing, or every cluster dropped), `absent` (no panel run for this head SHA). |
| 7 | `body` content | R1: could carry a support count or second citation as text | Claim verbatim | The representative's `claim` verbatim and nothing else | 90 | `fix_key` hashes `body` (`models.py:196-207`); I withdraw the R1 suggestion. Panel provenance and support go in the summary comment, never in `body`. |
| 8 | Thread-less panel findings (A-006) | R1: summary-only reporting | Left open | One PR conversation follow-up listing panel findings and what was applied; no inline reply, no resolve; the caller's `do_reply` and `do_resolve` skip any finding with no integer `comment_id` | 70 | The precedent exists (`thread-reply.md:92-99`). The FSM hands the whole list to the callbacks unfiltered (`fsm.py:1203-1205`), so the skip must live in the skill-supplied callbacks or the prose, because filtering in `fsm.py` would edit the FSM (INV-E). That skip is prose-level and unpinned until a test exists: stated as open INV-K (section 5). |
| 9 | Bots silent or clean while the panel has findings (C-008) | Not addressed | Open (O3) | First release is report-only for panel findings; they join `decision["used"]` (`SKILL.md:175-178`) only after the owner decides A-005 and INV-J | 65 | Both advocates said "report-only first". It also makes row 8 moot until promotion. `terminal_augment_no_response` stays keyed to the two bots because the panel is not in `merge_wait`. |
| 10 | Severity table | Adapter-owned, splits MAJOR by `blocking` | Lossy three-to-five map, or a fifth `severity_hint` key | Adapter-owned table: CRITICAL to `critical`; MAJOR with `blocking_any` to `medium`; MAJOR without and MINOR to `low`; no `high`, no `nit` from the table | 55 | Medium is the standard `--fix` route and High the costlier deep route (`severity_router.py:56-58, :203-214`); the router's category floors can still raise a non-blocking finding (`:34-53`, `:171`), so "blocking is authoritative" holds only up to the rubric. The table is the PR module's choice (INV-J, owner-decidable); I give a default, not a decision. |
| 11 | Cadence | Optional, per PR | Per round, inside the round cap | Once per PR head SHA at run start; no automatic re-run after a fix push in the first release; the field records the reviewed SHA | 65 | Cost is unmeasured (GQ-177); a stale result is shown as the SHA it reviewed, not as current. |

<!-- end section 4 -->

## 5. The single resolution I now propose as the debate outcome

Name: **C10-R, "separate pre-step, pure panel-to-Finding converter, sibling `panel` field"**. It is A's slot and ownership with B's reader logic, B's `incomplete` rule and B's measurements. Overall confidence 70%.

In one paragraph: the panel runs as a main-session pre-step before the snapshot gate. A new pure module on the `pr_submit` side takes `cluster_v2` output, the same reviewer records, the PR's changed-line ranges, the PR-profile severity table, the requested reviewer ids and the head SHA, and returns `Finding`s built through the unchanged `finding_from_comment`, `remap_severity` and `route`, plus a `dropped` list and the panel standing. The standing is reported in a new sibling Output Contract field `panel`, never inside `reviewers`. `REVIEWERS`, `reviewers.py`, `merge_wait`, the python gate, `Finding`, `Severity` and the FSM are not edited, and neither is any existing test.

Conditions (the resolution is wrong or incomplete without them):

1. **First release is report-only.** Panel findings are converted, remapped and routed, and listed in the summary and the `panel` field; they are not appended to `decision["used"]` (`SKILL.md:175-178`) and drive no push. Promotion needs the owner's answer on A-005, C-008 and INV-J.
2. **Converter shape.** Pure, dict in and out, no import from `cli/review`, `cli/reflect` or `cli/swarm`, no `gh` or `git` tokens (a new test applies the T-N50 token check to it; `test_static_grep.py` is not edited). Conversion is per cluster, each in its own `try`; a `ValueError`, a malformed primary citation, a join miss, an empty claim or missing `changed_ranges` is counted in `dropped` with a reason, never silent and never a batch drop (item (c)).
3. **Field rules.** Path and line from the representative member's `primary_citation`; `body` is the representative's `claim` verbatim; severity is the maximum over all joined members, `blocking` is `blocking_any`; `reviewer = "panel"`; `in_diff` computed from `changed_ranges`; `confidence` unset; `original_line` unset; `category` from the representative, checked against the PR profile set.
4. **Standing rule.** `present` when every requested reviewer is `complete`; `incomplete` when any requested reviewer is not (computed as requested ids minus `complete_reviewers`, so a reviewer that never produced a record counts), when `changed_ranges` is missing, or when every cluster was dropped; `absent` when no panel ran for this head SHA. The field carries the reviewed SHA, the finding count and the dropped count. A run summary never says "clean" while the panel is not `present`. Models named in a PR report say "requested", not "served", until C-08.
5. **Prerequisites owned elsewhere.** FX-5 category, severity and lens parameters on `check_finding` with today's constants as defaults (a PR category outside the core set invalidates a reviewer's whole block today, section 3 found-on-the-way 1); `snapshot_file_list` is the PR head file list; the PR template says the first citation is the defect location (C-07); the repair policy for over-limit lines and long hunks (C-06).
6. **Prose and test constraints.** No new ```python fence in `SKILL.md` (four tests pin one, item (d)); pre-step steps are prose or ```text, or live in a new ref; no `src/superclaude/` path in installed prose (INV-F); all new tests are new files.
7. **Thread-less rule on promotion.** One PR conversation follow-up for panel findings (`thread-reply.md:92-99`); the skill-supplied `do_reply` and `do_resolve` skip any finding with no integer `comment_id` (`fsm.py:1203-1205`); a test pins the callback contract.

Tests and measurements it commits to (all offline except M1 to M3):
- Conformance: golden fixtures of (cluster output + records) for single reviewer, multi-reviewer, citation-only, unresolved, malformed primary, `disputed`, non-blocking MAJOR, CRITICAL in a non-representative member, join miss, empty claim, missing ranges.
- T1 parity: the converter's output dict through `finding_from_comment` equals the hand-written equivalent field by field.
- U-001 equivalence run against a scratch B-style reader on fixtures that hold source blocks; promotion trigger if it differs.
- T3 pin that `merge_wait`, `reviewer_activity` and the python-fence count are unchanged; T4 grounding (anchor-only line dropped); a three-output standing test (clean, incomplete, absent) that leaves `reviewers` unchanged; a per-cluster drop test.
- M1 cost per round; M2 reviewer-stated versus hunk-computed `in_diff` (informs promotion only); M3 later-wave use of `quote`, a second citation or `blocking`.

Invariants it leaves open (my grading; ids as in the slot files, new ids marked):
- INV-G, HIGH: mutually blind, mechanically read-only reviewers. Launch path is C-07; C10-R neither helps nor worsens it.
- INV-I, HIGH: "absent or incomplete never reads clean" is satisfied as reporting only. Nobody has traced how `terminal_clean` is reached; `fsm.py` sets it at `:241, :805, :872, :1026, :1085, :1120, :1145, :1253` [CODE-VERIFIED by Grep, not traced]. The three-output test pins the field, not the FSM.
- INV-007 (from R-C03), HIGH: `requested` collapsing when slots are dropped without `skipped_slots`. Rule 4 depends on the pre-step passing the dispatched set.
- INV-003 (from R-C01), HIGH: a repair step versus the pins at `tests/review/test_review_findings.py:113, :117` [UNVERIFIED by me]. In a PR, one bad line costs a reviewer's whole block (section 3 found-on-the-way 1); C-06 owns it.
- INV-J, MEDIUM: Medium routes to `--fix`, and the merge guard keys on Medium or higher (`SKILL.md:305` per B and R1, not re-read) while the repo rule says Medium is a warning. The severity table is the PR module's choice; category floors can still raise a non-blocking finding.
- INV-K (new), MEDIUM: the thread-less skip is prose and callback behaviour, not FSM behaviour, and no test pins it until written (condition 7).
- INV-F, MEDIUM: open until the prose exists; check with `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`, and the one-python-fence pin must hold.
- Not open: INV-E HIGH (no edit to `Finding`, `Severity`, FSM, `reviewers.py`, existing tests), INV-A, INV-B, INV-C (not engaged, since no key is added to a line or re-parsed), INV-D.
- Unmeasured: per-round cost (GQ-177, OQ-18).

What would change my mind: M3 nonzero, a second consumer needing the same per-finding key, or M2 showing reviewer-stated `in_diff` is more accurate than the hunk computation. Any of these moves the converter's keys toward the line format (the "adapter now, extensible v2 later" lean).

<!-- end section 5 -->

## 6. Shared-assumption responses A-001 to A-013 (Round 2)

| A-NNN | Response | One sentence |
|-------|----------|--------------|
| A-001 | ACCEPT | `SKILL.md:47-49` requires the main orchestrating session and forbids an Agent-tool subagent, so the panel pre-step is a main-session step. |
| A-002 | ACCEPT | Grep of `src/superclaude/pr_submit` for `cli.review`, `cli.reflect`, `findings_v2`, `cluster_v2` and `superclaude.cli` returns 0 matches, so the PR path has no ledger and neither package imports the other. |
| A-003 | ACCEPT | No PR panel profile exists: `check_finding` takes no category, severity or lens-set parameters (`findings_v2.py:84-90`), `LENSES` has no PR value (`:36`), and the core category set shares no value with the router's 18 (`findings.py:15-22`, `severity_router.py:34-53`); this is prerequisite work for both hybrids. |
| A-004 | REJECT | After conversion a `Finding` is also read for `in_diff` and `verification_status` (`fsm.py:902-906`), for `fix_key` over path, line and body (`models.py:196-207`) and for `comment_id` and `thread_id` in reply and resolve (`fsm.py:1064-1074, :1203-1205`). |
| A-005 | QUALIFY | Panel findings entering Wave 2-4 is the owner's wish only once decided; the first release is report-only and promotion waits on INV-J and the owner's answer (condition 1). |
| A-006 | REJECT (`changed` from ACCEPT) | A thread-less panel finding is not safe by default: the FSM passes the whole verified list to `do_reply` and `do_resolve` unfiltered (`fsm.py:1203-1205`), so the callbacks or prose must skip findings with no integer `comment_id` and the summary follows `thread-reply.md:92-99`. |
| A-007 | QUALIFY | `fix_key` is stable within one pre-step run only if `body` is the representative's claim verbatim (`models.py:196-207`, `cluster.py:294, 374`); it is not stable across a re-run after a push, which is why a result is bound to its head SHA. |
| A-008 | ACCEPT | A panel result is valid only for the head SHA it reviewed; the `panel` field carries that SHA, modelled on the bot gate's `expected_head` and `pushed_sha` binding (`SKILL.md:103-112`). |
| A-009 | ACCEPT | Per-round cost is unmeasured (GQ-177, OQ-18); both hybrids need M1 first, and once per PR head is the cheaper default. |
| A-010 | QUALIFY | `dedup_groups` merges only equal `(path, line or original_line)` and keeps every finding (`reviewers.py:430-440`); panel-internal duplicates are already merged by `cluster_v2` within 3 lines (`cluster.py:72, :161-181`), so only panel-versus-bot near-duplicates stay separate and each costs one verification. |
| A-011 | ACCEPT | Independence stays "requested, not served" until C-08 records `model_observed`; PR reports must not state served-model diversity. |
| A-012 | ACCEPT | `finding_from_comment` validates and does not map (it reads none of `citations`, `claim`, `blocking`, `severity`), so a mapper is needed in both hybrids and no second typed validator is written (`severity_router.py:61-119`). |
| A-013 | REJECT (`changed` from QUALIFY) | A completeness and quorum rule outside the ledger does not exist: 0 matches for `quorum` or `min(2` in `cli/review` and `pr_submit`, and the only evaluator, `evaluate_quorum` (`cli/reflect/fallback.py:161-179`), works on swarm `WorkerResult`s with a model-class diversity requirement; the strict rule "any requested reviewer not `complete`" replaces it and needs no helper. |

<!-- end section 6 -->

## 7. Updated per-point table (every point; `changed` marks a movement from my Round 1 table)

"Hybrid" here means the section 5 resolution (C10-R) unless the sentence says otherwise.

| Point | Superior approach (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence |
|-------|-----------------------------------------------|--------------|------------------------|
| S-001 | Hybrid (`changed` from A 60) | 65 | A's two-stage topology keeps the python gate and its one-fence pins untouched (`test_codex_reviews.py:687-688`), and B's SHA binding closes the staleness gap; panel findings join `decision["used"]` (`SKILL.md:175-178`) only after promotion. |
| S-002 | Hybrid (`changed` confidence from 75) | 85 | Both advocates now agree the axes separate: slot to A (sibling field), reader logic to B, converter owns the PR facts. |
| S-003 | A | 75 | C10-R edits no existing Python module and no existing test; it adds one module, new tests and two prose rows, while B's original edits `reviewers.py` (five functions) and three prose copies. |
| S-004 | Hybrid (`changed` confidence from 65) | 70 | Sibling field (A) with B's derivation of the value; it avoids the `merge_wait` guards at `reviewers.py:412` and `:420`. |
| S-005 | Neither (`changed` from B 55) | 50 | Document spine does not bear on correctness; B's decision-oriented layout surfaced open sub-decisions, A's is easier to implement from. |
| S-006 | B (`changed` confidence from 55) | 60 | A's "preserved by construction" overclaimed (X-001, W4); B's "endangered in a narrow sense" row was more accurate, though INV-E now holds with zero edits to `reviewers.py`. |
| S-007 | Hybrid (`changed` confidence from 65) | 70 | Keep U-001 on fixtures that hold source blocks plus B's T1, T3, T4, M1-M3; T0 only on promotion because no hybrid re-parses an extended line (item (a)). |
| S-008 | Hybrid (`changed` confidence from 55) | 60 | B's C-06 over-limit dependency (`findings_v2.py:111`) and my R-C03 INV-007 note both belong; the quorum helper I named is no longer needed. |
| S-009 | B | 60 | B's numbered tagged evidence table and "Limits" section are easier to audit than inline tags. |
| S-010 | B | 55 | B carried five further objections with OPEN marks; A's single objection plus concessions covered less. |
| C-001 | Hybrid (`changed` from A 70) | 75 | Cluster first (`cluster.py:72, :161-181`), one `Finding` per cluster, content from the representative, severity from the maximum over joined members. |
| C-002 | Hybrid | 60 | `in_diff` is harness-computed from `changed_ranges`, fail-closed when absent, with reviewer-stated values only compared (M2); no producer exists for the bots (`classifier.py:443-456` per diff-analysis) and `pr_submit` has no hunk parser. |
| C-003 | A (`changed` confidence from 70) | 65 | A new module avoids the zero-token rule on `severity_router.py` (`test_static_grep.py:48, :136-147`); cost is no automatic purity coverage until a new test is added. |
| C-004 | A (`changed` confidence from 65) | 85 | All five two-name functions stay untouched (`reviewers.py:47-78, :276, :395-424`), and B's own hybrid drops them. |
| C-005 | A (`changed` from Hybrid 60) | 70 | Both hybrids use one sibling `panel` field beside `reviewers` (`SKILL.md:271`), unpinned for either until a new test exists (X-004). |
| C-006 | Hybrid (`changed` confidence from 55) | 70 | B's strict rule computed as requested ids minus `complete_reviewers` (`cluster.py:414-418`); no quorum helper and no floor. |
| C-007 | Hybrid (`changed` from B 60) | 65 | B's head-SHA binding adopted; A's once-per-head cadence kept because per-round cost is unmeasured (`fsm.py:32-33` per diff-analysis). |
| C-008 | Neither | 65 | Still an owner decision (A-005); C10-R's default is report-only in the first release, with `terminal_augment_no_response` keyed to the bots because the panel is not in `merge_wait` (`reviewers.py:420`). |
| C-009 | A (`changed` confidence from 55) | 60 | An adapter-owned table reaches `critical`, `medium` and `low` without a fifth key and never lowers a CRITICAL; B's route-cost point (`severity_router.py:56-58`) becomes a table test, and category floors (`:34-53`) remain the router's. |
| C-010 | Hybrid (`changed` from A 65) | 75 | `confidence` unset: a `disputed`-derived "low" would lower a CRITICAL via `severity_router.py:173-175`, and three meanings already exist (`findings_v2.py:178-182`, `cluster.py:39-44`). |
| C-011 | Neither (`changed` from A 60) | 65 | Neither hybrid adds a key to the v2 line or re-parses an extended line, so the shared core takes only the decided FX-5 parameters. |
| C-012 | Neither (`changed` from A 55) | 60 | Both end in a slot-less `Finding` (`models.py:179-194`); `body` is the claim verbatim, and whether dropped fields matter is M3's question. |
| C-013 | Neither | 60 | `verify-citations` writes an advisory sidecar both designs can read (X-007); it does not separate them [UNVERIFIED: `verify_cmd.py` not re-read]. |
| C-014 | Hybrid (`changed` from A 55) | 60 | Parity test of the converter's output dict against `finding_from_comment` plus golden fixtures of cluster output and source records; the join key makes fixtures cheap (`cluster.py:356-358, :373`). |
| C-015 | A | 55 | Per-consumer converters match B's own admission that the `/task` gate uses none of the four PR keys; this is a prediction [UNVERIFIED]. |
| C-016 | A (`changed` confidence from 75) | 85 | `Finding.reviewer` defaults to `"augment"` when absent (`severity_router.py:118`), so code must always set `"panel"`; both advocates now agree. |
| X-001 | B (`changed` confidence from 85) | 90 | The cluster record has no severity or category (`cluster.py:352-378`); the repair is a `(reviewer_id, id)` join, with path and line already on the member (`:363`). |
| X-002 | B | 70 | `reviewer_activity` is a literal two-key dict not read from `REVIEWERS`, so A's pin claim holds only for a B that edits it; both are bound by the one-python-fence pins (item (d)). |
| X-003 | B | 95 | 47 `test_*.py` files in `tests/pr_submit`, not 50 [RELIED on Glob in diff-analysis and my R1]. |
| X-004 | Neither | 85 | No test pins the `reviewers` row (the contract-slicing test checks only the `merge_guard` row and heading order, `test_merge_guard_protocol.py:498-508` per B), so an added key or field is equally unpinned. |
| X-005 | Neither | 70 | B10 holds only for an A without a `panel` field; `terminal_clean` is set at eight sites in `fsm.py` and nobody has traced them. |
| X-006 | A | 70 | The bots have no producer of `in_diff` or `confidence` (`classifier.py:443-456` per diff-analysis); `auggie-reviewer.md:54-67` carries two of B's four keys [RELIED]. |
| X-007 | Neither | 75 | `Finding` has no slot for citation flags in either design (`models.py:179-194`), so both read the same sidecar. |
| X-008 | A (`changed` confidence from 60) | 70 | B conceded; with the panel excluded from re-triggers only the name-agnostic absent fold is reusable, and C10-R can emit it too. |
| X-009 | Hybrid (`changed` from A 60) | 70 | No review-kernel quorum rule exists (0 matches) and `evaluate_quorum` (`fallback.py:161-179`) is the wrong shape; the strict rule needs none. |
| X-010 | Neither | 65 | `pr_submit` has no hunk parser, so both designs need new diff-aware code; C10-R makes `changed_ranges` an explicit fail-closed input. |
| A-001 | Neither | 90 | Shared and verified at `SKILL.md:47-49`. |
| A-002 | Neither (`changed` confidence from 85) | 90 | `pr_submit` has zero imports of `cli.review`, `cli.reflect`, `findings_v2`, `cluster_v2` or `superclaude.cli` (Grep). |
| A-003 | Neither | 85 | Both need a PR profile and FX-5 parameters (`findings_v2.py:84-90`), and the category sets share no value (`findings.py:15-22`, `severity_router.py:34-53`). |
| A-004 | Neither | 70 | False for both: `in_diff`, `verification_status`, `fix_key` and comment ids are read (`fsm.py:902-906`, `models.py:196-207`). |
| A-005 | Neither | 75 | Both treat Wave 2-4 entry as given; which tier blocks is open (INV-J) and the first release is report-only. |
| A-006 | Neither | 80 | The FSM hands thread-less findings to the callbacks unfiltered (`fsm.py:1203-1205`); C10-R adds a callback-level skip and a summary-only rule on promotion (INV-K). |
| A-007 | Hybrid (`changed` from Neither 70) | 70 | `body` as the claim verbatim keeps `fix_key` stable within a run (`models.py:196-207`); a re-run after a push is a new identity by design. |
| A-008 | Hybrid (`changed` from B 60) | 70 | The `panel` field carries the reviewed SHA, as the bot gate does (`SKILL.md:103-112`); no automatic re-run in the first release. |
| A-009 | Neither | 90 | Cost is unmeasured for both (GQ-177); M1 serves both. |
| A-010 | Hybrid (`changed` from A 55) | 60 | Exact-line dedup is correct but costly (`reviewers.py:430-440`); running `cluster_v2` first bounds the cost for panel-internal duplicates. |
| A-011 | Neither | 90 | Carried from R-C03; identical in both. |
| A-012 | Neither | 85 | `finding_from_comment` is the shared validation seam (`severity_router.py:61-119`); the question is only who owns the mapper, and the answer is a converter module. |
| A-013 | Hybrid (`changed` from A 55) | 70 | The strict rule "any requested reviewer not `complete`" needs no quorum rule; none exists in `cli/review` or `pr_submit` (0 matches). |

Status: Complete
<!-- end of round2-advocate-A.md -->
