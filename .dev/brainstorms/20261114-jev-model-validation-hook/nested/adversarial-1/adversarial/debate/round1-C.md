# Round 1 advocate output: Variant C

Debate: sc:adversarial, Step 2, Round 1. Variant files read in full. Repository files I read myself: `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` (lines 1-70), `launch-level-guard.sh` (140-170), `src/superclaude/hooks/hooks.json` (80-150), and a grep of `src/superclaude/cli/eval/claude_process.py` for HOME. Anything else is marked UNVERIFIED or relies on the Step 1 "Facts verified" table.

## Advocate: Variant C (sonnet:backend)

### Position Summary

Variant C is the most operable design: per-class observe/enforce modes with one-file rollback, a restricted tier that only sources the model cannot write can unlock, exact id matching, and a grant mechanism that does not depend on an environment variable. It is not the safest on every point: A is better on fail-closed coverage, nested launches and tamper scope, and B is better on missing-policy behaviour and keeping Jev code out of v1. I score each point on merit below and concede where C loses.

### Steelman: Variant A

The strongest case for A is defence in depth aimed at the exact property. L3 compares the model actually observed in the run output (`.message.model`, `modelUsage`) with the requested one, so it is the only mechanism in any variant that tests "used" rather than "written" (A section 0, row L3). A's fail-closed rule is scoped by a pure-bash prefilter on the raw input, so an internal error blocks only launch-shaped calls and never bricks ordinary Bash (A section 2, internal-error row). Its second, flat over-approximate scan can only add blocks, so `bash -c`, `eval`, `ssh`, `xargs` and heredoc-to-shell launches are blocked rather than listed as ceilings (A section 5). MP-STAGE-WIDEN stops the model from naming a wider stage for itself (A REQ-21). The tamper class covers `settings*`, `disableAllHooks` and `install_hooks`, and its matcher includes Edit, Write and NotebookEdit so the rule can actually fire (A section 8). The closed-world rule keeps table-driven launchers like `launch-variants.sh` usable.

Critique after granting all that: A says "Three layers" and then lists four (A section 0). A's Agent-without-model handling skips the `CLAUDE_CODE_SUBAGENT_MODEL` step that the documented order includes (A row 6, handling column; enrichment B5). A ships a synchronous Jev call path with a 2 s timeout (`jev_then_log`) with no measured need, which sits inside a 5 s hook. The flat scan has a false-block risk in a repository full of text about `claude --model opus` (commit messages, notes, heredocs); the rate is UNVERIFIED and A does not measure it. A needs two implementations (bash/jq and Python) kept in step by `vectors.json` (REQ-31), and its p95 pass mark of 100 ms for the hot path is loose.

### Steelman: Variant B

The strongest case for B is the fewest enforcement points with the strictest simple rule. Every model-bearing event is resolved by code or blocked; nothing is judged. REQ-29 fails CI if a raw `"--model"` appears in an argv builder outside the helper, which is the only mechanism in any variant that protects launchers written next year. The in-process `ModelPolicyError` has no spawn cost and no jq dependency. B is the only variant that says a hook timeout is UNVERIFIED rather than asserting platform behaviour (B section 6). It writes no Jev code at all (REQ-35), which is the cleanest reading of "Jev only where a measured need exists". It blocks model-bearing events when the policy is missing, so the policy cannot be disabled by deleting it. The measured-need rule (at least 3 labelled misses per 300 events, or any labelled code-ALLOW/label-BLOCK) is the most direct test of need.

Critique after granting all that: B's seed name `model-policy.example.json` breaks the verified `<dest>.example` pattern in `_SEED_FILES` (Step 1 table). B reads `process.py:171` as proof that child `claude` carries `CLAUDECODE`, but Step 1 verified the lines remove it (`env.pop`). B blocks every `--model "$M"` (MP-03) even when `M` is assigned once in the same file, so a compliant script like `launch-implement-2.sh` (cited by A at lines 8 and 28) is false-blocked. A missing or malformed policy blocks all Agent, Task, Workflow and Monitor calls (B section 2 table), which is an outage amplifier; B's own risk 7 admits it. Its Bash tamper rule is named-path only (`redirect`, `tee`, `sed -i`), and its hash-chained journal is written by a same-user CLI, so a same-user forger can rebuild the chain (my reading; UNVERIFIED as an attack, but the chain is not signed anywhere in B section 4). B has no self-timeout and does not say what happens when jq is missing (X-002).

### Key Strengths Claimed

1. **Operable rollout.** Per-class modes (`bash_claude`, `bash_script`, `agent`, `skill`, `prompt_command`), strictest-layer-wins (REQ-21), enforce order by false-positive risk, a 100-event gate before `bash_script`, and rollback by editing one policy file with no reinstall (C section 8 Rollout, section 2 Scoping). A has three event modes and B has one global flag. Bears on C-007, C-015, S-005.
2. **A restricted tier the model cannot self-grant inline.** `judge` is `restricted` and allowed only through the hook env, a binding or a grant (C section 2, REQ-17, REQ-18). This directly encodes "Opus is for blind scoring only". Bears on C-005, C-006. (The inline-prefix hole for non-human stages is conceded below, X-013.)
3. **Exact ids, unknown denied.** `id_prefix_match: false` plus `unknown_model: deny` keeps "defined model equals used model" and makes `claude-gw-tier3` show up in observe logs instead of passing (C section 2 notes; docs fact B7 says an id entry also permits later versions). Bears on C-004.
4. **Grant design that survives scrutiny.** One file per grant (no append races, revoke by delete), expiry required and capped, a typed `yes` read from `/dev/tty`, and no reliance on `CLAUDECODE` (which `process.py:171-179` removes per Step 1). The decision log never stores command text (C section 4). Bears on C-016, C-018, C-019, X-014.
5. **Jev kept inert and narrow.** Shadow only, default off, async, log only, with a `none` option; if Jev is down there is no fail-open versus fail-closed question because it decides nothing (C section 3). Bears on C-020. (Whether shipping even this is right is conceded under X-010.)
6. **Hot-path latency is the pass mark.** p95 at most 50 ms on the non-matching path over 200 runs (REQ-34), plus a per-event time table with recommended timeouts (C section 6). Every Bash call pays that path. Bears on X-012 and the "time cost small" property.
7. **Per-event missing/malformed table.** Two columns: ordinary events and positively detected model-choosing events. A malformed policy in enforce mode denies a launch but still allows `ls`, so the fix path is never bricked (C section 2 table, REQ-22). Bears on X-001 (partially; see concession).
8. **A tamper-proof layer in principle.** The root-owned `/etc/superclaude/model-policy.json` layer is the only layer in any variant that a same-user model cannot edit; availability is UNVERIFIED (Step 1: the directory does not exist today). Bears on X-003.

### Weaknesses in Variant A

1. **Missing policy allows (X-001).** A section 2 table: no policy file means launch events are allowed with `no_policy` logged. Deleting the policy then silently disables enforcement, which re-creates the incident condition (a rule that exists nowhere mechanical). B blocks in enforce mode; A should too.
2. **Documented Agent order is incomplete (C-011).** Enrichment B5 lists the order: parameter, frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL`, main model. A's handling (row 6) reads frontmatter, then the recorded session model, and never checks the env step. An Agent call under a set `CLAUDE_CODE_SUBAGENT_MODEL` is judged against the wrong model.
3. **Unmeasured Jev code in the hook (X-010).** A section 3 "Spec if enabled" builds a synchronous call with a 2 s timeout, a 2 KB excerpt sent off-machine, and a stage option `jev_then_log`. Nothing measured calls for it, and A's own conclusion is "v1 needs no Jev call". Dormant code in a security hook is attack surface and test burden with no payoff; B ships none.
4. **Timeout claim not supported (X-011).** A section 2 says a platform timeout is a non-blocking error "(B9)". Enrichment B9 covers only non-zero exits other than 2 (Step 1 table). A states as fact what its source does not say.
5. **Flat scan false-block risk is unmeasured (X-004).** Pass 2 blocks whenever the word `claude` appears with a `--model X` pair anywhere in the text. In this repository, text such as commit messages, `grep` patterns and heredocs that write documentation mention `claude --model opus`. A has no REQ that bounds the false-block rate (REQ-08 tests only that attacks are blocked). The rate is UNVERIFIED; observe mode would reveal it, but A does not make it a gate.
6. **Two implementations to keep in sync (C-002).** `check_launch` in Python and the bash/jq hook must agree (REQ-31). `vectors.json` helps, but it is permanent drift risk that B shares and C avoids for launchers only by delegating to the one script.
7. **Latency bar is loose (X-012).** REQ-24 accepts p95 100 ms for non-launch Bash and is a manual benchmark. The hot path runs on every Bash call alongside four existing PreToolUse hooks on `hooks.json` (lines 96, 106, 116, 126 as I read them); a bar of 50 ms is more honest about the cost.

### Weaknesses in Variant B

1. **Wrong seed file name (X-006).** `model-policy.example.json` breaks the `<dest>.example` rule that Step 1 verified at `install_hooks.py:104-106` (`auggie-projects.txt.example`). It would likely fail a naming check or confuse the next maintainer. A and C get this right.
2. **Wrong reading of `process.py:171` (X-014, C-019).** B's override guard says "child `claude` processes carry this variable". Step 1 verified the lines `env.pop` it. The `CLAUDECODE` refusal is not wrong for a human terminal, but the cited proof is false and a reviewer following B's citation will draw the opposite conclusion.
3. **No resolution for compliant dynamic launches (C-009).** B blocks any `--model "$M"` (REQ-05, MP-03). A compliant script with `M=claude-sonnet-5-5` then `--model "$M"` is blocked, so the owner must rewrite working scripts or switch the hook to observe. A and C resolve one in-file assignment.
4. **Missing or malformed policy blocks every Agent, Task, Workflow and Monitor call (X-001, section 2 table).** One bad edit stops all subagent work, and B's own risk 7 says so. A narrower class (a positively detected launch, as in C's table) gives the same safety on the incident path without the outage on Agent calls that name an allowed model. Note, though, that C loses X-001 to B overall because C allows when the file is absent.
5. **Tamper detection by named path only (C-014).** B's MP-06 covers Edit/Write plus `redirect`, `tee` and `sed -i` naming the policy path. `cp`, `mv`, `rm` and a Python write are listed as a ceiling "detected by audit". Audit runs when someone runs it; the hash-chained journal is written by the same user and is not signed, so a forger who can write the override file can rebuild the chain (UNVERIFIED as an attack, but nothing in B section 4 prevents it).
6. **No self-timeout and no jq-missing rule (X-002, X-011).** B fails closed on events it "cannot resolve", but does not say what happens when jq or awk is absent, and has no wrapper that converts its own timeout to exit 2. B is honest that timeout behaviour is UNVERIFIED, then relies on "staying well under" it.
7. **Matcher gaps (C-023).** B's `Edit|Write` registration omits NotebookEdit, and a 3 s Bash timeout stacks with four other Bash hooks. The latter is the same as C; the former is a real gap in B's MP-06.
8. **Python-only coverage of launchers makes the hook script depend on Python helper parity (REQ-30).** Acceptable, but the cost is a parity suite plus a copied tokenizer with its own parity test (B risk 4): two parity contracts to maintain.

### Concessions

1. **The registration omits the tools its tamper rule needs (X-007).** C section 4 and REQ-31 deny Edit, Write and NotebookEdit on the policy, but the section 8 PreToolUse matcher is `Bash|Agent|Task|Skill|Monitor`. MP-07 for file edits can never fire as written. This is a plain defect. Fix: add the three tools (A's matcher shows how).
2. **Fails open without jq or awk (X-002).** C copies `require-orca-worktree-agent.sh` (lines 65-70 print "fail open"). That is correct for an unrelated worktree hook and wrong here: on such a host the exact incident path stays open. A's pure-bash prefilter is the better design.
3. **Missing policy allows, and deletion is not covered (X-001).** MP-07 and REQ-30 name `model-policy grant` and the state directory, not `rm ~/.claude/model-policy.json`. A model can delete the policy through Bash, and C then allows everything with only a `no_policy` log line. B's behaviour is safer.
4. **Fail-closed on internal error only for governed sessions (C-013).** `launch-level-guard.sh:147-163` fails closed only when `LL_GOVERNED=1`, and C copies that. The incident sessions were ordinary sessions with no `SC_STAGE`, so an internal error there allows. A's launch-shaped prefilter covers them.
5. **Script over 256 KB is allowed (X-005).** REQ-09 allows and logs `scan_skipped` while REQ-33 blocks a command over 64 KB. An unscanned script is the largest possible blind spot, so that is inconsistent fail-open.
6. **Inline `SC_STAGE=` accepted for non-human stages, and glob bindings can be spoofed (X-013).** The model can name any stage not marked `declared_by: human`; C's own risk list admits a model can create a script with a name that matches a binding glob. A's MP-STAGE-WIDEN is the correct rule.
7. **Launcher coverage is weaker than B's (C-002, C-003).** The hook script spawn costs about 40 ms per launch (C's own estimate, UNVERIFIED), depends on jq being present, and unwired launchers are only "listed as uncovered". B's helper plus REQ-29 CI test is stronger.
8. **Native floor is promised and then deferred (C-025).** E7 says the native list is "generated from the same policy", while section 9 leaves generation to v2. `/model` therefore has no cover in v1.
9. **Timeout claim is unsupported (X-011).** C cites enrichment B9 for "a timeout fails open"; B9 does not say that (Step 1 table). Its self-timeout also applies to governed sessions only.
10. **Jev shadow code ships without measured need (X-010, C-021).** B ships none. C's gate (100 residue items, precision 0.95) tests Jev quality but never asks whether code is wrong, so it does not meet "Jev only where a measured need exists".
11. **Gaps in coverage.** No `fable` tier, no `Workflow` in the matcher (B has it, and existing `hooks.json:116` has it), and an unverified project path: `.superclaude/` is gitignored (Step 1), and `/etc/superclaude` does not exist on this host.
12. **No owner and no date for flipping enforce (A-003).** C gives per-class gates but still no named decision maker.
13. **Effective-default resolution rests on unverified assumptions (C-008).** C resolves the default model from hook env and settings; whether hook env equals session env is UNVERIFIED (A and C both say so).

### Shared-assumption responses

- **A-001: QUALIFY.** Accept that names map to served models only for the host table's ids; `modelOverrides` and gateway remaps are not mentioned by any variant and must be stated as a ceiling, with A's observed-model check as the only detective cover.
- **A-002: REJECT.** The assumption is false for eval children: `src/superclaude/cli/eval/claude_process.py` isolates HOME per eval (lines 7, 108-112 by my grep), so those children load neither `~/.claude` hooks nor `~/.claude/model-policy.json`; only an in-process check in the launcher covers them.
- **A-003: QUALIFY.** The observe window is a real exposure and acceptable only if a named owner flips the highest-risk classes (`bash_claude`, `agent`) to enforce first, with a date.
- **A-004: QUALIFY.** The assumption that legitimate Opus runs are rare is UNVERIFIED; the observe log should count them, and sha256-pinned script bindings or grants reduce rubber-stamping if they are frequent.

### Per-point positions

| Point | Winner | Basis (max 25 words) |
|---|---|---|
| S-001 | A | A's headline table states layers and blind spots up front, though it says "three layers" over a four-row table. |
| S-002 | B | Finer rows with explicit "cannot see" lines state visibility more plainly than C's nine folded rows. |
| S-003 | B | B's fixed verification vocabulary makes each REQ checkable; C's near-uniform "[unit test]" hides manual and timing checks. |
| S-004 | B | B states a numeric measured-need rule and ships zero Jev code; A and C ship dormant or shadow Jev paths. |
| S-005 | C | C's per-class rollout order, 100-event script gate and edit-one-file rollback is the most operable; A and B flip more coarsely. |
| S-006 | A | A ends without a chat-style status table; the trailer is noise in a design document and carries no requirement. |
| C-001 | A | A's detective L3 compares observed model to requested, the only check of "used" rather than "written"; C has none. |
| C-002 | B | B's in-process helper has no spawn cost or jq dependency and raises before Popen; C's hook-script spawn adds failure modes. |
| C-003 | B | B's REQ-29 test fails CI on any raw "--model" outside the helper, so new launchers cannot skip the check. |
| C-004 | C | C's exact ids (id_prefix_match false) and unknown-deny keep defined equals used; A's globs admit later versions. Brittle on new ids; observe surfaces them. |
| C-005 | C | Role tiers keep policy host-independent where "opus" maps to gateway ids; A's family names are closer to owner vocabulary. C must add fable. |
| C-006 | C | Bindings plus declared_by human give durable stage sources; A's env-only stage cannot name approved scripts. Inline-prefix hole is scored in X-013. |
| C-007 | C | Per-class modes let bash_claude and agent enforce first and any class roll back alone; A has three event modes, B one flag. |
| C-008 | A | A's require_explicit_model needs no guess; B and C resolve a default from env and settings the hook may not see (UNVERIFIED). |
| C-009 | C | C resolves one in-file assignment, denies the rest: small and sound. B false-blocks compliant scripts; A's closed-world heuristic adds unsound surface. |
| C-010 | A | A also scans a .py file named in the command; scope otherwise equals C, and ceilings are stated in both. |
| C-011 | B | B follows the documented order including CLAUDE_CODE_SUBAGENT_MODEL and re-records on /model; A skips the env step. |
| C-012 | B | B's policy-unreadable session lock and /model re-record add fail-safe behaviour; UserPromptSubmit firing is UNVERIFIED for all three. |
| C-013 | A | A's pure-bash prefilter fails closed for launch-shaped input in any session; C only for governed sessions, but incident sessions were ordinary. |
| C-014 | A | A's TAMPER class covers Bash edits of policy, settings, disableAllHooks and install_hooks; C's MP-07 misses rm or mv of the policy file. |
| C-015 | C | C has per-class order, measured gates and no-reinstall rollback; A and B flip globally. None names an owner or date. |
| C-016 | A | A logs policy_sha8 and ms, so a block matches a policy version and latency is measurable; C omits both. |
| C-017 | A | A adds an event id tying a block to its log row; message shape is otherwise equal. Low impact. |
| C-018 | C | One file per grant avoids append races and torn lines and revokes by delete; B's unsigned hash chain is forgeable by the same user. |
| C-019 | C | C needs a TTY and typed yes from /dev/tty, no reliance on CLAUDECODE; B's process.py:171 reading is wrong (Step 1: env.pop). |
| C-020 | C | C asks a short single-item question (is the model hidden?) with a none option; A and B ask Jev for values code already derives. |
| C-021 | B | B ties promotion to labelled code misses, the measured-need test; C's gate tests Jev precision but not whether code is wrong. |
| C-022 | A | A's ground truth is observed modelUsage in run JSON, which tests "used"; mutants reported separately. B's frozen labels are close second. |
| C-023 | B | B's split matchers (3 s Bash, 1 s Edit/Write) mirror sibling hooks and bound stacking; C's 5 s matcher omits Edit/Write. |
| C-024 | B | B keeps router output a request checked against stage allow; C permits updatedInput under an explicit mode, nearer to rewriting. |
| C-025 | A | A ships the native floor in v1, the only cover for /model; C says generated from policy yet defers generation to v2. |
| C-026 | A | A states "all sessions, seeded observe" explicitly; B implies it; C's governed-only fail-closed adds ambiguity. |
| X-001 | B | B blocks model-bearing events when policy is missing in enforce mode; A and C allow, so deleting the policy silently disables enforcement. |
| X-002 | A | A's pure-bash prefilter fails closed on launch-shaped input without jq; C copies fail-open and leaves the incident path open. |
| X-003 | C | C's root-owned managed layer is the only one a same-user model cannot edit (availability UNVERIFIED); every project path here is gitignored. |
| X-004 | A | A's flat over-approximate second pass blocks bash -c, eval, ssh, xargs and heredoc shells and can only add blocks; C keeps ceilings. |
| X-005 | A | A and B block oversize scripts; C allows scripts over 256 KB while blocking commands over 64 KB, an inconsistent fail-open. |
| X-006 | C | C follows the verified .example seed pattern and guard-suffix naming; B's seed name breaks it. A's SC_MODEL_STAGE is the better env name. |
| X-007 | A | A's matcher lists Edit, Write, NotebookEdit; C's tamper rules need them but its matcher omits them, so MP-07 file-edit cases never fire. |
| X-008 | A | A fixes default 2 h and maximum 24 h; shorter windows limit rubber-stamp exposure. C gives only a maximum, B allows 168 h. |
| X-009 | B | B blocks and re-records on /model where UserPromptSubmit fires, labelled UNVERIFIED; C covers nothing; A is internally ambiguous. |
| X-010 | B | B ships no Jev code (REQ-35); C's inert shadow and A's dormant synchronous call add unmeasured code beside the blocking path. |
| X-011 | NONE | None adequate: state timeout behaviour UNVERIFIED (as B) and add a self-timeout converting to exit 2 for all launch-shaped events. |
| X-012 | C | C measures the non-matching path every Bash call pays, p95 at most 50 ms over 200 runs; A's 100 ms is loose, B's corpus mixes paths. |
| X-013 | A | A's MP-STAGE-WIDEN lets a prefix only narrow; C lets command text pick any non-human stage and glob bindings are spoofable (C's own risks). |
| X-014 | C | B's reading is wrong: process.py:171-179 removes CLAUDECODE (Step 1). C's /dev/tty confirmation does not depend on that variable. |
| A-001 | QUALIFY | Accept for names only; modelOverrides and gateway remaps are unmentioned, so state them as a ceiling and use A's observed-model check. |
| A-002 | REJECT | Eval children run under a per-eval HOME (eval/claude_process.py:7,108-112), so they load neither hook nor policy; only the in-process check covers them. |
| A-003 | QUALIFY | Observe-first is a real exposure window; accept it only with a named flip owner, a date, and highest-risk classes enforced first. |
| A-004 | QUALIFY | UNVERIFIED; blind-scoring frequency is unmeasured. Count Opus grants in the observe log, and pin script bindings by sha256 to limit rubber-stamping. |

