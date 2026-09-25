---
title: "sc:pr-submit CI-failure phase"
version: "1.0.2"
status: draft
feature_id: PR-SUBMIT-CI
parent_feature: sc-pr-submit
spec_type: component
complexity_score: 0.30
complexity_class: SMALL
target_release: unscheduled
authors: [sc:design]
created: 2026-09-24
sources:
  - src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
  - src/superclaude/pr_submit/fsm.py
  - src/superclaude/pr_submit/classifier.py
  - src/superclaude/pr_submit/models.py
  - .github/workflows/quick-check.yml
  - .github/workflows/test.yml
---

# sc:pr-submit CI-failure phase

## 1. Problem

`sc:pr-submit` remediates Augment Code reviews. After Augment is clean it
emits `TERMINAL_CLEAN` even if GitHub Actions is red. Local VAL (VG-1..VG-6)
already runs the same commands as `quick-check.yml` (pytest, `make lint`
which includes `lint-architecture`, format, `verify-sync`). Remaining CI-only
failures are real: Python matrix (`test.yml` 3.10/3.11/3.12), jobs VAL did
not run, and environment drift.

This spec extends the **existing** monitor. It does not add a skill, FSM,
`--monitor` ordinal, or `EventType` member. `fsm.py` is unchanged.

## 2. Non-goals

- New skill / new FSM / new `--monitor` level.
- Any edit to `fsm.py`, `classifier.py`, or `DetectionContract`.
- New `EventType` members (closed 37; T-N50 / run-log writer).
- Fake `Finding.path` / `line=1` to sneak past `is_groundable`.
- `gh run rerun` (flake retry). A push after a real fix re-runs Actions.
- Auto-fix of human-gate checks (`boundary-guard`, `action_required`).
- Codecov-by-name special case. `gh pr checks --required` is the filter.
- Parallel Augment+CI polling in one script.
- New CLI flags (`--ci-timeout`, `--ci-only`). Reuse `--timeout`; reset the
  wait clock when the source flips to `ci`.
- Re-export from `pr_submit/__init__.py`.

## 3. Design thesis

The FSM events are already generic (`polling` / `clean` / `findings`). The
Augment-specific bits are the **classifier**, **S5a retrigger comment**,
**S5b decline fallback**, and **thread reply/resolve**. CI reuses the loop
and skips those four.

```
source = augment | ci   # SKILL-owned. Not an FSM field.
```

Augment phase unchanged until classify would be `clean`. The SKILL does
**not** send `clean` to `transition()`. It sets `source=ci`, resets elapsed,
swaps the poll script, and keeps `S2_CLASSIFY`. Timeout elapsed resets at
the flip. `fsm.py` never learns `source`.

## 4. Sequence

```mermaid
sequenceDiagram
    participant SKILL
    participant FSM
    participant AugmentPoll as poll-augment-review.sh
    participant CIPoll as poll-ci-checks.sh
    participant VAL
    participant GH as git push origin

    SKILL->>FSM: arm (L1+)
    loop Augment phase (existing)
        SKILL->>AugmentPoll: poll
        AugmentPoll-->>FSM: polling|clean|findings|declined
        alt findings
            FSM->>SKILL: verify → troubleshoot → fix
            SKILL->>VAL: VG-1..VG-6
            alt L3
                SKILL->>GH: push
                SKILL->>SKILL: S5a auggie review comment
            end
        end
    end
    Note over SKILL: Augment clean / REPORT_ONLY / HALT_MAX_ROUNDS → CI wait; cap = wait-only
    SKILL->>SKILL: source=ci, elapsed=0, swap poller
    loop CI phase
        SKILL->>CIPoll: gh pr checks --repo
        CIPoll-->>SKILL: polling|clean|findings
        alt human-gate after Augment HALT_MAX_ROUNDS
            SKILL->>SKILL: retain Augment halt; report CI human-gate alongside it
        else human-gate after Augment clean / REPORT_ONLY
            SKILL->>FSM: HALT_HUMAN (no Finding)
        else findings and budget spent
            SKILL->>SKILL: REPORT_ONLY (no log fetch, edit, or push)
        else findings (parseable file:line, budget left)
            SKILL->>FSM: findings → verify → troubleshoot → fix
            SKILL->>VAL: VG-1..VG-6
            alt L3
                SKILL->>GH: push (retriggers Actions)
                Note over SKILL: skip S5a, S6, RESOLVING
            end
        else findings (unparseable)
            SKILL->>SKILL: REPORT_ONLY (no Finding)
        else clean after Augment HALT_MAX_ROUNDS
            SKILL->>SKILL: retain Augment halt; report CI clean alongside it
        else clean after Augment clean / REPORT_ONLY
            SKILL->>FSM: transition(clean) → TERMINAL_CLEAN
        end
    end
```

```mermaid
stateDiagram-v2
    [*] --> S0_IDLE
    S0_IDLE --> S2_CLASSIFY: arm / G-arm
    S2_CLASSIFY --> S2_CLASSIFY: no_review
    S2_CLASSIFY --> S2_CLASSIFY: SKILL: augment clean → source=ci
    S2_CLASSIFY --> TERMINAL_CLEAN: clean (SKILL only sends this when source=ci)
    S2_CLASSIFY --> S2B_VERIFY: findings
    S2B_VERIFY --> S3_DIAGNOSE: verified
    S2B_VERIFY --> REPORT_ONLY: unverified
    S3_DIAGNOSE --> PROPOSED: G-edit fail
    S3_DIAGNOSE --> S3_FIXING: G-edit
    S3_FIXING --> S7_VALIDATING
    S7_VALIDATING --> S4_HALT_BEFORE_PUSH: G-push fail
    S7_VALIDATING --> S4_PUSHING: G-push
    S4_PUSHING --> S6_REPLYING: FSM unchanged
    note right of S4_PUSHING: SKILL source=ci: push then\nre-poll CI; do not reply/retrigger
    S6_REPLYING --> RESOLVING
    RESOLVING --> S5A_RETRIGGER_REVIEW
    S5A_RETRIGGER_REVIEW --> S5_AWAITING_REREVIEW
    S5_AWAITING_REREVIEW --> S2_CLASSIFY: attributed
```

The SKILL owns the phase flip. `transition()` is untouched: `clean` still
means `TERMINAL_CLEAN`, `pushed` still means `S6_REPLYING`. Production
never sends those events during the CI phase except a final CI `clean` on the non-halted path. After `HALT_MAX_ROUNDS` the FSM remains terminal; CI is an independent SKILL-owned wait with its result reported separately.

CI **wait** starts on Augment `clean`, `REPORT_ONLY`, or `HALT_MAX_ROUNDS`;
the last is wait-only because the shared fix budget is spent. It does **not**
start on `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` /
`TERMINAL_FAILED`. A CI failure after a spent round budget is `REPORT_ONLY`,
never an additional fix or push.

## 5. Functional requirements

| ID | Requirement |
|----|-------------|
| FR-CI-1 | After Augment `clean`, `REPORT_ONLY`, or `HALT_MAX_ROUNDS`, the SKILL sets `source=ci` and polls CI with the same Monitor interval (≥30s) and `--timeout`, elapsed reset. `HALT_MAX_ROUNDS` permits waiting only, not another fix. It calls `transition(..., "clean")` only after CI is clean **and** the Augment FSM did not halt. After `HALT_MAX_ROUNDS`, retain that terminal status and report the CI outcome separately. |
| FR-CI-2 | Poller is `scripts/poll-ci-checks.sh --pr N --repo owner/repo`. Every `gh` call pins `--repo` (T-104). |
| FR-CI-3 | `classify_checks(payload) -> polling \| clean \| findings` lives in `superclaude.pr_submit.ci`. **Not** in `classifier.py`. |
| FR-CI-4 | Mapping: any `bucket=pending` → `polling`; any `fail` or `cancel` → `findings`; only `pass`/`skipping` (or empty checks) → `clean`. Only two successfully parsed empty arrays (required + all checks) mean no Actions configured → `clean`; a failed check query with an empty chosen list is `polling`. `action_required` is a GitHub *conclusion*, not a gh bucket — if `state` matches it (case-insensitive), treat as findings. Do not invent an `action_required` bucket. |
| FR-CI-5 | `cancel` / `state` `action_required` / named human-gate (`boundary-guard`) → SKILL `HALT_HUMAN` on a non-halted Augment path; after `HALT_MAX_ROUNDS`, keep that terminal status and report the CI human-gate separately. **No Finding.** Skip log parse. No auto-fix, no rerun. |
| FR-CI-6 | On non-human `findings`, SKILL fetches failed logs once (`gh run view <id> --repo … --log-failed`). `findings_from_logs` parses pytest (`path:line:`) and ruff (`path:line:col:`) into `Finding(path, line, body)`. Omit `severity_hint` (remap fail-safe is Medium → `--fix`). |
| FR-CI-7 | Unparseable log → **no Finding**. SKILL `REPORT_ONLY`. Do **not** relax `is_groundable`. Do **not** invent `path=name, line=1`. |
| FR-CI-8 | Verified CI findings reuse Waves 3–5 (verify, troubleshoot, VAL, ordinals) only while `round_counter < max_rounds`. Shared budget; after the cap, wait-only CI findings are `REPORT_ONLY`. |
| FR-CI-9 | `source=ci` after L3 push: SKILL skips S5a (`do_retrigger` not called), S6, and RESOLVING. Push retriggers Actions. Re-enter CI poll on the new `headRefOid`. `transition()` is not called for `pushed` on this path. |
| FR-CI-10 | SHA attribution is PR-level: `gh pr view --json headRefOid` in the same script invocation as `gh pr checks`. `gh pr checks --json` has **no per-check SHA** — do not invent a per-check filter. If `head_sha` differs from the SHA this wait started on (the last push, or the SHA at source flip), emit `polling`. |
| FR-CI-11 | `--required` first; if that list is empty, fall back to all checks. That is the optional-check filter. Do not special-case any check by name. |
| FR-CI-12 | No new flags. Operator who needs a longer CI wait passes `--timeout 1800` for the run. Clock reset at source flip is the only timeout change. |

## 6. Invariants

| ID | Invariant |
|----|-----------|
| INV-CI-1 | `EventType` remains exactly 37 members. CI polls emit existing `poll_attempt` / `poll_result` with payload field `source: "ci"`. |
| INV-CI-2 | `classifier.py` and `DetectionContract` are unchanged. |
| INV-CI-3 | `do_retrigger` is not invoked when `source=ci`. |
| INV-CI-4 | NFR-6: `ci.py` has zero `gh`/`git` tokens. All GitHub I/O is in `poll-ci-checks.sh` (and a one-shot log fetch in the SKILL, same as reply scripts). |
| INV-CI-5 | Round tick stays `S5_AWAITING_REREVIEW → S2_CLASSIFY` (INV-001) for the Augment path. CI wait is SKILL-side; a CI `clean` does not tick. |
| INV-CI-6 | G-arm / G-edit / G-push ordinals unchanged. L0 never polls CI. |
| INV-CI-7 | `fsm.py` is byte-identical. SKILL intercepts augment-`clean` and CI push side-effects. No `source` on `transition()` / `RunConfig`. |

## 7. Poll contract

Script: `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh`

```bash
gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid
gh pr checks "$PR" --repo "$REPO" --required --json name,state,bucket,link,workflow
gh pr checks "$PR" --repo "$REPO" --json name,state,bucket,link,workflow
# use nonempty required results; otherwise use all checks
# no `conclusion` field — gh does not emit it
```

Stdout: one JSON line, fail-soft. Two successfully parsed empty check lists → `state:clean` (no Actions); an empty chosen list after a parse failure → `state:polling`.

```json
{
  "pr": 42,
  "head_sha": "abc123",
  "source": "ci",
  "state": "polling",
  "checks": [
    {
      "name": "Quick Test (Python 3.10)",
      "state": "IN_PROGRESS",
      "bucket": "pending",
      "link": "https://github.com/IronbellyOrg/IronClaude/actions/runs/1",
      "workflow": "Quick Check"
    }
  ]
}
```

`bucket` values from `gh pr checks` JSON: `pass` | `fail` | `pending` |
`skipping` | `cancel` ([gh pr checks](https://cli.github.com/manual/gh_pr_checks)).

Authoritative classify is `classify_checks` in `ci.py`, not the script's
coarse `state` (same seam as `poll-augment-review.sh`).

Log fetch (SKILL, only after non-human `findings`):

```bash
gh run view "$RUN_ID" --repo "$REPO" --log-failed
```

`RUN_ID` parsed from `checks[].link` (`/actions/runs/(\d+)`). Missing link →
unparseable (FR-CI-7).

## 8. `ci.py` surface

```python
def classify_checks(payload: dict) -> str:
    """Return polling | clean | findings. Pure. No DetectionContract."""

def is_human_gate(check: dict) -> bool:
    """cancel bucket, state action_required, or name contains 'boundary'."""

def findings_from_logs(checks: list[dict], logs_by_run: dict[str, str]) -> list[Finding]:
    """Parse pytest/ruff file:line. Empty list if none parse (no fake path)."""
```

`_parse_file_line` is a private helper, not part of the public surface.

`Finding` is unchanged. `comment_id=None`. **No `severity_hint`** — remap
fail-safe is Medium → `--fix`. Human-gate and unparseable produce **no**
`Finding`.

Cap parsed findings per run (e.g. 10 unique `path:line`) so a 400-test dump
does not explode troubleshoot dispatch. Existing `batch_by_file` still applies.

## 9. FSM / SKILL delta

**`fsm.py`:** no diff.

**SKILL.md:** Wave 8, lazy-load `refs/ci-poll.md`. After Augment classify
`clean` / `REPORT_ONLY` / `HALT_MAX_ROUNDS`: set source, reset elapsed, swap
poll script, continue Monitor (do not `transition(clean)` for Augment clean).
The spent-budget path is wait-only; L0 never reaches Wave 8.
On human-gate before Augment halts: `HALT_HUMAN`, no Finding. After Augment `HALT_MAX_ROUNDS`: preserve terminal status and report CI human-gate separately.
On CI findings with remaining round budget: log fetch → `findings_from_logs`
→ if empty, `REPORT_ONLY`; else existing Waves 3–5. With spent budget:
`REPORT_ONLY` without log fetch, edit, or push.
On CI push: do not call `retrigger-review.sh`, reply, or resolve. Re-poll CI.

**`state-machine.md`:** document SKILL-owned `source` and the intercept
(augment-clean does not terminate; CI push skips S5a/S6). No new FSM edges.

**`pr-submit.md` command:** one line under Will: "after Augment clean, wait
on PR checks and remediate parseable CI failures under the same ordinals."

## 10. File manifest

| File | Change |
|------|--------|
| `src/superclaude/pr_submit/ci.py` | **New.** `classify_checks`, `is_human_gate`, `findings_from_logs`. Private `_parse_file_line`. Zero `gh`/`git` tokens. Add to T-N50 `CORE_PURE_FILES`. |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` | **New.** T-104 `--repo` pin. |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md` | **New.** Lazy-loaded poll contract. |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | Wave 8. |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` | SKILL-owned `source` + skip S5a/S6. No new edges. |
| `src/superclaude/commands/pr-submit.md` | One Will line. |
| `tests/pr_submit/test_ci_classify.py` | New. Pure tests, fixtures. |
| `tests/pr_submit/fixtures/checks-pending.json` etc. | Three fixtures: pending / pass / fail. |

Do not edit `fsm.py`, `classifier.py`, or `pr_submit/__init__.py`.

`make sync-dev` after skill edits.

## 11. Failure modes

| ID | Case | Behavior |
|----|------|----------|
| FM-CI-1 | No Actions on the repo | Two parsed empty lists → CI `clean`; `TERMINAL_CLEAN` if Augment was not halted, otherwise report CI clean alongside retained `terminal_max_rounds`. |
| FM-CI-2 | Checks pending past `--timeout` | `TERMINAL_TIMEOUT` if Augment was not halted. After `HALT_MAX_ROUNDS`, retain `terminal_max_rounds` and report CI timeout separately. |
| FM-CI-3 | Matrix job fails on 3.12 only | Parse traceback `file:line` → verify → fix. If the defect is version-only and does not reproduce locally, `unverified` → `REPORT_ONLY`. |
| FM-CI-4 | Optional check red, not required | `--required` omits it. If `--required` is empty, all checks count. |
| FM-CI-5 | `boundary-guard` red | SKILL `HALT_HUMAN` before Augment halts; after `HALT_MAX_ROUNDS`, retain that status and report CI human-gate separately. No Finding. |
| FM-CI-6 | Flake, no code change | VAL green + same SHA would still be red after push. Next CI `findings` with same `fix_key` hits existing idempotency / round cap → `HALT_MAX_ROUNDS`. No rerun. |
| FM-CI-7 | Augment already consumed `max_rounds` | CI wait still starts after `HALT_MAX_ROUNDS`, with elapsed reset. CI failures are `REPORT_ONLY` (no more fixes/pushes); pending checks keep polling until completion or timeout. Preserve Augment `terminal_max_rounds` as the FSM/status result and report CI clean, failure, timeout, or human-gate alongside it; do not transition from a terminal state. |

## 12. Implementation plan (strategy for UC-1)

1. Add `ci.py` + three fixtures + `test_ci_classify.py` (**FR-CI-3, FR-CI-4, FR-CI-5, FR-CI-6 parse, FR-CI-7**; **INV-CI-2, INV-CI-4**). Cover: `pending`→polling, `fail`/`cancel`→findings, pass/skipping/empty→clean; `is_human_gate`; parse pytest/ruff; unparseable → `[]`. No `gh`/`git` tokens. Add `ci.py` to T-N50 `CORE_PURE_FILES`.
2. Add `poll-ci-checks.sh` with `--pr`/`--repo`, T-104 pin, fail-soft JSON (**FR-CI-2, FR-CI-10, FR-CI-11**). Same invocation: `gh pr view --json headRefOid` + `gh pr checks --json name,state,bucket,link,workflow` (`--required` first; empty → all checks). Stale `head_sha` vs wait SHA → `polling`. Static grep: no bare `gh`. Do not clone T-105 (`gh api` is not required here).
3. **No `fsm.py` diff** (**INV-CI-7**).
4. `refs/ci-poll.md` + SKILL.md Wave 8 + `state-machine.md` + one command-file Will line (**FR-CI-1, FR-CI-5, FR-CI-6 fetch, FR-CI-7, FR-CI-8, FR-CI-9, FR-CI-12, INV-CI-1 payload `source`, INV-CI-3, INV-CI-5, INV-CI-6**). After Augment `clean` / `REPORT_ONLY` / `HALT_MAX_ROUNDS`: set source, reset elapsed, swap poll script; do not `transition(clean)` from a terminal state. After Augment halt, preserve terminal status and report CI result separately; CI findings are `REPORT_ONLY` with no log fetch/edit/push. Otherwise human-gate → `HALT_HUMAN`, and CI findings: log fetch → `findings_from_logs` → empty → `REPORT_ONLY`; else Waves 3–5. CI push: skip retrigger/reply/resolve. `poll_result` payload may include `source: "ci"` (not a new EventType).
5. `make sync-dev`. `uv run pytest tests/pr_submit/test_ci_classify.py tests/pr_submit/test_run_log.py tests/pr_submit/test_static_grep.py -q`.

Do not add VG-7. `make lint` already runs `lint-architecture`. Do not edit `classifier.py` / `DetectionContract` / `fsm.py`. Do not add EventType members.

## 13. Test plan

| Test | Asserts |
|------|---------|
| `test_classify_pending` | `bucket=pending` → `polling` |
| `test_classify_all_pass` | → `clean` |
| `test_classify_empty` | `checks=[]` without a `polling` hint → `clean`; empty with `state=polling` → `polling` |
| `test_classify_fail` | any `fail` → `findings` |
| `test_classify_cancel` | `bucket=cancel` → `findings` |
| `test_classify_required_fallback` | empty `--required` list → classify the full list |
| `test_is_human_gate` | `boundary` name / `action_required` state / `cancel` bucket → True |
| `test_parse_pytest_line` | `tests/foo.py:12: in test_x` → `Finding(path=..., line=12)` |
| `test_parse_ruff_line` | `src/a.py:3:1: F401` → line 3 |
| `test_unparseable_empty` | no file:line → `findings_from_logs` returns `[]` |
| `test_no_severity_hint` | parsed Finding has `severity_hint is None` |
| `test_event_type_count_unchanged` | existing `test_eventtype_is_37_members_with_v11_events` still 37 |

No `transition()` / `source=` tests. `fsm.py` is not in the diff.

## 14. Skipped (add when)

| Skip | Add when |
|------|----------|
| `--ci-timeout` | Operators actually hit `--timeout` on green-but-slow CI. |
| Parallel Augment+CI poll | Augment wait is routinely longer than CI, so sequential wastes wall clock. |
| `gh run rerun` | A measured flake rate on VAL-green pushes. |
| VG-7 extra architecture gate | `make lint` stops running `lint-architecture`. |
| New skill | This phase grows a second ordinal table or a daemon. Never before. |
| `--resume` restores `source=ci` | Someone actually `--resume`s mid-CI. Until then, a crash during CI restarts Augment poll; operator re-runs. |
| `source` on `RunConfig` / `fsm.py` | A test needs the in-process loop to own the phase. Not before. |
| Codecov-by-name | `--required` is empty *and* optional Codecov is red *and* that happens in practice. |

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-25T01:18:34.308Z","contentHash":"8ec173ff","sections":[{"heading":null,"hash":"fbf508f5"},{"heading":"sc:pr-submit CI-failure phase","hash":"aa15221d"},{"heading":"1. Problem","hash":"89744550"},{"heading":"2. Non-goals","hash":"2b7a3abd"},{"heading":"3. Design thesis","hash":"5a7b6350"},{"heading":"4. Sequence","hash":"b9b5e57e"},{"heading":"5. Functional requirements","hash":"a1c65f64"},{"heading":"6. Invariants","hash":"620968d3"},{"heading":"7. Poll contract","hash":"648be85c"},{"heading":"use nonempty required results; otherwise use all checks","hash":"87b7349a"},{"heading":"no `conclusion` field — gh does not emit it","hash":"af9d90d1"},{"heading":"8. `ci.py` surface","hash":"d570392b"},{"heading":"9. FSM / SKILL delta","hash":"bbb15a86"},{"heading":"10. File manifest","hash":"d849d491"},{"heading":"11. Failure modes","hash":"074bfa0b"},{"heading":"12. Implementation plan (strategy for UC-1)","hash":"66b72c98"},{"heading":"13. Test plan","hash":"ee6f3609"},{"heading":"14. Skipped (add when)","hash":"13d7151b"}]}-->
<!--mc:threads:end-->
