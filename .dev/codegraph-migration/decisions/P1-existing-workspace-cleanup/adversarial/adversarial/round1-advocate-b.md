# Round 1: Advocate for Variant 2 (Option B)

Round 1 advocate report for Variant 2 (Option B): its key point holds (receipt-gated removal of IronClaude-acquired files), but two of its steps break ownership rules and should be dropped.

**Position summary.** B is the only variant that takes responsibility for files IronClaude itself provably installed (kind-B binary, receipt). Its Serena uv-tool step and updater deletion are wrong as written. I argue for a narrowed B merged into A: automatic registration retirement, plus receipt-gated kind-B removal kept for one release behind consent.

**Steelman V1 (A).** It meets the goal on `update.sh` and on Coder with no prompt, network or root, at almost no cost. It reuses the exact-user-scope helpers that install already uses without prompting (`install_mcp.py:874-895`). Its U-002 keep-and-report rule for same-named entries with a different shape is the best safety detail in any variant.
**Steelman V3 (C).** It is the only variant that never changes user MCP state without a visible preview (U-005 dry-run). It also respects the goal's hand-off clause for Coder-owned state completely.

**Strengths claimed**
1. B cleans IronClaude-owned files. The receipt and `.pending` marker are written by IronClaude (`install_codebase_memory.py:81-86`). A and C leave them orphaned once the module is deleted (A-006).
2. B reuses proven ownership proof instead of inventing it. The receipt identity is revalidated right before upstream removal (`install_codebase_memory.py:345-351`), and the external `/usr/local/bin` copy is refused (context, `install_mcp.py:957-959`).
3. B keeps a removal path alive. Deleting the 759-line module (A, C) removes the only tool that can remove a kind-B binary safely. B keeps that path for one release.
4. B costs nothing when there is no receipt. With no receipt, no subprocess runs. Coder workspaces are kind A, so B's slow path should only run on dev workspaces, which have no 60 s bound. This is my inference: whether any Coder workspace carries a receipt is UNVERIFIED.

**Weaknesses in V1 (A)**
1. The serena matcher (substring `serena-agent`) misses the older IronClaude shape (git `0e7bc31f`, A-001), so it falls short of the goal on older dev workspaces.
2. The basename match for codebase-memory is looser than the existing exact-path matcher (`install_mcp.py:757-763`).
3. A leaves the receipt and `.pending` marker behind, and it prints `codebase-memory-mcp uninstall -y` after the registration is already gone. Whether that order works is UNVERIFIED (A-005). Existing code uninstalls the native binary first and cleans up the registration after (`install_mcp.py:993-995`).

**Weaknesses in V3 (C)**
1. By its own "Against" section, `./update.sh` alone does not meet the goal (X-003).
2. Its consent premise is wrong for exact entries: install already removes them without a prompt (`install_mcp.py:874-883`). The consent gate (`:981-986`) covers only account-wide removal.
3. "Shape-matched" is never defined (S-002).
4. It adds a migration-only flag, help text, docs and tests that must be removed later.

**Concessions (B as written)**
1. `uv tool uninstall serena-agent` removes a tool Coder installed. The goal says Coder-owned leftovers are handed off, and doing this would churn Coder's health check. Drop the step.
2. Deleting the updater `~/.local/bin/install.sh` contradicts existing policy. The code says "The adjacent updater is left in place; IronClaude does not erase companion/cache files" (`install_codebase_memory.py:74-78`) and "adjacent updater left untouched" (`:371`).
3. A prompt-free account-wide uninstall breaks the consent requirement (`install_codebase_memory.py:331-336`, `install_mcp.py:981-986`).
4. B's "60 s" figure is wrong. The reused path uses `INSTALL_TIMEOUT = 300` (`install_codebase_memory.py:28`, `:352-355`).
5. Running upstream uninstall without network is UNVERIFIED, and kind-B workspaces may not exist at all.
6. B depends on A's text (S-002).

**Shared assumptions**
- A-001 REJECT: earlier IronClaude wrote the `git+https://github.com/oraios/serena ... --context ide-assistant` form. Match both historic argv lists exactly; the stored shape is `command` = first token, `args` = the rest (`install_mcp.py:1142-1159`).
- A-002 QUALIFY: matching every argument exactly is the best proof available. An identical hand-made entry is functionally the same, so report it and print the command to re-add it.
- A-003 QUALIFY: `main.py:193-275` runs every step with no early exit and nothing gated on `--force`, so the step is reached even after an earlier failure. A Coder 60 s kill or an uncaught exception still skips it, so wrap it and keep it cheap.
- A-004 QUALIFY: `read_user_mcp_entry` honours `CLAUDE_CONFIG_DIR` (`install_mcp.py:714-754`); whether the CLI does is UNVERIFIED. Verifying after removal catches a mismatch at that moment, and the next install retries without side effects.
- A-005 QUALIFY: the order is UNVERIFIED. Follow the existing order: upstream uninstall first, registration cleanup second.
- A-006 REJECT: the receipt and `.pending` are IronClaude-owned. Remove them under the same lstat/uid/nlink checks (`install_codebase_memory.py:87-100`).
- A-007 QUALIFY: the code already warns that removal "may interrupt active sessions" (`:74-78`). That applies mainly to binary removal, which is one more reason kind-B removal needs consent.

**Per-point preference**

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | Most complete section set |
| S-002 | A | B is not self-contained |
| C-001 | merge: A trigger for registrations, C consent for binary removal | Goal plus the consent rule |
| C-002 | merge: A registrations + B receipt/`.pending` cleanup; drop uv tool | Ownership |
| C-003 | merge: exact historic argv lists (fixes A) + B receipt identity | Covers A-001 |
| C-004 | A | Explicit non-fatal semantics |
| C-005 | tie | All keep data |
| C-006 | A | B churns Coder; C waits on Coder's schedule |
| C-007 | A | B's budget is misstated (300 s) |
| C-008 | merge: B's retained receipt logic behind consent | Keeps a safe path |
| C-009 | A | Only one that states it |
| C-010 | A | Sunset table |
| X-001 | A | Matches existing install behaviour |
| X-002 | A | Coder owns `serena-agent` |
| X-003 | A | `update.sh` alone must suffice |
| X-004 | A plus a Coder hand-off note | Identical IronClaude pin (`install_mcp.py:59`); bundle re-add is harmless |
| A-001 | merge: both historic shapes | Contradicted assumption |
| A-002 | A + report line | Best available proof |
| A-003 | A, wrapped | No early exit in install |
| A-004 | A | Verify after removal |
| A-005 | B order | Matches existing code |
| A-006 | B, extended to `.pending` | IronClaude-owned files |
| A-007 | C for binaries, A for registrations | Session impact |
