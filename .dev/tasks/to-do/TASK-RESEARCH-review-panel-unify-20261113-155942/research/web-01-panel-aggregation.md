# Web Research W1: Multi-Reviewer Panel Aggregation

- Topic: multi-reviewer LLM panel aggregation (quorum vs veto vs judge; ensemble and multi-agent code review; LLM juries; consolidation of duplicate findings)
- Date: 2026-11-13
- Status: Complete

Provider note: Tavily search/extract (litellm proxy) is the intended provider. Entries will say if WebSearch was used instead.

## Codebase context (read first)

Read from research/02-ledger-merge-verdict.md (ledger.py re-read 2026-11-14) and research/05-blocking-calibration.md. Facts used below as "our code":
- C1. Ledger row `blocking = any(member.blocking)` (ledger.py:187, :213-218); `_brief_ids` reads only `blocking` and `status` (:99-104); `confidence` ("overlap" if 2+ distinct reviewers in one round, else "single", :86-90) is displayed but never read by the verdict (D4 partly: display only).
- C2. One nonblocking re-report with no blocking member in the group sets row blocking False (:216-218): one reviewer can also UN-block.
- C3. A round passes if at least one reviewer block is valid (:150-157); an invalid reviewer never prevents clearing a `resolved_check` row (D2/D3); tests/review/test_review_ledger.py:376-385 pins it.
- C4. Reflect side: single-reviewer merge is DEGRADED, not a verdict (contract.py:295-296); T2 adversarial convergence < 0.80 is DEGRADED (contract.py:317-326); blocking classes are Drift and Regression (contract.py:377-381); calibrated C is a tier-routing input, not a per-finding blocking gate (SKILL.md:431-437); calibrator_diversity has no verdict effect in code.
- C5. Experiment: blind binary grader with a frozen rubric decides "blocking" per claim (finding-grader agent).

## 1. Aggregation rules and their error rates

### 1.1 Union ("any reviewer flags") versus majority/weighted voting: recall-precision trade-off (MultiVer)
- Source: https://arxiv.org/html/2602.17875v1 (arXiv 2602.17875, Feb 2026; found via search snippet, not yet extracted: confidence on exact numbers is MEDIUM until extracted below)
- Finding: a zero-shot multi-agent vulnerability-detection ensemble implemented two voting modes. Union voting (any security or correctness WARNING/FAIL triggers an overall warning) gave 82.7% recall, 48.8% precision and 85.0% false-positive rate; weighted voting gave 37.7% recall with 35.3% FPR. The authors state the union rule reflects cost asymmetry ("missing a vulnerability risks a breach; a false positive costs only review time") and call 85% FPR the "primary deployment constraint", unsuitable for CI gating.
- Relation to our code: SUPPORTS the finding that our any-member-blocks rule (C1) maximises recall at the cost of precision. It matches the measured 65 versus 38 blocking result direction (veto over-blocks). Note the domain differs (vulnerability classification, not spec/tasklist review); the direction, not the magnitude, transfers.
- Relevance: HIGH. Reliability: preprint (not peer-reviewed), Feb 2026.

### 1.2 Majority vote across judges, and calibrated weighted voting
- Source: https://arxiv.org/html/2609.12002v1 (arXiv 2609.12002, "Can We Trust LLM Judges: A Study of Capability-Dependent Biases and Multi-Judge Ensemble for Bias Calibration"; arXiv id implies Sep 2026; preprint). Extracted 2026-11-13.
- Finding: stronger examinee models receive systematically more false-positive leniency from all judges, not only from themselves. Cross-judge majority voting (self-judge excluded) already improves accuracy and reduces leniency substantially, but treats all judges as equally reliable. The authors propose calibrated weighted majority voting (WMV): each vote is weighted by an online estimate of that judge's false-positive and false-negative rates, derived purely from inter-judge agreement with no labels; in a simulation with shifting task distributions it tracked an oracle within 0.5 percentage points on average.
- Relation to our code: EXTENDS. Our `confidence` field (C1) is a count-of-distinct-reviewers signal that no decision reads; this paper is an example of using per-judge reliability instead of a flat count. Simulation-only evidence for WMV, so treat as an option, not a proven rule.
- Relevance: HIGH. Reliability: preprint, simulation for the WMV part.

### 1.3 Self-consistency / repeated runs and the aggregator
- Source: https://arxiv.org/abs/2509.01494 and https://arxiv.org/html/2509.01494v1 (SWR-Bench, "Benchmarking and Studying the LLM-based Code Review", Sep 2025; preprint). Extracted from search snippet (arXiv HTML content returned by Tavily search).
- Finding: "Multi-Review" aggregation: run the same PR through several independent review passes and have an aggregator LLM combine them. Two variants: Multi-Agg (distinct LLMs) and Self-Agg (same LLM, multiple runs). With Gemini-2.5-Flash, Self-Agg n=10 raised overall F1 to 21.91% (+43.67%) and recall to 30.44% (+118.83%); the authors say the larger gain in recall shows more true defects are found. The Zylos secondary summary says the F1 curve plateaus near n=5-10 runs (secondary, https://zylos.ai/research/2026-03-01-multi-model-ai-code-review-convergence, dated 2026-03-01).
- Relation to our code: EXTENDS. Aggregation gains here are mostly recall (union-like); it does not evidence that aggregation fixes false blockers. Absolute F1 is low (about 22%), so even the aggregated review is noisy: a blocking gate on raw aggregated findings would over-block.
- Relevance: MEDIUM. Reliability: preprint benchmark.

### 1.4 Agreeableness bias: validators confirm but do not reject; minority veto beats majority vote
- Source: https://arxiv.org/html/2510.11822v2 and https://arxiv.org/abs/2510.11822 ("Beyond Consensus: Mitigating the Agreeableness Bias in LLM Judge Evaluations", arXiv Oct 2025; preprint; OpenReview listing https://openreview.net/forum?id=3IsAoRHi9n). Extracted 2026-11-13.
- Finding: on 366 incorrect high-school Python programs with LLM-generated feedback, 14 state-of-the-art validators had true positive rate above 96% but true negative rate typically below 25% (they confirm valid feedback and fail to reject invalid feedback; overall accuracy is masked by class imbalance, about 7.5% invalid). Majority voting helps but "is not good enough". A Minority Veto (mark "invalid" if at least n validators say so) with n=4 of 14 gave the lowest maximum error, 2.8% after data repair, with TPR 95.5% and TNR 30.9%; the n=4 threshold itself needed a human-labelled calibration set. Minority veto was robust to missing votes; a super-majority rule (10 of 14) that defaults to "invalid" on a missing vote did slightly worse. A regression model of validator bias with a small human-labelled set reached 1.2% maximum absolute error (2x better than the best 14-model ensemble).
- Relation to our code: EXTENDS and PARTLY CAUTIONS. The "veto" here is a veto on the validating side (a few validators can reject a claim), the reverse polarity of our ledger, where one reviewer can assert `blocking` (C1). It shows that a lenient validator or grader is a weak precision filter on its own (TNR under 25%), so the blind-grader design (C5) needs its own measured true-negative rate. It also shows the cost of treating a missing vote as a default answer, which is the shape of D2/D3 (an invalid reviewer counted as "no finding"; C3). Task differs (feedback validity, not blocking severity), so transfer is by analogy.
- Relevance: HIGH. Reliability: preprint, single study; threshold n=4 is tuned on human labels.

### 1.5 LLM reviewers over-reject when asked to check a spec (false blockers)
- Source: https://arxiv.org/html/2603.00539v1 (arXiv Mar 2026; "Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement"); journal version https://link.springer.com/article/10.1007/s10515-026-00638-5 (Automated Software Engineering, 2026). Extracted 2026-11-13.
- Finding: when asked to judge conformance, justify and propose a fix ("Full" prompting), LLMs became overly conservative and rejected correct implementations (high false-negative rate = false rejection; false-positive rate comparatively low). Adding explanation and repair instructions raised misjudgment rather than lowering it. A reviewer can be "right for the inaccurate reason": GPT-4o symptom-level match 98.2% on HumanEval but bug-cause match only 59.1%.
- Relation to our code: SUPPORTS the direction of the other session's measurement that a single reviewer's veto produced wrong blockers (65 blocking versus 38; see C1, and research/05). Suggests a cause-level evidence check (our citation and anchor checks) is more valuable than another reviewer's opinion. Benchmarks are small coding sets (HumanEval, MBPP, QuixBugs), not spec or tasklist review.
- Relevance: HIGH. Reliability: preprint plus journal version.

## 2. LLM juries versus single judges

### 2.1 Panel of diverse smaller judges (PoLL) beats one large judge, in its settings
- Source: https://arxiv.org/abs/2404.18796 (Verga et al., arXiv submitted 29 Apr 2024, v2 1 May 2024; abstract extracted 2026-11-13). Numbers below are from secondary summaries (https://liner.com/review/replacing-judges-with-juries-evaluating-llm-generations-with-panel-diverse, https://www.alphaxiv.org/abs/2404.18796, https://medium.com/@techsachin/replacing-judges-with-juries-llm-generation-evaluations-with-panel-of-llm-evaluators-d1e77dfb521e; dates not shown) and are not read from the paper body.
- Finding (abstract, primary): across three judge settings and six datasets, a panel of a larger number of smaller models from disjoint families outperformed a single large judge, with less intra-model bias, and cost over seven times less. Secondary: three judges (Command R, GPT-3.5, Haiku), scores pooled by max voting or average pooling; Cohen's kappa on KILT-NQ 0.763 versus 0.627 for GPT-4; GPT-4 judge kappa moved from 0.518 to 0.725 with prompt wording; panel selection was left as future work and only three judge settings were tested.
- Relation to our code: SUPPORTS using a heterogeneous panel for grading, and SUPPORTS cheap panel members. Task is answer-correctness scoring, not "is this review finding blocking"; it says nothing about code review. Our T2 requirement of `t2_model_class_diversity == full` (contract.py:282-284, C4) is consistent with its "disjoint families" condition.
- Relevance: MEDIUM (task mismatch). Reliability: peer-visible primary paper (abstract), details secondary.

### 2.2 Counter-evidence: judge errors are correlated, so a panel of N is fewer than N votes
- Source: https://arxiv.org/html/2605.29800v1 ("Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels", arXiv May 2026; preprint) and https://machinelearning.apple.com/research/correlated-llm-evaluation-panels (Apple Machine Learning Research page). Extracted 2026-11-13.
- Finding: 9 frontier LLMs from 7 families on three natural-language-inference datasets (100 human labels per item set) gave about 2 effective independent votes (Kish effective sample size 2.0 to 2.5); panel accuracy fell 8 to 22 percentage points below what independent voting would give; the best single judge matched or beat the full panel in every condition; adding judges or smarter aggregation closed at most 11% of the gap. Same-family error correlation (phi 0.437, 0.435) was only slightly above the cross-family mean (0.389); the three most correlated pairs were all cross-family (Claude x Gemini 0.603); one-judge-per-family panels still had n_eff about 1.93. The authors note PoLL compares a panel with the average individual judge, not the best one.
- Relation to our code: CONTRADICTS a naive reading of heterogeneity as a guarantee. Our diversity gate counts model classes and vendors (contract.py:282-288, C4), which measures label diversity, not error independence. A "2-of-3 quorum" may behave like about 2 votes, and the panel should be compared with its best single reviewer in telemetry. Tasks are NLI and preference, not code review.
- Relevance: HIGH. Reliability: preprint (Apple authors listed on the research page), recent.

### 2.3 Self-preference and judge-family separation
- Source: https://www.alphaxiv.org/abs/2410.21819 ("Self-Preference Bias in LLM-as-a-Judge", arXiv Oct 2024; summary page, not the paper body); https://agentpatterns.ai/verification/judge-self-preference-detection (practitioner page citing Zheng et al. 2023, arXiv:2306.05685, strong judges above 80% agreement with humans); https://www.linkedin.com/posts/swordhealth_ai-judge-bias-why-judges-favor-their-own-activity-7508556825659822080-vlHX (LinkedIn post by a company research team citing a COLM 2026 paper; weakest source here).
- Finding: GPT-4 had the highest measured self-preference bias (0.520) among judges tested; recommendations are an ensemble of different models and periodic calibration against human ground truth. The LinkedIn post reports that a rubric did not remove self-preference, that ensembling helped but did not eliminate it, and that in the worst case a judge was 20x more likely to pass its own failed unit tests.
- Relation to our code: SUPPORTS the disjoint-set rule that the calibrator or grader class must differ from the reviewer classes (SKILL.md section 11.3, C4) and shows that rule is necessary, not sufficient. Note `calibrator_diversity: degraded` changes no verdict in code (research/05), so the rule is advisory today.
- Relevance: MEDIUM. Reliability: summary page plus practitioner and social posts (LOW to MEDIUM); the LinkedIn claim is unverified against the paper.

### 2.4 Debate versus meta-judge: debate amplifies bias
- Source: https://arxiv.org/html/2505.19477v3 and https://aclanthology.org/2025.findings-emnlp.941.pdf ("Judging with Many Minds: Do More Perspectives Mean Less Prejudice?", arXiv May 2025, EMNLP 2025 Findings). Snippets from the primary text via search; not fully extracted.
- Finding: in multi-agent debate, position, verbosity, chain-of-thought and bandwagon biases rose sharply after the first debate and stayed high; an LLM-as-meta-judge was more resistant. A meta-judge that selects the best candidate judgment had bias comparable to single-agent; one that generates a new judgment from the candidates cut bias more, especially with larger judgment pools. Adding a bias-free agent (PINE debiasing) helped debate and sometimes beat the meta-judge.
- Relation to our code: directly bears on the conflict. Reflect's adversarial-debate merge (C4) is the debate pattern; the experiment's blind grader (C5) is closer to a meta-judge over candidate findings. The paper measures bias, not blocking accuracy, so it does not prove the grader is more accurate; it does argue that debate is not safer by default.
- Relevance: HIGH. Reliability: peer-reviewed venue (Findings), primary.

## 3. Multi-agent code review systems

### 3.1 Cursor Bugbot: parallel passes, majority vote on singletons, validator, then an agentic redesign
- Source: https://cursor.com/blog/building-bugbot (vendor engineering blog; publication date not shown in the extract, text refers to "this fall"; secondary sources place the figures in early 2026). Extracted 2026-11-13. Secondary: https://victorinollc.com/thinking/ai-code-review-bugbot (52% to 70% resolution rate over 6 months and 40 experiments), https://zylos.ai/research/2026-03-01-multi-model-ai-code-review-convergence (dated 2026-03-01), https://www.spotdev.co.uk/blog/cursor-bugbot-ai-code-review (notes the metric is resolution by merge, "not false-positive rates").
- Finding: the early pipeline was: eight parallel passes with randomized diff order; combine similar bugs into one bucket; majority voting to drop bugs found in only one pass; merge each bucket into one description; filter unwanted categories; validator model to catch false positives; dedupe against bugs posted in earlier runs. The largest later gains came from a fully agentic design (agent reasons over the diff, calls tools, decides where to dig), which needed aggressive prompts that flag more. The extract does not say whether majority voting survived in the agentic version [UNCONFIRMED]. Resolution rate (share of reported bugs fixed by merge) rose 52% to 70% (secondary).
- Relation to our code: EXTENDS. It is a worked example of count-based singleton suppression plus a separate validator, and its step 7 (dedupe against previous runs) is the same job as our cross-round row matching (ledger.py:166-171). Caution: Bugbot's passes are one model with shuffled input, so single-pass findings are more likely noise than in a panel of different model families (inference, see 3.6).
- Relevance: HIGH. Reliability: vendor first-party blog for its own design; metric definitions self-reported.

### 3.2 Cloudflare: coordinator judges, deduplicates and decides blocking by severity rubric
- Source: https://blog.cloudflare.com/ai-code-review (vendor engineering blog; date not shown in extract). Extracted 2026-11-13.
- Finding: up to seven specialised reviewers run in parallel; a coordinator agent deduplicates, re-categorises, and applies a "reasonableness filter" that drops speculative issues, nitpicks and false positives, reading source with tools when unsure. The approval decision is a fixed rubric: any critical item or production safety risk gives `significant_concerns` (requested changes, blocks merge); multiple warnings suggesting a risk pattern revoke approval; a single warning in a clean change still gets `approved_with_comments`. The post states the bias is explicitly toward approval.
- Relation to our code: SUPPORTS a single adjudicator (not the reviewers) deciding blocking from a severity rubric, with the blocking trigger being a severity class (like reflect's Drift/Regression classes, contract.py:377-381) after a verification filter. Differs from reflect in that a single warning never blocks. The policy bias is stated, which our ledger lacks.
- Relevance: HIGH. Reliability: vendor first-party; no error rates published in the extract.

### 3.3 LinkedIn: overlap raises confidence; singletons are verified, not discarded
- Source: https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale (company engineering blog; date not shown in extract). Extracted 2026-11-13.
- Finding: each subagent (a distinct model-and-harness pairing) reviews the full diff without seeing the others' output. A finding raised independently by two or more subagents is treated as high-confidence and elevated. A finding from only one model is not discarded by default: it is passed back for verification, then rated separately for importance; the post says one model often misses a real issue another catches and confirms on re-check. Findings failing validation or scoring low on relevance heuristics become filter candidates.
- Relation to our code: SUPPORTS using overlap (our `confidence` "overlap" versus "single", ledger.py:86-90, currently display-only per C1) as a routing input to verification, not as a drop rule and not ignored. CONTRADICTS the Bugbot-style drop-singletons rule for heterogeneous panels (see 3.6).
- Relevance: HIGH. Reliability: vendor first-party.

### 3.4 Evidence that most true defects are found by only one model
- Source: https://zenodo.org/records/21328807 ("A Single LLM Is an Incomplete Code Reviewer: Evidence that Independent Review by Multiple LLM Families Recovers Code Defects Any One Model Misses", Zenodo record, version 2; reviews dated April to July 2026; not peer reviewed; single-organization case study). Read from the search result abstract, not a full-text extract.
- Finding: 33 code or mixed artifacts, 294 human-confirmed issues, fifteen model versions across eight providers. No large-sample model exceeded about 61% code recall (typical about half). 56.8% of confirmed defects (167 of 294) were found by exactly one model; median pairwise cross-family Jaccard about 0.29. Within artifacts, coverage rose from about 47% with one reviewer to about 72% with a second (largest step) with diminishing returns after; authors recommend two or three independent reviewers and a human verifying findings against source, and do not claim a specific second provider beats re-runs.
- Relation to our code: SUPPORTS keeping a union-of-reviewers candidate set (C1 recall behaviour) and CONTRADICTS a hard quorum as the only blocking gate: requiring agreement would have dropped more than half of the confirmed defects in this corpus. It also supports reflect's rule that a single-reviewer outcome is degraded (contract.py:295-296), since the second reviewer adds the most.
- Relevance: HIGH. Reliability: LOW to MEDIUM (preprint repository, self-published, single team corpus).

### 3.5 Recall-oriented aggregation and the precision price
- Sources already cited: MultiVer (1.1) and SWR-Bench Multi-Review (1.3). Additional secondary: https://dev.to/pyor/multiple-ai-code-reviewers-do-parallel-bots-help-57ag (Aug, year not shown) citing an experiment in which four parallel reviewers flagged 93.4% unique issues with no same-line overlap; https://www.augmentcode.com/guides/deep-code-review-recall-vs-precision (vendor guide, updated Aug 2026) arguing that when an agent filters before comments exist, recall is the better scan-layer target while a missed bug still reaches production.
- Finding: ensembles are usually run to raise recall; false positives stack with each added reviewer (dev.to); the cost of a false positive depends on whether a human or an agent reads it next (Augment guide).
- Relation to our code: EXTENDS. Supports a two-stage design (wide candidate set, then verification) rather than a stronger vote at the first stage. The 93.4% figure is second-hand and not verified against its original.
- Relevance: MEDIUM. Reliability: LOW (secondary blog and vendor marketing guide).

### 3.6 Practitioner consensus tools (structured findings grouped by location)
- Source: https://blog.mozilla.ai/the-star-chamber-multi-llm-consensus-for-code-quality (Mozilla.ai blog; date not shown) and https://www.zenml.io/llmops-database/building-and-deploying-production-llm-code-review-agents-architecture-and-best-practices (Ellipsis, 2024, summarized by ZenML).
- Finding: Star Chamber fans a review out to several providers with no cross-visibility and classifies issues as consensus (all providers), majority (two or more) or individual (one provider, "may be a specialised insight, or may be noise"); providers return JSON with typed severity, `file:line` location and category, so grouping uses location and category rather than fuzzy text. Ellipsis runs parallel comment generators and a filter pipeline: deduplication, confidence threshold, a hallucination filter that checks each comment against its attached evidence, and comment editing.
- Relation to our code: SUPPORTS our typed finding contract and anchor/citation checks as the enabling condition for reliable clustering (research/02 section 1, findings.py anchors). Our rule that a finding whose anchor is not in the document still becomes an open blocking row (test at tests/review/test_review_ledger.py:408-417, D5) is the opposite of Ellipsis's evidence filter.
- Relevance: MEDIUM. Reliability: vendor and practitioner blogs; Ellipsis is a third-party summary.

### 3.7 Inference that connects 3.1, 3.3 and 3.4 (not a sourced claim)
Cursor drops singletons (same model, shuffled input); LinkedIn verifies singletons (different model-and-harness pairings); the Zenodo corpus says most true defects are singletons across families. The three are consistent if singleton handling depends on reviewer independence: with homogeneous passes a singleton is more likely noise, with heterogeneous reviewers it is more likely a real catch. This is the inference of this report and is not stated by any one source.

## 4. Deduplicating findings across reviewers

### 4.1 Common shape of production dedup
- Sources: Cursor (3.1), Cloudflare (3.2), LinkedIn (3.3), Mozilla.ai (3.6), plus a forum write-up https://forum.level1techs.com/t/how-i-do-llm-assisted-code-reviews/250113 (community forum post, date not shown, LOW).
- Finding: the shared sequence is cluster findings that describe the same underlying problem, keep the merged item once where it fits best (Cloudflare), keep every contributing finder id and dimension on the merged record, let a verifier's severity override the finder's self-assessment, drop refuted items and carry "uncertain" with a reason (forum post), and dedupe again against earlier runs (Cursor step 7). Grouping works best on typed location and category fields (Mozilla.ai).
- Relation to our code: SUPPORTS our design: `_members` tracking, row match against the previous ledger (ledger.py:166-171), and the `same_defect` fingerprint. EXTENDS: verifier-severity-overrides-reviewer-severity is not in the ledger (blocking is any member's flag, C1) and is a ready-made alternative to `any(...)`.
- Relevance: HIGH. Reliability: vendor blogs (MEDIUM), forum post (LOW).

### 4.2 Embedding-based semantic dedup (generic)
- Source: https://docs.nvidia.com/nemo/curator/curate-text/process-data/deduplication/semdedup (NVIDIA NeMo Curator documentation; date not shown).
- Finding: general technique: embed items, cluster with k-means, compute pairwise cosine similarity inside clusters, treat pairs above a threshold as duplicates, keep one representative per group.
- Relation to our code: EXTENDS only as a fallback to anchor-and-fingerprint matching; documented for dataset curation, not for review findings, and no over-merge risk analysis for distinct defects was found.
- Relevance: LOW. Reliability: official vendor docs for the tool, wrong domain for our case.

### 4.3 Gaps (searched, not found)
- No peer-reviewed measurement was found of over-merge or under-merge error rates when clustering findings from several LLM reviewers, nor of how clustering errors change a blocking verdict. The dedup evidence above is practitioner description, not measurement.
- No source evaluated blocking decisions for spec or tasklist review (non-code documents) with a panel; all measured tasks are code, QA, NLI or feedback validity.
- Tavily was the provider for every search and extract in this file; WebSearch and WebFetch were not needed. context7 was not used (no library or framework API question).

## Discrepancies with the codebase
- None of the sources contradicts verified code behaviour. One wording point: the codebase note that `confidence` is "computed but unused" is only partly true (research/02 D4: it is displayed, not decision-bearing); the external sources treat overlap count as a decision or routing input, so the gap is a design choice, not a code error.
- Reflect's DEGRADED-on-single-reviewer rule (contract.py:295-296) and the ledger's PASS-on-one-valid-reviewer behaviour (ledger.py:150-157) are inconsistent with each other; external evidence (3.4, 2.2) supports treating one reviewer as insufficient for a PASS.

## Key External Findings

- Any-reviewer ("union") rules maximise recall and pay in false positives: 82.7% recall with 85.0% FPR (48.8% precision) for union voting versus 37.7% recall and 35.3% FPR for weighted voting (https://arxiv.org/html/2602.17875v1, Feb 2026, vulnerability detection). Relevance HIGH; direction matches our any-member-blocks ledger (C1).
- LLM reviewers checking code against requirements over-reject correct work, and richer prompts make it worse (https://arxiv.org/html/2603.00539v1, Mar 2026). Relevance HIGH; matches the measured wrong-blocker problem.
- LLM validators confirm but do not reject: TPR above 96%, TNR below 25%; majority vote is not enough, a calibrated minority veto is better, and missing votes must not default to an answer (https://arxiv.org/html/2510.11822v2, Oct 2025). Relevance HIGH; warns that a blind grader needs a measured true-negative rate, and maps to D2/D3.
- Heterogeneous panels beat a single large judge on average (PoLL, https://arxiv.org/abs/2404.18796, Apr 2024) but judge errors are correlated: 9 judges gave about 2 effective votes and the best single judge matched or beat the panel (https://arxiv.org/html/2605.29800v1, May 2026). Relevance HIGH; diversity of labels does not guarantee independent votes.
- Debate amplifies judge bias after the first round; meta-judge aggregation is more resistant (https://arxiv.org/html/2505.19477v3, EMNLP 2025 Findings). Relevance HIGH; debate is not safer than a grader by default, though accuracy was not measured.
- Production systems separate finding from deciding: reviewers propose, a coordinator or verifier deduplicates, verifies against source and applies a severity rubric before anything blocks (Cloudflare https://blog.cloudflare.com/ai-code-review, LinkedIn https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale, Cursor https://cursor.com/blog/building-bugbot). Relevance HIGH; vendor first-party, no error rates.
- Singleton handling splits the field: Cursor drops findings seen in one pass; LinkedIn verifies them; a self-published corpus found 56.8% of confirmed defects were found by exactly one of fifteen model versions and that the second reviewer is the biggest coverage step (https://zenodo.org/records/21328807, 2026). Relevance HIGH; a hard quorum alone would discard real defects (reliability LOW to MEDIUM).
- Aggregation gains in review benchmarks are mostly recall, and absolute F1 stays low (Self-Agg n=10: F1 21.91%, recall 30.44%; https://arxiv.org/abs/2509.01494, Sep 2025). Relevance MEDIUM.
- Dedup evidence is practitioner description only; no measured over-merge or under-merge error rate was found (section 4.3).

## Recommendations from External Research

These are options for the merge and blocking rule; the codebase remains the source of truth, and several cite inference marked below.

1. Split "candidate" from "blocking". Keep a wide any-reviewer candidate set (supported by recall evidence in 3.4 and 1.1) but make a finding blocking only after a verification step that re-checks it against source (anchor and citation checks first, then an independent adjudicator). Sources: Cloudflare, LinkedIn, Cursor validator, 1.5. This replaces `blocking = any(member.blocking)` (ledger.py:187, :213-218) as the decider while keeping it as the candidate filter.
2. Do not use a hard N-of-M quorum as the only gate. Use reviewer overlap as a routing and priority signal (verify singletons, rank overlaps first), as LinkedIn does. Reason: 3.4 (56.8% singletons among confirmed defects) and 2.2 (a panel of N is fewer than N votes). Wire the existing `confidence` field into this routing instead of leaving it display-only.
3. Let a blind adjudicator, not a debate, decide blocking, but measure it. Evidence favours meta-judge-style aggregation over debate for bias (2.4) and favours a different model family from the reviewers (2.3). Before trusting the grader, build a small human-labelled calibration set and report the grader's true-negative rate on known-false blockers, because validators are agreeable (1.4). Compare the panel with its best single reviewer in telemetry, not only with the average (2.2).
4. Treat an invalid or truncated reviewer block as an abstention that counts against the quorum of valid reviewers, not as "no findings". Evidence: missing-vote handling changed results in 1.4; the second reviewer is the biggest coverage step (3.4). Concretely, a PASS should need at least two valid reviewers (reflect already degrades a single-reviewer merge, contract.py:295-296), while a FAIL needs one verified blocking finding. This rule is an inference from those sources, not stated by any of them; it would change the assertion at tests/review/test_review_ledger.py:385 on purpose.
5. If a vote threshold is used anywhere (for example to promote a verified singleton), tune it on human labels; the minority-veto threshold in 1.4 was calibrated, not assumed. Prefer per-reviewer reliability weights learned from agreement (1.2) only after a calibration set exists (simulation-only evidence).
6. Dedup on typed fields (location, category, anchor), keep every contributing reviewer id on the merged record, and let the verifier's severity override a reviewer's self-assigned severity (4.1). Dedupe again across rounds, as the ledger already does. Treat embedding similarity as a fallback only (4.2).
7. State the verdict bias explicitly (Cloudflare states "bias toward approval") and record, per round, how many blockers were dropped at verification, so the policy is auditable.
8. Measure outcome, not volume: track the share of blocking findings that were actually fixed or upheld (Cursor's resolution rate, 3.1) rather than comment count. Caveat: that metric is self-reported and is not a false-positive rate.
9. Avoid over-relying on extra reviewers: the second reviewer gave the biggest gain and returns diminished after two to three (3.4, 2.2), so a panel of three heterogeneous reviewers plus one adjudicator is the evidence-supported size; more should be justified by measured error independence.

Status: Complete


