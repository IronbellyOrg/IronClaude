# Reflect reviewer brief — reviewer 3

- spec_path: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/TASK-RF-ci-doctor-20260924-174137.md
- tasklist_path: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/TASK-RF-ci-doctor-20260924-174137.md
- related_contract: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/specs/ccsession-native-install.md (FR-1/FR-4 comparison only; NOT --spec)
- diff_scope: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/test-results/workflow.diff
- reviewer_grounding_root: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install
- persona_lens: refactorer
- output_path: /config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/reflect/post/reviewer-cards/reviewer-3-card.yaml
- Do not run pytest, git, or shell. Do not write files. Return structured findings only.

## T1 card excerpt

## Scope
One unstaged hunk in `.github/workflows/test.yml` inserts `Install native components` (`superclaude install`) between `Install dependencies` and `Run doctor command` in job `doctor-check`. Production doctor/install code is unchanged.

## Recommendation
Treat the one-step workflow insert as complete vs Step 2.1. Do not promote. Do not remediate production code. Escalate to Tier 2 because `--depth deep`.

## Grounding hunks

### .github/workflows/test.yml:195-228
```yaml
  doctor-check:
    name: SuperClaude Doctor Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
      - name: Set up Python
      - name: Install UV
      - name: Install dependencies
      - name: Install native components
        run: |
          superclaude install
      - name: Run doctor command
        run: |
          superclaude doctor --verbose

  test-summary:
    needs: [test, swarm-marker-matrix, lint, plugin-check, doctor-check, verify-deps]
```

### .dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/BUILD-REQUEST.md:11-19
GOAL: insert native install step only; keep other jobs and doctor implementation unchanged. EXECUTION_SCOPE: no commit/push.

### src/superclaude/cli/main.py:46-51
`superclaude install` installs core, commands, agents, skills (native components). CI now calls this before doctor.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| Only doctor-check YAML changes | covered | one hunk | workflow.diff |
| No doctor.py edits | covered | absent from diff | workflow.diff |
| Neighbor jobs intact | covered | test-summary needs unchanged | test.yml:225-228 |
