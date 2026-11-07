# Scoring Pass 2 (reverse order: C, B, A)

Method: independent read of the three variants, diff-analysis.md (X-001..X-004, A-004), invariant-probe.md and the seed brief. A criterion is MET only with a quoted or sectioned citation. Shared note: `<D>` (and A's `<R>`) is never defined at first use in any variant, so Clarity.4 is 0 for all three. All three keep nine H2 sections.

## Variant C (variant-3-haiku-qa)

C.Completeness.1 | MET | s2 answers Q1-Q7; s7 T1 STOP, T2 argv pin, T4 path+copy, T3 re-claim
C.Completeness.2 | MET | s6 table "E1".."E15"
C.Completeness.3 | MET | E2 "orca not on PATH", E13 Wave 0 branch, R2 setup dependency
C.Completeness.4 | MET | s7 "Acceptance criteria: (1)" to "(6)"
C.Completeness.5 | 0 | no out-of-scope list, only "Rejected:" lines
C.Correctness.1 | 0 | Q7 "no primitive ... carries a version marker" is false (X-002, 8 of 47)
C.Correctness.2 | 0 | "cp -r <D> <worktree-path>/.dev/issues/<N>/" nests on re-claim (X-004)
C.Correctness.3 | MET | "reused", "created", "worktree.json" used uniformly
C.Correctness.4 | 0 | "Wave 6 stays byte-identical" vs Wave 7 "after Wave 6 step 4" which STOPs (X-001)
C.Correctness.5 | MET | "Every flag verified in `orca worktree create --help`", B2 line cited
C.Structure.1 | MET | summary, decisions, FR, contract, procedure, edges, tests
C.Structure.2 | MET | s2 uniform Q-headings with Decision/Why/Rejected
C.Structure.3 | MET | s3 requirements apart from s5 procedure
C.Structure.4 | MET | IDs FR-, E, T1-T6, R1-R6 and E-to-T mapping
C.Structure.5 | MET | nine H2 sections 1-9
C.Clarity.1 | 0 | Wave 7 placement vs Wave 6 STOP unclear; "parser must accept a nested `result`"
C.Clarity.2 | MET | s4 exact `orca worktree create` block
C.Clarity.3 | MET | each section has one stated job
C.Clarity.4 | 0 | `<D>` used undefined
C.Clarity.5 | MET | s8 file table, "go through `/sc:workflow`"
C.Risk.1 | 0 | R1-R6 carry no likelihood or impact rating
C.Risk.2 | MET | R1 "Verify in T4", R3 "FR-4 contains the blast radius"
C.Risk.3 | MET | E4 "worktree printed", "remedy line repeating the create command"
C.Risk.4 | MET | E2 orca missing, E3 "Orca daemon down"
C.Risk.5 | MET | T4-T6 observed runs, forbidden-flag regex in T2
C.Invariant.1 | 0 | no multiple-row or row-cap rule; only exact branch match
C.Invariant.2 | MET | E6 "Record deleted, list finds branch", E8 deleted worktree
C.Invariant.3 | MET | E12 "STOP before Wave 7", E13 "Wave 7 never reached"
C.Invariant.4 | 0 | "exactly one row" asserted while cp nesting duplicates tree; no multi-match count rule
C.Invariant.5 | MET | E7 "created (renamed)", E9 other-worktree claim
C subtotals: Completeness 4, Correctness 2, Structure 5, Clarity 3, Risk 4, Invariant 3. MET 21/30. qual_score 0.70. Edge-case floor: PASS (3/5).

## Variant B (variant-2-sonnet-refactorer)

B.Completeness.1 | MET | s2.1-2.7 cover all questions; s7 observed run covers path, copy, unflagged, STOP
B.Completeness.2 | MET | s6 table "Archived worktree", "Two parallel claims"
B.Completeness.3 | MET | step 1 "`command -v orca` missing", s9 UNVERIFIED prerequisites
B.Completeness.4 | MET | s7 "Acceptance: items 1-5 pass in CI; the four observations"
B.Completeness.5 | MET | "Left out on purpose: agent launch, a `--worktree <name>` form, dry-run"
B.Correctness.1 | 0 | s1 "rule B2 stays literally true" overstated (X-003, design doc line 27)
B.Correctness.2 | MET | re-list after create "not relying on the unread create JSON"
B.Correctness.3 | MET | `W-WORKTREE-*` family and status words consistent
B.Correctness.4 | MET | Wave 6 step 4 hand-off agrees with FR-4 and step 6
B.Correctness.5 | MET | "fields `branch`, `path`, `isArchived` were read live"; "grep found only the HOW-WE-WORK mirror"
B.Structure.1 | MET | decisions before FR before procedure
B.Structure.2 | MET | s2.x uniform Decision/Why/Rejected
B.Structure.3 | MET | s4 code table separate from s5 steps
B.Structure.4 | MET | FR-1..FR-11, numbered steps, "section 2.5" cross-refs
B.Structure.5 | MET | nine H2 sections
B.Clarity.1 | MET | step 3 "Exactly one match ... Several: ... skipped"
B.Clarity.2 | MET | exact create call with `<T>` and `<B>` defined
B.Clarity.3 | MET | s8 "No new file" scoping, s9 split into UNVERIFIED and risks
B.Clarity.4 | 0 | `<D>` undefined at first use (2.4)
B.Clarity.5 | MET | "go through `/sc:workflow` then `/sc:implement`"
B.Risk.1 | 0 | only "(low; accepted)" on one risk, no impact ratings
B.Risk.2 | MET | each UNVERIFIED line has "Verify:" action
B.Risk.3 | MET | "A failed create is retried by re-running the same command"
B.Risk.4 | MET | "`W-WORKTREE-NO-ORCA`", upstream projectId risk
B.Risk.5 | MET | flag-guard test 3, "watch network or Orca logs"
B.Invariant.1 | 0 | zero/one/several rows handled but list call has no `--limit` or truncation check (INV-001)
B.Invariant.2 | MET | "Archived worktree ... Ignored", re-list after create
B.Invariant.3 | MET | FR-4 gating, "`<T>` is a linked worktree ... UNVERIFIED"
B.Invariant.4 | MET | "`issue-1` never matches `issue-12`", `(-[0-9]+)?$` suffix
B.Invariant.5 | MET | "re-claim leaves stale copies", skip-existing protects user notes
B subtotals: Completeness 5, Correctness 4, Structure 5, Clarity 4, Risk 4, Invariant 4. MET 26/30. qual_score 0.867. Edge-case floor: PASS (4/5).

## Variant A (variant-1-opus-architect)

A.Completeness.1 | MET | s2.1-2.7 in seed order; FR-2, FR-3, FR-8, FR-13, AC-1..6 cover success criteria
A.Completeness.2 | MET | s6 table, "Matched path gone from disk"
A.Completeness.3 | MET | FR-5 script seam, "checks `orca` on PATH", fetch dependency `origin/<B>`
A.Completeness.4 | MET | s7 "AC-1".."AC-6"
A.Completeness.5 | 0 | only FR-12 "MUST NOT" and s9.6 "later agent launch"; no scope-exclusion list
A.Correctness.1 | MET | "eight commands already carry `version:`" matches X-002; observed prefix example fits probe
A.Correctness.2 | MET | script seam with timeouts; "else re-lists by marker" fallback for unknown JSON
A.Correctness.3 | MET | `W-WORKTREE-*`, `worktree_status` terms stable
A.Correctness.4 | MET | Wave 6 step 4 made conditional, same story in FR-3, FR-4, s5
A.Correctness.5 | MET | "observed: `bare-python-hook-357` is on `ironbelly/...`"; "`clickup_claim.py` pattern"
A.Structure.1 | MET | order matches the brief's required flow
A.Structure.2 | MET | H3 2.1-2.7 uniform fields
A.Structure.3 | MET | ref, script, tests, files each in own section
A.Structure.4 | MET | FR-1..14, AC-1..6, "section 4" references
A.Structure.5 | MET | nine H2 sections (template parentheticals left in headings, clutter only)
A.Clarity.1 | MET | s5 numbered steps, "reuse first marker match, else first path match"
A.Clarity.2 | MET | two exact argv lines, return contract YAML
A.Clarity.3 | MET | s1 limited to five sentences, each section scoped
A.Clarity.4 | 0 | `<D>` and `<R>` used undefined (`<main>` is defined)
A.Clarity.5 | MET | FR-13 "open it and run ... next-steps.md there", `/sc:workflow` route
A.Risk.1 | 0 | six items, no likelihood or impact ratings
A.Risk.2 | MET | "check on AC-1", "fallback: marker re-list"
A.Risk.3 | MET | "a timed-out create that finished is found next time"
A.Risk.4 | MET | "List fails or times out", `W-ORCA-MISSING`, 120 s timeout
A.Risk.5 | MET | fake-`orca` pytest plus AC observed run
A.Invariant.1 | MET | "Empty slug", one/several matches, `--limit 500` (truncation unchecked, INV-001)
A.Invariant.2 | MET | marker comment vs path, "Matched path gone from disk"
A.Invariant.3 | MET | "If listing fails, nothing is created", `<main>` via git-common-dir
A.Invariant.4 | MET | `^issue-<N>(-|$)` anchors (INV-012 ADDRESSED), several-match rule
A.Invariant.5 | MET | "edited ... overwritten on re-claim", slug drift on title edit
A subtotals: Completeness 4, Correctness 5, Structure 5, Clarity 4, Risk 4, Invariant 5. MET 27/30. qual_score 0.900. Edge-case floor: PASS (5/5).

## Summary

| Variant | Comp | Corr | Struct | Clar | Risk | Inv | MET/30 | qual_score | Floor |
|---|---|---|---|---|---|---|---|---|---|
| C haiku-qa | 4 | 2 | 5 | 3 | 4 | 3 | 21 | 0.700 | pass |
| B sonnet-refactorer | 5 | 4 | 5 | 4 | 4 | 4 | 26 | 0.867 | pass |
| A opus-architect | 4 | 5 | 5 | 4 | 4 | 5 | 27 | 0.900 | pass |

Key separators: C loses Correctness on X-001, X-002, X-004 (all orchestrator-verified). B loses one point on the overstated B2 claim and one on missing row-cap handling. A loses on missing out-of-scope list. Residual unaddressed items in all three: INV-001 truncation, INV-005 tracked files in the new worktree, A-004 hand-made worktree names.
