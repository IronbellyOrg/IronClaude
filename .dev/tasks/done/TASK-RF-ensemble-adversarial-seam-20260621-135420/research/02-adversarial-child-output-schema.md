# R2 — Adversarial Mode-A Child Output Schema (Data Flow / Integration)

Status: In Progress
Date: 2026-06-21
Scope: What the /sc:adversarial Mode-A child EMITS into `t2-adversarial`, and how the seam parses it today.

## Decisive question
Does the Mode-A child already emit deviation-count breakdown, regression/blocking flag,
unauthorized-deviation flag, human-decision flag, and a report path — OR only a convergence score?

## 1. How `run_adversarial_scorer` invokes the child (the seam)

`src/superclaude/cli/reflect/ensemble.py:244-271` `run_adversarial_scorer`:
- Builds a prompt via `build_adversarial_prompt` (L292-301) and launches a **`ClaudeProcess`**
  (`from superclaude.cli.pipeline.process import ClaudeProcess`, L36), i.e. a headless
  `claude --print` running the literal slash command — NOT a subprocess scorer module and NOT
  a swarm fan-out.
- stdout → `output_dir/"adversarial-stdout.json"`, stderr → `"adversarial-stderr.log"`,
  `output_format="stream-json"` (L262-266). Output dir is `output_dir/ADVERSARIAL_SUBRUN_DIR`
  where `ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"` (L67), passed in from
  `run_tier2_ensemble` as `output_dir / ADVERSARIAL_SUBRUN_DIR` (L225-227).
- On `proc.wait() != 0` → returns `None` (L269-270).
- On success: `return extract_convergence_score(parse_adversarial_contract(output_dir))` (L271).

The literal command built (L292-301):
```
/sc:adversarial --compare <files> --suspect-source <files> --output <output_dir>
```

**FINDING (flag mismatch — Unverified impact):** `--suspect-source` is NOT a flag the
`/sc:adversarial` command/skill defines. The command's documented flag surface
(`src/superclaude/commands/adversarial.md:39-70`) is exactly:
`--compare/-c`, `--source/-s`, `--generate/-g`, `--agents`, `--pipeline`, `--output/-o`,
`--focus/-f`, `--depth`, `--blind`. There is **no `--suspect-source`** and **no
`deviation-classification` focus token** anywhere in the adversarial skill or command
(grep over `src/superclaude/skills/sc-adversarial-protocol/` + `commands/` returned zero hits).
So the child runs a plain Mode-A `--compare` debate+merge; the extra flag is inert.

## 2. What the child PARSES today

`parse_adversarial_contract(output_dir)` (ensemble.py:274-289) looks for the child's
return contract at:
1. `<output_dir>/adversarial/return-contract.yaml`  (the skill's `artifacts_dir` convention)
2. `<output_dir>/return-contract.yaml`               (fallback)
via `parse_contract` (delegates to `superclaude.cli.reflect.contract.parse_contract`,
`contract.py:65-82` — generic `yaml.safe_load`, returns the full dict).

`extract_convergence_score(contract)` (ensemble.py:336-357):
- Unwraps a top-level `return_contract:` key if present (the skill nests under it).
- Reads `convergence_score`, falling back to `adversarial_convergence_score`.
- Coerces to float; returns it ONLY if `0.0 <= score <= 1.0`, else `None`.

**=> Today the seam extracts a SINGLE float and discards everything else in the contract.**

## 3. What the /sc:adversarial Mode-A child ACTUALLY EMITS

Authoritative producer schema: `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
"Return Contract (MANDATORY)" §L425-460 (and the duplicate spec at L2082-2145). The child
writes `return-contract.yaml` (into `artifacts_dir`) on EVERY invocation incl. failures.

The COMPLETE field set the Mode-A child emits (SKILL.md:431-443, field defs L449-460):

| Field | Type | Source |
|-------|------|--------|
| `merged_output_path` | string\|null | L433/L451 — path to merged file |
| `convergence_score` | float 0.0-1.0\|null | L434/L452 |
| `artifacts_dir` | string (always) | L435/L453 |
| `status` | enum success\|partial\|failed | L436/L454 |
| `base_variant` | string\|null (winning model:persona) | L437/L455 |
| `unresolved_conflicts` | integer count | L438/L456 |
| `fallback_mode` | boolean | L439/L457 |
| `failure_stage` | string\|null | L440/L458 |
| `invocation_method` | enum | L441/L459 |
| `unaddressed_invariants` | list[{id,category,assumption,severity}] | L442/L460 |

## 4. DECISIVE EVIDENCE — the reflect-deviation fields are NOT emitted by the child

The five target fields the track wants mapped — `deviation_count_by_class`,
`regression_present`, `unauthorized_deviation_present`, `needs_human_decision`,
`report_path` — appear **NOWHERE** in the adversarial producer:
- `grep -rln "deviation_count_by_class|regression_present|unauthorized_deviation_present|needs_human_decision"`
  over `src/superclaude/skills/sc-adversarial-protocol/` => **ZERO hits**.
- Those tokens live ONLY in `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (reflect's
  OWN §9.1 stable output contract, L700-704: `deviation_count_by_class: {authorized, necessary,
  drift, regression}`) and reflect's refs (`deviation-taxonomy.md`, `runtime-surface.md`).

i.e. the deviation taxonomy / regression / human-decision verdict is produced by REFLECT'S
OWN protocol (reviewer cards → adversarial-merged REPORT.md → reflect's return-contract.yaml),
NOT by the sc:adversarial child. The adversarial child only contributes the *merge* outputs:
a merged report path + a convergence score + a debate status. The reflect SKILL.md treats
sc-adversarial purely as a "merge 2-3 reviewer cards into one verdict" engine
(SKILL.md:635, L645-652) and even documents a consumer-side key-rename
(`artifacts_dir` → `adversarial_artifacts_dir`, SKILL.md:654) — it never expects deviation
fields back from the child.

**Where the verdict prose lives:** the child's `merged_output_path` (the merged REPORT) does
contain the reviewers' deviation classifications as free-form content, but the child does NOT
structure them into machine-readable contract fields. To get the five target fields as data,
they must be derived/extracted, not just key-mapped from the child contract.

## 5. The other artifact in play — swarm reduce merged_path

`run_tier2_ensemble` separately runs the swarm fan-out (Wave 1/2/3) and calls
`reduce_wave3(... mode="normalize+merge" ...)` (ensemble.py:202-217). `reduce.py`:
- `merged_path` is populated ONLY in `mode == "normalize+merge"` (reduce.py:642) and is `None`
  when `workers_succeeded < 2` (reduce.py:255-261).
- The merged file is the concatenation/merge of per-reviewer `final_path` artifacts; it carries
  the same kind of free-form reviewer content, not structured deviation counts.
`swarm_contract.merged_path` is passed into `build_reflect_contract(swarm_merged_path=...)`
(ensemble.py:234-239) and becomes `report_path` via `_select_report_path` (L375, L488-497) —
so `report_path` is ALREADY sourced from the swarm merge, independent of the adversarial child.

## 6. What `build_reflect_contract` does with the target fields TODAY

`build_reflect_contract` (ensemble.py:360-407) HARDCODES the five target fields to constants —
they are NOT derived from any adversarial output:
- `deviation_count_by_class: {authorized:0, necessary:0, drift:0, regression:0}` (L385-390)
- `regression_present: False` (L401)
- `unauthorized_deviation_present: False` (L402)
- `needs_human_decision: False` (L403)
- `report_path` = swarm merged_path (NOT adversarial) (L375)
Only `adversarial_convergence_score` (L395) actually carries data from the child.

## 7. Implication for the R6 mapping change

The track goal ("map deviation_count_by_class, regression_present,
unauthorized_deviation_present, needs_human_decision, report_path INTO build_reflect_contract")
CANNOT be a pure key-rename from the adversarial child contract, because the child does not
emit those fields. Feasible options (for downstream design — NOT decided here):
1. **Derive a regression signal from convergence vs threshold** — feasible immediately with
   only the float the child already emits. (reflect SKILL.md already documents convergence
   routing ≥0.75 PASS / ≥0.60 PARTIAL / <0.60 FAIL at L652, and `grader-extensions.md:300`
   uses `convergence_score < 0.75 OR verdict == regression_present`.) This derives a coarse
   `regression_present`-ish gate from the score; it does NOT recover per-class deviation counts.
2. **Extend the child's emission** — teach `/sc:adversarial` (or a reflect-specific Mode-A
   variant / the reviewer-merge step) to emit the reflect deviation taxonomy into its
   return-contract.yaml, then parse those new fields in `parse_adversarial_contract` /
   a new richer extractor. This is the only path that recovers true
   `deviation_count_by_class` / `unauthorized_deviation_present` / `needs_human_decision`.
3. **Extract from the merged report body** — parse the deviation classifications out of the
   merged `merged_output_path`/`report_path` markdown (brittle; the merged report is free-form).

Where the child writes (for option 2 wiring): contract at
`<t2-adversarial>/adversarial/return-contract.yaml` (ensemble.py:283), produced per
sc-adversarial-protocol/SKILL.md:435 (`artifacts_dir`) — the file the skill ALWAYS writes.

---

Status: Complete

**Decisive finding: SCORE-ONLY.** The `/sc:adversarial` Mode-A child emits ONLY a
convergence-oriented contract (`convergence_score`, `merged_output_path`, `artifacts_dir`,
`status`, `base_variant`, `unresolved_conflicts`, `fallback_mode`, `failure_stage`,
`invocation_method`, `unaddressed_invariants` — SKILL.md:431-443). It does NOT emit
`deviation_count_by_class`, `regression_present`, `unauthorized_deviation_present`,
`needs_human_decision`, or a reflect-style `report_path`. The seam today parses ONLY the
float (`extract_convergence_score`, ensemble.py:336-357). Therefore R6 is NOT a pure
ensemble-side key-rename: the task MUST either (a) derive a coarse regression signal from
`convergence_score` vs a threshold (immediately feasible from existing emission), and/or
(b) EXTEND the producer's emission (adversarial child or the reviewer-merge step) to write the
reflect deviation taxonomy before any richer mapping is possible. `report_path` is already
sourced from the swarm merge (`reduce_wave3` `merged_path`), not the adversarial child.
