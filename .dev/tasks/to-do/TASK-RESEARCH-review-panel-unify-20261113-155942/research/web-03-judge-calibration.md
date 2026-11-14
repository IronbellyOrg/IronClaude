# Web Research W3: LLM-as-Judge and Calibration

Topic: LLM-as-judge and calibration (self-preference and family bias, position and verbosity bias, blind vs informed grading, rubric-anchored grading, reliability of verbalized confidence, calibration methods)
Date: 2026-11-14
Status: Complete

Search provider: Tavily (mcp__litellm__Tavily-tavily_search / tavily_extract) unless noted per finding.

## Codebase context (read first, from research/05 and research/11)

- Reflect requires calibrator from a different model class than the reviewer; the calibrator agent is written for a 6-dimension troubleshoot rubric while reflect uses 5 dimensions; shadow runs recorded 0 numeric per-finding calibrations of 689 findings; the other session scored panels with a blind Opus judge over anonymised merged reports; the E2 judge was blind to reviewer ids but NOT to panel name (research/11 section 2: judge-one.sh schema contains the combo name); an experiment grader is blind with a frozen rubric (blocking yes/no); reflect code (contract.py) degrades single-reviewer merges and convergence < 0.80 rather than letting one flag decide.

## 1. Self-preference and same-family bias

### 1.1 Panickssery et al., "LLM Evaluators Recognize and Favor Their Own Generations" (NeurIPS 2024)
- URL: https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf (also https://www.alignmentforum.org/posts/CeCKzsKABGKt9aabb/llm-evaluators-recognize-and-favor-their-own-generations)
- Date: 2024 (NeurIPS 2024). Reliability: peer-reviewed paper. Model-behaviour evidence tested GPT-4, GPT-3.5, Claude 2, Llama-2 (2023-era models); date caveat applies to current Claude/other models.
- Key info: frontier LLMs show self-preference (score own output higher than others' at equal human-judged quality) and self-recognition (can tell own text from others'). Fine-tuning to vary self-recognition produces a linear trend with self-preference; correlation not explained by confounders. Evidence on summarization (XSUM, CNN/DM). Pairwise setting averages both orderings to cancel order bias.
- Relation to codebase: SUPPORTS the class-disjoint calibrator rule (calibrator from a different model class than the reviewer) and the blind-to-provenance design. Mechanism is recognition, so hiding provenance (anonymised labels, no model names, no reviewer ids) is the first mitigation; cross-family judge is the second. EXTENDS: E2 judge-one.sh leaked the combo name (encodes model names) into the judge schema, which removes the anonymisation benefit for any judge that can map combo names to its own family.
- Relevance: HIGH

### 1.2 Roytburg et al., "Are LLM Evaluators Really Narcissists? Sanity Checking Self-Preference Evaluations" (arXiv 2601.22548, reanalysis)
- URL: https://arxiv.org/abs/2601.22548 (extracted; summary also at https://www.emergentmind.com/papers/2601.22548)
- Date: submitted 30 Jan 2026, revised 22 Jun 2026 (v4). Reliability: arXiv preprint (abstract read via extract: only 51% of earlier findings keep significance, 89.6% of self-preference mass explained by the baseline); the 37,448-pair and chain-of-thought details come from the aggregator summary only.
- Key info (as reported by the summary): across 37,448 evaluation pairs, evaluator uncertainty on hard items accounts for about 89.6% of measured self-preference; only 51% of earlier findings stay significant under an "Evaluator Quality Baseline"; chain-of-thought mitigation does not generalise across models and tasks.
- Relation to codebase: EXTENDS/qualifies 1.1. Much of "self-preference" is judge error on hard items, not narcissism. For a panel: same-family judging is a risk, but a weak judge on hard findings is a bigger risk, so judge strength and a reference/ground truth matter more than family alone. Does not contradict the class-disjoint rule; it says the rule alone is not sufficient.
- Relevance: MEDIUM

### 1.3 Wataoka et al., "Self-Preference Bias in LLM-as-a-Judge" (2024)
- URL: https://scispace.com/papers/self-preference-bias-in-llm-as-a-judge-3ln30ufzod1e
- Date: 2024. Reliability: preprint (aggregator page).
- Key info: LLM evaluators assign higher ratings to lower-perplexity text regardless of whether it is their own; own-family text has lower perplexity on average. Suggests the mechanism is familiarity/low perplexity, not only explicit self-recognition.
- Relation: EXTENDS 1.1. Family-disjoint judging reduces but does not remove stylistic-familiarity bias; reviewer reports normalised into one template (as the merge step does) reduce the style signal.
- Relevance: MEDIUM

### 1.4 "Same Text, Different Filename: Are LLM Judges Biased?" (arXiv 2611.01829)
- URL: https://arxiv.org/html/2611.01829v1 (extracted)
- Date: arXiv id 2611 = November 2026 (v1). Reliability: single-author preprint, not peer reviewed; MEDIUM-LOW. Model-behaviour evidence on three frontier LLMs, dated Nov 2026.
- Key info: three frontier LLMs score the same document differently when only the filename (author label) changes. A person-related label scores higher than no label; there is no consistent preference for own-family vs rival label, but a context-specific label bias remains whose direction and size vary with document and label. With LLM-written documents some self-premium appears.
- Relation to codebase: SUPPORTS blinding reviewer identity and panel identity from the grader (anonymised labels, no model names, neutral file names). Qualifies 1.1: label effect is real but inconsistent, so blinding is cheap insurance, not a proven fix for a specific direction. Directly relevant to the E2 judge leak of the combo name (codebase finding, research/11 section 2).
- Relevance: MEDIUM

### 1.5 Identity-bias guidance in a governance review (IIARD WJIMT, 2026)
- URL: https://iiardjournals.org/abstract?id=67971 (search snippet only; not extracted)
- Date: 2026. Reliability: low-tier journal review; LOW, snippet only.
- Key info: recommends blinding model identity, standardising formatting, removing provider-specific markers, reporting order-swapped agreement, length-adjusted scores and blinded-vs-unblinded differences, and testing across multiple judge families.
- Relation: EXTENDS the codebase: the panel can log a blinded-vs-unblinded score difference as a standing bias metric. Treat as practice guidance only.
- Relevance: LOW

## 2. Position, verbosity and other judge biases

### 2.1 Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023 Datasets and Benchmarks)
- URL: https://arxiv.org/abs/2306.05685 (html extract: https://arxiv.org/html/2306.05685v4); secondary summary of figures: https://www.honeyhive.ai/learn/mt-bench
- Date: 2023 (v4 current). Reliability: peer-reviewed. Model evidence is GPT-4/Claude-v1/GPT-3.5 era (2023); magnitudes should not be assumed for current models. Numeric figures below (65.0% consistency, 91.3%/8.7% verbosity failure, 10% and 25% self-enhancement win-rate gain) come from the secondary summary (HoneyHive), not from the extracted page; the extracted page confirms the bias categories, the >80% human agreement and that few-shot examples improve consistency (D.2).
- Key info: position bias, verbosity bias ("repetitive list" attack), self-enhancement bias and limited reasoning ability; mitigations: swap positions and count inconsistent results as ties, few-shot examples, chain-of-thought and reference-guided judging for maths/reasoning; GPT-4 agreed with humans at over 80%, similar to human-human agreement.
- Relation to codebase: SUPPORTS the grader design in the experiment (blind, frozen rubric) and EXTENDS it: reference-guided judging (a ground truth list) is the documented mitigation for limited judge reasoning. The E2 judge was given ground-truth.json, which matches this pattern. For binary "is this finding blocking" grading there is no pair to swap, so position bias applies to finding ORDER and rubric option order, not answer order (see 2.3).
- Relevance: HIGH

### 2.2 Ye et al., "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge" (CALM, ICLR 2025)
- URL: https://arxiv.org/abs/2410.02736 (also https://proceedings.iclr.cc/paper_files/paper/2025/file/fdca08d371e4b6c031397909e20043bd-Paper-Conference.pdf)
- Date: Oct 2024 preprint, ICLR 2025. Reliability: peer-reviewed. Snippets only (not extracted).
- Key info: 12 bias types (including position, verbosity, self-enhancement, fallacy oversight, sentiment, distraction) measured by automated bias injection; advanced judges (Claude-3.5, GPT-4o in that study) are reasonably robust on some tasks but significant biases persist in specific tasks.
- Relation: EXTENDS. A panel judge should be bias-tested with injected perturbations (swap order, pad, rename) on a small fixed set before it is trusted; the experiment's "frozen rubric" has no such test recorded in the codebase notes.
- Relevance: MEDIUM

### 2.3 "Am I More Pointwise or Pairwise? Revealing Position Bias in Rubric-Based LLM-as-a-Judge" (arXiv 2602.02219)
- URL: https://arxiv.org/abs/2602.02219 (extracted)
- Date: Feb 2026. Reliability: arXiv preprint (abstract extracted). Model behaviour evidence from 2026-era judges.
- Key info: rubric-based scoring behaves like multiple-choice: judges prefer score options at particular positions in the rubric list; direction is model-specific (some first, some last); the order of criteria in a multi-criterion prompt also shifts scores; permuting rubric option order attenuates the bias and only a small number of random permutations are enough for most models.
- Relation to codebase: DIRECTLY relevant to a frozen rubric and to reflect's 5-dimension (or troubleshoot's 6-dimension) calibration rubric: the order of dimensions and of score anchors is itself a source of bias. EXTENDS: freezing a rubric text does not freeze its bias; a few permutations of anchor order per grading run is a cheap control. Notes a possible tension: "frozen" rubric (stability) vs permuted option order (bias control) - freeze the content, permute the presentation.
- Relevance: HIGH

### 2.4 Verbosity and length: June 2026 21-judge study (arXiv 2606.19544) as described by a secondary blog
- URL: https://digitortoise.com/mt-bench-explained (secondary blog; arXiv 2606.19544 not extracted)
- Date: blog 2026; claim attributed to a June 2026 study. Reliability: blog (LOW); the underlying paper was NOT read. Do not rely on the number without reading the paper.
- Key info (as reported): verbosity bias comparatively small next to other error sources across 21 judges; always-A degenerate behaviour in 8 of 9 judges in the rubric study (2602.02219 above; that specific figure NOT confirmed by my extract of the abstract).
- Relation: UNVERIFIED context only; listed so the lead can decide whether to fetch the primary paper.
- Relevance: LOW

### 2.5 Biases in LLM judges for code evaluation (EACL 2026 Findings)
- URL: https://aclanthology.org/2026.findings-eacl.70.pdf (extracted, partial)
- Date: 2026. Reliability: peer-reviewed (Findings). Model evidence 2026-era judges.
- Key info: across five programming languages and multiple LLMs, all tested judges are susceptible to positive and negative biases from superficial code features (longer variable names, illusory complexity, dummy code) producing inflated or unfairly low scores; the judges stay vulnerable even when asked to generate test cases before scoring.
- Relation to codebase: relevant to the PR code review and rf-qa replacement modules (judging code or code-adjacent text): surface features can sway a judge, and "write a test first" is not a sufficient mitigation. SUPPORTS the codebase choice of requiring citations and evidence validation (file:line re-reads) instead of relying on a judge's reading of the text.
- Relevance: MEDIUM

## 3. Panels versus single judges (who judges)

### 3.1 Verga et al., "Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models" (PoLL)
- URL: https://arxiv.org/abs/2404.18796 (extracted)
- Date: submitted 29 Apr 2024. Reliability: arXiv preprint, widely cited. Model evidence from 2024 models (Command R, GPT-3.5, Haiku vs GPT-4).
- Key info: a panel of three smaller judges from disjoint model families outperforms a single large judge (GPT-4) on agreement with humans across three judge settings and six datasets, shows less intra-model bias, and costs over 7x less. Voting: max vote for binary correctness, average pooling for 1-5 scores. Secondary summaries (liner.com, alphaxiv) report GPT-4 judge prompt sensitivity (kappa 0.518 zero-shot vs 0.725 with prompt tuning) and that the highest positive delta for a model occurs when it judges itself. Panel selection (which models) is left as future work by the authors; evaluated only on QA-style correctness and Chatbot Arena, not code review.
- Relation to codebase: SUPPORTS using the existing heterogeneous reviewers as a panel and the class-disjoint rule; CONTRADICTS the single blind Opus judge as the one decider (one strong judge from one family is the configuration PoLL argues against), though the codebase judge is used to score panels offline, not to decide verdicts. EXTENDS: the "calibrator" does not have to be one extra agent; a vote among the reviewers themselves (agreement) plays the same role. Caveat: PoLL targets correctness scoring, not discovering defects; evidence for finding-generation panels is indirect.
- Relevance: HIGH

### 3.2 Practitioner guidance on judge ensembles (blog and Medium surveys)
- URLs: https://digitortoise.com/mt-bench-explained ; https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80 ; https://wandb.ai/site/articles/exploring-llm-as-a-judge
- Date: 2026. Reliability: blogs (LOW); snippets only.
- Key info: cross-family three-judge panels as a default at about 3x single-judge cost; a two-tier setup (cheap ensemble filters easy cases, strong judge or human adjudicates); disagreement between judges marks the cases that need human review; weight judges by held-out accuracy; log all judge inputs and outputs to detect drift.
- Relation: SUPPORTS the idea that reviewer disagreement is a signal (reflect already degrades on convergence < 0.80, contract.py). EXTENDS: weighting reviewers by measured accuracy on a labelled set (the E2 ground-truth packages could supply this).
- Relevance: MEDIUM

## 4. Rubric anchoring and blind grading

### 4.1 Rubric-guided LLM scoring vs human grading across three university courses (Applied Sciences 2026)
- URL: https://www.mdpi.com/2076-3417/16/12/5902
- Date: 2026. Reliability: peer-reviewed journal (MDPI), one institution, ChatGPT only, student text responses; transferability to code review is LOW.
- Key info: 930 responses scored on a five-criterion analytic rubric; human-human ICC 0.819, AI-vs-human-consensus ICC 0.763 with wide limits of agreement (about plus or minus 4 points of 15); a course-specific linear calibration on a 70/30 split modestly improved ICC (0.774 to 0.782) and MAE (1.624 to 1.215); agreement is stronger for concrete, well-anchored criteria than for ambiguous ones; conclusion: calibrated co-grading, not unsupervised replacement.
- Relation: SUPPORTS rubric anchoring with concrete criteria and held-out calibration; CAUTIONS that aggregate agreement does not guarantee case-level reliability, relevant to per-finding decisions.
- Relevance: LOW (domain mismatch), MEDIUM for the "calibrate on held-out split" pattern

### 4.2 Prompt design for LLM essay scoring: rubrics to calibration (NHSJS 2026)
- URL: https://nhsjs.com/2026/prompt-design-for-llm-essay-scoring-from-rubrics-to-calibration
- Date: 2026. Reliability: student-run journal (LOW); two models (DeepSeek-R1, Qwen2.5-7B), 5,099 segments.
- Key info: adding the rubric to the prompt did NOT consistently improve alignment (DeepSeek-R1 accuracy fell 37.6% to 29.8%); adding calibration constraints was the decisive factor (about 20-25 points).
- Relation: CONTRADICTS the assumption that a frozen rubric alone anchors a judge: rubric text can amplify extreme labels. EXTENDS: pair the rubric with a calibration step against labelled examples. Low reliability, weak evidence.
- Relevance: LOW

### 4.3 RULERS: rubric unification, locking and evidence-anchored scoring (aggregator summary, Jan 2026)
- URL: https://www.emergentmind.com/topics/rulers-rubric-unification-locking-and-evidence-anchored-robust-scoring
- Date: updated 20 Jan 2026. Reliability: aggregator summary of a preprint; primary paper not read (LOW-MEDIUM).
- Key info: compiles a natural-language rubric into an immutable executable bundle; an "evidence gate" requires verifiable extracted evidence before a score counts, with deterministic verification of quotes; post-hoc Wasserstein calibration maps model score distribution to human distribution without retraining.
- Relation to codebase: closely mirrors what the codebase already does structurally (mandatory evidence-validator re-reading file:line citations, frozen rubric) and supports putting the evidence gate in the shared core, with calibration as a separate optional post-hoc step.
- Relevance: MEDIUM

### 4.4 Blind vs informed grading: what the evidence says
- Sources: 1.1 (self-recognition is the mechanism), 1.4 (filename label shifts scores), 1.5 (blinded-versus-unblinded reporting).
- Finding: no source I found measured a "blind grader sees a merged report with provenance stripped" setup in a code or spec review context. Direct evidence that blinding improves grader accuracy in this setting was NOT found; the support is mechanistic (self-recognition, label effects) and from document-labelling experiments. Mark as an evidence gap.
- Relevance: HIGH (because it limits how strongly the panel design can lean on blinding)

## 5. Reliability of verbalized confidence

### 5.1 Xiong et al., "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs" (ICLR 2024)
- URL: https://arxiv.org/abs/2306.13063 (extracted; html https://arxiv.org/html/2306.13063v2)
- Date: 2023 preprint, ICLR 2024. Reliability: peer-reviewed. Models: GPT-3, GPT-3.5, GPT-4, Vicuna, LLaMA 2 Chat (2023-era).
- Key info: verbalized confidence is overconfident (values cluster at 80-100% in multiples of 5); GPT-4 has lower ECE but average AUROC for separating right from wrong answers of only about 62.7% (near the 50% coin-flip line); consistency across several sampled answers plus better aggregation mitigates this; the gap to white-box methods is narrow (AUROC 0.522 vs 0.605 in the abstract); no technique wins consistently and all struggle on tasks needing professional knowledge.
- Relation to codebase: SUPPORTS the observation that numeric per-finding confidence is a weak signal (and the finding that none were recorded is not a loss of reliable information). Verbalized numbers are bad at ranking findings (low AUROC) even where ECE looks acceptable, so a numeric calibrator score should not gate a blocking verdict on its own.
- Relevance: HIGH

### 5.2 Tian et al., "Just Ask for Calibration" (EMNLP 2023)
- URL: https://arxiv.org/abs/2305.14975 ; PDF https://aclanthology.org/2023.emnlp-main.330.pdf (extract of the PDF)
- Date: 2023. Reliability: peer-reviewed. Models: ChatGPT, GPT-4, Claude 1/2, Llama-2 (2023-era).
- Key info: for RLHF-tuned models, verbalized confidence is often better calibrated than token probabilities on TriviaQA, SciQ and TruthfulQA, often cutting ECE by a relative 50%; prompting the model to list several candidate answers before stating confidence improves calibration; temperature scaling on top helps; ECE alone cannot detect discriminative power (a coin-flip 50% guesser has perfect ECE on a binary task).
- Relation: CONTRADICTS 5.1 in direction on verbalized vs token confidence, with different metrics and datasets; both are 2023 evidence. For a panel on black-box APIs (no token probabilities), "ask for confidence after listing alternatives" is the documented prompting pattern; it supports a calibrator that must consider counter-hypotheses (reflect/troubleshoot rubrics already contain a competing-hypothesis style dimension, per research/05, not re-verified here).
- Relevance: MEDIUM

### 5.3 Sanz-Guerrero et al., "Large Language Models Are Overconfident in Their Own Responses" (arXiv 2606.03437)
- URL: https://arxiv.org/abs/2606.03437 (extracted)
- Date: submitted 2 Jun 2026. Reliability: arXiv preprint; six recent open-weight LLMs, three benchmarks, three elicitation methods (2026-era evidence, open-weight models only, not Claude).
- Key info: "ownership bias": models are up to 26% more confident in an answer presented as their own (assistant turn) than in the identical answer supplied by a user; framing the answer as user input during confidence elicitation improves calibration by up to 26% with no retraining.
- Relation to codebase: DIRECTLY relevant to calibration design. If a reviewer's own finding is re-graded by the same model in the same conversation (self-calibration), it will be over-trusted. The documented fix, handing the finding to the calibrator as external input in a fresh context, matches the confidence-calibrator agent's "strip the formation context" design (agent description in the task environment) and the class-disjoint rule. Evidence for open-weight models; transfer to Claude models is UNVERIFIED.
- Relevance: HIGH

### 5.4 Tian et al., "Overconfidence in LLM-as-a-Judge: Diagnosis and Confidence-Driven Solution" (arXiv 2508.06225)
- URL: https://arxiv.org/abs/2508.06225 (extracted); html https://arxiv.org/html/2508.06225v2
- Date: submitted 8 Aug 2025, last revised 18 Aug 2025. Reliability: arXiv preprint (some numbers below from the html snippet and a secondary social summary, not independently checked).
- Key info: judges' predicted confidence systematically overstates correctness (14 models picking the better of two answers; most confidence mass at 90-100% while accuracy lags); ECE misses the high- and low-confidence zones that matter operationally, so they propose TH-Score; they propose "LLM-as-a-Fuser", a dedicated model that reads several judges' verdicts and critiques and emits one verdict with confidence, reporting up to +47.14% accuracy and -53.73% ECE on JudgeBench versus baselines (html snippet). Self-score, 10-run vote share and token probability were the three confidence signals compared.
- Relation to codebase: SUPPORTS a design where the merge step is a fuser (adversarial merge reading all reviewers' rationales) rather than a vote count, and SUPPORTS accepting only high-confidence-zone decisions automatically while routing the rest to a human. Note the claim concerns pairwise judging, not finding triage.
- Relevance: HIGH

### 5.5 Ferrer et al., "When Can We Trust LLM Graders? Calibrating Confidence for Automated Assessment" (arXiv 2603.29559)
- URL: https://arxiv.org/abs/2603.29559 (extracted)
- Date: submitted 31 Mar 2026. Reliability: arXiv preprint; seven LLMs (4B to 120B parameters), three education datasets (not code review).
- Key info: self-reported confidence gave the best calibration (average ECE 0.166 vs 0.229 for self-consistency voting, which cost 5x more inference); larger models were better calibrated (best average ECE 0.100, AUC 0.668); confidence is strongly top-skewed so thresholds must be set relative to each model's observed confidence distribution, not at an intuitive midpoint.
- Relation: PARTLY CONTRADICTS 5.1 (here the cheap self-report beats voting on ECE, though AUC stays modest at 0.668). Both agree the signal is top-skewed and weakly discriminative. Operational consequence for the panel: any numeric threshold must be fitted per model, per prompt on logged data; there is no portable constant like "0.80".
- Relevance: MEDIUM

### 5.6 Calibration of judge confidence is itself task- and population-dependent
- URL: https://aclanthology.org/2025.findings-acl.293.pdf (snippet only)
- Date: ACL Findings 2025. Reliability: peer-reviewed; content moderation task, GPT-4o.
- Key info: even the best model assigns high confidence regardless of human annotator agreement; correlation between confidence and agreement drops from above 0.7 on unanimous items to below 0.3 on disagreement items; the authors recommend ensembles and human-AI collaboration instead of sole LLM decision-makers.
- Relation: SUPPORTS escalating to a human on the contested findings, which in the codebase is the reflect `needs_human_decision` / `user_decision_required` path. Domain (moderation) differs from code review.
- Relevance: LOW-MEDIUM

## 6. Calibration methods and where they apply

### 6.1 Post-hoc calibrators (Platt scaling, isotonic regression, temperature scaling)
- URLs: https://www.kdnuggets.com/a-deep-dive-into-calibration-of-language-models-platt-scaling-isotonic-regression-temperature-scaling ; https://futureagi.com/blog/evaluating-llm-confidence-uncertainty-2026 ; https://arxiv.org/html/2512.11150v1 (isotonic reward calibration for judge scores, "Causal Judge Evaluation")
- Date: 2026 (blog posts), Dec 2025 (arXiv 2512.11150). Reliability: blogs LOW; arXiv preprint for 2512.11150 (snippet only, not extracted).
- Key info: Platt scaling is a one-parameter logistic fit that suits monotone miscalibration; isotonic regression is non-parametric and handles odd curves but overfits small calibration sets (blogs cite roughly 1000+ examples for stability; one study in the Springer snippet below fitted isotonic on only 60 examples and warns about instability); fit on a calibration split, never the test split; refit when model, prompt or distribution changes; a blog claims Platt scaling on 200+ examples commonly cuts verbalized-confidence ECE by 30-60% (unverified marketing-style claim). 2512.11150 uses isotonic regression from judge score to an oracle label on a small labelled slice, with an automatic fallback for covariate-dependent bias such as response length.
- Relation to codebase: the codebase has 689 findings and some ground-truth packages (E2 ground-truth.json, per research/11), which is the order of magnitude where Platt scaling is feasible and isotonic is marginal, but only for a model-prompt pair that stays fixed. Because the panel's models change (fallback ladders, combo experiments), a fitted mapping goes stale quickly; this argues against a numeric calibrator in the shared core until the panel composition stabilises.
- Relevance: MEDIUM

### 6.2 Springer claim-level self-verification with isotonic calibration (Discover Artificial Intelligence, 2026)
- URL: https://link.springer.com/article/10.1007/s44163-026-02240-w (snippet only)
- Date: 2026. Reliability: peer-reviewed journal; small study.
- Key info: raw confidence from claim-level verification risk, isotonic regression fitted on 60 calibration examples, correctness judged by an LLM judge of the SAME model family used for generation and verification, which the authors flag as a source of correlated errors; calibrated ECE estimates carry wide intervals and binning sensitivity.
- Relation: a worked example of the failure mode the class-disjoint rule is meant to prevent (generator, verifier and grader from one family). SUPPORTS the rule; EXTENDS by showing even careful calibration inherits the correlated-error problem.
- Relevance: MEDIUM

### 6.3 Apollo Research, "Evaluating LLM Calibration for Coding-Agent Monitoring"
- URL: https://www.apolloresearch.ai/monitoring/evaluating-llm-calibration-for-coding-agent-monitoring (extracted)
- Date: not shown on the extracted page (post-2025, 16 judges including Gemini 3.x, per the page text); date UNVERIFIED. Reliability: vendor research blog (MEDIUM); synthetic injected failures; reference labels come from a multi-step multi-model pipeline, so results are relative, not absolute truth.
- Key info: judges differ systematically in severity (some score high, e.g. Gemini 2.5 Flash; Claude models more conservative); more capable models show lower spread; especially Anthropic models have very similar judgments, so highly correlated models add little value, and ensembles with monitors from different providers calibrate better; no single model fully matched the reference; recommends ensembles and multi-step pipelines (ensembles plus meta-graders) for high fidelity.
- Relation to codebase: SUPPORTS vendor-level (not just model-class-level) diversity for the calibrator: Opus and Sonnet judging each other are one correlated family. This sharpens the reflect rule "different model class than the reviewer": class-disjoint inside one vendor may not give independence. The contract already tracks `t2_vendor_diversity` (research/05 section 1.3), which is the right signal. It also shows per-model severity offsets exist, so a panel mixing models needs per-model severity anchoring or a rank-based merge rather than raw severity averaging.
- Relevance: HIGH

### 6.4 Code-review practice: confidence filters and adversarial review (practitioner blogs)
- URLs: https://dev.to/dextralabs/how-to-build-a-custom-ai-code-review-agent-for-proprietary-codebases-329c ; https://heym.run/blog/ai-code-review ; https://sourcegraph.com/blog/automated-code-review-tools ; https://hidekazu-konishi.com/entry/llm_output_verification_patterns.html
- Date: 2026. Reliability: blogs and vendor content (LOW); snippets only.
- Key info: common production pattern is a confidence filter between the review engine and the comment publisher, with category-specific thresholds, deterministic-rule findings passing unconditionally, suppressed findings logged to tune thresholds; precision is prioritised over recall for adoption; adversarial review (proposer, challenger on a different vendor, arbiter) is described as the remedy for single-reviewer false positives; a verification stack's false-negative rate is invisible unless a random sample of passing output is audited, and thresholds drift permissive under the one-sided pressure of visible false positives.
- Relation to codebase: SUPPORTS keeping calibration as a pluggable filter whose suppressed items are logged (the panel's telemetry role), and EXTENDS with a standing audit sample of items the panel passed or suppressed to measure the invisible error side. Nothing here is independent evidence of effectiveness; it is practice description.
- Relevance: LOW-MEDIUM

### 6.5 Evidence gap: judges for defect-finding panels
- Searches for a controlled study of heterogeneous reviewer panels merged by a fuser for code or specification review (not answer-correctness scoring) returned no primary source. The closest are PoLL (3.1, QA correctness), LLM-as-a-Fuser (5.4, pairwise judging) and the code-evaluation bias paper (2.5). The panel's merge-and-grade design is therefore an extrapolation from adjacent evidence; the project's own labelled packages are the real validation set.
- Relevance: HIGH (limits confidence in any external recommendation)

## Key External Findings

1. Self-preference is real but partly an artefact (HIGH). Panickssery et al. (NeurIPS 2024) tie it to self-recognition; a 2026 reanalysis (arXiv 2601.22548) attributes about 90% of the measured effect to judge uncertainty on hard items, with only 51% of earlier findings staying significant. Both point the same way for design: hide provenance AND use a strong, different-family judge. Neither alone is enough. Tested models are 2023-2026 era; Claude-specific current magnitudes are unmeasured here.
2. Blinding must cover panel identity, not only reviewer ids (HIGH, mechanistic). Author labels and filenames shift judge scores (arXiv 2611.01829, Nov 2026, single-author preprint). The E2 judge saw the combo name, which encodes models, so that "blind" result is only partly blind. Direct proof that blinding improves accuracy for a merged-report grader was not found (evidence gap).
3. Vendor diversity beats class diversity (HIGH). Apollo Research found Anthropic models' judgments highly correlated and cross-provider ensembles better calibrated; PoLL used disjoint model FAMILIES. "Different model class" inside one vendor is a weaker guarantee than the contract's vendor-diversity field.
4. Panels beat single judges on agreement and bias, but the evidence is for correctness scoring (HIGH). PoLL (2024): three smaller judges from three families beat GPT-4 and cost under one seventh. A single blind Opus judge is the single-large-judge setup PoLL argues against; no evidence was found for defect-discovery panels.
5. Verbalized numeric confidence is weakly discriminative (HIGH). Overconfident, clustered at 80-100% (Xiong 2024: AUROC about 62.7% for GPT-4), top-skewed (Ferrer 2026), and inflated by ownership bias up to 26% when a model grades its own answer in its own turn (Sanz-Guerrero 2026). Zero numeric calibrations recorded by the shadow runs is a small loss of evidence by this literature, not a failure.
6. Rubric text is not an anchor by itself (HIGH/MEDIUM). Rubric option order and criterion order shift scores in a model-specific direction; a few random permutations remove most of it (arXiv 2602.02219). A weak study (NHSJS 2026, LOW) found rubric-in-prompt did not help without calibration. Evidence gating (verify quoted evidence deterministically before a score counts, RULERS) is the better-supported anchor and is already how the codebase's evidence-validator works.
7. Post-hoc calibration needs labelled data and goes stale (MEDIUM). Platt scaling needs on the order of hundreds of labelled items and isotonic regression more; mappings must be refit when model or prompt changes. A fuser that reads the reviewers' rationales (arXiv 2508.06225) improved calibration more than simple voting in that study.
8. Judges are manipulable by surface features in code (MEDIUM). EACL 2026 Findings: variable-name length and meaningless extra code bias code judges; asking for test generation first did not fix it.

## Recommendations from External Research

(External research adds options; the codebase facts in research/05 and research/11 remain the source of truth.)

1. Do not make a numeric per-finding calibrator a required panel role in the shared core. Evidence for numeric verbalized confidence is weak and any fitted mapping is model- and prompt-specific. Prefer cheaper, better-supported signals: reviewer agreement (cluster support), the deterministic citation/evidence check, and a binary blocking decision. Keep the calibrator as an optional module (disabled by default) that logs raw outputs for later fitting.
2. If a calibrator or grader is kept, give it (a) a fresh context with the finding supplied as external input, never as its own prior turn (ownership bias); (b) a different VENDOR from the reviewer whose finding it grades, not just a different class; (c) a rubric whose option and criterion order is permuted across a small number of runs; (d) a blinded input: opaque labels, no model names, neutral file names, no panel/combo names in the schema or paths.
3. Treat the merge step as the fuser: a model that reads all reviewers' rationales and emits one decision outperformed vote counting in the one study found, and PoLL supports panel pooling. Keep reflect's existing degrade rules (single-reviewer fallback, low convergence) as the fallback when diversity is missing.
4. Treat judge quality as a measured property of the panel: run a small fixed bias battery (swap order, pad length, rename author labels, rename files) on each candidate judge before it is trusted, report blinded-vs-unblinded score differences, and log them in the telemetry role. Use the E2 ground-truth packages as the labelled set.
5. Keep a standing audit sample of findings the panel dropped or passed, to measure the false-negative side that thresholds otherwise hide.
6. Any numeric threshold (such as the 0.82/0.85 values in the Reuse-Miss rule, or the 0.80 convergence value) should be re-derived per model from logged data; external work shows confidence distributions are top-skewed and not portable between models.
7. For an offline panel-scoring judge (as in the E2 harness), use a different vendor from every reviewer in the panels being scored, or at least two judges from different vendors and report agreement; a single judge from the same vendor as a panel member reintroduces self-preference in the benchmark itself.
8. Flag as open: no external study of heterogeneous panels for defect-finding or specification review was found; validate on the project's own labelled data before treating any of the above as settled.

Discrepancies with codebase to note: (a) the codebase's class-disjoint rule is weaker than the vendor-diversity evidence suggests; (b) the E2 judge's schema leaked panel identity, which external evidence treats as a bias channel; (c) Tian et al. 2023 and Xiong et al. 2024 disagree on whether verbalized confidence is "good", so there is no consensus on which confidence signal to trust; all confidence-method studies cited here use 2023-2026 models and none tested the project's current model set.

Provider note: all searches and extractions used Tavily (mcp__litellm__Tavily-tavily_search / tavily_extract); WebSearch/WebFetch were not needed. Items marked "snippet only" were not extracted and carry lower reliability.
