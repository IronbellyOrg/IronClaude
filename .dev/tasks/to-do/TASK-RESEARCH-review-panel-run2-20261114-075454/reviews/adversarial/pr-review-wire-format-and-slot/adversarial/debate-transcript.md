# Adversarial Debate Transcript

## Metadata
- Slot: C-10 (pr-review-wire-format-and-slot); Mode A, `--depth standard`, `--focus correctness,risk,test-coverage`, no `--merge`, no `--interactive`
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements; Round 2 sequential rebuttals A then B) plus Round 2.5 invariant probe (see `invariant-probe.md`); no Round 3 at standard depth
- Convergence achieved: see "Convergence Assessment" (label agreement 49 of 49 = 100%; content-adjusted 44 of 49 = 89.8%)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Variant A = `variant-1-original.md`, adapter now; Variant B = `variant-2-original.md`, one wire format and third reviewer name)
- Diff points: 49 (S 10, C 16, X 10, A 13); taxonomy levels L1 = 4, L2 = 30, L3 = 15 (all covered in both rounds)
- Shared-assumption omissions: none. Both advocates answered A-001..A-013 in Round 1 and Round 2 (`[OMISSION]` count 0)
- Round files: `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md` (full text below, unedited)

## Round 1: Advocate Statements

#### Variant A Advocate (Round 1)

Slot C-10 (pr-review-wire-format-and-slot), Round 1, standard depth. Focus: correctness, risk, test-coverage.
Code state: HEAD 50d4d2b9d. Everything below was read, not run. [CODE-VERIFIED] means I read that file:line myself in this session; [UNVERIFIED] means taken from a document and not re-read; [RELIED] means taken from `diff-analysis.md` (read, not re-checked by me).

## Position

Variant A is the safer and more testable way to enter the PR path: a new pure adapter module on the `pr_submit` side, fed by the panel's own cluster output, and a panel standing reported beside the bot `reviewers` object, with zero edits to any existing Python module in `pr_submit`. The conversion from a panel finding to a `Finding` is a rename-and-join in both designs (B concedes this in its own section 8), so the real choice is who owns the PR facts, and whether a local run is registered as a GitHub reviewer. I argue A, I concede that three of A's own claims are wrong as written (X-001, X-002/X-003, the "four fields" claim in A-004), and I would accept a hybrid that keeps A's topology and adopts B's SHA binding, status pin and measurements.

## Steelman of Variant B

The strongest version of B is not "add a third name". It is: the PR path already has one validated record shape, `finding_from_comment(raw)`, and its optional keys (`in_diff`, `confidence`, `original_line`, `reviewer`) are exactly B's four keys (`severity_router.py:67-118`, [CODE-VERIFIED]). The module's own docstring states the design intent: "One reviewer-agnostic path with a small per-reviewer adapter ... Everything after a normalized `Finding` is shared" (`reviewers.py:1-7`, [CODE-VERIFIED]). So B follows the grain of the existing code: a new reviewer is a small adapter inside the reviewer module, and the reader is a thin rename placed next to the function it feeds. B then makes five honest points that A cannot dismiss:

1. B's blast radius is smaller than A says. `reviewer_activity` is a literal two-key dict that does not read `REVIEWERS` (`reviewers.py:73-78`); B leaves it alone (B 3.2 a2). `merge_wait` has ten call sites that all pass two positional pairs (`test_marker_malformed.py:113,123,135`; `test_codex_reviews.py:319-382`), so an optional third parameter is source-compatible. `REVIEWERS` has no test reference, `reviewer_identities` and `list_review_threads` appear in no test, and `list_review_threads` has no caller in `src/` (grep, this session). No test pins the Output Contract `reviewers` row: the only contract-slicing test checks the `merge_guard` row and heading order (`test_merge_guard_protocol.py:498-508`). On the evidence, "B breaks pinned tests" is false for B as written (X-002).
2. B puts the panel's standing where operators already look, binds it to the head SHA it reviewed (A-008), and states the one guard a registry entry creates: a local reviewer that always answers must not make `terminal_augment_no_response` unreachable (`reviewers.py:420`, `SKILL.md:77,277`; B 3.2 item 3b, test T3).
3. B is lossless up to the conversion. A cluster record cannot supply severity or category (X-001, verified below), and `Finding` has no slot for citations, quote, role or lens (`models.py:179-194`), so any converter that picks one citation drops the rest; under B that choice is made once, in the one function that sees the whole line.
4. B names a severity cost A does not: a 3-token severity mapped onto five router tiers is lossy, and a MAJOR mapped to High takes the costlier `--depth deep --fix` route (`severity_router.py:56-58,122-133`; U-009).
5. B is honest about its open items (O3 bots-silent, O4 `fix_key` effect of appending `quote`, O5 `confidence` name), offers a deterministic fallback for `in_diff` (M2), and separates its wire-format evidence (B1-B8) from its slot evidence (B9, B10, B13). That separation invites exactly the split decision I propose in the hybrid.

## Key strengths claimed for Variant A

1. **Zero edits to existing `pr_submit` Python.** A touches no function in `reviewers.py`, `severity_router.py`, `fsm.py`, `models.py`; the snapshot-gate block (`SKILL.md:97-153`) stays the one executable python block the `_skill_gate` test requires (`test_codex_reviews.py:685-697`, `assert len(blocks) == 1`). B edits `severity_router.py` (adds `finding_from_v2`; that file is on the core-purity list, `test_static_grep.py:48`), `reviewers.py` (`REVIEWERS`, `reviewer_identities`, `list_review_threads`, `merge_wait`), `SKILL.md:271,277` and `commands/pr-submit.md:60`. A edits only `SKILL.md` prose plus one new Output Contract row. [CODE-VERIFIED for the files and lines named.]
2. **A third `REVIEWERS` name is a registry entry that every consumer must carve out.** `reviewers.py:1-7` defines a reviewer by four GitHub facts: author identity, completion proof, severity reading, re-review comment. The panel has none of them. B's own 3.2 item 3 needs: an empty-identity branch in `reviewer_identities` (colliding with the docstring rule "an empty identity set disables that reviewer", `reviewers.py:6-7`), a skip in `list_review_threads`, exclusion from `retrigger_phrase` and `reviewer_activity`, an optional `merge_wait` parameter, and a `no_response` guard keyed to two of three names (`reviewers.py:420`). After those carve-outs the registered name does almost nothing. And because `reviewer_identities` and `list_review_threads` appear in no test, those carve-outs would be new branches no existing test exercises, so a wrong carve-out is not caught by anything already in the repo.
3. **Clustering, the panel's multi-reviewer value, exists only in A's path.** `dedup_groups` groups by exact `(path, line or original_line)` and "every finding is kept" (`reviewers.py:430-440`). `cluster_v2` joins findings within `SPAN_TOLERANCE = 3` lines with intersecting `refs_norm` and yields `blocking_any`, `disputed`, `support` per cluster (`cluster.py:72,161-181,323-378`). Under B, panel reviewers citing lines 40, 41 and 42 become three `Finding`s, three verifications and three troubleshoot dispatches for one defect; B never says whether `cluster_v2` runs first (C-001). If B does run it, B imports the kernel's clustering into the PR flow and the remaining difference is only B's four line keys and the third name, which is the shape of A. [CODE-VERIFIED.]
4. **No model-asserted provenance or types reach the router.** B makes `reviewer`, `in_diff`, `confidence`, `original_line` reviewer-emitted line keys that the core never validates (`check_finding` never iterates unknown keys and rejects only `calibrated_confidence`, `findings_v2.py:96-97`). They are first validated deep in `finding_from_comment`, which raises `ValueError` on a non-bool `in_diff` or a non-text `reviewer` (`severity_router.py:74-82`). The bot gate turns any such `ValueError` into `review_state = "polling"` and drops every finding of that reviewer's batch (`SKILL.md:118-124`, same pattern at `:143-149`). If B copies that pattern, one string-typed `in_diff` from one model line silently discards the whole panel batch; if it does not, B must specify per-line handling it has not. Separately, `reviewer` is accepted as any text (`severity_router.py:118`) and `pending_retriggers` and the `absent_reviewers` fold key on that string (`reviewers.py:450-457`), so a model writing `"reviewer": "augment"` would enter the bot bookkeeping. Under A the adapter writes `reviewer = "panel"` as a constant and computes `in_diff`/`original_line` from the diff, so no model-typed field reaches the validator. [CODE-VERIFIED; the B-side consequence is an inference from B 3.2.1-2, not B's text.]
5. **A does not entangle panel standing with the bot status enum.** `terminal_augment_no_response` means "no configured reviewer (Augment, Codex) responded" (`SKILL.md:77,277`). A's sibling field leaves that meaning untouched by construction; B must pin it with a new test (T3) and still leaves "bots silent, panel has findings" OPEN (O3). B's presence value is also set by the same main session ("ran on this head SHA", B 3.2 a2), so a registered name adds no mechanical proof over A's sibling field (X-005): both are a prose rule plus one contract field.
6. **Staged rollout.** Because the adapter is a separate module, the PR panel can ship report-only first (findings listed, not dispatched) and be promoted without touching the reviewer registry or the gate. Under B the status object, `merge_wait` signature and prose copies change on day one.
7. **One experiment separates the designs on information, not ownership** (U-001, A section 6.3): run the same fixtures through A's adapter and a scratch B-style reader and compare `path`, `line`, `remapped_severity`, `route`, `seed_troubleshoot` output. If equal, B's extra keys carry nothing A lacks. This is cheap and offline, and it tells the owner whether to promote keys later (the research/13 lean "adapter now, extensible v2 later").
8. **Fail-closed groundability is shared and clean.** `is_groundable` drops an empty path or non-positive integer line (`fsm.py:364-372`, [CODE-VERIFIED]); the adapter never invents an anchor for a citation-less or unresolved cluster. Measurable by A section 6.5.

## Weaknesses identified in Variant B

1. **No stated clustering step (C-001).** B converts one v2 line to one `Finding`, so duplicates meet only in `dedup_groups`, which needs exact `(path, line)` equality (`reviewers.py:430-440`). The cluster-level facts `support`, `disputed`, `blocking_any` (`cluster.py:337-351,375-377`) never reach `pr_submit`. B's "no import of kernel code" claim (B14) and "no clustering" cannot both hold if the panel has more than one reviewer.
2. **Four unvalidated model-emitted keys on a line format shared with reflect.** The core accepts them silently (`findings_v2.py:96-97`); the first check is the PR-side `ValueError` (`severity_router.py:74-82`), and the bot-gate pattern converts that into dropping the batch (`SKILL.md:118-124`). B's M2 admits reviewer-emitted `in_diff` may be imprecise and falls back to computing it from hunks, which is A's design adopted inside B.
3. **Model-asserted `reviewer` provenance.** B 3.2.1-2 reads `reviewer` from the line with `default_reviewer = panel`. `finding_from_comment` accepts any text (`severity_router.py:118`), and re-trigger and absent bookkeeping key on that string (`reviewers.py:450-457`). Provenance should be a constant set by the code that ran the panel, not a field the model writes.
4. **The registry choice creates a hazard B then has to fence.** `terminal_augment_no_response` becoming unreachable (U-008, `reviewers.py:420`) exists only because the panel is put in the pair set; B's fix (keep `no_response` keyed to two of three names) is a special case inside a function whose docstring says it merges "per-reviewer `(wait_outcome, gate_state)` pairs" (`reviewers.py:395-401`). The carve-outs listed in strength 2 are untested new branches.
5. **B10 is not a weakness of A once A carries its sibling field (X-005).** B's argument that a failing separate pre-step "leaves no entry" is true only for an A without the `panel` field; A's section 2 and section 8 include one. B's standing is also set by the same main session, so it adds no mechanical proof.
6. **B1/B8 "lossless" is an unmeasured benefit with a measured cost.** What later waves read is `path`, `line`, `body`, `category`, route (`fsm.py:446-453`), plus `in_diff`, `verification_status` (`fsm.py:905-907`) and `fix_key` (`models.py:196-207`). Nothing reads `quote`, a second citation or role. B's own M3 asks whether any later step uses them, and O4 shows appending `quote` to `body` would change `fix_key`. Until M3 returns a nonzero count, "lossless" has no demonstrated consumer.
7. **B's evidence B4 is partly contradicted (X-006).** `auggie-reviewer` emits `in_diff` and `confidence` (and `file`, not `path`; no `body`, no `original_line`, no `reviewer`) (`auggie-reviewer.md:54-67`, [CODE-VERIFIED]), so two of the four keys, not "the same fields".
8. **B places a kernel-format parser inside a file on the purity list** (`severity_router.py`, `test_static_grep.py:48`). Any later change to the v2 line (the C-06 repair policy, C-01 convergence triggers) now lands inside the router module that the FSM and 47 test files lean on; under A it lands in one new adapter.
9. **Open sub-decisions on the critical path.** C-008 (bots silent, panel findings: remediate, report or wait) is OPEN in B and entangled with the bot-keyed status; severity (O6) and `confidence` meaning (O5) are open. A has the same open items but they sit behind an adapter, not in the registry and Output Contract that operators read.

## Concessions

1. **X-001, the cluster record does not hold severity or category.** [CODE-VERIFIED] Cluster keys are `cluster_id, members, member_scores, reviewers, chained, uncalibrated, support, representative, claim, blocking_any, blocking_all, disputed` (`cluster.py:352-378`); member keys are `reviewer_id, ordinal, id, blocking, deviation_class, finding_confidence, refs_norm, primary_citation, fp` (`:354-367`). A section 2 ("the highest member severity") and section 3.5 are wrong as written. The repair is cheap and stays inside A: members and `representative` carry `(reviewer_id, id)` (`cluster.py:356-358,373`), and the pre-step already holds the `reviewer_records` it passed to `cluster_v2` (`cluster.py:3-4`, a record is `(reviewer_id, ordinal, block, calibration_map)`), so the adapter's input becomes (cluster output, the same reviewer records, the diff text, the PR profile). Still plain JSON, still no import from `cli/review`. But A's claim "cluster output already holds what the adapter reads" is withdrawn, and the equivalence fixtures (U-001) must carry source blocks.
2. **X-002 and X-003, A's pin and file-count claims.** B as written does not touch `reviewer_activity` or the gate block, so A's "`test_codex_reviews.py:285-295, :705` break" holds only for a B that B does not propose. The file count is 47 `test_*.py`, not 50 (Glob this session lists 47). A's strongest B-side argument is therefore semantic (strength 2: carve-outs and the untested branches), not "B breaks tests". I also concede that two of the five touched functions are effectively dead or untested (`list_review_threads` has no caller in `src/`; `reviewer_identities` and `list_review_threads` have no test), which lowers B's cost and also its regression exposure.
3. **A-004 / "downstream reads only four fields".** A section 8 is wrong. Also read: `in_diff` and `verification_status` (`fsm.py:905-907`), `fix_key` over path, line, body (`models.py:196-207`), and `comment_id`/`thread_id` for reply and resolve (`fsm.py:1064-1074`, `refs/thread-reply.md:16-17`). The four-field claim is true only for `seed_troubleshoot` (`fsm.py:446-453`).
4. **X-009 / A-013, the quorum helper does not exist.** [CODE-VERIFIED] a count of `quorum|min\(2` over `src/superclaude/cli/review` returns 0. A's `incomplete` derivation needs new code. The minimum honest rule uses only fields `cluster_v2` returns (`complete_reviewers`, `invalid_reviewers`, `valid_blocks`, `cluster.py:414-418`): `incomplete` when `invalid_reviewers` is non-empty or `valid_blocks` is below the dispatched count; a PR floor `min(2, requested)` is the R-C03 value and is an unmeasured parameter.
5. **X-010 / C-002, the pre-step's diff.** `pr_submit` has no hunk parser (the only `@@` text is fix-hunk text at `fsm.py:395-429`); the poll payload has no diff keys (`classifier.py:443-456`). "Computed from the diff the pre-step already holds" is [UNVERIFIED]: the panel needs the diff as input, but how the main session retains it, and a small `@@ -a,b +c,d @@` parser, are new code in A's adapter. A must also say that the computation yields `in_diff` for lines in a hunk and `original_line` only when it can be derived.
6. **Unspecified in A:** (a) the injection point where adapter `Finding`s join the list the FSM receives after `merge_wait` (the gate yields `decision["used"]` findings, `SKILL.md:175-177`); (b) SHA binding and staleness after a fix push (A-008, A section 4 last bullet only says "needs a cycle id"); (c) the bots-silent case (C-008); (d) reply and resolve for a thread-less finding (A-006): `fsm.py:1064` treats a batch with no integer `comment_id` as fallback-only and `refs/thread-reply.md:16-17` assumes a bot thread root, and a mixed batch calls `do_resolve(findings=verified)` with no rule for panel members.
7. **Internal inconsistency in A section 6.** 6.1 says no existing test file is edited; 6.2 says "add the module to the static no-shell-token check", which is an edit to the module list in `test_static_grep.py:40-55` (that list names files; only the anthropic-import test globs, per C-003). Resolution: write a new test file for the adapter's purity instead and keep 6.1 true.
8. **Weaker single reporting surface.** A's panel standing sits in a sibling field, not inside `reviewers`; an operator reads two places. Accepted as a cost.
9. **Information loss is real and unmeasured.** A cluster collapses to one `Finding`; the second citation, role, lens and supporting-reviewer count are dropped or placed in `body` text. M3 would measure whether that matters.
10. **U-008, U-009, U-010, U-011, U-013 are genuine B contributions** that A lacked: the `no_response` guard, severity route-cost, `ROLES` already has `diff`/`source` (`findings_v2.py:35`), M3, and O4.

## Shared-assumption responses

| A-NNN | Response | One sentence |
|-------|----------|--------------|
| A-001 | ACCEPT | `SKILL.md:47-49` says the skill "MUST run in the main orchestrating session" and not in an Agent-tool subagent, so the pre-step is a main-session step. |
| A-002 | ACCEPT | A grep of `src/superclaude/pr_submit` for `cli.review`, `cluster_v2` and `findings_v2` returns 0 matches, so no ledger is needed or wanted on the PR path. |
| A-003 | ACCEPT | No PR panel profile exists (`findings_v2.py:36` `LENSES` has no PR value; `check_finding` at `:84-90` takes no category, severity or lens-set parameters), and A needs the same FX-5 parameterisation B does; this is prerequisite work for both. |
| A-004 | REJECT | A's own "downstream reads only path, line, body, category and route" is false: `in_diff`/`verification_status` (`fsm.py:905-907`), `fix_key` (`models.py:196-207`) and `comment_id`/`thread_id` (`fsm.py:1064`) are read too. |
| A-005 | QUALIFY | Panel findings entering Wave 2-4 is the owner's wish, but which tier blocks is open (INV-J) and A's separate module lets the first release be report-only before any push is authorised. |
| A-006 | ACCEPT | A panel finding has no thread, comment id or review id, and `fsm.py:1064-1074` plus `refs/thread-reply.md:16-17` give no rule for a mixed batch; A should say panel findings are reported in the single summary thread and never replied or resolved inline. |
| A-007 | QUALIFY | `fix_key` hashes path, line and body (`models.py:196-207`); the body is the cluster representative's text, stable within one pre-step run (which is what idempotency in one PR run needs) but not across re-runs after a push. |
| A-008 | ACCEPT | A result is valid only for the head SHA it reviewed; A needs a `panel_head_sha` carried with the standing and treated as stale after any fix push, which B states and A does not. |
| A-009 | ACCEPT | Per-round cost is unmeasured (GQ-177); both designs need M1 before the panel runs per round, and A's optional per-PR cadence is the cheaper default. |
| A-010 | QUALIFY | Exact `(path, line)` equality is the only cross-source dedup (`reviewers.py:430-440`), but under A the panel's own reviewers are already clustered within 3 lines (`cluster.py:72`), so only panel-versus-bot duplicates remain exact-only. |
| A-011 | ACCEPT | Independence stays "requested, not served" until C-08 records `model_observed`, and the PR report must not state served-model diversity. |
| A-012 | ACCEPT | `finding_from_comment` (`severity_router.py:61-119`) is the single validation seam and reads none of `citations`, `claim`, `blocking`, `severity`, so a mapper is needed under both designs. |
| A-013 | QUALIFY | No quorum or `min(2` exists in `cli/review` (count 0, verified), so A's "never clean" rule needs new code, but only over fields `cluster_v2` already returns (`cluster.py:414-418`); B's reliance on "a C-03 quorum refusal" is the same new code and B says it does not call `merge_round`. |

## Invariants

| Invariant | Does A keep it | Evidence and residual risk |
|-----------|----------------|-----------------------------|
| INV-E (HIGH): `Finding`, `Severity`, FSM, fork-only checks, no `gh`/`git` in the core | Yes | `models.py:168-194`, `fsm.py`, `pr_target_ok`/`origin_ok` are not edited; the adapter is a new pure module over dicts with no shell tokens. Residual: `test_static_grep.py:40-55` lists files by name, so the new module is unguarded until a new test (not an edit to that list) checks it. A edits `SKILL.md` prose and one Output Contract row; B additionally edits `severity_router.py`, `reviewers.py` and `commands/pr-submit.md`. B keeps INV-E too in its own words ("endangered in a narrow sense"). |
| INV-F (MEDIUM): no `src/superclaude/` path in installed primitives | Yes, conditionally | The pre-step prose must call package code as `from superclaude.pr_submit import ...` (the `SKILL.md:98` pattern) and the panel through the `superclaude` CLI or package import, never a source path. [UNVERIFIED] until the prose exists: run `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify each hit. B has the same condition. |
| INV-C (MEDIUM): findings-v1 grammar and `review merge` unchanged; unknown keys accepted | Yes | A adds no key to any line format, edits no parser, and the adapter reads named keys and ignores the rest. B relies on unknown keys staying open (`findings_v2.py:96-97`), so B depends on a property that C-01 kept but never pinned by a test for these four names. |
| INV-A: reflect contract 1.8.0 byte-identical | Yes | No edit under `cli/reflect`; the shared `check_finding` parameterisation (A-003) is needed by both, with defaults equal to today's constants. |
| INV-B: 36-test verdict matrix | Yes | The PR flow never calls `derive_verdict`; the panel verdict is not consumed (findings enter, not the verdict). |
| INV-I: absent or incomplete panel is never clean | Yes, by a new test | Tri-state `present / absent / incomplete` in a sibling field, derived from `invalid_reviewers` and `valid_blocks` (`cluster.py:414-418`), never mapped to "no findings". How `terminal_clean` interacts with an incomplete panel is not traced by anyone (X-005, [UNVERIFIED]); A section 6.7's three-output test would pin it. |

## Per-point positions

| Point | Superior approach per me (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence |
|-------|-------------------------------------------------------|--------------|------------------------|
| S-001 | A | 60 | Two stages keep the bot gate (`SKILL.md:97-153`) and its single-python-block test (`test_codex_reviews.py:688`) untouched, but A leaves the injection point unspecified (Concession 6a). |
| S-002 | Hybrid | 75 | The axes are separable: adapter plus sibling field with no `REVIEWERS` entry, and B itself says its wire and slot evidence "can be weighed separately" (B section 8 point 3). |
| S-003 | A | 75 | A edits zero existing Python modules; B edits `severity_router.py`, `reviewers.py` and two prose files (B 3.2 items 1, 3, 4). |
| S-004 | Hybrid | 65 | A's sibling field keeps the `reviewers` object bot-only, and B's derivation from `COMPLETION_STATES` (`findings_v2.py:40`) plus SHA binding is the better source for the value. |
| S-005 | B | 55 | B's decision-oriented layout surfaces open sub-decisions (severity, `confidence`) that A buries in prose. |
| S-006 | B | 55 | A's "preserved by construction" overclaims given X-001 and X-002, while B's "endangered in a narrow sense" row is more accurate. |
| S-007 | Hybrid | 65 | A's equivalence test (U-001) separates information from ownership, and B's T3 status pin and M3 count are tests A should adopt. |
| S-008 | Hybrid | 55 | A names the missing quorum helper (`cluster.py:414-418`, none in `cli/review`) and B names the C-06 over-limit dependency (`findings_v2.py:111`); both belong. |
| S-009 | B | 60 | B's numbered, tagged evidence table with a closing "Limits" section is easier to audit than A's inline tags. |
| S-010 | B | 55 | B carries five further objections with OPEN statuses; A's single objection plus a concession list is thinner. |
| C-001 | A | 70 | `dedup_groups` needs exact `(path, line)` (`reviewers.py:430-440`) while `cluster_v2` joins spans within 3 lines (`cluster.py:72,161-181`), and B never says clustering runs. |
| C-002 | Hybrid | 55 | The adapter should compute `in_diff` from hunks (needs a new parser, X-010) and reviewer-stated values should only be compared against it (B M2), since no producer exists today (`classifier.py:443-456`). |
| C-003 | A | 70 | A new module isolates a kernel-format parser from `severity_router.py`, which is on the purity list (`test_static_grep.py:48`); A must add a new purity test (Concession 7). |
| C-004 | A | 65 | A avoids five carve-outs (`reviewers.py:47-78,276,395-424`), though two of those functions are dead or untested, which lowers B's cost (Concession 2). |
| C-005 | Hybrid | 60 | Either new row or key is unpinned (X-004), and a sibling field keeps `reviewers` meaning "the bots" while B's wording convergence across `SKILL.md:271,277` and `commands/pr-submit.md:60` is a real maintenance cost. |
| C-006 | Hybrid | 55 | Both derive standing from the same inputs (`COMPLETION_STATES`, `invalid_reviewers`, `valid_blocks`) and both need a quorum helper that does not exist (count 0 in `cli/review`). |
| C-007 | B | 60 | B binds presence to the head SHA and the round cap (`fsm.py:32-33`); A's optional per-PR cadence leaves staleness unspecified (A-008). |
| C-008 | Neither | 65 | Bots silent with panel findings is open in B (O3) and unaddressed in A, and the 'Wave 8 wait-only' branch (`SKILL.md:77`) is where it must be decided. |
| C-009 | A | 55 | An adapter-owned table can split MAJOR by `blocking` and reach all five tiers without a fifth key, but B's route-cost warning (`severity_router.py:56-58`) must become a test. |
| C-010 | A | 65 | Setting `confidence` from cluster facts avoids a fourth meaning beside `self_confidence` (`findings_v2.py:178-182`), the calibrated value (`cluster.py:79-83`) and the router text (`severity_router.py:174`). |
| C-011 | A | 60 | A adds no key to the shared line; B's four keys ride unvalidated by the core (`findings_v2.py:96-97`). |
| C-012 | A | 55 | The lossless benefit has no measured consumer (nothing reads `quote` or a second citation, `fsm.py:446-453`), and B's O4 shows `quote` in `body` changes `fix_key` (`models.py:196-207`). |
| C-013 | Neither | 60 | The citation precheck writes a sidecar both designs can read (`verify_cmd.py:76-113` per X-007), so it does not separate them. |
| C-014 | A | 55 | Golden cluster fixtures pin both ends, and B's T1 parity test only proves a rename, but A's fixtures must now include source blocks (Concession 1). |
| C-015 | A | 55 | Per-consumer adapters match B's own admission that the `/task` gate does not use the four PR keys, but this is a prediction, [UNVERIFIED]. |
| C-016 | A | 75 | A sets `reviewer = "panel"` as a constant; B reads it from a model-written line key, and `finding_from_comment` accepts any text (`severity_router.py:118`). |
| X-001 | B | 85 | Cluster and member keys hold no severity or category (`cluster.py:352-378`), so A's adapter needs the source records (repairable by a `(reviewer_id, id)` join, `cluster.py:356-358,373`). |
| X-002 | B | 70 | `reviewer_activity` is a literal dict not read from `REVIEWERS` (`reviewers.py:73-78`) and B excludes the panel from it, so B as written does not break `test_codex_reviews.py:285-295,705`. |
| X-003 | B | 95 | Glob lists 47 `test_*.py` files in `tests/pr_submit`, not 50. |
| X-004 | Neither | 85 | No test pins the `reviewers` row (`test_merge_guard_protocol.py:498-508` slices only the `merge_guard` row), so an added key or an added field is equally unpinned. |
| X-005 | Neither | 70 | B10 holds only for an A without the `panel` field, and the panel's presence is main-session-asserted under both. |
| X-006 | A | 70 | The bots have no producer of `in_diff` or `confidence` (`classifier.py:443-456`), and `auggie-reviewer.md:54-67` carries only two of B's four keys (and `file`, not `path`). |
| X-007 | Neither | 75 | `Finding` has no field for citation flags in either design (`models.py:179-194`), so both read the sidecar. |
| X-008 | A | 60 | B9's "reuse the bookkeeping" conflicts with B 3.2 a2 excluding the panel from re-triggers; only the name-agnostic absent fold is reusable, and A can emit `reviewer_absent{reviewer: "panel"}` too (`reviewers.py:443-457`). |
| X-009 | A | 60 | A names the quorum helper as new work, while B depends on "a C-03 quorum refusal" it says it does not call. |
| X-010 | Neither | 65 | `pr_submit` has no hunk parser (A's adapter needs one) and B's reviewer-stated `in_diff` is unverified (M2), so both need new diff-aware code. |
| A-001 | Neither | 90 | Shared and verified at `SKILL.md:47-49`. |
| A-002 | Neither | 85 | Shared; grep of `pr_submit` for `cli.review` returns 0, so neither package imports the other. |
| A-003 | Neither | 85 | Both need a PR profile and FX-5 parameters on `check_finding` (`findings_v2.py:84-90`). |
| A-004 | Neither | 70 | The assumption is false for both: in_diff, verification_status, fix_key and comment ids are read (`fsm.py:905-907`, `models.py:196-207`, `fsm.py:1064`). |
| A-005 | Neither | 75 | Both treat Wave 2-4 entry as given, and which tier blocks is open (INV-J). |
| A-006 | Neither | 80 | The thread-less reply and resolve rule is missing in both (`fsm.py:1064-1074`, `refs/thread-reply.md:16-17`). |
| A-007 | Neither | 70 | `fix_key` over path, line, body (`models.py:196-207`) is as stable as one run of the pre-step under both. |
| A-008 | B | 60 | B states head-SHA binding (B 3.2 a2); A only mentions a cycle id. |
| A-009 | Neither | 90 | Cost is unmeasured for both (GQ-177). |
| A-010 | A | 55 | Panel-internal duplicates are removed by A's clustering within 3 lines, while panel-versus-bot dedup stays exact-only in both (`reviewers.py:430-440`). |
| A-011 | Neither | 90 | Carried from R-C03, identical in both. |
| A-012 | Neither | 85 | `finding_from_comment` is the shared seam (`severity_router.py:61-119`), so the question is only who owns the mapper. |
| A-013 | A | 55 | A names the quorum rule as new work over existing fields, and B relies on a refusal that is not in code (count 0 in `cli/review`). |

## Hybrid I would accept ("A-prime")

Keep A's topology and ownership, take B's guards and measurements, and leave promotion of the four keys to a trigger.

1. **From A, kept:** the panel runs as a main-session pre-step; a new pure adapter module on the `pr_submit` side; `reviewer = "panel"` set as a constant; no third `REVIEWERS` name, no `merge_wait` change, no edit to the gate block; the panel standing is a sibling Output Contract field, not a key inside `reviewers`.
2. **Fixed from X-001:** adapter input is (cluster output, the same reviewer records passed to `cluster_v2`, the diff text, the PR profile), joined on `(reviewer_id, id)`.
3. **Adopted from B:** the standing is derived from `COMPLETION_STATES` and `cluster_v2`'s `invalid_reviewers` and `valid_blocks`, carries a `panel_head_sha` and is stale after any fix push (A-008); the T3 pin that `terminal_augment_no_response` stays keyed to the two bots; B's M2 (compare reviewer-stated `in_diff` with hunk-computed) and M3 (count later-wave use of `quote`, second citation, `blocking`); the severity route-cost warning (U-009) as an adapter-table test; `ROLES` already has `diff` and `source` (U-010).
4. **Tests, new files only:** adapter conformance fixtures (with source blocks), adapter purity (new test, not an edit to `test_static_grep.py`), the three-output standing test, and the U-001 equivalence run.
5. **Promotion trigger ("adapter now, extensible v2 later"):** promote the four keys to the line format if M3 is nonzero, or a second consumer needs the same per-finding keys, or M2 shows reviewer-stated `in_diff` is more accurate than the hunk computation. Until then they stay in the adapter.
6. **Still open and owned by neither design alone:** C-008 (bots silent, panel findings), A-006 (thread-less reply and resolve; I propose summary-thread-only reporting), and the unmeasured per-round cost (M1).

I would not accept a third `REVIEWERS` name or four model-emitted line keys before the U-001 and M3 results exist.

#### Variant B Advocate (Round 1)

Slot C-10 (pr-review-wire-format-and-slot), conflicts CO-27 and CO-29. Code state: HEAD 50d4d2b9d. Nothing was run; [CODE-VERIFIED] means read at that file:line in this session, [UNVERIFIED] means carried from a document or not re-read. Paths are relative to the repository root. Cites nothing from the run-1 task folder or the run-1 queued file.

## Position

B is right on the wire-format axis in a narrow form: `pr_submit` should read the findings-v2 line itself through one pure reader next to `finding_from_comment`, because the cluster record cannot supply severity or category, so A's "pure adapter over a cluster record" is not what A says it is. B is wrong on the slot axis: a third name in `REVIEWERS` costs five edited functions and three prose copies and buys almost nothing that A's sibling `panel` field does not, so I concede that axis to A. The hybrid I would accept is B's reader on A's slot (section "Hybrid I would accept").

## Steelman of Variant A

The strongest A is not "adapters are tidier". It is a statement about what the bot machinery means. The bots are external actors observed through GitHub: identities, completion markers, silence deadlines, re-trigger phrases (`reviewers.py:47-72`, `:322-424`). The panel is a local run that is complete when a merge returns. A refuses to squeeze the second kind into the first kind's plumbing, and the code supports that refusal on every point it checks:

1. `reviewer_identities` and `retrigger_phrase` raise `ValueError("unknown reviewer")` for any third name (`reviewers.py:47-60`, `:63-70`) [CODE-VERIFIED]. `reviewer_activity` is a literal two-key dict (`:73-78`). `merge_wait(augment, codex)` takes two positional pairs and decides `no_response` as `len(absent) == len(pairs)` (`:395-424`, `:420`), and any pending pair returns `polling` early (`:412`) [CODE-VERIFIED]. A third pair therefore needs two guards, not one.
2. The tests pin the two-name shape: `test_codex_reviews.py:285-295` and `:705` compare `reviewer_activity` by equality to `{"augment", "codex"}` dicts, and `_skill_gate` asserts exactly one ```python block in `SKILL.md` (`:688`) [CODE-VERIFIED]. Under A none of this is touched.
3. A sees something B did not state: the router's steps 3 (`confidence == "low"`) and 4 (`in_diff is False`) are dormant for both bots, because the bot roots carry neither key (`severity_router.py:174`, `:178`; `refs/severity-routing.md:45`: "Category/confidence are not inferred from prose") [CODE-VERIFIED]. The panel would be the first producer, and the honest question is who should produce them.
4. A's answer to that question is the better one in principle: facts the harness can compute (`in_diff`, `original_line`, `reviewer`) should be computed by the harness, not asserted by a model on every line. A also restates the CRITICAL-never-lowered row in the adapter because the `merge_round` floor is off the PR path (U-004), and names the quorum helper as new work (U-003) where B hides it.
5. A is candid: it lists INV-G, INV-J, the unpinned prose guard and the unmeasured cost as open, and concedes weakness on a single reporting surface (A section 8).

In its best form A says: keep the bot machinery bot-only, make the panel a producer of the dicts `finding_from_comment` already accepts, compute PR-local facts where the diff is known, and report panel standing in a sibling field. I accept most of that. My disagreement is about what the adapter reads and about two claims A makes that the code does not support.

## Key strengths claimed

1. A cluster record cannot feed the adapter A describes. `cluster_v2` records carry `cluster_id, members, member_scores, reviewers, chained, uncalibrated, support, representative, claim, blocking_any, blocking_all, disputed` (`cluster.py:352-378`); each member carries `reviewer_id, ordinal, id, blocking, deviation_class, finding_confidence, refs_norm, primary_citation, fp` (`:354-365`), and `_members` adds only `claim`, `blocking` and the confidence (`:288-297`) [CODE-VERIFIED]. There is no `severity` and no `category` anywhere. `remap_severity` starts from `severity_hint` and clamps by `category` (`severity_router.py:161-171`) [CODE-VERIFIED]. So A's "highest member severity" (A section 2) and "cluster output already holds what the adapter reads" (A section 3.5) are false for the two fields the router needs most (X-001). A's adapter must read the source v2 lines as well. Once it does, it is the reader B proposes, wrapped in an extra module and an extra fixture set.
2. The clean way to keep clustering and keep the line is the key the cluster already holds: `representative: {reviewer_id, id}` (`cluster.py:373`) [CODE-VERIFIED] names the source line. Cluster for selection and support, line for content. B did not say this (concession 6), but it is B's reader plus A's grouping, not a third design.
3. The reader is a rename over a validator that already exists. `finding_from_comment` reads and validates exactly `path, line, body, severity_hint, category, confidence, in_diff, original_line, reviewer` and raises `ValueError` otherwise (`severity_router.py:67-118`) [CODE-VERIFIED]. B's parity test T1 (B section 6) asserts `finding_from_v2(line) == finding_from_comment(hand-written raw)` field by field. It is small and falsifiable, and it fails the moment the reader needs logic beyond renaming. A's equivalent is golden cluster fixtures that, per X-001, must also hold the source blocks.
4. The coupling A calls an advantage is the same coupling. A section 1 says "`pr_submit` knows the adapter's input shape, the core knows nothing about `pr_submit`". Under B `pr_submit` knows a text line format and imports no kernel code (B14). In both designs `pr_submit` learns a kernel-side shape and the kernel learns nothing of `pr_submit`. `pr_submit/` has no `panel` or `cli/review` reference today (grep: 0 matches) [CODE-VERIFIED], so both designs create the first awareness.
5. B binds the panel result to a head SHA and to the round cap (B section 3.2 a2; `DEFAULT_MAX_ROUNDS = 2`, `HARD_CAP_MAX_ROUNDS = 5`, `fsm.py:32-33` per diff-analysis C-007, not re-read by me). A leaves a re-run "needing a cycle id" and says nothing about staleness (A section 4, last bullet; A-008). A panel result for the wrong head is a correctness risk A leaves open.
6. B found and pinned a real hazard that A avoids only by omission: a local, always-answering third pair would make `terminal_augment_no_response` unreachable (`reviewers.py:420`; `SKILL.md:277` "no configured reviewer (Augment, Codex) responded") [CODE-VERIFIED]. B's T3 writes the expected outcome down before the code. The test is valuable under any design that touches `merge_wait`, and its absence under A is a gap in A's test list.
7. B's test structure is closer to decision-grade: T1 to T4 are offline, M1 (cost per round) is the measurement both positions need, M3 counts whether `quote`, a second citation or `blocking` was ever used downstream (U-011) and so can falsify B's own "lossless" argument. A has one comparable experiment (U-001, A section 6.3) which I would keep.
8. B corrects the census: `tests/pr_submit` holds 47 `test_*.py` files, not 50 (X-003, diff-analysis [CODE-VERIFIED] by Glob), and it names the one test that slices the Output Contract (`test_merge_guard_protocol.py:498-508`, X-004). Both variants then know an added Output Contract key is unpinned.

## Weaknesses identified in Variant A

1. A section 3.5 claim fails against code (X-001, strength 1). The consequence is not cosmetic: the adapter is no longer "a pure mapper over a record the core already emits". It needs source blocks or a `cluster.py` edit, and A section 2 promises no edit to `cluster.py`.
2. A applies the confidence collision it criticises. A section 3.4 says a fourth `confidence` meaning on the v2 line "would need a type and a meaning chosen". A section 2 has the adapter set `confidence` "from cluster facts (for example `disputed`)". That is a fourth meaning of `confidence` too, hidden in adapter code instead of in the line format. Existing meanings: numeric `self_confidence` (`findings_v2.py:178-182` per diff-analysis C-010), calibrated per-finding value (`cluster.py:79-83, 288-297`), router text `"low"` (`severity_router.py:174`).
3. A's primary producer of `in_diff` and `original_line` rests on "the diff the pre-step already holds" (A section 2). `pr_submit` has no hunk parser: grep for `hunk|diff --git|@@` over `src/superclaude/pr_submit` finds only fix-hunk text in `fsm.py:395-427` [CODE-VERIFIED]; the poll payload has no diff keys (diff-analysis C-002, X-010, [UNVERIFIED] for A). A's own test 4 (A section 6.4) says A is wrong if the hunk list is not available. That is a premise placed as primary, not as fallback.
4. A's "zero edits" claim is true of existing code and overstated as a contract statement. A adds a pre-step to `SKILL.md` prose, a sibling Output Contract field and a tri-state that A section 4 admits "no test pins until one is added". The field is exactly as contract-visible and exactly as unpinned as B's third key (X-004, X-005). INV-E is preserved by construction only for `Finding`, `Severity` and the FSM; for the Output Contract A and B edit the same table.
5. A's quorum rule has no home. A section 5 says the rule R-C03 describes is a ledger-merge refusal and proposes "a shared helper over `cluster_v2` output". `cli/review/` has zero `quorum` or `min(2` matches [CODE-VERIFIED]. A helper in the core contradicts "no change to `cluster.py`"; a helper in the adapter turns the "mapper" into a policy holder. A names the gap honestly (credit), but it undercuts "A touches nothing shared".
6. A's information-loss answer introduces an identity bug. A section 8 says a second citation or the supporting reviewers' count can go "in `body` as text". `fix_key = sha256(path, line, body)` (`models.py:196-207`) [CODE-VERIFIED], so a body that includes a support count changes whenever a second reviewer agrees or drops out, and the finding changes identity between rounds (INV-009 idempotency, A-007). B has the same exposure for `quote` (O4), but B leaves it as an open reader decision and A proposes it as the answer.
7. A leaves staleness and re-run open: optional, per PR, outside the round counter (A section 4). With bots the gate is SHA- and watermark-bound (`SKILL.md:103-152` per diff-analysis A-008); A specifies nothing equivalent for the panel.
8. "One adapter per consumer" (A section 7) is a linear cost model. It is honest, but B's counter is weak and I do not press it: B admits the `/task` gate does not use the four PR keys (B section 7), so rf-qa is not a separator.

## Invariants

- INV-E (HIGH): `Finding`, `Severity`, the FSM, `pr_target_ok`/`origin_ok` and the no-`gh`/`git` core stay untouched in B; B adds one function to `severity_router.py`, which is already one of the files the static-purity test lists by name (`test_static_grep.py:47-54` per diff-analysis C-003, not re-read by me). B-as-written is endangered in a narrow sense (B section 5 says so): `reviewers.py` (five functions), `SKILL.md:271`, `:277` and `commands/pr-submit.md:60` are edited. A is cleaner on code and equal on the Output Contract. In my hybrid `reviewers.py` is not edited and the Contract gains one sibling field, the same edit A makes.
- INV-F (MEDIUM): neither variant adds a `src/superclaude/` path to installed prose, but this is [UNVERIFIED] until text is written. B's as-written plan edits three prose copies of the `reviewers` object; A edits pre-step prose plus one field. Check for both: `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`. The reader is package code reached by import, as `refs/severity-routing.md:20` describes for `finding_from_comment`.
- INV-C (MEDIUM): B depends on unknown keys passing the v2 parser. They do today: `check_finding` never iterates keys outside its list and rejects only `calibrated_confidence` (`findings_v2.py:96-97`, read through `:153`), and `parse_block` appends the whole `obj` (`:288-290`) [CODE-VERIFIED]. I searched `tests/review` for a test pinning "unknown keys accepted" on a findings-v2 line and found none (the `unknown key` pins at `test_review_panel.py:33, :65` are for panel-config objects) [CODE-VERIFIED absent by grep]. So B rests on an unpinned absence of rejection, and A does not depend on it at all. This is a real test-coverage hole in B. The fix is a T0 test that a line with the four extra keys parses `complete` and survives unchanged. Under my hybrid the harness injects the keys, so the dependency and the T0 pin both remain.
- INV-A (reflect contract 1.8.0 byte-identical): B edits nothing under `cli/reflect/`; the only shared edit is vocabulary parameters on `check_finding` with today's constants as defaults, needed under both positions (A section 2, B section 3.1). Same for A and B.
- INV-B (36-test verdict matrix): `derive_verdict` is not on the PR path in either design. Same for both.
- INV-I (absent or incomplete never reads as clean): satisfied in both only as reporting. Neither design shows that `terminal_clean` cannot be reached with an incomplete panel; B did not trace it (B section 9) and I did not either [UNVERIFIED]. B's `reviewers.panel = "incomplete"` and A's sibling field are equally decorative unless the FSM reads them.

## Concessions

1. X-008: B9 and B section 3.2 a2 are in tension. B9 says a third name "reuses this bookkeeping", but a2 excludes the panel from `retrigger_phrase`, `reviewer_activity` and the re-trigger path. What remains reusable is name-agnostic: `pending_retriggers` filters by event reviewer (`reviewers.py:443-457`) and the `absent_reviewers` fold takes any string (`run_log.py:179, 226, 355`) [CODE-VERIFIED]. A can reuse the fold by emitting `reviewer_absent{reviewer: "panel"}`. B9 does not separate the designs.
2. X-009 and A-013: B's `incomplete` on "a C-03 quorum refusal" depends on a rule that does not exist at HEAD. `cli/review/` has zero `quorum` or `min(2` matches [CODE-VERIFIED]. A quorum evaluator does exist in `cli/reflect/fallback.py:76-82, :161-178` (`reviewer_count >= 2`), but over worker records for the reflect fallback ladder, not over `cluster_v2` output. B should drop the quorum clause and use the stricter rule: any reviewer whose state is not `complete` (`COMPLETION_STATES`, `findings_v2.py:40`) makes the panel `incomplete`. That needs no new rule. A names the new work; B hid it.
3. X-006: B4 is only partly true. `auggie-reviewer.md:54-67` emits `severity_hint`, `file`, `line`, `in_diff` and `confidence` (`high|medium|low`): two of B's four keys, `file` not `path`, no `original_line`, no `reviewer` [CODE-VERIFIED]. "The four keys are the common record of the two code-review consumers" is overstated; it is a partial precedent. A is right that no code sets these keys for the bots (`classifier.py:443-456` per diff-analysis).
4. C-004: B's slot cost is real and larger than B section 3.2 reads. `merge_wait` needs guards at `:412` (a pending third pair returns `polling`) and `:420` (`no_response`), not one. The module docstring says "an empty identity set disables that reviewer" (`reviewers.py:6-8`), which collides with B's "panel branch returns the empty set". `REVIEWERS` is exported at `__init__.py:104, :198`, and its only consumer `list_review_threads` (`:276`) has no caller in `src/` or `tests/` (diff-analysis C-004), so adding `panel` there buys no behaviour. I concede the slot axis (S-002, S-003, S-004, C-004, C-005).
5. X-005 and B10: "a separate pre-step that fails leaves no entry in the contract" is true only for an A without a presence field. A includes one (A section 2). B10 is not a separator.
6. C-001: B never says whether `cluster_v2` runs first. Without it `dedup_groups` merges only on exact `(path, line or original_line)` (`reviewers.py:430-440`), so three reviewers citing lines 40, 41 and 42 stay three `Finding`s with three verifications and possibly three troubleshoot dispatches. `cluster_v2` joins spans within `SPAN_TOLERANCE = 3` (`cluster.py:72, 161-181` per diff-analysis). A is right that the panel's clustering is its value-add and must run before conversion. The fix is strength 2 (representative line).
7. C-002, C-016, C-010: model-emitted `in_diff`, `original_line` and `reviewer` are the weakest part of B's four keys. The harness knows the reviewer name and can compute the hunk facts; B's own M2 admits the fallback. The `confidence` key collides with three existing meanings (B section 3.5). The defensible core of B is the reader, not the four keys.
8. C-008 and O3: bots silent, panel has findings. B marks it OPEN (`SKILL.md:77`, `:365`) and so does the hybrid. Neither variant resolves it, and both need an owner decision before the panel can drive a push on its own.
9. C-003 and X-010: B's M2 fallback ("deterministic hunk pre-check") is new diff-aware code too; `pr_submit` has no hunk parser. Both designs need it if reviewer-stated `in_diff` proves imprecise. A's position is not unique here, only more committed to it.
10. A-006: B's third reviewer name does nothing for a panel finding that has no `comment_id` or `thread_id`. `fallback_only = not any(isinstance(f.comment_id, int) for f in verified)` (`fsm.py:1064`) handles the all-thread-less batch only; a mixed bot plus panel batch reaches `do_resolve(findings=verified)` (`:1074`) with no stated rule for the panel member [CODE-VERIFIED]. Neither variant addresses it.

## Shared-assumption responses

| A-NNN | Response | One sentence |
|-------|----------|--------------|
| A-001 | ACCEPT | The panel runs from the main session only (`SKILL.md:47-49` per diff-analysis); B section 3.3 keeps that boundary and so does my hybrid. |
| A-002 | ACCEPT | The PR path needs no ledger, and `pr_submit` has no reference to `cli/review` today (0 grep matches in `pr_submit/`), so round identity and thread resolution stay `pr_submit`'s. |
| A-003 | ACCEPT | A PR panel profile (lens or none, category and severity sets, a template, tier resolution) does not exist: `check_finding` has no set parameters (`findings_v2.py:84-90`) and `LENSES` has no PR value (`:36`), so it is prerequisite work for both designs and neither lists it. |
| A-004 | REJECT | After conversion a `Finding` is also read for `in_diff` and `verification_status` (`fsm.py:905-907`), `fix_key` over path, line and body (`models.py:196-207`) and `comment_id`/`thread_id` for reply and resolve (`fsm.py:1064-1074`); the four-field claim holds only for `seed_troubleshoot` and `dedup_groups`. |
| A-005 | QUALIFY | Panel findings may enter Wave 2-4 only if the owner wants remediation; whether a panel finding may trigger a push, and which tier blocks, is open (INV-J, O3), so the hybrid should enter report-only first and gate remediation on the owner answer. |
| A-006 | REJECT | A thread-less panel finding does not pass reply, resolve and summary safely by default: `fallback_only` is decided by "no finding has an int `comment_id`" (`fsm.py:1064`), so a mixed bot plus panel batch reaches `do_resolve` with no rule for the panel member. |
| A-007 | QUALIFY | `fix_key = sha256(path, line, body)` is stable only if the body is a fixed string per defect; a cluster representative claim chosen by confidence (`cluster.py:338-344`) or a body carrying support counts or `quote` is not, so `body` must be the reviewer's `claim` verbatim and nothing else. |
| A-008 | ACCEPT | A panel result is valid only for the head SHA it reviewed; B binds it (a2), A leaves it open, and the hybrid must bind it. |
| A-009 | ACCEPT | Per-round panel cost is unmeasured (GQ-177, OQ-18) and M1 is the measurement both positions need before the panel runs per round. |
| A-010 | QUALIFY | Exact `(path, line)` equality is safe for correctness because every finding is kept (`reviewers.py:430-440` docstring), but it is inadequate for cost when several panel reviewers cite nearby lines, which is why `cluster_v2` must run first (concession 6). |
| A-011 | ACCEPT | Independence is "requested, not served" until C-08 records `model_observed`; any PR report that names panel models must say "requested". |
| A-012 | ACCEPT | `finding_from_comment` is the single validation seam (`severity_router.py:61-119`) and a second typed validator is not written; but it validates and does not map, so a mapper is needed in both designs. |
| A-013 | REJECT | "A completeness and quorum rule is available outside the ledger" is false at HEAD for the review kernel (0 `quorum` matches in `cli/review/`); the simplest fail-closed substitute is "any reviewer not `complete` means `incomplete`" using `COMPLETION_STATES` (`findings_v2.py:40`). |

## Per-point positions

| Point | Superior approach per me (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence |
|-------|------------------------------------------------------|--------------|-----------------------|
| S-001 | Hybrid | 55 | A's pre-step keeps `reviewers.py` and the gate untouched, B's SHA and round binding (a2) is what A leaves open (A-008). |
| S-002 | Hybrid | 85 | The axes are separable (A section 8 `panel` field; B section 8 point 3), so the right answer takes B's wire side and A's slot side. |
| S-003 | A | 75 | A's inventory is one module plus a field; B edits `reviewers.py` (five functions), `SKILL.md:271, :277` and `commands/pr-submit.md:60` (B section 3.2). |
| S-004 | A | 65 | A sibling field avoids the `merge_wait` guards at `reviewers.py:412` and `:420` and the `terminal_augment_no_response` hazard (U-008). |
| S-005 | Neither | 50 | Document structure does not bear on correctness; B's decision-oriented spine surfaces open sub-decisions, A's component spine is easier to implement from. |
| S-006 | B | 55 | B states INV-E as "endangered in a narrow sense" while A's "preserved by construction" overlooks its own Output Contract field and unpinned prose (X-004, X-005). |
| S-007 | Hybrid | 70 | Keep A's equivalence experiment (U-001) and B's T1, T3, T4 and M1-M3; add the T0 unknown-key pin (INV-C). |
| S-008 | A | 55 | A names the quorum helper as an addition beyond R-C03 (U-003); B's table lists the dependency on a refusal that is not in code (X-009). |
| S-009 | B | 55 | B's numbered table with a Tag column and a "Limits" section is easier to audit than inline tags in prose. |
| S-010 | B | 55 | B carries five further objections with OPEN status marked; A's single objection plus concession list is shorter but covers less. |
| C-001 | Hybrid | 65 | Cluster first for grouping and support, then read the `representative` source line (`cluster.py:373`) for content; neither variant says this. |
| C-002 | A | 65 | Harness-computed `in_diff` and `original_line` beat model-stated ones, though A's premise that the pre-step holds the hunks is [UNVERIFIED] (X-010). |
| C-003 | B | 55 | `severity_router.py` is already core-pure and listed in the static check (`test_static_grep.py:47-54` per diff-analysis), while A's new module must be added to it. |
| C-004 | A | 85 | `reviewer_identities`, `retrigger_phrase`, `reviewer_activity`, `merge_wait` and `list_review_threads` are all two-name (`reviewers.py:47-78, 276, 395-424`) and B's own B13 admits it. |
| C-005 | A | 65 | One sibling field edits one table row; B's third key edits the row and two prose copies (`SKILL.md:277`, `commands/pr-submit.md:60`). |
| C-006 | A | 60 | A reads `complete_reviewers`, `invalid_reviewers`, `valid_blocks` (`cluster.py:414-418`) and names the missing helper; B's "quorum refusal" has no code (X-009). |
| C-007 | B | 60 | B binds presence to the head SHA inside the round cap; A leaves a re-run needing a cycle id and says nothing on staleness. |
| C-008 | Neither | 60 | Both leave "bots silent, panel has findings" open; B at least flags it (O3), neither decides it. |
| C-009 | A | 55 | A's adapter-owned table restates the CRITICAL row and splits MAJOR by `blocking`; B's lossy map or a fifth `severity_hint` key is undecided (B section 3.4). |
| C-010 | Hybrid | 55 | Omit a model-stated `confidence` key and derive it in the reader, because `confidence` already has three meanings and A's `disputed`-based value adds a fourth. |
| C-011 | Neither | 60 | Both need only the decided FX-5 vocabulary parameters; B's four keys ride as unknown keys with no parser change but also with no pin (INV-C). |
| C-012 | Neither | 60 | Both end in a slot-less `Finding` (`models.py:179-194`); whether the extra line content is ever read is exactly what M3 measures. |
| C-013 | Neither | 75 | `verify-citations` runs on a cards directory and writes a sidecar under both designs (X-007), so it does not separate them. |
| C-014 | B | 55 | T1 parity against `finding_from_comment` is a smaller drift pin than golden cluster fixtures that must also hold source blocks (X-001). |
| C-015 | A | 55 | B itself says the `/task` gate does not use the four PR keys and B adds nothing for rf-qa beyond M2 (B section 7). |
| C-016 | A | 75 | The harness knows the reviewer name; `Finding.reviewer` should be set to `"panel"` by the caller, not asserted by a model on each line. |
| X-001 | B | 90 | A section 3.5 claims the cluster holds severity and category; `cluster.py:352-378` and `:354-365` have neither. |
| X-002 | B | 60 | A's pin claim holds only for a B that edits `reviewer_activity`, which B's a2 does not; both are still bound by the one-python-block pin (`test_codex_reviews.py:688`). |
| X-003 | B | 90 | 47 `test_*.py` files, not 50 (diff-analysis Glob); order of magnitude unchanged. |
| X-004 | Neither | 85 | No test pins the `reviewers` row (`test_merge_guard_protocol.py:498-508` pins only `merge_guard`), so an added key or field is unpinned in both. |
| X-005 | A | 65 | A has a sibling presence field, so B10's "leaves no entry" is true only for an A without it. |
| X-006 | A | 70 | `auggie-reviewer.md:54-67` carries two of B's four keys (`in_diff`, `confidence`) and `file` not `path`, so B4 is overstated. |
| X-007 | Neither | 75 | `Finding` has no flag slot under B either (B1 applies to both), and both read the same sidecar. |
| X-008 | A | 70 | With the panel excluded from re-triggers (a2), only the name-agnostic absent fold remains reusable, and A can use it too. |
| X-009 | A | 70 | A names the quorum helper as new work; `cli/review/` has no `quorum` match and B's `incomplete` depends on a rule that is not there. |
| X-010 | Neither | 60 | `pr_submit` has no hunk parser (grep: only fix-hunk text at `fsm.py:395-427`), so both designs need new diff-aware code. |
| A-001 | Neither | 80 | Both keep the main-session boundary (`SKILL.md:47-49` per diff-analysis). |
| A-002 | Neither | 80 | Both leave the PR path ledger-free; `pr_submit/` has no `cli/review` reference. |
| A-003 | Neither | 85 | A PR panel profile is unbuilt prerequisite work for both (`findings_v2.py:84-90`, `:36`). |
| A-004 | Neither | 70 | The four-field read claim is contradicted (`fsm.py:905-907`, `models.py:196-207`), and it hurts A's information-loss answer more than B's. |
| A-005 | Neither | 65 | Whether a panel finding may trigger a push is an owner decision both assume; hybrid enters report-only first. |
| A-006 | Neither | 75 | Neither covers a thread-less panel finding in a mixed batch (`fsm.py:1064-1074`). |
| A-007 | Neither | 60 | Both risk unstable `fix_key` through the body; A's "support count in body" suggestion makes it worse. |
| A-008 | B | 60 | B states the head-SHA binding (a2); A states it only as "needs a cycle id". |
| A-009 | Neither | 85 | Cost is unmeasured for both; M1 serves both. |
| A-010 | Hybrid | 60 | Exact-line dedup is correct but costly; running `cluster_v2` first is what bounds the cost. |
| A-011 | Neither | 85 | Carried from R-C03 by both; no code to check. |
| A-012 | Neither | 80 | The validation seam is `finding_from_comment`; the mapper is needed in both. |
| A-013 | Neither | 70 | No quorum rule exists in the review kernel, so both lean on future work; the stricter "any non-complete means incomplete" rule needs none. |

## Hybrid I would accept

B's reader on A's slot, with the open items kept open:

1. Slot (A wins): the panel is a separate pre-step from the main session; no `panel` in `REVIEWERS`; no third pair in `merge_wait`; `reviewers.py` is not edited. Panel standing is one sibling Output Contract field (`present | absent | incomplete`), bound to the head SHA it reviewed (B a2, A-008) and never read as clean (INV-I).
2. Wire (B's reader, A's provenance): `pr_submit` reads a findings-v2 line through one pure `finding_from_v2` next to `finding_from_comment` (already core-pure). The pre-step runs `cluster_v2` first and hands the reader the `representative` source line (`cluster.py:373`), so grouping is A's and content is B's. `in_diff`, `original_line` and `reviewer = "panel"` are set by the harness on that line (A's provenance; the `verify-citations` pattern), not asserted by the model. A model-stated `confidence` key is dropped until a threshold is measured.
3. Standing rule: `incomplete` when any reviewer's state is not `complete` (`COMPLETION_STATES`), with no quorum clause; the `min(2, requested)` floor stays with C-03 follow-up work.
4. `body` is the reviewer's `claim` verbatim, with no support counts or quotes appended, so `fix_key` stays stable (A-007).
5. Tests: T0 (a v2 line with the extra keys parses `complete` and survives unchanged, closing the INV-C hole); T1 parity of `finding_from_v2` against `finding_from_comment`; A's U-001 equivalence run on fixtures that hold source blocks; T4 grounding; a regression pin that `merge_wait`, `reviewer_activity` and the one-python-block count stay unchanged (`test_codex_reviews.py:285-295, :688, :705`); M1 cost per round; M3 usage of the dropped fields; `grep -rn 'src/superclaude'` over the installed primitives (INV-F). All of this is read, not run.
6. Still open and owner-owned: whether a panel finding may drive a push (A-005, C-008, O3), the thread-less mixed-batch rule (A-006), and the per-round cost (A-009).

## Round 2: Rebuttals

#### Variant A Rebuttal (Round 2)

Slot C-10 (pr-review-wire-format-and-slot), Round 2, standard depth; focus correctness, risk, test-coverage. Code state: HEAD 50d4d2b9d, branch ironbelly/shadow-runs. Nothing was run; no test, no pytest. Tags: [CODE-VERIFIED] = I read that file:line myself in this Round 2 session; [UNVERIFIED] = carried from a document or a Round 1 file and not re-read now; [RELIED] = taken from diff-analysis.md or a Round 1 file and not re-checked. Paths are relative to the repository root. This file cites nothing from the run-1 task folder or the run-1 queued file.

## 1. Responses to B's Round 1 criticisms of A

#### 1.1 B's Weaknesses 1-8

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

#### 1.2 B's concessions and what they leave

- B concessions 1 (X-008), 2 (X-009/A-013), 3 (X-006), 4 (C-004), 5 (X-005/B10), 6 (C-001), 7 (C-002/C-016/C-010) and 9 (C-003/X-010 hunk parser) are accepted as stated and I now rely on them. Net effect: B conceded the slot axis (S-002 to S-004, C-004, C-005) and the producer of the PR-local keys.
- B concession 2 names a quorum evaluator in `cli/reflect/fallback.py:76-82, 161-178`. It exists, but it is not a usable rule for the PR panel (item (b) below). B's replacement rule ("any reviewer not `complete`") is the right one and I take it.
- B concessions 8 and 10 (C-008/O3; A-006) leave two items open that I now close with defaults (section 4 rows 8 and 9; section 5 conditions 1 and 7), each flagged as owner-decidable.
- B concession 7 ("the defensible core of B is the reader, not the four keys") is the sentence that makes the two hybrids nearly one design; section 4 lists exactly what remains.

#### 1.3 B's per-point disagreements with my Round 1 table

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

#### (a) Do `parse_block` and `check_finding` keep unknown keys on a findings-v2 line, and does a test pin it? Result: B is right on both counts.

- `check_finding` never iterates the keys of `obj`; the only key-level rejection is `calibrated_confidence` (`src/superclaude/cli/review/findings_v2.py:96-97`). `parse_block` then appends the whole object after `obj.setdefault("refs", [])` (`:288-290`), so an extra key survives into `res["findings"]`. [CODE-VERIFIED]
- The module docstring reserves the opposite: "A findings-v1-valid line with other keys may be rejected" (`:3-5`). Acceptance is a property of the code today, not a stated promise. [CODE-VERIFIED]
- No test pins acceptance. `test_v1_line_passes_v2_unchanged` uses only lines whose keys are all in `V1_FIELDS` (`tests/review/test_review_findings_v2.py:69-81`, assertion at `:72`); `test_check_finding_never_raises` varies `V1_FIELDS`, `V2_FIELDS` and the citation keys only (`:372-401`); the other `base(...)` overrides set known keys or `calibrated_confidence` (`:128-172, :205, :330-350`); the `unknown key` pins in `tests/review/test_review_panel.py:33, :65` are for panel-config objects. [CODE-VERIFIED for those files; I did not read every test that calls `parse_block`, so "no test anywhere" is not shown, only "none in `test_review_findings*.py` and none by name or phrase in `tests/review` and `tests/cli/reflect`".]
- Engagement: the hole is live for B as originally written (reviewer-emitted keys). It is not live for either hybrid as long as the PR facts are set on the converter's output dict after `parse_block` and `cluster_v2` and are never written back into a findings-v2 block that is re-parsed. `annotate` and `_members` read only named keys (`cluster.py:126-154, :288-297`), so extra keys do not disturb clustering either. T0 stays a cheap insurance test if keys are ever promoted (promotion trigger in section 5).

#### (b) Is there a quorum evaluator at `cli/reflect/fallback.py:76-82, 161-178`? Result: yes, but it is not usable for the PR panel.

- `QuorumState` (`:75-82`) and `evaluate_quorum(workers: list[WorkerResult], *, allow_single_vendor)` (`:161-179`) exist. It counts workers whose `status == "success"` (`:166`) and requires `reviewer_count >= 2`, `model_class_diversity == "full"` and multi-vendor or `allow_single_vendor` (`:169-173`). [CODE-VERIFIED]
- It works on swarm `WorkerResult` records and statuses (`"success"`, `"timeout"`, `"proxy_error"`, `"parse_error"`, `:40`), not on findings-v2 completion states (`complete`, `truncated`, `invalid`, `failed`, `timed_out`, `findings_v2.py:40`) and not on `cluster_v2` output. The module imports `superclaude.cli.swarm.*` (`:15-28`). The names `evaluate_quorum` and `QuorumState` appear in no other file under `src/superclaude`. [CODE-VERIFIED]
- `pr_submit` has zero imports of `cli.review`, `cli.reflect`, `findings_v2`, `cluster_v2` or any `superclaude.cli` module (Grep, 0 matches). Reusing this evaluator would add the first `pr_submit` to `cli.swarm` dependency and would impose a model-class diversity requirement that the PR panel has not decided (independence is "requested, not served" until C-08). The `quorum` and `min(2` patterns have 0 matches in `cli/review` and `pr_submit`. [CODE-VERIFIED]
- Consequence: B's concession stands (no review-kernel quorum rule exists), B's own replacement rule needs no evaluator, and I adopt it.

#### (c) Does the bot-gate pattern at `SKILL.md:118-124` and `:143-149` drop a whole batch on a `ValueError`, and would B's reader need it? Result: yes it drops the batch; neither hybrid needs it, and copying it would be a defect.

- Both blocks read: `try: ... findings = [finding_from_comment(raw) for raw in selected] ... except ValueError: review_state = "polling"; findings = []` (`SKILL.md:118-124` Augment, `:143-149` Codex). One bad root discards that reviewer's whole batch and the gate retries on the next poll. [CODE-VERIFIED]
- That is correct for the bots, because a bot batch is re-read from GitHub on the next poll. The panel has no re-poll: a dropped batch would be a silent loss, which breaks INV-I.
- What can raise in the converter? `finding_from_comment` raises for a non-object, empty `path` or `body`, non-positive-integer locations, non-text hint/category/confidence/reviewer, non-bool `in_diff` (`severity_router.py:67-82`). After `check_finding`, `path` is a non-empty repo-relative string and `line_start` a positive integer (`findings_v2.py:59-81`), `claim` is a string of at most 300 flattened characters (`:111`), and `category` is in the allowed set (`:109-110`). `reviewer`, `in_diff`, `severity_hint` and `confidence` are set by converter code, not by a model. So no model-typed field can reach the `ValueError` branches under either hybrid; only the converter's own bugs or an empty/whitespace claim can. For original B (reviewer-emitted `in_diff`, `reviewer`), a string-typed `in_diff` passes the core silently (item (a)) and would raise here.
- Rule for both hybrids: convert per cluster, catch `ValueError` per cluster, collect `(cluster_id, reason)` into a `dropped` list that is reported in the `panel` field and the summary; never wrap the batch in one `try`. Test: three clusters with one malformed gives two `Finding`s and one reported drop.

#### (d) Is `severity_router.py` on the static-purity list, and does adding a module require editing that file? Result: yes it is listed; no, a new module needs no edit.

- `CORE_PURE_FILES` names `fsm.py`, `severity_router.py` (`tests/pr_submit/test_static_grep.py:48`), `loop_guard.py`, `ci.py`, `conflicts.py`, `merge_guard.py` and four skill refs (`:37-55`). `test_tn50_core_pure_no_gh_git_tokens` reads each listed file line by line and fails on any `\bgh\b` or `\bgit\b`, with no comment or docstring exemption (`:136-147`). `test_tn41_core_never_imports_anthropic` is the only test that globs every `PR_SUBMIT_PKG/*.py` (`:150-159`). [CODE-VERIFIED]
- So: a new module is outside T-N50 by default (no edit needed for the suite to pass, but also no purity coverage); covering it means appending it to `CORE_PURE_FILES` (an additive edit to an existing test file) or a new test file that applies the same token check (no existing test edited). A function added to `severity_router.py` stays under T-N50, so its code and docstrings must avoid the words `git` and `gh`; a hunk parser that quotes `diff --git` headers would fail the suite.
- Also pinned and binding on both hybrids: SKILL.md may contain exactly one ```python fence (`tests/pr_submit/test_merge_guard_protocol.py:533`, `tests/pr_submit/test_codex_reviews.py:687-688`, `tests/pr_submit/test_cosmos_protocol.py:35-36`; `test_conflict_sync_protocol.py:534` filters lines starting with ```python, assertion not read). The existing merge step is a ```text fence (`SKILL.md:160-173`). Any pre-step code must therefore be described in prose or ```text fences, or live in a new ref; it must not add a ```python fence to SKILL.md. [CODE-VERIFIED]
- `tests/pr_submit/test_cosmos_protocol.py:51` pins `core.finding_from_comment is severity_router.finding_from_comment`; a sibling function or module does not touch it. [CODE-VERIFIED]

#### (e) How does a cluster `representative: {reviewer_id, id}` (`cluster.py:373`) join back to the source line? Result: a well-defined key join, with three conditions.

- A reviewer record is `(reviewer_id, ordinal, findings_v2_block, calibration_map)` (`cluster.py:3-4, :202`); the block is a `parse_block` result or a bare list (`:218-223`). Each member carries `reviewer_id` and `id` (`:356-358`); the representative is `{reviewer_id, id}` (`:373`). The join is `lookup[(reviewer_id, id)]` over the findings of the valid records. [CODE-VERIFIED]
- Uniqueness: `_records` skips a duplicate `reviewer_id` (`:235-247`) and `_members` skips a duplicate finding `id` within a reviewer (`:258-277`), so each `(reviewer_id, id)` names at most one clustered finding; `parse_block` already rejects duplicate ids (`findings_v2.py:101-102`). The converter must build its lookup the same way: valid records only (a list block, or a dict with `state == "complete"`, `:218-223`), first occurrence wins.
- `cluster_v2` does not change its inputs (`:3-4`), so the same record objects can be passed to both calls with no drift. If a lookup misses (records changed between the two calls), skip the cluster and count it in `dropped`; never guess.
- What the join is needed for: only `severity` and `category` (and a quote if ever wanted). `path`, `line`, `claim` and `blocking_any` come straight from the cluster (`:354-367, :374-375`). Severity is the maximum over all joined members, not the representative's, because the representative is the most confident member, not the most severe (`:338-344`).
- Conditions: (1) `snapshot_file_list` must list the PR head's files, because only `resolved` citations cluster (`:170-179`) and a citation to a file missing from the list is `unresolved`; (2) a member whose `primary_citation` is `malformed` has `line_start None` (`:112-113`), so the converter drops that cluster and counts it; (3) `annotate` falls back to the first citation when the lens has no `PRIMARY_ROLES` entry (`:133-134`), so the PR template must say the first citation is the defect location (a template-content matter, slot C-07).

#### Found on the way

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

#### Variant B Rebuttal (Round 2)

Slot C-10 (pr-review-wire-format-and-slot), Round 2, standard depth; focus correctness, risk, test-coverage. Code state: HEAD 50d4d2b9d, branch ironbelly/shadow-runs. Nothing was run: no pytest, no script, no model call. Tags: [CODE-VERIFIED] = I read that file and line myself in this Round 2 session; [RELIED] = taken from A's Round 2, diff-analysis or my Round 1 and not re-read now; [UNVERIFIED] = not settled by reading. Paths are relative to the repository root. This file cites nothing from the run-1 task folder or the run-1 queued file. "C10-R" is A's Round 2 resolution; "C10-R-B" is C10-R plus the amendments named in section 6.

## 1. Responses to A's section 2, "What B still gets wrong", items 1 to 5

#### 1.1 Zero-token rule on `severity_router.py` and the home of the converter

The fact is right. `CORE_PURE_FILES` lists `severity_router.py` (`tests/pr_submit/test_static_grep.py:37-55`, entry at `:48`). `test_tn50_core_pure_no_gh_git_tokens` applies `\bgh\b|\bgit\b` to every line of every listed file with no comment or docstring exemption (`:136-147`). [CODE-VERIFIED] A function added to the router must keep those two words out of its code and its docstrings.

The argument does not separate the two homes, for two reasons.
1. A's own condition 2 puts a T-N50-style check on the new module. Then the hunk parser has the same vocabulary limit in the new module. The only way the new module escapes the rule is to stay uncovered, and A rejects that. A parser needs no such word anyway: it reads `@@ -a,b +c,d @@` and `+++ b/<path>` lines, not the `diff --git` header.
2. A `finding_from_v2` docstring or body fails the suite only if it uses the words `git` or `gh`. That is a style constraint, not a placement driver. The router's own docstring already complies (`severity_router.py:10-13`). [CODE-VERIFIED]

What I concede, and on different grounds: my Round 1 said the reader "is a rename" and that T1 (parity) "fails if the reader needs any logic beyond renaming". That falsifier has fired. Under C10-R the converter does a `(reviewer_id, id)` join (X-001), a severity maximum, a severity table, a diff-range computation and per-cluster error handling. Logic of that size does not belong in the router that the FSM and the tests import (`tests/pr_submit/test_cosmos_protocol.py:51` pins `core.finding_from_comment is severity_router.finding_from_comment`). So I accept a new module. C-003 goes to A on size and import fan-in, not on purity.

One dispute: A treats "no existing test edited" as a goal. INV-E names `Finding`, `Severity`, the FSM and the fork-only checks, not test files. Appending the new module to `CORE_PURE_FILES` is one additive list entry and keeps one definition of "core-pure"; a second copy of the token scan in a new test file can drift from the first. I propose the append (AM-5). If the owner prefers zero edits to existing tests, a new test file is acceptable; the stake is low.

#### 1.2 Representative is the most confident member, not the most severe

Confirmed. `_cluster` picks `rep = min(group, key=(-confidence, order))`, with a missing confidence ranked below every calibrated one (`src/superclaude/cli/review/cluster.py:338-344`). `claim` is the representative's claim and `blocking_any` is over all members (`:374-375`). [CODE-VERIFIED] I accept: severity must be taken over the joined members, not from the representative alone.

Two facts make this worse for the PR path than A states.
- `pr_submit` has no calibration step at all (Grep `calibrat` over `src/superclaude/pr_submit`: 0 matches). The only source of a per-finding confidence is a `calibration:` block in a reviewer card (`src/superclaude/cli/review/cluster_cmd.py:1-6, 28-40`), and whether the PR panel card carries one is the template's decision [UNVERIFIED]. With no calibration every member has `finding_confidence = None`, every member sorts on `order`, and the representative is the lowest `(ordinal, position)` member. In the default PR path "most confident" means "first reviewer". The claim text then comes from whichever reviewer has the lowest ordinal.
- The member dicts that `cluster_v2` returns carry no `claim` (`cluster.py:354-365`), so the claims of the non-representative members are recoverable only through the join.

Taking the severity maximum is necessary but not sufficient. See D1: it pairs a maximum severity with the representative's category and claim, which can produce a wrong outcome.

#### 1.3 `original_line` is useless for panel findings

Confirmed. Producers are the bot paths only: `classifier.py:449`, `reviewers.py:295, :309`. The one consumer of the value is `dedup_groups`, and only when `line` is None (`reviewers.py:438`). The SKILL and the routing ref call it "only a verification hint" (`SKILL.md:226`; `refs/severity-routing.md:48-50`). The field itself is `models.py:192`; the validator reads it at `severity_router.py:73, :116`. A Grep of `src/superclaude` for `original_line|originalLine` finds no other reader of the value. [CODE-VERIFIED] A panel `Finding` always has an integer `line` (`is_groundable`, `fsm.py:364-372`), so `original_line` is never read. I drop it from my hybrid.

#### 1.4 Harness injection versus the converter setting the keys on its own dict

Conceded. After `parse_block` the harness holds the dict in memory; writing `in_diff` and `reviewer` into it and building a `Finding` from it is the same operation as the converter building its own dict, and it additionally mutates a record the kernel handed out. If the keys were written back into a findings-v2 block and re-parsed, the unknown-key acceptance (confirmed in section 3 (a)) would be load-bearing and unpinned. The converter owning the keys removes that. The only residual difference was my T0 test, and T0 is only needed if keys are ever promoted. I withdraw "the harness injects them into the line".

#### 1.5 Open items C-008 and A-006

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

#### D1 (HIGH): the cluster collapse mixes different defects, then C10-R pairs a maximum severity with the wrong category and claim

Mechanism, all [CODE-VERIFIED]:
- `same_defect_v2` compares only deviation class, `refs_norm` and citation spans (`cluster.py:161-181`). It never compares `category` or claim text. The span test is `c1.line_start <= c2.line_end + 3 and c2.line_start <= c1.line_end + 3` on the same path (`:170-179`, `SPAN_TOLERANCE = 3` at `:72`).
- The refs test passes when both `refs_norm` lists are empty (`:167-169`). `refs_norm` takes tokens such as `FR-12` or `P1` from `refs`, `anchor`, `anchor2` and the claim text (`src/superclaude/cli/review/findings.py:321-337`). A PR finding about code has no requirement ids, so in the normal case both lists are empty.
- Clusters are union-find components, so adjacency chains (`cluster.py:302-320`; `chained` is only a flag, `:324-326`).
- `_cluster` keeps one claim, the representative's (`:374`), and the member dicts carry no claim (`:354-365`).

Failure example. Reviewer R1 emits `F1`: category `style`, MINOR, citation `a.py` lines 40-40, claim "rename this variable". Reviewer R2 emits `F1`: category `security`, CRITICAL, citation `a.py` lines 42-42, claim "token compared with ==". No refs, no requirement tokens. Both resolve against the snapshot, `|42-40| <= 3`, refs both empty: one cluster. With no calibration the representative is R1's finding (lowest ordinal, `:338-344`). C10-R then gives severity = maximum over members = CRITICAL; category from the representative = `style`; body = "rename this variable". `remap_severity` clamps `style` to a ceiling of LOW (`severity_router.py:52, :136-143, :171`), so the Finding is Low and report-only. The CRITICAL security defect is demoted to Low, and its text is nowhere in the Finding. If instead the category is taken from the maximum member, the Finding is CRITICAL with the body "rename this variable". Either way the output is wrong. A per-line reader keeps both: `dedup_groups` groups by exact `(path, line)` and keeps every finding (`reviewers.py:430-440`), so lines 40 and 42 stay two Findings and each routes on its own category.

This is a defect of "cluster first, one Finding per cluster" itself, which I conceded in Round 1 (C-001) too quickly, and it is in my Round 1 hybrid as well. A's value-add (merge near-duplicates) is real for same-category duplicates; it is wrong for cross-category adjacency.

Amendment AM-1: one Finding per (cluster, category) pair. Group the joined members of a cluster by their own source-line category; within a group the representative rule, the severity maximum and `blocking_any` apply. A `chained` cluster (`cluster.py:324-326`) emits one Finding per member. Test: the example above as a golden fixture; expected two Findings, `style` Low and `security` Critical.

#### D2 (MEDIUM): "a CRITICAL is never lowered" does not hold through the router

A's section 4 row 10 and its C-009 evidence say the adapter table "never lowers a CRITICAL". The table maps CRITICAL to the hint `critical`; `remap_severity` then applies, after it, the category ceiling (`performance` HIGH, `docs` MEDIUM, `dead-code` LOW, `naming` and `style` LOW: `severity_router.py:34-53`, clamp at `:171` and `:197`) and the `in_diff is False` drop (`:178-189`). So a reviewer's CRITICAL with category `docs` leaves the router as Medium, and a CRITICAL outside the diff in a `correctness` category leaves it at High. These are the router's rubric, shared with both bots, and I do not propose to fork them. The claim must go, and the information must not be lost: `Finding` has no slot for the reviewer's severity (`models.py:179-194`).

Amendment AM-2: the converter returns, per Finding, a small side record `{cluster_id, reviewer_severity_max, blocking_any, disputed, reviewers}` used only by the summary and the `panel` field. The summary shows the reviewer's tier beside the routed tier. No change to the router.

#### D3 (MEDIUM): the clause "every cluster was dropped" is vacuously true for a panel with zero clusters

C10-R's standing rule (section 5 condition 4) makes the panel `incomplete` "when every cluster was dropped". For a complete panel that found nothing, the set of clusters is empty and "every cluster dropped" is true under `all(...)`. A clean panel would read `incomplete`, and the first release would never show a clean panel. The opposite error is as bad: a rule written as "dropped count equals cluster count" must not treat 0 = 0 as a drop.

Amendment AM-4: `incomplete` for drops only when there is at least one cluster and all were dropped. Test: three-output standing test gains a "complete, zero findings, `present`" case.

#### D4 (MEDIUM): fail-closed on missing `changed_ranges` loses findings in the wrong direction

W3 and condition 2 say that with no `changed_ranges` the converter "converts nothing" and the panel is `incomplete`. Dropping a panel's CRITICAL because a diff parser failed is the unsafe direction. The router's own default is the conservative one: `Finding.in_diff` defaults to True (`severity_router.py:112`; `models.py:185`), so step 4 does not lower anything, and for both bots step 4 is already dormant because nothing produces `in_diff` (`classifier.py:443-456` per diff-analysis [RELIED]). `is_groundable` (`fsm.py:364-372`) drops findings that cannot be located; a missing diff is a different condition and the finding is located.

Amendment AM-3: with no ranges, convert with `in_diff` left unset (True), mark the panel `incomplete` with reason `ranges_missing`, and say in the summary that the diff-locality step was skipped. Test: fixture with absent ranges expects Findings present and standing `incomplete`.

#### D5 (MEDIUM, INV-I sibling): a `present` panel with blocking clusters beside `terminal_clean`

C10-R keeps INV-I for `absent` and `incomplete` (no "clean" wording). It does not cover `present` with `blocking_any` clusters while the bots are clean. In the first release those findings are report-only and never reach the FSM, so `status` can be `terminal_clean` (assigned at eight sites, `fsm.py:241, :805, :872, :1026, :1085, :1120, :1145, :1253`; the enum is documented unchanged at `SKILL.md:259, :277`) while the same run's `panel` field lists a CRITICAL. A reader of the Output Contract sees `terminal_clean` and `panel: present`.

Amendment AM-4 (second half): the `panel` field carries `blocking_clusters`; the run summary must not use the word "clean" for the run while `blocking_clusters > 0` or the panel is not `present`. This is prose plus a test on the summary template; the owner decision on whether such findings may drive a push (C-008, A-005) stays open.

#### D6 (LOW): the converter's invocation path is unspecified

`SKILL.md` may not take a second `python` fence (four pins, section 3 (d)); the converter has no CLI entry; `from superclaude.pr_submit import ...` would need an edit to the package `__init__.py` exports (existing Python module, contradicting "zero edits to existing modules"). A's condition 6 allows a new ref. Resolution: the pre-step ref imports by full module path (`superclaude.pr_submit.<new module>`) and keeps its own fence; add a new test that pins the ref's existence and the absence of a second fence in `SKILL.md`. Residual: `test_merge_guard_protocol.py:87-90` bans `python` fences only in the merge-guard ref; a repo-wide ref scan outside `tests/pr_submit` was not searched [UNVERIFIED].

#### D7 (LOW): M2 is unmeasurable as written, and cluster scope depends on `snapshot_file_list`

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

## Scoring Matrix

Winner = the superior approach both advocates named in their Round 2 tables (labels agree on all 49 points); confidence = mean of the two Round 2 confidences; evidence = Variant A's Round 2 sentence (Variant B's Round 2 sentence for the same point is in `round2-advocate-B.md`). "Hybrid (C10-R)" means the resolution Variant A's Round 2 section 5 names C10-R; Variant B endorses it as C10-R-B, that is C10-R plus amendments AM-1 to AM-6 (Round 2 B section 6), which Variant A had no opportunity to answer at standard depth.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| A-001 | Neither (open) | 90% | Shared and verified at `SKILL.md:47-49`. |
| A-002 | Neither (open) | 90% | `pr_submit` has zero imports of `cli.review`, `cli.reflect`, `findings_v2`, `cluster_v2` or `superclaude.cli` (Grep). |
| A-003 | Neither (open) | 85% | Both need a PR profile and FX-5 parameters (`findings_v2.py:84-90`), and the category sets share no value (`findings.py:15-22`, `severity_router.py:34-53`). |
| A-004 | Neither (open) | 70% | False for both: `in_diff`, `verification_status`, `fix_key` and comment ids are read (`fsm.py:902-906`, `models.py:196-207`). |
| A-005 | Neither (open) | 73% | Both treat Wave 2-4 entry as given; which tier blocks is open (INV-J) and the first release is report-only. |
| A-006 | Neither (open) | 80% | The FSM hands thread-less findings to the callbacks unfiltered (`fsm.py:1203-1205`); C10-R adds a callback-level skip and a summary-only rule on promotion (INV-K). |
| A-007 | Hybrid (C10-R) | 70% | `body` as the claim verbatim keeps `fix_key` stable within a run (`models.py:196-207`); a re-run after a push is a new identity by design. |
| A-008 | Hybrid (C10-R) | 70% | The `panel` field carries the reviewed SHA, as the bot gate does (`SKILL.md:103-112`); no automatic re-run in the first release. |
| A-009 | Neither (open) | 90% | Cost is unmeasured for both (GQ-177); M1 serves both. |
| A-010 | Hybrid (C10-R) | 60% | Exact-line dedup is correct but costly (`reviewers.py:430-440`); running `cluster_v2` first bounds the cost for panel-internal duplicates. |
| A-011 | Neither (open) | 90% | Carried from R-C03; identical in both. |
| A-012 | Neither (open) | 85% | `finding_from_comment` is the shared validation seam (`severity_router.py:61-119`); the question is only who owns the mapper, and the answer is a converter module. |
| A-013 | Hybrid (C10-R) | 70% | The strict rule "any requested reviewer not `complete`" needs no quorum rule; none exists in `cli/review` or `pr_submit` (0 matches). |
| C-001 | Hybrid (C10-R) | 68% | Cluster first (`cluster.py:72, :161-181`), one `Finding` per cluster, content from the representative, severity from the maximum over joined members. |
| C-002 | Hybrid (C10-R) | 60% | `in_diff` is harness-computed from `changed_ranges`, fail-closed when absent, with reviewer-stated values only compared (M2); no producer exists for the bots (`classifier.py:443-456` per diff-analysis) and `pr_submit` has no hunk parser. |
| C-003 | Variant A | 63% | A new module avoids the zero-token rule on `severity_router.py` (`test_static_grep.py:48, :136-147`); cost is no automatic purity coverage until a new test is added. |
| C-004 | Variant A | 85% | All five two-name functions stay untouched (`reviewers.py:47-78, :276, :395-424`), and B's own hybrid drops them. |
| C-005 | Variant A | 70% | Both hybrids use one sibling `panel` field beside `reviewers` (`SKILL.md:271`), unpinned for either until a new test exists (X-004). |
| C-006 | Hybrid (C10-R) | 70% | B's strict rule computed as requested ids minus `complete_reviewers` (`cluster.py:414-418`); no quorum helper and no floor. |
| C-007 | Hybrid (C10-R) | 65% | B's head-SHA binding adopted; A's once-per-head cadence kept because per-round cost is unmeasured (`fsm.py:32-33` per diff-analysis). |
| C-008 | Neither (open) | 65% | Still an owner decision (A-005); C10-R's default is report-only in the first release, with `terminal_augment_no_response` keyed to the bots because the panel is not in `merge_wait` (`reviewers.py:420`). |
| C-009 | Variant A | 58% | An adapter-owned table reaches `critical`, `medium` and `low` without a fifth key and never lowers a CRITICAL; B's route-cost point (`severity_router.py:56-58`) becomes a table test, and category floors (`:34-53`) remain the router's. |
| C-010 | Hybrid (C10-R) | 75% | `confidence` unset: a `disputed`-derived "low" would lower a CRITICAL via `severity_router.py:173-175`, and three meanings already exist (`findings_v2.py:178-182`, `cluster.py:39-44`). |
| C-011 | Neither (open) | 65% | Neither hybrid adds a key to the v2 line or re-parses an extended line, so the shared core takes only the decided FX-5 parameters. |
| C-012 | Neither (open) | 60% | Both end in a slot-less `Finding` (`models.py:179-194`); `body` is the claim verbatim, and whether dropped fields matter is M3's question. |
| C-013 | Neither (open) | 68% | `verify-citations` writes an advisory sidecar both designs can read (X-007); it does not separate them [UNVERIFIED: `verify_cmd.py` not re-read]. |
| C-014 | Hybrid (C10-R) | 60% | Parity test of the converter's output dict against `finding_from_comment` plus golden fixtures of cluster output and source records; the join key makes fixtures cheap (`cluster.py:356-358, :373`). |
| C-015 | Variant A | 55% | Per-consumer converters match B's own admission that the `/task` gate uses none of the four PR keys; this is a prediction [UNVERIFIED]. |
| C-016 | Variant A | 85% | `Finding.reviewer` defaults to `"augment"` when absent (`severity_router.py:118`), so code must always set `"panel"`; both advocates now agree. |
| S-001 | Hybrid (C10-R) | 68% | A's two-stage topology keeps the python gate and its one-fence pins untouched (`test_codex_reviews.py:687-688`), and B's SHA binding closes the staleness gap; panel findings join `decision["used"]` (`SKILL.md:175-178`) only after promotion. |
| S-002 | Hybrid (C10-R) | 85% | Both advocates now agree the axes separate: slot to A (sibling field), reader logic to B, converter owns the PR facts. |
| S-003 | Variant A | 75% | C10-R edits no existing Python module and no existing test; it adds one module, new tests and two prose rows, while B's original edits `reviewers.py` (five functions) and three prose copies. |
| S-004 | Hybrid (C10-R) | 70% | Sibling field (A) with B's derivation of the value; it avoids the `merge_wait` guards at `reviewers.py:412` and `:420`. |
| S-005 | Neither (open) | 50% | Document spine does not bear on correctness; B's decision-oriented layout surfaced open sub-decisions, A's is easier to implement from. |
| S-006 | Variant B | 58% | A's "preserved by construction" overclaimed (X-001, W4); B's "endangered in a narrow sense" row was more accurate, though INV-E now holds with zero edits to `reviewers.py`. |
| S-007 | Hybrid (C10-R) | 73% | Keep U-001 on fixtures that hold source blocks plus B's T1, T3, T4, M1-M3; T0 only on promotion because no hybrid re-parses an extended line (item (a)). |
| S-008 | Hybrid (C10-R) | 60% | B's C-06 over-limit dependency (`findings_v2.py:111`) and my R-C03 INV-007 note both belong; the quorum helper I named is no longer needed. |
| S-009 | Variant B | 58% | B's numbered tagged evidence table and "Limits" section are easier to audit than inline tags. |
| S-010 | Variant B | 55% | B carried five further objections with OPEN marks; A's single objection plus concessions covered less. |
| X-001 | Variant B | 90% | The cluster record has no severity or category (`cluster.py:352-378`); the repair is a `(reviewer_id, id)` join, with path and line already on the member (`:363`). |
| X-002 | Variant B | 65% | `reviewer_activity` is a literal two-key dict not read from `REVIEWERS`, so A's pin claim holds only for a B that edits it; both are bound by the one-python-fence pins (item (d)). |
| X-003 | Variant B | 93% | 47 `test_*.py` files in `tests/pr_submit`, not 50 [RELIED on Glob in diff-analysis and my R1]. |
| X-004 | Neither (open) | 85% | No test pins the `reviewers` row (the contract-slicing test checks only the `merge_guard` row and heading order, `test_merge_guard_protocol.py:498-508` per B), so an added key or field is equally unpinned. |
| X-005 | Neither (open) | 68% | B10 holds only for an A without a `panel` field; `terminal_clean` is set at eight sites in `fsm.py` and nobody has traced them. |
| X-006 | Variant A | 70% | The bots have no producer of `in_diff` or `confidence` (`classifier.py:443-456` per diff-analysis); `auggie-reviewer.md:54-67` carries two of B's four keys [RELIED]. |
| X-007 | Neither (open) | 75% | `Finding` has no slot for citation flags in either design (`models.py:179-194`), so both read the same sidecar. |
| X-008 | Variant A | 70% | B conceded; with the panel excluded from re-triggers only the name-agnostic absent fold is reusable, and C10-R can emit it too. |
| X-009 | Hybrid (C10-R) | 70% | No review-kernel quorum rule exists (0 matches) and `evaluate_quorum` (`fallback.py:161-179`) is the wrong shape; the strict rule needs none. |
| X-010 | Neither (open) | 65% | `pr_submit` has no hunk parser, so both designs need new diff-aware code; C10-R makes `changed_ranges` an explicit fail-closed input. |

Tally of winners over 49 points: Variant A 9, Variant B 6, Hybrid (C10-R) 16, Neither (open or not a separator) 18.
Round 1 label agreement was 33 of 49 (67.3%); differing points: A-010, A-013, C-001, C-002, C-003, C-005, C-006, C-010, C-011, C-012, C-014, S-001, S-004, S-005, S-008, X-005. Round 2 label agreement is 49 of 49.

## Round 2.5: Invariant Probe (summary; full table in `invariant-probe.md`)

Run by one independent fault-finder agent (not an advocate) against the emerging consensus. Result: 20 findings, 6 ADDRESSED, 14 UNADDRESSED (HIGH 5, MEDIUM 9, LOW 0). HIGH UNADDRESSED: INV-002 (panel standing has no durable home; the 45-member EventType is pinned in three test lines), INV-007 ("requested" defined as the dispatched count), INV-008 (a reviewer that finds nothing is invalid without Coverage rows, so a clean panel cannot read present), INV-011 (the "present" rule is vacuously true for an empty requested set), INV-012 (AM-1 splits by category only; a same-category cluster still pairs the maximum severity with the representative's claim and line). Standard depth has no Round 3, so none of these was debated.

## Convergence Assessment
- Points resolved: 49 of 49 by label (both Round 2 tables name the same superior approach on every S, C, X and A point); 44 of 49 once content is considered (C-001, C-002, C-006, S-004 and S-008 carry the label Hybrid but Variant B attaches amendments AM-1 to AM-6 that Variant A did not answer)
- Alignment: 100% by label; 89.8% content-adjusted (the figure used for the return contract: 0.90)
- Threshold: 80%
- Taxonomy coverage gate: passed (L1 = 4, L2 = 30, L3 = 15 points, all addressed in both rounds)
- Invariant probe gate: BLOCKED by 5 HIGH-severity UNADDRESSED items (INV-002, INV-007, INV-008, INV-011, INV-012); MEDIUM items INV-001, INV-003, INV-006, INV-009, INV-010, INV-014, INV-015, INV-018, INV-019 are warnings
- Status: BLOCKED_BY_INVARIANTS (agreement at or above the threshold, taxonomy covered, HIGH invariants unresolved)
- Unresolved points: C-001, C-002, C-006, S-004, S-008 (content), plus the open owner items C-008, A-005, A-006 (labelled Neither, carried as open by both advocates)
