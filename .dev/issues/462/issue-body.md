<!-- /sc:issue bug template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Bug Summary

The user reports that orchestrators spawn a large majority of sessions with Opus 5.5 as the default. Investigate the selection path and brainstorm the refactoring needed for Tier1b as the default; the cause is not yet established.

## Environment (OS, version)

- OS: Not known yet
- Version: Not known yet

## Current Behavior

The user observes Opus 5.5 selected by default for sessions in worktrees including `exp346-v-ponytail` and `exp346-v-ledger`, and many others. The actual resolved model and launch configuration for these specific sessions have not been verified in this investigation.

## Expected Behavior

Determine why these sessions select Opus and brainstorm a refactoring toward Tier1b as the default. Preserve deliberate model choices rather than applying a blanket override. Intelligent model-routing research is a separate follow-on issue.

## Steps to Reproduce

1. Not known yet: capture the orchestrator launch arguments, workspace configuration and resolved model for an affected session.

## Impact Assessment (Severity, Blast Radius)

- Severity: Not known yet
- Blast Radius: User reports many orchestrator-spawned sessions across multiple worktrees; extent remains unverified.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

- In tier mode, ccsession exports Opus, Sonnet and Haiku alias mappings only for tiers the owner may use; the Sonnet mapping points to Tier1b (`src/superclaude/skills/ccsession-tag/ccsession:880-898`). These alias settings do not alone establish the main session's resolved model.
- In tier mode, an allowed `ANTHROPIC_MODEL` takes precedence over the default tier when no explicit model or tier is supplied; otherwise selection calls `default-tier` (`src/superclaude/skills/ccsession-tag/ccsession:1143-1170`).
- The Orca wrapper recognizes `--model` as an option with a value (`src/superclaude/skills/ccsession-tag/ccsession-orca:103-108`). Whether it was supplied for the reported launches is not known.
- Prior documentation records alias probes and a same-family Sonnet edge case, not evidence of the model resolved in these reported sessions (`docs/reference/model-aliases.md:48-56`).
- Quick static pass used Glob, Grep and Read; codegraph and auggie tools were unavailable. No runtime probe was performed.

## Related Issues

- #384 is closed and possibly related to ccsession model aliases; it is not established as a duplicate.

## Testing Notes

Compare requested launch arguments, permitted tiers, relevant environment settings and actual resolved model for affected sessions. Check an unqualified launch and intentional explicit model/tier selections, including allowed and disallowed workspace defaults, so a proposed default does not erase deliberate choices. Confirm any proposed change with focused launcher tests and an appropriate runtime check; no tests were run in this static pass.

<!-- sc:issue:create template=issue-bug-simple -->
