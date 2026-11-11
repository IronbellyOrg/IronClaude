# Adjudication of findings X1-X29

Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited as `spec:N`). Inventories are cited by path. Source files under `src/`, `~/.claude` and the evidence files named in the README are not present in this sandbox, so any claim that depends on them is UNVERIFIED.

Test applied to each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is confirmed only if that sentence holds with no further assumption.

Result: 1 confirmed (X22), 1 unsure (X3), 27 rejected.

## Findings

### X1: rejected

No build results from the sentence at spec:39; `inventory/orca-capabilities.md:158` supports it. The test sentence cannot be written.

### X2: rejected

SA-3 (spec:148) is a permission bound ('only ... or'); 'the new output flag' is the `--output` that section 3.2 rows and P1 (spec:159) add. WC-4 (spec:62) mandates the contract only in unattended mode. An implementer may or may not write it on a standalone `--output` run; neither is shown wrong by any stated text.

### X3: unsure

Half true. spec:86 (index-repo: brief 'none', fix is only 'State the output location') conflicts with WC-11's 'Default output paths carry a timestamp or the slug' (spec:69), and unlike cleanup-audit (spec:85) no one-per-worktree rule is stated. But spec:87 makes the init-lite brief pass `--output <file>`, so that half of the claim is wrong, and an actual clobber needs the extra assumption that a coordinator dispatches two index-repo workers into one worktree.

### X4: rejected

Column header at spec:97; SA-1 at spec:146; AC-3.2 at spec:205. Not unclear.

### X5: rejected

spec:70. Nothing in any phase implements follow-up handling; it is Orca's own worker contract (`inventory/orca-capabilities.md:66-67` cited).

### X6: rejected

spec:52, spec:191. Holds only with an assumption the spec text does not make.

### X7: rejected

spec:104 cites `sk/sc-cli-eval-protocol/SKILL.md:128-153`; `inventory/commands-a.md:44` says the confirmation of 'the exact invocation and safety flags' is at S:135-146. The skill file is not in the sandbox (UNVERIFIED), so 'never named anywhere the implementer can read' cannot be established without assumption.

### X8: rejected

spec:88 (brief: 'no `--remediate`'; fix: 'Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule'), spec:122, spec:151.

### X9: rejected

spec:202. The pagination limit itself is not checkable in the sandbox (UNVERIFIED) and the failure needs a PR at or over the page size.

### X10: rejected

spec:160 ('P2 only turns it off'), spec:100 (`--post-pr` named), spec:121 ('refused unless authorized'), spec:225 ('Phases 0-3 can proceed on the recommendations'), spec:113-114 (D4/D3). The implementer builds a refusal, which is not wrong.

### X11: rejected

spec:105; `inventory/commands-a.md:68`. Non-goal 8 (spec:220) scopes out defects that do not stop worker use.

### X12: rejected

spec:158, spec:154, spec:194 ('a failure here reopens section 1'). The wording 'before anything is built on it' is loose, but no wrong artifact follows unless the smoke runs fail.

### X13: rejected

spec:68 vs spec:210, but spec:114 says 'confirm each single iteration ... stays under 4 minutes (WC-10)' for the one command AC-4.3 covers. Wording mismatch is real; a failing build needs an assumed 240-300 s call.

### X14: rejected

spec:114 (Phase P4), spec:162, spec:210.

### X15: rejected

spec:181 vs `inventory/orca-capabilities.md:129` ('An absent field means it never looked'). The observation is accurate for step 2 alone; the claimed consequence (a stalled worker passes) is contradicted by spec:182 and spec:184.

### X16: rejected

spec:228, spec:62, spec:159. Whether troubleshoot has `--output` today is UNVERIFIED here.

### X17: rejected

spec:180-182. WC-6 retry and WC-10 for cli-eval really have no check (spec:104, spec:199-203), but the implementer still builds what the rows say.

### X18: rejected

spec:76, spec:114, spec:139, spec:240.

### X19: rejected

spec:172, spec:147, spec:51 ('It names no Orca command'). The claim itself says 'may'.

### X20: rejected

`inventory/orca-capabilities.md:155`; spec:24; spec:45. No build depends on it.

### X21: rejected

spec:149, spec:176. Needs the assumption that a flag must be added by rewriting an existing line.

### X22: confirmed

An implementer who follows the stated text as written builds P1 with the commands in the P1 row (spec:159) and a load edit limited to its usage line (spec:112: Report 'none', 'P1 (usage line only)'), and that is wrong because AC-1.1 (spec:195) then fails: its test demands a `## Unattended mode` section naming `return-contract.yaml` in every section 3.1-3.2 command, including load, implement (spec:109, P4, waits for D2), post-release (spec:113, P4) and pr-submit (spec:114, P4; spec:240 'no pr-submit changes'). spec:154 forbids later phases until the earlier checks pass. No assumption is needed; the texts conflict directly.

### X23: rejected

spec:39, spec:215.

### X24: rejected

spec:73, spec:65, spec:43, spec:194, spec:272.

### X25: rejected

spec:59, spec:180.

### X26: rejected

spec:279. No AC covers the mirror, which is a coverage gap only.

### X27: rejected

spec:44, `inventory/orca-capabilities.md:47,52`, spec:180.

### X28: rejected

spec:122; `inventory/commands-a.md:14`; `inventory/commands-b.md:210,314`.

### X29: rejected

spec:51.

## Verdicts

```adj-v1
{"x": "X1", "verdict": "rejected", "reason": "Citation-strength remark only: CAPS:158 does say per-unit Task/Dispatch records require Orca workers started by the coordinator, and nothing is built from this sentence."}
{"x": "X2", "verdict": "rejected", "reason": "SA-3 only limits when the contract may be written and the output flags are the ones P1 adds per section 3 rows; either reading of a standalone --output run passes AC-1.3, so no wrong build follows."}
{"x": "X3", "verdict": "unsure", "reason": "index-repo does keep a fixed PROJECT_INDEX.md with no brief flag against WC-11's wording, but the claim is false for init-lite (its row requires --output <file>) and harm needs two indexers dispatched into one worktree."}
{"x": "X4", "verdict": "rejected", "reason": "The roadmap text sits in the column headed 'Unattended-mode gate resolution (WC-2)', so it applies only under --unattended, and AC-3.2 tests it with that flag."}
{"x": "X5", "verdict": "rejected", "reason": "WC-12 is a worker-session duty taken from the Orca preamble and states that commands need no change, so missing follow-up handling makes no implementer build anything wrong."}
{"x": "X6", "verdict": "rejected", "reason": "The failure needs the added assumption of a partial or older install; as written the contract is registered in KNOWN_CORE_FILES and installs with the commands (AC-0.1)."}
{"x": "X7", "verdict": "rejected", "reason": "The row cites the skill lines that define the invocation and safety-flag confirmation (SKILL.md:128-146), so the implementer reads the flags there rather than guessing; that they are missing there is UNVERIFIED in this sandbox."}
{"x": "X8", "verdict": "rejected", "reason": "It is stated, not unstated: the reflect row says that under --unattended --remediate follows the headless auto-accept rule, the brief must pass no --remediate, and local remediation is not a WC-9 outward action."}
{"x": "X9", "verdict": "rejected", "reason": "The one-page count misleads only if the test PR already has 30 or more reviews or comments, which is an added assumption about the scratch PR."}
{"x": "X10", "verdict": "rejected", "reason": "P2 as written only turns outward defaults off under --unattended (which needs no flag name), --post-pr is named, and section 9 says Phases 0-3 proceed on the D4 recommendation; missing flag names for P4 commands wait on D3/D4."}
{"x": "X11", "verdict": "rejected", "reason": "The row deliberately resolves the hardcoded path by a coordinator rule (dispatch only inside an IronClaude checkout), so the stated text yields a working restriction, not a wrong build."}
{"x": "X12", "verdict": "rejected", "reason": "P0 makes no command edits and the phase gate stops P1 until AC-0.4 passes; leftover contract and guide text is a problem only on the assumption that the smoke runs fail."}
{"x": "X13", "verdict": "rejected", "reason": "The pr-submit row itself sets the under-4-minute bound that AC-4.3 checks, so following the stated row passes; the 4-to-5-minute gap in WC-10's general wording bites only if such a call exists."}
{"x": "X14", "verdict": "rejected", "reason": "pr-submit is a P4 command and AC-4.3 is the check that measures the wait from the transcript, so a P2 check is not owed."}
{"x": "X15", "verdict": "rejected", "reason": "Step 2 does pass vacuously on an absent field, but a stalled worker still fails step 3 (no worker_done) and step 5 (transcript), so it cannot pass the 7.2 check as written."}
{"x": "X16", "verdict": "rejected", "reason": "The command line is an illustration inside open decision D1, and WC-4 plus P1 give every command an output directory flag; nothing is built from the example."}
{"x": "X17", "verdict": "rejected", "reason": "A missing acceptance check is a coverage gap, not a wrong build, and the claim overstates it: 7.2 step 1 checks readiness (WC-1) and step 3 exercises check."}
{"x": "X18", "verdict": "rejected", "reason": "pr-submit is counted under 'needs a change', which is true under either D3 answer, and section 4 states the D3 condition explicitly; the 10/27/6 split does not move."}
{"x": "X19", "verdict": "rejected", "reason": "The grep matches only literal orca command lines; SA-2 and section 2.1 keep such lines out of these files, and the contract and guide section can be written (as the spec itself does) without one, so a failure needs the assumption that the author writes them."}
{"x": "X20", "verdict": "rejected", "reason": "CAPS:155 states in its own heading sentence that subagents are not Orca workers and the depth limit does not count them; only the broader 'Orca never limits them' is UNVERIFIED, which section 1.4 says."}
{"x": "X21", "verdict": "rejected", "reason": "AC-C5 fails only if the implementer chooses to edit an existing Usage line; SA-4 asks for additive edits (new section, new flags), which can be met by added lines alone."}
{"x": "X22", "verdict": "confirmed", "reason": "AC-1.1 requires every command in sections 3.1-3.2 to have an Unattended mode section naming return-contract.yaml, yet load's row says no report and 'P1 (usage line only)', and implement, post-release and pr-submit are changed only in P4 (pr-submit not at all under recommended D3 (a)), so P1 as scoped cannot pass its own check and later phases may not start."}
{"x": "X23", "verdict": "rejected", "reason": "The troubleshoot-then-adversarial sequence is an example of coordinator planning in section 1.3; the spec builds no join step (non-goal 3)."}
{"x": "X24", "verdict": "rejected", "reason": "The brief carries the exact command line and the worker runs it directly; the spec admits the direct route is unproven and tests it first in AC-0.4, so no wrong build follows from the text."}
{"x": "X25", "verdict": "rejected", "reason": "WC-1 is deliberately a launch-setup duty with no command change, and 7.2 step 1 checks readiness (exit 0 and state: ready)."}
{"x": "X26", "verdict": "rejected", "reason": "The spec lists the plugins mirror as UNVERIFIED item 8 and orders each phase plan to resolve it before editing, so the stated text does not lead to an unsynced mirror."}
{"x": "X27", "verdict": "rejected", "reason": "A first-action question blocking readiness is speculation beyond the cited evidence; 7.2 step 1 tests readiness on every live run and unattended mode asks no question."}
{"x": "X28", "verdict": "rejected", "reason": "An evidence-strength remark: the tasklist row needs no build for nesting, and the failure requires the assumption that subagent-to-agent spawning does not work, which INV-B only marks UNVERIFIED."}
{"x": "X29", "verdict": "rejected", "reason": "An edge case that needs the assumption of a quoted argument containing the flag text; ordinary flag parsing is implied by 'passes --unattended'."}
```
