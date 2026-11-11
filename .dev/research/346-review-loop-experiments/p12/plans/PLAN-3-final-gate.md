# PLAN 3: A/B test of a final whole-document gate after the loop's PASS, with a bounded gate loop and a stall rule

Design 3.3 of the research report (the merge-queue analog: test the artifact in the state it will ship in). Against Stage 2 arm 3, after the loop ends in PASS, one labelled whole-document first review (the gate review) runs in a fresh context with no loop history. A gate PASS ends the run. Gate blocking findings start at most one gate loop (one revise, one scoped re-review); a FAIL there, or a stall, escalates. You (1) make the smallest product change, test-first, on branch `346Claude-ab3-final-gate`; (2) build an A/B harness in `$SP/p12/ab3/` from copies of the Stage 2 tooling; (3) test the tooling offline; (4) stop with a READY report, or run the experiment if you can launch subagents; (5) analyze into `$SP/p12/ab3/RESULTS.md`.

## 0. Read this first

You implement ONE A/B experiment, from this file alone. Do not open other plans in this folder. Read the whole file before you run anything, then run the self-check (section 8) before Part A.

Hard rules (from `/home/user/IronClaude/CLAUDE.md`; binding):

- Python only through UV: `uv run ...`, `uv pip ...`. Never `pip`, `python -m` or a bare `python script.py`. Scratch scripts outside the repo run as `uv run --no-project python <file>`; their tests run as `uv run --no-project --with pytest pytest <dir>`.
- Never stage or commit anything under `.claude/` (gitignored sync output of `src/superclaude/`). If `git add` ever needs `-f` for a `.claude/` path, stop: that is the violation.
- Edit product sources only under `src/superclaude/`, `plugins/superclaude/` and `tests/`. After editing, run `make sync-dev` and `make verify-sync`.
- `src/superclaude/commands/spec-panel.md` must stay at or below 500 lines (it is 490 now). Check with `wc -l`.
- Installed primitives (the rules file, spec-panel) must never name a `src/superclaude/...` path.
- Branch: `346Claude-ab3-final-gate`, created from `346Claude-p8a-first-review-grading` at commit `69ac8b3335564fb5551980e984c5d9b763039cc1` (open PR #484, base `346Claude-integration`). Commit and push the branch to `origin` (`https://github.com/IronbellyOrg/IronClaude`). Do NOT open a pull request. Never touch the upstream `SuperClaude-Org/SuperClaude_Framework` (no remote, fetch, push or gh call).
- Never edit anything under `$SP/p11/` (Stage 2 data, read-only) and never switch branches in the shared checkout `/home/user/IronClaude` (other sessions use it). You work in a private clone (Part A1).
- Experiment loop workers are Sonnet subagents in the decision stratum and Haiku subagents (Agent model `haiku`) in the Haiku robustness stratum (section 3b); the AUD/AUD2 audits are always Sonnet. At most 6 workers of this experiment may run at once, both strata together (the session limit is 20 across three parallel experiments).
- Owner decisions D1-D5 in `$SP/p14/DECISIONS-ADDENDUM.md` are binding and already applied in this file: D1 keeps the zones of section 3, D2 is the loop-only token convention (section 2), D3 the Haiku stratum (3b), D4 the extension (3c), D5 the private clone (A1).

## 1. Background you need

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export AB=$SP/p12/ab3
```

| What | Path |
|---|---|
| Research report (design source) | `$SP/p12/RESEARCH-REPORT.md`, section 3.3 and section 4 |
| Stage 2 harness (copy, never edit) | `$SP/p11/harness.py`, `$SP/p11/advance.py` |
| Stage 2 summary | `$SP/p11/STAGE2-REPORT.md` |
| Baseline runs (arm 3, read-only) | `$SP/p11/runs/a3-r1` .. `a3-r6` (`state.json`, `PROMPT-*.md`, `ws/`, `aud/`) |
| Baseline audit reports | `$SP/p11/runs/a3-rK/aud/ws/.dev/orca-command-refactor/review/audit.md` |
| Frozen audit rules file | `$SP/p11/rules.md`, sha256 `3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8` |
| Frozen audit command | `git show 69ac8b3335564fb5551980e984c5d9b763039cc1:src/superclaude/commands/spec-panel.md`, sha256 `e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494` |
| S1 repo overlay (sandbox seed) | `$SP/exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay` |
| Spec under review | overlay `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`: 57,763 bytes, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Worker transcripts (JSONL, one per launched agent) | `/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output`; the first user message names the PROMPT file |
| Shared second audit of baseline (made by the coordinator; all six reports present on 2026-11-10) | `$SP/p12/baseline-audit2/results.json` |
| Owner decisions D1-D5 (binding) | `$SP/p14/DECISIONS-ADDENDUM.md` |
| Shared Haiku baseline (made by the coordinator, may be absent; consume, never run your own) | `$SP/p14/haiku-baseline/results.json` (runs under `$SP/p14/haiku-baseline/runs/a3-r1` .. `a3-r6`) |
| Your experiment directory | `$AB` (clone `$AB/repo`, harness, `runs/`, `tests/`, `RESULTS.md`) |

**The loop under test.** `/sc:spec-panel --mode critique` reviews a document; a coordinator runs a loop capped at 3 reviews and 2 fix cycles: first review (R1), revise only the blocking findings in place (V1), scoped re-review of the changed lines plus prior blockers (R2), V2, R3; a review PASS ends the loop; FAIL at review 3 escalates. The coordinator briefs workers with prompts that live in the rules file `src/superclaude/rules/prompts/document_review_loop_prompts.md` (installed to `~/.claude/rules/prompts/`); spec-panel's "Review-loop prompts (hard gate)" section makes reading it mandatory before any re-review or brief. The design under test as baseline is branch `346Claude-p8a-first-review-grading`.

**How Stage 2 ran (you will copy this).** Each replicate ("run") is a sandbox `runs/<run>/` holding `ws/` (copy of the S1 overlay: `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, `specs/orca-worker-contract-spec.md`, plus empty `review/` and `specs/history/`), `home/.claude/rules/prompts/document_review_loop_prompts.md`, `command.md` (the spec-panel text) and `state.json`. `harness.py prep RUN STEP` writes `runs/<run>/PROMPT-<STEP>.md` = the fixed wrapper `WRAP` (sandbox, workspace, home, command and tool rules, then the brief verbatim, then "reply with only `DONE <path>`"); arm 3 uses short pointer briefs ("Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/..."). One Sonnet agent is launched per prompt with the message `Read <absolute PROMPT path> and follow it exactly. Touch nothing outside the sandbox directory it names.` `advance.py` found finished workers (DONE in the transcript), ran `harness.py ingest` (verdict, blocking ids, spec bytes, output tokens) and prepped the next step. Step outputs (relative to `ws/`, all under `.dev/orca-command-refactor/`): R1 `review/round1.md`, V1 `review/revise1.md` (spec copied to `specs/history/spec-v1.md` before V1), R2 `review/round2.md`, V2 `review/revise2.md` (snapshot `spec-v2.md`), R3 `review/round3.md`. Stop rules: R1/R2 FAIL goes to the next revise; any review PASS goes to AUD; R3 always goes to AUD (FAIL at R3 = escalated, loop not PASS). **AUD** = the frozen whole-document audit: fresh sandbox `runs/<run>/aud/` with the overlay, the final spec, the frozen command and frozen rules file; brief "This is a labelled whole-document audit of the final spec: a first review of the whole document. Review per the FIRST-REVIEW prompt ..."; output `aud/ws/.dev/orca-command-refactor/review/audit.md`. Read `$SP/p11/runs/a3-r1/PROMPT-R1.md`, `PROMPT-V1.md`, `PROMPT-R2.md`, `PROMPT-AUD.md` and `$SP/p11/runs/a3-r6/PROMPT-R3.md` now; your test arm must reproduce them byte-for-byte except for the sandbox path.

## 2. Baseline (Stage 2 arm 3, n=6, reused read-only)

Verified from `state.json`, the spec files and the transcripts:

| run | reviews | loop end | final spec bytes | growth | loop output tokens | audit tokens | audit | audit blocking ids (theme) |
|---|---|---|---|---|---|---|---|---|
| a3-r1 | 2 | PASS at R2 | 57,973 | +0.36% | 70,694 | 52,531 | FAIL | B1 T1, B2 T2 |
| a3-r2 | 2 | PASS at R2 | 59,034 | +2.20% | 109,207 | 78,276 | FAIL | F-01 T3, F-02 T1 |
| a3-r3 | 2 | PASS at R2 | 58,196 | +0.75% | 95,213 | 69,081 | FAIL | F-1 T1, F-2 T2 |
| a3-r4 | 2 | PASS at R2 | 57,873 | +0.19% | 81,415 | 59,033 | FAIL | A-01 other, A-02 T2 |
| a3-r5 | 2 | PASS at R2 | 58,448 | +1.19% | 94,998 | 84,759 | PASS | none |
| a3-r6 | 3 | PASS at R3 | 59,941 | +3.77% | 151,017 | 70,581 | FAIL | F-01 T2 |
| **mean** | **2.17** | **6/6 PASS** | | **+1.41%** | **100,424** | **69,044** | **1/6 PASS** | **1.50 per audit** |

Token columns are deduplicated (each message id counted once, section 2 convention below). Per-step baseline means used in section 7: R1 50,577 (50% of the loop), V1 14,255, R2 29,993, R3 28,871 and V2 4,726 (a3-r6 only), audit 69,044 (69% of the loop).

Baseline constants used below: `B_PASS = 6/6`, `B_REV = 2.17`, `B_GROWTH = 1.41%`, `A_BASE = 100,424` (loop only; every cost rule is a ratio to it), `AUD_BASE = 69,044` (one audit), `B_BASE = 169,468` (loop plus one audit; reported, never decides), `B_BLK = 1.50`, `B_AUDFAIL = 5/6`, `B_THEME = 5/6` (audits with at least one T1, T2 or T3 blocker). Per theme: T1 in 3/6 audits, T2 in 4/6, T3 in 1/6, other in 1/6. Baseline first reviews (k=1): T1 in 6/6, T2 in 2/6, T3 in 3/6.

Token convention (owner decision D2 in `$SP/p14/DECISIONS-ADDENDUM.md`, binding). A transcript logs an assistant message once per content block, every copy with the same `message.id` and usage, so summing lines double-counts. Count each message id ONCE: a step's output tokens = sum over unique `message.id` of the max `message.usage.output_tokens` seen for that id. The earlier figures (loop 243,056, loop plus audit 381,702, and the 0.33M of the first STAGE2-REPORT table) were inflated by this double count and are not used. `LOOP` (= A, the decision metric) sums every loop worker of a run (reviews, revises, verifies, gates, merges, adjudications) and excludes AUD and AUD2, which are measurement instrumentation. Every cost rule is the ratio `R_LOOP = LOOP_T / A_BASE` (= `LOOP_T / 100,424`). `TOK` (= B) = `LOOP` + AUD (first audit only) is reported beside it as `R_B = TOK_T / B_BASE` (= `TOK_T / 169,468`) and never decides. Your `harness.py basetokens` must reproduce the per-run loop and audit totals above within 1%; for a3-r1 R1 the glob finds one Sonnet transcript (49,641 tokens) and two Opus transcripts whose first message names the same prompt: keep the Sonnet one.

If baseline second audits exist under `$SP/p12/baseline-audit2/` when you analyze (Part F), recompute `B_BLK`, `B_AUDFAIL` and `B_THEME` over all 12 baseline audits and use those values; otherwise label every comparison PROVISIONAL (single baseline audit).

## 3. Goal, hypothesis, arms, pre-registered criteria

**Goal.** Decide whether a final whole-document gate with one bounded gate loop should end every review loop.

**Hypothesis** (report 3.3 and section 4; GitHub merge queue / GitLab merge trains, grade C): a scoped PASS verifies the diff but not the whole document; a fresh whole-document first review of the final state, with its blockers fixed once, lowers the residual blockers an independent audit finds. Risks: gate findings restart loops (non-convergence) and cost.

**Arms.** BASELINE = Stage 2 arm 3, runs `a3-r1..a3-r6`, reused read-only. TEST = `b3-r1..b3-r6` (n=6): the arm-3 loop unchanged (R1, V1, R2, V2, R3, no verify step), then `G` (gate review) after the loop's PASS, then, if G has blocking findings and the stall rule does not fire, `GV` (revise with the gate's ids) and `GR` (scoped re-review of the gate fix). Then the two frozen audits.

**Contract change and ceiling.** The scoped loop keeps "at most 2 fix cycles (3 reviews)". The gate adds one gate review, at most one fix cycle and one re-review: hard ceiling **5 reviews and 3 fix cycles per document**. The gate loop numbers its own reviews (`review: 1 of 3` gate, `review: 2 of 3` gate re-review), so no report is ever `review: 4 of 3`, which keeps the pinned "never start a fourth review". Escalation looks like this: a gate re-review FAIL, or a stall, ends the run as escalated to the user with the open gate findings; no second gate loop, no further review. A scoped-loop FAIL at review 3 escalates as before and no gate runs.

**When the gate runs.** After any loop PASS: a scoped PASS at R2 or R3, and also a first review (R1) that passed an unrevised document (report section 4: "do not skip the gate on no-edit runs"; Stage 2 lesson 6).

**Circularity control.** The gate review is the same kind of review as the audit, so the gate's own verdict is never an outcome metric. Outcomes come only from the two frozen audits (AUD, AUD2), which use the frozen baseline command and rules, not the product's GATE prompt.

**Pre-registered decision** (`B_*` from section 2, recomputed from 12 baseline audits if `baseline-audit2` exists). Final loop PASS = `GATE-PASS` or `GATE-LOOP-PASS`.

| Rule | Condition | Baseline numbers |
|---|---|---|
| DROP-1 (gate misses the themes) | theme rate >= 0.80 of test audits (>= 10 of 12 audits carry a T1, T2 or T3 blocker) | report: same three themes in >= 4/5 runs; baseline 5/6 |
| DROP-2 (non-convergence) | final loop PASS < 4/6 | report: convergence below 3/5 |
| DROP-3 (cost) | `R_LOOP > 1.8` (`LOOP_T > 1.8 * A_BASE`, loop including G, GV, GR) | 180,763 loop tokens |
| ADOPT | no DROP, `BLK_T <= 0.67 * B_BLK`, audit FAIL rate <= 0.8 * `B_AUDFAIL` | 1.00 per audit; <= 8/12 audits FAIL |
| INCONCLUSIVE | anything else; or the two audit replicas disagree; or fewer than 5 completed runs | |

Cost convention (D2). DROP-3's limit "1.8x" is unchanged but now applies to `R_LOOP` (loop only, AUD and AUD2 excluded); print `R_B` beside it, which never decides. Predicted `R_LOOP` is about 2.05 (range 1.72-2.13, section 7), so **DROP-3 is expected to fire**. Under the old loop-plus-audit convention it passed (`R_B` about 1.62). This plan keeps the stricter loop-only result. Because DROP-3 is checked before ADOPT, the expected outcome is DROP-3 whatever the audit blockers show, unless gate loops turn out rare and the gate review cheap. The coordinator should know this before launch; the rule is not changed here.

### 3b. Haiku robustness stratum (owner decision D3; secondary, never pooled)

- Runs `b3h-r1..b3h-r4` (n=4) are the TEST arm with every loop worker on Haiku 5.5 (Agent model value `haiku`): R1, V1, V2, R2, R3, the gate reviewer G, GV and GR. AUD and AUD2 always run on Sonnet with the frozen command and rules, two audits per final spec. Prompts are byte-identical to the Sonnet runs.
- The comparison is the shared Haiku baseline `$SP/p14/haiku-baseline/results.json`: the Stage 2 arm-3 design with Haiku loop workers, n=6, made by the coordinator. Consume it and never run your own. Take `H_BLK` (mean blockers per audit over its two audits per spec) and `H_LOOP` (mean loop tokens) from it. If its audit reports exist beside its runs, rescore them with `blocking_findings()`, use the rescored values and list any difference.
- Metric: `HR = BLK_TH / H_BLK` (Haiku test mean blockers per audit / Haiku baseline); the relative reduction is `1 - HR`. Also report the Haiku final loop PASS, gate loops, stalls, growth, the harness-failure rate (runs lost or needing a MANUAL relaunch, per run) and `R_LOOP_H = LOOP_TH / H_LOOP`, all as report-only figures. Haiku is judged only relatively, because its baseline is worse.
- Decision role: ADOPT additionally requires `1 - HR > 0` and a Haiku harness-failure rate no more than 1/4 (one run in four) above the Haiku baseline's. If the stratum points the other way, a Sonnet ADOPT becomes INCONCLUSIVE ("Haiku stratum disagrees"), and section 3c does not apply. If the stratum or `results.json` is missing, a clear Sonnet ADOPT reads `ADOPT (Haiku robustness pending)`. Haiku never triggers or vetoes a DROP and is never pooled into any Sonnet number.

### 3c. Adaptive extension (owner decision D4)

If the Sonnet n=6 outcome, after the replica-agreement check, is INCONCLUSIVE, run `harness.py build --extend` once. It adds 3 Sonnet replicates `b3-r7..b3-r9` (same harness, two audits each). Recompute every Sonnet metric and rule at n=9 (18 test audits). Count limits keep their fractions: DROP-1 theme rate `>= 15/18`; DROP-2 final loop PASS `< 6/9`; ADOPT audit FAIL `<= 12/18`; INCONCLUSIVE if fewer than 8 of 9 runs complete. Then decide. If the outcome is still INCONCLUSIVE, the final verdict is INCONCLUSIVE; never extend a second time without the owner. The Haiku stratum stays at n=4.

## Part A. Product change (test-first)

### A1. Private clone and branch

Private clones are accepted (owner decision D5): in this environment each implementer works in its own full `git clone` under `$SP`, with no git worktree and no Orca. The main checkout is shared, so never switch its branch.

```bash
mkdir -p $AB
git clone --branch 346Claude-p8a-first-review-grading /home/user/IronClaude $AB/repo
cd $AB/repo
git remote set-url origin https://github.com/IronbellyOrg/IronClaude
git remote -v                                   # only origin = IronbellyOrg/IronClaude
test "$(git rev-parse HEAD)" = 69ac8b3335564fb5551980e984c5d9b763039cc1 && echo BASE-OK
git fetch origin 346Claude-p8a-first-review-grading && git log --oneline -1 origin/346Claude-p8a-first-review-grading
git checkout -b 346Claude-ab3-final-gate
uv venv && make install
uv run pytest -q -p no:cacheprovider tests/skills/test_review_brief_placement.py \
  tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py \
  tests/skills/test_review_severity_mapping.py tests/skills/test_review_prompt_overrides.py \
  tests/skills/test_review_severity_rule.py tests/unit/test_cli_install.py      # expect 273 passed
```

If `git fetch` fails for lack of credentials, continue (BASE-OK is the binding check) and push at the end; if the push also fails, report it in the READY report instead of working around it. If origin's branch has moved past `69ac8b33`, stay on `69ac8b33` (the baseline was run on it) and say so in the READY report.

Pinned tests you must keep green (read them before editing): `tests/skills/test_review_brief_placement.py` (all prompt text lives only in the rules file; labels `- First-review brief: "`, `- Re-review brief: "`, `- Revise brief: "`; the spec-panel hard-gate paragraph is one sentence and names no prompt), `test_spec_panel_review_loop.py` (seven single-line Review Loop bullets in order; cap literal `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`), `test_review_loop_extension.py` (bullet 5 must contain `whole-document assurance needs a separate, labelled first review` and `never start a fourth review`; the section must not contain the words parser, script, state machine, transcript, asynchronous), `test_review_severity_mapping.py`, `test_review_prompt_overrides.py` (every quoted brief passes `lint_brief`; no finding quota anywhere under `src/` or `plugins/`), `tests/unit/test_cli_install.py` (the installer ships the list of rules files; you add no new file, so it does not change).

### A2. New static test first: `tests/skills/test_review_final_gate.py`

Create the file with exactly this content, run it, and see it FAIL (7 failures, 1 pass) before editing:

```python
"""Pins for the final whole-document gate of the review loop (#346, A/B design 3).

Enforcement type: STATIC - assertions over the rules file and both spec-panel copies.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.skills.test_review_prompt_overrides import lint_brief

_REPO = Path(__file__).resolve().parents[2]
RULES = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
LABEL = "This is a first review of a complete document; no prior rounds exist. "


def _text() -> str:
    return RULES.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _brief(label: str) -> str:
    m = re.search(rf'- {label}: "([^"]+)"', _text())
    assert m, label
    return m.group(1)


def test_gate_prompt_follows_revise_and_precedes_never():
    t = _text()
    assert t.index("### REVISE prompt") < t.index("### GATE prompt") < t.index("## Never")


def test_gate_brief_is_the_first_review_brief_with_the_label():
    assert _brief("Gate brief") == LABEL + _brief("First-review brief")


def test_gate_brief_passes_the_brief_lint():
    assert lint_brief(_brief("Gate brief")) == []


def test_routing_rows_and_own_numbering():
    t = _text()
    assert (
        "| After the loop's PASS (a scoped PASS, or a first review that passed) "
        "| GATE prompt, once |" in t
    )
    assert (
        "| After a gate review with open blocking findings | REVISE prompt, then one "
        "RE-REVIEW prompt: the gate loop |" in t
    )
    assert "so no report is ever a fourth review" in _flat(t)


def test_gate_loop_is_bounded_with_a_stall_rule_and_a_ceiling():
    flat = _flat(_text())
    for literal in (
        "fresh context that has seen no report of this loop",
        "starts one gate loop: one REVISE prompt with the gate's blocking ids, then one "
        "RE-REVIEW prompt with the gate report as PRIOR",
        "with no second gate loop and no further review",
        "**Stall rule**: if every blocking finding of the gate review repeats a blocking "
        "finding of an earlier review in this loop",
        "escalate to the user with them and start no gate loop",
        "at most 5 reviews and 3 fix cycles in all",
    ):
        assert literal in flat, literal


@pytest.mark.parametrize("rel", SPEC_PANELS)
def test_spec_panel_bullet_five_names_the_gate_and_the_ceiling(rel):
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    bullet = _flat(next(line for line in lines[start:] if line.startswith("5. **")))
    for literal in (
        "whole-document assurance needs a separate, labelled first review, the gate review,",
        "never start a fourth review",
        "they start at most one gate loop of one fix cycle and one re-review",
        "a FAIL or a stall there escalates to the user",
        "a document gets at most 5 reviews and 3 fix cycles in all",
    ):
        assert literal in bullet, (rel, literal)
    assert "whose blockers are escalated" not in bullet
    cap = _flat(next(line for line in lines[start:] if line.startswith("4. **")))
    assert (
        "at most 2 fix cycles (3 reviews), then escalate to the user with the open "
        "blocking findings" in cap
    )


def test_spec_panel_stays_within_500_lines():
    for rel in SPEC_PANELS:
        assert len((_REPO / rel).read_text(encoding="utf-8").splitlines()) <= 500
```

```bash
cd $AB/repo && uv run pytest -q tests/skills/test_review_final_gate.py      # 7 failed, 1 passed
```

### A3. Edits

**Rules file** `src/superclaude/rules/prompts/document_review_loop_prompts.md` (three edits):

1. In `## When to use which prompt`, add these two rows directly after the row `| After a review report with open blocking findings, to revise | REVISE prompt |`:
   `| After the loop's PASS (a scoped PASS, or a first review that passed) | GATE prompt, once |`
   `| After a gate review with open blocking findings | REVISE prompt, then one RE-REVIEW prompt: the gate loop |`
2. After the paragraph `` At `review: 3` with an open blocking finding the loop escalates to the user; no REVISE prompt and no fourth review. `` add a blank line and this paragraph: `` The gate loop under the GATE prompt numbers its own reviews (`review: 1 of 3` for the gate review, `review: 2 of 3` for its re-review), so no report is ever a fourth review. ``
3. Insert this block between the `### REVISE prompt` section and `## Never` (one blank line on each side):

   ```text
   ### GATE prompt

   Run it once, after the loop's PASS, on the document as it then stands. Brief the gate reviewer in a fresh context that has seen no report of this loop, and grade with the FIRST-REVIEW prompt's grading check.

   - **Gate loop**: a blocking finding of the gate review starts one gate loop: one REVISE prompt with the gate's blocking ids, then one RE-REVIEW prompt with the gate report as PRIOR. A PASS of that re-review ends the loop; a FAIL escalates to the user with the open blocking findings, with no second gate loop and no further review.
   - **Stall rule**: if every blocking finding of the gate review repeats a blocking finding of an earlier review in this loop (the same stated text and the same wrong outcome), the loop is stalled: escalate to the user with them and start no gate loop.
   - **Ceiling**: the loop's 3 reviews and 2 fix cycles, plus the gate review, one fix cycle and one re-review: at most 5 reviews and 3 fix cycles in all.
   - Gate brief: "This is a first review of a complete document; no prior rounds exist. Review the candidate {{CANDIDATE}} (sha256 of the file) against the requirements it states, review 1 of 3. Inspect behavior and the dependencies it touches. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. If an input is missing or unreadable, return incomplete. Do not edit the candidate and do not start another review. State what you covered."
   ```

**spec-panel, both copies** (`src/superclaude/commands/spec-panel.md` and `plugins/superclaude/commands/spec-panel.md`; their Review Loop sections are identical): in bullet `5. **Re-review output**`, replace
`and whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review.`
with
`and whole-document assurance needs a separate, labelled first review, the gate review, whose blockers never start a fourth review: they start at most one gate loop of one fix cycle and one re-review, a FAIL or a stall there escalates to the user, and a document gets at most 5 reviews and 3 fix cycles in all.`
The bullet stays one line; the file stays at 490 lines (plugins copy unchanged in length); no banned word (parser, script, state machine, transcript, asynchronous) is added.

Not changed: `HOW-WE-WORK.md` (both copies; it points at the hard gate, which already sends the coordinator to the rules file), bullet 4 (the per-loop cap literal stays), the installer. Existing tests stay green unchanged, and why: `test_review_loop_extension.py::test_scoped_pass_names_its_coverage` checks the substrings `whole-document assurance needs a separate, labelled first review` and `never start a fourth review`, both kept; no test pins `whose blockers are escalated` (verified with `grep -rn "are escalated" tests` returning nothing); `test_spec_panel_review_loop.py` (seven single-line bullets, cap literals in bullet 4) unchanged; `test_review_brief_placement.py` (three labels remain; the gate paragraph of spec-panel is untouched; no prompt text moves into the command); `test_review_prompt_overrides.py` (three briefs untouched, Gate brief passes the lint). Expected: no existing test changes.

```bash
cd $AB/repo && uv run pytest -q tests/skills/test_review_final_gate.py      # 8 passed
grep -rn "are escalated" tests                                              # no output
```

### A4. Verify, commit, push (no PR)

```bash
cd $AB/repo
wc -l src/superclaude/commands/spec-panel.md          # <= 500
grep -rn 'src/superclaude' src/superclaude/rules/prompts/document_review_loop_prompts.md   # no output
make lint
make sync-dev && make verify-sync
uv run pytest -q tests/skills tests/unit                # about 6 minutes; expect exactly 1 failure, pre-existing on 69ac8b33:
                                                        # tests/skills/test_task_workspace_smoke.py::test_installer_ships_scripts_and_documented_invocation_runs
git status --short                                      # only the files listed in Part A; nothing under .claude/
git add src/superclaude/rules/prompts/document_review_loop_prompts.md src/superclaude/commands/spec-panel.md plugins/superclaude/commands/spec-panel.md tests/skills/test_review_final_gate.py
git commit -F - <<'EOF'
experiment(review): final whole-document gate with one bounded gate loop (A/B design 3, refs #346)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Y28dBfZHbPhB1U1EM1XTUj
EOF
git push -u origin 346Claude-ab3-final-gate
git rev-parse HEAD                                      # this is PRODUCT_REF for Part B
```

If a test outside the files you touched fails, check whether it is pre-existing before you commit: `git stash -u && uv run pytest -q <that test>; git stash pop` (your private clone only). A failure that also happens without your changes is reported as pre-existing in the READY report; never "fix" unrelated tests.

## Part B. A/B harness in `$AB` (= `$SP/p12/ab3`)

### B1. Copy the Stage 2 tooling

```bash
mkdir -p $AB/runs $AB/tests
cp $SP/p11/harness.py $SP/p11/advance.py $AB/
```

Edit only the copies in `$AB`. Keep these byte-for-byte as in p11: `S1`, `D`, `SPEC`, `FLAGS`, `AUD_OUT`, `WRAP`, `CMDPART`, `section()`, `git_show()`, the arm-3 branches of `new_brief()` and the AUD brief text in `prep()`. Everything the workers read must match Stage 2 arm 3 except the factor under test.

### B2. Common changes to `harness.py`

1. Constants (replace the p11 ones):

```python
import os
P12 = SP/"p12"; AB = P12/"ab3"; RUNS = AB/"runs"
REPO = str(AB/"repo")                       # git_show reads the private clone
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"   # frozen audit command
PRODUCT_REF = "<full sha printed at the end of A4>"     # test-arm command + rules file
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
AUD_CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
AUD_RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
TASKS_GLOB = os.environ.get("AB_TASKS_GLOB", "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output")
MAX_CONCURRENT = int(os.environ.get("AB_MAX", "6"))
DESIGN = "b3"
```

   `arm_of(run)` returns `3` for every run (so `new_brief` always takes the arm-3 pointer-brief path). `P11` keeps pointing at `$SP/p11` (read-only: `rules.md` and baseline runs).
2. `build()`: create `b3-r1` .. `b3-r6` exactly like p11 arm 3 (overlay copy, `review/`, `specs/history/`, `home/.claude/rules/prompts/`), except `command.md` = `git_show(PRODUCT_REF, "src/superclaude/commands/spec-panel.md")` and the rules file = `git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md")`. Assert the copied spec's sha256 is `SPEC_SHA`. Do not write `P11/"rules.md"`. Initial `state.json`: `{"run", "design": DESIGN, "rep", "product_ref": PRODUCT_REF, "cmd_sha", "rules_sha", "done": [], "log": {}, "launched": {}, "noted_unactioned": [], "loop_end": null, "manual": []}`. 
3. Audits: replace the AUD branch of `prep()` with `prep_audit(run, k)`, k in {1, 2}: sandbox `runs/<run>/aud` (k=1, prompt `PROMPT-AUD.md`) or `runs/<run>/aud2` (k=2, prompt `PROMPT-AUD2.md`); identical to p11 otherwise, except the command comes from `git_show(BASE_REF, ...)` (assert sha256 `AUD_CMD_SHA`) and the rules file is copied from `P11/"rules.md"` (assert `AUD_RULES_SHA`). Brief text unchanged. Output `aud*/ws/.dev/orca-command-refactor/review/audit.md`. `ingest` for `AUD2` reads from `aud2/ws`.
4. Blocking ids: in `ids_from()` replace the first regex with `r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\b[^:\n]{0,60}:\s*(.+)$"` (the p11 one missed "Blocking finding ids to repair, and only these: **F1, F2**" in a3-r1) and add `parse_ids(raw) -> list[str]` (section B4). Every place that needs ids uses `parse_ids(ids_from(path))`. If a report's verdict is FAIL and `parse_ids` returns `[]`, the tooling prints `MANUAL <run> <step> no blocking ids parsed` and waits; you read the report's Reviser brief and run `harness.py setids RUN STEP "F1, F2"` (recorded in `state["manual"]`).
5. Output tokens: `harness.py tokens` scans `TASKS_GLOB`; a transcript belongs to `(run, step)` when its first user message contains `p12/ab3/runs/<run>/PROMPT-<STEP>.md`; sum, over unique `message.id`, the max `message.usage.output_tokens` of the assistant lines (section 2; never sum lines); keep only transcripts whose assistant `model` contains the step's expected model (`sonnet` for every step of a Sonnet run and for AUD/AUD2 of every run, `haiku` for the loop steps of a Haiku run) and print a WARN for any other model; if several remain for one step, keep the one that contains a `DONE` handback and has the most tokens, and print a WARN. Store as `state["log"][step]["output_tokens"]`. `harness.py basetokens` does the same for `p11/runs/(a3-r\d)/PROMPT-(\w+)\.md` and prints per-run loop and audit totals (must match section 2: loop mean 100,424, audit mean 69,044).
6. Done detection (in `advance.py`): a launched step is finished when its output file exists AND either a transcript for it (rule 5) contains a `SubagentHandback` or final assistant text with `DONE`, or no transcript is found and the output file has not changed for 180 seconds. A launched step with no output after 60 minutes prints `WARN stale <run> <step>`.
7. Launch ledger: `advance.py` (without `--dry-run`) records every prompt it prints in `state["launched"][step]` (ISO time). Running = launched and not yet ingested. It prints at most `MAX_CONCURRENT - running` new prompts, ordered by run number, then step order. `harness.py unlaunch RUN STEP` removes a ledger entry (for a prompt that could not be launched, or a worker that died without output; relaunch once, a second failure marks the run `lost`).
8. Keep the p11 stop for verdict `INCOMPLETE` or `NONE` on a review: print `MANUAL`, relaunch once via `unlaunch`, then mark the run `lost`. Lost runs are reported and excluded; fewer than 5 completed runs makes the result INCONCLUSIVE.
9. **Strata, decision file and extension (owner decisions D2-D4).** `harness.py build [--stratum sonnet|haiku] [--extend]`: the default `sonnet` creates `b3-r1..b3-r6`; `--stratum haiku` creates `b3h-r1..b3h-r4`; `--extend` (Sonnet only; refused unless `$AB/metrics.json` records a Sonnet n=6 outcome of INCONCLUSIVE, and refused if `b3-r7` exists) creates `b3-r7..b3-r9`. Every `state.json` gets `"stratum": "sonnet"|"haiku"` and `"loop_model": "sonnet"|"haiku"`, and every log, telemetry and metrics record copies `stratum`. `advance.py` prints `LAUNCH <absolute path> model=<m>`, with `m` = the run's `loop_model` for loop steps and always `sonnet` for AUD/AUD2 (assert it: Haiku never audits). Prompt files are identical across strata; the model is the only difference. Sonnet runs are printed before Haiku runs. Decision constants (`A_BASE` 100,424, `AUD_BASE` 69,044, `B_BASE` 169,468, the default `B_*` of section 2, every threshold of section 3 including the n=9 fractions of 3c, `N_SONNET` 6, `N_HAIKU` 4, `N_EXTEND` 3, the Haiku baseline path) live in `$AB/decision.json`, written once from sections 2-3 and read by `analyze`; no threshold literal appears in code. `analyze` computes `R_LOOP` (decides) and `R_B` (reported) in one function and writes per-stratum tables.

### B3. Wrapper and briefs (verbatim)

Every prompt is `WRAP.format(sb=<sandbox dir>, wsdir="ws", cmdpart=<CMDPART or "">, brief=<brief>)`, exactly as p11. With `ctx` as in p11 (`First read .dev/orca-command-refactor/README.md (binding shared context; the files under .dev/orca-command-refactor/inventory/ are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).`), the reused arm-3 briefs are (`{SPEC}` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, `{FLAGS}` = `--mode critique --focus requirements,architecture`, `{R}` = `.dev/orca-command-refactor/review`, `{H}` = `.dev/orca-command-refactor/specs/history`):

- First review (CMDPART): `Run /sc:spec-panel @{SPEC} {FLAGS} . Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}.\nWrite the full report to {out}. Do not edit anything else. {ctx}`
- Re-review (CMDPART): `Run /sc:spec-panel @{SPEC} {FLAGS} --re-review {prior} --baseline {base} . Re-review per the RE-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}, baseline={base}, prior={prior}.\nWrite the full report to {out}. Do not edit anything else. {ctx}`
- Revise (no CMDPART): `Revise per the REVISE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}, IDS={ids}.\nInputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under .dev/orca-command-refactor/inventory/. Edit the spec {SPEC} in place; it is the only file you may change besides your output. Do not run the spec-panel. Write {out} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {ctx}`
- Audit: the p11 AUD brief, unchanged, for both AUD and AUD2.

`{ids}` is `", ".join(ids)`. Generalize `new_brief` only by passing `out`, `prior`, `base`, `rep` explicitly; the strings must not change.

### B4. Finding parsing and theme scoring (`$AB/score_themes.py`, pure functions)

```python
import re
THEMES = [("T3", r"AC-0\.4|\bP0\b|Phase 0"),
          ("T2", r"WC-4|contract (?:file )?(?:path|location)|--output"),
          ("T1", r"AC-1\.[12]|/sc:load|\bP1\b|Phase 1|command counts?|\b36\b")]   # re.I; first match wins
EXCL = {"FR", "AC", "SHA", "WC", "INV", "SPEC", "CMD", "P", "GC", "SA", "NFR", "D"}
ID_TOKEN = r"\b(?:R\d-)?[A-Z]{1,4}-?\d+\b"
CITE = (r"(?i)(?:\b(?:spec(?:\.md)?|S)\s*:\s*|\blines?\s+|\bL(?=\d))"
        r"(\d{1,3}(?:\s*[-–]\s*\d{1,3})?(?:\s*(?:,|and)\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)*)(?![\d.])")
```

- `parse_ids(raw)`: `None` or text matching `(?i)^\W*none\b` gives `[]`; cut `raw` at the first match of `\.\s|\.$|\(|;|\n`; delete `*`; return the `ID_TOKEN` matches in order, without duplicates, dropping a token whose leading letters (before the first digit or hyphen) are in `EXCL`.
- `find_section(text, fid) -> (heading, body)`: try three line prefixes in this order, each followed by `re.escape(fid) + r"(?![\w-])"`: heading `^\s*#{2,6}\s*(?:\*\*)?`, bold `^\s*(?:[-*]\s*)?\*\*`, table row `^\s*\|\s*(?:\*\*)?`. For a heading match with `k` leading `#`, the body is every following line up to the next heading with at most `k` `#` (so sub-headings such as `#### M1.a` stay inside `### M1`) or the next line matching `^\s*(?:[-*]\s*)?\*\*(?:R\d-)?[A-Z]{1,4}-?\d+\b`; for a bold match, up to the next line matching `^#{1,6} ` or that bold-id pattern; for a table row the body is empty. Not found: `(None, None)`.
- `tag(heading, body)`: apply `THEMES` to the heading; if none matches, to the first non-empty body line; else `"other"`.
- `cited(text) -> set[int]`: for each `CITE` match split group 1 on `\s*(?:,|and)\s*`; a part `a` or `a-b` adds `a..b` (if `b < a` or `b - a > 30`, only `a`); keep 1..400.
- `same_defect(f, g)`: same theme and Jaccard(cited) >= 0.5. `matches_audit(f, a)`: (same theme, not `other`, and at least one shared cited line) or (both `other` and Jaccard >= 0.5).
- `blocking_findings(path)`: verdict = last `verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)` (re.I); ids = `parse_ids(ids_from(path))` when FAIL else `[]`; for each id `{"id", "heading", "body", "theme", "cited"}`.

Required behaviour on the baseline (unit test it; reviews are `ws/.../review/round1.md`, audits `aud/ws/.../review/audit.md`; tuples are `(id, theme)`):

| run | first review (R1) | audit |
|---|---|---|
| a2-r1 | B-1 T3, B-2 T1 | F-1 T1, F-2 T2 |
| a2-r2 | B1 T1, B2 T2 | F-01 T2, F-02 T3 |
| a2-r3 | PASS (none) | REQ-1 T1, REQ-2 T1, ARCH-1 T2 |
| a2-r4 | B-1 T1 | F-1 T1, F-2 T2, F-3 other |
| a2-r5 | B-1 T2, B-2 T3 | F-1 T1 |
| a2-r6 | F-01 T1 | PASS (none) |
| a3-r1 | F1 T3, F2 T1 | B1 T1, B2 T2 |
| a3-r2 | R1-B1 T1, R1-B2 T2 | F-01 T3, F-02 T1 |
| a3-r3 | F1 T1, F2 T1, F3 T3 | F-1 T1, F-2 T2 |
| a3-r4 | F-01 T1 | A-01 other, A-02 T2 |
| a3-r5 | F-1 T1, F-2 T3, F-3 other | PASS (none) |
| a3-r6 | REQ-1 T2, REQ-2 T1, ARCH-1 T2 | F-01 T2 |

Every one of these findings must have a section and at least one cited line. The tags are a keyword proxy: after every analysis, print each tagged finding's heading next to its tag and eyeball it; correct a wrong tag by hand in `$AB/theme-overrides.json` (`{"<run>/<file>/<id>": "T2"}`), which `analyze` applies and lists in RESULTS.md.

Theme definitions (what the tags stand for, from the six arm-2 and six arm-3 audits):
- **T1, P1 scope / AC-1.1 vs `/sc:load` and command counts**: Phase 1 and AC-1.1/AC-1.2 require the `## Unattended mode` section, `--unattended` or a contract on every command of sections 3.1-3.2, while rows say `/sc:load` (and brainstorm, init-lite) get none, or the counts disagree (36 vs 12/14), or P1 ships the flag before P2-P4 convert the gates.
- **T2, WC-4 contract path vs file-valued `--output`**: WC-4 puts the contract at `<output-dir>/return-contract.yaml`, but rows give commands a file-valued `--output`, no output flag, or a generated directory, so the path or AC-1.2 step 4 cannot be satisfied.
- **T3, AC-0.4 / P0 check cannot pass**: AC-0.4 requires 7.2 step 3 (outcome matches the WC-4 contract status) in Phase 0, before any contract exists.
- **other**: anything else (seen: AC-2.2 for non-blocking P2 gates, AC-2.3 for cli-portify, AC-C5 grep).

### B5. Design-specific steps

`STEPS = ["R1", "V1", "R2", "V2", "R3", "G", "GV", "GR", "AUD", "AUD2"]`. R1..R3 and V1, V2 are exactly the arm-3 steps (no verify step in this design: one factor only).

**Gate sandbox** `runs/<run>/g/`, created when G is prepped: overlay copy (README, inventory) with the spec replaced by the current main spec, an empty `review/`, `home/.claude/rules/prompts/` with the product rules file (`PRODUCT_REF`), and `command.md` from `PRODUCT_REF`. It holds no report, no history and nothing of the loop. **Gate prompt** `PROMPT-G.md` = `WRAP.format(sb=runs/<run>/g, wsdir="ws", cmdpart=CMDPART, brief=...)` with brief:

`Run /sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture . Review per the GATE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate=.dev/orca-command-refactor/specs/orca-worker-contract-spec.md.\nWrite the full report to .dev/orca-command-refactor/review/gate.md. Do not edit anything else. {ctx}`

Output `g/ws/.dev/orca-command-refactor/review/gate.md`; at ingest copy it to the main `ws/{R}/gate.md` and record verdict, ids, themes, `review_header`.

**Stall check** (deterministic, pre-registered; the harness proxy for "the same stated text and the same wrong outcome"): `Gs = blocking_findings(gate.md)`; `E` = the blocking findings of every scoped-loop review report of the run (`round1.md`, `round2.md`, `round3.md` where present). Stalled if and only if every `g` in `Gs` has some `e` in `E` with `same_defect(g, e)` (same theme and Jaccard of cited lines >= 0.5). Record `state["stall"] = {"auto": bool, "pairs": [[g_id, e_file, e_id], ...]}`. The run follows the automatic result; a person eyeballs every stall decision afterwards and RESULTS.md lists any disagreement (without changing the run).

**GV** (gate revise): snapshot the main spec to `ws/{H}/spec-g.md` first; brief = the revise brief (B3) with `rep = .dev/orca-command-refactor/review/gate.md`, `out = .dev/orca-command-refactor/review/revise-gate.md`, `IDS` = the gate's blocking ids. Sandbox = the run directory, as for V1.

**GR** (gate re-review): brief = the re-review brief (B3) with `prior = .dev/orca-command-refactor/review/gate.md`, `base = .dev/orca-command-refactor/specs/history/spec-g.md`, `out = .dev/orca-command-refactor/review/gate-round2.md`; CMDPART; sandbox = the run directory. Expected header `review: 2 of 3` (record it; a different header is noted, not corrected).

### B6. State machine (`advance.py`; restructure the p11 script into `main(argv=None)` so tests can call it)

| After | Condition | Next |
|---|---|---|
| start | | R1 |
| R1, R2 | FAIL and ids parsed | V1 / V2 (snapshot first, as p11) |
| R1, R2, R3 | verdict PASS | G |
| R3 | FAIL | `loop_end = ESCALATED` (scoped cap; no gate); AUD and AUD2 |
| any review incl. G, GR | FAIL with no ids, INCOMPLETE, NONE | MANUAL (B2 items 4, 8) |
| V1 / V2 | output present | R2 / R3 |
| G | PASS | `loop_end = GATE-PASS`; AUD and AUD2 |
| G | FAIL, stall check true | `loop_end = STALLED`; AUD and AUD2 |
| G | FAIL, stall check false | GV |
| GV | output present | GR |
| GR | PASS | `loop_end = GATE-LOOP-PASS`; AUD and AUD2 |
| GR | FAIL | `loop_end = GATE-LOOP-ESCALATED`; AUD and AUD2 |
| AUD and AUD2 | both ingested | run complete |

Assert in `advance.py` that no run ever executes more than 5 review steps (R*, G, GR) or more than 3 revise steps (V*, GV).

## Part C. Offline tests of the tooling (`$AB/tests/test_ab.py`)

Import `harness`, `advance` and `score_themes` from `$AB` (insert `$AB` in `sys.path`); point `harness.RUNS` at `tmp_path` with `monkeypatch`; simulate finished workers by writing the output file and setting its mtime 10 minutes back with `os.utime`. Real Stage 2 reports serve as fake outputs. Required tests:

1. Scoring: the B4 table for all 12 runs (ids, themes, a section and at least one cited line for each).
2. `parse_ids` on the six a3 R1 reports (`['F1','F2']`, `['R1-B1','R1-B2']`, `['F1','F2','F3']`, `['F-01']`, `['F-1','F-2','F-3']`, `['REQ-1','REQ-2','ARCH-1']`), on `"none (F1, F2 and F3 are resolved; no new blocking finding)"` (`[]`) and on `"NEW-1. Nothing else. REQ-1, REQ-2 and ARCH-1 are resolved"` (`['NEW-1']`).
3. `basetokens` reproduces the section 2 loop totals within 1% (skip if no transcripts are readable).
4. `build` in tmp: spec sha; `command.md` sha equals the sha of `git_show(PRODUCT_REF, spec-panel)` and differs from `AUD_CMD_SHA`; the rules file contains `### GATE prompt`. The audit sandboxes still get the frozen command (`AUD_CMD_SHA`) and frozen rules.
5. Prompt identity: with the tmp sandbox path replaced by `$SP/p11/runs/a3-r1`, `PROMPT-R1.md`, `PROMPT-V1.md` (IDS `F1, F2`), `PROMPT-R2.md`, `PROMPT-AUD.md` equal the a3-r1 files byte-for-byte; `PROMPT-R3.md` equals `a3-r6/PROMPT-R3.md` after replacing the path by `$SP/p11/runs/a3-r6`; `PROMPT-AUD2.md` equals `PROMPT-AUD.md` after replacing `/aud2` by `/aud`.
6. Gate sandbox: contains the overlay README and inventory, the current spec, product command and rules, and no file under `review/`; `PROMPT-G.md` names the GATE prompt and `gate.md`.
7. Path R1 FAIL (fake a3-r3 round1.md) → V1 → R2 PASS (fake a3-r3 round2.md) → G printed (not audits).
8. G PASS (fake a3-r5 audit.md copied as gate.md) → `GATE-PASS`, AUD and AUD2 printed together.
9. Stall: G FAIL whose findings are those of the run's own R1 (fake: copy a3-r3 round1.md as gate.md) → `STALLED`; G FAIL with new findings (fake a3-r1 audit.md, run's R1 = a3-r3 round1.md) → not stalled, GV printed with `IDS=B1, B2`, `spec-g.md` exists; record which pairs matched.
10. GR PASS → `GATE-LOOP-PASS`; GR FAIL → `GATE-LOOP-ESCALATED`; R3 FAIL → `ESCALATED` with no G; R1 PASS (fake a2-r3 round1.md) → G.
11. Ceiling assertion: a forged state with 5 review steps refuses a sixth.
12. Concurrency (6 LAUNCH lines max; `--dry-run` marks nothing) and `tokens` on a synthetic transcript (Sonnet sum, warning on another model).
13. Convention and strata: `analyze` on synthetic records computes `R_LOOP = LOOP / 100,424` and `R_B = (LOOP + AUD) / 169,468`; a case where the `R_B` limit holds and the `R_LOOP` limit fails is decided by `R_LOOP`; a transcript that logs one message on two lines counts it once; `build --stratum haiku` writes `stratum: haiku` into 4 runs whose loop LAUNCH lines say `model=haiku` and whose AUD/AUD2 lines say `model=sonnet`; Haiku runs never enter the Sonnet `BLK_T`; `build --extend` is refused unless the Sonnet outcome is INCONCLUSIVE and creates r7..r9 only once.

Check test 9's expectation against the real files before relying on it: print `same_defect` pairs for a3-r1 audit vs a3-r3 round1 and adjust the fake (not the rule) if the proxy happens to match.

```bash
cd $AB && uv run --no-project --with pytest pytest -q tests        # all pass
```

## Part D. Execution mode

Sonnet workers in this environment normally have no Agent tool, so you cannot launch experiment workers yourself. Check your tool list once: if it contains an Agent (or Task) tool that can start a subagent with a chosen model, use Mode B; otherwise Mode A.

**Launch protocol (both modes).** For every line `LAUNCH <absolute path> model=<sonnet|haiku>` that `advance.py` prints, start one subagent with that model (AUD/AUD2 lines always say `model=sonnet`) and exactly this message: `Read <absolute path> and follow it exactly. Touch nothing outside the sandbox directory it names.` Launch all printed prompts at once (never more than 6 running for this experiment), then call `advance.py` again after at least one has finished. `advance.py` prints `RUNNING n`, `MANUAL <run> <step> <reason>` (needs a person: see B2 items 4 and 8), `WARN ...`, or `ALL DONE`.

```bash
uv run --no-project python $AB/harness.py build            # once; creates b3-r1..r6
uv run --no-project python $AB/harness.py build --stratum haiku   # once; creates b3h-r1..r4 (Haiku stratum, 3b)
uv run --no-project python $AB/harness.py build --extend           # only after a Sonnet n=6 INCONCLUSIVE (3c); creates b3-r7..r9
uv run --no-project python $AB/advance.py --dry-run         # writes the first prompts, marks nothing
uv run --no-project python $AB/advance.py                   # marks printed prompts launched: only when you launch them
uv run --no-project python $AB/harness.py status
```

**Mode A (expected).** Do Part A (including the A4 commit and push, which gives `PRODUCT_REF`), then Parts B and C. Run `build`, `build --stratum haiku` and `advance.py --dry-run` (prompt files exist for the first wave, nothing is marked launched) and diff the first prompts against the baseline as in Part C. Do not run `advance.py` without `--dry-run`. Then STOP and send the READY report (section 9). The coordinator then runs the loop with the launch protocol until `ALL DONE`, then runs Part E (or hands it back to you).

**Mode B (Agent tool available).** Do Parts A-C, then run the loop yourself with the launch protocol, at most 6 concurrent workers, until `ALL DONE`; then Part E and write `$AB/RESULTS.md`. Send the READY report before the first launch (as a progress message, if you can) and the results report at the end.

If a worker returns without its output file: `harness.py unlaunch RUN STEP`, relaunch once; a second failure marks the run `lost` (B2 item 7).

## Part E. Measurement

`harness.py analyze` reads every `state.json` and report, applies `$AB/theme-overrides.json`, and writes `$AB/metrics.json` plus `$AB/RESULTS-tables.md` (the tables below, filled). Common metrics, identical in definition to Stage 2:

| Metric | Definition |
|---|---|
| Loop PASS within cap | final PASS: `loop_end` is GATE-PASS or GATE-LOOP-PASS; also report the scoped loop PASS (any review PASS before the gate) for comparison with the baseline 6/6 |
| Reviews | number of review steps the run executed (R1, R2, R3, G and GR; report scoped and gate reviews separately) |
| Spec growth % | (final spec bytes - 57,763) / 57,763; final = the spec the audits read |
| `LOOP` (A, decides) | sum of deduplicated `output_tokens` (B2 item 5) over every loop step, excluding AUD and AUD2; baseline `A_BASE` 100,424; `R_LOOP = LOOP_T / 100,424` |
| `TOK` (B, reported only) | `LOOP` plus AUD (not AUD2); baseline `B_BASE` 169,468; `R_B = TOK_T / 169,468`, printed beside `R_LOOP`, never decides |
| Stratum | every `state.json`, log record and metrics row carries `stratum: "sonnet"` or `"haiku"`; every table is per stratum and Haiku is never pooled into a Sonnet number |
| Audit tokens | per audit, reported separately |
| Audit verdict | last `verdict:` line of each audit report, for AUD and AUD2 |
| Blocking per audit | `len(blocking_findings(audit))`; `BLK_T` = mean over all completed test audits (12 when all runs complete) |
| Audit FAIL rate | audits with verdict FAIL / audits |
| Theme rate | audits with at least one T1, T2 or T3 blocker / audits; plus counts per theme |

Design-specific metrics (in `RESULTS-tables.md`):

- **Gate verdicts**: per run, loop end before the gate (PASS at R1/R2/R3, or ESCALATED), G verdict, G blocking count and themes, GR verdict, final `loop_end`.
- **Gate-triggered loops**: number of runs with GV/GR; mean added reviews and fix cycles; maximum reviews per run (must be <= 5).
- **Stall events**: automatic count, eyeball count, disagreements.
- **Total reviews**: scoped reviews + gate reviews per run; compare the scoped part with the baseline 2.17.
- **Gate vs audit (descriptive only)**: per run, themes of G findings vs themes of AUD/AUD2 findings. Never use the gate verdict as an outcome (circularity).
- **Cost split**: TOK and LOOP split into scoped loop, G, GV + GR.

## Part F. Validity controls (built in; do not skip)

- **Same instrument.** The audit is frozen: command from `BASE_REF`, rules from `$SP/p11/rules.md`, the p11 brief, the same overlay. `harness.py` asserts the three hashes at every audit prep. Every test-arm final spec gets TWO independent audits (`AUD` in `aud/`, `AUD2` in `aud2/`, fresh sandboxes, prepared and launched together). Report both, and pool them (12 audits) for the decision.
- **Baseline audit noise.** The baseline has one audit per spec. The coordinator produces a second audit of the six baseline final specs under `$SP/p12/baseline-audit2/` (all six reports present as of 2026-11-10): one sandbox per run, report at `$SP/p12/baseline-audit2/a3-rK/ws/.dev/orca-command-refactor/review/audit.md`, and `results.json` written by `$SP/p12/collect_baseline_audit2.py` with entries `{"verdict": "FAIL", "blocking_ids": "<raw ids_from text>", "n_blocking": N}` or `{"status": "missing"}`. Do not trust `n_blocking` (it counts tokens in raw text): score each existing report yourself with `blocking_findings()` and tag themes as for your own audits. Use all baseline second audits that exist for `B_BLK`, `B_AUDFAIL` and `B_THEME` (pooled with audit 1); if any of the six is missing or `INCOMPLETE`, use what exists and say so. If none exists when you analyze, label every comparison in RESULTS.md PROVISIONAL.
- **Same workers and prompts.** Same overlay and spec hash, same `WRAP`, same pointer briefs, same model (`sonnet` in the decision stratum), same stop rules, same REVISE prompt and in-place edit. Part C diffs prove the reused prompts are byte-identical apart from sandbox paths.
- **Replicate decision is pre-registered.** Sonnet n = 6, plus the one-time n = 9 extension of section 3c only when the n = 6 outcome is INCONCLUSIVE; Haiku n = 4 (section 3b), never extended. Lost runs are not replaced unless the coordinator asks; fewer than 5 completed Sonnet runs (8 at n = 9) makes the result INCONCLUSIVE.
- **Replica agreement.** Compute the primary metric once from audit 1 only and once from audit 2 only. If the two replicas give different decision outcomes, the overall outcome is INCONCLUSIVE whatever the pooled value says.
- **Drift.** The baseline workers ran on 2026-11-10 between 00:38 and 02:05 UTC (transcript timestamps). Model or service drift since then is a limitation; state it. Only if the coordinator asks, add 2 fresh baseline replicates (`base-r1`, `base-r2`: same harness, frozen command and rules for every step, baseline stop rules, one audit each; about 0.34M output tokens: 2 x (100,424 + 69,044), deduplicated). Do not run them on your own initiative.
- **Theme tags are a proxy.** Eyeball every tag (B4); report overrides.
- **Circularity.** Restate in RESULTS.md that the gate verdict is not an outcome; only AUD and AUD2 decide.

## Part G. Analysis and decision

Fill this table in RESULTS.md (mark PROVISIONAL if baseline-audit2 is absent):

| Metric | Baseline a3 (n=6) | Test b3 (n=6) | Delta | Rule | Met? |
|---|---|---|---|---|---|
| Scoped loop PASS within 3 reviews | 6/6 | | | report | |
| Final loop PASS (GATE-PASS + GATE-LOOP-PASS) | 6/6 (no gate) | | | DROP-2: >= 4/6 | |
| Gate verdict PASS / gate loops / stalls | n/a | | | report only (never outcome) | |
| Mean total reviews (max) | 2.17 (3) | | | ceiling 5 | |
| Mean growth | +1.41% | | | report | |
| Mean LOOP incl. gate (A) / `R_LOOP` | 100,424 / 1.00 | | | DROP-3: `R_LOOP` <= 1.8 | |
| Mean TOK (B = LOOP + AUD) / `R_B` | 169,468 / 1.00 | | | report only, never decides | |
| Audits PASS / audit FAIL rate | 1/6 / 5/6 | x/12 | | ADOPT: FAIL <= 8/12 | |
| `BLK_T` pooled / audit 1 only / audit 2 only | 1.50 | | | ADOPT <= 1.00 | |
| Theme rate (T1/T2/T3 per audit) and per theme | 5/6 (T1 3, T2 4, T3 1, other 1) | | | DROP-1: < 10/12 | |

Apply section 3 in this order: DROP-1, DROP-2, DROP-3, ADOPT, else INCONCLUSIVE. Then run the replica-agreement check, then the Haiku condition (3b), then, if the Sonnet outcome is INCONCLUSIVE, the one-time extension (3c). Fill a separate Haiku table with these columns: Haiku baseline (n=6, from `results.json`), Haiku test `b3h` (n=4), `H_BLK`, `BLK_TH`, `HR`, `1 - HR`, final loop PASS, gate loops, stalls, growth, harness failures and `R_LOOP_H`. Never pool it with the Sonnet table. If DROP-1 fires, add the report's pointer: the gate reviewer misses the same themes, which points to theme sweeps (report 3.4), not to more gate loops.

## 7. Cost and wave schedule

Estimates use the deduplicated baseline per-step means of section 2: R1 50,577, V1 14,255, R2 29,993, audit 69,044, and baseline loop `A_BASE` 100,424.

- **Sonnet stratum, per run (loop only):** the scoped loop is unchanged at about 100,424. G costs about 69,044, because a whole-document first review costs about as much as an audit, 69% of a baseline loop; the floor is the R1 mean of 50,577. The gate loop (GV + GR, about 44,248) runs in about 5/6 of runs, because 5/6 baseline audits failed; that averages about 36,900. LOOP is about 206,300, so **predicted `R_LOOP` is about 2.05** (range 1.72-2.13: G 50.6-69.0k, gate loop in 1/2 to 6/6 of runs). `R_B` = (206,300 + 69,044) / 169,468, about 1.62. The report's "+~20%" undercounts the gate. Two Sonnet audits add 138,088.
- **Sonnet n=6:** loop-only about **1.24M** output tokens; with the 12 audits about 2.07M. Workers: typical 8 per run (R1, V1, R2, G, GV, GR, AUD, AUD2), **about 48 in total**, maximum 10 per run (60).
- **Haiku stratum n=4 (3b):** no Haiku per-step data exists yet (the Haiku baseline was still running on 2026-11-10). Plan with the Sonnet per-step figures, and use 1.5x as a ceiling for extra rounds. That gives a Haiku loop of about **0.83M** (ceiling 1.24M) plus 8 Sonnet audits of 0.55M, so about 1.38M in total (ceiling 1.79M). Workers: about 32 (maximum 40).
- **Conditional D4 extension (3c), only after a Sonnet n=6 INCONCLUSIVE:** 3 Sonnet runs. Loop-only about **0.62M**, about 1.03M with the 6 audits; about 24 workers (maximum 30), with its own worker allocation in the waves below.
- Waves at no more than 6 concurrent, both strata together (Sonnet runs first). W1: R1 x6. W2: V1. W3: R2. W4: G. W5: GV. W6: GR. W7-W8: the 12 audits; runs with an extra scoped round lag one or two waves. This takes about 8-10 waves, about 3 hours. The Haiku runs `b3h-r1..r4` follow in the free slots, about 6-7 waves and 2-2.5 hours. Then analyze the Sonnet stratum. Only if it is INCONCLUSIVE, the conditional waves for `b3-r7..r9` follow (about 5 waves, about 2 hours).

## 8. Self-check before you start

Run these; every line must print the expected value. If one fails, stop and report it; do not improvise a substitute.

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export AB=$SP/p12/ab3
O=$SP/exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay
sha256sum $O/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md   # d3cdbe573e57...c31425200d
ls $O/.dev/orca-command-refactor/inventory/                                   # commands-a.md commands-b.md orca-capabilities.md
sha256sum $SP/p11/rules.md                                                    # 3eb772f9...5ddfb8
git -C /home/user/IronClaude show 69ac8b3335564fb5551980e984c5d9b763039cc1:src/superclaude/commands/spec-panel.md | sha256sum   # e62e70b9...497494
git -C /home/user/IronClaude show 69ac8b3335564fb5551980e984c5d9b763039cc1:src/superclaude/rules/prompts/document_review_loop_prompts.md | sha256sum   # 3eb772f9...5ddfb8
for r in 1 2 3 4 5 6; do test -f $SP/p11/runs/a3-r$r/state.json && test -f $SP/p11/runs/a3-r$r/aud/ws/.dev/orca-command-refactor/review/audit.md && echo a3-r$r ok; done
ls $SP/p11/runs/a3-r1/PROMPT-R1.md $SP/p11/runs/a3-r1/PROMPT-V1.md $SP/p11/runs/a3-r1/PROMPT-R2.md $SP/p11/runs/a3-r1/PROMPT-AUD.md $SP/p11/runs/a3-r6/PROMPT-R3.md
ls /tmp/claude-0/-home-user-IronClaude/*/tasks/*.output | wc -l            # > 0 (baseline transcripts for basetokens)
test ! -e $AB && echo "AB free"                                              # your directory must not exist yet
ls $SP/p12/baseline-audit2/a3-r*/ws/.dev/orca-command-refactor/review/audit.md 2>/dev/null || echo "no baseline second audit yet (PROVISIONAL unless they appear before analysis)"
ls $SP/p14/DECISIONS-ADDENDUM.md                                             # binding owner decisions
test -f $SP/p14/haiku-baseline/results.json && echo "haiku baseline ready" || echo "haiku baseline not yet produced (Haiku comparison pending; run the Sonnet stratum first)"
uv --version
```

## 9. Report formats

**READY report** (Mode A: your final message; Mode B: before the first launch):

```text
READY ab3 (final whole-document gate with a bounded gate loop)
branch: 346Claude-ab3-final-gate @ <full sha>   pushed: yes|no (<error>)   PR: none (by instruction)
product files changed: <list>   tests added: <list>   existing tests changed: none|<list + why>
checks: make lint <ok>; make verify-sync <ok>; pytest tests/skills tests/unit <N passed>; spec-panel.md <lines> lines
harness: $AB/harness.py, $AB/advance.py, $AB/score_themes.py; offline tests: <N passed>
prompt diffs vs baseline: <list, all empty>
basetokens: loop mean <n> (expected 100,424), audit mean <n> (expected 69,044), deduplicated by message id
decision file: $AB/decision.json; D2 (loop-only R_LOOP, R_B reported) in <files>; D3 (stratum tag, Haiku loop model, Sonnet-only AUD) in <files>; D4 (extension) in <files>
first wave written (dry run): <list of PROMPT paths>
how to launch: run `uv run --no-project python $AB/advance.py`, launch each LAUNCH line as a subagent of the model it names with
  "Read <path> and follow it exactly. Touch nothing outside the sandbox directory it names.", max 6 at once, repeat until ALL DONE;
  then `uv run --no-project python $AB/harness.py tokens && uv run --no-project python $AB/harness.py analyze`.
expected: <workers typical/max>, ~<tokens> output tokens, <waves>
open issues: <list or none>
```

**Results report**: `$AB/RESULTS.md` with, in order: (1) one-line outcome ADOPT / ADOPT (Haiku robustness pending) / DROP / INCONCLUSIVE (+ PROVISIONAL if baseline-audit2 is absent; + `n=9` if the 3c extension ran) and the rule that decided it, with `R_LOOP` and `R_B` side by side; (2) the analysis table (Part G) with baseline and test columns; (3) per-run table (loop end, reviews, growth, loop tokens, audit 1 and audit 2 verdicts with blocking ids and themes); (4) the design-specific tables (Part E) and the separate Haiku stratum table (3b), never pooled; (5) theme overrides and eyeball notes; (6) deviations from this plan, lost runs, manual interventions; (7) limitations (n=6, single document, drift, keyword proxy). The final chat message is the outcome line, the analysis table and the path of RESULTS.md.
