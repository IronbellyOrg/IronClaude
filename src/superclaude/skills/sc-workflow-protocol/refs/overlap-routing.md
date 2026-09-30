# Overlap routing

| Neighbor | Do | Do not |
|----------|----|--------|
| `/sc:implement` | `--handoff implement` → `Skill sc:implement-protocol` with `plan.md`. Missing skill → STOP, no silent skip | write product code |
| `/sc:tasklist` | print `/sc:tasklist --source <roadmap>` | invoke on `plan.md`; emit `tasklist-index.md` / `phase-N-tasklist.md` |
| `/sc:roadmap` | INFO if source already looks like a roadmap | run `superclaude roadmap` |
| `/sc:design` | print `/sc:design @plan.md` | invoke design |

`--handoff none` (default): print next-step strings only.
