# Reusable Prompt — Neutral 2-Release Split, Debate, Execution, and Fidelity Verification

I want you to help me determine whether a planned release should remain intact or be split into two sequential releases.

This workflow must be **neutral**. Do **not** assume that splitting is correct. In some cases, the right answer will be **not to split at all**.

If a split is justified, the goal is **not** to divide the sprint by size or effort. The goal is to identify a **small, low-lift, high-leverage subset** of work that can:

1. provide real value on its own,
2. improve confidence in the second half,
3. be tested and validated quickly in **real-world usage**,
4. allow us to react and iterate based on those results before planning/executing the second half.

## Global constraints

Apply these throughout all parts:

- Be neutral: **split** and **no split** must both remain valid outcomes until justified by evidence.
- This is **not** about halving the sprint evenly.
- **Release 1**, if a split is recommended, should focus on **planning fidelity and schema hardening only** unless there is compelling evidence otherwise.
- By default, **smoke gate belongs in Release 2**, unless analysis proves it is truly necessary and low-risk for Release 1.
- **Release 2 planning must be gated** on Release 1 passing real-world validation.
- **All tests must be real-world tests** using actual functionality in real usage patterns.
- **No mocks, no simulated tests, no fake harnesses, no synthetic validation** may be treated as sufficient.
- The workflow must explicitly consider the possibility that:
  - splitting is a mistake,
  - splitting adds no tangible value,
  - leaving the release intact is the best option.

## Input material

Analyze the following release artifact(s):

[PASTE SPEC / REFACTOR PLAN / ROADMAP / TASKLIST HERE]

---

## Part 1 — `/sc:brainstorm`
Use **`/sc:brainstorm`** to explore whether this release should remain intact or be split into two releases.

### Requirements for this stage
- Be explicitly neutral.
- Do not bias toward splitting.
- Treat **“do not split”** as a valid and possibly preferred conclusion.
- Identify whether there is a meaningful Release 1 candidate that is:
  - small,
  - low lift,
  - high leverage,
  - valuable to the second half,
  - quickly testable in real-world use,
  - likely to generate evidence that changes or improves the second half.
- Identify risks of splitting, including:
  - creating artificial boundaries,
  - introducing coordination cost,
  - reducing coherence,
  - delaying runtime-integrated work unnecessarily,
  - giving false confidence if Release 1 does not truly validate anything useful.
- Explicitly explore these discovery questions:
  - What are the dependency chains in this release, and which items are prerequisites for others?
  - Are there components that deliver standalone value and can be validated through real-world use before the rest ships?
  - What is the cost of splitting: integration overhead, context switching, release-management burden, or potential rework?
  - What is the cost of not splitting: delayed feedback, big-bang risk, or harder root-cause isolation if something fails?
  - Is there a natural **foundation vs. application** boundary, where Release 1 lays groundwork that Release 2 consumes?
  - Could splitting increase risk by shipping an incomplete mental model, a misleading intermediate state, or a half-baked operator/user experience?

### Output required from `/sc:brainstorm`
Produce:
1. **Recommendation:** split or do not split
2. **Why:** concise reasoning
3. If split is recommended:
   - **Proposed Release 1 objective**
   - **Proposed Release 2 objective**
   - **Candidate scope for Release 1**
   - **Candidate scope for Release 2**
   - **Why this is the best cut line**
4. If split is **not** recommended:
   - explain why keeping the release intact is the better decision
   - identify what risks or lost value would result from splitting

### Additional rule
If proposing a split, explicitly explain why the proposed Release 1 scope is **not just the easiest work**, but work that creates meaningful value for the second half.

---

## Part 2 — `/sc:adversarial`
Take the proposal from Part 1 and run **`/sc:adversarial`** against it.

### Requirements for this stage
- Debate the proposal rigorously.
- Explicitly test the proposition that:
  - the split is unnecessary,
  - the split is harmful,
  - the split creates no tangible value,
  - the wrong work was assigned to Release 1,
  - the split boundary is in the wrong place,
  - the release should remain intact.
- If the proposal survives, validate it.
- If it does not survive, refactor it or reject it.
- If refactored, produce a revised split proposal.
- If rejected, produce a clear “no split” recommendation.

### Output required from `/sc:adversarial`
Produce one of the following:
1. **Validated proposal**
2. **Refactored proposal**
3. **Rejected proposal with recommendation to keep release intact**

For whichever outcome you choose, include:
- strongest arguments for and against splitting,
- decision rationale,
- risks still remaining,
- what evidence would most increase confidence.

---

## Part 3 — Execute the approved proposal with the most appropriate custom command
Use the approved result from Part 2 and execute it using the most appropriate SuperClaude command.

### Command selection rules
- If the outcome is **split approved** and the next step is to create **two release specs**, default to **`/sc:design`**.
- If the outcome is **split approved** and the next step is an execution workflow rather than spec design, use **`/sc:workflow`**.
- Do **not** use `/sc:roadmap` or `/sc:tasklist` yet unless the approved proposal explicitly says they are appropriate at this stage.
- If the result is **do not split**, produce the correct single-release design/update instead.

### Requirements for this stage
If the release is split:
- Produce **Release 1 spec** and **Release 2 spec**
- Make the boundary explicit
- Ensure Release 1 is scoped to **planning fidelity and schema hardening only**, unless the approved proposal explicitly justifies an exception
- Keep smoke gate in Release 2 by default unless the earlier analysis overturned that
- Include an explicit gate:

> Release 2 roadmap/tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.

### Required outputs
If split:
- Release 1 spec
- Release 2 spec
- boundary rationale
- Release 2 planning gate
- real-world validation requirements for Release 1
- explicit traceability requirements ensuring that every deliverable, requirement block, or downstream planning item in both outputs maps back to the original release scope with no orphan scope and no invented scope

If no split:
- updated single-release spec
- rationale for preserving integrity
- validation strategy for the intact release

---

## Part 4 — Deep analysis and auditable verification
After Part 3, run a **deep analysis and auditable verification** using the most appropriate command, typically **`/sc:analyze`**.

### Verification objective
Verify that:
1. all aspects of the original spec are represented across the resulting output set,
2. nothing load-bearing was lost,
3. no requirement was silently weakened or reinterpreted without explicit documentation,
4. together, the resulting spec(s) preserve **100% of the original intended scope and meaning**.

### Verification requirements
Produce an auditable verification package with:

1. **Coverage matrix**
   - original spec section / requirement
   - destination in Release 1 or Release 2
   - status: preserved / transformed / deferred / removed
   - justification
   - explicit traceability check showing that every resulting requirement, deliverable, or planning item maps back to original source scope

2. **Losslessness check**
   - identify anything missing
   - identify anything weakened
   - identify anything newly introduced
   - explain whether each change is valid

3. **Fidelity assessment**
   - explicitly evaluate whether the two resulting specs together achieve **100% fidelity** with the original
   - if not, list exact gaps and required remediation

4. **Boundary integrity check**
   - verify that Release 1 contains only what belongs there
   - verify that Release 2 contains what was intentionally deferred
   - flag misplaced items

5. **Release 2 planning gate verification**
   - confirm that Release 2 roadmap/tasklist generation is blocked until Release 1 passes real-world validation

6. **Real-world validation audit**
   - verify that Release 1 validation uses real functionality in real-world use cases
   - reject any mocked or simulated validation as insufficient

### Required conclusion
End with one of these:
- **Verified: split is lossless and acceptable**
- **Verified with required remediation**
- **Not verified: split should be revised or abandoned**

---

## Final output format
Return the result in this order:

1. **Part 1 — Brainstorm outcome**
2. **Part 2 — Adversarial verdict**
3. **Part 3 — Executed design/spec output**
4. **Part 4 — Auditable fidelity verification**
5. **Final recommendation**
   - split / no split
   - why
   - what must happen before Release 2 planning can begin

---

## Hard rules
- Do not assume a split is beneficial.
- Do not preserve a split just because it was proposed.
- Do not treat mocked or simulated testing as valid evidence.
- Do not allow Release 2 roadmap/tasklist generation before Release 1 passes real-world validation.
- If the best answer is “keep the release intact,” say so clearly.
