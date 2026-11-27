350491022cacf81329f71e46bdaadd2a48c23ca6
## Family write-command-in-record (review r1-1, finding F1.1)
defect form: a write command (POST, PUT, PATCH, DELETE) listed in a Ryan-repo audit record that the AC says holds none
command: grep -n -E -e '--method (POST|PUT|PATCH|DELETE)' -e '-X (POST|PUT|PATCH|DELETE)' -- .dev/issues/837/audit/IronHands-CLI.md
before:
  82:| `bump-version.yml` (187 lines; `workflow_dispatch`; permissions `contents: read`) | `git push origin "$BRANCH_NAME"` | Read. It pushe
  83:| `bump-agent-sdk-version.yml` (151 lines; `workflow_dispatch`; `contents: read`) | `git push origin "$BRANCH_NAME"` | Read. It pushes 
  84:| `update-install-website.yml` (135 lines; `release: published` or `workflow_dispatch`; `contents: read`) | `git push origin "$BRANCH_N
  146:| `protect-main` (full role) | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronHands-CLI` | |
  147:| `protect-main-mirror` (mirror role, only if the rule above allows it on apply day) | `gh api --method DELETE repos/IronbellyOrg/$REP
  148:| `protect-release-tags` | `gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/<id>` with `REPO=IronHands-CLI` | |
coupled sites: the Revert commands section (140-148) and the text that says nothing was written (3, 156); the sentence at 142 that says the revert lines are written before any write
after:
  82:| `bump-version.yml` (187 lines; `workflow_dispatch`; permissions `contents: read`) | `git push origin "$BRANCH_NAME"` | Read. It pushe
  83:| `bump-agent-sdk-version.yml` (151 lines; `workflow_dispatch`; `contents: read`) | `git push origin "$BRANCH_NAME"` | Read. It pushes 
  84:| `update-install-website.yml` (135 lines; `release: published` or `workflow_dispatch`; `contents: read`) | `git push origin "$BRANCH_N
