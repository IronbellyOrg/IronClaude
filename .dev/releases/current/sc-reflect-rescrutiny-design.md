# Design: `/sc:reflect` — Recommendation Re-scrutiny Phase

**Date:** 2026-04-29
**Status:** Design (pre-implementation)
**Source:** Output of `/sc:brainstorm` adversarial debate; merged Proposal A (recursive validation) + B-lite (session-fact pass) + C-conditional (external doc lookup).
**Implementation target:** `/config/.claude/commands/sc/reflect.md` (deployed copy) — and, per the global CLAUDE.md sync rule, propagated back to whichever `src/superclaude/commands/reflect.md` is the canonical source.
**Bug-of-record:** Reflect emitted `pct start 300` against a CTID the session had twice asserted to be a Proxmox template. Templates reject `start`. The reflection's validation pass treated its own emitted command as commentary, not as artifact-under-review.

---

## 1. Scope

This refactor adds **one new behavioral phase** to `/sc:reflect`: *Recommendation Re-scrutiny*. It runs between the existing **Reflect** and **Document** phases, and only when the reflection's output contains executable artifacts.

**In scope:**
- New phase definition with extract / session-fact / external-fact / decision-gate steps.
- Tool-coordination updates: in-context reasoning for conversation review (no new tool); `Read`/`Grep` for files-the-conversation-points-at; conditional `context7`/`WebSearch` hooks.
- Stakes stratification (LOW/MEDIUM/HIGH) for the decision gate so HIGH-stakes verbs block on hedge instead of annotating.
- Category-organized CLI verb allowlist covering hypervisor, container, k8s, VCS, package managers, frontend (Vite/Next/Nuxt/Expo/Flutter), Unreal Engine (UBT/RunUAT/commandlets), Unity (batchmode/unityhub), game build infra (steamcmd/butler), cloud CLIs, IaC, service mgmt, DB CLIs, HTTP/transfer, Jenkins DSL, filesystem-destructive.
- Audit-annotation format for cleared recommendations.
- Single-file edit to `reflect.md` (skill spec is behavioral; no separate code module).

**Out of scope (deliberately):**
- Persistent entity registries / knowledge graphs across sessions.
- New MCP server dependencies beyond context7 (already global) and Grep/WebSearch (already global).
- Schema design for the session-fact set — it stays ephemeral, key/value, lives only inside one reflect call.
- Changes to other skills (`/sc:implement`, `/sc:task-unified`); those may benefit but are separate decisions.

---

## 2. Current vs. proposed behavioral flow

### Current (5 phases)
1. Analyze — examine current task and session progress.
2. Validate — assess task adherence and completion quality.
3. Reflect — apply deep analysis of collected information.
4. Document — update session metadata, capture insights.
5. Optimize — recommend process improvements.

### Proposed (6 phases)
1. Analyze.
2. Validate.
3. Reflect.
4. **Recommendation Re-scrutiny (NEW)** — gate any executable artifacts the previous phases produced.
5. Document.
6. Optimize.

---

## 3. Recommendation Re-scrutiny — phase specification

### 3.1 Activation

Phase activates if the reflection's draft output contains any of:
- Fenced code blocks tagged as `bash`, `sh`, `zsh`, `groovy`, `powershell`, `python`, or untagged but containing CLI invocations.
- Inline backtick commands of the form `<verb> <object>` against known external tools (allowlist below).
- Prose-embedded "run this" / "execute" / "you should run X" recommendations.

If none match, phase is a no-op and reflection proceeds straight to Document. **Most reflections will skip this phase entirely.**

### 3.2 CLI verb allowlist — by category

Verbs whose precondition checks are mandatory when targeting a named object. Organized by category to cover the surface across Unreal, Unity, frontend, and backend projects. Verbs not in this table bypass external-fact lookup but still go through session-fact pass.

| Category | Tools | Verbs requiring precondition check |
|---|---|---|
| Hypervisor / containers | `pct`, `qm`, `virsh`, `lxc` | start, stop, restart, exec, enter, mount, unmount, destroy, restore, snapshot, rollback |
| Container runtime | `docker`, `podman`, `docker compose`, `docker-compose` | run, exec, start, stop, kill, rm, push, pull, up, down, build (with `--push`), prune |
| Kubernetes / orchestration | `kubectl`, `helm`, `kustomize`, `kubeadm` | apply, delete, scale, rollout (restart/undo), drain, install, uninstall, upgrade, taint, cordon |
| VCS — state-changing | `git`, `p4`, `svn`, `hg` | push, push --force, reset --hard, rebase, branch -D, checkout (with `-f` or against dirty tree), merge, cherry-pick, p4 obliterate, p4 revert, p4 submit |
| Package managers | `npm`, `yarn`, `pnpm`, `bun`, `uv`, `pip`, `pipx`, `poetry`, `pdm`, `cargo`, `gem`, `composer` | install, uninstall, remove, publish, link, unlink, run (when script has side effects), update, audit fix |
| JVM / .NET build | `mvn`, `gradle`, `sbt`, `dotnet`, `nuget` | install, deploy, publish, release, push, restore (against private feeds) |
| Frontend build / dev | `vite`, `webpack`, `rollup`, `esbuild`, `parcel`, `next`, `nuxt`, `remix`, `astro`, `gatsby`, `expo`, `react-native`, `flutter`, `dart` | build, dev (with watch flags), start, deploy, export, eject, prebuild |
| Frontend test / lint with side effects | `eslint --fix`, `prettier --write`, `stylelint --fix`, `jest --updateSnapshot`, `vitest --update`, `playwright codegen`, `storybook build` | (any invocation that mutates files or pushes artifacts) |
| Unreal Engine | `UnrealBuildTool`/`UBT`, `RunUAT.bat`/`RunUAT.sh`, `UnrealEditor` (commandlets), `UnrealVersionSelector` | Build, BuildCookRun, Package, Cook, Deploy, Stage, Archive, ResavePackages, FixupRedirectors, MakeCookedEditor |
| Unity | `Unity` / `Unity.exe` (batchmode), `unityhub` | -batchmode -buildTarget, -executeMethod, -projectPath (with `-quit` mutating ops), unityhub install / uninstall, hub --headless install |
| Game build infra | `steamcmd`, `butler` (itch.io), Steamworks SDK tools | +login, +run_app_build, +app_update, push (butler), validate |
| Cloud CLIs | `aws`, `gcloud`, `az`, `doctl`, `linode-cli`, `oci`, `heroku`, `flyctl` | create, delete, terminate, deploy, update, scale, rollback, put-* (state-changing), modify-* |
| IaC | `terraform`, `pulumi`, `ansible`, `ansible-playbook`, `puppet`, `chef-client`, `salt`, `cdk` | apply, destroy, plan (with `-out` written or auto-approved), refresh, taint, import, deploy |
| Service mgmt | `systemctl`, `service`, `supervisorctl`, `launchctl`, `sc.exe` | start, stop, restart, enable, disable, mask, reload, daemon-reload |
| Database CLIs | `psql`, `mysql`, `mongosh`/`mongo`, `redis-cli`, `cqlsh`, `sqlite3`, `clickhouse-client` | (statements: DROP, DELETE without WHERE, TRUNCATE, ALTER on populated tables, FLUSHALL, FLUSHDB, GRANT/REVOKE) |
| HTTP / transfer | `curl`, `wget`, `httpie`/`http`, `scp`, `rsync` (with `--delete`), `sshfs`, `ssh` | -X POST/PUT/DELETE/PATCH against state-changing endpoints; rsync --delete; any ssh against a named host |
| CI / Jenkins (Groovy DSL via job config) | Jenkins pipeline steps | `currentBuild.result =`, `error(...)`, `archiveArtifacts`, `publishHTML`, `withCredentials` (when wrapping state-changing calls), `node('<label>')` (target-validity) |
| Filesystem destructive | `rm`, `mv` (overwrite), `dd`, `mkfs.*`, `parted`, `fdisk`, `gdisk`, `wipefs` | -rf, of= (dd), any |

The allowlist is expandable. New entries should be added when a re-scrutiny miss is observed for a verb not currently covered.

### 3.3 Extract step

For each candidate recommendation:
- Parse `(verb, object, flags)` tuples. Multi-line scripts produce a tuple per command.
- Resolve variable references where possible (`$CTID` from a heredoc array → concrete CTID).
- Output: an ordered list of tuples to scrutinize.

### 3.4 Session-fact pass (B-lite)

For each tuple's `object`:
- Perform an **in-context conversation review** — the assistant scans its own conversation history (already in context; no tool call needed) for assertions about the named object. This is reasoning, not Grep — Grep operates on files and is the wrong primitive for transcript scanning.
- Optional file-anchored augmentation: if the conversation references a config file, mirror file, or pasted log path that isn't already loaded, use `Read` (whole file) or `Grep` (pattern within file) to surface relevant content. The Grep here is for files-the-conversation-points-at, not for the conversation itself.
- Build an ephemeral key/value fact set: `object → list of asserted properties`.
  - Sources of assertions: explicit user statements ("CTID 300 is a template"), pasted command output (`basevol-300-disk-0` in zfs list ⇒ "300 has template-backed storage"), prior tool results in this session, contents of files the conversation has read.
- Lookup target properties relevant to the verb. For `pct start`, the relevant property is "is target a template?" For `git push --force` against a branch, the relevant property is "is branch protected? is it main?" For `npm publish`, "is the package version already on the registry?"
- The fact set is destroyed at the end of the reflect call. No persistence. No schema beyond key/value.

### 3.5 External-fact pass (C-conditional)

Trigger condition: tuple's `verb` is on the allowlist AND the session-fact pass returned no relevant property for the precondition the verb cares about.

Action:
- Resolve library/tool ID via `mcp__context7__resolve-library-id` (e.g., for `pct`, search "Proxmox VE" / "pct").
- Query `mcp__context7__query-docs` with the question: "preconditions for `<tool> <verb>` — what state must the target be in?"
- If context7 returns nothing, fall back to `WebSearch`: `<tool> <verb> <object-type> precondition`.
- Cache the result for the duration of the reflect call (don't re-fetch the same verb twice in one call).

External-fact pass NEVER runs if the session-fact pass already resolved the question — that's the "conditional" in the name and the cost-control point.

### 3.6 Decision gate — stratified by action stakes

Each tuple is first classified into a stakes tier based on the verb:

| Stakes tier | Definition | Example verbs |
|---|---|---|
| **LOW** | Read-only or trivially reversible. No filesystem, registry, or remote-state mutation. | `--version`, `list`, `status`, `log`, `get`, `describe`, `inspect`, `show`, `cat`, `ls`, `ps`, `df`, `free`, `nproc`, `pct config`, `kubectl get`, `git status`, `git log`, `docker ps` |
| **MEDIUM** | State-changing but reversible without lasting harm. Restartable, re-deployable, idempotent. | `start`, `stop`, `restart`, `set`, `update`, `apply` (when target is non-prod), `npm install`, `git checkout`, `pct set`, `systemctl reload`, `docker pull` |
| **HIGH** | Destructive, hard-to-reverse, or irreversible. Includes anything that loses data, mutates shared/published state, or burns credentials/identity. | `destroy`, `delete`, `rm -rf`, `dd of=`, `mkfs`, `force-push` (`git push --force`), `git reset --hard`, `git branch -D`, `p4 obliterate`, `kubectl delete`, `terraform destroy`, `npm publish`, `docker push` (to prod tag), `DROP TABLE`, `TRUNCATE`, `FLUSHALL`, `pct destroy`, `qm destroy`, cloud `terminate`/`delete-*` against prod |

Then apply the gate, with HIGH-stakes verbs blocking on hedge instead of annotating:

| Session-fact pass | External-fact pass | Stakes | Result |
|---|---|---|---|
| Confirms verb valid against object's known state | (skipped) | any | **PASS** — annotate `[verified: session]` |
| Reveals contradiction | (skipped) | any | **BLOCK** — surface contradiction, rewrite recommendation |
| Silent on relevant property | Confirms verb valid | any | **PASS** — annotate `[verified: docs/<source>]` |
| Silent on relevant property | Reveals contradiction | any | **BLOCK** — surface contradiction, rewrite recommendation |
| Silent | External-fact pass also silent or unavailable | LOW | **HEDGE** — annotate `[unverified: <reason>]`, recommend a verification step |
| Silent | External-fact pass also silent or unavailable | MEDIUM | **HEDGE** — annotate `[unverified: <reason>]`, recommend a verification step before action |
| Silent | External-fact pass also silent or unavailable | HIGH | **BLOCK** — refuse to ship the recommendation; demand a manual verification step from the user before retry |

**The reflection NEVER ships an unresolved contradiction.** It also **never ships an unverified HIGH-stakes recommendation** — those are blocked and handed back to the user as a flagged unknown. LOW and MEDIUM stakes recommendations may ship with `[unverified: ...]` annotation when neither pass can resolve them, because the cost of being wrong on those is bounded.

A blocked recommendation is replaced in the output by either (a) a verified alternative, or (b) the contradiction/unknown handed back to the user.

### 3.7 Output rewriting

When a tuple is BLOCKED:
- Original recommendation is removed from the output.
- Replacement is prefixed with `**Re-scrutiny caught:**` and includes:
  - The blocked verb+object.
  - The contradicting fact and its source (e.g., "user statement at message N: 'VMID 300 gs-template'").
  - A verified alternative if one is obvious; otherwise an open question for the user.

When a tuple PASSES:
- Recommendation is delivered with audit annotation appended (see §4).

---

## 4. Audit-annotation format

Every executable recommendation that survives re-scrutiny carries a tag at the end of its enclosing sentence or as a footnote, choosing the form that doesn't break copy-paste of the command itself:

**Format:** `[verified: <basis>]` where `<basis>` is one of:
- `session` — cleared by session-fact pass; relevant property found in conversation.
- `session+docs` — session-fact pass partially relevant, augmented by docs.
- `docs/context7` — cleared by context7 lookup.
- `docs/web` — cleared by WebSearch fallback.
- `unverified: <reason>` — could not clear; user must verify before running.

**Placement rules:**
- For inline backtick commands: tag at end of the sentence containing the command.
- For fenced code blocks: tag immediately after the closing fence, on its own line.
- For multi-command scripts: a single tag per script if all commands cleared on the same basis; otherwise a leading comment block summarizing per-command basis.

**Example (cleared):**
```bash
pct mount 300
pct unmount 300
```
`[verified: docs/context7 — pct(1): mount/unmount valid on stopped containers including templates]`

**Example (blocked → rewritten):**

> **Re-scrutiny caught:** Original recommendation included `pct start 300`. Session-fact pass: user message "VMID 300 gs-template exists" + zfs list line `basevol-300-disk-0` indicate CTID 300 is a Proxmox template. `pct(1)` rejects `start` against templates. Replacement: clone CTID 302 from 300 first, then start CTID 302 (canary-clone pattern). Original recommendation withdrawn.

---

## 5. Worked example — the `pct start 300` bug

**Reflection draft output (pre-re-scrutiny):**

```bash
pct start 300 2>/dev/null
sleep 2
pct exec 300 -- bash -c 'id gameserver; ...'
pct stop 300
```

**Re-scrutiny phase trace:**

1. **Activation:** detected fenced bash block → phase activates.
2. **Extract:** four tuples produced.
   - (`pct start`, `300`)
   - (`sleep`, `2`) — non-allowlist, skipped.
   - (`pct exec`, `300`)
   - (`pct stop`, `300`)
3. **Session-fact pass for object `300`:**
   - In-context review of conversation history surfaces: user message "VMID 300 gs-template exists" + earlier assistant tool result with zfs list containing `basevol-300-disk-0`.
   - Ephemeral fact: `300.type = template` (confidence high; two independent assertions).
4. **Verb-by-verb decision:**
   - `pct start` against `template` → context7 lookup `pct(1)`: "fails on templates with error 'CT N is a template'." → **BLOCK**.
   - `pct exec` against `template` → not strictly forbidden but requires the CT to be running, which a template can't be → **BLOCK** (transitive).
   - `pct stop` → moot once start is blocked → suppressed in rewrite.
5. **Output rewrite:**
   - The four-line block is removed.
   - Replacement explains the contradiction and recommends the canary-clone alternative (`pct clone 300 302 --full; pct start 302; pct exec 302 ...`).
6. **Audit annotation on the replacement:**
   - `[verified: session for object-state + docs/context7 for pct verb semantics]`

**Net effect:** The bug never reaches the user. The user sees a corrected recommendation with a transparent basis.

---

## 6. Tool coordination — additions

Existing reflect.md tool-coordination block lists Serena reflection tools and TodoRead/TodoWrite. The refactor adds:

| Tool | New role in reflect | When used |
|---|---|---|
| (in-context reasoning) | Scan current conversation history for assertions about a named object — performed by the assistant directly over its own context, not via a tool call | Session-fact pass, every activated re-scrutiny |
| `Read` / `Grep` | Augment session-fact pass when conversation references a config file, mirror file, or pasted log path that isn't already loaded | Session-fact pass, only when needed |
| `mcp__context7__resolve-library-id` + `query-docs` | Fetch verb preconditions for allowlisted CLI tools | External-fact pass, when session is silent |
| `WebSearch` | Fallback for verbs context7 doesn't cover | External-fact pass, when context7 is silent |

Performance impact:
- **Activated phase, session-fact pass only:** +1 in-context scan per object. Effectively free.
- **Activated phase, external-fact pass:** +1 context7 query per unresolved verb. Bounded by allowlist (currently 7 tools, ~30 verbs total).
- **Phase skipped:** zero impact; preserves the <200ms core reflection target for reflections with no executable output.

---

## 7. reflect.md spec-text changes (concrete)

The following sections of `/config/.claude/commands/sc/reflect.md` change. (Full diff deferred to `/sc:implement`; design records the targets.)

### 7.0 YAML frontmatter — declare new MCP dependency

Current:
```yaml
mcp-servers: [serena]
```
Change to:
```yaml
mcp-servers: [serena, context7]
```
(Add additional MCP entries here if `/sc:implement` introduces another lookup source — e.g., `tavily` if WebSearch is replaced by it.)

### 7.1 `## Behavioral Flow` — add phase between Reflect and Document

Insert after current step 3:

> 3.5. **Re-scrutinize**: For any executable artifacts produced (shell commands, code blocks, action recommendations), extract `(verb, object)` tuples; pass each through session-fact lookup; for allowlisted CLI verbs unresolved by session, fetch external preconditions via context7; block or rewrite contradictions before delivery. Skipped entirely when no executable artifacts are present.

### 7.2 `## MCP Integration` — add Context7

Append:

> - **Context7 MCP**: Conditional invocation during Recommendation Re-scrutiny for CLI verb precondition lookup when session-fact pass is silent.

### 7.3 `## Tool Coordination` — add Grep and WebSearch

Append:

> - **Grep**: Conversation-transcript scan for asserted facts about objects named in reflection-emitted recommendations.
> - **WebSearch**: Fallback CLI precondition lookup when Context7 doesn't cover the tool.

### 7.4 `## Key Patterns` — add re-scrutiny pattern

Append:

> - **Recommendation Re-scrutiny**: Extract executable artifacts → session-fact lookup → conditional external-doc lookup → decision gate (pass/block/hedge) → audit annotation.

### 7.5 `## Boundaries — Will`

Append:

> - Re-scrutinize executable artifacts emitted by the reflection itself before delivery.
> - Block reflection-emitted recommendations that contradict facts asserted in the current session or in authoritative external documentation.
> - Annotate every cleared recommendation with the basis on which it was cleared.

### 7.6 `## Boundaries — Will Not`

Append:

> - Maintain a persistent cross-session entity registry or knowledge graph; the session-fact set is ephemeral and lives only within one reflect call.
> - Block on hedge cases — when neither session nor external docs resolve a precondition question, surface the unverified status and recommend a check, but do not refuse to deliver.
> - Validate non-executable commentary, prose analysis, or reasoning narratives — only artifacts the user is expected to act on are in scope.

---

## 8. Performance budget

| Reflection scenario | Phase 4 cost | Total reflect call budget |
|---|---|---|
| No executable artifacts (most reflections) | 0 ms (phase skips) | unchanged, <200 ms |
| Executable artifacts, session resolves all | ~10 ms per object (in-context grep) | <250 ms typical |
| Executable artifacts, external lookup needed | ~500–1500 ms per uncovered verb | <2 s for typical 1–3 verb cases |

The <200ms target in the existing skill spec applies to "core reflection operations." Re-scrutiny is gated and explicitly opt-in by the presence of executable output, so the existing perf claim survives this change unchanged for the majority case.

---

## 9. Validation against /sc:brainstorm winning proposal

| Brainstorm requirement | Design fulfilment |
|---|---|
| A: trigger second look at emitted recommendations | §3.1 activation; §3.3 extract |
| B-lite: ephemeral session-fact pass, no persistent registry | §3.4 (ephemeral, destroyed end of call; in-context reasoning, not Grep) |
| C-conditional: external lookup ONLY when session is silent | §3.5 (gate condition specified) |
| Decision gate that never ships unresolved contradictions | §3.6 BLOCK row |
| Stakes-stratified gate — HIGH-stakes verbs block on hedge | §3.6 stakes tiers + per-tier gate behavior |
| Auditable basis for cleared recommendations | §4 annotation format |
| Allowlist covers project-relevant surface (Unreal, Unity, frontend, backend) | §3.2 category-organized table |
| Bounded scope — checkpoint skill, not knowledge graph | §1 explicit out-of-scope; §7.6 boundary |
| Catches the `pct start 300` bug | §5 worked example |

---

## 10. Implementation handoff

Next step: `/sc:implement` against this design document, applied to `/config/.claude/commands/sc/reflect.md`. Per the global CLAUDE.md component-sync rule, the same edit must propagate to the canonical source at `/config/.local/share/pipx/venvs/superclaude/lib/python3.12/site-packages/superclaude/_src/superclaude/commands/reflect.md` (or wherever the active SuperClaude install treats as source-of-truth — verify before editing). After both edits, run `make verify-sync` if the project's source tree is in scope, or perform a manual diff if the SuperClaude install is the only source.

Verification of the change: re-run the §5 worked-example scenario by hand-feeding the same draft output to a refactored `/sc:reflect` and confirm the bug is caught. No other functional regression test is needed; the phase is purely additive and skipped on reflections with no executable output.
