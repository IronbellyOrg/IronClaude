d729e5d2cd050384298ecc6b4cf02eb3e376f05f
family=new-claim
defect form: an added sentence in the Git Workflow section asserting a new fact
command: grep -n -F -e 2026-11-24 -- CLAUDE.md
before:
292:`integration` is the repository default branch (since 2026-11-24): feature branches are cut from it and pull requests are opened against it. `master` stays the production branch.
coupled sites: none other
after: grep -c 2026-11-24 CLAUDE.md -> 0
