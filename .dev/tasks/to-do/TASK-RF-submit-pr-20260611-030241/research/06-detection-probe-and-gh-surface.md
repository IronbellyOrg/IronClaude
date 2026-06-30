# R6 — Detection Probe + gh API Surface

**Status: Complete**
**Researcher:** R6 (Detection Probe + gh API Surface)
**Date:** 2026-06-11
**Spec:** `/config/workspace/IronClaude/.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`

Owns: gh API DETAIL + the R1 DET probe operationality. Does NOT cover R1 inventory,
R2 conventions, R3 reuse, R4 python test infra, R5 Monitor/wiring/registration, R7 template.

Environment facts (verified this session):
- `git remote -v` → `origin = https://github.com/IronbellyOrg/IronClaude.git` (fetch+push). **No `upstream` remote configured in this clone.** PR-target discipline (`--repo IronbellyOrg/IronClaude`) is therefore mandatory and not satisfiable by default `gh` inference.
- `gh --version` → **gh 2.45.0**. Relevant: gh has **no native `gh pr review-thread resolve`** verb (cli/cli#12419 was opened 2026-01-04 and closed as a duplicate of #359 — still unimplemented). Thread resolution MUST go through `gh api graphql` (the GraphQL `resolveReviewThread` mutation). REST has no resolve concept (confirmed: GitHub community #44650, reddit r/github thread).

---

## Section 1 — R1 DET Probe Operationality

### 1.1 What the probe concretely is

The DET probe is an **empirical, manual/operator capture step** run once against the **live Augment
Code GitHub App** on a **real PR** of `IronbellyOrg/IronClaude`. Its job is to replace every guessed
constant in `detection-contract.md` (§7) with observed data, then flip `locked: false → true`. The
build DAG (§3 step 0) BLOCKS step 1 until `detection-contract.md.locked == true` (HARD GATE AC-8;
asserted by T-210). There is no way to lock the contract from synthetic data — locking REQUIRES a real
Augment emission, because the whole point of DET is that the bot login + emission shape are
**unknown and must not be hard-guessed** (§7 consequence 1, R1 = P0 risk, §17).

The probe is **5 concrete `gh`/`gh api` captures** against a PR that the Augment app has already
reviewed. Concretely (all pinned to the fork per FR-1.3 / §19.2):

1. **Identify the bot login + author_association** (fills `augment_bot_login`,
   `augment_author_association`, `augment_app_slug`):
   ```
   gh pr view <N> --repo IronbellyOrg/IronClaude \
     --json reviews -q '.reviews[] | {author: .author.login, association: .authorAssociation, state: .state}'
   ```
   and the richer REST view (REST exposes `user.login`, `user.type=="Bot"`, `author_association`,
   and the `[bot]` suffix the GraphQL/`gh pr view` surface may strip):
   ```
   gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews \
     -q '.[] | {id, user: .user.login, type: .user.type, association: .author_association, state}'
   ```
   This is where `augment-code[bot]` (the *expected but unverified* literal, §7 example) gets
   confirmed or corrected. The spec is explicit: the value lives in **data**, never in a code literal
   (`if login == contract.augment_bot_login`, §7 consequence 1).

2. **Determine `emission_shape` + `findings_locus`** — which gh surface actually carries the
   findings (`review` vs `issue_comment` vs `check_run`). Capture all three surfaces and observe
   which is non-empty for the Augment author:
   ```
   gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews            # reviews[].body / state
   gh api repos/IronbellyOrg/IronClaude/pulls/<N>/comments           # inline review comments (path,line,body,id,in_reply_to_id)
   gh api repos/IronbellyOrg/IronClaude/issues/<N>/comments          # PR conversation (issue_comment) — note: issues/ not pulls/
   gh api repos/IronbellyOrg/IronClaude/commits/<headSHA>/check-runs # check_run.output.{title,summary,text,annotations}
   ```
   Whichever carries the Augment findings sets `emission_shape` and `findings_locus`
   (`reviews[].body` | `comments[]` | `check_run.output`).

3. **Locate `severity_field_path`** — does Augment self-report a severity, and where (a JSONPath into
   the finding payload, or `null` if severity is only prose in the body)? This is a *hint*, never
   authoritative (re-graded via the reused rubric, FR-3.1).

4. **Capture `review_completeness_signal`** — the marker that says "the review is finished, not
   mid-stream" (`state == "COMMENTED"` on the review object, or presence of a summary marker in the
   body). Needed so the poller does not classify a partial emission as "clean".

5. **Persist `probe_evidence`** — write the raw captured JSON to an absolute path under the run's
   output dir (e.g. `.dev/pr-monitor/probe/augment-review-<N>.json`) and record that path in the
   contract as the provenance for the lock.

### 1.2 Can it run NOW?

**No — not yet, and the task file must NOT auto-lock.** Evidence:

- **Augment app installation is unconfirmed.** Grep for `augment-code[bot]` / `augment_bot` /
  prior Augment review artifacts under `.dev/` returns only *brainstorm/spec/proposal prose*
  (`.dev/brainstorm/pr-remediation-pipeline-integration-20260531/…`, the merged-spec itself, and the
  TASK-RF-BRV-MG research notes) — **zero captured Augment review JSON** anywhere in the repo. There
  is no `*augment*` evidence file (`find .dev -iname '*augment*'` → empty).
- The repo's **existing** automated PR review is `/sc:auggie-review` (Auggie/Augment *codebase-retrieval*
  used as a review engine **inside** a session), which is a **different thing** from the **Augment Code
  GitHub App** that posts a review **on** the PR. The DET probe targets the latter, and there is no
  in-repo evidence the GitHub App is installed on `IronbellyOrg/IronClaude` or has ever posted.
- Confirming installation is itself an operator step:
  `gh api repos/IronbellyOrg/IronClaude/installation` (app installed on repo) or, after a real PR,
  observing an Augment-authored review. **R6 was instructed NOT to run a live probe**, so this stays
  characterized, not executed.

### 1.3 How the task file should encode the probe

Encode it as a **gating prerequisite checklist item (build step 0) that HALTs for a human/operator**,
exactly mirroring the §3 DAG and the `feedback_human_decision_items_must_halt` memory:

- A **`needs_human_decision` / operator item** named e.g. *"Run R1 Augment detection probe and lock
  `detection-contract.md`"* that:
  - Lists the 5 capture commands (§1.1) as the operator runbook (single-line, absolute-path,
    `--repo`-pinned — NFR-5).
  - **Writes `PENDING` and HALTs** the dependent build items (C1 skeleton onward); it must **never
    auto-apply a default `augment_bot_login` and ship** (that is precisely the
    `feedback_human_decision_items_must_halt` failure mode, and §7's "NOT hard-guessed").
  - Has acceptance = `detection-contract.md` exists with `locked: true` AND `probe_evidence` points at
    a real captured JSON file. (Programmatic check: `grep -q '^locked: true' detection-contract.md`.)
- **Synthetic fixtures unblock everything else (§18.4).** All of steps 2–5 of the build DAG are
  internal-pure and testable with the synthetic `tests/submit_pr/fixtures/*.json` (review-clean.json,
  review-with-findings.json, review-non-augment.json, review-interleaved.json, finding-*.json). These
  follow the *expected* GitHub API response schema and let the FSM/router/loop-guard/reply tests run
  with **zero network**. The §18.4 contract: once the real probe completes, a **schema-validation test
  re-asserts fixture parity** against the real captured shape (and the fixtures are regenerated from
  real data). So the task file should: (a) ship synthetic fixtures now, (b) add the parity/regenerate
  test as a post-probe item, (c) keep the `locked` gate as the only thing the probe unblocks.
- **T-210 is the mechanical enforcement**: contract `locked:false`/absent ⇒ skill HALTs with a
  "probe first" error. The task file's detection-contract item and its test (`test_detection_contract.py`)
  must include this assertion so the gate is *proven*, not just documented.

This makes R1 a **mechanically-enforced sequencing dependency** (§7 consequence 3), not a "should".

---

## Section 2 — gh API Surfaces (poller / reply / resolve)

All commands pin `--repo IronbellyOrg/IronClaude`; every `gh api` path is
`repos/IronbellyOrg/IronClaude/...` (FR-1.3 / AC-7 / §19.2). Static test T-104 greps all sources for a
bare `gh ` without `--repo`; runtime T-105 asserts `--repo` present.

### 2.1 Poller surface (FR-2.1)

**Primary `gh pr view`** (exact `--json` field set from the spec, FR-2.1):
```
gh pr view <N> --repo IronbellyOrg/IronClaude \
  --json number,url,headRefName,headRefOid,baseRefName,reviews,comments
```
- `headRefOid` = the head SHA (used by INV-001 `sha_attributed_to_our_push` and for `commit_id` in
  inline replies and `/commits/<sha>/check-runs`).
- `reviews` = array of `{author{login}, authorAssociation, state, body, submittedAt, url}`.
- `comments` = PR conversation (issue) comments — NOT inline review comments.

**REST poll surfaces** (`gh pr view` does not expose inline-comment ids or `in_reply_to_id`, which the
reply step needs — so REST is required):
```
gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews                  # review objects: id, user.login, state, body
gh api repos/IronbellyOrg/IronClaude/pulls/<N>/comments                 # inline review comments: id, path, line, body, commit_id, in_reply_to_id, pull_request_review_id
gh api repos/IronbellyOrg/IronClaude/commits/<headSHA>/check-runs       # only if probe shows emission_shape==check_run
```
Classification is **pure** against the probe-locked `DetectionContract` (§7): key on
`augment_bot_login`; three states no-review / clean / findings (T-201/202/203); non-Augment author ⇒
"review not detected" (T-211/T-N31).

**Backoff (FR-2.5 / NFR-2):** on HTTP 403 / 429 / secondary-rate-limit (gh surfaces these as non-zero
exit + a message on stderr), exponential 30→60→120→…cap 300s; backoff counts toward the wall-clock
timeout (default 1800s). The poll script returns the status so the FSM (not the script) does the
backoff arithmetic — keeping `gh` out of the deterministic core (NFR-6).

### 2.2 Reply surface (FR-6.1) — REST `in_reply_to` (CONFIRMED exact)

GitHub REST, **verified against docs.github.com/rest/pulls/comments "Create a reply for a review
comment"**:
```
POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies   body: { "body": "<text>" }
```
- `comment_id` **MUST be a top-level review comment** ("Replies to replies are not supported.") — so
  the reply targets the original Augment inline finding comment id captured in §2.1.
- `gh api` shape (single-line, NFR-5):
  ```
  gh api --method POST repos/IronbellyOrg/IronClaude/pulls/<N>/comments/<COMMENT_ID>/replies -f body="<reply-text>"
  ```
- This is the **thread-scoped reply** the spec wants (FR-6.5 "posted inline on the finding's source
  line"). The reply body must cite `applied_edits` status (FR-6.1 / INV-009): an `applied_edits==0`
  cycle says **"no code change applied"**, never "resolved" (T-603).
- For a **clean re-review summary** (FR-6.5: one summary thread, not N comments) and the §17 residual
  summary, the conversation-level comment is the issues endpoint:
  `gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body=...` (every PR is
  also an issue — confirmed GitHub community #167260).

> **Prior art in-repo:** `sc-auggie-review-protocol/SKILL.md` (lines 304–314) already posts inline
> comments via `gh api repos/<owner>/<repo>/pulls/<PR>/comments -f body=... -f commit_id=... -f
> path=... -F line=N -f side=RIGHT` and a summary via `gh pr review <PR> --comment --body-file ...`.
> That is the **create-a-new-comment** surface; this skill additionally needs the **reply-to-existing**
> surface (`.../comments/<id>/replies`) + the resolve mutation, which auggie-review does NOT have.
> Reuse the `--repo` pinning + body-file discipline; add the reply+resolve helper as genuinely new (C4).
> Note auggie-review uses `-F line=N` (`-F` = typed/number field) vs `-f` (raw string) — same
> distinction applies here.

### 2.3 Resolve surface (FR-6.2 / FR-6.1) — GraphQL `resolveReviewThread` (no REST/gh-native path)

There is **no REST endpoint** and **no native `gh pr` verb** to resolve a review thread (cli/cli#12419
unimplemented; community #44650, reddit confirm GraphQL-only). The exact mechanism is two GraphQL
calls via `gh api graphql`:

**(a) Obtain the thread node id** — REST `comment_id`/`review_id` are NOT GraphQL thread node ids
(the documented mismatch, reddit r/github). Walk the PR's `reviewThreads` connection and match the
thread containing the Augment comment (by `path`+`line` or by the comment's databaseId):
```
gh api graphql -f query='
  query($owner:String!,$repo:String!,$pr:Int!){
    repository(owner:$owner,name:$repo){
      pullRequest(number:$pr){
        reviewThreads(first:100){
          nodes{ id isResolved path line
                 comments(first:1){ nodes{ databaseId author{login} } } }
        }
      }
    }
  }' -f owner=IronbellyOrg -f repo=IronClaude -F pr=<N>
```
The matching node's `id` is the `threadId` (a base64 node id, e.g. `PRRT_…`).

**(b) Resolve it** (mutation verified to exist; input = `threadId`, returns `clientMutationId` +
`thread`; community #44650 / reviewdog#1720):
```
gh api graphql -f query='
  mutation($threadId:ID!){
    resolveReviewThread(input:{threadId:$threadId}){
      thread{ id isResolved }
    }
  }' -f threadId=<THREAD_NODE_ID>
```
- **Permissions caveat (community #44650):** `resolveReviewThread` needs **Pull Requests: read+write**
  on the authenticating identity; a GitHub App integration without it gets *"Resource not accessible by
  integration."* Since this skill authenticates as the **user's `gh` token** (NFR-7: authenticated `gh`
  + local git only), and the user owns the fork, this is satisfied — but the error-handling table
  should map this 403/forbidden to a HALT with a clear "needs PR read+write" message, not a silent
  retry.
- Idempotency: skip if the thread node already shows `isResolved:true` (the `resolved_thread_ids` set,
  §11.4) — append `idempotency_skip` rather than re-mutate (T-N01/N02 family).
- FR-6.1 ordering: **reply first, then resolve** (reply summarizes fix+SHA+passing validation, then the
  thread is resolved via the mutation, T-601→T-602).

### 2.4 PR-create surface (FR-1.4) — recap (owned mainly by R1/R2, noted for completeness)

`gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title … --body …`
(the CLAUDE.md mandatory shape). Pre-checks: `git remote -v` (origin==fork), `gh auth status`,
`git fetch origin` + rebase if behind `origin/master`, and verify the returned URL host is
`IronbellyOrg/IronClaude` (T-106/107/108; FM-11 misroute → `terminal_failed`). The existing
`offer-pr-review.sh` hook already extracts the PR URL/number from `gh pr create` stdout via
`grep -oE 'https://github\.com/[^[:space:]]+/pull/[0-9]+'` — reuse that extraction for the poller's
PR number.

---

## Section 3 — Hook + Bash Script Test Patterns (informs poll/reply script tests)

### 3.1 The established pattern: subprocess + JSON-stdin fixture

`tests/hooks/` tests bash hooks with **`subprocess.run(["bash", str(HOOK)], input=json.dumps(payload).encode(), capture_output=True, env=env, timeout=5)`** and assert on `returncode` / `stdout` / `stderr` / telemetry-file content. Canonical examples:
- `tests/hooks/test_freshness_pre_edit_create_case.py` — `_run_hook(payload, fake_home)` builds a
  `{session_id, tool_name, tool_input, cwd}` dict, pipes it as JSON stdin, sets `HOME` to a `tmp_path`
  fake-home, and asserts `returncode == 0/2` + a telemetry JSONL string (`'"reason":"create_allowed"'`).
- `tests/hooks/test_auggie_first.py` / `test_auggie_flag_clear_mcp_prefix.py` — same `_run_hook`
  shape; `HOOK = Path(__file__).resolve().parents[2] / "src/superclaude/hooks/scripts/<name>.sh"`
  (tests point at the **`src/` source of truth**, never `.claude/`).

Key conventions to copy for `tests/submit_pr/test_hook_update.py` (T-701..T-703):
- Resolve the script under `src/superclaude/...` via `Path(__file__).resolve().parents[N]`.
- Feed the **exact hook payload contract** the script parses. `offer-pr-review.sh` reads
  `.tool_name` (must == "Bash"), `.tool_input.command`, `.tool_response.error`,
  `.tool_response.stdout`/`.output`. T-701 asserts stdout contains **both** `/sc:auggie-review` and
  `/sc:submit-pr --monitor`; T-702 asserts exit 0 on non-matching input; T-703 asserts exit 0 on a
  failed `gh pr create` (`.tool_response.error` non-empty).
- `timeout=5`, `capture_output=True`, decode stderr in the assert message.

### 3.2 Pattern for the NEW scripts (`poll-augment-review.sh`, `reply-resolve-thread.sh`)

These are **not** Claude-Code hooks (no stdin JSON envelope) — they are **CLI wrapper scripts** the
skill invokes, so the test pattern adapts: the spec's §18.3 mock strategy mandates **`gh` mocked at the
subprocess boundary with pre-built JSON fixtures**. Two viable harnesses, both consistent with repo
conventions:
- **PATH-shim mock**: prepend a `tmp_path/bin` containing a fake `gh` shell script that `cat`s a
  fixture matching the requested subcommand, set `env["PATH"]`, run the real script via `subprocess`,
  assert on the script's stdout (the single JSON event line for `poll-augment-review.sh`) / on the
  argv the fake `gh` recorded (to prove `--repo` pin, `-f body=…`, the mutation query). This mirrors
  the `tests/hooks` subprocess discipline while satisfying §18.3's "gh via subprocess mock".
- **Argv-capture**: the fake `gh` appends `"$@"` to a log file; the test reads the log to assert the
  exact command shape (FR-1.3 `--repo` static intent, T-105 runtime; resolve mutation present).

`poll-augment-review.sh` contract (C2): single poll → emits **one JSON line** to stdout (the
Monitor-stream event), exits 0. Test: feed fixture review JSON via the fake `gh`, assert the emitted
line is valid JSON with the classified state (`polling`/`clean`/`findings`) and that **no `gh` call
lacked `--repo`**. `reply-resolve-thread.sh` contract (C4): REST reply then GraphQL resolve; test
asserts both calls fired in order, the reply body cited `applied_edits` status, and a pre-resolved
thread is skipped (idempotency).

These bash-script tests are the `@pytest.mark.integration` "subprocess hooks" row of §6.1 / §18.2.

---

## Summary (for parent agent)

1. **DET probe is a manual operator step that CANNOT run now and must HALT the build.** No `upstream`
   remote exists (PR-target pin is mandatory). There is **zero captured Augment GitHub-App review JSON**
   anywhere in `.dev/` — only prose mentions; the in-repo `/sc:auggie-review` is a *different* thing
   (in-session Augment retrieval, not the GitHub App). The probe is 5 `gh`/`gh api` captures
   (`pulls/<N>/reviews` for bot login+association+`[bot]` suffix; reviews vs `pulls/<N>/comments` vs
   `issues/<N>/comments` vs `commits/<sha>/check-runs` for emission_shape/findings_locus;
   severity_field_path; review_completeness_signal; persist probe_evidence). **Encode it as a
   `needs_human_decision` build-step-0 item that writes PENDING + HALTs, never auto-locks** (per
   `feedback_human_decision_items_must_halt` + §7 "NOT hard-guessed"); acceptance = `locked: true` +
   real `probe_evidence` path; T-210 mechanically enforces the gate. Synthetic fixtures (§18.4) unblock
   all other steps now; a post-probe schema-parity test regenerates fixtures from real data.

2. **gh surfaces (all `--repo IronbellyOrg/IronClaude` pinned):**
   - Poll: `gh pr view <N> --json number,url,headRefName,headRefOid,baseRefName,reviews,comments` +
     `gh api .../pulls/<N>/reviews` + `.../comments` (+ `.../commits/<sha>/check-runs` if check_run shape).
   - Reply (CONFIRMED vs GitHub REST docs): `POST .../pulls/<N>/comments/<COMMENT_ID>/replies` with
     `-f body=...` — `comment_id` must be a **top-level** review comment; conversation summary via
     `issues/<N>/comments`.
   - Resolve (GraphQL-ONLY — **no native `gh` verb**, gh 2.45.0; cli/cli#12419 open): two
     `gh api graphql` calls — query `pullRequest.reviewThreads.nodes{id,isResolved,path,line,...}` to
     get the **thread node id** (REST ids ≠ GraphQL thread ids), then `resolveReviewThread(input:{threadId})`.
     Needs PR read+write on the user token (community #44650 → map "Resource not accessible" to a HALT).
   - **In-repo prior art:** `sc-auggie-review-protocol/SKILL.md:304-314` already does
     `gh api .../pulls/<PR>/comments -f body -f commit_id -f path -F line -f side=RIGHT` + summary via
     `gh pr review --comment --body-file`; reuse the `--repo`/body-file/`-F`-vs-`-f` discipline. It does
     **NOT** have reply-to-existing or resolve — those are genuinely new (C4).

3. **Hook/script test pattern:** `tests/hooks/*` = `subprocess.run(["bash", HOOK], input=json.dumps(payload).encode(), capture_output, env, timeout=5)`, HOOK resolved under `src/superclaude/hooks/scripts/` (never `.claude/`), assert returncode/stdout/stderr/telemetry-JSONL. For `offer-pr-review.sh` edit (T-701..703): payload `{tool_name:"Bash", tool_input.command, tool_response.{error,stdout}}`; assert stdout has **both** `/sc:auggie-review` and `/sc:submit-pr --monitor`, exit 0 on non-match + failed-create. The NEW CLI wrapper scripts (`poll-augment-review.sh`, `reply-resolve-thread.sh`) aren't hooks (no stdin envelope) — test via a **PATH-shim fake `gh`** that cats fixtures + records argv (satisfies §18.3 "gh via subprocess mock + JSON fixtures"); assert the emitted single JSON event line + `--repo` on every call + reply-then-resolve order + idempotent skip.

**Sources:** merged-spec §3/§7/§18.3/§18.4/§19; `src/superclaude/hooks/scripts/offer-pr-review.sh`;
`tests/hooks/test_freshness_pre_edit_create_case.py`, `test_auggie_first.py`;
`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:304-314`; GitHub REST docs
(docs.github.com/rest/pulls/comments — reply endpoint verified); GitHub community discussions #44650
(resolveReviewThread permissions), #167260 (issues-vs-pulls comments); cli/cli#12419 (no native resolve
verb); reviewdog#1720 + r/github (GraphQL-only resolve). `git remote -v` (no upstream), `gh 2.45.0`.
