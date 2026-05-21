# Triage Checklist (Wave 1)

Passed to the `root-cause-analyst` agent as part of the Tier 1 brief. The agent uses this to structure its investigation; the skill itself does not iterate the checklist mechanically.

## Pre-investigation grounding

Before forming a hypothesis, the agent should have read:

- [ ] The exact code at the location named in the stack trace (or `--scope` if no trace)
- [ ] The auggie retrieval result that the skill provided in the brief
- [ ] The serena symbol overview / surrounding function definitions
- [ ] At least one test that exercises the suspect code path (or noted that no test exists)

If any of these were not possible (e.g. no MCP, file missing), state explicitly in the hypothesis card under "Grounding gaps".

## Cause-class scan

Run through this list once, top-down. Mark the most likely class. Do **not** force a fit — if nothing matches, mark "Other" and explain.

| Class | Typical signals |
|-------|-----------------|
| **Missing/wrong import** | `NameError`, `ImportError`, `ModuleNotFoundError`, "undefined" symbol |
| **Off-by-one / boundary** | `IndexError`, edge-case array access, "works for N items but not 0/1" |
| **Stale state / cache** | "Worked before", reverts on restart, intermittent, env-dependent |
| **Type mismatch** | `TypeError`, `AttributeError on None`, `'NoneType' has no attribute`, recent type-system change |
| **Race / concurrency** | Intermittent, "passes locally, fails in CI", order-dependent |
| **Config / env drift** | Works in one env, fails in another; missing env var; path issue |
| **Logic regression** | Recent diff in suspect file; symptom started after a known commit |
| **External dependency** | Stack trace ends in third-party code; library version pinned/unpinned recently |
| **Test infrastructure** | Test passes when run alone, fails in suite; fixture/teardown leakage |
| **Performance / resource** | OOM, timeout, slow, N+1 query, retained references |
| **Security** | Auth bypass, secret exposure, unsanitised input, IDOR, injection |
| **Build / packaging** | Module not found at runtime, version mismatch, install step missing |
| **Other** | Symptom doesn't fit any of the above (justify) |

## Evidence-or-drop check

For the cause class chosen, the agent must produce **at least one** of:

- A `file:line` citation showing the code that exhibits the bug
- A diagnostic command + its actual output (e.g. `python -c '...'` returning the unexpected value)
- A pointer to the failing test and the exact assertion that fires

If none of these are available, the hypothesis card is marked `unverified` and the confidence dimension "Evidence grounding" is scored 0.0.

## Fix sketch

The Tier 1 hypothesis card includes one proposed fix. It does **not** need to be the final patch — just enough to:

- Name the file(s) that would change
- Describe the change in one or two sentences
- State the test that would prove it (existing or new)

If the fix would touch more than 3 files, that's a signal the issue may be multi-domain — note it for the escalation rubric.

## When to refuse Tier 1

Refuse and recommend `--depth deep` immediately if:

- The symptom is "intermittent" with no reproducer
- The reported scope spans more than 3 modules and no single one is obviously implicated
- The stack trace bottoms out in compiled / closed-source code with no source pointer
- The user's description is ambiguous in a way that a single hypothesis would have to guess at the actual symptom

Refusal is not failure — it's correctly judging that a one-shot pass is the wrong tool.
