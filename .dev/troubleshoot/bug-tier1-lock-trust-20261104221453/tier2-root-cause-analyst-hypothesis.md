# Hypothesis: the trust gate belongs at step 5, on the work-tree pyproject.toml, as a pure conflicts.py function; the plan never sees pyproject content

**Agent**: root-cause-analyst (placement lens; worker troubleshoot-analyst)
**Tier**: 2
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: missing trust gate (unvalidated input to a code-executing command)
**Claim class**: `mixed`
**Evidence class**: `runtime_repro` (parent probe, probe-lock-trust.out:6)
**Verdict direction**: `AFFIRM` (the Tier 1 cause stands; this card settles where the fix goes)
**Consistency with docs**: conflicts (the design has no trust model, doc-context.md); matches the owner's decision "before Tier 1 runs uv lock" (audit.log header)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:84-87 @ attended Claude Code session, operator checkout with the merge in progress, operator credentials
producer-citation-check: skipped — menu absent or empty (producers.md header-only)

## Claim
Only step 5 can see the pyproject.toml `uv lock` will read. The probe JSON carries only the merge-tree output (tree id and stage records for conflicted paths), no blob content, and a Tier 1 pyproject.toml is never a conflicted path. A plan-time check needs a new probe and parse_probe field and still cannot see a Tier 2-resolved pyproject that also reaches `uv lock` (step 5, :95). A MechanicalRule hook puts a callable into classification data and still needs step 5 to supply the text. Option 1 (step 5) is the narrowest correct change.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:29; scripts/probe-merge.sh:15-19, :216 | probe fields: status, merge_tree, numstat, programs; no file content |
| E2 | source_citation | src/superclaude/pr_submit/conflicts.py:537, :727-740 | parse_probe decodes stage records only; _plan carries merge_tree_oid, not blobs |
| E3 | source_citation | src/superclaude/pr_submit/conflicts.py:791-792, :202-210 | Tier 1 is regen_only: every conflicted path is uv.lock |
| E4 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:144-159 | precheck allows work-tree changes only on unmerged paths |
| E5 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:95 | Tier 2 runs regen rules after its own resolution |
| E6 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:84-94, :216-223, :296 | no pyproject read; abort section 9; sync_tier3 row names only Tier 2 |
| E7 | source_citation | src/superclaude/pr_submit/conflicts.py:11-21; behaviour-definition: row 3 | stdlib allowlist without tomllib; tomllib needs 3.11+, floor 3.10 |
| E8 | command_output | probe-lock-trust.out:6; behaviour-definition: row 1 (observed), row 2 (unobserved) | backend-path + dynamic probed; path/editable not |

## Proposed Fix
1. conflicts.py: guarded tomllib import; `LOCK_TRUST_UNREADABLE = "pyproject.toml unreadable"`.
2. `lock_trust_findings(pyproject_text: str) -> list[str]`: pure, never raises, fail closed ([LOCK_TRUST_UNREADABLE] when tomllib is None, input not str, parse failure, bad table shape); else in order "build-system.backend-path" (key present), "project.dynamic" (truthy), then per sorted source name "tool.uv.sources.<name> (path)" / "(editable)"; a source value is a table or list of tables. Add tomllib to the docstring and `_ALLOWED_STDLIB`.
3. Step 5: after the precheck, before `git checkout --ours -- uv.lock`, evaluate it on the work-tree pyproject.toml (`uv run --no-sync python -I`, never plain `uv run`); any finding: abort (section 9), halt `sync_tier3`, `uv lock` never runs; section 4 template with File 1/1 `pyproject.toml` (`lock_trust`) and "`uv lock` would run code from this tree: <findings>." Extend :296 to "step 5 (Tier 1 or Tier 2 lock trust gate)".
4. Trust note (refs section 6, commands/pr-submit.md:54).
5. Tests: one per trigger + clean [] (skipped below 3.11); parse error; tomllib None on every Python; a protocol pin that the gate precedes `uv lock` in step 5.

## Confidence
Self-reported 0.86 (calibrator re-grades).

## Risks
- Python 3.10 halts every lock regeneration (intended fail-closed).
- A legitimate base `project.dynamic` halts every Tier 1 (false positive).
- In this repo's dev checkout the gate itself is imported from the merged tree; only the trust note covers it.
- Git, URL and workspace-member builds are outside the owner's list.

## If I'm wrong, it's probably because...
`uv run --no-sync python -I` still builds the project in some uv version, or the session reads the file before the precheck.

## Falsification standard
`lock_trust_findings` returns [] for a pyproject on which `uv lock --offline` still writes the probe marker; or after the precheck the work-tree pyproject.toml differs from `:0:pyproject.toml`.

## Alternatives considered
- Plan-time check: new probe field, parse_probe validation, new plan reason; cannot see a Tier 2-resolved pyproject.
- MechanicalRule.trust_check: speculative (one rule) and still needs step 5 to supply the text.
- Regex gate without tomllib: inline tables and quoted keys get past it.
- `git show :0:pyproject.toml`: no stage 0 for an unstaged Tier 2 resolution.
