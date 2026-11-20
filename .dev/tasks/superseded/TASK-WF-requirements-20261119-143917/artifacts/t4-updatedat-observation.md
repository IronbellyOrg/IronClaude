# T4: observation of the Status and Pipeline value times

Throwaway issues (chosen by the executor from the 100 items of Project 2 "Ironclaude - Development", id PVT_kwDODPJUp84Bo16j, owner's instruction "pick the most useful ones"): 
- IronbellyOrg/IronClaude#642 (primary) and #643 (repeat). Both are closed "[ob-442 disposable T1]" and "[ob-442 disposable T2]" launch-level observation issues, Status Done, no Pipeline value.
- Why these: they are the issues made to be disposable, they are closed, and their item has a Status value whose updatedAt already differs from createdAt. Every other item either is a real open issue or is not disposable.
- The Pipeline field exists on the Project (options None, Worktree, Full, Full Submit); no item in the Project has a Pipeline value yet (checked on all 100 items listed).
- Reads are the read-only GraphQL of Task 3 (Status and Pipeline createdAt and updatedAt of the issue's Project item). The executor changes nothing; the owner makes each change.

### Issue #642, read: 0 before any change (read at 2026-11-19T16:43:19Z)
```json
{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-18T19:39:55Z"},"pipeline":null}]}
```

### Issue #643, read: 0 before any change (read at 2026-11-19T16:43:19Z)
```json
{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:28:03Z","updatedAt":"2026-11-18T19:39:56Z"},"pipeline":null}]}
```

### Issue #642, read: 1 after the owner set Pipeline to Worktree (read at 2026-11-19T17:11:11Z)
```json
{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-18T19:39:55Z"},"pipeline":null}]}
```

### Issue #642, read: 1b re-read, same step (read at 2026-11-19T17:11:16Z)
```json
{"labels":[],"items":[{"status":{"name":"Done","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-18T19:39:55Z"},"pipeline":null}]}
```

### Issue #642, read: 1c after the owner set Pipeline to Worktree (second attempt) (read at 2026-11-19T17:20:34Z)
```json
{"labels":[],"items":[{"status":{"name":"Spec","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-19T17:20:09Z"},"pipeline":{"name":"Worktree","createdAt":"2026-11-19T17:20:06Z","updatedAt":"2026-11-19T17:20:06Z"}}]}
```

Note on reads 1, 1b and 1c: the first attempt (reads 1 and 1b, taken at 17:11) showed no Pipeline value, so no change had been saved then. After the owner's second attempt, read 1c shows the Pipeline set to Worktree at 17:20:06 and the Status already moved from Done to Spec at 17:20:09 (Status createdAt unchanged, updatedAt moved). Whoever made the Status move did it three seconds after the Pipeline change, so reads "after the Pipeline change" and "after the Status change" could not be taken apart; read 1c serves as both. The Status change moved only updatedAt, so the change time of a value is the later of createdAt and updatedAt (the rule Task 3 implements).

### Issue #642, read: 2 after the owner created the approved field (no label applied) (read at 2026-11-19T17:27:39Z)
```json
{"labels":[],"items":[{"status":{"name":"Spec","createdAt":"2026-11-18T16:27:18Z","updatedAt":"2026-11-19T17:20:09Z"},"pipeline":{"name":"Worktree","createdAt":"2026-11-19T17:20:06Z","updatedAt":"2026-11-19T17:20:06Z"}}]}
```

Outcome: NOT REACHED. T4 is paused, not failed. The owner replaced the approval label by a custom field 'approved' (set to yes by IronBelly, Clay or a maintainer) and chose "Pause, re-plan" on 2026-11-19. Read 3 (label applied) was never taken; reads 0, 1c and 2 are above. What the reads show so far: setting a Pipeline value creates it with createdAt = updatedAt; moving a Status moves only its updatedAt (createdAt stays); no field named 'approved' exists on Project 2.
