reviewer: qa
model: haiku (glm-5.3)
verdict: refactor
findings:
  - id: R2-F1
    severity: MINOR
    class: coverage-gap
    claim: "Two Phase 1 scope limits, 'Historical `.dev/` artifacts stay untouched' and the §2.3 table of leftovers IronClaude does not own (Coder image binary, `serena-agent` uv tool, bundle markers, upstream companions, `~/.local/bin/install.sh`), are carried by no plan task and no Constraint. An executor forbidden to ask the user would have nothing stopping it from editing `.dev/` history or removing Coder-owned leftovers."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:26", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:19-30", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:261", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:279-291"]
    grounded: true
    fix: "Add one Constraints bullet: 'Historical `.dev/` artifacts stay untouched (./source.md §2.1); no task removes or edits the §2.3 leftovers IronClaude does not own: the Coder `/usr/local/bin/codebase-memory-mcp` binary, the `serena-agent` uv tool and `~/.local/bin/{serena,serena-agent,serena-hooks}`, bundle markers, upstream companions and `~/.local/bin/install.sh` (./source.md §2.3)'."
  - id: R2-F2
    severity: MINOR
    class: plan-defect
    claim: "Task 18 claims DoD-1 to DoD-6, but its 'existing' sandbox seeds only `.claude.json` and `.claude/settings.json`, not the old core files and installed primitives with Serena rows that DoD-3 says the sandbox is seeded with. The `rg` check can therefore pass without proving that a forced install overwrites stale Serena-bearing files. The plan copies this gap from spec T14 step 5."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:243", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:248", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:269", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:781"]
    grounded: true
    fix: "Task 18: before `./update.sh`, also seed a stale `$T/old/.claude/CLAUDE.md` and a stale `$T/old/.claude/commands/sc/reflect.md`, each with one `serena` row; keep the expectation that `rg -n -i 'serena|codebase-memory' $T/old/.claude` prints nothing."
self_confidence: 0.82
calibrated_C: 0.77
