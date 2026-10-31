# Detection Contract (DET) — baked reviewer identities (Augment, Codex)

This ref holds the **default detection contract** for the two review bots: the Augment Code GitHub
App and the ChatGPT Codex Connector (Codex).
The YAML is **configuration, not a parser implementation**. The pure core owns marker validation,
completion attribution and root selection; the configured identities and decline regexes parameterize
it. `classify(payload, contract, *, watermark=None, current_head_sha=None)` returns exactly
`polling` / `clean` / `findings` / `declined`; it never embeds a literal bot login.

Arming does **not** require a local lock file or R1 probe. `DetectionContract.for_arming()`
loads this shipped contract (or an optional gitignored override at
`.dev/pr-monitor/detection-contract.locked.md` when present). A missing/unlocked override
is not a halt.

```yaml
# detection-contract.md — shipped defaults; optional local override may replace these
augment_bot_login: "augmentcode[bot]"                # REST bot-login shape
augment_author_association: ["NONE", "CONTRIBUTOR"]  # observed associations of the Augment author
augment_app_slug: "augmentcode"                      # GraphQL app-slug shape; accepted with bot login
emission_shape: "review"                             # documentary; classifier unused
findings_locus: "comments[]"                         # documentary; classifier unused
severity_field_path: null                            # Augment's self-reported severity, if any (hint only)
review_completeness_signal: "state==COMMENTED"       # documentary
probe_evidence: null                                 # optional provenance; not an arming gate
# V1.1 decline-detection (addendum §6.2 / FR-9.1) — baked defaults; both regexes must match an
# Augment-authored comment for a "declined". accepted_trigger_phrases = our operator re-trigger tokens.
decline_phrase_regex: 'abnormally\s+large'
decline_retrigger_regex: 'comment\s+["''`*_]*(augment|auggie|augmentcode)\s+review["''`*_]*'
accepted_trigger_phrases: ["auggie review", "augment review", "augmentcode review"]
# Codex (ChatGPT Codex Connector) reviewer. An override that omits these keys keeps the
# shipped values; setting BOTH identities to "" disables Codex.
codex_bot_login: "chatgpt-codex-connector[bot]"      # REST bot-login shape
codex_app_slug: "chatgpt-codex-connector"            # GraphQL login shape
codex_retrigger_phrase: "@codex review"              # documented Codex re-review trigger
locked: true                                         # vestigial; arming does not check this flag
```

`augment_author_association`, `emission_shape`, `findings_locus`, `severity_field_path`,
`review_completeness_signal`, and `probe_evidence` are documentary fields, not runtime parser rules.
Changing them does not add a provider, change finding selection or make `state==COMMENTED` sufficient
for Cosmos completion. Identity/decline configuration remains separate from the validation below.

## Cosmos evidence and selection

The `<!-- cosmos-review-status:v1 {JSON} -->` marker is an **observed integration format, not a stable
public API**. The core accepts one bounded v1 marker (JSON object, no duplicate keys), nonempty
`specialist`, `status: reviewed`, full 40-character hexadecimal `head` and `baseline`, and a
nonnegative integer `unresolved_count` (booleans excluded). `session_url` is diagnostic data only.
Malformed/duplicate/unsupported markers, unknown statuses and recognizable Cosmos evidence without
a valid marker cannot fall back to legacy clean. Summary prose and absent checks prove nothing.

`current_head_sha` defaults to `payload.head_sha`; an explicit argument **overrides** it. During a
pushed-SHA wait the caller must first check actual `payload.head_sha == pushed_sha`. The selected
latest relevant bot review is ordered by trustworthy submission time, not array order; marker head,
expected head and each provided review commit association must agree. Pending/newer invalid evidence
or ambiguous/missing times cannot be bypassed by an older clean review. Completion must be strictly
newer than `watermark` and no later than `observed_at` (the poll snapshot UTC observation, not a live
clock read in the pure core). Wrong-head-only evidence polls. Contextual legacy reviews also require
head/commit and submission attribution; context-free legacy injected payloads remain supported.

Live Cosmos snapshots require `reviews_ok`, `comments_ok`, `threads_ok` all literally true and complete
review/comment/thread collections. Selection uses unresolved **Augment-rooted** threads, not replies:
resolved roots are excluded even with integer current lines; older outdated-but-unresolved roots
survive a new baseline and the watermark. Their nullable current `line`, `original_line` hint,
`comment_id` (root database ID), `thread_id`, `review_id` and `is_outdated` pass through normalization.
Null current line is not evidence of resolution or a grounded defect.

`unresolved_count` is a conservative **lower bound** on required usable detail, not equality with all
historical unresolved threads: positive count with insufficient roots stays polling; zero cannot erase
independently observed old open roots. Classification and `actionable_finding_comments` share one
selection decision with identical payload/head/watermark. The SKILL gate handles empty legacy signals
and normalization errors without feeding empty findings to the driver. Existing decline precedence,
finite timeout and autonomy/round gates remain unchanged.

## Codex evidence and selection

Codex is identified by the non-empty members of `{contract.codex_bot_login, contract.codex_app_slug}`
(REST `chatgpt-codex-connector[bot]`, GraphQL `chatgpt-codex-connector`), read from the contract,
never a literal. An override file that omits a Codex key keeps the shipped value; an explicit empty or
null value blanks that one key. Codex is disabled only when the identity set is empty, so to disable
Codex, blank both keys; blanking one leaves the other identity active.

**Completion** (`codex_review_state` / `classify_codex(payload, contract, *, watermark=None,
current_head_sha=None)`): a Codex-authored issue comment carries one bounded
`<!-- codex-review-state:v1 {JSON} -->` marker (JSON object, duplicate keys rejected, as for Cosmos).
It is valid when `code_review.status` is a string, `code_review.commit_sha` is 40 hex and
`code_review.has_any_findings` is a boolean. When several Codex comments carry a valid marker, the
one with the latest `updated_at` is used; two distinct markers with the same latest time stay
`polling`. The review is complete only when `status == "completed"` and `commit_sha` equals the
expected head. The completion time is the later of the marker comment's `updated_at` and the
`submitted_at` of the newest Codex formal review on the expected head (when one exists); both must be
parseable aware times no later than `observed_at`, and with a watermark the completion must be
strictly newer than it. Anything else (running, wrong head, malformed or duplicate-key JSON, missing
time, incomplete snapshot) is `polling`, never clean. `security_review` is ignored.

**Findings** (`codex_finding_comments`): unresolved review threads whose root is Codex-authored, chosen
by the same root rules as Augment (root only, unique ids, `pullRequestReview` with a commit, nullable
current `line`, `original_line` hint, created no later than completion). Resolved threads are
excluded; older unresolved Codex roots stay visible. Each selected root gets `reviewer: "codex"`,
`codex_priority` and the mapped `severity_hint`. Gate state: no completion or an invalid selection →
`polling`; unresolved roots → `findings`; none and `has_any_findings` false → `clean`; none,
`has_any_findings` true and a Codex formal review on the expected head (its threads all resolved) →
`clean`; otherwise `polling`. Codex has no decline state.

**Badge parser** (`parse_codex_priority(body)`): the first non-blank line must hold exactly one
`![P<n> Badge](https://img.shields.io/badge/P<m>-<colour>...)` image with `n == m` and `n` in 0-3.
Zero or two badges, `P4`, or alt/URL disagreement give `None` (the Medium fail-safe). Colour is not
checked (only P2 yellow has been observed; P0, P1 and P3 colours are UNVERIFIED).

The `codex-review-state:v1` marker and the badge are **observed integration formats, not a stable
public API** (same standing as the Cosmos marker). A marker format change leaves Codex `polling`,
never a false clean (with Codex activity it ends `incomplete` at `--timeout`); a badge format change
gives `None`, the Medium fail-safe.

## Consequences

1. **Identity is configurable (no literal login).** The classifier builds the non-empty identity
   set `{contract.augment_bot_login, contract.augment_app_slug}`, **never** a literal string.
   This accepts REST bot-login shape (`augmentcode[bot]`) and GraphQL app-slug shape
   (`augmentcode`) when both are present in data. A different bot login is treated as
   "review not detected" (T-211). When Augment and human reviews are interleaved, only the
   Augment author is parsed (T-212). The default retrigger regex also matches the live
   `comment "**_augment review_**"` Markdown wrapper while still requiring the separate
   `abnormally\s+large` phrase. Codex identities work the same way
   (`{contract.codex_bot_login, contract.codex_app_slug}`); Codex roots never enter Augment's
   selection, and Augment roots never enter Codex's.

2. **No lock gate.** Arming loads this shipped contract (or an optional local override).
   `locked: false` / a missing override is not a halt. A local override is a refinement,
   not a requisite. One change point on Augment drift: edit the identity fields here
   (or drop a local override) — **no control-flow code changes** (spec §7 consequence 2).

3. **Optional override.** `.dev/pr-monitor/detection-contract.locked.md` is still preferred
   when present (`for_arming()` / `prefer_local_override=True`) so a fork can pin a
   different bot identity without forking the shipped skill.

4. **Purity seam (AC-9 / NFR-6).** No `gh`/`git` token appears in `state-machine.md`,
   `severity-routing.md`, or `loop-guard.md` — protecting the seam from a future maintainer
   inlining a bot-login string. Tested by **T-N50**.
