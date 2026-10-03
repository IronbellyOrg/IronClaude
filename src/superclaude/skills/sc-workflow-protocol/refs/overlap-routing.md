# Overlap routing

`<pkg>` = `.dev/tasks/to-do/<id>` (the package this run created). After an `implement` handoff re-resolve it by id (it may now be `.dev/tasks/done/<id>`): never write to or recreate a vanished `to-do` path; see the relocation rule in `return-contract.md`.

| Neighbor | Do | Do not |
|----------|----|--------|
| `/sc:implement` | `--handoff implement` → `Skill sc:implement-protocol` with `<pkg>/<id>.md`. Missing skill or implement STOP → contract `partial` (plan stays valid, handoff failed); never silently skip, never `failed` | write product code |
| `/sc:tasklist` | print `/sc:tasklist --source <roadmap>` | invoke on `<id>.md`; emit `tasklist-index.md` / `phase-N-tasklist.md` |
| `/sc:roadmap` | INFO if source already looks like a roadmap | run `superclaude roadmap` |
| `/sc:design` | print `/sc:design @<pkg>/<id>.md` | invoke design |
| `/task` (MDTM) | nothing — a `TASK-WF-*` package is an implement package, not an MDTM task file | route a package to `/task` |

`--handoff none` (default): print next-step strings only, including `/sc:implement <pkg>/<id>.md`. Never print or accept `--output`.
