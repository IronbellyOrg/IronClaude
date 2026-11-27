d3882935c4821173ac0f11327bd180eb9bb2e1bb
family page-recipe-not-possible
defect form: the page tells the operator to do something the script has no option for
command: grep -n -i -E "leave|omit|skip|without|only the|option" docs/developer-guide/branch-protection-multi-repo.md
before: lines 48 (leave the tag ruleset out) and 96 (a same-name ruleset is skipped, which is real: apply_org_rulesets.py:781).
coupled sites: line 48 (step 4), the canary paragraph (a repo whose workflows move tags), line 96.
family page-digest-overclaim
defect form: the page says the digest changes with something it does not hash
command: grep -n -i -E "digest|changed repo|recomput|reads everything" docs/developer-guide/branch-protection-multi-repo.md
before: lines 3, 12, 13, 47, 49, 52, 55 (a changed repo makes the digest differ), 91 (for the current rules and repo).
coupled sites: lines 55 and 91; lines 12, 13, 47 and 49 only say the digest is printed and repeated.
after:
--- fam1
48:4. **Check the release workflows by hand.** The tag ruleset blocks moving and deleting `v*` tags, with no b
96:A ruleset of the same name that already exists is skipped with a printed line; it is never edited. A failed
--- fam2
3:How to put the three rulesets of [Branch Protection](branch-protection.md) (`.github/rulesets/protect-master
12:- in a dry run (no `--apply`), prints all of that, the rulesets it would create in order, a digest of them,
13:- with `--apply --confirm <digest>`, saves the repo's before state to `<repo>-before.json`, creates the rul
47:   Read all of it: the repo facts, the push check per branch (`pass`, `blocked` or `incomplete`, with how m
49:5. **Apply**, with the digest the dry run printed:
52:   uv run python scripts/apply_org_rulesets.py --org "$OWNER" --repo "$REPO" --out "$OUT" --apply --confirm
55:   The script reads the repo again before it writes and recomputes the digest of the rendered rule bodies, 
91:| `confirm digest does not match the rulesets rendered now` | The digest is not the one the dry run printed
