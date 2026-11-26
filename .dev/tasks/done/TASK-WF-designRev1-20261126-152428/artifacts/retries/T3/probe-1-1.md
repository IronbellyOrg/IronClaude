8441a5c96b07c29ffc1fb2e0fce87fe081660444
## Family selftest-recipe (review r1-1, finding F1.1)
defect form: a recipe block that does not contain the step its text says produces the refusal
command: grep -n -F -e 'zz-ruleset-selftest' -e 'GH013' -e 'force push' -- docs/developer-guide/branch-protection.md
before:
  13:- Nobody can push straight to `master` or `integration`, force push over them or delete them. Every change arrives through a pull request, which a person or an automation may merge (zero approvals are required).
  49:The two branch checks must each print `deletion`, `non_fast_forward` and `pull_request`. Do not test a ruleset by pushing to, force pushing or deleting a real `master`, `integration` or release tag. To see a refusal, create a scratch ruleset on a throwaway branch name (for example `refs/heads/zz-ruleset-selftest`) with the same rules and push to that branch; delete the ruleset and the branch afterwards.
  161:Before the first real create, test the role on a throwaway branch of the target repo, from a scratch clone (never from IronClaude): create the branch `zz-ruleset-selftest` with two commits, create a scratch ruleset from the role file, check that a push is refused, then delete the ruleset and the branch.
  164:jq '.name="zz-selftest-<role>" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' <file> | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
  165:git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
  167:git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
  171:The full role must refuse an empty commit pushed to the branch (error GH013); the mirror must refuse a force push of the earlier commit. The last command must show no name that starts with `zz-selftest-`. The answer of the scratch create also settles whether the mirror's bypass actor is accepted. If the API refuses it, drop the bypass actor from `protect-main-mirror.json` and change the file, the test and this page together before anything is applied.
coupled sites: the Self-test intro line (161), the self-test code block (163-169), the sentence that names the expected refusals (171); the Check/Apply sections do not state the refusals
8441a5c96b07c29ffc1fb2e0fce87fe081660444
after:
  13:- Nobody can push straight to `master` or `integration`, force push over them or delete them. Every change arrives through a pull request, which a person or an automation may merge (zero approvals are required).
  49:The two branch checks must each print `deletion`, `non_fast_forward` and `pull_request`. Do not test a ruleset by pushing to, force pushing or deleting a real `master`, `integration` or release tag. To see a refusal, create a scratch ruleset on a throwaway branch name (for example `refs/heads/zz-ruleset-selftest`) with the same rules and push to that branch; delete the ruleset and the branch afterwards.
  161:Before the first real create, test the role on a throwaway branch of the target repo, from a scratch clone (never from IronClaude): create the branch `zz-ruleset-selftest` with two commits, create a scratch ruleset from the role file, check that a push is refused, then delete the ruleset and the branch.
  165:git push https://github.com/IronbellyOrg/$REPO.git HEAD:refs/heads/zz-ruleset-selftest
  166:jq '.name="zz-selftest-<role>" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' <file> | gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input -
  167:# full role: an empty commit on top must be refused (error GH013)
  169:git push https://github.com/IronbellyOrg/$REPO.git HEAD:zz-ruleset-selftest
  170:# mirror: rewinding the branch by one commit (a force push) must be refused
  171:git push --force https://github.com/IronbellyOrg/$REPO.git HEAD~1:zz-ruleset-selftest
  173:git push https://github.com/IronbellyOrg/$REPO.git --delete zz-ruleset-selftest
  177:Run the empty-commit push for the full role and the force push for the mirror (the mirror skips the empty commit, so the force push rewinds a branch that holds both commits). The full role must refuse the empty commit pushed to the branch (error GH013); the mirror must refuse the force push of the earlier commit. The last command must show no name that starts with `zz-selftest-`. The answer of the scratch create also settles whether the mirror's bypass actor is accepted. If the API refuses it, drop the bypass actor from `protect-main-mirror.json` and change the file, the test and this page together before anything is applied.
