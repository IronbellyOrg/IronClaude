<!-- sc:adversarial FINAL invocation -->
<!-- Skill name resolved: sc:adversarial (routed to sc-adversarial-protocol) -->
<!-- Invocation form: --compare A,B,C --depth deep -->
<!-- Skill output original path: /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/calibration-failure/final-merge/adversarial/ -->
<!-- Inputs: agent-A-merged.md, agent-B-merged.md, agent-C-merged.md -->
<!-- Note: --agents opus,haiku and --merge dropped per user re-spec; cross-model pressure is forfeited at this stage. Upstream Step 2 cross-model variance (when present) is what's actually being compared. -->
<!-- Convergence: 0.87 (above 0.80 threshold) -->

# T4 Pane-Title Investigation — Final Merged Root Causes of Calibration Failure

**Scope.** Why did Tier 2 produce H3 (REFUTE, 0.95) and H2 (REFUTE, 0.85) confidences that were empirically wrong, and why did the calibration layer fail to catch them?

**Method.** Consolidation of three independently merged adversarial passes (A, B, C). Likelihood scores capped at [0.30, 0.85] per the brief. Empirical disk check performed: `tier2-*-calibration.md` artifacts are absent from the run directory — confirming the calibrator did not execute.

---

## 1. Top Root Causes (Ranked)

### #1 — Calibrator non-execution (audit layer)

**Claim.** The `confidence-calibrator` agent never ran against the Tier 2 hypothesis cards; the 0.95 (H3) and 0.85 (H2) values in the audit log are agent-self-reported confidences passed through unchecked.

- **Layer:** audit
- **Likelihood:** 0.85 (empirically verified; cap applied)
- **Blast radius:** Universal — every hypothesis card in every troubleshoot run is silently unguarded. The protective layer is defined but not enforced.
- **Convergence:** 3/3 (B and C primary; A treats it as the load-bearing open question, resolved by empirical check)
- **Evidence:**
  - `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:92-93` — card's `## 4. Confidence` reads "**95%** that H3 is refuted"; same 0.95 surfaces unmodified in `audit.log:22` and `REPORT.md:166`, consistent with pass-through.
  - `/config/.claude/agents/confidence-calibrator.md:24-26` — Independence Instruction: "Self-reported confidence on the card is a signal, not a number." The protection is specified; the disk shows no `tier2-*-calibration.md` artifacts, so the protection did not run.
- **Rationale.** Highest likelihood because absence of the calibrator artifact is a direct, file-system-verifiable fact. Universal blast radius makes this the dominant fix surface even though it is not, by itself, sufficient (see INV-001).

### #2 — Rubric evidence-class disjunction (generation layer)

**Claim.** The escalation rubric's "Evidence grounding 1.0" anchor is disjunctive — `file:line` *OR* diagnostic command output — which lets a runtime claim be scored 1.0 from source-only refutation, with no claim-class vs evidence-class alignment check.

- **Layer:** generation
- **Likelihood:** 0.80
- **Blast radius:** All runtime-behavior claims (PTY, CLI dispatch, async timing, IPC, scheduler, environment-coupled bugs). Static-source claims are unaffected.
- **Convergence:** 3/3
- **Evidence:**
  - `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-17` — dimension table; the 1.0 anchor on "Evidence grounding" reads "Cited `file:line` matches a real code path... OR diagnostic command output reproduces the symptom." No dimension scores claim-type/evidence-type alignment.
  - `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:21-79` — H3's entire Evidence section is a static source-read across 4 files plus an anecdote; no `bash` runs, no `zellij list-sessions` traces. Scored 1.0 on Evidence grounding under the disjunction.
- **Rationale.** Even if #1 is fully fixed, a perfectly-executed calibrator using this rubric still scores H3 high (see INV-001). This is the generation-layer co-cause without which #1's fix is incomplete.

### #3 — Refute-vs-confirm verdict asymmetry (generation layer)

**Claim.** The rubric and calibrator treat REFUTE and CONFIRM verdicts symmetrically, but refutation requires strictly more evidence — a CONFIRM needs one positive sighting, a REFUTE needs exhaustive coverage of all paths. The symmetric rubric cannot detect this.

- **Layer:** generation
- **Likelihood:** 0.70
- **Blast radius:** All REFUTE cards across all troubleshoot runs, especially negative-existential refutations (e.g., "no early-return exists anywhere").
- **Convergence:** 3/3
- **Evidence:**
  - `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:11-19` — dimension table makes no confirm/refute distinction; "Evidence grounding 1.0" is defined identically for both verdict shapes.
  - `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:102` — risk §6 admits "If `start_client_impl` has a guard that early-returns when `command == Some(Command::Options(_))`, the refutation would weaken" — i.e., one unread file flips the verdict. For a CONFIRM, one unread file would not.
- **Rationale.** Explains the inversion (H3 0.95 REFUTE > H1 0.82 CONFIRM despite less empirical grounding) that no protective layer caught. Ranked below #2 because the disjunction (#2) is the more general defect; asymmetry is a specialization that hits REFUTE cards hardest.

### #4 — Anti-anchoring procedural deficit (design layer)

**Claim.** Even when the calibrator runs, its narrative-stripping defense ("you only see the finished card and the rubric") is procedural, not structural — a card's confident prose can still anchor the rubric scoring. The design relies on calibrator discipline that has no enforcement loop.

- **Layer:** design
- **Likelihood:** 0.55 (conditional on #1 being fixed — only observable once calibration actually runs)
- **Blast radius:** Narrative-anchored cards (cards with high prose-confidence even when evidence is thin); affects calibrated runs after #1 is remediated.
- **Convergence:** 3/3
- **Evidence:**
  - `/config/.claude/agents/confidence-calibrator.md:21` — "Apply the rubric mechanically: one dimension at a time, score with evidence, never inherit the card's self-reported confidence." Discipline is specified but not structurally enforced.
  - `/config/.claude/agents/confidence-calibrator.md:35` — Behavioral Mindset acknowledges "Anchoring bias is reduced, not eliminated. The card is still input." Design admits the residual anchor risk in plain text.
- **Rationale.** Ranked #4 because it is only visible after #1 is repaired; today's failure is dominated by #1 + #2. Stays on the list because the long-tail fix surface for the next generation of failures will be here.

### #5 — Agent-domain mismatch (assignment layer)

**Claim.** A `refactoring-expert` agent — whose focus areas are static code-simplification — was assigned a runtime CLI-dispatch hypothesis. The mismatch produced a thorough static read and zero runtime reproduction, which the rubric (per #2) cannot penalize.

- **Layer:** assignment
- **Likelihood:** 0.50
- **Blast radius:** Cards assigned to non-matching expertise (refactoring-expert on runtime; security-expert on perf; etc.). Bounded by the assignment surface, not the rubric surface.
- **Convergence:** 3/3
- **Evidence:**
  - `/config/.claude/agents/refactoring-expert.md:22-27` — focus areas: "Code Simplification, Technical Debt Reduction, Pattern Application, Quality Metrics, Safe Transformation." None are runtime/PTY/CLI-dispatch domains.
  - `/config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-h3-options-subcommand.md:21-79` — Evidence section is a static four-file source-read with no runtime traces — exactly the work product the focus areas predict.
- **Rationale.** Contributing factor, not the dominant fix surface. Ranked last because fixing assignment alone (#5) without fixing the rubric (#2) would still let the next mismatched agent score 1.0 on evidence grounding.

---

## 2. Unresolved Contradictions

### X-001 — Calibrator execution status (RESOLVED)

- **Original split.** Variant A treated calibrator execution as an open question; variants B and C treated calibrator-output absence as primary.
- **Resolution.** Empirically verified — `ls /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-*-calibration.md` returns "No such file or directory." Resolved toward the B/C framing.
- **Verification step (to re-run if doubted).** `ls /config/workspace/Coder/.dev/troubleshoot/t4-pane-title-20260526-101500/tier2-*-calibration.md` — must return file paths for the calibrator to have run.

### INV-002 — Partial-calibration handling (UNADDRESSED)

- **Issue.** None of the three merged inputs specify what happens when some hypotheses are calibrated and others are not, nor whether the audit layer detects a partial run.
- **Resolution.** None. Carry into Step 4 brainstorm as an open design question.
- **Verification step.** Read the orchestrating skill (`sc-troubleshoot-protocol/SKILL.md` or sibling) and search for any precondition gate that asserts "all Tier 2 cards have a sibling `*-calibration.md`." If no such gate exists, INV-002 is structurally open. Quick check: `grep -rnE 'calibration|calibrator' /config/.claude/skills/sc-troubleshoot-protocol/`.

### INV-003 — Rubric-version pin (LOW, UNVERIFIED)

- **Issue.** Whether the audit log records which version of the escalation rubric was applied.
- **Resolution.** Spot-checked: `grep -nE 'calibrat|rubric.version|escalation-rubric' audit.log` returned no matches. Treat as "rubric-version pinning is absent from the audit trail." Low blast radius; surface in Step 4 only if rubric is to be versioned.
- **Verification step.** Same `grep` above; absence of matches confirms the gap.

---

## 3. Causes Excluded From Top List

- **H3 verdict shape (Variant B unique).** "Negative-existential cards are ungradable by this rubric" — subsumed by #3 (refute-vs-confirm asymmetry), of which negative-existential is the extreme case.
- **H3 0.95 → 0.95 self-report pass-through framing (Variant C unique).** Subsumed by #1; pass-through is the symptom, calibrator non-execution is the cause.
- **GitHub-URL spot-check impotence (A, C).** Real but low blast radius for *this* failure (H3 cited local files, not GitHub URLs); folds under #4 as a structural-discipline gap. Surface separately only when remediation explicitly addresses external-URL evidence.
- **H3 0.95 REFUTE > H1 0.82 CONFIRM inversion (B, C).** Refuted as a *cause* — it is a diagnostic *smell* produced by #3; not an independent root cause.
- **"Confidence ≥0.90 has operational meaning downstream" assumption.** Surfaced as A-β (shared assumption, §5); not a cause but a constraint on remediation scope.

---

## 4. Convergence Statistics

- **3/3 (six themes):** rubric evidence-class disjunction; proposition substitution / claim-vs-evidence-class mismatch; refute-vs-confirm asymmetry; agent-domain mismatch; calibrator narrative-capture / anti-anchoring procedural deficit; calibrator-output absence (B/C primary, A as open question, resolved by empirical check).
- **2/3 (two themes):** GitHub URLs not Read-spot-checkable (A, C); H3 0.95 REFUTE > H1 0.82 CONFIRM inversion as calibration smell (B, C).
- **1/3 (two themes):** H3 verdict shape may be ungradable (B unique); H3 0.95 → 0.95 self-report pass-through as "placebo failure made manifest" (C unique).

Overall convergence (debate round 3): **0.87** — above 0.80 threshold.

---

## 5. Unstated Shared Assumptions (Limits of This Analysis)

All three merged inputs share these assumptions; none was probed in any of the variants. They bound what this final merge can claim.

- **A-α — Rubric/calibrator is the right layer to fix.** Alternatives (e.g., a verification-gate that requires actual command output for runtime claims before any confidence is assignable, sitting upstream of the rubric entirely) were not considered.
- **A-β — Confidence ≥0.90 has operational meaning downstream.** All three treat 0.95 as load-bearing. If downstream consumers (orchestrators, escalation gates) actually only branch on coarse buckets (e.g., {<0.70, 0.70–0.89, ≥0.90}), the calibration-precision target is much weaker than this analysis implies.
- **A-γ — Negative existential cards are gradable.** All three assume H3 ("no early-return exists anywhere") *can* receive a meaningful confidence score under a fixed rubric. It may be that such claims should be rejected at intake and required to convert to a positive falsifiable form.
- **A-δ — Rubric aggregation is arithmetic mean.** Confirmed by reading `escalation-rubric.md:19` ("Confidence = arithmetic mean of the five dimension scores"). The assumption is correct *as written* but never re-derived — alternatives (worst-dimension-wins, geometric mean, dimension-weighted) were not considered as remediation surfaces.

---

*End of consolidated root-cause merge. Step 4 (sc:brainstorm) will operate on this artifact.*
