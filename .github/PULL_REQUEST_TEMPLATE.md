# Pull Request

## Summary

<!-- Briefly explain the purpose of this PR -->

## Changes

<!-- List the major changes -->
-

## Related Issues

<!-- Include related issue numbers, if any -->
Closes #

## Skill, command or agent changes (not available yet)

New team members file an issue instead of opening a pull request that changes a skill, command or agent (see HOW-WE-WORK, section 4). The list shows what such a pull request will need once contribution opens; none of it can be met today.

Not applicable: this PR does not change a skill, command or agent.

- Linked proposal issue.
- Before-and-after evidence that the change adds value, not bloat.
- Known callers listed and rechecked, or "not known".
- Reviewer approval, given before the evaluation.
- CI evaluation passed at the ROI threshold: not available yet (metric, threshold and approving role not set).

## Checklist

### Git Workflow

- [ ] Opened with `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude` (fallback: `gh pr create --repo IronbellyOrg/IronClaude`).
- [ ] For collaborators: Used a topic branch (not directly committed to main).
- [ ] Branch rebased onto `origin/integration` (no conflicts).
- [ ] Commit messages conform to Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).

### Code Quality

- [ ] Changes are limited to a single purpose (not a large PR, guideline: ~200 lines of difference).
- [ ] Follows existing code conventions and patterns.
- [ ] Add appropriate tests for new features/fixes.
- [ ] Lint/Format/Typecheck all pass.
- [ ] CI/CD pipeline successful (green status).

### Security

- [ ] Secrets and authentication information not committed.
- [ ] Necessary files excluded with `.gitignore`.
- [ ] No breaking changes, or if there are, commit with `!` and include in MIGRATION.md.

### Documentation

- [ ] Update documentation as needed (README, CLAUDE.md, docs/, etc.).
- [ ] Add comments to complex logic.
- [ ] Properly document API changes.

## Testing Methods

<!-- How to verify this PR works -->

## Screenshots (if applicable)

<!-- Attach screenshots if there are UI changes -->

## Notes

<!-- What you want to communicate to reviewers, background to technical decisions, etc. -->
