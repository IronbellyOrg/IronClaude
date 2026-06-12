# Adversarial Debate Transcript

## Metadata

- Depth: standard (Round 1 parallel + Round 2 rebuttals + Round 2.5 invariant probe; no Round 3)
- Rounds completed: 2 + invariant probe
- Convergence achieved: 0.86 (after invariant-probe revision of consensus)
- Convergence threshold: 0.80
- Focus areas: All
- Advocate count: 3 (independent Task agents) + 1 fault-finder
- Topic: 3 competing fixes for the confirmed `superclaude prd run` document-step gate-failure bug

---

## Round 1: Advocate Statements (parallel, independent agents)

### Variant 1 Advocate — Solution 1 (Executor-side robust recovery)

- **Position**: S1 is the correct *hotfix* — single-function blast radius, zero agent-behavior change, cannot regress the 15-step capture path. Greens the capture failure (immediate cause) at least risk.
- **Steelman S2**: Attacks the root cause (prompt ambiguity); fixes both defects at source; reuses the proven `build_task_file` pinning idiom; makes S1's backstop strictly more effective.
- **Steelman S3**: Most architecturally correct; eliminates the failure *class* by retiring disk-path-matching as the capture channel; bundles structural cwd contamination prevention; feature-flagged.
- **Strengths**: (1) blast radius = 1 function; (2) zero agent-compliance dependency — "works even if agent ignores path"; (3) recovers the *already-reproduced* run (real 197-line doc in `.dev/specs/`); (4) generalizes the trusted `assembly` recovery pattern (executor.py:309-336); (5) no token-truncation cliff; (6) 4-6h ships today vs S3's 27h.
- **Critiques**: S2 is forward-only (can't recover the existing failed run); S2's load-bearing assumption is its own #1 HIGH risk; S3 blast radius disqualifying; S3 rests on unverified `result`-event contract; S3 cwd breaks codebase discovery.
- **Concessions**: (1) does NOT fix contamination, only recovers around it; (2) stale-file selection can pick a *wrong longer* doc (silent failure); (3) treats symptom not cause.
- **A-001**: QUALIFY (lean REJECT for STRICT gate) — sufficient for STANDARD (scope-discovery min_lines=50), conditionally sufficient for STRICT research-notes; *identical limitation across all three solutions*, not an S1-specific weakness.

### Variant 2 Advocate — Solution 2 (Prompt-side path pinning)

- **Position**: Fixes the bug at its origin (prompt's failure to say *where* to write); eliminates both filename and location mismatch in one stroke; stops `.dev/specs` contamination because output no longer lands in a WHERE-scoped source dir; composes with S1 as backstop (REPORT's recommendation).
- **Steelman S1**: Lowest-risk, fastest, zero compliance dependency, generalizes proven `assembly` recovery, near-zero regression surface — close to ideal as a backstop.
- **Steelman S3**: Only fix attacking the capture *channel*; only structural contamination prevention via cwd; correctly flagged + feature-flagged.
- **Strengths**: (1) fixes BOTH defects at source; (2) removes the ambiguity that *caused* deviation (no fuzzy-match over-matching risk); (3) consistent with the ~12 builders that already pin `Output path:` and don't exhibit the bug; (4) single source of truth + sync test; (5) lowest cost (~3h); (6) strictly improves S1's backstop (two-axis miss → one-axis miss).
- **Critiques**: S1 leaves contamination live + stale-file hazard + WHERE traversal surface; S3 widest blast radius (wrong for hotfix), unverified platform assumption, token-truncation can fail the gate it tries to fix.
- **Concessions**: (1) **retracts its own doc's "chroot/not-cross-platform" mislabel of S3** — S3 is stdout/result-capture + cwd, fully cross-platform; (2) depends on agent compliance (its #1 HIGH risk) — mitigated by the empirical fact that already-pinned steps don't break + S1 backstop + optional fail-fast assertion; (3) changes nothing about document *content*.
- **A-001**: QUALIFY — FALSE as stated for STRICT gate, but identical across all three; capture is necessary + likely-sufficient-in-practice (reproduction shows content wasn't the problem) but not provably sufficient. Residual belongs in the prompt's section/frontmatter contract.

### Variant 3 Advocate — Solution 3 (Stdout/result-contract capture + cwd isolation)

- **Position**: Only proposal that prevents `.dev/specs` contamination *structurally* (cwd=task_dir removes the writable source dir from the agent's default write surface). **But** for a reproduced production-blocker, the win condition is "greens the gate at lowest risk + fastest," not "most architecturally correct" — so S3's HIGH blast radius + UNVERIFIED core mechanism disqualify it as the *first* landing. Honest recommendation: ship Sol 2+1 now; land S3's cwd half as immediate follow-up.
- **Steelman S1**: Lowest-risk, attacks the exact reproduced failure, generalizes proven `assembly` recovery, zero compliance dependency — near-ideal backstop.
- **Steelman S2**: Only fix addressing the REPORT's stated root cause (prompt ambiguity); extends the established pinning idiom; fixes capture + contamination at source; ~3h, no token risk, no CLI assumptions.
- **Strengths**: (1) **structural (non-instruction) contamination prevention** — its unique decisive contribution; (2) fixes the capture *channel* not the filename lottery; (3) the design REPORT calls "most architecturally correct"; (4) backward-compatible fallback + `capture_mode` rollback lever.
- **Critiques**: S1 institutionalizes contamination (makes the pipeline *depend* on reading the agent's pollution); S1 stale-file → silent wrong doc; S2 depends on agent compliance; neither S1 nor S2 closes contamination structurally.
- **Concessions**: (1) **core mechanism UNVERIFIED — grep-confirmed zero `result`-event handling exists in source**; betting a hotfix on an unverified upstream contract is disqualifying; (2) blast radius HIGH (all 15 steps incl. parse-request JSON + 800-line assembly); (3) token truncation real + unmitigated at edges; (4) **retracts its own doc's "tool-interception" mislabel of S2** — S2 is prompt pinning, ~3h, additive, fully backward-compatible.
- **A-001**: QUALIFY (lean REJECT for research-notes) — gate is min_lines + semantic checks, not just lines; capture greens IFF the doc has frontmatter+sections; identical across all three; S3 on its own is *least* likely to satisfy the semantic gate since it touches no prompt content.

---

## Round 2: Rebuttals (synthesized — advocates pre-addressed each other in R1)

All three advocates independently converged, even while advocating their own side. The rebuttal exchange resolved to:

1. **On "which is the hotfix"**: Unanimous (3/3, including S3's own advocate) — **Solution 2 + Solution 1 as the hotfix**, Solution 3 deferred. S3's advocate explicitly conceded S3 should not be the first landing.
2. **On contamination**: Agreement that S1 alone leaves it live; S2 prevents it via instruction (task_dir is outside WHERE); S3's cwd is the only *structural* prevention — but its value vs risk became the central unresolved question handed to the invariant probe.
3. **On the two mislabels (X-001, X-002)**: Both retracted by their own advocates. Resolved — all three solutions correctly characterized: S1=executor recovery, S2=prompt pinning, S3=stdout/result-capture+cwd.
4. **On A-001**: Unanimous QUALIFY→REJECT-for-STRICT, agreed to be non-discriminating (identical across all three). Handed to the invariant probe for sufficiency enumeration.
5. **Corroborated finding**: Two independent advocates grep-verified that **zero `result`-event handling exists in the codebase**, independently confirming S3's capture mechanism is unimplemented + unverified.

---

## Round 2.5: Invariant Probe

See `invariant-probe.md`. 11 findings (3 HIGH, 5 MEDIUM, 3 LOW). The probe *overturned two pieces of the naive consensus*:

- **INV-001 (HIGH)**: the planned frontmatter prompt-edit is redundant (prompt already emits it) AND the PRD gate never checks frontmatter → DROP it.
- **INV-011 + INV-003 (HIGH/MED)**: cwd=task_dir breaks scope-discovery/investigation codebase reads → can *cause* the research-notes gate to fail → DEMOTE cwd out of the hotfix.
- **INV-002 (HIGH)**: capture-fix ≠ content-completeness → SCOPE the claim to "gate evaluates the real doc."
- **INV-006/INV-005**: adopt S1's explicit `_pick_best_candidate` (current source is "largest wins"); bound WHERE-broadening + add symlink containment (reverses an existing anti-widening guard otherwise).

---

## Scoring Matrix (per diff point)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| C-001 (where the fix lives) | S2 (producer-side) + S1 (consumer backstop) | 82% | At-source removal of ambiguity + recovery backstop; unanimous advocate consensus |
| C-002 (capture mechanism) | S2 (pin) + S1 (find) over S3 (result event) | 85% | S3's result-event channel grep-confirmed absent + unverified (INV-008) |
| C-003 (timing) | S2 (at source) | 78% | Root-cause framing; S1 after-the-fact is the backstop layer |
| C-004 (contamination) | S2 (pin to task_dir) | 70% | S3 cwd is the only *structural* fix but INV-011 shows it breaks reads → deferred; S2's task_dir pinning prevents it without that risk |
| C-005 (blast radius) | S1 (1 fn) / S2 (prompts) over S3 | 95% | S3 self-rates CRITICAL; REPORT agrees "follow-up not hotfix" |
| C-006 (effort) | S2 (~3h) | 88% | Lowest cost; S3 ~27h |
| X-001 (S2 mislabels S3 as chroot) | Corrected | 100% | Retracted by S2 advocate |
| X-002 (S3 mislabels S2 as tool-interception) | Corrected | 100% | Retracted by S3 advocate |
| X-003 (compliance vs root-cause) | Split→resolved: pin (S2) + backstop (S1) | 80% | Compliance risk real but backstopped; structural cwd alternative carries higher risk (INV-011) |
| U-001 (S1 tiebreak) | Incorporate (with fix) | 90% | Must replace current "largest wins" (INV-006) |
| U-002 (S1 traversal guard) | Incorporate (strengthen) | 85% | Add symlink containment (INV-005) |
| U-003 (S2 single-source-of-truth) | Incorporate | 88% | Sync test prevents drift |
| U-004 (S3 cwd isolation) | Defer (scoped follow-up) | 75% | INV-011: needs repo-root injection for reads first |
| U-005 (S3 truncation detection) | Incorporate (cheap) | 80% | Low-cost guard, harmless |
| U-006 (S3 capture_mode flag) | Defer with result-event work | 82% | Flag tied to the deferred capture half |
| A-001 (sufficiency) | Scoped (claim narrowed) | 80% | INV-002: fix delivers real doc; content quality is the gate's correct concern |

---

## Convergence Assessment

- Points resolved: 14 of 16 (the 2 mislabels resolved by retraction; cwd role resolved by invariant probe; A-001 resolved by scoping)
- Alignment: **0.86** (≥ 0.80 threshold)
- Taxonomy coverage: L1 ✅ (S-001, C-006), L2 ✅ (C-001, C-005, U-003), L3 ✅ (C-002, C-004, X-003, A-001, U-001, U-004) — all three levels covered
- Invariant gate: 3 HIGH UNADDRESSED at probe time → **resolved by merge revision** (drop item 5, demote cwd, scope claim) → 0 HIGH UNADDRESSED in final design
- **Status: CONVERGED** (after invariant-probe revision)
- Unresolved points: none blocking; 2 items explicitly DEFERRED by design decision (S3 cwd-isolation done safely; S3 result-event capture pending CLI verification)
