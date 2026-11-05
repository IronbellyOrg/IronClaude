reviewer: 2
model_class: haiku   # alias resolves to glm-5.3
persona: qa
agent_type: reflect-reviewer
status: complete
findings:
  - id: P2R2-1
    class: drift
    severity: important
    plan_ref: "plan:278 inside the block introduced at plan:275 ('This block exits 0'); contradicted by plan:286"
    spec_ref: "source.md:211; source.md:710 (spec T12 block carries the same tension); source.md:197"
    claim: "Task 16's local-scope jq -e sits inside the exit-0 block; on any workspace with a local-scope entry it exits 1, aborting lines 279-284 (registration, version, mcp get, install --list, doctor)."
    fix: "Move the local-scope jq out of the exit-0 block into a report-only criterion that records the 'claude mcp remove <name> --scope local' command in the t16 artifact."
  - id: P2R2-2
    class: drift
    severity: minor
    plan_ref: "plan:107"
    spec_ref: "source.md:534"
    claim: "Task 5 uses $E, never defined in the plan; under set -u the block aborts with an unbound variable."
    fix: "Inline the E construction from source.md T2 step 1 or prefix 'with $E as built in ./source.md T2 step 1'."
  - id: P2R2-3
    class: drift
    severity: minor
    plan_ref: "plan:86 (criterion); plan:73-79 (no before-hash outside Leg B)"
    spec_ref: "source.md:525; source.md:755"
    claim: "Task 3's real-.mcpServers-hash criterion is unverifiable when D is outside the undecided band: no step records the before-hash."
    fix: "Add H0=$(jq -S '.mcpServers' ~/.claude.json | sha256sum) as the first action and a closing equality test."
  - id: P2R2-4
    class: drift
    severity: minor
    plan_ref: "plan:79, 85, 237, 253, 287 vs plan:24"
    spec_ref: "source.md:465; plan:24"
    claim: "./artifacts/ paths resolve to the never-staged project-root artifacts/ when run from the repo root, contradicting the package-artifacts staging rule."
    fix: "Spell out .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/<file> in Tasks 3, 14 and 16."
  - id: P2R2-5
    class: drift
    severity: minor
    plan_ref: "artifacts/coverage-matrix.yaml:319-325 (INF-037 -> Task 7), :454-461 (INF-056 -> Task 3)"
    spec_ref: "source.md:289, :310, :466, :486"
    claim: "Two containment matches are false attributions (U4 -> Task 7, U25 -> Task 3); true carriers Task 4 and Task 5. No requirement lost."
    fix: "Correct matched_task_ids for INF-037 (Task 4) and INF-056 (Task 5)."
  - id: P2R2-6
    class: drift
    severity: minor
    plan_ref: "artifacts/coverage-matrix.yaml (rows cite only parts of source.md)"
    spec_ref: "source.md:59-193, 216-234, 254-272, 323-418, 727-741, 767-785"
    claim: "The matrix under-samples the spec (§2.1-§2.11, §3.1, §3.3-§3.4, §4.2, §6, §8 have no rows); reviewer verified each span is carried by a plan task, so no real gap, but the evidence is thin."
    fix: "Add rows or a documented span-to-task mapping, or annotate the T1 card."
  - id: P2R2-7
    class: authorized
    severity: minor
    plan_ref: "plan:48, 54, 237, 253"
    spec_ref: "source.md:439-443, 447-459, 669-684"
    claim: "Benign additions: Task 1 .claude/ staging guard, Task 2 commit-only-if-changed (Phase 1 spec already has 14 codegraph_ready hits), Tasks 14/16 evidence files."
    fix: "None."
calibration:
  calibrator_model_class: opus
  dimensions: {citation_grounding: 0.75, coverage_completeness: 0.70, deviation_classification_clarity: 0.65, risk_surface_coverage: 0.75, recommendation_actionability: 0.85}
  C: 0.74
  per_finding:
    P2R2-1: "confirmed; inherited from spec T12 block (source.md:709-716 vs :211)"
    P2R2-2: "confirmed (minor)"
    P2R2-3: "confirmed: H0 only in Leg B; plan:86 unverifiable otherwise"
    P2R2-4: "confirmed (spec_ref :465 does not support it; spec has no ./artifacts paths)"
    P2R2-5: "confirmed with mislabel: INF-037 (U4) -> Task 7 false; INF-056 is U23 at :308 (U25 is INF-058, unmatched); carriers Task 4 / Task 5"
    P2R2-6: "overstated: §6 has INF-093, §8 has INF-104; other spans indeed rowless"
    P2R2-7: "confirmed benign; misses that the t16 in-repo artifact conflicts with source.md:706 'Files: none in the repository'"
