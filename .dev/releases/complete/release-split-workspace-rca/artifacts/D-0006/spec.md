# D-0006 — Wire detection gate into quick-check.yml

**Task:** T02.03
**Roadmap Item:** R-006
**FR Source:** FR-L2.2
**Closes:** INV-002 (HIGH-severity unaddressed invariant)

## Scope

Convert the existing-but-dormant misplacement detection logic (from T02.01 + T02.02) into an enforcing CI gate. PRs that introduce a `.claude/skills/<X>-workspace/` directory without `SKILL.md` must fail the workflow before merge.

## Deliverable

Two added steps in `.github/workflows/quick-check.yml`, placed after `Verify pytest plugin` and before `Summary`:

```yaml
      - name: Verify component sync (src/ ↔ .claude/)
        run: |
          make verify-sync

      - name: Lint architecture policy
        run: |
          make lint-architecture
```

The Summary step is updated to enumerate the two new checks.

## Behaviour Contract

- Non-zero exit from either `make verify-sync` or `make lint-architecture` causes the GitHub Actions step to fail. Default step semantics (no `continue-on-error`) propagate that failure to the job and workflow.
- A failing required workflow blocks merge under standard branch-protection policy (admin-scoped; see `notes.md`).

## Out of Scope

- Branch-protection / required-check configuration (repo-admin scoped).
- Resolving 3 pre-existing `lint-architecture` errors unrelated to workspace misplacement (recorded in `notes.md` as a Phase-2 follow-up; they pre-date this task).
