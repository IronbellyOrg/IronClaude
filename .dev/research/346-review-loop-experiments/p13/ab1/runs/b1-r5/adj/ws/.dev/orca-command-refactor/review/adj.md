# Adjudication of review findings X1-X16

Inputs read: `.dev/orca-command-refactor/README.md`, `specs/orca-worker-contract-spec.md` (cited as `SPEC:N`), `review/adj-input.md`, and the three inventories (`INV-A`, `INV-B`, `CAPS`) where a finding depends on them. Files outside the workspace (`src/`, `cmd/`, `sk/`, Orca sources) could not be opened; anything resting on them is UNVERIFIED.

Test applied to each finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." Confirmed only when the sentence holds with no further assumption.

Result: 2 confirmed (X3, X4), 1 unsure (X13), 13 rejected.

## Confirmed

### X3 - confirmed
Sentence: an implementer who runs AC-C5 or AC-0.3 as written (`git diff -U0 ... | grep -E '^-[^-]'`, `SPEC:176`, `SPEC:193`) builds an "edits are additive" check, and the check is wrong because it prints nothing for a removed line whose own text starts with `-` (the diff line is `-- item`), for a removed `---` frontmatter delimiter, and for a removed blank line (the diff line is a lone `-`).
- This follows from the regex alone: `[^-]` requires a second character that is not a dash.
- The files checked are markdown command files and `HOW-WE-WORK.md`, where `- ` bullets and `---` delimiters are ordinary content, so a non-additive edit passes SA-4's only mechanical gate.
- The finding's wording "lines beginning with two dashes" is slightly off (a source line starting with one dash is already missed), which makes the gap wider, not narrower.

### X4 - confirmed
Sentence: an implementer who follows the adversarial row (`SPEC:83`) builds a contract at `<output>/adversarial/return-contract.yaml`, and that is wrong because WC-4 (`SPEC:62`) and the section 3 definition (`SPEC:76`) say the contract is `<output-dir>/return-contract.yaml` in the directory the coordinator passed, and check 7.2 step 3 (`SPEC:182`) requires the report path to be "the WC-4 contract path".
- The two statements name different paths for the same file and the same `--output` value, so both cannot be satisfied.
- WC-4's allowance for existing contracts covers fields only ("keep their fields and add the missing ones"), not location.
- The finding's last clause is overstated: the worker would pass the path it actually wrote. The path that does not exist is the one the coordinator derives before dispatch from WC-4 (section 2.3, `SPEC:73`).

## Unsure

### X13 - unsure
The tasklist row (`SPEC:122`) resolves the reflect `[yes / no]` offer by passing `--unattended`, but names no resolution for the Stage 10.5 HALT on `needs_human_decision` items that `INV-B:209` records at `sk/sc-tasklist-protocol/SKILL.md:1631`. WC-2 says each gate's resolution is "listed per command in section 3", so the row is incomplete on its face. Whether the HALT waits on a person or simply ends the run with a report depends on that skill line, which is outside the workspace (UNVERIFIED). The "stops without worker_done" part needs that assumption; WC-5 has the worker session send `worker_done` once the command ends either way.

## Rejected

### X1 - rejected
The row keeps reflect fan-out in subagents, against the change in `INV-B:214`. For that to be wrong, nested spawning has to fail. `INV-B:210` marks that UNVERIFIED, and `INV-A:14` quotes Claude Code as allowing three layers below the main conversation. Worker to reflect subagent to reflect's own agents is two layers. The divergence from the inventory is an unrecorded decision, not a wrong build.

### X2 - rejected
The WC-10 trigger (over 5 minutes) and the split size (4 minutes) do differ, so a 4-5 minute call is not caught by the general rule. But the two commands the spec identifies with long waits are pinned at 4 minutes in their own rows (`SPEC:104` cli-eval, `SPEC:114` pr-submit) and in AC-4.3 (240 s). The defect appears only if some other command has a single 4-5 minute blocking call, which is an added assumption. Worth a one-word wording fix; not blocking.

### X5 - rejected
E4 says subagents "are not counted by Orca's nesting limit". `CAPS:155` states exactly that as a finding; its UNVERIFIED covers a different point (whether Orca limits subagents in any other way). The spec states that gap itself in section 1.4 item 3. Nothing is built from E4.

### X6 - rejected
The section 1.1 summary sentence is looser than section 3, but SA-4 (`SPEC:149`) lists the defect fixes by name, including the roadmap drift. An implementer works from section 3 and SA-4 and builds the same thing either way.

### X7 - rejected
Section 3.1 defines "ready today" as ready "if the brief uses the stated flags", with small fixes in the last column (`SPEC:79`). The reflect brief passes no `--remediate`, so the P2 fix to `--remediate` does not contradict the label.

### X8 - rejected
`invocation_method: "skill-direct"` (E3, `INV-A:13`) sits awkwardly beside section 1.4's "no direct-route run was observed". That is a tension in how the evidence is read, and the contract file is outside the workspace (UNVERIFIED). It changes no build instruction: P0's smoke runs happen under either reading.

### X9 - rejected
Same ground as X1. The silent failure needs the fan-out to sit at the depth limit, which the layer count in `INV-A:14` does not show. WC-7 keeps the tasklist command itself at the top level. The dropped inventory change is a missing Decisions entry, not a wrong build.

### X10 - rejected
AC-C1 fails only if the P0 text added to `src/superclaude/core` contains lowercase `orca` or `orca-ide` followed by `orchestration`, `worktree`, `terminal` or `agent`. The spec does not require that wording, and section 2 as written does not contain it (WC-8 names bare verbs; "Orca" capitalised does not match). The check constrains the wording; it does not make the build wrong.

### X11 - rejected
The pr-submit row and the 27 count are stated as conditional on D3 (`SPEC:139`), Phase 4 waits for D3 (`SPEC:154`), and AC-4.3 opens with "If D3 allows". The classification moving with an open user decision is recorded, not a defect.

### X12 - rejected
Reflect's default tracked-file write and folder move (`INV-B:114`) are local and documented. WC-9 covers outward actions only. The tracked file carries a slug, which meets WC-11. The row offers `--no-promote`. Calling this wrong needs the assumption that those local writes are harmful.

### X14 - rejected
"Well inside the readiness limit" has no number in the requirement cell, but WC-1 is owned by launch setup, no phase builds a fallback, and the evidence cell gives the observed bounds (passes at 30 s, fails above about 45 s, `SPEC:59`).

### X15 - rejected
"Phases 1-3 need no user decision" (`SPEC:154`) and "Phases 0-3 can proceed on the recommendations" (`SPEC:225`) are compatible: both say the work goes ahead on D1's and D4's recommended options. A wrong build arises only if the user later picks a non-recommended option, which is an added assumption.

### X16 - rejected
This describes a limit of the review (citations point outside the workspace), not something the spec tells an implementer to build. The spec itself discloses which locations were re-read (`SPEC:11`).

```adj-v1
{"x": "X1", "verdict": "rejected", "reason": "Keeping reflect fan-out in subagents is wrong only if nested spawning fails, which INV-B:210 marks UNVERIFIED and INV-A:14 contradicts (two layers used, three allowed)."}
{"x": "X2", "verdict": "rejected", "reason": "The 5-minute trigger versus 4-minute split mismatch is real, but cli-eval and pr-submit are pinned at 4 minutes in their own rows, so a wrong build needs an unidentified 4-5 minute call."}
{"x": "X3", "verdict": "confirmed", "reason": "grep -E '^-[^-]' prints nothing for removed lines that start with a dash (markdown bullets, --- delimiters) or are blank, so AC-C5 and AC-0.3 pass non-additive edits."}
{"x": "X4", "verdict": "confirmed", "reason": "The adversarial row fixes the contract at <output>/adversarial/return-contract.yaml while WC-4, the section 3 definition and check 7.2 step 3 define it as <output-dir>/return-contract.yaml, so both cannot be met."}
{"x": "X5", "verdict": "rejected", "reason": "CAPS:155 states the nesting-limit point as a finding and marks only a broader no-limit-at-all claim UNVERIFIED, which the spec discloses in section 1.4."}
{"x": "X6", "verdict": "rejected", "reason": "The section 1.1 summary is loose, but SA-4 names the defect fixes including roadmap drift, so the implementer builds the same thing."}
{"x": "X7", "verdict": "rejected", "reason": "Section 3.1 defines ready-today as ready with the stated flags plus small fixes, and the reflect brief passes no --remediate."}
{"x": "X8", "verdict": "rejected", "reason": "The skill-direct citation is an evidence-reading tension that changes no build instruction, since the P0 smoke runs happen under either reading."}
{"x": "X9", "verdict": "rejected", "reason": "The silent Agent-tool loss needs the fan-out to sit at the depth limit, which the layer count does not show; the dropped inventory change is an unrecorded decision only."}
{"x": "X10", "verdict": "rejected", "reason": "AC-C1 fails only if the P0 core text uses a lowercase orca-plus-subcommand wording the spec does not require."}
{"x": "X11", "verdict": "rejected", "reason": "The pr-submit classification is stated as conditional on D3, and Phase 4 and AC-4.3 are gated on that answer."}
{"x": "X12", "verdict": "rejected", "reason": "Reflect's tracked-file write and folder move are local, documented, slug-named and switchable with --no-promote, so calling them wrong needs an added assumption."}
{"x": "X13", "verdict": "unsure", "reason": "The tasklist row names no resolution for the needs_human_decision HALT, but whether that HALT waits on a person depends on a skill line outside the workspace."}
{"x": "X14", "verdict": "rejected", "reason": "WC-1 is owned by launch setup with no phase building a fallback, and its evidence cell gives the observed 30 s and 45 s bounds."}
{"x": "X15", "verdict": "rejected", "reason": "The two gating statements both say Phases 0-3 proceed on the recommended options, so a wrong build needs the user to choose otherwise."}
{"x": "X16", "verdict": "rejected", "reason": "Citations outside the workspace are a limit of the review, not something the spec tells an implementer to build."}
```
