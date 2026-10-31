Repo: IronbellyOrg/Ironbrain. Context: IronClaude (issue IronbellyOrg/IronClaude#323) replaced codebase-memory with codegraph (https://github.com/colbymchenry/codegraph).
Do: PLANNING.md proposes codebase-memory for selective repository-local structural retrieval; update the proposal to name codegraph, or mark codebase-memory as retired. The inventory found no runtime integration.
Keep: the 8 historical research paths.
Verify: `git grep -n -i codebase-memory -- . ':!.dev' ':!claudedocs'`.
