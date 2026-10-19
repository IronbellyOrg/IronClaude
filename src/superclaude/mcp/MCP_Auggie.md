# Auggie MCP Server

**Purpose**: Hosted Augment Code search over the repository's default branch, served by the LiteLLM MCP gateway. Prior art and conventions in merged code only.

## Shared contract

Every consumer of `mcp__auggie__augment_code_search` follows this section.

- Scope. `augment_code_search` answers one question: what exists on `<default-branch>`.
  Use it for prior art and conventions in merged code. Never use it to decide whether
  code on the working branch, or in uncommitted/untracked files, exists, changed, or
  behaves a certain way. Use Serena, Grep, or Read for those.
- A hit is a lead: Read the file on the working tree before acting on or citing it.
  A miss is never evidence of absence, on any branch.
- Repo and branch. Read `augment_repo=<owner>/<name>@<default-branch>` from `<session-context>`. If it is absent, derive `owner/name` from `git remote get-url origin` and the default branch from `git symbolic-ref --short refs/remotes/origin/HEAD` (minus `origin/`).
- Call `augment_code_search(repo_owner, repo_name, branch=<default-branch>, query)`, optional `max_results`. Always pass `branch` explicitly. Only the default branch (`master` here) is indexed; the gateway never falls back to it by itself.
- If `<session-context>` has `augment_unavailable=<reason>`, or the call returns `[BRANCH_NOT_FOUND]` or `[REPO_NOT_FOUND]`, say "Augment unavailable: <reason>" and continue with local tools (Grep, Read, Serena). No retries.
- No hosted Q&A or implement tool exists; use `augment_code_search`.
- Absence rule. A miss from Augment (default branch only), Serena (exact symbols only) or any index never proves absence. Before claiming something is missing, unimplemented, unused or uncalled, check the diff for a renamed equivalent, then Grep or Read the working tree and cite the pattern and root searched. Read every hit before citing it: a hit whose file or identifier is gone was deleted or renamed here.

### Routing

Never pass a path, directory, file:line, or symbol to `augment_code_search`, and never put one in `query`. It has no path filter and indexes only the default branch. If you cannot tell whether the target is on that branch, treat it as branch-local.

| Question | Tool (working tree) | Empty means |
|---|---|---|
| Literal or regex under a path | `Grep` with `path=<scope>`. `files_with_matches` first, then content, `head_limit` 50 | no hit **in that tree**. A cap is `unscanned: capped`, not absence |
| Concept under a path | `Grep` 3-6 keywords from the question under the path; `Read` the top hits. On a code file, also Serena `get_symbols_overview`. Record `no ranked scoped retrieval` | `no_signal` after one keyword widening |
| Symbol definition, or file outline | Serena `find_symbol` / `get_symbols_overview` | one `Grep -nw` of the name, labelled `text-not-symbol` |
| Every call site of a symbol | Serena `find_referencing_symbols` | true negative **only** from Serena. If Serena is down: `Grep -nw`, labelled textual, and that empty is not a negative |
| Exact `file:line` | `Read` line-40..line+40 | missing file or past EOF: citation invalid, drop |
| Prior art or a convention in merged code on the default branch | one `augment_code_search` per this contract (explicit branch, Read before acting) | empty is not absence on the working tree. Confirm with Grep/Glob before any "not found" |
| Branch-local, uncommitted, PR head, or another workspace | Grep / Glob / Serena / `git status` / `git diff` only | true negative from Grep/Read/Serena. Never Augment |

A stored negative, a dropped finding, or a `sufficient` verdict comes only from Grep, Read, or Serena. Never from Augment, and never from prefix-filtering its top-k.

## Examples

```
"how do other skills in this repo structure a refs/ dir?" → Augment (prior art on master), then Read the hits
"does the new helper exist on this branch?"            → Grep / Read (never Augment)
"find all callers of UserService.login"                 → Serena find_referencing_symbols
"open the file at src/auth/jwt.ts"                      → Read
"what's the latest stable Next.js version?"             → Context7 / WebSearch
```

## Registration

The `auggie` entry in `~/.claude.json` (or `$CLAUDE_CONFIG_DIR/.claude.json`) points at the LiteLLM gateway:

```json
"auggie": {
  "type": "http",
  "url": "${SUPERCLAUDE_LITELLM_MCP_URL:-http://ibcore:4000/mcp/}",
  "headers": {
    "x-litellm-api-key": "Bearer ${LITELLM_API_KEY}",
    "x-mcp-servers": "augment_code"
  }
}
```

`LITELLM_API_KEY` must be set in Claude Code's environment.
