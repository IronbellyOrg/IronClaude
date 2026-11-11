# Jev and similar judgment models: outside reports, and 10 more places to try them (2026-11-11)

## What others report (desk research; read the caveats first)

**Caveats.** One research agent with WebSearch only: Tavily wasn't available, and docs.typesafe.ai and several blogs were outside its network allowlist. Every figure below comes from **search-result summaries, not pages read in full**. Check each at its URL before relying on it.
- Reddit: the targeted searches found **no Reddit threads about Jev**, so we can't say what Reddit thinks.
- Hacker News: a large launch thread (item 49813136) exists, but the agent could not read it. Its content is known only second-hand.

| Pattern | Where it sits | Reported result | Evidence |
|---|---|---|---|
| Tool-call gate in a coding agent | Before a tool runs (risk / allow) and after it returns (is the goal met?). A static deny list runs first, so Jev is called only when that list doesn't decide | Using Jev as a command-safety classifier was reported as 5 to 18x faster than an OpenAI model, at 70 to 500 ms | One practitioner write-up (levelup.gitconnected) and an OpenRouter cookbook. The speed figures are company-adjacent |
| Policy stays in code | Not a use but a rule: the LLM proposes, Jev answers narrow questions, code decides | "Letting Jev authorize a refund moves the permissions problem into another probabilistic model" | Towards Data Science opinion piece |
| Model / skill routing | Per request: pick the model or skill, and decline a weak match | No outcome numbers | Community projects: pi-jev-router, duet-agent, jev-agent-skill-router |
| Judge / grader for evals | In place of an LLM judge on narrow rubric items | Braintrust: 78.1% vs 88.6% (GPT, 13x the cost). Arize: about 87% for both Jev and Opus on hallucination detection, at $0.05 vs $14.30 per 1k. MLflow: 88.9% vs 100% agreement on 72 items | Partner benchmarks |
| Claim verification with an error budget | Automate the confident cases; send the rest to a person or an LLM | 0.975 on 400 SEC-filing claims; at a 1% budget it automated 95% of cases at 1.6% held-out error, so over budget | Vals AI, independent. A possible shared investor is unconfirmed |
| Analogues | Claude Code auto-mode permission classifier; RouteLLM; distilled rerankers | RouteLLM: up to 85% cost cut on MT-Bench at about 95% of GPT-4 quality (check the baseline it is measured against). An independent stress test of auto mode: 81% false negatives under ambiguous authorization | Papers and vendor posts |

**Reported pitfalls.** These match what we measured.
- **Right type, wrong value.** A valid answer can still be wrong.
- **Calibration is task-specific.** Vals measured an expected calibration error (ECE) of 0.011 on claim verification but 0.108 on LegalBench.
- **Order bias.** Preprints report 2.6 to 5.4% of answers flipping with option order. We saw 41/46 (A2) and 50 to 51 of 52 (issue mode) unchanged.
- **It answers out-of-scope inputs unless asked.** PriorBench found it flagged 0 of 30 out-of-scope messages without an explicit "none" option. Fix: a companion Noul.
- **Behind frontier LLMs on hard reasoning.** It came last of 12 on a LegalBench slice, consistent with our A2 result.
- **Speed and cost.** Outside tests find the vendor's speed and cost claims about 5 to 6x smaller at the median.

## Our own record, for comparison

- **Works:**
  - **Short pairwise or single-item System One judgments.** Duplicate findings: AUC 0.98 to 0.99. Issue mode: 96%, and 45/45 outside the 0.3 to 0.7 band.
- **Fails:**
  - **Multi-hop judgments over a large document.** Covered: A1/A2/A3 and fix verification.
  - **Decisions from counts.** Covered: test 2 (the stop rule).
- Every proposal below keeps the decision in code, uses a Noul per judgment, has an offline test against data we already have, and falls back to today's path on an unclear answer.

## 10 more places to try Jev

| # | Where | Jev judgments (Noul unless noted) | Decision in code | Offline test from existing data | Value | Main risk |
|---|---|---|---|---|---|---|
| 1 | **PreToolUse hook for outward actions** (CLAUDE.md fork rule, staging `.claude/`, pushes) | After the regex deny list: "Does this command publish or send something outside the repo?" and "Does it target a repository other than `origin`?" | Block or ask only when a regex rule fails to decide AND p > 0.7 | Tool calls from session transcripts, labelled by the existing hooks' decisions plus a sample labelled by hand | Catches the bypasses CLAUDE.md warns about, such as `git add -f` hidden in scripts and gh without `--repo`, at about 300 ms per call | False negatives on ambiguous cases (the auto-mode paper's 81%). Must only ever add a block, never allow |
| 2 | **`/sc:recommend` and skill routing** | Choice over the skills, plus a companion Noul "Does any listed skill fit this request?" | Hand off when one skill clearly wins; otherwise run today's LLM recommend | Past `/sc:recommend` sessions (request and chosen skill) | Skips an LLM pass for clear requests | More than 255 skills needs two stages; a long option list invites order bias |
| 3 | **`/sc:pr-submit` review-comment triage** | Per Augment/Codex comment: "Does it point at code that is in the diff?" and "Does it describe a behaviour change rather than style?". Pairwise: "Do these two comments report the same problem?" (our proven dedup) | Merge duplicates; send only behaviour-change comments in the diff to the Medium+ verification and fix loop | Comments on merged PRs (#490, #491 and others) with their resolution | Fewer duplicate fix rounds and verifier calls | Never drop a comment, only order and merge them |
| 4 | **Evidence-validator pre-screen** (the troubleshoot and reflect citation gate) | Code fetches the cited file:line; Jev answers "Does the quoted line support the claim?" | Pass confident yes answers; send no or unclear to the evidence-validator agent | Past evidence-validator verdicts | Fewer validator tokens on obviously grounded citations | Weak on multi-hop claims, so keep it to one cited line per claim |
| 5 | **`/sc:issue --create` duplicate detection** | Pairwise "Does issue A ask for the same change as issue B?" over candidates the T3 scout already lists | Show likely duplicates; never block a filing | The 93 repo issues, plus closed-as-duplicate links | Fewer duplicate issues; reuses the dedup result | Small corpus, so few positives to test on |
| 6 | **Memory and KNOWLEDGE.md loading** | Per entry: "Is this memory relevant to the current task?" (vendor cookbook: classifying RAG passages) | Load only relevant entries | Sessions where a memory was cited, as positives | Fewer context tokens at session start | Misses silently, so keep always-loaded rules out of scope |
| 7 | **Tier choice for issue workers and ccsession** | Atomic task facets: "Does it touch more than one package?", "Does it need a design decision?", "Is it a text-only change?" | A code table maps facets to a tier; escalate on failure (the RouteLLM lesson) | `/sc:implement` retry ledgers (tier and outcome); count them first | Fewer expensive-tier runs on easy tasks | Judging a hard task as easy; needs the escalation path |
| 8 | **Pre-screen for cliEval and eval-suite grading** | Per binary rubric item: "Does the output do X?" | Accept confident answers; send the 0.3 to 0.7 band to the LLM judge | Existing eval runs with LLM-judge verdicts | Cheaper eval sweeps (partner data: 10 to 280x cheaper) | Partner benchmarks show it 0 to 10 points less accurate; calibrate per suite |
| 9 | **`/sc:task` compliance-tier classification** | Per signal from the tier rubric (for example "Does the task change security-sensitive code?") | Existing rubric code combines the signals | **`/sc:validate-tests` YAML specs are ready-made labels** | Deterministic, auditable tiering at negligible cost | Rubric signals that need repository context become multi-hop |
| 10 | **CI failure triage in `/sc:pr-submit`** | Per known failure class, over the extracted log excerpt: "Is this a network or proxy failure?", "a flaky timeout?", "an assertion failure in changed code?" | Retry the infrastructure classes once; send assertion failures to the fix loop | Past CI logs on PRs with their real cause | Fewer wasted fix rounds on infrastructure noise | Long logs: send only the extracted error block |

Suggested order: 9 (labels exist), 3 and 5 (reuse proven dedup), then 1 (safety, add-only), then the rest. Before each one: an offline test against labels, a code baseline, an option-order check, and a pre-registered bar.

## Sources (from the research agent; not fetched)

Vals AI <https://www.vals.ai/blogs/independent-evaluation-of-jev>; PriorBench <https://github.com/priorbench/jev>; eight-day review <https://dev.to/aws-builders/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1c60>; Braintrust <https://www.braintrust.dev/evals/jev-vs-gpt-eval-judges>; Arize <https://arize.com/blog/jev-as-a-judge.md>; MLflow <https://mlflow.org/blog/jev-llm-judge-part-2/>; TDS <https://towardsdatascience.com/can-typesafes-jev-make-ai-agents-safer-without-another-llm/>; harness write-up <https://levelup.gitconnected.com/decision-models-inside-an-agent-harness-4f605b4d1ef2>; OpenRouter cookbook <https://openrouter.ai/docs/cookbook/building-agents/gate-tool-calls-with-jev.md>; RouteLLM <https://lmsys.org/blog/2024-07-01-routellm/>; auto-mode stress test (arXiv 2604.04978); Zheng et al. 2023 <https://arxiv.org/abs/2306.05685>; HN launch thread <https://news.ycombinator.com/item?id=49813136> (not read).
