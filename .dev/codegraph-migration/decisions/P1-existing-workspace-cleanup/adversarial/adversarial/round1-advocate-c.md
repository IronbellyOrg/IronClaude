# Round 1: advocate for Variant 3 (Option C)

Persona: security (least privilege, consent, blast radius, never surprising the user) with analyzer rigor.
Narrowed position: I argue for consent and Coder handoff for Serena only, and I concede to Option A on the codebase-memory registration.

## Position summary
Option C is right that a Serena registration should not be removed silently: Serena is an opt-in server (`"required": False`, install_mcp.py:55-61), and on Coder workspaces Coder's bundle writes the same argv. Option C is wrong that `./update.sh` should do nothing. The codebase-memory registration came from IronClaude's *required* install phase (main.py:254-262), so removing it automatically is the honest fit. Recommended merge: A's automatic exact-shape removal for `codebase-memory-mcp`, plus C's explicit, previewed, consented removal for `serena`.

## Steelman of Variant 1 (A)
It is the only option that meets "`./update.sh` leaves nothing behind" with no extra human step. It reuses helpers that are already verified (read_user_mcp_entry :714-754, verify-after-remove :939-944). It is non-fatal, which matters because `set -euo pipefail` would otherwise stop `make sync-dev`. It reports a same-named entry with a different shape as kept instead of removing it (U-002). Install already removes exact user entries without a prompt (:874-883), so A adds no new kind of mutation.

## Steelman of Variant 2 (B)
It leaves the most workspaces fully clean, and for kind-B binaries it reuses receipt plus sha256 proof that is already tested, not invented guesswork.

## Strengths claimed (C)
1. Serena is opt-in (`required: False`, :60), so a user who ran `superclaude mcp --servers serena` made a deliberate choice. Silently undoing that choice during a routine update is a surprise, and C prevents it.
2. Ownership of Serena cannot be proven. The registry pin (:59) is byte-identical to Coder's bundle argv (context.md:13), and the goal says Coder-owned leftovers are "handed off, not removed by IronClaude" (context.md:5). A and B both break that rule (X-004). C hands the Coder case off.
3. Automatic Serena removal on Coder does no lasting good. The bundle re-registers `serena` on every workspace start (context.md:19), so A's removal is undone each time and only adds churn and confusing output.
4. The dry-run preview (U-005) lets the user see exactly which entries match before anything is deleted, which is the least-privilege pattern.
5. C adds nothing to the Coder 60 s install bound (C-007).

## Weaknesses in Variant 1 (A)
1. The Serena matcher (argv contains `serena-agent` and `start-mcp-server`) misses the older IronClaude-written `git+https://github.com/oraios/serena ... --context ide-assistant` form (git 0e7bc31f, A-001), and it also matches any hand-made entry that contains those substrings.
2. The codebase-memory matcher loosens the existing exact-path rule (`command == str(executable)`, :757-763) to a basename match. Any user binary named `codebase-memory-mcp` anywhere on disk would then be treated as IronClaude's.
3. It ignores the IronClaude-written receipt and `.pending` marker (install_codebase_memory.py:81-86).

## Weaknesses in Variant 2 (B)
1. It uninstalls the `serena-agent` uv tool, which Coder installed and IronClaude has no receipt for. That breaks Coder's health check and the bundle reinstalls it (option-b.md:21).
2. It runs the account-wide upstream uninstall with no prompt, which is the exact action the consent gate at :981-986 exists to stop.
3. Its timeouts (60 s plus 30 s) exceed Coder's 60 s total bound.

## Concessions
1. C fails X-003: `./update.sh` alone leaves both registrations in place.
2. C's claim of "no prompt-free mutation" is factually overstated. Install already removes exact user entries without a prompt (:874-883), and the consent gate at :981-986 covers only the account-wide native uninstall.
3. "Shape-matched" is left undefined in C.
4. A new flag means extra migration code to remove later. A's sunset table is cheaper.

## Shared assumptions
- A-001 REJECT: git 0e7bc31f shows IronClaude once wrote a different argv, so the matcher must be an exact set of every argv IronClaude has shipped.
- A-002 QUALIFY: shape is acceptable proof for the full-path codebase-memory entry IronClaude wrote. For opt-in Serena, shape does not show the user wants it gone, so consent is needed.
- A-003 QUALIFY: main.py:189-275 runs every step with no early return and regardless of `--force`, so a final step is reached. An uncaught exception, or Coder's 60 s timeout firing earlier, would still skip it.
- A-004 QUALIFY: read_user_mcp_entry honours `CLAUDE_CONFIG_DIR`. Whether the `claude` CLI does the same is UNVERIFIED, and verify-after-remove only proves absence at that moment.
- A-005 QUALIFY: UNVERIFIED. When a receipt is present, print the upstream uninstall first, or skip codebase-memory registration removal entirely.
- A-006 REJECT: the receipt and marker are IronClaude-owned (install_codebase_memory.py:81-86). Remove them only after the binary is gone; otherwise list them.
- A-007 QUALIFY: running stdio servers stay up until restart, so the risk is low, but this is UNVERIFIED. Print "restart clients".

## Per-point preference
| point | preferred | reason |
|---|---|---|
| S-001 | A | most complete structure |
| S-002 | A | self-contained; C leaves "shape-matched" undefined |
| C-001 | merge: A for codebase-memory, C for serena | the required phase justifies automatic removal; an opt-in server needs consent |
| C-002 | merge: A for codebase-memory, C for serena | same reason |
| C-003 | merge | exact full-path set for codebase-memory (:757-763); exact argv set for serena including the 0e7bc31f form |
| C-004 | A | non-fatal; avoids stopping `update.sh` under `set -e` |
| C-005 | tie (A) | all keep data |
| C-006 | C for serena, A for codebase-memory | the bundle re-adds serena |
| C-007 | A/C | B exceeds the 60 s bound |
| C-008 | A | print, do not automate |
| C-009 | A | only option that defines missing-CLI behaviour |
| C-010 | A | sunset table is cheaper than a new flag |
| X-001 | A | :874-883 shows prompt-free exact removal is existing behaviour |
| X-002 | A/C | Coder owns the uv tool |
| X-003 | A | C misses the goal |
| X-004 | C | goal requires handing off Coder-owned leftovers |
| A-001 | none (all share it) | use an exact argv set |
| A-002 | C | consent for opt-in Serena |
| A-003 | A | end placement is reached (main.py:189-275) |
| A-004 | none | UNVERIFIED for all |
| A-005 | A | prints the upstream uninstall; order needs fixing |
| A-006 | B (partial) | only B touches the receipt; extend it to the marker |
| A-007 | tie | low risk; print "restart clients" |

| Status | Result |
|---|---|
| DONE | Read context, diff analysis and all three options; spot-checked install_mcp.py, main.py and install_codebase_memory.py read-only. |
| NEXT | Round 2 rebuttal, if called for. |
