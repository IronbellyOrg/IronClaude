# Round 2 debate: Advocate A (sonnet:architect), rebuttal

Evidence tags: VERIFIED = I read the line or text myself in this session (product files under the repository root, or the variant files); UNVERIFIED = not checked by me. Variant citations use the variant file name and line. Round 2 changes four of my round 1 rows (S-002, C-009, C-024, X-012); each says why in the Basis column. I did not touch `.dev/eval-workspaces/`.

## Rebuttal: Variant A (sonnet:architect)

### Response to criticisms

Criticisms by B (round1-B "Weaknesses in Variant A" 1-8) and by C (round1-C "Weaknesses in Variant A" 1-7 plus its steelman critique) are merged where they are the same point.

1. **B and C: a dormant Jev path ships in v1 and can turn a block into an allow (X-010, C-020).** Concede. A's text says that under `jev_then_log` an unreachable Jev leaves "allow-and-log" (variant-1 line 159). So choosing that stage option loosens the stage default `closed_world_then_deny`, and the claim "Jev can never turn a code block into an allow" (line 156) holds only relative to that loosened default. A's own conclusion is "v1 needs no Jev call" (line 143). Delete the path from v1; X-010 stays B.
2. **B: the closed-world rule is unsound and A pins only the easy case (C-009).** Concede. A lists "in-file flows where the closed-world rule is unsound" as residue (line 141) yet applies the rule first. REQ-10 (line 294) pins single assignment, REQ-11 (line 295) pins only an Opus word in a comment, and nothing pins `M=${M:-claude-sonnet-5-5}` with `M` set to Opus in the environment. The mutant list in the test plan (line 177) measures such cases but gates nothing. I move C-009 to C (below).
3. **B and C: Agent without `model` skips the env step and allows when the session model is unknown (C-011).** Concede. Row 6 (line 31) lists the documented order but its handling skips `CLAUDE_CODE_SUBAGENT_MODEL`, and REQ-17 (line 301) allows when the session model is unknown. A fix inside A's own principles: with `inherit_check: true`, an unknown session model blocks. Still B's point.
4. **B and C: the flat pass 2 may false-block read-only text that mentions a launch (X-004).** Partly concede. REQ-08 (line 292) tests only blocks, and no REQ says a `grep` for `--model claude-opus-5-5` must pass. The false-block rate is UNVERIFIED (by B, by C and by me). Defence: pass 2 can only add blocks, every would-block is logged in observe mode (REQ-25, line 309), and the other designs leave real holes. I verified the Orca hook lists `bash -c`, `eval`, `ssh`, `xargs`, `find -exec` and heredoc-to-shell as ceilings (`require-orca-worktree-agent.sh:39-45`). I keep X-004 as A and add a REQ: pass 2 starts in observe and a non-launch mention must pass.
5. **B: L3 has no REQ and no file (C-001, U-001).** Concede (also in round 1). L0 and L3 are in the headline table (lines 11, 14) and the recommendation (line 378) but not in REQ-01..35 or "Files to add" (lines 323-328). They are v1 gaps, not v1 deliverables. I keep C-001 as A only because every advocate's A-001 answer asks for exactly this observed-model check.
6. **B and C: the timeout claim cites B9, which does not support it (X-011).** Concede the citation: Step 1 records that B9 covers only non-zero exits other than 2. Line 123 uses it as the reason for the self-timeout. The mechanism (`timeout 4` converted to exit 2 for launch events) is safe whichever way the platform behaves, and C's alternative for X-011 ("state UNVERIFIED and add a self-timeout") is A with the citation corrected. X-011 stays A, with the claim re-marked UNVERIFIED.
7. **B: glob `ids` admit later versions (C-004).** Concede for the allow side. `claude-sonnet-*` (line 69) admits an unlisted newer Sonnet. Globs are safe on the deny side only (an unlisted newer Opus is still denied). C-004 goes to C.
8. **B: the hook reads only the last 200 override lines (C-018).** Concede, minor. A still-valid grant older than 200 appended lines is ignored (line 228), which is a false block, not a false allow. One file per grant (C) removes it. C-018 goes to C.
9. **C: "Three layers" is followed by a four-row table (S-001).** Concede as a wording slip (lines 7 and 9-14). The table itself is what S-001 judges, so S-001 stays A.
10. **C: two implementations (bash/jq and Python) can drift (C-002).** Partly concede. `vectors.json` plus REQ-31 (line 315) mitigates, but B has the same cost, and B's `build_flag` plus REQ-29 is the better closure. I also retract a round 1 argument: I said C's launcher spawn could fail under a per-eval HOME. I verified that the isolation applies to the child's env (`claude_process.py:228-255`, `isolation.py:665-668`), while the launcher check runs in the parent, so only a missing installed hook (dev checkout, CI) is the real dependency for C.
11. **C: latency bar of 100 ms and 150 ms is loose and manual (X-012).** Concede. REQ-24 is `[manual benchmark]` (line 308). C's REQ-34 is an automated timing test on the non-matching path (variant-3 line 273). X-012 moves to C.
12. **B: A's `check_launch(stage, model)` is separate from the argv builder (C-002, C-003).** Concede. I verified that `ClaudeProcess.build_command` adds `--model` only `if self.model:` (`process.py:163-164`), so a check that is not tied to the builder can drift from the value used, and A has no test for a new unrouted launcher.
13. **B: A's `require_explicit_model` over-blocks versus resolving the effective default (C-008).** Reject. B's own text says the order of `ANTHROPIC_MODEL` and settings `model` is UNVERIFIED and that hook env equals session env is UNVERIFIED (variant-2 line 16), so resolution can allow on wrong data. A's rule blocks the unpinned launch, which is the inherit path the incident used.
14. **B: A's 256 KB scan costs more than B's 64 KB (C-010).** Partly concede. A's own worst case is 400 ms (line 264, estimate, UNVERIFIED). `script_max_kb` is a policy field (line 79), so the owner can lower it toward 64 KB. A also scans a named `.py` file, which B leaves as a ceiling. I keep C-010 as A.
15. **C: A's L0 floor is promised and not built (C-025).** Concede; C-025 stays NONE.

### Updated assessment of Variant B

B is stronger than I scored it in round 1 on one structural point and weaker than its advocate says on three.

- Stronger: `build_flag` makes the checked value the used value, REQ-29 forces new launchers through the helper, and B names the `reflect/commands.py` default site. I verified `_DEFAULT_MODEL = "opus"` (line 37) and `model = os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL` (line 365). That config then reaches `config.model` in `reflect/runner.py:507-508`, so an argv-site check also sees it, but the product itself defaults reflect to Opus. Day-one observe logs will flag it in every variant.
- Weaker: MP-03 blocks every expansion, including a pinned single assignment, with no resolver (variant-2 lines 88, 153, 195). B's X-014 reading is wrong (`process.py:178-180` pops `CLAUDECODE`). B's seed name breaks the verified pattern (`install_hooks.py:104-105`). B has no jq-missing rule, its matcher omits NotebookEdit, its override window is 24 h default and 168 h maximum, and its log records denials only while its exit criterion counts live events.
- B's missing-policy rule (X-001) is the best of the three, as B's advocate conceded it should be narrowed to calls that name a model.

### Updated assessment of Variant C

C is the best operated design and the weakest on fail-closed coverage.

- Stronger than I said: C's single in-file assignment regex with everything else denied (variant-3 lines 107, 200, 249-250) is the sound minimum for C-009, and its REQ-34 timing test targets the path every Bash call pays.
- Confirmed weaknesses: it copies the fail-open precedent. I verified the Orca hook allows on missing `jq` or `awk` (`require-orca-worktree-agent.sh:65-72`) and the guard fails closed only for governed sessions ("an ordinary session is never blocked by a failure", `launch-level-guard.sh:142-163`). The incident sessions were ordinary. REQ-09 allows an unscanned script over 256 KB (variant-3 line 248). Its tamper rule needs Edit, Write and NotebookEdit but the registration lists Bash, Agent, Task, Skill, Monitor only; the existing wide matcher at `hooks.json:116` shows those tools are registrable.
- C's managed layer is real in design and untested and absent on this host; it needs a REQ before it counts as a v1 anti-tamper claim.

### New evidence

| # | Claim | Source | Tag |
|---|---|---|---|
| 1 | `ClaudeProcess.build_command` adds `--model` only when `self.model` is set; `build_env` pops `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` | `src/superclaude/cli/pipeline/process.py:163-164, 178-180` | VERIFIED |
| 2 | The eval adapter passes `model` into `ClaudeProcess` and merges the per-eval `HOME` last, so the child gets a scratch HOME while the launch check in the parent keeps the operator's | `eval/claude_process.py:233-241, 284-289`; `eval/isolation.py:665-668` | VERIFIED |
| 3 | `isolation.py` has no "hooks" string, so isolation does not seed operator hooks; that a per-eval child therefore loads no `~/.claude` hooks is an inference | `eval/isolation.py` (grep, 0 matches) | VERIFIED absence; inference UNVERIFIED |
| 4 | Edit and Write already run `freshness-pre-edit.sh` at 1 s; `launch-level-guard.sh` is registered on a wide matcher that includes Edit, Write, NotebookEdit at 5 s | `hooks/hooks.json:86-91, 115-123` | VERIFIED |
| 5 | The guard fails closed only when governed; ordinary sessions are never blocked by an internal failure; commands over 64 KB are class BIG | `hooks/scripts/launch-level-guard.sh:142-163, 422-423` | VERIFIED |
| 6 | The Orca hook fails open without `jq`/`awk` and lists `bash -c`, `eval`, `ssh`, `xargs`, `find -exec`, heredoc-to-shell as ceilings | `hooks/scripts/require-orca-worktree-agent.sh:39-45, 57, 65-72` | VERIFIED |
| 7 | Seed files are named `<dest>.example` | `cli/install_hooks.py:104-105` | VERIFIED |
| 8 | Reflect defaults to Opus (`_DEFAULT_MODEL = "opus"`, `ANTHROPIC_MODEL` override) and passes it as `config.model` to the argv at `runner.py:507-508` | `cli/reflect/commands.py:37, 365`; `cli/reflect/runner.py:507-508` | VERIFIED |
| 9 | A's own text admits closed-world unsoundness and REQ-11 tests only a comment; C's REQ-10/11 pair is the minimal resolver; B's line 279 bounds router output by the allow list | variant-1 lines 141, 295; variant-3 lines 249-250, 273; variant-2 line 279 | VERIFIED (document text) |
| 10 | `launch-implement-2.sh:8,28` pinned-variable pattern; B's 503-transcript count; whether `UserPromptSubmit` fires for `/model`; hook env equals session env; pass 2 false-block rate; all latency numbers; `/etc/superclaude` as a usable managed layer | not read (off-limits folder or not checkable read-only) | UNVERIFIED |

### Shared-assumption responses

- **A-001: QUALIFY.** A name check is necessary but not sufficient because `modelOverrides` and gateway remaps (named by no variant) can change what is served, so v1 must state that ceiling and add a REQ-tested observed-model comparison.
- **A-002: REJECT.** As worded it is false for eval children, which get a per-eval HOME (`claude_process.py:238-241`, `isolation.py:665-668`, verified); only the parent-side launcher check covers the launch and the child's inner calls are a stated ceiling.
- **A-003: QUALIFY.** Observe-first is acceptable only with a named owner, exit evidence, and day-one enforcement of the zero-ambiguity cases (literal Opus in `--model`, Opus in the Agent `model` parameter).
- **A-004: QUALIFY.** One grant per run is workable only if grants bind to a script sha256 and grant frequency is logged, because the "rare Opus runs" premise is UNVERIFIED.

### Per-point positions

Changed from my round 1: S-002 (A to B), C-009 (A to C), C-024 (A to B), X-012 (B to C). C-021 (split) I keep as A. No vote moved because two advocates disagreed; each change cites evidence read this round.

| Point | Winner | Basis (max 25 words) |
|---|---|---|
| S-001 | A | Headline table states the property and each layer's blind spot first; "three layers" over four rows is only a wording slip. |
| S-002 | B | Changed from A: re-read A rows 10-11 ("blocks or records" vs "not rejected") show unclear visibility; B rows 14-16 say "Cannot see" plainly. |
| S-003 | B | Fixed five-method verification vocabulary makes each REQ auditable; A's bracket text is mixed (REQ-24 is manual), C's is nearly all unit tests. |
| S-004 | B | B splits the residue into blocked, ceiling and not-a-selection classes and sets a measured-need rule; A has two buckets, C ships a shadow call. |
| S-005 | C | Per-class rollout order, 100-script-event gate and one-edit rollback beat A's phases, which name no rollback or owner. |
| S-006 | A | Design document ends without a chat-style status table; B and C append status-table trailers that carry no requirement. |
| C-001 | A | Only A has any check of the model actually used (L3), though L0 and L3 lack REQs and files; merge them in as v1 items. |
| C-002 | B | build_flag emits the checked value; I verified process.py:163-164 adds --model only if set, so a separate check_launch can drift from the argv. |
| C-003 | B | REQ-29 fails a build on a raw "--model" outside the helper; A and C have no test forcing new launchers through the check. |
| C-004 | C | Exact ids with unmapped-denied admit no unlisted version; A's allow-side globs (claude-sonnet-*) do. Glob only on the deny side. |
| C-005 | C | Role tiers avoid asserting an unverified gateway-to-family mapping and survive a change of judge model; A's family names need a host table. |
| C-006 | A | Two seeded stages with narrow-only prefixes and sha256-bound grants are minimal; C's glob bindings are forgeable by naming a script (C's own risk). |
| C-007 | C | Five per-class modes, strictest layer wins, rollback by one edit; A has three event classes, B one global switch. |
| C-008 | A | Blocking an unpinned launch is deterministic; B's effective-default lookup rests on settings order and hook-env equality, both UNVERIFIED, so it can allow on wrong data. |
| C-009 | C | Changed from A: A's own text lists closed-world as unsound and REQ-11 tests only a comment; C's single-assignment resolver (REQ-10/11) is the sound minimum. |
| C-010 | A | Same 256 KB depth-1 shell scan as C plus a named .py file; script_max_kb is policy-tunable down toward B's 64 KB. |
| C-011 | B | B follows the documented order including CLAUDE_CODE_SUBAGENT_MODEL; A's row 6 skips it and REQ-17 allows when the session model is unknown. |
| C-012 | B | B re-records the model on a /model prompt and locks on unreadable policy; A checks ^/model only. UserPromptSubmit firing is UNVERIFIED for all. |
| C-013 | A | Pure-bash prefilter fails closed for launch-shaped input in any session; guard-style governed-only fail-closed (guard.sh:147-163, verified) leaves ordinary incident sessions open. |
| C-014 | A | Widest tamper class (Edit, Write, NotebookEdit, settings, disableAllHooks, installer); B's audit and C's grant files are useful add-ons. |
| C-015 | C | Per-class enforce order, a 100-script-event gate and no-reinstall rollback; A and B flip coarser and name no owner or exit evidence. |
| C-016 | A | Logs every decision with policy_sha8, event id and ms, so false-positive rate and latency come from the log; B logs denials only. |
| C-017 | A | Event id ties a block to its log row; message shape is otherwise equal across variants. Low impact; merge B's do-not-edit line. |
| C-018 | C | One file per grant gives atomic create and revoke with reason and sha scope; A's append log has no revoke and a 200-line tail. |
| C-019 | C | Typed yes from /dev/tty is stricter than a bare TTY test; B's CLAUDECODE reasoning is refuted (process.py:178-180 pops it, verified). |
| C-020 | B | Three-option single-item tier question with "cannot tell" is simplest; A's option (c) needs multi-hop reasoning; C asks what code already knows. |
| C-021 | A | Only A's gate joins need (50 code misses Jev can see) with quality (precision 0.95, 1% false blocks); B lacks quality, C lacks need. |
| C-022 | A | Observed modelUsage is ground truth independent of the rule; merge B's frozen labels and second reader. Transcript shape UNVERIFIED in all. |
| C-023 | B | Split registration by cost: Edit\|Write at 1 s as freshness-pre-edit (hooks.json:86-91, verified) beats A's single 5 s matcher; add NotebookEdit. |
| C-024 | B | Changed from A: B's line 279 equals A's allow-set bound and adds candidates plus a replay corpus; A's only extra is a null log field. |
| C-025 | NONE | All three leave the native floor unbuilt or deferred; v1 needs a seeded deniedModels snippet derived from the policy, with a REQ. |
| C-026 | A | States all sessions with an observe seed, matching the incident (ordinary sessions); B implicit; C's governed-only fail-closed misses ordinary sessions. |
| X-001 | B | Missing policy blocks model-bearing events, so deletion is not a bypass; A and C allow it. Narrow B's block to calls that name a model. |
| X-002 | A | Prefilter plus REQ-23 fails closed for launch-shaped input without jq; C copies the fail-open precedent (orca hook lines 65-72, verified); B is silent. |
| X-003 | C | Only C has a root-owned layer a same-user model cannot edit; untested and absent here, so it needs a REQ. All project paths are gitignored. |
| X-004 | A | Flat second pass blocks bash -c, eval, ssh, xargs, heredoc-to-shell that the orca hook lists as ceilings (lines 40-44, verified); false-block rate UNVERIFIED. |
| X-005 | A | Block oversize like B, with a policy-tunable 256 KB cap; C allows an unscanned script (scan_skipped), a hole padding can exploit. |
| X-006 | A | Seed name model-policy.json.example follows the <dest>.example pattern (install_hooks.py:104-105, verified); SC_MODEL_STAGE is specific; B's seed name breaks the pattern. |
| X-007 | A | Matcher lists Edit, Write, NotebookEdit so the tamper rule can fire; C's omits all three; B omits NotebookEdit. |
| X-008 | A | Two-hour default with 24 h cap limits rubber-stamped grants; B's 24 h default and 168 h cap are too long for rare blind-scoring runs. |
| X-009 | B | Re-record on /model keeps inherit checks valid; UserPromptSubmit firing is UNVERIFIED, so say so, and do not block a person's own choice. |
| X-010 | B | No Jev code in v1 (REQ-35); A's line 159 lets jev_then_log allow on failure, C ships a shadow path; none has a measured need. |
| X-011 | A | Self-timeout converted to exit 2 for launch events is safe whichever way the platform behaves; A's B9 citation is unsupported and must be marked UNVERIFIED. |
| X-012 | C | Changed from B: C's REQ-34 is an automated timing test on the non-matching path every Bash call pays; B's corpus p95 mixes paths. |
| X-013 | A | Narrow-only prefix rule (MP-STAGE-WIDEN) is structural; C relies on declared_by flags and spoofable globs; B is silent yet tells launchers to prefix. |
| X-014 | A | B's reading is wrong: process.py:178-180 pops CLAUDECODE (verified), so the TTY check must carry the override guard. |
| A-001 | QUALIFY | Name checks are necessary, not sufficient: modelOverrides and gateway remaps (named by no variant) need a stated ceiling and an observed-model check. |
| A-002 | REJECT | False as worded: eval children get a per-eval HOME (claude_process.py:238-241, isolation.py:665-668, verified); only the parent-side launcher check covers the launch. |
| A-003 | QUALIFY | Observe-first is acceptable only with a named owner, exit evidence, and day-one enforcement of literal Opus launches and Agent model parameters. |
| A-004 | QUALIFY | Holds only if grants bind to a script sha256 and grant frequency is counted; the "rare" assumption itself is UNVERIFIED. |

