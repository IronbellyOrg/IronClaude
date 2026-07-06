# QA Report — Synthesis Gate

**Phase:** synthesis-gate
**Timestamp:** 2026-06-12T12:20Z
**Synthesis dir:** `.../prd-pr-auto-remediation-v2-0/synthesis`
**Research dir:** `.../prd-pr-auto-remediation-v2-0/research`
**Fix authorization:** true
**Verdict:** **PASS**
**EXIT_RECOMMENDATION:** **CONTINUE** (assembly-ready)

---

## Verdict Summary

All **9 of 9** synthesis files are present, fully populated (PRD §1–28), and **assembly-grade**.
This is an independent re-verification pass. The synthesis files are unchanged since the prior gate
(last mtimes 13:00–16:16 on 2026-06-11; prior report 16:14Z). I re-ran the table-parity sweep,
re-checked every load-bearing code anchor against the live working tree, and re-traced a sample of
distinctive claims to `research/`. **No new defects were found**; the two table-structure fixes from
the prior run remain in place and verified.

| File | Sections | Result |
|------|----------|--------|
| `synth-01-exec-problem-vision.md` | §1–4 | ✅ PASS |
| `synth-02-business-market.md` | §5–8 | ✅ PASS |
| `synth-03-competitive-scope.md` | §9–12 | ✅ PASS |
| `synth-04-stories-requirements.md` | §13, §21.1, §21.2 | ✅ PASS |
| `synth-05-technical-stack.md` | §14–15 | ✅ PASS |
| `synth-06-ux-legal-business.md` | §16–18 | ✅ PASS |
| `synth-07-metrics-risk-impl.md` | §19, §20, §21.3–21.5 | ✅ PASS |
| `synth-08-journey-design-api.md` | §22–25 | ✅ PASS |
| `synth-09-resources-maintenance.md` | §26–28 | ✅ PASS |

Full section coverage §1–28 with no gaps or duplicates. Feature-PRD adaptations (N/A
accessibility/localization/pricing; reframed §18 monetization; §24 adapted to the CLI/conversational
surface) are each justified by an explicit SCOPE NOTE.

---

## Independent Re-Verification

### Table column structure (item 2) — CLEAN

Automated unescaped-pipe parity sweep over all 9 files, per contiguous table block (header /
separator / body rows must share the same unescaped-pipe count, with `\|` correctly excluded):
**ALL TABLE BLOCKS ALIGNED — 0 mismatches.** The two prior-run fixes hold:

- `synth-06` §16.2 "Core User Flows" — 4-cell `Source` header column present and aligned.
- `synth-07` §20.1 risk table — `` (`flock … \|\| true`) `` pipes escaped; row parses as 5 cells.

### Live code anchors (items 4, 12) — VERIFIED against the working tree

| Claim (as cited in synth) | Live result | Verdict |
|---|---|---|
| `class ClaudeProcess` @ `process.py:72` | line 72 | ✅ |
| `--dangerously-skip-permissions` default @ `:93`; `timeout_seconds=6300` @ `:94` | confirmed | ✅ |
| `build_env()` additive `os.environ.copy()` @ `:145`/`:155`, `env.update` @ `:159` | confirmed | ✅ |
| `PROMPT_MAX_BYTES` @ `:56`; `PromptTooLargeForArgv` @ `:61`; pre-spawn raise @ `:169` | confirmed | ✅ |
| `build_command()` @ `:121`; `os.setpgrp` @ `:189`; `os.killpg` @ `:291`/`:304`; 64 KiB chunk @ `:219` | confirmed | ✅ |
| `DEFAULT_MAX_ROUNDS=2` / `HARD_CAP_MAX_ROUNDS=5` / `MIN_POLL_INTERVAL=30` @ `fsm.py:30–32` | confirmed | ✅ |
| `evaluate_push_decision` @ `fsm.py:145`; `should_halt_rounds` @ `:135` | confirmed | ✅ (drift note) |
| `needs_human_decision` has **no Python setter** | `grep '… = True'` → 0 | ✅ still true |
| **No Python `gh` caller** in `src/` | 0 subprocess gh callers | ✅ still true |
| `cli/remediate/` absent (greenfield) | absent | ✅ |
| top-level `remediation/` present & empty (stale placeholder) | empty | ✅ |
| `severity-rubric.md` + auggie `SKILL.md` paths | exist | ✅ |

**Line-drift note (advisory, non-blocking):** the in-flight, **git-untracked** V1 `pr_submit/`
build is still moving, so two `fsm.py` line cites in `synth-08` have drifted by ~6 lines
(`should_halt_rounds` cited `:129` → now `:135`; `evaluate_push_decision` `:141` → now `:145`).
**Function names, file paths, and constants are all correct.** Every synth file carries a standing
"re-verify `file:line` before relying" caveat (`synth-09` §26.2/§28.3), and the PRD explicitly
defers exact-line re-locking to TDD/build. Not corrected here — pinning lines now against a moving
untracked tree would simply drift again, and would risk churn for zero PRD-level accuracy gain.

### Fabrication sampling (item 3) — 0 unsourced claims

Distinctive market/security claims traced to `research/`: GitHub Community **#190027** (web-01),
**"Comment and Control"** (web-01/02), **"Clinejection"** (web-01), **Greptile 82%** bug-catch
(web-02/03), **84% adoption** (web-01/02), CSA "reasoning layer / credential-holding execution
layer" separation (web-01). All `[CODE-VERIFIED]` tags trace to live source confirmed above. No
fabricated or unsourced claims found.

### User stories & prioritization (items 5, 6)

- **30/30** `US-` stories in `synth-04` each carry the full **As a / I want / So that** triplet
  (30 / 30 / 30) plus Acceptance Criteria and Success Metrics (US-1.1 … US-7.4 across 7 epics).
- **MoSCoW** prioritization in §21.2.1 (P0/P1); **RICE** matrix in §21.2.2 with the formula
  `(Reach × Impact × Confidence) / Effort` stated and applied per feature.

---

## 12-Item Checklist — All 9 Files

| # | Checklist item | Result | Notes |
|---|----------------|--------|-------|
| 1 | Section headers match PRD template | ✅ PASS | §1–28 present, correctly numbered across the 9 partitions; feature-PRD N/A sections each justified by a SCOPE NOTE. |
| 2 | Table column structures correct | ✅ PASS | Independent parity sweep: all 9 files aligned, 0 mismatches; prior 2 fixes (synth-06 §16.2 header, synth-07 §20.1 escaped `\|\|`) hold. |
| 3 | No fabrication | ✅ PASS | 6+ distinctive claims re-traced to web-01..03; code anchors re-verified live; only inaccuracy is advisory line-drift, not fabrication. |
| 4 | Evidence citations use actual file paths | ✅ PASS | All cited in-repo paths exist; function/constant names correct; minor `fsm.py` line drift inside the synth's own re-verify caveat. |
| 5 | User stories As-a / I-want / So-that | ✅ PASS | synth-04: 30/30 stories carry the full triplet + AC + success metrics. |
| 6 | Requirements use RICE / MoSCoW | ✅ PASS | §21.2.1 MoSCoW; §21.2.2 RICE with formula stated and applied. |
| 7 | Cross-section consistency | ✅ PASS | Lattice `propose<patch<fix<push<resolve`, budget default 2/cap 5, poll floor ≥30s, AC-1/3/4/7, 5-predicate push conjunction, 16 MiB guard, KPIs→§19 forward-refs all uniform across files. |
| 8 | No doc-only claims in feature inventories | ✅ PASS | Reuse anchors `[CODE-VERIFIED]`; greenfield `[NEW]`/`[SPEC]`; prose-only `--repo` rule flagged as not-yet-code-enforced. |
| 9 | Stale docs surfaced | ✅ PASS | swarm `:2269` mis-cite, `.aienv` 644-not-600, `os.rename`→`os.replace`, and the untracked in-flight V1 build all surfaced in Open Questions / Risk / §28.3. |
| 10 | Content rules compliance | ✅ PASS | Greenfield-vs-verified discipline throughout; sources named (CSA/JHU/OWASP/Mordor/Anthropic); no UV/SoT/fork-target rule violations. |
| 11 | All expected sections have content | ✅ PASS | §1–28 populated; only legitimate TBDs (unassigned human owners §26/§28; un-kicked-off calendar dates §21.5); all "placeholder" hits describe the real empty `remediation/` dir. |
| 12 | No hallucinated file paths | ✅ PASS | Every cited path exists; the only "absent" path (`cli/remediate/`) is correctly asserted greenfield; `remediation/` confirmed empty. |

---

## Bottom Line

- **9 of 9** synthesis files present and assembly-grade; §1–28 fully populated.
- **0 new defects** this pass; independent table-parity sweep reports all 9 files aligned, and the
  two prior table fixes remain in place.
- Code anchors, story format (30/30 triplets), MoSCoW + RICE, and cross-section invariants all
  re-verified.
- One advisory: minor `fsm.py` line-number drift from the moving untracked V1 build — documented
  within the synth's own "re-verify `file:line`" caveat; not corrected to avoid churn.

**VERDICT: PASS**
**EXIT_RECOMMENDATION: CONTINUE** (assembly may proceed)

> **Carry-forward for assembly / TDD:** the in-flight `pr_submit/` + `sc-pr-submit-protocol/` V1
> build is **git-untracked** and still moving (`fsm.py` lines shifted ~6 between synthesis and now).
> Re-lock every `file:line` anchor at build time before `cli/remediate/` imports/cribs from it, and
> coordinate so V2 does not fork a divergent decision core.
