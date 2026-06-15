# G1 Approval Request — Troubleshoot Pipeline Hardening

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`

Status: awaiting human approval. No shared skill or command files have been edited for this G1 draft.

## Decision requested

Approve implementation of the troubleshoot pipeline hardening spec:

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md`

The requested implementation will harden `/sc:troubleshoot` and `sc:troubleshoot-protocol` with mechanism-based closure controls for pipeline escapes:

1. Runtime-entrypoint verification gate.
2. Contract-enumeration wave.
3. Unmask-and-sweep regression wave.
4. Effective-input proof for generated review/audit gates.
5. Off-path-reviewer rule for high-risk boundaries.

## Why this is needed

The frozen G0 escape set shows a repeated pattern: prior assurance artifacts often proved adjacent surfaces instead of the runtime contract that failed.

- E1: PRD `--file` misuse escaped because helper/argv proof did not exercise the headless Claude subprocess contract and sibling file-delivery contracts were not compared.
- E2: completion-phase false positive escaped because the parser/gate was not verified against generated artifact topology.
- E3: Task Log findings-heading false positive escaped because the first fix did not unmask-and-sweep sibling phase-like headings in the whole artifact.
- E4: PRD/generic/trailing evaluator divergence escaped because a shared advisory contract was validated on one evaluator while the real PRD runtime used another.
- E5: POST-reflect wrong diff base escaped because independent review existed but did not prove its effective input matched dirty `/task` work and excluded foreign commits.

The proposed hardening catches E1..E5, and future E6..En in the same family, by requiring issue-agnostic proof at runtime boundaries, contract consumers, classifier edges, sweep surfaces, and review-input selectors.

## Files likely to be edited after approval

Source-of-truth edits only:

- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`

Likely new ref/template files:

- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md`

Potential validation edits if tests need updates or coverage exists for command/skill metadata:

- `/config/workspace/IronClaude/tests/`

Potential docs edits only if implementation review determines user-facing docs must mirror command behavior:

- `/config/workspace/IronClaude/docs/`

After any source edits, run:

```bash
make sync-dev
make verify-sync
```

Do not stage `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates`; those are sync-dev output. Only `.claude/settings.json` is stageable if explicitly changed, which this plan does not require.

## Explicit halt before shared edits

This G1 package intentionally stops before editing:

- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- any `.claude/` generated command/skill mirror

Approval is required before implementation begins.

## Implementation risks

| Risk | Impact | Mitigation |
|---|---|---|
| Protocol bloat in main `SKILL.md` | Troubleshoot becomes harder to read and maintain. | Put detailed cards in refs and keep the main skill to trigger/wave wiring. |
| Over-gating simple bug reports | Tier 1 quick diagnosis could become slower or more ceremonial. | Trigger pipeline-hardening mode only for runtime boundaries, generated artifacts, gates, parsers, shared contracts, selectors, or prior escapes. Pure local bugs should record `not_applicable`. |
| False sense of safety from checklists | The same theatre problem could recur if cards are filled without evidence. | Require machine-checkable or cited evidence, negative controls, and `NOT PROVEN` blockers for missing proof. |
| Over-broad off-path review requirement | Every change could demand heavy adversarial review. | Use off-path review only when the boundary is high-risk or local proof does not execute it; allow waiver with evidence. |
| Source-of-truth drift | Editing `.claude/` directly would create sync drift and forbidden staged files. | Edit only `src/superclaude/`, then `make sync-dev` and `make verify-sync`; never stage generated `.claude/` mirrors. |
| Tests may not cover markdown-only protocol changes | Implementation could pass sync but regress command semantics. | Add targeted tests if existing test surfaces parse command/skill metadata or if a lightweight fixture can validate required protocol sections. |
| Gating language conflicts with existing Tier 1/Tier 2 flow | Pipeline-hardening mode could be ambiguously ordered. | Insert after diagnosis/remediation classification and before closure/report finalization, with clear H0-H5 wave names. |

## Scope boundaries

In scope after approval:

- Protocol and template hardening for `/sc:troubleshoot` and `sc:troubleshoot-protocol`.
- Source-of-truth skill/command edits under `src/superclaude/`.
- New refs/templates for hardening cards.
- Targeted tests or docs only if necessary for validation.

Out of scope unless separately approved:

- Product-code fixes for PRD, reflect, task-builder, or gates.
- Broad redesign of the troubleshoot architecture.
- Mandatory heavyweight e2e for every troubleshoot run.
- Edits directly under `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates`.
- Commit or PR creation.

## Approval criteria

Approve if the desired next phase is to implement the spec in source-of-truth protocol files.

Reject or request revision if:

- the hardening should live in another skill such as task-builder instead of troubleshoot;
- off-path review should be advisory-only;
- effective-input proof should be limited to reflect/review gates;
- new refs/templates should be consolidated into fewer files;
- tests/docs should be mandatory in the first implementation pass.

## Paste-ready next prompt

Single-line prompt to approve and start implementation:

```text
Approved G1. Implement /config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md in source-of-truth files only. Do not edit .claude mirrors directly. After edits, run make sync-dev and make verify-sync, then report changed files and any tests run. Do not commit.
```

## Current G1 artifacts

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md`
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/G1-APPROVAL-REQUEST.md`
