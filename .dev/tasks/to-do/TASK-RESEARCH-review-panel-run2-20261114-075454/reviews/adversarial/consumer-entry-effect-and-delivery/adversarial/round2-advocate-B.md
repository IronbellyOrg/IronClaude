# Round 2 advocate for Variant B (slot C-05, consumer-entry-effect-and-delivery)

Tags: [CHECKED] = read or run in this session at the cited line; [INFERRED] = reasoned from checked lines, not run; [NOT CHECKED] = not read. Paths are repo-relative. No test was run. `.dev/tasks/` was excluded from every repo-wide search.

## Responses to criticisms

**A's reach argument (i): conceded as a fact, and it undercuts B-add's cost case.** [CHECKED] reflect's default `--depth` is `standard` (`src/superclaude/commands/reflect.md:98`); Wave 4 passes no depth (`sc-workflow-protocol/SKILL.md:89`); a rubric stop never reads the engine and with `legacy` a rubric escalation never calls the panel (`sc-reflect-protocol/SKILL.md:317,327-328`). So workflow reaches a panel only on rubric escalation. But the share is not measured, by me or by A. My free check (B E4 item 1): outside `.dev/tasks/` only four `depth-map.yaml` files are tracked. Three are sandbox fixtures under `.dev/e2e-reflect/`, one of them in an older schema I cannot map (`tl-1`: `depth: 1`, `tier: EXEMPT`). The fourth is the tavily brainstorm bundle, where every verdict is `SKIPPED` (no reflect ran). The 8 mappable phases are 4 quick, 2 standard, 2 deep (one deep is an override). That is n = 8, mostly synthetic, and it cannot size the gap. B-add pays a second review on every phase to close a gap nobody has sized. A's cheaper remedy is also pin-safe: appending a depth flag after `<id>.md` still satisfies the substring pin at `tests/commands/test_workflow_command.py:255-258`. I concede B-add is not justified before the reach measurement. I still say B's reach argument is correct; I withdraw "B-add" as a recommendation for this release.

**A's new cost claims (ii).** Both confirmed, both smaller than A implied.
- `artifacts` rule: [CHECKED] `refs/return-contract.md:52-53` lists only "each file reflect wrote in its `<report-dir>/nested/reflect-<n>/` run directory". [CHECKED] `tests/skills/test_worker_contract.py:528-537` sets workflow's nested list to `["reflect"]` and `_check_nested_text` (`:1477-1482`) only requires listed kinds to appear and forbids `nested/` only when the list is empty. So a `nested/panel-<n>/` line passes while the `artifacts` list silently omits it. That is an untested omission, which is worse than a broken pin. B-add would need the rule edited in both trees plus a new pin. Under A the panel writes inside reflect's own run directory [INFERRED], so the rule already covers it.
- Eval allow-list: [CHECKED] `scripts/eval_workflow_vs_task_builder.py:563-575` allows only the workflow and reflect skills; `:520` stages only those two skill directories. A new skill needs three allow entries and one staged name. If omitted the call is denied and ends `skipped`, which `test_workflow_vs_task_builder_companion.py:1808-1813` treats as advisory and not required. More important: `:67` denies `Bash`, `Agent`, `Task` and `mcp__*`, so that harness cannot run a reviewer fan-out under either route [INFERRED]. It is not a measurement harness for this slot.

**A on (iii), entry versus loop.** Conceded. B's own R1 concession puts a blocking loop in Stages 7-10, not at Wave 4 or Stage 10.5, and `tasklist/SKILL.md:1621-1623,1646` fences 10.5 as non-executing and non-blocking. A Stage 7 reviewer-feed swap changes Stage 7 text, not the call at `:1630`. So the entry question (call-site shape) and the loop question separate, and a later direct module needs no call-site change except a Wave 4 `plan-review`, which is the same reach question again. I withdraw "B's seam is needed for the loop".

**A on (iv), plugin.** Conceded, with a precise account of what a copy delivers. [CHECKED] the plugin workflow skill already points at `~/.claude/CODEGRAPH.md` (`:27`), `~/.claude/WORKER-CONTRACT.md` (`:53,:91`) and the installed workflow command; plugin `commands/reflect.md:142` points at `~/.claude/skills/sc-reflect-protocol/SKILL.md`. So the plugin is a thin front over an installed tree by design. [CHECKED] `${CLAUDE_PLUGIN_ROOT}` appears in `sc-recommend`, `help.md` and `spec-panel.md:266`; the spec-panel use is a fallback for a plain prompts file that needs no CLI. [CHECKED] `superclaude review|reflect` command text appears in the plugin only in that prompts file and `commands/reflect.md`. A panel skill's first step is a `superclaude review` call, so a copy delivers: (a) CLI absent, the hard gate returns `skipped`, same as today, nothing gained; (b) CLI present and `superclaude install` run, `~/.claude/skills` already has it, copy redundant; (c) CLI present, install not run, plugin installed, which is the only case with value, and it also needs a reviewer agent copy and `~/.claude/` core refs the plugin lacks. Whether (c) exists is [NOT CHECKED]. B's "cannot make it worse" holds; "delivers" is unshown.

**A on (v), do modules and `effect` need to exist before a replay.** No. [CHECKED] `src/superclaude/cli/review` has 0 case-insensitive matches for `tasklist` and `T<PP>`, no `effect` field (the 10 hits for `LENSES|effect|profile` are `card_convert.py`, `findings_v2.py`, `panel.py`), and `LENSES = ("spec", "reflect-pre", "reflect-post")` (`findings_v2.py:36`). So `tasklist-review`, `plan-review` and `effect` are design hypotheses with no code home. Arm D of the replay should be the path E2 already measured (spec-panel loop plus `superclaude review`), not a module. B's section 3 design becomes a post-replay deliverable.

**Round 1 weaknesses 1 and 2 (dormancy, UC-1 is one pass).** Dormancy is symmetric: B's skill does not exist either. B's one real asymmetry is independence from reflect's engine readiness (E13); it is weakened because a direct skill would re-implement an orchestrator that shares the shadow-run failure modes [INFERRED]. Conceded.

## Updated assessment of Variant A

A's position is stronger than my R1 allowed. It touches no pin that B-add touches only by addition, it carries no C-02/C-03 loop conditions, and its R2 merged resolution already includes B's three-part structure, B's replay columns, B's `effect`-as-module-data rule for later modules and the plugin-as-a-set decision. A's remaining weakness is real: the panel stays dormant for consumers until reflect's engine ships, and A has not sized what it misses. A has withdrawn the fence-test claim and its "zero pin changes" wording, and reduced "only route that keeps the contract intact" to a claim B-add can also meet.

## Concessions and what I still defend

**Conceded.** (1) B-add is not justified before a measured reach share. (2) Plugin delivery has no forcing element once call sites stay. (3) The `artifacts` rule gap and eval edits are real costs of B-add. (4) `tasklist-review`, `plan-review` and `effect` need not exist before a replay. (5) E7 and the 1.1 to 1.2 bump are withdrawn (R1). (6) C-02 INV-001/002/003 and C-03 INV-007 are B costs A avoids. (7) Entry and loop separate.

**Still defended.** (1) The reach gap is structurally real; whether it matters is the measurement, so the measurement must come before the engine switch, not after. (2) Generation-time blocking already exists in Stages 8-10 (`:1604-1615`), so a later Stage 7 reviewer feed adds a reviewer set and no new authority. (3) A later direct module with module-declared effect is the right precedent for PR review and rf-qa. (4) The replay must test the "reach" claim itself: arm R must be a real Wave 4 or Stage 10.5 call, not a hand-run reflect.

## Shared assumption responses

- **A-002: Neither (unchanged).** Unmeasured on both sides; advisory first.
- **A-003: Hybrid, agreeing with A.** `nested/reflect-<n>/` is covered by the `artifacts` rule; `nested/panel-<n>/` is not and nothing tests that. Headless fan-out is unrun for both and the companion eval cannot run it.
- **A-004: Hybrid, agreeing with A.** Fail-open for advisory calls; a blocking feed escalates on zero success.
- **A-005: Neither.** Shared inference.
- **A-006: B.** The parity pin covers `*.md` of one skill and one command; every added plugin file needs its own test.

## Final per-point verdicts

| Point | Winner | Hybrid content or reason | Agrees with A's R2? |
|---|---|---|---|
| S-001 | Neither | Section order is cosmetic. | Yes |
| S-002 | B | Three separable parts; adopt the structure. | Yes |
| S-003 | B | "Keeps / Endangers" per row is more candid. | Yes |
| C-001 | A | Single `/sc:reflect --mode pre` call this release; B-add is a pre-registered reopen if the reach measurement shows blocking GT items in phases that never reach the panel. | Yes |
| C-002 | Hybrid | Advisory at Wave 4 and Stage 10.5; any blocking use is a later Stage 7 reviewer-feed change after replay. | Yes |
| C-003 | A | No plugin copy now; decide plugin delivery as a set after the CLI-availability fact is known. | Yes |
| C-004 | Hybrid | B is right on the reach fact; remedy (call-site depth flag versus direct call) is chosen by the measurement. | Yes |
| C-005 | Hybrid | No new keys now; any later module adds keys only, `contract_version` stays "1.1", `reflect_*` unchanged. | Yes |
| C-006 | Hybrid | One reflect-side switch gated by replay; fence is an uncommitted-diff guard [INFERRED]. | Yes |
| C-007 | Hybrid | `reflect-pre` lens for Wave 4 and 10.5; Stage 7 dimensions only for a Stage 7 feed, which is net-new code. | Yes |
| C-008 | Hybrid | Blocking exists in Stages 8-10; changing its reviewers touches P2 pins and halt strings, so it is a separate later module. | Yes |
| C-009 | A | Wave 4 stays one advisory Skill call; `:107` stays true. | Yes |
| C-010 | A | A carries no ledger-loop conditions. | Yes |
| C-011 | Hybrid | A's replay and contract-compat test plus B's loop and cost columns; arm D is the E2 path; harness is not the companion eval. | Yes |
| C-012 | Hybrid | Module-declared effect for later direct consumers; none added here. | Yes |
| X-001 | Hybrid | Blocking exists (B); a call-site direct call adds no loop, a Stage 7 feed swap changes the block's evidence base (A). | Yes |
| X-002 | Neither | Both consistent with checked facts; open fact is CLI availability in a plugin install. | Yes |
| X-003 | Hybrid | B-add rewrites no pin but needs unpinned edits (`artifacts` rule, nested pin, eval allow-list, plugin parity); A's "zero" was a prediction. | Yes |
| X-004 | Hybrid | A adds none; a reviewer swap inside P2 adds no cycle number, a new loop would. | Yes |
| A-002 | Neither | Unmeasured on both sides. | Yes |
| A-003 | Hybrid | See above. | Yes |
| A-004 | Hybrid | Fail-open for advisory only. | Yes |
| A-005 | Neither | Shared inference. | Yes |
| A-006 | B | Each added plugin file needs its own parity test. | Yes |

I agree with A's R2 verdict on all 24 points. I checked each against the A column rather than copying it; where the evidence moved me (C-001, C-003, C-004) it moved toward A's stated hybrid or winner.

## Response to A's proposed merged resolution

I accept all 10 bullets in substance. Changes I would make:
- **Bullet 4 (reach).** Add the data source: share must come from reflect contracts (`tier_reached`, effective engine) of real Wave 4 and Stage 10.5 calls. The 80 `.dev/reflect/pre-*` runs I counted (62 tier 2, 16 tier 1, 2 null or empty) cannot size it, because I cannot tell which were consumer calls [INFERRED]. State a numeric reopen threshold before the first run.
- **Bullet 5 (door open).** Say that a Wave 4 `plan-review` is a call-site change and edits both workflow trees (parity pin `:93-103`), unlike a Stage 7 feed.
- **Bullet 6 (plugin).** Add the three-case delivery table above and that the CLI-present, install-not-run case is the only one with value and is unverified.
- **Bullet 7 (fence).** Reword to "uncommitted-diff guard, [INFERRED] until run on a clean tree". Neither of us ran it.
- **Bullet 8 (measurement).** Add that arm D is the existing E2 path, so no `tasklist-review` module or `effect` field is a precondition.
- **Bullet 9 (pins).** Add the unpinned edits to the list (`artifacts` rule, nested pin, eval allow-list).

## New evidence and code checks

[CHECKED] `refs/return-contract.md:16-21,52-53`; `tests/skills/test_worker_contract.py:528-537,1477-1482`; `scripts/eval_workflow_vs_task_builder.py:66-67,90,520,563-575`; `tests/cli/eval/test_workflow_vs_task_builder_companion.py:1808-1813,1825-1837`; `tests/commands/test_workflow_command.py:243-261`; `src/superclaude/commands/reflect.md:98,142` (src) and `plugins/superclaude/commands/reflect.md:142`; `sc-reflect-protocol/SKILL.md:313-336`; `sc-tasklist-protocol/SKILL.md:1619-1686`; `sc-workflow-protocol/SKILL.md:83-107`; plugin workflow skill `~/.claude/` pointers (`:27,:53,:91`); `${CLAUDE_PLUGIN_ROOT}` hits (`spec-panel.md:266`, `sc-recommend`, `help.md`); `superclaude (review|reflect)` in plugin files (2 files); `cli/review` grep for `tasklist`, `T<PP>`, `effect` and `LENSES` (`findings_v2.py:36`); four tracked `depth-map.yaml` files and their phase bands; `.dev/reflect/pre-*` `tier_reached` counts.
[INFERRED] fence tests pass on a committed branch; a `nested/panel-<n>/` directory falls outside the `artifacts` rule; the eval harness cannot run reviewer fan-out; a direct skill re-implements an orchestrator.
[NOT CHECKED] CLI availability in a plugin-only install; `verify-sync` coverage of `plugins/`; the C-01 to C-03 result files (relied on both papers); `research/` files; any test run.
