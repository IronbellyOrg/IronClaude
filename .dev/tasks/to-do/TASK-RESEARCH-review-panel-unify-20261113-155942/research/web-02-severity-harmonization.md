# Web Research W2: Severity Taxonomies and Harmonization

Topic: severity taxonomies (SARIF level/rank, security-severity, CodeQL, Semgrep, review-comment conventions) and their harmonization into one core scale
Date: 2026-11-13
Status: Complete

Provider note: all findings were gathered with mcp__litellm__Tavily-tavily_search and mcp__litellm__Tavily-tavily_extract (provider=Tavily). No WebSearch/WebFetch fallback was used. Where a finding comes only from a search snippet (not a full-page extract) it says "snippet".

Codebase context read first (source of truth; external findings never override it): `research/01-finding-contract.md` (lines 1-376 of 475 read; sections 1-14) and `research/10-future-consumers.md` (full). Codebase facts used here, all marked CODE-VERIFIED in those files:
- findings-v1/v2 `SEVERITIES = ("CRITICAL","MAJOR","MINOR")`; MINOR can never be blocking (findings.py:14, :100-101; findings_v2.py:107-108). `blocking` is a reviewer-written bool.
- reflect legacy cards use HIGH/MEDIUM/LOW; card_convert maps `high`->MAJOR+blocking, `medium`/`low`->MINOR non-blocking, `important`->MINOR non-blocking (card_convert.py:71-83).
- rf-qa uses CRITICAL/IMPORTANT/MINOR; CRITICAL and IMPORTANT block "by definition, not by the label" (rf-qa.md:106-111); synthetic DNSP findings use HIGH.
- Auggie / PR review use Critical/High/Medium/Low/Nit; blocking is derived from the remapped level; route Critical/High -> deep fix, Medium -> fix, Low/Nit -> report-only (severity_router.py:203-223).
- The review-loop prose has a fourth grade "Medium" meaning "any label with blocking:false" (document_review_loop_prompts.md:31).

---

## 1. SARIF `level` and `rank` (the interchange baseline)

### 1.1 `level`: four values, three of them severities
- Source: OASIS SARIF 2.1.0 Plus Errata 01, sections 3.27.9 (`kind`) and 3.27.10 (`level`), https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html (tavily_extract). Reliability: official standard. Relevance: HIGH.
- Key information (spec text):
  - `warning`: "The rule ... was evaluated and a problem was found."
  - `error`: "... a serious problem was found."
  - `note`: "... a minor problem or an opportunity to improve the code was found."
  - `none`: "The concept of severity does not apply to this result because the kind property ... has a value other than 'fail'."
  - `kind` values: `fail` (default), `pass`, `open`, `informational`, `notApplicable`. "If level has any value other than 'none' and kind is present, then kind SHALL have the value 'fail'."
- Relation to codebase: SARIF `level` is a 3-bucket ordinal of problem seriousness, not a merge-gating flag. `none` plus `kind` is the standard's way to carry "not a defect" results, which fits our findings-v2 `channel` split (defect / grounding-gap / advisory) better than a fourth severity word. SUPPORTS keeping severity and result-kind as two orthogonal fields.
- SARIF `note` ("a minor problem or an opportunity to improve") covers our MINOR and the PR `Low` and `Nit` together; `level` cannot tell Low from Nit.

### 1.2 `rank`: continuous priority 0.0-100.0
- Source: same spec, sections 3.27.25 and 3.50.4. Reliability: official standard. Relevance: HIGH.
- Key information: `rank` is "a number between 0.0 and 100.0 inclusive, representing the priority or importance of the result. 0.0 is the lowest priority and 100.0 is the highest." It is "only meaningful if kind ... has the value 'fail'". When absent it is derived from `level` by the `level` procedure (with `warning` replaced by -1.0); -1.0 means "unknown (not set)". The spec gives no bucket boundaries for `rank` (snippet and extract show none).
- Relation to codebase: `rank` is the standard lossless slot for finer ordering inside a 3-bucket `level`, which is what PR `Critical`/`High`/`Medium` need when they collapse to `error`/`warning`. Our findings have no numeric priority field (CODE-VERIFIED absent in v1/v2). EXTENDS. Caveat: no standard cut points, so our core would own the table (see 3.1 for GitLab's).

---

## 2. `security-severity`, `precision`, `problem.severity` (GitHub code scanning)

- Source: GitHub Docs, "SARIF support for code scanning", https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support (tavily_extract and snippet). Reliability: official vendor docs. Relevance: HIGH.
- Key information:
  - `defaultConfiguration.level` defaults to `warning`; a `result.level` overrides it; valid values `note`, `warning`, `error`.
  - `properties.security-severity`: "a string representing a score ... greater than 0.0 up to 10.0"; its presence makes results "treated as security results". Translation: over 9.0 critical, 7.0-8.9 high, 4.0-6.9 medium, 0.1-3.9 low; 0.0 or out-of-range "is regarded as having no security severity".
  - `properties.precision` is one of `very-high`, `high`, `medium`, `low`: how often the rule's results are true. GitHub orders results by severity, then precision.
  - `properties.problem.severity` (non-security rules): `error` / `warning` / `recommendation`.
- Source: GitHub Changelog 2021-07-19, https://github.blog/changelog/2021-07-19-codeql-code-scanning-new-severity-levels-for-security-alerts (snippet). Reliability: official vendor changelog. Relevance: HIGH.
  - Security alerts get critical/high/medium/low from `security-severity`; non-security alerts "remain as error, warning, or note".
  - Gating is a separate threshold: "any code scanning alerts with a security-severity of critical or high will cause pull request check failure" by default; for non-security alerts "any code scanning results with the severity of error will cause check failure"; both are repository settings.
  - The number is derived: group the CVEs under the query's CWEs, take the 75th percentile CVSS.
- Relation to codebase: strongest external precedent for the core design question. GitHub keeps three independent things: a severity, a confidence-like field (`precision`), and a gate threshold that is policy (a repo setting), not a property of the finding. Our codebase mixes them: `blocking` is reviewer-written in v1/v2 (findings.py:98-99) but derived in pr_submit (`route`) and rf-qa (by definition). SUPPORTS `blocking = policy(severity, category, consumer)` computed by the consumer module. It CONTRADICTS (as a design choice, not as code behaviour) the v1/v2 reviewer-written `blocking`, which the codebase research ties to D9 (same category, opposite blocking rule in two stacks).
- Auggie remap comparison: the router lowers severity one tier on `confidence == low` (severity_router.py:174-175). GitHub keeps `precision` as a separate sort key and does not demote severity. EXTENDS (alternative): keeping confidence beside severity is lossless; demoting is not.

---

## 3. Other SARIF consumers: how they collapse levels (mapping precedent)

### 3.1 GitLab SARIF ingestion
- Source: GitLab Docs, "SARIF reports", https://docs.gitlab.com/user/application_security/detect/sarif (tavily_extract). Reliability: official vendor docs. Relevance: HIGH.
- Resolution order (first field with a value wins): `result.rank`; `rule.properties.security-severity` (x10); `result.properties.security-severity`; `result.level`; `rule.defaultConfiguration.level`; default `medium`.
- Score buckets (0-100): 0-9.9 Info, 10-39.9 Low, 40-69.9 Medium, 70-89.9 High, 90-100 Critical.
- Level map: error -> High, warning -> Medium, note -> Low, none -> Info. "GitLab assigns level: error to high, not critical. To report a critical finding, set result.rank to 90 or higher, or set security-severity to 9.0 or higher."
- Relation to codebase: a shipped consumer that needs 5 levels reading a 3-level `level` and recovering the top tier only through a finer numeric field. Shows `level` alone silently loses Critical vs High and that a precedence rule is needed. SUPPORTS "coarse ordinal plus finer field".

### 3.2 Aggregators and small-tool mappings
- DefectDojo, https://defectdojo.com/integrations/codeql (snippet; vendor page, medium reliability; relevance MEDIUM): `security-severity` 9.0+ Critical, 7.0-8.9 High, 4.0-6.9 Medium, above 0 Low, 0 Info; without a score `error` -> High, `warning` -> Medium, `note` -> Info. Warning on the page: "a code quality query at error level imports as High", so the security-versus-quality category must travel with severity or quality findings inflate.
- Perforce QAC, https://help.perforce.com/qac/current/validate/en-us/concepts/sarif.htm (snippet; vendor docs; relevance LOW-MEDIUM): native 0-9 severity -> error (8-9), warning (1-7), note (0). Another tool-specific many-to-3 collapse; no standard mapping exists.
- DEV Community AI-auditor SARIF post, https://dev.to/pavelespitia/sarif-the-format-that-connects-your-ai-auditor-to-github-code-scanning-311n (snippet; blog, low-medium; relevance MEDIUM): critical+high -> error, medium -> warning, low+informational -> note, "because they should block PRs in a branch protection rule"; "This mapping is a judgment call." Closest external analogue to our 5-to-3 collapse and it merges the High/Critical boundary that our PR router also treats as one route (`--depth deep --fix`).
- Relation to codebase: all collapse to `error/warning/note` and lose at least one distinction; only GitLab recovers it (through `rank`).

---

## 4. Tool-specific scales

### 4.1 CodeQL
- Sources: https://codeql.github.com/docs/writing-codeql-queries/metadata-for-codeql-queries and https://github.com/github/codeql/blob/main/docs/query-metadata-style-guide.md (snippets from both). Reliability: official docs / maintainer repo. Relevance: HIGH.
- Key information:
  - Two disjoint scales by query kind: `@problem.severity` = `error` / `warning` / `recommendation` for non-security queries; `@security-severity` = 0.0-10.0 for queries tagged `security`. Style guide: "We will use the problem.severity attribute to handle the severity for quality-related queries."
  - `@problem.severity` is defined by consequence: `error` "an issue that is likely to cause incorrect program behavior, for example a crash or vulnerability"; `warning` "a potential problem in the code, or makes the code fragile if another (unrelated) part of code is changed"; `recommendation` "the code behaves correctly, but it could be improved".
  - `@precision` (`low`, `medium`, `high`, `very-high`) "broadly indicates the proportion of query results that are true positives"; separate from severity.
  - Suites filter on `kind`, `precision`, `tags`, `problem.severity` together (Tweag https://tweag.io/blog/2025-08-28-codeql-part-two and colinsalmcorner https://colinsalmcorner.com/fine-tuning-codeql-scans ; blog tier, medium).
- Relation to codebase: CodeQL's definitions are consequence-based, the same style as our review-loop rule ("a stated text causes data loss ...", document_review_loop_prompts.md:31) and rf-qa ("wrong behaviour, false claim, missing deliverable", rf-qa.md:106-111). SUPPORTS defining each core severity by consequence. `recommendation` is the external name for our MINOR/Low/Nit region. Per-category-kind scales (CodeQL runs two) are the same shape as "per-lens severity namespace mapped to the core scale" (10-future-consumers.md X3).

### 4.2 Semgrep
- Sources: https://docs.semgrep.dev/writing-rules/rule-syntax ; https://docs.semgrep.dev/kb/rules/understand-severities ; https://docs.semgrep.dev/contributing/contributing-to-semgrep-rules-repository ; https://docs.semgrep.dev/semgrep-code/findings (all snippets). Reliability: official vendor docs. Relevance: HIGH.
- Key information:
  - Rule `severity` can be `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. "The older levels ERROR, WARNING, and INFO match HIGH, MEDIUM, and LOW. Severity values remain backwards compatible." Semgrep itself migrated 3 levels to 4 and kept the old names as aliases of HIGH/MEDIUM/LOW, never CRITICAL.
  - Registry rules carry `confidence`, `likelihood`, `impact` (each LOW/MEDIUM/HIGH); platform severity "is computed based on the values assigned for Likelihood and Impact by the rule's author". (Draugr, https://draugr.dev/docs/latest/scanners/semgrep, snippet, blog tier, relevance LOW, says the same.)
  - Confidence "describes the rule, not the vulnerability" and is how sure the author is that the patterns do not produce many false positives.
  - Supply Chain severity comes from CVSS (9.0+ Critical); an EPSS exploit probability is shown separately.
- Relation to codebase: clearest example of (a) a 3-level to 4-level extension with alias mapping, the migration shape we face (v1 CRITICAL/MAJOR/MINOR vs reflect HIGH/MEDIUM/LOW), (b) severity as a function of two axes (impact x likelihood) with confidence kept apart, which parallels our consequence sentence (`wrong_outcome`, review_ledger.py:270) plus `self_confidence`, and (c) the card_convert trap: legacy names land in the middle of the new scale (ERROR=HIGH), so Critical must be an explicit new value. SUPPORTS; no contradiction.

---

## 5. Review-comment conventions (blocking versus non-blocking, nit)

### 5.1 Google engineering practices
- Sources: https://github.com/google/eng-practices/blob/master/review/reviewer/standard.md (snippet, official repo); https://solmaz.io/google-eng-practices-github (snippet, blog adaptation quoting the severity-label section; relevance MEDIUM). Reliability: official repo. Relevance: HIGH. A secondary blog (https://pasqualepillitteri.it/en/news/3317/google-code-review-guidelines-internal-principles-industry-standard) claims the repo was archived in November 2025; not verified from the repo, so treat as UNVERIFIED.
- Key information: "if it's not very important, prefix it with something like 'Nit: ' to let the author know that it's just a point of polish that they could choose to ignore." Weight labels (via the adaptation): `Nit:` "Technically you should do it, but it won't hugely impact things"; `Optional:` / `Consider:` "a good idea, but not strictly required"; `FYI:` "I don't expect you to do this in this PR". "Don't block PRs from being merged based only on personal style preferences." The governing standard is a threshold (approve when overall code health improves) rather than a scale; only changes that definitely worsen code health block, except in emergencies.
- Relation to codebase: weight prefixes are orthogonal to category, and an unlabelled comment is read as mandatory. Our PR `Nit` tier equals Google's `Nit:`. Non-blocking itself has three obligation levels (Nit, Optional, FYI) that a 3-level scale with `blocking:false` cannot express. EXTENDS: findings-v2's `advisory` channel is the natural home of FYI.

### 5.2 Conventional Comments
- Source: https://conventionalcomments.org (snippet; community spec). Reliability: community spec, widely adopted (medium-high). Relevance: HIGH.
- Key information: format `<label> [decorations]: <subject>`. Labels: praise, nitpick, suggestion, issue, todo, question, thought, chore, note. Decorations: `(non-blocking)`, `(blocking)`, `(if-minor)`. Definitions: nitpick = "trivial preference-based requests. These should be non-blocking by nature."; `(blocking)` "should prevent the subject under review from being accepted, until it is resolved ... helpful for organizations that consider comments non-blocking by default"; `(non-blocking)` is the mirror; `(if-minor)` "resolve the comment only if the changes end up being minor or trivial". Comments are "parseable by machines".
- Relation to codebase: closest external convention to our `blocking` + `category` + severity split: kind (label) and obligation (decoration) are separate axes, and `(if-minor)` is a third obligation state that matches the review-loop prose "Medium" (not blocking, but a follow-up candidate, document_review_loop_prompts.md:31). SUPPORTS modelling obligation as its own field with three values (blocking, non-blocking, conditional). It also names the default-policy problem: the core must state whether an unlabelled finding blocks. Our v1/v2 rule (reviewer must write `blocking`; MINOR never true) is the opposite of Google's default.
- Secondary: Augment Code guide, https://www.augmentcode.com/guides/what-does-nit-mean-in-code-review (snippet; blog tier; relevance MEDIUM) lists blocking categories (logic errors, security vulnerabilities, race conditions, memory leaks, missing error handling, test coverage shortfalls): a category-driven blocking floor, the same idea as the Auggie per-category floors (severity_router.py:34-52). `missing error handling` there is the category the codebase notes is absent from both `_CATEGORY_TABLE` and the rubric (10-future-consumers.md section 2, D-b).

---

## 6. Other 5-level and 3-to-5-level scales in use (cross-tool equivalence)

### 6.1 SonarQube: legacy 5-level to new impact scale, and a documented regret
- Sources: SonarQube Server 10.4 "Issues", https://docs.sonarsource.com/sonarqube-server/10.4/user-guide/issues ; "Changing instance modes", https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/changing-modes ; glossary https://docs.sonarsource.com/sonarqube-server/10.8/glossary (all snippets; official vendor docs); Sonar Community thread, https://community.sonarsource.com/t/mapping-of-standard-experience-mode-old-to-multi-quality-rule-mqr-mode/133704 (snippet; reply by Sonar staff, medium-high reliability). Relevance: HIGH.
- Key information:
  - Standard mode severities: Blocker, Critical, Major, Minor, Info (one severity per rule). MQR mode severities: Blocker, High, Medium, Low, Info, applied per software quality (an issue "can have multiple severities if it impacts more than one software quality").
  - Old-to-new mapping applied in 10.2: Blocker and Critical -> High; Major -> Medium; Minor and Info -> Low.
  - Staff statement: "We initially mapped Blocker in standard to High and Info -> Low in the new severity system because we wanted to avoid a load of rules suddenly appear as Blocker/Info before users used to Low/Medium/High were ready to handle them. This isn't ideal because you don't get a rule being treated in the same way in both modes. We are looking to go to the more obvious Blocker/Info (standard) -> Blocker/Info (MQR) mapping".
  - Generic issue import: when `impacts` is not defined, the old format defaults to Maintainability + Medium (community thread, snippet).
- Relation to codebase: this is a production example of exactly our situation (legacy 5-level and a new 3-level or 5-level scale must coexist). Lessons: (1) a many-to-one collapse at the extremes (Blocker->High, Info->Low) was chosen for rollout comfort and later called "not ideal", so a core scale should keep both extremes; (2) Sonar maps its MAJOR to MEDIUM and MINOR to LOW, which contradicts card_convert's choice of `medium` -> MINOR non-blocking (card_convert.py:71-83, CODE-VERIFIED in 01-finding-contract.md section 3.2); (3) a per-quality severity (security vs maintainability) is the same idea as a per-lens/category severity namespace. SUPPORTS keeping `medium` as its own level and EXTENDS the finding that card_convert collapses it.

### 6.2 CodeRabbit (AI review bot) severity
- Source: CodeRabbit docs, https://docs.coderabbit.ai/guides/code-review-overview (snippet). Reliability: official vendor docs. Relevance: HIGH (same domain: AI reviewer comments).
- Key information: five severities with consequence definitions: Critical "could cause system failures, security breaches, or data loss"; Major "significant problems that impact functionality or performance"; Minor "should be addressed but don't critically impact the system"; Trivial "low-impact suggestions for code quality improvements"; Info "informational comments or context without requiring action". Category is a separate badge (Security & Privacy, Stability & Availability, Data Integrity & Integration, Functional Correctness, Performance & Scalability, Maintainability & Code Quality). Changelog (https://docs.coderabbit.ai/changelog, snippet): the Quiet profile posts inline only "critical and major issues that are also high-impact" and groups the rest into collapsed summary sections ("nothing is lost while the inline noise stays low"); a CLI skill (https://mcpservers.org/agent-skills/coderabbitai/skills/code-review, snippet, low-tier aggregator) says it "preserves finding severities: critical, major, minor, trivial, info, and none".
- Relation to codebase: independent 5-level scale with a bottom `info` that is explicitly non-actionable, the same role as our PR `Nit` plus the `advisory` channel. Severity and category are separate fields. Visibility (inline versus collapsed) is a policy on top of severity, not part of the finding. SUPPORTS.

### 6.3 Priority vocabularies (P0-P3) are priority, not severity
- Sources: CodeRabbit Triage, https://docs.coderabbit.ai/triage/prioritization (snippet; vendor docs; relevance MEDIUM): P0 "Urgent" ... P3 "Low priority. Can wait behind more actionable or more consequential work"; "Blockers do not raise priority". Codex reviewer: cubic.dev review https://www.cubic.dev/blog/codex-code-review (snippet; third-party blog, low-medium reliability; relevance MEDIUM) says the local Codex review prompt "tags each finding P0 to P3 ... and ends with a verdict that the patch is correct or incorrect, with a confidence score", and that on GitHub it reports only P0 and P1 findings; samwize.com (https://samwize.com/2026/03/25/what-your-ai-code-reviewer-actually-prompts-behind-your-back, snippet, blog, low-medium) reads P0 and P1 as the ones that "genuinely need fixing". I did not find the Codex prompt text itself, so the exact P-level definitions are UNVERIFIED.
- Relation to codebase: our Codex adapter takes a `severity_hint` from a P0-P3 badge (`reviewers.py:234-243`, `_CODEX_HINTS` at `:43`, per 10-future-consumers.md section 1.1). External usage treats P-levels as priority/urgency; mapping them onto a severity scale is a priority-to-severity conversion that needs its own table (and is a third scale in the "five vocabularies" count). EXTENDS.

### 6.4 OWASP risk rating: severity as likelihood x impact, with a `Note` floor
- Source: OWASP Risk Rating Methodology, https://community.owasp.org/OWASP_Risk_Rating_Methodology (snippet; official OWASP). Reliability: official foundation docs. Relevance: MEDIUM.
- Key information: likelihood and impact are each scored 0-9 and bucketed LOW (0 to <3), MEDIUM (3 to <6), HIGH (6-9); overall severity from a 3x3 matrix: HIGH impact gives Medium/High/Critical across LOW/MEDIUM/HIGH likelihood; MEDIUM impact gives Low/Medium/High; LOW impact gives Note/Low/Medium. The page stresses business context: a technically high finding with low business impact is "best described as low".
- Relation to codebase: the matrix form shows a lossless way to get a 5-level severity (Note, Low, Medium, High, Critical) from two 3-level inputs, and the bottom value is called `Note`, the same word as SARIF's lowest level and close to our Nit. Matches the Semgrep impact x likelihood derivation (section 4.2). Also supports having the consumer module supply context (business/consumer policy) rather than the reviewer. Applicable if the core derives severity from a consequence axis (what breaks) and a likelihood axis (how sure); our review-loop "consequence sentence" supplies only the impact axis today.

### 6.5 Cross-tool equivalence table (what each tool calls the same rank)
Order is by seriousness; blank = the tool has no such tier. Sources are those cited in sections 1 to 6; the cells are the documented values, the row grouping is my alignment by the vendors' own mappings (GitLab level map, Sonar mapping, Semgrep alias rule) and is a judgment where no vendor mapping exists.

| Rank | SARIF level (+rank) | GitHub code scanning | CodeQL | Semgrep | SonarQube (legacy / MQR) | CodeRabbit | OWASP | GitLab (from SARIF) |
|---|---|---|---|---|---|---|---|---|
| 1 | error (rank high) | critical (security-severity over 9.0) | security-severity 9.0-10.0 | CRITICAL | Blocker | Critical | Critical | Critical (rank 90-100) |
| 2 | error | high (7.0-8.9) | 7.0-8.9; problem.severity error | HIGH (= legacy ERROR) | Critical (legacy), High (MQR) | Major | High | High (error) |
| 3 | warning | medium (4.0-6.9) | 4.0-6.9; warning | MEDIUM (= WARNING) | Major / Medium | Minor | Medium | Medium (warning) |
| 4 | note | low (0.1-3.9) | 0.1-3.9; recommendation | LOW (= INFO) | Minor / Low | Trivial | Low | Low (note) |
| 5 | note (rank low) / none (kind not fail) | none (0.0) | none | (none) | Info | Info | Note | Info (none) |

Reading the table: (a) every 3-level scale (SARIF level, CodeQL problem.severity, legacy Semgrep) is a coarsening of the 5-level ones; (b) the 5-level scales line up tier by tier, so the top tier is always an explicit extra value above the legacy "error/high"; (c) no vendor equates the middle tier (Medium/warning/Major) with the bottom tier, except where a tool does so on purpose (Sonar's early Info->Low; card_convert's `medium` -> MINOR).

---

## 7. Lossless mapping strategies (3-level and 5-level without losing information)

### 7.1 What SARIF itself says about unmappable data
- Source: OASIS SARIF 2.1.0 converter guidance, https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html (snippet): "If the input data includes information for which there is no SARIF equivalent, a converter MAY use it to populate the various property bags ... When populating a property bag with such information, a converter SHOULD use a property name that matches the name of that piece of information in the native tool format." Every SARIF object defines a `properties` bag (Microsoft SARIF tutorial, https://github.com/microsoft/sarif-tutorials/blob/main/docs/2-Basics.md, snippet; official Microsoft tutorial repo, relevance MEDIUM), with the same tutorial advising to prefer first-class properties ("Generic SARIF tooling ... will at best be able to display property bag properties. It won't be able to extract any meaning from them."). Reliability: official. Relevance: HIGH.
- Source: microsoft/sarif-tools issue 43, https://github.com/microsoft/sarif-tools/issues/43 (tavily_extract; maintainer comment, medium reliability). "The SARIF standard defines three levels of severity, error, warning and note. ... Some tools use custom properties to store their own severity scale, e.g. DevSkimSeverity 4. But these are not comparable across tools." The same page quotes the spec default: "If level is absent, it SHALL default to 'warning'." Relevance: HIGH.
- Relation to codebase: the standard's own answer to losslessness is "first-class core value plus the native value preserved under its native name". A core finding should therefore carry both a comparable core severity and `native_severity` (and the native scale name), so a round trip back to rf-qa IMPORTANT or reflect MEDIUM is possible. The sarif-tools remark shows the price of skipping the core value: preserved native scales cannot be compared. SUPPORTS.

### 7.2 Strategies observed (each with the information it keeps or loses)

| # | Strategy | Used by (source) | Keeps | Loses or risks |
|---|---|---|---|---|
| S1 | Coarse ordinal plus a finer numeric field (`level` + `rank`) | SARIF 3.27.25; GitLab resolution order (rank first, then security-severity, then level) | Order inside a bucket; a 5th tier above `error` | `rank` has no standard cut points, so each consumer re-buckets; `rank` is meaningful only when kind is fail |
| S2 | Severity derived from impact and likelihood, confidence kept separate | Semgrep (impact x likelihood; confidence separate), OWASP matrix, GitHub (`precision` beside severity) | Why the severity is what it is; reviewer certainty not folded into severity | Needs two reviewer inputs, which today's findings do not carry (no likelihood field in v1/v2) |
| S3 | Obligation separate from severity | Conventional Comments `(blocking)/(non-blocking)/(if-minor)`; GitHub gate threshold; Google "Nit:" | Policy can change without re-grading findings; three obligation states | A free-form obligation can contradict severity (needs a validation rule such as v1's "MINOR cannot block") |
| S4 | Legacy alias table with versioning | Semgrep (ERROR=HIGH ...), SonarQube 10.2 mapping | Old rules and old reports keep working | Aliases land mid-scale (Semgrep ERROR=HIGH, never CRITICAL); Sonar's collapse of extremes was later called "not ideal" |
| S5 | Native value preserved in a named property | SARIF converter guidance; DevSkim example in sarif-tools issue 43 | Exact round trip | Not comparable across tools without a core value (S1/S4) |
| S6 | Category-kind-specific scale with a documented bridge | CodeQL (`problem.severity` for quality, `security-severity` for security); SonarQube MQR per-quality severity | Each family keeps its natural scale | Two scales to explain; DefectDojo warning that a quality `error` imports as High shows the bridge must carry the category |
| S7 | Visibility policy on top of severity | CodeRabbit profiles (Quiet/Chill/Assertive); GitHub repo gate setting | Nothing dropped from storage; display and gating tunable | Policy lives outside the finding, so exports lose it unless recorded |

### 7.3 Collapse analysis: 5-level to 3-level (SARIF `level`)
- Using the vendors' own mappings (GitLab level map; DEV post mapping; DefectDojo): Critical and High -> `error`; Medium -> `warning`; Low and Nit/Info -> `note`. The inverse is not a function: `error` could be Critical or High, `note` could be Low or Nit. GitLab states the consequence in its docs: `error` is read as High, "not critical".
- A 3 -> 5 -> 3 round trip is lossless only if the 5-level value (or `rank`) is kept; a 5 -> 3 -> 5 round trip is never lossless. Our PR router already has exactly three routes (Critical/High -> deep fix, Medium -> fix, Low/Nit -> report-only; severity_router.py:203-223, CODE-VERIFIED in 10-future-consumers.md), which line up with `error` / `warning` / `note`. So `level` is enough for routing, and not enough for the rubric's own Critical-versus-High distinction (Critical blocks merge, High should be fixed before merge, severity-rubric.md:11-61).

---

## 8. Mapping table: our five vocabularies onto a candidate external scale

Candidate external scale used below (derived from sections 1 to 7; not an existing standard): SARIF `level` (error / warning / note, plus `none` for non-defect kinds) as the interchange layer, with a five-tier core ordinal (critical / high / medium / low / info) and SARIF `rank` buckets as the lossless layer. Rank bucket boundaries here borrow GitLab's published table (critical 90-100, high 70-89.9, medium 40-69.9, low 10-39.9, info 0-9.9) because it is the only published bucket table for `rank`; it is an option, not a requirement of the SARIF spec.

Codebase inputs are the CODE-VERIFIED facts listed at the top of this file. Rows marked "(proposed)" are my mapping proposals; they are not stated by any source.

| # | Our vocabulary and value | Core ordinal (proposed) | SARIF `level` | Obligation (blocking) | Information lost by this mapping (and how to keep it) |
|---|---|---|---|---|---|
| 1 | findings-v1/v2 `CRITICAL` | critical | error | as written by reviewer (v1 allows CRITICAL with blocking:false, only MINOR is barred, findings.py:100-101) | A CRITICAL that the reviewer marked non-blocking is a contradiction in the data; keep both fields and flag the pair instead of collapsing |
| 2 | findings-v1/v2 `MAJOR`, blocking:true | high | error | blocking | Cannot tell High from Critical at the SARIF `level` layer; keep core ordinal or `rank` |
| 3 | findings-v1/v2 `MAJOR`, blocking:false (the review-loop prose "Medium", document_review_loop_prompts.md:31) | medium | warning | non-blocking, follow-up candidate | The label MAJOR is lost (the prose says "even when its label is MAJOR"); store `native_severity: MAJOR` |
| 4 | findings-v1/v2 `MINOR` | low | note | non-blocking (always) | Low vs Nit not distinguishable; MINOR is the only v1/v2 value that spans both |
| 5 | reflect `HIGH` (regression or load-bearing invariant break, reflect-reviewer.md:71) | high | error | blocking (card_convert: MAJOR+blocking) | Whether it deserves critical is not recorded by the legacy card; leave at high, do not guess |
| 6 | reflect `MEDIUM` (unjustified drift with real impact, reflect-reviewer.md:71) | medium | warning | UNDECIDED: card_convert makes it non-blocking (MINOR), reflect treats it as drift with real impact; the external scales (Sonar Major=Medium, CodeRabbit Minor, GitLab warning=Medium) keep it a distinct middle tier | Today's card_convert loses the medium tier entirely (maps to MINOR); keeping it at `medium` removes that loss. Whether medium drift blocks is an owner decision |
| 7 | reflect `LOW` (cosmetic / minor drift) | low | note | non-blocking | none beyond Low vs Nit |
| 8 | reflect deviation class `Authorized expansion`, `Necessary deviation` | not a severity: class field; (proposed) kind = informational | none (SARIF `kind` other than fail, spec 3.27.9-3.27.10) | non-blocking | These are non-defects; forcing them into a severity inflates counts. Keep `deviation_class` as its own field (already in findings-v2); the card_convert two-word-label mismatch loses them today (01-finding-contract.md section 3.4) |
| 9 | reflect deviation class `Drift`, `Regression` | class field; severity from the row's own HIGH/MEDIUM/LOW | per the row | per the row | Class and severity are independent; v2-19 already couples reflect_category to blocking only |
| 10 | rf-qa `CRITICAL` | critical | error | blocking (rf-qa.md:111) | none material |
| 11 | rf-qa `IMPORTANT` | high | error | blocking (rf-qa.md:111) | rf-qa defines blocking "by the definition above, not by the label"; carry `blocking` separately so a mislabelled IMPORTANT is still decidable. Collides with card_convert word `important` -> MINOR non-blocking (card_convert.py:82) |
| 12 | rf-qa `MINOR` | low | note | non-blocking | cosmetic, wording, citation format and nit all share one value (rf-qa.md:108), so Low vs Nit lost |
| 13 | rf-qa DNSP synthetic `HIGH` (rf-qa.md:84) | high | error | blocking (inherited FAIL uses HIGH, per 10-future-consumers.md X3) | A fourth word on a three-word scale; accept it as an alias of high |
| 14 | Auggie / PR `Critical` | critical | error | blocking (rubric: blocks merge) | none |
| 15 | Auggie / PR `High` | high | error | should fix before merge (rubric) | High vs Critical at the `level` layer; keep ordinal |
| 16 | Auggie / PR `Medium` | medium | warning | fix if cheap, else follow-up (rubric); route `--fix` | Today's v1/v2 has no Medium value (three values, MINOR barred from blocking); the nearest fit is MAJOR with blocking:false (row 3), but a mapper could equally send it to MINOR (row 4, as card_convert does for `medium`) |
| 17 | Auggie / PR `Low` | low | note | non-blocking, report-only | Low vs Nit |
| 18 | Auggie / PR `Nit` | info | note (rank low) | never blocks (rubric) | At `level` Nit equals Low; keep `rank` or the ordinal. The info tier has precedents (SonarQube Info, CodeRabbit Info/Trivial, OWASP Note, GitLab Info) |
| 19 | Codex badge `P0`-`P3` (priority, snippet-level sources only, section 6.3) | (proposed) P0->critical, P1->high, P2->medium, P3->low; UNVERIFIED against the Codex prompt | error / error / warning / note | via the PR router, not the badge | Priority is not severity; keep the badge as `native_severity` |

What a reader should take from the table: rows 1-4 and 10-18 are straightforward. The cases with real information loss are rows 3 and 6 (the "medium" tier, which exists today only as prose in the loop brief, as a card_convert collapse, and as a PR tier), row 8 (non-defect classes), and row 11 (label versus definition). All other loss is Low versus Nit and Critical versus High at the SARIF `level` layer, both recoverable with a core ordinal or `rank`.

---

## Key External Findings

1. SARIF `level` is a 3-bucket seriousness ordinal (error, warning, note) and `none` is reserved for results whose `kind` is not `fail`; `rank` (0.0-100.0) is the standard's lossless finer ordering and is meaningful only for `kind: fail`. The spec gives no bucket cut points for `rank`. (SARIF 2.1.0 3.27.10, 3.27.25; relevance HIGH; official.)
2. GitHub, CodeQL and GitLab all separate three things we mix: a severity, a confidence-like field (`precision`), and a gating threshold that is policy (a repository setting). Security alerts use `security-severity` (0.0-10.0; over 9.0 critical, 7.0-8.9 high, 4.0-6.9 medium, 0.1-3.9 low) and non-security alerts keep `error/warning/note`. By default only critical/high security alerts or `error` non-security alerts fail a PR check. (GitHub docs and changelog; HIGH; official.)
3. GitLab shows the standard pattern for a 5-level consumer reading SARIF: precedence `rank` > `security-severity` > `level` > default level > `medium`, with `error` read as High "not critical". Without `rank`/`security-severity` the Critical tier is unreachable. (GitLab docs; HIGH; official.)
4. Every shipped 3-level to 5-level or 5-level to 3-level mapping examined is a judgment call and loses a tier at the extremes; SonarQube staff called its own Blocker->High / Info->Low collapse "not ideal" and said they plan to map Blocker->Blocker and Info->Info. Semgrep moved from ERROR/WARNING/INFO to LOW/MEDIUM/HIGH/CRITICAL by aliasing ERROR=HIGH (never CRITICAL). (Sonar docs and community; Semgrep docs; HIGH.)
5. The middle tier is consistently kept distinct: Sonar Major=Medium (not Low), CodeRabbit Minor, Semgrep WARNING=MEDIUM, GitLab warning=Medium, SARIF `warning`. The only external-looking collapse of Medium into the bottom is our own card_convert (`medium` -> MINOR non-blocking), which departs from every vendor mapping reviewed. (Sections 4-6; HIGH.)
6. Review-comment conventions model obligation as its own axis, not as a function of severity: Conventional Comments `(blocking)` / `(non-blocking)` / `(if-minor)`; Google `Nit:` / `Optional:` / `Consider:` / `FYI:`, where an unlabelled comment is read as mandatory. `(if-minor)` and `Optional` give a third obligation state that matches the review-loop prose "Medium". (conventionalcomments.org; google/eng-practices; HIGH.)
7. Severity definitions in CodeQL, Semgrep, CodeRabbit and OWASP are consequence-based, and Semgrep/OWASP derive severity from impact x likelihood with confidence kept apart; this matches the consequence-sentence style already in the review-loop brief and rf-qa's definition-over-label rule. (Sections 4, 6; HIGH.)
8. SARIF converter guidance says to keep unmappable native data in a property bag under the native name; the sarif-tools maintainers note such custom scales "are not comparable across tools". So a lossless design needs both a comparable core value and the preserved native value. (SARIF 2.1.0; microsoft/sarif-tools#43; HIGH.)
9. P0-P3 vocabularies (Codex badges, CodeRabbit Triage) are priority/urgency vocabularies, not severity; the Codex prompt text itself was not found, so its definitions are UNVERIFIED. (Section 6.3; MEDIUM; blog-tier for Codex.)

## Recommendations from External Research

These are options supported by the sources above. They do not override the CODE-VERIFIED behaviour described at the top of this file; where they differ from current code the difference is named.

1. **Core scale: five ordinal tiers (critical, high, medium, low, info), with SARIF `level` (error/warning/note, `none` for non-defect kinds) as the export layer and `rank` buckets for the finer order.** Reason: the PR rubric already distinguishes five tiers and rf-qa/reflect/v1 map onto them without merging the middle (sections 6.5, 8); a 3-tier core would lose Critical vs High and Low vs Nit (section 7.3). Precedents: SonarQube MQR, CodeRabbit, GitLab buckets. Differs from code: findings-v1/v2 `SEVERITIES` has three values and bars MINOR from blocking (findings.py:14, :100-101).
2. **Keep `blocking` separate from severity and compute it per consumer from a policy**, as GitHub does with a repository threshold and Conventional Comments does with decorations. The reviewer may propose obligation, but the consumer module owns the predicate (rf-qa: "by definition, not by label"; PR router: derived from the remapped level; experiment ledger `PROFILES`, review_ledger.py:53-59, already has per-profile predicates). Differs from code: v1/v2 require a reviewer-written bool (findings.py:98-99), which the codebase research links to D9.
3. **Make `medium` a first-class tier, not prose.** The review-loop "Medium" (a MAJOR-labelled finding with blocking:false) is today a prose-only fourth grade (document_review_loop_prompts.md:31); every external scale keeps the middle tier. Fix the card_convert collapse (`medium` -> MINOR non-blocking; and `important` -> MINOR) in the legacy alias table instead of the core scale. Whether a medium reflect drift blocks stays an owner decision (table row 6).
4. **Carry five fields, not one: core severity, obligation, confidence, native severity plus native scale name, and category per lens.** Do not fold confidence into severity (the PR remap's one-tier drop for `confidence == low`, severity_router.py:174-175, discards the original severity; GitHub keeps `precision` as a separate sort key). Preserve the native value under its native name (SARIF converter guidance) so rf-qa IMPORTANT and reflect MEDIUM round-trip.
5. **Define each tier by consequence in one sentence** (CodeQL `error`/`warning`/`recommendation`, CodeRabbit Critical-to-Info), and make the loop brief, the PR rubric and the rf-qa rule share those sentences. This removes the three separate definitions of "blocking" (loop brief consequence sentence, rubric tiers, rf-qa definition).
6. **Treat deviation classes and the advisory channel as non-severity fields.** SARIF's `kind` (`informational`, `notApplicable`) with `level: none` is the standard precedent for non-defect results; this matches findings-v2 `channel` and `deviation_class`. Do not give Authorized expansion / Necessary deviation a severity.
7. **Version the legacy alias table and avoid collapsing the extremes.** Follow Semgrep (explicit alias list, new CRITICAL) and Sonar's stated regret: map legacy `CRITICAL` to critical and `MINOR` to low, route Nit/info to its own tier, and never map the top and bottom of a 5-level scale into the next tier for rollout comfort.
8. **If SARIF export is a goal, own the rank cut points and the category rule.** The spec gives no `rank` buckets (GitLab's table is the only published one) and `security-severity` is meant only for security rules (GitHub docs; safeguard.sh advice, blog-tier); a quality finding exported at `error` is read as High by DefectDojo. Export `level`, `rank`, and (security category only) `security-severity` together.
9. **Keep P0-P3 as a priority hint with its own table** (Codex badge, CodeRabbit Triage), and confirm Codex's P-level definitions from its prompt before relying on the proposed P0->critical mapping (UNVERIFIED here).

## Gaps and Unverified Items

- The `rank` bucket table used in section 8 is GitLab's, not SARIF's; the spec text read gives none.
- Semgrep, CodeQL, Google, Conventional Comments, SonarQube and CodeRabbit facts come from search snippets of the cited pages (the SARIF spec, GitHub SARIF docs and GitLab docs were fully extracted for the quoted parts).
- The claim that google/eng-practices was archived in November 2025 comes from one blog and is not verified.
- The Codex P0-P3 definitions and the GitHub-side "only P0 and P1" behaviour come from third-party blogs; the Codex prompt text was not retrieved.
- No source was found that gives a validated algorithm for 3-to-5 mapping beyond the vendor mappings above; the mapping table in section 8 is a proposal assembled from them.
- Search-query hygiene: no repository names, user names or internal file contents were sent in any query; all queries used generic technical terms.

