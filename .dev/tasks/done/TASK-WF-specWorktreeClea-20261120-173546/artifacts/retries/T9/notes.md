bcbec7b3496ae617b63e13242967471cef806251
A1 r1-2 observation scripts/worktree_cleanup.py:2053 ac=T9.AC2 n,n,n,n sync_evidence_clone can raise OSError (for example RUN_EVIDENCE_DIR is a regular file); it raises before anything is saved or deleted; the verbs of Task 11 must catch it per worktree and keep the worktree
