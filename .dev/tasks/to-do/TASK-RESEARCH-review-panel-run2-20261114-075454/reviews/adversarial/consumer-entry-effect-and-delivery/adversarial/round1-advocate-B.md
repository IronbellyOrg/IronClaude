# Round 1 advocate for Variant B (slot C-05, consumer-entry-effect-and-delivery)

Tags: [CHECKED] = I read the file and line in this session. [INFERRED] = follows from checked facts, not executed. Paths are repo-relative.

## Position summary

B's strongest form is B-add: keep the reflect UC-1 call as it is, add a direct panel call beside it, keep the effect advisory at Wave 4 and Stage 10.5, and let blocking enter only as the reviewer feed of the existing Stage 7-10 patch loop, after a replay shows it is better. Two of B's claims are wrong in code and B withdraws them (the 1.1 to 1.2 version bump; the strength of E6 and E7). The rest holds, and the reach argument against A is stronger than B stated.

## Steelman of Variant A

A's best case: reflect is the one choke point, so the panel can reach both consumers with zero call-site edits; the closed enum `reflect_status` has four skill readers plus a validator that A does not have to touch; Stage 10.5 and Wave 4 are advisory by their own text (`sc-tasklist-protocol/SKILL.md:1640,1646`; `sc-workflow-protocol/SKILL.md:93`) so nothing is lost at generation time; the only measured results (E2) show blocking panels producing wrong blockers; and U11 says keep today's entry semantics unless deliberately changed. A is also right that B-replace rewrites pins (`test_workflow_command.py:251-261` hard-codes the exact `/sc:reflect --mode pre --spec ...` string), and right that C-02 conditions stay closed behind reflect while B must carry INV-001/002/003. A carries fewer open conditions. That is a real advantage.

## Strengths claimed

1. **A's reach is narrower than A says.** [CHECKED] The panel is called "only after the final tier is 2" (`sc-reflect-protocol/SKILL.md:313`), and the table at `:325-336` shows `--depth standard` with rubric stop never reads the engine; with `legacy` it is "never"; `panel` is rejected until Stage 3 (`:87`). Workflow Wave 4 passes "defaults for every other flag" (`sc-workflow-protocol/SKILL.md:89`), i.e. standard depth. Tasklist depth 4-9 is `standard auto` and 0-3 is `quick` (`sc-tasklist-protocol/SKILL.md:1677-1680`). So behind reflect only forced-deep phases (`n_cpo >= 1` or `n_strict >= 2`, `:1685`, or score 10+) and rubric escalations reach the panel. B's E4 understated this: A loses the panel for quick phases and for every standard phase the rubric stops.
2. **Generation-time blocking already exists, so X-001 is settled by code.** [CHECKED] Unresolved High or Medium findings after the P2 loop "HALT the skill" (`:1614`), the loop is capped at 2 total passes (`:1604`), and Stage 7 gives each task range to exactly one agent (`:1353-1366`: Agent A tasks 1..split, Agent B the rest), so no task has a second reviewer to corroborate or contradict. A panel feed gives each task at least 2 blind reviewers inside an existing cap.
3. **B-add edits no pinned string.** [CHECKED] `test_workflow_command.py:246-248` uses `any(...)` over Wave 4 lines, and `:255-258` checks one exact call string; both still pass if a second panel line is added. The validator tolerates extra keys (`eval_workflow_vs_task_builder.py:1163`, `set(CONTRACT_KEYS) <= set(contract)`).
4. **A delegate-only entry is forced.** [CHECKED] Workflow Will Not lists "new agents, Task fan-out" (`sc-workflow-protocol/SKILL.md:107`); a direct call must hide the fan-out inside a skill, as reflect does today.
5. **B does not touch `cli/reflect`, `derive_verdict` or the 36-test matrix** (INV-B, INV-L hold).
6. **Plugin facts favour a deliberate decision.** [CHECKED by ls] `plugins/superclaude/skills/` has four skills; no `sc-reflect-protocol`, `sc-tasklist-protocol`, `reflect-reviewer` or `evidence-validator`; `commands/` has `reflect.md` and `workflow.md`, no `tasklist.md`. The workflow parity pin (`test_workflow_command.py:93-103`) already forces both trees to move together.

## Weaknesses identified in Variant A

1. **The consumer gets nothing until three other things land**: Stage 3 engine enablement, the fence test update (A item 8) and the C-04 engine choice. Until then `shadow` is non-authoritative (`SKILL.md:311`). A's own objection 3 concedes dormancy.
2. **A cannot deliver the review, revise, re-review loop.** UC-1 is one pass (A section 4 says so), so the E2 value A cites is exactly what A discards; A offers only "a later module change", which is B's seam by another name.
3. **A's "zero pin changes" is not zero**: the engine switch needs Wave 3/4 text edits outside the fence allow-list (`test_shadow_skill_contract.py:65`). A admits this in item 8.
4. **A leaves workflow's pre-implementation review dead in plugin installs** (A-005) and calls that "a separate decision". That is a real cost A defers, not avoids.
5. **A's low-phase miss is measured only by A's own proposal 6.2**; no data supports ignoring it.

## Concessions

1. **B's 1.1 to 1.2 bump is wrong.** [CHECKED] `eval_workflow_vs_task_builder.py:1140` requires `contract_version == "1.1"`; `sc-implement-protocol/scripts/archive_workspace.py:327-333` raises `E-ARCHIVE-PACKAGE` unless it is "1.1"; `sc-implement-protocol/refs/managed-workspace.md:10` and `test_workflow_command.py:178` repeat it. A bump would make `/sc:implement` refuse and archive-fail workflow packages. B must keep "1.1" and add keys only. [Not checked: whether `_kv` in the archive script tolerates extra keys.]
2. **E7 is weak.** [CHECKED] `LENSES = ("spec", "reflect-pre", "reflect-post")` (`findings_v2.py:36`) shows a missing data row, but B's tasklist module runs on the v1 engine, so the v2 lens gap does not bind it. A's `reflect-pre` lens works on a tasklist today.
3. **E6 is overstated.** [CHECKED] The allowed-sections test reads `git diff HEAD -U0` (`:53`), so it constrains uncommitted edits only; once committed, HEAD moves. Only the 9.1 block pin is a standing constraint. [INFERRED, not run.]
4. **B placed its blocking effect ambiguously.** Stage 10.5 is fenced after the P2 loop (`:1621-1623`), pinned by `test_tasklist_cli.py:572-580`, and is described as not executing the loop. A blocking loop must go in Stage 7-10, not 10.5. B's section 3 said 10.5.
5. **No data shows blocking is better.** E11 stands. B's cost is two reviews per phase in B-add, unmeasured.
6. **A carries fewer open C-02/C-03 conditions** than B (INV-001/002/003, INV-007).

## Shared assumption responses

- **A-002: QUALIFY.** No run exists through either entry, so both designs rest on an unmeasured panel. Acceptable only if any blocking effect waits for the replay and the first release is advisory.
- **A-003: QUALIFY.** [CHECKED] Reflect already runs nested and unattended with `nested/reflect-<n>/` (`sc-workflow-protocol/SKILL.md:91`; tasklist `:1638`; reflect table row `:336` "unchanged"), so the nested Skill-plus-fan-out shape exists. A new panel skill in that shape is unrun; B needs a headless smoke run before shipping, and A needs the same for the engine switch.
- **A-004: QUALIFY.** Fail-open holds only for advisory calls. A blocking feed cannot fail open: a zero-success panel must route like Stage 7's some-vs-zero gate (`:1702`: zero succeeded escalates), and only partial panels degrade to `partial`.
- **A-005: ACCEPT.** The skill's absence and the Wave 4 skip rule (`:93`) are checked; only the runtime outcome is inferred, not executed.
- **A-006: QUALIFY.** [CHECKED] `test_plugin_mirror_matches_src` compares only `*.md` under `sc-workflow-protocol` plus `workflow.md` (`:95-103`); a script or yaml in a new plugin skill is unguarded, so B needs its own parity test. `verify-sync` coverage of `plugins/` is [UNVERIFIED].

## Per-point positions

| ID | Winner | One sentence |
|---|---|---|
| S-001 | Neither | Section order does not affect correctness. |
| S-002 | B | Three separable parts let adoption be staged; A's bundle is all or nothing. |
| S-003 | B | B marks endangered invariants (INV-J, INV-G) in the table, where a reader looks. |
| C-001 | Hybrid | Keep the reflect call (A), add the direct call beside it (B-add); never B-replace. |
| C-002 | Hybrid | Advisory at generation for both; blocking only as the Stage 7 reviewer feed after replay. |
| C-003 | Hybrid | Delivery follows the entry decision; no plugin copy until the CLI-availability question is answered. |
| C-004 | B | Reach behind reflect is far narrower than quick phases alone (strength 1). |
| C-005 | Hybrid | B's additive keys, but `contract_version` stays "1.1" (concession 1). |
| C-006 | B | No fence or Stage 3 dependency, though the fence is weaker than B claimed. |
| C-007 | Hybrid | Stage 7 dimensions for a Stage 7 feed; `reflect-pre` lens for Wave 4 and 10.5. |
| C-008 | B | The block already exists at `:1614`; the choice is only the reviewer feed. |
| C-009 | A | Leave Wave 4 unchanged now; a plan-review module waits for measurement. |
| C-010 | A | A carries fewer open conditions; B's costs are real. |
| C-011 | Hybrid | Run A's static contract-compat test and B's two-arm replay with loop columns. |
| C-012 | B | A module-declared effect is a better precedent for PR review and rf-qa; low weight. |
| X-001 | B | `:1604-1615` shows blocking exists; B swaps the reviewers, not the authority. |
| X-002 | Neither | Both are consistent with the checked facts; the open fact is whether the CLI ships with a plugin. |
| X-003 | B | B-add rewrites no pin; its additions are new parity tests, if the version stays "1.1". |
| X-004 | Hybrid | A is right for a new loop; a reviewer swap inside P2 adds no new cycle number. |
| A-002 | Hybrid | Advisory first, blocking gated on replay (QUALIFY above). |
| A-003 | Hybrid | Headless smoke run required for either route. |
| A-004 | Hybrid | Fail-open for advisory, escalate on zero-success for blocking. |
| A-005 | Neither | Shared and accepted; the runtime outcome stays unrun. |
| A-006 | B | Add a parity test per added plugin file, because the existing pin covers `*.md` of one skill. |

## Code checks run

- (a) [CHECKED] Workflow Wave 4 at `SKILL.md:85-93`; Will Not at `:107`, wording "new agents, Task fan-out; modify the plan from reflect findings". Tasklist Stage 10.5 at `:1619-1646`, call at `:1630-1636`, non-blocking at `:1640`, gate "ships regardless" at `:1646`. All line references in both papers hold.
- (b) [CHECKED] `test_workflow_command.py:93-103` (byte parity, `*.md` only, plus `workflow.md`); `:243-261` as above; `test_workflow_vs_task_builder_companion.py:574-599` (keys required, `skipped` needs a null path, enum closed); `eval_workflow_vs_task_builder.py:1160-1176` (extra keys tolerated). New finding: version pin at `:1140` and `archive_workspace.py:327`.
- (c) [CHECKED by ls] The plugin lacks `sc-reflect-protocol`, `sc-tasklist-protocol` and `reflect-reviewer`; it has `commands/reflect.md` and `workflow.md`.
- (d) [CHECKED] D1 at `sc-reflect-protocol/SKILL.md:317`; `LENSES` at `findings_v2.py:36`.
- (e) [CHECKED] Generation-time blocking exists at `sc-tasklist-protocol/SKILL.md:1604-1615` (High and Medium blocking, 2 total passes, HALT on unresolved, `--unattended` resolves as blocked).
- Not run: any test, any headless call, `verify-sync`, the Stage 2 shadow-run counts, E2 numbers.
