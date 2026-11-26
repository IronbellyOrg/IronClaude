d3882935c4821173ac0f11327bd180eb9bb2e1bb
family page-digest-overclaim
defect form: the page says a digest mismatch is refused for any digest other than the printed one, but the script compares only with the digest of the bodies it renders at apply time (the same for any repo with the same branch set)
command: grep -n -i -E "digest|rendered" docs/developer-guide/branch-protection-multi-repo.md
before: lines 3, 7, 41, 44, 47 (A digest that is not the one the dry run printed gives ...), 87 (table row), 97, 118.
coupled sites: line 47 (the claim), line 41 (heading says the digest the dry run printed: an instruction), line 87 (the row tells the operator to rerun the dry run and use its digest: an instruction); lines 3, 7, 44, 97 and 118 only name the digest or the option.
after:
--- page-digest-overclaim
3:How to put the rulesets of [Branch Protection](branch-protection.md) on another repo of an organization, one repo per 
7:The script checks one repo and prints a dry run that writes nothing. With `--apply --confirm <digest>` and `--out` it 
41:5. **Apply**, with the digest the dry run printed:
44:   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm <digest>
47:   A digest that differs from the digest of the rulesets rendered at apply time gives `confirm digest does not match 
87:| `confirm digest does not match the rulesets rendered now` | Rerun the dry run and use the digest it prints |
97:- `--apply needs --confirm DIGEST`
118:`<repo>-before.json` in `OUT` holds the keys `org`, `repo`, `saved_at`, `digest`, `rulesets` and `protection`. It is
