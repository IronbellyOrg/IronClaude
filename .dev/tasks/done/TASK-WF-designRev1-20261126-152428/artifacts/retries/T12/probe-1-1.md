2a7b88e58a97f880e9155f3d02db7a78807d56e3
## Family break-glass-order (review r1-1, finding F1.1)
defect form: revert and break-glass commands run in one block in the wrong order (DELETE before the PUT calls)
command: grep -n -F -e 'enforcement=disabled' -e 'enforcement=active' -e '--method DELETE' -- .dev/issues/837/handoff-ryan.md
before:
  75:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  86:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  87:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  89:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  160:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  171:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  172:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  174:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  245:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  256:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  257:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  259:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
coupled sites: the Revert and break glass block in each of the three repo sections and the scratch self-test DELETE

## Family id-undefined (review r1-1, finding F1.2)
defect form: a command uses $ID that no block sets
command: grep -n -F -e '$ID' -e 'ID=' -- .dev/issues/837/handoff-ryan.md
before:
  62:gh api repos/IronbellyOrg/$REPO/rulesets/$ID
  65:The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full role. Compa
  75:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  82:Revert and break glass (the same commands as the IronClaude guide, with `$REPO` and `$ID`):
  86:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  87:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  89:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  98:What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `rules/branch
  147:gh api repos/IronbellyOrg/$REPO/rulesets/$ID
  150:The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full role. Comp
  160:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  167:Revert and break glass (the same commands as the IronClaude guide, with `$REPO` and `$ID`):
  171:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  172:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  174:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  183:What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `rules/branc
  232:gh api repos/IronbellyOrg/$REPO/rulesets/$ID
  235:The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full role. Comp
  245:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  252:Revert and break glass (the same commands as the IronClaude guide, with `$REPO` and `$ID`):
  256:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  257:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  259:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  268:What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `rules/branc
coupled sites: the apply read-back, the scratch self-test DELETE, the revert and break-glass block of each repo section

## Family irondots-tag-token (review r1-1, finding F2.1)
defect form: an unqualified safe-to-apply statement where the audit marks the workflow token behaviour UNVERIFIED
command: grep -n -F -e 'safe to apply' -e 'nothing to break' -- .dev/issues/837/handoff-ryan.md
before:
  179:No `v*` tag exists (0 `v*` refs, no tag of any name). Its workflow `.github/workflows/gated-release.yml` only crea
  264:No `v*` tag exists (0 `v*` refs, no tag of any name) and the repository has no workflow at all (HTTP 404 on the wo
coupled sites: the tag ruleset section of irondots only (ironops-marketplace and IronHands-CLI sections have their own text)
after:
 family break-glass-order:
  77:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  89:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  91:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  99:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  172:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  184:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  186:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  194:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  267:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  279:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  281:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  289:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
 family id-undefined:
  55:ID=<id printed by the create call of the ruleset you are reading back>
  63:gh api repos/IronbellyOrg/$REPO/rulesets/$ID
  66:The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full r
  72:ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
  77:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  84:Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, w
  88:ID=<id of the ruleset you apply this to>
  89:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  91:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  98:ID=<id of the ruleset to delete>
  99:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  108:What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `r
  151:ID=<id printed by the create call of the ruleset you are reading back>
  158:gh api repos/IronbellyOrg/$REPO/rulesets/$ID
  161:The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full 
  167:ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
  172:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  179:Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, 
  183:ID=<id of the ruleset you apply this to>
  184:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  186:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  193:ID=<id of the ruleset to delete>
  194:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  203:What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `r
  246:ID=<id printed by the create call of the ruleset you are reading back>
  253:gh api repos/IronbellyOrg/$REPO/rulesets/$ID
  256:The read-back of the branch types prints `deletion`, `non_fast_forward` and `pull_request` for the full 
  262:ID=<id of the zz-selftest- ruleset printed by the scratch create call below>
  267:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  274:Break glass (only for an emergency that needs a direct push; the same commands as the IronClaude guide, 
  278:ID=<id of the ruleset you apply this to>
  279:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=disabled
  281:gh api --method PUT repos/IronbellyOrg/$REPO/rulesets/$ID -f enforcement=active
  288:ID=<id of the ruleset to delete>
  289:gh api --method DELETE repos/IronbellyOrg/$REPO/rulesets/$ID
  298:What to report back as a comment on issue 837: the ruleset ids and the dates, the read-back output of `r
 family irondots-tag-token:
  294:No `v*` tag exists (0 `v*` refs, no tag of any name) and the repository has no workflow at all (HTTP 404
