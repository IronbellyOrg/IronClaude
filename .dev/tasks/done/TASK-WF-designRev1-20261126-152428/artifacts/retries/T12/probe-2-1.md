2a7b88e58a97f880e9155f3d02db7a78807d56e3
## Family selftest-path (review r2-1, finding F3.1)
defect form: a scratch-clone command reads a ruleset file by a path that exists only in an IronClaude checkout
command: grep -n -F -e 'other-repos/protect-main.json' -e 'scratch clone' -- .dev/issues/837/handoff-ryan.md
before:
  7:- Full role: https://github.com/IronbellyOrg/IronClaude/blob/<PUSHED-SHA>/.github/rulesets/other-repos/protect-main.json
  60:gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
  68:Scratch self-test before the first real create (from a scratch clone of this repository, never from IronClaude; the throwaway
  74:jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos/
  155:gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
  163:Scratch self-test before the first real create (from a scratch clone of this repository, never from IronClaude; the throwawa
  169:jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos
  250:gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
  258:Scratch self-test before the first real create (from a scratch clone of this repository, never from IronClaude; the throwawa
  264:jq '.name="zz-selftest-full" | .conditions.ref_name.include=["refs/heads/zz-ruleset-selftest"]' .github/rulesets/other-repos
coupled sites: the self-test block and its introducing sentence in each of the three repo sections (the apply block reads the same relative path from an IronClaude checkout, which its first comment says)
after:
  7:- Full role: https://github.com/IronbellyOrg/IronClaude/blob/<PUSHED-SHA>/.github/rulesets/other-repos/protect-main.json
  60:gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
  68:Scratch self-test before the first real create (the git commands run in a scratch clone of this repository, never in an IronC
  73:RULESET_FILE=<absolute path of .github/rulesets/other-repos/protect-main.json in a separate checkout of IronClaude at the pus
  156:gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
  164:Scratch self-test before the first real create (the git commands run in a scratch clone of this repository, never in an Iron
  169:RULESET_FILE=<absolute path of .github/rulesets/other-repos/protect-main.json in a separate checkout of IronClaude at the pu
  252:gh api --method POST repos/IronbellyOrg/$REPO/rulesets --input .github/rulesets/other-repos/protect-main.json
  260:Scratch self-test before the first real create (the git commands run in a scratch clone of this repository, never in an Iron
  265:RULESET_FILE=<absolute path of .github/rulesets/other-repos/protect-main.json in a separate checkout of IronClaude at the pu
