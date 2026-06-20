# rf-qa Structural Validation Report — TASK-RF-reflect-wrapper-autofix-20260610-053000

- **Mode:** task-integrity (structural lens), REPORT-ONLY, `fix_authorization: false`
- **Stance:** ADVERSARIAL (assume defects; min 5 findings unless exhaustively disproven)
- **Reviewer:** rf-qa structural validator
- **Date:** 2026-06-10
- **Task file:** `.dev/tasks/to-do/TASK-RF-reflect-wrapper-autofix-20260610-053000/TASK-RF-reflect-wrapper-autofix-20260610-053000.md` (535 lines)
- **Spec:** `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md`
- **Contract:** `.dev/handoffs/reflect-wrapper-contract.md`
- **Research:** R1 `01-reflect-cli-surface.md`, R2 `02-reflect-skill-contract.md`, R3 `03-claudeprocess-tests-thinness.md`

---

## Lens-by-lens findings

### Lens 1 — Frontmatter well-formed
PASS. `id` (L2), `title` (L3), `status: "🟡 To Do"` (L5), `type: "🔧 Refactor"` (L6), `spec_path` (L36), `related_docs` (L16-28) all present and well-formed. `priority`, `tags`, `template_schema_doc` also present. No issue.

### Lens 2 — B2 self-containment
PASS (strong). Every `- [ ]` item embeds context (file:line anchors), action, output path, an "ensuring…" verification clause, an evidence-on-failure clause, and a "mark this item complete" gate. All agent-spawn items (PG1.2, PG2.2/2.3, PG3.2/3.3, PG4.2/4.3, PG5.2/5.3, PG6.2/6.3, PG7.1/7.2) carry FULLY embedded verbatim prompts in quotes. No "see above" cross-references that defeat session-rollover isolation. The header L144 explicitly states the self-containment contract.

### Lens 3 — Granularity
PASS. Items are per-file/per-concern: Phase 2 splits models.py (2.1) from config._resolve_base (2.2) from config.resolve_config (2.3). Phase 4 splits classifier (4.1), field-surfacing (4.2), _audit_once extraction (4.3), _apply_remediation (4.4), loop-wiring (4.5), prompt/sidecar (4.6). Phase 6 has one item per AC fixture/test. No batch "edit all five files" items.

### Lens 4 — Phase ordering / DAG
PASS. Ordering is models/config (P2) → commands (P3) → contract/runner (P4) → skill (P5) → tests (P6) → verify (P7). Dependencies form a DAG: Step 2.1 adds the model fields that 2.3/3.1/4.2/4.6 populate; 4.2 depends on 2.1's `remediation_task_path` field; 4.5 depends on 4.1/4.3/4.4; 6.x tests depend on the impl phases. Each phase gate precedes the next phase. No cycles.

### Lens 5 — PER_PHASE QA gates
PASS. Every phase 1–7 has a trailing Phase Gate with aggregate → rf-qa (structural) → [rf-qa-qualitative for P2-P7] → conditional-fix-then-reverify (max 2 cycles). All gates: report-only `fix_authorization:false` for the audit agent, single fix agent `fix_authorization:true` only in the conditional step, adversarial framing ("ADVERSARIAL STANCE"). Gate 1 has 1 audit agent (structural only); Gates 2–7 have 2 (structural + qualitative). BUILD-REQUEST L77 specifies PER_PHASE — satisfied.

### Lens 6 — BOOTSTRAP EXEMPTION (CRITICAL)
PASS. The tasklist does NOT terminate with a `superclaude reflect run` gate. The POST reflect item (L450) is the INLINE `/sc:reflect --mode post --depth standard --tasklist … --spec …` form, explicitly annotated "NOT a `superclaude reflect run` shell-out — that command is the artifact this tasklist builds". The ONLY `superclaude reflect run` invocations are: Step 7.2 `superclaude reflect run --help` (L424, the allowed `--help` probe) and Step 4.5/contract prose describing the engine being built. Verified no terminal wrapper-gate exists. **NOTE:** the task correctly OVERRODE a contradictory BUILD-REQUEST L84-85 directive that suggested building with the ABANDONED `--reflect 1`/`--reflect none` dial; the task uses the clean inline form instead. This is a correct resolution, not a defect.

### Lens 7 — ANTI-ORPHANING
PASS. The final checklist item (L454) is the frontmatter "Update status to 🟢 Done + completion_date" item. It is preceded by Task Summary (L452), post-reflect (L450), and output-verification (L446) items. Done-status update is genuinely last.

### Lens 8 — AC coverage (spec §8, 9 ACs)
PASS — every AC maps to ≥1 item:

| AC | Requirement | Implementing item(s) | Test item(s) |
|----|-------------|----------------------|--------------|
| AC1 | marker self-suppress exit 0 | 3.3 | 6.3 |
| AC2 | auto-fixable+path → /task + re-audit → exit 0 | 4.5 | 6.5(a) |
| AC3 | regression/needs_human/user_decision/gaps → HALT 10 | 4.1, 4.5 | 6.4, 6.5 |
| AC4 | non-convergence → exit 10, fix_converged false | 4.5, 4.6 | 6.5(b) |
| AC5 | O1 promote / O2 no-promote | 3.2 | 6.6 |
| AC6 | --base override; single-ref --diff | 2.2 | 6.7 |
| AC7 | reflect emits remediation_task_path @1.4.0; wrapper reads | 4.2, 5.1, 5.2, 5.4 | 6.1, PG5 |
| AC8 | no sprint/roadmap import; no async; only ClaudeProcess; pipx | 4.4, 6.8 | 6.8, 7.2 |
| AC9 | v1 fail-closed tests stay green | (preserved across edits) | 2.4, 3.5, 4.7, 6.9, 7.1 |

### Lens 9 — Contract conformance (D1–D7, contract §§2–6)
Mostly PASS with gaps (see issues):
- O1 shape `--depth deep --fix --promote` → 3.1 (flags) + 3.2 (promote default) + 6.6.
- O2 shape `--fix --no-promote --base <sha>` → 3.1 + 2.2 + 6.6/6.7.
- Marker self-suppress (D2) → 3.3 + 4.4 (export) + 6.3.
- Bounded loop (D3) → 4.5 + 6.5.
- Safe-class carve-out (D4) → 4.1 + 6.4. **Gap: grounding-gaps trigger (see IMPORTANT-2).**
- Promote scope (D5) → 3.2; O2 force left to generator (U6) — correct.
- --base precedence (D6) → 2.2/2.3 + 3.4 (tmux) + 6.7.
- Depth passthrough (D7) → confirmed no-change (Key Objective; R1 §6); no dedicated item but research shows it is already correct. Acceptable.

### Lens 10 — [UNVERIFIED]/[CODE-CONTRADICTED] / research contradictions
PASS. All task file:line anchors match R1/R2/R3. Cross-checked: models.py:66-81/76/98-106/106 (R1 L285-297); config.py:81-93/111-127/168/205-222/51/44 (R1 L107-147); commands.py:62-107/108-119/131-144/70-75/233-255 (R1 L31-101); contract.py:304-325/90-101/104-124/65-82/5-8 (R1 L238-279); runner.py:378-501/459-468/331-352/181-225 (R1 §3); process.py:97-112 (R3 L38); cli/main.py:440-442 (R1 L322, R3 L463); _SPEC9_FLAGS :15-26 (R3 L232). No anchor contradicts its research source.

---

## Adversarial issues (severity-rated)

### IMPORTANT-1 — `write_sidecar` is called from 4 sites but the new sidecar keys are added before all 4 ReflectResult construction sites carry defaults verified
**File:line:** Task L290 (Step 4.6) adds `"fix_iterations"`/`"fix_converged"` to the `write_sidecar` data dict, which is called from 4 sites (commands.py:173 config-error, runner.py:422-427 preflight, runner.py:449-454 resume, runner.py:495-500 main). Step 2.1 (L190) defaults the new `ReflectResult` fields, and Step 4.6 relies on those defaults so non-main sites serialize. This IS correctly sequenced (2.1 before 4.6). However, R1 L228 internally states "3 sites" then lists 4 — a research inconsistency. The TASK uses "4 sites" (L290) which matches R1's actual enumeration. **Why flagged:** the config-error sidecar at `commands.py:173` builds `ReflectResult` BY HAND (R1 L228 "Builder note"). Step 4.6 references the sidecar add but the config-error hand-built `ReflectResult(...)` in `commands.py` is NOT given an explicit checklist item to confirm it still constructs validly after the field additions — it relies entirely on the Step 2.1 defaults holding. **Fix:** add to Step 4.6's "ensuring…" clause an explicit verification that the hand-built `commands.py` config-error `ReflectResult(...)` (R1 L304/L228) still constructs without the new fields (defaults cover it), and that Step 2.4/3.5 tests exercise the config-error path. (Low residual risk since defaults are mandated, but the adversarial lens wants the hand-built site named.)

### IMPORTANT-2 — Grounding-gaps HUMAN-REQUIRED trigger is silently narrowed to `needs_human_decision` with no test that the proxy actually holds
**File:line:** Spec FR-4 (merged-requirements L118/L121) and contract §4 (L121/L125) list "**non-empty grounding-gaps**" as an independent HUMAN-REQUIRED trigger, distinct from `needs_human_decision`. Task Step 4.1 (L270) implements `classify_fix` keying ONLY off `needs_human_decision` (per Open-Question U4, L137, citing deviation-taxonomy.md:132-135 that `needs_human_decision:true` is emitted whenever grounding-gaps is non-empty). The carve-out test Step 6.4 (L374) lists rows for `needs_human_decision:true` but NOT a dedicated row asserting a contract with non-empty `grounding_gaps_path` + `needs_human_decision:false` routes correctly. **Why flagged (adversarial):** the entire safety equivalence "grounding-gaps non-empty ⇒ needs_human_decision=true" rests on a single cited line in another doc (U4). If that emission invariant ever regresses in reflect, a grounding-gaps-only contract with `needs_human_decision:false` would be MISCLASSIFIED auto-fixable and a human-decision change could ship — violating `feedback_human_decision_items_must_halt`. **Fix:** add an explicit row to Step 6.4's matrix: a contract with non-empty `grounding_gaps_path` AND `needs_human_decision:false` → assert the test documents the U4 dependency (either the classifier ALSO reads a grounding-gaps signal, or the test asserts the invariant is relied upon and references the U4 source). At minimum, surface U4's load-bearing assumption in Step 4.1's "ensuring" clause as a named risk.

### IMPORTANT-3 — Bounded loop has no defined break for a DEGRADED/BLOCKED verdict reached WITH `--fix` set
**File:line:** Task Step 4.5 (L286) defines the loop breaks as: PASS→break; not-config.fix→break; classify_fix != auto-fixable→break; absent remediation_task_path→break; iteration>max→break. The spec state machine (merged-requirements L54-60) routes DEGRADED→exit 11 and BLOCKED→exit 2 as terminal states that must NOT enter the apply branch. Step 4.1 (L270) notes the classifier "is intended to be consulted ONLY on a HALTED result (DEGRADED/BLOCKED are terminal upstream in `derive_verdict`)." But Step 4.5's loop body, as written, calls `classify_fix` for any non-PASS verdict when `config.fix` is set — it does NOT explicitly short-circuit DEGRADED/BLOCKED BEFORE calling the classifier. If `classify_fix` is fed a degraded/blocked contract it would return "none" (break) only if drift/necessary are zero — but a degraded run could coincidentally carry drift>0, yielding a SPURIOUS "auto-fixable" and an erroneous `/task` apply on an untrusted audit. **Why flagged:** contract §4 (L125) explicitly lists "a `degraded`/`blocked` verdict" as HUMAN-REQUIRED/terminal; the loop must guard it. **Fix:** amend Step 4.5 to add an explicit early break "if `result.verdict` is DEGRADED or BLOCKED → break (terminal, no classify, no apply)" BEFORE the `classify_fix` call, and add a covering row to Step 6.4/6.5 asserting a degraded-with-drift contract does NOT auto-fix.

### MINOR-4 — `--base` precedence vs `--resume` clean-HEAD short-circuit interaction unspecified
**File:line:** Step 2.2/2.3 add `base_override` precedence; FR-10 (merged-requirements L166) preserves the `--resume` clean-HEAD short-circuit (R1 cites resume at runner.py:431-455). No item specifies whether an explicit `--base` interacts with the resume short-circuit (e.g. does `--base <sha> --resume` on a clean HEAD still short-circuit, ignoring the pinned base?). The O2 per-phase gate passes `--base` and could in principle be combined with resume. **Fix:** add a one-line note to Step 2.3 or Step 6.7 clarifying that `--base` does not alter the resume clean-HEAD short-circuit semantics (resume precedence is unchanged), or explicitly state it is out of scope. Low impact (generators don't emit `--resume` on gates per contract §2), hence MINOR.

### MINOR-5 — `task_type: static` frontmatter vs autogen subagent-spawn items
**File:line:** Frontmatter L50 sets `task_type: static`; L11 `autogen: false`. Yet ~13 checklist items spawn `rf-qa`/`rf-qa-qualitative`/fix agents (e.g. PG1.2 L178). Per memory `reference_subagent_cannot_nest_skill_fanout`, agent-tool subagents cannot nest skill fan-out — but the gate agents here are rf-qa structural/operational reviewers (read + report), not producers that spawn their own fan-out, so this is acceptable. **Why flagged (adversarial, low):** the executor running this task top-level must spawn these agents itself; a static-typed task that is itself executed as a subagent would lose the gate fan-out. **Fix:** add a one-line note in the Frontmatter Update Protocol or Phase 1 header stating "this tasklist MUST be executed top-level (not as a nested subagent) so the per-phase rf-qa gates spawn correctly" — mirroring the known nesting constraint. Documentation-only.

### MINOR-6 — Step 6.2 apply-launch-writes-no-contract handling is described but not pinned with a fixture
**File:line:** Step 6.2 (L366) extends the stub factory to a sequence and notes "the apply-launch (a `/task` ClaudeProcess) … writes no return-contract.yaml; the sequence must account for which launches are audits vs applies." Step 6.5 (L378) then asserts call-count arithmetic (3 / 5 / 1). The handling of "apply writes no contract" is left to the factory implementation without a named sentinel fixture for the apply step (audit#2 must overwrite the apply's empty output). **Fix:** Step 6.2's "ensuring" clause should explicitly require a test asserting the apply-launch's `output_dir` does NOT leave a stale `return-contract.yaml` that the next audit would misread (i.e., audit#2 writes a fresh contract). Low risk since the factory derives output_dir per call; MINOR.

---

## Verdict

**FAIL** — task is high-quality and passes lenses 1–8 and 10, but lens 9 (contract conformance) surfaces two IMPORTANT safety-loop gaps that an adversarial structural review must block on:

- **IMPORTANT-3** (no explicit DEGRADED/BLOCKED break before `classify_fix` in the bounded loop) is the most material: it admits a spurious auto-fix on an untrusted audit, directly contravening contract §4's "degraded/blocked ⇒ HUMAN-REQUIRED/terminal."
- **IMPORTANT-2** (grounding-gaps trigger narrowed to a single proxy field with no falsifying test) leaves a `feedback_human_decision_items_must_halt` blind spot resting on an unverified cross-doc emission invariant.
- **IMPORTANT-1** (hand-built config-error `ReflectResult` not explicitly re-verified) is a smaller correctness gap.

All three are remediable with targeted edits to Step 4.1, Step 4.5, Step 6.4, and Step 6.5 (add explicit terminal-verdict break, add grounding-gaps + degraded-with-drift matrix rows, name the hand-built construction site). The three MINOR items are documentation/edge-case hardening.

**Recommended action:** route to a single fix cycle adding the DEGRADED/BLOCKED loop break (4.5), the grounding-gaps + degraded-with-drift carve-out test rows (6.4/6.5), and the U4-dependency note (4.1); then re-verify.

### Severity summary
- CRITICAL: 0
- IMPORTANT: 3 (loop terminal-verdict break; grounding-gaps proxy + missing test; hand-built ReflectResult re-verify)
- MINOR: 3 (base×resume interaction; static-type top-level note; apply-launch stale-contract fixture)
