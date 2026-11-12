# Evidence Validation Report (final pass, after repairs)

**Report under validation**: .dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/REPORT.md.draft
**Timestamp**: 2026-11-08T00:22:12Z
**Total citations**: 14 numbered Evidence citations (12 file:line, 2 command), plus 3 supplementary file:line citations outside Evidence
**Verified**: 12 numbered, plus 3 supplementary
**Dropped**: 1 (D1, a detail inside the Diagnosis section; resolved by the parent, see Notes)
**Passed through (command, no reexec)**: 2
**Suggested report status**: partial. No structural FAIL and no A8 block this pass. A2 skipped. (Returned by evidence-validator; persisted by the parent; tables condensed. Attempt 1 is kept at evidence-validation-attempt1.md.)

## Verified citations
All 12 numbered file:line citations matched verbatim: CLAUDE.md:308 and :320; IronOrca worktree-first-surface.ts:2-14; worker-topology.ts:67-76; worker-start-receipt.ts:101; explicit-worker-terminal-validation.ts:49-54; install_core.py:70-72; src/superclaude/core/CLAUDE.md:47 (rule 45-53); orca_worktree.py:27 and :42; definitions-core-2.ts:69 and :74. Supplementary: CLAUDE.md:307, :312; core/CLAUDE.md:52.
Qualifications (not drops): item 2 needs the caller at runtime-local-worktree-terminal-startup.ts:202-214 (recorded in tier1-observation.md row 1, not cited in Evidence); item 3 "not the seeded one" is inference from `createTerminal`; item 4's recovery string is conditional on `releasable`; items 10a/10b are docstring lines documenting the script's command set.

## Dropped citations
- D1 (detail, Diagnosis > Falsifiers > Core M-QE): "observed on worktree liveness-v1-contract (a live worker tab titled '· Claude Code', tier1-observation.md O3)": snippet-mismatch at the time of validation, because O3 held only the generic statement and the named worktree, handle and title were in no recorded capture span. The reference value `true` itself was consistent with the generic O3 text.

## Passed-through citations (command, allow_command_reexec=false)
- Item 8 `grep -c "Orca session launches" ~/.claude/CLAUDE.md` → `0`: agrees with tier1-observation.md O5.
- Item 9 `jq` for install-core-stale-warning → `2026-11-07T05:36:16.234Z startup-command-delivery false 0` and one `session-created`: the exact tab-separated lines are now recorded in tier1-observation.md O2 (last bullet); attempt 1's gap is closed.

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | no definite enum token named; Diagnosis is `UNDETERMINED — among {...}`; max calibrated 0.30; observation_paths empty |
| A2 | skipped | — | — | input absent: diff_path (null) |
| A3 | no | — | — | draft Date 2026-11-08T00:18:09Z not later than any artifact mtime + 5 min; not T00:00:00Z |
| A4 | no | — | — | closure says "not applicable"; HC0 decisions use `not_applicable` |
| A5 | yes (literal reading; see Notes) | `consensus_on_unobserved` | partial | candidate-fixes.md:5 no longer says consensus (F1 row is `split-pending ... not marked consensus`), so the first clause is not met; the second clause ("or the calibration file states the evidence class is none/static") is met by every calibration file (tier1-calibration.md:14, tier2-root-cause-analyst-calibration.md:9, tier2-quality-engineer-calibration.md:9, tier2-system-architect-calibration.md:9 declare `source_static`). The validator read the second clause as part of the first and returned "no"; the parent adopts the literal standalone reading (agent-assertions.md:17), which fires. Effect: a partial contribution only (the status was already partial); no claim in the draft depends on consensus. |
| A6 | no | — | — | diagnosability-tasklist.md row M-QE: Reference-context value is the single literal `true` (observed reference arm); counter-case stated separately as a non-reference; no other row has a Reference-context field |
| A7 | no | — | — | execution-locus.md RUN-SITE now binds all four producers P1-P4 to runtime locations as an explicitly unresolved candidate set; locus mtime 00:21:55Z is after producers 00:00:28Z |
| A8 | no | — | — | the failing arm is an Orca UI tab or LLM orchestrator, not a CI job |
| A9 | no | — | — | M-QE literal `true` agrees with the recorded reference arm (O3); the failing-side counter-case was not used as the reference; CONTROL-PROOF stays unknown |
| A10 | no | — | — | `capability-verdict: n/a`; Emitter search block present with `usable-capture-routes: 1` |

## Notes
- Repairs from attempt 1 held: A6 and A7 no longer fire; all 12 numbered file:line citations still match.
- D1 resolution (parent, after receipt): the named capture was real, produced by the same-turn `orca terminal list --json` and `orca orchestration worker-list` commands; the parent wrote those two rows verbatim into tier1-observation.md O3. The draft text is unchanged. This resolution adds an observation, not a new file:line citation, and was not re-validated by a third pass (the structural rules were unaffected and the one repair/revalidation attempt was already used).
- The four calibration files still quote the earlier `RUN-SITE: pending-producers`; they predate the repair; the calibrators' `locus_unknown` flag still stands (SAME-ENV unknown).
- Not verified (no line claim in the draft): the docs under docs/ in Documentation Context; the "#412 (issue) / #415 (fix)" numbering outside tier1-observation.md O5.
- Skipped inputs: A2 (`diff_path` null); A1's observation-corpus clause (`observation_paths` empty); A6's first-run `n/a` exemption (`first_instrumented_run` unknown).
