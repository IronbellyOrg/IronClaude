# Merge Log (Q25)

## Metadata

- Base: Variant 1 (proposal-A), `adversarial/variant-1-original.md`
- Plan: `adversarial/refactor-plan.md`
- Executor: merge-executor
- Output: `../merged-proposal.md`
- Changes applied: 4 of 4
- Status: complete, validation passed
- Timestamp: 2026-11-14

## Changes Applied

### Change 1: named fallback when Orca refuses the second launch, with a stall rule

- Status: applied
- Before: step 1 ended "If it does not, the owner is asked again; proposal C's route is the natural fallback." "What stays unresolved" listed only "Whether Orca permits the second launch."
- After: step 1 names the fallback (one top-level agent per item via `orca worktree create --base-branch origin/master --agent claude --prompt "<item brief>"`, merged-requirements.md line 552) and the per-item deadline rule (read-only worktree check, then ask the owner; Orca idle notices UNVERIFIED). "What stays unresolved" now points to the fallback and adds the UNVERIFIED idle-notice question.
- Consistency updates caused by this change: the first "What it costs or risks" bullet changed from "the whole route needs replacing" to "is replaced by the fallback in step 1, which drops the brief guard, heartbeats and admitted `worker_done` for the code" (wording from Variant 3 costs and the plan's rejection table); the second "What it unlocks" bullet is qualified "On the primary route (not the fallback in step 1)".
- Provenance: Variant 3; Variant 3 advocate Concession 2

### Change 2: the person's go for the first push in the PR session's conversation

- Status: applied
- Before: step 4 went straight from commit to opening the PR; the Answer did not mention the person's go.
- After: step 4 has the PR session show the diff and wait for the person's go in its own conversation before the first push (meets `WORKER-CONTRACT.md:240`); step 2 keeps the coordinator's showing (`:244`), and step 4 says so. The Answer adds "waits for the person's go in its own conversation before its first push". A cost bullet states the go is needed once per PR and later review-fix pushes at `--monitor 3` are made without asking.
- Provenance: Variant 2 (C-004 unanimous; A-001); cost bullet wording from Variant 2 advocate Concession 3 and Variant 3 advocate weakness 3

### Change 3: name the commit and fix pushes in the grant row; one D3 sentence

- Status: applied
- Before: step 2 said the grant row lists "every write the tool makes" with no list; costs had no D3 item.
- After: step 2 enumerates the grant row (commit of the worker's changes by named paths, PR create, "augment review" re-trigger comment, review-fix commits and pushes made without asking at `--monitor 3`, replies and resolves). A new cost bullet requires one D3 sentence (or contract note) delegating these outward actions to the PR session, closing the gap between `WORKER-CONTRACT.md:240,245` and 6.4 rule 14 (merged-requirements.md line 987).
- Consistency update caused by this change: the "Respects every rule" bullet in "What it unlocks" now reads "Respects every rule once the D3 sentence under 'What it costs or risks' is added".
- Provenance: all three advocates (A-001); Variant 1 advocate Concession 3

### Change 4: reduce the cold-reader cost

- Status: applied
- Before: step 4 began with staging and committing; the cold-reader cost bullet had no mitigation.
- After: step 4 begins "The PR session reads the worker's contract and handoff files"; the cold-reader bullet adds that this (WC-15, `WORKER-CONTRACT.md:64`) reduces but does not remove the cost.
- Provenance: Variant 1 advocate Concession 2

## Post-Merge Validation

- Structural: pass. One H1 (the base title), then the base's five H2 sections in the base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). Numbered steps 1 to 5 kept. Provenance header comments and a `<!-- Source: ... -->` comment on each section or changed block are present.
- References: pass. Internal references ("the fallback in step 1", "the D3 sentence under 'What it costs or risks'") resolve to existing text. The base's reference to "proposal C's route" was removed with Change 1, so no reference to an outside proposal is left dangling. Citations kept: merged-requirements.md lines 552, 964, 987, 962, 951; `WORKER-CONTRACT.md:23,243`, `:240`, `:244`, `:245`, `:64`; 6.4 rule 14. UNVERIFIED labels kept on the second launch and added on Orca idle notices. The single gh reference names `--repo IronbellyOrg/IronClaude`. No em dashes or en dashes.
- Contradictions: pass. The Answer's one-time Orca confirmation agrees with step 1's check and fallback. The supervised-worker claim is limited to the primary route, matching the fallback's loss of those controls. The coordinator's showing (step 2) and the person's go in the PR session (step 4) are stated as both applying, not as alternatives. "One worktree never has two live agents" holds on both routes.

## Summary

- Planned: 4
- Applied: 4
- Failed: 0
- Skipped: 0
