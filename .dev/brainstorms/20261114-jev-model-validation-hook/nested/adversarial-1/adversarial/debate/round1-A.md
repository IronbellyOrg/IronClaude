# Round 1 debate: Advocate A (sonnet:architect)

Variant A = layered model-policy hook (`enforce-model-policy.sh`). Evidence tags: "A s3" = Variant A section 3; "verified" = I read the line myself in this session; "diff-analysis" = the Step 1 verified-facts table; UNVERIFIED = not checked by me.

## Advocate: Variant A (sonnet:architect)

### Position Summary

Variant A is the strongest on the failure paths that decide whether "the requested model is the model used" holds in practice: it fails closed for launch-shaped input in every session (not only governed ones), stops a model from claiming a wider stage, and over-approximates nested launches instead of listing them as ceilings. It loses on a few points where B or C are better (launcher chokepoint test, missing-policy rule, managed layer, no dormant Jev code), and I concede those below.

### Steelman: Variant B

The strongest case for B: enforcement should sit at the fewest points, so the property can be proved rather than hoped for. B's C1 helper has `build_flag`, which emits the very value it checked, so "checked" and "used" cannot drift (B s7 REQ-28). Its REQ-29 repo test fails if a raw `"--model"` appears in an argv builder outside the helper, so a new launcher cannot skip the check. B fails closed when the policy file is missing, so deleting the file does not switch enforcement off (B s2 table, REQ-19). It ships no Jev code at all (REQ-35), which is the purest reading of "Jev only where a measured need exists". It also has the most disciplined verification: a fixed method vocabulary (unit, integration, fixture replay, parity, manual), labels frozen before the run, a second reader on 20% (B s3), and a p95 target of 50 ms checked automatically (REQ-31). It states plainly that `/model`, mods and harness settings are "Cannot see" (B s1 rows 14-16) and does not borrow an unsupported claim about hook timeouts (B s6). Where B is genuinely better than A: C-002, C-003, C-011, C-012, C-020, C-023, X-001, X-009, X-010, X-012, S-003.

### Steelman: Variant C

The strongest case for C: this is an operations problem as much as a parsing problem, and C designs for the operator. Tiers are roles (`judge`, `work`, `light`) with a `restricted` flag, so the policy states what the owner allows and does not assert an unverified gateway-to-family mapping (`claude-gw-tier3` stays "unknown"). The `judge` tier is reachable only from sources a model cannot write (env, `bindings`, grants), never from inline text (C s2). A root-owned managed layer, `/etc/superclaude/model-policy.json`, is the only layer a same-user model cannot edit. Mode is per event class with the strictest layer winning, so rollout is gradual and rollback is one edit with no reinstall (C s8). Grants are one file each, so create and revoke are atomic and a reason and expiry are mandatory. Ids match exactly (`id_prefix_match: false`), and the log never stores raw command text. It also has a single implementation (the script in `--check` mode), so there is no hook/Python drift to test. Where C is genuinely better than A: C-004, C-005, C-007, C-015, C-018, C-019, X-003, S-005.

### Key Strengths Claimed

1. **Fail-closed on launch-shaped input in every session, with a pure-bash prefilter** (A s2 table, last row; REQ-22, REQ-23). The incident sessions were ordinary sessions. The precedent `launch-level-guard.sh:147-163` (verified) exits 0 on any internal failure unless the session is governed, so it would not have stopped them. A's prefilter fails closed only when the raw input mentions `claude`, `superclaude`, `ANTHROPIC_`, `CLAUDE_CODE_` or an Agent call with `model`, so ordinary Bash is never bricked. It also converts its own `timeout 4` expiry to exit 2 for launch events, which is safe whether or not the platform fails open on timeout. Bears on C-013, X-002, X-011.
2. **MP-STAGE-WIDEN: a command prefix may only narrow the session stage** (A s2, REQ-21). The model writes command text, so it must not be able to name `blind-scoring` for itself. A's rule is structural (a subset test on `allow`). C reaches a similar result through a per-stage `declared_by: human` flag plus glob `bindings`, which depends on every sensitive stage being flagged, and B says nothing about prefixes while telling shell launchers to prefix the stage (B s2, "Stage declaration"). Bears on X-013, C-006, A-004.
3. **A second, flat over-approximate pass closes the nested-launch ceilings** (A s5, REQ-08). `bash -c`, `eval`, `ssh host '...'`, `xargs`, `find -exec` and heredoc-to-shell are exactly the ceilings listed in `require-orca-worktree-agent.sh` (enrichment C). A blocks them, B scans only one level of `-c` strings, C lists them as ceilings. Pass 2 can only add blocks, never allow. Bears on X-004, C-010.
4. **Tamper class and registration are consistent** (A s5 TAMPER row, s8 matcher). The matcher `^(Bash|Monitor|Agent|Task|Skill|Edit|Write|NotebookEdit)$` covers every tool the TAMPER rule needs, and it sits inside the existing wide matcher at `hooks.json:116` (verified). C's matcher omits Edit/Write/NotebookEdit while its REQ-31 needs them. Bears on X-007, C-014, C-023.
5. **Closed-world rule keeps table-driven launchers out of the residue** (A s3). If a variable is assigned only from in-file text and every model-shaped literal in the file is allowed, the dynamic argument is bounded. This is plain code, so it shrinks the residue Jev would ever see; B blocks every expansion and so would false-block pinned variables such as `MODEL=claude-sonnet-5-5` then `--model "$MODEL"` (A s3, citing `launch-implement-2.sh:8,28`; UNVERIFIED by me, `.dev/eval-workspaces/` is off limits). Bears on C-009, C-021, S-004.
6. **Blocking an unpinned launch is deterministic** (A s1 row 2, REQ-06). Resolving the "effective default" from the hook's partial view (settings layering, env equality, both UNVERIFIED in B and C) can allow on wrong data. A makes the stage say `require_explicit_model`. Bears on C-008.
7. **A detective layer for "the model used is the model requested"** (A s0, L3). Name checks cannot see `modelOverrides` or a gateway remap; none of the three variants mention `modelOverrides` (diff-analysis A-001). Only L3 compares the observed `.message.model` and `modelUsage` with the request. Bears on C-001, C-022, A-001 (see concession: L3 has no REQ).
8. **Complete decision log** (A s4: `ts, sid, event, tool, stage, decision, rule, model_raw, tier, source, policy_sha8, ms`). It records allows and `would_block`, so false-positive rates and latency come straight from the log. B logs denials only (B s4). Bears on C-016, C-017.
9. **Fits the repo's own conventions** (diff-analysis Step 1 table): seed name `model-policy.json.example` follows the `<dest>.example` seed pattern, and the env name `SC_MODEL_STAGE` is specific where C's `SC_STAGE` is generic. Bears on X-006.
10. **The in-process check sits in `pipeline/process.py`, so eval children are covered even with a per-eval HOME.** `eval/claude_process.py` imports and wraps `ClaudeProcess` (lines 84, 284, verified) and isolates HOME (lines 7, 108-112, verified). A check at the argv build site, `pipeline/process.py:163-164` (verified), runs in the parent process, which keeps the operator's HOME. Note that site only adds `--model` `if self.model:` (verified), so the helper must also handle the no-model case. Bears on A-002, C-002.

### Weaknesses in Variant B

1. **No stated behaviour when `jq` or `awk` is missing** (diff-analysis X-002). B fails closed on "any model-bearing event it cannot resolve", but without `jq` it cannot tell which events are model-bearing, and B never says how it detects them. A answers this with the pure-bash prefilter and REQ-23. Bears on X-002, C-013.
2. **Stage prefixes are unaddressed, and B tells launchers to use them** (B s2, "Stage declaration": "shell launchers prefix it"). A model-written launcher can write `SC_MODEL_STAGE=blind-scoring claude ...`; B has no narrowing rule, so the child can end up governed by a stage the parent never held. Bears on X-013.
3. **Blocks every expansion in a model value** (B s5, MP-03; REQ-05). `--model "$M"` with `M=claude-sonnet-5-5` on an earlier line is a legitimate, fully visible launch and B rejects it. This forces authors to inline literals or flip the policy to observe, which weakens the property over time. It also leaves the table-driven case with no resolution. Bears on C-009.
4. **Tamper protection is partly detective and partly open** (B s5). MP-06 names `Edit|Write` but the matcher omits NotebookEdit (B s8 registration), and redirect/`tee`/`sed -i` are caught only by naming the path. `cp` or a Python write is a "ceiling; detected by audit". The hash-chained journal is written by the same OS user as the model, so a same-user process can regenerate it; B itself says "detection, not blocking". Bears on C-014, C-018, X-007.
5. **Agent-without-model leaves a stale record and an unspecified unknown case** (B s1 row 8, REQ-11). The main model is recorded at SessionStart and "stale after `/model`" (UNVERIFIED mitigations). B does not say what happens when the record is absent (SessionStart `model` is optional, enrichment B4). Bears on C-011.
6. **Labels are written by the rule's author** (B s3, "Labelling"). Even with a second reader on 20%, the label is "the decision the rule requires", which is the rule under test. A's ground truth, the model the run actually used (`modelUsage` in the output JSON), is independent of the rule. B also admits it does not yet know the transcript model key (B s3, UNVERIFIED). Bears on C-022.
7. **A Jev promotion gate that targets a class Jev cannot see** (B s3). Residue class (b) is described by B itself as "a ceiling, not a judgment problem" where Jev sees only short text, yet the gate promotes Jev on 3 misses in that class per 300 events. The second clause (any code-ALLOW on a launch code could see) is a code bug to be fixed in code, not a need for Jev. Bears on C-021.
8. **A wrong repository citation underpins the override guard** (B s4). B reads `process.py:171` as proof that child `claude` carries `CLAUDECODE`. Lines 178-180 (verified) do `env.pop("CLAUDECODE", None)` before spawning the child. TTY remains the load-bearing check. Bears on X-014, C-019.
9. **Overrides are too loose for an enforcement tool**: default 24 h, maximum 168 h (B s4). A two-hour default (A) limits what a rubber-stamped grant can cover. Bears on X-008.

### Weaknesses in Variant C

1. **Launchers depend on an installed hook script** (C s8 step 7; C-002). Each launcher spawns `model-policy-guard.sh --check`, about 40 ms per spawn (C s6), so package code relies on `~/.claude/hooks/` being present. In a dev checkout, CI or a per-eval HOME (`eval/claude_process.py:7,108-112`, verified) that path may not exist. An in-process module has no such dependency. Unwired launchers are only "on the uncovered list", with no repo test to force wiring (compare B's REQ-29). Bears on C-002, C-003, A-002.
2. **Fails open exactly where the incident happened** (C s2 table last two rows; REQ-24, REQ-25). Only a governed session (`SC_STAGE` in the hook env) fails closed on an internal error; every ordinary session fails open. With `jq` or `awk` missing the hook exits 0 (REQ-25), so on such a host every launch passes. Bears on C-013, X-002.
3. **Oversize scripts are allowed unscanned** (C s7, REQ-09: "not scanned and is logged `scan_skipped`"). A script over 256 KB that contains `--model claude-opus-5-5` runs, with only a log line. That is a silent hole in a design whose job is rejection. Bears on X-005.
4. **Tamper rule cannot fire**: MP-07 and REQ-31 require Edit, Write and NotebookEdit, but the registration in C s8 is `Bash|Agent|Task|Skill|Monitor` only (diff-analysis X-007). The policy file can be edited by Write without the hook ever seeing it. Bears on X-007, C-014.
5. **The managed layer is untested and absent here** (C s2; U-013). `/etc/superclaude` does not exist on this host (diff-analysis Step 1). C's 40 REQs contain no test that reads a managed layer, so the layer that is C's main anti-tamper claim has no verification. Bears on X-003.
6. **Inline stage acceptance depends on per-stage flags and forgeable bindings** (C s2, sources 2 and 3; C s10 risk 4). `SC_STAGE=` inline is accepted for every stage not marked `declared_by: human`; a glob binding such as `*/blind-score*.sh` is satisfied by a model writing a script with that name (C's own risk). A's grant binds to the script's sha256, and A's subset rule needs no per-stage flag. Bears on X-013, C-006, A-004.
7. **Unsupported timeout claim and an incomplete mitigation** (C s5 last row). "Platform treats non-exit-2 as non-blocking (B9), so a timeout fails open" is not in B9 (diff-analysis, enrichment B9 covers only non-zero exits other than 2). C converts a self-timeout to exit 2 for governed sessions only. Bears on X-011.
8. **`claude-mention` rule over-blocks** (C s5 row 2; U-017). Any `claude` word with no resolvable flag is treated as dynamic and denied (MP-04), so `claude --version` or `claude mcp list` is blocked in enforce stages (inference from the rule text; UNVERIFIED by test). Bears on X-004.
9. **A possible contradiction between REQ-27 and UserPromptSubmit blocking** (C s7). REQ-27 says the hook "never writes JSON to stdout", yet the only documented way to block a prompt in the enrichment is a JSON decision (enrichment B3), and REQ-16 requires a prompt denial. Whether exit 2 also blocks a prompt is UNVERIFIED. Bears on C-012, X-009.

### Concessions

1. **L0 and L3 are named but not built.** Neither the native floor (generate or seed `deniedModels`) nor the detective check has a REQ, a file in A s8, or an implementation step. L3 is the answer to A-001 only on paper. Without a REQ it is not a v1 deliverable.
2. **A ships a dormant Jev call path** (A s3 "Spec if enabled"; `jev.enabled`, `jev_then_log`, a synchronous 2 s call inside a 5 s hook, REQ-35). The measured-need rule says Jev should enter v1 only where a need is measured; B ships none, C ships a log-only shadow. A's own conclusion ("v1 needs no Jev call") argues for deleting that code from v1.
3. **No policy file means launches are allowed** (A s2 table). Deleting the file switches enforcement off, and the only defence is the TAMPER class on hook-visible paths; the `superclaude doctor` flag is "not designed here". B's rule is safer.
4. **Glob tiers** (`claude-opus-*`, `claude-sonnet-*`, A s2 canonicalisation step 5) admit an unlisted newer version into an allowed tier. Exact ids with unmapped-means-deny (B, C) are the more faithful reading of "any other model is rejected".
5. **No guard against a new unrouted launcher** (compare B's REQ-29). A lists four to five Python sites and says `eval/claude_process.py` was "not read"; I have now confirmed it wraps the pipeline `ClaudeProcess`, but A has no repo test.
6. **Agent-without-model handling is thinner than the documented order** (A s1 row 6): the v1 handling skips the `CLAUDE_CODE_SUBAGENT_MODEL` step and allows when the session model is unknown (REQ-17). That is a fail-open edge.
7. **`/model` handling is indecisive** (A s1 rows 10 and 11: "blocks or records", then "not rejected"). B's re-record is a concrete answer.
8. **Latency bar is loose and manual** (REQ-24: 100 ms / 150 ms, manual benchmark), and the single 5 s registration puts every Edit and Write through the full script (A s8). B's split registration (1 s Edit|Write, as `freshness-pre-edit.sh` at `hooks.json:86-91`, verified) is better engineering.
9. **Project policy path is under gitignored `.claude/`** (A s2). In this repo that path cannot be versioned (CLAUDE.md rule on `.claude/`; diff-analysis X-003). A did not notice; B did.
10. **Closed-world rule has one soundness test** (REQ-11, a comment mentioning Opus). A s3 itself says it is "unsound" in some flows and plans precision/recall measurement, but no REQ pins a hostile case such as an `export` or `source` rebinding.

### Shared-assumption responses

- **A-001: QUALIFY.** A name-based tier check is necessary but not sufficient because `modelOverrides` and gateway remaps can change what is served, so v1 should add a REQ-tested observed-model comparison and state the ceiling.
- **A-002: REJECT.** It is false for eval children, which run in a per-eval HOME (`eval/claude_process.py:7,108-112`, verified); only an in-process check in the parent covers them, and the ceiling must be stated.
- **A-003: QUALIFY.** Observe-first is acceptable, but v1 must name who flips each class and on what evidence, and should enforce the lowest-false-positive cases (literal Opus in `--model` and in the Agent `model` parameter) from day one.
- **A-004: QUALIFY.** One grant per run is workable only if grants bind to a script sha256 and grant frequency is logged, because frequent grants become rubber-stamped and defeat the rule.

### Per-point positions

| Point | Winner | Basis (max 25 words) |
|---|---|---|
| S-001 | A | Headline states the property and each layer's blind spots first; B and C bury them. |
| S-002 | A | Ties with B at 16 rows; C's 9 rows fold frontmatter and alias rows that have distinct visibility limits. |
| S-003 | B | Fixed verification-method vocabulary makes REQs auditable; A's bracket text is mixed and C is almost all unit tests. |
| S-004 | B | B splits the residue into blocked, ceiling and not-a-selection classes; sharper than A's two buckets. |
| S-005 | C | Per-class rollout, a 100-event script threshold and one-edit rollback beat A's phases, which lack rollback. |
| S-006 | A | Artifact stays a design document; B and C append chat-style DONE/NEXT status tables. |
| C-001 | A | Only A has a detective layer for silent substitution, but L0 and L3 lack REQs, so it is incomplete. |
| C-002 | B | build_flag emits the checked value, closing check-then-build drift; A passes the model separately; C spawns a script per launch. |
| C-003 | B | REQ-29 repo test fails on a raw "--model" outside the helper, so new launchers cannot skip the check; A and C have none. |
| C-004 | C | Exact ids admit no unlisted version; A's claude-sonnet-* glob would allow an undefined model. C's docs reason concerns native lists only. |
| C-005 | C | Role tiers avoid asserting an unverified gateway-to-family mapping and survive a change of judge model. |
| C-006 | A | Two seeded stages with sha256-bound elevation are minimal; C's glob bindings are forgeable by naming a script. |
| C-007 | C | Five per-class modes, strictest layer wins, rollback by one edit; A has three classes, B one global switch. |
| C-008 | A | Blocking an unpinned launch is deterministic; resolving the default from the hook's partial view (order and env UNVERIFIED) can allow on wrong data. |
| C-009 | A | Closed-world rule resolves table-driven launchers in code, shrinking Jev's residue; B false-blocks pinned variables; C resolves one regex only. |
| C-010 | A | 256 KB depth-1 shell scan plus a flat scan of a named .py file; B leaves interpreter scripts as a ceiling. |
| C-011 | B | Follows the documented order including CLAUDE_CODE_SUBAGENT_MODEL and re-records on /model; A skips the env step and allows an unknown session model. |
| C-012 | B | Re-recording the model on a /model prompt keeps the inherit check current; A checks only ^/model, C does not re-record. |
| C-013 | A | Pure-bash prefilter fails closed for launch-shaped input in every session; C fails open outside governed sessions, where the incident happened. |
| C-014 | A | Widest tamper class (NotebookEdit, settings, disableAllHooks) matching the launch-level-guard precedent; B's audit is a worthwhile add-on. |
| C-015 | C | Per-class enforcement order with an evidence threshold and no-reinstall rollback; B flips everything at once. |
| C-016 | A | Logs every decision with sha8, event id and latency, enabling false-positive rates; B logs denials only. |
| C-017 | A | Event id and policy path tie each block to its log row; merge C's property sentence and B's do-not-edit line. |
| C-018 | C | One file per grant gives atomic create, revoke, mandatory reason and sha scope; A has no revoke; B's chain is forgeable by the same user. |
| C-019 | C | TTY plus typed yes from /dev/tty is stricter than a bare TTY test; B's process.py:171 reading is refuted by the env.pop at line 179. |
| C-020 | B | Three-option single-item tier question is simplest; A's option (c) needs multi-hop reasoning; C asks what code already knows. |
| C-021 | A | Ties promotion to measured code misses plus precision and false-block limits; B's gate targets a class Jev cannot see. |
| C-022 | A | Observed modelUsage is ground truth independent of the rule under test; merge in B's frozen labels and second reader. |
| C-023 | B | Separate registrations by cost class (1 s Edit|Write like freshness-pre-edit, 3 s launches); add NotebookEdit to B's matcher. |
| C-024 | A | Router output must stay inside the stage allow set and a null routing log field is reserved; C allows updatedInput rewrites. |
| C-025 | NONE | All three leave the native floor manual or deferred; v1 needs a seeded deniedModels snippet derived from policy, with a REQ. |
| C-026 | A | States all sessions with an observe seed, matching the incident (ordinary sessions); B leaves scope implicit; C's governed-only fail-closed misses ordinary sessions. |
| X-001 | B | Fail closed on model-bearing events when policy is missing; A and C let deleting the file switch enforcement off. Seed must be guaranteed. |
| X-002 | A | Pure-bash prefilter fails closed for launch-shaped input without jq, tested by REQ-23; C fails open, B is silent. |
| X-003 | C | Root-owned managed layer is the only one a same-user model cannot edit; A's and B's .claude/ paths are gitignored here. |
| X-004 | A | Flat over-approximate pass blocks bash -c, eval, ssh, xargs and heredoc-to-shell; B scans one level; C keeps the ceiling. |
| X-005 | A | Block oversize script or command; C allows an unscanned script (scan_skipped), a silent hole; B's 64 KB cap false-blocks more. |
| X-006 | A | Seed name follows the repo's <dest>.example pattern and SC_MODEL_STAGE is specific; B's seed name breaks the pattern. |
| X-007 | A | Matcher covers Edit, Write and NotebookEdit; C's omits all three yet REQ-31 needs them; B omits NotebookEdit. |
| X-008 | A | Two-hour default with 24 h cap limits rubber-stamped grants; B's 24 h default and 168 h maximum are too long. |
| X-009 | B | Re-record on /model keeps inherit checks valid; must state UserPromptSubmit firing is UNVERIFIED and not block a person's own choice. |
| X-010 | B | No Jev code or network call in v1 (REQ-35) fits the measured-need rule; A ships a dormant synchronous call path. |
| X-011 | A | Self-timeout converted to exit 2 for launch events is safe either way; the B9 claim in A and C is unsupported, B is right to flag it. |
| X-012 | B | p95 of 50 ms on the fixture corpus, measured automatically; A's 100/150 ms manual bar is loose. |
| X-013 | A | Subset rule (declared stage must narrow the session stage) is structural; C relies on declared_by flags; B is silent yet tells launchers to prefix. |
| X-014 | A | B's reading is wrong (process.py:179 pops CLAUDECODE); the TTY check carries the guard; A and C make no wrong claim. |
| A-001 | QUALIFY | Name checks are necessary but not sufficient (modelOverrides, gateway remap); add a REQ-tested observed-model check and state the ceiling. |
| A-002 | REJECT | False for eval children: per-eval HOME (claude_process.py:7,108-112); only the in-process check in the parent covers them. |
| A-003 | QUALIFY | Accept observe-first, but name who flips and on what evidence, and enforce literal Opus launches from day one. |
| A-004 | QUALIFY | Valid only if grants bind to a script sha256 and grant frequency is logged; frequent grants become rubber stamps. |

