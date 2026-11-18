# Reviewer brief 3 — persona: refactorer (model class opus, reviewer t1a-1)

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

## Best-practice grade

4/5. Phase structure, per-task ACs with named evidence paths, dependency graph, and the
constraint block are all strong. Deduction: ACs that assert superseded semantics (T1-F1/F2)
are worse than missing ACs because they pin wrong behavior as "done".
End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:11:33Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/pr-submit-codex/design/pr-submit-codex-design.md:298-340

```python
## 14. Interfaces (new and changed)

All in the pure core (no `gh`/`git` tokens, NFR-6 / T-N50 purity kept).

```python
# pr_submit/detection.py — DetectionContract gains (defaults baked, YAML-overridable):
codex_bot_login: str | None = "chatgpt-codex-connector[bot]"
codex_app_slug: str | None = "chatgpt-codex-connector"
codex_retrigger_phrase: str = "@codex review"
# DetectionContract() direct construction keeps EMPTY identities for both reviewers (fail-safe).

# pr_submit/classifier.py — generalised, Augment behaviour unchanged:
def _thread_findings(threads, contract, completed, identities=None) -> list[dict] | None
def has_reviewer_activity(payload, identities: set[str]) -> bool

# pr_submit/reviewers.py — new
REVIEWERS = ("augment", "codex")
def reviewer_identities(contract, reviewer: str) -> set[str]
def retrigger_phrase(contract, reviewer: str) -> str
def reviewer_activity(payload, contract) -> dict[str, bool]
def parse_codex_priority(body: str) -> str | None            # "P0".."P3" or None
def codex_severity_hint(priority: str | None) -> str | None  # critical/high/medium/low
def codex_review_state(payload, contract, *, watermark=None, current_head_sha=None) -> dict | None
def classify_codex(payload, contract, *, watermark=None, current_head_sha=None) -> str
def codex_finding_comments(payload, contract, *, watermark=None, current_head_sha=None) -> list[dict]
def codex_wait_outcome(state, *, active, elapsed, timeout, silence_timeout, other_settled) -> str
def augment_wait_outcome(state, next_state) -> str
def merge_wait(augment: tuple[str, str], codex: tuple[str, str]) -> dict
#   -> {"outcome": "polling"|"clean"|"findings"|"declined"|"no_response"|"timeout",
#       "used": [...reviewers], "absent": [...], "incomplete": [...]}
def dedup_groups(findings: list[Finding]) -> list[list[Finding]]
def list_review_threads(payload, contract) -> list[dict]     # all bot threads, any state, for reports
def pending_retriggers(run_log_events: list[dict], cycle_id, present: list[str]) -> list[str]

# pr_submit/models.py
Finding.reviewer: str = "augment"
EventType.REVIEWER_ABSENT = "reviewer_absent"; EventType.REVIEWER_INCOMPLETE = "reviewer_incomplete"

# pr_submit/run_log.py — rebuild_state: rereview_request_count by distinct cycle_id;
#   new "absent_reviewers" list folded from reviewer_absent.
```

SKILL snapshot gate (normative, extends the existing block):
```

### .dev/pr-submit-codex/design/pr-submit-codex-design.md:341-350

```python

```python
aug = existing gate (unchanged)                       # review_state, findings, routes
cx_state = classify_codex(payload, contract, watermark=wm.get("codex"), current_head_sha=expected_head)
cx_roots = codex_finding_comments(...same args...) if cx_state == "findings" else []
# same normalization rule: empty selection or ValueError -> cx_state = "polling"
decision = merge_wait((augment_wait_outcome(review_state, nxt), review_state),
                      (codex_wait_outcome(cx_state, ...), cx_state))
```

```

### src/superclaude/pr_submit/reviewers.py:380-470

```python
    (A2). A Codex with no activity is absent as soon as Augment is settled or at the
    silence deadline; an active Codex with no completion is ``incomplete`` at
    ``--timeout``.
    """
    if absent:
        return WAIT_ABSENT
    if state in (STATE_CLEAN, STATE_FINDINGS):
        return WAIT_DONE
    if active:
        return WAIT_INCOMPLETE if elapsed >= timeout else WAIT_PENDING
    if other_settled or elapsed >= min(silence_timeout, timeout):
        return WAIT_ABSENT
    return WAIT_PENDING


def merge_wait(augment: tuple[str, str], codex: tuple[str, str]) -> dict:
    """Merge per-reviewer ``(wait_outcome, gate_state)`` pairs into one round outcome.

    ``outcome`` is ``polling`` / ``clean`` / ``findings`` / ``declined`` /
    ``no_response`` / ``timeout``; ``used`` names the reviewers whose results the
    outcome uses, ``absent`` / ``incomplete`` the others (design section 6 table).
    """
    pairs = {"augment": augment, "codex": codex}
    absent = [name for name, (out, _) in pairs.items() if out == WAIT_ABSENT]
    incomplete = [name for name, (out, _) in pairs.items() if out == WAIT_INCOMPLETE]
    done = [(name, st) for name, (out, st) in pairs.items() if out == WAIT_DONE]
    result = {
        "outcome": STATE_POLLING,
        "used": [],
        "absent": absent,
        "incomplete": incomplete,
    }
    if any(out == WAIT_PENDING for out, _ in pairs.values()):
        return result
    result["used"] = [name for name, _ in done]
    if augment == (WAIT_DONE, STATE_DECLINED):
        result["outcome"] = STATE_DECLINED
    elif done:
        findings = any(st == STATE_FINDINGS for _, st in done)
        result["outcome"] = STATE_FINDINGS if findings else STATE_CLEAN
    elif len(absent) == len(pairs):
        result["outcome"] = "no_response"
    else:
        result["outcome"] = "timeout"
    return result


# --- cross-reviewer dedup and re-trigger bookkeeping (design sections 9 and 12) ---


def dedup_groups(findings: list) -> list[list]:
    """Group findings by ``(path, line)``, using ``original_line`` when ``line`` is None.

    Input order is kept and every finding is kept: a group of two means Augment and
    Codex (or two findings) flagged the same place; each keeps its own verdict.
    """
    groups: dict[tuple, list] = {}
    for finding in findings:
        line = finding.line if finding.line is not None else finding.original_line
        groups.setdefault((finding.path, line), []).append(finding)
    return list(groups.values())


def pending_retriggers(
    events: list[dict], cycle_id: Any, present: list[str]
) -> list[str]:
    """Present reviewers with no ``rereview_requested`` for ``cycle_id`` yet.

    An event without ``reviewer`` counts as augment (logs written before Codex).
    """
    posted = {
        ev.get("reviewer") or "augment"
        for ev in events
        if isinstance(ev, dict)
        and ev.get("event_type") == EventType.REREVIEW_REQUESTED.value
        and ev.get("cycle_id") == cycle_id
    }
    return [name for name in present if name not in posted]
```

### src/superclaude/pr_submit/run_log.py:170-200

```python

        Reconstructs the FSM state, ``round_counter``, the 7 idempotency sets, and
        ``push_count``/``reply_count`` from the event stream. This is the source of
        truth on any snapshot/JSONL disagreement.

        ``rereview_request_count`` counts re-triggered push cycles: one cycle may
        post an Augment and a Codex re-trigger comment, so ``rereview_requested``
        events are folded by distinct ``cycle_id`` (an event without ``cycle_id``
        still counts once each, so old logs rebuild to the same number).
        ``absent_reviewers`` is the sorted set of reviewers named by
        ``reviewer_absent`` events.

        Issue #305 (conflict cycles and push kinds) adds four keys:

        - ``sync_push_count``: landed ``push_completed`` events with ``kind ==
          "sync"``. Such pushes do NOT count in ``push_count``; every other kind
          (``fix``, ``merge``, ``ci``, or absent, which means ``fix``) does.
        - ``conflict_cycles``: the distinct ``cycle_id`` values of ``sync_started``
          events in first-seen order (not sorted); a resume restart that re-opens
          the same id is counted once.
        - ``open_conflict_cycle``: the open cycle whose ``sync_started`` came last,
          or ``None``. A cycle opens on ``sync_started`` (the entry is the event's
          payload, so it carries ``hook``, ``review_terminal``, ``kind``,
          ``base_sha`` and ``pre_push_sha``, plus the flags ``push_initiated``,
          ``push_completed`` and ``superseded`` and the ``target_sha`` and
          ``expect_checks`` copied from its ``push_initiated``) and closes on
          ``sync_concluded``. A missing or non-bool ``expect_checks`` is stored as
          ``True`` (fail closed). A ``push_initiated`` of any other cycle marks
          every still-open cycle ``superseded``.
        - ``push_rejected``: ``True`` once a ``push_aborted_or_not_landed`` event
          carries ``rejected is True``.
```

### tests/pr_submit/test_run_log.py:168-178

```python
# --- V1.1 closed-enum count + new-event folds (addendum §6.1/§6.3) ------------


def test_eventtype_is_45_members_with_silence_reviewer_conflict_and_guard_events():
    """The closed EventType enum has EXACTLY 45 members, including INV-S1, the two
    reviewer-presence events, the two conflict-cycle events and the two merge-guard
    events."""
    assert len(EventType) == 45
    assert len(list(EventType)) == 45
    assert EventType.DRAFT_GUARD_REQUESTED.value == "draft_guard_requested"
    assert EventType.DRAFT_GUARD_SETTLED.value == "draft_guard_settled"
```

## Coverage slice

  - id: D-04    source: parsed    req: "design s4 adapter table + reviewer-agnostic path"            task: T6      status: covered
  - id: D-05    source: parsed    req: "design s5 reviewer detection + fail-open absence"            task: T8,T12  status: covered
  - id: D-06    source: parsed    req: "design s6 one-round polling + merge truth table"             task: T7,T8   status: covered
  - id: D-07    source: parsed    req: "design s7 Codex parsing + P0-P3 mapping"                     task: T6,T7   status: covered
  - id: D-08    source: parsed    req: "design s8 re-grade/verify/dispatch reused, wording only"     task: T13     status: covered
  - id: D-09    source: parsed    req: "design s9 cross-reviewer dedup groups"                       task: T9,T13  status: covered
  - id: D-10    source: parsed    req: "design s10 reply/resolve wording"                            task: T11     status: covered
  - id: D-11    source: parsed    req: "design s11 per-reviewer re-trigger + watermark"              task: T12,T14 status: covered
  - id: D-12    source: parsed    req: "design s12 loop guard + distinct-cycle count"                task: T3,T9   status: covered
  - id: D-13    source: parsed    req: "design s13 events name reviewer + output reviewers field"    task: T1,T12  status: covered
  - id: D-14    source: parsed    req: "design s14 interfaces incl. detection contract fields"       task: T2,T6   status: covered
  - id: D-16    source: parsed    req: "design s16 test matrix items 1-8"                            task: T10,T11 status: covered
