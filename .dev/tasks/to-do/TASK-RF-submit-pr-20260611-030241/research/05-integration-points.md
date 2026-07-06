# R5 Research — Integration Points (sc:submit-pr Wiring)

**Status: In Progress**

**Topic:** How the new `sc:submit-pr` skill wires into the harness and repo machinery —
Monitor tool arming, /sc:troubleshoot runtime invocation, command↔skill registration/sync,
and gh/git discipline surfaces.

**Spec:** `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`
(FR-1.5/FR-2.4 Monitor arming, FR-2.1 gh poll, FR-3.2/3.3 route to /sc:troubleshoot, §11 run-log, §19 SoT/PR-target)

---

## TL;DR / Decision Flags

1. **Monitor harness tool arming from a SKILL.md: FEASIBLE but with a hard caveat.** The Monitor
   harness tool IS a real tool available to the orchestrating agent (the same agent that runs the
   skill in-session). A SKILL.md can instruct that agent to call `Monitor` with `poll-augment-review.sh`.
   **However** the spec's own framing is correct and honest: the monitor is **in-session** and
   **session close = monitor lost** (FR-2.4, spec:181). The Monitor tool runs for the lifetime of the
   *session*, not detached from it. The skill is NOT a Python CLI that backgrounds a daemon — it is an
   agent-driven, in-session orchestration. This is consistent with how the spec already scopes it
   (`--resume` from JSONL is the documented mitigation, NOT true detachment). **No existing skill in
   this repo arms the Monitor harness tool** — this would be the first. See §1 below for the realistic
   mechanism and the caveat.

2. **/sc:troubleshoot runtime invocation: well-established pattern.** Skills invoke other skills via
   the **Skill tool** (`> Skill <name>` directive in SKILL.md prose, executed by the orchestrating
   agent). `sc:troubleshoot` is reachable two ways: (a) the command `/sc:troubleshoot` (activates
   `sc:troubleshoot-protocol` skill), or (b) directly invoking the `sc:troubleshoot-protocol` skill via
   the Skill tool. Multiple precedents exist (auggie-review→task-builder, roadmap→adversarial,
   troubleshoot→task-builder/reflect). See §2.

3. **Registration is purely file-presence + sync.** A new `/sc:submit-pr` needs exactly two source
   files: `src/superclaude/commands/submit-pr.md` (command) + `src/superclaude/skills/sc-submit-pr-protocol/SKILL.md`
   (protocol skill). `make sync-dev` mirrors them to `.claude/`; `make verify-sync` + `make lint-architecture`
   enforce the pairing. `superclaude install` enumerates by glob/iterdir — no manifest edit needed.
   See §3.

4. **gh/git discipline is binding and already codified** in CLAUDE.md AND duplicated in spec §19. See §4.

---

## §1 — Monitor Tool Arming Reality (FR-1.5, FR-2.4)

### 1.1 What the spec claims
- FR-1.5 (spec:169): "On `--monitor >= 1`, arm Monitor (initialize output-dir, run-log, baseline)
  after PR URL verification." Tests T-109 (Monitor spawned exactly once) / T-110 (never spawned at L0).
- FR-2.4 (spec:181): "**Monitor hosted by Monitor tool; session close = monitor lost** (documented
  limitation, mitigated by `--resume`, §12). T-230: close session mid-poll → run-log records
  `session_closed`; resume reconstructs (no code assertion beyond logging + resume)."
- §1.1 (spec:34-37): "an **in-session** Monitor-driven loop … Arms an **in-session monitor (hosted by
  the Monitor tool)** that polls for the Augment Code GitHub App review."
- The poller (spec:102, C2): `poll-augment-review.sh` — "single poll → emits one JSON line (Monitor stream)".

### 1.2 The realistic mechanism (and the honesty flag)

**FINDING — the Monitor "tool" the spec names is the harness `Monitor` tool, NOT a Python construct.**
The "Monitor" hits inside this repo's skills are a RED HERRING for this question:
- `sc-cli-portify-protocol` references a Python `OutputMonitor` class / `MonitorState` dataclass that
  generated CLI code uses (`src/superclaude/skills/sc-cli-portify-protocol/refs/code-templates.md:185,515`,
  `refs/pipeline-spec.md:130-136,322`). That is **time.sleep() polling inside a synchronous Python CLI**
  (`SKILL.md:423`), not the harness Monitor tool. Different thing entirely.
- **There is NO existing skill or command in `src/superclaude/` that instructs the orchestrating agent
  to call the harness `Monitor` tool or use `run_in_background`.** Grep across all skills/commands/agents
  for "Monitor tool" / "run_in_background" returns zero in-skill orchestration usages. `sc:submit-pr`
  would be the **first** skill to drive the harness Monitor tool. (Evidence: repo-wide grep, only the
  Python-OutputMonitor textual matches surfaced.)

**The harness `Monitor` tool is real and available to the in-session orchestrating agent** (it is in
the toolset of the agent that executes a skill). Its documented contract: it runs a shell command whose
each stdout line becomes a notification/event; `persistent: true` runs it for the lifetime of the
session; it is **stopped by TaskStop or session end**. This maps EXACTLY onto the spec's design:
`poll-augment-review.sh` emits one JSON line per poll → each line is a Monitor event.

**REALISTIC MECHANISM for the SKILL.md:** The SKILL.md instructs the orchestrating agent (in prose, the
same way `sc-troubleshoot-protocol` instructs `> Skill task-builder`) to:
1. After PR-URL verification, write the run-log + baseline (agent-driven Bash/Write).
2. Call the **`Monitor` tool** with `command` = the poll loop wrapper around `poll-augment-review.sh`
   (interval ≥30s, timeout default 1800s), `description` = "Augment review on PR #N", and an event
   filter that emits terminal states (review_detected / clean / timeout) per the Monitor-tool coverage
   guidance ("silence is not success").
3. On each emitted event line, the agent reads it, advances the FSM (S2_CLASSIFY etc.), and — when
   findings are verified — routes to `/sc:troubleshoot` (§2).

**HONESTY FLAG (mandatory per task brief):** Whether the SKILL.md drives a **`Monitor`-tool stream** vs a
**plain in-session Bash polling loop** (`Bash run_in_background` with an `until grep` script) is largely
a presentation choice — BOTH are in-session and BOTH die on session close. The spec's "mitigated by
`--resume`" + JSONL write-ahead log (§11) is what actually gives durability, NOT the Monitor tool. The
Monitor tool gives *event-streamed notifications back to the agent mid-session* (so the agent can
interleave classification/troubleshoot dispatch with polling), which the spec's FSM needs. A pure
synchronous Bash loop would block the agent between polls; the Monitor tool (or `Bash run_in_background`)
does not. So the Monitor tool IS the right primitive for the spec's interleaved FSM — but the
implementer must NOT over-promise detachment. **The skill cannot survive its own session**; that is a
true V1 limitation the spec already names (FR-2.4, §12, R3 risk spec:1006). The task file should keep the
spec's honest framing and NOT imply a daemon.

**Note on subagents:** Per project memory (`reference_subagent_cannot_nest_skill_fanout.md`), the
Monitor tool and the FSM driving must run at the **top-level orchestrating agent**, not inside an
Agent-tool subagent that itself spawns skills. The `sc:submit-pr` SKILL.md must be activated in the main
session loop so it has access to the `Monitor` tool and can call `> Skill sc:troubleshoot-protocol`.

---

## §2 — /sc:troubleshoot Runtime Invocation (FR-3.2, FR-3.3)

### 2.1 How one skill invokes another skill/command (the mechanism)
The orchestrating agent invokes another skill via the **Skill tool**, expressed in SKILL.md prose as a
`> Skill <name>` directive. Confirmed precedents:
- `sc-troubleshoot-protocol/SKILL.md:365`: "Invoke `/sc:adversarial` in compare mode via `Skill`".
- `sc-troubleshoot-protocol/SKILL.md:445`: Tier 3 — "invoke the `task-builder` skill **via `Skill`**".
- `sc-troubleshoot-protocol/SKILL.md:465` (tool table): `Skill` tool used for `sc:adversarial-protocol`,
  `task-builder`, `/sc:reflect`.
- `tdd/SKILL.md:411` / `prd/SKILL.md:420` / `tech-reference/SKILL.md:531`: "**Invoke /task using the
  Skill tool** with `skill: "task"` and `args` set to the task file path".
- `sc-roadmap-protocol/refs/adversarial-integration.md:161`: "All invocations use the `Skill` tool …
  Arguments are passed as a string to the Skill tool's `args` parameter."
- `sc-auggie-review-protocol/refs/remediation-handoff.md:75`: `> Skill task-builder`.

So `sc:submit-pr` routes a verified finding by invoking, via the Skill tool, either:
- the command surface `/sc:troubleshoot` (which itself activates the protocol skill — see 2.2), or
- the protocol skill directly: `Skill sc:troubleshoot-protocol` with `args` describing the finding/fix.

The troubleshoot skill is registered as `sc:troubleshoot` / `sc:troubleshoot-protocol` (confirmed in the
session's available-skills list). Its description self-activates on "a pasted stack trace" / failing
command — but `sc:submit-pr` should invoke it **explicitly via the Skill tool** (deterministic), not rely
on keyword auto-activation.

### 2.2 Command→skill delegation (the Activation pattern)
Every `/sc:<x>` command file delegates to its protocol skill via a mandatory **`## Activation`** section.
Canonical example — `src/superclaude/commands/auggie-review.md`:
- Behavioral Flow (head ~line 60): "Hand off to the skill via the Activation section below".
- `## Activation`: "**MANDATORY**: Before executing any protocol steps, invoke: `> Skill
  sc:auggie-review-protocol`. Do NOT proceed with protocol execution using only this command file."

The command file is a thin shell (triggers, flags table, required input, boundaries); the **behavioral
body lives in the skill**. `/sc:submit-pr` command must contain `> Skill sc:submit-pr-protocol`.

**How sc commands map to protocol skills / MCP listing:** The mapping is name-derived:
`commands/<x>.md` ⇄ `skills/sc-<x>-protocol/`. The install layer (§3) keeps protocol skills installed
standalone precisely so the `> Skill sc:<x>-protocol` activation resolves (install_skills.py docstring,
spec'd in §3.2). There is no separate registry file — discovery is by directory/glob.

### 2.3 The troubleshoot handoff contract `sc:submit-pr` must respect
`sc-troubleshoot-protocol` Tier 3 is **opt-in and user-gated** by design
(`SKILL.md:445-448`, `refs/remediation-handoff.md:96`): it builds an MDTM task file then **STOPS** — the
user runs `/task`, the skill never auto-executes. **Implication for `sc:submit-pr` at L2/L3:** when
`sc:submit-pr` invokes troubleshoot to *fix* (not just diagnose), it must drive troubleshoot in a mode
that yields an applied fix in the worktree, OR `sc:submit-pr` applies the fix itself from troubleshoot's
diagnosis. The spec's FSM (`S3_DIAGNOSE → S3_FIXING`, spec:266-280) expects edits to land in a worktree
at ordinal ≥2; troubleshoot's default Tier-3 chain does NOT apply edits. The task-builder/implementer must
reconcile: `sc:submit-pr` likely uses troubleshoot for *diagnosis* (Tier 1/2 REPORT.md) and performs the
*edit application* within its own FSM, since troubleshoot deliberately refuses to auto-apply. This is a
real integration seam to flag for the spec author / task design.

---

## §3 — Command↔Skill Registration + Install/Sync (what must exist)

### 3.1 The two source files (Source of Truth = `src/superclaude/`)
For `/sc:submit-pr` to be discoverable, create in `src/superclaude/`:
1. `src/superclaude/commands/submit-pr.md` — command (frontmatter `name: submit-pr`, flags table,
   `## Activation > Skill sc:submit-pr-protocol`).
2. `src/superclaude/skills/sc-submit-pr-protocol/SKILL.md` (+ `refs/`, `scripts/`, `templates/` as needed,
   e.g. `scripts/poll-augment-review.sh`, `refs/state-machine.md`, `refs/severity-routing.md`,
   `refs/loop-guard.md` per spec:97-105).

### 3.2 sync-dev mirroring (Makefile)
`make sync-dev` (Makefile:108-135):
- copies each `src/superclaude/skills/*/` (excluding `__init__.py`/`__pycache__`) → `.claude/skills/<name>/`
  (Makefile:112-123);
- copies `src/superclaude/agents/*.md` → `.claude/agents/` (Makefile:126-129);
- copies `src/superclaude/commands/*.md` → `.claude/commands/sc/<name>` (Makefile:131-135).
So after adding the two source files, `make sync-dev` auto-mirrors them — **no Makefile edit required**.

### 3.3 verify-sync + lint-architecture gates
- `make verify-sync` (Makefile:166+) bidirectionally diffs src ⇄ .claude for skills/agents/commands and
  fails on drift or on a `.claude/skills/<x>/` with no SKILL.md (Makefile:194). Run before committing.
- `make lint-architecture` (Makefile:361+) enforces:
  - Check (Makefile:369-374): every `commands/*.md` referencing a skill must have the skill dir present.
  - Check (Makefile:382-385): every `skills/sc-*-protocol/` must have a paired `commands/<x>.md`.
  - Check 6 "Activation Section Present" (Makefile:410-414): every `skills/sc-*-protocol/` must have its
    command file carry the Activation section.
  **⇒ `sc-submit-pr-protocol` and `commands/submit-pr.md` MUST be added together** or lint-architecture
  fails. Naming must be exactly `sc-submit-pr-protocol` ⇄ `submit-pr.md`.

### 3.4 `superclaude install` enumeration (no manifest)
- `install_commands.py:37` enumerates `command_source.glob("*.md")` → installs to `~/.claude/commands/sc/`.
  Pure glob; the new command is auto-picked-up.
- `install_skills.py` (`list_available_skills` + `install_all_skills`) iterates available skills; the
  `_has_corresponding_command()` helper (install_skills.py:29-46) strips **ONLY** the `sc-` prefix (NOT
  `-protocol`). **Critical policy (install_skills.py:12-21 docstring):** protocol skills named
  `sc-<command>-protocol` are **INTENTIONALLY installed standalone** because each command activates its
  skill via `> Skill sc:<command>-protocol`; the matcher must NOT strip `-protocol` or the activation
  breaks. `sc-submit-pr-protocol` → strips to `submit-pr-protocol`, which does NOT match
  `commands/submit-pr-protocol.md` (doesn't exist), so it is correctly installed standalone. **No code
  change to install_skills.py is needed** — the existing policy already covers a new protocol skill.
  Regression guard: `tests/unit/test_cli_install.py` (cited install_skills.py:21).

### 3.5 Summary — discoverability checklist for `/sc:submit-pr`
| Requirement | Mechanism | Action needed |
|---|---|---|
| Command file | `commands/submit-pr.md` glob-installed | CREATE |
| Protocol skill | `skills/sc-submit-pr-protocol/` iterdir-installed standalone | CREATE |
| Activation pairing | `## Activation > Skill sc:submit-pr-protocol` | INCLUDE in command |
| Dev mirror | `make sync-dev` (auto, no edit) | RUN |
| Parity gate | `make verify-sync` | RUN before commit |
| Arch gate | `make lint-architecture` (pairing + Activation) | RUN |
| Install enumeration | glob/iterdir; `_has_corresponding_command` strips only `sc-` | NO code change |

---

## §4 — gh/git Discipline Surfaces the Skill MUST Obey

Binding rules, cited. These appear in **two** authoritative places (CLAUDE.md = global binding;
merged-spec §19 = spec-internal restatement). The skill/poller/dispatcher must encode them.

### 4.1 PR-target = fork, never upstream (CLAUDE.md §"PR Target")
- `CLAUDE.md:35` — "ABSOLUTE RULE: PR Target = Fork (`IronbellyOrg/IronClaude`), NEVER Upstream".
- `CLAUDE.md:37` — `origin` = `IronbellyOrg/IronClaude`; `upstream` = `SuperClaude-Org/SuperClaude_Framework`.
- `CLAUDE.md:41` — bare `gh pr create` (no `--repo`) is FORBIDDEN (gh defaults to the parent/upstream).
- `CLAUDE.md:49` — mandatory shape: `gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "..." --body "..."`.
- `CLAUDE.md:54` — pre-PR: `git remote -v` confirm origin = `IronbellyOrg/IronClaude.git`.
- `CLAUDE.md:56` — post-PR: verify returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/N`;
  wrong owner ⇒ close immediately + reopen with `--repo`.
- **Spec restatement** spec §19.2 (spec:~): every `gh` call pins `--repo IronbellyOrg/IronClaude`; push
  target is `origin`, never `upstream`. (Also FR-1.4 spec:168, FR-2.1 spec:178 already pin
  `--repo IronbellyOrg/IronClaude` on the poll calls; FM-11/T-... misrouted-URL → `terminal_failed`,
  spec:791.)
- **NFR-6 purity** (spec:806): FSM/router/loop-guard contain ZERO `gh`/`git` tokens — all `gh`/`git` I/O
  is isolated to poller/dispatcher/helper/validator. The skill's deterministic core must stay gh/git-free.

### 4.2 Never stage/commit `.claude/` except settings.json (CLAUDE.md §"Never Stage")
- `CLAUDE.md:16` — "ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents".
- `CLAUDE.md:18` — `.claude/{skills,commands,agents,hooks,templates}/*` are gitignored sync-dev output;
  ONLY `.claude/settings.json` is tracked.
- `CLAUDE.md:22` — never `git add .claude/skills|commands|agents|hooks|templates`.
- `CLAUDE.md:29` — exception ONLY `.claude/settings.json`.
- `CLAUDE.md:31` — `git add -f` on a `.claude/` path is the violation siren → STOP.
- **Spec restatement** §19.1 (spec:~): edits originate in `src/superclaude/`; `make sync-dev` regenerates
  `.claude/`; `make verify-sync` before commit; an `-f` on `.claude/` is the siren.
  **⇒ When `sc:submit-pr` stages a fix it produced, it must `git add` only `src/superclaude/` paths
  (+ `.claude/settings.json` if relevant), NEVER the mirrored `.claude/` paths**, and run sync-dev so the
  committed change is the source side. This is a live concern because the skill auto-pushes at L3.

### 4.3 Commit trailer
- Per harness/global convention (SuperClaude global CLAUDE.md "Git" section): git commit messages end with
  the `Co-Authored-By:` trailer. The dispatcher that creates remediation commits at L2/L3 should append
  the project's standard commit trailer. (Project CLAUDE.md does not itself pin a specific trailer string;
  the global instruction supplies `Co-Authored-By: Claude ...`. The implementer should use the
  repo-conventional trailer — R2/conventions researcher owns exact string; flagged here as a surface, not
  re-derived.)

### 4.4 Feature-branch / never-commit-to-master
- Global CLAUDE.md Core Rule 4: "Git — feature branches only; never commit directly to master/main."
- Project CLAUDE.md Git Workflow: `master` ← `integration` ← `feature/*`. `sc:submit-pr` pushes to the
  PR's head branch (`--head <branch>`), never to `master`. The push triad (spec §12.1, INV-007) pushes
  `target_sha:<target_branch>` on `origin` — target_branch is the PR head, not master.

### 4.5 skill-creator eval workspace destination
- Spec §19.3 (spec:~) + project CLAUDE.md override: any `skill-creator` eval workspace for this skill goes
  to `.dev/eval-workspaces/sc-submit-pr/`, NEVER `.claude/skills/*-workspace/` (PreToolUse hook
  `reject-workspace-writes.sh` enforces; `.gitignore` matches). Relevant only if the skill is built via
  skill-creator.

---

## §5 — Run-Log / Resume Substrate Touchpoints (§11, §12) — wiring relevance

These are R3's contract domain, but the WIRING note: the run-log (`monitor-run-<PR>.jsonl`, spec:709) is
what makes the in-session Monitor tolerable. The skill writes write-ahead JSONL events (`monitor_armed`,
`poll_attempt`, `poll_result`, `push_decision`/`push_initiated`/`push_completed` triad, spec:724-727,
§12.1) via agent-driven Bash/Write at each FSM transition; `--resume <abs-run-log-path>` (FR-1.7 spec:171)
reconstructs state from JSONL when the session was lost. Default output-dir
`/config/workspace/IronClaude/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/` (spec:715). This is the durability
layer that compensates for the Monitor tool's session-bound nature (the §1 honesty flag).

---

## §6 — Open Integration Risks to Flag for Task Design

1. **Monitor-tool ≠ daemon (re-stated).** The task file MUST NOT imply detachment. Keep FR-2.4's
   "session close = monitor lost" honest framing. The Monitor tool gives interleaved in-session event
   streaming, not background survival. (Confidence: high — Monitor tool contract is session-bound;
   spec already concedes this.)
2. **Troubleshoot won't auto-apply edits.** `sc-troubleshoot-protocol` Tier 3 deliberately stops at an
   MDTM task file (user runs `/task`). `sc:submit-pr` at ordinal ≥2 needs edits IN the worktree. Resolve:
   use troubleshoot for diagnosis (REPORT.md) and apply edits within `sc:submit-pr`'s own FSM, OR drive a
   different fixing path. **This is the single biggest wiring seam** — flag to spec author. (Confidence:
   high — confirmed via SKILL.md:445-448 + remediation-handoff.md:96.)
3. **Top-level activation required.** The skill must run in the main session loop (Monitor tool access +
   `> Skill` nested invocation). Do NOT design it to run inside an Agent-tool subagent
   (`reference_subagent_cannot_nest_skill_fanout.md`). (Confidence: high.)
4. **No install-layer code change needed**, but naming is load-bearing: exactly `sc-submit-pr-protocol`
   ⇄ `submit-pr.md`, with the Activation section, or `make lint-architecture` Check 6 fails. (Confidence:
   high — Makefile:382-414, install_skills.py:12-46.)
5. **gh/git purity boundary** (NFR-6): keep FSM/router/loop-guard free of `gh`/`git`; isolate to
   poller/dispatcher/validator. The `--repo IronbellyOrg/IronClaude` pin + `origin`-only push + never-stage-`.claude/`
   discipline live in those I/O modules. (Confidence: high.)

---

**Status: Complete**

### Summary
- **Monitor tool arming is FEASIBLE from the SKILL.md** (the harness `Monitor` tool is available to the
  in-session orchestrating agent; `sc:submit-pr` would be the *first* skill to use it — no prior art).
  **Honest caveat flagged:** it is in-session only; "session close = monitor lost" is a true V1 limitation
  the spec already concedes (FR-2.4). The `--resume` + write-ahead JSONL run-log (§11/§12), not the
  Monitor tool, provides durability. The repo's other "Monitor" references (cli-portify) are an unrelated
  Python `OutputMonitor` class.
- **/sc:troubleshoot is invoked at runtime via the Skill tool** (`> Skill sc:troubleshoot-protocol` or
  the `/sc:troubleshoot` command, which activates the same skill). Pattern is well-precedented. **Seam
  flagged:** troubleshoot won't auto-apply edits, so `sc:submit-pr` must own edit application at L2/L3.
- **Registration = two source files** (`commands/submit-pr.md` + `skills/sc-submit-pr-protocol/`) +
  `make sync-dev`/`verify-sync`/`lint-architecture`. `superclaude install` glob/iterdir auto-discovers;
  the protocol-skill standalone-install policy already covers it (no install code change).
- **gh/git discipline** is binding and doubly-codified (CLAUDE.md:16,35 + spec §19): `--repo
  IronbellyOrg/IronClaude` on every gh call, push to `origin` not `upstream`, never stage `.claude/`
  except settings.json, feature-branch-only, commit trailer. NFR-6 keeps the deterministic core gh/git-free.
