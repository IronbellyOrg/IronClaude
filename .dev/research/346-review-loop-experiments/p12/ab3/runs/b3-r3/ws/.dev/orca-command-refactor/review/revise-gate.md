# Revise report: gate review, GF-01

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place)
- prompt: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:53-55`; ids from `review/gate.md` Reviser brief (GF-01 only)
- Evidence: only the spec and `review/gate.md` were opened; the S:73, S:79, S:154, S:158, S:182, S:194 lines were re-read in the spec before editing. Source files outside the workspace: UNVERIFIED.

## Byte accounting
| | bytes |
|---|---|
| Before | 59305 |
| After | 59481 |
| Net | +176 |

| Finding id | Added | Deleted |
|---|---|---|
| GF-01 | 259 | 83 |

(Deleted clause: "; step 4 uses the command's existing report file, since the contract arrives in P1."; added clause: the P0 reading in AC-0.4. 259 - 83 = 176 (the separator before the clause also changed from "; " to ", ").)

## Findings
| id | Disposition |
|---|---|
| GF-01 | Applied at spec line 194 (AC-0.4), single edit. The P0 live check now says: the brief omits `--unattended`; in step 3 `--report-path` is the command's existing report file and `--outcome` matches that report (not a contract `status`); step 4 is skipped. This removes the impossible demand of 7.2 step 3 (S:182) and the `--unattended` demand of S:73 for P0 only, without changing 7.2 or section 2.3 text. The step-4 wording was replaced rather than extended, so no new rule or section was added. |

Medium and minor findings (GM-01..GM-17, MN-1..MN-5) were left alone. Candidate returned once; no PASS is claimed.
