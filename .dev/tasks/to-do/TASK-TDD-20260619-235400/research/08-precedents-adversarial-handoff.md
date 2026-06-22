# 08 — Precedents + Adversarial Handoff

- **Topic:** Precedents for the reflect-ensemble thin-caller pattern + how `ensemble.py` should hand per-reviewer artifacts to `/sc:adversarial` Mode A
- **Type:** Doc Analyst (research for TDD)
- **Scope:** `sc-bare-review/SKILL.md`, `roadmap/validate_executor.py` (~L317-373), `pipeline/process.py`, `sc-adversarial-protocol/SKILL.md` (Mode A interface)
- **Status:** Complete
- **Date:** 2026-06-19

---

## 0. Evidence index (re-verified line numbers)

| Anchor | File | Lines (re-read) |
| --- | --- | --- |
| bare-review precedent flow + contract | `src/superclaude/skills/sc-bare-review/SKILL.md` | full file (81 lines) `[CODE-VERIFIED]` |
| swarm `--suspect-source` emission (the contract `ensemble.py` mirrors) | `src/superclaude/cli/swarm/commands.py` | L2020–2089 `[CODE-VERIFIED]` |
| `reflect-review` / `bare-review` lens shape | `src/superclaude/cli/swarm/lenses/bare_review.py` | full file (76 lines) `[CODE-VERIFIED]` |
| per-agent external fan-out reference | `src/superclaude/cli/roadmap/validate_executor.py` | L317–378 `[CODE-VERIFIED]` |
| subprocess lifecycle primitive | `src/superclaude/cli/pipeline/process.py` | full file (354 lines) `[CODE-VERIFIED]` |
| Mode A `--compare` interface | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | L24–69, L527–656 `[CODE-VERIFIED]` |
| OI-4 / NFR-RH2.2 / NFR-RH2.7 / FR-RH2.3 | `.dev/tasks/.../research/00-prd-extraction.md` | L62–72, L159–166, L246 `[CODE-VERIFIED against PRD-extraction]` |

> `ensemble.py` does **not yet exist** — it is the module this TDD designs. The reflect CLI package today is `commands.py`, `config.py`, `contract.py`, `models.py`, `runner.py` (`src/superclaude/cli/reflect/`, verified via `ls`). All "should hand…" statements below are design targets grounded in the cited precedents, not descriptions of existing reflect code.

---

## 1. Precedent A — `sc-bare-review`: the thin-caller-over-swarm pattern `ensemble.py` mirrors

### 1.1 Flow (verbatim from SKILL.md)

`sc-bare-review` is a **delegate-only** skill (no `/sc:bare-review` command). Its entire job is to be a **thin caller over `superclaude swarm run --lens bare-review`** — the swarm CLI owns preflight, parallel fan-out, normalization, and the return contract (SKILL.md L20–24). The flow is:

1. Caller flags map 1:1 onto `swarm run --lens bare-review` (`--target`, `--output`, `--reviewers`, `--target-line-cap`, `--timeout-sec`, `--label`); `--transport openai_compat` for the real T2 external proxy fan-out, `--transport stub` for a hermetic dry run (L29–39).
2. **Invoke once and relay** — non-zero exit → STOP, surface stderr verbatim; empty-target (IMM-4) and env-missing fail at preflight before any reviewer dispatches (L41–42).
3. On success, `Read` `<output-dir>/return-contract.yaml` and relay it. The CLI fans out the N reviewers internally (no manual single-message dispatch), normalizes each into the §4 template, writes `bare-review-NN-<model>.md`, emits the contract (L43–45).

The skill **never judges/scores/filters** — raw forwarding, `suspect: true` by construction, never Anthropic-routed (L24–26, L70). This is exactly the posture `ensemble.py` must take toward the swarm dispatch library: form the reviewer fan-out via swarm, do not score the result itself (scoring is `/sc:adversarial` Mode A's job).

### 1.2 Return contract (SKILL.md L49–56) — the artifact-handoff shape `ensemble.py` consumes

```yaml
contract_version: "1.0"; status: success | partial | failed   # IMM-5: M==N→success; 2≤M<N→partial; M<2→failed
target: { path, checksum, truncated, truncation_line_cap }
workers_requested: <N>; workers_succeeded: <M>; workers_failed: <N-M>
output_files: [ { index, path, raw_path, meta_path, final_path, model_id, model_label, status } ]
caller_metadata: { suspect: true, tier: T2 }   # suspect always — by construction
recommended_next_command: "/sc:adversarial --compare <existing>,<bare…> --suspect-source <bare…>"
```

**Load-bearing for this TDD:** the contract carries a per-reviewer `output_files[]` list, and each element has a **`final_path`** (the normalized markdown body) alongside `raw_path` and `meta_path`. The hand-off to `/sc:adversarial` is built from `final_path` values, **never** from any swarm-merged file. `[CODE-VERIFIED]`

### 1.3 How the `recommended_next_command` is actually built — `commands.py` L2058–2081

This is the mechanical precedent `ensemble.py` mirrors. After `normalize_wave2` writes each worker's normalized body to `final_path`, `commands.py` (PG2 C1, L2058–2081) computes the next-command substitutions from **succeeded workers' `final_path`s only**:

```python
succeeded_final_paths = [
    w.final_path
    for w in normalized_workers
    if w.status == "success" and w.final_path
]
next_cmd_subs.setdefault(
    "suspect_files",
    ",".join(succeeded_final_paths) if succeeded_final_paths else "<no-bare-files>",
)
next_cmd_subs.setdefault(
    "compare_files",
    ",".join(["<existing-review>", *succeeded_final_paths]),
)
```

Three facts the TDD must inherit `[CODE-VERIFIED]`:

- **`suspect_files` = the succeeded `final_path`s** (filtered on `status == "success" and w.final_path`). Failed/empty workers are excluded; if none succeed the placeholder is `<no-bare-files>`.
- **`compare_files` = `<existing-review>` PLUS the same succeeded `final_path`s** — i.e. the existing (Tier-1) reviewer artifact is prepended so Mode A compares the bare/suspect reviews *against* the trusted baseline.
- The merged/amalgamated swarm output is produced by `reduce_wave3` (L2082) but is **NOT** what flows into `--suspect-source`/`--compare`. The next-command is built purely from per-reviewer `final_path`s. This is the concrete realization of "consume `output_files[].final_path`, NEVER swarm's `merged.md`."

---

## 2. Precedent B — `validate_executor.py`: separate-process-per-agent external fan-out (§21 Alternatives prior art)

`src/superclaude/cli/roadmap/validate_executor.py` `_build_multi_agent_steps` (re-read L317–378) is the **proven prior art for fanning out one process per reviewer agent and then merging adversarially**. It remains untouched by this work and is cited in the TDD's §21 Alternatives as the "separate subprocess per agent" option that NFR-RH2.2 deliberately rejects for the inner loop.

### 2.1 How it fans out (L338–378) `[CODE-VERIFIED]`

```text
N agents -> N parallel reflections -> gate each -> adversarial merge      (docstring L328)
```

- **One `Step` per agent** (L341–362): iterates `config.agents`, builds a `reflect-{agent.id}` step whose `output_file = validate_dir / f"reflect-{agent.id}.md"`, with `model=agent.model` so each step binds a **distinct model**. The reflect prompt is identical across agents (`build_reflect_prompt(...)`); only the model differs — the heterogeneity comes from the model binding, not the prompt.
- **Per-step gate** (`gate=REFLECT_GATE`, `retry_limit=1`, `timeout_seconds=600`) — each reflection is independently gated before merge.
- **The N steps are returned as a parallel group** (L375–377): `return [reflect_steps, merge_step]` — `reflect_steps` is a `list[Step]` (a parallel batch), `merge_step` a single sequential step that runs after all reflections.
- **Adversarial merge step** (L364–373): `id="adversarial-merge"`, `prompt=build_merge_prompt([str(p) for p in reflect_outputs])`, `inputs=reflect_outputs`, `gate=ADVERSARIAL_MERGE_GATE`, `output_file=validate_dir / "validation-report.md"`. **Crucially, the merge prompt is fed the list of per-agent reflection output files** (`reflect_outputs`) — the same "merge consumes per-reviewer artifacts, not a pre-merged blob" contract.

### 2.2 Relevance and contrast for the TDD

- **Proves the pattern works**: per-reviewer-process fan-out → per-reviewer artifact → adversarial merge over those artifacts is already shipped and tested in roadmap-validate.
- **But each `Step` becomes its own `claude -p` subprocess** (driven by the pipeline executor / `ClaudeProcess`). For reflect's inner Tier-2 loop that is exactly the **`claude -p` nesting failure** the PRD-extraction (L17) says the swarm-library route sidesteps. So `validate_executor` is the **CLI-subprocess-per-agent alternative**, not the chosen inner-loop mechanism. The TDD chooses the in-process swarm-library import instead (see §4). `[CODE-VERIFIED]`

---

## 3. `pipeline/process.py` — ORTHOGONAL to the reflect-audit / Mode-A seam (stated explicitly)

**Verdict: orthogonal infrastructure primitive, not part of the reflect-audit seam or `/sc:adversarial` Mode A.** Do not force-fit it. Evidence `[CODE-VERIFIED]`:

- The module docstring (L1–10) defines its role precisely: *"subprocess lifecycle for `claude -p` invocations. Extracted from sprint/process.py… generic: accepts PipelineConfig-compatible parameters and an `output_format` flag."* It is a low-level **process manager**, one level below any reflect/adversarial logic.
- Its public surface is `ClaudeProcess` (L72): build a `claude --print` command (L121–143), build a child env stripping `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` to prevent nested-session detection (L145–160), `start()` (deliver prompt via **stdin** to dodge the 128 KB `MAX_ARG_STRLEN` argv ceiling, L162–217), `wait()`/`terminate()` (process-group SIGTERM→SIGKILL teardown, L260–323), `validate_tool_write_output()` (L325–345). Plus `PromptTooLargeForArgv` and `_parse_prompt_max_bytes` guards.
- It contains **no** reference to `adversarial`, `reflect`, `suspect`, `final_path`, `merge`, `swarm`, or any audit-contract field (grep returned zero hits — see §0 method). It does not know what a reviewer, a verdict, or Mode A is.

**Where it *does* touch this work, indirectly:** `ClaudeProcess` is the canonical subprocess primitive the reflect Tier-1 grounded pass uses (a single `claude -p` via `ClaudeProcess`, unchanged per FR-RH2.1 AC). And NFR-RH2.2 / FR-RH2.8 AC L147 explicitly allow the swarm call to go "through the swarm CLI surface / `ClaudeProcess`, **not a hand-rolled `Popen`**" — so if the optional `--detached` observability variant (NFR-RH2.7) ever shells out to `superclaude swarm run`, `ClaudeProcess`-style lifecycle management is the sanctioned mechanism rather than a raw `subprocess.run`. But for the **default in-process library-import path**, `process.py` is not invoked at all. It is a building block available to the observability sidecar, not a participant in the Mode-A handoff. `[CODE-VERIFIED]`

---

## 4. Mode A interface and how `ensemble.py` hands per-reviewer artifacts to it

### 4.1 Mode A `--compare` (sc-adversarial-protocol SKILL.md, re-read L24–69, L527–656)

Mode A is "Compare Existing Files" (FR-001, L55–64):

```bash
/sc:adversarial --compare file1.md,file2.md[,...,file10.md]
```

- Accepts **2–10 existing files**; count enforced (`2 ≤ file_count ≤ 10`, L563–568). <2 → STOP, >10 → STOP, missing file → STOP.
- Each input is **copied** to `<output>/adversarial/variant-N-original.md` (L62–63, L627–638), normalized (strip trailing ws, single trailing newline, preserve headings), then run through the 5-step protocol (diff → debate → hybrid-scoring/base-selection → refactor-plan → merge).
- Returns the standard `return_contract` (L431–443): `merged_output_path`, `convergence_score`, `artifacts_dir`, `status`, `base_variant`, `unresolved_conflicts`, etc. The reflect contract records `adversarial_convergence_score` from this (`contract.py` L284). `[CODE-VERIFIED]`

### 4.2 The `--suspect-source` gap — `[CODE-CONTRADICTED]` between bare-review SKILL and adversarial SKILL

The bare-review contract and the `bare-review` lens both emit a recommended-next-command containing **`--suspect-source`** (`bare_review.py` L65–68; SKILL.md L18, L55, L75). **But `--suspect-source` is NOT documented anywhere in `sc-adversarial-protocol/SKILL.md`** (grep over all 3002 lines returned zero `suspect` hits — §0 method). Mode A's documented surface is `--compare` only; the input-mode parser (L551–610) recognizes `--compare`, `--source/--generate/--agents`, `--pipeline`, `--depth`, `--convergence`, `--interactive`, `--output`, `--focus`, `--blind`, `--auto-stop-plateau` — **never `--suspect-source`.**

Implication for the TDD: `--suspect-source` is, today, a **behavioral convention defined by the swarm/bare-review side** (the lens emits it; the adversarial protocol does not yet formally consume it). Resolving OI-4 (§5) therefore also requires deciding whether `/sc:adversarial` Mode A must be taught to parse `--suspect-source` (apply extra scrutiny / a suspect rubric to the flagged files), or whether reflect simply passes the suspect files in `--compare` and the suspect handling is purely advisory. This is a documented seam-level gap, surfaced in "Gaps and Questions."

### 4.3 The handoff `ensemble.py` should perform (design target, grounded in §1.3 + FR-RH2.3)

Per FR-RH2.3 (PRD-extraction L62–72) — *"Reflect MUST consume the N normalized per-reviewer artifacts (swarm `final_path`s) as the input to its existing `sc-adversarial-protocol` Mode A merge. Swarm's `mechanical_merge` (`merge.py`) output MUST NOT be treated as the adversarial verdict."* The mechanics, taken directly from the bare-review precedent (§1.3):

1. Drive the swarm dispatch library (`dispatch_wave1` + per-slot transport factory + `reduce_wave3` in `normalize+merge` mode) with `--lens reflect-review`. Read the resulting return-contract's `output_files[]`.
2. Collect **`final_path` for each worker with `status == "success"`** — identical filter to `commands.py` L2066–2070. These M paths are the per-reviewer suspect-flagged artifacts.
3. Build the Mode A input as **`--compare <existing-reflect-review>,<final_path…>`** (existing Tier-1 reflection prepended, mirroring `compare_files` L2078–2081) and the suspect flag as **`--suspect-source <final_path…>`** (the succeeded paths, mirroring `suspect_files` L2071–2077).
4. Invoke `sc-adversarial-protocol` Mode A **in-process** (library/skill invocation — see §4.4), feeding it those existing files. Record its `convergence_score` / `merged_output_path` onto the reflect contract (`adversarial_convergence_score`).
5. **Never** pass `reduce_wave3`'s `mechanical_merge` / `merged.md` to Mode A — that swarm merge is a mechanical concatenation, not the adversarial verdict (FR-RH2.3 AC L68–69; no scoring/ranking/dedup may be added to `swarm/merge.py`).

### 4.4 In-process library-import vs CLI-subprocess shell-out (the sub-decision)

This is the decision that distinguishes the chosen design from Precedent B (§2):

- **Chosen — in-process library import (NFR-RH2.2):** `ensemble.py` imports the swarm dispatch functions (`dispatch_wave1`, `_resolve_run_transport_factory`, `reduce_wave3`) and calls them **in-process** — **no second `claude -p`/subprocess for the inner Tier-2 loop.** NFR-RH2.2 forbids `cli.sprint`/`cli.roadmap` imports, `async`/`await`, and any raw `subprocess.run`/`Popen` in the reflect package (PRD-extraction L160), guarded by `test_no_nesting_guard.py` import/async/subprocess regexes. This is precisely why `validate_executor`'s per-`Step`-becomes-a-subprocess model (§2) is rejected for the inner loop: it would spawn `claude -p` children and re-introduce the nesting failure. The reflect Tier-1 grounded pass still uses a single `ClaudeProcess` (unchanged, FR-RH2.1), but the Tier-2 reviewer fan-out is a library call, not a subprocess fan-out.
- **Retained for observability ONLY (NFR-RH2.7):** the `superclaude swarm run --lens reflect-review` CLI surface (with `--detached`/tmux + `done.json` sentinel + `--tui`) is kept as the **optional observability variant** so headless Tier-2 runs are pollable (PRD-extraction L17, L165). It is NOT the default inner-loop transport — it is the "watch a long headless run" affordance. PRD-extraction L17 states it verbatim: *"the `superclaude swarm run --lens reflect-review` CLI is the optional `--detached` observability variant, not the default inner-loop transport."* If that path ever shells out, it goes through the swarm CLI surface / `ClaudeProcess` (sanctioned), never a hand-rolled `Popen` (FR-RH2.8 AC L147).

**Net:** library import is the transport; CLI `--detached`/tmux is the telescope. Two different concerns, deliberately separated; conflating them would either re-introduce nesting (if the inner loop shelled out) or lose pollability (if the only path were a synchronous in-process call).

---

## 5. OI-4 — suspect-rubric symmetry between reflect-review and bare-review

OI-4 (PRD-extraction L246, verbatim): *"How does `/sc:adversarial` Mode A treat `suspect: true` reflect-review artifacts vs bare-review ones (any rubric difference)? Impact: Low-Medium — scoring fidelity. Resolution: During FR-RH2.3; confirm against `sc-adversarial-protocol`."*

Findings from the code/skill `[CODE-VERIFIED]` + `[CODE-CONTRADICTED]`:

- **Both lenses set `suspect: true` / `tier: T2` identically.** `bare-review` lens: `suspect=True, tier="T2"` (`bare_review.py` L63–64). The planned `reflect-review` lens (FR-RH2.2, L52) is specified to mirror it: `tier: "T2"`, `suspect: true`. So at the *lens/contract* level there is **no asymmetry** — both arrive at Mode A carrying `caller_metadata: {suspect: true, tier: T2}`.
- **Mode A's documented scoring rubric makes NO distinction by `suspect` flag.** The hybrid-scoring rubric (SKILL.md L210–273: quantitative 0.50 + qualitative 30-criterion 0.50, position-bias mitigation, tiebreakers) and the 6-category invariant probe (L1132–1199) contain **no `suspect`-conditional branch and no `--suspect-source` consumption** (grep: zero `suspect` hits across the whole SKILL). As written today, Mode A would score a reflect-review variant and a bare-review variant by the **same rubric** — the suspect flag is not a scoring input.
- **Therefore the honest answer to OI-4 is: there is currently NO rubric difference, because Mode A does not yet read `suspect` at all.** The "extra scrutiny on suspect:true" discipline lives in the *caller's* acceptance notes (`bare_review.py` L69–73 cites NFR-012 PR-review discipline) and in the next-command framing, not in Mode A's scoring. The symmetry is real but vacuous: identical treatment because suspect-awareness is unimplemented on the Mode-A side.
- **TDD decision needed (this is what OI-4 must close):** either (a) accept the status quo — reflect-review and bare-review suspect artifacts are scored identically and the suspect flag stays advisory/caller-side (lowest-risk, preserves NFR-RH2.7 backward-compat), or (b) teach Mode A to parse `--suspect-source` and apply a suspect rubric, in which case the rubric must be applied **symmetrically** to both lens families to avoid introducing an asymmetry that doesn't exist today. Option (a) keeps `swarm/merge.py` and the adversarial protocol untouched (consistent with FR-RH2.3 AC L69 "no scoring/ranking/dedup added to merge.py"); option (b) is a protocol change beyond this TDD's stated scope. Recommendation surfaced for the TDD author, not decided here.

---

## Key Takeaways

1. **`sc-bare-review` is the exact template for `ensemble.py`'s posture**: thin caller over the swarm dispatch surface, raw-forwards per-reviewer artifacts, never scores them itself, hands off to `/sc:adversarial`. `[CODE-VERIFIED]`
2. **The handoff is built from succeeded workers' `final_path`s, never the swarm merge.** `commands.py` L2066–2081 is the literal precedent: `suspect_files` = succeeded `final_path`s; `compare_files` = `<existing-review>` + those same paths. `reduce_wave3`'s merge is computed but excluded from the next-command. `[CODE-VERIFIED]`
3. **`validate_executor._build_multi_agent_steps` (L317–378) is proven per-agent-process fan-out prior art** (N model-bound steps → parallel group → adversarial-merge step consuming `reflect_outputs`), but each step is a `claude -p` subprocess — the nesting failure mode the in-process library import avoids. It is the §21 "subprocess-per-agent" alternative, untouched. `[CODE-VERIFIED]`
4. **`pipeline/process.py` is orthogonal** — a generic `claude -p` subprocess lifecycle primitive (`ClaudeProcess`) with zero awareness of reflect/adversarial/suspect/merge. It is the sanctioned subprocess mechanism *if* the optional `--detached` observability path shells out, but is uninvolved in the default in-process Mode-A handoff. `[CODE-VERIFIED]`
5. **Library import is the transport (NFR-RH2.2 — no second subprocess); CLI `--detached`/tmux is observability-only (NFR-RH2.7).** Deliberately separated. `[CODE-VERIFIED]`
6. **OI-4 resolves to "no rubric difference today, because Mode A doesn't read `suspect` at all."** Both lenses set `suspect:true/tier:T2` identically; Mode A's rubric has no suspect branch. The symmetry is real but vacuous; teaching Mode A `--suspect-source` would be an out-of-scope protocol change. `[CODE-VERIFIED]`

## Gaps and Questions

- **`[CODE-CONTRADICTED]` — `--suspect-source` is undocumented in `sc-adversarial-protocol/SKILL.md`.** The bare-review SKILL and `bare-review` lens both emit `/sc:adversarial --compare … --suspect-source …` (SKILL.md L55; `bare_review.py` L65–68), but the adversarial protocol SKILL (3002 lines) defines no `--suspect-source` flag and its Mode A input parser (L551–610) never lists it. The TDD must decide whether reflect's handoff relies on a flag the consumer doesn't formally parse, or passes suspect files via `--compare` with suspect handling advisory. (Surfaced for §21/OI-4.)
- **`ensemble.py` does not yet exist** — all handoff mechanics above are design targets grounded in the bare-review precedent, not observations of existing reflect code. The reflect package today has no `adversarial`/`swarm`/`final_path` references (grep over `runner.py`/`contract.py` returned only the verdict-trigger strings `adversarial_unavailable`, `merge_method`, `adversarial_convergence_score`). `[UNVERIFIED that the planned import shape compiles — depends on swarm dispatch public API stability, covered by research note 03-swarm-dispatch.md]`
- **`build_merge_prompt` content for reflect's Mode-A invocation not examined** — `validate_executor` uses a roadmap-specific `build_merge_prompt(reflect_outputs)`; whether reflect's `ensemble.py` reuses `sc-adversarial-protocol` Mode A as a skill invocation vs a prompt-built merge step is a design choice the TDD must state. (Out of this note's scope; flagged.)
- **OI-1 (the BLOCKING gate, PRD-extraction L243) is upstream of this note** — the swarm-ResultContract → reflect-contract field-correspondence table must land before FR-RH2.3 code; this note assumes `output_files[].final_path` / `status` fields exist as the bare-review contract shows, but the exact `WorkerResult`→contract mapping is OI-1's deliverable, not verified here.

## Summary

`ensemble.py` should replicate the `sc-bare-review` thin-caller pattern: form the Tier-2 reviewer fan-out by importing the swarm dispatch library **in-process** (NFR-RH2.2 — no second `claude -p` subprocess), collect each succeeded worker's normalized **`final_path`** from the swarm return contract (filtered on `status == "success"`, exactly as `commands.py` L2066–2070 does), and hand those per-reviewer artifacts to `/sc:adversarial` Mode A as `--compare <existing>,<final_path…>` + `--suspect-source <final_path…>` — **never** the swarm `mechanical_merge`/`merged.md` (FR-RH2.3). The `validate_executor` per-agent-process model is the proven §21 alternative but is rejected for the inner loop because its steps spawn `claude -p` children; the `superclaude swarm run --lens reflect-review` CLI (`--detached`/tmux) is retained solely as the NFR-RH2.7 observability variant. `pipeline/process.py` is an orthogonal subprocess primitive, uninvolved in the Mode-A handoff except as the sanctioned lifecycle mechanism for the optional detached path. OI-4 resolves to no rubric asymmetry — both lenses tag `suspect:true/tier:T2` identically and Mode A's rubric has no suspect branch — but a real contradiction surfaced: `--suspect-source` is emitted by the swarm/bare-review side yet undocumented and unparsed in `sc-adversarial-protocol/SKILL.md`, which the TDD must reconcile.

---
*Status: Complete*
