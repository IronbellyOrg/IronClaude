# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (22 of 22 points agreed; 16 unanimous, 6 by 2/3 majority)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3
  - Variant 1 advocate (Option A), persona architect
  - Variant 2 advocate (Option B), persona analyzer
  - Variant 3 advocate (Option C), persona devops/security
- Omissions: none (every advocate answered A-001..A-005)
- Taxonomy coverage: L1 (S-001, S-002), L2 (C-001, C-003, C-004, C-005, C-007..C-011, X-001..X-003, A-005), L3 (C-002, C-006, C-012, A-001..A-004). No level is empty, so no forced round.
- Harness note: the Variant 3 advocate's output was flagged by the harness for an instruction-shaped pattern ("settings-json"). On review it only discusses `settings.json` as a config file; it contains no directives. Treated as data.

## Round 1: Advocate Statements

### Variant 1 Advocate (Option A, architect)

**Position summary.** IronClaude should own installing codegraph: a pinned v1.6.2 tarball, checked against a SHA-256 kept in reviewed IronClaude source, with IronClaude registering the MCP server itself. It is the only option with a real integrity check that survives `./update.sh` and works the same on every platform. The right final shape is A plus C's detection step: reuse a baked binary when its version matches, otherwise do the verified download.

**Steelman B.** B means the least IronClaude code. Upstream `codegraph install --refresh` keeps the config shape correct across releases and removes legacy hooks (eval §2, `claude.ts:144-153`). B also matches today's codebase-memory flow, where `acquire_codebase_memory` runs "the complete official bootstrap" (`install_codebase_memory.py:611-612`). Fetching `install.sh` at a pinned tag improves on eval §2, which fetches from `main`.

**Steelman C.** C is the best experience in Coder: codegraph is on PATH from first boot, works offline, and skips the 63 MB download and 286 MB copy per home. The binary is root-owned, the hash is checked at build time, and the Coder team already bakes codebase-memory this way. C's `codegraph --version` equality check (U-010) is the cleanest detection point.

**Strengths claimed.**
1. Real integrity check. Upstream `install.sh` "does NOT verify" `SHA256SUMS` (eval §1, `install.sh:71-82`). A keeps the hash in reviewed source, a different trust root from the tarball server. The check was validated hands-on (eval §5.1, `ef0af416…` OK).
2. Survives `./update.sh`. `superclaude install --force` copies every core `.md` over `~/.claude/` (`install_core.py:62-71`), so upstream's block "is therefore erased" (eval §2). A puts guidance in `src/superclaude/core/CLAUDE.md`.
3. IronClaude is the only writer of Claude config. A uses the existing `claude mcp add-json … --scope user` (`install_mcp.py:775-786`) and keeps `alwaysLoad` (eval §3).
4. No prompt hook, which avoids an unchosen cost (a 41-symbol payload on one prompt, eval §5.9).
5. Telemetry and the update check are both off (`CODEGRAPH_TELEMETRY=0`, `CODEGRAPH_NO_UPDATE_CHECK=1`).
6. One code path for linux and darwin on x64 and arm64. Today's codebase-memory acquire step is Linux-only (`install_codebase_memory.py:630-635`).

**Weaknesses identified in others.**
1. B has no integrity check. It contradicts itself on X-001, and `--yes` with `--target=auto` lets upstream choose which agents it configures.
2. B puts `curl | sh` from an effectively single-maintainer repo (1,535 commits from one person, eval §1) in the required path.
3. C alone leaves macOS and non-Coder Linux with no install path. It needs two repos to change in lockstep, and existing workspaces drift (X-002).
4. C is silent on the update check, the prompt hook and uninstall.

**Concessions.** A is the most code to write: download, hash table, extract, symlinks, receipt, uninstall and tests, plus 4 hashes per release. As written, A never detects an existing binary, while today's pattern reuses one (`install_codebase_memory.py:637-650`). Because A keeps upstream's layout, `codegraph upgrade` still works, and it would re-run `install --refresh` and bring back the hook and the CLAUDE.md block. A must call this unsupported or warn about it. On Coder, the per-workspace download is a real cost.

**Shared assumptions.** A-001 QUALIFY (install correctly stops at register; per-checkout `init` needs a named owner). A-002 ACCEPT (reuse the existing readiness guard, `install_codebase_memory.py:614`). A-003 REJECT as unchecked (register an absolute command path). A-004 QUALIFY (versioned dirs plus a symlink swap help; install should warn about or stop running daemons). A-005 QUALIFY (the pinned hash makes a swapped asset fail loudly; the image copy is an offline fallback).

**Recommended combination.** A as the required phase, with C's detection in front: if `codegraph --version` equals the pin, reuse that binary, otherwise do the SHA-verified download into `~/.codegraph`. Register an absolute command path with both env flags. Baking becomes an optional speed-up, not a dependency. Per-checkout `init` is a separate decision.

### Variant 2 Advocate (Option B, analyzer)

**Position summary.** B has the strongest precedent: IronClaude already gets codebase-memory by running the upstream bootstrap, and B needs the least code. But B is weakest on integrity and on config ownership, so its acquisition step should feed a combination, not ship alone.

**Steelman A.** A pins a SHA-256 per platform in reviewed source, a separate trust root from the tarball and the only real integrity check on any path. It leaves config, guidance and hook policy to IronClaude, which `--force` rewrites anyway (`install_core.py:62-71`). Mirroring upstream's layout keeps `upgrade` and `uninstall` working.

**Steelman C.** Coder is the main deployment. Baking removes the 63 MB download and the 286 MB per-home copy (eval §5.2), works offline, and gives a root-owned binary. It is exactly how codebase-memory is deployed today, and the build-time hash gives the same integrity as A.

**Strengths claimed.**
1. Existing practice. `acquire_codebase_memory` (`install_codebase_memory.py:611-735`) downloads upstream `install.sh` and runs it with bash, noting "Upstream configures detected clients and companion instructions, skills, agents and hooks" (line 668). B is stricter: the script is fetched at a pinned tag, while codebase-memory uses `main` (lines 24-26).
2. Least code: three subprocess calls instead of a whole acquisition module.
3. Upstream keeps its config correct (`--refresh`, cleanup of legacy hooks).
4. `codegraph uninstall` fully reverses what upstream wrote.

**Weaknesses identified in others.**
1. A's layout mirror is partial: a user-run `codegraph upgrade` re-runs `install --refresh` and writes the CLAUDE.md block and the hook (eval §2). That brings back the ownership conflict, and A has no guard against it.
2. A must update 4 hashes per release, at about 8 releases in 3 months (eval §1).
3. C needs two repos to agree on a version, and it does nothing for macOS without A.
4. C does not address `CODEGRAPH_NO_UPDATE_CHECK`. A root-owned install that keeps prompting for upgrades nobody can apply is a usability defect.

**Concessions.** B has no integrity check: `install.sh` re-downloads the tarball and never checks `SHA256SUMS`, so checking the hash first does not help. `--force` wipes B's CLAUDE.md block. `--yes` installs a prompt hook that adds context nobody chose. B's behaviour can drift between pins.

**Shared assumptions.** A-001 ACCEPT (nothing upstream runs `init`; it needs a separate owner). A-002 ACCEPT (keep the readiness guard everywhere). A-003 QUALIFY (A+C needs the version check or an absolute path). A-004 QUALIFY (`install.sh` prunes older `versions/*` and can delete files under a running daemon; stop daemons before the swap). A-005 QUALIFY (low risk; C's build-time copy reduces it).

**Recommended combination.** C on Coder plus A as the verified fallback, with C's version-equality check deciding between them. Keep two parts of B: the upstream on-disk layout, and `codegraph install --print-config claude` (writes nothing, eval §5.9) as a unit-test drift check of IronClaude's `add-json` entry. Never run `codegraph install` or `install.sh` in the required path. Stop daemons before the swap.

### Variant 3 Advocate (Option C, devops/security)

**Position summary.** Bake codegraph into the Coder image: a SHA-256 pinned and checked at build time, a root-owned `/usr/local/bin/codegraph`, and telemetry off in the image env. `superclaude install` checks the exact version and registers. C alone does nothing for non-Coder machines, so it is the Coder-fleet layer of a C+A combination.

**Steelman A.** One code path and one repo to bump. The hash is pinned in reviewed source, the upstream layout is kept, `CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_UPDATE_CHECK=1` are set in the MCP entry, and the hook is explicitly excluded. It is the most complete single option.

**Steelman B.** B needs the least code. Upstream ships fast (8 releases from 2026-07-07 to 2026-10-03), so letting it own its config migrations avoids IronClaude chasing a moving target. Fetching the script at the pinned tag avoids drift to "latest".

**Strengths claimed.**
1. Smallest attack surface on disk. Under A or B, `~/.local/bin/codegraph` is writable by anything running as `coder`, including a bypass-mode agent. That binary runs on every session through an `alwaysLoad` MCP entry. A root-owned binary closes that path.
2. Same integrity as A, enforced earlier: the build-time check uses the same value that was checked hands-on (`ef0af416…`, eval §5.1).
3. A byte-identical binary across the fleet, no 63 MB download or 286 MB per-home copy, and it works offline.
4. Upgrades are safe for the daemon: the binary changes only at a rebuild or restart, which also ends the daemon (eval §5.7 shows it outlives clients, with a 300 s idle timeout).
5. A strict version gate, stricter than today's reuse of any external executable (`install_codebase_memory.py:643-650`).
6. Matches the Coder team's current codebase-memory bake.

**Weaknesses identified in others.**
1. A writes a user-writable binary, depends on GitHub at each workspace's first install, puts 286 MB in every home, and swaps the binary in place under a live daemon.
2. B has no integrity check and runs `curl | sh` from a single-maintainer repo.
3. B lets upstream edit `~/.claude.json`, `settings.json` and `CLAUDE.md`, then `--force` wipes the block, so the two fight.
4. B's prompt hook adds context nobody chose, and telemetry stays on by default until it is switched off.

**Concessions.** C couples two repos, and existing workspaces lag behind `./update.sh`. A's single bump is better. Non-Coder machines need A. C is silent on the hook, `CODEGRAPH_NO_UPDATE_CHECK` and uninstall. The image grows by about 286 MB. A fallback on version mismatch brings back a user-writable second copy that can shadow the baked one, so the mismatch behaviour must be decided explicitly.

**Shared assumptions.** A-001 QUALIFY (out of this decision; `init` needs an owner). A-002 QUALIFY (keep the readiness check). A-003 REJECT (a bare `codegraph` is unsafe with two copies; register the absolute path that passed the version check). A-004 QUALIFY (safe under C; unproven under A for a newer client talking to an older running daemon). A-005 QUALIFY (only image build time depends on GitHub; cached layers keep the file).

**Recommended combination.** A as the engine and C as the Coder fast path. IronClaude holds the single pin and the hash table, and the image bakes the same pin with a build-time hash check. `superclaude install` checks for an exact version match, then registers the absolute path with A's env settings and no hook. A's download into `~/.codegraph` runs only when no matching binary is found, and on a Coder workspace it warns that the image needs a rebuild.

## Scoring Matrix

Per-advocate verdicts are recorded as V1 / V2 / V3.

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | Tie (no winner) | 95% | All three use the same section model. |
| S-002 | L1 | 1 | 1 | 1 | Variant 1 | 92% | Exact MCP JSON, layout, receipt and tests make A buildable. |
| C-001 | L2 | 1+3 | 1+3 | 1+3 | Combo 1+3 | 95% | Unanimous: reuse a baked or matching binary, otherwise A's verified download. |
| C-002 | L3 | 1 | 1 | 1+3 | Variant 1 (with 3 at build time) | 85% | Only A's source-pinned hash covers every platform; C applies the same hash at build. B conceded. |
| C-003 | L2 | 1 | 1 | 1+3 | Variant 1 (= 3) | 92% | IronClaude-owned `add-json`, as at `install_mcp.py:775-786`. |
| C-004 | L2 | 1 | 1 | 1+3 | Variant 1 (= 3) | 95% | `install_core.py:62-71` erases B's block. B conceded. |
| C-005 | L2 | 1 | 1 | 1 | Variant 1 | 93% | Explicit no-hook choice; B conceded the context cost (eval §5.9). |
| C-006 | L3 | 1 | 1 | 1 | Variant 1 | 93% | The MCP env covers non-image machines and the update check. |
| C-007 | L2 | 3 | 1+3 | 3 | Variant 3 (on Coder) | 75% | Root-owned binary; user layout only where there is no image. |
| C-008 | L2 | 1+3 | 1 | 1 | Variant 1 | 80% | One pin in IronClaude, delivered by `./update.sh`. C conceded the two-repo cost. |
| C-009 | L2 | 3 | 3 | 3 | Variant 3 | 88% | Unanimous: bake, as long as install detects it rather than depending on it. |
| C-010 | L2 | 1 | 1 | 1 | Variant 1 | 93% | Only A covers linux/darwin on x64 and arm64. |
| C-011 | L2 | 1 | 2 | 1 | Variant 1 | 72% | A's receipt pattern. B's `uninstall` also deletes config. |
| C-012 | L3 | 3 | 3 | 3 | Variant 3 | 92% | Exact version-equality gate (U-010). |
| X-001 | L2 | 1 | 1 | 1+3 | Variant 1 (= 3) | 95% | IronClaude must own Claude config. B conceded. |
| X-002 | L2 | 1 | 1 | 1+3 | Variant 1 | 82% | The IronClaude pin is the single source of truth; the image bakes the same pin. |
| X-003 | L2 | 1+3 | 1+3 | 1+3 | Combo 1+3 | 95% | Today's pattern is a hybrid: bake, then reuse, else acquire (`install_codebase_memory.py:637-650`). |
| A-001 | L3 | none | none | none | None: gap carried forward | 90% | All three agree per-worktree `codegraph init` needs a separate owner (eval §4). |
| A-002 | L3 | 1 | tie | 1+3 | Variant 1 (= 3) | 88% | Reuse the existing Claude-readiness guard (`install_codebase_memory.py:614`). |
| A-003 | L3 | 3 | 3 | 3 | Variant 3 + absolute path | 90% | Register the absolute path of the binary that passed the version check. |
| A-004 | L3 | 1 | 1 | 3 | Variant 1 + daemon handling | 68% | Versioned dirs and symlink swap, plus warning about or stopping running daemons. C argued restart-only swaps are safer. |
| A-005 | L3 | 3 | 3 | 3 | Variant 3 | 85% | Only image build time depends on GitHub; the source-pinned hash makes a swapped asset fail loudly. |

Points won: Variant 1 = 13 (incl. shared wins C-003, C-004, X-001, A-002), Variant 3 = 5, Combo 1+3 = 2, Variant 2 = 0, tie/none = 2.

## Convergence Assessment
- Points resolved: 22 of 22 (16 unanimous, 6 by 2/3 majority: C-002, C-007, C-008, C-011, X-002, A-004)
- Alignment: 100%
- Threshold: 80%
- Taxonomy gate: passed (L1, L2 and L3 each have points)
- Invariant gate: not applied (Round 2.5 skipped at depth=quick)
- Status: CONVERGED
- Unresolved points: none. A-001 is agreed to be out of scope for this decision and is carried forward as a condition.
- Cross-advocate consensus: all three advocates independently recommended the same combination. IronClaude holds one pin and the hash table; `superclaude install` reuses a binary whose version matches exactly (baked in Coder), otherwise does A's verified download; it registers the absolute path with telemetry and update-check env, no prompt hook, and never runs `codegraph install` or `install.sh`.
