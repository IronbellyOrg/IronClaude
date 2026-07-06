# BUILD_REQUEST — Remediate PR #197 review findings

GOAL: Build an MDTM task file that remediates the findings in
`.dev/reviews/pr-197-20260620223934/REVIEW.md`, following the remediation specification at
`.dev/reviews/pr-197-20260620223934/remediation-spec.md`.

WHY: `/sc:auggie-review --depth deep` on PR #197 (IronbellyOrg/IronClaude, branch
`feat/rf-harness-sync`) surfaced 2 HIGH findings that block merge (R1: an inverted Tavily
MCP tool-id rename that silently breaks the Tavily-first protocol in 8 agents; R2: an
unvalidated default POST-reflect path shipped on an unproven "confirmed" assertion with no
in-file disclosure) plus medium/low fixes. This task file translates the remediation spec's
requirements R1–R5 into evidence-backed, executable steps.

WHERE (files cited in the review's HIGH/MEDIUM/LOW sections):
- `src/superclaude/agents/rf-analyst.md`, `rf-assembler.md`, `rf-qa.md`,
  `rf-qa-qualitative.md`, `rf-task-builder.md`, `rf-task-executor.md`,
  `rf-task-researcher.md`, `rf-team-lead.md` (R1)
- `src/superclaude/skills/task-builder/SKILL.md` (R2, R4, R5)
- `src/superclaude/cli/reflect/runner.py` + `tests/cli/reflect/` (R3)

SCOPE / CONSTRAINTS:
- Apply on branch `feat/rf-harness-sync` in an isolated worktree
  (`git worktree add .dev/worktrees/pr197-remediation feat/rf-harness-sync`); never on master,
  never share the index with another session.
- Source-of-truth: edit `src/superclaude/…` only, then `make sync-dev` + `make verify-sync`.
  NEVER stage any `.claude/` path.
- Python items: `uv run ruff format --check src/ tests/` before done (CI runs it separately);
  tests via `uv run pytest tests/cli/reflect/ -v`.
- R6 (pre-existing reflection-rubric line citations) is OUT OF SCOPE — do not include as work.

HUMAN-DECISION GATE (MANDATORY HALT — do NOT auto-default):
- HD-1 (spec R2b): the default-mode resolution for the unvalidated skill POST path
  (keep+cite validating run / invert to --cli default / mark EXPERIMENTAL) is RyanW's design
  decision. The built task MUST emit a `needs_human_decision` item that writes a PENDING record
  and HALTS the default-inversion; it MUST NOT flip the `--cli` default or edit O4 floors on its
  own. The always-safe disclosure (R2a) IS applied unconditionally; only the inversion question
  halts.

OUTPUT: MDTM task file under `.dev/tasks/`.

TEMPLATE: project standard MDTM template.

BUILD_REQUEST file: .dev/reviews/pr-197-20260620223934/BUILD-REQUEST-REMEDIATION.md
