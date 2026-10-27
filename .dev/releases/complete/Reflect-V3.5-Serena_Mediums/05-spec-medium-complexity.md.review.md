# spec-panel critique — `05-spec-medium-complexity.md`

- **Mode**: critique · **Focus**: correctness, architecture, compliance, testing · **Format**: detailed · **Iterations**: 1
- **Panel**: Nygard (correctness lead), Fowler, Newman, Hohpe, Wiegers, Adzic, Crispin, Gregory, Hightower, Whittaker (adversarial)
- **Reviewed**: 2026-06-01

## Findings count by severity

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| MAJOR | 7 |
| MINOR | 3 |

---

## === CORRECTNESS ANALYSIS ===

### CRITICAL

**C1 — `execute_shell_command` verb-allowlist is provably bypassable under `shell=True` (Whittaker: Sentinel Collision + Divergence Attack; Nygard).**
FR-4's safety envelope (control a) checks `cmd_tokens[0]` — the *first verb*. But the matrix itself documents that Serena runs `subprocess.Popen(command, shell=True)` with no sandbox (`02-matrix:236,247`). Under `shell=True`, a command whose first token is allowlisted still executes shell metacharacters.

> **I can break this specification by Sentinel Collision Attack.** The invariant at FR-4 control (a) "verb allowlist — first token ∈ {pytest,...}" fails when the command contains a shell separator. **Concrete attack**: `command = "pytest tests/ ; rm -rf src/"`. State trace: `cmd_tokens[0] == "pytest"` → allowlist check PASSES → `verify_blocked` stays false → the wrapped string `timeout 120 pytest tests/ ; rm -rf src/` is passed to `execute_shell_command` → `shell=True` parses `;` → `rm -rf src/` executes. The no-mutation denylist (control d) is a *blacklist* and cannot enumerate every mutation form (`&&`, `|`, `$(...)`, backticks, `>`-redirect, `python -c`). A first-token allowlist + a mutation blacklist is the classic allowlist-bypass-by-composition hole.

**Severity**: CRITICAL (specification is provably wrong — the stated envelope does not contain the hazard it claims to). **Priority**: High.
**Recommendation**: Require the command be (i) constructed from a fixed allowlisted-verb *template* with arguments passed as a vetted token list — never assembled from spec/tasklist prose — AND (ii) **rejected outright if it contains any shell metacharacter** (`; | & $ \` > < newline`) unless explicitly tokenized; AND (iii) invoked with `cwd` scoping as defense-in-depth. The envelope must validate the *whole command structure*, not just the first token. This is the single most important correctness fix in the spec.

**C2 — Non-zero exit code ≠ Regression: `verification_regressions_detected` conflates distinct failure classes (Whittaker: Divergence Attack; Nygard guard-boundary).**
FR-4.3 maps "non-zero exit on a tasklist-claimed-passing file" → `verification_regressions_detected ≥ 1` → `regression_present: true` → blocks §14.5.2 promotion. But exit codes are not a binary pass/regression signal.

> **I can break this specification by Divergence Attack.** The invariant "non-zero exit ⟹ regression" fails at the boundary between failure classes. **Concrete attack**: `ruff check` returns exit 1 for a *style* finding (not a behavioral regression); `pytest` returns exit 2 for a *collection error* (missing import in a sibling file, not the work-unit's regression); exit 5 = "no tests collected" (the test file the tasklist claimed it added does not exist — a Drift/coverage gap, NOT a Regression); exit 124 = timeout (already special-cased in FR-4.6, but it would also satisfy "non-zero"). Mapping all of these to `regression_present: true` produces **false-positive regressions that block legitimate promotions**, and mis-classifies a Drift (exit 5) as a Regression — violating the §10.5 precedence (Regression > Drift) by assignment, not by evidence.

**Severity**: CRITICAL (the classifier is provably wrong for ≥3 common exit codes and corrupts the deviation taxonomy). **Priority**: High.
**Recommendation**: Define a per-tool exit-code → deviation-class mapping. At minimum: `pytest` exit 1 = test failure → Regression candidate; exit 2/3 = collection/internal error → Grounding Gap (not Regression); exit 5 = no-tests-collected → Drift/coverage; `ruff`/`mypy` exit 1 = lint/type finding → feeds `S_dev_density`, NOT `regression_present`; exit 124 = timeout → Grounding Gap. Add an FR acceptance criterion and an OQ for the full table.

### MAJOR

**M-COR1 — State-machine invariant for the verify-state is implicit (Wiegers correctness shift; Nygard).**
FR-4 introduces a multi-valued verification lifecycle (`not-run` → `blocked` → `ran-pass` → `ran-fail` → `timeout` → `skipped`) but never states the invariant that exactly one terminal state holds per invocation, nor the initial value. Under correctness focus this must be explicit. See the **State Variable Registry** and **Guard Condition Boundary Table** below (mandatory artifacts, produced).

**M-COR2 — Verification side effects can trip the `input_tree_sha256` drift guard → spurious STOP (Whittaker: Sequence Attack; Nygard).**
Step 5.5 runs *before* the Wave 5 drift re-check (SKILL.md:193 recomputes `input_tree_sha256`; any modified file → STOP `status: partial`). `pytest` legitimately writes `.pyc`, `.pytest_cache/`, `.coverage`, fixtures — inside the work-unit tree, which is part of the input-hash tree (SKILL.md:174 item 4). 

> **I can break this specification by Sequence Attack.** Step 5.5 `pytest` writes `.pytest_cache/` into the work-unit dir → Wave 5 recomputes `input_tree_sha256` → mismatch → `input_drift_detected: true` → STOP. A *successful* verification run aborts the skill.

**Recommendation**: Either (a) exclude well-known build/test artifacts (`__pycache__`, `.pytest_cache`, `.coverage`, `*.pyc`) from the input-tree hash, or (b) run verification with artifacts redirected/`cwd` to a scratch dir, or (c) snapshot-and-restore the tree around step 5.5. Add an FR criterion + OQ. **Resolve before merge** — this is a guaranteed-failure interaction, not a corner case.

---

## === ARCHITECTURE ANALYSIS ===

### MAJOR

**M-ARC1 — `verify_invocations[]` inline array violates the fixed per-step audit-row schema (Fowler; Newman).**
SKILL.md:124 defines the audit row as a fixed 5-field shape `{wave, step, timestamp, outcome, evidence_ref}`. FR-4.1 emits a `verify_invocations[]` array of objects *into* `audit.log`. This breaks the audit-granularity contract. **Recommendation**: write the per-invocation array to `<output>/verify-logs/invocations.yaml` and reference it via the audit row's `evidence_ref` field; keep only scalar counts in telemetry. Align with the low-spec's pattern of `_path` contract fields.

**M-ARC2 — Handoff memory namespace escapes the retention sweep → unbounded accumulation (Whittaker: Accumulation Attack; Fowler).**
FR-3 introduces `reflect/handoff-{slug}-{timestamp}`. The low-spec's FR-RV3-LOW.8 retention sweep filters only `reflect/last-pass-*` and `reflect/deviation-patterns-*` prefixes (per low-spec §3 FR-8). The new `reflect/handoff-*` namespace is **never pruned** — every `--remediate` run leaks one timestamped memory forever.

> **Accumulation Attack**: N `--remediate` runs → N orphaned `reflect/handoff-*` memories, none covered by any retention loop.

**Recommendation**: Extend the FR-RV3-LOW.8 sweep prefix set to include `reflect/handoff-*` (co-design note already calls for a shared `reflect/<category>-<slug>[-<timestamp>]` convention — make the sweep cover it). Add an FR-3 criterion. Cross-spec coordination item.

**M-ARC3 — The "minimal inline `get_current_config` probe" (OQ-M5) has no defined contract (Newman; Fowler).**
Three of four FRs depend on the low-spec FR-7 substrate; the fallback "minimal inline probe" is named but its return shape, fields, and the reconciliation semantics at low-spec merge are undefined. A load-bearing dependency cannot be left as a bare OQ. **Recommendation**: define the minimal probe's required fields (`backend`, `execute_shell_command_available`, `onboarding_available`, `read_only`) in §5 so FR-1/2/4 have a stable contract regardless of merge order. Keep the *resolution* in OQ-M5 but pin the *interface* in the spec body.

### MINOR

**m-ARC1 — `hierarchy_coverage_pct` numerator/denominator undefined (Wiegers measurability).** FR-1.3 emits the field with no formula. Define it (e.g. `registered_subtypes / total_subtypes_in_hierarchy`) or mark `null` semantics explicitly.

---

## === COMPLIANCE ANALYSIS ===

### MAJOR

**M-CMP1 — `onboarding` has no context-budget cap despite a documented context-exhaustion hazard (Hightower; Nygard; Whittaker: Accumulation).**
NFR-3 excludes onboarding from the token cap and says "measured separately" — but the matrix flags onboarding as consuming enough context to "fill up the context window" (`02-matrix:122`) and recommends switching conversations after it. The spec sets no ceiling and no abort. **Recommendation**: add an NFR giving onboarding a hard context/turn budget with a `onboarding_budget_exceeded` abort that degrades to "not bootstrapped" rather than starving the reflection waves. Compliance with the skill's own §15 hard-kill-at-1.25× convention.

**M-CMP2 — Flaky / non-deterministic verification produces false regressions that block promotion (Crispin; Nygard).**
A flaky test failing once → `regression_present: true` → promotion blocked → operator friction, and worse, an *intermittent* false gate. No retry/quarantine policy is specified. **Recommendation**: specify single-retry-on-failure for verification commands (or a `verify_flaky_suspected` flag when a retry flips the result), and document that flakiness degrades to a Grounding Gap, not a hard Regression. Pairs with C2's exit-code taxonomy.

---

## === TESTING ANALYSIS ===

### MAJOR

**M-TST1 — The most important safety test (injection bypass) is not enumerated (Crispin; Gregory; Whittaker).**
§8.1 `serena-execute-verify` lists "allowlist block" and "no-mutation deny" but not the C1 composition-bypass (`pytest ; rm`, `pytest && curl`, `$(...)`, redirect). The envelope's headline guarantee is untested. **Recommendation**: add explicit eval assertions for each metacharacter bypass class; this becomes the gating test for FR-4.

### MINOR

**m-TST1 — FR-4 description mis-couples verification to `--with-hierarchy` (clarity).** FR-4's description says "UC-1 opt-in via `--with-hierarchy`-style gate is out of scope" — `--with-hierarchy` is `type_hierarchy`'s flag (FR-1), not verification's. Reword to avoid implying a coupling.

**m-TST2 — frontmatter `quality_scores` are self-assigned, not derived (Wiegers).** Acceptable for a draft; note they are provisional pending this review.

---

## Mandatory Correctness Artifacts

### State Variable Registry (FR-15.1)

| Variable Name | Type | Initial Value | Invariant | Read Operations | Write Operations |
|---------------|------|---------------|-----------|-----------------|------------------|
| `verification_state` | enum{not-run, blocked, ran-pass, ran-fail, timeout, skipped} | `not-run` | exactly one terminal state per invocation; `ran-fail`⟺exit≠0∧mapped-to-regression | §10.4 Regression detector; §5.3 rule-3 escalation; §14.5.2 cond 4 | step 5.5 per command |
| `verification_regressions_detected` | int ≥ 0 | `0` | monotonic non-decreasing within a run; `>0 ⟹ regression_present` | §14.5.2 promotion gate (:1097) | step 5.5 on regression-classified exit |
| `regression_present` | bool | `false` (existing, SKILL.md:557) | `true` once set within run (latch); consumed by sc-troubleshoot (:626) | promotion gate; consumer field map | step 5.5; §10.4 |
| `onboarding_ran` | bool | `false` | `true` only after a real `onboarding()` call attempt | §9.1 contract | step 0.7b |
| `hierarchy_backend` | enum{jetbrains,lsp,none,lsp-disabled} | (from Wave 0 probe) | fixed for the run after Wave 0 | step 4.5 gate; 1B.3 | Wave 0 probe |
| `handoff_memory_key` | str \| null | `null` | non-null ⟹ memory exists at that key OR `handoff_persist_failed` | task-builder handoff | Wave 6 |

### Guard Condition Boundary Table (hard gate — complete)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| verb-allowlist | FR-4 (a) | Zero/Empty | `command=""` | first-token=`""`∉allowlist | `verify_blocked` (empty verb) | OK |
| verb-allowlist | FR-4 (a) | One/Minimal | `"pytest"` | true | invoke | OK |
| verb-allowlist | FR-4 (a) | Typical | `"pytest tests/"` | true | invoke | OK |
| verb-allowlist | FR-4 (a) | Sentinel Collision | `"pytest ; rm -rf src"` | first-token=`pytest`→true | **invokes; `;` chain runs** | **GAP (C1)** |
| verb-allowlist | FR-4 (a) | Sentinel Collision | `"pytest && curl evil"` | true | **invokes; `&&` chain runs** | **GAP (C1)** |
| verb-allowlist | FR-4 (a) | Legitimate Edge | `"uv run pytest"` | true (`uv`∈list) | invoke | OK |
| exit→regression | FR-4.3 | Zero | exit `0` | not regression | no flag | OK |
| exit→regression | FR-4.3 | One/Minimal | exit `1` (pytest fail) | regression | `regression_present` | OK |
| exit→regression | FR-4.3 | Divergence | exit `1` (ruff style) | **regression (wrong)** | false `regression_present` | **GAP (C2)** |
| exit→regression | FR-4.3 | Divergence | exit `5` (no tests) | **regression (wrong)** | should be Drift | **GAP (C2)** |
| exit→regression | FR-4.3 | Maximum/Overflow | exit `124` (timeout) | regression? | special-cased FR-4.6 (timeout) but still non-zero | GAP (overlaps C2) |
| exit→regression | FR-4.3 | Sentinel Value | exit `2` (collection err) | **regression (wrong)** | should be Grounding Gap | **GAP (C2)** |
| onboard-gate | FR-2 | Zero/Empty | `list_memories=[]` ∧ `--onboard` | true | run onboarding | OK |
| onboard-gate | FR-2 | Non-empty | `list_memories=[m]` | false | skip (memories-present) | OK |
| onboard-gate | FR-2 | Sentinel | `--onboard` ∧ context-excluded | n/a | WARN, not STOP | OK |
| hierarchy-gate | FR-1 | Sentinel | backend=`none` | skip | no degrade | OK |
| hierarchy-gate | FR-1 | Divergence | backend=`lsp` ∧ no flag | skip | `lsp-disabled` | OK |

GAP rows above each generate a finding (FR-8 rule) — all map to C1 or C2 (already CRITICAL).

### Quantity Flow Diagram — verification triangle (FR-4 pipeline)

```text
[affected files: N] --> [verb-allowlist + metachar filter] --> [M allowed cmds (M <= N), N-M blocked]
                                                                 |
                                                                 v
                                                          [execute_shell_command: M runs]
                                                                 |
                                                                 v
                                          [exit-code classifier] --> R regressions + G grounding-gaps + L lint-signals
                                                                 |
                                                                 v
                            [§14.5.2 cond 4 consumer: expects regressions=R]  <-- must NOT assume R == M-failures (C2)
```
Divergence point: a failing command (M-failures) is NOT 1:1 with regressions (R) — the classifier (C2) must split M-failures into R + G + L. A consumer assuming "every failure is a regression" is the C2 defect.

---

## Synthesis

The spec is structurally strong and well-anchored to SKILL.md, but the **`execute_shell_command` safety envelope — its headline feature — has a provable injection bypass (C1)** and a **provably-wrong exit-code→Regression classifier (C2)**. Both are CRITICAL and must be resolved before task-builder consumption. Seven MAJOR findings center on the verify-state invariant, the audit-row schema violation, the unbounded handoff namespace, the drift-guard interaction, the undefined inline-probe contract, the onboarding budget, and flaky-verification handling. All are resolvable in-place or deferrable to §11 with rationale.

**Resolution requirement**: resolve C1 + C2 (CRITICAL); resolve or defer-to-§11 each MAJOR.
