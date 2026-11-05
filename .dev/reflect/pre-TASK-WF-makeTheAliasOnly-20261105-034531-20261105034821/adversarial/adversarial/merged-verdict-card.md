<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 3 (reviewer-3 card, refactorer, claude-opus-5-5) -->
<!-- Incorporated: Variant 1 (reviewer-1 card, analyzer, claude-sonnet-5-5); Variant 2 (reviewer-2 card, qa, glm-5.3 on the haiku alias) -->
<!-- Merge date: 2026-11-05 -->
<!-- Plan applied: refactor-plan.md (6 planned changes); merged ids M-1.., source ids kept in brackets -->

# Merged reviewer card (plan review)

Merged from the three reviewer cards by the sc:adversarial merge step. Every claim and citation below is copied from the variant named in its source tag.

<!-- Source: V3 Verdict (base), updated by refactor-plan changes 1 and 2; V1 PASS_WITH_NOTES rejected (refactor-plan X-001) -->
## Verdict

FAIL. Four blocking defects, each a small plan edit:

1. M-1: Task 2's comment puts the literal tier id into `src/superclaude/cli/`, which the Task 1 policy test forbids, and no task runs the whole policy test file [R3-1].
2. M-2: Task 9's failing-first launcher test is never run, and the test harness cannot see the three variables [R3-2].
3. M-3: Task 3's acceptance grep cannot pass with the bullet text Task 3 mandates [R2-1].
4. M-4: `docs/testing/v5.0.0/user/D12-reflect.md:235` pins the old model and the plan does not update it [R1-2].

## Blocking findings

<!-- Source: V3 R3-1 (base) -->
- **M-1 [R3-1] Task 2 breaks the Task 1 `claude-gw-tier` test and nothing catches it.**
  - Claim: Task 1's test allows the text `claude-gw-tier` under `src/superclaude/cli` only in listed paths and `cli/` is not listed. Task 2 tells the implementer to write a comment in `src/superclaude/cli/reflect/commands.py` saying the alias "resolves to claude-gw-tier1a". Acceptance criteria of Tasks 2-6 each run one named test; no task runs the whole `tests/skills/test_model_alias_policy.py` at the end. Today the 9 files containing the text are all allow-listed.
  - Evidence: plan:30 allow-list (three agents, `sc-issue-protocol/`, `commands/issue.md`, `ccsession-tag/`); plan:33 scan covers `cli`; plan:52 (Task 2 comment); plan:56, 66, 76, 86, 98 (one named test per task).
  - Fix: write the Task 2 comment without the literal id (point to docs/reference/model-aliases.md); add a final acceptance criterion (Task 9 or a new last task) that the whole policy test file passes, saved to `./artifacts/final-policy.log`.

<!-- Source: V3 R3-2 (base) -->
- **M-2 [R3-2] The launcher follow-up test is never shown to fail.**
  - Claim: the spec requires "a test that fails before the edit". Task 9 delivers it as a code block in `.dev/issues/384/launcher-followup.md` and only greps helper names. The harness cannot see the three variables: the fake claude records only `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `ANTHROPIC_CUSTOM_MODEL_OPTION`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, plus argv and settings, so a test that reads those variables from the captured dict would fail with a KeyError rather than because the exports are missing (a prediction; no test code exists yet, and plan:125 already tells the implementer to state the harness addition).
  - Evidence: source.md:5; plan:125, 129 (Task 9); `tests/unit/test_ccsession_tiers.py:332-341` (fake claude).
  - Fix: Task 9 states the exact `json.dump` lines to add, copies the harness plus the test into a scratch file under `./artifacts/`, runs it with `uv run pytest`, and saves a log showing an assertion failure on the three values (not a KeyError).

<!-- Source: V2 R2-1 (refactor-plan change 1; severity blocking as in V2) -->
- **M-3 [R2-1] Task 3's acceptance criterion contradicts Task 3's mandated replacement text.**
  - Claim: AC-1 requires `grep -n "models opus,sonnet" src/superclaude/skills/sc-issue-protocol/refs/chains.md` to return nothing, but the mandated line-21 bullet says "the brainstorm rows use the default models opus,sonnet,haiku; ..." and "models opus,sonnet" is a literal substring of "default models opus,sonnet,haiku". An executor who writes the mandated bullet fails the grep; one who satisfies the grep must deviate from the mandated wording.
  - Evidence: plan:65 (AC-1 grep); plan:62 (mandated bullet); current file `chains.md:11-13,21`.
  - Fix: change the AC grep to `grep -n -- "--models" .../chains.md` returning nothing (what the Task 1 policy test asserts, plan:36).

<!-- Source: V1 R1-2 (refactor-plan change 2; V1 graded it minor, the plan classifies it blocking as a missing required deliverable, spec item (4)) -->
- **M-4 [R1-2] `docs/testing/v5.0.0/user/D12-reflect.md:235` pins the old model and the plan does not update it.**
  - Claim: D12 pins `--model claude-opus-4-8` at line 235 (line 243 cites `commands.py:31,359`; the reviewer's "line 228" was dropped: it names no model id); Task 2 changes the default; spec item (4) asks to update pinned strings; the plan does not update D12. No pytest test pins the string, so no test catches the omission.
  - Evidence: `docs/testing/v5.0.0/user/D12-reflect.md:235` (also 243); `src/superclaude/cli/reflect/runner.py:507-508` appends `--model {config.model}`.
  - Fix: add D12 line 235 to Task 2.

## Minor findings

<!-- Source: V1 R1-1 (refactor-plan change 3; kept minor, acceptance criterion added by the plan) -->
- **M-5 [R1-1] Task 5 turns on the implement primary ladder and nothing records it.** `/etc/aidev02/aienv.d/defaults.sh:48,37,69,67` export T3Model01=gpt-6.1-terra, T2Model02=glm-5.3, T1Model02=gpt-6.1-sol, T1Model01=claude-opus-5-5; `src/superclaude/skills/sc-implement-protocol/refs/retry.md:162` says the ladder is active when all four are set. Rung 1 is non-Claude (glm-5.3), rungs 0 and 2 are GPT. Fix: add a Task 5 acceptance criterion that records the activation in `./artifacts/t5-notes.md`, and add it to Task 6 "Known consequences".

<!-- Source: V3 R3-3 (base) merged with V1 R1-8 (refactor-plan change 4) -->
- **M-6 [R3-3, R1-8] The "non-tier launch does not set them" check depends on the runner's environment.** `_launch_env` copies `os.environ` (`env = os.environ.copy()` at `tests/unit/test_ccsession_tiers.py:359`); the autouse `_isolated` fixture does not clear `ANTHROPIC_DEFAULT_*` (`tests/unit/test_ccsession_tiers.py:101-120, 359`); this workspace exports all three ANTHROPIC_DEFAULT_* variables (`defaults.sh:92-94`), and Task 6 admits the workspace exports real ids today (plan:94). The fake claude at lines 330-341 captures none, so the "not set" assertion would fail or pass by accident. Fix: remove the three variables from `env` first, or assert they equal the inherited values; say so in the spec and state the capture addition.

<!-- Source: V3 R3-4 (base) -->
- **M-7 [R3-4] The frontmatter test read literally fails on today's tree.** 48 agent files, only 16 have a `model:` line (plan:32, 42; count corrected by the evidence validator: the reviewer's 17 was wrong). Fix: say "when present".

<!-- Source: V3 R3-5 (base) merged with V2 R2-3 and V1 R1-10 (refactor-plan change 4), plus the calibrator gap from reviewer-cards/reviewer-3-calibration.yaml:15 -->
- **M-8 [R3-5, R2-3, R1-10] Task 1's policy scans are narrower than spec item (1) and the plan does not say so.**
  - The dated-id scan covers only `src/superclaude/cli/**/*.py` while the spec says "agents, commands, skills and Python" (source.md:1, plan:34). Today nothing is missed: the only non-docstring hit is `commands.py:31`; `aienv.py:94-96`, `runner.py:300`, `monitor.py:283`, `swarm/models.py:1067` are docstrings, AST-skipped. `ccsession-tag/models.py:113,122` would need allow-listing under a wider scan.
  - The frontmatter check covers agents and skills but not `commands/*.md`.
  - Calibrator gap: source.md:1 asks to scan agents, commands and skills for full model ids used as selections; the plan scans Python constants (plan:34) and frontmatter (plan:32) only, never markdown body text such as `--model claude-opus-4-8`.
  - This is a guard-strength gap: no violations exist today.
  - Fix: scan all `src/superclaude/**/*.py` with ccsession-tag allow-listed and add `commands/*.md` frontmatter, or record why the scope is narrower.

<!-- Source: V3 R3-6 (base) merged with V1 R1-9 (refactor-plan change 4) -->
- **M-9 [R3-6, R1-9] Task 7 misdirects the developer-guide edit and leaves `tiers.md:40` stale.** The only frontmatter heading is "5.2 SKILL.md Frontmatter" (skills); the agent `model:` text is at line 411 under "4.1 Anatomy of an Agent File" and already says `model:` takes "a full model ID or picker ID (for example `claude-gw-tier3`)" (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:388, 411, 515`), so Task 7's note would sit beside text that promotes picker IDs. `src/superclaude/skills/sc-issue-protocol/refs/tiers.md:40` still says "a fallback to `haiku` can land on a non-Claude model (`glm-5.3` here)"; the plan edits line 26 and adds a sentence after 40 but not line 40 (tiers.md:26, 40; plan:104, 107). Fix: name line 411 and reconcile it; reword tiers.md:40.

<!-- Source: V3 R3-7 (base) merged with V2 R2-2 and V1 R1-12 (refactor-plan change 4); provenance doubt resolved per refactor-plan "Changes NOT Being Made" (R3-7 / R1-11) -->
- **M-10 [R3-7, R2-2, R1-12] Task 4 misses `src/superclaude/skills/sc-cleanup-audit-protocol/templates/final-report.md:77` ("Pass 1 ... Haiku agents").** Task 4's "search and fix any other text that says audit-scanner runs on Haiku" sweep has no acceptance criterion; its closing search covers the line, but the cleanup-audit test checks only SKILL.md and cleanup-audit.md. `src/superclaude/cli/cli_portify/steps/discover_components.py:60,121` has a comment `(Haiku)` and a parse alternative; it is parser machinery, and the task exempts only the test fixtures. Fix: name final-report.md:77 and extend the test; state the cli_portify comment/regex stays (plan:72 vs :75). The commit provenance claim (70ef6486) that R3-7 marked unverifiable holds for `audit-scanner.md` (the orchestrator verified with `git log -S` that 70ef6486 touched audit-scanner.md).

<!-- Source: V3 R3-8 (Task 8 scope part, base) kept as a minor note per refactor-plan C-008; V1 R1-6 kept as a location hint only per refactor-plan X-002 / C-012 -->
- **M-11 [R3-8] Task 8 is not requested by the spec.** Characterization tests are not requested by spec items (1)-(4); Task 8 is cheap and guards the follow-up, so this is a note, not a defect. It is accurate otherwise (`tests/sprint/test_aienv.py:3-4` env seam; `tests/swarm/test_coder_tier_env_2026_10.py:113-124`; traces: `_load_aliases` returns ids, `suggest_alternate_model("claude-opus-5-5")` None at aienv.py:111-128, count 3 at runner.py:306-310). Fix: keep Task 8 only with owner agreement. Note: plan line 116 says "search tests/ for count_model_aliases" and names no path, so R1-6 ("Task 8 points at the wrong module") is not a defect; the only test calling `count_model_aliases` is `tests/swarm/test_coder_tier_env_2026_10.py:18,115-124`, a useful hint for the implementer.

<!-- Source: V1 R1-5 merged with V3 R3-8 (Task 6 wording part) (refactor-plan change 4) -->
- **M-12 [R1-5, R3-8] Task 6 states the sprint suggester limitation too broadly.** Task 6's "return nothing for tier-valued slots" is too broad: `suggest_alternate_model("opus", env)` returns "sonnet" (aienv.py:115-118, 149-152); `suggest_alternate_model("claude-opus-5-5")` returns None only when the three variables hold tier ids (`src/superclaude/cli/sprint/aienv.py:111-128`, the `return None` is at 127-128; with the variables unset the family fallback at 119-126 matches and the function returns "sonnet"). Corrected by the evidence validator. Task 8's assertion is right, the prose is not. Fix: reword.

<!-- Source: V1 R1-3 (refactor-plan change 4; kept minor per refactor-plan C-013) -->
- **M-13 [R1-3] Task 6's `unrecognized_model` sentence is not supported by the repo.** Task 6 claims Claude Code logs an `unrecognized_model` notice for tier-valued variables; the spec (`source.md:6`) records only that requests ran on the tier ids; grep of `.dev/issues/384` finds no "notice"/"unrecognized". The notice is real (observed in the orchestrator's throwaway-HOME run), but that run is not recorded in the repo. Fix: drop the sentence or cite the throwaway-HOME log.

<!-- Source: V1 R1-4 (refactor-plan change 4) -->
- **M-14 [R1-4] The alias-to-tier mapping is stated as current fact.** Task 2's comment, Task 3's chains bullet and Task 7's brainstorm row state the mapping as current fact; it is true only after the launcher change (`defaults.sh:92-94` set haiku=T2Model02 glm-5.3, opus=T1aModel01, sonnet=T1aModel02). Fix: use "once the launcher sets it" wording everywhere.

<!-- Source: V2 R2-4 (refactor-plan change 4) -->
- **M-15 [R2-4] Spec item (2) "user-guide ... pages that describe model selection" only partly lands.** Task 7 extends `docs/user-guide/brainstorm.md` (line 52) and the developer guide; `docs/user-guide/commands.md:849,859` also describes the brainstorm model-selection surface (`[--models opus,sonnet,haiku]`) and no task covers it. Fix: add it to Task 7 or record that brainstorm.md is canonical (plan:104).

<!-- Source: V2 R2-5 (refactor-plan change 4) -->
- **M-16 [R2-5] Task 6's "markdown contains no secrets or tokens" (plan:98) has no verification procedure.** Fix: name a grep or drop it.

<!-- Source: V3 R3-9 item 1 (refactor-plan change 5, split) -->
- **M-17 [R3-9] Forward link.** Tasks 2 and 3 link to a page Task 6 creates later.

<!-- Source: V3 R3-9 item 2 (refactor-plan change 5, split) -->
- **M-18 [R3-9] Unneeded dependency.** Task 9 is marked "Depends on: Task 6" but does not use its output (plan:123).

<!-- Source: V3 R3-9 item 3 (refactor-plan change 5, split) -->
- **M-19 [R3-9] Duplicated sentence.** Task 5's new sentence repeats retry.md:162.

<!-- Source: V3 R3-9 item 4 (refactor-plan change 5, split) -->
- **M-20 [R3-9] Test overlap.** The chains rule is tested twice (plan:36 and Task 3).

<!-- Source: V3 R3-9 item 5 (refactor-plan change 5, split) -->
- **M-21 [R3-9] Dead allow-list entry.** The allow-list entry `commands/issue.md` matches nothing today.

<!-- Source: V3 R3-9 item 6 (refactor-plan change 5, split) -->
- **M-22 [R3-9] Task 9 anchor correction.** Task 9 says the anchor "exports PROFILE_MODEL" but that is a shell variable: the tier-mode block is ccsession:776-785 and the custom-option exports at 1099-1103; the launcher also checks `CCSESSION_EXT_PROFILE != 1` (ccsession:777), which the stated tier-mode rule omits.

<!-- Source: V1 Coverage audit note (diff point U-001; refactor-plan change 6) -->
- **M-23 [V1 coverage note] The plan uses the legacy T1Model slots without saying so.** The plan uses T1Model01/T1Model02, which `defaults.sh:63-65` calls legacy slots kept for swarm and reflect (the newer ccsession does not use them). Fix: state this in retry.md.

<!-- Source: V3 Coverage audit (base) merged with V2 Coverage audit; V1 "None found" superseded by M-4, M-8 and M-23 -->
## Coverage audit

- "scan ... Python" (source.md:1): partly covered (M-8). The plan also never scans markdown body text for full model ids (M-8, calibrator gap).
- "a test that fails before the edit" (source.md:5): not verified (M-2).
- "and templates" (source.md:1): no `--models` in sc-issue-protocol templates, so nothing to change; the plan never says so.
- Spec item (2) user-guide pages: `docs/user-guide/commands.md:849,859` uncovered (M-15).
- Spec item (4) pinned strings: `D12-reflect.md:235` not updated (M-4).
- INF-010 and INF-011 are mapped to Task 1 in the brief's coverage slice but are delivered by Task 5 mirror copies and the test edits in Tasks 3 and 5; INF-011's match score is none 0.5. INF-011 is a matcher false negative (covered by Tasks 3 and 5).
- V2 checked every requirement-bearing span of source.md lines 1, 5-9; absent-from-matrix spans: none beyond R2-4 (M-15) and R2-3 (M-8).

<!-- Source: V3 "Verified correct" (base) merged with V1 "Verified without defect" and V2 Coverage audit verifications -->
## Verified correct

- `commands.py:31` and `359`; `chains.md:11-13` and `21`; `test_issue_protocol.py:268-282`; `sc-issue-command.md:237` and `442`. (V3, V1, V2)
- cleanup-audit SKILL.md:68, 74, 95, 99, 114 and cleanup-audit.md:43, 53 (Haiku lines). (V3, V2)
- `retry.md:162-172` (names at lines 162, 164, 168, 169, 172); `ledger.md:200`; `test_workflow_archive.py:774-777, 786` (`RUNGS`); `test_task_workspace_lifecycle.py:597`. (V3, V1, V2)
- `archive_workspace.py:57` regex accepts `[A-Za-z0-9_]+`. (V1, V2)
- `test_implement_adviser_family.py` exists. (V3)
- Mirrors: plugin mirrors of retry.md and ledger.md exist with line counts equal to their src copies (500 and 251 lines; the reviewer's 404 and 175 were dropped by the evidence validator); no mirror for chains.md, tiers.md, cleanup-audit.md, cleanup-audit SKILL.md; Task 5 copies both. (V3, V1, V2)
- `tier1a`, `tier1b`, `tier2` keys at ccsession-models.json:78, 85, 93. (V3, V1)
- `tier_mode` in models.py:469-479 matches Task 9's rule (see M-22 for the omitted `CCSESSION_EXT_PROFILE` check); Task 9 anchors `ccsession:1100-1102`, `models.py:469-479`. (V3, V2)
- MODEL-TIERS.md:38-39; brainstorm.md:52; `split_frontmatter` at test_issue_worker_agents.py:51-59. (V3)
- The allow-list is complete for the current tree: every `claude-gw-tier` hit under src/superclaude is in the three issue-worker agents, `sc-issue-protocol/**` or `ccsession-tag/**`. (V2)
- The six expected-red tests are red for the stated reasons and the other two pass today (Task 1's "fails exactly these tests" is accurate). (V2)
- No other test pins an edited string: no test imports `_DEFAULT_MODEL`, `test_codegraph_adoption.py` reads the cleanup-audit files but pins no Haiku text, no test pins tiers.md content. (V2)
- Task 8 claims: `aienv.py:73-77,111-128`, `runner.py:291-310`. (V2)
- `src/superclaude/agents/audit-scanner.md:5` pins `model: sonnet`; commit 70ef6486 touched audit-scanner.md (orchestrator `git log -S`). (V1)

<!-- Source: V3 Self-confidence (base) with V1 and V2 self-confidence notes -->
## Self-confidence

- Reviewer 3 (base): 0.85. Blocking claims are backed by lines read (allow-list and scan scope, Task 2 comment, harness recorded keys). Every SKILL.md frontmatter was not checked; the commit hash was not checked by this reviewer (since verified by the orchestrator, see M-10).
- Reviewer 1: 0.78. Could not run git, pytest or cmp (mirror byte-identity unverified by this reviewer).
- Reviewer 2: 0.86. Residual risk: docs-breadth gaps under `docs/` beyond the greps run; `test_workflow_archive.py` RUNGS context seen via targeted grep only.
- No merged confidence figure is computed here.
