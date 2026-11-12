observation-kind: trace
producer-count: 4 (enumerated by reasoning about Orca CLI and UI, not by grep of an emitted token: the observation is a UI state, not a string)

## Producers
| id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving |
|----|------|-----------|----------------|-----------------------------|----------------------|------------------|-----------|
| P1 | CLAUDE.md:308 | `orca worktree create --name <name>` with no `--agent` leaves only the default plain terminal | none cited | n/a | yes | tier1-observation.md O3, O4 | yes |
| P2 | tier1-observation.md O1 (orca terminal create --help) | `orca terminal create` makes a plain shell | none cited | n/a | yes | transcript grep O4 (0 real calls) | yes |
| P3 | IronOrca src/shared/keybindings/definitions-core-2.ts:69 | UI shortcut Mod+T / "New Terminal" opens a plain terminal | none cited | n/a | yes | daemon.log hasCommand=false (O2), cannot name caller | yes |
| P4 | tier1-observation.md O1 (worker-start / agent launch) | `--agent claude` start that fails or stalls before Claude is ready | none cited | n/a | unknown | worker-list verdict stale_status (O3) | yes |
