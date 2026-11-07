# Scoring Pass 1 (forward order: A, B, C)

Inputs: the three variants, `diff-analysis.md` (X-001..X-004), `invariant-probe.md`, `seed-brief.md`. Repo checks made read-only: `refs/claim.md` Wave 6 (lines 82-90; step 3 is the `E-POST-FAILED` rule, step 4 is "Print ... and STOP"), `SKILL.md` claim steps 1-7. Counts below come from a grep of each variant file.

## Part 1: Quantitative

### Counts

| Metric | A (opus architect) | B (sonnet refactorer) | C (haiku qa) |
|---|---|---|---|
| RC: open questions decided (of 7) | 7 | 7 | 7 |
| RC: success criteria with decision or AC (of 5) | 5 | 4 (SC5 miss: no test pins the re-claim path; static tests 1-5 cover flag, argv, guard only) | 5 |
| **RC** | 12/12 = 1.000 | 11/12 = 0.917 | 12/12 = 1.000 |
| Scorable claims (FR + decisions) | 14 + 7 = 21 | 11 + 7 = 18 | 11 + 7 = 18 |
| Contradictions | 2 (see note A) | 1 (X-003) | 5 (X-001, X-002, X-004, plus 2 found) |
| **IC** | 1 - 2/21 = 0.905 | 1 - 1/18 = 0.944 | 1 - 5/18 = 0.722 |
| Concrete tokens (backticked flags, files, codes) | 206 | 201 | 184 |
| Vague tokens (may, might, normally, appropriate, etc.) | 0 | 3 (May, may, normally) | 3 (may x3) |
| **SR** | 206/206 = 1.000 | 201/204 = 0.985 | 184/187 = 0.984 |
| Internal references (FR-, AC-, T, E, Q, section, in-procedure step) | 12 | 16 | 39 |
| Resolved | 12 | 16 | 36 (see note C) |
| **DC** | 1.000 | 1.000 | 0.923 |
| H2 count (max 9) | 9 | 9 | 9 |
| **SC** | 1.000 | 1.000 | 1.000 |
| **quant_score** | **0.976** | **0.959** | **0.917** |

quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC.
A: 0.300 + 0.226 + 0.150 + 0.150 + 0.150 = 0.976. B: 0.275 + 0.236 + 0.148 + 0.150 + 0.150 = 0.959. C: 0.300 + 0.181 + 0.148 + 0.138 + 0.150 = 0.917.

### Contradiction notes

- **A (2, none from X-001..X-004):** (1) FR-8 "next-steps.md and issue-summary.md MUST exist" after create or reuse, yet section 6 allows "Copy fails | W-WORKTREE-COPY-FAILED" with the worktree reported. (2) Section 2.3 treats the branch prefix as fact ("Orca applies the configured prefix (observed ...)"), while 2.5 rejects branch matching because it "relies on the unverified prefix rule" and Risk 3 marks it UNVERIFIED.
- **B (1):** X-003, "rule B2 stays literally true", against `docs/designs/sc-issue-command.md:27`. No internal contradiction found.
- **C (5):** X-001 (Wave 6 "byte-identical" but step 4 STOPs before Wave 7); X-002 (false "no primitive carries a version marker"; 8 of 47 commands do); X-004 (E5 re-copy with `cp -r <D> <wt>/.dev/issues/<N>/` nests into `<N>/<N>/`); found: FR-1 "byte-identical ... return contract" vs FR-9 / section 4 / E15 adding `worktree_path: null` to unflagged claims; found: E7 records a renamed branch (`issue-<N>-2`), but the next re-claim checks HEAD prints `issue-<N>` (step 1) and list-matches exact `issue-<N>` (step 2), so both miss and FR-6 (no second worktree) breaks.

### Reference note C

Three E-to-T mappings point at tests that cannot exercise the case: E4 (copy fails) to T5 (orca hidden, so no create happens), E9 (lineage) to T2 (static text pin), E11 (wrong repo inferred) to T5 (orca hidden). Counted unresolved.

## Part 2: Qualitative (Claim-Evidence-Verdict)

### Variant A

```
A.Completeness.1 | MET | sections 2.1-2.7 decide all 7 questions; AC-1..AC-6 cover all 5 success criteria
A.Completeness.2 | MET | section 6, 11 rows incl. "List fails or times out", "Matched path gone from disk"
A.Completeness.3 | MET | 2.3 "`<B>` from Wave 0 step 3, fetched in Wave 1"; Risk 4 setup/.claude check
A.Completeness.4 | MET | AC-1 "git merge-base HEAD origin/<B> equals git rev-parse origin/<B>"
A.Completeness.5 | MET | section 8 "Boundaries (Will Not: launch an agent, pass Orca link flags)"; FR-12
A.Correctness.1 | MET | "eight commands already carry `version:`" matches X-002 census; no X-row flags A as wrong
A.Correctness.2 | MET | FR-5 single script seam, fake `orca` on PATH test (diff U-001)
A.Correctness.3 | MET | W- codes in section 4 reused verbatim in sections 6 and 9
A.Correctness.4 | NOT MET | FR-8 "MUST exist" vs section 6 "Copy fails | W-WORKTREE-COPY-FAILED"
A.Correctness.5 | MET | cites `docs/designs/sc-issue-command.md:27`, D3, "UNVERIFIED" tags in section 9
A.Structure.1 | MET | summary, decisions, FR, contract, procedure, edges, tests, files, risks
A.Structure.2 | MET | H2 sections, H3 per open question, numbered FR list
A.Structure.3 | MET | contract (section 4) separate from procedure (section 5)
A.Structure.4 | MET | FR-1..FR-14, AC-1..AC-6, "see section 6", "(2.1)"
A.Structure.5 | MET | 9 H2 headings
A.Clarity.1 | NOT MET | FR-4 "after Wave 6 step 3 succeeded" (step 3 is a failure rule); "reuse first marker match" with no ordering defined
A.Clarity.2 | MET | exact argv code block in section 4
A.Clarity.3 | MET | each H2 carries its scope in the heading
A.Clarity.4 | NOT MET | `<D>` and `<R>` used in 2.4/2.5 without definition; `<main>` used in 2.3, defined only in section 4
A.Clarity.5 | MET | FR-13 "open it and run `.dev/issues/<N>/next-steps.md` there"; section 8 `/sc:workflow` then `/sc:implement`
A.Risk.1 | NOT MET | section 9 lists 6 items, none rated for likelihood or impact
A.Risk.2 | MET | each item names a check ("check on AC-1", "fallback: marker re-list")
A.Risk.3 | MET | "Create fails or times out | failed ... re-run reuses if it finished"
A.Risk.4 | MET | `W-ORCA-MISSING`, `W-ORCA-LIST-FAILED`, 120 s timeout per call
A.Risk.5 | MET | `<D>/worktree.json` record plus AC-1..AC-6 observed run
A.Invariant.1 | MET | "Empty slug | name issue-<N>", "One match", "Several matches", `--limit 500`
A.Invariant.2 | MET | "Claim run in a linked worktree | <main> is still the main checkout"
A.Invariant.3 | MET | "If listing fails, nothing is created"; "STOP before Wave 6 step 3 ... no Orca call"
A.Invariant.4 | MET | basename regex `^issue-<N>(-|$)` (INV-012: ADDRESSED, issue-3 never matches issue-30)
A.Invariant.5 | MET | "Worktree copy of next-steps.md edited by the user | overwritten on re-claim"
```

### Variant B

```
B.Completeness.1 | NOT MET | section 7 static tests 1-5 pin no re-claim path; SC5 requires it
B.Completeness.2 | MET | section 6, 7 rows incl. "Archived worktree", "Create --json shape unknown"
B.Completeness.3 | MET | 2.3 "`<B>` from Wave 0, refreshed by the Wave 1 `git fetch origin`"; step 1 `command -v orca`
B.Completeness.4 | MET | "Acceptance: items 1-5 pass in CI; the four observations are in the plan's evidence file"
B.Completeness.5 | MET | "Left out on purpose: agent launch, a `--worktree <name>` form, dry-run, auto-removal, a `--setup` choice"
B.Correctness.1 | NOT MET | "rule B2 stays literally true" (X-003); "The files stay untracked (D24)" false for tracked `.dev/issues/433/` (INV-005)
B.Correctness.2 | MET | re-list after create avoids the unverified create JSON (U-009)
B.Correctness.3 | MET | four `W-WORKTREE-*` codes used consistently in sections 4-6
B.Correctness.4 | MET | no internal contradiction found; X-003 is a source mismatch, scored in Correctness.1
B.Correctness.5 | MET | "the list fields `branch`, `path`, `isArchived` were read live"; per-item "Verify:" lines
B.Structure.1 | MET | nine sections in brief order
B.Structure.2 | MET | H2, H3 per question, tables for codes and files
B.Structure.3 | MET | code table (section 4) separate from steps (section 5)
B.Structure.4 | MET | FR-1..FR-11, "section 2.5", "go to step 7", "(section 9)"
B.Structure.5 | MET | 9 H2 headings
B.Clarity.1 | MET | step 3 "Exactly one match ... Several: W-WORKTREE-AMBIGUOUS, status skipped, go to step 7"
B.Clarity.2 | MET | exact create call and regex `(^|/)issue-<N>(-[0-9]+)?$`
B.Clarity.3 | MET | headings scoped; summary 5 sentences
B.Clarity.4 | NOT MET | `<D>` used in 2.4 and FR-7 without definition; `<T>` used in 2.5, defined in section 4
B.Clarity.5 | MET | "go through `/sc:workflow` then `/sc:implement`"; "Verify:" commands in section 9
B.Risk.1 | NOT MET | only "Parallel claims ... (low; accepted)" carries a rating; others unrated
B.Risk.2 | MET | each UNVERIFIED item has a "Verify:" step; risks marked "Accepted" with reason
B.Risk.3 | MET | "A failed create is retried by re-running the same command"
B.Risk.4 | MET | "`orca` missing or app not running | W-WORKTREE-NO-ORCA"; projectId upstream risk (U-008)
B.Risk.5 | MET | "Observed run (manual, once, recorded as evidence)"
B.Invariant.1 | MET | step 3 "Exactly one match" / "Several" / step 4 "No match"
B.Invariant.2 | MET | "`<T>` is a linked worktree | `--repo path:<T>` resolution UNVERIFIED"
B.Invariant.3 | MET | "Wave 2 STOP or Wave 6 E-POST-FAILED | Wave 7 never runs"
B.Invariant.4 | MET | "`issue-1` never matches `issue-12`"
B.Invariant.5 | MET | "Two parallel claims of one issue | May make two rows"
```

### Variant C

```
C.Completeness.1 | MET | Q1-Q7 decided; acceptance criteria (1)-(6) and T1-T6 cover all 5 success criteria
C.Completeness.2 | MET | section 6, E1-E15
C.Completeness.3 | MET | Q3 "`<B>` = default branch from Wave 0 step 3"; R2 setup dependency
C.Completeness.4 | MET | "Acceptance criteria: (1) unflagged claim output ... byte-identical ... (6) make verify-sync passes"
C.Completeness.5 | MET | FR-10 "MUST NOT run, prompt or schedule any next-step command in the worktree"
C.Correctness.1 | NOT MET | Q7 "no primitive in src/superclaude/ carries a version marker" (X-002: 8 of 47 do)
C.Correctness.2 | NOT MET | step 5 `cp -r <D> <worktree-path>/.dev/issues/<N>/` nests on reuse (X-004)
C.Correctness.3 | MET | single code `W-WORKTREE-FAILED` used throughout
C.Correctness.4 | NOT MET | "Wave 6 stays byte-identical" vs Wave 6 step 4 STOP (X-001); FR-1 vs E15 `worktree_path: null`
C.Correctness.5 | MET | "Every flag verified in `orca worktree create --help` (2026-11-05)"; R1-R6 tagged
C.Structure.1 | MET | nine sections in brief order
C.Structure.2 | MET | H2, H3 per question, ID-bearing table
C.Structure.3 | MET | edge table, tests and files kept in separate sections
C.Structure.4 | MET | FR, Q, E, T, R IDs; edge rows mapped to tests
C.Structure.5 | MET | 9 H2 headings
C.Clarity.1 | NOT MET | "Placement: a new Wave 7 ... after Wave 6 step 4; Wave 6 stays byte-identical" cannot both hold
C.Clarity.2 | MET | create argv code block with `--setup run`
C.Clarity.3 | MET | headings scoped
C.Clarity.4 | NOT MET | `<D>` used in Q4/Q5 without definition
C.Clarity.5 | MET | FR-7 "one remedy line"; section 8 "goes through `/sc:workflow`"
C.Risk.1 | NOT MET | R1-R6 carry no likelihood or impact rating
C.Risk.2 | MET | R1 "parser accepts top-level and nested result"; R3 "FR-4 contains the blast radius"
C.Risk.3 | MET | "a remedy line repeating the create command"; E8 "Fresh create; record replaced"
C.Risk.4 | MET | E2 "orca not on PATH", E3 "Orca daemon down", E11 "Orca infers a wrong repo"
C.Risk.5 | MET | T4-T6 observed runs "recorded in the plan's verification evidence"
C.Invariant.1 | NOT MET | several matching rows not addressed (diff C-005 "not addressed")
C.Invariant.2 | MET | E9 "Claim run from another worktree"; E15 "Unflagged claim after a flagged one"
C.Invariant.3 | MET | E12 "E-POST-FAILED in Wave 6, flag set | STOP before Wave 7"; E13
C.Invariant.4 | NOT MET | E7 renamed `issue-<N>-2` is missed by both re-claim keys (HEAD == `issue-<N>`, exact list match), giving a duplicate
C.Invariant.5 | MET | E7 "Suffix accepted; created (renamed)"; E8 deleted worktree re-created
```

### Dimension subtotals

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 5 | 4 | 5 |
| Correctness | 4 | 4 | 2 |
| Structure | 5 | 5 | 5 |
| Clarity | 3 | 4 | 3 |
| Risk coverage | 4 | 4 | 4 |
| Invariant and edge case | 5 | 5 | 3 |
| **MET / 30** | **26** | **26** | **22** |
| **qual_score** | **0.867** | **0.867** | **0.733** |

## Combined

| Variant | quant | qual | combined = 0.5 quant + 0.5 qual |
|---|---|---|---|
| A | 0.976 | 0.867 | **0.922** |
| B | 0.959 | 0.867 | **0.913** |
| C | 0.917 | 0.733 | **0.825** |

## Edge-case floor

All three are eligible as base: A 5/5, B 5/5, C 3/5 (floor is 1/5).

## Defects found in this pass, beyond diff-analysis

- A: section 5 step 2 writes the script's stdout to `<D>/worktree.json` while the same script copies `<D>` into the worktree, so a partial or stale `worktree.json` lands in the worktree; A never excludes it (consensus INV-013 took the exclusion from C).
- A: "Matched path gone from disk | failed, W-WORKTREE-STALE; no create" has no recovery path; the flag stays useless for that issue until the Orca row is removed by hand.
- B: the regex tolerates only a numeric suffix, so hand-made rows such as `issue-330-ponytail-plugin` (A-004) never match and a duplicate is created.
- B: "Orca adds a numeric suffix" for an existing git branch is stated as fact without an UNVERIFIED tag (the brief says the suffix applies to a taken name).
- C: E4 and E11 map to T5, which hides `orca` from PATH and so cannot reach a copy-failure or wrong-repo state (counted in DC). E3 (daemon down) is only approximated by T5 (not counted).
