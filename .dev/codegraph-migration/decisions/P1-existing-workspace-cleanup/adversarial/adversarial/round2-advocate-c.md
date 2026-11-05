# Round 2: Advocate for Variant 3 (Option C), rebuttals

Sources re-checked read-only: `install_mcp.py:55-61,1320-1339`, `git show 0e7bc31f` (registry and docs hunks), `docs/reference/mcp-server-guide.md:394`, `docs/troubleshooting/serena-installation.md:34`, `main.py:161-186`.

## Responses to criticisms

**1. The `--retire-legacy` flag is unnecessary (A, B). Conceded in full.** `install_mcp.py:1320-1324` rejects `--uninstall` for every server except `codebase-memory-mcp`, so no consented Serena removal path exists today. A printed `claude mcp remove serena --scope user` gives the user the same choice with no new code and nothing to delete later. The `--dry-run` also loses its reason to exist: automatic removal is now limited to entries IronClaude provably wrote, and each one can be restored with one printed command. A cheaper preview should survive only where code is already being rewritten. Phase 1 must rewrite the codebase-memory block of `superclaude install --list` (`main.py:161-186`) anyway, because it calls `discover_executable` and `_native_registration_matches`, which Phase 1 deletes. Replace that block with one read-only line per retired name: "absent", "will be removed (IronClaude shape)" or "kept: <reason>". That adds no new flag and no new tests beyond the rewrite.

**2. Does the opt-in argument cover the older Serena form? Yes, honestly, and I accept B's removal anyway.** The user still chose Serena. So consent alone does not decide this case; provable ownership does. The older argv (`... --from git+https://github.com/oraios/serena ... --context ide-assistant --enable-web-dashboard false --enable-gui-log-window false`) was written only by IronClaude's registry code. I confirmed this in the `0e7bc31f` `install_mcp.py` hunk. The docs of that time told users to type a shorter command without the `--enable-*` flags, so an exact argv match separates the two. From a security view the removal is also a net gain: the older form runs unpinned code from the GitHub HEAD on every start, and IronClaude deliberately dropped it in `0e7bc31f` ("pin supported server launchers"). Condition: print the exact removed argv and tell the user how to register Serena themselves.

**3. Goal tension on non-Coder dev workspaces. Yes, keep-and-print fails the goal there.** I checked whether a hand-typed docs command could explain a user-scope current-pin entry. Today's docs command (`mcp-server-guide.md:394`, `serena-installation.md:34`) is byte-identical to the registry pin, but it passes no `--scope`. It would therefore land in the CLI's default scope, which I believe is local (UNVERIFIED in this repo). On a dev workspace with no Coder bundle, a user-scope current-pin entry was therefore most likely written by `superclaude mcp --servers serena`. That makes it an IronClaude-owned leftover, which the goal says must go. The only blocker is telling a dev workspace from a Coder one. One candidate signal: Coder's bundle installs the `serena-agent` uv tool, while IronClaude's registry only uses `uvx` and installs no tool. This is a heuristic, not proof, and it is UNVERIFIED as a reliable discriminator. I would not ship it without the Coder repo confirming it.

Proposed residual-risk statement for the decision:
> On non-Coder workspaces, a user-scope `serena` entry that exactly matches the current `serena-agent==1.7.0` pin is kept, not removed, because IronClaude cannot tell it from the identical entry Coder's bundle writes. This leaves one IronClaude-written registration of a retired server. It still works (uvx fetches the pinned package; it depends on no binary the image stops shipping), needs no privilege, and `superclaude install` prints the exact one-line removal command on every run. The gap closes when a verified Coder-workspace signal exists or when Coder's bundle stops registering Serena (Phase 2 handoff); the sunset task then removes this entry automatically.

I judge this acceptable only if it is written down as a known goal miss, not as goal met.

## Updated assessment

C as a separate variant should not win. What survives of C is this: Coder-owned and ambiguous state is handed off; consent comes from a printed command, not a flag; and `--list` shows a read-only preview inside the existing rewrite. Amended A, plus B's older-form row, plus these points is the merge I support.

## New evidence

- Today's docs register Serena without `--scope`, so a hand-typed entry most likely lands in local scope, not user scope (CLI default UNVERIFIED here). This raises the odds that a user-scope current-pin entry on a dev workspace is IronClaude-written.
- The `main.py:161-186` `--list` block depends on code Phase 1 deletes, so the preview costs no extra surface.

## Updated per-point positions (changed only)

| Point | Preferred | Reason |
|---|---|---|
| C-001 | merge: A automatic for codebase-memory and the older Serena argv; current pin kept and printed | Remove what is provably owned |
| C-003 | merge: exact allowlist with an ownership tier per shape (B) | Provenance differs by shape |
| C-010 | A | My flag is withdrawn |
| U-005 | merge: read-only preview inside the rewritten `--list` block | No new flag |
| X-003 | A, with the residual recorded | The current pin on dev workspaces is a recorded miss |
| A-002 | B's tiering | Shape proves ownership only when one writer is possible |
