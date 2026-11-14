# Research: Multi-model and multi-agent review panel evidence (web topic W1)
**Topic:** reviewer agreement and its measurement, position and verbosity bias, LLM-as-judge reliability and self-preference, cross-model diversity, debate vs independent review plus merge, quorum and verdict rules
**Scope:** external web sources only (Tavily); codebase is the source of truth
**Status:** Complete
**Date:** 2026-11-14
**web-provenance:** provider=tavily
---

## Codebase context handed in (not verified by this agent)
- E1: 3 heterogeneous reviewers per shadow run, class dispatch (collapse to 1 of 3 distinct models under tier3 is [UNVERIFIED]); 7 multi-reviewer clusters among 216 findings [UNVERIFIED].
- E2: independent reviewers per model id; one valid reviewer passing is a code behaviour (`tests/review/test_review_ledger.py:376-385`); blind judges against a 16-defect ground truth.
- E1 seeded-defect quality measurement was never run.

---

## Area A: LLM-as-judge biases (position, verbosity, self-enhancement)

### A1. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023 datasets track)
- **Source:** https://arxiv.org/abs/2306.05685 (full text https://arxiv.org/html/2306.05685v4); secondary summaries: https://www.alphaxiv.org/abs/2306.05685, https://tailoredai.substack.com/p/judging-llm-as-a-judge-with-mt-bench
- **Reliability:** peer-reviewed paper (primary); secondary summaries are blog-grade.
- **Key information extracted:**
  - Names four judge limitations: position bias, verbosity bias, self-enhancement bias, limited reasoning ability. Says some biases are minor or mitigable.
  - Position bias: all tested judges showed strong position bias, most favour the first position; Claude-v1 also showed a name bias toward "Assistant A" (rename test). Per the alphaxiv summary, GPT-4 was consistent when answer order was swapped in 65.0% of cases with the default prompt on deliberately similar answers (a stress test, not a general rate).
  - Verbosity ("repetitive list" attack on 23 answers): all judges can be fooled, GPT-4 defends significantly better. Figures 91.3% failure for Claude-v1 and GPT-3.5 and 8.7% for GPT-4 come from a secondary summary (https://note.com/_snsk/n/nf67a8c43e938?hl=en); not read in the primary paper table here.
  - Self-enhancement: per the substack summary, GPT-4 favours itself with a roughly 10% higher win rate and Claude-v1 roughly 25%; GPT-3.5 does not favour itself. Treat these numbers as second-hand.
  - With biases addressed, GPT-4 agreement with humans exceeds 80%, equal to human-human agreement (paper abstract).
  - Mitigations named: swap positions and only accept consistent verdicts, reference-guided grading, few-shot and chain-of-thought judges.
- **Relation to codebase:** E2 used blind judges against a 16-defect ground truth. This paper supports that design (reference-guided, blind) and says order randomisation is needed for any pairwise comparison the panel does. For a findings-merge panel, the position-bias risk applies wherever a judge sees two reviewers' findings side by side or in a fixed order.
- **Supports / extends / contradicts:** SUPPORTS blind judging with a ground truth; EXTENDS with a need to randomise order and control length when judging reviewer output.
- **Relevance:** HIGH

### A2. Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations" (NeurIPS 2024)
- **Source:** https://arxiv.org/abs/2404.13076 ; https://neurips.cc/virtual/2024/poster/96672
- **Reliability:** peer-reviewed paper.
- **Key information extracted:** Self-preference (an LLM scores its own outputs above others' while human annotators rate them equal). Out of the box, GPT-4 and Llama 2 distinguish their own outputs from other LLMs' and humans' with non-trivial accuracy. After fine-tuning, self-recognition correlates linearly with self-preference strength, and controlled experiments argue the link is causal.
- **Relation to codebase:** A reviewer panel member that also produced the code under review (for example a Claude reviewer of Claude-written changes) may favour it. E1/E2 reviewers were of mixed model classes; whether the code under review was written by one of the panel models was not given to this agent, so the exposure is [UNVERIFIED].
- **Supports / extends / contradicts:** EXTENDS: gives a reason to include at least one reviewer from a model family different from the author.
- **Relevance:** HIGH

### A3. Chen et al. 2025 "Measuring Self-Preference in LLM Judgments" (EMNLP 2025), with overview of related mitigation work
- **Source:** https://aclanthology.org/2025.emnlp-main.86.pdf ; overview https://www.emergentmind.com/topics/self-preference-bias ; https://neurips.cc/virtual/2025/122352
- **Reliability:** peer-reviewed papers (EMNLP, NeurIPS); overview site is a secondary aggregator.
- **Key information extracted:** Self-preference appears in both pre-trained and post-trained models. The paper's "DBG" score compares judge win rates against gold judgments to separate real quality from bias. Reasoning models are not automatically less biased (DS-R1-Distill-Qwen-32B 4.8% DBG vs Qwen2.5-72B-Instruct 2.6% in the paper's table). The overview reports a perplexity-based account (judges prefer low-perplexity, familiar text) and lists mitigations: blind evaluation, ensemble judging, activation steering. A NeurIPS 2025 paper on activation steering found it changes outcomes in up to 97% of biased cases but destabilises legitimate evaluations.
- **Relation to codebase:** Using gold labels (the 16-defect ground truth of E2, or E1's never-run seeded-defect design) is the same remedy the paper uses to separate bias from quality. This strengthens the case for running the seeded-defect measurement that E1 designed but did not run.
- **Supports / extends / contradicts:** SUPPORTS the E1/E2 ground-truth approach.
- **Relevance:** MEDIUM

### A4. Ye et al., "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge" (CALM, ICLR 2025)
- **Source:** https://arxiv.org/abs/2410.02736 (HTML https://arxiv.org/html/2410.02736v1); https://proceedings.iclr.cc/paper_files/paper/2025/file/fdca08d371e4b6c031397909e20043bd-Paper-Conference.pdf
- **Reliability:** peer-reviewed paper (ICLR).
- **Key information extracted:** Defines 12 judge biases (position, verbosity, compassion-fade, bandwagon, distraction, fallacy-oversight, authority, sentiment, diversity, chain-of-thought, self-enhancement, refinement-aware) and tests each with an "attack-and-detect" perturbation: change one bias-inducing feature and check whether the verdict stays stable. Position bias is tested by rotating answer order and counting inconsistent selections. Conclusion: advanced models such as Claude-3.5 and GPT-4o can serve as reliable judges for specific tasks, but significant biases persist in specific tasks and robustness varies across scenarios.
- **Relation to codebase:** Gives a ready test method (perturb and re-judge, rotate order) for the blind judges E2 used, and for any judge that adjudicates between reviewers in a merge. Two of its bias types matter for reviewer output: authority (a citation or apparent expert cue) and bandwagon (a stated majority); a merge or verdict step that shows a judge "2 of 3 reviewers agree" may bias it. That inference is mine, not a finding of the paper.
- **Supports / extends / contradicts:** EXTENDS (adds a concrete bias-test method).
- **Relevance:** MEDIUM

## Area B: Panels and juries of diverse models

### B1. Verga et al. (Cohere), "Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models" (PoLL)
- **Source:** https://arxiv.org/abs/2404.18796 ; https://huggingface.co/papers/2404.18796 ; summaries https://liner.com/review/replacing-judges-with-juries-evaluating-llm-generations-with-panel-diverse, https://www.alphaxiv.org/abs/2404.18796
- **Reliability:** arXiv preprint from an industry lab (not confirmed as peer-reviewed in the sources read); summaries are secondary.
- **Key information extracted:** A panel of smaller judges from disjoint model families (Command R, Haiku, GPT-3.5) pooled by a voting function correlated better with human judgments than a single GPT-4 judge across three judge settings and six datasets, showed less intra-model bias, and cost over seven times less. On KILT-NQ, Cohen's kappa with humans: PoLL 0.763, GPT-4 0.627, Haiku 0.749, Command R 0.734, GPT-3.5 0.726 (liner.com summary). On Chatbot Arena, PoLL had Pearson 0.917 with crowd Elo (alphaxiv summary). Limits stated by the authors: only three judge settings and a limited number of panel compositions; math and reasoning not tested; panel selection (which models to include) left as future work.
- **Relation to codebase:** Directly relevant to the panel-composition options. The task is scoring answer correctness (QA), not code-defect finding, so transfer to code review is [UNVERIFIED]. Supports dispatching 2-3 reviewers from different model families rather than one large reviewer. It does not say anything about which voting function suits a "find defects" task, where recall of distinct findings matters more than agreement.
- **Supports / extends / contradicts:** SUPPORTS the 2-3 heterogeneous reviewer design; EXTENDS with the point that heterogeneity helps by cancelling intra-model bias. If E1's class dispatch collapses to fewer distinct models under tier3 ([UNVERIFIED] in the codebase), the diversity benefit would shrink accordingly.
- **Relevance:** HIGH

### B2. Kim, Garg, Peng, Garg, "Correlated Errors in Large Language Models" (ICML 2025)
- **Source:** https://arxiv.org/abs/2506.07962 ; https://www.alphaxiv.org/abs/2506.07962
- **Reliability:** peer-reviewed paper (ICML 2025, per a repository README citing it; venue not checked on the arXiv page).
- **Key information extracted:** Over 350 LLMs, substantial error correlation: on one leaderboard dataset, models agree 60% of the time when both are wrong. Shared architecture and provider raise correlation, but larger, more accurate models have highly correlated errors even across providers. LLM-as-judge effect: judges inflate the accuracy of models less accurate than themselves and under-rate more accurate ones, more so for same-provider models. Recommendations: anchor to ground truth, select judges with uncorrelated error patterns, use multi-judge consensus, track error correlation.
- **Relation to codebase:** Complicates the heterogeneity argument. Different model classes are necessary for diversity but may not be sufficient. For code review, the relevant quantity is whether reviewers miss the same defects. E1's low overlap among reviewers (7 multi-reviewer clusters among 216 findings, [UNVERIFIED]) points to low overlap in what they flag, which is a different measure from error correlation on a labelled set; it cannot be turned into an error correlation without the ground truth E1 never ran.
- **Supports / extends / contradicts:** EXTENDS and partly CAUTIONS against B1; does not contradict the codebase.
- **Relevance:** HIGH

### B3. Kohli, "Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels" (Apple ML Research; arXiv 2605.29800)
- **Source:** https://machinelearning.apple.com/research/correlated-llm-evaluation-panels ; https://arxiv.org/html/2605.29800v1
- **Reliability:** preprint from a corporate research lab (peer review status not shown in the sources read). Published 2026 per its arXiv id; the date was not extracted.
- **Key information extracted:** 9 frontier LLMs from 7 families on three NLI datasets with 100 human annotations per item: the panel carries only about 2 independent votes of information (Kish effective sample size). Panel accuracy falls 8-22 points short of the independent-voting ideal, and the best single judge matches or beats the full panel in all conditions. Same-family pairs are only slightly more correlated than cross-family (phi 0.437 vs 0.389); the three most correlated pairs are cross-family (Claude x Gemini 0.603). Using one judge per family leaves n_eff at 1.93. Adding judges or using smarter aggregation closes at most 11% of the gap. A secondary summary (https://note.com/logicalskill/n/n53fc8c04b75e?hl=en) reports that even when all 9 judges agreed they were wrong 9.1% of the time; not verified in the primary text here. Authors list limits: gold standard is a 100-annotator majority; tasks are NLI and one preference task, not code review.
- **Relation to codebase:** CONTRADICTS the simple reading of B1 for verdict computation: if reviewers' errors are correlated, a "k of n agree" quorum is weaker evidence than it looks. It is evidence about voting on a shared answer; a review panel whose value comes from union of distinct findings (each independently verified against code) is a different mechanism, so applicability is [UNVERIFIED]. It does argue for adding verification that is not another LLM vote (see Area G, citation verification).
- **Supports / extends / contradicts:** CONTRADICTS (in part) the assumption that three model families give three independent opinions; consistent with the codebase fact that citations are verified by code in the planned core.
- **Relevance:** HIGH

## Area C: Debate versus independent review plus aggregation

### C1. "Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?" (NeurIPS 2025)
- **Source:** https://arxiv.org/abs/2508.17536 ; https://proceedings.neurips.cc/paper_files/paper/2025/file/934252acd87f254d5d4672fbde283bd2-Paper-Conference.pdf ; https://neurips.cc/virtual/2025/poster/116557
- **Reliability:** peer-reviewed paper.
- **Key information extracted:** Across seven NLP benchmarks, majority voting over independent agents' initial answers accounts for most of the gain usually credited to multi-agent debate; in most cases voting without debate performs on par with debate. The authors model debate as a martingale over agents' beliefs and conclude debate alone does not raise expected correctness. The study also covers heterogeneous agent populations and open-ended tasks. The authors do not claim debate can never help; they propose strategies that preserve correct answers across rounds and report gains from those. Tasks are NLP benchmark questions with a single answer, not defect finding.
- **Relation to codebase:** E2 ran independent reviewers per model id and merged afterwards, which is the "independent then aggregate" side of this comparison. This is evidence that independent review plus merge is a sound default and that a debate stage should not be assumed to add accuracy. It does not test finding-set unions, so applicability to a merge that keeps findings only one reviewer raised is [UNVERIFIED].
- **Supports / extends / contradicts:** SUPPORTS independent review plus merge. Does not contradict anything verified in code.
- **Relevance:** HIGH

### C2. Explainer on independence and correlated errors
- **Source:** https://datarekha.com/agentic-ai/multi-agent-debate
- **Reliability:** blog / tutorial (lowest tier).
- **Key information extracted:** The wisdom-of-crowds lift from voting depends on independent errors; same model with same prompt gives correlated errors and the vote barely helps. Debate's failure mode is conformity (a confident wrong answer wins), countered by diversity of models, prompts and roles. The numbers quoted (5 agents at 60% give 68%, 15 give 79%) are textbook arithmetic under independence, not an empirical result about LLMs.
- **Relation to codebase:** Frames why cross-model dispatch matters and why a tier setting that collapses reviewers to one model removes the benefit. Consistent with, but not evidence for, the codebase facts.
- **Relevance:** LOW

## Area D: Code-review-specific evidence on multi-reviewer ensembles and merge rules

### D1. SWR-Bench, "Benchmarking and Studying the LLM-based Code Review" (arXiv 2509.01494)
- **Source:** https://arxiv.org/abs/2509.01494 ; https://arxiv.org/html/2509.01494v1 ; https://www.alphaxiv.org/abs/2509.1494v1 (summary; alphaxiv URL as returned by search)
- **Reliability:** arXiv preprint (peer review status not shown in the sources read).
- **Key information extracted:** 1,000 manually verified PRs; LLM-based evaluation that checks whether ground-truth issues are covered, reporting about 90% agreement with human judgment. A "Multi-Review" strategy generates several independent reviews and aggregates them with one extra LLM call: "Multi-Agg" over different LLMs, "Self-Agg" over repeated runs of one LLM. Reported: F1 up to +43.67%; Gemini-2.5-Flash with Self-Agg (n=10) reached 21.91% overall F1 and 30.44% recall (+118.83% recall). Overlap analysis found considerable inconsistency in the change-points flagged: only 36 overlapped across different LLMs and 27 across five runs of the same LLM (alphaxiv summary). Authors list reducing false positives while keeping recall as future work.
- **Relation to codebase:** This is the closest external match to the planned core (independent reviewers, then aggregation). It supports a union-style merge: low overlap between reviewers is expected and is the reason aggregation raises recall, consistent with E1's low-overlap observation (7 multi-reviewer clusters among 216 findings, [UNVERIFIED]). It also shows that repeated runs of one model overlap about as little as different models, so a one-model collapse could be partly offset by repeated runs, though that comparison was not run in our codebase. Aggregation here uses an LLM call, not citation verification.
- **Supports / extends / contradicts:** SUPPORTS union merge; EXTENDS with the Self-Agg option as a cheaper substitute for model diversity.
- **Relevance:** HIGH

### D2. GitHub, "ReviewBench: An open benchmark for AI code review" (GitHub Blog)
- **Source:** https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review ; https://www.linkedin.com/posts/github_reviewbench-an-open-benchmark-for-ai-code-activity-7513480739162677250-JNli (commentary, low reliability)
- **Reliability:** vendor engineering blog (official for the claims about its own product, not peer-reviewed).
- **Key information extracted:** 219 PRs from 187 repositories in 19 languages (per vendor post). Golden set built from human reviewers, follow-up commits, deterministic tools and multiple frontier LLMs across model families, then semantically deduplicated so that agreement across producers does not inflate the set. Six metrics: grounded and augmented precision, recall and F1; the augmented family credits valid findings absent from the golden set, judged by an LLM. Senior engineers re-labelled the golden set and agreed 96.6% of the time (vendor figure). A lite-tier multi-model ensemble review was predicted by ReviewBench to raise precision, recall and comment volume while lowering cost per review (vendor statement; no numbers in the extracted text). A commenter notes grounded recall is the cross-system number and leaderboard rows are best runs, so spread across runs is hidden (LinkedIn comment; low reliability).
- **Relation to codebase:** Offers a measurement design for E1's never-run quality measurement: a deduplicated multi-source golden set plus grounded vs augmented scoring, and reporting variance across runs. The "semantic dedup without letting agreement inflate" rule matches the planned cluster-duplicates step.
- **Supports / extends / contradicts:** EXTENDS E1's seeded-defect design with a second measurement style (real PRs, golden set).
- **Relevance:** MEDIUM

### D3. LangChain, "Evaluating code review agents with ReviewBench" and Entelligence benchmark post
- **Source:** https://www.langchain.com/blog/evaluating-code-review-agents-with-reviewbench ; https://entelligence.ai/code-review-benchmark-2026
- **Reliability:** vendor blogs (not peer-reviewed). Note: the LangChain post uses the name ReviewBench for its own 59-task benchmark; it is a different artifact from the GitHub one in D2 as far as the extracted text shows.
- **Key information extracted:** LangChain: with a minimal harness, the strongest runs recover only about 30% of baseline issues; narrow review strategies lower cost but hurt coverage; prompting changes results; scoring is by an LLM verifier that compares submitted findings to a curated baseline, F1 headline. Entelligence: built a golden set with three frontier models reviewing independently, a separate GPT-4o call as arbiter keeping comments flagged by 2 of 3 (comments flagged by only one model were discarded), then human validation. That is a majority-vote rule applied to findings.
- **Relation to codebase:** The Entelligence rule is a concrete example of a 2-of-3 quorum on findings, and it discards single-reviewer findings. That directly conflicts with the union approach in D1 (which gains recall from findings few reviewers share). Which is right depends on whether the goal is precision of a ground truth (Entelligence) or recall of a review (D1); the planned core's choice for single-reviewer findings is a design option, not settled by these sources.
- **Supports / extends / contradicts:** EXTENDS; shows two opposed merge rules in practice. The "one valid reviewer passing" behaviour pinned at `tests/review/test_review_ledger.py:376-385` (per the task) corresponds to the permissive end.
- **Relevance:** MEDIUM

### D4. c-CRAB "Code Review Agent Benchmark" (arXiv 2603.23448)
- **Source:** https://arxiv.org/html/2603.23448v2
- **Reliability:** arXiv preprint.
- **Key information extracted:** Automated review tools pass 20.1% to 32.1% of tests built from human reviews, humans 100%; the union of four tools passes 97 of 234 tests (41.5%); agent reviews often consider different aspects than human reviews.
- **Relation to codebase:** Union of tools still leaves a large gap to human review, so a panel of LLM reviewers should not be described as a full replacement for human review or for a test gate. Relevant to the rf-qa replacement goal as a limit on claims.
- **Supports / extends / contradicts:** EXTENDS (limits).
- **Relevance:** MEDIUM

### D5. Practitioner note, "Evaluating LLM Code Reviewers: Precision, Recall, and Routing"
- **Source:** https://prakharsingh.github.io/notes/evaluating-llm-code-reviewers
- **Reliability:** personal blog (lowest tier).
- **Key information extracted:** Suggests self-consistency over N samples as a cheap signal (inconsistent findings on the same diff correlate with false positives in production, claimed without cited evidence); treat disagreement between a cheap and a frontier reviewer as a signal worth surfacing; use three-tier labels (hard reject, soft reject, accept) to compute precision at different strictness.
- **Relation to codebase:** Suggests keeping reviewer disagreement as data rather than discarding it, and a three-way finding label for the quality measurement. Claims are unsupported opinion.
- **Relevance:** LOW

## Area E: Measuring agreement and judge reliability

### AE-1. Agreement metrics: raw agreement overstates reliability
- **Source:** https://arxiv.org/html/2606.19544v1 ("Reliability without Validity", 21 judges, 3 benchmarks, ~541,000 judgments); https://arxiv.org/html/2510.27106v1 ("Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks"); https://kili-technology.com/blog/inter-rater-reliability ; https://arize.com/blog/measuring-human-llm-judge-alignment ; https://www.honeyhive.ai/learn/inter-annotator-agreement
- **Reliability:** two arXiv preprints (neither confirmed as peer-reviewed in what was read; 2606.19544 carries a mid-2026 id); the other three are vendor blogs (lowest tier).
- **Key information extracted:**
  - Reliability without Validity: raw agreement overstates chance-corrected discrimination by 33-41 percentage points in all 21 judges; judge rankings shift by up to 14 positions across benchmarks; high test-retest reliability (above 0.95) coexists with severe position bias (above 0.10) in two production-deployed judges ("test-retest measures stability, not correctness"); verbosity bias was small (below 0.011) across the cohort under one pairwise rubric, in contrast to the 2023 literature.
  - Rating Roulette: judges are self-inconsistent across repeated runs; Krippendorff's alpha over 3 runs is 0.33 (Llama 3.1), 0.63 (DeepSeek-R1), 0.79 (Qwen-3) on SummaC; up to 5 runs did not change self-reliability; accuracy-style metrics inflate agreement relative to alpha. Recommendation: account for self-reliability.
  - Blogs (Kili, Arize, HoneyHive): report chance-corrected agreement (Cohen's kappa for 2 raters, Fleiss' kappa or Krippendorff's alpha for 3 or more or missing data) next to raw agreement; Cohen's kappa is for the same two raters on every item; a kappa of 0.667 is "substantial", "moderate" or "tentative" depending on the scale used (Kili); McHugh is quoted as saying a kappa below 0.60 is inadequate agreement (HoneyHive).
- **Relation to codebase:** E1's quality measurement and E2's blind-judge scoring both need an agreement statistic. Raw percent agreement between reviewers would look high when most items are clean. Reviewers here do not label a fixed item set (each emits its own findings), so kappa and alpha apply only after findings are clustered into shared items or after reviews are scored against the 16-defect ground truth; this application is my inference, not stated in the sources. Also, judge verdict stability across reruns should be measured separately from correctness.
- **Supports / extends / contradicts:** EXTENDS. Note that "reliability without validity" (a deterministic judge that is consistently wrong) warns against treating stable verdicts across reruns as evidence of correctness.
- **Relevance:** HIGH

### AE-2. Position bias is judge-dependent and task-dependent; code judges have their own biases
- **Source:** https://aclanthology.org/2025.ijcnlp-long.18.pdf ("A Systematic Study of Position Bias in LLM-as-a-Judge", IJCNLP-AACL 2025); https://aclanthology.org/2026.findings-eacl.70.pdf ("Exploring Biases in LLM Judges for Code Evaluation", EACL 2026 Findings); https://medium.com/softtechas/utilising-llm-as-a-judge-to-evaluate-llm-generated-code-451e9631c713 (blog survey); https://ai-tldr.dev/learn/evaluation-safety/llm-as-judge/llm-judge-biases (blog)
- **Reliability:** two peer-reviewed ACL Anthology papers (the Anthology listing was read via search excerpts only); the two blogs are lowest tier, and their numbers are second-hand.
- **Key information extracted:**
  - Position bias study: bias varies by judge and by task; weakly influenced by prompt length but strongly affected by the quality gap between candidates; more capable models (GPT-4o, Claude-3.5-Sonnet) stay consistent from pairwise to list-wise comparisons, while GPT-3.5-Turbo is more sensitive to more candidates. At least 75% of judges agreed on more than half of the instances; the authors say reliability on such easy instances is enhanced by majority voting.
  - Code-judge biases paper: first systematic study of LLM code evaluators under semantically equivalent but superficially different code (variable names, comments, formatting). It defines six bias types and positive/negative bias (a superficial change pushes the verdict toward correct, or toward incorrect, regardless of ground truth).
  - Blog survey (Softtech) of code-judge papers: swapping the order of good and bad code changed judgments by up to 14% (second-hand); judges struggled to evaluate code from different sources consistently; detecting functional bugs without execution is a major weakness; judge hallucination of a missing requirement or nonexistent bug is the most common reason for rejecting valid code. ai-tldr.dev blog: swap consistency across 15 judge models ran from 70.5% (GPT-3.5-Turbo) to 77.3% (Gemini-Pro), citing arXiv 2406.07791 (not opened).
- **Relation to codebase:** Review panels judge code, so the code-specific bias evidence matters more than the chat-quality evidence. Two usable points: order of reviewers' findings in a merge or judging prompt should be randomised or swapped, and a judge that sees only the diff with no execution is weak on functional bugs, which supports requiring cited evidence from the repository.
- **Supports / extends / contradicts:** EXTENDS A1 and A4 to code; partly CONTRADICTS the 2023 verbosity-bias evidence (finding AE-1 above found it much reduced in recent judges), so a verbosity guard is a cheap precaution rather than a proven need.
- **Relevance:** MEDIUM

## Area F: Quorum, verdict and aggregation rules

### F1. Unanimous (AND) juries for code acceptance, Ullah and Serwadda, "Vibe Coding on Trial: Operating Characteristics of Unanimous LLM Juries" (ICSC 2026)
- **Source:** https://arxiv.org/abs/2602.18492 (HTML https://arxiv.org/html/2602.18492v2, v1 https://arxiv.org/html/2602.18492v1); venue per a repository README https://github.com/abdullazada-mustafa/llm-jury-sql ; secondary summary https://www.emergentmind.com/topics/multi-llm-jury-protocol
- **Reliability:** peer-reviewed conference paper (ICSC 2026 per the README citation; not checked at the venue).
- **Key information extracted:** 15 open models benchmarked on 82 MySQL text-to-SQL prompts with an execution-based ground truth; unanimous committees of size 1 to 6 built from the six best models see the prompt, schema and candidate SQL and accept only when every member says it is correct. Single-model judges are uneven; small unanimous committees of strong models cut false accepts while still passing many good queries; the exact committee composition matters significantly. The paper reports TPR, FPR and Youden's J (TPR minus FPR). The emergentmind summary (secondary) states the best committees were 3 to 4 strong LLMs with Youden's J about 0.52 and that composition matters more than size past basic thresholds; not verified in the primary text read.
- **Relation to codebase:** This is the strict end of the verdict-rule spectrum: accept only when all reviewers agree. The current code behaviour (one valid reviewer passing, `tests/review/test_review_ledger.py:376-385` per the task) is the permissive end. The paper gives a concrete way to compare rules: measure TPR and FPR of each rule against a labelled set, which E2's 16-defect ground truth could provide. The task is single-answer SQL correctness, so transfer to a multi-finding review verdict is [UNVERIFIED].
- **Supports / extends / contradicts:** EXTENDS (offers a measurable comparison of quorum rules); does not contradict the code.
- **Relevance:** HIGH

### F2. Practitioner guidance on verdict rules
- **Source:** https://www.splunk.com/en_us/blog/learn/tuning-llm-judges.html ; https://www.emergentmind.com/topics/multi-llm-jury-protocol (rule table, secondary)
- **Reliability:** vendor blog and aggregator site (lowest tier).
- **Key information extracted:** Splunk suggests majority vote for binary pass/fail, max pooling (any judge says pass gives pass) when recall has priority, mean for ordinal scales, three judges as the minimum for meaningful aggregation, five judges to separate "5 of 5" from "3 of 5", and mixed model families to reduce systematic bias. Emergentmind lists unanimity (AND), majority, weighted average, dynamic selection and sequential tie-breaker rules with example domains. Neither source gives measurements for code review.
- **Relation to codebase:** Names the same options the unified panel must choose between (any-pass, majority, unanimity, weighted) without evidence for which fits PR review. With 2-3 reviewers (as designed), a majority rule has only 2-of-3 granularity; Splunk's five-judge remark suggests 3 reviewers give coarse confidence levels.
- **Supports / extends / contradicts:** EXTENDS (option list only).
- **Relevance:** LOW

### F3. Aggregation cannot fix correlated judges: CARE, Ising-model aggregation and process-level decorrelation
- **Source:** https://arxiv.org/html/2603.00039v1 (CARE: Confounder-Aware Aggregation); https://builder.aws.com/content/3JbMv6rSHOq4TA8stg8pevGzupx/aggregation-methods-for-llm-as-a-judge ; https://www.emergentmind.com/topics/llm-as-a-judge-implicit-aggregation ; https://aclanthology.org/2025.acl-long.756.pdf (SkillAggregation)
- **Reliability:** arXiv preprint (CARE), ACL 2025 paper (SkillAggregation, excerpt only), AWS community blog and an aggregator (lowest tier). Reported gains below come from the AWS blog and are not verified in the primary papers.
- **Key information extracted:** CARE models judge scores as a latent true-quality signal plus shared confounders such as verbosity and style, because majority vote or averaging "provide little gain or even amplify systematic mistakes" when judges share confounders. AWS blog reports CARE with up to 26.8% error reduction and a two-phase "reasoning jury" with a blind moderator giving +12 F1 points at 8-16% extra cost (blog claims, unverified). SkillAggregation and Dawid-Skene weight judges by estimated reliability instead of equal votes; SkillAggregation reports its largest gains over majority voting when a majority of judges are good and a couple are bad. Dependence-aware (Ising) aggregation is listed as outperforming majority vote and Dawid-Skene (secondary summary).
- **Relation to codebase:** Weighted or dependence-aware aggregation needs labelled data to estimate reliability per reviewer, which is exactly what the unrun E1 seeded-defect measurement would produce. Before that data exists, equal-weight rules are the only option that does not rest on assumptions about reviewer reliability.
- **Supports / extends / contradicts:** EXTENDS B3 with remedies; consistent with the point that verification rather than voting should carry the decision.
- **Relevance:** MEDIUM

## Area G: Verification of reviewer findings (grounding and citation checks)

### G1. Mechanical citation verification
- **Source:** https://arxiv.org/html/2512.12117v1 ("Citation-Grounded Code Comprehension: Preventing LLM Hallucination Through Hybrid Retrieval and Graph-Augmented Context")
- **Reliability:** arXiv preprint (peer review status not shown).
- **Key information extracted:** A mechanical check that every cited code location overlaps context actually supplied flagged about 8% of responses as hallucinated; manual review of a sample (31 of 32 examined flags) confirmed 97% were genuine and found zero false negatives among the 92% passing responses (the paper calls this 100% precision and 97% recall on its sample). Hallucinated citations were fabricated locations or wrong line numbers, off by 10-50 lines. The authors say a passing citation proves only that the cited code existed in context, not that the claim about it is right.
- **Relation to codebase:** Supports the planned "verify citations" step as a cheap, non-LLM filter, and fits the Kohli finding that a second LLM opinion is weaker than evidence tied to code. A passing citation check does not validate the claim; that limit should be kept in the verdict design. The codebase mechanics of the citation check were not given to this agent and are [UNVERIFIED] here.
- **Supports / extends / contradicts:** SUPPORTS the citation-verification step.
- **Relevance:** HIGH

### G2. Two-pass detect-then-filter patterns and the "AI opinion is not evidence" principle
- **Source:** https://www.gresearch.com/news/building-a-code-review-tool-the-llm-patterns-that-actually-work ; https://evolink.ai/blog/ai-code-review-false-positives ; https://tomosu.ai/blogs/ai-code-review-false-positives-reliability-findings.html ; https://megalens.ai/research/ai-code-review-false-positives ; https://www.augmentcode.com/guides/ai-code-review-accuracy
- **Reliability:** vendor and practitioner blogs (lowest tier); the MegaLens figures come from a self-described sample of 20 findings with no human review and an admitted wide error bar.
- **Key information extracted:** G-Research split recall and precision into separate prompts (first pass captures everything, second pass filters) after single-pass reviews showed two or three false positives in eight findings. Evolink and Tomosu both say a second LLM judging comment wording is not verification; evidence is code, a documented default, a test or a trace. Augment Code's guide cites a CodeRabbit field study (July 2026) tracing 10.3% of false positives to missing visibility into other files. MegaLens: two models from different companies checked 20 findings; of 16 they agreed on, 9 were real and 7 not (about 44% false positives among agreed findings), and none of 9 "critical" labels were rated critical by both (sample of 20; read as a warning only).
- **Relation to codebase:** Agreement between model reviewers is weak evidence that a finding is real (MegaLens, anecdotal; consistent with Kohli B3), which argues against a verdict rule that treats 2-of-3 reviewer agreement as validation. Severity labels across reviewers were inconsistent in that sample, relevant to any severity-based verdict threshold. All of this is blog-grade and should be treated as hypotheses to test with E1's seeded-defect run.
- **Supports / extends / contradicts:** EXTENDS; consistent with, not proof of, the codebase's design.
- **Relevance:** LOW

## Discrepancies and gaps against the codebase facts handed in
- No external source contradicts a verified code behaviour. The codebase facts handed in (class dispatch collapse under tier3, 7 clusters among 216 findings, `tests/review/test_review_ledger.py:376-385`) were not verified by this agent and remain as the task states them.
- Tension (not a contradiction): PoLL (B1) and the "diverse panel" assumption vs Kim et al. and Kohli (B2, B3), which find cross-family judges still make correlated errors. Both are measured on single-answer tasks (QA, NLI), not on finding-set review, so neither can settle the question for the review panel.
- Tension: the Entelligence 2-of-3 finding filter (D3) vs the SWR-Bench union gain (D1) and the one-valid-reviewer-passes behaviour.
- Not found: any peer-reviewed study of heterogeneous multi-reviewer panels for PR code review that compares quorum rules (any-pass, majority, unanimous) on findings with ground truth. The closest are SWR-Bench (aggregation, D1) and the SQL unanimous-jury paper (F1).
- Not verified at the primary source (second-hand numbers flagged inline): MT-Bench self-enhancement and verbosity percentages (A1), emergentmind and AWS blog figures (F1, F3), the 9.1% "all nine agreed and were wrong" figure (B3), PoLL kappa figures (B1, from a summary site).

## Key External Findings
1. LLM judges show position, verbosity and self-preference bias (A1, A2, A3, A4); the standard remedies are order swapping or randomisation, reference or ground-truth grounding, and not letting a model judge its own family's output. Verbosity bias appears much smaller in recent judges (AE-1) but a length guard is cheap.
2. A panel of judges from different model families beat a single large judge in agreement with humans and cost over 7 times less, on QA-style correctness tasks (B1, HIGH relevance, transfer to code review unverified).
3. Cross-family diversity is necessary but not sufficient: error correlation stays high across providers (B2: 60% same-wrong-answer agreement on one dataset; B3: 9 judges from 7 families gave about 2 independent votes; best single judge matched or beat the panel). More judges or smarter aggregation closed at most 11% of the gap (B3).
4. Independent review plus aggregation is a sound default; debate adds little over voting on benchmark tasks (C1).
5. For code review specifically, aggregating several independent reviews raises recall substantially (SWR-Bench: F1 up to +43.67%, recall +118.83% in one setting) because different reviewers and different runs flag largely different change-points (D1). That supports a union-style merge and is consistent with low overlap between reviewers.
6. Merge rules in use differ sharply: 2-of-3 majority that discards single-reviewer findings (Entelligence golden-set construction, D3), a deduplicated union without agreement inflation (GitHub ReviewBench golden set, D2), and strict unanimity for acceptance (F1). Evidence on which fits PR review is absent; the quorum rule is a design choice that should be measured with labelled defects (F1, D2).
7. Agreement must be reported chance-corrected (kappa, Krippendorff's alpha) and judge stability across reruns is not correctness (AE-1); raw agreement overstated chance-corrected discrimination by 33-41 points in all 21 judges tested.
8. Cheap, non-LLM verification helps: a mechanical citation-overlap check separated hallucinated from genuine citations with high precision on one sample (G1), and practitioner sources say a second LLM opinion is not evidence (G2). A passing citation proves existence in context, not correctness of the claim.
9. Even the union of several automated reviewers falls well short of human review on a human-derived test set (D4: 41.5% of tests passed by the union of four tools), a limit on any replacement claim.

## Recommendations from External Research
(External context and options only; the codebase remains the source of truth, and these are not overrides of verified behaviour.)
1. Keep independent per-model review followed by a merge. Do not add a debate stage on the strength of accuracy claims; the evidence does not support it (C1).
2. Treat reviewer-diverse dispatch as the design goal but measure it: if class dispatch collapses to one distinct model under tier3 (a codebase claim marked [UNVERIFIED]), either fix that or add repeated independent runs of the one model, which SWR-Bench shows can give recall gains similar to model diversity (D1, Self-Agg). Do not describe a panel as diverse unless distinct models actually ran (B2, B3).
3. Do not use "k of n reviewers agree" as validation of a finding. Prefer evidence checks that are not another LLM vote: citation verification against the repository (G1) and, where possible, executable tests. Use agreement as a prioritisation signal, not as proof (B3, G2).
4. Choose the verdict rule by measurement. Run the seeded-defect measurement E1 designed (and reuse E2's 16-defect ground truth) to compare at least any-pass, majority and unanimous rules on TPR, FPR and Youden's J, as in F1; report chance-corrected agreement (AE-1) and per-reviewer variance across repeated runs (D2 commentary, AE-1).
5. Until measured, state the current one-valid-reviewer-passes rule as a permissive default whose false-accept rate is unknown, and keep single-reviewer findings in the merge as unconfirmed findings rather than discarding them (supported by D1, opposed by D3's filter; a design option for the report's Section 5.1 to weigh).
6. In any judge or merge step that sees more than one reviewer's output, randomise or swap the order, avoid showing a stated majority or authority cue to the judge, and keep the judge blind to which model produced which finding (A1, A2, A4).
7. Exclude from the panel, or down-weight, a reviewer from the same model family as the code author when that is known (A2; self-recognition drives self-preference). Evidence is on text and summaries, not on code review, so treat as a precaution.
8. Do not claim the panel replaces human or test-based review: union of automated reviewers still misses most human-found issues in c-CRAB (D4). This bears on the rf-qa replacement framing.
9. Defer weighted or dependence-aware aggregation (F3) until labelled data exists to estimate per-reviewer reliability and error correlation; equal-weight rules are the only ones that need no such estimate.

## Summary
- Sources reached through Tavily (provider=tavily; no WebSearch/WebFetch fallback used). Peer-reviewed primary papers: A1, A2, A3, A4, C1, F1 (venue per repository), AE-2 (two ACL Anthology papers, excerpts only). Preprints: B1, B3, D1, D4, AE-1, G1, F3. Vendor and personal blogs: D2, D3, D5, F2, G2, C2 and the blog summaries cited inside other findings.
- No content in this file comes from `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`; neither path was opened. Only the task file's line 297 was read.
- Limits: web sources were read through search excerpts and a few page extracts, not full paper reads; second-hand numbers are labelled. All transfer from QA/NLI/SQL evidence to PR code review is [UNVERIFIED].

