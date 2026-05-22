# Diff Analysis — Fix-1 vs Fix-2 vs Fix-3

| Aspect | Fix-1 | Fix-2 | Fix-3 |
|--------|-------|-------|-------|
| Lines changed in production | 1 (drop kwarg) | 1 + ~8 (helper guard) | 1 (drop kwarg) |
| Lines added in tests | 0 (relies on existing) | ~10 (helper unit test) | ~40 (CLI boundary suite) |
| Closes the reported bug | yes | yes | yes |
| Prevents reintroduction at same call site | no | partial (API guards same-path tautology) | yes (test pins boundary) |
| Prevents reintroduction in other commands | no | yes (helper guard applies to all callers) | partial (generic test in optional step 3) |
| API surface change | no | yes (new exception path in helper) | no |
| Risk of breaking `containment_guard` | none | low (current guard does not use the kwarg) | none |
| Reviewability | trivial | moderate (helper semantics review needed) | moderate (test scaffolding) |

## Key observation

Fix-1 and Fix-3 are **additive** (test + call-site fix), not competing.
Fix-2 is **orthogonal** — it strengthens the API but does not subsume the need for a regression test.

The natural merge is Fix-1 + Fix-3, with Fix-2 as a follow-up.
