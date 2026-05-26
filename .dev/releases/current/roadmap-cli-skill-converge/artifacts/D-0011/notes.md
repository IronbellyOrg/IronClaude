# D-0011 — Notes: Authorization scope and tier routing

## Authorization scope

T05.01 is a **mechanical sync-and-verify** task. It applies one repeatable command sequence and records the result. No source edits, no design decisions, no `.claude/` hand-edits.

### Authorized actions

1. `make sync-dev` — regenerates `.claude/{skills,agents,commands,hooks,templates}/` from `src/superclaude/`.
2. `cp src/superclaude/commands/roadmap.md /config/.claude/commands/sc/roadmap.md` — manual global refresh per `release-scope.md:193`.
3. `cp src/superclaude/commands/validate-roadmap.md /config/.claude/commands/sc/validate-roadmap.md` — same, for the second command file.
4. `make verify-sync` — confirms src ↔ `.claude/` parity.
5. `md5sum` against all six paths to record three-way parity.
6. `uv run superclaude roadmap run <sample-spec> --dry-run` — lightweight regression for `/sc:roadmap` slash-command (which delegates to this CLI).
7. `uv run superclaude roadmap validate --help` plus `uv run pytest tests/roadmap/test_validate_cli.py tests/roadmap/test_cli_contract.py tests/roadmap/test_integration_contracts.py` — regression for `/sc:validate-roadmap` slash-command and the integration-contracts wiring that Phase 1 (B-1, B-2) touched.

### NOT authorized

- Staging or committing any `.claude/{skills,commands,agents,hooks,templates}/*` path. Per CLAUDE.md "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents", these are gitignored sync-dev output. Phase 5 produces the `.claude/` regen as a side effect of `make sync-dev`; it is consumed by Claude Code at read-time and **never** added to a commit. If `git add` requires `-f` on any `.claude/` path, that is the violation siren.
- Editing `/config/.claude/commands/sc/{roadmap,validate-roadmap}.md` by hand. Global refresh is byte-copy from `src/superclaude/commands/`; any divergence indicates a procedure violation, not a legitimate edit.
- Re-running any Phase 1–4 task. T05.01 verifies state, it does not re-derive it.

## Tier routing

T05.01 is tier **STANDARD** (per `phase-5-tasklist.md:14`). The STANDARD checks for a mechanical sync task are:

1. **Direct test execution** — `make verify-sync` is itself the unit-level direct test; the pytest regression suite (`test_validate_cli.py`, `test_cli_contract.py`, `test_integration_contracts.py`) is the integration-level direct test.
2. **Evidence captured in `evidence.md`** — verbatim command outputs, including the md5sum lines, the verify-sync success banner, and the pytest pass counts.
3. **No sub-agent delegation** — task definition `phase-5-tasklist.md:21` sets `Sub-Agent Delegation: None`.

## Relationship to B-1, B-2, B-3 through B-8, B-9, B-10

Phase 5 is the closeout for the source edits made in earlier phases:

- **B-1, B-2** (Phase 1, T01.01–T01.03, D-0002 / D-0003 / D-0004) — `src/superclaude/commands/roadmap.md` and `src/superclaude/commands/validate-roadmap.md` were re-aligned to the CLI flag set.
- **B-3 … B-8** (Phase 2, T02.01–T02.06, D-0005 … D-0008) — `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` and `refs/*.md` were re-aligned to the CLI pipeline. **Skill files are synced by `make sync-dev` but not re-copied to `/config/.claude/skills/` here** — `verification.md:193-205` REFUTED the B-11 "global-install gap" claim by demonstrating both skills are already byte-identical at `/config/.claude/skills/`. Phase 5 deliberately leaves the global skill copies untouched and instead relies on `make sync-dev` parity to keep `src/` ↔ `.claude/` aligned.
- **B-9** (Phase 3, T03.01, D-0009) — `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` got the Relationship-to-CLI header + crosswalk. Same sync semantics as B-3…B-8.
- **B-10** (Phase 4, T04.01, D-0010) — Packaging deferral, no source edits. Phase 4 is a no-op for sync.

## Why this matters

B-12's drift claim (`release-scope.md:181-194`) is mechanical: once Phase 1 and Phase 2 land source-side edits, the three locations carrying `roadmap.md` and `validate-roadmap.md` will diverge until the sync sequence runs. T05.01 is the explicit gate that closes that drift before the release ships.

## Cross-references

- `release-scope.md:181-194` — B-12 definition and update procedure.
- `release-scope.md:198-207` — Release acceptance criteria 2, 3, 4.
- `verification.md:32` — B-12 status: VERIFIED.
- `verification.md:193-228` — B-11 REFUTED; global skill copies are already in sync.
- `CLAUDE.md` — "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents".
