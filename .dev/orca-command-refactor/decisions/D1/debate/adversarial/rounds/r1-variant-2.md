# D1 Round 1: advocate for Variant 2 (option b, the command detects it is an Orca worker)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration` (re-read 2026-11-02; it reads bundled content without the Orca runtime, `CAPS:147`); `V1:N`/`V2:N`/`V3:N` = line N of the variant files. Every source cited below was re-read for this round.

## Position summary
I argue the strongest form of option (b): **preamble-only detection**. The environment route is dropped. A command is in unattended mode when its session is a "worker run" as the spec already defines it (a live Orca preamble with Task and Dispatch IDs, `SPEC:53`), with that rule written once in `WORKER-CONTRACT.md`. It removes the one switch a coordinator can forget and leaves a person's own session untouched. I also say plainly where it loses, mainly to Variant 3.

## Steelman
### Variant 1 (option a, `--unattended` flag)
The best case for (a): the trigger is a literal token that anyone can see in the brief and that a static check can grep. A person cannot trip it, because quoted text never counts (`SPEC:55`, AC-2.8 at `SPEC:269`). It names the condition rather than the tool, so any caller with no person present can use it (`SPEC:54`, `SPEC:361`). It fits SA-2 and non-goal 1 without amendment (`SPEC:170`, `SPEC:314`). The whole spec is already written around it (`SPEC:54`), so it costs least to adopt. Phase gating is explicit (`SPEC:187-195`). Its only stated failure, a forgotten flag, is caught by the 7.2 step-3 stall proof (`SPEC:238`).

### Variant 3 (option c, flag plus worker-session guard)
The best case for (c): it keeps everything (a) gets right and also turns (a)'s silent stall into an immediate, named `worker_done --outcome failed`. That is Orca's only guaranteed failure signal ("Never encode failure only in prose", `[G]` lines 88-90, `CAPS:73`). The check sits in the worker session, which already carries the Orca duties (WC-3, WC-5, WC-7, WC-12, `SPEC:67-76`), so commands stay Orca-free. The same guard stops a worker from running the coordinator-only commands (`SPEC:151`). It costs one rule in one file.

## Strengths claimed
1. **It uses Orca's own definition of a worker, which the spec already depends on.** Orca's role table: a prompt with "a live injected preamble with Task and Dispatch IDs" is a "Dispatched worker", and "No live preamble" means an "Ordinary terminal agent" (`[G]` lines 38, 41; `CAPS:148`). The spec takes that rule as its "Worker run" term (`SPEC:53`). Every worker-session duty depends on the model recognizing that preamble: asking (WC-3), `worker_done` (WC-5), the top-level rule (WC-7) and `check` (WC-12) (`SPEC:67-76`). So preamble-only (b) asks the model to make no recognition the contract does not already require.
2. **A person's own session is safe on this route.** A session a person started has no live preamble (`[G]` line 41), so prompts and outward defaults stay as they are (SA-1, `SPEC:169`). A false positive needs a person to paste a live preamble into their own session. That is the same kind of unenforced risk as a person pasting a brief's command line under (a) (A-003).
3. **No coordinator omission causes a silent stall.** Under (b) there is no switch to forget. The brief can still miss other content, such as the report directory, but that fails fast: WC-4 refuses and gives `failed` (`SPEC:68`; AC-1.5 at `SPEC:261`). Under (a), a missing flag leaves the worker parked on a prompt, and Orca reports that as "healthy, not failed" (`CAPS:52`, `CAPS:129`; `SPEC:47`).
4. **Phase gating works with no special case.** The detection text arrives with each command's `## Unattended mode` section in the phase that converts it (`SPEC:182`, `SPEC:187-195`). Flagless P0 smoke runs and `/sc:load` briefs (`SPEC:181`, `SPEC:191`, `SPEC:197`) therefore behave as they do today, so X-005 does not arise.
5. **The repo already infers "no person" without a flag.** `/sc:reflect` treats `claude --print` with no TTY as "the headless signal" (`src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:239-242`), and SA-6 protects that rule (`SPEC:174`). Option (b) applies the same pattern to the signal an Orca worker actually has, because the print signal does not fire for one (`SPEC:391`).
6. **Per-command cost is the same as (a).** The detection rule is written once in `WORKER-CONTRACT.md`, which AC-C1 already excludes (`SPEC:205-211`). Each command's section refers to "unattended mode" as that file defines it, so commands stay free of Orca text. This corrects `V2:25`; see Concessions.

## Weaknesses identified
**Variant 1**
1. **A forgotten flag fails silently and late.** The worker parks on a prompt that Orca reports as healthy (`CAPS:52`, `CAPS:129`). The 7.2 proof needs a 900 s wait plus a transcript read (`SPEC:238`), and V1 admits it catches the problem "only after the fact" (`V1:19`).
2. **"Deterministic" covers the text only, not the run.** The coordinator that writes the flag is a model, and the command's parse is "applied by the model reading the rule, not by code" (`V1:22`). The runtime check AC-2.8 is manual (`SPEC:269`). Remembering a token is the same kind of model-applied step that V1 holds against (b) (X-003).
3. **No caller in scope needs caller-neutrality yet.** The spec says the mode "serves any caller" (`SPEC:54`), but `claude -p` appears only in AC-1.3's file-creation check (`SPEC:259`); A-007 records that no other caller is shown in scope.

**Variant 3**
1. **As written, the guard refuses legitimate briefs (X-005).** P0 smoke runs carry no flag (`SPEC:181`, `SPEC:191`), `/sc:load` never gains it (`SPEC:197`), and the guard is proposed for "P0 or P1" (`V3:23`).
2. **It relies on the same recognition it calls authoritative.** The guard runs only if the worker session recognizes its preamble (`V3:3`, `V3:8`). If that recognition is reliable enough to base a guard on, then `SPEC:330`'s main objection to preamble-only (b) is weaker than V1 and V3 imply (X-001).
3. **One citation range is overstated.** `[G]` line 78 says "The injected preamble is authoritative" about a worker's obligations; the identity rule is at lines 38 and 41, not 78-82 (`V3:8`).

## Concessions
1. **I drop the environment route.** By design, Orca uses `ORCA_TERMINAL_HANDLE` to identify the caller in any "live Orca terminal" (`CAPS:149`, `terminal-identity.js:213-215`), including a coordinator's tab, which is not a dispatched worker. In this subagent the variable was set on 2026-11-02 (`term_feb70160-...`). It is unsafe for SA-1 (`V2:13`).
2. **X-002 holds.** `V2:9` says detection removes "that whole failure class", which overclaims. A missed preamble produces the same stall, with no contract written. The failure moves from the coordinator's memory to the worker's recognition; it does not disappear.
3. **I withdraw the `CAPS:47` claim (OVERSTATED).** That line says only that Claude's task is passed on the command line (`promptInjectionMode: 'argv'`); it says nothing about the preamble.
4. **I correct the AC-C1 claim (WRONG).** The AC-C1 pattern would not match detection text, so it needs no exception. The real conflict is SA-2's sentence ("The only allowed mention of Orca ... as an example of a caller's question channel", `SPEC:170`) and non-goal 1's ban on "Orca-specific branching" (`SPEC:314`). Option (b) needs both amended, even in its strongest form.
5. **Shorter briefs is a small gain (X-006).** Option (b) removes one token; every brief still needs a report directory and the section 3 flags (`SPEC:57`, `SPEC:79`).
6. **Option (b) gives nothing to callers with no preamble,** such as CI or `claude -p` (`V2:18`).
7. **Variant 3 is better overall if X-005 is fixed.** It gets (b)'s main benefit (a forgotten switch fails visibly) without amending SA-2, and it degrades more gently. If the worker session misses its preamble under (c), the flagged command still writes its contract; under (b), the command prompts and stalls with nothing written.

## Shared assumption responses
| ID | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The three preconditions are unverified: `worker-list` paging (`CAPS:127`), remote workers, and the handle format. The conclusion stands on other evidence: Orca resolves the caller of any lifecycle command from `ORCA_TERMINAL_HANDLE` in a live Orca terminal (`CAPS:149`), including a coordinator's, which is not a worker. Variant 2 drops the environment route either way. |
| A-002 | ACCEPT | `CAPS:52` and `CAPS:129` quote `worker-show` line 16 directly. |
| A-003 | QUALIFY | It is a design intent, not a guard (`SPEC:329`). Option (b) has the matching risk: a person pasting a live preamble. Both are unenforced, and the quoted-argument rule covers only the typed-prompt case (`SPEC:55`). |
| A-004 | QUALIFY | All three options rest on a model applying a text rule at runtime (`V1:22`, `V3:17`, `SPEC:53`). Only static text checks are deterministic. The differences are in how each option fails, not whether it can fail. |
| A-005 | ACCEPT | The spec's own plan contradicts it (`SPEC:181`, `SPEC:191`, `SPEC:197`). It is a precondition of Variant 3 only; options (a) and (b) do not depend on it. |
| A-006 | QUALIFY | They are fixed only until the user rules on D1. Option (b) needs SA-2 and non-goal 1 amended (`SPEC:170`, `SPEC:314`), and that cost counts against it. |
| A-007 | QUALIFY | It is stated (`SPEC:54`), but no in-scope caller other than Orca is shown, so it should carry little weight. |
| A-008 | ACCEPT | `check --wait` returns on `worker_done` (`SPEC:238`), whereas a stall proof needs a timed-out wait plus a transcript read. |
| A-009 | QUALIFY | Nothing enforces use of the template (`SPEC:58`, `SPEC:79`). Under (b) and (c), leaving template content out fails fast (WC-4 refusal, or the guard); under (a), leaving out the flag stalls. |

## Per-point positions
| ID | Superior approach | One-line reason |
|---|---|---|
| S-001 | V3 | It meets both alternatives before making its own case. |
| S-002 | V1 | V2 never said which route it recommends; this round fixes that (preamble only). |
| S-003 | V1 | It commits to one mechanism; V2's original offered two and picked neither. |
| S-004 | V3 | It keeps the Orca-aware check in the worker session and the command side Orca-free; V2's strongest form still needs SA-2 amended. |
| S-005 | equal | `[G]` needs only `orca-ide` installed, not running (`CAPS:147`); the other keys need only the repo. |
| S-006 | V3 | Framing itself against both alternatives makes the comparison explicit. |
| S-007 | V1 | It covers both the person and the coordinator concretely. |
| C-001 | V1 and V3 | Preamble-only (b) is safe for people, but it relies on model judgment of context rather than on a visible token. |
| C-002 | V1 and V3 | They state outright that outward defaults stay on for people; (b) is safe here only on the preamble route. |
| C-003 | V1 | The trigger is visible to static checks; the runtime parse is model-applied under every option (X-003). |
| C-004 | V3 | A named failure with no SA-2 change; (b) replaces the forgotten flag with a missed preamble (X-002). |
| C-005 | V1 and V3 | (b) ties commands to Orca and does nothing for callers that have no preamble. |
| C-006 | V2 | One fewer token for the coordinator to remember; a small gain (X-006). |
| C-007 | V1 | The lowest cost; (b) also needs SA-2, non-goal 1, section 2.1 and AC-2.8 rewritten. |
| C-008 | equal | When commands refer to the contract file's definition of "unattended mode", changing the trigger means editing one file under any option. |
| C-009 | equal | All three read it as killing the environment route; I agree (A-001). |
| C-010 | V2 | It brought in Orca's own worker definition (`[G]` lines 38 and 41), which V3 then reuses. |
| C-011 | V3 | Only V3 blocks coordinator-only commands from being run by a worker. |
| C-012 | V2 | Only V2 checked the repo's headless precedent and showed that it misses Orca workers. |
| C-013 | V1 | It is the only one to state phase gating explicitly; (b) can follow it, but V2 did not say so. |
| X-001 | V3 | Both rely on preamble recognition, but a miss under (c) still leaves a flagged command that writes its contract. |
| X-002 | V1 and V3 | I concede that `V2:9` overclaims. |
| X-003 | equal | Every runtime switch is applied by a model; only text checks are deterministic. |
| X-004 | V2 | Adding Orca detection to commands later would break SA-2, so `V1:23`'s "cheap" add-on is not cheap. |
| X-005 | V1 and V2 | Neither refuses flagless P0 or `/sc:load` briefs; V3 must exempt them or ship the guard after P0. |
| X-006 | V1 | I concede: (b) removes one token, and the report directory and section 3 flags remain. |
| X-007 | V3 | The guard makes a forgotten flag fail at once instead of after a 900 s wait. |
| A-001 | equal | Every variant rejects the environment route; Orca's design (`CAPS:149`) supports that whatever the `worker-list` gaps. |
| A-003 | equal | (a) and (b) each depend on a person not pasting worker text: a command line under (a), a preamble under (b). |
| A-005 | V1 and V2 | Only V3 depends on this contradicted precondition. |
| A-009 | V2 and V3 | A template omission fails fast rather than stalling. |
