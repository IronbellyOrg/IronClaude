# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (18 of 18 diff points agreed; 13 unanimous, 5 by 2/3 majority)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (Mode A, one per input file, current model, read-only general-purpose agents)
- Every advocate read `../../context.md`, all three variants and `diff-analysis.md` (confirmed in each statement's file list)
- Taxonomy coverage gate: L1 covered (S-001, C-008), L2 covered (S-002, C-001, C-003, C-004, C-005, C-007, C-009, X-002, A-005), L3 covered (C-002, C-006, C-010, X-001, A-003, A-004, A-006). No forced round needed.
- Shared-assumption omissions: none (all three advocates answered A-003..A-006)

## Round 1: Advocate Statements

### Variant 1 Advocate (option-a, persona architect)

**Position:** Ship no automation, only the core CLAUDE.md rule plus a docs page; Coder owns worktree creation and codegraph's own guards (refuses `$HOME`//, re-init is a no-op) make the rule safe. Treat B as a later opt-in.

**Steelman V2:** only option that works on every machine and is per-worktree by construction; no global writes (C-004); good guards (U-002, U-003, U-001); detached so no agent turn waits (C-007); most implementable (S-002).
**Steelman V3:** only option that indexes before any session (U-006) and keeps fresh with no MCP client (U-005), the one freshness path not depending on A-004.

**Strengths claimed:**
1. Smallest correct code (C-009): text only vs B's script + hooks.json + plugin mirror + `_FRESHNESS_SCRIPTS` + test pin (context.md).
2. Mid-session init is safe: MCP server "re-checks per call" (evaluation §4); re-init is a ~125 ms no-op; init refuses home/root (context.md).
3. Guidance must live in core CLAUDE.md because `superclaude install --force` overwrites `~/.claude/CLAUDE.md` (evaluation §2); B and C both reuse A's rule (C-008).
4. The no-sync rule (U-008) matches the verified lock failure.
5. No global state (C-004).
6. Indexes only repos actually used (A-005).

**Weaknesses in others:**
1. B step 3 relies on A-003: an OOM-killed init (~1 GB peak) may leave a DB and be skipped forever, silently.
2. B indexes every git repo opened (A-005 unstated).
3. B's `mkdir` lock does not cover a concurrent Coder init (UNVERIFIED behaviour).
4. B still needs A's rule.
5. C self-contradicts (X-001).
6. C mutates global `init.templateDir`; misses `core.hooksPath` users; nothing for existing clones; foreground cost; no uninstall.

**Concessions:** outside Coder nothing automates; the first agent pays a turn (4.5 s to ~100 s) or forgets (A-006); B beats A on C-003, C-007, S-002.

**Shared assumptions:** A-003 QUALIFY (A triggers on a tool reply, not file existence; whatever ships should check index state). A-004 QUALIFY (registration must ship alongside). A-005 REJECT (no evidence users want every repo indexed). A-006 QUALIFY (MCP wording unverified; widen the rule).

**Recommended shape:** ship A now; pair with MCP registration; B later as opt-in (`SUPERCLAUDE_CODEGRAPH_AUTOINIT=1`) after A-003 and Coder overlap are checked; reject C.

### Variant 2 Advocate (option-b, persona backend)

**Position:** A SessionStart hook that backgrounds `codegraph init --yes` is the only option that indexes existing clones and sibling worktrees on any machine without global git config. As written it has one real integrity gap (DB existence as completeness proof, A-003) and a stale-able `mkdir` lock; both are fixable in a few lines.

**Steelman V1:** zero code and failure modes; cost only where queried; failures surface in the foreground; contributes U-008, backed by evaluation line 224 ("Sync could not acquire the file lock").
**Steelman V3:** indexes before any session (U-006); covers pulls/branch switches with no MCP client (U-005); tool-agnostic.

**Strengths claimed:**
1. Coverage (C-003): `git rev-parse --show-toplevel` on first session covers sibling worktrees and existing clones.
2. No global state (C-004).
3. Boundary guards (C-010, U-002) match init's own refusal.
4. Fits existing machinery (`hooks.json` SessionStart, `_FRESHNESS_SCRIPTS` `install_hooks.py:42-79`, test pin).
5. Opt-out (C-005).

**Weaknesses in others:**
1. V1 leaves every worktree unindexed and depends wholly on A-006.
2. V3 X-001.
3. V3 misses `core.hooksPath` users; template hooks are frozen at clone time, so fixes never reach existing checkouts.
4. V3 foreground cost unspecified (C-007).

**Concessions:**
1. The `codegraph.db` check is not robust to an interrupted init (A-003; partial DB left behind is UNVERIFIED but likely); worse than V1 where failure is visible.
2. A bare `mkdir` lock goes stale on kill.
3. The hook could be smaller: init is a ~125 ms no-op when indexed (partial-index behaviour UNVERIFIED).
4. Possible race with the MCP daemon started at the same session (watcher pickup UNVERIFIED).
5. V1 is right on cost (A-005).

**Shared assumptions:** A-003 REJECT (clean up after failed init; probe a killed init). A-004 QUALIFY. A-005 QUALIFY (acceptable only with the opt-out). A-006 QUALIFY (cover any codegraph tool error; `status` exits 0 when not initialized).

**Recommended shape:** keep V2 guards; fast path on DB existence; lock with liveness; fully detached init with `</dev/null` and output redirected (otherwise Claude Code waits); clean up on failure; adopt V1's rule and docs page; reject V3.

### Variant 3 Advocate (option-c, persona devops)

**Position:** C is the only design that indexes before any session; git `post-checkout` runs after clone and after `git worktree add` (git 2.47.3 manual). On the evidence, B is the better default; C's value is as an opt-in recipe, not installer behaviour.

**Steelman V1:** no code, no failure modes, upstream's own freshness design; U-008 is the one rule consistent with the lock.
**Steelman V2:** reaches every checkout opened in Claude on any machine; fail-open; concrete guards; follows the existing hook pattern.

**Strengths claimed:**
1. Earliest trigger (U-006), so no first-turn race.
2. Tool-agnostic.
3. Existing clones can be fixed by re-running `git init` (git-init manual), so C-003 "nothing until re-clone" is overstated (still manual per clone).
4. No `core.hooksPath` conflict in this repo (`git config --get core.hooksPath` empty); general case UNVERIFIED.

**Weaknesses in others:** V1 puts cost in an agent turn and depends on A-006; V2 can still show "not initialized" in the first session and carries more maintenance than its bullets suggest; V2 and V3 share A-003.

**Concessions:** X-001 is real, and a hook's exit status becomes `git checkout`'s, so an unswallowed lock error would fail checkout: drop the sync half (connect-time catch-up already covers between-session branch switches, so U-005 adds little). C-004 is a new class of side effect; "only when unset" silently no-ops for users with a template dir. C-003, C-005, C-010 gaps. C is worst on A-005 (indexes every clone). C has the largest maintenance surface (C-009).

**Shared assumptions:** A-003 QUALIFY (probe before relying on file existence). A-004 QUALIFY (`superclaude doctor` could check registration). A-005 QUALIFY (only behind an opt-out; B's scope defensible, C's not). A-006 QUALIFY (capture the real MCP reply text).

**Recommended shape:** ship B's hook with a completeness safeguard; keep A's rule and docs page; offer C only as a documented opt-in `post-checkout` recipe (`codegraph init --yes`, backgrounded, `|| true`, never `sync`); installer never writes global git config.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie | 95% | Cosmetic; all agree. |
| S-002 | L2 | V2 | V2 | V2 | V2 | 95% | Only V2 is specific enough to build and test. |
| C-001 | L2 | V2 | V2 | V2 | V2 | 92% | Automatic, no agent turn, no global config; V3 earlier but narrower. |
| C-002 | L3 | V1/V2 | V1/V2 | V1/V2 | V1=V2 | 92% | Watcher + catch-up suffices; V3 sync fights the writer lock. |
| C-003 | L2 | V2 | V2 | V2 | V2 | 92% | First session covers any checkout; V3 needs clone or manual `git init`. |
| C-004 | L2 | V1/V2 | V1/V2 | V1/V2 | V1=V2 | 95% | V3 alone writes global git config. |
| C-005 | L2 | V2 | V2 | V2 | V2 | 90% | Only V2 has an opt-out. |
| C-006 | L3 | V2 | V2 | V2 | V2 | 80% | V2 has a lock, but all agree it needs liveness/staleness handling. |
| C-007 | L2 | V2 | V2 | V2 | V2 | 92% | Detached beats blocking an agent turn or `git clone`. |
| C-008 | L1 | tie | tie | tie | tie | 95% | All keep V1's rule. |
| C-009 | L2 | V1 | V1 | V1 | V1 | 95% | Docs only; V2 and V3 conceded. |
| C-010 | L3 | V2 | V2 | V2 | V2 | 92% | Explicit non-git / `$HOME` / `/` guards. |
| X-001 | L3 | V1 | V1/V2 | V1 | V1 | 90% | V1's no-sync rule is right; V3 conceded the contradiction. |
| X-002 | L2 | tie | tie | V2 | tie | 70% | Acceptable once, in background, with an opt-out; V1's cost point stays valid. |
| A-003 | L3 | V1 | V1 | tie | V1 | 80% | DB-existence skip can hide a partial index; V2 conceded (REJECT). |
| A-004 | L3 | tie | tie | V3 (marginal) | tie | 70% | All depend on MCP registration, decided elsewhere. |
| A-005 | L2 | V1 | V1 | V1 | V1 | 90% | V1 indexes only on demand; V2 acceptable only with opt-out. |
| A-006 | L3 | V2 | tie | tie | tie | 70% | MCP reply wording unverified for all; widen the rule to any codegraph error. |

Debate points won: V2 7, V1 4, V3 0, tie 7.

## Convergence Assessment
- Points resolved: 18 of 18
- Alignment: 100%
- Threshold: 80%
- Status: CONVERGED (taxonomy gate passed; invariant probe gate not applied at depth quick)
- Unresolved points: none
- Open verification items (agreed, not contested): what a killed `codegraph init` leaves behind and whether `init --yes` repairs it (A-003); behaviour of two concurrent inits; the MCP "not initialized" reply text (A-006). All UNVERIFIED; no advocate ran codegraph (read-only constraint).
