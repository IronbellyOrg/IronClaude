<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (Option C, original) -->
<!-- Merge date: 2026-10-29T16:40:00Z -->

<!-- Source: Base (original, modified) — title extended to name the merged decision -->
# W4 decision: codegraph install strategy (merged: C-shaped gate + A's verified fallback)

<!-- Source: Base (original) — evidence line kept -->
Context and evidence: `.dev/codegraph-migration/research/codegraph-evaluation.md` sections 1-5. Today codebase-memory-mcp is baked at `/usr/local/bin/codebase-memory-mcp` by `templates/VSCode-AIDev02/Dockerfile.coder` in IronbellyOrg/Coder.

<!-- Source: Base (original, modified) — new summary section built from the debate consensus; merged per Changes 1, 2, 3 -->
## Decision

`superclaude install` reuses a codegraph binary whose version exactly equals the single IronClaude pin (the root-owned copy baked into the Coder image when present), otherwise installs IronClaude's own SHA-256-verified download, and then registers the absolute path of the winning binary itself.

Top reasons:

1. **Integrity on every path.** Upstream `install.sh` does no checksum check (eval §1, `install.sh:71-82`; eval §5.2). The hash lives in reviewed IronClaude source, a separate trust root from the tarball server, and was checked hands-on (`ef0af416…`, eval §5.1). Debate: C-001, C-002, C-010.
2. **IronClaude stays the only writer of Claude config.** `superclaude install --force` copies core files over `~/.claude/` and would erase an upstream block (`install_core.py:62-71`, eval §2), and the upstream prompt hook adds unchosen context (41-symbol payload, eval §5.9). Debate: X-001, C-004, C-005.
3. **One pin, exact gate, explicit path.** One pin and hash table in IronClaude, consumed by the image (C-008, X-002). The gate requires exact version equality (C-012), and registering the absolute path removes PATH-order ambiguity when two copies exist (A-003). On Coder the baked copy avoids the 63 MB download and 286 MB per-home copy (C-009, eval §5.1-5.2).

<!-- Source: Base (original) — section structure kept -->
## What it does

<!-- Source: Base (original, modified) — bake bullet now consumes the IronClaude pin and sets both env flags; merged per Changes 2 and 4 -->
### (a) Coder image

- `Dockerfile.coder` downloads the pinned `codegraph-linux-<arch>.tar.gz`, checks its SHA-256 at build time, extracts to `/opt/codegraph/v1.6.2/`, and links `/usr/local/bin/codegraph`.
- Image env sets `CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_UPDATE_CHECK=1`.
- The pin and hash are copied from the IronClaude values. Baking is an optimization, not a dependency: a stale or missing baked copy is detected by the gate and repaired by the fallback.

<!-- Source: Base (original, modified) — fail-or-fallback replaced by a required ordered phase; merged per Changes 1, 3, 4, 6, 7, 8, 9 -->
### (b) `superclaude install` codegraph phase

Replaces the Codebase Memory phase at `src/superclaude/cli/main.py:254-262`. Steps run in this order:

<!-- Source: debate A-002 — merged per Change 9 -->
1. **Claude CLI readiness guard.** Reuse the existing readiness check that `install_codebase_memory.py:614` leaves to its caller; stop with a clear message if the Claude CLI is not ready.
<!-- Source: Base (original, modified) plus debate A-003 — merged per Change 3 -->
2. **Candidate discovery and exact gate.** Candidates in order: (1) `/usr/local/bin/codegraph`, or whatever `codegraph` resolves to on PATH if different; (2) `~/.local/bin/codegraph`. The first whose `codegraph --version` exactly equals the pin wins.
<!-- Source: Variant 1 (Option A), What it does bullets 2-3 — merged per Change 1 -->
3. **Verified fallback, only if no candidate passes.** Download `https://github.com/colbymchenry/codegraph/releases/download/v1.6.2/codegraph-<os>-<arch>.tar.gz`, verify it against the per-platform SHA-256 table in IronClaude source (linux-x64, linux-arm64, darwin-x64, darwin-arm64), extract into `~/.codegraph/versions/v1.6.2/`, and link `~/.local/bin/codegraph` and `~/.codegraph/current`. On a Coder workspace, also warn that the image is stale and needs a rebuild.
<!-- Source: debate A-004 plus Variant 2 advocate (install.sh prune hazard) — merged per Change 8 -->
4. **Running-daemon handling.** Install into a new `versions/<tag>/` directory, then flip the symlink. Leave the previous version directory until the next run; never delete a version directory in the same run that flips the symlink. Warn that open sessions keep the old daemon until its 300 s idle timeout (eval §5.7).
<!-- Source: Base (original, modified) plus Variant 1 (Option A), bullet 4 JSON — merged per Changes 3 and 4 -->
5. **Register the winning binary.** Use its absolute realpath:
   `claude mcp add-json codegraph '{"type":"stdio","command":"<abs path>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1"}}' --scope user`
   Re-register whenever the winning path changes.
<!-- Source: Base (original, modified) plus Variant 1 (Option A), bullet 5 — merged per Change 6 -->
6. **Guidance and permission.** Guidance ships in `src/superclaude/core/CLAUDE.md`. The `mcp__codegraph__*` permission is added through IronClaude's own settings handling.
<!-- Source: Variant 1 (Option A), bullet 6 — merged per Change 7 -->
7. **Receipt and removal, user copy only.** Reuse the receipt and removal pattern in `install_codebase_memory.py`. They cover only `~/.codegraph` and `~/.local/bin/codegraph`; the baked copy is image-owned.

<!-- Source: Base (original, modified) — update path; merged per Changes 2 and 11 -->
### (c) `./update.sh`

- `./update.sh` runs `superclaude install --force` then `superclaude doctor` (`update.sh:8,10`).
- On a pin bump, the gate rejects the old version. Non-Coder machines and stale Coder images take the verified fallback and re-register; a rebuilt image passes the gate directly.
- `superclaude doctor` flags drift: a codegraph version that differs from the pin, a `CODEGRAPH_START` block in `~/.claude/CLAUDE.md`, or a `codegraph prompt-hook` entry in `~/.claude/settings.json`.

<!-- Source: Base (original, modified) — two-repo sync replaced by single IronClaude bump point; merged per Changes 2 and 10 -->
### (d) Version bumps

- One place in IronClaude: the pin plus the 4 hashes, covered by unit tests. The Coder image copies the same values; a rebuild is a speed-up, not a prerequisite.
- **Drift test, test-time only.** A recorded fixture of `codegraph install --print-config claude` (writes nothing, eval §5.9) is refreshed on each pin bump. A unit test compares IronClaude's `add-json` entry with it, ignoring IronClaude's added `env`. It never runs during `superclaude install`.

<!-- Source: Variant 1 (Option A), bullets 5-6, plus Variant 2 advocate weakness #1 — merged per Changes 5, 11, 12 -->
## Explicitly not done

- No `codegraph install` and no upstream `install.sh`, in the install path or anywhere else at runtime.
- No `UserPromptSubmit` prompt hook.
- No `codegraph upgrade`: unsupported, documented as such, and detected by `superclaude doctor`.
- No writes to `/usr/local/bin` or `/opt/codegraph` from IronClaude.
- `gh attestation verify` is optional and non-blocking only (needs GitHub auth and writes a sigstore cache, eval §5.1).

<!-- Source: Base (original, modified) — merged and deduplicated with Variant 1 (Option A) Strengths -->
## Strengths

- Real integrity check on every platform: build-time on Coder, install-time elsewhere, same source-pinned values.
- Deterministic: no "latest" resolution, no self-update, no upstream installer editing `~/.claude.json`, `~/.claude/settings.json` or `~/.claude/CLAUDE.md`.
- Guidance survives `./update.sh`, because it lives in the file IronClaude overwrites anyway.
- Telemetry and the update check are off explicitly, both in the image env and in the MCP entry.
- One place to bump; one code path covers linux and darwin on x64 and arm64.
- Up-to-date Coder workspaces start with codegraph on PATH: no first-run download, no per-home copy, works offline.
- On Coder the registered binary is root-owned and not writable by agents running as `coder`, matching the existing codebase-memory bake.

<!-- Source: Base (original, modified) — merged and deduplicated with Variant 1 (Option A) Weaknesses; resolved base weaknesses removed -->
## Weaknesses

- Most IronClaude code of the three options: download, hash table, extract, symlinks, receipt, removal, doctor checks and tests.
- Fallback machines (non-Coder, stale images) download 63 MB and write 286 MB under `$HOME`.
- A stale image makes the user-writable copy the registered binary until the image is rebuilt.
- The image still has to copy the pin and hash; a missed copy costs speed, not correctness.
- Upstream installer improvements (for example config migrations) are missed unless copied; the drift test only flags them.

<!-- Source: debate A-001, A-004, A-005 and advocate concessions — merged per Change 12 -->
## Conditions and risks attached by the debate

- **A-001:** per-worktree `codegraph init` needs a named owner. It is a separate follow-up decision, not part of this one (eval §4).
- **A-004:** a newer client talking to an older running daemon is untested; Change 8's warning is a mitigation, not proof.
- Maintaining 4 hashes per release, at about 8 releases per quarter observed (eval §1).
- Single-maintainer upstream (eval §1).
- Image growth of about 286 MB uncompressed (eval §5.2).
- Fallback machines depend on GitHub availability at install time; Coder depends on it only at image build (A-005).
- The registered absolute path must be re-registered whenever the winning binary changes (A-003).

<!-- Source: refactor-plan.md, Changes NOT Being Made -->
## Rejected alternatives

- **Delegate acquisition to upstream `install.sh`** (Option B; C-001, C-002): no checksum step (`install.sh:71-82`), and a prior hash check cannot cover bytes from a separate download.
- **`codegraph install --target=claude --location=global --yes`** (Option B; X-001, C-003): edits `~/.claude.json`, `settings.json` and `CLAUDE.md`, and `--force` erases the block (`install_core.py:62-71`).
- **Install the prompt hook** (Option B; C-005): adds context nobody chose (eval §5.9). Can be revisited later as an explicit opt-in.
- **User-writable `~/.local/bin` everywhere, Coder included** (Option A; C-007): an `alwaysLoad` binary runs every session, so the root-owned baked copy is preferred whenever its version matches.
- **`gh attestation verify` as part of the check** (Option A; U-001): needs GitHub auth and writes under `$HOME` (eval §5.1). Optional and non-blocking only.

<!-- Source: debate-transcript.md Convergence Assessment and base-selection.md Combined Scoring -->
## Debate summary

Convergence 100% (22/22, threshold 80%, depth quick, 1 round); base scores C 0.879, A 0.808, B 0.752.
