# Round 2.5 invariant probe, fault-finder raw (slot C-05, consumer-entry-effect-and-delivery)

Role: independent fault-finder. Not an advocate for A or B. Read-only except this file. No test was run; every [CHECKED] below is a read of the cited line in this session. [INFERRED] = reasoned from checked lines. Paths are repo-relative to `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` (HEAD 50d4d2b9d). `.dev/tasks/` was excluded from every repo search except this task folder.

Probed text: the emerging consensus (A's 10-bullet merged resolution in `round2-advocate-A.md:69-79`, accepted by B with 6 amendments in `round2-advocate-B.md:70-78`).

Summary: 15 findings. HIGH UNADDRESSED: 7 (INV-001, INV-002, INV-003, INV-005, INV-007, INV-013, INV-014).

---

ID: INV-001
CATEGORY: guard_conditions
ASSUMPTION: "Effect advisory at Wave 4 / Stage 10.5; blocking stays at T5 and Stages 6-10" (consensus bullet 3), and, from test 7 of the brief, that no generation-time halt is reachable from Stage 10.5 or Wave 4.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- Wave 4 is advisory with no halt path: `src/superclaude/skills/sc-workflow-protocol/SKILL.md:93` ("never change the workflow status ... still proceed to Wave 5"); the call passes no `--remediate` (`:89`). [CHECKED] So for Wave 4 the consensus text is right, also under `--unattended` (`:91`).
- Stage 10.5 is NOT advisory-only. `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1640`: "any `needs_human_decision` item in that remediation HALTs". `:1642`: under `--unattended` this "resolves as blocked: the item goes in `blocked_question` and the run ends as `blocked`". `:1646`: "The bundle ships regardless of verdict (advisory-blocking)". [CHECKED] task-builder has the same label for its PRE gate (`src/superclaude/skills/task-builder/SKILL.md:1664`, "advisory-blocking").
- `needs_human_decision` is true when `grounding-gaps.yaml` is non-empty (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:858`). The engine decides what reaches the evidence gate (dropped citations, uncalibrated findings), so an engine switch can change how often a Stage 10.5 generation run halts or ends `blocked`. [INFERRED: the panel's effect on the gap count is unmeasured]
- Round 2 A cites `tasklist :1640` as an "advisory call" (`round2-advocate-A.md:37`, A-004 response). The same line carries the halt sentence. Neither R2 file mentions the halt or the `blocked` terminal state.
ANSWER TO BRIEF ITEM 7: yes, a generation-time halt is reachable from Stage 10.5 today (interactive halt, unattended `blocked`). It is not reachable from Wave 4.

---

ID: INV-002
CATEGORY: interaction_effects
ASSUMPTION: Stage 10.5 is a read-only review whose only output is a verdict; the engine switch changes review quality, nothing else.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- Stage 10.5 always passes `--remediate` (`sc-tasklist-protocol/SKILL.md:1630`). Under `--unattended`, "the headless rule above applies whatever the terminal state (AUTO-FIXABLE registers only, no yes/no prompt)" (`sc-reflect-protocol/SKILL.md:369`); headless `--remediate` auto-accepts and "authors the corrective artifact" (`:371`). [CHECKED]
- On the plan route reflect calls `Skill sc:workflow-protocol` (`:383`), which creates a new package `.dev/tasks/to-do/<slug>/`, and that workflow runs its own Wave 4 `/sc:reflect --mode pre` (`:385`; workflow `SKILL.md:89`). So one Stage 10.5 phase call can nest: tasklist -> reflect (engine X, Tier 2) -> workflow -> reflect (engine X again on rubric escalation). Nested directories `nested/reflect-<n>/` then `nested/workflow-<n>/` (`:384`). [CHECKED]
- Consequences the consensus does not price: (a) the panel's finding set decides whether a corrective package is authored (AUTO-FIXABLE vs HUMAN-REQUIRED registers, `:371`); (b) a default flip multiplies panel runs per phase, N phases in parallel (`tasklist :1625`); (c) the reach statement "panel reached only on forced-deep phases and rubric escalations" undercounts panel runs once nested workflow Wave 4 calls are included.
- Neither advocate paper nor R2 file mentions `--remediate` at Stage 10.5 as a write path.

---

ID: INV-003
CATEGORY: interaction_effects
ASSUMPTION: The "depth-policy remedy before any second entry" (consensus bullet 4: "a call-site depth flag or the Stage 10.5 table") is a pure reach fix with no side effect.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- Remediation route follows the REQUESTED `--depth`, not the tier reached: `sc-reflect-protocol/SKILL.md:363` ("an auto-escalation to Tier 2 does not change it"); `--remediate --depth deep` -> MDTM route via task-builder; under `--unattended` the MDTM route "is skipped and recorded" (`:369`). Pinned by `tests/cli/reflect/test_remediation_route_table.py:26-39` (plan route for default depth, MDTM for deep, headless follows depth). [CHECKED]
- Stage 10.5 passes `--depth` per phase from the score table (`tasklist :1633, 1677-1681`). Widening the forced-deep set (the likely remedy: lower the score threshold or the override at `:1685`) moves those phases from the plan route to the MDTM route, and to "skipped and recorded" under unattended. A different artifact kind and a different terminal state, caused by a reach tweak.
- At Wave 4 the remedy forces `--depth deep` on every plan. Under the default engine `legacy` that already means forced Tier 2 with the legacy reviewer rotation for every workflow run, so the remedy changes cost and wall-clock today, before any panel exists (`sc-reflect-protocol/SKILL.md:329`, "`--depth deep` | forced T2"; D3 applies, `:319`).
- Documentation drift worth fixing in the same change: tasklist `:1640` says reflect "offers a Tier-3 `task-builder` remediation", while reflect routes the standard and quick depths to the workflow plan route (`reflect SKILL :366`).
- Neither R2 file connects depth to route.

---

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: A call-site depth flag at Wave 4 is "pin-safe" (R2-B `:7`: "appending a depth flag after `<id>.md` still satisfies the substring pin").
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE (answer to brief item 3):
- Substring pin `tests/commands/test_workflow_command.py:255-258` requires `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` as one contiguous string; a flag appended after `<id>.md` passes, a flag inserted before `--tasklist` fails. `:243-248` (`any(... "nested/reflect-" and "--unattended")`) is unaffected. [CHECKED]
- Parity pin `tests/commands/test_workflow_command.py:93-103` byte-compares every `*.md` of `src/.../sc-workflow-protocol` with `plugins/superclaude/skills/sc-workflow-protocol` and the command file. The plugin copy carries the identical Wave 4 text (`plugins/superclaude/skills/sc-workflow-protocol/SKILL.md:89`). A depth-flag edit in `src` alone fails the parity test; it must be made in both trees. Neither R2 file says this for the depth-flag remedy (B names both trees only for a later `plan-review`, `round2-advocate-B.md:75`). [CHECKED]
- The phrase "defaults for every other flag" (`workflow SKILL.md:89`) becomes untrue and must be reworded; no test pins that phrase (rg of `tests/` for it: no hit). [CHECKED]
- Return contract: unaffected. `reflect_status` and `reflect_report_path` are still recorded from reflect's contract (`return-contract.md:16`); `contract_version: "1.1"` pinned at `test_workflow_command.py:178` and read at `scripts/eval_workflow_vs_task_builder.py:1140` and `sc-implement-protocol/scripts/archive_workspace.py:~327` stays valid.

---

ID: INV-005
CATEGORY: collection_boundaries
ASSUMPTION: The reach share can be measured "from the existing shadow runs" (A's measurement 6.2, `variant-1-original.md:74`); B's amendment says to source it from reflect contracts of real Wave 4 and Stage 10.5 calls.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- `scripts/reflect_shadow_exit.py:209` globs `runs_root.glob("pre-*/panel/manifest.json")`; `:215` skips any manifest whose `t2_engine_effective` is not `shadow`; default `--runs-root` is `.dev/reflect` (`:392`). [CHECKED]
- Survivorship: a phase that never reaches the panel (D1, `sc-reflect-protocol/SKILL.md:317`: quick, `--tier 1`, rubric stop never reads the engine) writes no `panel/manifest.json`. The population the share must count is invisible to the only aggregator.
- Directory blindness: Stage 10.5 always passes `--output TASKLIST_ROOT/validation/reflect-pre/phase-<P>/` (`tasklist :1635`) or `nested/reflect-<n>/` under unattended (`:1638`); workflow unattended uses `nested/reflect-<n>/` (`workflow :91`). Neither matches `pre-*` directly under `.dev/reflect`. Only an interactive Wave 4 call, which takes the default `--output` `.dev/reflect/<mode>-<slug>-<ts>/` (`reflect SKILL :88`), is visible. So tasklist consumer calls, the larger consumer, are outside the aggregator whatever the engine.
- The state variable that would identify unreached runs exists (`t2_engine_requested`/`t2_engine_effective` are null "when the final tier is 1", `reflect SKILL :464-465`) but no script reads it for consumer outputs. B's "80 `.dev/reflect/pre-*` runs, 62 tier 2, 16 tier 1" (`round2-advocate-B.md:73`) cannot be turned into a consumer share (B says so: cannot tell which were consumer calls).
- Consequence: the pre-registered reopen condition of bullet 1 ("blocking GT items in phases that never reach the panel") has no instrument that can fire it.

---

ID: INV-006
CATEGORY: collection_boundaries
ASSUMPTION: "Measure the share" of phases/plans that reach the panel (bullet 4) has a well-defined denominator.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- Populations that produce no reflect run, and so no `tier_reached`: `n_tasks == 0` phases skipped entirely (`tasklist :1686`); `--no-reflect` and `--dry-run` skip Stage 10.5 (`:1644`); workflow `reflect_status: skipped|failed` with a null path (`workflow :93`); the plugin-only install where Wave 4 calls a skill the plugin does not ship (shared inference A-005, not run); `--budget-remaining` N < 65 downgrades rubric escalations to T1 and "never calls the panel" (`reflect SKILL :331-333`). [CHECKED]
- Whether these count in the denominator changes the reported reach (understated if skipped phases are counted as unreached, overstated if dropped). The consensus says "state plainly and measure the share" but fixes no rule. Budget downgrade is a second, independent reach limiter that neither R2 file lists.
- Boundary of the forced-deep rule: `n_cpo >= 1 OR n_strict >= 2` (`tasklist :1685`); a phase with exactly one STRICT task and no CPO scores >= 4 (3 + ceil(n_tasks/5)) and is `standard`, so it reaches the panel only on a rubric escalation. [CHECKED; arithmetic from `:1667-1673`]

---

ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: "A panel result reaches consumers only as reflect's `status`, `coverage_pct`, `tier_reached`" (consensus bullet 3).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- The consumer read surface is wider than three fields: workflow records `status` and `report_path` (`workflow :89`); tasklist reads the verdict, coverage, and `needs_human_decision` (`tasklist :1640-1642`), plus `reflect_pre_summary` counts (`:1640`); task-builder reads `status`, `coverage_pct`, `unmapped_requirements`, `run_id`, `tier_reached` (`task-builder/SKILL.md:1682`). [CHECKED]
- Two of the three named fields are fixed before the engine is read: reflect computes the T1 card, coverage map and rubric in Waves 1-2 and "only now `--t2-engine` is read, at the start of Wave 3" (`reflect SKILL :313`). `coverage_pct` is UC-1 coverage of the spec by the tasklist (`:738`); `tier_reached` is 2 under any Tier-2 engine. By construction neither can carry a panel benefit. Only `status` (and the report and gap fields) can. [CHECKED]
- The sentence is therefore both too narrow (omits `needs_human_decision`, `unmapped_requirements`, `run_id`, `report_path`) and partly vacuous (two of three fields cannot move).

---

ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: The default flip touches "two consumers" and "four readers of `reflect_status`" (A `diff-analysis.md` U-002; round2-advocate-A item 5).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- A flip of reflect's UC-1 default engine reaches every UC-1 caller, not only workflow and tasklist. A third direct caller: task-builder PRE gate, "Mandatory-run", `--mode pre --remediate`, with depth derived from its own TCS (`task-builder/SKILL.md:1664-1680`; also `:210`). `rg "--mode pre"` over `src/superclaude` outside the reflect skill: task-builder 5 hits, auggie-review command 4, troubleshoot command 3, workflow skill 3, tasklist skill 2 (grep run this session). [CHECKED]
- `reflect_status` readers by file: troubleshoot `SKILL.md`, `refs/remediation-handoff.md:34,112,119`, `refs/diagnosability-audit.md:252`; auggie-review `SKILL.md:348` and its `refs/remediation-handoff.md`; reflect `refs/remediation-handoff.md:81-84,209,303`; `commands/reflect.md:211`; code validator `scripts/eval_workflow_vs_task_builder.py:1166-1175`; `tests/troubleshoot/test_diagnostic_worker_contract.py:67`; companion tests `:574-599`. That is more than four kinds of reader, one of them a closed-enum code validator. [CHECKED]
- The 36-test verdict matrix is `tests/cli/reflect/test_verdict_mapping.py` (36 `def test_` counted). [CHECKED]

---

ID: INV-009
CATEGORY: state_variables
ASSUMPTION: A short, refused or failed panel cannot push `reflect_status` outside the closed enum `success | partial | failed | skipped` (brief item 5).
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE:
- Enum closure is real: `workflow refs/return-contract.md:16`; reader `scripts/eval_workflow_vs_task_builder.py:1166-1175` (`status in ("success","partial","failed","skipped")`, failed/skipped need a null report path); test `tests/cli/eval/test_workflow_vs_task_builder_companion.py:582-599` ("the enum is closed", `bogus` rejected). [CHECKED]
- Reflect's own status adds `dry-run` (`reflect SKILL :728`), which the workflow enum lacks, but Wave 4 never passes `--dry-run` (`workflow :89`), so no path found. Panel shortfall is handled inside the enum: D3 forces `status: partial` only when the effective engine is `panel` (`reflect SKILL :319`); D4 unsupported cells run legacy and record `panel_fallback_reason` (`:320`). [CHECKED]
- Both R2 files handle fail-open for advisory calls (A-004 responses). No violation found; residual risk is the unpinned map (see INV-011).

---

ID: INV-010
CATEGORY: state_variables
ASSUMPTION: "One reflect-side switch at reflect's default" is a single well-defined change; "what flips" is known.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The default is prose in three places, not code: `sc-reflect-protocol/SKILL.md:87` (`--t2-engine legacy | shadow`, default `legacy`, `panel` rejected with a literal message), `:311` ("With the default `--t2-engine legacy`"), and the telemetry enums `:464-465`, `:970-971`. `rg "t2-engine|t2_engine"` over `src` and `tests` finds no `cli/reflect` reader of the flag; the command table `src/superclaude/commands/reflect.md` has no `--t2-engine` row (`:98` is `--depth`). No environment-variable selector exists (rg over the skill directory: none). [CHECKED]
- Consequences: (a) the switch is a skill-text edit, so "no change to `cli/reflect`" (C-01 result item 12) holds trivially while the behaviour change is in prose that three standing test groups read (INV-012); (b) a real consumer call cannot select an engine except by editing its call string or by flipping the global default, so an arm "R as a real consumer call" (B's rule, `round2-advocate-B.md:29`) can only run `shadow` or `panel` after the flip or after a call-site edit that the consensus forbids this release; (c) `shadow` runs the panel in addition to the legacy rotation (`reflect SKILL :311`, `:338`), so flipping to `shadow` first doubles Tier-2 reviewer spend on every consumer escalation. The consensus names neither the staged option nor its cost.

---

ID: INV-011
CATEGORY: guard_conditions
ASSUMPTION: A "contract-compat test against the 36-test verdict matrix" (bullet 2) is enough to show the panel engine's contract is compatible; "a panel result maps onto status".
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- `derive_verdict` degrades a Tier-2 run on null convergence (`src/superclaude/cli/reflect/contract.py:299-300`), on convergence below 0.80 or non-finite (`:317-326`), on `merge_method == "single-reviewer-fallback"` (`:295-296`), on single vendor (`:287-288`). It reads adversarial fields only; no input is a panel manifest state. [CHECKED]
- The existing panel lint adds closed rules the matrix does not test: L1 version equals 1.8.0, L2 no top-level key outside the stable list plus `telemetry`, L3 `merge_method` in `{adversarial, single-reviewer-fallback}` (EV-2), L6 EV-1 needs `adversarial/merged-verdict.yaml` with `merge_method: adversarial` and enough reviewer cards, else a loud fallback row (`src/superclaude/cli/reflect/panel_lint.py:272, 288-298, 311-334, 360-365`; reflect `SKILL :837`). [CHECKED]
- So for a `panel` effective engine the consensus must say who writes `adversarial_convergence_score` and `merge_method` (the panel's cluster-and-union merge produces neither), whether the nested `sc:adversarial` call stays, and where panel-only state (refusal, short quorum) goes (only `telemetry:` is allowed). No R2 text answers this. Today, in every shadow run "the legacy builder writes the contract" (`scripts/reflect_shadow_exit.py:21-22`), so no map from panel states to `status` has ever been exercised. [CHECKED]

---

ID: INV-012
CATEGORY: guard_conditions
ASSUMPTION: "Fence tests are a working-tree guard (INFERRED, not run)" and "I withdraw 'the fence test must be changed'" (`round2-advocate-A.md:18`; bullet 7).
STATUS: ADDRESSED (partly wrong)
SEVERITY: MEDIUM
EVIDENCE (answer to brief item 1; read, not run):
- True for three tests, all in `tests/cli/reflect/test_shadow_skill_contract.py`: `:42-49` compares the working copy of the 9.1 block to `git show HEAD:<skill>` (a clean tree is trivially equal); `:52-75` runs `git diff HEAD -U0` and checks each hunk's section, passing on an empty diff; `:78-98` compares `git grep -c src/superclaude` at HEAD with the working tree. Each also `pytest.skip`s when git has no history (`:45-46, 54-55, 87-88`). On a committed branch with a clean tree they pass whatever the commit contained. [CHECKED]
- Not true of the other tests in the same file. They read the committed text and pin it: exactly three brief sections (`:146-165`); the shadow section must contain "authoritative and unchanged", `manifest advance`, `kept-ids.txt`, `judge_class_collision: unknown` (`:168-181`); the calibrator line appears exactly once (`text.count(line.group(1)) == 1`, `:183-196`); the shadow steps pin `reviewers[N].model`, `model_observed`, "valid on this first parse", "before any re-ask", `merged-verdict.yaml`, `adversarial/adversarial/` (`:221-238`); a manifest recipe runs as written (`:104-140`). A Stage 3 edit that restructures the shadow steps, adds panel steps next to them, or edits the calibrator line fails these on a clean tree. [CHECKED]
- During development the `git diff HEAD` test fails for any uncommitted edit outside sections 3.1, 4.3a, 5.4, 9.2 (`:65`), and the consensus (A R2 v(a)) says the "authoritative Wave 3/4 text" must change. So the fence blocks the author until commit, then stops blocking: a guard that is bypassed by committing first. The right wording for bullet 7 is "three diff-based tests are working-tree guards; the content pins in the same file are standing and the Stage 3 change must update them".
- Bullet 9 ("reflect-owned tests change at Stage 3") already covers the need to edit; what is unaddressed is that the withdrawal of "must be changed" understates it.

---

ID: INV-013
CATEGORY: sufficiency_challenge
ASSUMPTION: "The replay/measurement decides it" (bullets 2, 4, 8): there is a replay that can be run with ground truth, someone runs it, and arm R is a real consumer call.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE (answer to brief item 6):
- No ground-truth scorer exists. `scripts/reflect_shadow_exit.py` (`:1-35`) checks parity, MALFORMED rows, panel lint, a `derive_verdict` replay and EV-1 rates; `rg "ground|recall"` over it and `scripts/reflect_verdict_replay.py` returns nothing. [CHECKED]
- Ground truth is thin and biased: GT contains only defects that surfaced during implementation, so a novel true defect scores as a wrong blocker; real blocking was 0 of 8 in every pilot arm (`variant-2-original.md:106, 110`, E11, research 08 cited by B, UNVERIFIED here by me). With n = 8 and three arms at zero, a difference of one item is the whole signal.
- The harness named for measurement cannot run it: the companion eval pool denies Bash, Agent, Task and `mcp__*` (`scripts/eval_workflow_vs_task_builder.py:66-67`, per both advocates; `:563-575` allow-list per B); both R2 files say so. No replacement runner is assigned. "Held-out package" labelling has no owner.
- Arm R as a real consumer call needs an engine selector (INV-010). No environment variable or call-string option exists, so without a call-site edit or a global flip R is a hand-run of reflect with the call site's arguments, which is the very thing B said it must not be.
- No pre-registered numeric threshold exists; B asked for one (`round2-advocate-B.md:73`) and A did not answer.
- Net: the consensus resolves every disputed point to "replay decides", while the replay has no instrument, no labeller, no selector and tiny n. That moves the whole slot's decisions to an unscheduled study.

---

ID: INV-014
CATEGORY: sufficiency_challenge
ASSUMPTION: "The consensus resolution alone achieves its stated outcome: consumers get the panel's benefit without a second entry; no consumer pin changes."
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE (falsifying conditions, with source enumeration):
- F1 (benefit invisible). Consumers read `status`, `coverage_pct`, `tier_reached`, plus gap and report fields (INV-007). `coverage_pct` and `tier_reached` are fixed before the engine is read (`reflect SKILL :313`). The panel, as C-01/C-02/C-03 leave it, changes no verdict while shadow (INV-L, A `diff-analysis.md` U-004), and reflect "keeps `shortfall: visible`, `derive_verdict`, its 36 tests" (C-03 result, condition 3). So a faithful engine switch changes consumer-visible output only through `status` and the report body. If the panel is fixed to reflect's verdict authority, the consumer outcome is the legacy `status` with a different reviewer layer underneath. The benefit claim then rests on REPORT.md content no consumer reads (workflow only stores the path, `workflow :89`). No instrument in the consensus measures consumer-visible benefit.
- F2 (contract change hidden). To make the benefit visible the panel must change `status`, which needs a defined map (INV-011) and either keeps `adversarial_convergence_score` (then the Wave 4 debate remains the verdict authority) or sets it to null (then `derive_verdict` yields `null-convergence` at `contract.py:299-300` for T5-style readers). Either way the "no second verdict authority" claim of bullet 2 and the "consumers see the panel" claim cannot both hold. [INFERRED]
- F3 (pin edits). "No consumer-side test pin changes expected" (bullet 9) holds for the pins I enumerated on the consumer side: `test_workflow_command.py:178, 243-261`, companion `:574-599`, `archive_workspace.py:167-173` (`_kv` ignores extra keys). It fails for reflect-owned pins that consumers' suites share: `tests/cli/reflect/test_remediation_route_table.py:26-39` if depth policy changes the route (INV-003), `tests/cli/reflect/test_shadow_skill_contract.py:146-238` content pins (INV-012), and, for a later direct module, `tests/skills/test_worker_contract.py:1678-1689` (`EXPECTED_NESTING` closed dict: `workflow: ["reflect"]`, `tasklist: ["reflect","task"]`) plus the `UNATTENDED_EXPECT` nested lists read by `_check_nested_text` (`:1477-1482`). [CHECKED] Bullet 5 lists "nested-kind list extended by hand" but not that two test constants are edited.
- F4 (halts). If a Stage 10.5 run ends `blocked` or halts because the panel raised a gap (INV-001), consumers get the panel's cost, not its benefit.
- Source enumeration of consumer-side closed-key readers of the workflow contract (grep for `handoff_action|handoff_output_path|reflect_status`, `src`, `scripts`, `tests`, excluding `.dev`, `docs`): `scripts/eval_workflow_vs_task_builder.py:1139-1176` (superset check `set(CONTRACT_KEYS) <= set(contract)`, version "1.1"), `archive_workspace.py:167-173, ~327` (line `_kv`, version "1.1"), `tests/skills/test_task_workspace_smoke.py:79-80` (writer), brainstorm `refs/handoff-routing.md` (its own contract, not workflow's). None closes the key set, so additive keys with `contract_version` "1.1" are safe at these readers. [CHECKED] This part of the consensus survives.

---

ID: INV-015
CATEGORY: interaction_effects
ASSUMPTION: A later direct module adds a nested directory without a pinned-test change; "nested-kind list extended by hand" (bullet 5).
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE:
- Both R2 files record the `artifacts` rule gap (`return-contract.md:52` names only `nested/reflect-<n>/`) and the test blind spot (`test_worker_contract.py:1477-1482` only requires listed kinds to appear). Under the engine route no new nested kind exists because the panel writes inside reflect's own run directory (`reflect SKILL :311, 338`). Residual: adding a kind needs edits to the closed `EXPECTED_NESTING` equality (`:1678-1689`), see INV-014 F3. [CHECKED]

---

## Claims in the consensus that I found FALSE or unsupported in code

1. FALSE as stated: "effect advisory at ... Stage 10.5" (bullet 3). Stage 10.5 carries a `needs_human_decision` halt and an unattended `blocked` terminal state (`tasklist :1640-1642, 1646`) and, through `--remediate`, a write path that authors a new plan package (`reflect SKILL :369-371, 383-385`). Wave 4 is advisory; Stage 10.5 is "advisory-blocking" by its own label.
2. FALSE in part: "A panel result reaches consumers only as `status`, `coverage_pct`, `tier_reached`" (bullet 3). Consumers also read `needs_human_decision`, `unmapped_requirements`, `run_id`, `report_path` (`task-builder :1682`, `tasklist :1640-1642`, `workflow :89`); and two of the three named fields cannot change with the engine (`reflect SKILL :313`).
3. UNSUPPORTED: "count the share from the existing shadow runs" (A 6.2) and B's contract-based variant. The only aggregator globs `pre-*/panel/manifest.json` of shadow runs (`reflect_shadow_exit.py:209, 215`) and cannot see runs that never reach the panel or any tasklist consumer output directory (INV-005).
4. WRONG in part: "fence tests are a working-tree guard" (bullet 7, withdrawal of "must be changed"). True for 3 git-based tests, false for the content pins in `test_shadow_skill_contract.py:146-238` (INV-012).
5. UNSUPPORTED: the depth-policy remedy is "cheaper" and "pin-safe" (R2-A `:6`, R2-B `:7`). Substring pin: yes. Parity pin: needs both trees (INV-004). Behaviour: it changes remediation route and, at Wave 4, forces Tier 2 on the legacy engine immediately (INV-003).
6. UNSUPPORTED: "one reflect-side switch" as a single bounded change. It flips every UC-1 caller (task-builder PRE gate, troubleshoot and auggie-review handoffs) and has no staged selector reachable from a consumer call (INV-008, INV-010).
7. HOLDS (checked): additive keys with `contract_version: "1.1"` are safe at the three consumer-side readers (INV-014 enumeration); the enum cannot be violated by a short or refused panel (INV-009); "a rubric stop never reads the engine" and "with `legacy` a rubric escalation never calls the panel" (`reflect SKILL :317, 327-328`); the reach chain: without `--t2-engine` the engine is `legacy`, so consumer calls reach the panel only after the default flips (`:87`); workflow depth defaults to `standard` (`commands/reflect.md:98`, `workflow :89`).

## Not checked

`findings_v2.py:36` (cited by B), `plugins/` CLI availability, whether `make verify-sync` covers the plugin tree, research files 08 and 11, `tests/tasklist/` pins of the P2 halt strings beyond `test_tasklist_cli.py:576-580`, any test execution.
