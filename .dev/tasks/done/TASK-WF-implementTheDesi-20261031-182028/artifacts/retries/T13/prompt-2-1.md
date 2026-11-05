3939477e29cadc940a1cd304bdf78131bfa8653b
Review one task for spec compliance.

Task brief: ## Task 13: Update the detection, poll, severity and verification refs

Depends on: Task 12

Edit, in src/superclaude/skills/sc-pr-submit-protocol/refs/: detection-contract.md prose (Codex identities, the codex-review-state:v1 marker contract, badge parser, observed-format caveat), augment-poll.md (one snapshot for both reviewers, per-reviewer wait outcomes, merge table, Codex absence rule), severity-routing.md (P0-P3 → hint mapping table, reviewer-neutral wording), finding-verify.md (per-finding verdicts inside dedup groups) and troubleshoot-dispatch.md (group seed with every verified body and the reviewer names). Keep T-N50 purity for severity-routing.md (no gh or git tokens).

Acceptance criteria:
- Each of the five refs names Codex where it previously said Augment-only behaviour, matching design sections 5-9.
- tests/pr_submit/test_static_grep.py and test_skill_parse.py pass; make verify-sync passes after make sync-dev.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 3939477e29cadc940a1cd304bdf78131bfa8653b
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
index b2292240..2969ecd4 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md
@@ -1,6 +1,7 @@
-# Detection Contract (DET) — baked Augment identity
+# Detection Contract (DET) — baked reviewer identities (Augment, Codex)
 
-This ref holds the **default detection contract** for the Augment Code GitHub App.
+This ref holds the **default detection contract** for the two review bots: the Augment Code GitHub
+App and the ChatGPT Codex Connector (Codex).
 The YAML is **configuration, not a parser implementation**. The pure core owns marker validation,
 completion attribution and root selection; the configured identities and decline regexes parameterize
 it. `classify(payload, contract, *, watermark=None, current_head_sha=None)` returns exactly
@@ -27,7 +28,7 @@ decline_phrase_regex: 'abnormally\s+large'
 decline_retrigger_regex: 'comment\s+["''`*_]*(augment|auggie|augmentcode)\s+review["''`*_]*'
 accepted_trigger_phrases: ["auggie review", "augment review", "augmentcode review"]
 # Codex (ChatGPT Codex Connector) reviewer. An override that omits these keys keeps the
-# shipped values; an explicit empty value ("") disables Codex.
+# shipped values; setting BOTH identities to "" disables Codex.
 codex_bot_login: "chatgpt-codex-connector[bot]"      # REST bot-login shape
 codex_app_slug: "chatgpt-codex-connector"            # GraphQL login shape
 codex_retrigger_phrase: "@codex review"              # documented Codex re-review trigger
@@ -71,6 +72,47 @@ selection decision with identical payload/head/watermark. The SKILL gate handles
 and normalization errors without feeding empty findings to the driver. Existing decline precedence,
 finite timeout and autonomy/round gates remain unchanged.
 
+## Codex evidence and selection
+
+Codex is identified by `{contract.codex_bot_login, contract.codex_app_slug}` (REST
+`chatgpt-codex-connector[bot]`, GraphQL `chatgpt-codex-connector`), read from the contract, never a
+literal. An empty identity set disables Codex: it is never present. An override file that omits the
+Codex keys keeps the shipped values. An explicit empty or null value blanks that one key; to disable
+Codex, blank **both** `codex_bot_login` and `codex_app_slug`. Blanking only one leaves the other
+identity active, and since the REST summary comment is authored by the `[bot]` login, a blank
+`codex_bot_login` alone leaves Codex present but never complete (it ends `incomplete`).
+
+**Completion** (`codex_review_state` / `classify_codex(payload, contract, *, watermark=None,
+current_head_sha=None)`): a Codex-authored issue comment carries one bounded
+`<!-- codex-review-state:v1 {JSON} -->` marker (JSON object, duplicate keys rejected, as for Cosmos).
+It is valid when `code_review.status` is a string, `code_review.commit_sha` is 40 hex and
+`code_review.has_any_findings` is a boolean. When several Codex comments carry a valid marker, the
+one with the latest `updated_at` is used; two distinct markers with the same latest time stay
+`polling`. The review is complete only when `status == "completed"` and `commit_sha` equals the
+expected head. The completion time is the later of the marker comment's `updated_at` and the
+`submitted_at` of the newest Codex formal review on the expected head (when one exists); both must be
+parseable aware times no later than `observed_at`, and with a watermark the completion must be
+strictly newer than it. Anything else (running, wrong head, malformed or duplicate-key JSON, missing
+time, incomplete snapshot) is `polling`, never clean. `security_review` is ignored.
+
+**Findings** (`codex_finding_comments`): unresolved review threads whose root is Codex-authored, chosen
+by the same root rules as Augment (root only, unique ids, `pullRequestReview` with a commit, nullable
+current `line`, `original_line` hint, created no later than completion). Resolved threads are
+excluded; older unresolved Codex roots stay visible. Each selected root gets `reviewer: "codex"`,
+`codex_priority` and the mapped `severity_hint`. Gate state: no completion or an invalid selection →
+`polling`; unresolved roots → `findings`; none and `has_any_findings` false → `clean`; none,
+`has_any_findings` true and a Codex formal review on the expected head (its threads all resolved) →
+`clean`; otherwise `polling`. Codex has no decline state.
+
+**Badge parser** (`parse_codex_priority(body)`): the first non-blank line must hold exactly one
+`![P<n> Badge](https://img.shields.io/badge/P<m>-<colour>...)` image with `n == m` and `n` in 0-3.
+Zero or two badges, `P4`, or alt/URL disagreement give `None` (the Medium fail-safe). Colour is not
+checked (only P2 yellow has been observed; P0, P1 and P3 colours are UNVERIFIED).
+
+The `codex-review-state:v1` marker and the badge are **observed integration formats, not a stable
+public API** (same standing as the Cosmos marker). A format change makes Codex `polling`, then
+`incomplete` at `--timeout`, never a false clean.
+
 ## Consequences
 
 1. **Identity is configurable (no literal login).** The classifier builds the non-empty identity
@@ -80,7 +122,9 @@ finite timeout and autonomy/round gates remain unchanged.
    "review not detected" (T-211). When Augment and human reviews are interleaved, only the
    Augment author is parsed (T-212). The default retrigger regex also matches the live
    `comment "**_augment review_**"` Markdown wrapper while still requiring the separate
-   `abnormally\s+large` phrase.
+   `abnormally\s+large` phrase. Codex identities work the same way
+   (`{contract.codex_bot_login, contract.codex_app_slug}`); Codex roots never enter Augment's
+   selection, and Augment roots never enter Codex's.
 
 2. **No lock gate.** Arming loads this shipped contract (or an optional local override).
    `locked: false` / a missing override is not a halt. A local override is a refinement,
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md
index 078eedcc..995eabcf 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/augment-poll.md
@@ -2,7 +2,9 @@
 
 This ref pins the poll surface and timing for the SKILL's attended, in-session poll loop. The poll **script**
 (`scripts/poll-augment-review.sh`) performs a single `gh`/`gh api` poll and emits one JSON line; the
-**FSM** (`superclaude.pr_submit`) does the backoff arithmetic. This split keeps `gh` out of the
+**FSM** (`superclaude.pr_submit`) does the backoff arithmetic. The script name is kept, but **one
+snapshot serves both reviewers** (Augment and Codex): the same reviews, comments and threads are
+classified twice, once per reviewer adapter, on the same `expected_head`. This split keeps `gh` out of the
 deterministic core (NFR-6) — the script touches `gh`, the core decides.
 
 > Every `gh`/`gh api` call below pins the RESOLVED `--repo <owner/repo>` (origin's `owner/repo`,
@@ -22,7 +24,9 @@ gh api repos/<owner/repo>/pulls/<N>/comments --method GET -F per_page=100 -F pag
 REST page numbers advance until a page has fewer than 100 records. Reviews preserve `id`, `commit_id`,
 `submitted_at`, `state`, `body`, `user`. `comments` merges raw issue and inline comments (including
 `pull_request_review_id`, nullable `line`/`original_line` when supplied); issue comments retain the
-legacy decline surface. The configured `augmentcode[bot]` and `augmentcode` identities are unchanged.
+legacy decline surface; they also carry the Codex summary comment (its `codex-review-state:v1`
+marker and `updated_at`). The configured `augmentcode[bot]` and `augmentcode` identities are unchanged;
+the Codex identities are `chatgpt-codex-connector[bot]` (REST) and `chatgpt-codex-connector` (GraphQL).
 No check-run fetch is implemented here; an absent check run is not completion evidence.
 
 The repo-pinned GraphQL query uses `reviewThreads(first:100,after:$endCursor)` with
@@ -65,13 +69,57 @@ Metadata validation and historical unresolved-root/count rules are in `detection
 Incomplete or invalid evidence remains `polling` under the existing finite timeout: no automatic fix,
 round increment or `terminal_clean`.
 
+The advisory `state` (`review_present` when any formal review exists) is an Augment-era hint only;
+it is not used for Codex, whose completion is the `codex-review-state:v1` marker
+(`detection-contract.md`). Codex is classified with `classify_codex` and `codex_finding_comments` on
+the same payload and context.
+
+## Two reviewers: wait outcomes and the merge
+
+Each poll gives each reviewer a **wait outcome**: `pending`, `done`, `absent` or `incomplete`.
+
+| Wait outcome | Augment (`augment_wait_outcome(state, nxt, absent=...)`) | Codex (`codex_wait_outcome(...)`) |
+|---|---|---|
+| `pending` | `polling` and `poll_outcome` is `S2_CLASSIFY` or `S5C_SILENCE_REREQUEST` | no completion yet, and either active and before `--timeout`, or inactive, before the silence deadline and Augment not settled |
+| `done` | gate state `clean` / `findings` / `declined` | gate state `clean` / `findings` |
+| `absent` | `TERMINAL_AUGMENT_NO_RESPONSE`, or already absent | inactive when Augment has settled or at the silence deadline, or already absent |
+| `incomplete` | `TERMINAL_TIMEOUT` (partial activity) | active but no completion at `--timeout` |
+
+A reviewer already recorded absent (`rebuild_state()["absent_reviewers"]`), or one whose identity set
+is empty, is `absent` at once and is never `pending`. `merge_wait((augment_wait, augment_state),
+(codex_wait, codex_state))` maps the pair to one round outcome:
+
+| Augment | Codex | Round outcome |
+|---|---|---|
+| `pending` | any | keep polling |
+| any | `pending` | keep polling |
+| `done: declined` | any settled | `declined` (S5b fallback; Codex `findings` join its single re-entry) |
+| `done` | `done` | `findings` if either has findings, else `clean` |
+| `done` | `absent` / `incomplete` | Augment's state (Codex incomplete is reported) |
+| `absent` / `incomplete` | `done` | Codex's state (Augment's condition is reported) |
+| `absent` | `absent` | `no_response` → `TERMINAL_AUGMENT_NO_RESPONSE` (no configured reviewer responded) |
+| `incomplete` | `absent` / `incomplete` | `timeout` → `TERMINAL_TIMEOUT` |
+| `absent` | `incomplete` | `timeout` → `TERMINAL_TIMEOUT` (partial reviewer activity, no classified review) |
+
+Both reviewers share the one `--timeout` wall clock and `--poll-interval`; no second wait is added.
+
+**Codex absence rule.** Codex posts its summary comment seconds after a PR opens, so a connected
+repository shows Codex activity within the first polls. Codex with no activity when Augment's wait
+outcome is settled, or by the silence deadline, is absent: append `reviewer_absent{reviewer:
+"codex"}` and ignore Codex for the rest of the run (no wait, no re-trigger). There is no Codex silence
+poke. When Augment's silence outcome fires while Codex is present, append `reviewer_absent{reviewer:
+"augment"}` and continue with Codex. An Augment-only PR therefore waits no longer than before and adds
+only one `reviewer_absent` event.
+
 ## Interval, timeout, backoff (FR-2.3 / FR-2.5 / NFR-2)
 
 - **Interval ≥ 30s.** A value below 30 is **rejected, not rounded** ("minimum is 30 seconds", T-111).
 - **Timeout default 600s** (~10 min), configurable; **wall-clock since entering wait** (T-221/T-222).
 - **Silence window default 300s** (`--silence-timeout`, min 30, clamped to `--timeout`). Zero
-  Augment-attributed review/comment (`has_augment_activity` false) is `TERMINAL_AUGMENT_NO_RESPONSE`,
-  not `TERMINAL_TIMEOUT`. Partial activity (summary/comment but no classified review) still times out
+  Augment-attributed review/comment (`has_augment_activity` false) is Augment's
+  `TERMINAL_AUGMENT_NO_RESPONSE` outcome (its wait outcome `absent`), not `TERMINAL_TIMEOUT`; the run
+  ends there only when Codex is absent too (merge table above). The same deadline is the Codex
+  absence deadline. Partial activity (summary/comment but no classified review) still times out
   as `TERMINAL_TIMEOUT`. L3 may consider one poke: pass `rerequested=` / `rerequested_at=` from
   `rebuild_state()`, then `check_idempotent("silence_rerequest_invoked")` → append
   `{event_type: silence_rerequested, pr_number, elapsed}` → `retrigger-review.sh --body "augment review"`.
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md
index 120a649e..ab1087fb 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/severity-routing.md
@@ -15,7 +15,26 @@ After `classify(payload, contract, watermark=watermark, current_head_sha=expecte
 `findings`, obtain `actionable_finding_comments` with the **same payload and attribution context**.
 For each root call `superclaude.pr_submit.severity_router.finding_from_comment(raw)` (also exported
 as `superclaude.pr_submit.finding_from_comment`), then `remap_severity(finding)`, then `route(finding)`.
-Never independently filter raw comments or infer findings from summary prose.
+Never independently filter raw comments or infer findings from summary prose. Codex findings take the
+same seam: after `classify_codex` returns `findings`, `codex_finding_comments` (same payload and
+context) feeds the same `finding_from_comment(raw)` → `remap_severity` → `route` calls. Each `Finding`
+carries `reviewer` (`"augment"` or `"codex"`); the rules below are reviewer-neutral.
+
+**Codex priority → severity hint.** Codex marks each finding with a P0-P3 badge on its first line
+(`parse_codex_priority`, see `detection-contract.md`); `codex_finding_comments` turns it into an
+explicit `severity_hint`, exactly like Augment's `**Severity:**` line:
+
+| Codex badge | `severity_hint` | Route after `remap_severity` (no category, default confidence) |
+|---|---|---|
+| P0 | `critical` | `--depth deep --fix` |
+| P1 | `high` | `--depth deep --fix` |
+| P2 | `medium` | `--fix` |
+| P3 | `low` | report-only |
+| missing / malformed | not set | Medium fallback → `--fix` after verification |
+
+**Dedup groups.** `dedup_groups(findings)` groups the merged findings of both reviewers by path and
+line (`original_line` when `line` is null), keeping every finding. A group routes at the **highest
+remapped tier among its members**; each member keeps its own remapped tier, verdict and thread.
 
 `finding_from_comment` raises `ValueError` for invalid root fields. The SKILL gate treats that or an
 empty selected list (possible for a legacy `has_findings` signal) as incomplete/polling under the
@@ -35,12 +54,13 @@ evidence-validator gate can authorize diagnosis/remediation; unverified findings
 
 ## 1. Grade — DEFER TO the rubric (reuse, do NOT copy)
 
-Re-grading is **not** reinvented here. For every Augment finding, **apply the severity-remap
+Re-grading is **not** reinvented here. For every review finding (Augment or Codex), **apply the severity-remap
 algorithm defined in `sc-auggie-review-protocol/refs/severity-rubric.md` §Severity-remap algorithm**
 (the 5-step pipeline at `severity-rubric.md:63-101`), keyed on the rubric's **category floor/ceiling
 table** (`severity-rubric.md:70-87`). The five steps, applied by reference:
 
-1. Start from Augment's `severity_hint` (a hint, not authoritative — FR-3.1).
+1. Start from the reviewer's `severity_hint` (Augment's `**Severity:**` line or the Codex badge
+   mapping above; a hint, not authoritative — FR-3.1).
 2. **Category floor/ceiling override** (`severity-rubric.md:70-87`) — the category is more reliable
    than the hint; clamp to the category's floor (minimum severity) and ceiling (maximum severity).
    E.g. `security (exploitable)` floor = Critical; `naming`/`style` ceiling = Nit.
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
index 50789a9c..9789bfa9 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
@@ -1,7 +1,7 @@
 # Finding Verify (C3a) — verify-before-remediate, by reference
 
 This wave is the **false-positive filter** (FR-3.5): between routing (C3) and dispatch (C3b), each
-routed finding must independently **ground in real code** before any `/sc:troubleshoot --fix` session
+routed review finding (Augment or Codex) must independently **ground in real code** before any `/sc:troubleshoot --fix` session
 — or any round, or any push — is spent on it. It reuses the repo's existing grounding discipline
 **by reference** (never copied or forked) and **spawns the existing `evidence-validator` agent**
 rather than authoring a new verifier.
@@ -56,6 +56,15 @@ A finding is:
 | **Structural drop** (EC-9) | Missing/invalid `file:line` (cannot be grounded at all) | Dropped, not downgraded | the Wave-3 floor above |
 | **False-positive demote** (FR-3.5) | `file:line` EXISTS but the defect does NOT reproduce | Demoted to report-only, no round | the C3a "reproduce" delta |
 
+## Two reviewers and dedup groups
+
+Augment and Codex findings are verified the same way and **in one batch**: the verdict is **per
+finding**, never per reviewer or per group, and each `finding_verified` / `finding_unverified` event
+carries the finding's `reviewer`. Inside a dedup group (same path and line, `dedup_groups`), each
+member keeps its own verdict: a group is dispatched to C3b only when at least one member is
+`verified`, and an unverified member stays report-only (no reply, no resolve) even when another
+member of its group is fixed.
+
 The structural drop happens first (a finding with no valid location never reaches the reproduce
 check). The false-positive demote is the NEW filter this wave contributes. Both keep the loop from
 burning a round or a push on a hallucinated or stale finding (directly attacking risks R1 and R4).
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
index c1cadf6c..3bc5cbc6 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
@@ -10,8 +10,8 @@ reused by reference (`sc-troubleshoot-protocol/SKILL.md:103`).
 
 For each verified finding, construct:
 
-- **issue description** ← the Augment finding `body` + recommendation + evidence excerpt, so
-  troubleshoot does not re-derive the symptom (FR-3.3).
+- **issue description** ← the review finding `body` (Augment or Codex, named in the seed) +
+  recommendation + evidence excerpt, so troubleshoot does not re-derive the symptom (FR-3.3).
 - **`--scope <file:line>`** ← the finding's grounded `file:line` (T-320 asserts the dispatched
   `scope` contains the finding's file:line).
 - **`--type <category>`** ← the rubric category (security / performance / tests / …), so troubleshoot
@@ -23,6 +23,15 @@ For each verified finding, construct:
   - Low / Nit → **report-only**: troubleshoot is NOT called; the finding is recorded in the
     report-only list.
 
+## Dedup groups (Augment and Codex on the same line)
+
+A dedup group (`dedup_groups`: same path and line, `original_line` when `line` is null) is seeded
+**once**: the issue description holds **every verified member's body, each labelled with its
+reviewer** (for example "augment:" and "codex:"), so two different claims on one line are both fixed,
+never silently merged. The group's route is its members' highest remapped tier; `--scope` is the
+shared `file:line`. The group gets one diagnosis and one set of edits (no double fix), and
+`fix_applied` is recorded for each member's `fix_key`. Unverified members are not in the seed.
+
 ## STOP — never emit `--depth quick --fix`
 
 `--depth quick` with `--fix` is an explicit troubleshoot conflict
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
index 6a62d59c..c5fdaa86 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
@@ -266,7 +266,7 @@ Wave 8: CI wait (after Augment clean / REPORT_ONLY / HALT_MAX_ROUNDS / TERMINAL_
 
 - **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` (with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL's `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
 - **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: "PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; a branch Wave 0 rebased needs a force-push, which this skill never does for you; `git pull --ff-only` if you are behind), then re-run with `--pr <N>`." True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.
-- **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt; the contract also carries the Codex identities (`codex_bot_login`, `codex_app_slug`) and `codex_retrigger_phrase`, and an empty Codex identity disables Codex. Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s; the one snapshot serves both reviewers); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Record `reviewer_absent{reviewer}` for a reviewer the merge settles as absent, and `reviewer_incomplete{reviewer, phase: "initial"}` for a present reviewer that did not complete by `--timeout` while the other's result was used. Every event that concerns one reviewer carries a `reviewer` field (`"augment"` or `"codex"`; a missing field means `augment`): `poll_result` (with the per-reviewer wait outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. On `--resume`, read `rebuild_state()["absent_reviewers"]` and keep those reviewers absent. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor.
+- **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt; the contract also carries the Codex identities (`codex_bot_login`, `codex_app_slug`) and `codex_retrigger_phrase`, and Codex is disabled only when both Codex identities are blank. Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s; the one snapshot serves both reviewers); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Record `reviewer_absent{reviewer}` for a reviewer the merge settles as absent, and `reviewer_incomplete{reviewer, phase: "initial"}` for a present reviewer that did not complete by `--timeout` while the other's result was used. Every event that concerns one reviewer carries a `reviewer` field (`"augment"` or `"codex"`; a missing field means `augment`): `poll_result` (with the per-reviewer wait outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. On `--resume`, read `rebuild_state()["absent_reviewers"]` and keep those reviewers absent. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor.
 - **Wave 2:** load `refs/severity-routing.md`; use only the snapshot gate's `actionable_finding_comments` → `finding_from_comment` → `remap_severity(finding)` → `route(finding)` results from `superclaude.pr_submit` (Augment's and, for Codex, `codex_finding_comments` → the same three calls; a Codex P0/P1/P2/P3 badge is its severity hint, a missing or malformed badge is the Medium fail-safe), then map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`. Group the merged findings with `dedup_groups(findings)` (same path and line, `original_line` when the line is null): a **dedup group routes at its members' highest remapped tier**; every member keeps its own finding, verdict and thread.
 - **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces (one verdict per finding, Augment and Codex in one batch). `unverified` → REPORT_ONLY, consuming NO round. A dedup group is dispatched only when at least one member is verified.
 - **Wave 4:** load `refs/troubleshoot-dispatch.md`; for VERIFIED findings only, `> Skill sc:troubleshoot-protocol` for diagnosis, once per dedup group with every verified member's body in the seed and each body naming its reviewer; the group gets one diagnosis and one set of edits (no double fix), and `fix_applied` is recorded for **every** member's `fix_key`. **At L1 (G-edit `ordinal < 2`): PROPOSE "fix these? y/n" and apply NO edits.** At L2+ the skill applies the diagnosed edits ITSELF in the working tree (troubleshoot does NOT auto-apply — `sc:pr-submit` owns edit application in `S3_FIXING`). Before the cycle's first edit, record the operator's pending files (`git status --porcelain=v1 -z --untracked-files=all`: every modified, staged and untracked file, both sides of a rename) as `OPERATOR_PENDING`; the Wave 6 fix commit refuses any of them.
diff --git a/src/superclaude/pr_submit/detection.py b/src/superclaude/pr_submit/detection.py
index 3f1ae628..4618e966 100644
--- a/src/superclaude/pr_submit/detection.py
+++ b/src/superclaude/pr_submit/detection.py
@@ -43,7 +43,8 @@ _LOCAL_OVERRIDE_PATH: Path | None = None
 # Shipped Codex (ChatGPT Codex Connector) identity and re-trigger phrase. A YAML
 # contract that OMITS a Codex key falls back to these values (an override written
 # by contract setup has no Codex keys and must not switch Codex off); an explicit
-# empty or null value disables Codex. Direct ``DetectionContract()`` construction
+# empty or null value blanks that one identity, and Codex is disabled only when
+# both identities are blank. Direct ``DetectionContract()`` construction
 # keeps both identities empty (fail-safe, like Augment).
 _SHIPPED_CODEX_BOT_LOGIN = "chatgpt-codex-connector[bot]"
 _SHIPPED_CODEX_APP_SLUG = "chatgpt-codex-connector"
@@ -146,7 +147,9 @@ class DetectionContract:
         """Build a contract from YAML, trimming identity padding (no lock enforcement).
 
         Codex keys use key-presence semantics: an absent key falls back to the
-        shipped Codex value; a present empty or null value disables Codex.
+        shipped Codex value; a present empty or null value blanks that identity.
+        Codex is disabled only when both ``codex_bot_login`` and ``codex_app_slug``
+        are blank (an empty identity set).
         """
         data = data.copy()
         for key, shipped in (
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-check.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-check.py
new file mode 100644
index 00000000..3cb2ada3
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-check.py
@@ -0,0 +1,8 @@
+import dataclasses, json
+from superclaude.pr_submit import DetectionContract, classify_codex, reviewer_identities, reviewer_activity
+base = DetectionContract.load()
+data = {f.name: getattr(base, f.name) for f in dataclasses.fields(base)}
+p = json.load(open("tests/pr_submit/fixtures/codex-findings-pr336.json"))
+for blank in (("codex_bot_login",), ("codex_bot_login", "codex_app_slug")):
+    c = DetectionContract.from_yaml({**data, **{k: "" for k in blank}})
+    print(blank, sorted(reviewer_identities(c, "codex")), reviewer_activity(p, c)["codex"], classify_codex(p, c))
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-check.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-check.log
new file mode 100644
index 00000000..847a984a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-check.log
@@ -0,0 +1,2 @@
+('codex_bot_login',) ['chatgpt-codex-connector'] True polling
+('codex_bot_login', 'codex_app_slug') [] False polling
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-sync.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-sync.log
new file mode 100644
index 00000000..52c90cec
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-sync.log
@@ -0,0 +1,217 @@
+🔄 Syncing src/superclaude/ → .claude/ for local development...
+✅ Sync complete.
+   Skills:    36 directories
+   Agents:    45 files
+   Commands:  43 files
+   Hooks:     12 files
+   Templates: 52 files
+sync-dev rc=0
+🔍 Verifying src/superclaude/ ↔ .claude/ sync...
+
+=== Skills ===
+  ✅ ccsession-tag
+  ✅ confidence-check
+  ✅ operational-guide
+  ✅ prd
+  ✅ readme
+  ✅ roadmap
+  ✅ sc-adversarial-protocol
+  ✅ sc-auggie-review-protocol
+  ✅ sc-bare-review
+  ✅ sc-brainstorm-protocol
+  ✅ sc-cleanup-audit-protocol
+  ✅ sc-cli-eval-protocol
+  ✅ sc-cli-portify-protocol
+  ✅ sc-crash-recovery
+  ✅ sc-implement-protocol
+  ✅ sc-init-lite-protocol
+  ✅ sc-pm-protocol
+  ✅ sc-post-release-protocol
+  ✅ sc-pr-submit-protocol
+  ✅ sc-recommend
+  ✅ sc-reflect-protocol
+  ✅ sc-release-split-protocol
+  ✅ sc-review-translation-protocol
+  ✅ sc-roadmap-protocol
+  ✅ sc-swarm-wizard-protocol
+  ✅ sc-task-protocol
+  ✅ sc-tasklist-protocol
+  ✅ sc-troubleshoot-protocol
+  ✅ sc-validate-roadmap-protocol
+  ✅ sc-validate-tests-protocol
+  ✅ sc-workflow-protocol
+  ✅ task-builder
+  ✅ task
+  ✅ tdd
+  ✅ tech-reference
+  ✅ tech-research
+
+=== Agents ===
+  ✅ audit-analyzer.md
+  ✅ audit-comparator.md
+  ✅ audit-consolidator.md
+  ✅ audit-scanner.md
+  ✅ audit-validator.md
+  ✅ auggie-reviewer.md
+  ✅ backend-architect.md
+  ✅ business-panel-experts.md
+  ✅ confidence-calibrator.md
+  ✅ debate-orchestrator.md
+  ✅ deep-research-agent.md
+  ✅ deep-research.md
+  ✅ devops-architect.md
+  ✅ eval-docs-loader.md
+  ✅ eval-run-reporter.md
+  ✅ eval-suite-author.md
+  ✅ evidence-validator.md
+  ✅ frontend-architect.md
+  ✅ implement-retry-adviser.md
+  ✅ learning-guide.md
+  ✅ merge-executor.md
+  ✅ performance-engineer.md
+  ✅ pm-agent.md
+  ✅ python-expert.md
+  ✅ quality-engineer.md
+  ✅ refactoring-expert.md
+  ✅ reflect-reviewer.md
+  ✅ repo-index.md
+  ✅ requirements-analyst.md
+  ✅ reuse-auditor.md
+  ✅ rf-analyst.md
+  ✅ rf-assembler.md
+  ✅ rf-qa-qualitative.md
+  ✅ rf-qa.md
+  ✅ rf-task-builder.md
+  ✅ rf-task-executor.md
+  ✅ rf-task-researcher.md
+  ✅ rf-team-lead.md
+  ✅ root-cause-analyst.md
+  ✅ security-engineer.md
+  ✅ self-review.md
+  ✅ socratic-mentor.md
+  ✅ system-architect.md
+  ✅ technical-writer.md
+  ✅ troubleshoot-analyst.md
+
+=== Commands ===
+  ✅ adversarial.md
+  ✅ agent.md
+  ✅ analyze.md
+  ✅ auggie-review.md
+  ✅ brainstorm.md
+  ✅ build.md
+  ✅ business-panel.md
+  ✅ cleanup-audit.md
+  ✅ cleanup.md
+  ✅ cli-eval.md
+  ✅ cli-portify.md
+  ✅ design.md
+  ✅ document.md
+  ✅ explain.md
+  ✅ git.md
+  ✅ help.md
+  ✅ implement.md
+  ✅ improve.md
+  ✅ index-repo.md
+  ✅ index.md
+  ✅ init-lite.md
+  ✅ load.md
+  ✅ pm.md
+  ✅ post-release.md
+  ✅ pr-submit.md
+  ✅ recommend.md
+  ✅ reflect.md
+  ✅ release-split.md
+  ✅ research.md
+  ✅ review-translation.md
+  ✅ roadmap.md
+  ✅ save.md
+  ✅ spawn.md
+  ✅ spec-panel.md
+  ✅ swarm-wizard.md
+  ✅ task.md
+  ✅ tasklist.md
+  ✅ tdd.md
+  ✅ test.md
+  ✅ troubleshoot.md
+  ✅ validate-roadmap.md
+  ✅ validate-tests.md
+  ✅ workflow.md
+
+=== Hooks ===
+  ✅ auggie-flag-clear.sh
+  ✅ codegraph-session-start.sh
+  ✅ freshness-file-changed.sh
+  ✅ freshness-post-read.sh
+  ✅ freshness-pre-edit.sh
+  ✅ freshness-session-start.sh
+  ✅ freshness-subagent-start.sh
+  ✅ freshness-subagent-stop.sh
+  ✅ freshness-user-prompt.sh
+  ✅ reject-workspace-writes.sh
+  ✅ sc-recommend-phase0.sh
+  ✅ pragmatic-subagent.js
+
+=== Templates ===
+  ✅ workflow/05_prd_template.md
+  ✅ workflow/03_project_plan_template.md
+  ✅ workflow/03_component_authoring_template.md
+  ✅ workflow/00_mdtm_template_simple_task.md
+  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
+  ✅ workflow/06_architecture_proposal_template.md
+  ✅ workflow/02_mdtm_template_complex_task.md
+  ✅ workflow/04_feature_brief_template.md
+  ✅ workflow/changelog_template.md
+  ✅ workflow/01_mdtm_template_generic_task.md
+  ✅ workflow/99_mdtm_template_generic_task_old.md
+  ✅ documents/prd_template.md
+  ✅ documents/operational_guide_template.md
+  ✅ documents/GFxAI_Master_Documentation_Template.md
+  ✅ documents/tdd_template.md
+  ✅ documents/agent_template_analysis.md
+  ✅ documents/supplemental-doc-creation-checklist.md
+  ✅ documents/agent_template_qa.md
+  ✅ documents/skill_template.md
+  ✅ documents/roadmap_template.md
+  ✅ documents/agent_template_worker.md
+  ✅ documents/release-spec-template.md
+  ✅ documents/supplemental_doc_template.md
+  ✅ documents/technical_reference_template.md
+  ✅ documents/readme_template.md
+  ✅ modularization-template-review/qa-fix-summary_template.md
+  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
+  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
+  ✅ modularization-template-review/research-notes_template.md
+  ✅ modularization-template-review/synthetic-dnsp-finding.contract
+  ✅ modularization-template-review/INDEX.md
+  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
+  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
+  ✅ modularization-template-review/track-scope-map_template.md
+  ✅ modularization-template-review/claim-evidence-matrix_template.md
+  ✅ modularization-template-review/qa-inventory_report_template.md
+  ✅ modularization-template-review/analyst-coverage-matrix_template.md
+  ✅ modularization-template-review/codebase-research_template.md
+  ✅ modularization-template-review/analyst-completeness_report_template.md
+  ✅ modularization-template-review/analyst-gap-analysis_template.md
+  ✅ modularization-template-review/qa-lens_report_template.md
+  ✅ modularization-template-review/qa-consolidated-findings_template.md
+  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
+  ✅ modularization-template-review/qa-research-gap_report_template.md
+  ✅ modularization-template-review/qa-research-evidence_report_template.md
+  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
+  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
+  ✅ modularization-template-review/analyst-cross-validation_report_template.md
+  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
+  ✅ modularization-template-review/pipeline-complete_report_template.md
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+verify-sync rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-test.log
new file mode 100644
index 00000000..4aec32ce
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-test.log
@@ -0,0 +1,14 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 33 items
+
+tests/pr_submit/test_static_grep.py ...................                  [ 57%]
+tests/pr_submit/test_skill_parse.py ..............                       [100%]
+
+============================== 33 passed in 0.55s ==============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-pr-submit.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-pr-submit.log
new file mode 100644
index 00000000..2d660dc8
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t13-pr-submit.log
@@ -0,0 +1,56 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 705 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  1%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  2%]
+tests/pr_submit/test_autonomy_gates.py .......                           [  3%]
+tests/pr_submit/test_ci_classify.py ....................                 [  6%]
+tests/pr_submit/test_codex_reviews.py .................................. [ 11%]
+........................                                                 [ 14%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [ 16%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 19%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 20%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 21%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 23%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 25%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 31%]
+...............................................................          [ 40%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 42%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 46%]
+........................................................................ [ 57%]
+                                                                         [ 57%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 59%]
+tests/pr_submit/test_detection_contract.py ............................. [ 63%]
+.....                                                                    [ 64%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 66%]
+tests/pr_submit/test_finding_verify.py ...                               [ 67%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 68%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 72%]
+                                                                         [ 72%]
+tests/pr_submit/test_idempotency.py ......                               [ 72%]
+tests/pr_submit/test_loop_guard.py .............                         [ 74%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 75%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 80%]
+.....                                                                    [ 80%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 81%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 82%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 83%]
+tests/pr_submit/test_run_log.py ............                             [ 85%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 85%]
+tests/pr_submit/test_severity_router.py ............................     [ 89%]
+tests/pr_submit/test_silence.py .................                        [ 92%]
+tests/pr_submit/test_skill_parse.py ..............                       [ 94%]
+tests/pr_submit/test_static_grep.py ...................                  [ 97%]
+tests/pr_submit/test_timeout.py .....                                    [ 97%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 98%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 98%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================= 705 passed in 14.51s =============================
+rc=0
Delta diff from the previous reviewed tree (empty on the first review): Fix pass for F1.1 (family codex-disable-semantics): reworded refs/detection-contract.md:31 (YAML comment) and :79-83, SKILL.md Wave 1 sentence, and the comments at src/superclaude/pr_submit/detection.py:43-48 and from_yaml docstring :148-152 (comments only, no code change). Evidence: artifacts/t13-check.py + t13-check.log (blank codex_bot_login alone -> identities ['chatgpt-codex-connector'], active True, classify_codex polling; both blank -> [] / False). Logs t13-test.log, t13-pr-submit.log, t13-sync.log regenerated.
Earlier blocking findings of this start (empty on the first review): F1.1 at=refs/detection-contract.md:80 family=codex-disable-semantics: 'an explicit empty or null value disables Codex' is false when only one Codex identity key is blanked (detection.py:166-168 blanks per key)
Saved-probe re-check hit locations (may be empty): src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:31:# shipped values; setting BOTH identities to "" disables Codex.;src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:79:literal. An empty identity set disables Codex: it is never present. An override file that omits the;src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md:80:Codex keys keeps the shipped values. An explicit empty or null value blanks that one key; to disable;src/superclaude/pr_submit/detection.py:46:# empty or null value blanks that one identity, and Codex is disabled only when;src/superclaude/pr_submit/detection.py:140:    # from_yaml supply the real values. An empty identity set disables Codex.;src/superclaude/pr_submit/detection.py:150:        shipped Codex value; a present empty or null value blanks that identity.;

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
