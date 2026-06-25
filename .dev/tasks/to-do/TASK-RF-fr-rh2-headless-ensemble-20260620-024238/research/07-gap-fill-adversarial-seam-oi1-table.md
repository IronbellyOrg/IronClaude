# Research (Gap-Fill): Adversarial Scoring Seam + OI-1 Provenance Table + PreflightResult

Status: Complete
Date: 2026-06-20

This gap-fill targets four research gaps found by the quality gate for FR-RH2
(sc:reflect Tier-2 ensemble via swarm dispatch library). Each claim cites file:line.
All citations re-verified against worktree source on 2026-06-20.

---

## GAP 1 (CRITICAL) — the `ensemble.py` → `/sc:adversarial` scoring seam

### 1.0 Headline conclusion (read first)

**`/sc:adversarial` is a Claude-inference SKILL, not an importable Python module.** There is NO
`src/superclaude/cli/adversarial*` module (verified: `find src/superclaude/cli -iname '*advers*'`
returns only `cli/eval/suites/adversarial_merge_consistency.yaml`, an eval YAML — no code module).
The only adversarial implementation is `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
(3003 lines), executed by a Claude agent via the Skill/Task tools, which it itself uses
(`allowed-tools: ... Task, Skill`, SKILL.md:4; Step 2 Round 1 dispatches advocate agents "via Task
tool", SKILL.md:1051).

**Therefore `ensemble.py` cannot "call `/sc:adversarial`" in-process.** Any path where the reflect
Python package obtains a real adversarial convergence score must route through a Claude inference
surface. Inside the reflect package the ONLY sanctioned inference launch is `ClaudeProcess`
(runner.py:11-12, NFR-7). This is the crux of GAP 1 and the spec/TDD under-specify exactly how the
score is obtained — see the OPEN DECISION in §1.6.

### 1.1 What the NFR-7 / no-nesting guard actually bans (precise scope)

The guard is `tests/cli/reflect/test_no_nesting_guard.py`. Two layers; Layer B governs the reflect
package. The exact banned/allowed surface:

| Banned token / pattern | Regex / literal | Scope | Citation |
|---|---|---|---|
| `Task(` | literal in `_NESTING_TOKENS` | `runner.py` (Layer B test) | test_no_nesting_guard.py:46, 99-102 |
| `subagent` / `subagent_type` | literal | `runner.py` | test_no_nesting_guard.py:99-102 |
| `import anthropic` / `from anthropic` | literal | `runner.py` | test_no_nesting_guard.py:99-102 |
| raw `subprocess.run(` / `subprocess.Popen(` / `Popen(` CALLS | `_RAW_SUBPROCESS_CALL_RE` (`\b(?:subprocess\.(?:run\|Popen)\|Popen)\s*\(`) | `runner.py` ONLY | test_no_nesting_guard.py:38, 128-142 |
| `import subprocess` | `_IMPORT_SUBPROCESS_RE` | `runner.py` ONLY | test_no_nesting_guard.py:39-41, 142 |
| `from\|import ... sprint\|roadmap` | `_SPRINT_ROADMAP_IMPORT_RE` | ALL `cli/reflect/*.py` | test_no_nesting_guard.py:29-31, 105-113 |
| `async def` / `await ` (anchored, real code) | `_ASYNC_DEF_RE` / `_AWAIT_RE` | ALL `cli/reflect/*.py` | test_no_nesting_guard.py:33-34, 116-125 |

**Key scoping facts:**
- `ClaudeProcess` is EXPLICITLY the sanctioned launch path: `assert "ClaudeProcess" in src`
  (test_no_nesting_guard.py:98, 136). The ban targets `subprocess.run`/`Popen`/`Task(` LITERALS, NOT
  `ClaudeProcess` (which internally wraps subprocess inside `cli/pipeline/process.py`, outside the
  reflect package and outside the guard's file set). runner.py:11-12 states the rule: "The only
  reflect-launch path is `ClaudeProcess` (subprocess) -- never an Agent/Task surface (NFR-7)."
- The raw-subprocess + agent-import bans currently scan ONLY `runner.py` (`_RUNNER_SRC`,
  test_no_nesting_guard.py:22). The sprint/roadmap-import + async bans scan ALL `*.py` in the package
  (`_REFLECT_PY`, test_no_nesting_guard.py:24). So a NEW `ensemble.py` is TODAY covered by the
  async/import bans but NOT by the `Task(`/`subprocess`/`anthropic` bans — FR-RH2.8 / TDD G8 / NFR-001
  require EXTENDING `_RUNNER_SRC`-style checks to `ensemble.py` (spec FR-RH2.8 AC; TDD NFR-001).
- The guard is purely a STATIC TEXT grep over source — it does not execute anything. So whatever
  `ensemble.py` does, it must not contain those literal tokens.

**Net:** `ensemble.py` calling swarm `dispatch_wave1` (plain sync `def`, HTTP workers via
`ParallelExecutor` — research 03 §1) is NFR-7-legal (no `Task(`, no `subprocess.*(`, no `anthropic`,
no async). Launching a `ClaudeProcess` from `ensemble.py` would ALSO be NFR-7-legal **provided** the
guard's raw-subprocess scan is not extended to forbid `ClaudeProcess` (it asserts presence, not
absence, of `ClaudeProcess`). The blocker for option (b) below is therefore NOT NFR-7 — it is that
the score must come from a Claude inference surface and the spec under-specifies which one.

### 1.2 How `runner.py` launches `ClaudeProcess` today (Tier-1 + the contract pin)

`_audit_once` (runner.py:392-428) is the single launch seam:
- `expected_tier = 2 if config.depth in {"standard","deep"} else 1` (runner.py:403).
- Builds ONE `ClaudeProcess(prompt=self._build_prompt(), output_file=.../reflect-stdout.json,
  error_file=..., model=config.model, timeout_seconds=..., max_turns=..., output_format="stream-json",
  env_vars={_WRAPPER_MARKER:"1"})` (runner.py:405-417).
- `proc.start(); rc = proc.wait()` (runner.py:418-419).
- `contract = parse_contract(config.contract_path)` (runner.py:420) — the child `/sc:reflect` is
  trusted to WRITE `config.contract_path` (the pinned `return-contract.yaml`); the wrapper only READS
  it. `derive_verdict(contract, expected_tier=..., ...)` (runner.py:421-426) maps it to a verdict.
- The prompt is `/sc:reflect --mode post --no-promote --diff <base> --tasklist <t> [--spec <s>]
  --depth <d> [--remediate] [--executor-model <m>] --output <out>` (`_build_prompt`, runner.py:341-366).

So TODAY the child `/sc:reflect` agent is the thing that is supposed to fan out the Tier-2 ensemble
AND run the adversarial merge AND write `adversarial_convergence_score` into the contract
(`pass.yaml` fixture hard-codes it at 0.86 — TDD §2.2). The defect: that in-process Task fan-out
cannot nest under `claude -p` (spec §1). `ClaudeProcess` is a reflect-package-local launch the ban
EXEMPTS (it is the mandated path); the ban is on `subprocess.run`/`Popen`/`Task(` literals.

### 1.3 `/sc:adversarial` Mode A INPUT/OUTPUT contract (the scorer)

Mode A is the path reflect uses (compare existing files). From SKILL.md:

**INPUT contract (Mode A):**
- Invocation: `/sc:adversarial --compare file1.md,file2.md[,...,fileN.md] [options]` (SKILL.md:29, 57).
- Accepts 2-10 existing files; copied to `<output>/adversarial/variant-N-original.md` (SKILL.md:63-64,
  389). 2-10 count enforced (SKILL.md:565-566).
- `--suspect-source <files>` is the suspect-aware flavor the bare-review precedent hands off to
  (sc-bare-review/SKILL.md:55: `/sc:adversarial --compare <existing>,<bare…> --suspect-source <bare…>`).
  (The adversarial SKILL's own flag table does not enumerate `--suspect-source` explicitly — it is the
  suspect-routing convention OI-4 flags as needing confirmation.)
- Common flags: `--depth {quick,standard,deep}` (default standard), `--convergence` (default 0.80),
  `--output` (SKILL.md:332-344).

**OUTPUT contract (the score):**
- `/sc:adversarial` writes a MANDATORY return contract on EVERY invocation (SKILL.md:425-445), as YAML:
  ```yaml
  return_contract:
    merged_output_path: "<path>"        # null if merge not reached
    convergence_score: 0.75             # float 0.0-1.0, null if debate not reached
    artifacts_dir: "<path to adversarial/>"
    status: "success"                   # success | partial | failed
    base_variant: "opus:architect"
    unresolved_conflicts: 2
  ```
  (SKILL.md:431-443). The score field is `convergence_score` (SKILL.md:435, 452).
- It is emitted by the agent into the return contract (SKILL.md:425-427: "sc:adversarial MUST write
  this return contract on every invocation, including failures"). The SKILL does NOT specify a fixed
  on-disk filename for the return contract — it is "returned" to the caller. When invoked headlessly
  via `claude -p`, the caller must instruct WHERE to write it (this is the under-specified seam).
- **Name mismatch to flag:** the adversarial SKILL emits `convergence_score` (SKILL.md:435); the
  reflect contract field is `adversarial_convergence_score` (contract.py:284). The mapping layer must
  rename `convergence_score` → `adversarial_convergence_score` (research 02 §7; research 03 §7 confirms
  the swarm seam never produces either name).

### 1.4 Precedent: `sc-bare-review` is a SKILL-driven (inference) handoff, NOT a Python call

This is the precedent the TDD says reflect mirrors (spec §2 / Decision row "Who scores"; TDD §1).
Reading `src/superclaude/skills/sc-bare-review/SKILL.md`:
- bare-review IS "a **thin caller over `superclaude swarm run --lens bare-review`**" and "a pure
  delegation target invoked as `Skill sc-bare-review …`" (sc-bare-review/SKILL.md:22-26). It is
  **inference-driven**: a Claude agent runs the skill.
- Its flow: shell out `superclaude swarm run --lens bare-review --target … --output … --transport
  openai_compat` (SKILL.md:35-39), then on success "`Read` `<output-dir>/return-contract.yaml` and
  relay it" (SKILL.md:43-45).
- It does NOT itself run `/sc:adversarial`. It emits a `recommended_next_command:
  "/sc:adversarial --compare <existing>,<bare…> --suspect-source <bare…>"` (SKILL.md:55) and the
  CALLING agent is expected to run that next. So in the bare-review precedent, **the swarm fan-out is
  CLI/Python (a subprocess), but the adversarial scoring is a SEPARATE downstream Claude-inference
  step run by the orchestrating agent — never a Python import.**
- `allowed-tools: Read, Bash` (SKILL.md:4) — bare-review itself has NO Task/Skill tool; it cannot run
  the adversarial merge. Confirms the merge is a SEPARATE caller-driven inference step.

**Consequence for reflect:** the precedent's "score" is produced by a Claude agent running
`/sc:adversarial`, not by Python. The TDD's "in-process library import" design (TDD §2.2, Decision
row "Swarm integration contract") imports the swarm FAN-OUT (`dispatch_wave1`/factory/`reduce_wave3`,
all sync `def`s — research 03) but the TDD does NOT show a corresponding in-process mechanism for the
adversarial SCORING step, because none exists in Python.

### 1.5 Contrast case: `roadmap/validate_executor.py` — adversarial-merge-as-a-ClaudeProcess-Step

The TDD calls this the "separate-process-per-agent" reference (spec §1.1, §9; TDD §2.2). Reading
`validate_executor.py:317-378`:
- `_build_multi_agent_steps` builds N parallel reflection `Step`s (one per agent, each a
  `claude` subprocess with `build_reflect_prompt` + `REFLECT_GATE`, validate_executor.py:341-362), then
  a SINGLE `merge_step = Step(id="adversarial-merge", prompt=build_merge_prompt([reflect_outputs]),
  output_file=.../validation-report.md, gate=ADVERSARIAL_MERGE_GATE, inputs=reflect_outputs)`
  (validate_executor.py:365-373).
- The merge is run as a `claude` SUBPROCESS step via `execute_pipeline()` + `ClaudeProcess`
  (validate_executor.py:7-8, 24, 88, 122 — "Reuses `execute_pipeline()` and `ClaudeProcess`";
  "Execute a single validation step as a Claude subprocess"). It is NOT a Python adversarial scorer
  and NOT the `/sc:adversarial` SKILL — it is an inline `build_merge_prompt` (validate_prompts.py:233-282)
  that instructs Claude to merge the reports and emit YAML frontmatter with
  `blocking_issues_count`/`warnings_count`/`tasklist_ready`/`validation_mode: adversarial`
  (validate_prompts.py:267-272). The "score" is parsed back from the report's frontmatter
  (`_parse_report_counts`, validate_executor.py:381-389) — NOT a `convergence_score`.

**This is the decisive precedent:** in roadmap-validate, the adversarial merge IS a separate
`ClaudeProcess` step driven by a prompt + a gate, and its result is parsed from the step's output
file. No Python module scores anything; a `claude` subprocess does, and Python reads the file.

### 1.6 SYNTHESIS — three candidate seams, NFR-7 legality, OPEN DECISION

Restating the three options from the brief, each grounded:

**Option (a): `ensemble.py` does ONLY swarm fan-out+reduce; `adversarial_convergence_score` is left
to the Tier-1/Tier-2 `/sc:reflect` `ClaudeProcess` child via its `return-contract.yaml`.**
- Mechanism: keep launching the `/sc:reflect` child (runner.py:405-419) for the grounded pass + verdict
  writeback; `ensemble.py` performs the swarm fan-out to produce N normalized per-reviewer artifacts;
  the child agent's `/sc:reflect` protocol consumes them and runs its OWN adversarial merge, writing
  `adversarial_convergence_score` into `config.contract_path`.
- NFR-7: LEGAL — no new launch surface; uses existing `ClaudeProcess`.
- Problem: this is essentially the BROKEN path. The whole defect (spec §1) is that the `/sc:reflect`
  child cannot nest Task to form the ensemble. If the child still owns the adversarial merge, the
  ensemble it merges must somehow be the swarm artifacts — which means the child would have to READ
  swarm's `t2-swarm/` outputs, violating the path-confinement invariant (spec §5.3 path_confinement:
  "reflect MUST NOT parse the t2-swarm/ subdir's contract directly"; TDD §5.4). Tenuous and contradicts
  the spec's own confinement rule. **Not well-supported.**

**Option (b): `ensemble.py` (or the runner) launches a SECOND `ClaudeProcess` running
`/sc:adversarial --compare <swarm final_paths> --suspect-source <...>` and parses its emitted
`convergence_score`.**
- Mechanism: exactly the `validate_executor` pattern (§1.5) + the bare-review handoff (§1.4) made
  headless: after `ensemble.py` reduces the swarm fan-out to N `final_path` artifacts, launch one more
  `ClaudeProcess` whose prompt is the `/sc:adversarial` Mode A invocation (or an inline merge prompt
  mirroring `build_merge_prompt`), pin its return-contract/report path, and parse
  `convergence_score` → `adversarial_convergence_score`.
- NFR-7: LEGAL provided the launch is via `ClaudeProcess` (the sanctioned path; the guard asserts
  `ClaudeProcess` presence and bans only `subprocess.*(`/`Task(`/`anthropic` literals — §1.1). A
  `/sc:adversarial` child that itself uses Task internally is fine: the ban is a STATIC grep of the
  REFLECT package source, and the child's Task usage lives in the SKILL, not in `ensemble.py`. And a
  top-level `claude -p /sc:adversarial` CAN nest Task (it is the top-level agent, exactly like the
  Tier-1 child) — the nesting defect only bit the DOUBLY-nested `claude -p → /sc:reflect Task-worker →
  Task` path (spec §1). A fresh `claude -p /sc:adversarial` is single-level and nests fine.
- Satisfies: FR-RH2.3 (adversarial merge produces a convergence score recorded on the reflect
  contract — spec FR-RH2.3 AC3), the §2.2 flow step (3) "/sc:adversarial (Mode A) … adversarial merge
  verdict + convergence score", and phase_c_to_d `adversarial_convergence_score` (spec §5.3).
- Cost: adds a SECOND `ClaudeProcess` per audit (latency + credits; the `--fix` loop multiplies it —
  spec §7 last risk row). But it is the only option that produces a REAL convergence score headlessly.
- **This is the best-supported seam.** It is the literal union of the two cited precedents
  (validate_executor's ClaudeProcess-merge-step + bare-review's `/sc:adversarial` handoff), it
  respects path-confinement (ensemble.py consumes `t2-swarm/` artifacts and the adversarial child
  writes the reflect-side score), and it is NFR-7-legal.

**Option (c): score left `None` at the swarm layer; the existing `derive_verdict` null-convergence
trigger handles it.**
- Mechanism: `ensemble.py` synthesizes the contract with `adversarial_convergence_score: None`;
  contract.py:284 trigger 11 (`tier_reached == 2 and adversarial_convergence_score is None →
  "null-convergence"`) routes DEGRADED.
- NFR-7: LEGAL (no launch at all).
- Problem: this means EVERY Tier-2 run DEGRADES (exit 11) on null-convergence — it can NEVER PASS.
  That directly violates FR-RH2.4 AC ("On a successful Tier-2 run, `tier_reached == 2`" with a real
  merge) and FR-RH2.5 (the stub test asserts a faithful PASS-eligible run). **Disqualified as the
  steady-state design** — though it IS the correct FALLBACK when the adversarial child fails (graceful
  degrade rather than crash). Note spec §5.3 phase_c_to_d explicitly marks
  `adversarial_convergence_score` as "recorded TELEMETRY at tier 2, NOT a pass gate (a low score alone
  does not fail a PASS)" — but `None` (absent) is a DEGRADE trigger, distinct from a low float. So the
  ensemble MUST produce a non-None score to PASS, which requires option (b).

**RECOMMENDED SEAM: Option (b)** — `ensemble.py`/runner launches a second `ClaudeProcess` running the
adversarial Mode A merge over the swarm `final_path` artifacts and parses `convergence_score` into
`adversarial_convergence_score`; option (c)'s null-convergence path is the graceful fallback when that
child fails.

**OPEN DECISION (must be surfaced as a human-decision item in the task):** The spec and TDD genuinely
**under-specify this seam.** Evidence of under-specification:
- The TDD's data-flow (spec §2.2 step 3, TDD §6.1 diagram) draws `/sc:adversarial` as a downstream box
  but never states HOW a Python driver invokes a Claude-only skill headlessly. TDD §4.1 lists
  `ensemble.py` deps as `dispatch_wave1`/`_resolve_run_transport_factory`/`reduce_wave3` — all swarm
  FAN-OUT symbols — with NO adversarial-scoring dependency listed.
- spec OI-4 ("How does `/sc:adversarial` Mode A treat `suspect:true` reflect-review artifacts") is
  flagged Low-Medium and unresolved.
- The spec's NFR-7 reconciliation (spec §9) only argues that the swarm HTTP fan-out is out of NFR-7
  scope; it is SILENT on whether a second `ClaudeProcess /sc:adversarial` is launched and from where
  (`ensemble.py` vs `runner.py`).
- Whether the adversarial merge runs as the literal `/sc:adversarial` SKILL (SKILL.md Mode A) or an
  inline `build_merge_prompt`-style prompt (validate_executor pattern) is a real design fork with
  different test surfaces and is not decided.

The task should encode this as a **`needs_human_decision` item**: "Decide the adversarial-scoring
launch seam for headless Tier-2: (b1) second `ClaudeProcess /sc:adversarial --compare … --suspect-source`
launched from `ensemble.py`/`runner.py`, parsing `convergence_score`; vs (b2) an inline
`build_merge_prompt`-style `ClaudeProcess` merge step mirroring `validate_executor`. Confirm WHERE the
launch lives (ensemble.py vs runner.py — note `_RAW_SUBPROCESS_CALL_RE` only scans `runner.py` today;
either is NFR-7-legal via `ClaudeProcess`), the on-disk path the adversarial child writes its return
contract to (so `ensemble.py` parses `convergence_score`), and the fallback when the child fails
(option (c) null-convergence DEGRADE)." Per `feedback_human_decision_items_must_halt`, this must HALT
the dependent spec/gate mutation, not auto-default. This is the single largest residual risk in
FR-RH2 and it is an architecture decision, not a wiring detail.

---

## GAP 2 (MINOR) — minimal `PreflightResult` construction for `dispatch_wave1`

`dispatch_wave1(preflight_result: PreflightResult, ...)` reads EXACTLY ONE field off the
PreflightResult: `workers_requested = preflight_result.manifest.preflight.workers_requested`
(dispatch.py:412). Nothing else on the PreflightResult is touched by `dispatch_wave1` (the rest of the
function uses `transport`/`transport_for_slot`/`prompt`/`worker_spec`/`parallel_executor`/`logger` —
dispatch.py:409-508, research 03 §1).

**`PreflightResult` dataclass (preflight.py:239-263):**
```python
@dataclass
class PreflightResult:
    manifest: Manifest
    state: SwarmState
    manifest_path: Optional[str] = None
    caller_metadata: CallerMetadata = field(default_factory=lambda: CallerMetadata())
```
Only `manifest` and `state` are required positionally; `manifest.preflight.workers_requested` is the
single load-bearing path for dispatch.

**Two minimal-construction options:**

1. **Synthetic construction (precedent exists).** The resume path in `commands.py` already builds a
   synthetic `PreflightResult` for re-dispatch (commands.py:2415-2427):
   ```python
   synthetic_manifest = _Manifest(
       contract_version=..., job_id=...,
       resolved_lens_entry=resolved_lens_entry_for_dispatch,
       preflight=_PreflightSummary(
           target_checksum=...,
           workers_requested=len(remaining_indices),   # <-- the only field dispatch reads
           transport_kind=resolved_transport_kind,
       ),
   )
   synthetic_state = _SwarmState(state="preflight_ok", job_id=...)
   synthetic_preflight = _PreflightResult(manifest=synthetic_manifest, state=synthetic_state)
   ```
   `ensemble.py` can mirror this: build a `Manifest` whose `.preflight.workers_requested == reviewers`,
   a `SwarmState(state="preflight_ok", job_id=...)`, and a `PreflightResult(manifest=..., state=...)`.
   This is the lightest path and needs no real target file.

2. **Real `run_preflight`.** `run_preflight(...)` (preflight.py, used by `swarm run` at
   commands.py:1761) does full Wave-0 (target checksum, manifest emit) and returns a real
   `PreflightResult`. Heavier (needs a real target path/lens job) — appropriate only if `ensemble.py`
   wants the manifest.json side effects. For the reflect fan-out (per-reviewer BRIEFS as prompt, not a
   target file), the synthetic construction (#1) is the minimal correct choice.

**Note:** `ModelPoolTooSmallError` is raised by `_resolve_run_transport_factory(...,
workers_requested=N)` (commands.py:687-688), NOT by `dispatch_wave1`, so the pool guard is independent
of the PreflightResult — `ensemble.py` passes `workers_requested` to BOTH the factory (for the guard)
and via the synthetic PreflightResult (for dispatch's slot count). These two N values must agree.

---

## GAP 3 — explicit OI-1 provenance table (one row per reflect verdict-driver field)

Left column = the fields `derive_verdict` + helpers read (research 02 §7). Provenance = exactly one of
{MAPPED (from a swarm `ResultContract`/`WorkerResult` field), DERIVED (computed from swarm raw facts),
SYNTHESIZED (no swarm source — `ensemble.py` constructs)}. Research 03 §7 CONFIRMED (grep exit 1) that
NONE of `tier_reached`/`merge_method`/`t2_model_class_diversity`/`t2_vendor_diversity`/`reviewer_count`/
`adversarial_convergence_score` appear in the swarm seam; the ONLY shared key is `status` (different
semantics). Swarm `ResultContract` fields: research 03 §6b (models.py:997-1015). `WorkerResult` fields:
research 03 §6a (models.py:1117-1128).

| # | Reflect contract field | Read at (contract.py) | Provenance | Swarm source / derivation rule |
|---|---|---|---|---|
| 1 | `contract_version` | :166 (BLOCKED gate; must be "1.x") | SYNTHESIZED | swarm `ResultContract.contract_version` is also "1.0" (models.py:997) but semantics differ; ensemble must SET reflect's `"1.0"` literal — do NOT pass swarm's through blindly. Same VALUE, different contract → SYNTHESIZED. |
| 2 | `status` | :235 PASS gate; :311,:313 halted; `_make_result`:118 | DERIVED | swarm `ResultContract.status` (models.py:998) is IMM-5 worker-count `success\|partial\|failed` (M/N), NOT reflect's deviation-taxonomy status. ensemble DERIVEs reflect `status` from M (e.g. M≥2 distinct → `success`; M==0 → drive BLOCKED). Same key, different domain (research 03 §7). |
| 3 | `tier_reached` | :195; :235 PASS; degraded trig 6 & 11; `_make_result`:116 | DERIVED | No swarm field. DERIVE: `2` when M≥2 with ≥2 distinct classes (faithful), else `1` (M==1 single-reviewer fallback per FR-RH2.9). |
| 4 | `degraded_components` (list) | :184 (shape-guard; trig 1-5) | SYNTHESIZED | No swarm equivalent. ensemble emits `[]` unless surfacing a chain-critical loss; default `[]`. |
| 5 | `deviation_count_by_class` (4 keys) | `_extract_deviations`:92; `_make_result`:122; halted:323-326 | SYNTHESIZED | Deviation taxonomy is the adversarial/reflect domain, absent from swarm. From the GAP-1 merge child or `{}` (→ all 0). |
| 6 | `report_path` | `_make_result`:119 | MAPPED/DERIVED | Map from swarm `ResultContract.merged_path` (models.py:1012) or the adversarial child's report path. (Telemetry only; not a verdict driver.) |
| 7 | `remediation_task_path` | `_make_result`:126 | SYNTHESIZED | Authored by the `/sc:reflect --remediate` child, not swarm. `None` in the swarm path unless a merge/reflect child writes one. |
| 8 | `regression_present` (bool) | :315; `_LOAD_BEARING_BOOL`:200 | SYNTHESIZED | Adversarial/reflect-domain finding. From the merge child or omitted (absent → no trigger). |
| 9 | `unauthorized_deviation_present` (bool) | :317; :200 | SYNTHESIZED | Same as #8. |
| 10 | `needs_human_decision` (bool) | :319; :200; `classify_fix`:358 | SYNTHESIZED | Same as #8 (grounding-gaps domain). |
| 11 | `user_decision_required` (bool) | :321; :200 | SYNTHESIZED | Same as #8. |
| 12 | `adversarial_unavailable` (bool) | :276; :200 | DERIVED | Set `True` when the GAP-1 adversarial child could not run (→ `adversarial-unavailable` degrade). DERIVED from the adversarial-launch outcome, not swarm. |
| 13 | `input_drift_detected` (bool) | :301; :200 | SYNTHESIZED | reflect-domain; omit (absent → no trigger). |
| 14 | `verification_ran` (bool) | :288; :200 | SYNTHESIZED | reflect-domain; omit/set per the reflect child, not swarm. |
| 15 | `verification_skip_reason` | :289 | SYNTHESIZED | paired with #14. |
| 16 | `t2_model_class_diversity` | :267 (trigger 7) | DERIVED | DERIVE from distinct `WorkerResult.model_id` of the M SUCCEEDED workers (models.py:1122; status=="success" only). `"full"` when distinct-class count ≥ expected (FR-RH2.4/NFR-RH2.5); else non-`"full"` → degrade. **The core diversity fix.** |
| 17 | `t2_vendor_diversity` | :272 (trigger 8) | DERIVED | DERIVE from the vendor of each succeeded `model_id` (proxy pool). `"single"` → single-vendor degrade unless `--allow-single-vendor`. |
| 18 | `merge_method` | :280 (trigger 10) | DERIVED | DERIVE: `"single-reviewer-fallback"` when M==1 (→ degrade); else the adversarial method (e.g. `"adversarial"`) from the GAP-1 merge child. Per FR-RH2.4/§5.3. |
| 19 | `adversarial_convergence_score` (float\|None) | :284 (trigger 11; only when tier_reached==2) | MAPPED (from GAP-1 child) / DERIVED | NOT in swarm (research 03 §7). MAPPED from the adversarial child's `convergence_score` (sc-adversarial SKILL.md:435) — renamed `convergence_score`→`adversarial_convergence_score`. `None` only on adversarial failure (→ null-convergence degrade). **Depends on GAP-1 option (b).** |
| 20 | `citations_dropped` (int) | :295 (trigger 13) | SYNTHESIZED | reflect-domain; omit (→ 0). |

**Provenance tally:** MAPPED-ish: #6 (report_path), #19 (convergence — via the GAP-1 child, not swarm).
DERIVED from swarm raw `WorkerResult`/M facts: #2 status, #3 tier_reached, #12 adversarial_unavailable,
#16 model_class_diversity, #17 vendor_diversity, #18 merge_method (6 fields). SYNTHESIZED (no swarm
source; ensemble constructs `[]`/`{}`/omit/literal): the remaining ~12 (#1, #4, #5, #7, #8, #9, #10,
#11, #13, #14, #15, #20). **This sizes the `ensemble.py` mapping layer: ~6 fields derived from M /
distinct model_ids, 1-2 from the adversarial child, the rest synthesized as inert defaults.** Cross-ref
TDD §8.3 / OI-1 (spec §11): the table confirms the mapping layer is small and that the heavy lifting is
DERIVING diversity/tier/merge_method from the M succeeded `WorkerResult.model_id`s — exactly the swarm
facts that exist. `adversarial_convergence_score` is the one field requiring the GAP-1 seam to be
resolved before it can be populated (hence OI-1 is the BLOCKING GATE in spec §11).

---

## GAP 4 (MINOR) — retry/backoff anchor

The retry-once-on-5xx-with-2s-backoff is implemented in `retry_policy` (dispatch.py:195-276), called
per slot via `_run_worker` (dispatch.py:309). Precise anchors:

- **Defaults** `on_5xx=True` / `on_5xx_backoff_sec=2` / `on_4xx=False` / `on_timeout=False`:
  documented at dispatch.py:45-49 and dispatch.py:224 (the `WorkerSpec.retry` default matrix). These
  are the values TDD §12.4/§17.2 cite.
- **5xx → retry decision:** `if first.status == "proxy_error": bucket = _classify_http_code(...); if
  bucket == "5xx" and retry.on_5xx: should_retry = True` — dispatch.py:250-253.
- **Backoff slept BEFORE the single retry:** `backoff = max(0, retry.on_5xx_backoff_sec); if backoff >
  0: sleep_fn(backoff)` — **dispatch.py:269-271**. The second attempt is issued immediately after:
  `second = _send_once(transport, prompt, timeout_sec); second.attempts = 2` — dispatch.py:273-274.
- **Single retry only:** `attempts` is stamped to `2` on the 5xx branch (dispatch.py:274); there is no
  loop — exactly one retry. `sleep_fn` is injectable (`sleep_fn: Callable[[float], None] =
  time.sleep`, dispatch.py:200) so a test can record the backoff call without real sleeping.

**Anchor for any retry test:** assert `sleep_fn` is called once with `2` (the backoff) and
`result.attempts == 2` on a 5xx-then-success sequence → dispatch.py:269-274. 4xx/network/timeout do
NOT retry (dispatch.py:254-259).

---

## SUMMARY

**(a) Recommended adversarial seam + human-decision item.** `/sc:adversarial` is a Claude-inference
SKILL with no Python module (`find` returns only an eval YAML). The reflect package can only obtain a
real `adversarial_convergence_score` via a Claude inference surface, and inside the package that is
`ClaudeProcess` (the sanctioned path; the NFR-7 guard bans `subprocess.run`/`Popen`/`Task(`/`anthropic`
LITERALS, asserts `ClaudeProcess` PRESENCE, and scans the raw-subprocess ban only over `runner.py`).
**Recommended = Option (b): launch a SECOND `ClaudeProcess` running `/sc:adversarial` Mode A (or an
inline `build_merge_prompt`-style merge, mirroring `validate_executor.py:365-373`) over the swarm
`final_path` artifacts, parse `convergence_score` → `adversarial_convergence_score`; option (c)
null-convergence DEGRADE is the graceful fallback.** This is the union of the two cited precedents
(bare-review's `/sc:adversarial` handoff is inference-driven, sc-bare-review/SKILL.md:55;
validate_executor's merge is a `ClaudeProcess` Step). **YES — this REQUIRES a `needs_human_decision`
item**: the spec/TDD genuinely under-specify the seam (TDD §4.1 lists only swarm fan-out deps; spec §9
NFR-7 reconciliation is silent on a second adversarial child; OI-4 unresolved). Per
`feedback_human_decision_items_must_halt`, encode it as a HALTing decision, not an auto-default.

**(b) OI-1 provenance table** rendered above (20 rows): ~6 fields DERIVED from M / distinct succeeded
`WorkerResult.model_id`s (status, tier_reached, model/vendor diversity, merge_method,
adversarial_unavailable), 1-2 MAPPED from the GAP-1 adversarial child (report_path, convergence_score),
the remaining ~12 SYNTHESIZED as inert defaults (`[]`/`{}`/omit/literal `"1.0"`). All swarm
verdict-driver fields CONFIRMED ABSENT (research 03 §7, grep exit 1).

**(c) PreflightResult minimal construction.** `dispatch_wave1` reads ONLY
`preflight_result.manifest.preflight.workers_requested` (dispatch.py:412). `PreflightResult` =
`@dataclass(manifest, state, manifest_path=None, caller_metadata=...)` (preflight.py:239-263). Mirror
the existing synthetic construction at commands.py:2425-2427 (Manifest with
`preflight.workers_requested == reviewers` + `SwarmState(state="preflight_ok")`); the `T2Model0N` pool
guard (`ModelPoolTooSmallError`) is independent, raised by `_resolve_run_transport_factory(...,
workers_requested=N)` (commands.py:687-688) — pass the same N to both.

**(d) Retry anchor.** retry-once-on-5xx with 2s backoff: defaults `on_5xx=True`/`on_5xx_backoff_sec=2`
at dispatch.py:45-49/224; backoff slept BEFORE the single retry at **dispatch.py:269-271**; second
attempt + `attempts=2` at dispatch.py:273-274; `sleep_fn` injectable at dispatch.py:200.
