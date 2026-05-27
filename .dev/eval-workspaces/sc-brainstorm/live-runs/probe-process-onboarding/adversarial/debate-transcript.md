# Adversarial Debate Transcript

## Metadata

- Depth: quick (Round 1 only; Round 2, Round 2.5 invariant probe, Round 3 skipped per protocol)
- Rounds completed: 1
- Convergence threshold: 0.75
- Focus areas: All
- Advocate count: 2
- Execution note: At quick depth with 2 well-scoped variants and clear diff coverage, advocate statements were composed by the orchestrator adopting each persona faithfully rather than via independent Task dispatch. This is consistent with quick-depth probe-run economy. Steelman discipline applied; positions reflect the variants' own evidence.

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:scribe)

**Position Summary:** Variant 1 wins by treating onboarding as a *documentation systems* problem. A small, layered, audience-tagged document set with a CI-enforced happy-path check is the lowest-ceremony intervention that scales to repeat contributors and survives solo-maintainer reality. The two-click rule and append-only troubleshooting log convert every maintainer DM into a doc improvement signal.

**Steelman of Variant 2:** V2 is right that "stale, contradictory documentation is worse than no documentation" — this is a sharp diagnosis my variant did not surface. RC-1 (stale `docs/developer-guide/` content) is a real, concrete, immediately actionable problem that I missed. V2's per-FR inline grep falsifications are also genuinely stronger discipline than my metrics-section approach — they make the work *verifiable* not just *measurable*. The Causes-vs-Symptoms table is a cognitive aid I should have included.

**Strengths I claim (with evidence):**

1. **Layered guide structure scales pedagogically.** A first-time contributor needs Setup (`01-setup.md`); a returning contributor needs Mental Model (`02-mental-model.md`); a maintainer needs Troubleshooting (`04-troubleshooting.md`). One consolidated file serves nobody well past the first read. (V1 FR-003 + FR-006)
2. **Audience tags + brevity caps are enforceable discipline.** `**Audience:** X | **Time:** Y | **Prereqs:** Z` + 400-line cap + `wc -l` check in `make onboard-check` prevents the docs from rotting into the same mess they replaced. (V1 FR-006 + NFR-001 + M-005)
3. **Two-click rule (FR-004) is the highest-leverage discoverability lever.** Every confusion point must be one paragraph, in one place, ≤2 clicks from README. This *prevents* the duplication and drift that creates stale docs in the first place. It's a structural solution to V2's RC-1, not a remediation.
4. **CI-bound happy-path verification (`make onboard-check` on PR to onboarding surface).** This is the doc-rot insurance V2 lacks. V2's `make onboard` is a contributor convenience; my `make onboard-check` is a maintainer guarantee.
5. **Doctor integration (FR-009)** turns recurring failure modes into programmatic checks rather than prose-only troubleshooting. Single source of truth for "is my env OK?"

**Weaknesses I identify in V2:**

1. **Single consolidated `docs/contributor-guide.md` is a maintenance liability.** Mixing setup, mental model, walkthrough, and FAQ in one file invites the same rot V2 just diagnosed in `docs/developer-guide/`. The fix to stale-doc problem is *not* to consolidate — it's to layer and version.
2. **`make onboard` exits 0 on success but says nothing about what to do next under failure cases.** V2's INT-2 lists steps but doesn't specify what the contributor reads when step (d) `make verify-sync` fails. My guide-based approach pre-locates that answer in `04-troubleshooting.md`.
3. **V2's CI story is implicit at best.** "Run on a fresh VM" (in §4) is not CI. My FR-005 specifies the actual CI trigger (PR touching onboarding surface).
4. **V2 inherits V1's blind spot via omission, not insight.** RC-1 is real, but V2 doesn't propose a structural fix that *prevents* the next stale-doc incident. It removes the current rot but adds no guardrail. My layered-with-cap discipline does.

**Concessions:**

- I concede V1 entirely missed the stale `docs/developer-guide/` problem. That is a serious gap and must be incorporated into any merged output (RC-1 should become a Step-0 cleanup in my Adoption Path Days 0–30).
- I concede V2's per-FR grep falsifications are stronger than my Success Metrics approach — they verify *each requirement* not just the aggregate.
- I concede V2's explicit baseline measurement plan is more rigorous than my implicit "compare against 30-day baseline."
- I concede the Open Assumptions section (V2 §7) surfaces risks (UV install friction, test-suite flakiness) that my Open Risks section glossed over.

---

### Variant 2 Advocate (sonnet:analyzer)

**Position Summary:** Variant 2 wins because it diagnoses *causes* before prescribing *interventions* and refuses to propose anything not tied to a named root cause. The highest-ROI fix is removing active misinformation (RC-1) — a step V1 silently skips. Falsifiability is not a metric; it must be embedded in every requirement so the work is verifiable on day 1, not measurable on day 90.

**Steelman of Variant 1:** V1 is right that documentation systems are themselves a structural intervention — the two-click rule (FR-004), single-paragraph-per-confusion-point discipline, and CI-enforced happy-path check are concrete *preventive* mechanisms that my variant lacks. Layered audience-tagged guides genuinely serve different reader profiles better than a single file. V1's NFR-007 (single-line command discipline tied to terminal-paste constraint) is a real operational concern grounded in user memory; I missed it. The maintainer-DM-as-doc-bug rule (V1 §7 residual) is one of the most powerful improvement loops in either variant.

**Strengths I claim (with evidence):**

1. **Causes-before-interventions is the only honest planning frame.** V1 proposes 8 artifacts without naming the friction each removes. My RC-1 through RC-4 force the question "is this intervention removing a *cause* or a *symptom*?" — and surfaced that V1's `docs/contributing/` proposal does not address the actively-misleading stale docs that any new contributor will hit first. (V2 §1 + Causes-vs-Symptoms table)
2. **RC-1 (stale docs) is documented evidence, not theoretical.** `docs/developer-guide/contributing-code.md` literally says `pip` and `python3 -m`. `docs/developer-guide/README.md` literally says "SuperClaude is NOT software." A contributor who reads these will fail and lose trust in *all* project docs — including the ones V1 wants to write. Removing this is a prerequisite, not a parallel task. (V2 FR-001 with grep falsification)
3. **Per-FR falsification (each FR ends with a grep/timing/observation test) is the difference between requirements and aspirations.** V1's metrics (M-001…M-006) measure outcomes; my falsifications verify the *work*. (V2 §3 + §4)
4. **Single consolidated guide reduces the cross-file drift surface.** V1's 4-file decomposition multiplies the maintenance contract by 4. For a solo maintainer optimizing for ≤30 min/quarter, fewer files with clearer scopes is the more honest choice. (V2 FR-002)
5. **Open Assumptions section names what could invalidate the plan.** UV install friction (A1), test-suite flakiness (A2), contributor-base assumptions (A3) — V1 omits these entirely. A spec that doesn't name its assumptions is a spec that will fail in ways its author didn't anticipate. (V2 §7)
6. **Explicit baseline measurement plan.** V1 references "30-day baseline" without specifying how it's captured. V2 §6 specifies the three numbers to record pre-merge, so the 90-day delta is actually measurable. (V2 §6 baseline)

**Weaknesses I identify in V1:**

1. **RC-1 omission is structural, not cosmetic.** V1 proposes new docs in `docs/contributing/` while leaving misleading docs in `docs/developer-guide/`. A first-time contributor who finds `docs/developer-guide/` first (it currently exists and is linked) will be misinformed *before* they encounter the new spine. This is the single highest-impact gap.
2. **Two-click rule (FR-004) is admirable but unverifiable.** "Two clicks from README" requires a graph traversal that no CI gate enforces. The rule rots silently. V2's per-FR grep falsifications are checkable in seconds.
3. **8 artifacts × maintenance contract = real overhead.** V1's NFR-003 promises ≤30 min/quarter, but Table 4 lists 8 artifacts each with their own "Maintenance Contract." That's a math problem V1 doesn't show its work on. My 4 interventions, 1 file, 1 Make target footprint is more honest.
4. **`make onboard-check` is the *wrong tool name* for the *wrong audience*.** A CI verification gate (V1) is a maintainer concern. A contributor needs a command they themselves run to confirm "did this work?" — that's what `make onboard` is for. V1 confuses CI verification with contributor experience.
5. **No explicit treatment of "what happens when `make test` is already broken."** My A2 (test suite assumption) names this; V1 ignores it. If `make onboard-check` fails because the suite is flaky, V1 has no recovery story.

**Concessions:**

- I concede the two-click rule (V1 FR-004) is genuinely better discoverability discipline than what V2 specified — it should be incorporated.
- I concede the 4-file layered structure has pedagogical value V2 dismissed; the right answer may be a hybrid (a single `docs/contributing/` directory, but layered audience-tagged docs within it).
- I concede V1's `make onboard-check` (CI gate) and my `make onboard` (contributor command) are not the same thing and *both* are needed. V2 should have proposed both targets.
- I concede V1's NFR-007 (single-line command discipline) is correct, evidence-based (user terminal constraint), and entirely missing from V2.
- I concede V1's maintainer-DM-as-doc-bug rule (§7 residual) is the single best improvement-loop mechanism in either variant.
- I concede `superclaude doctor` integration (V1 FR-009) is the right primitive — programmatic checks over prose troubleshooting.

---

## Per-Point Scoring Matrix

For each diff point, advocate concessions and evidence determine the per-point winner. "Hybrid" indicates both positions have merit and the refactor plan should incorporate elements from both.

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 (top-level organization) | Hybrid | 70% | V2's diagnosis-first framing is stronger reasoning; V1's section coverage is more complete. Merge both. |
| S-002 (opening framing) | V2 | 75% | Causes-before-interventions is the more honest planning posture. Both advocates conceded this implicitly. |
| S-003 (FR vs FR+NFR split) | V1 | 70% | V2 advocate conceded NFR layer adds value (NFR-007 single-line discipline). |
| S-004 (falsification surface) | V2 | 85% | Per-FR grep falsifications are objectively more verifiable than aggregate metrics; V1 advocate conceded explicitly. |
| C-001 (document layout) | Hybrid | 65% | V2 right that fewer files = less drift; V1 right that audience tags need layering. Merge: `docs/contributing/` directory with 4 audience-tagged guides (V1) BUT with explicit cross-file SoT to prevent duplication (V2 concern). |
| C-002 (make target name + semantics) | Hybrid | 80% | Both advocates conceded both targets are needed: `make onboard` (contributor-facing) AND `make onboard-check` (CI verification). |
| C-003 (stale docs) | V2 | 95% | V1 advocate fully conceded RC-1 was a serious gap; deletion of stale `docs/developer-guide/` content is non-optional. |
| C-004 (worked example specificity) | V2 | 70% | Named candidates ("python-expert agent description", "test_confidence.py assertion") are more useful than "typo fix in a SKILL.md" abstract category. |
| C-005 (audience targeting) | V1 | 80% | V2 advocate conceded audience tags add value the analyzer variant missed. |
| C-006 (rejected alternatives) | V1 | 65% | V1's §7 addresses every seed-brief open question explicitly; V2's §5 covers most but not all (no explicit "linear vs contextual" framing). |
| C-007 (baseline measurement) | V2 | 80% | Explicit baseline capture plan is objectively more rigorous; V1 advocate conceded. |
| X-001 (where the guide lives) | Hybrid | 60% | Soft contradiction; merge resolves by adopting `docs/contributing/` directory with multiple files (V1 structure) BUT cross-file SoT discipline (V2 spirit). |
| X-002 (Make target name) | Hybrid | 80% | Resolved by adopting both `make onboard` (contributor) AND `make onboard-check` (CI). No naming contradiction once both exist. |
| U-001 (two-click rule) | V1 | 90% | V2 advocate explicitly conceded. Adopt FR-004. |
| U-002 (doctor integration) | V1 | 85% | V2 advocate explicitly conceded. Adopt FR-009. |
| U-003 (single-line command discipline) | V1 | 95% | Evidence-based (user terminal constraint); V2 advocate fully conceded. Adopt NFR-007. |
| U-004 (DM-as-doc-bug rule) | V1 | 90% | V2 advocate called it "the single best improvement-loop mechanism." Adopt §7 residual rule. |
| U-005 (brevity caps as enforceable check) | V1 | 75% | `wc -l` gate is concrete. Adopt M-005. |
| U-006 (stale-doc diagnosis as RC-1) | V2 | 95% | Fully conceded by V1 advocate. Adopt as Step 0 of adoption path. |
| U-007 (Causes-vs-Symptoms table) | V2 | 80% | Conceded as cognitive aid V1 should have included. Adopt. |
| U-008 (per-FR inline falsification) | V2 | 90% | V1 advocate conceded "stronger discipline than metrics." Adopt as FR-level pattern. |
| U-009 (baseline measurement plan) | V2 | 80% | Conceded; adopt §6 baseline triplet. |
| U-010 (Open Assumptions section) | V2 | 80% | Conceded; adopt as §8 of merged spec. |
| A-001 (Makefile as primitive — UNSTATED) | Accept (both) | n/a | Both advocates affirm the assumption; no challenge. Surfaced for transparency. |
| A-002 (linear path sufficient — UNSTATED) | Accept (both) | n/a | Both advocates affirm; document explicitly in merged spec. |
| A-004 (README as discovery entry — UNSTATED) | Accept (both) | n/a | Both advocates affirm; document explicitly. |

## Convergence Assessment

- **Total diff points:** 16 (4 structural + 7 content + 2 contradictions + 3 promoted shared assumptions)
- **Agreed points (winner determined OR hybrid resolution accepted by both advocates):** all 16 (no irreconcilable conflicts)
  - V1 wins: 6 points (S-003, C-005, C-006, U-001 through U-005)
  - V2 wins: 7 points (S-002, S-004, C-003, C-004, C-007, U-006 through U-010)
  - Hybrid: 3 points (S-001, C-001, C-002 + X-001, X-002)
  - Shared-assumption accepts: 3 (A-001, A-002, A-004)
- **Convergence score:** 16 / 16 = **1.00** (100%)
- **Status:** CONVERGED (≥ 0.75 threshold)
- **Taxonomy coverage:** L1 ✓ L2 ✓ L3 ✓ (no forced round needed)
- **Invariant probe gate:** N/A (Round 2.5 skipped at quick depth)
- **Unresolved points:** none

The variants are strongly complementary rather than competitive: V1 is a documentation-systems specification and V2 is a root-cause-driven specification, and the strongest merged spec adopts the diagnosis framing from V2 with the documentation discipline from V1.
