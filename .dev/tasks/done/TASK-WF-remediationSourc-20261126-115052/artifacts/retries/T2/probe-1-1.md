7f9f65b5e32ef5e1d5a066a5c728ff8748128d5c
## family: evidence-after-worktree-ids
defect form: the after reading of this repository's worktree ids is reduced to a count
command: grep -n -F -e 'e8e07d51-c261-4936-815e-06aeceeb5bf8::' ./artifacts/t2-after.txt
before-output (touched files: ./artifacts/t2-after.txt, plus the AC-named ./artifacts/t1-before.txt): 2 matching lines in t2-after.txt; 32 in t1-before.txt
coupled sites: ./artifacts/t2-after.txt:30 (claim every id is still listed); ./artifacts/t2-outcome.md:3 (worktrees preserved: yes (32 of 32)); Task 4 note copies the count only
after: 34 matching lines in t2-after.txt (the 32 ids and the comparison sentence)
