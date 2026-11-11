# Research prompts: better review and remediation pipelines

Three self-contained prompts. Each one embeds the same background block, so any of them can be pasted alone. They name no project, repository or person.

---

## Prompt 1: easily adaptable methods (testable on the existing framework this week)

**ROLE.** You are a research analyst. Find evidence, not opinions. Never invent a source. If you cannot find evidence for a claim, say so.

**BACKGROUND (our own measurements; treat as facts about our system, not as literature).**
We run an LLM-driven review-and-remediation loop on long requirements and architecture documents. The test document is real: 57 KB, about 285 lines. Workers are Sonnet-class LLM agents following markdown instructions. The loop is capped at 3 reviews and 2 fix cycles: review, then revise only the blocking findings, then re-review scoped to the changed lines plus the prior blockers, and so on. It ends in PASS, FAIL or escalate to a human.
What we measured (15 runs, 3 arms):
- Original setup: coordinator prompts told reviewers "assume defects remain / any finding of any severity is FAIL" and told revisers "apply all findings". 0 of 3 loops converged. The document grew 56 to 79%. About 1.25M output tokens per run. The final independent whole-document audit was clean in 2 of 3.
- New setup: severity is graded by consequence. A finding is blocking only if it names a concrete wrong outcome, a data-loss or security risk, or a contradiction between two stated texts. Medium and minor findings never trigger edits. Re-review is scoped. The reviser may touch only named blocking ids and prefers deleting. Result: 12 of 12 loops converged in 3 reviews or fewer, growth about 1%, about 0.33M tokens. But an independent whole-document audit of the final document still found 1 to 3 blocking defects in 10 of 12. The same three themes recurred: contradictions between sections, an acceptance check that cannot pass, and a path rule that collides with per-item rows. Different runs' first reviews caught different subsets of those defects.
Other lessons:
1. Re-reviewers confused which file was the candidate and which the baseline until we forced a mechanical evidence block (diff plus a grep self-check).
2. A prior PASS can regress, and a scoped re-review misses it unless the diff is quoted verbatim.
3. Where an instruction lives matters: in the command 3 of 3, in a routing doc 3 of 3, in a separate rules file 2 of 3 until it was refactored to a single home with a hard gate.
4. Clean documents were over-blocked on ambiguities until reviewers had to write "an implementer who follows the stated text builds X, and X is wrong because Y".
5. Scoring by grepping agent transcripts produced false positives.
6. One first review in six PASSed an unrevised document that the audit later failed.
7. Samples are small (3 to 6 per cell) and noisy.
Constraints: prose and markdown commands run by agents in Claude Code. No model fine-tuning. Token cost matters. Findings must be auditable and fail closed.

**GOAL.** Find methods or theories that we could adopt by changing prompts, policy text, the order of steps, or the sampling of reviews. No new infrastructure. We must be able to A/B test each one in our existing harness (same document, 3 to 6 replicates per arm).
You must cover this specific candidate: after a scoped PASS, run one labelled whole-document first review as a separate step. Any blockers it finds start a new bounded loop. Find how others handle "scoped review versus full review", "final full pass", "release gate" or "merge queue" analogs, and stopping rules.

**TOPICS TO COVER (not exhaustive).**
- Sampling several independent first reviews and merging them (self-consistency, union with deduplication). What k is worth the cost?
- Checklist or rubric-driven review, and calibration of severity grades.
- A verify-before-fix pass on each finding (a second agent confirms or rejects).
- Reviser edit minimization: patch or diff-based edits, deletion over addition.
- Evidence-or-drop rules for findings; confidence thresholds; position and verbosity bias in LLM judges.
- Stopping and escalation rules; budget-aware loops.
- Known failure modes of self-critique and self-refine loops, including results where LLMs cannot self-correct without external feedback.
- Practices from human code review and software inspection that transfer to LLM reviewers.

**WHERE TO LOOK.** Academic papers (arXiv and conference proceedings), engineering blogs, conference talks and video transcripts (YouTube), Reddit (r/ClaudeAI, r/LocalLLaMA, r/MachineLearning, r/ExperiencedDevs, r/softwaretesting), Hacker News threads, and GitHub projects including issues and discussions. Prefer code you can read over descriptions of code.

**SEARCH METHOD.** Use at least 15 distinct queries, mixing terms such as "LLM self-refine loop convergence", "multi-agent code review false positives", "reviewer severity calibration LLM", "whole document audit after incremental review", "verify then fix agents", "self-consistency review merge". For each source note the date; prefer the last 24 months unless it is foundational.

**SELECTION.** Keep a source only if it gives a mechanism, a measurement, or runnable code. Drop generic prompt-engineering listicles. Drop vendor marketing without data. Keep negative results.

**OUTPUT.** Return:
1. A ranked table of 10 to 15 techniques. Columns: name; one-sentence mechanism; source URL and date; evidence grade (A replicated empirical, B single study or benchmark, C practitioner report, D opinion); expected effect on residual blocking defects, document growth, tokens and convergence; cost to adopt (hours); main risk.
2. For the top 5: a concrete A/B test design in our harness (arms, replicates, metric, what result would make us drop it), and the exact change to the prompt or step order.
3. A section on the follow-up whole-document step: what the evidence says about its design (who runs it, how many blockers trigger a new loop, how to cap it).
4. A list of what you searched and found nothing for.
Quote no more than 25 words from any source. Mark anything you could not open as UNVERIFIED. Do not fabricate links.

---

## Prompt 2: medium to heavy refactors that fit the current architecture

**ROLE.** You are a research analyst. Find evidence, not opinions. Never invent a source. If you cannot find evidence for a claim, say so.

**BACKGROUND (our own measurements; treat as facts about our system, not as literature).**
We run an LLM-driven review-and-remediation loop on long requirements and architecture documents. The test document is real: 57 KB, about 285 lines. Workers are Sonnet-class LLM agents following markdown instructions. The loop is capped at 3 reviews and 2 fix cycles: review, then revise only the blocking findings, then re-review scoped to the changed lines plus the prior blockers, and so on. It ends in PASS, FAIL or escalate to a human.
What we measured (15 runs, 3 arms):
- Original setup: coordinator prompts told reviewers "assume defects remain / any finding of any severity is FAIL" and told revisers "apply all findings". 0 of 3 loops converged. The document grew 56 to 79%. About 1.25M output tokens per run. The final independent whole-document audit was clean in 2 of 3.
- New setup: severity is graded by consequence. A finding is blocking only if it names a concrete wrong outcome, a data-loss or security risk, or a contradiction between two stated texts. Medium and minor findings never trigger edits. Re-review is scoped. The reviser may touch only named blocking ids and prefers deleting. Result: 12 of 12 loops converged in 3 reviews or fewer, growth about 1%, about 0.33M tokens. But an independent whole-document audit of the final document still found 1 to 3 blocking defects in 10 of 12. The same three themes recurred: contradictions between sections, an acceptance check that cannot pass, and a path rule that collides with per-item rows. Different runs' first reviews caught different subsets of those defects.
Other lessons:
1. Re-reviewers confused which file was the candidate and which the baseline until we forced a mechanical evidence block (diff plus a grep self-check).
2. A prior PASS can regress, and a scoped re-review misses it unless the diff is quoted verbatim.
3. Where an instruction lives matters: in the command 3 of 3, in a routing doc 3 of 3, in a separate rules file 2 of 3 until it was refactored to a single home with a hard gate.
4. Clean documents were over-blocked on ambiguities until reviewers had to write "an implementer who follows the stated text builds X, and X is wrong because Y".
5. Scoring by grepping agent transcripts produced false positives.
6. One first review in six PASSed an unrevised document that the audit later failed.
7. Samples are small (3 to 6 per cell) and noisy.
Constraints: prose and markdown commands run by agents in Claude Code, plus a Python CLI that already runs deterministic multi-step pipelines (sprint, roadmap and similar). No model fine-tuning. Token cost matters. Findings must be auditable and fail closed.

**GOAL.** Find methods or theories that need medium to heavy refactoring but stay compatible with that architecture: markdown commands and agents, plus Python helpers and CLI pipelines. We are willing to add deterministic scripts, persistent files and new agent roles. We are not willing to replace the platform.

**TOPICS TO COVER (not exhaustive).**
- Role separation with independent contexts: reviewer, verifier or adjudicator, reviser, auditor. Heterogeneous models as reviewers; multi-agent debate and adversarial verification, including where they fail.
- A persistent finding ledger with typed statuses (open, resolved, regressed, deferred), stable ids and an explicit state machine, so identity and counts are mechanical rather than model-judged.
- Mechanical pre-checks before the LLM reads: extraction of counts, ids, section references and cross-references into structured data and automatic consistency checks (requirements linting, traceability matrices, link and reference checkers).
- Change-impact analysis for scoped review: using a dependency graph so a scoped re-review also covers the text that depends on the changed lines.
- Coverage maps: recording which parts of a document each reviewer actually examined, and routing the next review to the uncovered parts.
- Metamorphic or property-based testing applied to specifications and to review quality itself, including seeding known defects to measure recall.
- Monotone convergence arguments: designing the loop so a progress measure can only improve, and what to do when it does not.
- How CI review bots and code-review systems structure triage, deduplication, suppression and re-review (look at open-source code review bots, Gerrit-style and merge-queue practices).

**WHERE TO LOOK.** Academic papers (arXiv and conference proceedings), engineering blogs, conference talks and video transcripts (YouTube), Reddit (r/ClaudeAI, r/LocalLLaMA, r/MachineLearning, r/ExperiencedDevs, r/softwaretesting, r/devops), Hacker News threads, and GitHub projects including issues and discussions. Prefer code you can read over descriptions of code. Read the implementation of at least 5 open-source projects and say what they do differently from the description in their README.

**SEARCH METHOD.** Use at least 20 distinct queries, for example "finding ledger LLM review state machine", "requirements consistency checker cross reference extraction", "change impact scoped re-review", "multi-agent debate verification failure modes", "seeded defect recall review", "LLM code review bot deduplication suppression". Note the date of every source; prefer the last 24 months unless foundational.

**SELECTION.** Keep a source only if it gives a mechanism, a measurement, or runnable code. Drop generic listicles and unsupported vendor claims. Keep negative results and post-mortems.

**OUTPUT.** Return:
1. A ranked table of 8 to 12 designs. Columns: name; mechanism; source URL and date; evidence grade (A replicated empirical, B single study or benchmark, C practitioner report, D opinion); which of our measured problems it addresses (residual blockers after PASS, growth, tokens, convergence, role confusion, regression misses, review-to-review variance); refactor size (files and components touched, rough days); compatibility risks with markdown-plus-CLI architecture.
2. For the top 3: a minimal design sketch (components, files, state transitions, what is deterministic and what is LLM-judged), an incremental migration path that keeps the current loop working at each step, and an experiment that compares it with our current setup using the same document and at least 6 replicates.
3. A comparison of what mechanical checks could have caught the three recurring defect themes above without an LLM.
4. A list of what you searched and found nothing for.
Quote no more than 25 words from any source. Mark anything you could not open as UNVERIFIED. Do not fabricate links.

---

## Prompt 3: outside-the-box approaches that may justify re-architecting

**ROLE.** You are a research analyst. Find evidence, not opinions. Never invent a source. If you cannot find evidence for a claim, say so. Treat any names or approaches in this prompt as leads to verify, not as facts.

**BACKGROUND (our own measurements; treat as facts about our system, not as literature).**
We run an LLM-driven review-and-remediation loop on long requirements and architecture documents. The test document is real: 57 KB, about 285 lines. Workers are Sonnet-class LLM agents following markdown instructions. The loop is capped at 3 reviews and 2 fix cycles: review, then revise only the blocking findings, then re-review scoped to the changed lines plus the prior blockers, and so on. It ends in PASS, FAIL or escalate to a human.
What we measured (15 runs, 3 arms):
- Original setup: coordinator prompts told reviewers "assume defects remain / any finding of any severity is FAIL" and told revisers "apply all findings". 0 of 3 loops converged. The document grew 56 to 79%. About 1.25M output tokens per run. The final independent whole-document audit was clean in 2 of 3.
- New setup: severity is graded by consequence. A finding is blocking only if it names a concrete wrong outcome, a data-loss or security risk, or a contradiction between two stated texts. Medium and minor findings never trigger edits. Re-review is scoped. The reviser may touch only named blocking ids and prefers deleting. Result: 12 of 12 loops converged in 3 reviews or fewer, growth about 1%, about 0.33M tokens. But an independent whole-document audit of the final document still found 1 to 3 blocking defects in 10 of 12. The same three themes recurred: contradictions between sections, an acceptance check that cannot pass, and a path rule that collides with per-item rows. Different runs' first reviews caught different subsets of those defects.
Other lessons:
1. Re-reviewers confused which file was the candidate and which the baseline until we forced a mechanical evidence block (diff plus a grep self-check).
2. A prior PASS can regress, and a scoped re-review misses it unless the diff is quoted verbatim.
3. Where an instruction lives matters: in the command 3 of 3, in a routing doc 3 of 3, in a separate rules file 2 of 3 until it was refactored to a single home with a hard gate.
4. Clean documents were over-blocked on ambiguities until reviewers had to write "an implementer who follows the stated text builds X, and X is wrong because Y".
5. Scoring by grepping agent transcripts produced false positives.
6. One first review in six PASSed an unrevised document that the audit later failed.
7. Samples are small (3 to 6 per cell) and noisy.
Constraints today: prose and markdown commands run by agents in Claude Code, plus a Python CLI for deterministic pipelines; no model fine-tuning. For this prompt you may assume we are willing to re-architect parts of the system if the evidence is strong.

**GOAL.** Find the most promising unconventional methods or theories for structuring review and remediation. We expect some to require re-architecting how documents are represented, how defects are modelled, or how loops are controlled. Rank by promise, not by ease.

**LEADS TO INVESTIGATE (verify each; add your own).**
- Representing a specification as structured claims or constraints and checking consistency with a solver or model checker (SMT, Alloy, TLA+, Lean or similar), with an LLM translating text to constraints. What happens when the translation is wrong?
- Verifier-in-the-loop search: generate several revision candidates and select with a verifier (best-of-n, tree search, beam search over edits). Process supervision and reward models for review steps.
- Estimating how many defects remain unfound: capture-recapture and species-richness estimators (for example Lincoln-Petersen or Chao-style estimators) applied to the defect sets found by independent reviewers, and software-inspection literature on defect-count estimation. Could this give a principled stop rule instead of a fixed cap of 3?
- Control theory and fixed-point arguments for loops: contraction, monovariants and potential functions, dead bands, and what guarantees a review-revise loop terminates at a correct fixed point.
- Reviewer reliability modelling: item-response theory or Bayesian models of reviewer sensitivity and specificity, with independent and correlated errors; diversity as redundancy (N-version ideas for reviewers).
- Scalable oversight ideas: debate, critique models trained to find flaws in outputs, weak-to-strong supervision. What transfers to prompting-only systems?
- Executable specifications: examples and acceptance tests as the primary artifact, with the prose as a derived view; example mapping and specification by example; generating tests from the document to expose contradictions.
- Treating the document as a typed program: a requirements DSL that compiles, with a type-checker for cross-references, counts and path rules.
- Agent architectures that separate planning, editing and verification (for example architect/editor splits, SWE-style agents, graph-based orchestration frameworks) and what their published evaluations say about review loops.
- Human-factors results on inspection (Fagan-style inspections, reading techniques such as perspective-based and checklist-based reading) and whether they carry over to LLM reviewers.

**WHERE TO LOOK.** Academic papers (arXiv and conference proceedings), engineering blogs, conference talks and video transcripts (YouTube), Reddit (r/MachineLearning, r/LocalLLaMA, r/ClaudeAI, r/formalmethods, r/ExperiencedDevs), Hacker News threads, and GitHub projects including issues and discussions. Prefer implementations and benchmarks over position papers. Read the code of at least 5 projects.

**SEARCH METHOD.** Use at least 25 distinct queries across the leads above. Record dates. Include foundational work regardless of age, and prefer the last 24 months for LLM-specific results.

**SELECTION.** Keep a source only if it gives a mechanism with a measurement, or runnable code, or a clear theoretical guarantee with stated assumptions. Drop hype. Keep negative results, failed replications and critiques.

**OUTPUT.** Return:
1. A ranked list of 6 to 10 approaches. For each: mechanism; sources with URLs and dates; evidence grade (A replicated empirical, B single study or benchmark, C practitioner report, D theory only); what it would change in our architecture (representation, control flow, state, tooling); what it would fix among our measured problems and what it would not; cost and risk of adopting it; the cheapest experiment that could falsify it on our test document.
2. A one-page recommendation: the single most promising direction, the second most promising, and what to rule out, with reasons.
3. An explicit statement of which of our own findings these approaches contradict or would overturn, if any.
4. A list of what you searched and found nothing for.
Quote no more than 25 words from any source. Mark anything you could not open as UNVERIFIED. Do not fabricate links.
