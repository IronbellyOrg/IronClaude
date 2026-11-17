# Reviewer brief 1 — persona: analyzer (model class sonnet, reviewer t1b-1)

## T1 card excerpt

## Findings (Tier 1)

T1-F1 [MAJOR, contradiction] Task 7 pins superseded completion semantics.
Task 7 body says `codex_review_state` has "completion time = `updated_at`" and its AC makes
"two summary comments" classify `polling`. Amendment A1 (design s18) redefines completion as
the LATER of the marker `updated_at` and the newest completing review's `submitted_at`;
amendment A3 makes multiple valid markers resolve to the latest `updated_at` (only same-time
ties poll). An executor following Task 7 verbatim implements both rules wrong and writes
tests asserting the wrong behavior.
citations: plan:91,95 -> spec(design):439-443,452-454

T1-F2 [MAJOR, contradiction] Task 2's second AC asserts A0 reversed.
Plan AC: "A local override YAML without Codex fields still loads (Codex identities empty, so
Codex is disabled for that override)". A0: absent keys FALL BACK to shipped values; only an
explicit empty/null disables. The executor would write a test pinning the wrong semantics.
Ground truth: progress.md records the coordinator overturning exactly this mid-run ("T2:
Ruling: accept T2 F1.1 ... yes-fallback"), and shipped detection.py:157-158 implements A0 —
evidence the contradiction was live, not theoretical.
citations: plan:44 -> spec(design):434-437, progress.md T2 Ruling

T1-F3 [MAJOR, missing requirement] Amendment A6 (root-selection later-of rule) is in no task.
A6 overrides design s7's "created no later than completion" wording after a live PR 337
incident (root stamped 1s after review submission polled to terminal_timeout, 622 s). Task 7
passes "the marker time" to `_thread_findings` — the pre-A6 rule. No task, AC or test item
carries A6. (Shipped classifier.py:321 implements A6; again corrected outside the plan.)
citations: spec(design):467-479 -> plan:91 (absent)

T1-F4 [MINOR, partial] A2's augment-absent-continue rule lacks an AC.
When Augment alone hits TERMINAL_AUGMENT_NO_RESPONSE with Codex present, the run must record
reviewer_absent{augment} and CONTINUE with Codex. Task 12 says only "Wave 1 records
reviewer_absent / reviewer_incomplete"; no AC pins the continue rule or A2's absent-set
input to the wait outcomes (Task 8 signature has no absent-set parameter).
citations: spec(design):445-449 -> plan:102,147

T1-F5 [MINOR, weak AC] Task 15's grep AC cannot enforce its rule.
"`grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md` returns no pr-submit
sentence that omits Codex" — grep returns the matching lines; deciding none is a pr-submit
sentence that omits Codex is judgment, not the grep's exit state. Recurring repo pattern:
grep-count ACs do not gate exact rule text (deviation-patterns, shadow04/shadow06).
citations: plan:182

T1-F6 [MINOR, partial] A5 report/dedup specifics only partially in Task 12.
"flagged by: augment, codex" report line, fix_applied per member fix_key, and "S5 wait covers
only re-triggered reviewers" appear in the design amendment but not in Task 12's bullet list.
citations: spec(design):459-466 -> plan:147
End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:11:33Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md:40-44

```md
Edit src/superclaude/pr_submit/detection.py and the YAML block in src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md per design section 14: `codex_bot_login` (shipped "chatgpt-codex-connector[bot]"), `codex_app_slug` (shipped "chatgpt-codex-connector"), `codex_retrigger_phrase` (default "@codex review"). `from_yaml` trims the identities like the Augment ones. Direct `DetectionContract()` construction keeps both Codex identities empty (fail-safe, same as Augment), while the shipped ref supplies the real values.

Acceptance criteria:
- `DetectionContract.load()` returns the two Codex identities and the "@codex review" phrase; `DetectionContract()` has empty Codex identities.
- A local override YAML without Codex fields still loads (Codex identities empty, so Codex is disabled for that override) and existing tests in tests/pr_submit/test_detection_contract.py pass.
```

### .dev/pr-submit-codex/design/pr-submit-codex-design.md:427-479

```md
## 18. Amendments from the plan review (coordinator-approved 2026-10-31)

Source: the pre-execution plan review in
`.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/reflect-pre/adversarial/merged-verdict.yaml`
(finding ids M-NN). Approved by the Orca coordinator on 2026-10-31. These sections override any
earlier text they contradict. Each amendment is pinned by at least one test in `tests/pr_submit/`.

- **A0 (M-05, Task 2 Ruling).** Section 14's Codex contract fields use key-presence semantics in
  `DetectionContract.from_yaml`: an absent `codex_bot_login` / `codex_app_slug` falls back to the
  shipped value, so an override written by contract setup keeps Codex on; an explicit empty or
  null value disables Codex. Direct `DetectionContract()` construction keeps them empty.
- **A1 (M-01, M-03).** Codex completion time is the later of (a) the summary comment's
  `updated_at` and (b) the `submitted_at` of the newest Codex formal review whose commit is the
  expected head, when such a review exists. Both must be parseable aware times no later than
  `observed_at`; the watermark test (strictly newer) uses this later time. `_thread_findings`
  receives it through an explicit keyword `completed_at`, so a Codex root created after the
  marker edit but no later than the review submission is still selected.
- **A2 (M-02, M-09, M-24).** The wait outcomes take the set of reviewers already absent as an
  input: a reviewer in that set, or a reviewer whose identity set is empty, is `absent` at once
  and is never `pending`. When Augment's own silence outcome (`TERMINAL_AUGMENT_NO_RESPONSE`)
  fires while Codex is present, the run records `reviewer_absent{reviewer: "augment"}` and
  continues through `merge_wait` with Codex; it does not stop at that outcome. Only when both
  reviewers are absent does the run end `terminal_augment_no_response`.
- **A3 (M-10).** When several Codex summary comments carry a valid `codex-review-state:v1`
  marker, the one with the latest `updated_at` is used (as Augment uses its latest review); two
  distinct markers with the same latest time are ambiguous and stay `polling`.
- **A4 (M-06, M-07, M-08, M-11).** Each re-trigger POST is recorded as
  `rereview_requested{cycle_id, reviewer, timestamp}` where `timestamp` is the UTC time taken
  right after that reviewer's successful POST. On `--resume` the per-reviewer watermark is the
  `timestamp` of that reviewer's latest `rereview_requested` for the cycle; the resume reuses the
  `cycle_id` of the dangling push record (never a new one); and every resume at S5a or S5 of a
  re-triggered cycle first calls `pending_retriggers` and posts the reviewers still missing.
- **A5 (M-12, M-13, M-14, M-16, M-27).** The SKILL text states explicitly the rules already in
  sections 6, 9, 13 and 5: a dedup group routes at its members' highest remapped tier, is
  diagnosed and fixed once with `fix_applied` recorded for every member's `fix_key`, and every
  verified member's thread is replied to and resolved; the report shows "flagged by"; the S5
  wait covers only the re-triggered reviewers, is attributed when at least one reaches `done`
  on the pushed SHA, and records `reviewer_incomplete{phase: "rereview"}`; S5b fallback
  re-entry includes the merged Codex findings; the nine events of section 13 carry `reviewer`;
  and resume reads `rebuild_state()["absent_reviewers"]`.
- **A6 (PR 337 live run, 2026-10-31).** On PR 337 Augment's review was submitted at 21:22:29Z and
  its only root comment was stamped 21:22:30Z, so the rule "a root created after completion means a
  newer review is still running" polled until `terminal_timeout` (622 s). For root selection the
  completion time of either reviewer is therefore the later of (a) the completion time above
  (Augment: the completed review's `submitted_at`; Codex: A1) and (b) the `createdAt` of the
  reviewer's own roots whose `pullRequestReview` is a completing formal review (same review id, every
  commit equal to that review's commit). For Augment the completing review is the selected latest
  review; for Codex it is each Codex formal review on the expected head. A newer root from any other
  review, or from an older head, still polls. The fix is in `_thread_findings`, shared by both
  reviewers; the attribution rules (submission strictly newer than the watermark, no later than
  `observed_at`) are unchanged. Overrides the "created no later than completion" wording in
  section 7. Pinned by `tests/pr_submit/test_cosmos_review.py::test_a6_*` (verbatim PR 337 snapshot
  `fixtures/cosmos-pr337.json`) and `test_codex_reviews.py::test_a6_*`.
```

### .dev/tasks/done/TASK-WF-implementTheDesi-20261031-182028/progress.md:12-13

```md
T4: complete verdict=compliant ac=T4.AC1,T4.AC2 evidence=T4.AC1@src/superclaude/pr_submit/classifier.py:299,T4.AC1@./artifacts/t4-test.log:53,T4.AC2@src/superclaude/pr_submit/classifier.py:320,T4.AC2@./artifacts/t4-check.log:3 extras=lint:pass,typecheck:skip,test:pass files=src/superclaude/pr_submit/classifier.py
T5: start sha=4dbc1d1a24209823d68b72ac423d79376ab92c0f
```

### src/superclaude/pr_submit/detection.py:150-175

```python
        Codex keys use key-presence semantics: an absent key falls back to the
        shipped Codex value; a present empty or null value blanks that identity.
        Codex is disabled only when both Codex identities are blank; it stays on
        while either remains.
        """
        data = data.copy()
        for key, shipped in (
            ("codex_bot_login", _SHIPPED_CODEX_BOT_LOGIN),
            ("codex_app_slug", _SHIPPED_CODEX_APP_SLUG),
        ):
            if key not in data:
                data[key] = shipped
        for key in (
            "augment_bot_login",
            "augment_app_slug",
            "codex_bot_login",
            "codex_app_slug",
        ):
            if isinstance(data.get(key), str):
                data[key] = data[key].strip()
        for key in ("codex_bot_login", "codex_app_slug"):
            if not data.get(key):
                data[key] = None
        phrase = data.get("codex_retrigger_phrase")
        if not isinstance(phrase, str) or not phrase.strip():
            phrase = _DEFAULT_CODEX_RETRIGGER_PHRASE
```

### src/superclaude/pr_submit/classifier.py:318-375

```python
def _completion_time(
    threads: list, identities: set[str], reviews: list[dict], completed_at: Any
) -> Any:
    """The later of ``completed_at`` and the creation of the reviewer's own roots
    that belong to one of the completing ``reviews`` on that review's commit
    (design section 18, A6: a root posted seconds after its review's submission
    is part of that review, not a sign of a newer one)."""
    if completed_at is None:
        return None
    latest = completed_at
    for review in reviews:
        keys = _review_keys(review)
        heads = {_sha(c) for c in _review_commits(review)} - {None}
        if not keys or not heads:
            continue
        for thread in threads:
            connection = thread.get("comments") if isinstance(thread, dict) else None
            nodes = connection.get("nodes") if isinstance(connection, dict) else None
            if not isinstance(nodes, list) or not nodes:
                continue
            root = nodes[0]
            origin = root.get("pullRequestReview") if isinstance(root, dict) else None
            if not isinstance(origin, dict) or _login_of(root) not in identities:
                continue
            commits = _review_commits(origin)
            if (
                not commits
                or any(_sha(c) not in heads for c in commits)
                or not keys & _review_keys(origin)
            ):
                continue
            created = _timestamp(_entry_ts(root))
            if created is not None and created > latest:
                latest = created
    return latest


def _thread_findings(
    threads: Any,
    contract: Any,
    completed: dict | None,
    identities: set[str] | None = None,
    *,
    completed_at: Any = None,
    reviews: list[dict] | None = None,
) -> list[dict] | None:
    """Return roots only, or None if an unresolved source cannot be safely selected.

    Current-null/original-only locations stay hints. Resolution is authoritative;
    neither outdated state nor the re-trigger watermark discards an open root.
    ``identities`` selects whose roots count (default: the Augment identities).
    ``completed_at`` overrides the completion time otherwise read from the
    ``completed`` review's submission time (Codex passes its marker-derived time).
    ``reviews`` are the completing formal reviews (default: ``[completed]``); the
    creation times of their own roots extend the completion time (A6).
    """
    if not isinstance(threads, list):
        return None
```

## Coverage slice

  - id: INF-002 source: inferred  req: "A0 override key-presence semantics"             task: T2      status: CONTRADICTED (plan AC asserts the reverse)
    quote: "an absent codex_bot_login / codex_app_slug falls back to the shipped value ... an explicit empty or null value disables Codex"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:434-437
  - id: INF-003 source: inferred  req: "A1 completion = later of marker updated_at and completing review submitted_at"   task: none    status: CONTRADICTED (Task 7 pins pre-A1 'completion time = updated_at')
    quote: "Codex completion time is the later of (a) the summary comment's updated_at and (b) the submitted_at of the newest Codex formal review whose commit is the expected head"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:439-443
  - id: INF-004 source: inferred  req: "A3 multiple valid markers: latest updated_at wins; only same-time ties poll"     task: none    status: CONTRADICTED (Task 7 AC pins 'two summary comments -> polling')
    quote: "the one with the latest updated_at is used ... two distinct markers with the same latest time are ambiguous and stay polling"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:452-454
  - id: INF-005 source: inferred  req: "A2 absent-set input; Augment no-response with Codex present records absent and continues"   task: partial (T8 lacks absent-set input; T12 records the event but no AC pins the continue rule)   status: partial
    quote: "a reviewer in that set, or a reviewer whose identity set is empty, is absent at once ... it does not stop at that outcome"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:445-449
  - id: INF-006 source: inferred  req: "A4 per-reviewer POST timestamp watermark; resume reuses dangling cycle_id; pending_retriggers at every resume"   task: T9,T12 (resume cycle_id reuse unstated)   status: covered-partial
    quote: "On --resume the per-reviewer watermark is the timestamp of that reviewer's latest rereview_requested for the cycle; the resume reuses the cycle_id of the dangling push record"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:454-458
--
  - "INF-003 (A1) contradicted by Task 7 text"
  - "INF-004 (A3) contradicted by Task 7 AC"
  - "INF-008 (A6) absent from every task"
  - "INF-005 (A2) partial: augment-absent-continue rule has no AC"
notes: >-
  Section 18 amendments are dated 2026-10-31 (coordinator-approved after this plan was
