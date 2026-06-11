# Finding Verify (C3a) — verify-before-remediate, by reference

This wave is the **false-positive filter** (FR-3.5): between routing (C3) and dispatch (C3b), each
routed finding must independently **ground in real code** before any `/sc:troubleshoot --fix` session
— or any round, or any push — is spent on it. It reuses the repo's existing grounding discipline
**by reference** (never copied or forked) and **spawns the existing `evidence-validator` agent**
rather than authoring a new verifier.

> **Inside the core-purity boundary (NFR-6).** This wave is **read-only**: it `Read`s cited lines and
> spawns a read-only validator agent. It performs NO version-control mutation and contains no shell
> command tokens. The verdict it emits (`verified` / `unverified`) is consumed by the FSM.

## Governing rule — the hallucination contract (reuse, verbatim)

The governing rule is the auggie-review hallucination contract
(`sc-auggie-review-protocol/SKILL.md:22`), reused verbatim:

> "Every finding emitted in the final report must cite a `file:line` that exists in the repo at the
> time of review. Findings that cannot be grounded are dropped, not downgraded."

`sc-troubleshoot-protocol/SKILL.md:24` states the same drop-not-downgrade principle.

## Grounding floor — the Wave-3 file:line validation pass (reuse, cite)

The structural grounding floor is the auggie-review **Wave-3 step-3 "File:line validation pass
(non-negotiable)"** (`sc-auggie-review-protocol/SKILL.md:206-209`), reused by reference:

1. For each finding, **`Read` the cited file at the cited line range**; confirm the line exists and
   (where possible) confirm the cited snippet actually appears on that line (`:207`).
2. For PR/diff mode, additionally confirm the line is within the diff hunks (`:208`).
3. For `needs-grounding` findings, attempt grounding via `mcp__auggie__codebase-retrieval` or `Grep`;
   promote on success, **drop and log** on failure (`:209`).

## The delta C3a adds — "does the defect reproduce"

Spawn the existing **`evidence-validator` agent** (`sc-troubleshoot-protocol/SKILL.md:409`) via the
`Task` tool (read-only, citation-dropping; `allow_command_reexec=false`) for the "cited line exists +
snippet matches" check, then **layer the "defect reproduces" judgment on top** — the delta FR-3.5
adds over the structural drop. Mirror the independent-pass / cross-check shape
(`sc-auggie-review-protocol/SKILL.md:183, 215`): the verification fans out across findings **in
parallel, in one batched message** (T-342).

A finding is:

- **`verified`** — iff its cited `file:line` exists AND the described defect grounds in / reproduces
  against the real working-tree code. → proceeds to C3b dispatch (FR-3.3); emits a `finding_verified`
  run-log event.
- **`unverified`** — location exists but the claimed defect does NOT reproduce (a false positive). →
  demoted to **report-only**, never auto-remediated, **NO round consumed**, reason logged; emits a
  `finding_unverified` run-log event.

## Two distinct rejections — do NOT conflate

| Rejection | Trigger | Mechanism | Where |
|-----------|---------|-----------|-------|
| **Structural drop** (EC-9) | Missing/invalid `file:line` (cannot be grounded at all) | Dropped, not downgraded | the Wave-3 floor above |
| **False-positive demote** (FR-3.5) | `file:line` EXISTS but the defect does NOT reproduce | Demoted to report-only, no round | the C3a "reproduce" delta |

The structural drop happens first (a finding with no valid location never reaches the reproduce
check). The false-positive demote is the NEW filter this wave contributes. Both keep the loop from
burning a round or a push on a hallucinated or stale finding (directly attacking risks R1 and R4).
