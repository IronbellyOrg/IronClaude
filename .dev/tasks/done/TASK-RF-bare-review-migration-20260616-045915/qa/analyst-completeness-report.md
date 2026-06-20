# Research Completeness Verification — sc-bare-review M8/M9 Migration

**Topic:** Corrective MDTM tasklist to complete sc-bare-review M8/M9 migration (thin-caller rewrite, end-to-end parity gate, retire legacy scripts, 6 OPS docs, supersede false cp1/cp2)
**Lens:** completeness (BREADTH — verify every area needed to author the tasklist has research coverage)
**Date:** 2026-06-16
**Files assigned:** 5
- 01-skill-and-scripts-inventory.md
- 02-swarm-cli-thin-caller-surface.md
- 03-parity-test-and-swarm-test-conventions.md
- 04-docs-and-release-notes-staleness.md
- 05-mdtm-template-and-sync-discipline.md

---

## Verdict: PASS (see VERDICT section at end)

---

## Lens-Focus Checklist (9 items)

### 1. SKILL.md rewrite scope (keep/drop) covered? — PASS

**Evidence:** File 01 (`01-skill-and-scripts-inventory.md`) §1.1–§1.11 gives a region-by-region
KEEP/DROP map of all 231 SKILL.md lines, culminating in the quantified disposition table (01:101-114)
and the explicit net statement: "the ~62-line Behavioral Protocol (Waves A→E … incl. the AC-1.5
single-message assertion and 3 script invocations) is the migration-relevant deletion. Everything
else … is boilerplate-to-preserve" (01:114). The preserved external contract is enumerated
(flag surface §3.2, Return Contract §3.3, Failure Modes §8, Boundaries §3.4, ACs §9.1) at 01:195.
Per-line dispositions cite exact ranges (frontmatter 1-6, Behavioral Protocol 72-133, Return
Contract 135-160, etc.). A builder can write per-region checklist items directly from this.

**Granularity:** Sufficient — each KEEP/DROP region has a line range and a disposition verb.

### 2. swarm CLI thin-caller surface + flag mapping + blockers covered? — PASS

**Evidence:** File 02 (`02-swarm-cli-thin-caller-surface.md`) §1 enumerates the COMPLETE `run_cmd`
option set (9 options + 1 positional) with `commands.py` line evidence (02:42-53) and the legacy
`t2_preflight.sh` flag surface (02:64-71), then a direct legacy→swarm mapping table (02:75-82).
Two DIRECT mappings (`--target`, `--output`) and four BLOCKERS (B-1 `--reviewers`, B-2
`--target-line-cap`, B-3 `--timeout-sec`, B-4 `--label`) each carry a code anchor and a remediation
note (02:230-241). Negative grep evidence confirms the missing flags (02:57). The lens entry (§2)
and recipe (§3) are confirmed correct/complete. This is more than sufficient for per-flag checklist
items.

### 3. parity test rebuild design (golden baseline) covered? — PASS

**Evidence:** File 03 (`03-parity-test-and-swarm-test-conventions.md`) §1 documents what the current
`test_bare_review_parity.py` compares (library-vs-library, self-admitted at 03:38-51), §2 gives the
reusable CliRunner e2e pattern (`test_e2e_user_guide.py:68-70`, 03:88-97), §3 covers `--transport stub`
determinism, and §4 is a full FROZEN-GOLDEN design: capture legacy golden before deletion (03:144-150),
golden fixture layout (03:155-168), deterministic `generated` wiring (03:170-174), sequencing (03:176-180),
regen procedure (03:182-184), and the 5 invariants the permanent gate asserts (03:186-194). Design is
concrete enough to author test-build items.

### 4. OPS docs reconciliation (net-new vs relocate) covered? — PASS

**Evidence:** File 04 (`04-docs-and-release-notes-staleness.md`) §0 maps OPS-001..006 → roadmap rows
R-150..155 → required paths (04:22-29), §1 inventories existing `docs/swarm/` and identifies the two
naming-collision overlaps (`runbook.md` vs `operator-runbook.md`; `monitoring-patterns.md` vs
`observability-procedure.md`), §3 establishes OPS-005 is already satisfied by the pre-existing
`docs/dev/lens-contribution-policy.md` (515 lines, C1-C5 mapped 1:1), and §4 is a per-OPS-doc
classification table (NET-NEW / EXTEND / RELOCATE) with target path + rationale (04:126-133). Plus the
two missing checkpoints. This directly supports per-deliverable items.

### 5. MDTM template rules + sync discipline covered? — PASS

**Evidence:** File 05 (`05-mdtm-template-and-sync-discipline.md`) §1 extracts template-02 mandatory rules
with line cites (frontmatter §1.1, A3 granularity §1.2, B2 six self-contained elements §1.4, D3 no-items-
before-Phase-1 §1.6, E1/E2 flat-box rules §1.7, F1/F2 execution §1.8, I18 testing requirement §1.9, L1-L7
handoff patterns §1.10, M3 lens-QA gate §1.11, Execution Context block §1.12). §2 covers both pre-commit
hooks (AC11 block-claude-mirrors + MIG-001 verify-bare-review-sync) and the mandatory
`make sync-dev && make verify-sync` completion step with the `.claude/` staging prohibition. §3 supplies the
prior phase-8 structural model AND the failure-mode lesson (tasks marked done without on-disk deliverable).
§4 supplies STRICT gate commands with the `make lint`-is-red caveat. Comprehensive.

### 6. Granularity sufficient for per-deliverable checklist items? — PASS

**Evidence:** Every deliverable in scope has at least one item-authorable anchor:
- SKILL.md rewrite → 01:101-114 disposition table + preserved-contract list 01:195.
- Each `scripts/*.sh` deletion → individually named (01:0 inventory; 05 §3.1 L5 conditional-delete pattern).
- Parity gate → 03 §4 design + 5 named invariants.
- Each OPS doc → 04:126-133 per-doc path + classification.
- The 4 CLI blockers → 02:230-241 each with code anchor + remediation.
Files 01, 02, 04 explicitly frame their output "for the builder" with per-item dispositions.

### 7. Doc-sourced claims tagged CODE-VERIFIED/CONTRADICTED/UNVERIFIED? — PASS (file 04); N/A-but-evidenced (01,02,03,05)

**Evidence:** File 04 declares the tag legend (04:8) and applies tags throughout: the load-bearing
`[CODE-CONTRADICTED]` thin-caller claim in `release-notes-v1.md:16-26` (04:75-94, with three concrete
disproofs: SKILL.md=231 lines, scripts still present, conditional escape clause), plus `[CODE-VERIFIED]`
on OPS-ID mappings, lens-policy coverage, and parent-spec IDs. Files 01/02/03/05 are code-inventory
(not doc-sourced) research — every claim carries `file:line` evidence rather than a doc-staleness tag,
which is the correct discipline for those lenses. No untagged doc-sourced architectural claim was found.

**One CRITICAL-flag note (positive):** the single `[CODE-CONTRADICTED]` claim (the false "is now a
~60-line thin caller" release note) is correctly surfaced as a reconciliation requirement in WS-D
(04:94, 04:154), NOT reported as current fact. This is the desired handling.

### 8. Cross-stream dependency (inline-run-path CLI gap B-5) surfaced as a blocking prerequisite? — PASS (STRONG)

**Evidence:** B-5 is surfaced with maximum prominence and is corroborated across TWO independent files:
- File 02 labels it "B-5 (PIPELINE, HEADLINE)" in the TL;DR (02:13-32) and the net-findings (02:243-248):
  the inline `run_cmd` path calls only `dispatch_wave1` with `prompt=""`, never `normalize_wave2` /
  `reduce_wave3` / `emit_contract`, so `swarm run --lens bare-review` produces NO `merged.md`,
  NO `return-contract.yaml`, NO normalized bodies. The recipe "exists but is never invoked on the inline
  path." Grep evidence at 02:208-212; resume-path contrast at 02:219-224.
- File 03 independently re-derives the SAME blocker as its "⚠️ BLOCKER" §3.3 (03:124-134) and "HARD
  BLOCKER" summary (03:202), pinned by `test_e2e_user_guide.py:104-114`, and explicitly states the CLI
  golden gate is "dependent on R2/M5 landing normalize+reduce on the fresh path."

**Cross-validation:** The two files independently converge on the same root cause with the same code
anchors (commands.py:1554-1577 stub; resume path 1930-1977). This is the strongest possible signal for
the builder to sequence B-5 (M5 inline-pipeline wiring) as a BLOCKING PREREQUISITE before WS-A SKILL.md
thin-caller rewrite and before the WS-C parity gate. The dependency is unambiguous.

### 9. Unresolved ambiguities documented? — PASS

**Evidence:** Open decision-hinges are explicitly flagged for the builder rather than silently resolved:
- 01:169 — whether the swarm lens reads prompts from `refs/prompts.md` or carries its own copy (parity
  risk if duplicated); 01:199 reiterates "must verify the swarm lens carries identical prompt text."
- 01:173 — disposition of overlapping `output-template.md` vs `bare-review-output.md` (cross-link vs delete).
- 04:120 — OPS-005 decision hinge: cross-reference (if inbound links exist) vs relocate (if none).
- 02:84-87 — the spec-file escape hatch "defeats the thin-caller model," framing why B-1..B-4 need real CLI flags.
- 03:176-180 — the parity gate's hard sequencing dependency on M5 (3 options a/b/c, with c explicitly
  flagged as regressing to the flaw being fixed).
- 04:131 / 05 §3.2 — OPS-004 tabletop rehearsal is a HALT/human-sign-off item, not auto-stampable.

These are documented as builder decisions with the deciding criterion, which is the correct disposition.

---

## File Completeness Table

| File | Status header | Summary section | Gaps/ambiguities surfaced | Evidence discipline | Rating |
|------|---------------|-----------------|---------------------------|---------------------|--------|
| 01-skill-and-scripts-inventory.md | Complete (top & bottom) | §4 "R1 summary for the builder" | Yes (01:169,173,199) | file:line throughout | Complete |
| 02-swarm-cli-thin-caller-surface.md | Complete | TL;DR + "Net findings" | Yes (B-1..B-5) | file:line throughout | Complete |
| 03-parity-test-and-swarm-test-conventions.md | **In Progress (top, L3) / Complete (bottom, L205)** | "Summary for the tasklist author" | Yes (§4.5, HARD BLOCKER) | file:line throughout | Complete-content; header mismatch (MINOR) |
| 04-docs-and-release-notes-staleness.md | Complete | "Summary for the tasklist author" | Yes (§3,§4 decision hinges) | file:line + CODE-* tags | Complete |
| 05-mdtm-template-and-sync-discipline.md | Complete | "Summary for the builder" | Yes (§3.2 failure-mode lesson) | file:line throughout | Complete |

## Cross-File Consistency / Contradictions

No substantive contradictions found across the five files. Convergences (mutually reinforcing, not
conflicting):
- The "SKILL.md is 231 lines, not ~60; scripts still present" fact is independently asserted by 01:16,
  04:88-89, and 05:302-308 with consistent figures. Agreement.
- The B-5 inline-pipeline gap is independently derived by file 02 (§4/B-5) and file 03 (§3.3) with
  identical code anchors (commands.py:1554-1577 stub vs 1930-1977 resume). Agreement.
- The T08.07-after-T08.11 destructive-deletion ordering is cited by both 03 (§4.5 sequencing) and
  05 (§3.1, L5 conditional-action). Agreement.
- File 04 explicitly defers SKILL.md size/structure authority to R1 (04:96) — correct cross-reference
  hygiene, no overlap conflict.

## Compiled Gaps

### Critical Gaps (block tasklist authoring)
- **NONE.** All nine lens-focus areas have sufficient, evidence-backed coverage at item-authorable
  granularity. The single biggest cross-stream risk (B-5) is surfaced redundantly and clearly enough
  that the builder will sequence it as a blocking prerequisite.

### Important Gaps (affect quality)
- **NONE that block.** Note for the builder (not a research gap): the B-5 prerequisite means WS-A
  (SKILL.md thin-caller) and WS-C (parity gate) both depend on M5 inline-pipeline wiring landing first.
  This is correctly identified by the research; the builder must encode it as a `depends_on` / L5
  conditional ordering. Flagged here so it is not lost.

### Minor Gaps (must still be fixed)
- **File 03 status-header mismatch:** top-of-file declares `**Status: In Progress**` (03:3) while
  bottom declares `**Status: Complete**` (03:205). Content is complete and the bottom marker is
  authoritative, but the stale top marker should be corrected to avoid a downstream gate
  mis-reading the file as unfinished. Cosmetic; does not affect coverage.

## Depth Assessment

**Expected depth:** Deep (corrective-tasklist research must trace data flow + integration points +
exact code/line anchors so per-deliverable items can be authored without re-investigation).

**Actual depth achieved:** Deep. Every file carries `file:line` evidence; file 02 traces the full
`run_cmd` execution path step-by-step (02:163-186); file 03 traces the normalize/reduce seam to the
on-disk write (`normalize.py:482-483`); file 05 traces both pre-commit hooks to their script bodies
and the Makefile sync/verify targets. Integration-point mapping (inline vs resume pipeline divergence)
is the headline finding and is fully traced.

**Missing depth elements:** None material.

---

## VERDICT: PASS

All 9 lens-focus areas PASS with evidence. Research coverage is sufficient (BREADTH) for a builder to
author the corrective MDTM tasklist with per-deliverable, self-contained checklist items across all five
workstreams (SKILL.md thin-caller rewrite, swarm CLI flag/pipeline blockers, parity-gate rebuild, OPS
docs reconciliation, MDTM/sync discipline). No critical or important gaps block authoring.

**Gap list (non-blocking):**
1. MINOR — File 03 (`03-parity-test-and-swarm-test-conventions.md`) status-header mismatch: `In Progress`
   at L3 vs `Complete` at L205. Correct the L3 marker.
2. BUILDER-NOTE (not a research gap) — Sequence B-5 (M5 inline-pipeline wiring: dispatch with real
   prompt+worker_spec, then normalize_wave2 → reduce_wave3 → emit_contract) as a BLOCKING PREREQUISITE;
   both WS-A (SKILL.md thin-caller) and WS-C (CLI parity golden gate) depend on it. Encode as
   `depends_on` + L5 conditional ordering.

**Verdict: PASS.**
