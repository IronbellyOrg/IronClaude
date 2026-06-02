# R1.3 UC2 Adversarial Review Card — Sonnet

Reviewer stance: independent adversarial review. Every verdict below is grounded in files read in this worktree.

## Overall recommendation: block

Primary blocker: the new `CodeAssertion` is not enforced on the live runtime gate path. The generic pipeline executor still calls `gate_passed(...)` without `envelope`/`repo_root`, causing the new `code_assertions` branch to fail open; the dynamically executed certify step bypasses `execute_pipeline` gate evaluation entirely, so `CERTIFY_GATE` content checks and code assertions are not runtime-enforced.

---

## Q1 — `assert_step_reachable` accepts either `_build_steps` literal or production caller

**Verdict:** Faithful to BUILD-REQUEST `reachable`, but an authorized/necessary generalization beyond design §6.2; flag one precision caveat.

**Deviation class:** Necessary deviation.

**Evidence:** BUILD-REQUEST requires both a code-graph predicate and final-step wiring: `code_assertions: list[CodeAssertion]` at `/config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md:111`, AST dispatch-map checking at `:114`, and `build_certify_step()` wired as final step at `:115`. The design §6.2 scoped the first walker to `_build_steps` literals only at `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-3-codeassertion-design.md:260-263` and explicitly said Step calls outside `_build_steps` are not counted at `:377-384`, but the same design later chooses dynamic post-remediate construction with `_build_steps` unmodified at `:456-460`. The implementation documents the two accepted dispatch shapes at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/code_assertions.py:37-47` and implements `static_reachable or dynamic_reachable` at `:94-99`.

**Adversarial note:** `_build_certify_step_has_production_caller` treats any non-self `build_certify_step(...)` call in `executor.py` as production wiring at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/code_assertions.py:187-228`; it does not prove that the caller itself remains reachable from `execute_roadmap`. Current code is reachable because `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:3403-3409` calls `_run_certify_after_remediate`, which calls `build_certify_step` at `:2165-2170`, but the assertion would still pass if the helper call were later removed and the helper remained.

**Confidence:** 0.91.

---

## Q2 — Runtime enforcement of `CERTIFY_GATE.code_assertions`

**Verdict:** Not enforced at pipeline runtime; currently CI-only, and worse, dynamic certify bypasses gate evaluation entirely. This is a regression against the §MVR §2 guarantee, not merely a harmless R1.3→R1.6 staging deviation.

**Deviation class:** Regression.

**Evidence:** The live generic pipeline executor calls `gate_passed(gate_target, step.gate)` without `envelope` or `repo_root` at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/pipeline/executor.py:264-268`, and its remediation recheck also omits them at `:327-330`. Other CLI call sites likewise omit the kwargs: `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/cli_portify/executor.py:414-417`, `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/sprint/executor.py:840-842`, and `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/cleanup_audit/executor.py:133-137`. `gate_passed` explicitly fail-opens when code assertions exist but either kwarg is missing: `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/pipeline/gates.py:92-98` returns `True, None`.

**Runtime-specific evidence:** The certify step is not inserted into `_build_steps`; it is executed after `execute_pipeline` returns via `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:3401-3409`. `_run_certify_after_remediate` directly calls `roadmap_run_step(certify_step, config, lambda: False)` and appends the result at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:2165-2171`. But `roadmap_run_step` does not run gates; its inner implementation says gate checks happen in `execute_pipeline` at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:1326-1333`. Therefore `CERTIFY_GATE` is not applied to the dynamic certify result at all, so the code assertion is runtime-dormant and the semantic certification checks are also skipped for this dynamic execution path.

**CI-only evidence:** The tests directly call `assert_step_reachable(...)` at `/config/workspace/IronClaude-RoadmapRewrite/tests/roadmap/test_dispatch_reachability.py:62-69` and cover the unwired synthetic case at `:72-80`; that is real CI coverage, but it is not runtime gate enforcement. `CERTIFY_GATE` is wired with only `step_reachable` in `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/gates.py:1461-1471`.

**Fail-open self-contradiction:** The task later targets fail-open defaults for deletion at `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md:98-99`, and PG8.1 explicitly asks QA to verify zero new `return True` stubs at `:524-526`. Introducing `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/pipeline/gates.py:94-98` is a new fail-open shim. The design doc authorized such a temporary skip at `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-3-codeassertion-design.md:176-185` and `:198-207`, but BUILD-REQUEST’s stronger guarantee says CodeAssertion prevents future unwired shipping at `/config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md:114-115`.

**Confidence:** 0.96.

---

## Q3 — `assert_envelope_artifacts_present` requirement and wiring

**Verdict:** The function was required by Step 8.3, not an unrequested expansion; it is not wired into any gate and is currently dead-but-tested.

**Deviation class:** Compliant, with dead-code note.

**Evidence:** Step 8.3 explicitly required a new module containing both `assert_step_reachable(...)` and `assert_envelope_artifacts_present(...)` at `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md:514-516`. The implementation defines `assert_envelope_artifacts_present` at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/code_assertions.py:126-184`. The only gate code-assertion wiring in `CERTIFY_GATE` is `CodeAssertion(name="step_reachable", check_fn=assert_step_reachable, ...)` at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/gates.py:1461-1471`; there is no envelope artifact assertion in that list. The test imports the envelope assertion at `/config/workspace/IronClaude-RoadmapRewrite/tests/roadmap/test_dispatch_reachability.py:19-22` and includes it in the signature invariant only at `:139-161`.

**Confidence:** 0.94.

---

## Q4 — Step-count budget and live executed count

**Verdict:** The literal budget is satisfied, but the “budget unaffected” framing is incomplete: the live successful run now performs the previously-unreached certify step, moving live execution from 13 to 14.

**Deviation class:** Compliant, with notes.

**Evidence:** `_build_steps` currently constructs 13 `Step(...)` objects: extract at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:2235-2262`; two generate steps at `:2263-2301`; diff/debate/score/merge at `:2302-2363`; anti-instinct through remediate at `:2364-2439`; and it leaves certify to dynamic construction at `:2440-2443`. `ALL_GATES` has 14 entries, including `("certify", CERTIFY_GATE)`, at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/gates.py:1546-1562`. The acceptance budget is “Final pipeline step count MUST be ≤ current (14)” at `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md:185` and also appears as acceptance gate #13 at `:101-102`. Dynamic certify now runs after a successful pipeline at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:3401-3409`, and `_run_certify_after_remediate` appends its result at `:2165-2171`.

**Assessment:** Count ≤14 is genuinely satisfied if the counting authority is `ALL_GATES` / live executed step IDs. However, the code comment that “step-count budget is unaffected” at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:2120-2122` hides a real runtime behavior change: before R1.3 `certify` was defined and registered but not executed; after R1.3, a successful remediate path executes it.

**Confidence:** 0.93.

---

## Q5 — New LLM subprocess and certification report on every successful run

**Verdict:** Authorized by §MVR §2’s “wire as final step,” but the behavioral magnitude is under-surfaced and currently not gate-enforced.

**Deviation class:** Authorized expansion.

**Evidence:** BUILD-REQUEST explicitly says to wire `build_certify_step()` as the final step at `/config/workspace/IronClaude-RoadmapRewrite/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md:114-115`. `build_certify_step` creates a `Step` with `id="certify"`, `output_file=certification-report.md`, `gate=CERTIFY_GATE`, timeout 300, and retry limit 1 at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:2088-2105`. `_run_certify_after_remediate` runs only when `remediate` passed at `:2133-2138`, then calls `roadmap_run_step` for that certify step at `:2165-2171`. `roadmap_run_step` runs the normal LLM subprocess path by constructing `ClaudeProcess` at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:1178-1189`, starting it at `:1191`, and waiting at `:1207`. The operator sees “Pipeline complete” before certify at `:3401`, then a certify status message at `:2172-2179`.

**Magnitude note:** This is a new LLM subprocess plus a new `certification-report.md` artifact for every successful remediate path. That is within the stated “final step” requirement, but it is not fully surfaced in the top-level completion semantics: the pipeline prints completion before certify at `/config/workspace/IronClaude-RoadmapRewrite/src/superclaude/cli/roadmap/executor.py:3401-3409`, and because certify bypasses `execute_pipeline`, failures of `CERTIFY_GATE` are not blocking as runtime gates (see Q2).

**Confidence:** 0.92.
