# Qualitative Re-evaluation of Disputed Criteria (final)

- Scope: the five criteria where `scoring/qual-pass1.md` and `scoring/qual-pass2.md` disagree.
- Rubric: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md`, section A.2.
- Inputs read: both scoring passes, `blind/variant-B.md` (all 523 lines), `blind/variant-C.md` (all 122 lines), the seed brief's Constraints section, and the repository files named below. Nothing under `debate/` and no diff analysis was read.
- Rule applied: MET only with specific cited evidence; binary; this verdict is final.
- Repository checks (read-only, 2026-11-26):
  - `src/superclaude/skills/sc-implement-protocol/SKILL.md:72`: Wave 0 step 6 is "Open or create ledger (header first, before any product edit)".
  - `SKILL.md:37`: in the STOP table, the "Ledger?" column records when a header may exist ("Header/prior tasks may exist").
  - `src/superclaude/core/HOW-WE-WORK.md:293`: the `/sc:git` row reads "Requested status, add, local smart commit, branch or merge operations using declared controls. ... Do not append push, merge or PR creation."
  - `seed-brief.md:29` (Constraints): "`/sc:git` never pushes, merges or opens PRs".
  - The `git-merge-tree` manual says "After the merge completes, a new toplevel tree object is created".

---

## 1. Variant B, clarity.1

**Criterion (Clarity 1):** Unambiguous language (no "should consider", "might", "as appropriate").

**Pass 1 (NOT MET):** "FR-009: "The `/sc:git` row in `HOW-WE-WORK.md:293` may gain the words ..." leaves the change optional; FR-006 pointer "everything else should be run by the person""

**Pass 2 (MET):** "The vague-word scan finds no hedging in normative text; "could" appears only in quoted rationale (lines 85, 463)"

**Own check:**

- Pass 2's scan list (stated in its header: might, should consider, as appropriate, as needed, when applicable, etc., various, appropriate, properly, adequate, useful, where observable, could) contains neither "may" nor "should". So it could not have found the FR-009 wording.
- A grep of Variant B for may/should/might/could finds:
  - Line 180 (FR-009, a requirement): "The `/sc:git` row in `<pkg>/core/HOW-WE-WORK.md:293` may gain the words "submodule status, update and pointer commit" and "branch removal: /sc:worktrees"." The variant defines no RFC 2119 convention, so "may" leaves it open whether the row edit is part of the deliverable.
  - The rest of the document reads both ways:
    - §9.2 (line 425) requires tests to "Stay green after the FR-009 row edit", which treats the edit as happening.
    - AC-13 (line 520) checks only the three kept phrases, never the added words.
  - Two implementations, one that edits the row and one that does not, would both pass. That is the kind of ambiguity the criterion excludes.
- Pass 1's second example is not decisive. Line 171 ("everything else should be run by the person") is the text of a message printed to the person, not a requirement on the implementer.
- The other "may" hits are clear permissions with defined limits: line 194 "It may run when another command suggests it", line 352 "It may clone or fetch ... authorizes that network read", and line 364 "the command the person may run".

**FINAL: NOT MET.** FR-009 (line 180) states a deliverable change with a discretionary "may". §9.2 (line 425) assumes the edit happens, and AC-13 does not settle it. The requirement is ambiguous.

---

## 2. Variant B, clarity.4

**Criterion (Clarity 4):** Acronyms and domain terms defined on first use.

**Pass 1 (NOT MET):** "Aliases (Path notation table) and RC are defined, but FR-010 uses "`deferred:P4`", "(WC-9)" and "/sc:implement is converted in P4" with neither P4 nor WC-9 defined; R1 uses "TAMPER class" undefined"

**Pass 2 (MET):** "The alias table defines `<name>`, `<pkg>`, `<plugin>`, `<dev>` and `<home>`, and the "(new)" marker is defined; RC-3 explains Q0 ("Q0 pins each task's start tree as `refs/<name>/implement/<slug>/T<id>` and deletes the pin at `complete`"); RC-1 explains S23; RC-2 explains K3 and the launch levels"

**Own check:** Pass 2's examples are accurate, but they show only that some terms are defined. The criterion fails on any undefined term. A grep of Variant B finds several:

- **P4**, first used at line 186 (FR-010): "`deferred:P4` ... /sc:implement is converted in P4". It is never defined. Line 386 only cites "developer guide Archetype 3, "converted in P4"" and does not say what P4 is.
- **WC-9**, first used at line 186 with no explanation. Its meaning can only be inferred 200 lines later, at line 386 ("WC-9's existing rule ...") and line 392 ("end-of-Task commit grant (WC-9 ...)").
- **WC-4**, used at line 384 (FR-040). It is never defined anywhere.
- **Launch levels "W, WA and F"**, used at line 393 (FR-044). They are never expanded. RC-2 (line 67) names only "level `full --submit`", so pass 2's claim that RC-2 "explains ... the launch levels" does not cover these three abbreviations.
- **`TAMPER` class**, used at line 433 (R1). It is never defined.
- **`LL-PROTECTED`** (line 216), **`LL-COMMIT`** (line 224) and **`LL_GIT`** (line 434) are guard identifiers used without definition.

**FINAL: NOT MET.** P4 and WC-9 are used undefined at their first appearance (line 186). WC-4 (line 384), the levels W/WA/F (line 393) and TAMPER (line 433) are never defined at all.

---

## 3. Variant B, correctness.2

**Criterion (Correctness 2):** Technical approaches are feasible with stated constraints.

**Pass 1 (NOT MET):** "FR-013 Merge class runs `git merge <branch>` after a confirmation, which conflicts with the seed constraint "`/sc:git` never pushes, merges or opens PRs" (Constraints)"

**Pass 2 (MET):** "FR-016 runs the commit as a literal Bash command so the guard sees it; FR-024 Q7b sits after `complete` and before the next Q0, so the HEAD invariants hold; FR-020/FR-021 preflight/verify classification"

**Own check:**

- The stated constraint is verified. `seed-brief.md:29`, under "## Constraints", reads: "Keep authorization limits: no commit without authorization; `/sc:git` never pushes, merges or opens PRs; destructive operations need confirmation."
- Variant B adds a merge operation:
  - FR-006 (line 166) lists the operation "`merge <branch> [--interactive]`" with class "merge".
  - FR-013 (line 202) says: "Ask for a yes/no confirmation in chat, and run `git merge <branch>` only after a yes."
  - §1.3 (line 41) narrows the exclusion to "merging into a shared or protected branch". That redefines the constraint rather than meeting it.
- The current routing row (`HOW-WE-WORK.md:293`) mentions "merge operations", but the seed brief's Constraints section is the stated constraint for this work, and it forbids `/sc:git` merges outright.
- Pass 2's evidence is correct for the commit mechanism. It does not cover the merge class, which is part of Variant B's technical approach. A single approach that the stated constraints rule out is enough to fail the criterion.
- Supporting point, not needed for the verdict: FR-019 (line 235) and NFR-003 (line 492) say the helper "writes nothing in the repository". Yet its allow-list (line 236) includes `merge-tree --write-tree`, and `add`/`write-tree` under a private index. These write objects into the repository's object store; the git-merge-tree manual says "a new toplevel tree object is created". So the helper also cannot meet Variant B's own stated constraint as written.

**FINAL: NOT MET.** FR-013 (line 202) runs `git merge <branch>`. That conflicts with the stated constraint "`/sc:git` never pushes, merges or opens PRs" (`seed-brief.md:29`).

---

## 4. Variant B, correctness.4

**Criterion (Correctness 4):** No internal contradictions.

**Pass 1 (NOT MET):** "FR-023 runs the Wave 0 preflight "after step 6 (ledger) and before the first Q0" yet says the run stops "Before the ledger is created", and the STOP row gives Wave 0 "Ledger? No"; implement Wave 0 step 6 is "Open or create ledger (header first ...)" (`SKILL.md:72`), so the ledger already exists. Also FR-009 keeps "Do not append push, merge or PR creation" in the routing row while FR-013 adds a merge operation"

**Pass 2 (MET):** "None found: FR-025 "When any member halts, no commit is made for the batch" agrees with the FR-029 resume clause that routes through Q7b; FR-018's undo hint, "printed and never run", agrees with NFR-005 "nothing in this work runs `reset`""

**Own check:**

- The pairs pass 2 checked are indeed consistent. But finding some consistent pairs does not rule out a contradiction elsewhere.
- FR-023 contradicts itself, and it contradicts the STOP row:
  - Line 265: "Wave 0 runs `commit_plan.py preflight` once with no paths, after step 6 (ledger) and before the first Q0."
  - Line 266: "Before the ledger is created or any product is written, the run stops with `E-COMMIT-REFUSED` and one of the reasons `helper-missing`, `detached`, `branch`, `in-progress-op` or `index-lock`."
  - Line 326, the STOP row: "Ledger? ... Wave 0: No".
  - Verified: `SKILL.md:72` step 6 is "Open or create ledger (header first, before any product edit)". On a fresh run, a preflight placed after step 6 runs after the ledger header has been created. So a refusal there cannot happen "Before the ledger is created".
  - The STOP table's own convention (`SKILL.md:37`, E-NO-AC: "Header/prior tasks may exist") records when a header exists. Variant B's "Wave 0: No" therefore contradicts its own placement of the check.
- I do not rely on pass 1's second example. `HOW-WE-WORK.md:293` already lists "branch or merge operations" in the same row as "Do not append push, merge or PR creation". So that phrase means "do not tack those steps onto a route", and keeping it next to a merge operation is not, on its own, a contradiction. The merge problem is a constraint violation, decided under correctness.2.

**FINAL: NOT MET.** FR-023 puts the Wave 0 refusal "after step 6 (ledger)" (line 265), which per `SKILL.md:72` creates the ledger header. Yet line 266 says the stop happens "Before the ledger is created", and the STOP row (line 326) gives "Ledger? Wave 0: No".

---

## 5. Variant C, clarity.2

**Criterion (Clarity 2):** Concrete rather than abstract (specific actions, not general principles).

**Pass 1 (NOT MET):** "Key interfaces left abstract: FR-019 boundary-key trailer "Its exact token is UNVERIFIED: proposed interface"; FR-021 "versioned structured request" with no format and no STOP code named ("any required STOP-table change must be explicit"); FR-033 "New test filenames are UNVERIFIED"; NFR-003 no timeout values"

**Pass 2 (MET):** "FR-015 "Stage explicit paths with the existing `git add -- <paths>` pattern"; FR-025 "`git status --porcelain=v2 --ignore-submodules=none`"; FR-021 closed outcome list"

**Own check:** The criterion's own test is "specific actions, not general principles". Across the normative body, Variant C states its requirements as specific, checkable actions with named commands, fields, outcomes, orderings and refusal triggers:

- FR-015 (line 36): stage with `git add -- <paths>`, commit with `git commit --only -- <paths>`, "Include deletions and both ends of renames", "Never stage the project runtime mirrors or root-level `artifacts/`".
- FR-018 (line 39) gives an exact list of refusal triggers: "An existing index lock, unmerged entries, active merge/rebase, moved HEAD, changed candidate, or another writer causes refusal". It also requires literal path handling for "spaces, leading dashes and pathspec metacharacters".
- FR-021 (line 42) lists the request fields (checkout root, operation identity, expected parent, boundary key, task IDs, allowed paths, candidate digest, message, journal location) and the result fields. It names exactly six outcomes, "only the first three allow normal continuation".
- FR-022 (line 43) names the journal destinations `<managed package>/artifacts/commit-boundaries/` and `<legacy run>/commit-boundaries/`. It requires reconciling "before selecting the next Q0 and before the existing all-complete short-circuit", and "record `no-change` and never create an empty commit".
- FR-024 (line 50) lists the inspection record fields. It requires sorting "deterministically by nesting and path" and says "No submodules produces an empty list".
- FR-025 (line 51) names `git status --porcelain=v2 --ignore-submodules=none` and the interpretation of `S<c><m><u>` and `-`/`+`/`U`.
- FR-026 and FR-027 (lines 52-53) fix the ordering: "parent initialization before child initialization" and "deepest module first, then intermediate pointers, then the superproject pointer".
- FR-034 (line 80): "Reinvoke twice and assert at most one commit for a boundary key".

Pass 1's items are open parameter values attached to specific actions. None is a general principle standing in for an action:

- FR-019 still requires "Add one machine-readable boundary-key trailer"; only the token's spelling is open.
- NFR-003 still requires "a documented finite deadline for every Git subprocess"; only the number is open.
- FR-021's request has its field list, with no wire format.
- FR-020 specifies the failure action ("report no commit and stop the run before the next Q0") but no STOP code.
- FR-033 leaves only test filenames open; the test cases themselves are listed.

These lower precision, but they do not make the document abstract in the sense this criterion tests. The few principle-style sentences, such as NFR-005 "Treat repository messages ... as data", sit inside requirements that also list concrete actions.

**FINAL: MET.** FR-015, FR-018, FR-021, FR-022, FR-024 to FR-027 and FR-034 (lines 36-80) state specific actions with exact git commands, field lists, outcome sets, refusal triggers and orderings. The deferred items pass 1 cites are open values of specific actions, not general principles.

---

## Final verdicts

| Variant | Criterion | Final verdict |
|---|---|---|
| B | clarity.1 | NOT MET |
| B | clarity.4 | NOT MET |
| B | correctness.2 | NOT MET |
| B | correctness.4 | NOT MET |
| C | clarity.2 | MET |
