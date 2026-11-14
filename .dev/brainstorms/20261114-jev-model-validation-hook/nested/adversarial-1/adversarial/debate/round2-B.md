# Round 2 debate: Variant B advocate (sonnet:analyzer), rebuttal

Evidence tags: VERIFIED = I read the line or text myself in this session (product files under the repository root, or the variant, enrichment and diff files). UNVERIFIED = not checked by me. "variant-2 line N" means `variant-2-original.md`. I did not touch `.dev/eval-workspaces/`. Round 2 changes 12 of my round 1 rows: S-006, C-004, C-008, C-009, C-010, C-017, C-018, C-021, C-023, X-005, A-002, A-003. Each says in Basis what evidence moved it. One round 1 row I kept against the majority: C-001.

## Rebuttal: Variant B (sonnet:analyzer)

### Response to criticisms

Critics: A = round1-A and round2-A; C = round1-C. Merged where two critics made the same point.

1. **A and C: B reads `process.py:171` as proof that child `claude` carries `CLAUDECODE` (X-014, C-019).** Concede the citation. I read `process.py:171-172` (docstring "Remove CLAUDECODE ... to prevent nested-session detection") and `:179` (`env.pop("CLAUDECODE", None)`). B's variant-2 line 137 has it backwards for launcher-started children. Nuance, not a defence: the step 1 note says the variable is `1` in this Bash tool (observed once, UNVERIFIED by me), so the refusal still has some use against a model typing the CLI in a Bash call, but a child started by a launcher has it removed, so the TTY test must carry the guard. X-014 stays A.
2. **A and C: the seed name `model-policy.example.json` breaks the seed pattern (X-006).** Concede. `install_hooks.py:104-105` reads `("auggie-projects.txt.example", "auggie-projects.txt")`. B's variant-2 line 238 uses the wrong shape.
3. **A and C: no rule for a host without `jq` or `awk`, and no self-timeout (X-002, X-011, C-013).** Concede. Enrichment line 22 (VERIFIED) says a non-zero exit other than 2 proceeds and "a hook that must fail closed has to convert its own errors to exit 2". B's section 6 (variant-2 line 185) only promises to "stay well under" the timeout and has no trap, so a crash inside the script (exit 1) fails open on exactly the events B calls fail-closed. B also cannot tell which events are model-bearing without `jq`. A's prefilter plus `timeout 4` conversion is the only answer. X-002, X-011 and C-013 stay A.
4. **A and C: MP-03 blocks every expansion, so a pinned `MODEL=claude-sonnet-5-5` then `--model "$MODEL"` is blocked (C-009).** Concede in part and move to C. I read C's REQ-10 (`$` in the flag value is dynamic and denied) and REQ-11 (single in-file literal assignment resolves and is allowed) at variant-3 lines 249-250. That is a small, tested allow inside a deny default. My round 1 claim that C "resolves cases it cannot prove" (`M=${M:-...}` with `M` set in the environment) is not supported by C's text: REQ-11 pins only a literal assignment and how the regex treats a `${...}` assignment value is UNVERIFIED either way. A has since conceded that its closed-world rule is unsound (round2-A item 2). B keeps the safest default but gives the owner no way to keep a legitimate pinned launch except inlining the literal.
5. **A and C: B's matcher omits NotebookEdit, so MP-06 cannot fire for it (X-007, C-014).** Concede (variant-2 lines 247-250 list `Edit|Write` only). One-token fix; the existing wide matcher at `hooks.json:116` already lists NotebookEdit (VERIFIED).
6. **A and C: a missing or malformed policy blocks every Agent, Task, Workflow and Monitor call (X-001).** Concede the width. Variant-2 lines 70 and 72 block them without asking whether a model is named, and B's own risk 7 (line 292) admits the outage. Narrow it to calls that name a model, keep the block. X-001 stays B because A and C let deleting the file switch enforcement off.
7. **A and C: override window 24 h default and 168 h maximum (X-008).** Concede. A (2 h and 24 h) is the safer shape.
8. **A and C: the hash-chained journal is written by the same OS user, so it is detection only (C-014, C-018).** Concede. B says "detection, not blocking" (variant-2 line 145), but also has no revoke command, which C's one-file grants have. C-018 moves to C.
9. **A: B's labels are circular (C-022).** Concede. Variant-2 line 109 labels by "the decision the rule requires", and line 105 admits the transcript model key is UNVERIFIED. A's observed `modelUsage` is independent of the rule.
10. **A and C: B's Jev gate has no precision bar and counts misses in a class Jev cannot see (C-021).** Concede. Variant-2 line 89 calls class (b) "a ceiling, not a judgment problem", and line 92 triggers Jev on class (b) misses. Those two lines contradict each other. C-021 moves to A.
11. **C: B logs denials only but its exit criterion counts live events (C-016).** Concede. Variant-2 line 132 writes denials only; line 271 counts "200 model-bearing live events".
12. **A: B's Agent-without-model case is unspecified when no session record exists (C-011).** Partly concede: variant-2 REQ-11 ends the order at the SessionStart record and says nothing for an absent record, and `SessionStart.model` is optional. Still B over A: A's REQ-17 allows on an unknown session model (A conceded), and B re-records on any `/model` prompt.
13. **A: B's single global mode and its two-week window give the longest exposure (C-007, C-015).** Concede (variant-2 lines 271-274). S-005, C-007 and C-015 stay C.
14. **A (round 2): B's corpus p95 mixes script scans with the common path (X-012).** I voted C in round 1 and keep C. Variant-2 REQ-31 measures "the fixture corpus", which is launch-heavy, while line 177 itself says the common path exits early at 10 to 30 ms.
15. **C: two parity contracts to maintain (REQ-30 plus the copied tokenizer parity, B risk 4).** Concede as a cost. It is the price of one checked-and-emitted value (C-002) and a repo test that forces new launchers through the helper (C-003).
16. **A and C: B's trailer is a chat-style status table (S-006).** Concede after re-reading variant-2 lines 295-303: the table carries no requirement and A also states what was not checked (section 10). S-006 moves to A.
17. **A and C: B has no `modelOverrides` line in its "Cannot see" rows (A-001).** Concede. Rows 14 to 16 (variant-2 lines 28-30) name `/model`, mods and harness settings, not `modelOverrides`; the diff analysis found 0 matches in all three proposals. This weakens B's "states plainly what it cannot see" claim.
18. **A (round 2): B's row 4 covers launchers through an in-process helper, so `uv run python x.py` is still a ceiling (C-010).** Concede; I had argued "Python launches are covered in-process", which is true only for the five package builders (variant-2 line 18) and not for an arbitrary script. C-010 moves to A.

### Updated assessment of Variant A

A is the strongest of the three on fail-closed behaviour and has conceded most of what B and C raised.

- Confirmed strengths: the pure-bash prefilter is the only answer to a missing `jq` that does not brick ordinary Bash; I read `launch-level-guard.sh:153-155` (an ungoverned session exits 0 on any internal failure) and `require-orca-worktree-agent.sh:65-72` (fail open without `jq` or `awk`), so copying either precedent leaves the incident path open. A's flat second pass can only add blocks and closes the nested-launch ceilings that the Orca hook lists (lines 39-45, VERIFIED). A's oversize rule covers both scripts and commands, with a tunable cap (variant-1 lines 79, 241, 297, VERIFIED).
- Confirmed weaknesses: L0 and L3 have no REQ and no file (A conceded twice). The dormant Jev path ends with "allow-and-log for `jev_then_log`" when Jev is unreachable (variant-1 line 159, VERIFIED), so line 156's "can never turn a code block into an allow" holds only against a loosened default. The closed-world rule is unsound by A's own line 141. The glob tiers admit later versions on the allow side. The single 5 s matcher puts every Edit and Write through the full script (hooks.json:86-91 shows the existing precedent at 1 s, VERIFIED). The 200-line override tail can drop a valid grant (a false block).
- Net: A wins the failure-path points; B still beats it on launcher closure (C-002, C-003), Agent resolution (C-011), missing-policy (X-001) and Jev scope (X-010).

### Updated assessment of Variant C

C is the best-operated design and the weakest on fail-closed coverage.

- Stronger than I scored: REQ-10 and REQ-11 are a small, tested resolver inside a deny default (variant-3 lines 249-250, VERIFIED). Per-class modes with rollback by one edit, one-file grants, `id_prefix_match: false` with a stated reason, and a timing test on the non-matching path are real advantages.
- Confirmed weaknesses: REQ-25 says that with `jq` missing the hook exits 0 (variant-3 line 264, VERIFIED), copying the fail-open precedent; REQ-09 allows an unscanned script over 256 KB (line 248, VERIFIED), which a model can trigger by padding; the tamper rule needs Edit, Write and NotebookEdit but the matcher lists only Bash, Agent, Task, Skill and Monitor (diff X-007; the real registrable set is visible at hooks.json:116, VERIFIED). The `claude-mention` rule (line 197) treats any `claude` word with no resolvable flag as dynamic, so over-blocking of `claude --version` is likely (UNVERIFIED, no REQ tests it).
- Net: C wins the operations points (C-005, C-007, C-015, C-018, C-019, S-005, X-003, X-012) and the narrow C-009 resolver; it loses the fail-open points.

### New evidence

| # | Claim | Source | Tag |
|---|---|---|---|
| 1 | `ClaudeProcess.build_command` adds `--model` only `if self.model:`; `build_env` pops `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`. B's reading of `:171` is the reverse. A separate check can drift from the argv, which is B's `build_flag` argument | `src/superclaude/cli/pipeline/process.py:163-164, 171-172, 178-180` | VERIFIED |
| 2 | Seeds are named `<dest>.example`; B's seed name breaks the pattern | `src/superclaude/cli/install_hooks.py:104-106` | VERIFIED |
| 3 | A governed session fails closed; an ordinary session exits 0 on any internal failure ("never blocked by a failure") | `src/superclaude/hooks/scripts/launch-level-guard.sh:142-163` | VERIFIED |
| 4 | The Orca hook fails open without `jq` or `awk`, and lists `bash -c`, `eval`, `ssh`, `xargs`, `find -exec` and heredoc-to-shell as ceilings | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:39-45, 65-72` | VERIFIED |
| 5 | The eval adapter merges `HomeIsolation.env` last ("Isolation always wins"), and constructs `ClaudeProcess(model=self._model)`, so the argv-site check sits in the parent while the child gets a scratch HOME | `src/superclaude/cli/eval/claude_process.py:238-241, 252-255, 284-289` | VERIFIED |
| 6 | That an eval child therefore loads no operator `~/.claude` hooks follows from the HOME override; I did not read the isolation code for hook seeding | inference from item 5 | UNVERIFIED (inference) |
| 7 | Existing registrations: `Edit\|Write` at 1 s (`freshness-pre-edit.sh`); wide matcher including NotebookEdit, Monitor, Workflow at 5 s (`launch-level-guard.sh`) | `src/superclaude/hooks/hooks.json:86-91, 115-123` | VERIFIED |
| 8 | Reflect defaults to Opus: `_DEFAULT_MODEL = "opus"` and `model = os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL`. Day-one observe logs flag it in any variant | `src/superclaude/cli/reflect/commands.py:37, 365` | VERIFIED |
| 9 | Enrichment B9: non-zero exit other than 2 is non-blocking; a fail-closed hook "has to convert its own errors to exit 2". It says nothing about a timeout, so A's and C's timeout claims and B's "stay well under" are all unsupported | `enrichment/codebase-context.md:22` | VERIFIED |
| 10 | A line 159: Jev unreachable gives "allow-and-log" under `jev_then_log`; A line 156 claims Jev can never turn a block into an allow; A REQ-13 blocks oversize scripts and commands; `script_max_kb` is a policy field | `variant-1-original.md:79, 156, 159, 241, 297` | VERIFIED (document text) |
| 11 | C REQ-09 allows an oversize script with `scan_skipped`; REQ-10 and REQ-11 define the dynamic and single-assignment rules; REQ-25 exits 0 without `jq` | `variant-3-original.md:248-250, 264` | VERIFIED (document text) |
| 12 | B contradicts itself on Jev: class (b) is "a ceiling, not a judgment problem" (line 89) yet it is the trigger in the measured-need rule (line 92). B's missing-policy table blocks Agent, Task, Workflow and Monitor without asking whether a model is named (lines 70, 72) | `variant-2-original.md:70, 72, 89, 92` | VERIFIED (document text) |
| 13 | `launch-implement-2.sh:8,28` pinned-variable pattern; B's 503-transcript and 470-match counts; whether `UserPromptSubmit` fires for `/model`; hook env equals session env; false-block rate of A's flat pass and C's `claude-mention`; every latency number; `/etc/superclaude` as a usable managed layer | not checkable read-only or off limits | UNVERIFIED |

### Shared-assumption responses

- **A-001: QUALIFY.** A name check is the most a hook sees, so v1 must say plainly that it checks the requested name and not the served model, and list `modelOverrides` (enrichment B6) and settings `env` redirects as cannot-see rows, which none of the three proposals does.
- **A-002: REJECT.** As worded it is false for eval children, because `HomeIsolation.env` always wins over the caller's env (`claude_process.py:238-241`, VERIFIED); the parent-side launch check covers the launch and the child's inner tool calls are a stated ceiling. I moved from QUALIFY because my own round 1 text already said the assumption is false.
- **A-003: QUALIFY.** Observe-first is acceptable only with a named owner, a date, exit evidence beyond counts, and day-one enforcement of the zero-ambiguity cases (literal `--model`, Agent `model` parameter); B's own plan (variant-2 lines 271-274) has the same open window, so rejecting it outright would condemn B.
- **A-004: QUALIFY.** It holds for blind scoring itself, but the incident launchers start Opus children from default-stage orchestrators, so the stage must come from the launcher or a human-owned binding, and grant frequency must be logged because the "rare" premise is UNVERIFIED.

### Per-point positions

| Point | Winner | Basis (max 25 words) |
|---|---|---|
| S-001 | A | Headline layer table states the property and each layer's blind spot first; B opens with three points and no property sentence. |
| S-002 | B | Rows 14-16 say "Cannot see" and attach an owner decision (variant-2 lines 28-32); A rows 10-11 hedge between "blocks or records" and "not rejected". |
| S-003 | B | Fixed five-method verification vocabulary (variant-2 line 189) makes each REQ auditable; A mixes wording, C is nearly all unit tests. |
| S-004 | B | Residue split into blocked, ceiling and not-a-selection classes with a numeric need rule; A and C ship dormant or shadow Jev code. |
| S-005 | C | Per-class order, 100-script-event gate and one-edit rollback; B's single flip after 200 events is the longest exposure. |
| S-006 | A | Changed from B: re-read variant-2 lines 295-303; the status table carries no requirement and A also states what was not checked in section 10. |
| C-001 | B | Three points each with REQs; A's L0 and L3 have no REQ or file (A conceded). Floor unbuilt in both; B omits modelOverrides. |
| C-002 | B | build_flag emits the checked value; I verified process.py:163-164 adds --model only when set, so a separate check can drift from the argv. |
| C-003 | B | REQ-29 fails on a raw "--model" outside the helper; B also names reflect/commands.py:365 (verified `_DEFAULT_MODEL = "opus"`). A and C have no such test. |
| C-004 | C | Changed from B: B states no prefix rule (variant-2 line 60); C's exact-id rule cites docs B7. Otherwise equal, so rationale breaks the tie. |
| C-005 | C | Role tiers avoid asserting an unverified gateway-to-family mapping and mirror the owner's "judge" rule; concession kept. |
| C-006 | A | Two seeded stages with narrow-only prefixes are minimal; B's extra stages are speculative and C's glob bindings are forgeable by naming a script. |
| C-007 | C | Five per-class modes, strictest layer wins, rollback by one edit; B's single global mode is the longest exposure. |
| C-008 | A | Changed from B: variant-2 line 16 admits ANTHROPIC_MODEL versus settings order and hook-env equality are UNVERIFIED, so resolve-then-check can wrongly allow. |
| C-009 | C | Changed from B: variant-3 REQ-10/11 (lines 249-250) pin literal single assignment and deny the rest; A conceded closed-world unsound; my `${M:-}` fear unsupported. |
| C-010 | A | Changed from B: variant-2 row 4 covers only five package launchers in-process; `uv run python x.py` stays a ceiling, which A scans. |
| C-011 | B | Follows the documented order including CLAUDE_CODE_SUBAGENT_MODEL and re-records on /model; A allows an unknown session model (A conceded). |
| C-012 | B | Blocks forbidden /sc: command frontmatter, re-records on /model, locks the session on unreadable policy; UserPromptSubmit firing UNVERIFIED for all three. |
| C-013 | A | Pure-bash prefilter fails closed for launch-shaped input in any session; guard.sh:153-155 exits 0 for ordinary sessions (verified); B has no trap. |
| C-014 | A | Widest tamper class; B's MP-06 omits NotebookEdit, covers redirects by named path only, and its journal is forgeable by the same user. |
| C-015 | C | Per-class enforce order, 100-event gate for scripts, no-reinstall rollback; B flips every class at once. |
| C-016 | A | Logs every decision with policy_sha8 and ms; B logs denials only (variant-2 line 132) yet its exit criterion counts live events (line 271). |
| C-017 | A | Changed from B: B's message and log line (variant-2 lines 117-132) carry no event id tying a block to its log row; A's does. |
| C-018 | C | Changed from B: B's CLI (variant-2 lines 136-145) has no revoke and its hash chain is same-user forgeable; C's one-file grants revoke by delete. |
| C-019 | C | Typed yes from /dev/tty is stricter than a TTY test; process.py:178-180 pops CLAUDECODE (verified), refuting B's citation. |
| C-020 | B | Three-option tier question with a "cannot tell" option; A's option (c) needs multi-hop reasoning; C asks what code already knows. |
| C-021 | A | Changed from C: variant-3 line 137 tests Jev quality only, and B's line 89 vs 92 contradicts itself; A alone pairs code misses with precision. |
| C-022 | A | Observed modelUsage as ground truth tests "used"; B's labels are circular and its transcript model key is unverified (variant-2 line 105). |
| C-023 | B | Changed from A: hooks.json:86-91 shows Edit and Write already run at 1 s; B's split registration matches, A sends every Edit through 5 s. |
| C-024 | B | Router output is a request checked against the same allow list (variant-2 line 279); C reserves updatedInput, nearer to rewriting. |
| C-025 | NONE | Nobody builds or tests the native floor; C says generated yet defers it. Ship a coarse deniedModels snippet with a REQ, or drop it. |
| C-026 | A | States all sessions with an observe seed, matching the ordinary-session incident; B implicit, C hybrid. |
| X-001 | B | Missing policy blocks model-bearing events so deletion is not a bypass (REQ-19); narrow to calls naming a model. A and C allow. |
| X-002 | A | Pure-bash prefilter plus REQ-23 fails closed without jq; C exits 0 (REQ-25; require-orca:65-72 verified); B is silent. |
| X-003 | C | Only root-owned layer a same-user model cannot edit; absent here and untested, and project paths are gitignored in all three. |
| X-004 | A | Flat second pass blocks nested launches the Orca hook lists as ceilings (lines 39-45, verified); false-block rate UNVERIFIED; B scans one level. |
| X-005 | A | Changed from B: A blocks scripts over a tunable script_max_kb and commands over 64 KB (REQ-13); B's REQ-07 covers scripts only; C allows. |
| X-006 | A | Seed name follows the <dest>.example pattern (install_hooks.py:104-105, verified); B's seed name breaks it. |
| X-007 | A | Matcher lists Edit, Write, NotebookEdit so tamper can fire; B omits NotebookEdit; C omits all three yet needs them. |
| X-008 | A | Two-hour default and 24 h cap limit rubber-stamped grants; B's 24 h default and 168 h maximum are too long. |
| X-009 | B | Works either way: blocks if UserPromptSubmit fires, says "cannot see reliably" otherwise, and re-records the model; A hedges. |
| X-010 | B | No Jev code or network call in v1 (REQ-35); A line 159 lets jev_then_log allow on failure; C ships a shadow path. |
| X-011 | A | Self-timeout converted to exit 2 is safe either way; enrichment B9 says fail-closed hooks must convert errors; B has no trap (variant-2 line 185). |
| X-012 | C | C's REQ-34 times the non-matching path every Bash call pays; B's REQ-31 corpus is launch-heavy and omits the fast path. |
| X-013 | A | Narrow-only prefix rule is structural; B is silent while telling launchers to prefix; C accepts inline non-human stages. |
| X-014 | A | A and C cite no wrong fact; B's process.py:171 reading is refuted by lines 178-180 (verified), so the TTY test carries the guard. |
| A-001 | QUALIFY | Name check is the v1 limit; modelOverrides and settings env redirects are in no proposal's cannot-see list, so state the ceiling plainly. |
| A-002 | REJECT | Changed from QUALIFY: claude_process.py:238-241 shows isolated HOME always wins (verified), so false as worded; the parent-side check covers the launch only. |
| A-003 | QUALIFY | Changed from REJECT: B's own plan (variant-2 lines 271-274) is observe-first with no date; accept only with owner, exit evidence, day-one literal enforcement. |
| A-004 | QUALIFY | Holds for blind scoring, but incident launchers run from default-stage sessions, so the stage must come from launcher or human binding; frequency unmeasured. |



