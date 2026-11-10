1fd69f04fe7dc34cd2fc82e8c5f168276f3cda7a
A1 r1-1 F1.3 minor src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py:497 ac=scope n,n,n,n init checks the ledger folder before taking the lock and does not re-check after it (two concurrent init runs).
A1 r1-1 F1.4 minor src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py:780 ac=scope n,n,n,n close commits ledger.json before appending the tail; a crash between leaves no tail and a replay does not re-append it.
A1 r1-1 F1.5 minor .dev/tasks/to-do/TASK-WF-spec-20261108-181649/artifacts/untracked-before.txt:59 ac=scope n,n,n,n the baseline lists its own file (created by the shell redirect before git status ran); Task 12 excludes .dev/tasks/ anyway.
