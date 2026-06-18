# Analyst Completeness Report — BREADTH lens

**Analysis type:** completeness-verification
**Lens:** completeness (BREADTH — every spec area has corresponding research coverage; depth is NOT assessed here)
**Date:** 2026-06-15
**Track:** Sprint Run 429 / account-exhaustion recovery task-builder (single track, P1-P6)
**Driving spec:** `.dev/brainstorms/sprint-429-recovery-spec.md`
**Scope map:** `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/research-notes.md`
**Files analyzed (6):** `01-file-inventory.md`, `02-patterns-conventions.md`, `03-integration-points.md`, `04-data-flow-tracer.md`, `05-test-verification.md`, `06-template-examples.md`

**Method:** For each of the 8 breadth criteria, map the spec requirement to the research file(s) that cover it, citing the specific section/finding. PASS = the spec area is covered with an insertion point / decision the builder can act on. FAIL = a spec-required area has no corresponding research coverage (a gap), or coverage is materially wrong such that the builder would have nothing to act on.

**Coverage rating legend per spec area:**
- COVERED — at least one research file documents the area with actionable insertion points.
- COVERED+ — covered, and a research file additionally surfaced a correction/finding strengthening coverage.
- PARTIAL — area covered but a sub-element of the spec requirement is missing or only flagged Unverified.
- GAP — spec-required area absent from all research files.

---

## Criterion 1 — P1 Detection (detect_provider_failure + ProviderFailure enum + text-core split + 2 regexes + 6 fixtures)

**Spec requirement (§4 Layer 1, §6, §7 P1):** new `detect_provider_failure` detector, `ProviderFailure` enum (4 members), `_provider_failure_from_text` text-core split (so `_classify_transcript` shares one core), 2 regexes (`_RE_ALL_ACCOUNT` with model capture, `_RE_SINGLE_ACCOUNT`), `ProviderFailureSignal` return type, 6 fixtures, subtype-trap avoidance, timeout-separation.

**Verdict: PASS — COVERED+**

| Sub-element | Covered by | Evidence |
|---|---|---|
| `detect_provider_failure` path wrapper | 01 §FILE 1 item 6; 02 Pattern A; 03 (consumed); 04 §1 | Insertion zone L250-253 (between `count_turns_from_output` end and `OutputMonitor`); mirrors `detect_error_max_turns` (monitor.py:37-61). |
| `ProviderFailure` enum (4 members) | 01 §FILE 1 item 1 | Members NONE/SINGLE_ACCOUNT_LIMIT/ALL_ACCOUNT_COOLDOWN/OPERATION_TIMEOUT verbatim from spec §4. |
| `_provider_failure_from_text` text-core | 01 §FILE 1 item 5; 02 Pattern A "text-core split"; 03 IP-6; 04 §2 | Net-new factoring forced by `_classify_transcript(text: str)` at rerun_tasks.py:547 — explicitly flagged as having no monitor exemplar (02). |
| 2 regexes (`_RE_ALL_ACCOUNT` + `_RE_SINGLE_ACCOUNT`) | 01 §FILE 1 items 3-4; 02 Pattern A elem 1 | `_RE_ALL_ACCOUNT` named group `model` captures resolved model for the suggester. |
| `ProviderFailureSignal` return type | 01 §FILE 1 item 2 | Proposed `@dataclass(frozen=True)` (kind, resolved_model); spec names but does not define — research supplies the shape. |
| 6 fixtures | 05 §3.1-3.6 | All 6 authored from spec §2 verbatim JSON: single_account_429, all_account_cooldown (+resolved model + prior tokens), operation_timeout, api_retry_maxed, task_failure_real, clean_pass. Target dir `tests/sprint/fixtures/exhaustion/` (new). |
| subtype-trap + timeout-separation | 01 item 5; 02 Pattern B; 04 §1 edge #8/#10; 05 §3.3 | Key on `is_error`+`api_error_status`, NEVER `subtype`; OPERATION_TIMEOUT discriminated by `api_error_status==null`. |
| Insertion point precision | 01 §FILE 1 + SUMMARY | Includes 2 NEW import-adds (`from enum import Enum`, `from dataclasses import dataclass`) NOT flagged in research-notes — a correction strengthening coverage. |

**Notable correction (COVERED+):** 01 + 04 + 05 all independently flag that the spec/research-notes symbol name `count_turns_from_stream_json` is wrong — the real monitor.py symbol is `count_turns_from_output` (monitor.py:223), and the true last-result-event `json.loads` mirror is `count_turns_from_stream_json` in **process.py:32-76** (02 Pattern B). The builder has the corrected mirror target. No gap.

---

## Criterion 2 — P2 Taxonomy (FAIL_PROVIDER_EXHAUSTED + is_failure, TaskResult new fields + back-compat from_dict, PhaseStatus.PROVIDER_EXHAUSTED, _classify_transcript alignment, resume-safety)

**Spec requirement (§4 Layer 2, §6, §7 P2):** `TaskStatus.FAIL_PROVIDER_EXHAUSTED` added to `is_failure`; 3 `TaskResult` fields (`failure_class`/`session_resets`/`exhausted_model`) serialized in to_dict and read with `.get()` back-compat in from_dict; `PhaseStatus.PROVIDER_EXHAUSTED`; `_classify_transcript` aligned to the shared detector; resume-safety (both per-task and hard-crash fallback paths).

**Verdict: PASS — COVERED+**

| Sub-element | Covered by | Evidence |
|---|---|---|
| `FAIL_PROVIDER_EXHAUSTED` + is_failure | 01 §FILE 2 items 1-2; 02 Pattern C; 03 IP-8; 04 §6 | Add member after L54; extend `is_failure` tuple L62-66; do NOT add to is_success. |
| 3 TaskResult fields | 01 §FILE 2 items 3-5; 02 Pattern D | Added after L188 `output_path`; defaults `""`/0/`""`. |
| to_dict serialize | 01 §FILE 2 item 6; 02 Pattern D | After L215. |
| from_dict back-compat (.get()) | 01 §FILE 2 item 7; 02 Pattern D; 04 §6; 05 §7 | VERIFIED `TaskResult.from_dict` is HARD-KEYED (models.py:218-240) — the back-compat hazard is real; use `.get()` exactly as `HandoffRecord.from_dict` (models.py:337-349). Back-compat test authored both directions (05 §7). |
| `PhaseStatus.PROVIDER_EXHAUSTED` | 01 §FILE 2 items 8-10; 02 Pattern C; 03 IP-3 | Member near L404; add to `is_terminal` AND `is_failure` — but see Criterion 4 (F-1) for the is_failure decision. |
| `_classify_transcript` alignment | 03 IP-6; 04 §2 offline ladder; 05 §P2 | Exact insert above rerun_tasks.py:582, after :580, calling `_provider_failure_from_text(text)`; returns FAIL_PROVIDER_EXHAUSTED for SINGLE/ALL. |
| resume-safety (both paths) | 03 IP-8; 04 §6; 05 §10 | Per-task `_coerce_task_status → TaskStatus(value)` (planner.py:339) AND hard-crash `discover_failed_tasks_from_transcripts → _classify_transcript` both auto-resolve; ZERO planner edit; resume-safety TEST authored. |

**Notable correction (COVERED+):** 01 flags that **PhaseStatus has THREE membership properties** (`is_terminal` L409, `is_success` L425, `is_failure` L436) — research-notes under-counted by mentioning only the member add. The builder is told PROVIDER_EXHAUSTED must touch `is_terminal` (the silent-omission hazard per 02 Pattern C). 03 IP-8 also corrects the `_coerce_task_status` location (DEF at planner.py:339; the CALL is at :157 — research-notes cited :157 for both). No gap.

---

## Criterion 3 — P3 Policy + Executor (recovery_policy.py, per-task re-spawn loop, latch threading at BOTH call sites, persistence, diagnostic-bundle hazard at executor.py:2103)

**Spec requirement (§4 Layer 3+4, §5 edge #3, §6, §7 P3):** new `recovery_policy.py` (Action enum, SessionResetPolicy.decide); bounded re-spawn loop wrapping the spawn in `_run_one_task`; global latch threaded at BOTH call sites (K>1 and K=1); persistence of `session_resets`/`failure_class`/`exhausted_model`/`halt_reason`; the diagnostic-bundle hazard addressed.

**Verdict: PASS — COVERED+ (the diagnostic-bundle hazard is not only addressed but materially corrected)**

| Sub-element | Covered by | Evidence |
|---|---|---|
| `recovery_policy.py` (Action enum + SessionResetPolicy + decide) | 01 §FILE 3; 04 §1 table; 05 §6.1 | 4-member Action enum, 3-field dataclass (max_session_resets=8, _exhaustion_attempts, _latch_tripped), pure `decide`; truth-table test authored. |
| re-spawn loop wrap point | 03 IP-1 (exact `:986-993` block); 04 §0/§2 | 4-step loop: check latch under lock → spawn unlocked → detect → decide; insert branch ABOVE :1012 BELOW :1003 gate; reuse `_task_completed_before_overrun` guard. |
| latch threading BOTH call sites | 02 Pattern E elem 3; 03 IP-1 (`:1134-1145` K>1 lock=lock; `:1337-1348` K=1 lock=None) | Explicitly per-call-site items; "missing either site = no recovery on that K mode." Shared policy constructed once per phase. |
| persistence | 03 IP-5 (payload `:2685-2696`); 04 §6; 05 §6 persistence asserts | Two new top-level keys (`halt_reason`/`exhausted_model`) + per-task TaskResult fields via `tr.to_dict()` at :2691. PhaseResult gains halt_reason/exhausted_model fields. |
| storm bound arithmetic | 02 Pattern E; 03 §summary; 04 §3 | `≤ cap+(K−1)` AND `< K×cap`, NOT `≤ cap` — the over-strict-assertion trap is called out for the test author. |
| **diagnostic-bundle hazard (executor.py:2103)** | 03 IP-3; 04 FINDING F-1 | **MATERIALLY CORRECTED — see below.** |

**Material correction on the diagnostic-bundle hazard (COVERED+, the most important finding in the research set):**
Both 03 (IP-3) and 04 (FINDING F-1) independently **correct** the spec's §4-Layer-2 claim that `executor.py:2103` "only halts the phase" / "has no auto-remediation consumer." Verified reality: the `:2103` block runs `DiagnosticCollector` + `FailureClassifier` + writes `phase-N-diagnostic.md` **automatically** — but ONLY on the single-session `PhaseStatus.is_failure` path. The per-task path `continue`s at :1781 and never reaches :2103, so a per-task `FAIL_PROVIDER_EXHAUSTED` already satisfies UX contract #4 by construction.

This is correctly covered for P3 (per-task = safe by construction) and escalated to Criterion 4 (single-session = the hazard the builder must guard). The research did NOT silently accept the spec's wrong premise — it traced the real wiring and corrected it. No gap.

---

## Criterion 4 — P4 Single-session path (ClaudeProcess wrap + PhaseStatus routing, incl. is_failure vs is_terminal decision)

**Spec requirement (§4 Layer 4, §6, §7 P4):** wrap the single-session `ClaudeProcess` spawn in a re-spawn loop; route ALL_ACCOUNT/cap-exhausted to `PhaseStatus.PROVIDER_EXHAUSTED`; decide is_failure vs is_terminal placement so the phase halts without tripping the diagnostic bundle.

**Verdict: PASS — COVERED+**

| Sub-element | Covered by | Evidence |
|---|---|---|
| `ClaudeProcess` wrap point | 03 IP-2 (exact `:1815-1956` block, before `:1993`) | spawn :1815-1816 → poll :1831-1948 → exit-capture :1950-1956; short-circuit to PROVIDER_EXHAUSTED before `_determine_phase_status`; must re-`monitor.reset`/re-`setup_isolation` per attempt. |
| reads `config.output_file(phase)` not task_output_file | 03 IP-2; 05 §6 single-session | Single-session uses `output_file` (phase-N-output.txt), per-task uses task_output_file — distinction documented. |
| do-NOT-route-through `_determine_phase_status` | 03 IP-2 | At :2774 `exit_code != 0` would fall to PhaseStatus.ERROR (:2795) — the exact misclassification P4 fixes; no edit inside `_determine_phase_status`. |
| **is_failure vs is_terminal decision** | 03 IP-3 (options B1/B2, recommends B1); 04 FINDING F-1 (alt resolutions) | Both files present the decision EXPLICITLY: add PROVIDER_EXHAUSTED to `is_terminal` always; for halt, EITHER guard the :2103 bundle with `and status is not PhaseStatus.PROVIDER_EXHAUSTED` (B1, recommended — reuses is_failure→halt→break) OR keep it out of is_failure and add an explicit halt branch (B2). Test: assert NO `phase-N-diagnostic.md` is written on a single-session 429 halt. |
| single-session test | 05 §6 (TestExecuteSprintIntegrationCoverage, mirror :383-434) | Patch subprocess.Popen, write cooldown to output_file, assert status==PROVIDER_EXHAUSTED + outcome==HALTED. |

**Notable correction (COVERED+):** The `is_failure` vs `is_terminal` decision is exactly the kind of fork that the spec left implicit ("routes to halt") and the research made explicit and actionable with two encoded options + a recommendation + a regression test. Both 03 and 04 independently surface that putting PROVIDER_EXHAUSTED in `is_failure` naively WOULD trip the diagnostic bundle. No gap.

---

## Criterion 5 — P5 (aienv.py + build_account_exhaustion_halt + --max-session-resets flag 4-hop + doc⇆CLI parity)

**Spec requirement (§4 Layer 5, §6, §7 P5):** new `aienv.py` (parse ~/.aienv, `suggest_alternate_model`); `build_account_exhaustion_halt` single-line resume + CLIProxyAPI rationale; `--max-session-resets` flag (4-hop chain); doc⇆CLI parity.

**Verdict: PASS — COVERED+ (with a flagged design decision the builder must encode, not silently pick — see Criterion 8)**

| Sub-element | Covered by | Evidence |
|---|---|---|
| `aienv.py` + `suggest_alternate_model` | 01 §FILE 4 + §FILE 5; 03 IP-9 (env inheritance); 05 §8.2 | ~/.aienv convention extracted from scripts/ic + swarm/config.py; slot names (ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL, T2Model01..09); suggester prefix-agnostic + None-safe; matches resolved model from cooldown body. aienv test authored with injectable `aienv_path`. |
| `build_account_exhaustion_halt` | 01 §FILE 2 item 11; 02 Pattern D build_* convention; 04 §6 halt UX; 05 §8.1 | Insert after build_resume_output (after L1071); single-line `--resume … --model <suggested>`; names exhausted model + CLIProxyAPI rationale; None-safe (no fabricated alias). Golden-string test authored. |
| `--max-session-resets` flag 4-hop | 03 IP-10 (all 4 touch points confirmed) | commands.py @click.option (mirror --task-parallelism :202-209) → run() param → load_sprint_config call + DEF (config.py:281-298) → SprintConfig field (models.py); default 8. |
| doc⇆CLI parity | 05 §9.1 + §9.2 | TWO layers: help-surface (test_cli_contract.py) + guide-vs-Click (NEW test_sprint_docs_cli_parity.py mirroring tests/cli/reflect/test_docs_cli_parity.py); guide `docs/guides/sprint-cli-tools-release-guide.md` must gain a `--max-session-resets` option bullet w/ `Default: 8`. |
| 4-hop verified end-to-end | 03 IP-10 + 03 cross-cutting table | Consumption point: `SessionResetPolicy(max_session_resets=config.max_session_resets)` constructed per-phase, threaded into both per-task and single-session loops. |

**Notable correction / flag (COVERED+):** 01 §FILE 4 surfaces a genuine `needs_human_decision`-adjacent design fork — the spec says "parse ~/.aienv" but the existing Python convention (swarm/config.py) reads exported `os.environ`, and no Python in the repo parses the ~/.aienv FILE. Research presents design (A) os.environ reader [convention-consistent] vs (B) file parser [matches spec wording + testable fixture], recommends (A) with (B) as documented fallback. This is correctly NOT silently resolved (see Criterion 8). `IC_ALIASES` token is flagged Unverified (does not exist as a literal var in scripts/ic). No breadth gap; one Unverified sub-element correctly surfaced.

---

## Criterion 6 — P6 (execution-log events + nominator failure_class exclusion (G) + KNOWLEDGE.md)

**Spec requirement (§4 Layer 4 persistence, §4 (G), §7 P6):** emit `session_reset` / `account_exhaustion_halt` events to `execution-log.jsonl`; recovery nominator `failure_class == "provider_exhaustion"` exclusion (G); KNOWLEDGE.md note + telemetry.

**Verdict: PASS for events + nominator; PARTIAL for KNOWLEDGE.md (minor)**

| Sub-element | Covered by | Evidence | Rating |
|---|---|---|---|
| execution-log.jsonl events | 03 IP-5 (logging_.py:295-301 `_jsonl` emitter; mirror `write_task_complete`) | Two new SprintLogger methods (`write_session_reset`, `write_account_exhaustion_halt`); emit sites + `if logger is not None:` guard documented. | COVERED |
| nominator (G) failure_class exclusion | 03 IP-7; research-notes (G); 04 §4 (parallel theme) | Exclusion belongs in `ManualNominator.nominate` (recovery.py:160-161); CORRECTS research-notes: NO `DriftNominator` exists (only Nominator/ManualNominator/ReflectReportNominator). | COVERED+ |
| KNOWLEDGE.md note + telemetry | research-notes RECOMMENDED_OUTPUTS (none assigned); spec §7 P6 gate "Events emitted" | No research file gives a specific KNOWLEDGE.md insertion target/section. This is a low-risk mechanical doc append (P6 gate is "Events emitted", not "KNOWLEDGE.md"), but the builder lacks an explicit anchor. | PARTIAL (minor) |

**Notable correction (COVERED+):** 03 IP-7 corrects research-notes line 38 — there is **no `DriftNominator`** class; the "classification == drift" filter is a branch INSIDE `ReflectReportNominator.nominate`. The builder is pointed at the real symbols (ManualNominator for the (G) exclusion). 03 IP-7 also honestly flags the `context: dict` contents as UNVERIFIED — the builder must trace the `nominate(context=…)` call site before implementing the filter — and correctly ties (G) to the `needs_human_decision` HALT-on-nontrivial discipline.

**Minor gap (KNOWLEDGE.md):** No research file specifies where in KNOWLEDGE.md the note lands or what telemetry surface "telemetry" refers to beyond the two jsonl events. The P6 gate itself is satisfied by the events (covered), so this does not block synthesis — but the builder will author the KNOWLEDGE.md item without a research anchor. Classified MINOR (must still be fixed: a one-line research pointer or the builder reads KNOWLEDGE.md structure at build time).

---

## Criterion 7 — Output paths, granularity (per-file/per-test items), template rules (A3/B2/M3/I19/I22)

**Spec requirement (research-notes TEMPLATE_NOTES, §7 SoT):** the builder needs the correct template path, granularity rule (one item per file-edit / per-test / per-fixture), self-containment, and the QA encoding (M3 lens-based gates, I19/I22 agent minimums) sufficiently documented.

**Verdict: PASS — COVERED+**

| Sub-element | Covered by | Evidence |
|---|---|---|
| Correct template path | 06 §0 | CORRECTS the skill default: `.claude/templates/workflow/` does NOT exist in this worktree; authoritative file is `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md`. |
| A3 granularity (per-file/per-test/per-fixture) | 06 §2 (A3 L108); 01 SUMMARY per-symbol counts; 05 §5 per-test-item checklist | A3 documented; 01 gives a per-symbol edit count (one item each); 05 gives per-test/per-fixture item lists. research-notes TEMPLATE_NOTES already says "one item per file-edit / per-test / per-fixture, NOT 'implement P3' batch." |
| B2 self-containment (6 elements) | 06 §3 (B2 L159) + §8 verbatim B4/L1 examples | 6-element item shape quoted verbatim; the builder has the exact paragraph format. |
| M3 lens-based QA sequence | 06 §5 M3 (8 steps) | Full 8-step sequence documented with template line anchors. |
| I19/I22 agent minimums + intensity | 06 §5 (I15/I16/I17/I18/I19/I20/I21/I22) | Full intensity scaling tables; I22 lite/standard/full; I21 fidelity-gate applicability. |
| M4/I21 applicability call | 06 §5 builder mapping note | CORRECTLY scopes: this is a code-modifying task, so M4 source-fidelity gate is NOT required (I21); M3 lens gate IS required; I18 testing item required. |
| Output paths (phase-outputs, qa/) | 06 §5 M3 (`${TASK_DIR}phase-outputs/...`, `${TASK_DIR}qa/...`); 06 §6 PART 2 skeleton | Handoff file convention + qa report paths documented. |
| Frontmatter + POST reflect gate | 06 §1, §9 (start_commit/executor_model_class builder-injected; POST reflect penultimate FLAT wrapper) | research-notes start_commit (59b9e2a2b9f0) + executor_model_class (sonnet) supplied; POST_REFLECT_GATE ENABLED encoding documented (SKILL O1 emission, canonical one-liner). |

**Notable correction (COVERED+):** 06 §0 corrects the template path (the skill's documented default is wrong for this worktree) and 06 §9 correctly identifies that the POST reflect gate item is NOT in the template — it is injected by the task-builder SKILL — with `start_commit`/`executor_model_class` as builder-injected frontmatter. These are exactly the traps that would silently break the build. No gap.

---

## Criterion 8 — Unresolved / needs_human_decision items flagged (not silently assumed)

**Spec requirement (research-notes AMBIGUITIES (G); memory `feedback_human_decision_items_must_halt`):** the two deferred decisions — (a) aienv reader-vs-parser, (b) nominator (G) exclusion — must be flagged as encode-the-default-and-HALT-on-nontrivial items, NOT silently auto-resolved.

**Verdict: PASS — COVERED+**

| Deferred decision | Covered by | Evidence |
|---|---|---|
| (a) aienv os.environ-reader vs file-parser | 01 §FILE 4 design-decision callout; 01 SUMMARY finding 4; 05 §8.2 (injectable aienv_path) | Explicitly presented as `needs_human_decision`-adjacent: encode (A) os.environ reader + document (B) file-parse fallback; do NOT silently pick. Cross-referenced to `feedback_human_decision_items_must_halt`. |
| (b) nominator (G) failure_class exclusion | 03 IP-7 (G) deferred-decision; 04 §4; research-notes AMBIGUITIES (G) | Spec offers two options (P6 nominator-exclusion as default, OR scope contract #4 to live auto-path). Research instructs: encode the P6 exclusion as the default + document the fallback in item Context; if `context`-plumbing proves non-trivial, write PENDING finding + proceed with documented default — NOT silently pick. |
| Discipline reference | 02 Pattern F item 6; 01/03/research-notes | All cite memory `feedback_human_decision_items_must_halt` (write PENDING + halt the dependent mutation; never auto-apply a default that ships a behavior change unreviewed). |

**Additional Unverified items honestly surfaced (not assumed):** the research set flags several builder-must-close Unverified edges rather than fabricating answers — `decide` boundary `<` vs `<=` (05 §12); real ~/.aienv export format `T*Model0N` vs `IC_ALIASES` (01, 05); `run` Click subcommand symbol name (05); sprint guide internal heading structure (05 §9.2); `nominate(context)` dict contents (03 IP-7); new `reset_policy`/latch param name (05). These are correctly marked Unverified, not silently assumed — consistent with the breadth-without-fabrication standard.

**No silent assumptions detected.** Both spec-named deferred decisions are flagged with the correct HALT-on-nontrivial discipline. No gap.

---

## Cross-cutting checks

### File completeness / status
| File | Status line | Summary | Gaps/Unverified flagged | Rating |
|---|---|---|---|---|
| 01-file-inventory.md | Complete | Yes (SUMMARY) | Yes (6 corrections) | Complete |
| 02-patterns-conventions.md | **Header says "In Progress" (L2) but body ends "Status: Complete" (L205)** | Yes | Yes (Unverified section) | Complete-with-stale-header |
| 03-integration-points.md | Complete | Yes | Yes (5 corrections + UNVERIFIED context) | Complete |
| 04-data-flow-tracer.md | Complete | Yes | Yes (FINDING F-1) | Complete |
| 05-test-verification.md | Complete | Yes | Yes (UNVERIFIED list §12) | Complete |
| 06-template-examples.md | Complete | Yes | Yes (§1 Unverified resolved §9) | Complete |

**Minor flag:** 02 has a stale `**Status:** In Progress` at line 2 while line 205 declares `## Status: Complete` and the file is fully populated with a summary. Cosmetic only — the file IS complete. Recommend the header be corrected to Complete (does not block synthesis).

### Contradiction detection (surfaced, not resolved)
The research set is internally consistent on the BREADTH map. The notable cross-file **agreements that override the spec** (these are resolved corrections, not unresolved contradictions, and are surfaced here per protocol):
1. **executor.py:2103 diagnostic bundle** — 03 IP-3 and 04 F-1 BOTH contradict the spec's "no auto-remediation consumer" claim, and AGREE with each other (bundle fires on single-session path only). Convergent, not conflicting.
2. **`count_turns_from_stream_json` name** — 01/04/05 agree the monitor symbol is `count_turns_from_output`; the stream-json mirror lives in process.py. Convergent.
3. **No `DriftNominator`** — 03 IP-7 corrects research-notes; no other file contradicts. Convergent.

No unresolved cross-file contradiction was found. All three corrections converge and are the kind the builder must carry forward.

### Breadth-vs-depth note (lens scope)
This report is the BREADTH lens: every spec area (§4 Layers 1-5, §6 test plan, §7 P1-P6) maps to research coverage. Depth adequacy (whether each covered area is traced deeply enough for Deep tier) is the sibling depth-lens's job and is NOT graded here. Where I note "COVERED+", that reflects breadth-coverage plus a surfaced correction — not a depth judgment.

---

## Compiled gaps

### Critical gaps (block synthesis)
- **None.** All 6 phases (P1-P6) and all 8 breadth criteria have actionable research coverage with insertion points.

### Important gaps (affect quality)
- **None.** The two areas that could have been gaps (the diagnostic-bundle hazard and the aienv reader-vs-parser fork) are both covered AND correctly escalated/flagged.

### Minor gaps (must still be fixed)
1. **KNOWLEDGE.md anchor (P6).** No research file gives a specific KNOWLEDGE.md insertion section or defines the "telemetry" surface beyond the two jsonl events. The P6 gate ("Events emitted") is satisfied, so synthesis is not blocked, but the builder authors the KNOWLEDGE.md item without a research anchor. Fix: add a one-line pointer to the KNOWLEDGE.md structure, or have the builder Read KNOWLEDGE.md at build time. (Source: Criterion 6.)
2. **02 stale status header.** Line 2 says "In Progress" while the file is Complete (line 205). Cosmetic; correct the header. (Source: Cross-cutting / file completeness.)

### Builder-must-close Unverified edges (not gaps — correctly surfaced by research)
These are NOT breadth gaps (the area is covered); they are precise items the research honestly marked Unverified for the builder to close during implementation: `decide` boundary `<`/`<=`; real ~/.aienv export format (`T*Model0N` vs `IC_ALIASES`); `run` Click subcommand symbol; sprint guide heading structure; `nominate(context)` dict contents; `reset_policy`/latch param name. Listing here for builder visibility, not as completeness failures.

---

## Recommendations

1. **Proceed to synthesis / task-building.** Breadth coverage is complete; no critical or important gaps.
2. **Carry the three convergent corrections into the tasklist** so the builder does not re-trust the spec's stale premises: (a) executor.py:2103 fires a diagnostic bundle on the single-session path → P4 must guard it (option B1); (b) use `count_turns_from_output` / process.py mirror, not `count_turns_from_stream_json`; (c) target `ManualNominator` (no `DriftNominator`).
3. **Encode the two deferred decisions as needs_human_decision items** with the documented default + HALT-on-nontrivial (aienv design A; nominator (G) exclusion), per `feedback_human_decision_items_must_halt`.
4. **Address the two MINOR fixes** (KNOWLEDGE.md anchor; 02 status header) — neither blocks synthesis.
5. **Surface the Unverified edges in the relevant build items' Context** so the builder closes them at implementation time rather than fabricating.

---

VERDICT: PASS

**Rationale:** All 8 breadth criteria PASS. Every spec area (§4 Layers 1-5, §6 test plan, §7 phases P1-P6) maps to actionable research coverage with insertion points, and the research set additionally CORRECTED three spec/research-notes inaccuracies (the executor.py:2103 diagnostic-bundle hazard, the `count_turns_from_stream_json` misnomer, the non-existent `DriftNominator`) rather than propagating them. The two spec-named deferred decisions are correctly flagged as needs_human_decision items. Only two MINOR gaps remain (KNOWLEDGE.md anchor; a cosmetic stale status header in file 02), neither of which blocks synthesis. Per the protocol's "any gap = surface it" rule the two MINOR gaps are recorded, but they do not warrant a FAIL — they are non-blocking and have clear, low-cost fixes.

**Gap count:** 0 critical, 0 important, 2 minor.
