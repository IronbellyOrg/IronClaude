# Research: Finding-schema standards and review-bot practice (W4)
**Topic:** SARIF 2.1.0, reviewdog rdjson, GitHub code scanning and PR review comment APIs, review-bot severity/confidence/dedup/resolution, minimal interoperable finding record
**Scope:** external web research only (Tavily); codebase is source of truth
**Status:** Complete
**Date:** 2026-11-14
**web-provenance:** provider=tavily
**Codebase context (from the task prompt, not re-verified here):** review package has two finding contracts (v1 anchor quotes plus category set; v2 path:line citations plus optional lens); `src/superclaude/pr_submit/` has its own severity router and third-party reviewers (Augment, Codex); a future PR-code-review module needs a file-and-line location type.
---

## 1. SARIF 2.1.0 result and location model

### 1.1 Result object: kind vs level, location, identity
- **Source:** https://sarif.info/Result (secondary explainer of the OASIS text; reliability: well-maintained reference site, below the standard itself); https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html (official standard, OASIS SARIF 2.1.0 Plus Errata 01)
- **Key information:**
  - A SARIF `result` carries `ruleId`, `message`, `locations[]`, optional `relatedLocations[]`, `kind`, `level`, `fingerprints`, `partialFingerprints`, `guid`, `correlationGuid`, `baselineState`.
  - `kind` (evaluation state, spec 3.27.9) and `level` (how bad) are separate properties. `kind` values listed on sarif.info: `notApplicable`, `pass`, `fail`, `review`, `open`, `informational`. `level` values used throughout the sources: `error`, `warning`, `note`.
  - Identity across runs: `guid` identifies the result in one run; `correlationGuid` identifies the equivalence class of logically identical results across runs; `fingerprints` are full stable identities; `partialFingerprints` contribute to identity and are expected to change when surrounding code changes; `baselineState` is one of `new`, `unchanged`, `updated`, `absent`.
  - Location: `locations[].physicalLocation.artifactLocation.uri` (+ optional `uriBaseId` such as SRCROOT) and `region` (`startLine`, `startColumn`, `endLine`, `endColumn`). Spec 3.29.4 (OASIS): if `region` is absent the physicalLocation refers to the entire artifact (file-level finding).
- **Relation to codebase:** EXTENDS. The v2 contract (path:line citation) maps cleanly to `artifactLocation.uri` + `region.startLine`; the v1 anchor-quote location has no SARIF-native location analogue. SARIF separates "state" (`kind`/`baselineState`) from "severity" (`level`), which matches a panel that needs both a severity and a verdict/resolution state on one finding.
- **Relevance:** HIGH

### 1.2 SARIF in practice: GitHub code scanning subset
- **Source:** https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support (official GitHub docs)
- **Key information:** The GitHub-consumed example has `tool.driver.rules[]` with `id`, and in rule `properties` the keys `kind` (e.g. `path-problem`), `problem.severity` and `security-severity` (a numeric string such as `9.8`); results carry `ruleId`, `message.text`, `locations[].physicalLocation` with `artifactLocation.uri` and `region.startLine/startColumn/endColumn`, and `partialFingerprints` with `primaryLocationLineHash` (example value `39fa2ee980eb94b0:1`) and `primaryLocationStartColumnFingerprint`. `relatedLocations[]` carry an `id`, location and message. Relative URIs with `uriBaseId: "%SRCROOT%"` are the producer guidance.
- **Relation to codebase:** EXTENDS. A minimal interoperable location is (relative path, start line, optional end line, optional column), and the dedup fingerprint is a hash of line content plus an occurrence counter, not the line number. Our v1 anchor quote is conceptually the same idea as a content-based fingerprint, which survives line drift; a bare path:line citation does not.
- **Relevance:** HIGH

### 1.3 SARIF limitations noted by practitioners
- **Source:** https://boostsecurity.io/blog/sarif-cant-save-you-now (vendor blog; reliability: blog post)
- **Key information:** The spec calls for stable fingerprints and has an appendix on fingerprint properties (deterministic computation; incorporate tool name, rule ID and physical location of the target). Vulnerability-management needs (new/unchanged/fixed state, approved suppression, remediation validation) are representable in the schema, but consumers must still apply them in context; partial fingerprints exist to follow findings through code motion.
- **Relation to codebase:** SUPPORTS keeping finding state across review rounds (ledger) as a layer on top of the finding record rather than inside it.
- **Relevance:** MEDIUM

### 1.4 Ingestion behaviour of a third-party consumer (GitLab)
- **Source:** https://docs.gitlab.com/user/application_security/detect/sarif (official GitLab docs)
- **Key information:** GitLab requires `ruleId` and a physical location (findings without either are not added); severity defaults to `medium` when unset; finding identity = report type + fingerprint of `ruleId` + location fingerprint of the form `file:startLine:endLine`; results in the same file with the same `ruleId` and no `region` collapse into one finding and the rest are silently discarded.
- **Relation to codebase:** EXTENDS, a concrete pitfall: if a unified finding record lets `location` be file-only, or lets `category` stand in for a rule id, a downstream consumer can silently dedup distinct findings. Suggests requiring a line (or a content anchor) plus a category/rule id on every record meant to be exported.
- **Relevance:** MEDIUM

---

## 2. reviewdog Diagnostic Format (rdjson / rdjsonl)

### 2.1 RDFormat shape
- **Source:** https://github.com/reviewdog/reviewdog/blob/master/proto/rdf/README.md (official repository documentation, well-maintained); https://github.com/reviewdog/reviewdog (main repo README)
- **Key information:**
  - rdjson top level: `source {name, url}`, `severity` (default for the set), `diagnostics[]`. rdjsonl is one diagnostic per line.
  - Diagnostic: `message`, `location {path, range {start {line, column}, end {line, column}}}` (end optional), `severity` (`ERROR`/`WARNING`/`INFO`), `code {value, url}` (rule id with doc link), `suggestions[] {range, text}` (replacement text for the range).
  - Stated purpose: a generic protocol between diagnostic tools and development tools (editors, reviewdog, code review APIs); supports multiline ranged comments, severity, rule code with URL, and code suggestions; suggestions are applied only by reporters that support them (github-pr-review, gitlab-mr-discussion, local).
  - reviewdog reporters include `github-pr-review`, `github-pr-check`, `github-annotations`/`github-pr-annotations` (GitHub Actions `::error line=,col=,file=::` commands) and `local`.
- **Relation to codebase:** EXTENDS. rdjson is the closest existing format to "a PR-review finding": path + range + severity + rule code + optional suggested fix, with no confidence, dedup or resolution fields. A shared finding record that can be projected into rdjson (message, path, line range, severity, code=category) would let a future PR-code-review module reuse reviewdog reporters instead of writing its own GitHub poster. Its three-level severity (ERROR/WARNING/INFO) maps one-to-one onto SARIF `error/warning/note`.
- **Relevance:** HIGH

---

## 3. GitHub pull-request review comment API

### 3.1 Create a review comment (single) and create a review (batch)
- **Source:** https://docs.github.com/rest/pulls/comments and https://docs.github.com/rest/pulls/reviews (official GitHub REST docs)
- **Key information:**
  - `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments`: parameters `body`, `commit_id`, `path`, `line`, `side` (`LEFT`/`RIGHT`), optional `start_line` and `start_side` for multi-line comments. `position` (lines down from the first `@@` hunk header) is described as "closing down"; if `position` is used, `line/side/start_line/start_side` are not required. 422 on validation failure or if the endpoint is spammed; the endpoint triggers notifications and can hit secondary rate limits.
  - `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`: body has `commit_id` (not using the latest SHA may render comments outdated), `body`, `event`, and `comments[]` each with `path` (required), `body` (required), and `position` or `line`/`side`/`start_line`/`start_side`.
- **Relation to codebase:** EXTENDS. The location type a PR-code-review module needs is `(path, line, side, optional start_line/start_side, commit_id)`. `commit_id` is required context that the v1 anchor and v2 path:line contracts do not appear to carry (not verified against the code here): without a commit SHA a line citation is not reproducible against a moving PR head.
- **Relevance:** HIGH

### 3.2 Practical constraints reported by users
- **Source:** https://github.com/orgs/community/discussions/202426 ; https://github.com/cli/cli/issues/13358 ; https://github.com/orgs/community/discussions/187218 ; https://github.com/orgs/community/discussions/168380 ; https://github.com/orgs/community/discussions/143197 (all GitHub community discussions or issues; reliability: forum answers, lowest tier)
- **Key information (user reports, not official statements):**
  - The create-review endpoint returns comment objects in the older position/diff_hunk shape with `line`/`side` null; re-fetching by comment id (`GET /pulls/comments/{id}`) returns the line model.
  - One report: a direct `gh api` call to the single-comment endpoint with `start_line`/`start_side`/`line`/`side` returned 422, while the same comment inside a review `comments[]` array worked.
  - Comments on lines outside the diff hunks are rejected with 422 `pull_request_review_thread.line is not part of the diff`, although the web UI allows commenting on unchanged lines of changed files (announced Sept 2025); API support was reported as limited.
  - No API (REST or GraphQL) to append comments to an existing pending review (feature request); file-level comments cannot be mixed with line comments inside one review via REST (Oct 2024 answer).
- **Relation to codebase:** EXTENDS and constrains. A PR-code-review module cannot post a finding whose line is outside the diff; the finding record therefore needs a "postable vs report-only" distinction (a finding outside the diff must degrade to the review body or a file-level comment). The existing fork-only `pr_submit` flow is unaffected (this is a posting-time constraint).
- **Relevance:** MEDIUM (forum reports; verify against the current API before relying on any of them)

---

## 4. Severity models in code scanning and review bots

### 4.1 GitHub code scanning: two severity ideas
- **Source:** https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts (official); https://github.blog/changelog/2021-07-19-codeql-code-scanning-new-severity-levels-for-security-alerts (official changelog); https://safeguard.sh/resources/blog/sarif-security-severity-how-github-maps-scores-to-levels (blog, secondary)
- **Key information:** All code scanning alerts have a level of Error, Warning or Note. Security alerts additionally carry a security severity of Critical/High/Medium/Low derived from a numeric `security-severity` score (0.1-3.9 low, 4.0-6.9 medium, 7.0-8.9 high, 9.0-10.0 critical; 0.0 none) following CVSS; when present, security severity is displayed and used in preference to level. PR check failure defaults: security-severity critical or high fails the check; for non-security alerts severity `error` fails the check; both thresholds are configurable (repository settings or rulesets: "Errors", "Errors and Warnings", "All"; security "High or higher", "Medium or higher", "All").
- **Relation to codebase:** EXTENDS. This is the standard pattern for a severity router: a coarse 3-level result severity plus an optional finer score, and a configurable gate threshold decoupled from the finding. It parallels the `pr_submit` severity router (fixes confirmed findings of Medium or higher per the repo CLAUDE.md; lower ones only reported): the router threshold should be configuration over a shared ordinal scale, not a property of the finding record.
- **Relevance:** HIGH

### 4.2 CodeRabbit: severity, category, type and effort as independent axes
- **Source:** https://docs.coderabbit.ai/change-stack/findings and https://docs.coderabbit.ai/guides/code-review-overview (official vendor docs); https://docs.coderabbit.ai/guides/dashboard-metrics (official)
- **Key information:** A finding carries labels from four independent closed vocabularies, explicitly "not one severity ladder": Type (Nitpick, Potential issue, Refactor suggestion); Severity (ranked critical, major, minor, trivial; plus `info` and `none` outside the ranking); Category (six areas: functional correctness, security and privacy, data integrity and integration, performance and scalability, stability and availability, maintainability and code quality); Effort (cost to fix). Overview items also carry a priority band p1-p4. Acceptance rate is computed per severity and per category as accepted comments / posted comments, where "accepted" means CodeRabbit can verify the feedback was addressed.
- **Relation to codebase:** SUPPORTS. Our v1 contract's category set and the v2 contract's optional lens are both "what area" axes; CodeRabbit's model confirms severity and category must stay orthogonal and that a lens/category is a label, not a filter or a severity. The acceptance-rate metric is a resolution-derived measure that needs a per-finding resolution state in the ledger.
- **Relevance:** HIGH

### 4.3 Greptile: per-PR confidence score and severity threshold
- **Source:** https://www.greptile.com/docs/code-review/first-pr-review and https://www.greptile.com/agent (official vendor docs); https://www.greptile.com/what-is-ai-code-review (vendor marketing, treat statistics as vendor-reported)
- **Key information:** Greptile assigns a 0-5 confidence score per pull request (5 production ready ... 0-1 critical problems) computed from the severity and quantity of issues, change complexity and alignment with codebase patterns; inline comments carry severity levels and suggested fixes; a configurable severity threshold filters noise so only high-impact issues surface. The vendor states the score is a triage tool, not a rubber stamp.
- **Relation to codebase:** EXTENDS. For the rf-qa replacement ("checklist-and-confidence model") the bot practice puts confidence at the unit-of-review level (PR/document verdict), not on each finding; per-finding confidence is not part of the SARIF or rdjson models. Suggests: finding record stays confidence-free (or carries an optional field), verdict record carries the confidence.
- **Relevance:** MEDIUM

### 4.4 Observed bot behaviour on re-review (user-level evidence)
- **Source:** https://t2informatik.de/en/blog/how-effective-are-ai-code-reviews (blog); https://www.morphllm.com/comparisons/greptile-vs-copilot (vendor comparison with benchmark figures, treat as unverified)
- **Key information:** One evaluation reports GitHub Copilot review surfaced new comments on re-run that did not relate to the latest changes and should have appeared earlier (unstable finding set across runs), and Greptile placing some findings only in the summary rather than as inline comments. Precision and recall figures quoted in the comparison are vendor-reported benchmarks (e.g. Greptile 66.2% precision, Copilot 56.5%); not independently verified here.
- **Relation to codebase:** SUPPORTS the need for a stable finding identity (dedup key) across review rounds in the ledger, so that re-runs can be compared; does not contradict any code finding.
- **Relevance:** LOW

### 4.5 Codex review (third-party reviewer already used by pr_submit): P0-P3 priority tags
- **Source:** https://learn.chatgpt.com/docs/third-party/github (official OpenAI docs); https://gist.github.com/cbh123/ce4893a10ed2b87a89d9114b08118a08 (gist reproducing codex-rs/core/review_prompt.md; reliability: secondary copy of a repo file, the prompt may have changed); https://www.cubic.dev/blog/codex-code-review and https://www.qodo.ai/glossary/what-is-codex-code-review (competitor blogs, treat as secondary); https://github.com/openai/codex/issues/27691 (issue on the official repo)
- **Key information:**
  - Official docs: on GitHub, Codex posts a standard GitHub review and flags only P0 and P1 issues; comments carry a `[P1]` title tag plus an explanation; repository guidance comes from `AGENTS.md`.
  - The gist of the review prompt defines P0 (drop everything), P1 (urgent), P2 (normal), P3 (low), asks for the line range to be kept short (avoid ranges over 5-10 lines), a numeric `priority` field 0-3 (null if unknown), and an "overall correctness" verdict that ignores non-blocking issues such as style and typos.
  - Issue 27691 (user report): when Codex finds an issue it creates a formal `COMMENTED` PullRequestReview with a full `commit_id` and inline comments; when it finds nothing it posts only an issue comment (short SHA in prose) and a reaction, so a clean result cannot be bound to the exact PR head SHA.
  - Third-party action `gersmann/codex-review-action` (GitHub Marketplace): skips findings whose line is not in the current diff; on re-runs does semantic dedup against prior unresolved comments and re-adjudicates which prior comments are still relevant; reports new and still-relevant prior findings separately.
- **Relation to codebase:** EXTENDS and partly CONTRADICTS an assumption. Codex uses a 4-step P0-P3 ordinal and shows only P0/P1 on GitHub, while CodeRabbit uses critical/major/minor/trivial/info and SARIF uses error/warning/note. The in-repo `pr_submit` severity router therefore must normalise at least three vendor vocabularies (and Augment's, not researched here: no official source found in this pass) onto one internal ordinal; a unified finding record's `severity` should be the internal ordinal with the vendor label kept as an opaque string for audit. The "overall correctness verdict" is a verdict-level record, separate from findings, which matches the planned cluster/verdict/ledger split. The clean-result-has-no-SHA gap is a concrete reason for the ledger to record the reviewed head SHA itself.
- **Relevance:** HIGH

---

## 5. Resolution, suppression and dedup vocabularies

### 5.1 GitHub review threads: resolved state lives on the thread, not the comment
- **Source:** https://github.com/cli/cli/issues/12419 (cli/cli issue showing the GraphQL calls; forum-level reliability); https://github.com/orgs/community/discussions/19206 ; https://github.com/orgs/community/discussions/196714 ; https://github.com/orgs/community/discussions/187953 (community discussions, forum-level). No official GitHub GraphQL reference page was fetched in this pass, so the mutation names below are user-reported.
- **Key information (user reports):** Resolving a review conversation uses the GraphQL mutations `resolveReviewThread` and `unresolveReviewThread` with a thread node id (`PRRT_...`) taken from `reviewThreads.nodes[].id`; `isResolved` is a thread field; replies use `addPullRequestReviewThreadReply`. REST does not return thread node ids. Reports say a Copilot coding agent's `GITHUB_TOKEN` could not call `resolveReviewThread` and that Copilot re-review leaves earlier comments behind (feature request to mark them outdated or dismiss them).
- **Relation to codebase:** EXTENDS and matches the CLAUDE.md description of `/sc:pr-submit` (replies to and resolves review comments it fixed): the unit of resolution is a thread id, so a ledger row for a PR finding needs a `thread_id` (and comment id), in addition to path and line.
- **Relevance:** MEDIUM

### 5.2 GitHub code scanning alert state and dismissal reasons
- **Source:** https://docs.github.com/rest/code-scanning/code-scanning (official GitHub REST docs)
- **Key information:** Alert `state` is `open` or `dismissed`; `dismissed_reason` is required when dismissed and is one of `false positive`, `won't fix`, `used in tests`, `mitigated` (or null); `dismissed_comment` is free text. The alert response also shows `rule {id, severity, tags, description}`, `tool {name, guid, version}`, and `most_recent_instance {ref, commit_sha, message, location {path, ...}}`, so an alert is a rule-level object with per-commit instances.
- **Relation to codebase:** EXTENDS. A small closed resolution vocabulary with a mandatory reason when closing without a fix is a ready-made model for the ledger's disposition field (for example fixed, rejected as false positive, accepted as won't-fix). The alert/instance split mirrors the cluster/finding split in the planned shared core.
- **Relevance:** MEDIUM

### 5.3 SARIF suppressions and baseline state
- **Source:** https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html (official standard); https://github.com/advanced-security/dismiss-alerts (GitHub-maintained action repository)
- **Key information:** A SARIF `suppression` object has a `kind` (`inSource`, which is a syntactic construct in the code, or `external`; only `inSource` text was seen in this extraction) and, per the standard's rationale text, `suppressions` is either null for all results or non-null for all results in a run, so a consumer can tell whether suppression information is available from one result. `baselineState` records state against a previous run (`new`, `unchanged`, `updated`, `absent`). Per the standard, `kind` defaults to `fail` and any `level` other than `none` requires kind `fail`. The `dismiss-alerts` action maps SARIF suppressions to GitHub alerts by matching rule id + file + line + column and dismisses with reason `won't fix` and comment `Suppressed via SARIF`.
- **Relation to codebase:** EXTENDS. Suppression in SARIF is a property of the result (in-source marker or external decision) and the cross-run state is a separate property; the planned ledger can adopt the same split (decision recorded with who/why, state vs previous round). The identity key used by interop tooling is rule id + file + line + column, again an argument for a location with line and an id-like category on every exported finding.
- **Relevance:** MEDIUM

### 5.4 Cross-round dedup and carry-forward in review bots
- **Source:** https://github.com/marketplace/actions/codex-code-review-actor (GitHub Marketplace listing of a third-party action; reliability: well-maintained repo-level docs, not official); https://t2informatik.de/en/blog/how-effective-are-ai-code-reviews (blog)
- **Key information:** The action passes prior unresolved comments to the model so it avoids reposting them, then asks the model separately to mark which prior comments are still relevant, and reports new and still-relevant counts separately; it deletes its own prior summary comment on each run. A blog evaluation observed Copilot re-runs surfacing comments unrelated to the latest changes.
- **Relation to codebase:** SUPPORTS adding a per-finding `status` across rounds (new, carried, resolved, superseded) in the ledger rather than treating each round as a fresh finding list.
- **Relevance:** MEDIUM

---

## 6. What a minimal interoperable finding record needs (synthesis of the sources above)

This is a synthesis by the researcher from the sources cited in sections 1 to 5; it is not a quoted standard.

| Field | Evidence for needing it | Source section |
|---|---|---|
| stable id (rule/category id plus per-finding id) | SARIF `ruleId`, `guid`; rdjson `code.value`; GitLab and GitHub require a rule id to ingest or dedup | 1.1, 1.4, 2.1 |
| location: repo-relative path, start line, optional end line, optional column | SARIF `region`; rdjson `range`; PR API `path`/`line`/`start_line` | 1.2, 2.1, 3.1 |
| location side and commit SHA (only for PR posting) | PR API `side`, `commit_id`; Codex issue about SHA binding | 3.1, 4.5 |
| content anchor or fingerprint (survives line drift) | SARIF `partialFingerprints.primaryLocationLineHash`; our v1 anchor quote | 1.2 |
| message | present in every format | 1.1, 2.1, 3.1 |
| severity as a small ordinal (3-4 levels) plus optional vendor label | SARIF `level`; rdjson ERROR/WARNING/INFO; Codex P0-P3; CodeRabbit 4+2 levels | 2.1, 4.1, 4.2, 4.5 |
| category/lens kept separate from severity | CodeRabbit four independent axes; SARIF rule tags | 4.2 |
| tool/reviewer identity | SARIF `tool.driver`; rdjson `source`; alert `tool` | 1.2, 2.1, 5.2 |
| optional suggested fix | rdjson `suggestions`; GitHub suggestion blocks | 2.1 |
| state/disposition outside the finding (ledger): status vs baseline, dismissal reason, thread id | SARIF `baselineState`/`suppressions`; code scanning `dismissed_reason`; GraphQL thread id | 5.1, 5.2, 5.3 |
| confidence at verdict level, not per finding | Greptile PR-level 0-5 score; Codex overall correctness verdict; no per-finding confidence in SARIF or rdjson | 4.3, 4.5 |

Not found in any source: a standard per-finding confidence field, and a standard "quote anchor" location type; both are our own extensions (v1 anchor quote is closest to SARIF `region.snippet` plus fingerprint, but `snippet` was not verified in this pass).

---

## 7. Discrepancies and caveats
- No external source contradicts a verified code behaviour; none was checked against code in this pass (the research prompt supplied codebase facts only as context). All "relation to codebase" statements rest on those supplied facts and are marked as such.
- Augment's review output format (the second third-party reviewer in `pr_submit`) was not researched; no official source was located in this pass. Gap.
- The GitHub PR API behaviours in 3.2 and 5.1 come from forum or issue reports, not official docs; the API changes (e.g. the `X-GitHub-Api-Version: 2026-03-10` header appears in current official examples), so re-verify before design depends on them.
- Vendor statistics (Greptile precision and recall, merge-time figures) are vendor-reported and are not used as design evidence.
- The SARIF `level` value `none` and the `kind` value list were read from the OASIS text and sarif.info; the full `suppression.kind` and `baselineState` value tables were only partly visible in the extraction.

---

## Key External Findings
1. SARIF 2.1.0 (OASIS) separates what happened (`kind`, `baselineState`) from how bad (`level`: error, warning, note, none) and from cross-run identity (`fingerprints`, `partialFingerprints`, `correlationGuid`); a result without `region` refers to the whole file. [HIGH, official standard]
2. GitHub code scanning consumes a SARIF subset: `ruleId`, relative `artifactLocation.uri`, `region.startLine`, `partialFingerprints.primaryLocationLineHash`; severity is `error`/`warning`/`note` plus an optional numeric `security-severity` (0.1-3.9 low, 4.0-6.9 medium, 7.0-8.9 high, 9.0-10.0 critical) shown in preference to level; the PR check gate is a configurable threshold, not part of the finding. [HIGH, official docs]
3. reviewdog's rdjson is the closest existing format to a PR-review finding: path, line/column range, ERROR/WARNING/INFO, rule code with URL, optional suggestion; it has no confidence, dedup or resolution fields. [HIGH, official repo docs]
4. The GitHub PR review comment API location type is `(path, line, side, optional start_line/start_side, commit_id)`; `position` is being closed down; lines outside the diff are rejected (user-reported, medium reliability). [HIGH for fields, MEDIUM for restrictions]
5. Review bots keep severity, category, type and effort as independent axes (CodeRabbit) and put confidence at the PR or verdict level (Greptile 0-5, Codex overall correctness); Codex uses P0-P3 and shows only P0/P1 on GitHub. [HIGH for CodeRabbit and Codex docs, MEDIUM for Greptile]
6. Resolution is a separate state with a small closed vocabulary (`false positive`, `won't fix`, `used in tests`, `mitigated`) and a mandatory reason; for PR review threads the resolvable unit is a GraphQL thread id. [MEDIUM to HIGH]
7. Dedup in practice relies on rule id + file + line (+ column) or content-hash fingerprints; a missing `region` or rule id causes silent collapse in at least one consumer (GitLab). [MEDIUM, official GitLab docs]

## Recommendations from External Research
These are options for the Section 5.4 external-context discussion; the codebase findings take precedence.
1. Keep one shared finding record with: id, category or rule id, repo-relative path, start line (end line optional), a content anchor (quote or hash), severity as an internal 3-4 level ordinal (vendor label kept as an opaque string), message, reviewer, and lens as a label separate from severity. This is the intersection of SARIF, rdjson and the PR API and lets both the v1 anchor-quote and v2 path:line citation contracts project onto it.
2. Keep disposition, round-to-round status, thread id, dismissal reason and reviewed head SHA in the ledger, not in the finding record, following SARIF `baselineState`/`suppressions` and GitHub alert `dismissed_reason`.
3. Put confidence on the verdict or cluster record (rf-qa replacement checklist verdict, PR-level score), not on each finding; no standard supports per-finding confidence.
4. For PR code review, make export adapters (to rdjson for reviewdog reporters, to the GitHub review `comments[]` array, optionally to SARIF) the extension point, and add a "postable" check (line is inside the diff, commit SHA present) at posting time rather than widening the core record.
5. Treat the severity router as configuration over the internal ordinal (threshold such as "Medium or higher"), mirroring code scanning's configurable gate, with a mapping table from each third-party vocabulary (Codex P0-P3, CodeRabbit critical-trivial, SARIF error/warning/note) to the internal scale.
6. Do not adopt full SARIF as the internal format: its value is as an export target; the internal record can stay smaller. This is a judgement from the sources (SARIF has many properties a review panel does not need), not a finding stated by any of them.
7. Open gap for the builder: look up Augment's comment format directly (or read `pr_submit` code) before fixing the severity mapping table.

## Summary
Research complete for W4. Sources: official OASIS SARIF 2.1.0, GitHub Docs (code scanning, REST pulls and reviews), reviewdog repository docs, CodeRabbit and Greptile and OpenAI Codex vendor docs, plus forum reports flagged as lower reliability. web-provenance: provider=tavily for all findings (no fallback used).
