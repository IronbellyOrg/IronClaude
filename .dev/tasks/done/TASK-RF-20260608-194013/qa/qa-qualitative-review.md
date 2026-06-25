# QA Report — Task File Qualitative Review (task-qualitative)

**Topic:** task-builder `--reflect <none|0|1|2|auto>` POST-gate dial — collapse 3 knobs into 1 dial (SKILL.md + rf-qa.md)
**Date:** 2026-06-09
**Phase:** task-qualitative
**Fix cycle:** N/A (first pass)
**Stance:** ADVERSARIAL, falsification-first. `fix_authorization: true`.
**Task under test:** `.dev/tasks/to-do/TASK-RF-20260608-194013/TASK-RF-20260608-194013.md`
**Driving spec (GOAL):** `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md` (986 lines, read in full)

---

## Overall Verdict: PASS

## Drift baseline (AX-1) — GOAL captured verbatim

> **TRACK GOAL (verbatim, from spec thesis §0/§2/§5/§9 + spawn prompt):** refactor the
> task-builder POST reflect gate into a single `--reflect <none|0|1|2|auto>` dial (default 2)
> subsuming `POST_REFLECT_GATE` + `POST_REFLECT_MODE` as deprecated read-time aliases, a single
> producer at A.9, per-mode emitted-item templates, byte-for-byte `halt` reversibility
> (`SKILL.md:1994-1999`), and a V1–V16 / MODE-MATCH rf-qa gate keyed on the single oracle
> `reflect_post_mode`. SCOPE = exactly 2 files (SKILL.md + rf-qa.md); does NOT build the wrapper,
> does NOT touch the PRE gate (A.10.7).

AX-1 **ACTIVE** for this review (GOAL verbatim available). Drift hunting applied to every cited
fact (file path, line number, signature, count, predicate) against live source.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (Step 1.1 anchor re-verify, Step 5.1 sync, 5.5 pytest) | none | PASS | `git rev-parse HEAD`, `make sync-dev` (Makefile:109), `make verify-sync` (Makefile:166) all real. `uv run pytest tests/skills/test_reflect_mode_validation.py` targets a NEW file (Step 5.5 self-declares creation). All preconditions satisfiable at current repo state. |
| 2 | Project convention compliance (SoT: edit `src/`, never `.claude/`) | none | PASS | Every edit step targets `src/superclaude/skills/task-builder/SKILL.md` or `src/superclaude/agents/rf-qa.md`; Step 5.1 is the sole `make sync-dev` path; Post-Completion item forbids `git add .claude/`. Matches CLAUDE.md ABSOLUTE RULE + memory `feedback_claude_dir_gitignored`. |
| 3 | Intra-phase execution-order simulation | none | PASS | P1 snapshots V15 → P2 flag surface → P3 consumes V15 snapshot in Step 3.2 halt arm → P4 rf-qa → P5 sync/validate. Step 3.2 reads the Step-1.1 snapshot (dependency satisfied earlier). Step 5.4 diffs against Step 1.1 output. No forward dependency. |
| 4 | "Function signature" verification → every cited line/value vs live source | AX-1 | PASS | `:853-856` POST_REFLECT_GATE block, `:1994-1999` V15 item, `:2051` bullet, `:2108` Rule 19 (POST_REFLECT_GATE twice + "MUST NOT run reflect inline"), `:2114-2156` TCS (O1-O4 at :2149-2152, ±4 tiebreaker :2154), `:41`/`:201`/`:1423`/`:1933`/`:1942`, INV-010 regex `:1335-1346`, rf-qa `:298`(28 items)/`:330`(TB-Add-1 through TB-Add-7)/`:378`(TB-Add-8 end)/`:382`(Fix Cycle) — ALL verified byte-accurate. SKILL.md = 2308 lines (task says 2308). |
| 5 | Module context (auto predicate reuses existing TCS/S5/S6, no 2nd model) | none | PASS | Step 2.4 reuses S5(:2126)/S6(:2127)/TCS(:2134) and reads the RESOLVED band (§4.4 INV-004). Step 3.3 keeps O1/O2/O3/O4 as the single producer; auto is a thin band-reading wrapper (NFR-1/NFR-5). No second complexity model authored. |
| 6 | Downstream consumer analysis (oracle consistency across all surfaces) | none | PASS | `reflect_post_mode` 8-value set propagated to: frontmatter doc (3.1), `:2051` bullet (3.4), Rule 19 (3.5), rf-qa V2/active-map/MODE-MATCH (4.1). Step 5.3 is a dedicated cross-surface self-consistency walkthrough asserting no surface lists 7. |
| 7 | Test validity (real artifact, representative input) | none | PASS | Step 5.5 builds fixture `.md` tasklists with real `reflect_post_mode` + mismatched Action shapes (mode:1 w/ `superclaude reflect run`→V6; mode:2 w/ inline→V8; mode:1 w/ `--remediate`→V9) — exercises the actual validation rules, not a `# Test` stub. Precedents `test_evidence_bound_tb_add_8.py` + `test_task_builder_merge.py` confirmed to exist. |
| 8 | Test coverage of primary use case | none | PASS | AT-VALIDATION-1 + AT-MISMATCH-1 + AT-MODE-MATCH + AT-PLUMBING-1 + content-markers (TB-Add-9, `Checklist (29 items)`, 8th value token). Honestly scopes OUT the unreachable `build_tasklist()` end-to-end (no such entry point — research 06). |
| 9 | Error-path coverage (unknown token, wrapper-absent, nested executor) | none | PASS | Step 2.1 unknown token → MALFORMED-input STOP (FR-1). Step 2.4 wrapper-absent under resolved-2 → `*-degraded-halt`, never silent Mode 1, never build STOP (§8/NFR-8). Step 3.2 Mode 1 nested-executor → HALT `mode1-nested-executor` (FR-11). |
| 10 | Runtime failure-path trace (degraded auto→2 validates via V16) | none | PASS | input → A.9 resolve (2.4) → frontmatter 8-value oracle (3.1) → per-mode template (3.2) → rf-qa MODE-MATCH (4.1). The `auto-resolved-2-degraded-halt` path is carried at EVERY surface (OQ-1 8-value union), so a degraded auto→2 emits §6.4 manual-HALT and validates via V15∧V16. No surface drops the 8th value → no silent break. |
| 11 | Completion-scope honesty (OQs resolved or HALT-gated; no shipping auto-default) | none | PASS | OQ-1 resolved w/ applied 8-value union + FLAG-in-Task-Log + explicit HALT-at-3.1 option if operator prefers; OQ-2..OQ-6 resolved/scope-clarified. Phase-6 self-referential POST gate correctly uses CURRENT manual-HALT machinery (refactor not landed at build time), writes PENDING, HALTs per `feedback_human_decision_items_must_halt` — no shipping auto-default. |
| 12 | Ambient dependency completeness (all touchpoints) | none | PASS | Input doc (2.1) + A.2 component (2.2) + A.9 schema (2.3) + A.9 producer (2.4) + frontmatter (3.1) + template (3.2) + depth note (3.3) + `:2051` (3.4) + Rule 19 (3.5) + PRE cross-ref (3.6) + rf-qa TB-Add-9 (4.1) + heading counts (4.2). All read-sites of `POST_REFLECT_GATE`/the old item are accounted for. |
| 13 | Kwarg/dependency sequencing | none | PASS | A.9 schema field `REFLECT_POST_MODE` (2.3) precedes its producer prose (2.4); frontmatter field (3.1) precedes the templates that write it (3.2); rf-qa TB-Add-9 (4.1) precedes the heading bump that counts it (4.2). No "use before define". |
| 14 | Existence claims ("exists at X" / "absent") grep-verified | AX-1 | PASS | "Absent from live source": `grep POST_REFLECT_MODE\|REFLECT_POST_MODE\|reflect_post_mode src/.../SKILL.md` → 0 hits (confirms INV-005 no-live-collision). "Exists": every `:NNN` anchor confirmed (rows above). Phantom 3rd file `rf-task-builder.md` correctly NOT edited (OQ-3). |
| 15 | Cross-reference accuracy for templates/spec sections | AX-1 | PASS | Step 2.4 auto predicate == spec §4.2 lines 271-285 EXACTLY (2-stage, S6→S5→TCS≥35, Stage-2 W-branch). §10.4 WARNING condition (3.5/2.4) == spec line 859 EXACTLY. MODE-MATCH (4.1) == spec §9.3 lines 759-770. Active map (4.1) == §9.2 lines 746-750. V15 byte-anchor == `:1994-1999`. |

**Axis legend:** AX-1 drift, AX-2 contradictions, AX-3 omissions, AX-4 weakened-criteria, AX-5 invented-content, none.

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (no defects found; the plan is high-fidelity)
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep/Bash-grep: 7 | Glob: 0 | Bash: 3

## Spec-Intent Axis Findings (the 5 spawn-prompt judge axes)

**Axis 1 — Does each edit step, executed literally, produce the spec's intended edit?** YES.
- *Step 2.4 auto predicate* matches spec §4.2 byte-for-byte: Stage 1 `S6==1→2 / elif S5>0→2 / elif TCS>=35→2 / else→1`; Stage 2 `risk_mode==1→return 1; risk_mode==2 → W==true?2:2-degraded-halt`. Precedence chain (`--reflect` > `REFLECT_POST_MODE` field > §5 alias map > default 2) matches §10.1. §10.4 WARNING (`fixed --reflect 1 ∧ (S6==1 ∨ S5>0)` → non-blocking, honor request, no STOP) matches FR-13/§10.4.
- *Step 3.2 templates*: Mode 1 = inline top-level `/sc:reflect --mode post --depth standard`, no `--remediate`, FR-11 nested-executor HALT (matches §6.2). Mode 2 = Bash shell-out `superclaude reflect run {TASK_FILE}`, never Agent/Task (matches §6.3). `halt` arm required byte-identical to `:1994-1999` (§6.4/V15) with degraded variant adding ONLY the `<!-- wrapper-absent: degraded from Mode 2 -->` comment.
- *Step 3.5 Critical Rule 19*: correctly CONDITIONS "MUST NOT run reflect inline" on mode (applies to 2/halt/degraded, NOT Mode 1) — this is the FR-3 contradiction fix. A blind preservation would have been a defect; the task explicitly avoids it (task line 159).
- *Step 4.1 TB-Add-9*: carries V1–V16 + §9.2 active map + MODE-MATCH keyed on the 8-value oracle, shaped to INV-010 regex `^[0-9]+\. \*\*TB-Add-([0-9]+):` inside the bounded `#### Structural Gate Additions` span (verified the regex + span boundaries at SKILL.md:1335-1346 / rf-qa.md:330-382).

**Axis 2 — OQ-1 (7-vs-8 value inconsistency).** Correctly resolved. Spec §10.3 (line 848) lists
7 values; §8.2 (line 678), §9.1 V16 (line 739), §9.2 active map (line 749), §9.3 MODE-MATCH
(line 766) all REQUIRE `auto-resolved-2-degraded-halt` (8th). The task applies the **8-value
union** as the sole oracle across ALL surfaces (frontmatter 3.1, Rule 19 3.5, `:2051` 3.4, rf-qa
4.1) AND flags the upstream §10.3 correction as out-of-scope-but-noted AND offers an operator HALT
at Step 3.1. This is the only internally-consistent reading — a degraded auto→2 case validates via
V16. End-to-end coherent.

**Axis 3 — Scope honesty.** Confined to exactly 2 files. The phantom `rf-task-builder.md` edit is
explicitly avoided (OQ-3: completeness gate `grep`-verified it carries no POST-item body). PRE gate
(A.10.7) only receives a COSMETIC cross-ref rename at Step 3.6 (`:1423` token only, no PRE logic) —
spec §11 hard non-goal honored. Wrapper (sibling task) not built.

**Axis 4 — Completion-scope honesty.** All 6 OQs resolved-with-applied-default-and-flag or
HALT-gated; no step ships behavior via silent auto-default. Self-referential Phase-6 gate correctly
uses current (pre-refactor) manual-HALT machinery.

**Axis 5 — No reflect-logic duplication (NFR-1).** Verified. Mode 1 templates INVOKE
(`/sc:reflect`); Mode 2 templates SHELL OUT (`superclaude reflect run`). Step 3.3 is a depth-doc
RECONCILIATION only ("do NOT author depth-derivation logic into any emitted item"). No
deviation-taxonomy / tier / depth-derivation logic re-authored anywhere.

## Issues Found

None. (Adversarial stance held: I actively hunted for a stale citation, a predicate transcription
error, a dropped 8th value, an unconditioned Rule-19 prohibition, and a phantom-file edit — the four
most likely defect classes for this refactor — and found none. Every `:NNN` anchor and every
predicate clause was independently re-verified against live source, not relied upon from the
research files.)

## Actions Taken

None required — no defects found. `fix_authorization: true` was available but unused because the plan
contains no misstatement, wrong-edit, or false-source-claim to fix.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` block was passed in this spawn (this is a standalone
qualitative gate, not a PR-04 passthrough consumer). Per release-spec §19.4 fallback, I performed
INDEPENDENT source-grounded verification rather than relying on any upstream PASS.

**(a) Reliance list — structural items I did NOT independently re-derive:**
- I relied on the research-gate (`qa-research-gate-report.md` PASS) and completeness-gate
  (`analyst-completeness-report.md` PASS) for the claim that the research files faithfully transcribe
  source — BUT I did not take that on faith for the load-bearing anchors (see below).

**(b) Independent semantic checks (≥1 required, INV-019) — where my own tool work was load-bearing:**
- **Live V15 byte-anchor**: I `Read` `src/.../SKILL.md:1990-2006` directly and confirmed the
  `:1994-1999` item text byte-for-byte (title "Independent post-execution reflection gate (fresh
  session, HALT)", `<BASE>` angle-literal, `[--spec {SPEC_PATH}]`, `{DEPTH}` floored-standard, em-dash,
  `feedback_human_decision_items_must_halt`). The task's byte-identity requirement (Step 3.2/5.4)
  rests on this; I verified the source, not the research summary of it.
- **INV-005 no-live-collision**: I ran `grep` for `POST_REFLECT_MODE|REFLECT_POST_MODE|reflect_post_mode`
  over live SKILL.md → 0 hits, independently confirming the task's forward-looking-reconciliation
  premise (task line 68) rather than trusting the research assertion.
- **auto-predicate transcription**: I diffed Step 2.4's predicate against spec §4.2 lines 271-285
  clause-by-clause (a place a paraphrase could have weakened `>=35` to `>35` or dropped Stage-2's
  degraded-halt) — exact match.
- **Rule 19 FR-3 conditioning**: I `Read` live `:2106-2108` and confirmed `POST_REFLECT_GATE: ENABLED`
  appears twice and "MUST NOT run reflect inline" is present unconditioned today — making Step 3.5's
  mode-conditioning the correct (non-defect) fix.

## Recommendations

- **Proceed to execution.** The plan is build-ready. Green light.
- **(Carry-forward, non-blocking)** When this task executes, the executor should honor OQ-1's note
  that the **upstream spec §10.3 enumeration should be corrected to list 8 values** — that is a
  separate edit to `merged-requirements.md`, out of scope here, but worth a follow-up so the spec and
  the shipped oracle agree.

## QA Complete
