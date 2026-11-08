# Base Selection

Method note (read first): the variants are two short option write-ups, not full documents, so the five automatic metrics have little signal. The values below are the orchestrator's judgments grounded in the files read, not outputs of a script; they are not deterministic. The qualitative layer was scored in one pass. The reverse-order second pass the protocol asks for was not run as a separate evaluation at depth quick. As a substitute, the headline verdict was checked against facts that do not depend on order (the working-tree text, the pinned test and the spec lines), and both advocates, who saw the variants in opposite orders, reached the same winner.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (A) | Variant 2 (B/B2) | Basis |
|--------|--------|---------------|------------------|-------|
| Requirement coverage (4 judging criteria + SA-1/SA-4, 2.1, WC-4, WC-9, WC-11 named) | 0.30 | 0.75 | 0.75 | Both name the changed lines and the spec check; neither discusses WC-9 or WC-11 |
| Internal consistency | 0.25 | 1.00 | 0.80 | Variant 2 itself admits B2 contradicts neighbouring sentences |
| Specificity ratio | 0.15 | 0.90 | 0.85 | A cites exact lines and evidence commands; B cites lines but no evidence command |
| Dependency completeness | 0.15 | 1.00 | 1.00 | All internal references resolve |
| Section coverage | 0.15 | 1.00 | 1.00 | Same structure |
| **quant_score** | | **0.910** | **0.853** | |

## Qualitative Scoring (50% weight): additive binary rubric (orchestrator-scored, evidence in this file and the debate transcript)

| Dimension | Variant 1 | Variant 2 | Evidence (claim, evidence, verdict) |
|-----------|-----------|-----------|-------------------------------------|
| Completeness (5) | 4 | 3 | A names tests, spec check, evidence commands; B omits the test impact and `ac-c5.txt` rewrite, which the Variant 2 advocate had to concede |
| Correctness (5) | 5 | 3 | A's end state matches workflow.md:72,75 and reflect.md:101,263; B keeps `.dev/reflect/` (false under `--output`) and B2 keeps "without `--unattended`" |
| Structure (5) | 4 | 4 | Both use claim, strength, weakness, judging criteria |
| Clarity (5) | 4 | 3 | A's end state is unambiguous; B's reader meets stale plus correction and has no precedence rule (WORKER-CONTRACT.md grep: no precedence wording) |
| Risk coverage (5) | 3 | 3 | A names its hand-made exemption; B names the contradiction risk; neither gives probabilities or a rollback |
| Invariant and edge-case coverage (5) | 2 | 1 | A covers the standalone-run guard (workflow.md:70) implicitly; B covers none explicitly |
| **Total (of 30)** | **22** | **17** | |
| **qual_score** | **0.733** | **0.567** | |

Edge Case Floor Check: Variant 1 scores 2/5, Variant 2 scores 1/5; both meet the 1/5 floor and are eligible.

## Position-Bias Mitigation
Dual-pass rubric not run separately (see method note). Substitute check: the three facts that decide the verdict were re-read from disk by the orchestrator after the debate (spec line 152, absence of a precedence rule in WORKER-CONTRACT.md, `.dev/reflect` occurrences). Disagreements found: 0. Verdicts changed: 0.

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | Combined |
|---------|--------------|-------------|----------|
| Variant 1 (A) | 0.455 | 0.367 | **0.822** |
| Variant 2 (B/B2) | 0.427 | 0.283 | **0.710** |

Margin: 0.112 (11.2 points), above the 5% tiebreaker window. Tiebreaker applied: No.

## Selected Base: Variant 1 (option A, original)

- Selection rationale: it is the only variant that leaves every sentence of `## Unattended mode` true when a worker runs the command under `--unattended`; it matches the working tree (`git diff HEAD -U0` shows 2 added and 2 deleted lines), the pinned test (`test_worker_contract.py:1679-1712`) and `ac-c5.txt:18`; and spec line 222 names the workflow section edit as a P2 change.
- Strengths to preserve: in-place replacement of lines 72 and 75; the named exemption of exactly two deleted lines for workflow.md (and one for brainstorm.md); the evidence commands.
- Strengths to incorporate from Variant 2: (1) B2's concern that a hand-made exemption is a precedent: record why this one is bounded (exactly two lines, both false under `--unattended`, section inert in standalone runs); (2) Variant 2's note that the exemption count is enforced only by the annotation: keep the "exactly 2 deleted lines" wording in `ac-c5.txt` so a third deleted line fails.
