# Base Selection Report

## Metadata
- Decision: D4 (`SPEC:345-348`). V1 = option (a), V2 = option (b), V3 = option (c). Every score is for the original variant text (`variant-{1,2,3}-original.md`). Refinements made only during the debate, such as (c′), are not credited to any variant's score; they appear under "Strengths to incorporate" and in the refactoring plan.
- Inputs:
  - `diff-analysis.md`
  - `debate-transcript.md` (its scoring matrix)
  - `scoring/qual-pass-1.md` (input order V1, V2, V3)
  - `scoring/qual-pass-2.md` (reverse order V3, V2, V1)
  - `invariant-probe.md`
- Protocol: `~/.claude/skills/sc-adversarial-protocol/SKILL.md`, sections Quantitative Scoring Layer, Qualitative Scoring Layer (6 dimensions, 30 criteria), Position-Bias Mitigation, and Combined Scoring & Tiebreaker; also `refs/scoring-protocol.md`.
- Produced by debate-orchestrator, 2026-11-02T16:25Z.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (option a) | V2 (option b) | V3 (option c) |
|---|---|---|---|---|
| requirement_coverage (RC) | 0.30 | 0.800 (16/20 topics) | 0.900 (18/20) | 0.900 (18/20) |
| internal_consistency (IC) | 0.25 | 0.950 (1 contradiction / 20 claims) | 1.000 (0 / 16) | 0.9375 (1 / 16) |
| specificity_ratio (SR) | 0.15 | 1.000 (12 concrete / (12 + 0 vague)) | 1.000 (9 / (9 + 0)) | 1.000 (11 / (11 + 0)) |
| dependency_completeness (DC) | 0.15 | 1.000 (13/13 key references resolve) | 1.000 (9/9) | 1.000 (10/10) |
| section_coverage (SC) | 0.15 | 1.000 (5/5 H2) | 1.000 (5/5) | 1.000 (5/5) |
| **quant_score** | | **0.9275** | **0.9700** | **0.9544** |

Formula: quant = 0.30·RC + 0.25·IC + 0.15·SR + 0.15·DC + 0.15·SC.

- V1 = 0.2400 + 0.2375 + 0.15 + 0.15 + 0.15 = 0.9275
- V2 = 0.2700 + 0.2500 + 0.45 = 0.9700
- V3 = 0.2700 + 0.234375 + 0.45 = 0.954375

### Computation details

**Method.** One script run over the three variant files produced the counts, so they can be reproduced. The only judgment calls are the RC rule and the list of contradictions, and both are stated below.

- Body text is every non-blank line that is neither a heading nor the `Citation key` line.
- The body is split into sentences at sentence ends, keeping only sentences of 3 or more words.
- Sentence counts: V1 20, V2 16, V3 16.

**RC (requirement coverage).** D4 has no requirement IDs (FR-, NFR- or R-), so the protocol's fallback applies: topic matching.

- There are 20 topics: the five the decision asks for (safety, reliability, day-to-day use, implementation cost and the worker-commit question), plus the 15 content topics C-001 to C-015 in `diff-analysis.md`.
- A topic counts as covered when the variant has a section or a sentence on it.
- For the C-NNN topics, this rule is applied mechanically to the variant's cell in `diff-analysis.md`. The topic is not covered when that cell starts with "Not discussed", "Not addressed", "Silent", "Does not", "No scope rule" or "n/a".

| Topic | V1 | V2 | V3 | Basis |
|---|---|---|---|---|
| Safety / Reliability / day to day / cost (4) | 4 | 4 | 4 | All four H2 sections in each variant (V1:13-23, V2:12-22, V3:12-22) |
| Worker-commit question | 1 | 1 | 1 | V1:3, V2:3, V3:5 |
| C-001 provenance across sessions | 1 | 1 | 1 | `diff-analysis.md:31` |
| C-002 reversibility | 1 | 1 | 1 | `:32` |
| C-003 retry-ladder HEAD guard | 0 ("Silent") | 1 | 1 | `:33` |
| C-004 post-release real-target steps | 1 | 1 | 1 | `:34` |
| C-005 auggie-review posting | 1 | 1 | 1 | `:35` |
| C-006 task's EXEMPT commit/push | 0 | 0 | 0 | `:36`, "Not discussed" for all three |
| C-007 consistency with D2 | 1 | 1 | 0 ("Does not cite D2") | `:37` |
| C-008 testability | 1 | 1 | 1 | `:38` |
| C-009 implementation cost | 1 | 1 | 1 | `:39` |
| C-010 #326 alignment | 1 | 1 | 1 | `:40` |
| C-011 PR path | 0 ("Not addressed") | 1 | 1 | `:41` |
| C-012 commit scope and branch | 0 ("No scope rule") | 0 ("n/a") | 1 | `:42` |
| C-013 cost of changing later | 1 | 1 | 1 | `:43` |
| C-014 day-to-day work | 1 | 1 | 1 | `:44` |
| C-015 basis of today's ban | 1 | 1 | 1 | `:45` |
| **Covered / 20** | **16** | **18** | **18** | |

**IC (internal consistency).** A scorable claim is a body sentence with no vague indicator. None of the three variants has one, so claims equal sentences. The internal contradictions come from the diff analysis, and both qualitative passes confirm them (Correctness criterion 4):

- V1: X-003. It cites `PRL:351` both as support (V1:8) and as the gap (V1:14). 1 / 20.
- V2: none; `diff-analysis.md:47-57` lists no contradiction inside V2. 0 / 16.
- V3: X-006. "No command needs a new outward flag" (V3:23) conflicts with its own commit window inside `/sc:implement` (V3:5). 1 / 16.

Contradictions between variants (X-001, X-002, X-004, X-005, X-007) are not internal, so they are not counted.

**SR (specificity ratio).**

- A sentence is concrete when it contains a number or a code-formatted named entity: a path, command, flag or `KEY:N` citation.
- A sentence is vague when it contains one of the protocol's vague indicators: "appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practices" or "industry standard".
- Counts (concrete, vague, neither): V1 12, 0, 8; V2 9, 0, 7; V3 11, 0, 5.
- The table uses the SKILL formula, SR = concrete / (concrete + vague). No variant has a vague sentence, so all three score 1.000.
- Sensitivity check: `refs/scoring-protocol.md` defines SR as concrete / all substantive statements. That gives SR of V1 0.600, V2 0.5625 and V3 0.6875. Under it, quant scores become V1 0.8675, V2 0.9044 and V3 0.9075, and combined scores become V1 0.7504, V2 0.7522 and V3 0.7871. The selected base (V3), the tiebreaker trigger and the tiebreaker outcome do not change.

**DC (dependency completeness).** Internal references are `KEY:N` citations. Each must resolve to a key declared in the variant's own Citation key line. Full-path citations, and references to other options or to the spec, are external and are excluded.

- V1: 13 references, all resolve (keys used: SPEC, PRL, EVAL). The declared `HWW` key is never used (S-006); an unused key is not an unresolved reference.
- V2: 9 of 9 resolve (SPEC, PRL, PRS, HWW).
- V3: 10 of 10 resolve (SPEC, PRL, HWW, EVAL).

**SC (section coverage).** H2 counts are V1 5, V2 5 and V3 5. The maximum is 5, so all three score 1.000.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

How to read these tables:

- Each verdict is the final one, after position-bias resolution.
- "P1" is `scoring/qual-pass-1.md` and "P2" is `scoring/qual-pass-2.md`. "Both" means the two passes gave the same verdict, and the evidence is condensed from them.
- "Re-eval" marks a criterion where the passes disagreed. The orchestrator's re-evaluation, which is final, is in the Position-Bias Mitigation section.
- Each evidence cell is a condensed Claim-Evidence-Verdict (CEV) entry.

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | Both: Safety, Reliability, day to day and cost sections (V1:13-24); commit answer at V1:3 | MET | Both: V2:12-23; commit answer "none" (V2:3) | MET | Both: V3:12-23; dedicated commit-rule paragraph (V3:5) |
| Edge cases / failures | MET | Both: worker "cannot check" the quote; published PR "visible at once" (V1:14-15) | NOT MET | Both: no failure scenario of (b) itself (V2:7-23 searched) | MET | Both: never the default branch; the retry-ladder window (V3:5) |
| Dependencies / prerequisites | MET | Both: quote plus explicit flag (V1:3); flags honoured under `--unattended` (V1:24) | MET | Both: WC-9 and AC-4.2 baseline (V2:9); pr-submit (V2:10) | MET | Both: quoted instruction, own branch, window (V3:3-5) |
| Success / completion criteria | MET | Both: AC-4.2 plus a live check per action (V1:18) | MET | Both: AC-4.2 (V2:9, `SPEC:275`) | MET | Both: AC-4.2 plus the `origin` check; SHAs in `artifacts` (V3:5, V3:17) |
| Out of scope stated | NOT MET | Both: none found (V1:1-24) | NOT MET | Both: none found (V2:1-23) | NOT MET | Both: the never-list is policy, not scope (V3:1-23) |
| **Subtotal** | **4/5** | | **3/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| No factual errors | NOT MET | Both: `PRL:351` overstated as support (V1:8; `diff-analysis.md:105`); `CLAUDE.md:68` overstated (V1:14; `:102`); conceded at r1-variant-1.md:38 | NOT MET | Both: `CLAUDE.md:68` generalized (V2:8); `PRS:43-49` overread (V2:10); "Zero beyond today's spec" false (V2:23); all conceded | NOT MET | Both: "No command needs a new outward flag" (V3:23) and "local and undoable" (V3:13), both conceded (r1-variant-3.md:37-38) |
| Feasible under stated constraints | NOT MET | Both: there is no implement commit step to switch on (A-005); shared-worktree commits (A-004); conceded (r1-variant-1.md:43-44) | MET | Both: needs no new command feature; X-006 and C-003 won by V2 in the scoring matrix | NOT MET | Both: the window inside implement needs a missing step (`MW:63,67`); "own feature branch" is not the default (`SPEC:75`) |
| Consistent terminology | MET | Both: "outward action", "brief", "flag" each keep one meaning | MET | Both: "outward changes" kept distinct from "commits" | MET | Both: "leaves the machine" defined by a list (V3:3) |
| No internal contradictions | NOT MET | Both: X-003, `PRL:351` read both ways (V1:8 vs V1:14) | MET | Both: no V2-internal contradiction in `diff-analysis.md:47-57` | NOT MET | Both: X-006 (V3:23 vs V3:5) |
| Claims supported by evidence | MET | Both: every case bullet carries `path:line` (V1:8-11) | MET | Both: V2:8-10 cited | MET | Both: V3:5, V3:10 cited and confirmed on re-read |
| **Subtotal** | **2/5** | | **4/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| Logical ordering | MET | Both: position, key, case, then four sections (V1:3-24) | MET | Both: same order (V2:3-23) | MET | Both: position and commit rule before the key and the sections (V3:3-23) |
| Consistent hierarchy | MET | Both: one H1 and five H2 | MET | Both: one H1 and five H2 | MET | Both: one H1 and five H2 |
| Separation of concerns | MET | Re-eval (P1 MET, P2 NOT MET). Each H2 holds one concern; the commit clause is labelled within the position (V1:3); S-001 is an L1/Low surface point | NOT MET | Both: policy basis and #326 weakness sit inside day to day (V2:20; S-004) | MET | Both: action split separated from the commit rule (V3:3-5; S-001) |
| Navigation aids / cross-references | MET | Both: key (V1:5) and `SPEC` cross-references | MET | Both: key (V2:5) and `SPEC` cross-references | MET | Both: key (V3:7) and cross-references to other options |
| Artifact-type conventions | MET | Both: Position line, key, "Strongest case" plus the four standard sections | MET | Both: same | MET | Re-eval (P1 NOT MET, P2 MET). "Why a third option" is the heading the D1 and D3 option-c files use (`decisions/D1/option-c.md:7`, `decisions/D3/option-c.md:7`, re-read) |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Clarity (5 criteria)
<!-- TODO -->

### Risk Coverage (5 criteria)
<!-- TODO -->

### Invariant & Edge Case Coverage (5 criteria)
<!-- TODO -->

### Qualitative Summary
<!-- TODO -->

### Edge Case Floor Check
<!-- TODO -->

## Position-Bias Mitigation
<!-- TODO -->

## Combined Scoring
<!-- TODO -->

## Selected Base: Variant 3 (option (c))
<!-- TODO: confirm after scoring -->

### Selection Rationale
<!-- TODO -->

### Strengths to Preserve from Base
<!-- TODO -->

### Strengths to Incorporate from Non-Base Variants and the Debate
<!-- TODO -->
