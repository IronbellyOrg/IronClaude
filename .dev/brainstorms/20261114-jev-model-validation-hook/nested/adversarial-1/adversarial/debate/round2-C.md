# Round 2 debate: Advocate C (sonnet:backend), rebuttal

Evidence tags: VERIFIED = I read the file, line or text myself in this session (product files under the repository root, variant files, enrichment file). UNVERIFIED = not checked by me. "variant-N line M" means `variant-N-original.md`. I did not touch `.dev/eval-workspaces/`. Round 2 changes six of my round 1 rows: C-006, C-020, C-021, C-025, X-006, X-011. Each says in Basis what evidence moved it. I keep X-014 against the round 1 majority (A) and say why; C-001 stays A although B dissents.

## Rebuttal: Variant C (sonnet:backend)

### Response to criticisms

Critics: A = round1-A and round2-A; B = round1-B and round2-B. Merged where two critics made the same point.

1. **A and B: the tamper rule cannot fire, the matcher omits Edit, Write and NotebookEdit (X-007, C-014, C-023).** Concede. Variant-3 line 302 registers `Bash|Agent|Task|Skill|Monitor`, while MP-07 and REQ-31 (lines 188, 270) need the three file tools. The existing wide matcher at `hooks.json:116` already lists them and `hooks.json:86-91` shows Edit|Write can run on a 1 s registration (VERIFIED). Fix: split registration as B does (1 s for Edit|Write|NotebookEdit, 5 s for the rest), add `Workflow`.
2. **A and B: fails open without `jq` or `awk`, and fails closed only for governed sessions (X-002, C-013).** Concede. REQ-25 (line 264) makes the hook exit 0 without `jq`, copying `require-orca-worktree-agent.sh:65-72` (VERIFIED). Worse than I said in round 1: I grepped `src/` for `SC_STAGE` and `SC_MODEL_STAGE` and found 0 matches (a repo-wide grep outside `.dev/` and `.git/` for `SC_STAGE` also found 0). So no session today carries `SC_STAGE`, and C's "governed" fail-closed branch covers no session until a launcher sets it. `launch-level-guard.sh:145-155` governs by session records, not by that variable, so my "as the guard does" analogy was loose. A's pure-bash prefilter is the right design; this is a gap in C.
3. **A and B: a missing policy allows, and `rm` or `mv` of the policy is not covered (X-001, C-014).** Concede. REQ-23 allows everything when no policy exists (line 262). Section 5 (line 204) says edits to the policy are blocked "for Bash, Edit, Write and NotebookEdit by path and text", but section 4 (line 187) and REQ-30 (line 269) name only `model-policy grant` and the state directory, so the policy path itself is untested for Bash. X-001 stays B. Fix: in enforce mode, a missing or malformed policy denies positively detected model-bearing calls only (narrow, as B's advocate also agreed), and REQ-30 adds the policy path, `settings*` and `disableAllHooks`.
4. **A and B: scripts over 256 KB are allowed unscanned (X-005).** Concede. REQ-09 (line 248) allows with `scan_skipped`, while a command over 64 KB is denied (REQ-33). Padding a script past the cap turns the scan off. Fix: deny in enforce mode with a size rule, cap tunable in policy as A has it.
5. **A and B: launchers spawn an installed hook script, about 40 ms, and no test forces wiring (C-002, C-003, A-002).** Concede. Line 295 says unwired launchers stay "on the uncovered list" and REQ-39 tests only the helper's return code. B's REQ-29 is the stronger closure. One correction in my favour: A retracted its per-eval HOME argument in round2-A item 10. I read `eval/claude_process.py:238-241, 252-255, 283-289`: the isolated HOME wins in the child env, but `ClaudeProcess(model=self._model)` is built in the parent, so a parent-side check still runs (VERIFIED). The real dependency is an installed `~/.claude/hooks/` file in a dev checkout or CI.
6. **A and B: `judge` is not reachable only from sources the model cannot write; glob bindings and inline stages are spoofable (X-013, C-006).** Concede and move C-006 to A. The seeded binding `*/blind-score*.sh` has no `sha256` (line 50), and my own risk list (line 349) says a model can create a script with a matching name. Inline `SC_STAGE=` is accepted for every stage not marked `declared_by: human` (line 67), which relies on every sensitive stage carrying the flag. A's subset rule needs no flag.
7. **A and B: the timeout claim cites B9 and B9 does not say it (X-011).** Concede. Enrichment line 22 covers non-zero exits other than 2 and says a fail-closed hook must convert its own errors to exit 2; it says nothing on timeouts (VERIFIED). My line 208 also limits the self-timeout to governed sessions, which per item 2 is an empty set today. I move X-011 from NONE to A: A's `timeout 4` converted to exit 2 for launch events (variant-1 line 123) is the mechanism I said was missing.
8. **A and B: the `claude-mention` rule over-blocks `claude --version` and similar (X-004, U-017).** Partly concede. Line 197 says a `claude` word anywhere with no resolvable flag is treated as dynamic, and no REQ in 01-40 tests a pass case for a non-launch mention. The rate is UNVERIFIED. Defence: it only fires when no flag resolves, observe mode logs it first, and A's flat pass 2 (any `claude` word with a `--model` pair anywhere) has the same exposure over a wider pattern. Fix: add a pass-case REQ and limit the rule to the command word and to `-c` or `eval` string arguments.
9. **A: REQ-27 ("never writes JSON") contradicts denying a prompt (C-012, X-009).** Partly concede. I read `launch-level-guard.sh:156-161`: its `prompt` branch denies with `ll_say` and `exit 2`, no JSON, and `hooks.json:63-71` registers it on UserPromptSubmit (VERIFIED). So the repo precedent denies prompts by exit 2. But the enrichment documents only a JSON block for prompts (line 16, VERIFIED), and whether exit 2 blocks a prompt on the platform I did not check against docs (UNVERIFIED). Fix: allow the JSON decision for UserPromptSubmit only and amend REQ-27.
10. **A and B: the managed layer is absent and untested (X-003).** Concede both parts. `ls -d /etc/superclaude` returns rc=2 on this host (VERIFIED), and REQ-20 and REQ-21 name project and user layers, not a managed one. It is still the only layer in any variant a same-user model cannot edit, so X-003 stays C. Fix: add a REQ with a path override for the managed file.
11. **B: E7 says the native list is "generated from the same policy" while section 9 defers generation (C-025).** Concede. Lines 17 and 341 disagree (VERIFIED). With A's L0 also lacking a REQ or a file (see the assessment of A), C-025 becomes NONE.
12. **B: heredoc bodies are "scanned as text" yet a heredoc piped to a shell is a ceiling (X-004).** Concede as a wording defect. A body that sits in the same command string is visible as text (line 199); the ceiling only holds when the body is built at run time. Line 198 should say so.
13. **B: every class starts in observe and only `bash_script` has an exit gate (A-003, C-015).** Partly concede. Lines 329-333 give a 100-event gate for scripts and an order for the rest, but no owner, date or criterion for flipping `bash_claude` and `agent`. All three share this; C-015 stays C because it is the only one with an order and a one-edit rollback.
14. **A and B: C ships a Jev shadow with no measured need, and its gate tests quality, not need (X-010, C-020, C-021).** Concede all three. Line 111 says Jev is not needed in the blocking path, and line 114 feeds Jev only items code already denies as dynamic, so the shadow decides nothing and the question has no decision value. Line 137's gate is precision on 100 residue items and has no code-miss threshold. C-020 moves to B, C-021 to A, X-010 stays B.
15. **B: C omits `claude-gw-tier3` and a `fable` tier, and the matcher has no `Workflow`.** Concede (from my own round 1). Day-one observe will flag `issue-worker-t3` unmapped; add `fable` and `Workflow`.
16. **B (round 2): my `${M:-...}` fear about C is unsupported, but C's REQ-11 does not pin how a `${...}` or conditional assignment is treated (C-009).** Accept. Line 250 pins only a literal `M=claude-sonnet-5-5` followed by `--model "$M"`. Fix: the assignment must be a top-level literal on a line before the use, with no `${`, `$(`, `export` or second assignment; anything else is dynamic and denied. Without this the claim "small and sound" is only half tested.

### Updated assessment of Variant A

A is the strongest of the three on fail-closed behaviour and has conceded most of what was raised.

- Confirmed strengths: the prefilter (variant-1 line 121) fails closed for launch-shaped input without bricking Bash; the flat second pass closes nested launches that the Orca hook lists as ceilings (`require-orca-worktree-agent.sh:39-45`, VERIFIED); MP-STAGE-WIDEN (line 57) is structural; the matcher includes the file tools.
- Confirmed weaknesses: a grep of variant-1 shows no REQ and no file for L0 or L3 (the only matches are lines 11, 14, 32-38 and 376-377), so the layer that tests "used" is a headline, not a deliverable (VERIFIED). Line 159 allows on Jev failure under `jev_then_log`, which contradicts line 156 (VERIFIED). Line 141 admits the closed-world rule is unsound. The override CLI (line 225, REQ-27 line 311) keys on `CLAUDECODE` unset, a signal that `process.py:178-180` pops for launcher children (VERIFIED) and that Step 1 saw only once in this Bash tool. Missing policy allows (REQ-22).
- Where I now rate A higher than in round 1: C-006 (forgeable bindings), X-006 (no precedent for C's name), X-011, C-021.

### Updated assessment of Variant B

B is the best on launcher closure and on missing policy; weaker than its advocate says on fail-closed machinery and on Jev.

- Confirmed strengths: `build_flag` plus REQ-29 makes check and use one operation. I verified `process.py:163-164` adds `--model` only `if self.model:`, so a separate check can drift from the argv (VERIFIED). Missing policy blocks model-bearing events, so deletion is no bypass. No Jev code (REQ-35).
- Confirmed weaknesses: no trap or self-timeout and no jq-missing rule (B conceded). Variant-2 line 89 calls class (b) "a ceiling, not a judgment problem" while line 92 uses class (b) misses as the trigger for Jev (VERIFIED), and the gate has no precision bar. The missing-policy block is wider than needed (lines 70, 72). The override has a 24 h default and 168 h maximum, no revoke command, and a same-user-forgeable chain. The `process.py:171` reading is the reverse of what lines 178-180 do. B's matcher omits NotebookEdit. Its seed name breaks the `<dest>.example` pattern (`install_hooks.py:104-106`, VERIFIED).
- B's own round 2 moved A-003 to QUALIFY because its plan has the same open observe window; I agree.

### New evidence

| # | Claim | Source | Tag |
|---|---|---|---|
| 1 | `SC_STAGE` and `SC_MODEL_STAGE` appear 0 times under `src/`; `SC_STAGE` appears 0 times in the repo outside `.dev/` and `.git/`. Both names are new, and C's "governed" set is empty today | grep, this session | VERIFIED |
| 2 | An ordinary session exits 0 on any internal failure; only a governed one fails closed; the `prompt` branch denies by `exit 2` with no JSON; the guard is registered on UserPromptSubmit | `launch-level-guard.sh:142-163`; `hooks.json:63-71` | VERIFIED |
| 3 | Edit\|Write runs at 1 s (`freshness-pre-edit.sh`); the wide matcher lists Edit, Write, NotebookEdit, Monitor, Workflow at 5 s | `hooks.json:86-91, 115-123` | VERIFIED |
| 4 | The Orca hook fails open without `jq` or `awk` and lists `bash -c`, `eval`, `ssh`, `xargs`, `find -exec`, heredoc-to-shell as ceilings | `require-orca-worktree-agent.sh:39-45, 65-72` | VERIFIED |
| 5 | Seeds are `<dest>.example` | `install_hooks.py:100-106` | VERIFIED |
| 6 | `/etc/superclaude` does not exist on this host | `ls -d /etc/superclaude`, rc=2, 2026-11-14 | VERIFIED |
| 7 | `build_command` adds `--model` only if set; `build_env` pops `CLAUDECODE`; the eval adapter lets isolated HOME win and builds `ClaudeProcess(model=...)` in the parent | `pipeline/process.py:163-164, 178-180`; `eval/claude_process.py:238-241, 252-255, 283-289` | VERIFIED |
| 8 | Enrichment: prompts are blocked by a JSON decision (line 16); a non-zero exit other than 2 is non-blocking and the text says nothing on timeouts (line 22) | `enrichment/codebase-context.md:16, 22` | VERIFIED |
| 9 | Variant text: C matcher line 302; C REQ-09 line 248, REQ-25 line 264, REQ-30 line 269; seeded binding without `sha256` line 50 and own risk line 349; C Jev lines 111, 114, 137; A lines 123, 141, 156, 159, 225, 311 and no L0/L3 REQ; B lines 89 vs 92 | variant files | VERIFIED (document text) |
| 10 | Exit 2 blocks a UserPromptSubmit prompt on the platform; UserPromptSubmit fires for `/model`; hook env equals session env; false-block rate of A's flat pass and C's `claude-mention`; every latency number; a per-eval child loads no operator hooks (inference from HOME override); `launch-implement-2.sh:8,28` and B's 503-transcript count; `reflect/commands.py` default Opus (A and B each read it, I did not) | not checked by me | UNVERIFIED |

### Shared-assumption responses

- **A-001: QUALIFY.** A name check is necessary but not sufficient, because `modelOverrides` and gateway remaps (named by no variant) can change what is served, so v1 must list them as "cannot see" and add an observed-model comparison with a REQ.
- **A-002: REJECT.** The assumption fails as worded because the isolated HOME always wins in an eval child (`claude_process.py:238-241`, verified), and only the parent-side launch check covers the launch.
- **A-003: QUALIFY.** Observe-first is acceptable only with a named owner, a date, exit evidence and day-one enforcement of literal Opus launches and the Agent `model` parameter, and `SC_STAGE` being unused in the repo means no session is "governed" yet.
- **A-004: QUALIFY.** That Opus runs are rare is UNVERIFIED, so count grants in the log, bind script grants to a `sha256`, and have the launcher or a human-owned entry set the stage.

### Per-point positions

Changed from my round 1: C-006 (C to A), C-020 (C to B), C-021 (B to A), C-025 (A to NONE), X-006 (C to A), X-011 (NONE to A). Each cites evidence read this round. I kept X-014 at C against the round 1 majority: the facts tie, and C's guard needs no env signal. I kept C-001 at A: L3 is the only layer aimed at "used" and A-001 needs it, but I verified it has no REQ, so the merge must add one. No vote moved only because others disagreed.

| Point | Winner | Basis (max 25 words) |
|---|---|---|
| S-001 | A | Headline table states each layer's blind spot first; "three layers" over four rows is a wording slip only. |
| S-002 | B | B's rows 14-16 say "Cannot see" plainly; A's rows 10-11 hedge between "blocks or records" and "not rejected"; C folds nine rows. |
| S-003 | B | B's fixed five-method vocabulary makes each REQ checkable; C labels almost everything "[unit test]", including REQ-16 which needs a manual check. |
| S-004 | B | B splits residue into blocked, ceiling and not-an-event with a numeric need rule; C and A ship dormant or shadow Jev paths. |
| S-005 | C | Per-class enforce order, 100-script-event gate and one-edit rollback; no variant names an owner or date. |
| S-006 | A | A ends as a design document; the B and C status-table trailers carry no requirement. |
| C-001 | A | A's L3 is the only layer testing "used", but I verified no REQ names L0 or L3; add one at merge. |
| C-002 | B | B's in-process build_flag emits the checked value; C's launcher spawns an installed script, absent in CI and dev checkouts. |
| C-003 | B | B's REQ-29 fails a build on a raw "--model" outside the helper; C's unwired launchers only sit on a list. |
| C-004 | C | Exact ids plus unknown-deny admit no unlisted version; A's claude-sonnet-* glob admits later ones, and B states no prefix rule. |
| C-005 | C | Role tiers avoid asserting an unverified gateway-to-family mapping. Concession: C needs a fable tier. |
| C-006 | A | Changed from C: C's own risk list (variant-3 line 349) says a script named to match a binding glob gains judge; sha256 pin optional. |
| C-007 | C | Five per-class modes, strictest layer wins, rollback by editing one file; A has three classes, B one flag. |
| C-008 | A | Blocking an unpinned launch needs no guess; resolving a default depends on settings order and hook-env equality, both UNVERIFIED. |
| C-009 | C | REQ-10/11 deny any "$" and resolve one literal assignment; A conceded closed-world is unsound, B moved to C. |
| C-010 | A | Same 256 KB depth-1 shell scan as C plus a named .py file; the cap is policy-tunable. |
| C-011 | B | B and C follow the documented order; only B re-records on /model, closing the stale-record gap C lists as a ceiling. |
| C-012 | B | B re-records the model on /model and locks on unreadable policy; UserPromptSubmit firing stays UNVERIFIED for every variant. |
| C-013 | A | A's pure-bash prefilter fails closed for launch-shaped input in any session; guard.sh:153-155 exits 0 for ordinary sessions, and SC_STAGE is unused in the repo. |
| C-014 | A | Widest tamper class (Edit, Write, NotebookEdit, settings, installer); C's REQ-30 names only grant and state paths, not rm of the policy. |
| C-015 | C | Per-class order, measured gate for scripts, no-reinstall rollback; all three still lack a named owner and date. |
| C-016 | A | A logs every decision with policy_sha8 and ms, so false-positive rate and latency come from the log; C omits both. |
| C-017 | A | Event id ties a block to its log row; message shape is otherwise equal. Low impact. |
| C-018 | C | One file per grant: atomic create, revoke by delete, reason and expiry required; A's append log has no revoke, B's chain is forgeable. |
| C-019 | C | Typed yes from /dev/tty needs no env signal; process.py:178-180 pops CLAUDECODE (verified), refuting B's citation. |
| C-020 | B | Changed from C: variant-3 lines 111, 114 feed Jev only items code already denies as dynamic, so C's question has no decision value. |
| C-021 | A | Changed from B: variant-2 lines 89 and 92 contradict, and variant-3 line 137 tests Jev quality only; A pairs code misses with precision. |
| C-022 | A | Observed modelUsage is ground truth independent of the rule under test; merge B's frozen labels and second reader. |
| C-023 | B | Split registration by cost: Edit\|Write at 1 s as freshness-pre-edit (hooks.json:86-91, verified); C's 5 s matcher omits Edit and Write. |
| C-024 | B | Router output stays a request checked against the allow list; C reserves updatedInput, which is nearer to rewriting a model. |
| C-025 | NONE | Changed from A: grep of variant-1 shows no REQ or file for L0 or L3 (A conceded); C defers generation. None builds it. |
| C-026 | A | A states "all sessions, seeded observe", matching the ordinary-session incident; C's governed-only fail-closed reaches no session today. |
| X-001 | B | Missing policy blocks model-bearing events, so deleting the file is no bypass; narrow to calls that name a model. C allows. |
| X-002 | A | Prefilter plus REQ-23 fails closed on launch-shaped input without jq; C's REQ-25 exits 0 (orca hook lines 65-72, verified). |
| X-003 | C | Only a root-owned layer resists a same-user model; /etc/superclaude is absent here (verified) and no REQ tests it. |
| X-004 | A | Flat second pass closes bash -c, eval, ssh, xargs and heredoc-to-shell, which the orca hook lists as ceilings; false-block rate UNVERIFIED. |
| X-005 | A | A and B block oversize scripts; C's REQ-09 allows an unscanned script over 256 KB, which padding can trigger. |
| X-006 | A | Changed from C: grep shows SC_STAGE is unused in the repo, so C has no precedent edge; A's SC_MODEL_STAGE is more specific. |
| X-007 | A | A's matcher lists Edit, Write, NotebookEdit; C's variant-3 line 302 lists none of them, so REQ-31 cannot pass. |
| X-008 | A | Two-hour default with 24 h cap limits rubber-stamped grants; C gives only a 24 h cap, B 168 h. |
| X-009 | B | B blocks and re-records if UserPromptSubmit fires and says "cannot see" otherwise; A is ambiguous, C defers to the native floor. |
| X-010 | B | B ships no Jev code (REQ-35); A's line 159 allows on Jev failure under jev_then_log; C ships an unneeded inert shadow. |
| X-011 | A | Changed from NONE: A's timeout-to-exit-2 for launch events (variant-1 line 123) is the fix I asked for; enrichment B9 requires converting errors. |
| X-012 | C | C's REQ-34 times the non-matching path every Bash call pays (p95 50 ms, 200 runs); A's 100 ms bar is manual. |
| X-013 | A | MP-STAGE-WIDEN lets a prefix only narrow; C's inline stage works for any non-human stage and its glob bindings are spoofable. |
| X-014 | C | Tie on the facts; A's REQ-27 still keys on CLAUDECODE (variant-1 line 311), observed once only. C needs no env signal. |
| A-001 | QUALIFY | Name checks are necessary, not sufficient; modelOverrides and gateway remaps (named by no variant) need a stated ceiling and an observed-model check. |
| A-002 | REJECT | Isolated HOME always wins (claude_process.py:238-241, verified), so the assumption fails as worded; the parent-side launch check covers only the launch. |
| A-003 | QUALIFY | Observe-first is acceptable only with a named owner, a date, exit evidence and day-one enforcement of literal Opus launches and Agent model parameters. |
| A-004 | QUALIFY | UNVERIFIED that Opus runs are rare; log grant counts, bind script grants to sha256, and set the stage from the launcher. |

