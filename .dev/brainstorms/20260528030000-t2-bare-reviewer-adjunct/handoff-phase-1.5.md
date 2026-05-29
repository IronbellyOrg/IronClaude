# Handoff prompt — Phase 1.5 (c7-enrichment skill + integration + spec-gap fixes)

> Paste the section below (everything inside the fenced block) verbatim into a fresh
> Claude Code session to hand off Phase 1.5. It is self-contained — the new agent
> should not need to read this surrounding commentary.

---

```text
You're picking up implementation of Phase 1.5 from a 6-phase tasklist. Phase 1 is
COMPLETE and committed; Phase 1.5 is the next gate before Phase 2 or 3 can start.

## Repository & Branch

- Repo: IronClaude (IronbellyOrg/IronClaude — a FORK; PRs must target the fork, not
  upstream SuperClaude-Org. See project CLAUDE.md.)
- Branch: brainstorm/t2-bare-reviewer-adjunct (HEAD = 8a1bbc72)
- Worktree to work in: /config/workspace/IronClaude/.claude/worktrees/BareReview
  (the bundle and Phase 1 artifacts live in this worktree; the branch is checked out
  here. The main repo at /config/workspace/IronClaude is on a DIFFERENT branch —
  enter this worktree, do not cd to the main repo.)
- Bundle path (in the worktree):
  .dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/

## What just shipped (Phase 1 — commit 8a1bbc72)

The sc-bare-review skill v1.0 is live at src/superclaude/skills/sc-bare-review/:

  SKILL.md                       (thin orchestrator, sonnet, Bash+curl reference impl)
  scripts/t2_preflight.sh        (Wave A+B: env/args, IMM-4 empty-target guard,
                                  SHA-256 checksum, manifest.json)
  scripts/t2_dispatch.sh         (Wave C: single reviewer curl + 5xx retry / 4xx
                                  no-retry / timeout; always exits 0 — status in
                                  .meta.json so siblings never abort, AC-1.7)
  scripts/t2_normalize.py        (Wave D+E: .raw → §4 template .md, IMM-5 status,
                                  IMM-6 atomic+idempotent write, write-on-failure
                                  return-contract.yaml with literal --suspect-source)
  refs/output-template.md
  refs/prompts.md                (system+user with <<<TARGET>>> injection guard §11.5)

Phase 1 acceptance gate (AC-1.1..AC-1.12 incl. IMM-3/4/5/6) verified by manual
drives against /tmp fixtures. Committed tests deferred to Phase 4 per plan.

## What you're building (Phase 1.5)

The standalone c7-enrichment skill (Variant B from the adversarial debate) + its
integration into sc-bare-review Wave B.5 + three spec-gap fixes. Full task
breakdown is in tasklist/phase-1.5.md (8 tasks: T-1.5.1 through T-1.5.8).

The proposed SKILL.md is ALREADY DRAFTED at
.dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/proposed-c7-enrichment-SKILL.md
(321 lines, used as the house-style template for the Phase 1 sc-bare-review SKILL.md).
T-1.5.1 is largely a copy to src/superclaude/skills/c7-enrichment/SKILL.md with
path/reference adjustments.

Estimated effort: ~430 LOC new + ~50 LOC modified. Compliance tier STANDARD.

## READ THESE FIRST — in this order

1. tasklist/phase-1.5.md — Per-task breakdown, ACs, risks. Your work order.
2. proposed-c7-enrichment-SKILL.md — The drafted SKILL.md (T-1.5.1 source).
3. merged-requirements.md §18 (the v1.2 amendment, lines ~1050+) — canonical spec
   for c7-enrichment. AC-1.24..AC-1.32 are in §18.8.
4. reflect-validation-2026-05-28.md — Documents the three spec gaps (SG-A/B/C):
   - SG-A: --libs flag semantics (skips vs augments auto-detect)
   - SG-B: failure_stage field missing from §18.5 return contract
   - SG-C: AC-1.32 metrics ownership (skill vs caller vs shim)
5. src/superclaude/skills/sc-bare-review/SKILL.md — Phase 1's house-style example
   for a thin-orchestrator-over-scripts skill. Note its frontmatter, section
   ordering, and how it documents scripts/ delegation.
6. src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py — Phase 1's
   write-on-failure / atomic-write / contract-emit precedent that c7-enrichment
   should mirror for its own return contract.

## Decisions already made (do NOT re-litigate)

- Variant B from adversarial debate (standalone skill, NOT an agent, NOT inlined
  into sc-bare-review). See adversarial/c7-agent-debate.md if needed.
- Delegate-only — no /sc:c7-enrichment slash command. Pure infrastructure.
- Lens taxonomy = 6 named lenses + custom. Full lens→queries map lives in
  src/superclaude/skills/c7-enrichment/refs/lens-queries.md (T-1.5.2 builds this).
- sc-bare-review uses --challenge-label="code-review" as its fixed lens (T-1.5.4).
- Spec-gap resolutions:
  - SG-A: --libs SKIPS auto-detect entirely (use list verbatim). Add AC-1.33.
  - SG-B: failure_stage added to return contract. Values: null | library_detection |
    id_resolution | doc_fetch | auggie_indexing | synthesis.
  - SG-C: caller-side shim owns metrics (NOT the skill). Add AC-1.34. Document the
    minimal metric-event JSON schema for callers.
  All three can be addressed inline AND documented as v1.4 spec amendment notes in
  commit messages. Do NOT block on a v1.4 spec re-write first.

## Architecture suggestion (consistent with Phase 1)

Phase 1 used "helper scripts + thin SKILL.md" successfully. c7-enrichment is
different: it's primarily MCP orchestration (context7 resolve-library-id +
query-docs + auggie codebase-retrieval), with very little shell to factor out.
That likely means MOSTLY a prose SKILL.md with one Python helper (synthesis
assembly + return-contract emit + frontmatter parsing). Get user sign-off via
EnterPlanMode before committing to a structure — Phase 1's plan-mode pattern is
in /config/.claude/plans/refactored-dancing-ullman.md if you want a template.

## Test scope (consistent with Phase 1 decision)

Committed tests deferred to Phase 4. Phase 1.5 ships skill + integration + manual
verification drives. AC-1.31 (caller-agnostic) per T-1.5.8 is the one place the
spec asks for an integration fixture *in this phase* — implement it as a manual
drive against /tmp now, formalize it into tests/skills/ in Phase 4. Confirm this
matches user preference before deviating.

## Prerequisites already in place

- T2ProxyUrl / T2ProxyKey / T2Model01..04 env vars are in ~/.aienv (source it if
  needed; the Phase 1 manual drives needed these only nominally — c7-enrichment
  doesn't need them at all since it hits context7+auggie MCPs, not the T2 proxy).
- mcp__context7__resolve-library-id, mcp__context7__query-docs, and
  mcp__auggie__codebase-retrieval are available in the MCP server registry.
- make sync-dev + make verify-sync are clean as of HEAD.
- The pre-commit hooks (markdownlint, shellcheck, ruff, secret-scan, "block
  generated .claude mirror commits") all fire. Phase 1 lessons:
    * MD040: every fenced code block needs a language tag (use `text` for prompts
      or `bash`/`yaml`/`python`/`markdown` as appropriate).
    * Never `git add .claude/<anything-but-settings.json>`. The .claude/ mirror
      is sync-dev output; commit only src/ paths. Hook will block -f attempts too.
    * Conventional commits, Co-Authored-By Claude trailer.
- PR target (if you open one): IronbellyOrg/IronClaude. Never upstream. The
  --repo IronbellyOrg/IronClaude flag is mandatory on every gh pr create.

## Done definition for Phase 1.5

- src/superclaude/skills/c7-enrichment/{SKILL.md, refs/lens-queries.md} authored.
- sc-bare-review/SKILL.md modified to delegate Wave B.5 to Skill c7-enrichment.
- AC-1.24..AC-1.32 + AC-1.33 (SG-A) + AC-1.34 (SG-C) + return-contract
  failure_stage (SG-B) all addressed inline in the new SKILL.md.
- make sync-dev + make verify-sync clean.
- Pre-commit hooks pass.
- Phase 1.5 work committed to brainstorm/t2-bare-reviewer-adjunct with a
  conventional-commit message naming the ACs covered and noting the SG-A/B/C
  resolution decisions for the v1.4 amendment trail.

Start by reading the 6 files listed above in order, then EnterPlanMode and present
a structured plan (decisions to confirm: skill architecture, test scope, whether
to do v1.4 spec amendment inline vs. just commit-message notes). Confirm with the
user via AskUserQuestion if any of the three "already made" decisions feel wrong.
```
