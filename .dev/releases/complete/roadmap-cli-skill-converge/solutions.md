---
type: "🧠 Solution Brainstorm"
release: "roadmap-cli-skill-converge"
date: "2026-05-15"
brainstormer: "sc:brainstorm pass"
items_addressed: 11
solutions_per_item: 3
total_solutions: 33
---

# Solution Brainstorm — Roadmap CLI ↔ Skill / Command Convergence

**Cross-cutting design decision recap.** Each item below has solutions that lean toward one of three postures: **(A) Option 1 — CLI is canonical**, rewrite the skill/command to mirror CLI 1:1 (tight coupling, generated or hand-mirrored); **(B) Option 2 — parallel inference surface**, keep current skill richness, add "Relationship to CLI" disclaimers (loose coupling, two documented surfaces); **(C) hybrid / decoupled**, factor shared vocabulary into a crosswalk artifact while letting each surface own its execution semantics. Solution 1s in the body generally lean Option 1, Solution 2s generally lean Option 2, Solution 3s generally explore the hybrid axis or a higher-risk reshape. The user picks the design posture once; the per-item recommendations below presume Option 1 unless explicitly noted.

---

## B-1 — `commands/roadmap.md` flag-set drift

**Verification status:** VERIFIED — command has 6 flags CLI lacks; CLI has 11 flags command lacks; default `--output` differs (`.dev/releases/current/<spec-name>/` vs `input_files[0].parent`).

**Solution 1: Full 1:1 flag-table rewrite**
- **Approach:** Replace the flag table at `commands/roadmap.md:22-37` with a hand-authored mirror of `cli/roadmap/commands.py:34-149`. Drop `--specs`, `--template/-t`, `--multi-roadmap`, `--interactive/-i`, `--compliance/-c`, `--persona/-p`. Add the 11 CLI-only flags. Rewrite the examples block to use `--agents opus:architect,haiku:architect`, `--input-type`, `--tdd-file`, `--prd-file`. Fix default output to "parent dir of spec-file".
- **Files touched:** `src/superclaude/commands/roadmap.md` (sections: frontmatter unchanged; §Usage, §Flags, §Examples, §Output rewritten).
- **Effort:** M
- **Reversibility:** moderate (git revert restores; muscle-memory of `--multi-roadmap` users lost).
- **Pros:** Single source of truth; matches CLI `--help` exactly; eliminates user confusion; satisfies AC-5.
- **Cons:** Loses inference-only ergonomics (`--persona`, `--compliance`); users with existing `--multi-roadmap` muscle memory break; doc maintenance cost on every CLI flag addition.
- **Best when:** Option 1 chosen and team commits to keeping CLI authoritative going forward.

**Solution 2: Disclaimer + "Relationship to CLI" header**
- **Approach:** Prepend a "Relationship to CLI" section to `commands/roadmap.md` after the frontmatter listing inference-only flags and pointing at `superclaude roadmap run --help`. Leave the existing flag table intact. Add a footnote on each inference-only flag (`--multi-roadmap`, `--compliance`, `--persona`, etc.) clarifying "no CLI equivalent — inference layer only".
- **Files touched:** `src/superclaude/commands/roadmap.md` (insert ~20-line header block; annotate flag rows in §Flags).
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Surgical; preserves inference ergonomics; cheap to maintain; honest about divergence.
- **Cons:** Two surfaces remain non-isomorphic; users still confused about which flags actually work; flag table still drifts as CLI evolves.
- **Best when:** Option 2 chosen; team values the inference UX more than 1:1 parity.

**Solution 3: Generated flag table from `--help`**
- **Approach:** Add a `make sync-flags` Makefile target that runs `superclaude roadmap run --help` and `--help` for each subcommand, parses the output, and writes a `<!-- BEGIN CLI-FLAGS -->`/`<!-- END CLI-FLAGS -->` fenced block inside `commands/roadmap.md`. Inference-only flags live in a separate frozen block above the generated section.
- **Files touched:** `Makefile` (new target), `src/superclaude/commands/roadmap.md` (insert fenced markers), `scripts/sync-flags.py` (new).
- **Effort:** L
- **Reversibility:** hard (introduces tooling dependency).
- **Pros:** Eliminates future drift mechanically; CI can `make sync-flags && git diff --exit-code` to fail on drift.
- **Cons:** New tooling to maintain; brittle if `argparse` output format changes; over-engineered for two files.
- **Best when:** Convergence is a recurring problem across many commands, not a one-shot fix.

**Recommendation:** Solution 1 — Option 1 is the stated direction in the release scope, and a hand-authored mirror is the right granularity for two files.

---

## B-2 — `commands/validate-roadmap.md` frontmatter + flag-set drift

**Verification status:** PARTIAL (treat as VERIFIED) — `name: validate-roadmap` missing `sc:` prefix at `:2`; 7 inference-only flags; 3 CLI flags missing (`--model`, `--max-turns`, `--debug`); output-dir mismatch confirmed; NFR-006 (exit 0 always) undocumented.

**Solution 1: Full 1:1 rewrite + frontmatter fix + NFR-006 callout**
- **Approach:** Fix `:2` to `name: sc:validate-roadmap`. Replace flag table at `:27-37` with the CLI's `validate` signature (`output_dir` positional, `--agents`, `--model`, `--max-turns`, `--debug`). Drop `--specs`, `--exclude/-x`, `--max-agents`, `--skip-adversarial`, `--skip-remediation`, `--report/-r`, `--prior-taxonomy`. Add an explicit "Exit codes (NFR-006)" subsection stating exit is always 0. Fix output-dir reference at `:30` to `<OUTPUT_DIR>/validate/`.
- **Files touched:** `src/superclaude/commands/validate-roadmap.md` (§Frontmatter, §Usage, §Flags, §Output, new §Exit codes).
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Resolves all 4 sub-claims at once; satisfies AC-5; CC/CI behavior of exit-0 becomes discoverable.
- **Cons:** Loses deep-validation flag UX (`--skip-adversarial`, `--max-agents`); inference users must drop those flags.
- **Best when:** Option 1 chosen.

**Solution 2: Cosmetic-only — frontmatter fix + disclaimer header**
- **Approach:** Fix `:2` to `name: sc:validate-roadmap`. Add a "Relationship to CLI" header naming the 3 missing CLI flags and stating "CLI exits 0 always (NFR-006)". Leave the deep-validation flag set intact. Fix the path reference at `:30` to match `validate_executor.py:468` (`<OUTPUT_DIR>/validate/`) since both surfaces should at least agree on terminology.
- **Files touched:** `src/superclaude/commands/validate-roadmap.md` (frontmatter line, new header block ~15 lines, one path fix).
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Tiny diff; preserves inference flag set; closes the trivially-wrong items (name prefix, output dir) without philosophy.
- **Cons:** Two surfaces remain non-isomorphic; NFR-006 buried in disclaimer rather than first-class.
- **Best when:** Option 2 chosen.

**Solution 3: Split the file — `validate-roadmap.md` (CLI mirror) + `validate-roadmap-deep.md` (inference)**
- **Approach:** Rename current file to `validate-roadmap-deep.md` (an explicit inference-only deep-validation command). Create new `validate-roadmap.md` that is a 1:1 mirror of CLI `validate`. Update `commands/sc:` slash binding so `/sc:validate-roadmap` points at the CLI mirror; introduce `/sc:validate-roadmap-deep` for the rich inference flow.
- **Files touched:** Two files in `src/superclaude/commands/`; sync targets in `.claude/commands/sc/`; cross-references in skill files.
- **Effort:** L
- **Reversibility:** hard.
- **Pros:** Both surfaces fully preserved; users choose explicitly; no false isomorphism.
- **Cons:** New command surface to maintain; sync logistics multiply; risks user confusion about which command to call.
- **Best when:** Team wants to keep deep validation but also wants CLI-faithful surface — strongly post Option 1/2 fork.

**Recommendation:** Solution 1 — fixes all four sub-claims cleanly under Option 1.

---

## B-3 — `sc-roadmap-protocol/SKILL.md` pipeline taxonomy mismatch

**Verification status:** VERIFIED — Wave 0–4 + Post-Wave in SKILL.md; CLI has 14 named steps; 6 step names absent from skill; thresholds (0.6/0.5 + 85%/70%) absent from CLI gates; 2–10 agent range not in CLI.

**Solution 1: Replace Wave taxonomy with 14-step CLI taxonomy**
- **Approach:** Rewrite `SKILL.md:84-260` (Wave Architecture section). New §4 enumerates the 14 steps from `_get_all_step_ids` at `executor.py:2156-2170`: `extract → generate-A ∥ generate-B → diff → debate → score → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate → certify`. Each gets an H3 with inference instructions matching the CLI prompt builder. Remove `convergence_score ≥ 0.6 → PASS` thresholds; replace with citation of `cli/roadmap/gates.py`. Drop the "2–10 agents" claim or scope it to "N≥2 for debate/merge".
- **Files touched:** `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` (lines 84–260 plus the validation.md ref).
- **Effort:** L
- **Reversibility:** hard (large reshape).
- **Pros:** True 1:1 mental model with CLI; eliminates orphan thresholds (OQ-2); skill instructions become directly verifiable against CLI step IDs.
- **Cons:** Large diff (~3-5 KB net); risk of introducing skill-side bugs; loses the Wave abstraction users may already know.
- **Best when:** Option 1 chosen and team is willing to invest a full pass on the skill.

**Solution 2: Crosswalk table + top-of-file disclaimer**
- **Approach:** Insert §3.5 "Crosswalk: Waves ↔ CLI Steps" before §4. A 2-column table: Wave → CLI step set. Add an opening paragraph in the YAML description noting "thresholds in this file are inference-only and may differ from CLI gate criteria in `cli/roadmap/gates.py`". Leave Wave Architecture intact otherwise.
- **Files touched:** `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` (~30 line insert).
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Lowest risk; preserves Wave mental model; surfaces the 6 missing step names in the table; clarifies thresholds are inference-only.
- **Cons:** Doesn't eliminate the divergence; reader must mentally translate; thresholds remain orphan.
- **Best when:** Option 2 chosen.

**Solution 3: Two-tier rewrite — Waves stay as orchestration, steps become substeps**
- **Approach:** Keep Wave 0–4 as the high-level orchestration outline but add an explicit "CLI step mapping" sub-section under each Wave listing which of the 14 CLI step IDs fall inside it (e.g., Wave 2 → `debate, score, merge, anti-instinct`). Reconcile thresholds by adopting CLI gate criteria as canonical and reframing the 0.6/0.5 thresholds as "inference heuristics — fall back to CLI gates for hard pass/fail".
- **Files touched:** `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` (~150-200 lines edited inside §4).
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Preserves both abstractions; users can read either way; lower risk than full rewrite; addresses all 4 sub-claims.
- **Cons:** Compound model — readers may still not know which to trust; thresholds reconciled but still present.
- **Best when:** Hybrid posture — team values Wave pedagogy but wants every CLI step explicitly mapped.

**Recommendation:** Solution 3 — best balance of preserving accumulated skill pedagogy while making CLI step IDs first-class.

---

## B-4 — `refs/scoring.md` stale CLI cross-reference

**Verification status:** PARTIAL (treat as VERIFIED) — cross-reference at `:18` claims algorithm match; TDD detection present, PRD detection algorithm omitted; CLI checks PRD signals *first* per `executor.py:73-148`.

**Solution 1: Re-derive scoring tables from `executor.py:73-148`**
- **Approach:** Rewrite `refs/scoring.md` to add a §0 "PRD Detection (checked first)" with the 5 PRD signals (type field, 12 section headings, user-story pattern, JTBD pattern, tags, threshold ≥5), then §1 "TDD Detection (checked second)" (existing content). Update line 18 cross-reference to cite `executor.py:73-148` and the exact function name `_detect_input_type`. Keep PRD enrichment section at `:165-171` as §3.
- **Files touched:** `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md`.
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Fixes the omission; preserves the file's purpose; cross-reference becomes verifiable.
- **Cons:** Risk of misreading `executor.py` signal definitions; need to keep in sync if CLI signals change.
- **Best when:** Either Option 1 or Option 2.

**Solution 2: Inline-quote the CLI source**
- **Approach:** Replace prose scoring tables with a fenced ```python block excerpted from `executor.py:73-148` (the actual signal-counting logic), followed by a one-paragraph annotation. Add a `<!-- source: cli/roadmap/executor.py:_detect_input_type as of <git-sha> -->` comment at the top.
- **Files touched:** `refs/scoring.md`.
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Zero translation error — readers see exactly what CLI does; sha stamp lets reader notice staleness.
- **Cons:** Code-in-docs duplicates source; updates require copy-paste; sha stamp drifts silently unless enforced.
- **Best when:** Team prefers verbatim over prose summaries.

**Solution 3: Delete `refs/scoring.md`; cross-link to CLI source**
- **Approach:** Remove the file. Replace with a stub or top-level reference in SKILL.md that points readers to `cli/roadmap/executor.py:_detect_input_type` directly. Acknowledge that detection is a deterministic CLI concern, not an inference concern.
- **Files touched:** `refs/scoring.md` (delete), `SKILL.md` (small reference update).
- **Effort:** S
- **Reversibility:** moderate (file deletion).
- **Pros:** Eliminates drift entirely; honest about who owns the algorithm; reduces skill footprint.
- **Cons:** Skill loses self-contained reference; offline readers can't see the scoring; Option 2 posture is implicitly weakened.
- **Best when:** Option 1 chosen and team prefers source-of-truth purity over self-contained skill docs.

**Recommendation:** Solution 1 — restores the missing PRD-detection algorithm with low risk.

---

## B-5 — `refs/templates.md` 4-tier discovery vs single-template CLI

**Verification status:** VERIFIED — 4 tiers in skill at `:7-36`; CLI has single `ROADMAP_TEMPLATE` constant and `get_template_path(name)` with no tier system.

**Solution 1: Collapse to single-template reference**
- **Approach:** Rewrite `refs/templates.md` to describe the CLI's `get_template_path()` behavior only: `importlib.resources` lookup → src-relative fallback → file resolution. Drop Tier 1 Local, Tier 2 User, Tier 3 Plugin, Tier 4 Inline generation. Add a `ROADMAP_TEMPLATE = "roadmap_template.compressed.md"` callout matching `templates.py:14`.
- **Files touched:** `refs/templates.md`.
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Eliminates fiction; readers stop expecting tier behavior that doesn't exist; aligns with Option 1.
- **Cons:** Loses the inference-only fallback design that some users may have relied on; "future v5.0 plugin marketplace" framing disappears.
- **Best when:** Option 1.

**Solution 2: Disclaimer at top + keep 4-tier as roadmap**
- **Approach:** Add a header: "The 4-tier discovery below is inference-only. The CLI currently uses a single template resolved by `get_template_path()` in `templates.py`. Tier 3 (Plugin) is roadmap-only." Leave the tier descriptions intact as forward-looking design.
- **Files touched:** `refs/templates.md` (~10 line insert).
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Preserves design intent for future; honest about current state; tiny diff.
- **Cons:** Readers still see a 4-tier model and may implement around it; design-vs-reality remains co-mingled.
- **Best when:** Option 2.

**Solution 3: Split into `refs/templates.md` (current CLI) + `refs/templates-future.md` (4-tier vision)**
- **Approach:** Move the 4-tier discovery to a new file `refs/templates-future.md` clearly marked as design vision. Rewrite `refs/templates.md` to mirror CLI behavior.
- **Files touched:** `refs/templates.md` (rewrite), `refs/templates-future.md` (new), SKILL.md references.
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Both narratives preserved; reality and vision visibly separated.
- **Cons:** Two files to maintain; risks orphaning the vision file; readers may still confuse them.
- **Best when:** Team wants to preserve the 4-tier design for a future plugin release.

**Recommendation:** Solution 1 — the 4-tier design has no implementation runway; collapse and move on.

---

## B-6 — `refs/validation.md` sub-agent pattern absent from CLI

**Verification status:** VERIFIED — `quality-engineer` + `self-review` sub-agents and REVISE loop (max 2) in skill `:8, :76, :171-196`; CLI has no `Task(`, no sub-agent spawn, only subprocess `ClaudeProcess` and gate criteria.

**Solution 1: Replace sub-agent dispatch with CLI gate-criteria flow**
- **Approach:** Rewrite `refs/validation.md` to describe `cli/roadmap/validate_gates.py`'s `REFLECT_GATE` and `ADVERSARIAL_MERGE_GATE` (frontmatter checks + semantic checks). Remove the `Dispatch this prompt to a quality-engineer sub-agent` lines and the REVISE loop. Add a sub-section "Inference equivalent" that maps gate criteria to a single-shot self-check prompt (no sub-agent).
- **Files touched:** `refs/validation.md`.
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Skill no longer claims behavior CLI doesn't execute; reduces complexity; aligns with Option 1.
- **Cons:** Loses inference enhancement that may actually catch bugs the CLI misses; REVISE-loop value disappears.
- **Best when:** Option 1.

**Solution 2: Move sub-agent pattern to "Optional inference enhancement" appendix + disclaimer**
- **Approach:** Move the `quality-engineer`/`self-review`/REVISE sections into a clearly-labelled appendix at the bottom of `refs/validation.md`. Add a top-of-file note: "The CLI uses deterministic gate criteria from `cli/roadmap/validate_gates.py`. The sub-agent pattern below is an inference-only enhancement and is not part of CLI behavior."
- **Files touched:** `refs/validation.md` (reorganize, add disclaimer).
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Preserves the inference enhancement; honest about non-CLI nature; lowest risk.
- **Cons:** Doesn't reduce file size; readers may still implement the sub-agent pattern thinking it's canonical.
- **Best when:** Option 2.

**Solution 3: Delete file entirely; fold gate criteria into SKILL.md**
- **Approach:** Delete `refs/validation.md`. Inline a 1-paragraph reference to `validate_gates.py` in SKILL.md's validation section. Document that validation is a CLI concern; skill stops claiming a parallel validation pipeline.
- **Files touched:** `refs/validation.md` (delete), `SKILL.md` (small edit).
- **Effort:** S
- **Reversibility:** moderate (deletion).
- **Pros:** Maximum simplification; eliminates entire drift vector; SKILL.md becomes more honest about its scope.
- **Cons:** Loses validation guidance entirely for the inference layer; users hit a wall when validating inference output.
- **Best when:** Aggressive Option 1.

**Recommendation:** Solution 1 — fixes the drift without losing the validation guidance; sub-agent enhancement can be reintroduced later if measured to add value.

---

## B-7 — `refs/extraction-pipeline.md` 8-step extraction vs single CLI prompt

**Verification status:** VERIFIED — 8 sequential steps in skill `:7-9`; CLI has single `Step(id="extract", ...)` via `build_extract_prompt` / `build_extract_prompt_tdd`.

**Solution 1: Collapse to single-pass reference mirroring `build_extract_prompt`**
- **Approach:** Rewrite `refs/extraction-pipeline.md` to describe the single CLI prompt builder. Preserve the per-step rationale as design-notes commentary under one heading "Eight-aspect coverage inside one prompt" — the 8 original steps become bullet points the prompt covers in parallel, not sequential phases.
- **Files touched:** `refs/extraction-pipeline.md`.
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Aligns with CLI; preserves design intent; reduces reader confusion about sequencing.
- **Cons:** Loses prescriptive 8-step structure; risk of dropping useful detail in the collapse.
- **Best when:** Option 1.

**Solution 2: Disclaimer header + 8-step as inference framework**
- **Approach:** Add header: "This 8-step decomposition is an inference-only thinking framework. The CLI consolidates extraction into a single prompt built by `build_extract_prompt` (or `build_extract_prompt_tdd` for TDD input)." Leave the 8-step content intact.
- **Files touched:** `refs/extraction-pipeline.md` (~10 line insert).
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Preserves the pedagogy; honest about CLI behavior; tiny diff.
- **Cons:** Two mental models persist; inference users may waste cycles executing the 8 steps sequentially.
- **Best when:** Option 2.

**Solution 3: Rewrite as annotated CLI prompt with embedded 8-aspect checklist**
- **Approach:** Replace the file body with the actual `build_extract_prompt` text (or a sanitized version) and annotate it with the 8 original aspects as inline markers. Cite `prompts.py:180` and `:328` exactly.
- **Files touched:** `refs/extraction-pipeline.md`.
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Highest fidelity; readers see exactly what the CLI sends to the LLM; 8-aspect lineage preserved as annotations.
- **Cons:** Tight coupling — prompt changes require ref update; duplicates source; risks confusion if CLI prompt evolves.
- **Best when:** Hybrid posture.

**Recommendation:** Solution 1 — collapse to single-pass; the 8-step framing is more pedagogy than process.

---

## B-8 — `refs/adversarial-integration.md` `sc:adversarial-protocol` delegation

**Verification status:** VERIFIED — multiple `Skill sc:adversarial-protocol args: "..."` invocations at `:83, 102, 112, 126, 135, 137`; CLI uses single-shot `build_debate_prompt` at `prompts.py:878-902` with `_DEPTH_INSTRUCTIONS`.

**Solution 1: Remove delegation; replace with CLI debate flow**
- **Approach:** Rewrite `refs/adversarial-integration.md` to describe `build_debate_prompt` with depth-controlled rounds (`_DEPTH_INSTRUCTIONS` at `prompts.py:18-37`). Remove every `Skill sc:adversarial-protocol args` invocation. Update SKILL.md `:417-424` to drop the D-0001 reversal claim.
- **Files touched:** `refs/adversarial-integration.md`, `SKILL.md` (lines 417-424).
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Eliminates delegation that CLI doesn't do; reader sees CLI-faithful debate flow.
- **Cons:** `sc:adversarial-protocol` is a real skill with value — losing the delegation removes a reusable abstraction; some debates may genuinely benefit from the richer protocol.
- **Best when:** Option 1.

**Solution 2: Mark delegation as inference-only enhancement; document CLI alongside**
- **Approach:** Restructure `refs/adversarial-integration.md` into two sections: §A "CLI debate (single-shot)" describing `build_debate_prompt`, §B "Inference enhancement: sc:adversarial-protocol delegation" with the existing content. Top-of-file note: "the CLI debate step is single-shot; sc:adversarial-protocol is an inference-only enrichment".
- **Files touched:** `refs/adversarial-integration.md`, SKILL.md note around `:417-424`.
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Preserves the delegation value; honest about CLI; clear "use which when" guidance.
- **Cons:** Two flows for users to grok; risk that inference users still pick the richer one by default and waste budget.
- **Best when:** Option 2.

**Solution 3: Move delegation into `sc-adversarial-protocol` SKILL.md as an inbound integration; trim this ref**
- **Approach:** Move the integration writeup to the *target* skill (`sc-adversarial-protocol`) as an "inbound consumers" section. Reduce `refs/adversarial-integration.md` to a short reference: "CLI uses `build_debate_prompt` (single-shot). For richer debate, the skill may delegate to `sc:adversarial-protocol`; see that skill's docs for invocation."
- **Files touched:** `refs/adversarial-integration.md` (shrink), `sc-adversarial-protocol/SKILL.md` (add section).
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Each skill owns its surface; reduces duplication; cleaner inversion of dependency direction.
- **Cons:** Touches a skill outside this release scope; coordination cost.
- **Best when:** Cross-skill cleanup is permitted in scope.

**Recommendation:** Solution 1 — remove delegation to match CLI; the D-0001 reversal can be reconsidered in a separate release if needed.

---

## B-9 — `sc-validate-roadmap-protocol/SKILL.md` entirely different pipeline from CLI

**Verification status:** VERIFIED — 7 numbered phases + 2 bracketing phases; CC1–CC4 cross-cutting agents; GO/CONDITIONAL_GO/NO_GO verdict matrix; Auggie/Serena enrichment. CLI does `_validate_input_files → build steps → execute_pipeline → _parse_report_counts` against 7 dimensions.

**Solution 1: Major rewrite to mirror CLI reflect + adversarial-merge flow**
- **Approach:** Replace `SKILL.md:96-1000+` with a CLI-faithful description: §0 input validation, §1 build single-agent or multi-agent steps, §2 execute pipeline, §3 parse report counts, §4 dimensional checks (Schema, Structure, Traceability, Cross-file consistency, Parseability, plus Coverage/Proportionality or Interleave/Decomposition). Drop CC1–CC4, drop GO/CONDITIONAL_GO/NO_GO, drop phase numbering. Preserve Auggie/Serena enrichment as optional Phase 0 prep.
- **Files touched:** `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` (most of the ~56 KB).
- **Effort:** L
- **Reversibility:** hard.
- **Pros:** Skill becomes CLI counterpart in fact, not name; orphan verdict matrix retired; OQ-3 resolved by collapse.
- **Cons:** Major content loss; risk that the rich validation philosophy was actually adding signal; user re-learning cost; large reviewer burden.
- **Best when:** Option 1, strongly.

**Solution 2: Top-of-file disclaimer + crosswalk; preserve rich pipeline**
- **Approach:** Add 30-line opening section: "This is an inference-only deep-validation protocol. The CLI counterpart at `superclaude roadmap validate` runs a simpler reflect + adversarial-merge flow against 7 fixed dimensions (see `cli/roadmap/validate_prompts.py:7,68,74-123`). Use this skill for thorough investigative validation; use the CLI for automated CI/CD gating." Add a crosswalk table mapping each Phase to CLI dimensions where overlap exists.
- **Files touched:** `SKILL.md` (insert opening section, add table).
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Preserves the entire inference investment; honest framing; lowest risk.
- **Cons:** Two surfaces persist; 56 KB of inference content still in repo; OQ-3 unresolved.
- **Best when:** Option 2.

**Solution 3: Split — CLI-mirror SKILL + deep-validation companion skill**
- **Approach:** Rewrite `SKILL.md` to be a CLI-faithful counterpart (Solution 1 content). Create new skill `sc-validate-roadmap-deep` with the current rich content. Update `/sc:validate-roadmap` slash command to route to either based on a flag (or the deep one becomes `/sc:validate-roadmap-deep`).
- **Files touched:** `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` (rewrite), new skill directory + SKILL.md, slash command routing.
- **Effort:** L
- **Reversibility:** hard.
- **Pros:** Both surfaces survive; users pick explicitly; clearest mental model.
- **Cons:** Skill proliferation; sync targets multiply; coordinates with B-2 Solution 3.
- **Best when:** Pairs naturally with B-2 Solution 3 if team wants both flavors.

**Recommendation:** Solution 2 — the deep-validation pipeline likely has real value; disclaim first, rewrite only if measured drift damage justifies it.

---

## B-10 — `sc-validate-roadmap-protocol` packaging shape

**Verification status:** VERIFIED — only `SKILL.md` (56 KB); no `refs/`, `rules/`, `templates/` subdirs. Sibling `sc-roadmap-protocol` has `refs/`.

**Solution 1: Factor SKILL.md into `refs/` subdirectory**
- **Approach:** Create `refs/extraction.md`, `refs/decomposition.md`, `refs/adversarial.md`, `refs/remediation.md`, `refs/cc-agents.md` (or topics determined by content boundaries). Move corresponding sections out of SKILL.md and replace with references. Mirror `sc-roadmap-protocol` shape.
- **Files touched:** `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` + new `refs/*.md` files.
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Structural consistency with sibling skill; smaller SKILL.md improves on-load token efficiency; refs load on demand.
- **Cons:** Non-blocking effort; new files must be kept in sync; if B-9 Solution 1 lands, much of this content is going away anyway.
- **Best when:** B-9 Solution 2 chosen (deep pipeline preserved) — factoring is then worth it.

**Solution 2: Leave as-is**
- **Approach:** No change. Document the single-file shape as intentional in a comment.
- **Files touched:** none.
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Zero risk; respects "if it works, leave it"; cheapest option.
- **Cons:** Structural inconsistency persists; SKILL.md remains 56 KB heavy.
- **Best when:** B-9 Solution 1 chosen (most content goes away) or release scope tight.

**Solution 3: Lazy-split — only factor sections that are reusable across skills**
- **Approach:** Identify the 1–2 sections that have reuse potential (e.g., remediation rubric, CC-agent dispatch templates). Factor only those into `refs/`. Leave the rest in SKILL.md.
- **Files touched:** SKILL.md, 1–2 new `refs/*.md`.
- **Effort:** S
- **Reversibility:** easy.
- **Pros:** Surgical; preserves most of SKILL.md while introducing the `refs/` shape; opens path for future factoring.
- **Cons:** Doesn't achieve full structural parity; reviewer must decide what to factor.
- **Best when:** Middle path between B-9 outcomes.

**Recommendation:** Solution 2 — defer until B-9 design is settled; structure-only refactor is premature.

---

## B-12 — Synced copies will need refresh after src updates

**Verification status:** VERIFIED — all three locations currently in sync (md5 confirmed); but edits to `src/` will diverge until `make sync-dev` + manual copy to `/config/.claude/`.

**Solution 1: Run `make sync-dev` + manual `/config/.claude/` copy after B-1/B-2 land**
- **Approach:** After B-1 and B-2 commits land in `src/`, run `make sync-dev` to refresh `.claude/commands/sc/`; then `cp src/superclaude/commands/roadmap.md /config/.claude/commands/sc/` and same for `validate-roadmap.md`. Re-run md5sum to confirm three-way parity. Record in commit message.
- **Files touched:** `.claude/commands/sc/roadmap.md`, `.claude/commands/sc/validate-roadmap.md`, `/config/.claude/commands/sc/roadmap.md`, `/config/.claude/commands/sc/validate-roadmap.md` (all auto-updated).
- **Effort:** S
- **Reversibility:** easy (re-run sync).
- **Pros:** Mechanical; uses existing tooling; matches current dev workflow.
- **Cons:** Manual step for global copy is brittle (could be forgotten); future similar releases repeat the gap.
- **Best when:** One-shot release; team accepts manual global step.

**Solution 2: Extend `make sync-dev` to also sync `/config/.claude/`**
- **Approach:** Modify `Makefile` `sync-dev` target to additionally copy `src/superclaude/commands/`, `src/superclaude/skills/`, `src/superclaude/agents/` into `/config/.claude/`. Add a `verify-sync` extension that md5-checks the global location too.
- **Files touched:** `Makefile`, possibly a sync script.
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Permanent fix; global sync no longer a forgettable manual step; benefits every future release.
- **Cons:** Out of release scope (touches build tooling); risks unintended overwrites if user has local-only edits in `/config/.claude/`.
- **Best when:** Team commits to global install as canonical (answers OQ-4 yes).

**Solution 3: Add a post-merge CI check (md5 three-way parity)**
- **Approach:** Add a script (`scripts/check-sync.sh`) that md5sums all command files across the three locations and fails CI if they diverge. Run on every PR touching `src/superclaude/commands/` or `skills/`.
- **Files touched:** `scripts/check-sync.sh` (new), CI config.
- **Effort:** M
- **Reversibility:** moderate.
- **Pros:** Catches drift mechanically; defends against future regressions; orthogonal to manual vs Makefile sync.
- **Cons:** New CI tooling; doesn't fix drift, only detects it; requires CI infrastructure investment.
- **Best when:** Team has CI capacity and wants long-term drift prevention.

**Recommendation:** Solution 1 — minimal, matches existing workflow; revisit Solution 2 if drift recurs.

---

## Cross-cutting observations

**Shared solution shapes.** Three groups emerge: (i) **flag/frontmatter mirroring** — B-1, B-2 — both want Solution 1 hand-authored 1:1 rewrites under Option 1, both fall back to a small "Relationship to CLI" header under Option 2; (ii) **skill ref drift with low coupling cost** — B-4, B-5, B-7 — collapse-and-cite solutions are cheap and largely independent of the Option 1/2 fork; (iii) **structural rewrites of large skill content** — B-3, B-6, B-8, B-9 — these are the high-stakes items where Option 1 means significant content loss and Option 2 means leaving 56+ KB of inference content in place behind a disclaimer.

**Sequencing.** B-12 sync depends strictly on B-1 + B-2 landing first (it's mechanical post-step). B-10 packaging should follow B-9 outcome — if B-9 Solution 1 lands (major content reduction), B-10 Solution 2 (leave as-is) becomes correct by accident. B-3 thresholds reconciliation interacts with B-6: if B-6 Solution 1 removes the sub-agent REVISE loop, the 85%/70% aggregate thresholds in B-3 lose their last home and should be dropped in the same pass. B-8 D-0001 reversal claim in SKILL.md must be edited consistently with whatever B-3 says about delegation.

**Fourth-option drafts ruled out.** For B-9, considered "generate SKILL.md from the CLI prompt files mechanically" — rejected because the skill is meant to guide an LLM, not to replicate prompts verbatim; mechanical generation would lose pedagogical context. For B-1, considered "deprecate the slash command entirely and route `/sc:roadmap` to invoke the CLI as a subprocess" — rejected because it conflicts with the inference-layer purpose and is out of release scope. For B-11 (now refuted), no solutions proposed.
