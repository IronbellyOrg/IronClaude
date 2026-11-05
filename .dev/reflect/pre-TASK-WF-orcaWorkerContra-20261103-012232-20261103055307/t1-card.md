# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md` (cited `SRC:N`). Tasklist: `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md` (cited `TL:N`). Grounding: `artifacts/grounding-hunks.md` (cited `H<n>`). Coverage matrix: `artifacts/coverage-matrix.yaml`. It has 105 inferred rows and 0 parsed; 29 match by containment, so `coverage_pct_union` is 0.2762 and `S_dev_density` is 0.7238; `coverage_degraded` is parsed-sparse. In scope after deferrals: 62 rows, of which 21 match.

Note on independence: the orchestrator writing this card also wrote the plan. Treat this card as the weakest input; the blind calibration and Tier 2 exist to correct it.

## Coverage and acceptance (qa slice)
- Scope decision. The plan is the static half of P0 (`TL:19`). The spec now says each phase's plan has a static part and a live part, with the owner's commit and install in between (`SRC:238`). Classification: authorized scope limit. AC-0.4, AC-0.5, AC-0.6 and the 7.2 live check are deferred to the P0 live plan by that rule.
- Low union coverage is mostly deferral plus identifier-style citation. Tasks 1 and 2 name rules by WC identifier and section ("Section 2.3 in full", `TL:56`), so containment under-scores rows such as INF-013 (WC-2) and INF-029 (git ownership). By meaning these rows are assigned to `WORKER-CONTRACT.md`.
- Unverified: whether the eleven-check static report (`TL:154`) is enough for the live plan to cite. The spec's phase report is written by the live plan (`SRC:238`), but no line says how the static report's results carry into it.

## Root cause and deviation (analyzer slice)
- Task 3 asks the executor to decide the plugin copy by reading `scripts/build_superclaude_plugin.py` (`TL:69`). A grep of that script for "core" returns nothing (H4), yet `plugins/superclaude/core/` holds six core files (H5). The evidence that decides the convention may live elsewhere (for example a Makefile plugin target), so the task can reach a conclusion from the wrong file. Candidate class: drift (an incomplete instruction).
- Task 6 requires each allowlisted write-verb hit to carry "the phase that converts its command" (`TL:125`). H9 shows about 121 hits, many in commands that no phase converts: `/sc:pr-submit` and `/sc:git` are never workers (`SRC:61`). The reason format has no slot for "never a worker", so an executor may invent a phase. Candidate class: drift.
- Task 1 adds the `KNOWN_CORE_FILES` entry in the same task that creates the file (`TL:42`). `test_known_core_set_matches_shipped` compares the frozenset with the shipped files (H3, `tests/cli/test_how_we_work_install.py:44`), so the tree stays green. No defect.

## Structure and maintainability (refactorer slice)
- The executor rules hold. Tasks run in source order and Depends-on is ignored (H10). No task asks the owner anything (`TL:20`), which matches the no-prompt rule (H10).
- Task 8 runs AC-C4 and then `git add .dev/tasks` (`TL:154`). The staged set at the coordinator's later commit can still change, which is why the Constraints also give AC-C4 to the coordinator at commit time (`TL:19`).

## Self-assessed confidence
0.70 (uncalibrated). Main uncertainty: the card was written by the plan's author.
