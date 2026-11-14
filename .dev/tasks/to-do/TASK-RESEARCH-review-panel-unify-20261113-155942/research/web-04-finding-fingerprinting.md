# Web Research W4: Finding Location and Fingerprinting Across Revisions

Date: 2026-11-13
Status: Complete
Topic: SARIF partialFingerprints/fingerprints, GitHub code scanning alert tracking across commits, line drift, snippet/region hashing, multi-tool deduplication, transitive-chaining safeguards.
Provider: Tavily (mcp__litellm__Tavily-tavily_search / tavily_extract) unless noted.

## Codebase context read first
Read: 03-clustering.md Summary and 10-future-consumers.md Summary (summarised below).

## Codebase context (from 03-clustering.md Summary and 10-future-consumers.md Summary)
- v1 `findings.cluster` and v2 `cluster_v2` both use transitive O(n^2) union-find over a prose-harvested `refs_norm` regex (misses `T01.02`, pulls `P1` from `D-P1`). Replay of v1 found 195 chained rows and 83 mega-rows (up to 19 members over 8 sections). v2 flags chains but does not split them; section is always empty so equal refs on one file merge at any distance. Quality figures (precision 0.84, recall 0.95) are AI-labelled; human labels pending.
- Consumers need a location union: anchor, path+line+in_diff, file:section, multi-file.

## Fingerprint fields (SARIF 2.1.0)

### F1. `fingerprints` vs `partialFingerprints` vs `correlationGuid` / `guid`
- Source: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html (OASIS SARIF 2.1.0 Errata 01, sections 3.27.2-3.27.4, 3.27.16, 3.27.17, Appendix B). Reliability: OFFICIAL SPEC (highest).
- Key information: Two results with the same `fingerprint` are "logically the same". A direct producer SHOULD NOT populate `fingerprints`; a result management system (RMS) that computes fingerprints populates it. An RMS that groups results by an arbitrary unique id populates `correlationGuid` instead (or as well). `guid` is a stable unique id of one result. `partialFingerprints` are producer-supplied strings that "contribute to the stable, unique identity" of the result; each key is a versioned hierarchical string (e.g. `prohibitedWordHash/v3`); the RMS SHOULD fold them into its own fingerprint and, when two results carry different versions, SHOULD compare using the greatest common version.
- Relation to our codebase: our findings today have no stable id other than the anchor quote or cited reference. SARIF's split (producer-side partial identity + consumer-side computed identity + separate grouping id) maps onto our need: each reviewer emits location evidence (partial), the shared core computes the cluster fingerprint, and the cluster id is a separate grouping id. Version-suffixed keys map onto the "version pinning" recommendation in 03-clustering.md.
- Supports / extends: SUPPORTS "citation-based location model with version pinning" (03-clustering Summary). EXTENDS: the fingerprint should be a dictionary of named, versioned components, not one string.
- Relevance: HIGH

### F2. What SARIF says a fingerprint should be built from
- Source: same OASIS spec, section 3.27.2 and Appendix B (extract text: "A result management system SHOULD construct a fingerprint by using information contained in the SARIF file such as the name of the tool that produced the result, the rule id, the file system path to the analysis target ..."; logical location "is typically more resilient to changes in source code than are the line numbers"; `logicalLocation.fullyQualifiedName` "is particularly convenient for fingerprinting"; for XML/JSON targets an internal structural path such as `/orders/customers/lastName` helps). Reliability: OFFICIAL SPEC.
- Corroboration: https://boostsecurity.io/blog/sarif-cant-save-you-now (blog, MEDIUM reliability) summarises the Appendix B properties as deterministic computation, tool name, rule id, physical location of the analysis target.
- Relation to our codebase: our "section or symbol" suggestion in 03-clustering.md (put the section back into the fingerprint) matches SARIF's preference for logical location over line numbers. For markdown specs and tasklists, "logical location" = heading path / task id; for code = symbol. Contradiction check: v2 uses an empty section, which discards exactly the component the spec calls most change-resilient.
- Supports codebase finding D6/over-merge diagnosis: YES (extends it).
- Relevance: HIGH

## Alert matching across commits (GitHub code scanning)

### A1. GitHub matches alerts only through `partialFingerprints.primaryLocationLineHash`, plus ruleId and path
- Source: https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support (official docs, read with extract). Reliability: OFFICIAL.
- Key information: "Code scanning uses fingerprints to match results across various runs so they only appear once in the latest run for the selected branch. This makes it possible to match alerts to the correct line of code when files are edited. The `ruleId` for a result has to be the same across analysis." The filepath "has to be consistent across the runs to enable a computation of a stable fingerprint. If the filepaths differ for the same result, each time there is a new analysis a new alert will be created, and the old one will be closed." "Code scanning only uses the `primaryLocationLineHash`." If the upload action finds no `partialFingerprints`, it computes them (needs the source in the workspace). Results are also scoped by `automationDetails.id` (category) so several tools/configs do not collide.
- Relation to our codebase: the identity tuple GitHub really uses is (category, ruleId, path, primaryLocationLineHash). Our equivalent would be (review run/lens category, finding category/rule, normalised path or document id, location hash). Path normalisation is a hard prerequisite: our `in_diff` PR findings and spec-anchor findings must normalise paths (repo-relative, forward slashes) before hashing, otherwise the same finding splits (GitHub's "closes the old alert and opens a new one" failure mode).
- Supports/extends: EXTENDS. Our v2 path-aware clusterer already keys on path; add ruleId/category as a hard key and a normalised-path rule.
- Relevance: HIGH

### A2. Failure mode when the hash input is empty: matching falls back to order
- Source: https://github.com/SureA11y/core/issues/47 (GitHub issue in a third-party repo, dated Oct 2026; reliability: forum/issue report, LOW-MEDIUM, single case, but the behaviour is consistent with A1).
- Key information: results without a line (DOM finding) got an empty `primaryLocationLineHash`; GitHub then "matched alerts by their order in the file", so fixing one finding closed another. Supplying a per-result hash computed from `ruleId + reasonCode + html` fixed it, and the upload action keeps a hash that is already present. Changing a line at the top of the file had no effect either way.
- Relation to our codebase: direct analogue of v2's empty-section over-merge (D6 family): when the location component is empty, the system degrades to a coarse key and merges or mis-matches distinct findings. Lesson: a finding with no resolvable location must get a content-derived fingerprint component (rule/category + normalised claim text), never an empty one.
- Supports codebase finding: YES. Relevance: HIGH

### A3. Alerts only show on a PR if every line of the alert is inside the diff
- Source: https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts (official). Reliability: OFFICIAL.
- Key information: "You will only see an alert in a pull request if all the lines of code identified by the alert exist in the pull request diff."
- Relation to our codebase: matches our `in_diff` flag semantics for PR review findings; GitHub treats in-diff as a display/placement filter, not as part of identity. Recommends keeping `in_diff` OUT of the cluster key (it is per-revision state, not identity).
- Relevance: MEDIUM

## Line drift and snippet/region hashing

### H1. How the CodeQL `primaryLocationLineHash` is computed (line-drift resistant by construction)
- Source: https://github.com/github/codeql-action/blob/main/src/fingerprints.ts (official source, read with extract) and https://github.com/aquasecurity/trivy/discussions/9070 (community reverse-engineering, MEDIUM; matches the source). Reliability: official source code.
- Key information: a rolling hash is computed for every line of the file over the next `BLOCK_SIZE = 100` non-space, non-tab characters starting at that line (spaces and tabs skipped; CR, LF and CRLF normalised to LF; padding at end of file), so the hash identifies "this line plus the next 100 significant characters" and is independent of the line NUMBER and of indentation/whitespace. Identical hashes in one file get a numeric suffix (`hash:1`, `hash:2`) in order of appearance. The fingerprint of a result is the hash of the line of its first location, so moving a block up or down keeps the fingerprint; editing the line or the 100 characters after it changes it.
- Relation to our codebase: our anchor model (an exact quote of up to 200 chars, rejected above 200 = D1) is the same idea done with the literal text. The CodeQL scheme shows the robust version: hash a whitespace-stripped, line-ending-normalised, fixed-length window, so anchor length limits never reject a finding (truncate-then-hash) and re-flowed text still matches. The `:n` suffix is a documented answer to "same snippet appears twice" (disambiguate by occurrence index instead of merging).
- Contradiction/limit: it is a heuristic over raw text; a one-character edit inside the window breaks identity. CodeQL accepts that and relies on the alert being re-opened as new.
- Relevance: HIGH

### H2. Hash of snippet text alone is not enough: SARIF `region.snippet` and `contextRegion`
- Source: https://github.com/github/awesome-copilot/blob/main/skills/codeql/references/sarif-output.md (maintained repo, MEDIUM; summarising GitHub's SARIF output). Key information: SARIF carries `region` (start/end line and column), optional `snippet`, and `contextRegion` (surrounding lines) next to `artifactLocation`; limits are 1,000 locations per result and 25,000 results per run.
- Relation to our codebase: our location union (anchor, path+line, file:section, multi-file) maps to SARIF `physicalLocation` (artifactLocation + region + contextRegion/snippet) and `logicalLocation` (section/symbol). One internal shape could be `locations[]` of {artifact, region?, snippet_hash?, logical?} with a cap on locations per finding.
- Relevance: MEDIUM

### H3. Other tools' answers to line drift
- Source: https://defectdojo.com/integrations/sarif (vendor docs, MEDIUM). Key information: DefectDojo deduplicates SARIF with "Unique ID From Tool or Hash Code": results with `fingerprints`/`partialFingerprints` match on that id "even when lines shift"; results without fall back to a hash that includes line and description, "so edits can produce new Findings". Also: a single result with five locations becomes five findings (count inflation).
- Relation to our codebase: confirms the two-tier design (stable id when present; else content hash with a known drift weakness). A finding with several locations should stay ONE finding with many locations, not N findings.
- Relevance: MEDIUM

## Line drift: tiered matching in SonarQube (third reference design)

### S1. SonarQube issue tracking: ordered match rules, line hash of the FIRST line only
- Source: https://docs.sonarsource.com/sonarqube-server/discovering/analysis-overview/process-steps (official docs; same text on the 2025.1, 2025.6, 2026.1 and Community Build pages). Reliability: OFFICIAL.
- Key information: for each file, every previous issue is compared with every current issue; no match = Fixed, match on a Fixed issue = reopen, unmatched current issue = new. The algorithm "relies on the issue's line hash", which is "the content of the first line the issue is reported on, excluding the white spaces". Match rules (all require the same rule): (1) same line hash, message may differ: MATCH; (2) same line number and same message, hash may differ: MATCH; (3) the detected block moved within the file, same line within the moved block and same message: MATCH. File renames are checked first, so a renamed file keeps its issues.
- Relation to our codebase: three precise, ordered, independent signals (content hash OR position+message OR moved-block offset+message), each gated on the same rule/category, instead of one union-find over any shared reference. The order gives a deterministic precedence and an explicit "why did these two match" reason that we could log per cluster (telemetry). Rename handling maps onto our "version pinning": findings against revision N must be re-resolved against revision N+1 files before matching.
- Supports/extends: EXTENDS (adds match reasons and a rule-equality gate; v2 has no category gate in the key).
- Relevance: HIGH

## Multi-tool deduplication

### M1. DefectDojo: identity is per-tool; cross-tool dedup is hash-code on a CHOSEN field set
- Sources: https://docs.defectdojo.com/triage_findings/finding_deduplication/deduplication_across_tools and https://docs.defectdojo.com/triage_findings/finding_deduplication/about_deduplication (official product docs), https://docs.defectdojo.com/triage_findings/finding_deduplication/pro__deduplication_tuning (official; mentions "Track Findings as Locations Change", "Content Fingerprint", "Location Drift Matching"). Reliability: OFFICIAL vendor docs (MEDIUM-HIGH).
- Key information: four algorithms per parser: `unique_id_from_tool` (same tool only), `hash_code` (can match across tools), `unique_id_from_tool_or_hash_code`, `legacy` (title or CWE plus endpoints or file path and line). "Matching on the tool's own unique ID only works within a single tool." Cross-tool matching requires configuring both tools "to hash fields that carry the same values across tools, such as vulnerability IDs, CWE, component name and version, or file path and line". The hash fields are configurable per scanner; an editor refuses an algorithm with no fields. Legacy: if both file path and line are empty, dedup "typically does not occur" (it refuses to merge on nothing). Tuning docs say a content fingerprint is useful where tools put paths or line numbers in titles that change when code moves.
- Relation to our codebase: our reviewers are different "tools" (models and lenses). The per-source id (their own `id` or anchor) is only valid within one reviewer; cross-reviewer identity must come from shared normalised fields (path or section, category, cited reference). This matches the plan to put citations, not model-written ids, into the cluster key, and the 03-clustering recommendation to separate same-reviewer pairs from cross-reviewer pairs. The "refuse to merge when location is empty" behaviour is the opposite of v2's empty-section merge (and the right default).
- Supports/extends: SUPPORTS and EXTENDS (explicit "no location, no merge" rule; per-source configurable field set = our per-target id grammar).
- Relevance: HIGH

### M2. Merging several tools' SARIF: dedupe by fingerprint, keep paths consistent, one finding with many locations
- Source: https://www.sonarsource.com/resources/library/sarif (vendor guide, MEDIUM) and https://defectdojo.com/integrations/sarif (vendor, MEDIUM). Key information: merge = concatenate `runs`, keep each tool's metadata with its run; "Fingerprints help remove duplicate results"; make paths repo-relative so one file is not seen under two paths; keep tool names stable because the tool name is part of the identity; multi-location results inflate counts if split.
- Relation to our codebase: keep `(reviewer, model, lens)` as run metadata and never as part of the cluster key; cluster across runs. Stable reviewer names matter for telemetry strata.
- Relevance: MEDIUM

### M3. DefectDojo "track findings as locations change"
- Source: https://docs.defectdojo.com/triage_findings/finding_deduplication/pro__deduplication_tuning (official vendor docs, read with extract; this section is for the Pro edition, MEDIUM-HIGH).
- Key information: with a hash-code reimport algorithm plus location tracking, "a finding whose location moved between reimports (a line shift or file rename ...) is treated as the same finding, even if the tool re-scored its severity. One finding is maintained in place and its location history is preserved, instead of the old finding closing and an identical new one being created." A "Content Fingerprint" field is recommended for tools that embed paths or line numbers in titles.
- Relation to our codebase: location should be a mutable attribute with history on a stable finding identity (the identity excludes the line number and the severity). Severity change must not split a cluster (our merge step compares severity across reviewers; severity belongs to the verdict, not the key).
- Relevance: MEDIUM

## PR review findings across commits (path, line, in_diff)

### P1. GitHub's own review-comment location model
- Sources: https://docs.github.com/rest/pulls/comments and https://docs.github.com/rest/pulls/reviews (official REST docs, read with extract); response-field names `original_line`, `original_commit_id`, `original_position`, `diff_hunk` from a third-party mirror of the schema, https://github.apidog.io/api-3489528 (LOW-MEDIUM; verify against the live API before relying); https://github.com/orgs/community/discussions/23138 (community answer, LOW-MEDIUM) for "Outdated" behaviour.
- Key information: a review comment is addressed by `path` + `line` (+ `start_line` for ranges) + `side` (LEFT/RIGHT of the diff) + `commit_id`, or `subject_type: file` for a whole-file comment; the older diff `position` (lines below the first `@@` hunk header) "is closing down". "Not using the latest commit SHA may render your comment outdated if a subsequent commit modifies the line you specify." When a later commit changes the commented line, GitHub marks the comment Outdated instead of re-anchoring it, because "the automatic tools have no way of knowing if the comment targeted at the old line still makes sense on the new line". The response schema keeps both the current `line`/`commit_id` and the `original_line`/`original_commit_id`, i.e. GitHub stores the location at the commit where it was made and a best-effort current location separately.
- Relation to our codebase: confirms that PR finding location = (path, line range, side, commit) and that `in_diff` is a derived per-revision fact. Best practice from GitHub itself: store the ORIGINAL (commit, line) forever, store the CURRENT mapping as a re-computable field, and mark a finding "outdated" rather than silently re-anchor. A cluster key must use the original commit (revision-pinned) so two reviewers who reviewed the same revision cluster by line overlap, while findings across revisions are linked through a separate "tracked-as" relation (SonarQube-style tiered match), not by the same union-find.
- Supports/extends: EXTENDS (revision-pinned original + current location pair; `subject_type: file` = a legitimate location kind with no line, needing a content-derived key per A2).
- Relevance: HIGH

## Transitive-chaining safeguards (union-find over-merge)

### C1. Single-linkage chaining is a documented, general failure of transitive closure
- Sources: https://en.wikipedia.org/wiki/Complete-linkage_clustering (MEDIUM, general reference), https://pmc.ncbi.nlm.nih.gov/articles/PMC4849582 (peer-reviewed record-linkage paper, "Efficient Record Linkage Algorithms Using Complete Linkage Clustering", MEDIUM-HIGH), https://rich-d-wilkinson.github.io/MATH3030/7.3-hierarchical-clustering-methods.html (course notes, MEDIUM).
- Key information: single linkage joins two clusters if ANY pair is close, so chains of close intermediates merge distant members; clusters can have very large diameters. Complete linkage requires ALL pairs in the cluster to be within the threshold (maximum pairwise distance), producing compact clusters, but "behaves badly when outliers are present" (statisticshowto.com, LOW). The record-linkage paper gives a minimal example: A-B and B-C within threshold, A-C beyond it; transitive closure puts all three together, complete linkage does not. Its pipeline uses blocking on stable fields, then complete linkage inside each block, then a post-pass that moves records to the best-matching cluster using a priority list of attributes.
- Relation to our codebase: this is exactly D6 (A-B on anchor 1, B-C on anchor 2, so A and C chain; 83 mega-rows). "Complete-link" in our setting = a candidate joins a cluster only if it matches EVERY current member (or the cluster medoid), not just one. Our findings per cluster are small (a few reviewers x a few lenses), so the O(n^2) cost is negligible; complete-link is affordable.
- Supports codebase finding: YES (D6 confirmed as a textbook failure). Relevance: HIGH

### C2. Entity-resolution literature: transitive closure has high recall and poor precision; "black hole" clusters
- Sources: http://www.vldb.org/pvldb/vol2/vldb09-1025.pdf (Hassanzadeh et al., VLDB 2009, "Framework for Evaluating Clustering Algorithms in Duplicate Detection"; peer-reviewed, HIGH) and https://www.cse.unr.edu/~hkardes/pdfs/organizationEntityResolution.pdf ("Graph-based Approaches for Organization Entity Resolution", MEDIUM-HIGH).
- Key information: "Partitioning" (connected components = transitive closure) "may result in big clusters, [with] many records that are not similar being put in the same cluster"; it is the baseline that the other algorithms (Center, Merge-Center, Star, Ricochet, Correlation Clustering and others) are built to beat, and the paper's results confirm its poor quality. Center assigns a record only if it is similar to the cluster CENTER (not to any member); Merge-Center merges two clusters only when a record similar to one centre sits in the other; Star picks centres by node degree. The second paper measures transitive closure at very high recall but 64% precision (pairwise classifier 97% precision, 63% recall at threshold 0.65), and defines a "black hole threshold": if a connected component exceeds a size cap, raise the match threshold by a delta and repartition that component, repeating until all components are under the cap, then run a finer clusterer inside each component.
- Relation to our codebase: gives three concrete, cheap options in increasing strength: (a) size cap with threshold escalation (black-hole threshold), (b) centre-based assignment (a finding joins a cluster only if it matches the cluster's representative; v2 already computes a representative, so this is a small change), (c) correlation-style pivot clustering. Our measured v2 pair precision of 0.84 sits between the 0.64 (closure) and 0.97 (pairwise) figures from the external paper, consistent in direction (not a like-for-like comparison: different domain).
- Supports/extends: EXTENDS (adds centre-based and black-hole-threshold options beyond complete-link or caps).
- Relevance: HIGH

### C3. A hard size cap limits all chain paths at once (single recent preprint)
- Source: https://arxiv.org/html/2611.03080 (arXiv preprint "VL-Dedup", dated Nov 2026; not peer reviewed, and the domain is image-text records, so reliability LOW-MEDIUM; read via search snippet only, NOT confirmed with extract).
- Key information (as reported in the snippet): one wrong edge joins two groups and every later edge extends the cluster; "the size cap limits all paths at once, because no cluster can grow beyond K records"; the cap must be tuned on validation data with entity sizes like the real corpus: with the cap off the largest cluster grew from 64 to 598 records at the same F1 on that data, with a cap too small (K=5) F1 fell from about 0.998 to 0.299; the cap was never more than 0.0051 below the best of Center, Merge-Center, KwikCluster, MCL and Louvain over eight settings.
- Relation to our codebase: supports a size cap as a SAFETY NET, bounded by the maximum possible members of one true cluster in our setting (number of reviewers x lenses per finding is known, so the cap can be derived instead of tuned: a real cluster cannot exceed one finding per reviewer-lens run, plus a small allowance for split findings). A cap below that bound silently splits true clusters (the K=5 failure).
- Relevance: MEDIUM (flag as unverified)

## Snippet / syntax hashing and occurrence index (more reference designs)

### X1. Semgrep: two fingerprints, occurrence index appended AFTER the hash
- Source: https://docs.semgrep.dev/semgrep-code/remove-duplicates (official docs, read with extract). Reliability: OFFICIAL. (The page notes the calculations "are subject to change at any time".)
- Key information: `syntactic_id` = hash of (file path, rule name, the literal matched code, and an index = count of times that rule matched in the file). `match_based_id` is built from the rule pattern with metavariable values substituted, so it survives moved code and ignores lines that do not change function; the index is "appended to the hash, not combined with the other finding information before hashing ... to preserve information on how findings are related" (e.g. `123_0` and `123_1` = same rule, same pattern, same file, two occurrences). A January 2026 Semgrep release note (https://docs.semgrep.dev/release-notes/january-2026, official) says a bug where the selected representative among equivalent findings was not always identical could make fingerprints change between scans: the choice of representative must be deterministic.
- Relation to our codebase: (1) two-level identity (exact vs abstracted) maps to "exact anchor/citation hash" vs "normalised claim and category hash"; (2) the occurrence index kept outside the hash is a clean way to separate "same defect pattern" from "second occurrence" without merging them; (3) deterministic representative choice is a stated requirement for our cluster representative (v2 already has a representative; make the tie-break explicit and stable).
- Relevance: HIGH

### X2. GitLab scope-offset signatures; third-party SARIF falls back to path+line
- Source: https://docs.gitlab.com/user/application_security/detect/vulnerability_deduplication (official docs, read with extract). Reliability: OFFICIAL.
- Key information: for SAST, GitLab fingerprints a vulnerability by its enclosing scope (class/function chain) plus an offset within the scope, so "a signature that stays the same even when code moves around, as long as it stays within the same scope". Third-party SARIF uploads cannot supply that data; they use "a location fingerprint based on the file path and line numbers", so a vulnerability "can be recorded as a new finding when unrelated code changes shift its line numbers". A primary identifier must be a stable rule key; "a primary identifier that changes between runs, such as a value generated for each scan, breaks tracking and produces duplicate vulnerabilities".
- Relation to our codebase: the same lesson as SARIF logical location: scope (section heading path, task id, symbol) + offset-in-scope is more drift-tolerant than absolute line. For markdown targets the natural scope is the heading path; for code, the enclosing symbol. Never include per-run values (run id, timestamp, reviewer-generated finding ids such as `F-3`) in the identity.
- Supports/extends: EXTENDS (concrete drift-tolerant key: scope + offset). Relevance: HIGH

### X3. Code Climate engine spec: fingerprint defaults to a hash of the referenced code
- Sources: https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md (official spec, `fingerprint` is "a unique, deterministic identifier for the specific issue being reported"; `other_locations` carries extra locations), https://github.com/troessner/reek/issues/1115 (issue report; "when a fingerprint isn't included, Code Climate generates a default one based on a hash of the code referred to by the issue's location", LOW-MEDIUM), https://aarongoldenthal.com/posts/gitlab-code-quality-duplication-analysis-with-pmd-cpd (blog, LOW-MEDIUM; the fingerprint is suffixed with the occurrence number so each duplicate is shown, and GitLab otherwise shows only the LAST occurrence per fingerprint).
- Relation to our codebase: confirms the common default (hash of referenced code), the occurrence-suffix idiom (also seen in CodeQL `:n` and Semgrep `_n`), and a hazard: if two distinct occurrences share one fingerprint, the consumer silently displays one. A cluster with N members must still list all member locations.
- Relevance: MEDIUM

## Deduplicating findings from several AI reviewers (closest to our use)

### D1. Production AI review systems dedup in an orchestrator and use overlap as a confidence signal
- Sources: https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale (engineering blog, read with extract; MEDIUM) and https://blog.cloudflare.com/ai-code-review (engineering blog, read with extract; MEDIUM).
- Key information: LinkedIn: subagents review independently without seeing each other's output; "overlapping findings across subagents can be elevated as high-confidence issues"; a finding from only one model "isn't discarded by default; it's first verified" and rated separately; dedup "converts [cost] into a verification signal" and keeps output bounded. Cloudflare: up to seven specialised reviewers; a coordinator (top-tier model) does (1) dedup, "kept once in the section where it fits best", (2) re-categorisation, (3) a reasonableness filter that reads the source to verify when unsure. Neither post gives the matching algorithm.
- Relation to our codebase: confirms the architecture (independent reviewers, central dedup, agreement as signal, verify singletons) but gives NO clustering recipe, so it does not contradict or help choose the key. It does support keeping "cluster support = number of independent reviewers" as a first-class output of the clusterer.
- Relevance: MEDIUM

### D2. Practitioner dedup rules: location AND defect shape, not text similarity alone
- Sources: https://forum.level1techs.com/t/how-i-do-llm-assisted-code-reviews/250113 (forum post with a prompt for a dedupe stage; LOW reliability, single practitioner) and https://singhajit.com/building-code-review-assistant-with-llms (blog; LOW-MEDIUM; "Deduplicate by file + line + semantic similarity"; validates that the reported file is in the diff and the line is in the diff range before accepting a comment).
- Key information: merge when same file with overlapping line range AND the same defect; also merge different locations with the same root cause; two findings at one location describing different defects are NOT merged; on merge keep the highest severity (do not downgrade) and the union of dimensions/lenses; "Deduping by `claim` text similarity alone -> use location + defect-shape, not surface text".
- Relation to our codebase: matches the codebase direction (path-aware v2 over exact-quote v1). The "different locations, same root cause" rule is the one a pure location key cannot do; it needs a second, explicit link type (root-cause group) layered above location clusters rather than loosening the location key. Input validation (file exists in the diff, line within the diff range) matches our `in_diff` and citation checks.
- Relevance: MEDIUM

## Key External Findings

1. SARIF separates producer-supplied partial identity (`partialFingerprints`, versioned keys, compare on greatest common version), consumer-computed identity (`fingerprints`) and a separate grouping id (`correlationGuid`). Appendix B says build identity from tool, rule id, target path and logical location, which is "more resilient" than line numbers. [OASIS spec] (HIGH)
2. GitHub code scanning matches alerts across commits using only `partialFingerprints.primaryLocationLineHash`, together with `ruleId` and a consistent path; inconsistent paths close the old alert and open a new one; an EMPTY hash degrades to order-based matching and mis-closes alerts. [GitHub docs; one issue report] (HIGH)
3. The CodeQL line hash is a whitespace-insensitive, line-ending-normalised rolling hash of the next 100 non-space characters from the line, with a per-file `:n` suffix for identical hashes: drift-proof for pure line shifts, broken by any edit in the window. [codeql-action source] (HIGH)
4. SonarQube uses ordered rules within the same rule key: same first-line hash (message may differ), else same line number and message, else same offset inside a moved block and message; file renames first. [Sonar docs] (HIGH)
5. Semgrep and GitLab use syntax/scope-based identities (abstracted pattern; scope + offset) and keep the occurrence index OUTSIDE the hash (Semgrep) or as a suffix (CodeQL, Code Climate users) so duplicates stay distinct. [Semgrep, GitLab docs] (HIGH)
6. DefectDojo: tool-native ids only work within one tool; cross-tool dedup needs a hash over fields that carry the same values in every tool; it refuses to dedup when file path and line are both empty; location tracking keeps ONE finding with a location history. [DefectDojo docs] (HIGH, vendor)
7. Transitive closure (union-find/connected components) is the known-bad baseline: high recall, poor precision, "black hole" clusters; complete-linkage, centre-based assignment, size cap with threshold escalation and correlation clustering are the documented remedies. [VLDB 2009; record-linkage paper; organization-ER paper] (HIGH to MEDIUM)
8. GitHub PR review comments store (path, line range, side, commit) and an original-vs-current pair, mark comments Outdated instead of re-anchoring, and treat whole-file comments (`subject_type: file`) as a separate location kind. [GitHub REST docs] (HIGH)
9. Production AI review pipelines (LinkedIn, Cloudflare) dedup centrally and treat multi-reviewer overlap as confidence; they publish no matching algorithm. (MEDIUM; confirms architecture only)

## Recommendations from External Research

(Our codebase remains the source of truth. These are options to weigh in the design; none overrides D1/D6/D7 as verified in 03-clustering.md.)

R1. One location model with explicit kinds, as SARIF does: `locations[]` of `{artifact (normalised repo-relative path or document id), region?(line range), logical?(heading path / task id / symbol), quote_hash?, revision}` with kinds anchor, path+line, file:section, whole-file, multi-file. Keep `in_diff` as per-revision derived state outside identity (GitHub shows alerts only if all lines are in the diff but does not put that in the fingerprint). Supports D-codebase need for a location union. [F1, F2, A1, A3, P1]

R2. Identity = versioned dictionary of components, not one string: `{category_or_rule, path_norm, logical_scope, content_hash/v1, occurrence_index}`; compare on the greatest common version. Keep the occurrence index OUTSIDE the content hash (Semgrep) so "same pattern, second place" stays visible. Never put reviewer-generated ids, run ids, timestamps or the reviewer name into identity. [F1, X1, X2, M2]

R3. Replace exact-quote equality with a drift-tolerant text component: normalise (strip whitespace, unify line endings), truncate to a fixed window (CodeQL uses 100 characters) and hash. This also removes the D1 rejection of anchors over 200 characters (truncate instead of reject). Accept the known limit: one edit inside the window changes identity, so add a second, scope-based component (heading path / task id + offset) as fallback. [H1, X2]

R4. Tiered, ordered matching with a logged reason per match (SonarQube style), always gated on equal category/rule: (1) equal content hash, (2) same scope and same normalised message/claim, (3) overlapping line ranges in the same revision plus same defect shape. Emit `match_reason` per cluster edge for telemetry and for the human labelling that is still pending. [S1, D2]

R5. Never merge on an empty location component. If section/scope/path is empty, require a content-derived component or leave the finding as a singleton (DefectDojo legacy refuses to merge on empty path and line; the SureA11y case shows order-based fallback mis-matches). This directly addresses v2's empty-section over-merge. [A2, M1]

R6. Chaining safeguards, strongest to cheapest to adopt: (a) complete-link or centre-based admission: a finding joins a cluster only if it matches the representative (v2 already computes one) or all members; (b) black-hole threshold: if a connected component exceeds a cap derived from (reviewers x lenses + allowance), raise the match threshold and repartition (organization-ER paper); (c) keep v2's chain flag as a diagnostic; (d) do NOT set a cap below the maximum legitimate cluster size (reported K=5 failure in the preprint, unverified). Component sizes are small here, so O(n^2) complete-link is affordable. [C1, C2, C3]

R7. Cross-revision tracking is a separate link, not part of the clustering key: store the original (revision, location) and recompute the current mapping; mark `outdated` rather than silently re-anchor; first resolve renames, then apply R4's tiers between revision N and N+1. Severity changes must not split a cluster or a tracked identity. [P1, S1, M3]

R8. Cross-reviewer matching uses only shared normalised fields (path or scope, category, cited reference); reviewer-native ids are valid only within one reviewer (DefectDojo). Keep (reviewer, model, lens) as run metadata, and expose `support = distinct independent reviewers` and a deterministic representative tie-break as clusterer outputs. [M1, X1, D1]

R9. Add a separate, explicit "same root cause across different locations" link above location clusters (second-level grouping), rather than loosening the location key; keep highest severity and union of lenses on merge. [D2]

R10. Validate empirically before adopting any threshold: our only quality figures (precision 0.84, recall 0.95) are AI-labelled. External figures (transitive closure 64% precision vs 97% pairwise in one paper) are a different domain and show direction only. Complete the human labelling and measure chain-split changes (mega-row count 83 before) as the acceptance metric.

## Discrepancies and caveats
- Codebase vs external: the codebase's cluster key has no category/rule gate; every mature tracker above gates matching on equal rule or category. This is a gap in our design, not a contradiction of verified code behaviour.
- The arXiv preprint (C3) and forum/blog items (D2, A2) are LOW-MEDIUM reliability and were not independently reproduced; the `original_*` response field names (P1) were seen only on a third-party schema mirror. Verify against the live GitHub API before wiring them.
- No source found gives a published algorithm for clustering findings from several LLM reviewers; D1 and D2 describe architecture and heuristics only.
- Search provider: Tavily (litellm proxy) for all searches and extractions; no WebSearch/WebFetch fallback was needed. Some extract calls returned query-relevant excerpts rather than full pages (SARIF spec Appendix B, GitHub docs); quotes above are from those excerpts.

