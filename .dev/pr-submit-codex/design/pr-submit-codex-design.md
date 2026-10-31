# Design: /sc:pr-submit handles Codex review threads like Augment

- Command: `/sc:design pr-submit-codex-reviews --type component --format spec`
- Date: 2026-10-31
- Branch: `feat/pr-submit-codex-reviews`
- Status: complete (validated against the code read in section 3 and the PR 334/335/336 data in section 2)

## 1. Problem and goal

`/sc:pr-submit` (command `src/superclaude/commands/pr-submit.md`, skill
`src/superclaude/skills/sc-pr-submit-protocol/`, deterministic core `src/superclaude/pr_submit/`)
only polls, verifies, fixes, replies to and resolves review threads from Augment
(`augmentcode[bot]` / `augmentcode`). On PRs 335 and 336 the ChatGPT Codex Connector bot left five
P2 review threads that the monitor never saw, so they were fixed by hand.

Goal: Codex review threads go through exactly the same path as Augment threads: detect, poll,
classify, re-grade, verify, diagnose, fix (Medium or higher), validate, push, reply, resolve,
re-trigger, loop-guard. Low and Nit stay report-only. Augment-only PRs behave exactly as today;
Codex-only PRs work; PRs with neither reviewer end as today.

Non-goals: Codex "security review" results, Codex answering questions or editing the PR
(`@codex address that feedback`), any other review bot.

Scope note: the deterministic core `src/superclaude/pr_submit/` is part of the skill (SKILL.md
defers every classification decision to it and forbids a second body parser), so the Codex parser
lives there, not in the markdown or the bash scripts.

## 2. Evidence: what Codex actually posts (observed on PRs 334, 335, 336)

Read with `gh api graphql` and `gh api repos/IronbellyOrg/IronClaude/...` on 2026-10-31.

| Surface | Observed shape |
|---|---|
| Author | REST `user.login` = `chatgpt-codex-connector[bot]` (`type: Bot`); GraphQL `author.login` = `chatgpt-codex-connector`. Same two-shape pattern as Augment. |
| Summary issue comment | One PR conversation comment created seconds after the PR opens and **edited in place** (`created_at` 14:38:21, `updated_at` 14:40:37 on PR 335). Body starts `<!-- codex-pull-request-review-summary -->` then `<!-- codex-review-state:v1 {JSON} -->`. JSON: `{"code_review":{"commit_sha":"<40 hex>","has_any_findings":bool,"has_unresolved_findings":bool,"status":"completed"},"security_review":{...}}`. |
| Clean review | PR 334: summary with `code_review.status:"completed"`, `has_any_findings:false`; **no formal review, no review thread, and no visible reaction**. The marker is the only completion evidence. |
| Review with findings | One formal review (`state: COMMENTED`, `commit_id` = reviewed head) whose body starts `<!-- codex-review-receipt:v1 -->` and `### 💡 Codex Review`, plus one inline root comment per finding, each the root of its own review thread (`pull_request_review_id` set, `in_reply_to_id` null, `line` null once outdated, `original_line` set). |
| Finding body | First line: `**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  <title>**`, then prose, then `Useful? React with 👍 / 👎.`, then `<!-- codex-code-review-finding:v1 -->`. Only P2 (yellow) occurs in this repo's history; P0, P1, P3 colours were not observed. |
| Stale marker | After the five threads were resolved, `has_unresolved_findings` still read `true`: the summary is not updated on resolve, so threads (not the marker) are the source of truth for open findings. |
| Re-review on push | Not observed: PRs 334, 335, 336 each got one Codex review ("Review trigger: PR opened") although later commits were pushed. |
| Documented triggers | The bot's own text: "Reviews are triggered when you open a pull request for review, mark a draft as ready, comment "@codex review"". OpenAI docs (https://learn.chatgpt.com/docs/third-party/github): "In a pull request comment, mention `@codex review`", and an optional "Automatic review" setting. |

## 3. Current system (read before designing)

- **Poll script** `scripts/poll-augment-review.sh`: one repo-pinned snapshot (PR metadata, REST
  reviews, REST issue + inline comments, GraphQL review threads with root comment, author,
  `pullRequestReview{commit{oid}}`), completeness flags, `observed_at`. It is already
  reviewer-neutral in what it fetches: Codex's summary comment, review and threads are all in the
  snapshot today. Nothing in it filters by author.
- **Classifier** `pr_submit/classifier.py`: `classify` / `actionable_finding_comments` share one
  selection; identities come only from `contract.augment_bot_login` / `augment_app_slug`.
  `_thread_findings` selects unresolved roots authored by those identities, validated against a
  completion review time. Cosmos completion uses a validated HTML-comment JSON marker.
- **Severity** `pr_submit/severity_router.py`: `finding_from_comment` (explicit `severity_hint`
  wins, else one `**Severity:**` line, else Medium fail-safe) → `remap_severity` → `route`
  (Critical/High `--depth deep --fix`, Medium `--fix`, Low/Nit report-only).
- **FSM** `pr_submit/fsm.py`: `poll_outcome` (Augment silence/timeout), `transition` table,
  INV-001 increment at `S5_AWAITING_REREVIEW → S2_CLASSIFY` on `rereview_attributed`.
- **Run log** `pr_submit/run_log.py`: closed `EventType` enum (39 members), `rebuild_state`
  folds `rereview_requested` as a plain count (INV-R1: `rereview_request_count <= max_rounds`).
- **Recovery** `pr_submit/recovery.py`: a landed push resumes at S5a unless a
  `rereview_requested` event exists for that `cycle_id`.
- **Reply/resolve** `scripts/reply-resolve-thread.sh`: identifies the thread by root
  `databaseId` (optionally `--thread-id`), replies, then `resolveReviewThread`. The logic is
  author-independent; only its header wording says "Augment".
- **Re-trigger** `scripts/retrigger-review.sh`: one issue-comment POST, body defaults to
  `auggie review`, already parameterised by `--body`.
- **Detection contract** `refs/detection-contract.md` YAML + `DetectionContract` dataclass:
  Augment identities and decline regexes; optional local override.
- **Plugin twins**: `plugins/superclaude/` has no pr-submit command or skill, so the mirror rule
  has nothing to update here (checked with `find plugins -iname '*pr-submit*'`: no result).

## 4. Design overview: one reviewer-agnostic path, one small adapter per reviewer

The snapshot is already shared (one poll per round covers both bots). What differs per reviewer
is only: who the author is, how completion is proven, how severity is read, and what comment asks
for a re-review. Everything after "a list of normalized `Finding` objects" is already
reviewer-agnostic and is reused unchanged.

```text
poll-augment-review.sh  (one snapshot, unchanged data)
        │
        ├── augment adapter: classify / actionable_finding_comments   (existing, unchanged)
        └── codex adapter:   classify_codex / codex_finding_comments  (new, same gate rules)
        │
merge_wait()  ── per-reviewer wait outcome → one round outcome (pure truth table)
        │
dedup_groups() ── group same path+line across reviewers
        │
finding_from_comment → remap_severity → route        (existing; Codex sets severity_hint)
evidence-validator → troubleshoot → fix → VAL         (existing)
push triad → reply-resolve-thread.sh per thread       (existing script, wording generalised)
retrigger-review.sh per present reviewer              (existing script, --body per adapter)
```

Adapter table (new module `pr_submit/reviewers.py`), values read from the detection contract so a
local override can change or blank them:

| Field | augment | codex |
|---|---|---|
| identities | `augment_bot_login`, `augment_app_slug` | `codex_bot_login` (`chatgpt-codex-connector[bot]`), `codex_app_slug` (`chatgpt-codex-connector`) |
| completion proof | formal review / Cosmos marker (existing) | `codex-review-state:v1` marker, `code_review.status == "completed"` for the expected head |
| severity | `severity_hint` / `**Severity:**` line (existing) | P0-P3 badge on the first line (section 7) |
| re-trigger body | `auggie review` (existing) | `codex_retrigger_phrase` = `@codex review` |
| silence poke | yes, L3, once (existing INV-S1) | no (section 5) |
| decline | "abnormally large" (existing) | none |

A blank identity set disables that reviewer (it is never present). No new provider abstraction
beyond this table: two reviewers, one dict, no class hierarchy.

## 5. Reviewer detection and fail-open

A reviewer is **present** on the PR when the snapshot holds at least one entry authored by its
identities (a review, an issue or inline comment, or a thread root):
`reviewer_activity(payload, contract) -> {"augment": bool, "codex": bool}`.

- Codex posts its summary comment seconds after a PR opens, long before any review (Augment's
  reviews on PRs 335/336 took about 4-5 minutes), so a connected repository shows Codex activity
  within the first polls. Codex with no activity when Augment's wait outcome is already settled,
  or by the silence deadline (`--silence-timeout`, default 300 s), is **absent**: the run appends
  `reviewer_absent{reviewer:"codex"}` and ignores Codex for the rest of the run (no wait, no
  re-trigger). There is no Codex silence poke: posting `@codex review` on a repository without the
  Codex connector only produces an error reply, and absence here means "not installed".
- Augment keeps its existing silence path unchanged (optional single L3 poke, then
  `TERMINAL_AUGMENT_NO_RESPONSE` when it alone decides the run). When Augment reaches that
  silence outcome but Codex is present, Augment is recorded absent (`reviewer_absent{reviewer:
  "augment"}`) and the round continues with Codex alone.
- Absence is sticky and rebuilt from the run log on `--resume` (`rebuild_state()["absent_reviewers"]`).
- Neither reviewer present: unchanged `TERMINAL_AUGMENT_NO_RESPONSE` (status value kept for
  compatibility; its message now says "no configured reviewer (Augment, Codex) responded").

Augment-only PR: Codex becomes absent no later than the poll on which Augment settles (or at
the silence deadline if Augment is still pending), so the wait never runs longer than today and
every Augment outcome, status and event is the same as today plus one `reviewer_absent` event. Codex-only PR: Augment's silence outcome marks it absent; Codex's
result drives the round.

## 6. Polling both reviewers in one round, and the terminal conditions

Each poll runs the existing Augment snapshot gate and, on the same snapshot with the same
`expected_head`, the Codex gate. Each reviewer gets a **wait outcome**:

| Wait outcome | augment (from existing gate + `poll_outcome`) | codex (`codex_wait_outcome`) |
|---|---|---|
| `pending` | `polling` and `poll_outcome` is `S2_CLASSIFY` or `S5C_SILENCE_REREQUEST` | no completion yet, and (active, not timed out) or (inactive, before silence deadline, and Augment not settled) |
| `done` | gate state `clean` / `findings` / `declined` | gate state `clean` / `findings` |
| `absent` | `TERMINAL_AUGMENT_NO_RESPONSE`, or already absent | inactive at silence deadline, or already absent |
| `incomplete` | `TERMINAL_TIMEOUT` (partial activity) | active but no completion at `--timeout` |

`merge_wait(augment, codex)` (pure, row-tested) maps the pair to the round outcome:

| augment | codex | round outcome |
|---|---|---|
| `pending` | any | keep polling |
| any | `pending` | keep polling |
| `done: declined` | any settled | `declined` (existing S5b fallback; Codex `findings` join the fallback's single Waves 2-6 re-entry) |
| `done` | `done` | `findings` if either has findings, else `clean` |
| `done` | `absent` / `incomplete` | Augment's state (Codex incomplete is reported) |
| `absent` / `incomplete` | `done` | Codex's state (Augment's condition is reported) |
| `absent` | `absent` | `TERMINAL_AUGMENT_NO_RESPONSE` (unchanged) |
| `incomplete` | `absent` / `incomplete` | `TERMINAL_TIMEOUT` (unchanged) |
| `absent` | `incomplete` | `TERMINAL_TIMEOUT` (partial reviewer activity, no classified review) |

Both reviewers share the one `--timeout` wall clock and one `--poll-interval`; no second wait is
added. In the S5 re-review wait only reviewers that were re-triggered in this cycle are waited
for; a reviewer that is `incomplete` at S5 expiry is reported and the other's attributed result
is used. The re-review is **attributed** (the INV-001 edge) when at least one re-triggered
reviewer reaches `done` (clean or findings) attributed to the pushed SHA; `timeout` when none
does; `declined` when Augment declines (existing).

## 7. Parsing Codex findings and mapping P0-P3 onto severity routing

**Completion** (`codex_review_state(payload, contract, expected_head, watermark)`): exactly one
issue comment authored by a Codex identity carries one `<!-- codex-review-state:v1 {JSON} -->`
marker (bounded length, JSON object, duplicate keys rejected, same as the Cosmos marker). Valid
when `code_review.status` is a string, `code_review.commit_sha` is 40 hex,
`code_review.has_any_findings` is a boolean. Completed only when `status == "completed"`,
`commit_sha == expected_head`, the comment's `updated_at` is a parseable aware time no later than
`observed_at`, and (with a watermark) strictly newer than the watermark. Anything else (two
summary comments, malformed JSON, `running`, wrong head, missing time) is `polling`, never clean.
The `security_review` object is ignored.

**Findings** (`codex_finding_comments`): unresolved review threads whose root is Codex-authored,
selected by the existing `_thread_findings` rules generalised to take an identity set and a
completion time (root-only, unique ids, `pullRequestReview` with a commit, nullable current
line, `original_line` hint, created no later than completion). Resolved threads are excluded;
older unresolved Codex roots stay visible (same as Augment).

**Codex gate state**: completion missing → `polling`; selection invalid → `polling`; unresolved
roots → `findings`; none and `has_any_findings` false → `clean`; none, `has_any_findings` true
and a Codex formal review exists for the expected head (its threads were all resolved) → `clean`;
otherwise `polling` (findings promised but not yet visible).

**Badge parser** (`parse_codex_priority(body) -> "P0".."P3" | None`): the body must contain
exactly one badge image `![P<n> Badge](https://img.shields.io/badge/P<m>-<colour>?...)` with
`n == m` and `n` in 0-3, on the first non-blank line. Colour is not checked (only P2 yellow was
observed). Zero badges, two badges, `P4`, or alt/URL disagreement → `None`.

**Mapping** onto the existing tiers (the priority is the reviewer's own hint, exactly like
Augment's `**Severity:**` line):

| Codex | `severity_hint` | Route after `remap_severity` (no category, default confidence) |
|---|---|---|
| P0 | `critical` | `--depth deep --fix` |
| P1 | `high` | `--depth deep --fix` |
| P2 | `medium` | `--fix` |
| P3 | `low` | report-only |
| malformed / none | not set | Medium fail-safe (existing NFR-4 rule) → `--fix` after verification |

`codex_finding_comments` adds `severity_hint`, `reviewer: "codex"` and `codex_priority` to each
selected root dict; `finding_from_comment` already gives an explicit hint precedence. Augment
roots get `reviewer: "augment"`. `Finding` gains one field, `reviewer: str = "augment"`.

## 8. Re-grade, verification and troubleshoot dispatch (reused)

No change to `remap_severity`, `route`, `refs/finding-verify.md` (evidence-validator, verified /
unverified, no round for unverified) or `refs/troubleshoot-dispatch.md` (seed, `--scope`,
routes, never `--depth quick --fix`). The refs change only their wording from "Augment finding"
to "review finding (Augment or Codex)" and the seed names the reviewer.

## 9. Dedup when both reviewers flag the same line

PR 336 had Augment and Codex threads on the same three lines with the same defect.
`dedup_groups(findings) -> list[list[Finding]]` (pure) groups findings by
`(path, line if line is not None else original_line)`, in input order, and keeps every finding.

- Severity and route of a group = the highest remapped tier in the group.
- Verification still produces one verdict **per finding** (one evidence-validator batch); a
  group is dispatched only if at least one member is verified, with every verified body in the
  troubleshoot seed, so two different claims on one line are both fixed, never silently merged.
- One diagnosis and one set of edits per group (no double fix); `fix_applied` is recorded for
  each member's `fix_key`.
- Every verified thread in the group gets its own reply and resolve, all citing the cycle's one
  fix SHA. An unverified or Low/Nit member is handled as today: no reply, no resolve, listed in
  the report.
- The report lists a group once, with "flagged by: augment, codex".

## 10. Reply and resolve

`scripts/reply-resolve-thread.sh` already identifies a thread only by its root `databaseId`
(and optional `--thread-id`), checks the PR's threads completely, skips a resolved thread, replies
first and then resolves. None of that depends on the author, so a Codex root works unchanged. The
change is wording only: the header and messages say "review finding" instead of "Augment
finding"; no second copy of the script. `refs/thread-reply.md` says the `<COMMENT_ID>` is the
Augment or Codex root id. The reply text (`build_reply`) is unchanged; the reply on a Codex
thread is posted by the operator's identity like any other reply.

## 11. Re-trigger after a push

Neither bot reviews a pushed commit by itself in this repository (section 2). After the push,
reply and resolve, and only when the cycle applied edits, the SKILL posts one re-trigger comment
**per present reviewer** with `scripts/retrigger-review.sh --pr <N> --repo "$REPO" --body
<adapter phrase>`: `auggie review` for Augment (unchanged), `@codex review` for Codex. Each post is
preceded by a write-ahead `rereview_requested{cycle_id, reviewer}` check: a reviewer that already
has one for this `cycle_id` is not posted again (crash safety, INV-R1). Each reviewer gets its own
watermark (UTC recorded right after its own successful POST), used only for that reviewer's
completion attribution.

`@codex review` is the trigger documented by OpenAI and by the bot's own summary text. Whether a
Codex re-review after `@codex review` updates the same summary comment with the new
`commit_sha` (as the marker format implies) has not been observed in this repository:
**UNVERIFIED** until the dry run in this task's PR shows it. If the marker is not updated, the
Codex re-review wait ends `incomplete` at `--timeout` and the run continues with Augment (fail
open), so the gap cannot hang the loop.

The S5b decline fallback keeps its "no second re-trigger" rule for both reviewers. The silence
poke stays Augment-only.

## 12. Loop guard, round counter and the re-trigger count

- One remediation cycle covers the findings of **both** reviewers from one round outcome: one fix
  commit, one push, one `round_counter` tick (INV-001 edge unchanged, fired once per cycle when the
  merged S5 outcome is attributed). `max_rounds=N` still means at most N pushes.
- `rereview_request_count` (INV-R1, `<= max_rounds`) now counts **cycles that were re-triggered**,
  not comments: `rebuild_state` folds `rereview_requested` by distinct `cycle_id` (an event with no
  `cycle_id` still counts once each, so old logs rebuild to the same number). Two comments in one
  cycle (Augment + Codex) count once.
- `recovery.resolve_crash_window` keeps its rule (resume at S5a when no `rereview_requested` exists
  for the cycle). At S5a the SKILL posts only for present reviewers that have no
  `rereview_requested{cycle_id, reviewer}` yet (`pending_retriggers(run_log, cycle_id,
  present)`), so a crash between the two posts neither skips Codex nor double-posts Augment.

## 13. Run-log events and state machine naming the reviewer

- Add two `EventType` members (39 → 41): `reviewer_absent` (`{reviewer}`; fail-open, sticky,
  folded into `rebuild_state()["absent_reviewers"]`) and `reviewer_incomplete` (`{reviewer,
  phase: "initial"|"rereview"}`; a present reviewer that did not complete by `--timeout` while the
  other reviewer's result was used).
- Events that concern one reviewer carry a `reviewer` field: `poll_result` (per-reviewer wait
  outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`,
  `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. Missing `reviewer`
  means `augment` (old logs).
- No new FSM state or edge: the two reviewers are merged **before** the FSM sees an outcome
  (section 6). `state-machine.md` gets a short "reviewers" paragraph saying so, and that
  `TERMINAL_AUGMENT_NO_RESPONSE` means no configured reviewer responded.
- Output contract gains `reviewers`: `{"augment": "present"|"absent"|"incomplete", "codex": ...}`.
  The `status` enum is unchanged.

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

```python
aug = existing gate (unchanged)                       # review_state, findings, routes
cx_state = classify_codex(payload, contract, watermark=wm.get("codex"), current_head_sha=expected_head)
cx_roots = codex_finding_comments(...same args...) if cx_state == "findings" else []
# same normalization rule: empty selection or ValueError -> cx_state = "polling"
decision = merge_wait((augment_wait_outcome(review_state, nxt), review_state),
                      (codex_wait_outcome(cx_state, ...), cx_state))
```

## 15. Files changed

| File | Change |
|---|---|
| `src/superclaude/pr_submit/reviewers.py` | new: adapter table, Codex parser/classifier, merge, dedup, thread listing, pending re-triggers |
| `src/superclaude/pr_submit/classifier.py` | identity parameter on `_thread_findings`; `has_reviewer_activity` |
| `src/superclaude/pr_submit/detection.py` | Codex contract fields |
| `src/superclaude/pr_submit/models.py` | `Finding.reviewer`; two event types |
| `src/superclaude/pr_submit/run_log.py` | distinct-cycle re-trigger count; `absent_reviewers` |
| `src/superclaude/pr_submit/severity_router.py` | carry `reviewer` into `Finding` |
| `src/superclaude/pr_submit/__init__.py` | export the new public functions |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | reviewer-agnostic wording; gate extended; re-trigger per reviewer; output `reviewers` |
| `.../refs/detection-contract.md` | Codex identity, marker and badge contract; YAML fields |
| `.../refs/augment-poll.md` | one snapshot serves both reviewers; per-reviewer wait outcomes and `merge_wait` |
| `.../refs/severity-routing.md` | P0-P3 mapping row; reviewer-neutral wording |
| `.../refs/finding-verify.md`, `troubleshoot-dispatch.md` | wording; dedup groups; seed names reviewer |
| `.../refs/thread-reply.md` | Augment or Codex root id |
| `.../refs/review-retrigger.md` | per-reviewer phrase, watermark, `pending_retriggers` |
| `.../refs/loop-guard.md` | 41 events; distinct-cycle INV-R1 fold; reviewer field |
| `.../refs/state-machine.md` | reviewers merged before the FSM; no-response meaning |
| `.../scripts/reply-resolve-thread.sh`, `retrigger-review.sh`, `poll-augment-review.sh` | header/message wording only (file names kept: tests and installers reference them) |
| `src/superclaude/commands/pr-submit.md` | description and arming text name both reviewers |
| `tests/pr_submit/test_codex_reviews.py` (+ fixtures) | new tests (section 16) |
| `tests/pr_submit/test_run_log.py` | 39 → 41 events |
| `CLAUDE.md`, `docs/user-guide/commands.md`, `docs/guides/tdd-skill-release-guide.md`, `docs/guides/prd-skill-release-guide.md` | where they state Augment-only behaviour |
| `CHANGELOG.md` | Unreleased entry |

No `plugins/superclaude/` twin exists for pr-submit. No installed primitive gains a
`src/superclaude/` path (the refs keep referring to the `superclaude.pr_submit` package).

## 16. Tests

New `tests/pr_submit/test_codex_reviews.py`, fixtures built from the real PR 334/336 shapes:

1. `parse_codex_priority`: P0, P1, P2, P3 → label; no badge, two badges, `P4`, alt/URL mismatch → `None`.
2. Severity mapping: P0/P1 → `--depth deep --fix`, P2 → `--fix`, P3 → report-only, malformed → Medium `--fix`.
3. `codex_review_state` / `classify_codex`: completed clean (PR 334 shape) → `clean`; findings
   (PR 336 shape, unresolved) → `findings` with 3 roots, `reviewer=="codex"`, hint `medium`;
   `running`, wrong head, duplicate summary, malformed JSON, `updated_at` after `observed_at` or not
   newer than watermark → `polling`; resolved threads only + Codex review on head → `clean`.
4. Reviewer detection: `reviewer_activity` and `merge_wait` rows for Augment only, Codex only,
   both, neither (and the pending / incomplete rows).
5. Augment classification unchanged when Codex threads are present in the payload (Codex roots
   never leak into `actionable_finding_comments`).
6. `reply-resolve-thread.sh` on a Codex-rooted thread with a fake `gh` on PATH (the
   `test_cosmos_poll.py` adapter pattern): replies to the root id, then resolves that thread.
7. `dedup_groups`: Augment + Codex on the same path/line → one group of two; different lines →
   two groups; `original_line` used when `line` is null.
8. Run log: 41 event types; `rereview_request_count` counts distinct cycles;
   `absent_reviewers` rebuilt; `pending_retriggers` after a crash between two posts.

Commands (named files only): `uv run pytest tests/pr_submit -q -p no:cacheprovider`,
`uv run pytest tests/skills/test_primitive_dual_surface_lookup.py tests/unit/test_cli_install.py
tests/core/test_how_we_work_routing_table.py -q -p no:cacheprovider`, `make sync-dev`,
`make verify-sync`, `make lint`. Dry check: `poll-augment-review.sh --pr 336 --repo
IronbellyOrg/IronClaude` piped to `list_review_threads` lists the three resolved Codex threads as P2
/ Medium.

## 17. Out of scope, risks and UNVERIFIED items

- **UNVERIFIED**: the summary marker is updated in place after an `@codex review` re-review (only
  "PR opened" reviews were observed). Fail-open covers it (section 11).
- **UNVERIFIED**: P0, P1, P3 badge colours; the parser ignores colour.
- **UNVERIFIED**: Codex posts no decline/size-limit message in a documented format; a usage-limit
  reply is plain activity without completion, so Codex ends `incomplete` (fail open).
- The `codex-review-state:v1` marker is an observed integration format, not a public API (same
  standing as the Cosmos marker); a format change makes Codex `polling` → `incomplete`, never a
  false clean.
- Risk: a Codex connector whose summary comment appears only after Augment has settled is marked
  absent for the run. Observed latency (seconds vs Augment's minutes) makes this unlikely; the
  report names the absent reviewer so the operator can re-run with `--pr <N>`.
- Risk: same path+line findings describing different defects are grouped; mitigated because each
  keeps its own verdict and both bodies go into one diagnosis.
- Out of scope: Codex security review results; reacting to 👍/👀 reactions (not fetched; the
  marker is sufficient).

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
