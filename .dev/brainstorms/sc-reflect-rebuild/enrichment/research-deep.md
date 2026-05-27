# Research: Rebuild /sc:reflect — Deep Context

## Executive Summary

**Topic 1 — Serena MCP tool surface:** The `think_about_*` triad (`think_about_task_adherence`, `think_about_collected_information`, `think_about_whether_you_are_done`) is **current, not deprecated** — they ship in Serena's default 18-tool MCP surface as of Aug 2025 and remain documented in Dec 2025 Japanese/English community guides. They are under-leveraged "meta-cognition checkpoints," not symbolic tools. The modern symbolic surface (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `replace_symbol_body`, `insert_after_symbol`, `insert_before_symbol`, `replace_regex`/`replace_content`, `write_memory`, `read_memory`) is the primary value-add and is what reflection workflows should orchestrate. Recommend: keep the `think_*` tools as lightweight intra-turn nudges but build the heavy reflection logic around `find_referencing_symbols` + `get_symbols_overview` + `read_memory` for evidence gathering, and `write_memory` for cross-session persistence.

**Topic 2 — Multi-agent verification:** ICLR 2025 blogpost benchmark of 5 MAD frameworks across 9 benchmarks shows MAD does **not consistently beat self-consistency** without careful tuning — naive MAD is often overly aggressive and erases correct answers. Key positive finding from Khan et al. (ICML 2024 Oral) and the NeurIPS 2024 scalable-oversight paper: **weak judges + strong persuasive debaters outperform strong judge + weak debaters**. This validates a "cheap merge model adjudicating between heterogeneous frontier critics" architecture. Heterogeneous ensembles consistently outperform homogeneous-cheap stacks (Gensyn HDEE, LLM-TOPLA focal-diversity work). Reflexion (Shinn 2023) is still cited as the canonical pattern but its single-agent variant has documented "Degeneration of Thought" failure modes — successors are CRITIC (Gou 2024), Self-Refine (Madaan 2023), MACA (ICLR 2026 submission), and Agent-as-Judge (Zhuge 2024/2025).

**Topic 3 — Pre-execution validation:** Plan-quality validation is converging on "spec-as-source-of-truth + LLM-as-judge over coverage matrix." Microsoft Azure AI Content Safety ships a "Task Adherence" feature (preview, late 2025) that **explicitly validates agent plans before tool calls** — the exact UC-1 pattern. NASA's MBSE+LLM traceability work (Sept 2025) reports going from 35%→67% coverage and 76.7%→92% accuracy by integrating LLMs into requirement traceability. The Kitchen Loop paper (2026) formalizes "user-spec-driven development" with structural enforcement (tests that cannot be skipped). LangGraph 1.0 (Oct 2025) is the production-preferred orchestrator with explicit conditional edges for pre-execution gates.

**Topic 4 — Post-execution review:** AI code review tools converged on 42–48% bug-detection rates (CodeRabbit 46%, Cursor Bugbot 42%, Qodo 42–48%, Greptile 85% with sub-3% FP) vs <20% for traditional SAST. **Self-confirmation bias is structurally unavoidable in single-model self-review** — "the same representational biases that produced the error are present when it re-evaluates" (Towards AI 2026). The mature pattern is: independent reviewer using a different model class, "spec drift" detection (Kinde 2025) treats spec as source of truth and regenerates code to conform, and a "validated-deviation taxonomy" distinguishing authorized vs unauthorized drift. METR RCT (July 2025) found AI tooling slowed experienced devs by 19% despite predicted 24% speedup — review discipline matters more than raw generation.

**Topic 5 — Skill design + eval harness:** Anthropic's Skill Creator 2.0 (Oct 2025–Mar 2026) shipped 4 modes (Create, Eval, Improve, Benchmark) with four composable parallel sub-agents (grader, comparator, analyzer + skill-creator). Test cases are JSON files pairing a realistic user prompt with verifiable assertions. Anthropic's published guidance: **start with evaluation** — identify capability gaps by running on representative tasks first, then build skills incrementally. Inter-rater reliability for LLM graders: Arize and Evidently both recommend a **different, more capable model as judge** (Sonnet/Opus judging Haiku, not Haiku judging Haiku). 0–5 grading scales show highest human-LLM alignment (Anthropic 2025 study). Avoid 100% pass rate — 70% on a rigorous evaluator beats 100% on a soft one.

---

## Topic 1: Modern Serena MCP — Best Practices

### 1.1 Tool inventory (current as of 2025-08 / 2025-12)

Per GitHub issue oraios/serena#494 log dump (Aug 2025) and the Dec 2025 hatena blog confirmation, Serena's MCP server exposes **18 tools by default**, with up to 36 loaded in the agent's internal registry:

Active MCP tools (18):
- **Discovery**: `list_dir`, `find_file`, `search_for_pattern`, `get_symbols_overview`, `find_symbol`, `find_referencing_symbols`
- **Symbolic editing**: `replace_symbol_body`, `insert_after_symbol`, `insert_before_symbol`
- **Memory**: `write_memory`, `read_memory`, `list_memories`, `delete_memory`
- **Onboarding/lifecycle**: `check_onboarding_performed`, `onboarding`
- **Meta-cognition (the "think" trio)**: `think_about_collected_information`, `think_about_task_adherence`, `think_about_whether_you_are_done`

Additional tools loaded but not always MCP-exposed (36 total): `read_file`, `create_text_file`, `replace_regex`, `delete_lines`, `replace_lines`, `insert_at_line`, `restart_language_server`, `execute_shell_command`, `activate_project`, `remove_project`, `switch_modes`, `get_current_config`, `summarize_changes`, `prepare_for_new_conversation`, `initial_instructions`, `jet_brains_find_symbol`, `jet_brains_find_referencing_symbols`, `rename_symbol`, `edit_memory`. [oraios/serena#494; CLOVER hatena 2025-12-07]

### 1.2 Are the `think_about_*` tools deprecated?

**No.** They are documented as current tools in:
- Dev.to Mar 2025 guide ("Thinking tool for pondering the completeness of collected information")
- Qiita 2025 deep-dive (categorized under 「思考・分析ツール」)
- CLOVER hatena Dec 7, 2025 (still in default 23-tool ide-assistant context)
- vibetools.net "Detailed User Guide" 2025

Official Serena documentation positions them as agent-loop guard rails: "Serena does not usually get lost (unlike some other agents that summarize under the hood), and it is also instructed to occasionally check whether it's on the right track" [oraios.github.io / MCP Marketplace mirror]. The three tools map to three reflection moments:
- `think_about_collected_information` → after evidence-gathering, before synthesizing a plan
- `think_about_task_adherence` → mid-execution drift check
- `think_about_whether_you_are_done` → completion gate

**Why "under-leveraged":** these tools return prompts/instructions to the model rather than computing anything — they're cheap nudges. Most workflows skip them because the model self-reflects implicitly. For a reflection-protocol skill, they should be **explicit, scripted checkpoints** rather than optional self-nudges.

### 1.3 Best-practice patterns for the symbolic surface

**`get_symbols_overview` → `find_symbol` → `find_referencing_symbols`** is the canonical exploration chain. Anthropic Opus 4.6 testimonial (oraios docs): "Serena's IDE-backed semantic tools are the single most impactful addition to my toolkit – cross-file renames, moves, and reference lookups that would cost me 8–12 careful, error-prone steps collapse into one atomic call." [oraios.github.io/serena/01-about/]

**Symbolic editing primitives**:
- `replace_symbol_body` — atomic, semantic, less error-prone than line-based edits
- `insert_after_symbol` / `insert_before_symbol` — precise insertion without LSP race
- `replace_regex` / `replace_content` — fallback for non-symbolic content (markdown, configs)

**Memory pattern** (oraios docs, MCP Marketplace mirror):
> "Serena has a dedicated tool to create a summary of the current state of the progress and all relevant info for continuing it. You can request to create this summary and write it to a memory. Then, in a new conversation, you can just ask Serena to read the memory and continue with the task."

**Memory naming convention** (observed in DEV community guide and `.serena/memories/` directories): kebab-case or snake_case task scoping, e.g. `task_completion_guidelines.md`, `project_structure.md`. No formal naming spec — community convention only.

### 1.4 Known anti-patterns / pitfalls

1. **Project activation race conditions** — must call `activate_project` (or use `--project $(pwd)` at startup) before any symbolic tool; otherwise Claude Code "tries to use normal bash commands" and bypasses Serena. [Qiita 2025 「アクティベートを忘れがち」]
2. **LSP/language-server bootstrap failures** — Serena issue #354 documents `npm install` failures for TypeScript LSP when run under fnm/nvm-managed Node; `restart_language_server` is the documented escape hatch.
3. **Memory file proliferation** — onboarding can create duplicate memories; "定期的に人間が監視・整理することをお勧めします" (recommend periodic human curation). [Qiita 2025]
4. **`execute_shell_command` security surface** — Serena defaults to enabling this in Claude Desktop/Code; vibetools.net flags this: "Since this executes arbitrary commands, review parameters carefully. For analysis-only mode, set `read_only: true` in project config."
5. **Context limit and re-summarization** — long sessions should use `prepare_for_new_conversation` to checkpoint, then `read_memory` in a fresh session. Avoids implicit summarization drift. [oraios docs]
6. **`.serena/` must be gitignored** — stores memories that pollute git history if tracked. [James Acres blog 2025-05]

### 1.5 Real-world reflection/validation workflows on Serena

Direct community examples are thin — Serena is most commonly used as a coding-tool augmentation rather than a reflection scaffold. The closest analog is the Serena-managed "memory of project structure + task completion guidelines" pattern, where `write_memory` after onboarding establishes a project contract that subsequent sessions verify against via `read_memory`. This maps cleanly onto reflection: the "spec" can be written as a memory and re-read by reviewer agents.

---

## Topic 2: Multi-agent / Multi-model Verification

### 2.1 Does multi-agent debate actually beat single-agent self-review?

**Mixed evidence, with conditions.** The ICLR 2025 blogpost "Multi-LLM-Agents Debate - Performance, Efficiency, and Scaling Challenges" (Smit et al. follow-up) evaluated 5 MAD frameworks across 9 benchmarks and concluded:

> "current MAD methods fail to consistently outperform simpler single-agent strategies, even with increased computational resources... Self-Consistency effectively minimizes the frequency of errors while correcting a significant number of wrong answers. In contrast, while Multi-Persona and AgentVerse sometimes achieve comparably tall green bars, these methods often fail to preserve correct answers. This suggests that MAD methods can be overly aggressive, lacking the ability to reliably identify incorrect answers."

[d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159]

**However**, controlled debate with explicit role separation (judge vs debater) and persuasion optimization does help:
- **Khan et al., ICML 2024 Oral**: "debate consistently helps both non-expert models and humans answer questions, achieving 76% and 88% accuracy respectively (naive baselines obtain 48% and 60%)... optimising expert debaters for persuasiveness in an unsupervised manner improves non-expert ability to identify the truth." [icml.cc/virtual/2024/oral/35483; arxiv 2402.06782]
- **Kenton et al., NeurIPS 2024 "On scalable oversight with weak LLMs judging strong"**: "on previously unstudied closed QA tasks, weak judges achieve higher accuracy in the debate protocol than consultancy, and around the same as direct question answering." [proceedings.neurips.cc 2024 paper 899511e37]

### 2.2 Reflexion and its successors

**Reflexion (Shinn et al. 2023)** remains the canonical citation but has documented weaknesses:
> "Research studying single-agent Reflexion found that self-reflections tend to repeat earlier misconceptions rather than introduce new reasoning paths — particularly on difficult examples." [pub.towardsai.net Mehta Mar 2026]

This is called the **"Degeneration of Thought" problem** [Liang et al., cited in Tool-MAD arxiv 2601.04742]. Modern successors:
- **CRITIC (Gou et al. 2024)** — tool-interactive critiquing, model uses external tools to verify its claims
- **Self-Refine (Madaan et al. 2023)** — iterative refinement with self-feedback, NeurIPS 2023
- **MACA / Multi-Agent Consensus Alignment (Samanta et al., ICLR 2026 submission)** — RL post-training using multi-agent debate consensus as reward signal [openreview.net id=Ma0LTdFVeL]
- **Agent-as-Judge (Zhuge et al. 2024/2025)** — agent evaluating another agent's trajectory, not just final output [arxiv 2508.02994 survey]
- **CourtEval (Kumar et al. 2025)** — Grader + Critic (prosecutor) + Defender (defense attorney) trio for adversarial-but-balanced evaluation

### 2.3 Critic / judge model patterns from labs

- **Anthropic constitutional AI** — uses a critic model with explicit principles
- **OpenAI process supervision** (PRM, process reward models, 2024) — verifier on intermediate steps not just final answer
- **DeepMind self-debate / scalable oversight** — Bowman/Hendrycks lineage
- **Pareto frontier finding**: "a weaker judge with strong debaters can still yield good results, whereas a strong judge with weak debaters is worse" [arxiv 2508.02994 §"Cost and Scalability"]

### 2.4 Model diversity vs quantity

Strong empirical support for heterogeneous ensembles:
- **LLM-TOPLA (Wu et al., EMNLP 2024 Findings)**: "the smaller ensemble size and the higher ensemble diversity, the better the generation performance... multiple sub-ensemble teams of size 2-4 that outperform the largest ensemble of size 8, and a majority of the smaller ensemble teams also outperform the best-performing individual model." [aclanthology.org/2024.findings-emnlp.698]
- **HDEE (Gensyn 2025)**: heterogeneous expert ensemble outperforms baseline in 20/21 evaluated domains at equivalent compute budget. [blog.gensyn.ai/diverse-expert-ensembles]
- **Wisdom of the Silicon Crowd (PMC 2025)**: ~12-model ensemble of frontier + open-source LLMs from "demographically diverse companies" rivals human crowd forecasting accuracy at ~$1/forecast.
- **DeePEen (NeurIPS 2024)**: training-free probability-distribution fusion across heterogeneous LLMs achieves consistent improvements on 6 benchmarks. [openreview.net id=7arAADUK6D]

**Rule of thumb from ensemble ML theory** (MachineLearningMastery): "combining a bunch of top-performing models will likely result in a poor ensemble as the predictions made by the models will be highly correlated. Unintuitively, you might be better off combining the predictions from a few top-performing individual models with the prediction from a few weaker models. So, it is desired that the individual learners should be accurate AND diverse."

**Practical implication for sc-reflect Tier 2/3**: a haiku + sonnet + (qwen | kimi | deepseek) trio is likely strictly better than 3×haiku or 3×sonnet, because of cross-vendor representational diversity. Confirmed by the Awesome-LLM-Ensemble survey citing 30+ heterogeneous-ensemble papers in 2024–2025.

### 2.5 Tier-decision rubrics

Microsoft's Azure AI **Task Adherence** feature (preview, Dec 2025) is the closest commercial analog to a tier-decision signal:
> "The Task Adherence feature identifies discrepancies such as misaligned tool invocations, improper tool input or output relative to user intent, and inconsistencies between responses and customer input. This feature lets system developers proactively mitigate misaligned actions by blocking them or escalating the issue for human intervention." [learn.microsoft.com/azure/ai-services/content-safety/concepts/task-adherence]

Escalation signals from the literature:
- **Confidence below threshold** (most agent frameworks gate at 0.7–0.9)
- **Contradictory evidence ratio >30%** (Tool-MAD, ReConcile use confidence-weighted consensus)
- **Tool-output–intent mismatch** (Azure Task Adherence)
- **Dead-end / no-progress on N consecutive turns**
- **Spec coverage gap detected** (NASA MBSE, Sept 2025)

### 2.6 Three adversarial patterns worth copying

From Mehta (Towards AI, Mar 2026):
1. **Generator–Critic** loop (Reflexion-style, single model OK for simple tasks)
2. **Reflexion loop with external verifier** (CRITIC pattern, uses tools)
3. **Adversarial debate** with two solver agents + critique exchange + judge synthesis — **the pattern matching sc-reflect Tier 2/3**:
   > "Two agents with different personas independently propose answers, critique each other's reasoning, and a judge synthesizes into a final verdict."

Key economic insight: **"your verifier doesn't need to be your most expensive model. Smaller models verify better than they generate — and this changes the economics dramatically."** [Mehta 2026]

---

## Topic 3: Pre-execution Validation Patterns

### 3.1 Requirements traceability via LLM (the academic frame)

NASA's AI4SE workshop paper "AI-Enhanced Requirements Traceability Using MBSE and LLM Complex Systems" (Legesse & Bicknell, Sept 2025) reports:
- Coverage: **35% → 67%** with LLM augmentation
- Accuracy: **76.7% → 92%**
- Still **33% of requirements require manual analysis**
- Limitations: dependency on requirement quality, context-length constraints, vertical (parent-child) traceability only

This validates pre-execution coverage analysis as a tractable LLM problem when paired with structured spec representation. [sercuarc.org/wp-content/uploads/2025/09/Legesse_AI_Enhanced_Requirements_Traceability]

### 3.2 LLM-as-judge for plan quality

The cleanest production formulation is **Promptfoo's `llm-rubric`** [promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric]:
- General-purpose grader; assertion configured as a natural-language rubric
- Default grader is GPT-5 (override via `provider`)
- Outputs structured JSON: `{pass, score, reason}`
- **Search-rubric variant** uses web-search-enabled grader for fact-grounding

For plan quality specifically, the assertion patterns that matter:
- Coverage: "Does plan address each of the N spec objectives?"
- Specificity: "Is each step concrete enough to execute?"
- Risk acknowledgment: "Are documented risks/dependencies surfaced?"
- Best-practice compliance: "Does plan follow [framework]'s recommended approach?"

### 3.3 Agentic framework pre-execution gates

**LangGraph 1.0 (Oct 2025)** is the production-preferred orchestrator with **conditional edges** that map to retry-vs-pass gates:
> "LangGraph has emerged as the production-preferred choice with its 1.0 stable release in October 2025, offering battle-tested state management, 6.17M monthly downloads, and proven enterprise deployments at companies like LinkedIn, Replit, and Elastic." [zenml.io/blog/langgraph-vs-crewai]

LangGraph's checkpointing + breakpoints + state inspection enable mid-execution intervention. CrewAI relies on role-based delegation with less granular control; AutoGen uses conversational multi-agent dialog.

The **plan-and-act pattern** [Erdogan et al. 2025, arxiv] formalizes pre-execution as a separate phase: planner LLM outputs structured plan, validator LLM scores it against objectives, executor only runs if validator-score ≥ threshold.

### 3.4 Best practices for catching spec gaps

The Red Hat Developer article "How spec-driven development improves AI coding quality" (Oct 2025) frames the recommended practice:
- Treat spec as source of truth
- Three policy options for drift:
  1. **Regenerate** all code from updated specs (consistent, resource-hungry)
  2. **Hand-edit** AI output as a draft (familiar, drifts if not synced)
  3. **Interactive vibe-loop** with approval gates + lesson logs (hybrid)

The **Kitchen Loop paper** (arxiv 2603.25697v1, 2026) cites Huang et al. (2025): "69% of professional developers carefully review every agentic change and 75% read every line of AI-generated code." But Fawzy et al. (2025) found "36% of practitioners using AI code generation skip quality assurance entirely, 18% place uncritical trust in AI output, and 10% delegate QA back to the same AI that wrote the code." Result: "68% of practitioners characterize the output as 'fast but flawed'." The Kitchen Loop argues **only structural enforcement — tests that cannot be skipped — is the only reliable solution.**

### 3.5 Azure Task Adherence — the closest commercial precedent

Microsoft Azure AI Content Safety (preview, late 2025) explicitly validates agent plans BEFORE tool execution:
> "A customer support assistant... A user messages the chatbot: 'Can you check how much data I've used this month?' The assistant plans to invoke a `change_data_plan()` tool. Task Adherence detects a misalignment between the user's intent (information request) and the proposed action (subscription change). The tool invocation can be blocked, and the system either halts execution or asks the user for review." [learn.microsoft.com/azure/ai-services/content-safety/concepts/task-adherence]

This is **exactly** the UC-1 pattern for sc-reflect.

---

## Topic 4: Post-execution Review Patterns

### 4.1 State of AI code review (2025–2026)

Quantitative benchmark from "AI Code Review Automation: Complete Guide 2025" (digitalapplied.com):

| Tool | Bug Detection | False Positives | Speed | Context |
|---|---|---|---|---|
| Greptile | 85% | sub-3% | moderate | full codebase |
| Qodo | 78% (claimed) / 42–48% (verified runtime) | low | <60s | multi-repo |
| CodeRabbit | 46% | 10–15% | ~5s | PR diff |
| Cursor Bugbot | 42% | sub-15% | 30–60s | PR diff |
| GitHub Copilot | basic | <15% | fast | file-level |
| Traditional SAST | <20% | high | variable | rule-based |

Augment Code, Qodo (71.2% SWE-bench), and Augment (70.6% SWE-bench, 59% F-score) are the enterprise-grade entries. [augmentcode.com/tools/best-ai-code-review-tools-2025]

### 4.2 Self-confirmation bias — the structural argument

The Towards AI Mehta piece (Mar 2026) provides the cleanest statement:
> "Ask an LLM to verify its own output, and it will often agree with itself — not because it has checked carefully, but because it is structurally predisposed to. This isn't a capability gap that better prompting can fix. The core issue is that a single model acting as its own generator, evaluator, and critic tends to reproduce the same reasoning structure across iterations, with little meaningful correction. If the model reasoned incorrectly the first time, the same representational biases that produced the error are present when it re-evaluates."

**Mitigation techniques** with empirical support:
- Different model class as reviewer (Galileo, Arize, Evidently — see Topic 5)
- Tool-grounded verification (CRITIC pattern)
- Adversarial framing (CourtEval prosecutor role, debate protocol)
- Reference-grounding (re-read the original spec/citation before judging)
- Process verification (verify intermediate steps not just final answer; OpenAI PRM lineage)

### 4.3 Spec-drift / diff-vs-spec verification

Kinde's "Spec Drift: The Hidden Problem AI Can Help Fix" (Aug 2025) lays out the pattern:
- Train AI on relationship between codebase and spec files (e.g., OpenAPI)
- Integrate into CI/CD:
  - Auto-open PR when drift detected
  - Slack notification
  - Fail the build
- "Spec-first" approach: regenerate code to conform to documentation, not the reverse

The Kitchen Loop paper formalizes this as **"User-Spec-Driven Development for a Self-Evolving Codebase"** (arxiv 2603.25697). [arxiv.org/html/2603.25697v1]

### 4.4 Validated-deviation taxonomy

There is **no canonical published taxonomy** for "validated deviation vs unauthorized drift" — this is a gap in the literature. Closest analogs:
- **Devinterrupted AI code review benchmark manifest** (Zigler, Nov 2025): scoring weights `{precision: 0.35, recall: 0.35, statefulness: 0.20, noise: 0.10}` — `statefulness` is the closest to "did the review recognize valid scope expansion." [devinterrupted.substack.com]
- **DORA 2025 Report** distinguishes "AI as accelerator" vs "AI as drag" based on organizational foundations (clear AI policies, healthy data ecosystem, strong version control). [augmentcode.com citing DORA]
- **Faros AI 2025 telemetry** (10,000+ devs, 1,255 teams): high AI adoption → 21% more tasks completed, 98% more PRs merged, BUT PR review time +91%, PR size +154%, bug count +9%. **No measurable DORA-level improvement.** This argues that authorization vs drift cannot be inferred from velocity alone.

**Practical taxonomy proposal** (synthesized, not cited):
- **Authorized expansion**: scope addition with explicit prompt or task-list update
- **Necessary deviation**: blocked by technical constraint, deviation documented in code/PR
- **Drift**: silent change not in original spec/tasklist, no documentation
- **Regression**: change that contradicts the spec

### 4.5 Production patterns

Production-Ready LLM Agents framework (Towards Data Science 2025) recommends **three pillars of offline evaluation**:
1. **Routing eval** — did the right agent get the query?
2. **Retrieval eval** — was the right context fetched?
3. **Generation eval** — was the final output correct?

Observability via Langfuse: each evaluation sample → trace + scores. CI/CD quality gates fail builds on regression. The author emphasizes that "assertion-based mental model breaks down" for LLMs — must shift to score-based gates with explicit thresholds.

---

## Topic 5: Skill Design + Eval Harness

### 5.1 Anthropic Skills 2.0 / Skill Creator update (Oct 2025 – Mar 2026)

Official skill-creator SKILL.md core loop [github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md]:
1. Figure out what the skill is about
2. Draft or edit the skill
3. Run claude-with-access-to-the-skill on test prompts
4. With the user, evaluate the outputs:
   - Create `benchmark.json` and run `eval-viewer/generate_review.py` for human review
   - Run quantitative evals
5. Repeat until satisfied
6. Package and return

Skill Creator 2.0 ships **four modes**:
- **Create** — initial drafting
- **Eval** — run test prompts with assertions
- **Improve** — iterate based on eval results
- **Benchmark** — A/B test new skill vs raw Claude

Four composable parallel sub-agents:
- `grader.md` — evaluates assertions against outputs
- `comparator.md` — blind A/B comparison between two outputs
- `analyzer.md` — analyzes why one version beat another
- (plus the skill-creator orchestrator)

[tessl.io/blog/anthropic-brings-evals-to-skill-creator; thetoolnerd.com/p/anthropic-skill-creator-20-update]

### 5.2 Test case structure

From tessl.io's eval example (Express handler reviewer):

```json
{
  "eval_id": 2,
  "eval_name": "api-handler",
  "prompt": "Review this Express handler for me — it processes orders. Any issues?",
  "assertions": [
    {"id": "no-input-validation", "text": "Flags that req.body items are used without validation", "type": "quality"},
    {"id": "foreach-async-inventory", "text": "Flags forEach with async callback for inventory updates (not awaited)", "type": "quality"},
    {"id": "loose-equality", "text": "Flags == instead of === for coupon code comparison", "type": "quality"},
    {"id": "error-logging", "text": "Flags console.log(err) as inadequate error handling", "type": "quality"},
    {"id": "unused-validation", "text": "Notes that validateOrder exists but is never called", "type": "quality"}
  ]
}
```

Each assertion is verifiable, specific, and unambiguous. The grader sub-agent returns pass/fail per assertion → numeric score.

### 5.3 Anthropic's official skill-design guidance

From "Equipping agents for the real world with Agent Skills" (anthropic.com/engineering, Oct 2025):
> "**Start with evaluation**: Identify specific gaps in your agents' capabilities by running them on representative tasks and observing where they struggle or require additional context. Then build skills incrementally to address these shortcomings.
> **Structure for scale**: When the SKILL.md file becomes unwieldy, split its content into separate files and reference them. If certain contexts are mutually exclusive or rarely used together, keeping the paths separate will reduce the token usage. Finally, code can serve as both executable tools and as documentation."

Anthropic also formalized **two skill categories** [Cohen LinkedIn re: Skills 2.0]:
- **Capability Uplift Skills**: fill model gaps (may expire as models improve)
- **Workflow Skills**: encode business processes (durable because unique to org)

`sc:reflect` is squarely a **Workflow Skill** — its value is encoding a specific reflection protocol, not patching a model capability gap.

### 5.4 Rubric design for "reflection quality"

No canonical published rubric. Synthesizing from Anthropic skill-creator patterns, Promptfoo `llm-rubric` patterns, and Mehta's verification taxonomy:

**Dimensions that matter for reflection skill output**:
1. **Citation accuracy** — every claim traceable to source (line/file/spec section)?
2. **Coverage completeness** — does the reflection address each spec/tasklist item?
3. **Deviation-classification precision** — authorized vs drift vs regression correctly tagged?
4. **Recommendation actionability** — concrete next steps, not vague advice?
5. **Hallucination rate** — fabricated claims vs grounded claims (search-rubric assertions can catch some)
6. **False-positive rate** — does it flag valid work as drift?
7. **Latency/cost vs Tier** — Tier 1 must be cheap and fast, Tier 3 can be expensive and thorough

Scoring scale recommendation: **0–5** based on Anthropic grading-scale paper (arxiv 2601.03444v1) — highest human-LLM ICC alignment compared to 0–10 or binary.

### 5.5 Iteration acceptance thresholds

From Hwee-Boon Yar's `writing-voice` skill case study using skill-creator 2.0:
- Three test prompts × two skill variants (new vs old) = 6 parallel runs
- Per-prompt grade: e.g., 10/10, 9/9, 9/10
- Convergence signal: new version scores ≥ old version on all prompts, with at least one strict improvement

From Arize LLM-judge guidance:
> "Treating a 100% pass rate as success... if your judge passes everything, the eval likely isn't challenging enough. A 70% pass rate on a rigorous evaluator that genuinely stress-tests your system is more informative than perfect scores on one that doesn't."

**Practical acceptance threshold for sc-reflect**:
- Tier 1 fast-path: ≥80% assertion pass rate, <5s latency budget
- Tier 2/3 multi-agent: ≥90% assertion pass rate, debate transcript shows real disagreement-then-convergence (not echo-chamber)
- Iteration cycle: ship at iteration N if iteration N+1 shows <5% absolute improvement on held-out test set (60/40 train/test split is Anthropic's default in skill-creator)

### 5.6 Inter-rater reliability for LLM graders

**The judge model should be different from (and typically more capable than) the model being evaluated.**

- Arize FAQ: "No. Pick a different, more capable model. If your app uses Claude Haiku, use Claude Sonnet or a competitive alternative as your judge. Reasoning models are overkill for evaluation and add unnecessary latency and cost without meaningful benefit."
- Evidently AI: "you can often use the same LLM as both the generator and the judge. Just make sure you formulate a distinct, clear prompt for evaluation. That said, sometimes it helps to use a different model (or even several)... you can experiment with LLM juries, where multiple models provide judgments that you then aggregate."
- IJCNLP 2025 study cited in Galileo: "judge model choice has the highest impact on positional bias compared to task complexity, output length, or quality gaps. When researchers swapped answer positions, GPT-4's judgment flipped to favor the alternative."
- Anthropic grading-scale study (arxiv 2601.03444): 0–5 scale highest human-LLM ICC; "Llama-3.3-70B-Instruct… open-source models assess essays more uniformly, clustering ratings around the midpoint, whereas human raters and the closed-source models provide a [wider range]."

Documented biases to design around:
- **Positional bias** (highest impact per IJCNLP 2025)
- **Self-enhancement bias** — model favors its own outputs
- **Verbosity bias** — prefers longer responses
- **Reference-answer score bias** — fixed scores in rubric anchor outputs

### 5.7 Eval harness tooling landscape (May 2026)

Per digitalapplied.com "AI Agent Eval Frameworks 2026":
- **Commercial**: LangSmith, Braintrust, Helicone, Phoenix (Arize), Promptfoo (acquired by OpenAI 2026)
- **Open-source**: OpenAI Evals (registry-style), DeepEval v4.0.3 (pytest-native), Inspect AI v0.3.225 (UK AI Security Institute, public-sector focus)

Best fit for a `.dev/eval-workspaces/`-style local harness:
- **Promptfoo** — YAML config, `llm-rubric` and `search-rubric`, easy ad-hoc setup
- **Inspect AI** — pytest-native, Python-first (aligns with UV/superclaude environment)
- **DeepEval** — pytest-native with rich assertion library
- **OpenAI Evals** — JSON registry, well-suited if assertions stable

For the sc-reflect-protocol skill specifically, the **Anthropic skill-creator eval harness** (using `benchmark.json` + `eval-viewer/generate_review.py`) is the canonical local pattern and is what the existing `.dev/eval-workspaces/sc-brainstorm/` likely mirrors.

---

## Synthesis: Concrete Recommendations for sc-reflect-protocol

1. **Keep the `think_about_*` triad as scripted Tier-1 checkpoints, not optional self-nudges.** They are current, not deprecated, and map cleanly to the three reflection moments (evidence-complete? on-task? done?). Wire them as mandatory protocol steps with explicit "if think returns 'concerns', escalate to Tier 2" logic. [Topic 1; oraios docs; Qiita 2025]

2. **Build evidence-gathering on `get_symbols_overview` → `find_symbol` → `find_referencing_symbols`** rather than file reads. Anthropic Opus 4.6's own testimony is that this collapses 8–12 step exploration into one atomic call. For post-execution review, this directly enables "is the work referenced where the spec says it should be?" verification. [Topic 1; oraios.github.io]

3. **Use `write_memory` after each tier's completion as a persistent contract.** Tier 1 writes a summary memory; Tier 2/3 sessions begin with `read_memory` for context handoff. Avoids implicit summarization drift documented in oraios docs. Memory naming: `reflect-<usecase>-<timestamp>.md` (e.g., `reflect-uc1-20260526T1500.md`). [Topic 1]

4. **For Tier 2/3, use heterogeneous models (haiku + sonnet + qwen/deepseek/kimi), not 3× haiku.** Empirical support: HDEE, LLM-TOPLA, DeePEen, Wisdom of Silicon Crowd. Cross-vendor representational diversity outperforms intra-vendor cheap stacks at equivalent cost. The "accurate AND diverse" rule from classical ensemble ML applies directly. [Topic 2; aclanthology.org/2024.findings-emnlp.698]

5. **Adopt the weak-judge + strong-debaters pattern for the merge step.** Per Khan et al. (ICML 2024 Oral) and Kenton et al. (NeurIPS 2024), Opus-as-debater + Sonnet-as-merge-judge is the right architecture, not Opus-as-judge + cheap-debaters. Anthropic's own scalable-oversight lineage supports this. Important caveat: judge must NOT be one of the debating models (self-enhancement bias). [Topic 2; arxiv 2402.06782; proceedings.neurips.cc 2024]

6. **Frame Tier 2 explicitly as an adversarial debate, not a multi-agent vote.** Mehta's three patterns (Generator-Critic, Reflexion+verifier, Adversarial Debate) — debate is the right one for sc-reflect's "merge by Opus" step. CourtEval's Grader/Critic/Defender trio is a published template. Avoid naive majority-vote (ICLR 2025 MAD blogpost found this "overly aggressive, erases correct answers"). [Topic 2; arxiv 2508.02994 CourtEval; d2jud02ci9yv69.cloudfront.net 2025-04-28-mad-159]

7. **For UC-1 (pre-execution validation), build an explicit coverage matrix + LLM-as-judge gate.** Model after NASA MBSE+LLM (35%→67% coverage, 76.7%→92% accuracy) and Microsoft Azure Task Adherence (intent vs proposed tool call). The plan-validator output should be a structured JSON: `{coverage_pct, gaps: [...], risks: [...], recommendation: pass|escalate|reject}`. [Topic 3; sercuarc.org; learn.microsoft.com]

8. **For UC-2 (post-execution review), make the spec/tasklist the source of truth and re-ground on every claim.** The Kinde "spec drift" pattern + Kitchen Loop's "tests that cannot be skipped" structural enforcement. Critically: the reviewer agent must NOT be the executor agent. The Mehta/Towards AI argument is structural — same-model self-review is biased by design, not by prompting. Use a different model class as reviewer. [Topic 4; kinde.com; arxiv 2603.25697v1; pub.towardsai.net]

9. **Build the eval harness on the Anthropic skill-creator pattern** (benchmark.json + grader sub-agent + 60/40 train/test split). Use 0–5 grading scale (highest human-LLM ICC per arxiv 2601.03444). Target 70–90% assertion pass rate as ship-acceptance, NOT 100% (Arize, Evidently both flag 100% as a smell). Iteration acceptance: stop iterating when N+1 vs N improvement is <5% absolute on held-out test set. [Topic 5; anthropics/skills SKILL.md; arxiv 2601.03444v1]

10. **Use a *different, more capable* model as the grader than the skill-under-test uses.** If sc-reflect Tier 1 runs on Sonnet, grader runs on Opus. If Tier 2 runs heterogeneous Sonnet+Haiku, grader is Opus solo. This avoids positional bias (IJCNLP 2025 highest-impact bias) and self-enhancement bias. For final accept/reject of the skill release, consider a 2–3 model LLM-jury aggregated by majority — but only after individual judge validation. [Topic 5; Arize, Evidently, Galileo, arxiv 2601.03444]

---

## Sources Cited

**Topic 1 — Serena MCP**:
- [tavily] github.com/oraios/serena — primary repo, README, evals
- [tavily] github.com/oraios/serena/issues/494 — tool inventory log dump Aug 2025
- [tavily] github.com/oraios/serena/discussions/545 — Serena vs Claude Code built-in tools
- [tavily] github.com/oraios/serena/issues/354 — Windows/npm TypeScript LSP bootstrap failure
- [tavily] oraios.github.io/serena/01-about/000_intro.html — official about/methodology
- [tavily] dev.to/webdeveloperhyper/how-to-use-ai-more-efficiently-for-free-serena-mcp — DEV community guide
- [tavily] qiita.com/shi902/items/ed59f096c3c8032c51c3 — Qiita Japanese guide with troubleshooting
- [tavily] vibetools.net/posts/serena-mcp-complete-guide — detailed configuration and security guide
- [tavily] kazuhira-r.hatenablog.com/entry/2025/12/07/011522 — CLOVER Dec 2025 tool surface verification
- [tavily] jamesacres.co.uk/2025/05/coding-with-serena-and-claude-desktop-via-mcp — practical setup
- [tavily] mcp.nacos.io/mcp/server/server20211 — oraios docs mirror with usage recommendations

**Topic 2 — Multi-agent verification**:
- [tavily] d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159 — ICLR 2025 MAD benchmark blogpost
- [tavily] emergentmind.com/topics/multi-agent-debate-system — MAD system survey
- [tavily] openreview.net id=Ma0LTdFVeL — MACA (ICLR 2026 submission)
- [tavily] icml.cc/virtual/2024/oral/35483 — Khan et al. ICML 2024 Oral on persuasive debate
- [tavily] arxiv.org/html/2402.06782v4 — Khan et al. full paper
- [tavily] proceedings.neurips.cc/.../899511e37 — Kenton et al. NeurIPS 2024 scalable oversight
- [tavily] arxiv.org/html/2601.04742v1 — Tool-MAD with diverse tool augmentation
- [tavily] composable-models.github.io/llm_debate — Du et al. multiagent debate
- [tavily] link.springer.com/article/10.1007/s44443-025-00353-3 — Adaptive heterogeneous MAD survey
- [tavily] pub.towardsai.net/how-multi-agent-self-verification-actually-works — Mehta Mar 2026 production patterns
- [tavily] neurips.cc/virtual/2025/poster/117644 — Multi-Agent Debate for LLM Judges (NeurIPS 2025)
- [tavily] arxiv.org/html/2508.02994v1 — Agent-as-Judge survey (CourtEval, Kumar et al. 2025)
- [tavily] arxiv.org/html/2503.16416v1 — Survey on Evaluation of LLM-based Agents
- [tavily] blog.gensyn.ai/diverse-expert-ensembles — HDEE
- [tavily] aclanthology.org/2024.findings-emnlp.698.pdf — LLM-TOPLA focal diversity
- [tavily] openreview.net id=7arAADUK6D — DeePEen NeurIPS 2024
- [tavily] pmc.ncbi.nlm.nih.gov/articles/PMC11800985 — Wisdom of Silicon Crowd
- [tavily] github.com/junchenzhi/Awesome-LLM-Ensemble — comprehensive ensemble paper list
- [tavily] machinelearningmastery.com/ensemble-diversity-for-machine-learning — classical ensemble theory

**Topic 3 — Pre-execution validation**:
- [tavily] sercuarc.org/wp-content/uploads/2025/09/Legesse_AI_Enhanced_Requirements_Traceability — NASA MBSE+LLM, AI4SE workshop Sept 2025
- [tavily] learn.microsoft.com/azure/ai-services/content-safety/concepts/task-adherence — Azure Task Adherence preview
- [tavily] zenml.io/blog/langgraph-vs-crewai — LangGraph 1.0 production status, Oct 2025
- [tavily] arxiv.org/html/2603.25697v1 — Kitchen Loop user-spec-driven dev
- [tavily] arxiv.org/html/2605.01160v1 — Productivity-Reliability Paradox specification governance
- [tavily] kinde.com/learn/ai-for-software-engineering/ai-devops/spec-drift-the-hidden-problem-ai-can-help-fix
- [tavily] developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality
- [tavily] agentics.scitevents.org/Abstract.aspx — AGENTICS 2025 abstracts with MCP+LangGraph integration

**Topic 4 — Post-execution review**:
- [tavily] digitalapplied.com/blog/ai-code-review-automation-guide-2025 — benchmark table for 2025 tools
- [tavily] augmentcode.com/tools/best-ai-code-review-tools-2025 — Qodo, Augment, DORA 2025 citation
- [tavily] kinde.com/learn/ai-for-software-engineering/ai-devops/spec-drift-the-hidden-problem-ai-can-help-fix
- [tavily] devinterrupted.substack.com — AI code review benchmark manifest (Zigler Nov 2025)
- [tavily] the-ai-corner.com/p/ai-code-review-checklist-2026-failure-modes-prompts — failure modes catalog
- [tavily] arxiv.org/html/2603.25697v1 — Kitchen Loop structural enforcement
- [tavily] kiuwan.com/blog/code-review-tools — Qodo Merge, AI code review tools survey
- [tavily] towardsdatascience.com/production-ready-llm-agents — three-pillar offline eval framework
- [tavily] pub.towardsai.net/how-multi-agent-self-verification-actually-works — self-confirmation bias structural argument

**Topic 5 — Skill design + eval**:
- [tavily] anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — Anthropic official Oct 2025
- [tavily] github.com/anthropics/skills — public Skills repo
- [tavily] github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md — official skill-creator SKILL.md
- [tavily] tessl.io/blog/anthropic-brings-evals-to-skill-creator — Skill Creator 2.0 deep-dive with eval JSON example
- [tavily] thetoolnerd.com/p/anthropic-skill-creator-20-update — Skill Creator 2.0 multi-agent testing
- [tavily] hboon.com/using-the-skill-creator-skill-to-improve-your-existing-skills — writing-voice skill case study
- [tavily] arxiv.org/html/2601.03444v1 — Grading Scale Impact on LLM-as-a-Judge (0–5 best)
- [tavily] galileo.ai/blog/llm-as-a-judge-vs-human-evaluation — biases, IJCNLP 2025 cites
- [tavily] arize.com/llm-as-a-judge — judge model selection guidance
- [tavily] evidentlyai.com/blog/llm-judges-faq — practical FAQ
- [tavily] promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric — official llm-rubric docs
- [tavily] digitalapplied.com/blog/ai-agent-eval-frameworks-testing-guide-2026 — 8-framework matrix May 2026

**`[UNCONFIRMED]` items in the synthesis:**
- The specific "haiku + sonnet + qwen/deepseek/kimi" model trio recommendation is extrapolated from heterogeneous-ensemble research; no source benchmarks this exact combination.
- The validated-deviation taxonomy proposal in Topic 4 is synthesized, not cited — the literature gap is real.
- The specific 70–90% assertion pass rate thresholds in Recommendation 9 are interpolations from Arize/Evidently "70% > 100%" guidance combined with skill-creator's 60/40 train/test pattern, not a single published threshold.
