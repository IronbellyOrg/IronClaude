# Evaluation: Bare Reviewer Adjunct on /sc:auggie-review

```yaml
evaluation_metadata:
  date: 2026-05-28T04:47Z
  spec_context: merged-requirements.md (v1.2.0-draft)
  question: "What's the marginal value of adding --bare-reviewers N to /sc:auggie-review's existing pipeline?"
  scope: /sc:auggie-review specifically (not all callers)
  framing: honest cost/benefit, not advocacy
```

---

## 1. What /sc:auggie-review Already Does

Per the protocol skill (`sc-auggie-review-protocol`) and agent (`auggie-reviewer`):

1. **Auggie deep-retrieval pass** — `mcp__auggie__codebase-retrieval` against the diff/PR/snapshot target. Auggie indexes the full repo and surfaces semantically-relevant code regions for the changed lines.
2. **Claude-side review pass** — independent agent (`auggie-reviewer`) reviewing the same target with Read/Grep/Glob + Serena symbol navigation. Cross-validation of Auggie's findings against real file content.
3. **Findings triage** — bugs, architectural risks, anti-patterns categorized.
4. **PR-post** — if invoked on a PR, posts validated findings as PR comments.
5. **Remediation handoff** — offers to chain into task-builder if findings warrant work.

**Effective reviewer count today: 2** (Auggie + Claude-side), both Anthropic-trained, both protocol-driven.

---

## 2. What Bare Adds That Isn't Already There

| Dimension | Existing pipeline | What bare adds | Marginal value |
|-----------|-------------------|----------------|----------------|
| Reviewer count | 2 | +2/3/4 → 4-6 total | Linear with N (more eyes, more findings) |
| Training-distribution diversity | Both Anthropic | DeepSeek + Qwen + Kimi + GLM (non-Anthropic) | Genuine — non-Anthropic models hallucinate differently |
| Protocol vs unstructured | Both protocol-driven | Bare = no protocol | Catches edge cases protocols don't probe (the 7.8 lesson) |
| Codebase context | Auggie has deep repo context | Bare sees ONLY the diff snippet | LOWER context — but that's a feature, not a bug, for fresh-eyes probing |
| Library-knowledge grounding | Auggie indexes code; no docs | With `--bare-c7`: docs context injected | Net new — neither Auggie nor Claude-side currently pulls library docs |
| Hallucination tolerance | Cross-validation gates findings | Validator-gated with suspect-tagging | Existing tolerance + new SUSPECT layer |

**The honest summary:** Bare adds *distribution diversity* and *unstructured probing*. These are real, but conditional on the validator working correctly. They're not free.

---

## 3. Concrete Value Mechanisms

### 3.1 Cross-vendor agreement is a stronger signal than within-Anthropic agreement

When Auggie and Claude-side both flag a finding, the agreement is meaningful but **within-distribution** — both are Anthropic-trained and may share systematic blindspots.

When Auggie + Claude-side + a non-Anthropic bare reviewer (say, DeepSeek) all flag the same finding, the agreement crosses training distributions. This is genuinely stronger evidence.

**Concrete example:** A subtle data-race in a Go file. Auggie surfaces the relevant code; Claude-side reviews it; both miss the race (Anthropic-distribution blindspot). DeepSeek (trained on different code corpora) flags it. The bare reviewer has caught what the existing pipeline missed.

**Honest caveat:** This relies on training distributions actually being independent. DeepSeek, Qwen, Kimi, and GLM all train on overlapping public web/code data. Genuine independence is weaker than the diversity hypothesis assumes. In the literature, ensemble methods get 1-3% accuracy gain at the high end, not 30%.

### 3.2 Unstructured probing finds protocol-blindspots

The `auggie-reviewer` agent is **structured**: it follows a review template (bugs / architectural risks / anti-patterns). The bare prompt is `Review {target}.` — no template, no rubric.

This is the empirically-demonstrated value from the 7.8 experiment: bare caught 8 things the structured reviewer missed. The same dynamic applies on auggie-review IF the existing reviewers have systematic blindspots beyond what diversity alone covers.

**The 7.8 case was Reflect (one reviewer) + Bare (one reviewer).** auggie-review already has 2 reviewers. The marginal yield from a 3rd reviewer (bare) is smaller than the marginal yield in the 7.8 case (which doubled the reviewer count). Realistic estimate: 15-25% additive findings, not 36%.

### 3.3 c7 library-doc grounding is genuinely net-new

Existing auggie-review pipeline does NOT pull library docs. Auggie indexes code; it doesn't fetch context7 docs. If a diff uses `lipgloss.Style.Render()` and a future v2 changes the return type, neither Auggie nor Claude-side has up-to-date docs to catch the staleness.

With `--bare-c7`, the bare reviewers have fresh library docs. This is the strongest single argument for the bare adjunct on auggie-review: **bare-with-c7 catches a class of issues (library deprecations, breaking changes, API drift) that the existing pipeline has zero coverage of.**

### 3.4 Suspect isolation works as a noise filter

When bare reviewers hallucinate (and they will), the SUSPECT tagging + validator gate prevents hallucinations from leaking into the merged output. Worst case: bare contributes nothing actionable (all findings Demoted/Dropped). Best case: bare contributes 1-3 high-value findings per call (Validated/Corroborated).

**This holds ONLY if IMM-1 (corroboration rule) and IMM-2 (semantic-match validation) are correctly implemented.** See §5 below.

---

## 4. Concrete Cost Mechanisms

### 4.1 Token + latency cost per invocation

| Phase | Existing (no bare) | With --bare-reviewers 3 | With --bare-reviewers 3 --bare-c7 |
|-------|-------------------|--------------------------|-------------------------------------|
| Auggie retrieval | ~5K tokens, 5-15s | unchanged | unchanged |
| Claude-side review | ~20K tokens, 15-30s | unchanged | unchanged |
| Bare dispatch (3×) | — | ~45K tokens external, 10-30s wall (parallel) | ~45K tokens external + 8K c7 docs, 15-45s wall |
| c7 enrichment | — | — | +3K-10K tokens internal, +30-60s wall |
| Adversarial merge | — | +10-15K tokens, +20-40s | +12-18K tokens, +20-40s |
| **Total delta vs baseline** | — | **+55-60K tokens, +30-70s** | **+68-81K tokens, +60-145s** |

Existing baseline: ~25K tokens, ~30-45s wall clock.
With `--bare-reviewers 3`: ~3x token cost, ~2x wall clock.
With `--bare-c7`: ~3.5x token cost, ~3x wall clock.

**This is non-trivial.** It's defensible for high-stakes PRs (large, architecture-changing, security-sensitive). It's wasteful for trivial diffs.

### 4.2 Output-volume cost (PR-post mode)

If `/sc:auggie-review` auto-posts to PR, every finding becomes a PR comment. Going from 2 reviewers to 4-5 reviewers can multiply finding count.

**Even with validator gating (only Validated/Corroborated reach merged output), the noise floor rises.** A 3-finding PR comment thread becomes a 7-finding thread. Some of those extra 4 will be genuine; some will be near-misses or Corroborated-but-not-actionable.

For PR ergonomics, the bare adjunct is a double-edged sword: more findings means better coverage AND more noise. The signal-to-noise ratio of the merged output depends entirely on validator quality.

### 4.3 Reviewer-fatigue cost

PR reviewers (humans) calibrate to bot-comment volume. If sc:auggie-review historically posted 2-4 findings per PR, and now posts 5-8, the human reviewer's mental triage cost goes up. They may start ignoring bot comments — which destroys the value of the more-thorough review.

This is a real but qualitative cost. Mitigation: when posting to PR, surface the bare-sourced findings under an explicit "Cross-validated by additional models" header so human reviewers know what they're looking at.

---

## 5. The IMM-Blocker Dependency (Honest Conditional)

The value calculation depends on validator quality. From spec-panel-review.md, six IMM items still block Phase 1:

- **IMM-1** — Corroboration must require ≥1 non-suspect source (currently bare-on-bare corroboration validates wrong claims)
- **IMM-2** — Validated rule needs semantic-match check (currently cite±5-lines can be gamed)
- IMM-3, IMM-5, IMM-6 — operational fixes
- IMM-4 — empty-target guard

**If IMM-1 and IMM-2 are correctly implemented:**
- Bare-on-auggie-review adds **net positive value** (15-25% additive Validated/Corroborated findings, distribution diversity, library-doc grounding)
- The hallucination risk is bounded

**If IMM-1 and IMM-2 are NOT implemented or implemented incorrectly:**
- Bare-on-auggie-review adds **net negative value** in PR-post mode (hallucinations leak into PR comments, eroding human-reviewer trust)
- Bare-on-auggie-review may add net positive value in NON-post mode (artifact-only review, human consumes with caveat)

**Decisive recommendation:** Do not enable `--bare-reviewers` on auggie-review's PR-post mode until IMM-1 + IMM-2 ship. For non-post (artifact-only) use, the risk is acceptable today.

---

## 6. When Bare Adds The Most Value

Concrete diff/PR shapes where the bare adjunct's value is HIGHEST:

1. **Library-heavy diffs** — adds, removes, or upgrades a third-party dependency. `--bare-c7` makes auggie-review aware of library docs it currently can't see.
2. **Cross-cutting refactors** — touches ≥5 files, changes interfaces across modules. Unstructured probing catches integration risks Auggie's per-file retrieval may miss.
3. **Security-sensitive surfaces** — auth, crypto, input validation. Distribution diversity catches different threat-model assumptions.
4. **Performance-critical paths** — hot loops, locking, memory layouts. Bare reviewers with different training corpora flag different perf concerns.
5. **First contribution from a new contributor** — high investment in catching style/correctness/conformance issues; bare adjunct's coverage breadth pays off.

## 7. When Bare Adds The LEAST Value (or Negative)

1. **Trivial diffs** — typo fixes, single-line bug fixes, simple test additions. Cost outweighs benefit; bare findings will be either redundant or noise.
2. **Codebase-pattern-heavy diffs** — applying an existing pattern to a new file. Auggie's repo context is most valuable here; bare's fresh-eyes lacks the pattern awareness.
3. **PR-post mode with un-shipped IMM-1/IMM-2** — net negative per §5.
4. **Very long diffs (>10K lines)** — bare reviewers will be heavily truncated (`--target-line-cap` triggers); their review of the visible portion is less reliable.
5. **Generated-code diffs** — auto-formatter changes, codegen output. Bare reviewers will flag stylistic "issues" that are intentional.

---

## 8. Recommended Defaults for /sc:auggie-review Integration

```yaml
recommended_defaults:
  flag_exposure:
    - "--bare-reviewers <0|2|3|4>"           # opt-in per call
    - "--bare-c7"                            # opt-in companion
    - "--bare-c7-libs <comma-list>"          # explicit lib override
    - "--bare-pr-post-mode <strict|loose>"   # NEW for auggie-review specifically

  default_bare_reviewers: 0                  # off by default — opt-in per call
  default_c7: false                          # off by default
  default_pr_post_mode: strict               # for safety until validator quality is empirically baselined

  pr_post_mode_semantics:
    strict: |
      Only Validated findings (cited file:line + semantic-match verified) reach PR comments.
      Corroborated-only findings are demoted to merged-output appendix.
      Mitigates IMM-1/IMM-2 risk for PR ergonomics.
    loose: |
      Both Validated and Corroborated findings reach PR comments.
      Use ONLY after IMM-1 and IMM-2 are confirmed correct in production.
      Higher recall at cost of higher noise floor.

  artifact_only_mode:                        # when NOT posting to PR
    bare_reviewers_acceptable: true          # the artifact consumer can apply caveat
    c7_acceptable: true                      # net positive for artifact reviewers
```

---

## 9. A/B Test Proposal (the empirical-validation path)

The spec's value-of-c7 question (INV-04 from c7-agent-debate.md) and this evaluation's marginal-value-on-auggie-review question share an empirical gap. Same A/B test answers both:

```yaml
ab_test_design:
  population: "20 recent merged PRs across the project (mix of trivial, medium, complex)"
  arms:
    A_baseline: "/sc:auggie-review (no bare adjunct)"
    B_bare_no_c7: "/sc:auggie-review --bare-reviewers 3 (no --bare-c7)"
    C_bare_with_c7: "/sc:auggie-review --bare-reviewers 3 --bare-c7"
  measurements_per_PR:
    - total_findings_count
    - validated_findings_count
    - corroborated_findings_count
    - dropped_findings_count
    - novel_findings_not_in_A (for B and C)
    - human_reviewer_agreement (3-point: agree, partial, disagree)
    - wall_clock_seconds
    - estimated_cost_USD
  decision_criteria:
    enable_bare_by_default: "B or C produces >2 novel + human-agreed findings per PR averaged"
    enable_c7_by_default: "C produces >1 c7-attributable novel finding per PR averaged"
    abort_bare_on_pr_post: "B or C produces >0.5 human-disagreed findings per PR (noise floor too high)"
  estimated_cost_to_run: "~200 invocations × ~$0.30 avg = ~$60 total"
```

This $60, ~1 day test would settle:
- Is bare worth the cost on auggie-review specifically? (B vs A)
- Is c7 enrichment net-positive? (C vs B)
- Should PR-post default to strict or loose? (noise-floor measurement)

---

## 10. Final Verdict

**Conditional value:**

- **Today (pre-IMM-1/IMM-2 fixes):** Implement `--bare-reviewers` flag on auggie-review for **artifact-only mode**, but disable it for **PR-post mode** until validator quality is verified. The signal-to-noise ratio in PR comments is too sensitive to current validator weaknesses.
- **Post-IMM-1/IMM-2 fixes:** Enable for all modes. Default to off (opt-in per call) until A/B test results justify a default change. `--bare-c7` is the strongest single argument — addresses a coverage gap (library docs) the existing pipeline has zero coverage of.
- **Post-A/B test (depending on results):** Either enable by default for medium/complex PRs, or leave opt-in for power users.

**Numerical estimate:**

Per-invocation value for medium-complex PR, post-IMM fixes, with --bare-c7:
- +1 to +3 high-quality findings the existing pipeline would have missed
- +2 to +5 low-quality findings (noise — gated by validator)
- +60-145s wall-clock
- +~$0.10-$0.40 per invocation external proxy cost

Per-invocation value for trivial PR:
- +0 to +1 finding (mostly noise)
- +60-145s wall-clock
- +~$0.10-$0.40 cost
- Negative ROI

**Recommendation:** Implement the integration with default-off behavior. Run the A/B test before defaulting on. PR-post mode is gated on IMM-1/IMM-2 landing.

---

*Evaluation produced 2026-05-28T04:47Z. Honest framing: value-add is real but conditional on validator quality and PR-size; not a blanket "enable everywhere" recommendation. The single highest-ROI scenario is library-heavy diffs with `--bare-c7` post-IMM-1/IMM-2 fixes.*
