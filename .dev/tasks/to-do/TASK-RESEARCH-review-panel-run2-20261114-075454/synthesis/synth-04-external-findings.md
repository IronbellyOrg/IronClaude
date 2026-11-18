# Synthesis 04: External Research Findings

Date: 2026-11-14
Status: Complete
Inputs: `research/web-01-multi-model-review-evidence.md`, `research/web-02-claude-code-hooks-headless.md`, `research/web-03-git-branch-hierarchy-stacked-prs.md`, `research/web-04-finding-schemas-review-bots.md`
Research question context: which ONE unified central Review Panel design captures all the value of E1, E2 and E3 and keeps future PR code review and rf-qa replacement unblocked.

## 5. External Research Findings

**All findings in this section are EXTERNAL CONTEXT.** They come only from the four web research files. Every block is marked `[EXTERNAL]`. External findings never override code-verified facts. Where a web file records that its codebase statement was handed in and not verified, that caveat is kept. Wherever a web file says a codebase research file takes precedence, that is repeated here.

**Web provenance (kept from each web file):**

| Web file | web-provenance | Status in file | Date in file |
|---|---|---|---|
| web-01-multi-model-review-evidence.md | provider=tavily; no WebSearch/WebFetch fallback used | Complete | 2026-11-14 |
| web-02-claude-code-hooks-headless.md | provider=tavily (Tavily returned passages, not full pages, for the official docs) | Complete | 2026-11-14 |
| web-03-git-branch-hierarchy-stacked-prs.md | provider=tavily (default); no fallback fired | Complete | 2026-11-14 |
| web-04-finding-schemas-review-bots.md | provider=tavily; no fallback used | Complete | 2026-11-14 |

**How to read the Relationship field.** `supports` = the external finding agrees with a codebase fact or design as handed to the web researcher; `extends` = it adds information the codebase facts do not cover; `contradicts` = it conflicts with a codebase fact or with an assumption. The codebase facts quoted in the web files (E1, E2, E3 labels, `tests/review/test_review_ledger.py:376-385`, `src/superclaude/agents/reflect-reviewer.md`, `src/superclaude/pr_submit/`) were supplied to the web researchers as context; each web file says they were not re-verified there, and this synthesis did not re-verify them either. Many of them are marked `[UNVERIFIED]` by web-01 and web-02.

**Discrepancies with code-verified facts.** None of the four web files records an external source that contradicts a code-verified behaviour. Web-03 states explicitly that research item 2.18 (`research/18-repo-constraints-and-branching.md`, scratch-repository ref-rule test) takes precedence over its summary. If a discrepancy appears later, the code wins.

### 5.1 Multi-model review evidence

Source file: `research/web-01-multi-model-review-evidence.md` (labels A1 to G2 below are that file's labels). Almost all evidence is on QA, NLI, SQL or chat-quality tasks; transfer to PR code review is `[UNVERIFIED]` unless stated. Codebase facts handed to the web researcher: E1 uses 3 heterogeneous reviewers per shadow run with class dispatch (collapse to 1 of 3 distinct models under tier3 is `[UNVERIFIED]`; 7 multi-reviewer clusters among 216 findings is `[UNVERIFIED]`); E2 uses independent reviewers per model id, one valid reviewer passing is a code behaviour (`tests/review/test_review_ledger.py:376-385`), and blind judges score against a 16-defect ground truth; E1's seeded-defect quality measurement was never run.

#### 5.1.1 LLM-as-judge biases (position, verbosity, self-preference)

**Finding:** [EXTERNAL] [A1] Zheng et al. (MT-Bench / Chatbot Arena) name four judge limits: position bias, verbosity bias, self-enhancement bias and limited reasoning. All tested judges showed strong position bias (most favour the first position); Claude-v1 also showed a name bias toward "Assistant A". With biases addressed, GPT-4 agreement with humans exceeds 80%, equal to human-human agreement. Named mitigations: swap positions and accept only consistent verdicts, reference-guided grading, few-shot and chain-of-thought judges. Second-hand figures (not read in the primary paper by the web researcher): GPT-4 order-swap consistency 65.0% on deliberately similar answers (alphaxiv summary); repetitive-list attack failure 91.3% for Claude-v1 and GPT-3.5 versus 8.7% for GPT-4 (note.com summary); self-enhancement roughly 10% higher win rate for GPT-4 and roughly 25% for Claude-v1 (substack summary).
**Source:** https://arxiv.org/abs/2306.05685 (full text https://arxiv.org/html/2306.05685v4); secondary: https://www.alphaxiv.org/abs/2306.05685, https://tailoredai.substack.com/p/judging-llm-as-a-judge-with-mt-bench, https://note.com/_snsk/n/nf67a8c43e938?hl=en. Reliability: peer-reviewed (NeurIPS 2023 datasets track); summaries are blog-grade.
**Relevance:** HIGH
**Relationship to codebase:** supports. Per web-01 A1, blind judging against a ground truth (E2's 16-defect design) matches the paper's reference-guided approach; extends it with a need to randomise order and control length wherever a judge sees two reviewers' findings side by side.

**Finding:** [EXTERNAL] [A2] Panickssery, Bowman and Feng: LLM evaluators recognise their own outputs and score them higher than others' while human annotators rate them equal. Out of the box, GPT-4 and Llama 2 tell their own outputs from other LLMs' and humans' with non-trivial accuracy. After fine-tuning, self-recognition correlates linearly with self-preference strength, and controlled experiments argue the link is causal.
**Source:** https://arxiv.org/abs/2404.13076 ; https://neurips.cc/virtual/2024/poster/96672. Reliability: peer-reviewed (NeurIPS 2024).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-01 A2). A panel reviewer from the same model family as the code author may favour that code. Whether the code under review was written by a panel model was not given to the web researcher, so the exposure is `[UNVERIFIED]`. Evidence is on text and summaries, not on code review.

**Finding:** [EXTERNAL] [A3] Chen et al. 2025: self-preference appears in both pre-trained and post-trained models. The "DBG" score compares judge win rates against gold judgments to separate quality from bias. Reasoning models are not automatically less biased (DS-R1-Distill-Qwen-32B 4.8% DBG versus Qwen2.5-72B-Instruct 2.6%). An overview site lists mitigations (blind evaluation, ensemble judging, activation steering); a NeurIPS 2025 paper found activation steering changes outcomes in up to 97% of biased cases but destabilises legitimate evaluations.
**Source:** https://aclanthology.org/2025.emnlp-main.86.pdf ; https://neurips.cc/virtual/2025/122352 ; overview https://www.emergentmind.com/topics/self-preference-bias (secondary aggregator). Reliability: peer-reviewed (EMNLP 2025, NeurIPS 2025).
**Relevance:** MEDIUM
**Relationship to codebase:** supports (web-01 A3). Using gold labels (E2's 16-defect ground truth, or E1's never-run seeded-defect design) is the same remedy the paper uses; web-01 says this strengthens the case for running the seeded-defect measurement E1 designed.

**Finding:** [EXTERNAL] [A4] Ye et al., CALM: defines 12 judge biases (position, verbosity, compassion-fade, bandwagon, distraction, fallacy-oversight, authority, sentiment, diversity, chain-of-thought, self-enhancement, refinement-aware) and tests each by an attack-and-detect perturbation (change one bias-inducing feature, check verdict stability; position bias by rotating answer order). Conclusion: advanced models such as Claude-3.5 and GPT-4o can be reliable judges for specific tasks, but significant biases persist in specific tasks and robustness varies.
**Source:** https://arxiv.org/abs/2410.02736 (HTML https://arxiv.org/html/2410.02736v1); https://proceedings.iclr.cc/paper_files/paper/2025/file/fdca08d371e4b6c031397909e20043bd-Paper-Conference.pdf. Reliability: peer-reviewed (ICLR 2025).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-01 A4). Gives a ready test method for E2's blind judges and any merge judge. The web researcher's own inference, not the paper's: authority and bandwagon biases mean showing a judge "2 of 3 reviewers agree" may bias it.

#### 5.1.2 Panels of diverse models, and correlated errors

**Finding:** [EXTERNAL] [B1] Verga et al. (Cohere), PoLL: a panel of smaller judges from disjoint families (Command R, Haiku, GPT-3.5) pooled by a voting function correlated better with human judgments than a single GPT-4 judge across three judge settings and six datasets, showed less intra-model bias, and cost over seven times less. KILT-NQ Cohen's kappa with humans (liner.com summary): PoLL 0.763, GPT-4 0.627, Haiku 0.749, Command R 0.734, GPT-3.5 0.726. Chatbot Arena: PoLL Pearson 0.917 with crowd Elo (alphaxiv summary). Authors' stated limits: only three judge settings and limited panel compositions; math and reasoning not tested; panel selection left as future work.
**Source:** https://arxiv.org/abs/2404.18796 ; https://huggingface.co/papers/2404.18796 ; summaries https://liner.com/review/replacing-judges-with-juries-evaluating-llm-generations-with-panel-diverse, https://www.alphaxiv.org/abs/2404.18796. Reliability: arXiv preprint from an industry lab (peer review not confirmed in sources read); figures from summaries are second-hand.
**Relevance:** HIGH
**Relationship to codebase:** supports (web-01 B1) the 2-3 heterogeneous reviewer design, and extends it: heterogeneity helps by cancelling intra-model bias. The task is answer-correctness QA, not defect finding, so transfer is `[UNVERIFIED]`. If E1's class dispatch collapses to fewer distinct models under tier3 (`[UNVERIFIED]` in the codebase), the diversity benefit would shrink accordingly. It says nothing about which voting function suits a "find defects" task.

**Finding:** [EXTERNAL] [B2] Kim, Garg, Peng and Garg, "Correlated Errors in LLMs": across over 350 LLMs, substantial error correlation (on one leaderboard dataset, models agree 60% of the time when both are wrong). Shared architecture and provider raise correlation, but larger, more accurate models have highly correlated errors even across providers. As judges, models inflate the accuracy of less accurate models and under-rate more accurate ones, more so for same-provider models. Recommendations from the paper: anchor to ground truth, pick judges with uncorrelated error patterns, use multi-judge consensus, track error correlation.
**Source:** https://arxiv.org/abs/2506.07962 ; https://www.alphaxiv.org/abs/2506.07962. Reliability: ICML 2025 per a repository README citing it (venue not checked on the arXiv page).
**Relevance:** HIGH
**Relationship to codebase:** extends and partly cautions against B1 (web-01 B2); does not contradict the codebase. Different model classes are necessary for diversity but may not be sufficient. E1's low reviewer overlap (7 multi-reviewer clusters among 216 findings, `[UNVERIFIED]`) measures overlap in what reviewers flag, which is not error correlation; it cannot be turned into one without the ground truth E1 never ran.

**Finding:** [EXTERNAL] [B3] Kohli, "Nine Judges, Two Effective Votes" (Apple ML Research; arXiv 2605.29800): 9 frontier LLMs from 7 families on three NLI datasets with 100 human annotations per item carry only about 2 independent votes of information (Kish effective sample size). Panel accuracy falls 8-22 points short of the independent-voting ideal; the best single judge matches or beats the full panel in all conditions. Same-family pairs are only slightly more correlated than cross-family (phi 0.437 versus 0.389); the three most correlated pairs are cross-family (Claude x Gemini 0.603). One judge per family leaves n_eff at 1.93. Adding judges or smarter aggregation closes at most 11% of the gap. A secondary summary reports that even when all 9 judges agreed they were wrong 9.1% of the time (not verified in the primary text). Authors' limits: gold standard is a 100-annotator majority; tasks are NLI and one preference task, not code review.
**Source:** https://machinelearning.apple.com/research/correlated-llm-evaluation-panels ; https://arxiv.org/html/2605.29800v1 ; secondary https://note.com/logicalskill/n/n53fc8c04b75e?hl=en. Reliability: preprint from a corporate research lab; peer-review status not shown; publication date not extracted (2026 per its arXiv id).
**Relevance:** HIGH
**Relationship to codebase:** contradicts (in part) the assumption that three model families give three independent opinions (web-01 B3); consistent with the codebase fact, as handed in, that citations are verified by code in the planned core. It is evidence about voting on a shared answer; a panel whose value is the union of distinct, independently verified findings is a different mechanism, so applicability is `[UNVERIFIED]`. It argues for verification that is not another LLM vote (see 5.1.6).

**Tension table (web-01, "Discrepancies and gaps"):**

| Claim | Source in web-01 | Counter-source | Note |
|---|---|---|---|
| Diverse-family panel beats a single large judge | B1 PoLL | B2 Kim et al.; B3 Kohli: cross-family judges still make correlated errors | All measured on single-answer tasks (QA, NLI), so none settles the review-panel question |
| Merge keeps only findings flagged by 2 of 3 reviewers | D3 Entelligence golden-set rule | D1 SWR-Bench: union gains recall because few findings overlap | See the merge and verdict rule table in 5.1.7 |
| Independent review plus merge is a sound default | C1 | none found | No peer-reviewed study of heterogeneous multi-reviewer PR-review panels that compares quorum rules on findings with ground truth was found |

#### 5.1.3 Debate versus independent review plus aggregation

**Finding:** [EXTERNAL] [C1] "Debate or Vote" (NeurIPS 2025): across seven NLP benchmarks, majority voting over independent agents' initial answers accounts for most of the gain usually credited to multi-agent debate; in most cases voting without debate performs on par with debate. The authors model debate as a martingale over agents' beliefs and conclude debate alone does not raise expected correctness; the study also covers heterogeneous agent populations and open-ended tasks. They do not claim debate can never help; they propose strategies that preserve correct answers across rounds and report gains from those. Tasks are single-answer NLP benchmarks, not defect finding.
**Source:** https://arxiv.org/abs/2508.17536 ; https://proceedings.neurips.cc/paper_files/paper/2025/file/934252acd87f254d5d4672fbde283bd2-Paper-Conference.pdf ; https://neurips.cc/virtual/2025/poster/116557. Reliability: peer-reviewed (NeurIPS 2025).
**Relevance:** HIGH
**Relationship to codebase:** supports (web-01 C1). E2 ran independent reviewers per model id and merged afterwards, the "independent then aggregate" side of this comparison. Does not contradict anything verified in code. It does not test finding-set unions, so applicability to a merge that keeps single-reviewer findings is `[UNVERIFIED]`.

**Finding:** [EXTERNAL] [C2] An explainer states the voting lift depends on independent errors (same model, same prompt gives correlated errors and the vote barely helps); debate's failure mode is conformity (a confident wrong answer wins), countered by diversity of models, prompts and roles. Its numbers (5 agents at 60% give 68%, 15 give 79%) are textbook arithmetic under independence, not an empirical LLM result.
**Source:** https://datarekha.com/agentic-ai/multi-agent-debate. Reliability: blog/tutorial (lowest tier).
**Relevance:** LOW
**Relationship to codebase:** supports (web-01 C2), but only as framing, not evidence: it explains why cross-model dispatch matters and why a tier setting that collapses reviewers to one model removes the benefit.

#### 5.1.4 Code-review-specific evidence on ensembles and merge rules

**Finding:** [EXTERNAL] [D1] SWR-Bench: 1,000 manually verified PRs, LLM-based evaluation of whether ground-truth issues are covered (about 90% agreement with human judgment). A "Multi-Review" strategy generates several independent reviews and aggregates them with one extra LLM call: "Multi-Agg" over different LLMs, "Self-Agg" over repeated runs of one LLM. Reported: F1 up to +43.67%; Gemini-2.5-Flash with Self-Agg (n=10) reached 21.91% overall F1 and 30.44% recall (+118.83% recall). Overlap analysis: only 36 change-points overlapped across different LLMs and 27 across five runs of the same LLM (alphaxiv summary). Authors list reducing false positives while keeping recall as future work.
**Source:** https://arxiv.org/abs/2509.01494 ; https://arxiv.org/html/2509.01494v1 ; summary https://www.alphaxiv.org/abs/2509.1494v1 (URL as returned by search, per web-01). Reliability: arXiv preprint (peer review not shown).
**Relevance:** HIGH
**Relationship to codebase:** supports (web-01 D1) a union-style merge, and extends it. It is the closest external match to the planned core (independent reviewers then aggregation). Low overlap is expected and is why aggregation raises recall, consistent with E1's low-overlap observation (7 multi-reviewer clusters among 216 findings, `[UNVERIFIED]`). Repeated runs of one model overlap about as little as different models, so a one-model collapse could be partly offset by repeated runs; that comparison was not run in the codebase. Aggregation there uses an LLM call, not citation verification.

**Finding:** [EXTERNAL] [D2] GitHub ReviewBench: 219 PRs from 187 repositories in 19 languages (vendor figures). Golden set built from human reviewers, follow-up commits, deterministic tools and multiple frontier LLMs across model families, then semantically deduplicated so that agreement across producers does not inflate it. Six metrics: grounded and augmented precision, recall and F1 (augmented credits valid findings absent from the golden set, LLM-judged). Senior engineers re-labelled the golden set with 96.6% agreement (vendor figure). The vendor says a lite-tier multi-model ensemble was predicted to raise precision, recall and comment volume while lowering cost per review (no numbers in the extracted text). A commenter notes leaderboard rows are best runs, hiding spread across runs (low reliability).
**Source:** https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review ; commentary https://www.linkedin.com/posts/github_reviewbench-an-open-benchmark-for-ai-code-activity-7513480739162677250-JNli. Reliability: vendor engineering blog (not peer-reviewed); LinkedIn is low reliability.
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-01 D2) E1's never-run seeded-defect design with a second measurement style (real PRs, deduplicated golden set). Its rule "semantic dedup without letting agreement inflate" matches the planned cluster-duplicates step as handed in.

**Finding:** [EXTERNAL] [D3] LangChain's ReviewBench (a different artifact from GitHub's, a 59-task benchmark): with a minimal harness the strongest runs recover only about 30% of baseline issues; narrow review strategies lower cost but hurt coverage; scoring is an LLM verifier against a curated baseline with F1 headline. Entelligence built a golden set with three frontier models reviewing independently, a separate GPT-4o call as arbiter keeping comments flagged by 2 of 3 (single-model comments discarded), then human validation: a majority-vote rule applied to findings.
**Source:** https://www.langchain.com/blog/evaluating-code-review-agents-with-reviewbench ; https://entelligence.ai/code-review-benchmark-2026. Reliability: vendor blogs (not peer-reviewed).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-01 D3). The 2-of-3 rule discards single-reviewer findings and directly conflicts with the union approach in D1; which is right depends on whether the goal is precision of a ground truth (Entelligence) or recall of a review (D1). The "one valid reviewer passing" behaviour pinned at `tests/review/test_review_ledger.py:376-385` (per the task, as handed in) corresponds to the permissive end. The planned core's choice for single-reviewer findings is a design option these sources do not settle.

**Finding:** [EXTERNAL] [D4] c-CRAB code review benchmark: automated review tools pass 20.1% to 32.1% of tests built from human reviews, humans 100%; the union of four tools passes 97 of 234 tests (41.5%); agent reviews often consider different aspects than human reviews.
**Source:** https://arxiv.org/html/2603.23448v2. Reliability: arXiv preprint.
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-01 D4) as a limit: even a union of LLM reviewers leaves a large gap to human review, so a panel should not be described as a full replacement for human review or a test gate. Relevant to the rf-qa replacement goal as a limit on claims.

**Finding:** [EXTERNAL] [D5] A practitioner note suggests self-consistency over N samples as a cheap signal (inconsistent findings on the same diff correlate with false positives in production, claimed without cited evidence), treating disagreement between a cheap and a frontier reviewer as a signal worth surfacing, and three-tier labels (hard reject, soft reject, accept) for precision at different strictness.
**Source:** https://prakharsingh.github.io/notes/evaluating-llm-code-reviewers. Reliability: personal blog (lowest tier); claims are unsupported opinion.
**Relevance:** LOW
**Relationship to codebase:** extends (web-01 D5): suggests keeping reviewer disagreement as data rather than discarding it, and a three-way finding label for the quality measurement.

#### 5.1.5 Measuring agreement and judge reliability

**Finding:** [EXTERNAL] [AE-1] Raw agreement overstates reliability. "Reliability without Validity" (21 judges, 3 benchmarks, about 541,000 judgments): raw agreement overstates chance-corrected discrimination by 33-41 percentage points in all 21 judges; judge rankings shift by up to 14 positions across benchmarks; test-retest reliability above 0.95 coexists with severe position bias (above 0.10) in two production judges ("test-retest measures stability, not correctness"); verbosity bias was small (below 0.011) under one pairwise rubric, in contrast to the 2023 literature. "Rating Roulette": judges are self-inconsistent across runs; Krippendorff's alpha over 3 runs is 0.33 (Llama 3.1), 0.63 (DeepSeek-R1), 0.79 (Qwen-3) on SummaC; up to 5 runs did not change self-reliability. Blogs recommend reporting chance-corrected agreement (Cohen's kappa for 2 raters, Fleiss' kappa or Krippendorff's alpha for 3 or more or missing data) beside raw agreement; the same kappa (0.667) reads as "substantial", "moderate" or "tentative" depending on the scale (Kili); McHugh is quoted as calling kappa below 0.60 inadequate (HoneyHive).
**Source:** https://arxiv.org/html/2606.19544v1 ; https://arxiv.org/html/2510.27106v1 ; https://kili-technology.com/blog/inter-rater-reliability ; https://arize.com/blog/measuring-human-llm-judge-alignment ; https://www.honeyhive.ai/learn/inter-annotator-agreement. Reliability: two arXiv preprints (peer review not confirmed; 2606.19544 carries a mid-2026 id); three vendor blogs (lowest tier).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-01 AE-1). E1's quality measurement and E2's blind-judge scoring both need an agreement statistic. Reviewers do not label a fixed item set, so kappa and alpha apply only after findings are clustered into shared items or after reviews are scored against the 16-defect ground truth; that application is the web researcher's inference, not stated in the sources. Verdict stability across reruns should be measured separately from correctness.

**Finding:** [EXTERNAL] [AE-2] Position bias is judge-dependent and task-dependent. A systematic position-bias study: bias varies by judge and task, is weakly influenced by prompt length but strongly affected by the quality gap between candidates; more capable models (GPT-4o, Claude-3.5-Sonnet) stay consistent from pairwise to list-wise comparison, GPT-3.5-Turbo is more sensitive to more candidates. A code-judge paper (first systematic study of LLM code evaluators under semantically equivalent but superficially different code) defines six bias types and positive/negative bias. Blog surveys (second-hand): swapping the order of good and bad code changed judgments by up to 14%; detecting functional bugs without execution is a major weakness; hallucinating a missing requirement or nonexistent bug is the most common reason for rejecting valid code; swap consistency across 15 judge models ran from 70.5% to 77.3% (cites arXiv 2406.07791, not opened).
**Source:** https://aclanthology.org/2025.ijcnlp-long.18.pdf ; https://aclanthology.org/2026.findings-eacl.70.pdf ; https://medium.com/softtechas/utilising-llm-as-a-judge-to-evaluate-llm-generated-code-451e9631c713 ; https://ai-tldr.dev/learn/evaluation-safety/llm-as-judge/llm-judge-biases. Reliability: two peer-reviewed ACL Anthology papers (read via search excerpts only); the two blogs are lowest tier with second-hand numbers.
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-01 AE-2) A1 and A4 to code, and partly contradicts the 2023 verbosity-bias evidence (AE-1 found it much reduced), so a verbosity guard is a cheap precaution rather than a proven need. Two usable points per web-01: randomise or swap the order of reviewers' findings in a merge or judging prompt; a judge that sees only the diff with no execution is weak on functional bugs, which supports requiring cited evidence from the repository.

#### 5.1.6 Verification of reviewer findings (grounding and citation checks)

**Finding:** [EXTERNAL] [G1] "Citation-Grounded Code Comprehension": a mechanical check that every cited code location overlaps context actually supplied flagged about 8% of responses as hallucinated. Manual review of a sample (31 of 32 examined flags) confirmed 97% were genuine and found zero false negatives among the 92% passing responses (the paper calls this 100% precision and 97% recall on its sample). Hallucinated citations were fabricated locations or wrong line numbers, off by 10-50 lines. The authors say a passing citation proves only that the cited code existed in context, not that the claim about it is right.
**Source:** https://arxiv.org/html/2512.12117v1. Reliability: arXiv preprint (peer review not shown).
**Relevance:** HIGH
**Relationship to codebase:** supports (web-01 G1) the planned "verify citations" step as a cheap non-LLM filter, and fits Kohli (5.1.2 B3): evidence tied to code is stronger than a second LLM opinion. The passing-citation limit should be kept in the verdict design. The codebase mechanics of the citation check were not given to the web researcher and are `[UNVERIFIED]` here.

**Finding:** [EXTERNAL] [G2] Two-pass detect-then-filter patterns and "AI opinion is not evidence". G-Research split recall and precision into separate prompts (first pass captures everything, second filters) after single-pass reviews showed two or three false positives in eight findings. Evolink and Tomosu both say a second LLM judging comment wording is not verification; evidence is code, a documented default, a test or a trace. Augment Code's guide cites a CodeRabbit field study (July 2026) tracing 10.3% of false positives to missing visibility into other files. MegaLens: two models from different companies checked 20 findings; of 16 they agreed on, 9 were real and 7 not (about 44% false positives among agreed findings), and none of 9 "critical" labels were rated critical by both (self-described sample of 20, no human review, admitted wide error bar; read as a warning only).
**Source:** https://www.gresearch.com/news/building-a-code-review-tool-the-llm-patterns-that-actually-work ; https://evolink.ai/blog/ai-code-review-false-positives ; https://tomosu.ai/blogs/ai-code-review-false-positives-reliability-findings.html ; https://megalens.ai/research/ai-code-review-false-positives ; https://www.augmentcode.com/guides/ai-code-review-accuracy. Reliability: vendor and practitioner blogs (lowest tier).
**Relevance:** LOW
**Relationship to codebase:** extends (web-01 G2); consistent with, not proof of, the codebase's design. Agreement between model reviewers is weak evidence a finding is real (anecdotal; consistent with Kohli B3), which argues against treating 2-of-3 agreement as validation. Severity labels across reviewers were inconsistent in that sample, relevant to any severity-based verdict threshold. Hypotheses to test with E1's seeded-defect run.

#### 5.1.7 Quorum, verdict and aggregation rules

**Finding:** [EXTERNAL] [F1] "Vibe Coding on Trial" (unanimous LLM juries): 15 open models benchmarked on 82 MySQL text-to-SQL prompts with execution-based ground truth. Unanimous committees of size 1 to 6 built from the six best models accept a candidate only when every member says it is correct. Single-model judges are uneven; small unanimous committees of strong models cut false accepts while still passing many good queries; composition matters significantly. Metrics: TPR, FPR, Youden's J (TPR minus FPR). A secondary summary (emergentmind, not verified in the primary text) says the best committees were 3 to 4 strong LLMs with Youden's J about 0.52 and that composition matters more than size past basic thresholds.
**Source:** https://arxiv.org/abs/2602.18492 (HTML https://arxiv.org/html/2602.18492v2, v1 https://arxiv.org/html/2602.18492v1); venue per https://github.com/abdullazada-mustafa/llm-jury-sql ; secondary https://www.emergentmind.com/topics/multi-llm-jury-protocol. Reliability: conference paper (ICSC 2026 per a repository README citation; not checked at the venue).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-01 F1); does not contradict the code. It is the strict end of the verdict-rule spectrum (accept only when all agree); the current one-valid-reviewer-passes behaviour (`tests/review/test_review_ledger.py:376-385`, per the task) is the permissive end. It gives a measurable comparison (TPR and FPR of each rule against a labelled set), which E2's 16-defect ground truth could provide. Task is single-answer SQL correctness, so transfer to a multi-finding review verdict is `[UNVERIFIED]`.

**Finding:** [EXTERNAL] [F2] Practitioner guidance on verdict rules: Splunk suggests majority vote for binary pass/fail, max pooling (any judge says pass gives pass) when recall has priority, mean for ordinal scales, three judges as the minimum for meaningful aggregation, five judges to separate "5 of 5" from "3 of 5", and mixed model families. Emergentmind lists unanimity (AND), majority, weighted average, dynamic selection and sequential tie-breaker rules. Neither gives measurements for code review.
**Source:** https://www.splunk.com/en_us/blog/learn/tuning-llm-judges.html ; https://www.emergentmind.com/topics/multi-llm-jury-protocol. Reliability: vendor blog and aggregator (lowest tier).
**Relevance:** LOW
**Relationship to codebase:** extends (web-01 F2): names the options the unified panel must choose between (any-pass, majority, unanimity, weighted) without evidence for which fits PR review. With 2-3 reviewers a majority rule has only 2-of-3 granularity; Splunk's five-judge remark suggests 3 reviewers give coarse confidence levels.

**Finding:** [EXTERNAL] [F3] Aggregation cannot fix correlated judges. CARE (Confounder-Aware Aggregation) models judge scores as a latent true-quality signal plus shared confounders such as verbosity and style, because majority vote or averaging "provide little gain or even amplify systematic mistakes" when judges share confounders. SkillAggregation and Dawid-Skene weight judges by estimated reliability; SkillAggregation reports its largest gains over majority voting when a majority of judges are good and a couple are bad. Dependence-aware (Ising) aggregation is listed as outperforming majority vote and Dawid-Skene (secondary summary). AWS blog figures (CARE up to 26.8% error reduction; a two-phase "reasoning jury" with a blind moderator +12 F1 points at 8-16% extra cost) are blog claims, unverified in the primary papers.
**Source:** https://arxiv.org/html/2603.00039v1 ; https://builder.aws.com/content/3JbMv6rSHOq4TA8stg8pevGzupx/aggregation-methods-for-llm-as-a-judge ; https://www.emergentmind.com/topics/llm-as-a-judge-implicit-aggregation ; https://aclanthology.org/2025.acl-long.756.pdf. Reliability: arXiv preprint (CARE), ACL 2025 paper (excerpt only), AWS community blog and aggregator (lowest tier).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-01 F3) Kohli (5.1.2 B3) with remedies. Weighted or dependence-aware aggregation needs labelled data to estimate per-reviewer reliability, which is what the unrun E1 seeded-defect measurement would produce; before that data exists, equal-weight rules are the only option that does not rest on assumptions about reviewer reliability.

**Merge and verdict rules seen in external sources (comparison, from web-01):**

| Rule | Where it appears | Effect on single-reviewer findings | Evidence quality | Corresponding codebase behaviour as handed in |
|---|---|---|---|---|
| Union with semantic dedup | SWR-Bench Multi-Review (D1); GitHub ReviewBench golden set (D2) | Kept | Preprint / vendor blog; recall gain F1 up to +43.67% (D1) | Not stated by web-01 |
| 2-of-3 majority on findings | Entelligence golden set (D3) | Discarded | Vendor blog | Opposite of the permissive behaviour |
| Unanimous (AND) acceptance | Ullah and Serwadda (F1) | n/a (accept/reject of a candidate) | Conference paper, single-answer SQL task | Strict end of the spectrum |
| Any-pass / max pooling | Splunk guidance (F2) | n/a | Vendor blog, no measurements | `tests/review/test_review_ledger.py:376-385` one valid reviewer passes (permissive end) |
| Weighted / dependence-aware | CARE, SkillAggregation, Dawid-Skene, Ising (F3) | Depends on estimated reliability | Preprint / ACL paper; needs labelled data | Not present as handed in |

Web-01 states: not found, any peer-reviewed study of heterogeneous multi-reviewer panels for PR code review that compares quorum rules (any-pass, majority, unanimous) on findings with ground truth. The closest are SWR-Bench (D1) and the SQL unanimous-jury paper (F1).

### 5.2 Claude Code hooks and headless semantics

Source file: `research/web-02-claude-code-hooks-headless.md` (its section numbers are cited as "web-02 section N"). Tavily returned query-reranked passages, not full pages, for the official docs, so statements are limited to those passages. Codebase facts handed to the web researcher: E2 collaboration designs r1-r5 assume a per-tool-call hook can publish a reviewer's progress to a board file and that `claude -p` reviewers can be resumed; "hooks fire in `claude -p`" is marked `[UNVERIFIED]` in the brief; `src/superclaude/agents/reflect-reviewer.md` is read-only with an allowlist that has no Bash/Edit/Write/Task; the product path dispatches reviewers through the orchestrator's Agent call by model class. No code was read by the web researcher, so no code discrepancy was found.

#### 5.2.1 Hook events and when PostToolUse fires

**Finding:** [EXTERNAL] `PostToolUse` fires only after a tool call SUCCEEDS; a failed call fires `PostToolUseFailure`. `PostToolBatch` fires after a full batch of parallel tool calls resolves, before the next model call. `SubagentStart` fires when a subagent is spawned, `SubagentStop` when it finishes. `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop` and `SubagentStop` use the top-level decision pattern `decision: "block"` plus `reason`; `SubagentStop` with `decision: "block"` keeps the subagent running and delivers `reason` as its next instruction (a hook that exits 2 delivers stderr the same way). To inject context into the PARENT session after a subagent returns, the docs say to use a `PostToolUse` hook on the `Agent` tool, not `SubagentStop`. Command hooks receive event JSON on stdin; handler types are shell commands, HTTP endpoints, MCP tool calls, LLM prompts and subagents. Only some event rows were in the extracted passages; `SessionStart`, `PreToolUse`, `Stop` rows were not seen, though the decision table names `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `ConfigChange`, `PreCompact`, `TeammateIdle`, `TaskCompleted`.
**Source:** https://code.claude.com/docs/en/hooks (official Claude Code docs, highest reliability).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 1) the E2 r1-r5 assumption at the event level: `PostToolUse` is the documented event for per-tool-call publishing, with the success-only caveat, so a board writer on `PostToolUse` alone misses failed calls. The `PostToolUse`-on-`Agent`-tool pattern is relevant to the product path, where an orchestrator-side hook could observe each reviewer's return without any `claude -p` child process. Says nothing about gateway model ids.

#### 5.2.2 Hooks inside `claude -p` and `--bare`

**Finding:** [EXTERNAL] `--output-format` values: `text` (default), `json`, `stream-json`. The headless page says to add `--bare` in CI so Claude Code starts without loading the host's hooks, plugins, auto memory or `CLAUDE.md`; this implies that WITHOUT `--bare`, `claude -p` loads the host's hooks. In bare mode, hooks still do not run when passed with `--settings`, or via a flag-loaded plugin's `hooks/hooks.json` or `hooks` key ("Don't use bare mode for a run that needs them"). Flags that still load things in bare mode: `--append-system-prompt(-file)`, `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`, `--plugin-url` (but not their hooks). A configured `SessionStart` or `Setup` hook emits `hook_started`, `hook_progress`, `hook_response` events into the `stream-json` stream.
**Source:** https://code.claude.com/docs/en/headless (official docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 2). E2 marks "hooks fire in `claude -p`" as `[UNVERIFIED]`; the official docs support it for the non-bare invocation. A collaboration package that launches reviewers with `--bare` would silently lose its `PostToolUse` board-writer hook even if passed via `--settings`, a failure mode to add to E2's risk list. Docs say nothing about hooks being model-specific, so whether hooks fire for a gateway `--model` id is not answered by official docs.

#### 5.2.3 stream-json shape, `--resume`, `--fork-session`, cost

**Finding:** [EXTERNAL] `stream-json` needs `--verbose` (documented example: `claude -p "..." --output-format stream-json --verbose --include-partial-messages`); each stdout line is one JSON event. The `system/init` event is first (unless startup events precede it) and carries model, tools, MCP servers, loaded plugins and an optional `capabilities` array of strings (for example `interrupt_receipt_v1`) for feature detection. `--output-format json` includes `total_cost_usd` and a per-model cost breakdown; with `--continue` or `--resume` it reports the whole conversation's total; both figures are client-side estimates. `--resume` / `--continue` work in print mode; `--fork-session` creates a new session id. Piped stdin is capped at 10MB. A `claude -p` run does not wait for MCP background work; for other background work it prints `Waiting for background work to finish` to stderr. If the working directory is deleted mid-session the session keeps running and emits a warning in the stream.
**Source:** https://code.claude.com/docs/en/headless ; https://code.claude.com/docs/en/cli-reference (official docs).
**Relevance:** HIGH (stream-json, resume); MEDIUM (cost)
**Relationship to codebase:** extends (web-02 section 3). E2 designs need `--resume` to reopen a reviewer's session across rounds; official docs support `--resume <id>` in `-p` but do NOT state whether a session created under a gateway model id can be resumed or whether session storage is keyed to the model: stays `[UNVERIFIED]` for gateway ids. The `capabilities` array is a probe for transports that must detect hook or resume support at runtime.

#### 5.2.4 Tool restriction flags

**Finding:** [EXTERNAL] `--allowedTools` / `--allowed-tools` lists tools that run WITHOUT a permission prompt; it does NOT restrict availability ("To restrict which tools are available, use `--tools` instead"). `--disallowedTools` / `--disallowed-tools` are deny rules: a bare tool name removes the tool from Claude's context, while a scoped rule such as `Bash(rm ...)` leaves the tool available and denies only matching calls. The extractor stripped wildcard characters from some code spans, so exact globs must be confirmed on the page. `--fallback-model` takes a comma-separated chain tried in order when the primary model is overloaded or unavailable.
**Source:** https://code.claude.com/docs/en/cli-reference (official docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 4). `reflect-reviewer` is read-only via an agent-frontmatter allowlist; web-02 says that allowlist protects the in-session Agent path only, and a `claude -p` reviewer needs its own CLI-level restriction. For no-Bash enforcement on a headless reviewer, use `--tools` or `--disallowedTools Bash`, not `--allowedTools` (a common mistake).

#### 5.2.5 Subagent definitions

**Finding:** [EXTERNAL] Subagent frontmatter has `tools` (allowlist) and `disallowedTools` (denylist); if both are set, `disallowedTools` applies first and `tools` resolves against the remaining pool; a tool in both is removed. An allowlist excludes MCP tools unless listed. A `disallowedTools` entry with a specifier such as `Bash(git push ...)` still removes the WHOLE tool for a subagent (unlike the CLI flag). The `model` field accepts `sonnet`, `opus`, `haiku`, `fable`, a full Anthropic model ID such as `claude-opus-5-5`, or `inherit`; nothing in the passage documents arbitrary gateway model ids. If `Agent` is omitted from `tools`, the agent cannot spawn subagents; the `Agent(agent_type)` allowlist syntax applies only to an agent running as the main thread (`claude --agent`). `permissionMode` in frontmatter is ignored for plugin subagents.
**Source:** https://code.claude.com/docs/en/sub-agents (official docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 5). The docs confirm the reflect-reviewer allowlist (Read, Grep, Glob and search MCP tools; no Bash/Edit/Write/Task) is the supported way to make a read-only reviewer, and omitting `Agent` stops nesting. Web-02 concludes that an E2 r1-r5 design needing the reviewer itself to WRITE to a board conflicts with that allowlist; the write must come from a hook process or the orchestrator. A plugin-shipped subagent cannot set `permissionMode`.

#### 5.2.6 Settings precedence and `--settings`

**Finding:** [EXTERNAL] Managed (organization) settings are top level and cannot be overridden by user, project, local settings, or `--settings`. The command line (`--settings`) "sits above every file except managed" and lasts one session without writing a file, so a per-reviewer `--settings` JSON can override user/project/local files for that process. Some keys do not merge across sources (the whole value comes from the highest source that defines it); array-valued keys such as `availableModels` merge across non-managed scopes, but when managed settings define the list it is applied as-is. NOT CONFIRMED in the retrieved passages: how `hooks` blocks from several sources combine, i.e. whether a `--settings` hooks block replaces or adds to hooks from `~/.claude/settings.json`.
**Source:** https://code.claude.com/docs/en/settings (official docs).
**Relevance:** HIGH
**Relationship to codebase:** supports (web-02 section 6) the E2 design choice of a per-reviewer `--settings` file, with the open replace-versus-add question. In this environment user hooks in `~/.claude/` (freshness, policy hooks) exist, so a `claude -p` reviewer launched without `--bare` would also load those host hooks and their side effects.

#### 5.2.7 `--model` with non-Anthropic gateway ids

**Finding:** [EXTERNAL] `ANTHROPIC_CUSTOM_MODEL_OPTION` adds one custom id to the `/model` picker and skips validation ("any string your API endpoint accepts"); if `availableModels` is set, the custom id must also be in that allowlist or Claude Code "rejects a `--model` selection of it like any other excluded model". `--model` and `ANTHROPIC_MODEL` apply only to the launched session, and the docs say to launch each terminal with its own `--model` to run different models at once. `modelOverrides` keys must be Anthropic ids; an unrecognised id yields a `[claude-code:unrecognized_model]` diagnostic that can be silenced. For a gateway whose model window differs from the built-in size for its name, set `CLAUDE_CODE_MAX_CONTEXT_TOKENS` (v2.1.193 and later). v2.1.126 and later can fill the `/model` picker from the gateway's `/v1/models` with `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` (documented via an official-repo docs issue that says the docs omit it). LiteLLM docs: the `/model` picker keeps only gateway models whose id contains `claude` or `anthropic`, so a non-Anthropic model needs a claude-flavoured id (for example `kimi-k3-claude-compatible`) to appear in the picker while requests use the raw id; this is about the picker, not whether `--model <non-claude-id>` is accepted.
**Source:** https://code.claude.com/docs/en/model-config ; https://code.claude.com/docs/en/env-vars (official); https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models (LiteLLM project docs); https://github.com/anthropics/claude-code/issues/55182 (docs issue in the official repo).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 7). The per-process `--model` supports the E2 pattern of one `claude -p --model <id>` per reviewer. The product path dispatches reviewers through the Agent call by model class, and subagent frontmatter `model` is documented only for aliases and Anthropic ids, so per-reviewer non-Anthropic gateway choice is documented only on the `claude -p --model` side. The session environment is a LiteLLM-style gateway with a claude-flavoured id (`claude-gw-tier1b[1m]`), consistent with the picker note. Hooks and `--resume` behaviour for gateway ids is `[UNVERIFIED]` and needs a local probe.

#### 5.2.8 Field reports on hooks and resume in `claude -p`

All five are GitHub issues in the official repo `anthropics/claude-code`; reliability: user-reported, forum-grade, below the docs. Dates as given in the issue text.

**Finding:** [EXTERNAL] Issue 79702 (opened 2026-07-21, Claude Code v2.1.216, macOS): in print mode `SessionStart` and `Stop` hooks fired but `SessionEnd` did NOT fire on normal exit (project `.claude/settings.json` hooks, no plugins).
**Source:** https://github.com/anthropics/claude-code/issues/79702
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 8): a design that relies on `SessionEnd` to flush a board in `claude -p` is at risk; `Stop` fired. Relates to the E2 `[UNVERIFIED]` "hooks fire in `claude -p`" assumption.

**Finding:** [EXTERNAL] Issue 10373 (date not shown, older): the reporter notes "PreToolUse and PostToolUse hooks work correctly" and that the SessionStart bug "only affects the interactive CLI mode, not `--print` mode". Weak support that `PostToolUse` fires in print mode.
**Source:** https://github.com/anthropics/claude-code/issues/10373
**Relevance:** HIGH
**Relationship to codebase:** supports (web-02 section 8) the E2 assumption for `PostToolUse` on Anthropic-routed runs; the statement may be outdated (date unknown).

**Finding:** [EXTERNAL] Issue 37559 (Mar 2026 per the thread): a user reported no hooks fired in `-p` mode for a `type: "prompt"` hook; a reply said hooks fire in interactive mode "but not consistently in `-p` pipe mode" and recommended `type: "command"` hooks for automation; the reporter asked the docs to state print-mode behaviour. Unresolved in the extract.
**Source:** https://github.com/anthropics/claude-code/issues/37559
**Relevance:** HIGH
**Relationship to codebase:** contradicts the optimistic reading of 5.2.2 (hooks run in print mode) for prompt-type hooks (web-02 section 8); command-type hooks are the safer choice. This is an external-versus-external tension, not a conflict with a code-verified fact.

**Finding:** [EXTERNAL] Issue 9630 (date not shown): a response states "It is intentional that we do not support UserPromptSubmit hooks in non-interactive mode. Prefer SessionStart hooks for non-interactive mode." Possibly outdated for current versions.
**Source:** https://github.com/anthropics/claude-code/issues/9630
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-02 section 8): check before relying on `UserPromptSubmit` in `-p`.

**Finding:** [EXTERNAL] Issues 18311 and 22724 (early 2026): `--resume` problems when `sessions-index.json` is out of sync with the `.jsonl` session files, and a resume failure from orphaned `tool_result` blocks after corrupted history; resuming with an explicit session id worked in one report where `--resume` without an id did not.
**Source:** https://github.com/anthropics/claude-code/issues/18311 ; https://github.com/anthropics/claude-code/issues/22724
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-02 section 8) the E2 resume assumption: a transport should resume by explicit session id, never "most recent". None of the field reports covers a gateway model id.

#### 5.2.9 Hooks inside subagents and hook input fields

**Finding:** [EXTERNAL] "Hooks from settings files, managed policy settings, and plugins also run inside subagents"; when a subagent calls a tool, `PreToolUse` and `PostToolUse` fire the same configured hooks as in the main conversation, with `agent_id` and `agent_type` in the input. Common fields: `session_id`, `transcript_path`, `cwd`, `hook_event_name`. `SubagentStart` adds `agent_id` and `agent_type` (the matcher filters on `agent_type`, the agent name such as `reflect-reviewer`). `SubagentStop` adds `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` (the subagent's own transcript in a nested `subagents/` folder) and `last_assistant_message` (the subagent's final response text); its `transcript_path` is the MAIN session's. Some `SubagentStop` events come from Claude Code's internal agents (for example prompt suggestions), so a hook must filter on `agent_type`. Agent SDK docs: token-level stream events are emitted for the main session only; subagent deltas are not forwarded; complete messages carry `parent_tool_use_id` for attributing output to a subagent; the session id is on the `result` message's `session_id` and on the init system message.
**Source:** https://code.claude.com/docs/en/hooks ; https://code.claude.com/docs/en/agent-sdk/streaming-output ; https://code.claude.com/docs/en/agent-sdk/sessions (official docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 9) the codebase fact that the product path dispatches reviewers through the orchestrator's Agent call. A `SubagentStop` hook with `agent_type` matcher `reflect-reviewer` can capture each reviewer's `last_assistant_message` and `agent_transcript_path` with no `claude -p` child, no `--resume` and no reviewer-side Bash: an official-docs-supported transport for the board idea that does not depend on the two `[UNVERIFIED]` assumptions. Limit: the Agent path runs reviewers on the orchestrator's gateway and model-class mapping, not on a per-reviewer arbitrary gateway id (5.2.7). That hooks are model-independent is an inference from hooks being client-side shell commands; no source reviewed states it.

#### 5.2.10 `--session-id`, `--settings`, `--restricted`

**Finding:** [EXTERNAL] `--session-id <uuid>` uses a specific session id (must be a valid UUID), so an orchestrator can choose each reviewer's session id up front and later `--resume` it by explicit id. `--settings` takes a settings JSON file path or inline JSON (regular file, at most 2 MiB); values override the same keys in the settings files for the session, omitted keys keep their file-based values. `--setting-sources user,project,local` chooses which file sources load. `--restricted` (Claude Code v2.1.248 or later) is for evaluation harnesses: it removes built-in tools that run commands or code and WebFetch unless named in `--tools`, confines file tools to the working directories, loads only managed settings and `--settings`, and refuses `bypassPermissions`.
**Source:** https://code.claude.com/docs/en/cli-reference (official docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-02 section 10). E2's per-reviewer process can pin its session id, removing one output-parsing risk. `--restricted` is the closest official analogue of a read-only reviewer process and an alternative to relying on the agent file's allowlist (which applies only to Agent-tool subagents). The v2.1.248 version gate was not checked against the installed client.

**Open or unconfirmed items (web-02 "Gaps and unconfirmed items"):**

| Item | Status in web-02 |
|---|---|
| Full hook event list and exact `PostToolUse` input schema (`tool_response` shape) | Not in passages retrieved |
| Hook merge behaviour across settings sources | Not confirmed |
| Gateway model id behaviour for hooks, `--resume`, `--session-id`, subagent `model:` frontmatter | Not documented in any source reviewed |
| Dates of issues 9630 and 10373 | Not shown; statements may be outdated |
| Wildcard globs in code spans | Stripped by the extractor; check source pages |
| Official docs content | Passages only, not full pages |

### 5.3 Git branch hierarchy and stacked PRs

Source file: `research/web-03-git-branch-hierarchy-stacked-prs.md` (labels A1 to G3 below are that file's labels). Codebase context handed to the web researcher: the fork `IronbellyOrg/IronClaude` is the only PR target; branches are `feature/*`, `fix/*`, `docs/*` off `integration`; PRs are created by `/sc:pr-submit --monitor 3` with `gh pr create --repo IronbellyOrg/IronClaude`. Research item 2.18 (`research/18-repo-constraints-and-branching.md`) holds the codebase-verified ref-rule test (scratch repository) and **takes precedence** over everything in this subsection. No git command was run by the web researcher. The two names in question are `feat/review-panel` and `feat/review-panel/<name>`.

#### 5.3.1 Ref naming rules and the leaf-versus-prefix conflict

**Finding:** [EXTERNAL] [A1] `git check-ref-format` rules: slash-separated components may not begin with `.` or end with `.lock`; at least one `/` is required unless `--allow-onelevel`; no `..`, no ASCII control characters, DEL, space, `~`, `^`, `:`; no `?`, `*`, `[` (except with `--refspec-pattern`); cannot begin or end with `/` or contain consecutive slashes (exception with `--normalize`); cannot end with `.`; cannot contain `@{`; cannot be the single character `@`; no backslash. The rule list does NOT state the "a name cannot be both a leaf and a prefix of another name" constraint: the command validates one name in isolation, so that conflict is detected only when Git tries to create the ref.
**Source:** https://git-scm.com/docs/git-check-ref-format (official docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-03 A1) item 2.18's framing. `feat/review-panel` and `feat/review-panel/<name>` each pass `check-ref-format` individually; the failure is a ref-store conflict, not a syntax violation. The item 2.18 scratch-repository result (`research/18-repo-constraints-and-branching.md`) takes precedence.

**Finding:** [EXTERNAL] [B1] Loose refs are one file per ref in a (sub)directory under `$GIT_DIR/refs`; `git pack-refs` stores refs in the single flat file `$GIT_DIR/packed-refs`, looked up when a ref is missing from the directory hierarchy, and later updates create new files under `$GIT_DIR/refs`. `refs/heads/<name>` records the tip commit of branch `<name>`. Inference stated in web-03 (not on these pages): `feat/review-panel` is the file `refs/heads/feat/review-panel`, while `feat/review-panel/x` needs `feat/review-panel` to be a directory; a path cannot be both; Git enforces the same rule across loose and packed refs.
**Source:** https://git-scm.com/docs/git-pack-refs ; https://git-scm.com/docs/gitrepository-layout (official docs).
**Relevance:** HIGH
**Relationship to codebase:** supports (web-03 B1) research item 2.18; explains the constraint that `feat/review-panel` and `feat/review-panel/<name>` cannot both exist. Item 2.18's scratch-repo result takes precedence.

**Finding:** [EXTERNAL] [B2] Exact error text for the directory/file conflict, creating the parent after the child exists: `fatal: cannot lock ref 'refs/heads/foo': 'refs/heads/foo/bar' exists; cannot create 'refs/heads/foo'`. Creating the child after the parent exists gives the mirror form (HN thread: `... 'refs/heads/test' exists; cannot create 'refs/heads/test/1'`; oneuptime post: `error: cannot lock ref 'refs/heads/feature/login': 'refs/heads/feature' exists`). General form: `cannot lock ref '<new ref>': '<existing conflicting ref>' exists; cannot create '<new ref>'`; the `error:` or `fatal:` prefix depends on the command (`git branch`, `git checkout -b`, `git fetch`). A Stack Overflow comment confirms the file/directory explanation; the fix is deleting or renaming the conflicting shorter branch. Caveats: seen only in community reproductions on Git 2.39.3 (Apple) and blogs, not the Git manual; wording can vary by Git version and ref backend; the same phrase is also used for stale `.lock` files (`Unable to create '...lock': File exists`), a different cause.
**Source:** https://news.ycombinator.com/item?id=38844343 ; https://oneuptime.com/blog/post/2026-01-24-git-cannot-lock-ref-errors/view ; https://stackoverflow.com/questions/45141188/git-fatal-cannot-lock-ref. Reliability: forum thread corroborated by a blog post and a vendor guide.
**Relevance:** HIGH
**Relationship to codebase:** supports (web-03 B2) the failure expected for `feat/review-panel` versus `feat/review-panel/<name>`. If research item 2.18 recorded different exact wording, that scratch-repo output takes precedence.

**Finding:** [EXTERNAL] [B3] `TRANSACTION_NAME_CONFLICT` is Git's internal error code for failing to create a ref due to a name conflict (example: `A/B` versus `A`); `git fetch` uses it to recommend `git remote prune` for refs deleted on the remote. A Git commit ("refs: return conflict error when checking packed refs", by Ivan Tse, acked by Patrick Steinhardt) fixes the case where the conflicting ref is in packed refs, so the conflict is enforced whether the existing ref is loose or packed.
**Source:** https://stackoverflow.com/questions/10068640/git-error-on-git-pull-unable-to-update-local-ref (quotes the commit message). Reliability: Git commit message quoted in a Stack Overflow answer.
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-03 B3). Deleting the conflicting branch on the fork does not remove a stale remote-tracking ref in a local clone; `git fetch --prune` (or `git remote prune origin`) is needed before creating the other form. Relevant because Orca worktrees and several clones share `origin` (as stated in web-03).

**Finding:** [EXTERNAL] [B4] The same constraint applies to remote-tracking refs: after a remote branch is renamed from `x` to `x/y`, a local fetch fails with `error: cannot lock ref 'refs/remotes/origin/<x>': ... exists; cannot create` because `refs/remotes/origin/x` is still a file; the fix is `git fetch --prune` / `git remote prune origin` or removing the stale ref.
**Source:** https://dev.to/cristiansifuentes/git-remote-ref-lock-errors-advanced-diagnosis-and-recovery-1jmp ; https://medium.com/@nirbhaysingh281/error-cannot-lock-ref-refs-remotes-origin-release-exists-cannot-create-42230d262e23 (paywalled excerpt only). Reliability: blog posts (lower).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-03 B4): practical risk if the review-panel branch is renamed later from `feat/review-panel` to `feat/review-panel/<name>`. No contradiction.

**Finding:** [EXTERNAL] [B5] `--ref-format=files` (loose files plus packed-refs) is the default; `reftable` is the alternative. A blog says Git's `BreakingChanges` document announces reftable as the default for new repositories in Git 3.0 and that reftable does not encode ref names as filesystem paths; gitperf.com says reftable is still marked experimental. UNVERIFIED by the web researcher: whether reftable also removes the leaf-versus-prefix restriction; none of the fetched pages states it, and it must not be assumed.
**Source:** https://git-scm.com/docs/git-refs (official option docs); https://tomodahinata.com/en/blog/git-internals-object-model-refs-index-packfile-guide ; https://gitperf.com/chapter-17.html (blogs).
**Relevance:** LOW
**Relationship to codebase:** extends (web-03 B5): the repo's ref backend is expected to be `files` (default); item 2.18's scratch-repo test (`research/18-repo-constraints-and-branching.md`) takes precedence for actual behaviour.

#### 5.3.2 Naming conventions that avoid the conflict

**Finding:** [EXTERNAL] [C1] Slashes group branches, but a group name cannot also be a branch. Stack Overflow: "Because branches are implemented as paths, you cannot have a branch named 'foo' and another branch named 'foo/bar'." A knowledge-base page recommends dashes between words and slash-separated grouping prefixes (`topic/`, `release/`, `hotfix/`, `wip/`) that can combine (for example `hotfix/42687/buggy-thing`). Several blogs recommend `<type>/<short-hyphenated-description>`, lowercase; none of the excerpts addresses the leaf-versus-prefix conflict. Practical rules derived in web-03 (consistent with the sources, not quoted): (1) a grouping prefix is never itself a branch name; (2) for an umbrella plus per-piece branches use hyphenated siblings (umbrella `feat/review-panel`, pieces `feat/review-panel-<name>`) or an explicit leaf umbrella (`feat/review-panel/main`, `/base` or `/umbrella` with pieces `feat/review-panel/<name>`); (3) decide the layout BEFORE the first push, since renaming leaves stale remote-tracking refs (B4) and any open PR on the old branch name must be re-created or retargeted; (4) never use bare numbers as the leading part.
**Source:** https://stackoverflow.com/questions/273695/what-are-some-examples-of-commonly-used-practices-for-naming-git-branches ; https://idiv-biodiversity.github.io/git-knowledge-base/branch-naming-conventions.html ; blog posts pullpanda.io, deepsource.com, conventionalbranch.org (no URLs given in web-03). Reliability: widely cited forum answer plus a maintained knowledge-base page.
**Relevance:** HIGH
**Relationship to codebase:** extends (web-03 C1). The repo's current one-slash `<type>/<name>` layout (`feature/*`, `fix/*`, `docs/*`) cannot hit the conflict unless a branch is named just `feature`, `fix` or `docs`; it appears only when a second slash level is added under an existing leaf. Item 2.18 takes precedence on what the repo's actual branches are.

#### 5.3.3 GitHub native stacked pull requests

**Finding:** [EXTERNAL] [D1] GitHub stacked PRs (generally available per a changelog dated 2026-10-06): each PR targets the branch of the PR below it, trunk at the bottom. Branch protection (such as CODEOWNER approvals) is enforced on every PR in the stack, and CI triggered by PRs on the default branch runs for all PRs in the stack. Merging is bottom-up only: a contiguous group from the lowest unmerged PR can merge together; a mid-stack PR cannot merge alone; PRs above stay open and auto-retarget to the stack's base. Merge requirements: all PRs below approved with passing checks, linear history, protection requirements met; otherwise a "Rebase stack" button appears (server-side cascading rebase that keeps approvals if the diff is unchanged). Merge commit, squash and rebase are supported; stacks are merge-queue aware; programmatic access via webhooks, REST and GraphQL; CLI extension `gh stack`. Once all PRs in a stack merge, it cannot be extended; new branches pushed with `gh stack submit` start a new stack. Branching stacks retarget automatically when the base branch is deleted. LIMITATION: "Stacked pull requests require all branches to be in the same repository. Cross-fork stacks are not supported." Not supported in GitHub Desktop. Date caution: the feature is new, so behaviour may change.
**Source:** https://docs.github.com/en/pull-requests/get-started/about-stacked-prs ; https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-stacked-pull-requests ; https://github.blog/changelog/2026-10-06-stacked-pull-requests-generally-available (official docs and changelog).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-03 D1). The fork `IronbellyOrg/IronClaude` is the only PR target and branches would be in one repository, so the same-repository rule is satisfied for fork-internal stacks (not verified against the repo's actual PR-creation path). Web-03 did not check whether `/sc:pr-submit --monitor 3` can set a non-default base or create stack links; do not assume `gh stack` can be used from `/sc:pr-submit`; that is a codebase question for research item 2.18 and the pr-submit findings, which take precedence.

**Finding:** [EXTERNAL] [D2] Community reports on rough edges (single-source, unverified): (a) a stack misbehaving when the bottom branch is merged by squash and the stack was created from a not-yet-merged branch, with `gh stack rebase --no-trunk` not recovering; (b) a bug report that the top PR of a squash-merged 3-PR stack went to `REVIEW_REQUIRED` / `DIRTY` after the merge though approved on an unchanged head commit; (c) AlphaSignal (written during the preview, possibly outdated after GA) says squash or rebase default merge settings break stack identity tracking after the first merge and suggests merge commits; (d) diffox.ai says a hand-built chain after a squash needs `git rebase --onto`, and that with a hand-built chain branch protection and CI often trigger only for the bottom PR; (e) dandoescode.com says that even without the stack feature GitHub auto-retargets an open PR to `main` when its base branch is merged and deleted, and that merging stacked PRs one at a time with squash, without tooling, rewrites the base the next PR was built on. (c) and (d) conflict with the GA docs in D1 on whether squash is supported (the docs say it is); web-03 says prefer the docs and test before relying on either.
**Source:** https://github.com/orgs/community/discussions/201439 (comments up to Nov 4, 2026) ; https://alphasignal.ai/news/github-ships-stacked-pull-requests-so-developers-stop-rebasing-branches-manually ; https://diffox.ai/blog/github-stacked-pull-requests ; https://www.dandoescode.com/blog/github-stacked-pull-requests. Reliability: blog posts and a community discussion (lower).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-03 D2). Whether the fork squash-merges was not confirmed in the codebase by the web researcher; if it does, a stack of review-panel PRs needs either GitHub stack tooling or a manual `git rebase --onto` after each lower merge.

#### 5.3.4 Manual stacked-branch practice

**Finding:** [EXTERNAL] [E1] After `feature1` is squash-merged into `master` as a new commit `S`, `feature2` still carries `feature1`'s original commits, which differ from `S`. Recipe: `git rebase --onto master feature1 feature2` (a Stack Exchange comment: the third argument avoids a prior checkout; if `feature1` was deleted, `git rebase --onto master HEAD~1 feature2` works by naming the boundary commit). Nutrient shows `git rebase --onto main A` then `git push --force-with-lease`, after which the PR page shows only changes not in `main`. Reason: plain `git rebase` skips commits already upstream only when patches are identical, so conflict-resolved duplicates survive and conflict repeatedly; `--onto` names the exact boundary. Per dandoescode.com, GitHub re-points an open PR to `main` when its base is merged and deleted; pullnotifier.com recommends the "Automatically delete head branches" setting for stacks; web-03 did not verify these two claims against GitHub's non-stack documentation. The fetched `git-rebase` excerpt did not include the "TRANSPLANTING A TOPIC BRANCH WITH --ONTO" section body, so the recipe rests on community sources.
**Source:** https://git-scm.com/docs/git-rebase (official, option existence) ; https://softwareengineering.stackexchange.com/questions/365658/does-squashing-pull-requests-break-gits-merging-algorithm ; https://www.nutrient.io/blog/how-to-handle-stacked-pull-requests-on-github ; https://mreigen.medium.com/git-rebase-onto-the-trick-i-wish-id-known-for-stacked-pull-requests-275e7a5b661c (excerpt only) ; https://pullnotifier.com/tools/stacked-prs.
**Relevance:** HIGH
**Relationship to codebase:** extends (web-03 E1). Applies if review-panel pieces are stacked by hand under `/sc:pr-submit --monitor 3` (which, per the task context, pushes fixes without asking); a force-push after `--onto` would need its own check, not verified by web-03.

**Finding:** [EXTERNAL] [E2] `rebase.updateRefs` / `--update-refs` for stacks: pullnotifier.com recommends at minimum `git config --global rebase.updateRefs true` so rebasing the top branch of a stack also moves intermediate branch refs; andrewlock.net shows an interactive rebase todo list with `update-ref refs/heads/feature/part-1` lines. Neither page was read in full; the official manual text for the option was not in the excerpt. UNVERIFIED against the official manual.
**Source:** https://pullnotifier.com/tools/stacked-prs ; https://andrewlock.net/working-with-stacked-branches-in-git-part-1. Reliability: blog posts.
**Relevance:** LOW
**Relationship to codebase:** extends (web-03 E2) as a possible low-tooling option for hand-built stacks; none verified. The andrewlock example uses one slash level (`feature/part-1`).

#### 5.3.5 Stacking tools: naming and where they push

**Finding:** [EXTERNAL] [F1] `gh stack` (GitHub CLI extension): install with `gh extension install github/gh-stack`; requires GitHub CLI v2.0+ and Git 2.36+. Commands: `gh stack init`, `add`, `view`, `checkout`, `modify`, `unstack`, plus `push`, `submit`, `rebase`, `sync` in the quickstart and README. `submit` creates each PR with the correct base (first branch targets the trunk, each next the one below). `init` adopts existing branches and uses the default branch as trunk unless `--base` is given. A separate command creates or updates a stack from branch names or PR numbers without touching local tracking state (aimed at jj, Sapling, git-town users). Two release-note entries disagree depending on version: one says the branch-name prefix and `--numbered`/`--prefix` flags were removed so names are used exactly as given (`gh stack add refactor/foo` creates `refactor/foo`); another says `--prefix` is the opt-in. Verify the installed version.
**Source:** https://github.com/github/gh-stack ; https://github.com/github/gh-stack/releases ; https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands ; https://docs.github.com/enterprise-cloud@latest/pull-requests/get-started/stacked-prs-quickstart (official repository and docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-03 F1). The tool takes explicit branch names literally, so a stack such as `feat/review-panel/a`, `feat/review-panel/b` works only if no branch is named `feat/review-panel`; a stack whose bottom branch IS `feat/review-panel` must name its upper layers without a `feat/review-panel/` prefix. Whether `/sc:pr-submit` can drive `gh stack` was not checked.

**Finding:** [EXTERNAL] [F2] Graphite (`gt` CLI): `gt submit` pushes every branch of the stack atomically and creates or updates one PR per branch (`--stack` includes descendants; `gt ss -np` short form), "potentially a temporary base branch for each", so a GitHub setting limiting atomic push size can block large stacks. Graphite REQUIRES the branch protection setting "Dismiss stale pull request approvals when new commits are pushed" to be Disabled; a comparison page adds a second setting to turn off (require approval of the most recent reviewable push) and a price list (free Hobby, $20 Starter, $40 Team per user per month, annual billing) that web-03 did not verify. Graphite supports multiple trunks and merges stacked PRs only into their trunk. A Semgrep dev.to guide reports a CI check can prevent merging a PR before its lower PRs have merged.
**Source:** https://graphite.com/docs/github-configuration-guidelines ; https://graphite.com/docs/create-submit-prs ; https://graphite.com/docs/command-reference ; https://graphite.com/docs/multiple-trunks ; https://www.learncursor.dev/compare/github-stacked-prs-vs-graphite-vs-origin (third-party, lower) ; https://dev.to/semgrep/a-guide-to-using-graphites-stacked-prs-for-github-users-5c47 (blog). Reliability: vendor documentation of a commercial product.
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-03 F2). Adopting it would change fork-level settings (stale-approval dismissal off); web-03 judges it not a fit where review and approvals are bot-driven (Augment and Codex via `/sc:pr-submit`), but did not verify how those bots treat stale approvals.

**Finding:** [EXTERNAL] [F3] ghstack: every local commit becomes its own PR, pushed to three branches `gh/<username>/<n>/base`, `/head`, `/orig`. `base` and `head` are never force-pushed (rebases add merge commits on top of `base`). Because the bases are not `main`, these PRs cannot be merged with the normal GitHub merge button; use `ghstack land <PR URL or #N>` or a bot. A PR is always created in the repository holding the base branch, so branches must be pushed to the upstream repository, leaving stale branches needing separate pruning; branch names carry no PR number. By construction its `<n>/base|head|orig` layout never makes a parent also a branch, so it does not trigger the leaf-versus-prefix conflict.
**Source:** https://github.com/ezyang/ghstack (official repository README).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-03 F3). The "never mergeable via the GitHub merge button" constraint conflicts with the fork's PR path through `/sc:pr-submit --monitor 3` (a codebase fact stated in the task context; not re-verified). Web-03 treats it as a negative fit unless pr-submit research says otherwise.

**Finding:** [EXTERNAL] [F4] git-branchless is a suite of tools (`git undo`, smartlog, `git restack`, `git sync`, `git move`), branch-optional ("100% compatible with branches"). The README excerpt does not describe creating GitHub PRs; olivernguyen.io pairs it with a separate tool `git-pr` that creates one PR per commit and appends a `Remote-Ref:` attribute to each commit message. Benjamin Congdon names ghstack, `epage/git-stack` and Stacked Git as related tools.
**Source:** https://github.com/arxanas/git-branchless ; https://olivernguyen.io/w/stacked.prs ; https://benjamincongdon.me/blog/2021/12/07/Branchless-Git. Reliability: official repository README; blogs for PR creation.
**Relevance:** LOW
**Relationship to codebase:** extends (web-03 F4). No branch-name conflict by design (commit-based); not integrated with `/sc:pr-submit` as far as web-03 knows (not verified).

#### 5.3.6 How reviews and CI treat stacked PRs

**Finding:** [EXTERNAL] [G1] Reviewers see only the diff of their own layer (stack map in the merge box). GitHub's "Rebase stack" retains approvals when the layer's diff is unchanged even with "dismiss stale approvals" on (GitHub docs). With hand-built stacks and Graphite, rebasing the lower layer re-triggers approval dismissal, so Graphite requires the setting off and pullnotifier.com advises disabling it to avoid re-review cascades; pullnotifier.com also advises reviewing bottom-to-top and marking upper PRs as drafts.
**Source:** https://docs.github.com/en/pull-requests/get-started/about-stacked-prs ; https://github.blog/changelog/2026-10-06-stacked-pull-requests-generally-available ; https://pullnotifier.com/tools/stacked-prs ; https://graphite.com/docs/github-configuration-guidelines. Reliability: official docs plus vendor blogs.
**Relevance:** HIGH
**Relationship to codebase:** extends (web-03 G1) the sequence-and-gates inputs: a stack is a way to land a multi-piece unified review panel in dependency order while each piece is reviewed alone, and the lower piece gates the upper under GitHub's bottom-up merge rule. Whether the repo's review bots (Augment, Codex) review against the stack base or `master` is not verified.

**Finding:** [EXTERNAL] [G2] CI: GitHub docs say CI checks triggered by PRs on the default branch run for all PRs in the stack, and branch protection is evaluated against the stack base, not the immediate parent. CircleCI blog: each PR in a stack needs its own validation; updating a lower PR and rebasing those above re-runs pipelines across the stack (four branches can mean four sets of builds); it suggests path filtering, and says that if managing the stack costs more than reviewing one larger PR, keep the change together. diffox.ai reports that for hand-built chains checks "did not run again" after a rebase and the old commit's result was displayed (single-source, unverified). NOT verified: whether GitHub Actions `pull_request` workflows with a `branches:` filter match the PR's BASE branch, so a hand-built stacked PR whose base is another feature branch would not trigger a workflow filtered to `master`/`integration` (only a Stack Overflow snippet hinted at this: https://stackoverflow.com/questions/79292495/trigger-action-on-pull-request-not-working). A 404 on GitHub's "Optimizing CI for stacked pull requests" page meant GitHub's own advice could not be read.
**Source:** https://docs.github.com/en/pull-requests/get-started/about-stacked-prs ; https://circleci.com/blog/stacked-prs-and-ci ; https://diffox.ai/blog/github-stacked-pull-requests. Reliability: official docs; CircleCI vendor blog.
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-03 G2). The codebase's CI workflow triggers are the source of truth; compare them with the above in research item 2.18 / CI findings.

**Source conflicts flagged in web-03 (G3):**

| Claim | Source | Conflicting source | Web-03 resolution |
|---|---|---|---|
| Squash-merge cannot be used on intermediate PRs; GitHub's native merge queue does not handle dependent PR ordering | pullnotifier.com (blog, undated "(2026)" title) | GitHub GA docs (D1): stacks support merge commit, squash and rebase and are merge-queue aware | Blog treated as superseded for native GitHub stacks, still valid for hand-built chains and some third-party tools; prefer the docs |
| Squash or rebase default merge settings break stack identity tracking | AlphaSignal (preview-period blog, D2c) | GitHub GA docs (D1) | Prefer the docs; test before relying on either |

### 5.4 Finding schemas and review bots

Source file: `research/web-04-finding-schemas-review-bots.md` (its section numbers are cited as "web-04 N.N"). Codebase context handed to the web researcher and not re-verified there: the review package has two finding contracts (v1 anchor quotes plus a category set; v2 path:line citations plus an optional lens); `src/superclaude/pr_submit/` has its own severity router and third-party reviewers (Augment, Codex); a future PR-code-review module needs a file-and-line location type. Augment's review output format was not researched (no official source found): a gap.

#### 5.4.1 SARIF 2.1.0

**Finding:** [EXTERNAL] [web-04 1.1] A SARIF `result` carries `ruleId`, `message`, `locations[]`, optional `relatedLocations[]`, `kind`, `level`, `fingerprints`, `partialFingerprints`, `guid`, `correlationGuid`, `baselineState`. `kind` (evaluation state, spec 3.27.9: `notApplicable`, `pass`, `fail`, `review`, `open`, `informational`) and `level` (how bad: `error`, `warning`, `note`) are separate properties. Identity: `guid` identifies the result in one run; `correlationGuid` the equivalence class of logically identical results across runs; `fingerprints` are full stable identities; `partialFingerprints` contribute to identity and are expected to change when surrounding code changes; `baselineState` is `new`, `unchanged`, `updated` or `absent`. Location: `locations[].physicalLocation.artifactLocation.uri` (+ optional `uriBaseId` such as SRCROOT) and `region` (`startLine`, `startColumn`, `endLine`, `endColumn`); per spec 3.29.4, if `region` is absent the physicalLocation refers to the entire artifact (file-level finding).
**Source:** https://sarif.info/Result (secondary explainer, well-maintained) ; https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html (OASIS SARIF 2.1.0 Plus Errata 01, official standard).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-04 1.1). The v2 path:line citation maps to `artifactLocation.uri` + `region.startLine`; the v1 anchor-quote location has no SARIF-native analogue. SARIF separates state (`kind`/`baselineState`) from severity (`level`), matching a panel that needs both severity and verdict/resolution state on one finding.

**Finding:** [EXTERNAL] [web-04 1.2] GitHub code scanning consumes a SARIF subset. Example: `tool.driver.rules[]` with `id`, and rule `properties` keys `kind` (e.g. `path-problem`), `problem.severity` and `security-severity` (numeric string such as `9.8`); results carry `ruleId`, `message.text`, `locations[].physicalLocation` with `artifactLocation.uri` and `region.startLine/startColumn/endColumn`, and `partialFingerprints` with `primaryLocationLineHash` (example `39fa2ee980eb94b0:1`) and `primaryLocationStartColumnFingerprint`. `relatedLocations[]` carry an `id`, location and message. Producer guidance: relative URIs with `uriBaseId: "%SRCROOT%"`.
**Source:** https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support (official GitHub docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-04 1.2). A minimal interoperable location is (relative path, start line, optional end line, optional column), and the dedup fingerprint is a hash of line content plus an occurrence counter, not the line number. The v1 anchor quote is conceptually a content-based fingerprint that survives line drift; a bare path:line citation does not.

**Finding:** [EXTERNAL] [web-04 1.3] The SARIF spec calls for stable fingerprints and has an appendix on fingerprint properties (deterministic computation; incorporate tool name, rule ID and physical location of the target). Vulnerability-management needs (new/unchanged/fixed state, approved suppression, remediation validation) are representable but consumers must still apply them in context; partial fingerprints exist to follow findings through code motion.
**Source:** https://boostsecurity.io/blog/sarif-cant-save-you-now (vendor blog).
**Relevance:** MEDIUM
**Relationship to codebase:** supports (web-04 1.3) keeping finding state across review rounds (ledger) as a layer on top of the finding record rather than inside it.

**Finding:** [EXTERNAL] [web-04 1.4] GitLab ingestion: requires `ruleId` and a physical location (findings without either are not added); severity defaults to `medium` when unset; finding identity = report type + fingerprint of `ruleId` + location fingerprint of the form `file:startLine:endLine`; results in the same file with the same `ruleId` and no `region` collapse into one finding and the rest are silently discarded.
**Source:** https://docs.gitlab.com/user/application_security/detect/sarif (official GitLab docs).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-04 1.4) with a pitfall: if a unified finding record lets `location` be file-only, or lets `category` stand in for a rule id, a downstream consumer can silently dedup distinct findings. Suggests requiring a line (or content anchor) plus a category/rule id on every record meant to be exported.

#### 5.4.2 reviewdog rdjson

**Finding:** [EXTERNAL] [web-04 2.1] rdjson top level: `source {name, url}`, `severity` (default for the set), `diagnostics[]`; rdjsonl is one diagnostic per line. Diagnostic: `message`, `location {path, range {start {line, column}, end {line, column}}}` (end optional), `severity` (`ERROR`/`WARNING`/`INFO`), `code {value, url}`, `suggestions[] {range, text}`. Stated purpose: a generic protocol between diagnostic tools and development tools (editors, reviewdog, code review APIs), with multiline ranged comments, severity, rule code with URL and code suggestions; suggestions are applied only by reporters that support them (github-pr-review, gitlab-mr-discussion, local). reviewdog reporters include `github-pr-review`, `github-pr-check`, `github-annotations`/`github-pr-annotations` and `local`.
**Source:** https://github.com/reviewdog/reviewdog/blob/master/proto/rdf/README.md ; https://github.com/reviewdog/reviewdog (official repository documentation, well-maintained).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-04 2.1). rdjson is the closest existing format to a PR-review finding (path, range, severity, rule code, optional suggested fix) with no confidence, dedup or resolution fields. A shared finding record projectable into rdjson (message, path, line range, severity, code=category) would let a future PR-code-review module reuse reviewdog reporters. Its three-level severity maps one-to-one onto SARIF `error/warning/note`.

#### 5.4.3 GitHub pull-request review comment API

**Finding:** [EXTERNAL] [web-04 3.1] `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments` takes `body`, `commit_id`, `path`, `line`, `side` (`LEFT`/`RIGHT`), optional `start_line` and `start_side`; `position` (lines down from the first `@@` hunk header) is described as "closing down"; 422 on validation failure or if spammed; triggers notifications and can hit secondary rate limits. `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews` takes `commit_id` (not the latest SHA may render comments outdated), `body`, `event`, and `comments[]` each with `path` (required), `body` (required), and `position` or `line`/`side`/`start_line`/`start_side`.
**Source:** https://docs.github.com/rest/pulls/comments ; https://docs.github.com/rest/pulls/reviews (official GitHub REST docs).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-04 3.1). The location type a PR-code-review module needs is `(path, line, side, optional start_line/start_side, commit_id)`. `commit_id` is required context that the v1 anchor and v2 path:line contracts do not appear to carry (not verified against the code): without a commit SHA a line citation is not reproducible against a moving PR head.

**Finding:** [EXTERNAL] [web-04 3.2] User-reported constraints (not official statements): the create-review endpoint returns comment objects in the older position/diff_hunk shape with `line`/`side` null (re-fetching by id returns the line model); one report of a direct single-comment `gh api` call with `start_line`/`start_side`/`line`/`side` returning 422 while the same comment inside a review `comments[]` array worked; comments on lines outside the diff hunks are rejected with 422 `pull_request_review_thread.line is not part of the diff`, although the web UI allows commenting on unchanged lines of changed files (announced Sept 2025) and API support was reported as limited; no API (REST or GraphQL) to append comments to an existing pending review; file-level comments cannot be mixed with line comments inside one review via REST (Oct 2024 answer).
**Source:** https://github.com/orgs/community/discussions/202426 ; https://github.com/cli/cli/issues/13358 ; https://github.com/orgs/community/discussions/187218 ; https://github.com/orgs/community/discussions/168380 ; https://github.com/orgs/community/discussions/143197 (community discussions and issues, lowest tier).
**Relevance:** MEDIUM (forum reports; verify against the current API)
**Relationship to codebase:** extends and constrains (web-04 3.2). A PR-code-review module cannot post a finding whose line is outside the diff, so the finding record needs a "postable versus report-only" distinction (outside the diff degrades to the review body or a file-level comment). The existing fork-only `pr_submit` flow is unaffected (a posting-time constraint).

#### 5.4.4 Severity models in code scanning and review bots

**Finding:** [EXTERNAL] [web-04 4.1] GitHub code scanning has two severity ideas. All alerts have a level of Error, Warning or Note; security alerts additionally carry a security severity Critical/High/Medium/Low derived from a numeric `security-severity` score (0.1-3.9 low, 4.0-6.9 medium, 7.0-8.9 high, 9.0-10.0 critical; 0.0 none; following CVSS), shown in preference to level. PR check failure defaults: security-severity critical or high fails the check; for non-security alerts severity `error` fails; both thresholds are configurable (repository settings or rulesets: "Errors", "Errors and Warnings", "All"; security "High or higher", "Medium or higher", "All").
**Source:** https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts ; https://github.blog/changelog/2021-07-19-codeql-code-scanning-new-severity-levels-for-security-alerts (official); https://safeguard.sh/resources/blog/sarif-security-severity-how-github-maps-scores-to-levels (blog, secondary).
**Relevance:** HIGH
**Relationship to codebase:** extends (web-04 4.1). The standard pattern for a severity router: a coarse 3-level result severity plus an optional finer score, with a configurable gate threshold decoupled from the finding. It parallels the `pr_submit` severity router (fixes confirmed findings of Medium or higher; lower ones only reported, per the repo CLAUDE.md as cited by web-04): the threshold should be configuration over a shared ordinal scale, not a property of the finding record.

**Finding:** [EXTERNAL] [web-04 4.2] CodeRabbit labels a finding with four independent closed vocabularies, explicitly "not one severity ladder": Type (Nitpick, Potential issue, Refactor suggestion); Severity (ranked critical, major, minor, trivial; plus `info` and `none` outside the ranking); Category (six areas: functional correctness, security and privacy, data integrity and integration, performance and scalability, stability and availability, maintainability and code quality); Effort (cost to fix). Overview items carry a priority band p1-p4. Acceptance rate is computed per severity and category as accepted comments / posted comments, where "accepted" means CodeRabbit can verify the feedback was addressed.
**Source:** https://docs.coderabbit.ai/change-stack/findings ; https://docs.coderabbit.ai/guides/code-review-overview ; https://docs.coderabbit.ai/guides/dashboard-metrics (official vendor docs).
**Relevance:** HIGH
**Relationship to codebase:** supports (web-04 4.2). The v1 contract's category set and the v2 contract's optional lens are both "what area" axes; this model confirms severity and category must stay orthogonal and a lens/category is a label, not a filter or a severity. The acceptance-rate metric is resolution-derived and needs a per-finding resolution state in the ledger.

**Finding:** [EXTERNAL] [web-04 4.3] Greptile assigns a 0-5 confidence score per pull request (5 production ready ... 0-1 critical problems), computed from severity and quantity of issues, change complexity and alignment with codebase patterns; inline comments carry severity levels and suggested fixes; a configurable severity threshold filters noise. The vendor states the score is a triage tool, not a rubber stamp. Vendor statistics are vendor-reported.
**Source:** https://www.greptile.com/docs/code-review/first-pr-review ; https://www.greptile.com/agent (official vendor docs) ; https://www.greptile.com/what-is-ai-code-review (vendor marketing).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-04 4.3). For the rf-qa replacement ("checklist-and-confidence model") bot practice puts confidence at the unit-of-review level (PR/document verdict), not per finding; per-finding confidence is not in SARIF or rdjson. Web-04 suggests the finding record stays confidence-free (or carries an optional field) and the verdict record carries confidence.

**Finding:** [EXTERNAL] [web-04 4.4] One evaluation reports GitHub Copilot review surfacing new comments on re-run that did not relate to the latest changes (unstable finding set across runs), and Greptile placing some findings only in the summary rather than inline. Precision and recall figures in a comparison (e.g. Greptile 66.2% precision, Copilot 56.5%) are vendor-reported benchmarks and unverified.
**Source:** https://t2informatik.de/en/blog/how-effective-are-ai-code-reviews (blog) ; https://www.morphllm.com/comparisons/greptile-vs-copilot (vendor comparison).
**Relevance:** LOW
**Relationship to codebase:** supports (web-04 4.4) the need for a stable finding identity (dedup key) across review rounds in the ledger; does not contradict any code finding.

**Finding:** [EXTERNAL] [web-04 4.5] Codex review (a third-party reviewer already used by `pr_submit`): official docs say Codex on GitHub posts a standard GitHub review and flags only P0 and P1 issues, with a `[P1]` title tag plus explanation; repository guidance comes from `AGENTS.md`. A gist reproducing the review prompt defines P0 (drop everything), P1 (urgent), P2 (normal), P3 (low), asks for short line ranges (avoid over 5-10 lines), a numeric `priority` 0-3 (null if unknown) and an "overall correctness" verdict that ignores non-blocking issues. Issue 27691 (user report): when Codex finds an issue it creates a formal `COMMENTED` PullRequestReview with a full `commit_id` and inline comments; when it finds nothing it posts only an issue comment (short SHA in prose) and a reaction, so a clean result cannot be bound to the exact PR head SHA. A third-party action (`gersmann/codex-review-action`) skips findings whose line is not in the current diff and on re-runs does semantic dedup against prior unresolved comments, reporting new and still-relevant prior findings separately.
**Source:** https://learn.chatgpt.com/docs/third-party/github (official OpenAI docs) ; https://gist.github.com/cbh123/ce4893a10ed2b87a89d9114b08118a08 (secondary copy of codex-rs/core/review_prompt.md; the prompt may have changed) ; https://www.cubic.dev/blog/codex-code-review ; https://www.qodo.ai/glossary/what-is-codex-code-review (competitor blogs) ; https://github.com/openai/codex/issues/27691 (issue on the official repo).
**Relevance:** HIGH
**Relationship to codebase:** extends and partly contradicts an assumption (web-04 4.5). Codex uses a 4-step P0-P3 ordinal and shows only P0/P1 on GitHub, CodeRabbit uses critical/major/minor/trivial/info, SARIF uses error/warning/note, so the in-repo `pr_submit` severity router must normalise at least three vendor vocabularies (and Augment's, not researched) onto one internal ordinal; a unified record's `severity` should be that ordinal with the vendor label kept as an opaque string. The "overall correctness verdict" is a verdict-level record separate from findings, matching the planned cluster/verdict/ledger split. The clean-result-has-no-SHA gap is a reason for the ledger to record the reviewed head SHA itself.

#### 5.4.5 Resolution, suppression and dedup vocabularies

**Finding:** [EXTERNAL] [web-04 5.1] Resolved state lives on the review thread, not the comment. User-reported (no official GraphQL reference page was fetched): resolving a conversation uses the GraphQL mutations `resolveReviewThread` and `unresolveReviewThread` with a thread node id (`PRRT_...`) from `reviewThreads.nodes[].id`; `isResolved` is a thread field; replies use `addPullRequestReviewThreadReply`; REST does not return thread node ids. Reports say a Copilot coding agent's `GITHUB_TOKEN` could not call `resolveReviewThread` and that Copilot re-review leaves earlier comments behind (feature request to mark them outdated or dismiss).
**Source:** https://github.com/cli/cli/issues/12419 ; https://github.com/orgs/community/discussions/19206 ; https://github.com/orgs/community/discussions/196714 ; https://github.com/orgs/community/discussions/187953 (forum-level).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-04 5.1) and matches the CLAUDE.md description of `/sc:pr-submit` (replies to and resolves review comments it fixed): the unit of resolution is a thread id, so a ledger row for a PR finding needs a `thread_id` (and comment id) in addition to path and line.

**Finding:** [EXTERNAL] [web-04 5.2] GitHub code scanning alert state is `open` or `dismissed`; `dismissed_reason` is required when dismissed and is one of `false positive`, `won't fix`, `used in tests`, `mitigated` (or null); `dismissed_comment` is free text. The alert response shows `rule {id, severity, tags, description}`, `tool {name, guid, version}`, and `most_recent_instance {ref, commit_sha, message, location {path, ...}}`, so an alert is a rule-level object with per-commit instances.
**Source:** https://docs.github.com/rest/code-scanning/code-scanning (official GitHub REST docs).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-04 5.2). A small closed resolution vocabulary with a mandatory reason when closing without a fix is a model for the ledger's disposition field (for example fixed, rejected as false positive, accepted as won't-fix). The alert/instance split mirrors the cluster/finding split in the planned shared core.

**Finding:** [EXTERNAL] [web-04 5.3] A SARIF `suppression` object has a `kind` (`inSource`, a syntactic construct in the code, or `external`; only `inSource` text was seen) and, per the standard's rationale, `suppressions` is either null for all results or non-null for all results in a run. `baselineState` records state against a previous run (`new`, `unchanged`, `updated`, `absent`). Per the standard, `kind` defaults to `fail` and any `level` other than `none` requires kind `fail`. The `dismiss-alerts` action maps SARIF suppressions to GitHub alerts by rule id + file + line + column and dismisses with reason `won't fix` and comment `Suppressed via SARIF`.
**Source:** https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html (official standard) ; https://github.com/advanced-security/dismiss-alerts (GitHub-maintained action repository).
**Relevance:** MEDIUM
**Relationship to codebase:** extends (web-04 5.3). Suppression is a property of the result and cross-run state is a separate property; the planned ledger can adopt the same split (decision with who/why, state versus previous round). The identity key used by interop tooling is rule id + file + line + column, again an argument for a location with a line and an id-like category on every exported finding.

**Finding:** [EXTERNAL] [web-04 5.4] Cross-round dedup and carry-forward in bots: a third-party action passes prior unresolved comments to the model so it avoids reposting them, then asks separately which prior comments are still relevant, reports new and still-relevant counts separately, and deletes its own prior summary comment on each run. A blog evaluation observed Copilot re-runs surfacing comments unrelated to the latest changes.
**Source:** https://github.com/marketplace/actions/codex-code-review-actor (third-party GitHub Marketplace listing; not official) ; https://t2informatik.de/en/blog/how-effective-are-ai-code-reviews (blog).
**Relevance:** MEDIUM
**Relationship to codebase:** supports (web-04 5.4) adding a per-finding `status` across rounds (new, carried, resolved, superseded) in the ledger rather than treating each round as a fresh finding list.

**Minimal interoperable finding record (web-04 section 6; a synthesis by the web researcher from sections 1 to 5, not a quoted standard):**

| Field | Evidence for needing it | Web-04 section |
|---|---|---|
| stable id (rule/category id plus per-finding id) | SARIF `ruleId`, `guid`; rdjson `code.value`; GitLab and GitHub require a rule id to ingest or dedup | 1.1, 1.4, 2.1 |
| location: repo-relative path, start line, optional end line, optional column | SARIF `region`; rdjson `range`; PR API `path`/`line`/`start_line` | 1.2, 2.1, 3.1 |
| location side and commit SHA (only for PR posting) | PR API `side`, `commit_id`; Codex issue about SHA binding | 3.1, 4.5 |
| content anchor or fingerprint (survives line drift) | SARIF `partialFingerprints.primaryLocationLineHash`; v1 anchor quote | 1.2 |
| message | present in every format | 1.1, 2.1, 3.1 |
| severity as a small ordinal (3-4 levels) plus optional vendor label | SARIF `level`; rdjson ERROR/WARNING/INFO; Codex P0-P3; CodeRabbit 4+2 levels | 2.1, 4.1, 4.2, 4.5 |
| category/lens kept separate from severity | CodeRabbit four independent axes; SARIF rule tags | 4.2 |
| tool/reviewer identity | SARIF `tool.driver`; rdjson `source`; alert `tool` | 1.2, 2.1, 5.2 |
| optional suggested fix | rdjson `suggestions`; GitHub suggestion blocks | 2.1 |
| state/disposition outside the finding (ledger): status versus baseline, dismissal reason, thread id | SARIF `baselineState`/`suppressions`; code scanning `dismissed_reason`; GraphQL thread id | 5.1, 5.2, 5.3 |
| confidence at verdict level, not per finding | Greptile PR-level 0-5 score; Codex overall correctness verdict; no per-finding confidence in SARIF or rdjson | 4.3, 4.5 |

Web-04 reports not found in any source: a standard per-finding confidence field, and a standard "quote anchor" location type; both are the project's own extensions (the v1 anchor quote is closest to SARIF `region.snippet` plus a fingerprint, but `snippet` was not verified).

**Vocabulary comparison (web-04 4.1, 4.2, 4.5, 2.1, 1.1):**

| Source | Severity vocabulary | Gate or display note |
|---|---|---|
| SARIF / code scanning `level` | error, warning, note (and none) | Numeric `security-severity` 0.1-10.0 maps to low/medium/high/critical; gate is a configurable threshold |
| reviewdog rdjson | ERROR, WARNING, INFO | Maps one-to-one onto SARIF levels |
| CodeRabbit | critical, major, minor, trivial (plus info, none); p1-p4 on overview items | Severity, category, type, effort are independent axes |
| Codex on GitHub | P0, P1, P2, P3 (numeric priority 0-3) | Only P0 and P1 shown on GitHub |
| Greptile | per-PR confidence 0-5; inline severity levels | Configurable severity threshold |
| Augment | not researched | Gap (web-04 section 7) |

**Web-04 caveats (section 7):** GitHub PR API behaviours in 5.4.3 (web-04 3.2) and 5.4.5 (web-04 5.1) come from forum or issue reports, not official docs, and the API changes (the `X-GitHub-Api-Version: 2026-03-10` header appears in current official examples), so re-verify before design depends on them. Vendor statistics are vendor-reported and not used as design evidence. The SARIF `level` value `none` and the `kind` value list were read from the OASIS text and sarif.info; the full `suppression.kind` and `baselineState` tables were only partly visible.

### 5.5 External Research Summary

#### Key takeaways (external context only)

| # | Takeaway | Subsection | Relevance | Relationship to codebase |
|---|---|---|---|---|
| 1 | Judge biases (position, verbosity, self-preference) are documented; standard remedies are order swapping or randomisation, ground-truth grounding and not letting a model judge its own family's output. Verbosity bias appears much smaller in recent judges. | 5.1.1, 5.1.5 | HIGH | supports E2 blind judging; extends |
| 2 | Cross-family panels beat a single large judge on QA-style tasks (B1), but errors stay correlated across providers (B2) and 9 judges from 7 families gave about 2 independent votes (B3). Transfer to code review is `[UNVERIFIED]`. | 5.1.2 | HIGH | supports and partly contradicts the independent-opinions assumption |
| 3 | Independent review plus aggregation is a sound default; debate adds little over voting on benchmark tasks. | 5.1.3 | HIGH | supports E2 independent-then-merge |
| 4 | For code review, aggregating several independent reviews raises recall (SWR-Bench F1 up to +43.67%) because reviewers and runs flag largely different change-points. | 5.1.4 | HIGH | supports union merge |
| 5 | Merge and verdict rules in use are opposed (union, 2-of-3 majority that discards single-reviewer findings, unanimity, any-pass); no study compares them on findings with ground truth. | 5.1.4, 5.1.7 | HIGH | extends; design choice not settled by external sources |
| 6 | Agreement must be reported chance-corrected; judge stability across reruns is not correctness. | 5.1.5 | HIGH | extends E1/E2 measurement |
| 7 | Cheap non-LLM verification (mechanical citation check) separated hallucinated from genuine citations on one sample; a passing citation proves existence in context, not correctness. A union of automated reviewers still falls well short of human review (c-CRAB 41.5%). | 5.1.6, 5.1.4 | HIGH / MEDIUM | supports citation verification; limits replacement claims |
| 8 | `PostToolUse` fires only on success; hooks load in `claude -p` unless `--bare`; `--bare` drops hooks even when passed via `--settings`. | 5.2.1, 5.2.2 | HIGH | extends E2 `[UNVERIFIED]` assumption |
| 9 | Field reports: `PostToolUse`, `Stop`, `SessionStart` command hooks worked in print mode; `SessionEnd`, `UserPromptSubmit` and prompt-type hooks were unreliable or unsupported. | 5.2.8 | HIGH / MEDIUM | supports (partly) and cautions |
| 10 | Hooks also run inside Agent-tool subagents with `agent_id` / `agent_type`; `SubagentStop` exposes `last_assistant_message` and `agent_transcript_path`, so the product Agent-dispatch path can be observed without `claude -p`. | 5.2.9 | HIGH | extends product-path dispatch |
| 11 | `--allowedTools` only pre-approves; availability uses `--tools`, `--disallowedTools` or `--restricted`; the agent-frontmatter allowlist covers only the Agent path. | 5.2.4, 5.2.5, 5.2.10 | HIGH | extends reflect-reviewer restriction |
| 12 | Gateway model ids: `--model` is per-process; hooks, `--resume`, `--session-id` and subagent `model:` behaviour for gateway ids are not documented anywhere reviewed. | 5.2.7 | HIGH | `[UNVERIFIED]` for gateway ids |
| 13 | `feat/review-panel` and `feat/review-panel/<name>` pass `check-ref-format` individually but cannot coexist (loose or packed, local or remote-tracking); item 2.18's scratch-repo test takes precedence. | 5.3.1 | HIGH | supports / extends item 2.18 |
| 14 | GitHub native stacked PRs are generally available (2026-10-06), same-repository only; merge is bottom-up; hand-built stacks after a squash need `git rebase --onto` plus `--force-with-lease`; ghstack and Graphite have repository-level costs. | 5.3.3 to 5.3.6 | HIGH / MEDIUM | extends; `/sc:pr-submit` capability unchecked |
| 15 | SARIF, rdjson and the GitHub PR comment API share a minimal location (repo-relative path, line, optional range); content fingerprints survive line drift; severity is a small ordinal separate from category; confidence sits at verdict level; resolution state is separate with a closed vocabulary. | 5.4 | HIGH | extends v1/v2 contracts, `pr_submit` router and ledger |

#### Coverage of every web file's Key External Findings and Recommendations (check required by the task)

Each item is either represented in the subsection shown or explicitly excluded. Recommendations are listed as the web researchers stated them (options from external research); they are not adopted here, because this section is report-only (no roadmap, plan or risk register).

| Web file | Item | Where represented | Status |
|---|---|---|---|
| web-01 | Key finding 1 (judge biases, remedies) | 5.1.1, 5.1.5 | Included |
| web-01 | Key finding 2 (diverse panel beats single judge) | 5.1.2 B1 | Included |
| web-01 | Key finding 3 (correlated errors, at most 11% gap closed) | 5.1.2 B2, B3 | Included |
| web-01 | Key finding 4 (independent review plus aggregation; debate adds little) | 5.1.3 C1 | Included |
| web-01 | Key finding 5 (SWR-Bench recall gain, union merge) | 5.1.4 D1 | Included |
| web-01 | Key finding 6 (opposed merge rules; no evidence on which fits) | 5.1.4 D2, D3; 5.1.7 F1 and rule table | Included |
| web-01 | Key finding 7 (chance-corrected agreement; stability is not correctness) | 5.1.5 AE-1 | Included |
| web-01 | Key finding 8 (non-LLM verification; citation limit) | 5.1.6 G1, G2 | Included |
| web-01 | Key finding 9 (union still short of human review) | 5.1.4 D4 | Included |
| web-01 | Rec 1 (keep independent per-model review plus merge; no debate stage) | 5.1.3 C1 | Included as source option |
| web-01 | Rec 2 (measure diversity; fix collapse or repeat runs; do not call a panel diverse unless distinct models ran) | 5.1.2 B1, B2, B3; 5.1.4 D1 (Self-Agg) | Included as source option |
| web-01 | Rec 3 (agreement as prioritisation, not proof; citation verification) | 5.1.2 B3; 5.1.6 G1, G2 | Included as source option |
| web-01 | Rec 4 (choose verdict rule by measurement; TPR/FPR/Youden's J; chance-corrected agreement; per-reviewer variance) | 5.1.7 F1; 5.1.4 D2; 5.1.5 AE-1 | Included as source option |
| web-01 | Rec 5 (state the one-valid-reviewer-passes rule as permissive with unknown false-accept rate; keep single-reviewer findings as unconfirmed) | 5.1.4 D1, D3; 5.1.7 rule table | Included as source option |
| web-01 | Rec 6 (randomise or swap order; hide majority or authority cues; blind judge to model identity) | 5.1.1 A1, A4; 5.1.5 AE-2 | Included as source option |
| web-01 | Rec 7 (down-weight a reviewer from the code author's model family) | 5.1.1 A2 | Included as source option; web-01 labels it a precaution |
| web-01 | Rec 8 (do not claim replacement of human or test-based review) | 5.1.4 D4 | Included as source option |
| web-01 | Rec 9 (defer weighted aggregation until labelled data exists) | 5.1.7 F3 | Included as source option |
| web-02 | Key finding 1 (`PostToolUse` success only) | 5.2.1 | Included |
| web-02 | Key finding 2 (`--bare` drops hooks) | 5.2.2 | Included |
| web-02 | Key finding 3 (field reports) | 5.2.8 | Included |
| web-02 | Key finding 4 (hooks in subagents; `SubagentStop` fields) | 5.2.9 | Included |
| web-02 | Key finding 5 (`--allowedTools` vs `--tools`; subagent allowlist) | 5.2.4, 5.2.5 | Included |
| web-02 | Key finding 6 (per-process `--model`; custom ids) | 5.2.7 | Included |
| web-02 | Key finding 7 (LiteLLM picker filter) | 5.2.7 | Included |
| web-02 | Key finding 8 (`--session-id`, resume, stream-json, cost) | 5.2.3, 5.2.8, 5.2.10 | Included |
| web-02 | Key finding 9 (`--settings` precedence; hooks merge unconfirmed) | 5.2.6 | Included |
| web-02 | Rec 1 (do not mark hooks-in-`claude -p` verified for gateway ids; one-call local probe) | 5.2.2, 5.2.7, 5.2.3 and the open-items table in 5.2 | Included as source option; the probe command shape is derived from documented flags and untested; not reproduced here because it is a procedure, not a finding |
| web-02 | Rec 2 (never launch hook-dependent reviewers with `--bare`) | 5.2.2 | Included as source option |
| web-02 | Rec 3 (hook on both `PostToolUse` and `PostToolUseFailure`; command hooks; avoid `SessionEnd` / `UserPromptSubmit`; use `Stop`) | 5.2.1, 5.2.8 | Included as source option |
| web-02 | Rec 4 (prefer Agent dispatch with a `SubagentStop` command hook; keep `claude -p` only for gateway ids the Agent tool cannot select) | 5.2.9, 5.2.7, 5.2.10 | Included as source option |
| web-02 | Rec 5 (keep the reviewer allowlist; board writes via hook or orchestrator) | 5.2.5 | Included as source option |
| web-02 | Rec 6 (hooks-merge question blocks only layered `--settings` hooks) | 5.2.6 and open-items table | Included as source option |
| web-02 | Rec 7 (codebase precedence reminder) | Section 5 preamble | Included |
| web-03 | Key finding 1 (ref storage; `check-ref-format` does not forbid either name) | 5.3.1 A1, B1 | Included |
| web-03 | Key finding 2 (error text) | 5.3.1 B2 | Included |
| web-03 | Key finding 3 (packed and remote-tracking refs; prune) | 5.3.1 B3, B4 | Included |
| web-03 | Key finding 4 (naming rule; layout before first push) | 5.3.2 C1 | Included |
| web-03 | Key finding 5 (GitHub native stacks; same-repo limit) | 5.3.3 D1 | Included |
| web-03 | Key finding 6 (`git rebase --onto`; auto-retarget unverified) | 5.3.4 E1 | Included |
| web-03 | Key finding 7 (Graphite, ghstack, git-branchless) | 5.3.5 F2, F3, F4 | Included |
| web-03 | Key finding 8 (reviews and CI; source conflicts) | 5.3.6 G1, G2, conflict table | Included |
| web-03 | Rec 1 (name branches so none is a prefix of another; decide before first push) | 5.3.2 C1 | Included as source option |
| web-03 | Rec 2 (GitHub-native stack if `/sc:pr-submit` can create stacked PRs; else sequential PRs with `git rebase --onto`) | 5.3.3 D1; 5.3.4 E1 | Included as source option; the `/sc:pr-submit` capability is an open codebase question |
| web-03 | Rec 3 (check CI `branches:` filters for hand-built stacks) | 5.3.6 G2 | Included as source option; unverified |
| web-03 | Rec 4 (avoid ghstack; avoid Graphite unless settings acceptable) | 5.3.5 F2, F3 | Included as source option |
| web-03 | Rec 5 (treat bottom-up merge order as a gate; plan CI cost) | 5.3.3 D1; 5.3.6 G1, G2 | Included as source option |
| web-03 | Rec 6 (items left open: reftable, official `--onto` and `--update-refs` text, GitHub CI page 404, `gh stack` prefix-flag scope) | 5.3.1 B5; 5.3.4 E1, E2; 5.3.5 F1; 5.3.6 G2 | Included |
| web-04 | Key finding 1 (SARIF kind/level/identity; absent `region` = whole file) | 5.4.1 (1.1) | Included |
| web-04 | Key finding 2 (GitHub SARIF subset; severity and gate) | 5.4.1 (1.2); 5.4.4 (4.1) | Included |
| web-04 | Key finding 3 (rdjson closest to a PR-review finding) | 5.4.2 | Included |
| web-04 | Key finding 4 (PR review API location type; out-of-diff rejection) | 5.4.3 | Included |
| web-04 | Key finding 5 (bot severity/category axes; verdict-level confidence; Codex P0-P3) | 5.4.4 | Included |
| web-04 | Key finding 6 (closed resolution vocabulary; thread id) | 5.4.5 | Included |
| web-04 | Key finding 7 (dedup keys; silent collapse in GitLab) | 5.4.1 (1.4, 1.2) | Included |
| web-04 | Rec 1 (one shared record: id, category, path, start line, content anchor, severity ordinal with opaque vendor label, message, reviewer, lens separate) | 5.4.5 minimal-record table | Included as source option |
| web-04 | Rec 2 (disposition, status, thread id, dismissal reason, reviewed head SHA in the ledger, not the record) | 5.4.5 (5.1, 5.2, 5.3) and minimal-record table | Included as source option |
| web-04 | Rec 3 (confidence on verdict or cluster, not per finding) | 5.4.4 (4.3, 4.5) | Included as source option |
| web-04 | Rec 4 (export adapters to rdjson, GitHub `comments[]`, optionally SARIF; a "postable" check at posting time) | 5.4.2, 5.4.3 | Included as source option |
| web-04 | Rec 5 (severity router as configuration over the internal ordinal with a vendor mapping table) | 5.4.4 (4.1, 4.5) and vocabulary table | Included as source option |
| web-04 | Rec 6 (do not adopt full SARIF internally; export target only) | 5.4.1 | Included as source option; web-04 labels it a judgement, not a finding stated by any source |
| web-04 | Rec 7 (look up Augment's comment format or read `pr_submit` code before fixing the mapping table) | Section 5.4 preamble and vocabulary table | Included as an open gap |

Nothing from the four web files' Key External Findings or Recommendations sections is excluded, except that web-02 Rec 1's probe command text is referenced but not reproduced (reason stated in its row).

#### Statement on precedence

External findings in this section supplement and never override code-verified facts. All findings are external context drawn only from the four web research files, each flagged by its own reliability tier. Where a web finding conflicts with a code-verified fact, the code wins and the discrepancy is stated; none of the four web files recorded such a conflict, and web-03 explicitly defers to research item 2.18. Codebase statements quoted in the web files were supplied as context, not verified by the web researchers, and are labelled `[UNVERIFIED]` where those files said so.

Status: Complete

