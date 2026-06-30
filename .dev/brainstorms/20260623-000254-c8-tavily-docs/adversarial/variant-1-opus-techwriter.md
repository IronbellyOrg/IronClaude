# C8 Doc-Alignment Spec — Tavily 0.2.x Upgrade (Technical-Writer Variant)

**Lens:** accuracy · consistency · single-source-of-truth · zero param duplication.
**Principle (C3):** docs POINT to `src/superclaude/mcp/MCP_Tavily.md` + `install_mcp.py` as source of truth; never duplicate param tables or the install command.

Cross-cluster decisions (C1/C2/C7) are FIXED inputs here, not re-decided: pin `0.2.20`, stdio-local `npx`, `tavily.json` deleted, map/crawl added, `MCP_Tavily.md` canonical, eval token `mcp_server.tavily`.

---

## Per-file edit list

### 1. `docs/user-guide/mcp-servers.md` — TWO edits
- **L273 version fix (C1):** `"args": ["-y", "tavily-mcp@latest"]` → `"args": ["-y", "tavily-mcp@0.2.20"]`. Add `"env"` keys for `TAVILY_API_KEY` already present; append `DEFAULT_PARAMETERS` per C1? **No** — anti-duplication: keep the snippet minimal (pin + key only) and add one trailing line under the block: `> Canonical install args live in `install_mcp.py`; tool/param reference: `src/superclaude/mcp/MCP_Tavily.md`.` This kills the third version stance without re-publishing the param table.
- **L138 Node fix:** `Node.js 16+` → `Node.js 18+` (matches installer + mcp-installation.md L91/L213). This is the only stale Node string.
- **L136 capability line (map/crawl, C2):** broaden one line: `**Purpose**: Web search and real-time information retrieval for research` → `…research, plus extract / map / crawl for deep multi-source research`. Append pointer: `See `src/superclaude/mcp/MCP_Tavily.md` for the full tool list.` No tool table inline.

### 2. `src/superclaude/core/FLAGS.md` — ONE edit (L69–72)
Broaden `--tavily` Behavior from search-only to the 0.2.x surface, with a pointer (no param table):
- Trigger line: unchanged (already covers research queries).
- Behavior: `Enable Tavily for web search and real-time information gathering` → `Enable Tavily for web search, content extract, and deep-research map/crawl (see MCP_Tavily.md)`.
- Source-of-truth note: `src/superclaude/core/*` is canonical → edit here, then `make sync-dev`, then `make verify-sync`. Do NOT edit `.claude/core/FLAGS.md`.

### 3. `docs/eval/retry.md` — ONE edit (token fix, C7)
- **L138** manifest example: `- mcp.tavily       # capability gate` → `- mcp_server.tavily # capability gate`. This is the ONLY stale `mcp.tavily` occurrence in scope (confirmed: grep of docs/eval/retry.md returns exactly one). No other prose in this file references the token.

### 4. `docs/reference/comprehensive-features.md` — ONE edit (L98)
- The **Configuration Files** inventory lists `- tavily.json`. Since C1 DELETES that orphan, **remove the `- tavily.json` line** to prevent a doc pointing at a deleted file. (This is the one place the deletion DOES require a doc edit — corrects the task note's "no doc edit needed" assumption for the file inventory, distinct from the remote endpoint which truly has no doc ref.)
- L75 tool-list entry (`7. tavily - Web search…`): broaden to `Web search, extract, and deep-research (map/crawl)` + the existing L80 already points to `MCP_Tavily.md` as primary doc — no further table.

### 5. Files needing NOTHING (verified)
- `src/superclaude/core/MODES.md` (L293): mentions "Tavily" as a named MCP in research-mode behavior. No version/install/tool-surface claim → no edit.
- `src/superclaude/core/COMMANDS.md` (L57): lists Tavily among `/troubleshoot` MCPs. Name-only → no edit.
- `docs/user-guide/{commands,flags,modes,agents}.md`: no tavily version/install/tool-list claims in scope → no edit (flags.md is a rendered mirror of FLAGS.md surface; if it duplicates the `--tavily` description verbatim, apply the same Behavior broadening — verify before edit).
- `docs/user-guide/mcp-installation.md`: already Node 18+ (L91/213), no version string, API-key flow correct (L70–79) → no edit.
- `docs/mcp/mcp-integration-policy.md` + `mcp-optional-design.md`: tavily appears only as an optional/fallback named server (policy/lifecycle prose, no version/install/tool-table) → no edit.
- `docs/reference/basic-examples.md` (L36): "optional Tavily enrichment" name-only → no edit.
- `docs/research/*`, `docs/analysis/*`: EXCLUDED per scope (research-output artifacts).

---

## (d) Verification — doc-consistency check

Run from worktree root (UV-only; these are read-only greps, no UV needed):

```bash
# V1: no doc claims any tavily version other than 0.2.20
grep -rn "tavily-mcp@" docs/ src/superclaude/core/ src/superclaude/mcp/ \
  | grep -v "tavily-mcp@0.2.20" && echo "FAIL: stray version" || echo "PASS V1"

# V2: no stale mcp.tavily token (must be mcp_server.tavily)
grep -rn "mcp\.tavily" docs/ && echo "FAIL: stale token" || echo "PASS V2"

# V3: no doc references the deleted tavily.json
grep -rn "tavily\.json" docs/ && echo "FAIL: dangling config ref" || echo "PASS V3"

# V4: no stale Node 16+ near tavily
grep -rn "Node.js 16" docs/ && echo "FAIL: stale node" || echo "PASS V4"

# V5: core sync after FLAGS.md edit
make sync-dev && make verify-sync
```

## Acceptance criteria
1. `grep tavily-mcp@` across docs+core yields ONLY `0.2.20` (V1 PASS).
2. Zero `mcp.tavily` occurrences; `mcp_server.tavily` present in retry.md (V2 PASS).
3. Zero `tavily.json` references in docs (V3 PASS).
4. Zero `Node.js 16` in docs; tavily entry reads 18+ (V4 PASS).
5. `--tavily` (FLAGS.md) and tavily tool entries name extract + map/crawl AND point to `MCP_Tavily.md`; no param table is duplicated outside MCP_Tavily.md.
6. `make verify-sync` clean (FLAGS.md change propagated) (V5 PASS).
7. MODES.md, COMMANDS.md, mcp-installation.md, both mcp/* policy docs unchanged.

## Biggest risk
`comprehensive-features.md` Configuration-Files inventory (L98) silently references the **deleted** `tavily.json`. If V3 is skipped, the only surviving dangling pointer to a removed file ships — a single-source-of-truth violation that the version/token fixes would otherwise mask. V3 is the load-bearing check.
