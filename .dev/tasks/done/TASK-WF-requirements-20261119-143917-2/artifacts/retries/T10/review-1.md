4ae82798c25abbfd4f726e36c1f674f43fa00bfd
tree=none
Reconstructed after context compaction: the original review text was not saved; these lines record the blocking families it raised and that the fix pass addressed.
F1.1 ac=T10.AC1 at=docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1074 anchor="grep -rn -- \"--pipeline none\" src tests docs plugins has no hit that still presents it as the only watcher prompt" chk=y,n,n,y family=stale-fixed-prompt fix=reword every sentence that presents `--pipeline none` as the only watcher prompt sev=blocking trigger=B4 first=start origin=new: tech reference lines 1074 and 1416 still gave the old fixed pattern
F1.2 ac=T10.AC1 at=src/superclaude/core/WORKER-CONTRACT.md:293 anchor="no hit that still presents it as the only watcher prompt" chk=y,n,n,y family=stale-fixed-prompt fix=cover a claim at any level sev=blocking trigger=B4 first=start origin=new: coordinator duties said they apply only to a `--pipeline none` claim
