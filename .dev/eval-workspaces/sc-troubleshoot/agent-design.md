# Custom Agent Design for sc:troubleshoot

**Author**: design exploration for `sc:troubleshoot-protocol`
**Date**: 2026-05-21
**Status**: proposal — no agent files created yet (per user instruction)

## 1. Existing agent landscape

The skill at `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` already delegates to a fleet of existing agents (SKILL.md:162-169 agent-selection table, SKILL.md:301 Task row):

| Agent | Role in protocol | Source |
|-------|------------------|--------|
| `root-cause-analyst` | Wave 1 (single hypothesis), Wave 3 (every type) | `src/superclaude/agents/root-cause-analyst.md:1-49` |
| `quality-engineer` | Wave 3 edge-case lens for bug/security/test | `src/superclaude/agents/quality-engineer.md:1-49` |
| `performance-engineer` | Wave 3 when `--type performance` | `src/superclaude/agents/performance-engineer.md:1-49` |
| `security-engineer` | Wave 3 when `--type security` | `src/superclaude/agents/security-engineer.md` |
| `refactoring-expert` | Wave 3 when recent-refactor signal | `src/superclaude/agents/refactoring-expert.md` |
| `system-architect` | Wave 3 when multi-component | `src/superclaude/agents/system-architect.md` |
| `devops-architect` | Wave 3 when build/deployment | `src/superclaude/agents/devops-architect.md` |
| `self-review` | Wave 4 post-adversarial-merge sanity check | `src/superclaude/agents/self-review.md:1-33` |

### Gaps the existing fleet does NOT cover

Walking the protocol wave-by-wave, three orchestration tasks have no dedicated agent and live as "the skill does it" prose in `SKILL.md`:

1. **Wave 1 / Wave 3 confidence re-grading.** The protocol explicitly says "Trust agent-reported confidence without re-grading against the rubric" is in the Will-Not-Do list (`SKILL.md:325`). The 5-dimension rubric in `refs/escalation-rubric.md:9-22` is meant to be applied **independently** of the agent that produced the card. Today this re-grade lives inside the orchestrator, in the same context that just read the hypothesis card — anchored, not independent.

2. **Wave 5 file:line citation validation.** `SKILL.md:247` calls this "non-negotiable" and `SKILL.md:24` makes the hallucination contract load-bearing for the whole skill. The work is mechanical (Read each cited file, compare quoted snippet, drop unfounded items, mark `partial` if any dropped) but it is the **last gate** before the report ships, and the orchestrator at that point is tired and biased toward declaring done.

3. **Wave 1 reproducer construction for intermittent symptoms.** When the rubric's "Reproducibility fit" dimension scores 0.0 (`refs/escalation-rubric.md:15`), the protocol escalates — but no agent is specialized in *trying to make the symptom deterministic*. Currently `root-cause-analyst` does inline repro as part of its hypothesis work; for the hard cases this is divided attention.

A fourth candidate exists (hypothesis-clustering before adversarial debate, `SKILL.md:186-187`) but `sc:adversarial-protocol`'s own diff-analysis step already does clustering — see debate below.

## 2. Candidate agents (brainstorm)

### Candidate A — `confidence-calibrator`

- **Name**: `confidence-calibrator`
- **Fires when**: End of Wave 1 (always); end of Wave 3 (once per Tier 2 hypothesis card)
- **Problem solved**: Independent application of the 5-dimension rubric in `refs/escalation-rubric.md:9-22` to a hypothesis card produced by another agent. Returns per-dimension scores + average + an explicit escalation recommendation (matching the decision logic at `refs/escalation-rubric.md:25-43`).
- **Why a custom agent vs. SKILL.md paragraph**: The re-grade is supposed to be untainted by the hypothesis-*formation* context. An orchestrator that just walked the hypothesis-forming agent through grounding queries, reproducer attempts, and brief composition is anchored — its calibration tends to inherit the agent's self-reported confidence. A fresh agent context strips the *formation* anchor (it sees only the card and the rubric, not the upstream investigative trail). The card itself is still present, so anchoring is *reduced*, not eliminated — but the upstream trail is the dominant anchor in practice. Reusable: runs ~1x in Tier 1, up to 4x in Tier 2.
- **Risk of redundancy**: Very low. No existing agent scores against a rubric; this is not what `self-review` does (post-implementation sanity, not pre-fix confidence scoring).

### Candidate B — `evidence-validator`

- **Name**: `evidence-validator`
- **Fires when**: End of Wave 5, before `REPORT.md` is finalized (always; every tier).
- **Problem solved**: For every `file:line` citation in the draft report, Read the cited file at the cited range, confirm the quoted snippet matches, return the validated set + the dropped set. Also validates command-output evidence by re-running cheap commands when safe. Drives the `success` vs `partial` status decision (`SKILL.md:247`).
- **Why a custom agent vs. SKILL.md paragraph**: This is the protocol's load-bearing hallucination guarantee (`SKILL.md:24`). A paragraph can describe what to do; an isolated agent forces the work to *happen* and isolates the N Reads from the orchestrator's main context. A typical report has 10-30 evidence items — bringing all those file Reads into orchestrator context inflates it precisely when token discipline matters most. Runs on every report regardless of tier — maximum reusability.
- **Risk of redundancy**: Zero. No existing agent validates citations.

### Candidate C — `reproducer-builder`

- **Name**: `reproducer-builder`
- **Fires when**: Wave 1 if the symptom is described as intermittent/flaky/non-deterministic; Wave 3 for `--type test` or when Tier 1's reproducibility dimension scored ≤ 0.5.
- **Problem solved**: Construct the smallest possible command that reliably (or unreliably) produces the symptom. Report whether it reproduces, how often, and what environmental conditions matter. Returns either a deterministic repro recipe or a "could not stabilise" verdict with the configurations tried.
- **Why a custom agent vs. SKILL.md paragraph**: For deterministic bugs the work is trivial and the existing agents handle it inline. For flaky/intermittent bugs the work is substantial (multiple runs, environmental variation, timing analysis) and divided attention from a hypothesis-forming agent under-serves both jobs.
- **Risk of redundancy**: Partial. `root-cause-analyst` already does inline repro; `quality-engineer` knows about flaky tests. But neither is specialized at *just stabilising a reproducer*. Worth deeper debate.

### Candidate D — `hypothesis-clusterer`

- **Name**: `hypothesis-clusterer`
- **Fires when**: End of Wave 3, before deciding whether to invoke Wave 4 adversarial.
- **Problem solved**: Read all 2-4 Tier 2 hypothesis cards, cluster their proposed fixes (sometimes two cards propose the same fix in different words), produce the `candidate-fixes.md` index, and recommend `consensus` / `competing` / `outlier` for each cluster.
- **Why a custom agent vs. SKILL.md paragraph**: The clustering is a non-trivial judgement when proposed fixes are paraphrased differently.
- **Risk of redundancy**: HIGH — `sc:adversarial-protocol`'s diff-analysis stage already does exactly this clustering as part of its work; this agent would duplicate it. The only thing the orchestrator needs to decide *before* Wave 4 is "are there 2+ distinct fixes?" which is a paragraph-sized decision, not an agent-sized one.

### Candidate E — `symptom-grounder`

- **Name**: `symptom-grounder`
- **Fires when**: Start of Wave 1, before `root-cause-analyst` is spawned.
- **Problem solved**: Issue the parallel `auggie` + `serena` queries, distill the results, return a "grounded brief" with file paths, relevant symbols, and recent-change context.
- **Why a custom agent vs. SKILL.md paragraph**: It wouldn't be. This is literally the work already described at `SKILL.md:117-120`.
- **Risk of redundancy**: Total. Two MCP calls and a summary do not earn an agent.

### Candidate F — `regression-detective`

- **Name**: `regression-detective`
- **Fires when**: Tier 2, when the symptom contains "used to work" / "started recently" / a commit reference.
- **Problem solved**: `git log -p` / `git bisect`-style investigation to find the introducing commit.
- **Why a custom agent vs. SKILL.md paragraph**: A focused specialist would be more rigorous than a general-purpose investigator.
- **Risk of redundancy**: HIGH. `refactoring-expert` is already routed for "recent refactor signals" (`SKILL.md:165`) and `root-cause-analyst` can run `git log` from its standard toolkit. The signal-driven escalation table already covers this case.

## 3. Adversarial debate

### Round 1 — drop the no-value candidates

- **Drop E (`symptom-grounder`)** — duplicates a paragraph (`SKILL.md:117-120`). Two MCP calls + a string don't earn an agent.
- **Drop F (`regression-detective`)** — overlaps with `refactoring-expert` (already routed for refactor signals) and `root-cause-analyst` (already knows `git log`). The agent-selection table at `SKILL.md:162-169` already handles this case.
- **Drop D (`hypothesis-clusterer`)** — `sc:adversarial-protocol` already clusters as part of its diff-analysis. Adding a pre-clustering agent duplicates work that the downstream skill is purpose-built to do. The Wave 3 → Wave 4 decision ("≥2 distinct fixes? then debate; else skip") is a paragraph-sized choice, not an agent.

### Round 2 — interrogate the survivors (A, B, C)

**A vs B**: which is more critical to ship first?

- B (`evidence-validator`) directly defends the hallucination contract that the entire skill's credibility rests on (`SKILL.md:24`). Without it the protocol degrades to "feels right". The work is mechanical but the discipline to do it must be enforced by isolation.
- A (`confidence-calibrator`) defends the escalation gate. Without it, the gate still works but with anchoring bias — the orchestrator tends to inherit the agent's self-confidence. Important but second-order.
- Verdict: B is must-ship, A is high-value follow-up.

**Could A and B be one agent?** No. Different waves, different cognitive tasks (rubric scoring vs. file:line verification), different invocation cadences (once per card vs. once per report). Combining them muddies both.

**C vs the existing fleet**: how often does the value materialise?

- C only earns its keep when Tier 1's reproducibility dimension scores 0.0 (intermittent/flaky). For deterministic bugs, `root-cause-analyst` inline repro is already cheap and good.
- The Tier 2 fan-out is already capped at 4 agents (`SKILL.md:323`). Spawning a reproducer specialist consumes one of those slots; in most cases a domain specialist (e.g., `quality-engineer` for flaky tests) is a better use of the slot.
- The protocol already has an escape valve for non-reproducible symptoms: escalate to Tier 2 with multiple perspectives. The reproducer-builder is a refinement, not a missing capability.
- Verdict: C is a future enhancement, not a v1 must-ship. Defer until eval data shows the protocol losing on intermittent cases.

### Round 3 — final cut

**Keep**: B (`evidence-validator`) — primary, must-ship; A (`confidence-calibrator`) — secondary, ship together if budget allows.

**Defer**: C (`reproducer-builder`) — revisit after running the existing eval suite to see whether intermittent-case failures are a real pattern.

## 4. Chosen agent(s) — full proposals

### Agent 1: `evidence-validator` (primary)

```markdown
---
name: evidence-validator
description: Validates every file:line citation and command-output claim in a draft report against the real files, drops unfounded items, and returns the verified evidence set. Used by sc:troubleshoot-protocol in Wave 5 before REPORT.md is finalized; designed to be reusable by any skill that produces an evidence-cited report.
category: quality
tools: Read, Grep, Glob, Bash
model: sonnet
---

# Evidence Validator

## Triggers

- Delegated by `sc:troubleshoot-protocol` in Wave 5 (before report finalization).
- Never auto-activates from keywords; invoked only via the `Task` tool with an explicit draft-report path.

## Behavioral Mindset

You are the last gate between a draft report and the user. Your job is to find unfounded citations, not to confirm absence of them. A pass that drops zero items is suspect — either the upstream agents were unusually disciplined, or you weren't thorough enough. When in doubt, drop it.

You do not improve the report's prose, you do not propose new evidence, you do not re-grade confidence. Your single output is a list: which citations survived, which were dropped, and why.

The orchestrator depends on your honest count of dropped items to decide whether the report ships as `success` or `partial`. A false PASS here is worse than a false FAIL — a hallucinated citation in a shipped report is the failure mode the entire protocol exists to prevent.

## Inputs

The orchestrator passes you:

- `report_draft_path`: absolute path to the draft `REPORT.md`
- `evidence_section_locator`: hint about which section contains evidence items (typically "## Evidence")
- `output_path`: where to write your validation report
- `allow_command_reexec`: bool, whether you may re-run cited commands (default false; only true when the orchestrator has vetted the commands as side-effect-free)

## Responsibilities

1. **Parse every citation** in the draft report. Citations come in two forms:
   - `file:line` references with a quoted snippet (e.g., `path/to/file.py:142` — `result = Path(...)`).
   - Command + output (e.g., `Command: uv run pytest ... -x` → `NameError: ...`).
2. **For each `file:line` citation**:
   - Read the cited file at a small window around the cited line (default ±5 lines).
   - Compare the quoted snippet to the actual content. Tolerate whitespace and trailing-comment differences; do not tolerate semantic differences.
   - Verdict: `verified` / `line-mismatch` / `file-missing` / `snippet-mismatch`.
3. **For each command citation**:
   - If `allow_command_reexec=false`, mark as `unverified-by-policy` and pass through (the command is a claim the report makes; the orchestrator decides whether to trust it).
   - If `allow_command_reexec=true` AND the command is read-only (no `rm`, no `git checkout`, no network mutation), re-run it and compare output. Verdict: `verified` / `output-mismatch` / `command-failed`.
4. **Return a structured validation report** as Markdown.

## Output Format

Write to `output_path`:

```markdown
# Evidence Validation Report

**Report under validation**: <abs path>
**Timestamp**: <ISO 8601>
**Total citations**: <N>
**Verified**: <N>
**Dropped**: <N>
**Suggested report status**: <success | partial>

## Verified citations

| # | Type | Location | Verdict |
|---|------|----------|---------|
| 1 | file:line | `path/file.py:142` | verified |

## Dropped citations

| # | Type | Location | Reason | Recommended action |
|---|------|----------|--------|--------------------|
| 1 | file:line | `path/file.py:88` | line-mismatch — actual content at line 88 is `def helper():` not the cited snippet | remove citation; if the underlying claim is still believed, hunt for the correct line |

## Notes

- Any patterns observed (e.g., "3 of 4 dropped citations came from quality-engineer's card") — useful for orchestrator to decide whether to penalize an upstream agent.
```

## Tools

- **Read**: pull the cited file at a ±5 line window around each citation
- **Grep**: when the cited line is wrong but the snippet exists elsewhere in the file, find the real line
- **Glob**: when the cited file path doesn't exist, check if it was moved
- **Bash**: only when `allow_command_reexec=true` and only for read-only commands

## Boundaries

**Will:**

- Read every cited file at the cited range
- Drop citations that don't match, with a specific reason
- Return an honest count even if it embarrasses an upstream agent
- Note when a snippet exists at a *different* line than cited (useful for the report-writer to fix vs. drop)

**Will Not:**

- Rewrite the report
- Propose new evidence
- Re-grade confidence
- Execute mutating commands (even if `allow_command_reexec=true`)
- Hide drops behind a "close enough" judgement — match or drop

```

### Agent 2: `confidence-calibrator` (secondary)

```markdown
---
name: confidence-calibrator
description: Independently re-grades a hypothesis card against a 5-dimension rubric and returns calibrated confidence plus an escalation recommendation. Used by sc:troubleshoot-protocol in Wave 1 (Tier 1 calibration) and Wave 3 (per-card Tier 2 calibration). Designed to defeat the anchoring bias of in-context self-grading.
category: analysis
tools: Read
model: sonnet
---

# Confidence Calibrator

## Triggers

- Delegated by `sc:troubleshoot-protocol` after Wave 1 produces a Tier 1 hypothesis card, and after each Wave 3 hypothesis card is written.
- Never auto-activates from keywords; invoked via `Task` with a card path and a rubric path.

## Behavioral Mindset

You are deliberately stripped of the hypothesis-formation context — you did not run the grounding queries, you did not draft the brief, you did not iterate on the hypothesis. You only see the finished card and the rubric. The card itself is present (you must read it) but the upstream investigative trail is not — that is where the anchoring bias lives. Apply the rubric mechanically: one dimension at a time, score with evidence, never inherit the card's self-reported confidence.

Self-reported confidence is a signal, not a number. Treat it as part of the card's narrative, not as input to your score. If the card says "Confidence: 0.92" and the evidence chain is two cited lines and an unverified command, the dimension scores tell the truth and the average wins.

## Inputs

- `card_path`: absolute path to the hypothesis card to score
- `rubric_path`: absolute path to `refs/escalation-rubric.md`
- `card_tier`: 1 or 2 (affects the escalation recommendation)
- `flags_context`: dict with `--depth`, `--no-escalate`, `--type` (for the decision logic in the rubric's Escalation Decision section)
- `output_path`: where to write your calibration report

## Responsibilities

1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
2. **Read the card** at `card_path`.
3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches. This is essential to scoring "Evidence grounding" honestly. Do NOT trust the card's quoted snippet without verifying.
4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score. Never split-the-difference to please the upstream agent.
5. **Compute the arithmetic mean**, rounded to 2 decimals.
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.

## Output Format

Write to `output_path`:

```markdown
# Calibration Report

**Card under calibration**: <abs path>
**Rubric**: <abs path>
**Card tier**: <1|2>
**Timestamp**: <ISO 8601>

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 / 0.5 / 0.0 | <one-line citing what in the card supports this> |
| Symptom coverage | ... | ... |
| Reproducibility fit | ... | ... |
| Fix directness | ... | ... |
| Domain coherence | ... | ... |

## Confidence

- **Self-reported (in card)**: <X.XX>
- **Calibrated (this report)**: <Y.YY>
- **Delta**: <signed difference, and a one-line read on why it differs>

## Escalation recommendation

- **Verdict**: `STOP` | `ESCALATE`
- **Reason**: `none` | `low_confidence` | `multi_domain` | `intermittent` | `not_reproducible` | `forced_by_depth_deep` | `security_caution`
- **Rubric rule fired**: <quote the rule from § Escalation Decision>

## Notes

- Any evidence the card cited that did not verify on spot-check (this also feeds the Wave 5 evidence-validator's work, but is worth surfacing early)
- Any dimension scored low specifically because the card omitted a section the rubric expects
```

## Tools

- **Read**: the rubric, the card, the cited files (for spot-check)

## Boundaries

**Will:**

- Score each dimension independently using the rubric's anchors
- Spot-check evidence citations to honestly score "Evidence grounding"
- Cite what in the card drove each score
- Return a calibrated number even when it differs sharply from the self-report

**Will Not:**

- Trust the card's self-reported confidence
- Re-write the card
- Propose new evidence or fixes
- Inherit the card's narrative framing — score what's there, not what's implied
- Apply social judgement ("the agent seemed careful") — only the rubric anchors and the cited evidence

```

## 5. Direct-invocation eval cases for the chosen agent(s)

These are designed to verify the agent works correctly **when called directly via Task**, independent of the orchestrating skill. Each scenario: input, expected behavior, failure mode.

### Evals for `evidence-validator`

**E1 — All citations verified**

- **Input**: a draft REPORT.md with 5 `file:line` citations, all of which match the actual files in the repo (use real lines from `src/superclaude/cli/eval_run.py` and friends).
- **Expected**: returns `Verified: 5`, `Dropped: 0`, `Suggested report status: success`. Verified table lists all 5.
- **Failure mode**: drops any of the 5 (false-positive), or fails to read any of the cited files.

**E2 — Half the citations have wrong line numbers**

- **Input**: a draft REPORT.md with 4 citations. Two cite the right file but a line that doesn't contain the quoted snippet (snippet exists elsewhere in the file). Two are correct.
- **Expected**: returns `Verified: 2`, `Dropped: 2`, `Suggested report status: partial`. Each dropped citation has reason `line-mismatch` and the "Notes" section flags that the snippet exists at a different line.
- **Failure mode**: passes the wrong-line citations (false negative), or drops the correct citations (false positive).

**E3 — Fabricated file**

- **Input**: a draft REPORT.md citing `src/superclaude/cli/imaginary_module.py:42`.
- **Expected**: `Dropped: 1` with reason `file-missing`. Status: `partial`.
- **Failure mode**: passes a citation to a nonexistent file.

**E4 — Mixed command + file:line evidence**

- **Input**: a draft REPORT.md with 3 `file:line` citations (all valid) and 1 command citation (`Command: uv run pytest tests/foo.py::test_bar -x` → some output). `allow_command_reexec=false`.
- **Expected**: 3 verified file citations, 1 command marked `unverified-by-policy` and passed through. The validation report explicitly notes that command-output evidence was not re-executed by policy. Status: `success` (passed-through evidence doesn't downgrade).
- **Failure mode**: re-runs the command despite `allow_command_reexec=false`, or drops the command citation as "unverified" rather than "passed through".

**E5 — Adversarial: snippet matches but in a comment/docstring, not code**

- **Input**: a draft REPORT.md citing `path/to/file.py:42` with a quoted snippet that exists at line 42 — but line 42 is inside a docstring or a `#` comment block, not executable code. The cited claim is that this line *exhibits a bug*.
- **Expected**: drop with reason `snippet-mismatch (context: cited as code but located in comment/docstring)`. This tests whether the validator examines context, not just string equality. Status: `partial`.
- **Failure mode**: passes the citation because the string matches verbatim. The "tolerate whitespace and trailing-comment differences" boundary is asserted in the design but never tested without this case.

**E6 — Whitespace-only differences (boundary verification)**

- **Input**: a draft REPORT.md citing `path/to/file.py:60` with the snippet `    result = compute(x, y)` — actual line 60 is `\tresult = compute(x, y)` (tab vs spaces) or `result  =  compute(x, y)` (extra spaces).
- **Expected**: verified. The boundary explicitly says whitespace differences are tolerated.
- **Failure mode**: drops on whitespace, which would force false-negative `partial` status on legitimate reports.

**E7 — All citations drop**

- **Input**: a draft REPORT.md with 3 citations, all of which fail validation (e.g., one wrong file, one wrong line, one wrong snippet).
- **Expected**: `Verified: 0`, `Dropped: 3`, `Suggested report status: partial` (NOT `failed` — the report still exists, just with no surviving evidence; the orchestrator decides the final disposition). The Notes section should call out that no evidence survived and recommend the orchestrator escalate or rerun.
- **Failure mode**: returns `failed` (overstepping into the orchestrator's status decision), or returns `success` with zero verified items.

**E8 — Missing/empty draft report**

- **Input**: `report_draft_path` points to a file that does not exist, or exists but is empty.
- **Expected**: returns a validation report with a clear failure note, suggested status `failed`, and zero citations processed. Does not crash, does not write garbage.
- **Failure mode**: silent crash, or invents citations to validate.

### Evals for `confidence-calibrator`

**C1 — Card with strong evidence, low self-reported confidence (under-confident agent)**

- **Input**: a hypothesis card citing 3 file:line refs (all real), a passing reproducer command + output, single-domain symptom, direct fix. Card self-reports 0.65.
- **Expected**: per-dimension scores all 1.0 or 0.5. Calibrated confidence ≥ 0.85. Verdict: `STOP`, reason `none`. Delta is positive and the "why" line notes the agent under-graded itself.
- **Failure mode**: returns calibrated < 0.85, or `ESCALATE`, due to inheriting the self-reported anchor.

**C2 — Card with weak evidence, high self-reported confidence (over-confident agent)**

- **Input**: a hypothesis card with one `file:line` citation to a file that doesn't contain the quoted snippet (intentional spot-check failure), no reproducer, multi-domain symptom (mentions both performance and correctness). Card self-reports 0.92.
- **Expected**: "Evidence grounding" scored 0.0 (spot-check failed) and called out; "Domain coherence" scored 0.5 or 0.0; calibrated confidence drops well below 0.85. Verdict: `ESCALATE`, reason `low_confidence` OR `multi_domain` (whichever rule fires first in the rubric's order).
- **Failure mode**: returns calibrated ≥ 0.85 (inherits self-report), or fails to spot-check and scores "Evidence grounding" 1.0 based on the card's claim.

**C3 — Intermittent symptom forces escalation regardless of score**

- **Input**: a hypothesis card with strong evidence (calibrated would be ≥ 0.85) but the symptom description says "fails intermittently in CI". `flags_context = {--depth: standard, --no-escalate: false, --type: bug}`.
- **Expected**: calibrated confidence high, but verdict `ESCALATE` with reason `intermittent`. The "Rubric rule fired" line quotes the intermittent rule from § Escalation Decision.
- **Failure mode**: returns `STOP` because the score is high, ignoring the intermittent escalation rule.

**C4 — `--depth deep` forces escalation regardless of score**

- **Input**: a strong card, `flags_context = {--depth: deep, --type: bug}`.
- **Expected**: verdict `ESCALATE`, reason `forced_by_depth_deep`. Confidence still reported honestly (calibrated ≥ 0.85), but the recommendation is escalate because the rubric's forced-escalation rule wins.
- **Failure mode**: returns `STOP` because the score is high, or hides the calibrated number behind the forced-escalation recommendation.

**C5 — Adversarial: card cites a real file but quoted snippet is invented**

- **Input**: a hypothesis card with three `file:line` citations. Files exist, line numbers are real, but two of the three quoted snippets are paraphrased/invented (the real file content at those lines is different). Self-reported confidence 0.80.
- **Expected**: "Evidence grounding" scored 0.0 or 0.5, with the spot-check failures explicitly enumerated in the Notes section ("Citation 2: line 42 reads X, card quoted Y"). Calibrated confidence drops well below 0.85.
- **Failure mode**: spot-checks only the *first* citation, or trusts the card's quoted snippets without reading the actual files. This is the calibrator's hardest job — actually doing the Reads the upstream agent should have done.

**C6 — Truncated / malformed card**

- **Input**: a hypothesis card that is missing one of the required rubric-relevant sections (e.g., no reproducer description, or no "Fix" section).
- **Expected**: the missing dimension scores 0.0 (not 0.5 — absence of evidence is not weak evidence), with a Notes entry that the card was incomplete. Calibrated confidence reflects the missing section's drag on the mean. Verdict tracks the rubric.
- **Failure mode**: scores the missing dimension as 0.5 ("partial") on the assumption that absence equals weakness, or invents a score from adjacent sections.

## 6. Integration plan

The two agents drop into specific waves in `SKILL.md` with minimal disruption:

### `evidence-validator` integration

- **Where**: `SKILL.md:247` (Wave 5 step 3, the "File:line validation pass (non-negotiable)").
- **Change**: replace the inline-orchestrator description with a `Task` spawn:
  - Spawn `evidence-validator` via `Task` with `report_draft_path=<output-dir>/REPORT.md.draft`, `output_path=<output-dir>/evidence-validation.md`, `allow_command_reexec=false`.
  - Read the returned report; apply its `Suggested report status` to the report's frontmatter; remove dropped citations from the final `REPORT.md`; if any dropped, add a "Grounding Gaps" entry referencing them.
- **Audit log addition**: add `evidence_validator_path` to the Wave 5 audit footer.
- **Output contract change**: none — `status: partial` is already in the contract.

### `confidence-calibrator` integration

- **Where (Tier 1)**: `SKILL.md:126` (Wave 1 step 4, "Self-calibrate confidence").
- **Change**: replace the inline "the skill re-grades" with `Task` spawn of `confidence-calibrator` with `card_path=<output-dir>/tier1-hypothesis.md`, `rubric_path=src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`, `card_tier=1`, `flags_context=<wave 0 parsed flags>`. The agent's `Calibrated confidence` and `Verdict` feed directly into the Wave 2 decision.
- **Where (Tier 2)**: `SKILL.md:185-186` — between Wave 3 step 3 ("Wait for all agents to complete. Read each card") and step 4 ("Distill candidate fixes"). After all hypothesis agents return, spawn N `confidence-calibrator` instances in parallel (one per card); the calibrated scores feed into step 4's clustering (strong cards weighted higher when picking the consensus/competing/outlier verdict).
- **Audit log addition**: add `calibration_report_paths: [...]` to the Wave 1 and Wave 3 audit entries.

### Order of operations

1. Ship `evidence-validator` first — it is the load-bearing defender of the hallucination contract.
2. Ship `confidence-calibrator` second — it tightens the escalation gate against anchoring bias.
3. Re-run the existing eval suite at `.dev/eval-workspaces/sc-troubleshoot/evals/evals.json` after each ships. If intermittent-case scenarios start failing visibly, revisit Candidate C (`reproducer-builder`).

### Failure handling additions to `SKILL.md` Error Handling table

The Error Handling table at `SKILL.md:329-342` must gain two rows so the skill degrades gracefully when the new agents misbehave:

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `evidence-validator` agent fails (subprocess crash, timeout, or returns malformed report) | Inline-validate citations in the orchestrator context (the original Wave 5 step 3 behavior); mark `status: partial` and add a Grounding Gap entry noting the validator was unavailable | None — the inline path is the fallback |
| `confidence-calibrator` agent fails for any card | Fall back to inline orchestrator calibration for that card; mark the card with `calibration: inline-fallback` in the audit log; do NOT block escalation on a missing calibration | None |

Without these rows, the new dependencies become hard-fail points for an otherwise-working skill.

### What this design deliberately does NOT do

- Does not add a new wave or change the wave count.
- Does not modify the agent-selection table at `SKILL.md:162-169` (the new agents are orchestration helpers, not hypothesis-producing specialists).
- Does not change the output contract.
- Does not pre-create the agent .md files — that is a follow-up after the user reviews and approves this design.

## Open questions for the human

These are the judgement calls left for you. The reviewer flagged them as decisions that require product/architectural taste, not unambiguous fixes.

### Q1 — Is `evidence-validator` actually a new agent, or `audit-validator` reskinned?

`src/superclaude/agents/audit-validator.md` already exists as a "spot-check validator verifying claim accuracy by re-testing independently, DO NOT modify any file". It is currently scoped to cleanup-audit findings with a fixed sample rate (5 per 50 files). The proposed `evidence-validator` is the same shape — independent verifier, no mutations, citation-by-citation pass/fail — but generalized to "report draft + evidence list" rather than "audit findings + file list".

**Options**:
- **(a)** Ship `evidence-validator` as a separate agent (current design). Tradeoff: two agents that do conceptually identical work for different artifact types; some duplication.
- **(b)** Generalize `audit-validator` to accept a "validation profile" (audit-findings vs. report-evidence) and keep one agent. Tradeoff: one agent grows a mode switch; less duplication; but `audit-validator`'s heavy "Check 5: Wiring Claim Verification" is dead weight for troubleshoot reports.
- **(c)** Keep them separate but extract a shared `refs/independent-verification-protocol.md` they both reference. Tradeoff: middle ground.

The design as proposed assumes (a). The reviewer's lean is (c) if you anticipate more independent-verifier agents (rf-qa, future evaluators) and (a) if you don't.

### Q2 — Could `self-review` be extended in Wave 4 instead of adding `evidence-validator` to Wave 5?

`self-review` (`src/superclaude/agents/self-review.md`) is already invoked at SKILL.md:223 (Wave 4) as the post-adversarial-merge sanity check. Its four questions are tests/edge-cases/requirements/follow-up — none of them touch citation validation. If a fifth question ("evidence cited in the merged proposal is real and matches the cited files") were added, plus a corresponding pass through the file:line list, the work could happen in Wave 4 without a new agent.

**Pro extending `self-review`**: one fewer agent, one fewer wave-5 dependency, validation happens before adversarial merge ships.
**Pro a separate `evidence-validator`**: Wave 4 only runs for Tier 2; Tier 1 reports also need citation validation, so something must run in Wave 5 regardless. Extending `self-review` would still leave a Wave-5 gap for Tier 1. The proposed `evidence-validator` runs **every tier**, which is the right shape.

The reviewer's lean: keep `evidence-validator` as a separate agent — the Tier 1 coverage gap is the deciding factor — but the doc should explicitly acknowledge it considered and rejected extending `self-review`.

### Q3 — Did `reproducer-builder` get killed too quickly?

The adversarial debate Round 2 verdict on Candidate C was "defer until eval data shows the protocol losing on intermittent cases". But the eval workspace at `.dev/eval-workspaces/sc-troubleshoot/evals/` already contains an intermittent case (eval 2 — "test passes locally, fails in CI" is a CI-only flakiness symptom). The defer rationale ("revisit after running the existing eval suite") is partially answered before it is asked.

**Options**:
- **(a)** Keep deferring — argue eval 2 is a *single* case, not enough signal to justify the agent yet. Wait for ≥2-3 intermittent-case failures across evals before adding.
- **(b)** Promote `reproducer-builder` to a v1 ship alongside the other two, on the grounds that the eval workspace already includes the canonical flaky-CI case.
- **(c)** Ship a *minimal* v1 of `reproducer-builder` — narrower than the current proposal, just "when `--type test` and reproducibility scores 0.0, attempt the reproducer in a small loop and report stability".

The reviewer's lean: (c) is the right call. The eval workspace has the signal; deferring entirely smells like the easy way out. But this is a roadmap-shape question, not a design-correctness question.

### Q4 — Bash tool on `evidence-validator` — necessary or risk-without-payoff?

The `tools:` field includes `Bash` to support `allow_command_reexec=true`. The agent's own Boundaries say "Will Not: Execute mutating commands (even if `allow_command_reexec=true`)" — meaning the agent itself filters which commands to run.

A self-enforced filter on a Bash-allowed agent is a softer guarantee than a no-Bash agent. The reviewer's read: as long as the orchestrator *never* sets `allow_command_reexec=true` in v1 (which the integration plan confirms — `allow_command_reexec=false` is hardcoded), Bash provides no v1 value and adds risk surface.

**Options**:
- **(a)** Drop `Bash` from the tools list for v1. Re-add when the orchestrator actually flips `allow_command_reexec=true`, which the design says is a future enhancement anyway.
- **(b)** Keep `Bash` to avoid a frontmatter change later. Tradeoff: agent has a capability it never uses, which violates the broader "least privilege" intuition for agent design.

The reviewer's lean: (a). Land Bash when the feature that needs it lands.

### Q5 — Does `confidence-calibrator` overlap with the orchestrator's existing inline calibration so much that the agent earns its keep only via the anchoring claim?

The rubric application itself is mechanical (read card, score five dimensions, average, apply escalation rules). The orchestrator can already do this. The agent's value proposition is **independence from the formation context**. As the in-place edits softened above, this is a *real* effect but partial — the card is still input. If the anchoring delta in practice turns out to be small (e.g., calibrated confidence diverges from inline confidence by < 0.05 on average), the agent does not earn its overhead.

This is a question only eval data can answer. The reviewer recommends: before declaring `confidence-calibrator` v1-ready, run evals C1 and C2 *twice* — once with inline calibration and once with the agent — and measure the delta. If the delta is < 0.05 average, the agent is a placebo and the design should fall back to inline calibration with a comment explaining why.

### Q6 — `evidence-validator` integration replaces a "non-negotiable" inline step. What if the agent itself silently produces wrong results?

The in-place edit above added "Failure handling additions to SKILL.md Error Handling table" rows for subprocess crash and malformed output. But **silently wrong output** (validator says all 10 citations verified when 3 actually fail) is not caught by those rows. The orchestrator would ship a `success` report containing hallucinated citations — the exact failure mode the protocol exists to prevent.

**Mitigations to consider**:
- **(a)** Have the orchestrator re-sample ~20% of validator-verified citations and compare. If discrepancies exceed a threshold, the orchestrator overrides the validator and marks the report `partial`.
- **(b)** Periodic offline meta-eval: run the validator on a fixture report with known-good and known-bad citations and check it correctly partitions them. If the fixture eval fails, alert.
- **(c)** Accept the risk because Anthropic-grade agents on a mechanical task are unlikely to silently fabricate validation results. The orchestrator-resample-20% adds cost without clear payoff at expected accuracy.

This is a "how paranoid is paranoid enough?" question for the protocol's hallucination contract. The reviewer recommends (b) as the cheapest meaningful guard, but it requires a meta-eval fixture that does not exist yet.

### Q7 — Frontmatter convention: `tools:` field present or absent?

The in-place edits switched the `tools:` field from JSON-array `[Read, Grep, Glob, Bash]` to comma-string `Read, Grep, Glob, Bash` to match `audit-validator.md`. However, the *domain* agents (`root-cause-analyst.md`, `self-review.md`, `quality-engineer.md`) have **no `tools:` field at all** — they inherit the parent's allowed-tools set.

The `tools:` field appears on the audit-family and rf-family agents — i.e., agents that are spawned via `Task` for a tightly-scoped purpose with a defined verification protocol. That matches the proposed `evidence-validator` and `confidence-calibrator` profile, so keeping `tools:` is correct.

The remaining judgment call: does `audit-validator`'s `model: sonnet` + `maxTurns: 25` + `permissionMode: plan` triple apply here too? The in-place edits added `model: sonnet` but omitted `maxTurns` and `permissionMode`.

- `evidence-validator` does N file reads where N ≈ 10-30 citations + some Grep/Glob; 25 turns may be tight for the upper end. Consider `maxTurns: 50`.
- `confidence-calibrator` does ~5-8 reads (rubric + card + 3-5 spot-check files); 25 turns is comfortable.
- `permissionMode: plan` makes sense for both — they should never need to ask for elevated permissions.

The reviewer recommends explicitly adding `maxTurns` and `permissionMode` before these ship.
