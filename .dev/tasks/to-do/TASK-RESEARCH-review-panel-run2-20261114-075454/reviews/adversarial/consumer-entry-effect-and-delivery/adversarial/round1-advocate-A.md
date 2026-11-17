# Round 1 advocate for Variant A (slot C-05)

Tags: [CHECKED] = read in this session at the cited line; [INFERRED] = reasoned from checked lines, not run; [NOT CHECKED] = not read here. All paths are repo-relative.

## Position summary

Keep `/sc:reflect --mode pre` as the single review call that workflow and tasklist make, and let the panel arrive as a Tier-2 engine inside reflect. That keeps every pinned consumer surface valid, adds no second verdict authority and no unmeasured generation-time blocking. Variant B's three parts (direct entry, blocking revise loop, plugin copy) each rest on the premise that nothing measured says the direct path is better. B itself concedes this in section 9, and its safe starting form (B-add, advisory) costs two reviews per phase.

## Steelman of Variant B

B's best case is that the entry decision is separable from the effect decision, and that reflect is a poor home for a tasklist review. First, the v2 kernel has no tasklist lens (`LENSES = ("spec", "reflect-pre", "reflect-post")`, B E7, not re-read by me). Reflect asks "does this tasklist cover the spec", not "do the Stage 7 dimensions hold". Second, A's route reaches the panel only after reflect's depth, pin and rubric decisions. Rule D1 means quick-depth, `--tier 1` and rubric-stopped runs never call it. Third, the one working "review, revise, re-review" shape in the repo already exists at generation time (Stages 8-10), so B only changes who feeds it. Fourth, `effect` as module data makes a wrong setting a one-field change. Fifth, B is honest: it names B-add advisory as its own safe form and lists its weakest link (the human-only exit for rejected rows). B is also right that A's "dormant until reflect's default changes" is the current state of affairs. B's measurement (two-arm replay with loop columns and a cost column) is better specified than A's.

## Strengths claimed

1. One call shape, all pins stay valid. [CHECKED] `tests/commands/test_workflow_command.py:251-261` pins the Wave 4 order, the exact string `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` and both `reflect_*` keys. `tests/cli/eval/test_workflow_vs_task_builder_companion.py:574-599` pins both keys present, `skipped` only with a null path, and `"bogus"` rejected. A touches none of these.
2. The advisory/blocking split is already how the products are built. [CHECKED] workflow `sc-workflow-protocol/SKILL.md:93` ("never change the workflow `status`... still proceed to Wave 5") and `:107` (Will Not: "new agents, Task fan-out; modify the plan from reflect findings"). [CHECKED] tasklist `sc-tasklist-protocol/SKILL.md:1640` ("the bundle **still ships**") and `:1646` ("ships regardless of verdict").
3. Panel results inherit a map that already exists. [CHECKED] `cli/reflect/runner.py:573-580` runs `derive_verdict` after both the swarm and the T1 path. A panel behind reflect is judged by the same function, with no second verdict authority. This is the condition C-03 sets for reflect.
4. No new nested directory kind. [CHECKED] the worker contract at `refs/return-contract.md:52` lists "each file reflect wrote in its `<report-dir>/nested/reflect-<n>/` run directory". A shadow or panel run writes under reflect's own `<output>/panel/` (reflect `SKILL.md:311`), so the `artifacts` rule is unchanged. B's `nested/panel-<n>/` needs that rule, `test_workflow_command.py:243-248` coverage and the worker contract extended.
5. A single choke point. [CHECKED by lead's grep result in A section 3 item 1, partly] no workflow or tasklist file mentions `--t2-engine`; reflect rejects `panel` at `:87`.
6. Low-complexity phases are not the high-risk phases. [CHECKED, new evidence] tasklist `:1658-1686`: any phase with `n_cpo >= 1` or `n_strict >= 2` is floored at `--depth deep --tier 2`. One STRICT task plus any regular task already scores 4 (3 + `ceil(n_tasks/5)` >= 1), which is `standard`. So a score of 0-3 can only be a phase with no STRICT task, no critical-path override and at most one High-risk task. D1's coverage gap hits the phases the generator itself rates lowest risk.

## Weaknesses identified in Variant B

1. B's "entry" argument needs an engine that does not exist yet and a measurement it has not run. B section 9: "Nothing here shows the direct entry gives better outcomes." B E11 supplies the opposite evidence: 0 of 8 real blocking in every arm and wrong blockers 0, 1, 3. B asks to build a blocking loop on that.
2. B-add costs two reviews per phase and a second report beside the first. B concedes the cost column is unmeasured (section 8, second objection). B-replace degrades `reflect_status` readers to `skipped` (B section 3), which breaks the troubleshoot, auggie-review and reflect hand-off readers that A lists as four consumers.
3. The plugin copy does not buy what it claims. [CHECKED] `plugins/superclaude/skills/` has four skills (`confidence-check`, `sc-implement-protocol`, `sc-recommend`, `sc-workflow-protocol`); `plugins/superclaude/commands/` has `reflect.md` and `workflow.md`, no `tasklist.md`; `plugins/superclaude/agents/` has no `reflect-reviewer` or `evidence-validator`. [CHECKED] the plugin's `reflect.md:142` still says the protocol is "at `~/.claude/skills/sc-reflect-protocol/SKILL.md`". So the plugin is already a thin front over an installed tree. A plugin copy of a delegate skill that needs the `superclaude` CLI, the reviewer agent and rules/briefs is a half-delivery unless reflect ships too.
4. The parity pin is narrower than B assumes. [CHECKED] `test_workflow_command.py:93-103` compares `rglob("*.md")` only. A delegate skill that carries any script or non-Markdown file is not covered by a copy of this test shape. B's own E9 notes the spec-panel plugin copy is already stale (25-line diff, not re-read by me).
5. B's pin-change claim is overstated. B section 6 says the `:243-248` pin "needs a panel line added in both forms". [CHECKED] that test is `any(... "nested/reflect-" in ln and "--unattended" in ln ...)`; a new panel line cannot break it. The real extra cost is new tests plus double-tree edits of the workflow skill, not rewrites.
6. B moves reviewer authority onto Stages 8-10. That stage's text and pins are `test_tasklist_cli.py:568-580` (disjointness predicate, "including any P2 bounded loop-back iterations", "BEFORE Stage 10.5") [CHECKED]. Replacing the reviewer side reopens the fence and the OQ-24 cap question (B INV-J "Endangers").
7. B's headless story is unproven. Workflow's Will Not at `:107` forbids Task fan-out; B resolves it with a delegate-only Skill call, which is the same shape A already uses via reflect. B gains nothing on that axis.

## Concessions

1. D1 is a real reachability limit. [CHECKED] reflect `:317` and table `:325-327`: quick, `--tier 1`, `--no-escalate` and rubric-stopped standard runs never call the panel under any engine. My new evidence (strength 6) narrows it but does not remove it.
2. T5 is not behind `--t2-engine`. [CHECKED] `runner.py:538-545` branches on depth, not on the engine flag, and calls `run_tier2_ensemble(config)` in production. "Blocking at the execution gate" is as strong as the engine C-04 picks.
3. A's item 8 overstates the fence cost. [CHECKED] `test_shadow_skill_contract.py:52-75` diffs `git diff HEAD -U0`, so it constrains only an uncommitted working tree. [INFERRED] on a committed branch it passes trivially. The `:42-49` contract-block pin and the `:98` string rule remain real. So the fence is lighter than A said, and also a weaker guard than A implied.
4. The v2 kernel has no tasklist lens (B E7). Reflect reviews tasklist-versus-spec coverage, not the five Stage 7 dimensions.
5. A's "zero pin changes outside the fence test" is a prediction, not a run.

## Shared assumption responses

- A-002 (the panel reviews tasklist and plan documents well enough to be consumed): QUALIFY. It holds only after a replay through the consumer entry, which neither paper has run. A's route tests it before activation (section 6.1); B builds a blocking loop on it first.
- A-003 (nested fan-out completes headless and respects the closed enum): QUALIFY. The `nested/reflect-<n>/` convention is checked (`SKILL.md:91`, `return-contract.md:52`), but headless panel behaviour is unrun. A reuses the existing directory kind; B adds a new kind and extends the artifacts rule.
- A-004 (panel failure or short panel maps to a fail-open status): QUALIFY. True for the two advisory call sites (`:93`, `:1640`). Mapping a short panel to `failed` with a null path discards a partial panel's findings, and at T5 the same map is fail-closed by design (`runner.py:573-580`).
- A-005 (plugin-only install already skips Wave 4 review): ACCEPT, as an inference. [CHECKED] `plugins/.../sc-workflow-protocol/SKILL.md:22,89` names `sc:reflect-protocol`; no such skill is in the plugin. [INFERRED] `:93` turns that into `skipped|failed`; not executed.
- A-006 (source/plugin pins keep their meaning; `verify-sync` is the only guard): QUALIFY. [CHECKED] the byte-parity test covers `*.md` of one skill and one command only; whether `verify-sync` covers `plugins/` is [NOT CHECKED]. The guard is narrower than "only mechanical guard" suggests.

## Per-point positions

| Point | Winner | One sentence |
|---|---|---|
| S-001 | Neither | Section order is cosmetic. |
| S-002 | Hybrid | B's separable three-part structure is a genuine strength; A should state its three parts separately. |
| S-003 | B | B's per-row "Keeps / Endangers" verdicts are more candid than A's all-"Preserved" table. |
| C-001 | A | One call shape keeps every checked pin and reader valid, and B-add doubles review cost. |
| C-002 | A | Advisory at generation is the existing product choice; B itself starts advisory. |
| C-003 | A | The plugin copy cannot work without reflect, agents and CLI; decide it separately. |
| C-004 | Hybrid | D1 is real, but score 0-3 phases carry no STRICT or CPO task; let measurement 6.2 decide the depth table. |
| C-005 | A | No new keys, no closed-enum change, no reader degradation. |
| C-006 | A | One controlled switch beats a second entry; the fence is lighter than A claimed. |
| C-007 | Hybrid | B is right that no tasklist lens exists; A does not claim to replace Stage 7. |
| C-008 | A | Replacing the Stages 8-10 reviewer side reopens its pins and the cap question. |
| C-009 | A | Wave 4 stays one advisory Skill call; the Will Not line stays true. |
| C-010 | A | A carries no ledger-loop conditions; B carries C-02 INV-001/002/003 and C-03 INV-007. |
| C-011 | Hybrid | Merge A's replay (6.1) with B's loop and cost columns. |
| C-012 | A | No copyable direct-call precedent forces PR review and rf-qa to define their own shapes. |
| X-001 | Hybrid | B is right that generation-time blocking already exists; A is right that B changes its reviewer feed and fences. |
| X-002 | A | A plugin delegate skill alone is incomplete; the plugin's own `reflect.md` points at `~/.claude/skills/`. |
| X-003 | A | B-add also keeps all pins but adds new tests and double-tree edits; A edits the reflect skill only. |
| X-004 | A | A adds no new review severity text; B's revise loop must reconcile "2 TOTAL passes" with S3. |
| A-002 | Neither | Unmeasured on both sides; see above. |
| A-003 | A | A reuses `nested/reflect-<n>/`. |
| A-004 | Hybrid | Fail-open holds for advisory calls only. |
| A-005 | Neither | Shared inference; both rely on it. |
| A-006 | Neither | The guard is narrower than both assume. |

## Code checks run

- (a) [CHECKED] workflow `SKILL.md`: Wave 4 starts `:85`; call `:89`; unattended `:91`; advisory rule `:93`; Will Not `:107`. Tasklist Stage 10.5 at `:1619`; command `:1630-1636`; verdict handling `:1640`; gate `:1646`; depth table `:1677-1681`. Both variants' citations are accurate.
- (b) [CHECKED] `test_workflow_command.py:93-103` (byte parity, `rglob("*.md")`, command file); `:243-248` (`any` of one line); `:251-261` (order, exact string, keys, command text). Companion test `:574-599` as A and B state. `test_tasklist_cli.py:568-580` as A states.
- (c) [CHECKED] plugin has the four skills, `reflect.md` and `workflow.md` commands, no `tasklist.md`, and no `reflect-reviewer`, `evidence-validator` or `rf-*` agent. Both variants are right.
- (d) [CHECKED] reflect `SKILL.md:317` (D1) and `:87` (`panel` rejected with "ships in Stage 3"). Table `:325-330` extends D1 to rubric-stopped standard runs.
- (e) [CHECKED, not run] `test_shadow_skill_contract.py:42-49, 52-75, 78-98` as described in concession 3. `runner.py:538-545, 573-580` also read.
- [NOT CHECKED] default `--depth` that workflow Wave 4 gets from "defaults for every other flag"; B's E7 line `findings_v2.py:36`; all `research/` and prior-slot files (I relied on the two papers' account of C-01 to C-03).
