# Adversarial Qualitative QA — Gate-Sufficiency + Requirements-Coverage

**Task file:** `.dev/tasks/to-do/TASK-RF-prd-local-file-20260609-005242/TASK-RF-prd-local-file-20260609-005242.md`
**Driving spec:** `.dev/specs/prd-local-file-delivery-fix.md`
**Build profile:** QA_INTENSITY=lite, FINAL_ONLY, TESTING=UNIT, VALIDATION present, POST_REFLECT_GATE=ENABLED (depth=standard)
**Lens:** QA-gate-sufficiency + requirements-coverage. Read-only.
**Reviewer stance:** ADVERSARIAL — assume the encoding is under- or over-built until each dimension is proven against the live task text.

---

## Dimension 1 — Phase 6 FINAL gate meets the lite I22 floor (not under-, not absurdly over-encoded)

**Floor required:** ≥1 structural + ≥1 content + ≥1 domain lens agent, each report-only (`fix_authorization:false`) with adversarial framing → ONE serialized fix agent (`fix_authorization:true`) → ONE verification agent.

| Slot | Step | Agent | fix_authorization | Adversarial framing | Lens |
|------|------|-------|-------------------|---------------------|------|
| Structural lens | 6.2 (L257) | `rf-qa` | `false` (report-only) | byte-exact "Assume…at least 5 errors…" | template-conformance + internal-consistency + evidence-quality |
| Content lens | 6.3 (L261) | `rf-qa-qualitative` | `false` | byte-exact same stance | actionability + domain-accuracy + cross-reference-chain |
| Domain lens | 6.4 (L265) | `rf-qa` | `false` | byte-exact same stance | SOURCE-FIDELITY (semantic-coverage + phantom-detection) |
| Consolidation | 6.5 (L269) | (inline) | n/a | n/a | any-fail-is-fail (I16) |
| Serialized fix | 6.6 (L273) | `rf-qa` | `true` | conditional, exactly ONE, "NO parallel fixes" (I20, 1 cycle max) | applies ALL findings |
| Verification | 6.7 (L277) | `rf-qa` | `false` | "Assume the fixes were applied incompletely…" | combined structural + content re-check |

- 3 report-only lens agents covering structural + content + domain → **floor met exactly**.
- All three carry the byte-exact adversarial stance string.
- Fix is **serialized, singular, conditional** (skipped on PASS-with-zero-issues), explicitly capped at 1 cycle per I20 lite.
- Verification is a single agent, report-only, with its own adversarial framing, gating Post-Completion (does not proceed unless PASS or residuals logged as Open Questions).
- The gate header (L249) correctly self-documents the I22 lite floor and ties the single-gate justification to the <500-line / ~15-line change size.

**Over-encoding check:** 3 lenses (each a *combined* lens, not split into 5–6 separate agents) + 1 consolidation + 1 conditional fix + 1 verification = the minimum viable lite shape. No per-phase rf-qa spawns exist in Phases 1–5 (FINAL_ONLY honored). Not absurdly over-built for a tiny fix.

**Verdict: PASS.**

---

## Dimension 2 — TESTING_REQUIREMENTS=UNIT reflected as real pytest items

- **Real test-authoring items exist** (not stubs):
  - Step 4.1 (L217) — invert/replace `TestSpecFileAttach` to assert NO `--file`; deletes the three `== []` tests naming the removed `_build_file_args`.
  - Step 4.2 (L221) — adds 4 concrete tests: content-inline (UNIQUE_MARKER + `AUTHORITATIVE SPECIFICATIONS`), >50 KB truncation (`_TRUNCATION_MARKER`), missing-path-no-raise, empty-input parity.
- **Test file path present:** `tests/cli/prd/test_spec_flag.py` named explicitly in Phase 4 header and both items.
- **Required command present verbatim:** `uv run pytest tests/cli/prd/ -q` appears at Step 5.2 (L235), the baseline capture Step 1.3 (L159), and the fix-agent re-run 6.6 (L273). UV-only discipline stated repeatedly.
- Baseline-vs-final regression discrimination encoded (Step 1.3 baseline → Step 5.2 compare), with the intentional `TestSpecFileAttach` inversion explicitly flagged as expected-not-regression.

**Verdict: PASS.**

---

## Dimension 3 — VALIDATION_REQUIREMENTS reflected

| Validation requirement | Encoded? | Where |
|------------------------|----------|-------|
| `grep -rn '"--file"' src/superclaude/cli/prd/` → 0 guard | YES | Step 5.1 (L231), exact command + PASS-iff-zero verdict; re-run in fix agent 6.6 |
| `make sync-dev && make verify-sync` clean | YES | Step 5.3 (L239), both commands, PASS-iff-verify-sync-clean; correctly framed as drift guard (never touches `cli/`) |
| Headless-acceptance (spec §8: `--spec`, no session token, reaches `research-notes`) | PARTIAL — reflected, not independently runnable | See note below |

**Headless-acceptance note (adversarial scrutiny):** Spec §7.7 and §8 item 4 are explicitly labeled *manual/integration* — they require a live `claude` subprocess against the octodive repro, which a unit-tier executor cannot run deterministically in-harness. The criterion IS reflected:
- Stated as the task's blocking outcome (L92: "A headless PRD `--spec` run reaching `research-notes` (clearing `scope-discovery`) with no session token").
- Pushed into the QA gate as a verification target — the qualitative lens (6.3, L261) is directed to confirm "the removal leaves headless `--spec` runs token-free," and the domain-fidelity lens (6.4, L265) is directed that "each §8 acceptance criterion has a corresponding verification."
- The grep-guard (§8 item 1) is the deterministic proxy that proves the token-dependency is gone, which is the mechanical precondition for the headless run to clear `scope-discovery`.

This is the correct treatment for a lite UNIT task: the manual/integration criterion is surfaced and audited by the gate rather than fabricated as a non-runnable "executor runs the live pipeline" item (which would be a phantom). No over-claim, no fabricated run. Acceptable.

**Verdict: PASS** (all three reflected; the integration criterion appropriately reflected-but-not-runnable, consistent with spec §7.7 labeling).

---

## Dimension 4 — POST_REFLECT_GATE (ENABLED, depth=standard)

POST reflect item at **L289**.

- **Position:** penultimate. L289 is the reflect gate; L291 is the final `status → 🟢 Done` flip. The Done-flip item (L291) explicitly states it is the LAST item and that the reflect verdict "must be done first…preserving anti-orphaning." **Penultimate placement confirmed.**
- **References `/sc:reflect --mode post`** — YES, the paste-ready command is `/sc:reflect --mode post --remediate --diff <START_COMMIT>..HEAD … --depth standard`. Item body asserts "the command names `/sc:reflect` for the gate and NEVER `/sc:task`." Not `/sc:task`.
- **`--spec` points at driving spec** — YES: `--spec .dev/specs/prd-local-file-delivery-fix.md`, and the closing constraint re-asserts it.
- **`--depth standard`** — YES, present in the command and reinforced ("`--depth standard` is the POST floor (NEVER `quick`)").
- **Fresh-session HALT semantics correct:** writes `reflect_post: PENDING`, STOPS, does not run inline, does not self-resolve, cannot be marked done until operator records `reflect_post: {verdict, run_id, report}` (waiver path also provided). `<START_COMMIT>` sourced from Step 1.3 `start_commit` (or `git merge-base HEAD main` fallback).

**Verdict: PASS.**

---

## Dimension 5 — Scope creep (items beyond spec §5 scope flagged)

Spec scope (frontmatter §scope + §5 + §9): `src/superclaude/cli/prd/{process.py,prompts.py}` + `tests/cli/prd/`. §9 out-of-scope: executor crashloop hardening, sibling pipelines, raising the 50 KB cap / >50 KB digest, base-class `--file` test.

Walked every checklist item:
- Phase 2 (process.py): both `--file` branches, `_build_file_args`, `extra_args` wiring, 3 dead constants (grep-gated), docstrings — all map to §5.1. In scope.
- Phase 3 (prompts.py): `_authoritative_specs_block` body + docstring, `is_file()` guard — §5.2. `_read_file`/`_TRUNCATION_MARKER` explicitly NOT modified (locked by `TestReadFileTruncation`). In scope.
- Phase 4 (tests): only `tests/cli/prd/test_spec_flag.py`. **`tests/pipeline/test_process.py:78-81` explicitly protected from modification** (L213, L243) per §7.5/§9. In scope.
- Phases 1, 5, 6, Post-Completion: discovery, verification, QA, reflect, status — process scaffolding, not product scope-creep.

**No scope creep found.** The task is, if anything, defensive about scope: it actively flags and forbids the §9 out-of-scope edits (base-class test, sibling pipelines), and Step 5.4 (L243) adds a git-scope guard asserting changes are confined to exactly the three files + `.dev/` and ZERO tracked `.claude/`. No speculative additions (no cap-raising, no digest, no executor hardening).

**Verdict: PASS.**

---

## Adversarial residual observations (non-blocking)

1. **Spec §5.2 latitude vs task rigidity (intentional, correct):** Spec §5.1 offers an *either/or* — remove `_build_file_args` OR retain it returning `[]`. The task hard-selects removal (Steps 2.4–2.5). This is a *tightening*, justified by research 04 Decision 4 (sole constructor passes no `extra_args`), not a deviation. Acceptable and arguably better than leaving dead code.
2. **Headless §8 criterion is the only acceptance item with no deterministic in-harness assertion.** Flagged in Dimension 3 — it is reflected and audited, not fabricated. The grep-guard is its mechanical proxy. No action required for a lite UNIT task, but a reviewer should not expect a green "headless run cleared scope-discovery" artifact among the phase-outputs; its verification lives in the §8 narrative + the two QA-agent prompts.
3. **Gate self-documentation is accurate:** the Phase 6 header's claim of "3 agents → 1 consolidation → 1 fix → 1 verification" matches the actual encoded items 6.2–6.7. No drift between the header's claimed shape and the implemented shape.

---

## FINAL VERDICT

- D1 Phase 6 lite I22 floor: **PASS**
- D2 UNIT pytest items + command: **PASS**
- D3 VALIDATION (grep guard / verify-sync / headless-acceptance reflected): **PASS**
- D4 POST_REFLECT_GATE penultimate, `/sc:reflect --mode post`, correct `--spec` + `--depth standard`: **PASS**
- D5 no scope creep: **PASS**

**VERDICT: PASS**

The Phase 6 final gate is encoded to the lite I22 floor exactly (3 report-only adversarial lens agents spanning structural/content/domain → 1 consolidation → 1 serialized conditional fix → 1 verification), neither under- nor over-built for a ~15-line fix. UNIT testing is realized as genuine pytest authoring items with the correct file path and `uv run pytest tests/cli/prd/ -q` command. All three validation requirements are reflected — grep-guard and verify-sync as deterministic in-harness items, and the spec-§7.7-labeled manual/integration headless-acceptance criterion appropriately surfaced and audited by the QA lenses rather than fabricated as a non-runnable item. The POST_REFLECT_GATE is correctly placed penultimate, halts for a fresh session, and names `/sc:reflect --mode post` (not `/sc:task`) with `--spec .dev/specs/prd-local-file-delivery-fix.md` and `--depth standard`. No scope creep — the task actively forbids the §9 out-of-scope edits and adds a git-scope confinement guard.
