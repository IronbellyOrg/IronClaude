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
| **Substituted primitive** | Same code + same input differs by environment; the differing call is to something the code does not implement (fs, clock, network, DB engine, mocked/polyfilled/vendored API); repro flips by swapping the provider, not the code. Not env drift: no config value differs, and the stack trace (if any) ends in your code, not the provider's |
| **Other** | Symptom doesn't fit any of the above (justify) |

## Evidence-or-drop check

For the cause class chosen, the agent must produce **at least one** of:

- A `file:line` citation showing the code that exhibits the bug
- A diagnostic command + its actual output (e.g. `python -c '...'` returning the unexpected value)
- A pointer to the failing test and the exact assertion that fires
- The diagnostic output must be *read from the system*, not supplied by the harness: a mock, fixture, or assertion that returns the expected value is not evidence (refs/diagnosability-audit.md rubric row S14 and Section 7 constraint 5)

If none of these are available, the hypothesis card is marked `unverified` and the confidence dimension "Evidence grounding" is scored 0.0.

## Producer citation (categorical symptoms)

When the observed symptom is a categorical value — an enum string, a status word, an exit code — and Wave 1.6 enumeration ran, the orchestrator writes `<output-dir>/producers.md` (S1.6.0b) and pastes its `## Producers` table into your brief: `id | line | statement | exit statement | before/after started marker | wall-time compatible | cheap observable | surviving`. Preserve the stable `P1`…`Pn` IDs assigned in grep-hit order, including after candidates are reopened. An audit bypass may leave that table absent.

- With a nonempty surviving menu, cite producers by row identity (row ID and `file:line`), never by re-grepping: any claim that names the value MUST cite the row(s) with `surviving=yes`. Distinct producers sharing an enum token remain distinct candidates.
- Excluding a producer requires the `file:line` of the `return` / `exit` / `break` statement that rules it out (the row's *exit statement* column). "Excluded by source logic" without that line is an unverified counterfactual: Evidence grounding is scored 0.0 for that claim.
- If `producer-count=unknown`, retain all candidates without a unique-cause claim. When enumeration eliminates every row, the orchestrator records the contradiction, reopens the candidates and restores `surviving=yes` before consumers; disputed exclusions remain visible. Missing/header-only/empty surviving menus skip only the producer-citation check with a logged reason: require ordinary grounded source or captured-output citations and continue behaviour binding and independent calibration, with no documentation, locus, evidence or confidence exemption. No menu yields the report form `UNDETERMINED — producer menu unavailable`, never fabricated rows.
- Do not rank producers by plausibility. Until a probe row has run, the partition columns (started marker, wall time, cheap observable) are the only discriminators.
- A passing arm counts as a control only when the execution-locus card records `CONTROL-PROOF: yes: <file:line>` for it.

If a nonempty surviving producer menu is in your brief and your card cites none of its rows, the card is returned unread. This rejection does not apply to the missing/empty-menu bypass.

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
- The symptom is environment-dependent and only one of the environments is reachable, so no A/B probe is possible (the protocol still proceeds with `comparator=none` and an `UNDETERMINED — no comparator` headline; refusal here means recommending `--depth deep`, not halting)

Refusal is not failure — it's correctly judging that a one-shot pass is the wrong tool.
