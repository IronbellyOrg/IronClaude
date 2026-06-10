# Reflect Report — UC-1 Pre-Execution Coverage/Gap Audit

- **Mode**: pre (UC-1)
- **Tier reached**: 1 (rubric default-stop; no escalation rule fired)
- **Spec**: `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md`
- **Tasklist**: `.dev/tasks/to-do/TASK-RF-20260608-194013/TASK-RF-20260608-194013.md`
- **Calibrated confidence**: 0.89
- **coverage_pct**: 1.00 (21/21 FR+NFR mapped; 0 unmapped requirements)
- **Grounding**: spec + tasklist both read in full this turn. No code `file:line` citations requiring independent re-Read — the audit is tasklist-vs-spec coverage, and the live-`SKILL.md` anchors were independently re-verified by this task's own research-gate + completeness-gate (both PASS, per frontmatter `related_docs`).
- **Verdict**: **PROCEED.** Coverage is complete; 4 soft refinements below are quality nudges, not blockers.

---

## Coverage Summary

Every one of the 13 FRs and 8 NFRs maps to at least one concrete task step (full matrix:
`artifacts/coverage-map.yaml`). All major spec sections (§4 auto predicate, §5 knob map, §6
templates, §7 depth, §8 fallback, §9 V1–V16, §10 plumbing) and all six Open Questions are
covered. **No requirement is unmapped.**

| Bucket | Count | Notes |
|---|---|---|
| Covered (clean) | 17 | direct step mapping |
| Soft (covered-with-refinement) | 4 | FR-1, FR-12, NFR-4, §13 ATs |
| Gap (unmapped) | 0 | — |

This is a high-quality, well-grounded tasklist: drift-guard before edits (Step 1.1), byte-for-byte
reversibility with snapshot+diff (1.1/5.4), SoT discipline on every step, the INV-010 regex shape
explicitly preserved for TB-Add-9 (4.1), and adversarial PG-5 gates with `fix_authorization: true`
+ regression-then-monotonicity halt guards. The load-bearing OQ-1 inconsistency is correctly
identified, resolved (8-value union), and given an operator-HALT escape hatch.

---

## Findings (soft — refine, do not block)

### S1 — FR-1 unknown-token MALFORMED handling lives in the Input doc, not the A.9 producer [LOW]

FR-1 + AT-FR1 require `--reflect foo → MALFORMED-input STOP`. **Step 2.1** documents this in the
`--reflect` Input-doc bullet, and **V1** (Step 4.1) asserts the *BUILD_REQUEST field value* is in
the valid set. But **Step 2.4** — the A.9 *resolution producer* prose, where parse/resolution
actually happens — enumerates 6 sub-behaviors (precedence, §5 map, auto predicate, W probe, ladder,
advisory WARNING) and **none is "reject an unknown `--reflect`/`REFLECT_POST_MODE` token as a
MALFORMED-input STOP."** The input-validation path is therefore documented + output-asserted but not
authored into the producer logic itself.

- **Why it matters**: a reader of A.9 alone (the single producer per FR-9) would not see the
  invalid-token rejection branch; FR-1's STOP behavior is split across two surfaces.
- **Recommendation**: add a 7th bullet to Step 2.4: *"(7) unknown `--reflect`/`REFLECT_POST_MODE`
  token (∉ {none,0,1,2,auto}) → MALFORMED-input STOP per Critical Rule #12, before any §5/auto
  resolution."* Verifier: grep the edited A.9 prose for the unknown-token branch.

### S2 — FR-12 Mode-2 spec threading relies on a pre-existing frontmatter field, unasserted [LOW]

FR-12 threads `--spec` into Mode 1 inline *and* makes `spec_path` available to the Mode-2 wrapper via
frontmatter. **Step 3.2** Mode-2 template reads "`--spec` (from frontmatter `spec_path`)", and **V13**
asserts only the *Mode-1* `--spec {SPEC_PATH}` token. No step writes or asserts the `spec_path`
frontmatter field for the Mode-2 path — it depends on `:1933 spec_path:` pre-existing (re-verified in
Step 1.1).

- **Why it matters**: if the pre-existing `spec_path` frontmatter were ever absent/renamed, Mode-2
  spec threading would silently break with no V-assertion to catch it.
- **Recommendation**: in Step 5.3's self-consistency walkthrough, add assertion (e) — "Mode-2 template
  references frontmatter `spec_path` and that field exists in the Output-Structure frontmatter doc."
  No new code; one walkthrough line.

### S3 — §13 acceptance tests are mostly (c)-class unreachable; mechanical coverage is shallow [MEDIUM-INFO]

**Step 5.5** correctly does NOT fake a `build_tasklist()` entry point (none exists — research 06) and
tests only string/content-marker assertions (AT-VALIDATION-1, AT-MISMATCH-1, AT-MODE-MATCH,
AT-PLUMBING-1 + the 8-value token + `TB-Add-9` + `(29 items)` markers). The bulk of §13's behavioral
ATs (AT-FR1 retry, AT-FR5 auto determinism across implementers, AT-FR10 fallback, AT-WRAPPER-1 probe)
have **no automated surface** and are validated only by the PG-5 rf-qa adversarial gates.

- **Why it matters**: the central invariant ("emitted item == `reflect_post_mode`") is mechanically
  tested only as *marker presence*, not as *behavioral correctness*. Real assurance leans on PG5.1/PG5.2.
- **Recommendation**: this is acknowledged and correctly scoped — **no change required**. Just enter
  the run with the expectation that PG5.1/PG5.2 (not pytest) are the load-bearing correctness gate, and
  that Step 5.3 must explicitly tag each §13 AT as `tested` / `(c)-unreachable` so the gap is visible.

### S4 — NFR-4 extensibility is an emergent property with no discrete verification [INFO]

NFR-4 ("adding `--reflect 3` is one new row, never a 4th knob") is a structural-design claim. No step
verifies it directly; it falls out of the §4/§5/§6/§9 single-dial shape. **Acceptable** — PG5.2
(qualitative) is the natural place to confirm the dial is genuinely monotone-extensible. No change
required.

---

## Cross-checks that PASSED (high-value spot-verifications)

- **OQ-1 (7 vs 8 values) — verified against the spec directly.** §10.3 (`:848`) lists 7
  (`none|1|2|auto-resolved-1|auto-resolved-2|halt|2-degraded-halt`); §8.2 ladder row
  (`auto|2|false → auto-resolved-2-degraded-halt`), §9.1 V16, §9.2 active map, and §9.3 MODE-MATCH all
  require the 8th value. The task's 8-value-union resolution is the **only** internally-consistent
  oracle. Correctly load-bearing; correctly handled at Steps 3.1/4.1/5.3.
- **V15 byte-identity chain is sound.** §6.3.1 shows the current item title
  ("Independent post-execution **reflection** gate (**fresh session**, HALT)"); Step 1.1 snapshots it,
  Step 3.2 §6.4 reproduces verbatim, Step 5.4 diffs. The `2-degraded-halt` single-comment delta is
  consistent across spec §6.4 and Step 3.2.
- **Recursion handling (Phase 6) is correct.** This task edits the POST-gate machinery it is gated by;
  Phase 6 correctly uses the *current* (pre-refactor) manual fresh-session HALT item, with the right
  `--spec`/`--diff`/`--depth deep` and the `feedback_human_decision_items_must_halt` HALT.
- **FR-3 fix is real and located.** The known contradiction (Rule 19 "MUST NOT run reflect inline" vs
  Mode 1 which DOES) is explicitly reconciled at Step 3.5 by conditioning the prohibition on mode.

---

## Tier Decision (audit trail)

```yaml
selected_tier: 1
fired_rule_number: 8        # §5.3 default-stop
mode: pre
S_scope: ~20                # tasklist items
S_domains: 2                # skill/agent markdown + one pytest
S_dev_density: ~0.0         # 0 unmapped requirements
calibrated_confidence: 0.89
coverage_pct: 1.0
escalation_reason: "no rule 1–7 fired: not UC-2 (no regression/reuse-miss), domains<3, density<0.20, C>=0.85, no --depth deep / --tier 2"
```

## Recommendation

**Proceed to execution.** Optionally apply S1 (one bullet in Step 2.4) and S2 (one line in Step 5.3)
first — both are ~2-minute tasklist edits that close the only two split-surface coverage seams. S3/S4
are informational. No blocking gaps.
