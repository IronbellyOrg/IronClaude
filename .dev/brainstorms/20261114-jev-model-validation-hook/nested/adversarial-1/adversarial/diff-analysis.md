# Diff Analysis: model-policy hook version 1 proposal comparison

## Metadata
- Generated: 2026-11-14 (UTC), Step 1 of /sc:adversarial, Mode A, `--depth standard`, `--convergence 0.75`
- Variants compared: 3 (A = `proposal-A.md` "layered model-policy hook, Lens A architect"; B = `proposal-B.md` "chokepoint and evidence"; C = `proposal-C.md` "policy and operations")
- Variant files: `adversarial/variant-1-original.md` (A), `variant-2-original.md` (B), `variant-3-original.md` (C)
- Agent specs assigned to advocates: A = `sonnet:architect`, B = `sonnet:analyzer`, C = `sonnet:backend` (no Opus anywhere)
- Total differences found: 70
- Categories: structural (6), content (26), contradictions (14), unique (20), shared assumptions (4 promoted)
- Taxonomy column `Lvl`: L1 surface, L2 structural, L3 state-mechanics (guard conditions, fail modes, boundaries). Auto-tagged by the highest matching level.
- Verification done while writing this file (read-only on product code; `.dev/eval-workspaces/` not touched): see "Facts verified in Step 1" at the end.

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity | Lvl |
|---|------|-----------|-----------|-----------|----------|-----|
| S-001 | Framing before section 1 | "0. Headline design": four-layer table (L0 floor, L1 hook, L2 launcher, L3 detective) plus the v1 property statement | No headline; three enforcement points C1, C2, C3 stated at the top of section 1 | No headline; goes straight to the E1-E9 event table | Low | L2 |
| S-002 | Event table granularity | 16 rows | 16 rows | 9 rows (E1-E9); folds frontmatter and alias rows together | Low | L2 |
| S-003 | Requirements list shape | 35 REQs; verification written as bracket text, mixed wording | 36 REQs; fixed method set: unit, integration, fixture replay, parity, manual | 40 REQs; almost all "[unit test]" | Medium | L2 |
| S-004 | Section 3 sub-structure | Code decides / residue / "Honest conclusion" / spec if enabled / offline test plan | Code decides / residue (a)(b)(c) / measured-need rule / spec if spike / offline replay | Code decides (about 95%, estimate) / residue / optional shadow call / offline test table | Low | L1 |
| S-005 | Where rollout lives | Section 8, four phases (0 to 3) | Section 8, 8-step order plus one rollout paragraph | Section 8, week-based rollout with per-event-class order and rollback | Low | L1 |
| S-006 | Chat-style trailer | None; "Not checked" folded into section 10 | Ends with a Status/Result table and a "Not checked" line | Ends with a Status/Result table and a "Not checked" line | Low | L1 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity | Lvl |
|---|-------|--------------------|--------------------|--------------------|----------|-----|
| C-001 | Enforcement layers | Four: L0 native floor, L1 hook, L2 Python `check_launch`, L3 detective post-run check of the observed model | Three: C1 Python helper, C2 hook, C3 native floor (coarse) | Hook plus launchers calling the hook script in `--check` mode; native list generation named in E7 but deferred in section 9 | High | L2 |
| C-002 | How Python launchers are covered | In-process function `check_launch(stage, model)` before every Popen; `superclaude model-policy check` for shell launchers | In-process `model_policy.py` with `resolve`, `check`, `build_flag`, `ModelPolicyError` | Launchers spawn `model-policy-guard.sh --check <stage> <model>` (about 40 ms per spawn) | High | L2 |
| C-003 | Launcher inventory and guarding new launchers | 4 sites (`process.py:163-164`, `tmux.py:194`, `prd/models.py:283`, `reflect/runner.py:508`), `summarizer.py:330` added in section 8; `eval/claude_process.py` not read; nothing stops a new unrouted launcher | 5 sites plus `reflect/commands.py:365`; REQ-29 test fails if a raw `"--model"` appears in an argv builder outside the helper | `tmux.py:193-194` named, "four launcher families"; unwired launchers kept on an uncovered list | Medium | L2 |
| C-004 | Model id and alias canonicalisation | Six steps: strip `[...]`, lower-case, `host_ids` table, alias, host_env value, glob `claude-opus-*`; else unclassified | Strip and lower-case, exact `ids` and `aliases`, family alias through `ANTHROPIC_DEFAULT_<FAMILY>_MODEL`, else unmapped (deny) | Exact `ids` and `aliases`; `id_prefix_match: false` because docs say an id entry also permits later versions (B7) | Medium | L2 |
| C-005 | Tier vocabulary | Family names: opus, sonnet, haiku, fable | Family names: opus, sonnet, haiku | Role names: `judge` (restricted), `work`, `light` | Medium | L2 |
| C-006 | Stage model and seeded stages | `default` and `blind-scoring`; stage from env `SC_MODEL_STAGE` set by a person, Orca or the helper | `blind-scoring`, `brainstorm-proposal`, `implement-worker`, `unscoped`; env `SC_MODEL_STAGE` | `default`, `proposal`, `implement`, `blind-scoring` (`declared_by: human`) plus `bindings` mapping script glob, agent or skill to a stage; env `SC_STAGE` | Medium | L2 |
| C-007 | Observe/enforce granularity | Global `mode` plus `event_mode` (bash_launch, agent, script_scan) | One global `mode` | Per-class `mode` (bash_claude, bash_script, agent, skill, prompt_command); strictest layer wins | Medium | L2 |
| C-008 | `claude` launched with no `--model` | Blocked (MP-NOT-PINNED) when the stage sets `require_explicit_model`, because inheriting is how an Opus session spawns Opus children | Resolve the effective default (env, settings) and check it; unresolved gives MP-03 | Resolve the effective default and check it (REQ-07) | High | L3 |
| C-009 | `--model` value built at run time | Single-assignment variable resolved; closed-world rule (every in-file model-shaped literal allowed, comments stripped) bounds table-driven launchers; else MP-DYNAMIC | Any expansion or substitution blocked (MP-03); nothing resolved | Single in-file assignment resolved by regex; anything else dynamic and denied (MP-04) | High | L3 |
| C-010 | Script scan scope | Shell scripts up to 256 KB, depth 1, plus a `.py` file named in the command (flat scan) | Shell scripts, one level, up to 64 KB; interpreter scripts are a ceiling | Shell scripts, depth 1, up to 256 KB; deeper is a stated ceiling | Medium | L3 |
| C-011 | Agent call without `model` | Read frontmatter by `subagent_type`, else recorded session model; MP-INHERIT if that tier is forbidden; unknown session model allows | Frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then SessionStart record; re-record on any `/model` prompt | Same order as B; a mid-session switch is a ceiling | Medium | L3 |
| C-012 | UserPromptSubmit and SessionStart roles | UPS checks `^/model` only; SessionStart records the model | UPS blocks `/model` and `/sc:` commands whose file names a forbidden model; SessionStart records model and a `policy-unreadable` lock | UPS reads `/command` frontmatter; SessionStart records model | Medium | L2 |
| C-013 | Internal-error handling | Pure-bash prefilter on raw input; fail closed only if it saw claude, superclaude, `ANTHROPIC_`, `CLAUDE_CODE_` or an Agent call with `model`; own `timeout 4` converted to exit 2 for launch events | Fail closed on any model-bearing event it cannot resolve; ordinary calls never blocked | Governed sessions (`SC_STAGE` in env) fail closed on any internal error; own `timeout 2` converted to exit 2 for governed sessions only | Medium | L3 |
| C-014 | Tamper protection scope | TAMPER class: Edit, Write, NotebookEdit and Bash touching hook, policy, state dir, `settings*`, `disableAllHooks`, `install_hooks`, `model-policy allow` | MP-06 for Edit/Write and for redirect, `tee`, `sed -i` naming the policy; MP-07 for the override CLI named in Bash; `audit` detects forged rows | MP-07 for Bash naming `model-policy grant` or the state dir, and for Edit, Write, NotebookEdit on policy, grant, state paths | Low | L3 |
| C-015 | Rollout order and rollback | Observe about one week; enforce bash_launch and agent; then script scan and inherit; optional Jev last | Observe two weeks or 200 live events; then one flip to enforce | All observe; enforce bash_claude and agent, then skill, prompt_command, then bash_script after at least 100 script events; rollback by setting a class back to observe | Medium | L2 |
| C-016 | Decision log and CLI | `decisions.jsonl` with 12 fields incl `policy_sha8`, `ms`; `log --tail` | `denials.jsonl`; `report`; `overrides-used.jsonl` | `decisions.jsonl` with 8 fields; raw command text never logged | Low | L1 |
| C-017 | Block message content | Event id, rule id, tier, policy path and key; names an allowed model; human grant command | Rule, stage, policy key path; "Do not edit the policy or the override file" | Rule, policy line, path, layer; "the requested model must be the model used"; grant command | Low | L1 |
| C-018 | Override record design | Append-only `overrides.jsonl`; scope tier, stage, session, project or script sha256; hook reads last 200 lines only when about to block | `overrides.jsonl`, `overrides-used.jsonl`, hash-chained journal; `audit` flags rows with no journal line; reason at least 20 characters | One file per grant `grants/<id>.json`; scope session, cwd glob or command sha256; reason required | Medium | L2 |
| C-019 | Guard on creating an override | CLI refuses unless stdin is a TTY and `CLAUDECODE` is unset; says the Bash tool has no TTY | Same; cites `process.py:171` as proof that child claude carries `CLAUDECODE` | TTY plus a typed `yes` read from `/dev/tty`; Bash no-TTY marked UNVERIFIED | Medium | L3 |
| C-020 | Jev question design | Choice, 4 options on the value of `--model` (literal forbidden, literal allowed, from a table including a forbidden name, cannot tell); block if p(a or c) at least 0.70 | Choice, 3 options on the tier (forbidden, allowed, cannot tell); block only on "forbidden" with p at least 0.7 | Choice, 4 options on whether the model is hidden (dynamic, static, not-a-launch, none); log only when p(dynamic) above 0.7 | Medium | L2 |
| C-021 | Gate to promote Jev | At least 50 labelled in-file indirect launches that code misses; precision at least 0.95 at p at least 0.7; at most 1% false blocks | At least 3 labelled misses in class (b) per 300 events, or any labelled code-ALLOW/label-BLOCK on a launch code could see | At least 100 residue items; precision at least 0.95 at p above 0.7; zero Jev-added blocks on static and not-a-launch items | Medium | L2 |
| C-022 | Offline test data and labelling | Incident scripts, transcripts (shape UNVERIFIED), observed `modelUsage` in run JSON as ground truth, synthetic mutants reported separately | Transcript `tool_use` records (503 jsonl files, model key UNVERIFIED), 20 `.dev` launchers, dry-run argv builders; author labels, second reader labels 20%, labels frozen before the run | Extraction script, deterministic literal pass, human labels the rest; fixtures replayed in CI | Medium | L2 |
| C-023 | Hook registration shape and timeouts | One PreToolUse matcher `^(Bash\|Monitor\|Agent\|Task\|Skill\|Edit\|Write\|NotebookEdit)$` at 5 s; SessionStart `*` at 3 s; UPS at 3 s | PreToolUse `^(Bash\|Agent\|Task\|Skill\|Workflow\|Monitor)$` at 3 s and `Edit\|Write` at 1 s; UPS 3 s; SessionStart 3 s | PreToolUse `Bash\|Agent\|Task\|Skill\|Monitor` at 5 s; UPS 3 s; SessionStart 2 s | Medium | L2 |
| C-024 | Room for version 2 | `routing: dynamic` marker read as "unpinned" in v1; `model-policy route --stage --facets`; null `routing` field in the log | `routing: dynamic` plus `router:`; per-stage `candidates`; v1 replay corpus becomes the v2 evaluation set | Marker plus facet table; `updatedInput` only under an explicit mode; native `availableModels` generation | Low | L2 |
| C-025 | Role of native `availableModels` floor | L0 shipped as a global floor; per-child injection UNVERIFIED | C3 coarse floor; lists concatenate across layers | "Generated from the same policy" (E7) yet generation left to v2 (section 9) | Medium | L2 |
| C-026 | Default enforcement scope | All sessions, seeded `observe` (stated) | All sessions for model-bearing events (implicit) | All sessions per mode; governed sessions additionally fail closed | Low | L2 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact | Lvl |
|---|-------------------|--------------------|--------------------|--------------------|--------|-----|
| X-001 | Policy file missing | Launch events allowed, `no_policy` logged (A section 2 table) | Model-bearing events blocked MP-04 in enforce, non-model events allowed (B section 2 table) | Allowed, `no_policy` logged (C section 2 table) | High | L3 |
| X-002 | `jq` or `awk` missing | Fail closed when a pure-bash prefilter sees a launch-shaped input; REQ-23 tests it | Not stated; fail closed only on model-bearing events it can detect | Fail open, copying `require-orca-worktree-agent.sh` (REQ-25 expects exit 0) | High | L3 |
| X-003 | Project and managed policy paths | Nearest `.claude/model-policy.json`, walk up at most 8 levels, tighten only | `<cwd>/.claude/model-policy.json`, no walk; B itself flags that `.claude/` is gitignored here | `<project root>/.superclaude/model-policy.json`, walk up 8, plus root-owned `/etc/superclaude/model-policy.json` | Medium | L2 |
| X-004 | Launches nested in `bash -c`, `eval`, `ssh`, `xargs`, `find -exec`, heredoc piped to a shell | Blocked by a second flat over-approximate scan that can only add blocks | `bash -c`, `sh -c`, `eval` strings scanned one level; heredoc piped to a shell is a ceiling | Ceiling, softened by a `claude-mention` rule (claude word with no resolvable flag is dynamic); C also says heredoc bodies are "scanned as text" while listing the shell-stdin case as a ceiling | High | L3 |
| X-005 | Oversized script or command | Script over 256 KB or command over 64 KB blocked (MP-BIG) | Script over 64 KB or unreadable blocked (MP-03) | Script over 256 KB not scanned and allowed with `scan_skipped` logged (REQ-09); command over 64 KB blocked (MP-09) | Medium | L3 |
| X-006 | Names of shipped artifacts | Hook `enforce-model-policy.sh`; seed `model-policy.json.example`; env `SC_MODEL_STAGE`; CLI `check, allow, log, lint` | Hook `model-policy-guard.sh`; seed `model-policy.example.json`; env `SC_MODEL_STAGE`; CLI `override, audit, report` | Hook `model-policy-guard.sh`; seed `model-policy.json.example`; env `SC_STAGE`; CLI `grant, list, revoke, check` | Low | L1 |
| X-007 | Registration covers the tamper rule | Matcher includes Edit, Write, NotebookEdit | Matcher has `Edit\|Write` but not NotebookEdit | Tamper rule MP-07 and REQ-31 need Edit, Write, NotebookEdit, but the PreToolUse matcher lists only Bash, Agent, Task, Skill, Monitor | Medium | L3 |
| X-008 | Override validity | Default 2 h, maximum 24 h | Default 24 h, maximum 168 h | Maximum 24 h (`grant_max_hours`) | Medium | L2 |
| X-009 | `/model` typed by a person | If UPS fires, "blocks or records" (row 10); row 11 says the human's own session is not rejected | UPS returns a block decision for `/model`; also re-records the model on a `/model` prompt | Cannot see; native floor only | Medium | L3 |
| X-010 | Jev code in the v1 deliverable | Dormant switch `jev.enabled: false`, stage option `jev_then_log`, synchronous call with 2 s timeout when on | None; REQ-35 says the hook makes no network call and does not reference Jev | Optional async shadow `jev.shadow` (default false) that logs only | Medium | L2 |
| X-011 | What a hook timeout does | "A platform timeout is a non-blocking error (B9)" | Behaviour UNVERIFIED; B9 covers only non-zero exits other than 2 | "Platform treats non-exit-2 as non-blocking (B9), so a timeout fails open" | Medium | L3 |
| X-012 | Latency pass mark | p95 at most 100 ms (non-launch) and 150 ms (launch), 200 runs, manual | p95 at most 50 ms on the fixture corpus | p95 at most 50 ms on the non-matching path, 200 runs | Low | L2 |
| X-013 | Stage named inside a command text | `SC_MODEL_STAGE=x claude ...` may only narrow the session stage; otherwise MP-STAGE-WIDEN | Silent on a prefix; stage comes from the session env | Inline `SC_STAGE=` accepted for stages that are not `declared_by: human`; `bindings` by script glob can raise a stage | High | L3 |
| X-014 | Reading of `process.py:171` | Not cited | "says child `claude` processes carry this variable, so it is a usable session marker" | Not cited | Medium | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Detective layer L3: after a headless run, compare the observed model in the output JSON (`.message.model`, `modelUsage`) with the requested one; catches silent substitution that name checks cannot see | High |
| U-002 | A | Closed-world rule for table-driven launchers (all in-file model-shaped literals allowed, comments stripped), so legitimate `SPECS`-array scripts are not all blocked | Medium |
| U-003 | A | Pure-bash prefilter on the raw hook input so internal errors fail closed only for launch-shaped calls and never brick ordinary Bash | High |
| U-004 | A | MP-STAGE-WIDEN: a command prefix may only narrow the session stage, so the model cannot claim `blind-scoring` for itself | High |
| U-005 | A | Event id in the block message and `policy_sha8` in every log line, so a block and its log row can be matched | Low |
| U-006 | B | REQ-29 repo test: fail if a raw `"--model"` literal appears in an argv builder outside the helper module, so new launchers cannot skip the check | High |
| U-007 | B | Hash-chained journal written by the CLI plus `audit` that flags override rows with no journal line (detects forged grants the hook cannot block) | Medium |
| U-008 | B | `overrides-used.jsonl`: one line per use of an override, tied to the launch | Low |
| U-009 | B | Replay method: labels frozen before the hook runs, a second reader labels a random 20% from the written rule only, disagreements change the rule first | Medium |
| U-010 | B | A forbidden-model child that starts through a Python launcher is still caught by its own SessionStart record and later tool calls (child with no tool call is the stated ceiling) | Medium |
| U-011 | B | `Workflow` in the PreToolUse matcher (the name is valid: it is in the existing matcher at `hooks.json:116`); `reflect/commands.py:365` `ANTHROPIC_MODEL` default routed through the helper | Low |
| U-012 | B | SessionStart writes a `policy-unreadable` lock so later model-bearing calls in that session are blocked | Low |
| U-013 | C | Root-owned managed layer `/etc/superclaude/model-policy.json` that a same-user model cannot edit (availability UNVERIFIED; the directory does not exist on this host today) | High |
| U-014 | C | `bindings` (script, agent, skill to stage), `declared_by: human` and a `restricted` tier, so Opus is reachable only from sources the model cannot write | Medium |
| U-015 | C | `id_prefix_match: false` with the docs B7 reason (an id entry permits later versions) | Medium |
| U-016 | C | Decision log never stores raw command text, only extracted model tokens | Medium |
| U-017 | C | `claude-mention` rule: a `claude` word with no resolvable flag is treated as dynamic | Low |
| U-018 | C | Rollback with no reinstall: set an event class back to `observe` in the user policy file | Medium |
| U-019 | A | Synthetic mutants of real launches (`M=...; --model "$M"`, `${M:-...}`, `bash -c`, heredoc, array) reported separately from real data | Medium |
| U-020 | C | Typed `yes` read from `/dev/tty` in the grant command | Low |

## Shared Assumptions

Agreement points scanned: no Jev call in the v1 blocking path (A, B, C); JSON policy read by `jq` and Python; user policy seeded once by `_SEED_FILES`; block with exit 2 and a `Blocked/Why/You can` message; hook never rewrites a model; observe-first rollout; same-user model ceiling; `/model` not reliably visible; decisions written to a log.

| A-NNN | Assumption | Source Agreement | Class | Impact | Status |
|-------|------------|------------------|-------|--------|--------|
| A-001 | The model name in the command, agent parameter or frontmatter is the model actually served. Gateway ids (`claude-gw-*`) map to tiers only by the host table, and the `modelOverrides` setting (enrichment B6) can remap ids; none of the three proposals mentions `modelOverrides` (0 matches) | Name-based tier check (A, B, C) | UNSTATED for `modelOverrides`; gateway part is STATED as UNVERIFIED by A and C | High: a remap would defeat every tier check silently | Promoted |
| A-002 | Every child that must obey the policy sees the operator's `~/.claude` hooks and `~/.claude/model-policy.json` | Hook-based enforcement for children (A, B, C) | CONTRADICTED for eval children: `src/superclaude/cli/eval/claude_process.py` runs each eval in a per-eval HOME (lines 7, 108-112, 238-241 read in Step 1), so that child loads neither the hook nor the policy | High: launches inside eval children are covered only by the in-process helper | Promoted |
| A-003 | The observe-first period is an accepted exposure window: until the owner flips a class to enforce, the incident (Opus on unattended stages) is still possible. No proposal states who flips it, by when, or what exit evidence is enough beyond counts (B: 200 events; C: 100 script events) | Observe-first rollout (A, B, C) | UNSTATED | Medium: v1 "ships" with nothing enforced | Promoted |
| A-004 | Legitimate Opus runs (blind scoring) are rare and started or approved by a person, so a human grant or binding per run is acceptable. The incident launcher scripts start Opus children from ordinary orchestrator sessions in the default stage | Default stage denies Opus; elevation by grant or binding (A, B, C) | UNSTATED | Medium: if blind scoring is frequent, grants become routine and are rubber-stamped | Promoted |
| (not promoted) | Hook env equals session env (used for aliases and `SC_MODEL_STAGE`) | A and C mark it UNVERIFIED; B states it as fact | STATED | - | Kept UNVERIFIED |
| (not promoted) | `UserPromptSubmit` fires for `/model` and for typed `/sc:` commands | All three mark it UNVERIFIED | STATED | - | Kept UNVERIFIED |
| (not promoted) | What the gateway runs behind `claude-gw-tier1a/1b/2/3` | A and C mark it UNVERIFIED | STATED | - | Kept UNVERIFIED |
| (not promoted) | A model run by the same OS user with a pty can forge a grant or edit the policy | All three state it as a ceiling | STATED | - | Ceiling kept |

## Summary
- Total structural differences: 6
- Total content differences: 26
- Total contradictions: 14
- Total unique contributions: 20
- Total shared assumptions surfaced: 4 promoted (UNSTATED: 3, CONTRADICTED: 1) plus 4 STATED rows not promoted
- Diff points counted for convergence (S + C + X + A): 6 + 26 + 14 + 4 = 50 (unique contributions are not debated points)
- Highest-severity items: C-001, C-002, C-008, C-009, X-001, X-002, X-004, X-013, A-001, A-002; High-value unique items: U-001, U-003, U-004, U-006, U-013

## Facts verified in Step 1

Read-only checks on this checkout, 2026-11-14. These are the only claims this merge upgrades from "cited" to "verified".

| Check | Result |
|-------|--------|
| Argv builders with `--model` in `src/superclaude/cli` | Verified at `pipeline/process.py:164`, `sprint/tmux.py:194`, `prd/models.py:283`, `sprint/summarizer.py:330`, `reflect/runner.py:508` (string form). No literal `--model` in `eval/claude_process.py`. `sprint/models.py:899,907,1246` only builds advice text |
| `install_hooks.py` | `_FRESHNESS_SCRIPTS` at line 42; `_SEED_FILES` at 104-106, first entry `("auggie-projects.txt.example", "auggie-projects.txt")`: the repo names seeds `<dest>.example`, so `model-policy.json.example` (A, C) follows the pattern and `model-policy.example.json` (B) does not. Seeds are never overwritten, even with `--force` (lines 100-103) |
| `hooks.json` | Edit\|Write matcher line 86 (timeout 1); Bash matchers lines 96 and 106 (timeout 3); wide matcher line 116 with Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger (timeout 5); Bash line 126 (timeout 5); async example line 144. A's `:113` and `:122` are off by two lines (real: 111 and 121) |
| `CLAUDECODE` | `pipeline/process.py:171-179` removes `CLAUDECODE` from the child env (`env.pop`); B's reading of `:171` is wrong. The variable is `1` in this Bash tool (observed) |
| TTY | In this Bash tool stdin and stdout are not TTYs (observed once, this host, today); A's flat statement holds for this harness, C's UNVERIFIED is downgraded to "observed once" |
| `.superclaude/` | Per-project memory store (`save.md:42`) made gitignored by a `*` file (`save.md:43`); so C's project path is not versioned either. `/etc/superclaude` does not exist on this host |
| Agent and skill models | 16 agents with `model:`: 11 sonnet, 2 opus (`auggie-reviewer`, `eval-suite-author`), 3 gateway ids (`issue-worker-t1` tier1a, `-t2` tier2, `-t3` tier3); 1 skill (`sc-bare-review`) sonnet. Day-one observe flags therefore include `issue-worker-t3` (unmapped), which C omits |
| Tests present | `tests/hooks/test_launch_level_guard*.py`, `test_require_orca_worktree_agent*.py`; `tests/cli/test_install_hooks.py`, `test_verify_sync_hooks.py` |
| Precedent hooks | `launch-level-guard.sh:126` Blocked/Why/You can; `:94-97` TAMPER text; `:102-105` 64 KB cap; `:147-163` governed fail-closed trap; `:431-437` normalisation; `:454` basename claude match; `:706` tamper patterns. `require-orca-worktree-agent.sh:5-6` subagents, `:9-16` fail-open contract, `:38-62` ceilings |
| Makefile | `sync-dev` copies hook scripts at 136-143; `verify-sync` diffs at 254-263 and requires `_FRESHNESS_SCRIPTS` membership at 306-326 |
| Enrichment B9 | Says only that non-zero exits other than 2 are non-blocking; says nothing about timeouts, so A's and C's timeout claims are unsupported (X-011) |
| Not checked | `.dev/eval-workspaces/` incident scripts and their line numbers (this merge may not touch that folder); session transcript shape; Jev endpoint; any latency |
