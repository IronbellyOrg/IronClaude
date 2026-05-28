# Agent A — Theories: Why the Calibrator Confidently Scores Source-Only Evidence on Runtime-Behavior Claims

**Author**: Agent A (unmediated first-principles channel — no /sc:* skill invocation)
**Timestamp**: 2026-05-26
**Substrate**: `pr86-integration-contracts-20260526100600` (structurally analogous to the H3 0.95-REFUTE miss)
**Mechanism files read**:
- `/config/.claude/agents/confidence-calibrator.md`
- `/config/.claude/agents/refactoring-expert.md`
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`
- `/config/.claude/skills/confidence-check/SKILL.md`
**Substrate artifacts read**: `REPORT.md`, `audit.log`, `tier1-hypothesis.md`, `tier2-root-cause-analyst-calibration.md`, `tier2-quality-engineer-calibration.md`, `tier2-refactoring-expert-hypothesis.md`

---

## Theory 1 — Arithmetic-Mean Dilution of the Only Honest Dimension

### Mechanism

The rubric collapses five very heterogeneous dimensions into an unweighted arithmetic mean (`escalation-rubric.md:19` — "**Confidence** = arithmetic mean of the five dimension scores"). Four of those dimensions (symptom coverage, reproducibility fit, fix directness, domain coherence) can be scored to 1.0 *purely from the card's prose* — they are essentially "is the card well-organized, internally consistent, and tightly scoped?" Only **evidence grounding** asks the question that matters for runtime-behavior claims: "does the cited line actually do what the card says it does at runtime?" When evidence-grounding is honestly scored 0.5 (because the calibrator can't run `git show` / can't execute / can't observe), it is averaged against four 1.0s and the composite still lands at **(0.5 + 1 + 1 + 1 + 1) / 5 = 0.90** — visible verbatim in `tier2-root-cause-analyst-calibration.md:9-19`. The dimension that should have *vetoed* the verdict instead contributes 20% weight. In the H3 case the same arithmetic explains why a "I read main.rs and it falls through to start_client" verdict (evidence-grounding can only be partial because you didn't *run* it) survives as 0.95: the prose-readable dimensions all score 1.0 and dilute the one honest 0.5 (or the agent never even self-scores the source-vs-runtime gap, since the rubric doesn't *name* "did you actually execute this?" as a distinct check).

### Evidence

- `escalation-rubric.md:19` — `**Confidence** = arithmetic mean of the five dimension scores.` (unweighted, no veto rule).
- `escalation-rubric.md:11-17` (the dimension table) — four of five dimensions are scoreable from the card's prose alone; only "Evidence grounding" requires touching the cited substrate, and even *that* row defines 1.0 as "Cited `file:line` matches a real code path that exhibits the symptom" — "exhibits the symptom" is treated as inferable from reading code, not requiring execution.
- `tier2-root-cause-analyst-calibration.md:11-17` — explicit demonstration: evidence-grounding=0.5, other four=1.0, calibrated mean = **0.90**. The Note at `tier2-root-cause-analyst-calibration.md:33` admits "F5 test fixture citation is factually absent at current HEAD" — yet the dilution math still produced 0.90.
- `tier2-quality-engineer-calibration.md:13-17` — same shape: evidence-grounding=0.5, three 1.0s, fix-directness=0.5 → 0.60. When fix-directness *also* drops to 0.5 the score finally moves; when only evidence-grounding is honest, the math hides it.
- `REPORT.md:114-116` — "Tier 1 confidence-calibrator scored evidence-grounding 0.5 because it lacked Bash to verify PR-sha citations via `git show`. The orchestrator (this skill) DID verify those citations directly in Wave 0" — confession that the calibrator's evidence-grounding score is structurally truncated, *and the rubric has no mechanism to translate that structural truncation into a confidence ceiling.*

### Per-theory confidence

**0.85** — the math is directly observable on disk (`tier2-root-cause-analyst-calibration.md`), and the rubric's own text in `escalation-rubric.md:19` confirms the unweighted-mean structure with no veto-on-low-evidence-grounding rule.

### If this theory is right, the systemic fix is…

Replace the unweighted arithmetic mean with a **veto-or-cap rule**: any dimension scored ≤ 0.5 caps the composite at 0.75 (below the 0.85 escalation threshold), regardless of how clean the other four are.

---

## Theory 2 — "Evidence Grounding" Conflates Source-Citation with Runtime-Verification

### Mechanism

The rubric's "Evidence grounding" row defines 1.0 as "**Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom**" (`escalation-rubric.md:13`). The OR is the trap. It permits the calibrator (and the upstream agent self-grading) to score 1.0 on **source citation alone** without ever requiring "diagnostic command output reproduces the symptom." For a static defect (missing import, wrong regex literal) this is fine — the source IS the runtime behavior. For a **dynamic-control-flow defect** (does `Some(Command::Options(...))` fall through to `start_client`? Does an empty `contract_idents` *actually* bypass the guard at runtime?), source citation can be deeply misleading: control flow that *appears* to fall through in a static read can be diverted by a match arm, a `?` operator, a panic, a feature flag, or a side-effecting initializer that wasn't on the read path. The rubric never names this distinction. So an agent that read 200 lines of Rust source and traced a control flow with their eyes can in good conscience claim "Evidence grounding = 1.0" — and the calibrator, also tooled only with `Read`, has no way to falsify that claim. The H3 0.95-REFUTE is exactly this pathology: a source-traceable "falls through" claim that the runtime contradicts.

### Evidence

- `escalation-rubric.md:13` — the literal OR clause: `Cited file:line matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom`. There is no third clause requiring "AND runtime verification when the claim is about dynamic behavior."
- `confidence-calibrator.md:5` — `tools: Read`. The calibrator agent **cannot execute anything**; it physically cannot upgrade an evidence-grounding score by reproducing the symptom. It can only spot-check source-vs-citation, which is *exactly the half of the OR clause that is insufficient for runtime claims.*
- `confidence-calibrator.md:51` — "Spot-check the evidence: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches." The instruction is about **snippet match**, not about **runtime behavior of the cited code**. A snippet match → 1.0 is fully compatible with the runtime behavior being the opposite of what the card claims.
- `confidence-check/SKILL.md:53-110` — the upstream `Confidence Check` skill that feeds this culture has 5 weighted checks, none of which is "did you reproduce the symptom?" Check 3 is "Official Documentation Verified?" (`SKILL.md:80`) and Check 5 is "Root Cause Identified?" (`SKILL.md:102`) — both phrased so that *reading* is the verification act. The cultural prior, established at the pre-implementation gate, treats source-reading as the highest tier of evidence.
- `tier2-refactoring-expert-hypothesis.md:91-96` — even the refactoring-expert's *self*-stated confidence of 0.78 is sourced from "I am confident the helper exists and is small (0.95 on F1/F3 collapsing cleanly)" — confidence is calibrated against *structural* readability of the proposed change, not against any runtime probe.

### Per-theory confidence

**0.80** — the OR clause is directly cited; the calibrator's `tools: Read` restriction is mechanically incontestable. The slight gap is uncertainty about whether the H3-case `refactoring-expert` would have *self*-rated evidence-grounding lower if the rubric had a third "runtime-verified" anchor. (May still have not, given the cultural prior in `confidence-check/SKILL.md`.)

### If this theory is right, the systemic fix is…

Split "Evidence grounding" into two dimensions: **Source-citation accuracy** (snippet matches) and **Runtime verification** (symptom reproduced or behavior asserted by test). For claims whose answer depends on dynamic control flow, runtime-verification ≥ 0.5 must be required before source-citation can score above 0.5.

---

## Theory 3 — Stripped-Context Independence Removes the Doubt Signal Without Removing the Confidence Signal

### Mechanism

The calibrator is *deliberately* deprived of the hypothesis-formation context (`confidence-calibrator.md:21` — "You are deliberately stripped of the hypothesis-formation context — you did not run the grounding queries, you did not draft the brief, you did not iterate on the hypothesis"). The stated goal is to reduce anchoring bias from the upstream agent's narrative. But this strip **also removes the upstream agent's hedges, doubts, near-misses, and "I almost concluded X but then noticed Y" trail** — the very signals that would tell a calibrator "this is the kind of question where source-only reading is insufficient." What survives the strip is the *clean, finished card* — and clean finished cards optimize for the rubric's prose-readable dimensions (symptom coverage, fix directness, domain coherence all default to 1.0 when the card is well-written). The cleaner the card, the higher the dilution-survivable score (compounding Theory 1). The H3 0.95-REFUTE is consistent with this: a confidently-written REFUTE card with crisp citations and clean control-flow narrative will pass the strip cleanly *because the doubts that should have been there were never written down* — and the calibrator, by design, has no upstream signal to flag the missing-doubt. The agent's `confidence-calibrator.md:35` mindset — "Never apply social judgement ('the agent seemed careful')" — is correct as anti-anchoring discipline but also forbids the calibrator from noticing "this REFUTE was issued without any runtime check, on a question that has a runtime dimension."

### Evidence

- `confidence-calibrator.md:21` — explicit strip: "the upstream investigative trail is not [seen by you] — that is where the dominant anchoring bias lives." The trail-strip is framed as pure benefit; the cost (loss of doubt-signal) is unnamed.
- `confidence-calibrator.md:25` — "**Self-reported confidence on the card is a signal, not a number.**" The card's own confidence is downweighted, but the rubric scores remain inputs — so a card that scored itself with appropriate self-doubt (the H3 agent's *real* uncertainty about source-only-evidence on a runtime claim) gets that doubt discarded.
- `hypothesis-card-template.md:104-108` and `:60-62` — the template has an "If I'm wrong, it's probably because..." section but it's a one-sentence next-most-likely-explanation, NOT a "what kind of evidence would falsify me." A well-written card fills this with a substantive alternative (`tier1-hypothesis.md:101-103`, `tier2-refactoring-expert-hypothesis.md:104-106`) — but neither template nor rubric ask "what would have been the gold-standard evidence vs what you actually have."
- `tier2-refactoring-expert-hypothesis.md:91-92` — the only place hedge survives in the substrate is the self-confidence number (0.78 instead of 0.90+) — and that signal is *explicitly downweighted* per `confidence-calibrator.md:25-27` ("the dimension scores tell the truth and the average wins"). The doubt that the upstream agent actually had cannot push the calibrated score down.
- `audit.log:35` — even the orchestrator notes the calibrator "spot-checked against current branch `feat/agents-tavily` rather than PR sha `67ab0af5` because it has no Bash; could only verify F1." The calibrator was *aware it was scoring on partial information* — and the rubric's structure still let it score the other four dimensions at 1.0 anyway.

### Per-theory confidence

**0.65** — the strip-removes-doubt mechanism is logically sound and mechanically supported by `confidence-calibrator.md:21,25`, but I cannot directly verify (from substrate only) that the H3 `refactoring-expert` *did* write hedging text in its grounding-trail that got stripped. The pr86 substrate shows hedge-text *survives in the final card* in some cases (`tier2-refactoring-expert-hypothesis.md:91-96`), which weakens the "doubts only live in stripped context" claim. Still distinct enough from Theories 1 and 2 because the mechanism is about *information channel* rather than *arithmetic* or *dimension definition*. `[partially uncited — H3 stripped-context hedge inference based on calibrator prompt's strip mandate, not on a verified H3 trail]`

### If this theory is right, the systemic fix is…

Add a mandatory "Falsification standard" field to the hypothesis card template — "what evidence would prove me wrong" — that survives the strip, and require the calibrator to score whether that standard was met by the card's actual evidence (not whether the cited evidence merely matches).

---

## Cross-theory implications

- **Theories 1 and 2 compound multiplicatively, not additively.** The arithmetic-mean structure (T1) only produces a 0.90 from a 0.5 evidence-grounding because the OR clause (T2) lets four other dimensions honestly score 1.0 on prose. Fix only T1 (cap on low evidence-grounding) and well-written cards still pass; fix only T2 (split into source-citation + runtime-verification) and the dilution math still hides the low new dimension. **Both fixes are required, and applying either alone underfits the failure mode.**
- **Theory 3 is upstream of Theories 1 and 2.** Even with veto rules (T1) and runtime-verification dimension (T2), if the calibrator never sees the trail of doubts, it cannot raise *new* concerns the upstream agent failed to articulate — it can only re-grade against what's on the card. T3's fix (mandatory falsification-standard field) generates the input that T1's veto and T2's new dimension would then act on.
- **All three theories share a common root**: the entire calibration apparatus treats **source-reading as a complete epistemology for code claims**. This is true for static defects and structurally false for control-flow / runtime / environment-dependent claims. The H3 case (`zellij` subcommand dispatch behavior) and the pr86 case (PR-sha citations + Layer 3 emptiness bypass) both have a runtime dimension that source-only reading systematically under-detects.
- **A potential conflict**: T3's recommended "Falsification standard" field could amplify well-written but wrong cards (a confident "this would be falsified by X" claim still anchors the calibrator) unless paired with T2's runtime-verification dimension that demands the falsification standard *be applied*, not just *be stated*.
- **Substrate-vs-H3 fidelity caveat**: the pr86 substrate's calibrations are 0.90 and 0.60, not 0.95. The mechanism is structurally identical (`tier2-root-cause-analyst-calibration.md:11-19` shows evidence-grounding=0.5 + four 1.0s = 0.90) but the H3 0.95 would require either (a) the upstream agent self-scoring evidence-grounding at 1.0 (not 0.5) by claiming the source read *did* match runtime behavior — Theory 2 in its strongest form — or (b) all five dimensions self-scored at 1.0 with the calibrator unable to dispute. Either route is consistent with the theories above; without H3's calibration card on disk I cannot distinguish which dominated.
