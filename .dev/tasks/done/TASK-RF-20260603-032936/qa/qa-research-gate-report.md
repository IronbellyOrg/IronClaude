# QA Report — Research Gate

**Topic:** sc-recommend lookup-cache layer (complex template-02 MDTM task build)
**Date:** 2026-06-03
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assume errors, verify every load-bearing claim against actual source.

---

## Overall Verdict: FAIL

FAIL on the strict zero-tolerance research-gate standard: the research is of unusually high
quality and ~95% of load-bearing claims independently verified against source, but there is ONE
cross-file factual contradiction (the NEW module path: `cli/recommend/` vs `cli/sc_recommend/`)
that would mislead the builder, plus a small cluster of off-by-one line-count errors in file 04
and one coverage gap worth a flag. None of the issues are deep — all are MINOR/IMPORTANT and a
single gap-fill round resolves them. No CRITICAL/hallucinated-evidence issues found.

---

## Verification Methodology

Independently re-verified every spot-check target named in the spawn prompt against ACTUAL source
files (not trusting the research files). Cited tool output below. 6 research files fully read;
research-notes.md + analyst stub read.

---

## Items Reviewed

| # | Check | Result | Evidence (independently verified) |
|---|-------|--------|-----------------------------------|
| 1 | File inventory / Status:Complete | PASS | All 6 files `Status: Complete` (04/05 say "Complete" in Summary; 05 header still says "In Progress" L3 — see I-3). Each has a Summary section. |
| 2 | convergence.py `save()` ~304 atomic tmp+os.replace | PASS | `sed 300-320`: `save()` at L304, `tmp_path = self.path.with_suffix(".tmp")` + `os.replace(...)`, `schema_version:1`, JSON body. Exactly as file 01/02 describe (incl. the file-02 nuance that it writes JSON not YAML). |
| 3 | convergence.py `load_or_create` ~104 hash-reset | PASS | `load_or_create` at L104; `data.get("spec_hash")==spec_hash` gate, `except (json.JSONDecodeError, KeyError)` → fresh. File 02 quote is VERBATIM-accurate. |
| 4 | install_mcp.py `check_mcp_server_installed` ~470 | PASS | At L470; substring `server_name.lower() in output.lower()`, fail-closed `False`. File 02 quote verbatim-accurate. |
| 5 | install_mcp.py `check_binary_available` ~156 | PASS | At L156; `[binary, "--version"]` exit-0, `FileNotFoundError`→False. Verbatim-accurate. |
| 6 | main.py registration block ~400-426 | PASS | Block at 400-426; tasklist idiom L412-414 + eval `.commands` L424-426 exactly as file 01/06 describe. New-reg snippet is correct. |
| 7 | install_hooks.py `_FRESHNESS_SCRIPTS` ~43 incl sc-recommend-phase0 | PASS | List opens L43; `"sc-recommend-phase0.sh"` IS at L85 (last entry). research-notes claim "already includes sc-recommend-phase0.sh:85" is CORRECT. |
| 8 | .gitignore L103 `.claude/cache/` + L117-118 blanket+settings exception | PASS | `nl`: L103 `.claude/cache/`, L117 `.claude/`, L118 `!.claude/settings.json`. Both regions exist exactly as files 01/06 map. git last-match-wins reasoning is sound. |
| 9 | pyproject `pyyaml>=6.0` | PASS | L38 `"pyyaml>=6.0"`. Confirmed. |
| 10 | eval/models.py NO token/model axis (EvalOutcome ~337, EvalSpec ~74) | PASS | `EvalOutcome` at L293 fields: eval_id/title/status/duration_sec/expects/skip_reason/skip_flag_triggered/artifacts/error_class — NO tokens, NO model. `EvalSpec` at L75: id/title/category/requires/timeout_sec/isolation/inputs/expects/parameterize/no_pty — NO model axis. File 03's single-most-load-bearing claim is TRUE. (Note: EvalOutcome is at L293 not L337; the L337-345 cite points into the same dataclass body — harmless.) |
| 11 | anthropic SDK ban + enforcement | PASS | `pyproject.toml:208-211` `[tool.ruff.lint.flake8-tidy-imports.banned-api]` with `"anthropic"`, `.Anthropic`, `.AsyncAnthropic` banned (FR-G1); `TID` selected in `select` L189; enforcement test `tests/cli/eval/test_ban_import_rule.py` exists. Ban points to PtyDriver/ClaudeProcessAdapter. File 06 §5 + file 03 claims VERIFIED. |
| 12 | test_cli_registration frozen roster (recommend must be added) | PASS | `EXPECTED_TOP_LEVEL_COMMANDS` frozenset matches file-06 quote VERBATIM; `test_top_level_command_roster_unchanged` asserts `unexpected` empty → adding `recommend` WITHOUT updating the set FAILS the test. Highly-actionable finding is CORRECT. |
| 13 | settings.json sc-recommend-phase0 PreToolUse registration | PASS | settings.json L16 `"matcher":"Skill"`, L21 `$CLAUDE_PROJECT_DIR/.claude/hooks/sc-recommend-phase0.sh`. File 06 §3.3 template accurate. |
| 14 | eval config.py scratch-root allowlist excludes .claude/cache/eval-runs | PASS | `config.py`: allowlist = `/tmp/eval-runs` + `.dev/eval-runs` (SCRATCH_ROOT_POLICY L42-52). Does NOT include `.claude/cache/eval-runs/`. File 03 FRICTION flag #4 CORRECT. |
| 15 | model_capability_matrix.yaml delegates per-model to /sc:adversarial | PASS | suite L12-13: invokes `/sc:adversarial --agents opus,sonnet,haiku`. Confirms it does NOT do harness-level panel. File 03 flag #3 CORRECT. |
| 16 | generate_review.py does NOT exist | PASS | `find .dev/eval-workspaces -name generate_review.py` → empty. File 03 claim CORRECT. |
| 17 | sc-reflect grader check_checkpoint_logged precedent | PASS | `check_checkpoint_logged` L212, `check_citation_resolves` L120, `check_yaml_list_contains` L172 in `.dev/eval-workspaces/sc-reflect/grader.py`. File 03 §2 CORRECT. |
| 18 | merged-req vs round-4 eval-reuse conflict surfaced honestly | PASS | `merged-requirements.md:259-269` DOES say reuse `.dev` scripts; `round-4:16,24,54` DOES say reuse cliEval harness. File 03 §1 "CONFLICT in the spec sources (must be resolved by the builder)" + flag #1 surfaces it explicitly, does NOT paper over. EXEMPLARY. |
| 19 | command count 42 (file 04) | PASS | `ls commands/*.md \| wc -l` = 42. Correct. |
| 20 | DERIVED claims flagged as inferences (not stated as fact) | PASS | YAML adaptation (file 02 §1e "derived — user did not specify"); new module layout ("Recommended", "builder's call"); classification-key vocabulary (file 04 §3.2 "DESIGN PROPOSAL", "only spec-generation is spec-confirmed", "needs_human_decision-adjacent"); Python-vs-prose ("DO NOT DECIDE", Resolution H vs P). All inference-tagged. STRONG. |
| 21 | hot-path "parent commits cache" given anthropic-ban + Haiku-cannot-write | PARTIAL | File 04 §4 + §2.3 cover "Haiku cannot write files; parent commits" (stated twice in spec) and split sha256/write to parent-Python. BUT neither file traces HOW the parent (a skill, not Python with anthropic SDK) actually invokes the Agent tool + commits — see GAP-1. |
| 22 | --eval = CLI subcommand vs skill Agent-fanout | PARTIAL | File 03 §3 says `--eval` is "a flag on the /sc:recommend skill invocation driven by an agent, not a superclaude eval run subcommand" (NO). File 06 §3.1 says wire `recommend_group` for "the --eval pipeline" (implies CLI subcommand YES). Contradiction overlaps GAP-1/I-1. |
| 23 | Module-path consistency across files | **FAIL** | Files 01+06 say NEW module = `src/superclaude/cli/recommend/` (8 refs, incl. test obligation on `recommend`); file 03 says `src/superclaude/cli/sc_recommend/` (5 refs). Both "verified does not exist" (trivially true — neither exists). Builder cannot create two. See I-1 (IMPORTANT). |

## Confidence

**Confidence:** Verified: 21/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 91.3%
(2 items rated PARTIAL count against confidence; they are coverage gaps, not unverified.)

**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 6 (each Bash batched multiple `grep`/`sed`/`wc` verifications mapping to specific checklist items above)

No web research performed (all claims internal/source-truth — Principle 6). tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| I-1 | IMPORTANT | files 01/06 vs 03 | **Module-path contradiction.** Files 01+06 target `src/superclaude/cli/recommend/`; file 03 targets `src/superclaude/cli/sc_recommend/`. Five+ references each. The builder needs ONE canonical module path — `cli/recommend/` is more consistent with the click-group name `recommend` (file 06's frozen-roster test obligation hardcodes `"recommend"`) and the `roadmap`/`tasklist`/`prd` peer convention (hyphen-free dir = group name). `sc_recommend` would force the group registration to import from a differently-named dir. | Builder must reconcile to ONE path before writing per-file items. Recommend `cli/recommend/` (matches command name + peer convention). Gap-fill: add a one-line note to file 03 OR a research-notes addendum declaring the canonical path so per-file checklist items don't split across two module names. |
| I-2 | MINOR | file 04, L14, §1 | **Self-contradicting line counts.** File 04 asserts "SKILL.md (227 lines — note: brief says 226, actual 227)" and refs "108/98/103". Independently `wc -l`: SKILL.md=226, surface-enum=107, delegation=97, plugin=102. File 04 is off-by-one HIGH on all four (file 01 + research-notes have the correct 226/107/97/102). Builder copying file-04's counts into items would cite wrong line totals. | Trust file 01 / research-notes counts (226/107/97/102). Gap-fill: correct file 04 §1 counts, or builder uses file 01's. Non-blocking for logic but a factual error in research. |
| I-3 | MINOR | file 05 L3 | File 05 header says `Status: In Progress` (L3) but its Summary (L219-227) says `Status: Complete` twice. Stale header. | Flip L3 to `Status: Complete` (content IS complete — fully covers template 02 + PENDING shapes). |
| GAP-1 | IMPORTANT | files 03/04 (coverage) | **The hot-path execution mechanism is under-specified for the builder.** The spec says "parent spawns Haiku via Agent tool" + "parent commits cache via atomic Python write" + "Haiku cannot write files," AND anthropic SDK is banned in-process. But NO research file traces the concrete seam: is the "parent" the SKILL (Claude orchestrating Agent-tool calls, with the YAML write done by... what? a skill can't run Python inline) OR a `superclaude recommend` CLI subcommand (Python that CANNOT spawn Agent-tool subagents — those are a Claude-harness construct, and the anthropic SDK is banned so Python can't call a model either)? This is the crux: Agent-tool spawning is Claude-only; atomic Python file-writes are CLI-only; the two cannot both live in one "parent." File 04 §4.4 frames Resolution H vs P but does NOT resolve the deeper "who is the parent process" question that the anthropic-ban makes acute. | This overlaps the existing `needs_human_decision` "Python-vs-skill boundary" item (research-notes GAP), so it is partially covered as a HALT gate — acceptable. BUT the builder needs the evidence sharpened: gap-fill should add one explicit paragraph (file 04 §4 or a new note) stating that "parent" is ambiguous between skill-orchestrator and CLI-subcommand, that Agent-tool spawn ⟹ Claude-side and atomic-write ⟹ Python-side are mutually-exclusive homes, and that the anthropic ban forecloses "Python parent calls Haiku directly." This makes the HALT item's options concrete. |
| GAP-2 | MINOR | file 03 §4 vs file 06 §3.1 | `--eval` entry-point is described inconsistently: file 03 says it is NOT a `superclaude eval` subcommand (it's a skill flag, agent-driven); file 06 says wire `recommend_group` for "the --eval pipeline" (CLI subcommand). Same ambiguity as GAP-1 (does eval orchestration run as Claude-fanout or Python CLI?). | Fold into the GAP-1 clarification — the `--eval` home follows from the parent-process resolution. Surface as a sub-bullet of the boundary HALT item. |

## What Was Done WELL (evidence the work is genuinely strong, not just unaudited)

- **Evidence density: DENSE (>80%).** Nearly every claim carries `file:line` + verbatim excerpts. Spot-checked ~15 distinct cited line ranges; all real and accurately quoted.
- **DERIVED claims are honestly inference-tagged** (item 20) — the highest-risk failure mode (inferences-as-facts) is well-controlled. File 02 §1e, file 04 §3.2 + §4 are model examples of flagging derivations.
- **The merged-req vs round-4 conflict is surfaced loudly** (item 18), exactly as the spawn prompt demanded — not papered over.
- **Adversarial seams the builder will hit are pre-flagged**: anthropic ban → eval-via-subprocess (file 06 §5, file 03), Haiku-cannot-write → parent-commits (file 04), frozen test roster → must update (file 06 §3.1), gitignore last-match-wins ordering (file 01/06 §4), scratch-root allowlist friction (file 03 #4).

## Actions Taken

None — `fix_authorization: false` (report-only). All issues documented above with specific fixes for the orchestrator/gap-fill round.

## Recommendations (single gap-fill round resolves all)

1. **Resolve I-1 (module path)** — declare `src/superclaude/cli/recommend/` canonical in a research-notes addendum or correct file 03's `sc_recommend` references. BLOCKS clean per-file checklist items.
2. **Sharpen GAP-1/GAP-2 (parent-process seam)** — add one paragraph making the skill-vs-CLI-subcommand ambiguity explicit, noting the anthropic-ban + Agent-tool-is-Claude-only constraints. This feeds the existing Python-vs-skill `needs_human_decision` HALT item with concrete options. Does NOT require deciding — just sharper evidence.
3. **Fix I-2/I-3 (cosmetic)** — correct file 04 line counts and file 05 status header. Low priority; builder can rely on file 01's correct counts.

After gap-fill, this research is green-light quality for a complex template-02 build. The substance is excellent; the FAIL is on the strict "any gap = FAIL" rule (I-1 contradiction + GAP-1 under-specification), not on research depth.

---

## QA Complete

VERDICT: FAIL (gap-fill round, then PASS-eligible. 1 IMPORTANT contradiction [I-1], 1 IMPORTANT coverage gap [GAP-1], 2 MINOR cosmetic [I-2/I-3], 1 MINOR ambiguity [GAP-2]. No CRITICAL, no hallucinated evidence.)
