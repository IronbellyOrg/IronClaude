# Evidence validation: REPORT.md.draft

<!-- Returned by evidence-validator (read-only), persisted by orchestrator on receipt 2026-11-08T04:41Z. Policy: full re-read. -->

## Counts
- citations_total: 107 (73 file:line claim pairs + 34 INF rows; same line cited for two claims counted once per claim)
- citations_revalidated: 107
- citations_dropped: 0

## Partial holds (fixed in REPORT.md)
1. R-006 `SKILL.md:90-91` "(Wave 7 runs for every value)": lines right, phrase not there; the phrase "Runs for every `--pipeline` value" is at `refs/claim.md:97`. SKILL.md:90 says "continue with Wave 7 and Wave 8"; :91 has no `none` exclusion.
2. R-004 `block-bare-python.sh:106`: `if (!need[o]) return` ignores later words once `need[o] = 0` is set at :132; cite :106 and :132 together.
3. R-009 `orca_worktree.py:954-975` "no agent and no tab": the code shows no agent; "no tab" follows from the plan's close step.

## Full holds
plan :19, :20, :22, :23, :29-36, :34 (exactly 12 cases), :38-47, :42, :47, :53, :57, :75, :84-92, :88, :94-103, :98, :111; orca_worktree.py :20-30, :198-206, :232-235, :507-513, :521-524, :526, :575, :594-646 (no parse of `created.out`), :611, :614-630, :728, :934-936, :941/:954, :954-975; SKILL.md :17, :89, :92, :149, :150, :170; refs/claim.md :93, :131-136; block-bare-python.sh :48-61; launch-job-identity.sh :14-15; tests/skills/test_issue_orca_worktree.py :376, :559; CLAUDE.md :305, :320, :333-337; docs/user-guide/commands.md :367, :379, :394; HOW-WE-WORK.md :329; WORKER-CONTRACT.md :62; IronOrca src/cli/help.ts :88-89; IronOrca src/shared/runtime-terminal-contracts.ts :38-39.

## INF rows
34/34 valid (exact substrings of source.md:1, including the em dash in INF-027). Coverage arithmetic: 24 matched + 4 departure = 28/34 = 0.8235; unmapped INF-004, 026-030 = the "constraint" rows.

## Uncited factual claims (handled in REPORT.md by citing run artifacts or tagging [INFERRED])
1. Summary finding counts and grades → cite adversarial/merged-verdict.yaml, t1-card.md.
2. Summary Tier 2 route facts → cite artifacts/tier_decision.yaml, adversarial/debate-transcript.md.
3. "Parsed requirement IDs: 0" → cite source.md:1.
4. G-1 "both reviewers withdrew labels; alternatives untested" → cite debate-transcript.md Round 2, diff-analysis.md A-005.
5. D-003, D-004 rationales → [INFERRED].
6. R-006 HOW-WE-WORK plugin mirror (not read) → [INFERRED]; four worktree fields → SKILL.md:121-134 (ten keys counted).
7. R-009 "re-run reuses and does not close" → [INFERRED] (only :575 supports it).
8. R-010 design assertions (`--prompt "--agent"` known hole) → [INFERRED].
9. R-011 humans / other agent tools / `--activate` claim → [INFERRED]; `claude --bare` supported by block-bare-python.sh:61.
10. Finding ids R1-x, M-x are references to adversarial/merged-output.md.

## Self-audit
Dropped nothing: every line number, quote and count tested matched the files on disk. Not read: the HOW-WE-WORK plugin mirror, the run artifacts behind the Summary counts, the hook and install tests the plan cites (not file:line citations in the draft).
