# Merge Log

## Metadata

- Base: Variant 2 (`adversarial/variant-2-original.md`, proposal B)
- Plan: `adversarial/refactor-plan.md` (15 planned changes, 5 rejected)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `merged-output.md` (in folder O)
- Changes applied: 15 of 15
- Status: complete, with 3 new contradictions flagged below for the orchestrator (not resolved by the executor)
- Timestamp: 2026-11-14

## Changes Applied

| # | Title | Status | What changed | Provenance tag |
|---|---|---|---|---|
| 1 | Grants as one immutable file each; ledger stays one file | applied | Layout: `grants.md` replaced by `grants/20261114-093000-g0001.md`. Naming: grant id row is now `<YYYYMMDD-HHMMSS>-g<4 digits>`, the file stem. Concurrency: grants are created once and never edited; a correction is a new grant file naming the old one (the base's own correction rule, applied to grants); the ledger stays one append-only file with the reason given. Relation to rules and Cost and risk updated to match. | Base (original, modified): change 1 |
| 2 | Ids qualified by the coordinator | applied | Naming: new "qualified id" row `<coordinator-id>/<row id or grant id>`, example `epic-orchestrator-mode/ironbelly/20261114-093000-g0001`; ledger row id is now `<YYYYMMDD-HHMMSS>` with `-2`, `-3` for the same second (the `<dev>-` prefix dropped because the coordinator id carries it); grant id `g` counter is per coordinator. Relation to rules: grants cited by qualified id. | Base (original, modified): change 2 |
| 3 | `-N` suffix rule | applied | Naming: row now says `<dev>-<N>`, next unused integer from 2, never reused, independent of whether an earlier coordinator is active; coordinator id row allows `<dev>-<N>`. Layout: `ironbelly-2/` folder added. Visibility: developer view is `*/<dev>/` plus `*/<dev>-<N>/`. | Base (original, modified): change 3 |
| 4 | `adhoc` kind | applied | Naming: `<kind>` = `epic`, `release` or `adhoc`, example `adhoc-pr-539-triage` (taken from Variant 3). Layout: `adhoc-pr-539-triage/` added. Intro: one-sentence summary and Terms name ad hoc scopes. | Base (original, modified): change 4; Variant 3 C-009 |
| 5 | Claim procedure and conflict rule | applied | New subsection "Claim procedure" under Concurrency with the five steps from the plan. Step 4's "otherwise rebase and push again" uses the base's own publish step (`git pull --rebase`); no new command. Collision rule 3 points to it; Double dispatch bullet points to it; Cost and risk notes the written rule. | V2 advocate concession 1, V3 advocate weakness 3: change 5 |
| 6 | Never force-push or rewrite `coordinators` | applied | Concurrency: new bullet, with branch protection as an owner decision (UNVERIFIED). Relation to rules: new "No force push" bullet. Cost and risk: force-push risk and restore path from the plan's risk summary. What stays unresolved: branch protection bullet (UNVERIFIED). | Diff assumption A-003: change 6 |
| 7 | Stale-base reading rule | applied | New subsection "Reading current code and documents" under Concurrency: `git show origin/master:<path>` or the owning branch, record the revision, never assume the checkout is current, never rebase `coordinators` onto master. | Diff assumption A-004: change 7 |
| 8 | Identity from `gh` | applied | Naming: handle row says it is read once from `gh` and frozen in `coordinator.md`; new "Identity" paragraph (no authenticated `gh` means no folder and no claim; never `git config user.name`). Layout: `coordinator.md` comment lists the handle. | Diff assumption A-001: change 8 |
| 9 | Handle in the worktree name | applied | Naming: worktree name `coord-<dev>-<kind>-<scope>`, example `coord-ironbelly-epic-orchestrator-mode`, limit recomputed from 54 to 94 characters (the base's 54 plus up to 39 handle characters and one hyphen); worktree branch example updated. Collision rule 5 uses the new name. Relation to rules: `orca worktree create --name coord-<dev>-<kind>-<scope>`. What stays unresolved: shared-host bullet kept with its UNVERIFIED marker, now noting the clash no longer matters. | Diff assumption A-002: change 9 |
| 10 | Unpushed coordinators | applied | Visibility: new "Unpushed coordinators" bullet. Lifecycle: "created" row adjusted so an unpushed coordinator is allowed but cannot claim (needed so the row does not contradict the new bullet). | Variant 3 Visibility (A-006 reconciled with C-003): change 10 |
| 11 | Path-narrowed push grant | applied | Relation to rules: new bullet with the exact path list and the `git diff --name-only origin/coordinators..HEAD` check, marked procedural (no hook). Path list kept exactly as the plan states it (see contradiction N1). | Variant 3 C-008: change 11 |
| 12 | Content rule for pushed files | applied | Relation to rules: new "Content of pushed files" bullet (no tokens, secrets, host or contact details; captures sanitized; fork private but grants quote owner wording). | Diff assumption A-006, V3 advocate concession 7: change 12 |
| 13 | Scope-wide decisions as create-once files | applied | Layout: `decisions/q26.md` under the epic folder (key `q26` taken from Variant 1's entry tag). Naming: decision file row (no length limit set, because the plan sets none). Concurrency: create-once set includes decisions; new "Scope-wide decisions" bullet; merge paragraph lists `decisions/*.md` as a possible conflict. Collision rule 4 added. Claim procedure applies to decision files. Intro and Terms mention decision files. Cost and risk: over-use risk from the plan's risk summary. | Variant 1 strength 1: change 13 |
| 14 | Losing `scope.md` race is recorded | applied | Collision rule 1 rewritten: the loser keeps the pushed `scope.md`, writes a ledger row in their own folder saying what they would change; later changes need the project owner. | V1 and V3 advocate critiques: change 14 |
| 15 | Base branch fallback and branch prefix wording | applied | Facts: second bullet corrected (habit with exceptions, the two named exceptions, no lock depends on it; UNVERIFIED kept). Naming: worktree branch row says "usually" and "no lock depends on it". Relation to rules: fallback to `origin/master` plus one `git merge origin/coordinators` before the first push. What stays unresolved: first bullet names the fallback. | Diff point X-003 and advocates' `git worktree list` facts: change 15 |

Rejected items (C-002, C-001, C-005, C-003, S-003 ledger part) were not applied, as the plan says.

## Post-Merge Validation

### Heading hierarchy

- One H1 (the requested title), then the base's 8 H2 sections in the base's order: Layout, Naming convention, Concurrency, Visibility, Lifecycle, Relation to existing rules, Cost and risk, What stays unresolved.
- Two new H3 subsections, both under Concurrency: "Claim procedure" and "Reading current code and documents". No skipped levels.
- Intro (one-sentence summary, Terms, Facts) kept above the first H2.
- No `FILL-` placeholder remains (checked with Grep).

### Internal references

- Collision rule 3 points to "Claim procedure" under Concurrency: resolves.
- Naming handle row points to "Identity below": resolves (paragraph directly after the table).
- Concurrency merge paragraph points to "Relation to existing rules" for the fallback: resolves (Orca bullet).
- Relation to rules "No force push" points to Concurrency: resolves.
- Lifecycle "created" row points to Visibility: resolves ("Unpushed coordinators" bullet).
- Layout tree and naming table agree on: `grants/` file stem, `decisions/q26.md`, `adhoc-pr-539-triage`, `ironbelly-2`, `coordinator.md` holding the handle.

### Markers and wording

- UNVERIFIED markers: the base has 5 (Facts prefix, worktree branch row, Orca base branch, two unresolved bullets); all 5 are kept, and 2 new ones come from change 6 (branch protection). Total 7.
- Em dash and en dash scan: none found.

### New contradictions introduced by the merge (scanned explicitly)

- **N1. Push grant path list omits decision files (change 11 versus change 13).** Change 11 allows only the coordinator's own folder, `claims/` files naming it, or a new `scope.md`. Change 13 makes coordinators create `<kind>-<scope>/decisions/<key>.md`. Under the pre-push check, a coordinator stops on its own decision file. Left as the plan states; the orchestrator should decide whether `decisions/` files naming the coordinator join the list.
- **N2. Fallback merge versus the push grant and the claim precondition (change 15 versus changes 11 and 5).** When the worktree comes from `origin/master`, the `git merge origin/coordinators` commit makes `git diff --name-only origin/coordinators..HEAD` list every master path, so the change 11 check stops the first push. The merge commit is also an unpushed commit, so the change 5 precondition ("no other unpushed commit") blocks the first claim until the merge is pushed. Left as the plan states.
- **N3. Fallback merge versus the stale-base rule (change 15 versus change 7).** Pushing a master-based merge as `HEAD:coordinators` puts the master tree of that day on `coordinators`. Change 7 says the worktree holds only the branch base plus `.dev/coordinators/` and that `coordinators` is never rebased onto master; a merge is not a rebase, so this is a tension rather than a direct conflict, but `coordinators` would then carry a stale copy of master code. Left as the plan states.

### Checked and not counted as new contradictions

- `-<N>` suffix versus the handle grammar: a GitHub login such as `ironbelly-2` would look like a `-<N>` folder, and the Visibility glob `*/<dev>-<N>/` could match another developer. This ambiguity already existed in the base (`<dev>-2`); change 3 did not create it.
- `coordinator.md` records a worktree path while change 12 forbids host details: a local path is not a host name or contact detail, so no conflict; a reviewer may still want to confirm.
- Lifecycle "created" row path `<scope>/<dev>/coordinator.md` is the base's original shorthand for `<kind>-<scope>/<dev>/`; unchanged by the merge.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 15 | 15 | 0 | 0 |

Three new contradictions (N1, N2, N3) are reported for the orchestrator; the executor did not resolve them because that would be a strategic decision outside the plan.

## Orchestrator post-merge fixes (2026-11-14, in-context, after the executor returned)

| Item | Fix applied to `merged-output.md` | Status |
|---|---|---|
| N1 | `decisions/` files naming the coordinator added to the path-narrowed push grant | resolved |
| N2 | the fallback bootstrap merge is pushed alone, first, recorded as the first ledger row, and is the only push exempt from the path check; the claim precondition is met once it is pushed | resolved |
| N3 | judged a tension, not a contradiction: `coordinators` already carries master's tree as of its base, the bootstrap only moves it forward, and the coordinator reads code and documents through `git show origin/master:<path>`; a sentence saying so was added to the Orca bullet | resolved by clarification |
| `-<N>` ambiguity (listed above as pre-existing) | suffix changed to `--<N>` (two hyphens), which GitHub's published login rule cannot produce (not read in this repo); layout tree, naming table and Visibility glob updated | resolved |

After these fixes no open contradiction remains in the merged output that this worker found. The fixes were not re-reviewed by a separate agent.
