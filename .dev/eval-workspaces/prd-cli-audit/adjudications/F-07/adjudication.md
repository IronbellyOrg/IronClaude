# F-07 Adjudication — `--where` flag stored on config, never read by any consumer

**Mode**: B (three personas → convergence)
**Preliminary severity (from finding)**: HIGH
**Pattern tag**: P2 (dead knob)

---

## Re-verification (read-only, mechanical)

| Claim | Source | Status |
|---|---|---|
| `--where` declared on `prd run` with `multiple=True` | `src/superclaude/cli/prd/commands.py:41-45` | CONFIRMED |
| `where=where if where else None` passed into `resolve_config` | `src/superclaude/cli/prd/commands.py:107` | CONFIRMED |
| `where=list(where) if where else []` stored on `PrdConfig` | `src/superclaude/cli/prd/config.py:134` | CONFIRMED |
| `where: list[str] = field(default_factory=list)` field declared | `src/superclaude/cli/prd/models.py:182` | CONFIRMED |
| Zero downstream readers of `config.where` / `cfg.where` / `self._config.where` | `grep -rn -E "\.where\b\|where=\|\"where\"\|'where'" src/superclaude/` returns only the two write-side hits (`commands.py:107`, `config.py:134`); zero read sites | CONFIRMED — no consumers |
| `WHERE` is extracted by the LLM from `config.user_message` (parse-request prompt) | `src/superclaude/cli/prd/prompts.py:65-95` (template) and specifically `:81` (`"WHERE": [<list of source directories to focus on>]`) and `:95-96` (instructions to extract from the natural-language request) | CONFIRMED |
| Downstream `scope-discovery` reads `parsed["WHERE"]` from the LLM JSON, not from `config.where` | `src/superclaude/cli/prd/prompts.py:111-113` (`if parsed.get("WHERE"): … parsed["WHERE"]`) | CONFIRMED |

**Net**: The finding's mechanical claim is correct. `PrdConfig.where` is a write-only field. The pipeline's `WHERE` semantics are entirely sourced from the LLM's natural-language extraction over `user_message`.

---

## Persona 1 — Analyzer (reproducibility / user experience)

**Question**: When `--where` is silently ignored, what does the user actually experience?

**Trace of the user-facing surface**:

1. User invokes `superclaude prd run "Add search" --where src/api --where src/search` (per the docstring example at `commands.py:25`).
2. Click parses both `--where` values into the tuple `("src/api", "src/search")` and stores them on `PrdConfig.where` via `config.py:134`.
3. `build_parse_request_prompt` (`prompts.py:54-101`) ignores `config.where` entirely. It hands only `config.user_message` (`prompts.py:69`) to the LLM and asks the LLM to *re-derive* `WHERE` from that natural-language string.
4. The LLM writes `parsed-request.json["WHERE"]` based purely on what it saw in the natural-language request.
5. `build_scope_discovery_prompt` (`prompts.py:104-145`) reads `parsed["WHERE"]` from the file at `prompts.py:111` and uses it to build the `Focus on these directories:` clause (`prompts.py:112-114`). If the LLM's extraction is empty, the prompt instead instructs "Explore the codebase starting from the repo root" (`prompts.py:116-121`).

**Observable failure modes**:

- **Mode A (LLM happens to extract the same paths)**: User passes `--where src/api --where src/search`, and the natural-language string also contains "search". The LLM may extract `["src/search"]` (or `[]`, or something else). The output looks plausible — the user has no way to detect the flag was ignored. Worst kind of bug: silent disagreement masquerading as success.
- **Mode B (vague request, explicit flag)**: User says `superclaude prd run "Add search" --where src/api --where src/search`. The LLM sees "Add search" (Scenario B per the prompt's classification, `prompts.py:86-89`) and per `prompts.py:95` *explicitly* sets `WHERE=[]`. Scope-discovery then "roams the whole repo" (`prompts.py:116-121`). The user's intent — pinning scope to two dirs — is fully discarded.
- **Mode C (Scenario A with mismatched paths)**: User's natural-language string names `src/api` but flag says `src/search`. The LLM extracts `["src/api"]`. The flag is ignored, and the user has no diagnostic to discover the divergence.

**Reproducibility**: Trivial. Any invocation with `--where` and a vague request demonstrates Mode B. There is no log line, no warning, no visible signal that the flag was dropped — the only evidence is reading `parsed-request.json` and noticing the CLI-supplied paths are absent.

**Analyzer verdict**: Reproducible silent contract violation. The `--help` text at `commands.py:44` ("Source directories to focus on (repeatable)") and the docstring example at `commands.py:25` both promise the flag has effect. It does not.

---

## Persona 2 — Refactorer (blast radius / pattern density)

**Question**: Is F-07 isolated, or part of a systemic P2 (dead knob) pattern? Cross-check sibling findings.

**P2 sibling cluster** (knob defined → reaches config → never consumed downstream):

| Finding | Knob | Wired through config? | Read at consumer? | Severity (prelim) |
|---|---|---|---|---|
| **F-03** | `--tier` → `_tier_min_lines` / `_tier_min_lines_assembly` | Yes (`config.tier`) | No — `GATE_CRITERIA` hard-codes 400/800 at module import; helpers have zero call sites (`gates.py:281-292`, exec at `executor.py:530,596`) | CRITICAL |
| **F-07** (this) | `--where` | Yes (`PrdConfig.where`) | No — LLM re-extracts `WHERE` from `user_message`; CLI list never injected into prompts (`prompts.py:54-101`) | HIGH (preliminary) |
| **F-11** | `--stall-timeout` / `stall_action` via `PrdMonitor` | Yes (`config.stall_timeout`, `config.stall_action`, `models.py:190-191`) | No — `PrdMonitor` instantiated at `executor.py:334` but `parse_line`/`check_stall` never called; entire 202-line module is dead (`monitor.py:1-202`) | HIGH |
| **F-22** | `enforcement_tier="EXEMPT"`/`"LIGHT"` labels on gates | N/A (constants in `gates.py:300,356,404,504`) | Partial — `_evaluate_gate` recognizes only `STRICT` (`executor.py:531-540`); EXEMPT/LIGHT labels are decorative | MEDIUM |

**Quantification**:

- **4 confirmed P2 instances** in the PRD CLI module alone (out of 34 findings = ~12% of total findings).
- **3 of 4** involve a CLI flag (`--tier`, `--where`, `--stall-timeout` indirectly through monitor) — the user-facing contract violation rate is high.
- **All 4** share the same architectural defect: the configuration-resolution layer accepts and stores values that the downstream execution layer does not consult. The wiring stops at `PrdConfig` and never threads through to the point of use.
- **Severity correlation**: F-03 is CRITICAL because the dead knob causes wrong gate behavior end-to-end. F-11 is HIGH because the dead knob silently disables a whole subsystem (stall detection). F-07 is "between" — the LLM provides a *fallback* signal that masks the failure, which makes it less catastrophic than F-03/F-11 but arguably more insidious than F-22 (which is currently latent).

**Refactorer verdict**: F-07 is one of the more numerous instances in a clear systemic P2 cluster. A blanket P2 sweep should be planned — the fix shape (thread config field into the prompt/consumer) is mechanically similar for F-07, F-03, and F-11. Doing them as one PR is cheaper than three sequential patches because they share test scaffolding (config → consumer round-trip assertions). The pattern is well-bounded to `src/superclaude/cli/prd/` and has not (per grep) leaked into other CLI modules.

---

## Persona 3 — Architect (severity calibration)

**Question**: Preliminary HIGH. But the LLM downstream extraction *does* still work — so is this MEDIUM?

**Calibration axes**:

1. **Correctness ceiling** — When the user's `--where` and the LLM's extraction agree, output is correct (by accident). When they disagree, output is incorrect with no signal. Ceiling: user cannot rely on the flag, period.

2. **User-visible contract** — `commands.py:25` example *explicitly* shows `--where src/api`. The `--help` text *explicitly* promises directory focus. The flag is documented as a working feature. This is a documentation-vs-behavior contradiction, not just an internal dead knob.

3. **Safety / data integrity** — No. The pipeline does not corrupt anything. Worst case is the LLM scopes too broadly or too narrowly. No persistent damage, no security exposure.

4. **Failure mode under "Scenario B" (vague request)** — Per `prompts.py:95`, the LLM is *instructed* to set `WHERE=[]` when the request is vague, then scope-discovery is *instructed* to "explore the codebase starting from the repo root" (`prompts.py:116-121`). For a user passing `--where` *precisely because* their request is vague, the system is guaranteed to ignore them. This is the canonical use case for the flag — and it's the case that fails 100% of the time.

5. **Fix difficulty** — Low. Two-line patch in `build_parse_request_prompt`: if `config.where` is non-empty, inject it into the prompt as a pre-seeded `WHERE` value (or pass it through directly and have the LLM treat it as authoritative). Plus one analogous patch in `build_scope_discovery_prompt` if you prefer to bypass the LLM round-trip entirely for the directory list. ~30-60 minutes including a regression test.

6. **Comparable findings in the cluster**:
   - F-03 (CRITICAL): tier flag fully wired but gate construction bypasses it → wrong-direction halts/passes affect end-to-end pipeline correctness.
   - F-07 (this): where flag fully wired but prompt construction bypasses it → wrong-scope LLM exploration; LLM may compensate by accident.
   - F-11 (HIGH): stall config fully wired but monitor.check_stall never called → guaranteed 30x worse stall timeout (3600s vs 120s).

   F-07 sits between F-03 and F-11 on impact, but lower on detectability (LLM masks it). Calibration logic:
   - vs F-03: F-07 lower (correctness ceiling is non-binary — LLM may succeed). **→ less severe than F-03's CRITICAL.**
   - vs F-11: F-07 comparable (both silently violate documented config-driven behavior, both 100% repro for the canonical use case). **→ HIGH is defensible.**
   - vs F-22 (MEDIUM): F-07 worse because (a) F-22 has no current behavior change while F-07 has guaranteed silent contract violation, and (b) `--where` is a documented CLI flag while EXEMPT/LIGHT are internal labels. **→ strictly more severe than F-22.**

**Architect verdict**: Sustain **HIGH**. The LLM extractor does not "rescue" this finding — it merely hides the failure on a subset of inputs. The Scenario-B failure mode is deterministic and is exactly the case the flag was added to serve.

---

## Convergence

### Verdict
**Sustain finding.** `PrdConfig.where` is mechanically write-only. The CLI `--where` flag has zero behavioral effect on the pipeline. The downstream `WHERE` value used by scope-discovery comes from the LLM's extraction over `user_message`, not from the CLI input. This contradicts both the `--help` text (`commands.py:44`) and the docstring example (`commands.py:25`).

### Convergence score
**3 / 3** — All three personas concur:
- Analyzer: reproducible silent contract violation with no observable user signal.
- Refactorer: one of 4 confirmed P2 (dead knob) instances; pattern is real and bounded; consolidate fix with F-03/F-11.
- Architect: severity calibrated against siblings; HIGH stands.

### Final severity
**HIGH** (unchanged from preliminary).

Rationale: documented CLI contract is unconditionally violated in the canonical use case (Scenario B + explicit `--where`); LLM fallback masks the bug on Scenario-A inputs but does not fix it; fix is mechanically trivial.

### Fix difficulty
**Low** (≈30-60 min):
1. In `build_parse_request_prompt` (`prompts.py:54-101`), if `config.where` is non-empty, inject the list into the prompt with a directive like "Pre-seeded WHERE (authoritative): [...]; use these as the WHERE field unless the natural-language request explicitly contradicts them."
2. Alternative / additive: have `build_scope_discovery_prompt` (`prompts.py:104-145`) prefer `config.where` over `parsed["WHERE"]` when both are present (`prompts.py:111-113`).
3. Add a regression test asserting `config.where=["src/api"]` propagates into the constructed prompt (string-level assertion).

The fix can be staged as part of a unified P2 cleanup PR alongside F-03 (`_tier_min_lines` wiring) and F-11 (`PrdMonitor` wiring or removal).

### Synthesis

F-07 is a textbook P2 dead-knob defect: configuration is accepted, validated, and stored at `PrdConfig.where` (`models.py:182`, written from `config.py:134`, sourced from `commands.py:107`) but never read by any downstream consumer (`grep` confirms zero hits across `src/superclaude/`). The pipeline's `WHERE` semantics are independently produced by the LLM in `build_parse_request_prompt` (`prompts.py:54-101`), which is handed `config.user_message` only — the CLI flag is structurally invisible to the prompt-construction path.

The LLM's natural-language extraction provides a *masking* fallback rather than a *substitute* for the flag: it produces a plausible `WHERE` in Scenario A (explicit requests) but is instructed at `prompts.py:95` to emit `WHERE=[]` in Scenario B (vague requests). For the canonical use case of `--where` — a vague request that the user wants to scope manually — the flag's failure is deterministic and total.

F-07 sits inside a confirmed cluster of four P2 findings (F-03, F-07, F-11, F-22) all within `src/superclaude/cli/prd/`. F-03 is more severe (CRITICAL — gate behavior is wrong); F-11 is comparable (HIGH — stall detection disabled); F-22 is less severe (MEDIUM — latent). Severity HIGH is calibrated and consistent with the cluster. The recommended remediation is a single P2-sweep PR threading config fields through to their declared consumers, with simple config-to-prompt round-trip assertions in tests.

---

## Citations

- `src/superclaude/cli/prd/commands.py:25` — docstring example showing `--where src/api`
- `src/superclaude/cli/prd/commands.py:41-45` — `--where` flag declaration
- `src/superclaude/cli/prd/commands.py:107` — `where=where if where else None` passed to `resolve_config`
- `src/superclaude/cli/prd/config.py:134` — `where=list(where) if where else []` stored on `PrdConfig`
- `src/superclaude/cli/prd/models.py:182` — `where: list[str] = field(default_factory=list)`
- `src/superclaude/cli/prd/prompts.py:65-101` — `build_parse_request_prompt` template (note: only `config.user_message` is interpolated at `:69`; no `config.where` reference)
- `src/superclaude/cli/prd/prompts.py:81` — `"WHERE": [<list of source directories to focus on>]` (LLM-generated field)
- `src/superclaude/cli/prd/prompts.py:95-96` — instructions to leave WHERE empty in Scenario B
- `src/superclaude/cli/prd/prompts.py:111-114` — `parsed["WHERE"]` read from LLM JSON (not from `config.where`)
- Sibling P2 findings: `F-03-tier-min-lines-unwired-dead-code.md`, `F-11-prdmonitor-entirely-dead-code.md`, `F-22-exempt-light-enforcement-not-recognized.md`
