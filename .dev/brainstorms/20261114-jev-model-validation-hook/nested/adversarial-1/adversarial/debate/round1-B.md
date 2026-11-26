# Round 1 debate: Variant B advocate (sonnet:analyzer)

Evidence tags: "verified" means I read the line in this session. "UNVERIFIED" means I did not. Repository root is the IronClaude worktree.

## Advocate: Variant B (sonnet:analyzer)

### Position Summary

Variant B is strongest on the property itself. One helper both checks and emits the `--model` flag, so the value checked is the value used. Every unresolvable case stays on the blocking side: no allow on an unresolved variable, an oversized script or a missing policy. Jev stays out of the v1 deliverable. B loses to A and C on rollout granularity, override-guard strength, tamper breadth, jq-missing handling and several wrong or silent details, and I concede those below.

### Steelman: Variant A

A's strongest argument is that no single mechanism sees everything, so it layers four of them and says what each is blind to (A section 0 table). It adds three things B lacks. First, a detective layer (L3) that compares the model a headless run reports (`.message.model`, `modelUsage`) with the model requested; that is the only mechanism in any variant that can notice a silent remap (A-001). Second, a pure-bash prefilter on the raw hook input (A section 2, last row of the failure table), so a missing `jq` fails closed only for launch-shaped input and never bricks ordinary Bash. Third, MP-STAGE-WIDEN: a command prefix may only narrow the session stage, so the model cannot write `SC_MODEL_STAGE=blind-scoring` for itself. A also has the broadest tamper class (Edit, Write, NotebookEdit, settings, `disableAllHooks`, `install_hooks`), a second flat over-approximate scan that closes `bash -c`, `ssh`, `xargs`, `find -exec` and heredoc-to-shell, a closed-world rule that lets legitimate table-driven launchers through, a 12-field decision log, and a shorter override window (2 h default, 24 h maximum). Its seed file name follows the repository's `<dest>.example` pattern (verified: `install_hooks.py:104-106` uses `auggie-projects.txt.example`). It also ground-truths its replay on the model the run actually reported, which is the closest any variant gets to measuring "used" rather than "named".

### Steelman: Variant C

C's strongest argument is operational: a guard that cannot be rolled out safely will never be enforced, so the incident repeats. C has per-class modes (`bash_claude`, `bash_script`, `agent`, `skill`, `prompt_command`), strictest layer wins, and rollback with no reinstall by setting a class back to `observe` (C section 8). It stages enforcement by false-positive risk and gates the script class on at least 100 clean script events. It is the only variant with a layer a same-user model cannot edit (`/etc/superclaude/model-policy.json`, root-owned), it never logs raw command text, and its grant needs a typed `yes` read from `/dev/tty`, a stronger human check than a bare TTY test. Its `bindings` and `declared_by: human` let Opus be reachable only from sources the model cannot write. Its role vocabulary (`judge`, `work`, `light`) avoids claiming that `claude-gw-tier1a` is "Opus", which is unverified. Its Jev shadow call is logging-only and cannot change an outcome. Its latency target (p95 at most 50 ms on the non-matching path) measures the path every ordinary Bash call pays. It also refuses `id_prefix_match`, citing docs B7.

### Key Strengths Claimed

1. **Check and use are one operation (C-002, C-003, C-001).** B's `model_policy.build_flag` returns the flag from the checked value, so a launcher cannot check one model and pass another (B section 8, "Add"). A's `check_launch(stage, model)` and C's `--check` spawn are separate from the argv builder. B's REQ-29 fails the build if a literal `"--model"` appears in an argv builder outside the helper, so a new launcher cannot skip the check; A says nothing stops a new unrouted launcher, and C keeps unwired launchers on an "uncovered" list. B also covers `reflect/commands.py:365`, where I verified `_DEFAULT_MODEL = "opus"` at line 37 and `model = os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL` at line 365. A names `reflect/runner.py:508` but not this site, and C names no file for reflect.
2. **Every unresolvable case blocks (C-009, X-001, X-005, C-010).** B blocks any expansion or substitution in the model value (MP-03), a missing or malformed policy for model-bearing events (MP-04), and a script that is unreadable or over 64 KB (MP-03). Soundness is the property: a false block costs an edit to a launcher; a false allow is the incident. A's closed-world and single-assignment rules and C's single-assignment regex both allow cases they cannot prove (for example `MODEL=${MODEL:-claude-sonnet-5-5}` with `MODEL` set to Opus in the environment; neither text excludes it). C also allows scripts over 256 KB with only a `scan_skipped` log (C REQ-09), which a model can trigger by padding a file past the cap.
3. **Missing policy is a lock, not a hole (X-001).** In A and C a missing policy allows launches. C's tamper rule MP-07 names only `model-policy grant` and the state directory in Bash text (C section 4). The policy file `~/.claude/model-policy.json` is outside that directory, so a Bash `rm` or `mv` of it is not covered by MP-07, and the next Opus launch is allowed. In B the same deletion makes model-bearing events block (B section 2 table), so B does not depend on its tamper list being complete.
4. **No Jev code in the v1 deliverable (X-010, C-020, C-021).** B REQ-35 requires no network call and no Jev reference. A ships a dormant `jev.enabled` switch with a synchronous 2 s call path; C ships an async shadow path. The brief says Jev is used in v1 only where a measured need exists; B's measured-need rule (at least 3 labelled misses in the unreadable-file class per 300 events, or any labelled miss on a launch the code could see) is explicit and replay-measurable. B's 3-option Choice question includes a "cannot tell" option, as the enrichment requires.
5. **Honest, row-level visibility (S-002, C-011, C-012, X-009).** B's event table has 16 rows and marks rows 14 to 16 (`/model`, mods with `agent.spawn`, harness or managed settings) as "Cannot see", and states "C2 does not promise rows 14 to 16" with an owner decision attached. B resolves an Agent call with no `model` in the documented order (frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, main model) and re-records the session model on any `/model` prompt, which A's inherit rule omits (A reads only frontmatter, then the recorded model).
6. **Requirements with a fixed verification vocabulary (S-003, S-004).** B's 36 REQs use five methods only (unit, integration, fixture replay, parity, manual). REQ-30 (hook and Python helper agree on a shared table), REQ-36 (the hook never returns `updatedInput`) and REQ-25 (no `src/superclaude/` path in a block message) each map one-to-one to a constraint in the brief.
7. **Override recording with audit (C-018).** B records each use in `overrides-used.jsonl` tied to the launch, requires a reason of at least 20 characters, and ships `audit`. I do not claim the hash chain is tamper-proof against a same-user writer (see Concessions).
8. **Replay method discipline (C-022).** Labels are frozen before the hook runs, a second reader labels 20% from the written rule only, and disagreements change the rule first (B section 3). B also did a first count of the corpus (503 transcript files, `--model` in 470 places across 94 files; UNVERIFIED by me, B's own report), and noted that the transcript model key is unverified and a raw line must be read first.
9. **Room for version 2 keeps the v1 invariant (C-024).** B states router output is "a request, not an allow": the hook still checks the chosen model against the same allow list. C reserves `updatedInput` under an explicit mode, which is the one thing v1 forbids.

### Weaknesses in Variant A

1. **Jev can turn a block into an allow (X-010, C-020).** A's section 3 says that when Jev is unreachable under `dynamic_model: jev_then_log`, "the code result stands (allow-and-log)". So in a stage that enables Jev, an unresolved model value is allowed unless Jev says "forbidden" at p of at least 0.70. That makes Jev the only gate on dynamic launches in that stage, which is weaker than the default `closed_world_then_deny`. It breaks the brief's principle that Jev "may only ever add a block, never allow" (seed brief, Known Context). The dormant code path also ships an untested synchronous network call (2 s timeout) inside a 5 s security hook.
2. **Closed-world rule admits cases A itself calls unsound (C-009).** A section 3 lists "in-file flows where the closed-world rule is unsound" as residue, yet the rule is applied before that residue is considered, and A's REQ-11 only tests the easy case (an Opus word in a comment). A has no REQ for a conditional or env-overridable assignment. A false allow here is the incident. B blocks all of it (MP-03).
3. **Inherit check allows when the session model is unknown (C-011).** A's REQ-17 allows an Agent call with no `model` and no frontmatter "when [the recorded session model] is unknown". Incident #3 in the enrichment (session switched to Opus, then four subagents pinned to Opus) is exactly the case where the record is stale or missing. B re-records on any `/model` prompt and checks `CLAUDE_CODE_SUBAGENT_MODEL` before the session record.
4. **The flat pass-2 scan can block read-only commands (X-004).** Pass 2 blocks "any `--model X` pair ... whenever the word `claude` appears" (A section 5). This repository's own work is full of commands such as a `grep` for `--model claude-opus-5-5` in `.dev/` or a heredoc that writes documentation containing a launch line. A has no REQ for a non-launch mention that must pass (REQ-08 tests only blocks). Rate of false blocks: UNVERIFIED. I concede the coverage gain (see Concessions-adjacent rows X-004 and C-014 in the table).
5. **L3 detective layer has no requirement and no file (C-001, U-001).** A's headline lists L3 but none of REQ-01 to REQ-35 verifies it, and section 8 "Files to add" lists no code for it (verified by reading A in full). It also runs after the event, so it does not meet "rejected before the event runs". It is a good idea; it is not yet a v1 deliverable.
6. **Cited platform fact does not support the claim (X-011).** A says "a platform timeout is a non-blocking error (B9)". Enrichment B9 says only that non-zero exits other than 2 are non-blocking (diff-analysis Step 1 table). The defensive `timeout 4` conversion is still sound, but the stated reason is unsupported.
7. **Glob `ids` accept later versions (C-004).** `"claude-sonnet-*"` allows any future Sonnet id without owner review. Enrichment B7 warns that an id entry already permits later versions; for a rule whose purpose is "the defined model is the model used", exact ids with a deny on unmapped (B, C) are the safer reading.
8. **Override tail read can drop a valid grant (C-018).** The hook reads "the last 200 lines only when about to block" (A section 4). A still-valid grant older than 200 appended lines is ignored, so a launch the human approved blocks. This is a false block, not a false allow, and unlikely inside a 2 h window.

### Weaknesses in Variant C

1. **Fail-open holes that a model can trigger (X-001, X-002, X-005).** (a) Missing policy allows (C section 2 table) and the tamper rule MP-07 covers Bash text naming `model-policy grant` or the state directory only; `~/.claude/model-policy.json` is not in `~/.claude/state/model-policy/`, so Bash `rm` or `mv` of the policy is not caught, and the next launch is allowed. (b) Scripts over 256 KB are allowed with `scan_skipped` (REQ-09); padding a script past the cap bypasses the scan. (c) Missing `jq` or `awk` fails open (REQ-25), and the launcher check runs the same script, so Python launcher coverage also fails open.
2. **The tamper rule cannot fire as registered (X-007).** C's PreToolUse matcher is `Bash|Agent|Task|Skill|Monitor` (C section 8). MP-07 and REQ-31 require a block on Edit, Write and NotebookEdit of the policy, but those tools never reach the hook. REQ-31 cannot pass as written.
3. **`judge` is not "reachable only from sources the model cannot write" (U-014, X-013).** A `bindings` entry maps a script glob to `blind-scoring`, and a model can write a script whose name matches `*/blind-score*.sh`. C's own risk list says so ("satisfied by a model that creates a script with a matching name"), and the `sha256` pin is optional. Inline `SC_STAGE=` is also accepted for stages not marked `declared_by: human`, which is the widening A's MP-STAGE-WIDEN closes.
4. **Launcher check by spawning a shell script (C-002, C-003).** C's own estimate is about 40 ms per spawn (section 6) against B's in-process 5 ms. The launcher then depends on an installed hook file and `jq`. No test stops a new launcher from skipping the check, and "unwired launchers stay on an uncovered list" (section 8) is a standing gap for the very path (Python subprocess) the hook cannot see.
5. **Internal contradictions (C-025, X-004).** E7 says native `availableModels` is "generated from the same policy", but section 9 defers that to v2. The bypass table says heredoc bodies are "scanned as text" while listing a heredoc piped to a shell as a ceiling.
6. **`claude-mention` rule over-blocks (U-017).** A `claude` word with no resolvable flag is treated as dynamic (MP-04). That includes `claude --version`, `claude mcp list` and any `git commit -m` that mentions claude. Rate: UNVERIFIED; C has no REQ for these pass cases.
7. **Observe on every class on day one with no exit evidence (A-003).** C gates only `bash_script` (100 events). Nothing says who flips the other classes or on what evidence, so the incident path stays open indefinitely.
8. **Managed layer is not available today (X-003).** `/etc/superclaude` does not exist on this host, and the project path `.superclaude/` is gitignored by a `*` file (diff-analysis Step 1, `save.md:42-43`). Both are listed as UNVERIFIED availability by C; neither protects v1 on day one.

### Concessions

1. **Wrong fact in B (X-014).** B says `pipeline/process.py:171` shows that child `claude` processes carry `CLAUDECODE`. I read the lines: `process.py:171-172` says "Remove CLAUDECODE ... to prevent nested-session detection" and `process.py:179` does `env.pop("CLAUDECODE", None)`. B's reading is the reverse. The override CLI's `CLAUDECODE` test is therefore weak, and the TTY test carries the guard. C's typed `yes` read from `/dev/tty` is the stronger human check.
2. **Seed name breaks the repo pattern (X-006).** B's `model-policy.example.json` does not follow the `<dest>.example` form that `_SEED_FILES` uses (`install_hooks.py:104-106`, `auggie-projects.txt.example`). It should be `model-policy.json.example`.
3. **Matcher omits NotebookEdit (X-007).** B's tamper rule MP-06 names Edit and Write only.
4. **No answer for missing `jq`/`awk`, no pure-bash prefilter, no self-timeout (X-002, X-011, C-013).** B says it fails closed "on any model-bearing event it cannot resolve", but without `jq` it cannot tell whether an event is model-bearing. A's prefilter and `timeout 4` conversion solve this; B leaves timeout behaviour as UNVERIFIED and does nothing about it.
5. **Missing-policy block is wider than B says (X-001).** B's table blocks Monitor and Workflow on every call and every Agent call, which contradicts "ordinary tool calls are never blocked". The `mode` field lives in the policy, so a malformed policy blocks even during the observe period. The block should apply only to calls that name a model.
6. **Single global mode flip (C-007, C-015, A-003).** B has one `mode`, a two-week or 200-event observe period, then one flip. That is the longest exposure window of the three. B's log also records denials only (`denials.jsonl`), yet its exit criterion counts "model-bearing live events", which needs allows logged too. A's 12-field `decisions.jsonl` is better (C-016).
7. **Silent on an inline stage prefix (X-013).** B says "shell launchers prefix" `SC_MODEL_STAGE` but never says whether the hook honours an inline prefix. If it does, the model can claim `blind-scoring`; if it does not, shell launchers cannot use it. A's narrow-only rule (MP-STAGE-WIDEN) is the answer.
8. **Operational costs of B's strictness.** Blocking every expansion rejects the common `MODEL=claude-sonnet-5-5` then `--model "$MODEL"` pattern (A cites `launch-implement-2.sh:8,28`; I did not re-read it, UNVERIFIED). Exact ids need a table edit on every model release.
9. **Override design overclaims.** The hash-chained journal and `audit` detect naive forgery only; a same-user writer can rewrite both files. A 24 h default and 168 h maximum (X-008) is too long compared with A's 2 h and 24 h.
10. **Jev gate is weak (C-021).** B's trigger counts misses in class (b), which B itself says Jev cannot fix (it reads only short text), and B sets no precision or false-block threshold for Jev acceptance. A (50 items, precision at least 0.95, at most 1% false blocks) and C (100 items, zero Jev-added blocks on static and not-a-launch items) are better.
11. **Replay ground truth (C-022).** B labels by "the decision the rule requires", which is circular. A's use of the model a run reported (`modelUsage`) measures "used", and B has no layer for silent remap (A-001).
12. **Native floor is named, not built (C-025).** B section 1 names C3 but no REQ or plan step writes `availableModels`. A has the same gap.
13. **Latency numbers are estimates and several counts are UNVERIFIED.** B's 503 transcripts, 470 matches and 20 launchers are B's own report; I did not re-run them.

### Shared-assumption responses

- **A-001: QUALIFY.** A name-based check is the most a hook can do, but v1 must say plainly that it checks the requested name, not the served model, and must add `modelOverrides` (docs B6) and the settings `env` redirects to the "cannot see" list (all three proposals omit `modelOverrides`).
- **A-002: QUALIFY.** The assumption is false for eval children (per-eval HOME), but I read `eval/claude_process.py:284-289`: it builds `ClaudeProcess(model=self._model)`, so the launch-time check at `pipeline/process.py:164` runs in the operator's process and covers the launch; only the child's inner tool calls go unhooked and must be listed as a ceiling.
- **A-003: REJECT.** An open-ended observe period is not an acceptable exposure window; enforce the zero-ambiguity classes (literal `--model`, Agent `model` parameter, Python launcher helper) from day one, observe only the script scan and inherit checks, and name an owner and an exit condition.
- **A-004: QUALIFY.** It holds for blind scoring itself, but the incident launchers start Opus children from default-stage orchestrators, so the stage must be set by the launcher or a human-owned binding (not a per-run grant), and the proposals must say who sets it.

### Per-point positions

| Point | Winner | Basis (max 25 words) |
|---|---|---|
| S-001 | A | Headline layer table states the v1 property and each layer's blind spot before the detail. |
| S-002 | B | B rows 14-16 mark `/model`, mods and harness settings "Cannot see" and attach an owner decision. |
| S-003 | B | Fixed five-method verification vocabulary makes each REQ checkable. A is mixed; C is nearly all unit. |
| S-004 | B | Residue split into (a) code blocks anyway, (b) ceiling, (c) not a model event, plus a measurable need rule. |
| S-005 | C | Per-class order with a stated rollback by editing the policy; A and B give less rollback detail. |
| S-006 | B | "Not checked" line names unread docs, gateway ids and unmeasured latency. Equal to C; A folds it into section 10. |
| C-001 | B | Three points each with a named REQ-covered mechanism; A's L3 detective has no REQ and no file. Floor unbuilt in both. |
| C-002 | B | In-process helper, `build_flag` emits the checked value, so check equals use; C spawns a script about 40 ms each. |
| C-003 | B | REQ-29 fails on a raw `"--model"` outside the helper; B also covers `reflect/commands.py:365` (`_DEFAULT_MODEL = "opus"`, verified). |
| C-004 | B | Exact ids plus aliases, unmapped denied; A's globs accept later versions, which docs B7 warns about. C is equal. |
| C-005 | C | Role names avoid claiming `claude-gw-tier1a` is Opus (unverified) and mirror the owner's "judge" rule. Concession. |
| C-006 | A | Two stages (`default`, `blind-scoring`) match the one rule; B's extra stages are speculative, C's bindings add attack surface. |
| C-007 | C | Five per-class modes with strictest-layer-wins allow staged enforcement; B's single flip is the longest exposure. Concession. |
| C-008 | B | Resolves the effective default and blocks when unresolved (MP-03); checks the model that would run without over-blocking pinned defaults. |
| C-009 | B | Block every expansion: no false allow from conditional or env-overridable assignment. A and C resolve cases they cannot fully prove. |
| C-010 | B | Depth-1 shell scan, 64 KB, bounded latency; Python launches are covered in-process. A's `.py` flat scan value UNVERIFIED. |
| C-011 | B | Full documented order including `CLAUDE_CODE_SUBAGENT_MODEL`, and re-record on `/model`; A allows when session model unknown. |
| C-012 | B | UserPromptSubmit blocks forbidden `/sc:` command frontmatter and re-records on `/model`; A checks `^/model` only. All UNVERIFIED firing. |
| C-013 | A | Pure-bash prefilter fails closed only for launch-shaped input and converts own timeout to exit 2. B cannot detect model-bearing without jq. |
| C-014 | A | Broadest tamper class: Edit, Write, NotebookEdit, settings, `disableAllHooks`, installer. B misses NotebookEdit; C misses Bash on the policy path. |
| C-015 | C | Enforce lowest-risk classes first, gate scripts on 100 clean events, rollback without reinstall. B's one flip after 200 events is weaker. |
| C-016 | A | 12-field log with `policy_sha8` and `ms`, all decisions logged; B logs denials only yet counts live events. |
| C-017 | B | Message carries rule, stage, policy key path and "Do not edit the policy"; REQ-24 golden-text test. Low impact, A and C close. |
| C-018 | B | Per-use record, reason of 20+ characters, audit command. Detection only against naive forgery; A's script-sha binding is also good. |
| C-019 | C | Typed `yes` from `/dev/tty` beats a bare TTY test. B's `CLAUDECODE` reasoning is wrong (`process.py:179` pops it). |
| C-020 | B | Three-option Choice with "cannot tell", block only on "forbidden" at p of at least 0.7; A's list-membership option is multi-hop. |
| C-021 | C | 100 items, precision 0.95 at p over 0.7, zero Jev-added blocks on static items; B has no acceptance threshold, A's 50 is thin. |
| C-022 | A | Ground truth from the model the run reported measures "used"; B's frozen labels and 20% second reader should be merged in. |
| C-023 | A | One matcher includes NotebookEdit, Edit, Write, Monitor with 5 s and an internal 4 s cap; B omits NotebookEdit, C omits Edit and Write. |
| C-024 | B | Router output is "a request, not an allow" and stays checked against the same allow list; C reserves `updatedInput`. |
| C-025 | NONE | Nobody wires or tests the floor; a global Opus deny conflicts with blind scoring. Decide: ship a coarse `deniedModels` or drop it from v1. |
| C-026 | A | States all sessions, seeded observe, with reason (incident sessions were ordinary). B implicit; C hybrid. |
| X-001 | B | Missing policy blocks model-bearing events, so deleting it is not a bypass. Narrow it to calls that name a model. |
| X-002 | A | Prefilter plus REQ-23 stub test fails closed for launch-shaped input; B silent, C fails open. |
| X-003 | C | Only variant with a root-owned layer a same-user model cannot edit. Not available today; project paths are gitignored in all three. |
| X-004 | A | Flat second scan closes `bash -c`, `ssh`, `xargs`, heredoc-to-shell; false-block rate on read-only mentions UNVERIFIED, measure in observe. |
| X-005 | B | Block oversize like A; 64 KB cap bounds scan time (B worst 150 ms vs A 400 ms). C's allow-on-oversize is bypassable by padding. |
| X-006 | A | Seed name follows the `<dest>.example` pattern (`install_hooks.py:104-106`) and env name is explicit. B's seed name breaks the pattern. |
| X-007 | A | Matcher includes Edit, Write, NotebookEdit so the tamper rule can fire. B lacks NotebookEdit; C's REQ-31 cannot pass. |
| X-008 | A | Two hours default, 24 h maximum limits blast radius; B's 24 h and 168 h are too long for rare blind-scoring runs. |
| X-009 | B | Works either way: blocks if UserPromptSubmit fires, says "cannot see reliably" otherwise, and re-records the model. A is ambiguous. |
| X-010 | B | No Jev code or network call in v1 (REQ-35). A's dormant path can allow on Jev failure; C ships a shadow path. |
| X-011 | A | A's self-timeout conversion is safe whichever way the platform behaves, though its B9 citation is unsupported; B does nothing. |
| X-012 | C | Targets the non-matching path every Bash call pays; B's corpus-wide p95 mixes in script scans. |
| X-013 | A | MP-STAGE-WIDEN narrow-only rule closes inline claims; B is silent and C accepts inline stages. |
| X-014 | A | Does not cite `process.py:171`; B's reading is wrong (`process.py:179` removes `CLAUDECODE`), so the TTY check must carry the guard. |
| A-001 | QUALIFY | Name-based check is the v1 limit; state it and add `modelOverrides` and settings `env` to the cannot-see list. |
| A-002 | QUALIFY | Eval child loads no hooks, but `claude_process.py:289` passes through `ClaudeProcess`, so launch-time check covers the launch. |
| A-003 | REJECT | Open-ended observe window is unacceptable; enforce literal and Agent-parameter classes from day one with a named owner and exit condition. |
| A-004 | QUALIFY | True for blind scoring, but incident launchers run from default-stage sessions, so stage must come from the launcher or a human binding. |

