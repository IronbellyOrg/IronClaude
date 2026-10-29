reviewer: 1
model_class: sonnet
persona: analyzer
agent_type: reflect-reviewer
status: complete   # first result truncated mid R1-04; remainder received on resend
findings:
  - id: R1-01
    class: drift
    severity: important
    plan_ref: "plan:48 (Task 1, acceptance bullet 4)"
    spec_ref: "source.md:440-442; source.md:445"
    claim: "`git diff --name-only HEAD~1 HEAD | rg '^\\.claude/' | rg -v ...` exits 1 under pipefail in the success case (first rg finds nothing), contradicting plan:21 (every line exits 0). The line is plan-added; the spec has none."
    fix: "test -z \"$(git diff --name-only HEAD~1 HEAD | { rg '^\\.claude/' || true; } | { rg -v '^\\.claude/settings\\.json$' || true; })\""
  - id: R1-02
    class: drift
    severity: important
    plan_ref: "plan:277-278 vs plan:286"
    spec_ref: "source.md:710-711; source.md:211"
    claim: "Confirms D-1: the local-scope jq -e inside the exit-0 block aborts it under -e, so the codegraph entry, --version, mcp get, install --list and doctor lines never run."
    fix: "Move the local-scope jq out of the block as its own reported criterion (`|| echo LOCAL_SCOPE_HIT`), printing the `claude mcp remove <name> --scope local` command into the G6 comment."
  - id: R1-03
    class: necessary
    severity: minor
    plan_ref: "plan:107"
    spec_ref: "source.md:534; source.md:540"
    claim: "Confirms D-2: `$E` is undefined within Task 5."
    fix: "Say `E` is built exactly as in ./source.md T2 step 1 (with MT from the evidence file)."
  - id: R1-04
    class: drift
    severity: important
    plan_ref: "plan:79, 85-86 (Task 3); plan:237, 252-253 (Task 14); plan:272, 287 (Task 16)"
    spec_ref: "none (plan-introduced ./artifacts/ paths); user rule: project-root artifacts/ is never staged"
    claim: "Acceptance commands run from the repo root, so `./artifacts/...` resolves to the project-root artifacts/ (never staged) instead of the package's artifacts/. Task 3's real-hash bullet names no before/after command. Task 14's block writes only /tmp but requires ./artifacts/t14-*.txt with no copy line."
    fix: "Define ART=.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts once in Constraints (mkdir -p) and use $ART everywhere; add explicit cp /tmp/p2-final-run.txt and /tmp/p2-new-failures.txt lines to Task 14; give Task 3 an explicit H0 before and a final equality test after."
  - id: R1-05
    class: necessary
    severity: important
    plan_ref: "plan:92, 96 (Task 4 U1-U11) vs plan:104-110 (Task 5 phase function)"
    spec_ref: "source.md:296 (U11); source.md:101; source.md:33"
    claim: "U11 (claude --version fails before discovery/download) tests install_codegraph_mcp, which Task 5 creates; Task 4 cannot pass it."
    fix: "Move U11 to Task 5 (U11-U19, U23, U25); Task 4 keeps U1-U10, U20-U22, U24."
  - id: R1-06
    class: necessary
    severity: important
    plan_ref: "plan:120 (Task 6 --list block) vs plan:131 (Task 7 codegraph_ready())"
    spec_ref: "source.md:142; source.md:194; source.md:573"
    claim: "Task 6's --list block prints 'Ready for Serena retirement' which needs codegraph_ready(), created only in Task 7."
    fix: "State Task 6 omits the Ready line until Task 7 and add the Ready-line check to Task 7's acceptance, or move codegraph_ready() into Task 5."
  - id: R1-07
    class: drift
    severity: important
    plan_ref: "plan:84, 162, 165, 202-203, 244"
    spec_ref: "source.md:445; source.md:625; source.md:325"
    claim: "`A && B` and `A && ! B` lines are non-gating under bash -euo pipefail: errexit ignores a failing A inside an && list and ignores `! B`, so e.g. an INTERNALERROR hit or a missing AUTOINIT doc line does not fail the block unless it is the last line."
    fix: "One condition per line, negatives as `if cmd; then exit 1; fi`."
  - id: R1-08
    class: necessary
    severity: minor
    plan_ref: "plan:216 (Task 12)"
    spec_ref: "source.md:649-651"
    claim: "`uv run --no-project python -c 'import yaml...'` likely fails (pyyaml is a project dependency, pyproject.toml:38); the working form is only a parenthetical fallback."
    fix: "Make `uv run python -c ...` the primary command."
  - id: R1-09
    class: necessary
    severity: minor
    plan_ref: "plan:282 (Task 16)"
    spec_ref: "source.md:714; source.md:374-375"
    claim: "`grep -i connected` also matches Disconnected / Not connected; no negative check as in layer 2 step 5."
    fix: "Add `if grep -iE 'disconnected|not connected|failed' /tmp/p2-t12-get.txt; then exit 1; fi` and copy the get output into the t16 artifact."
  - id: R1-10
    class: drift
    severity: minor
    plan_ref: "plan:54 (Task 2)"
    spec_ref: "source.md:448"
    claim: "Spec T0b requires the outcome to be reported to the coordinator in the completion message; Task 2 drops it."
    fix: "State whether Phase 1 already carried the amendments or this task made them, in the task completion message."
  - id: R1-11
    class: necessary
    severity: minor
    plan_ref: "plan:227 (Task 13)"
    spec_ref: "source.md:416"
    claim: "Task 13 omits the spec's sanctioned fallback for step 5 when `claude mcp get` cannot run in the sandbox."
    fix: "Add: apply the §4.2 Notes fallback (stdio initialize + tools/list, serverInfo.name == codegraph) and record it in P2-layer2.md."
self_audit: "Checked T0-T12 mapping and order, U1-U25 assignment (U11 misplaced), human items and hard rules vs §7, G0-G6 comment placement, Task 9 baseline-diff pipefail safety, Task 10 sed|rg SIGPIPE. UNVERIFIED: whether directory-level pytest runs (tests/core, tests/docs, tests/recommend) hit baseline failures."
calibration:
  calibrator_model_class: opus
  dimensions: {citation_grounding: 0.85, coverage_completeness: 0.80, deviation_classification_clarity: 0.60, risk_surface_coverage: 0.85, recommendation_actionability: 0.90}
  C: 0.80
  per_finding:
    R1-01: confirmed
    R1-02: "confirmed; inherited from spec source.md:710-711"
    R1-03: confirmed
    R1-04: "confirmed (prose ./ refs ambiguous rather than wrong)"
    R1-05: "confirmed; inherited from source.md:466"
    R1-06: "overstated: Task 6 acceptance never checks the Ready line; Task 7 owns the wiring (ordering ambiguity)"
    R1-07: "confirmed for plan:162,165,202-203,244 (plan:84 is standalone, wrong citation); inherited from source.md:601,604,636,675"
    R1-08: confirmed
    R1-09: "confirmed; inherited from source.md:714"
    R1-10: confirmed
    R1-11: "overstated: fallback included by reference (plan:19, plan:223, source.md:416)"
  extra_risk: "Task 7 (plan:134-135): if $(rg -l install_retired_mcp tests) is empty, pytest runs the whole suite."
