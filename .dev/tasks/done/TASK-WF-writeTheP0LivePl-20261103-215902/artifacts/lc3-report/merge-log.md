# Merge Execution Log

## Metadata
- Base: Variant 1 (option a, explicit --unattended flag; default model)
- Executor: merge-executor agent
- Changes applied: 8 of 8
- Status: success
- Timestamp: 2026-11-04T08:58:52Z

## Changes Applied

### Change 1: Correct the citation key and add the guide source
- **Status**: Applied
- **Source**: Variant 2, citation key line (V2:5) for the `[G]` entry; SPEC path correction from `base-selection.md` Structure criterion 4 (via the plan)
- **Target**: Base, citation key line (V1:5) (replace)
- **Before**: Key mapped `SPEC:N` to `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N` and listed only SPEC and CAPS.
- **After**: Key maps `SPEC:N` to `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md:N` with the note "(the spec version this paper was written against; the current spec is renumbered)", keeps the CAPS entry, and adds `[G] N` = line N of `orca-ide skills get orchestration` (1.4.237). No body SPEC or CAPS number changed.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change #1, SPEC path corrected to the spec version the line numbers match; [G] entry merged from Variant 2, citation key line (V2:5); Disposition: merged-from-multiple -->`
- **Validation**: Structural integrity PASS (single paragraph replaced in place) | References PASS (key now covers SPEC, CAPS and [G], all three used in the body after Change 3) | Contradictions PASS (none)

### Change 2: Qualify the 2026-11-02 observation and add the person scenario
- **Status**: Applied
- **Source**: Variant 2, Safety (V2:13) for the `/sc:cleanup --interactive` scenario; debate shared assumptions A-001 and A-002 (QUALIFY) for the qualification
- **Target**: Base, Safety, second bullet (V1:9) (modify)
- **Before**: "Detection would misfire, and that is now observed rather than hypothetical." followed by the 2026-11-02 observation, item 13 and the SPEC:330 quote, ending "An explicit flag is immune to it."
- **After**: Opening changed to "partly observed". All original text and citations kept exactly. After the SPEC:330 quote: the concrete case (`/sc:cleanup --interactive` in a person's own Orca tab loses approval prompts and outward defaults, V2:13), then the qualification (observation used `worker-list` without `--include-remote`, CAPS:128; not the direct `check --terminal` test, CAPS:151; not made in a hand-opened tab; item 13 narrowed, not closed). "An explicit flag is immune to it." kept last. The 2026-11-04 subagent-shell report was not carried, as the plan directs.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change #2, "observed" narrowed to "partly observed", person scenario merged from Variant 2, Safety (V2:13), qualification from shared assumptions A-001 and A-002 (debate); Disposition: merged-from-multiple -->`
- **Validation**: Structural integrity PASS (bullet edited in place) | References PASS (CAPS:128, CAPS:151, SPEC:330, SPEC:395 present; anchors "2026-11-02", "11 workers", `ORCA_TERMINAL_HANDLE`, `agentTerminalHandle`, item 13 kept exact) | Contradictions PASS (none). Note: the inline attribution "(V2:13)" follows the plan's integration text; V2 has no entry in the citation key because the plan specifies none.

### Change 3: Answer the preamble route directly
- **Status**: Applied
- **Source**: Variant 2, Strongest case for it (V2:8) and Safety (V2:14); V2:17 for the invisible wrong judgement; debate X-009 for separating Orca's rule from the command's judgement
- **Target**: Base, Safety, new bullet inserted after V1:9 (insert)
- **Before**: Section did not answer the preamble route (requirement R5 gap).
- **After**: New third Safety bullet in the plan's order: (1) preamble detection is the strongest form of detection and safer for people than the environment route; Orca's guide labels "Dispatched worker" and "Ordinary terminal agent" quoted verbatim (`[G]` lines 38 and 41; CAPS:148; SPEC:53); (2) Orca's definition is a rule, but applying it is the command's judgement from prose (SPEC:330), and a wrong judgement is invisible until a stall or a lost prompt (V2:17); (3) Orca passes the task on its command line (CAPS:47) and the preamble arrives with it (V2:14), so the two are hard to tell apart in a test. Executor note followed: CAPS:47 cited only for the task on the command line; the preamble arriving with it attributed to V2:14. The bullet does not declare the route safe or unsafe overall (X-001 unresolved).
- **Provenance tag**: `<!-- Source: Variant 2, Strongest case for it (V2:8) and Safety (V2:14), with V2:17 and the X-009 debate wording separating Orca's rule from the command's judgement — merged per Change #3; Disposition: merged-from-multiple -->`
- **Validation**: Structural integrity PASS (bullet inside Safety list, before the WC-9 bullet) | References PASS (`[G]` now defined in the key by Change 1; CAPS:148, SPEC:53, SPEC:330, CAPS:47 present) | Contradictions PASS (none; "safer ... than the environment route" is comparative and qualified in the same bullet)

### Change 4: Narrow "Deterministic" to what is actually checkable
- **Status**: Applied
- **Source**: Debate, X-004 (Variant 2 at 97%; V1 Concession 1) and shared assumption A-008
- **Target**: Base, Reliability, first bullet (V1:13) (modify)
- **Before**: "Deterministic and checkable by text: the brief is plain text ... (`SPEC:257`). The live 7.2 checks then show the flag's effect (`SPEC:234-246`)."
- **After**: Opens "The flag's presence is checkable by text:" with the brief and AC-1.1 clause unchanged (SPEC:257). Adds: what is not deterministic is whether the command obeys the parse rule, because the model applies it (see Implementation cost); that is checked live by AC-2.8 (SPEC:269) and the 7.2 checks (SPEC:234-246), not by text. The final sentence "The live 7.2 checks then show the flag's effect (`SPEC:234-246`)." kept verbatim.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change #4, "Deterministic" narrowed to what is checkable by text per debate X-004 and shared assumption A-008; Disposition: modified -->`
- **Validation**: Structural integrity PASS (bullet edited in place) | References PASS ("see Implementation cost" resolves to the H2 "Implementation cost"; AC-1.1, SPEC:257, AC-2.8, SPEC:269, 7.2, SPEC:234-246 present) | Contradictions PASS (removes the "Deterministic" against "applied by the model" contradiction)

### Change 5: Add the coupling and headless-precedent argument
- **Status**: Applied
- **Source**: Variant 2, Reliability (V2:18, V2:19); per-command coupling from V2:25 (the AC-C1 grep claim in V2:25 excluded, as the plan directs)
- **Target**: Base, Reliability, new bullet inserted after V1:14 (insert)
- **Before**: Reliability had no coupling or headless-precedent argument.
- **After**: New bullet after "Caller-neutral": option (b) would put Orca-specific branching into every command (V2:25), forbidden by non-goal 1 (SPEC:314) and kept out by SA-2 because commands run in other projects (SPEC:170; CLAUDE.md:74); the repo's one headless precedent detects `claude --print` with no TTY (remediation-handoff.md:239-242) and would not fire for an Orca worker, launched interactively with the prompt on the command line (SPEC:391; CAPS:47).
- **Provenance tag**: `<!-- Source: Variant 2, Reliability (V2:18, V2:19), with the per-command coupling from V2:25 — merged per Change #5; Disposition: merged-from-multiple -->`
- **Validation**: Structural integrity PASS (bullet inside Reliability list, before "Phase-gated") | References PASS (SPEC:314, SPEC:170, CLAUDE.md:74, remediation-handoff.md:239-242, SPEC:391, CAPS:47 present, exact) | Contradictions PASS at this step; the tension with V1:23 "cheap" is resolved by Change 7

### Change 6: Move and rewrite the known weakness
- **Status**: Applied
- **Source**: Variant 2, Strongest case for it (V2:9) for the failure-class framing and V2:17 for the missed-preamble stall; debate evidence (`rounds/r1-variant-1.md` Key Strength 6 and Concession 3; `rounds/r1-variant-2.md` Key Strength 2); A-005 for the gate qualifier
- **Target**: Base, "How a person works day to day", second bullet (V1:19) (moved to the end of Reliability and rewritten)
- **Before**: Under the person section: "Known weakness: if a coordinator forgets the flag, the command prompts and the worker stalls with no `worker_done`, which Orca reports as healthy (`SPEC:47`; `CAPS:52`). The brief template and the 7.2 step-3 stall proof (`SPEC:238`) catch it, but only after the fact."
- **After**: V1:19 removed from the person section; V1:18 left there unchanged. New last Reliability bullet "Known weakness:" in the plan's order: (1) forgotten flag is a coordinator-side failure class detection aims to remove (V2:9), though a missed preamble stalls the same way (V2:17); (2) P1 command has no gate (SPEC:182), runs in person mode, writes no worker contract, worker reports failed (WC-5, SPEC:69); a gated command prompts only when the coordinator's arguments reach a gate, then stalls with no `worker_done`, reported healthy (SPEC:47; CAPS:52); (3) stall visible only after the fact: transcript with no `worker_done` on the last turn is the positive proof (CAPS:126; the 7.2 step-3 stall proof at SPEC:238), `agentWait` names a worker parked on a prompt (CAPS:129), UNVERIFIED for a turn ending on a chat question (SPEC:397); (4) person mode keeps outward defaults on (SA-1, SPEC:169), so a forgotten flag on auggie-review would post its review; (5) the brief template reduces the chance (SPEC:58, SPEC:79). No P1 count written ("14 P1 commands" dropped per the plan).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change #6, V1:19 moved from "How a person works day to day" to the end of Reliability and rewritten; failure-class framing from Variant 2, Strongest case for it (V2:9) and V2:17; gate qualifier from debate A-005; P1, agentWait and outward-default points from debate (r1-variant-1.md Key Strength 6, Concession 3; r1-variant-2.md Key Strength 2); Disposition: merged-from-multiple -->`
- **Validation**: Structural integrity PASS (person section keeps one bullet; Reliability ends with Known weakness) | References PASS (SPEC:47, CAPS:52, SPEC:238, "7.2 step-3 stall proof", brief template, SPEC:182, SPEC:69, CAPS:126, CAPS:129, SPEC:169, SPEC:397, SPEC:58, SPEC:79 present) | Contradictions PASS (known weakness appears once)

### Change 7: Qualify "cheap" and add the reverse-cost point
- **Status**: Applied
- **Source**: Variant 2, Implementation cost (V2:25, second sentence); debate X-002 and V2 Concession 7
- **Target**: Base, Implementation cost, second bullet (V1:23) (modify and append)
- **Before**: "Changing later is cheap: if detection ever becomes reliable, it can be added as an extra trigger without removing the flag."
- **After**: Original sentence kept verbatim, then: adding it would also need an explicit amendment to SA-2 (SPEC:170) or non-goal 1 (SPEC:314), so "cheap" means cheap to edit, not free of a spec change; then: going the other way, from per-command detection back to a flag, would mean touching every command again (V2:25).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change #7, "cheap" qualified with the SA-2 or non-goal 1 amendment per debate X-002 and V2 Concession 7; reverse-cost sentence merged from Variant 2, Implementation cost (V2:25, second sentence); Disposition: merged-from-multiple -->`
- **Validation**: Structural integrity PASS (bullet extended in place) | References PASS (SPEC:170, SPEC:314 present, exact) | Contradictions PASS (resolves the tension between Change 5's "non-goal 1 forbids" and the unqualified "cheap")

### Change 8: Add the open points the debate left
- **Status**: Applied
- **Source**: Debate, `debate-transcript.md` Convergence Assessment; `rounds/r1-variant-2.md` Key Strength 6 (fail-closed fallback, SPECULATIVE); `rounds/r1-variant-1.md` Concessions 2 and 3
- **Target**: Base, new final H2 "Open points" after Implementation cost (append)
- **Before**: Section did not exist (no next steps).
- **After**: New H2 "Open points" with the six bullets in the plan's order: (1) preamble-triggered fail-closed fallback, SPECULATIVE, needs an SA-2 or non-goal 1 amendment, unresolved (X-001); (2) pre-dispatch token check on every brief using the AC-1.1 phase table, SPECULATIVE; (3) repeat AC-2.8-style runs and add the standalone-token-after-long-quoted-argument case, AC-2.8 is one manual run (SPEC:269) (A-008); (4) count how many of the 35 commands (36 with pr-submit, SPEC:195) would prompt on a coordinator's arguments (A-005); (5) close item 13 directly with a hand-opened tab, `check --terminal` (CAPS:151) and `worker-list --include-remote` (CAPS:128) (A-001, A-002); (6) repeat on later Orca versions and launch paths (A-003, unresolved).
- **Provenance tag**: section `<!-- Source: Debate, debate-transcript.md Convergence Assessment — merged per Change #8; Disposition: merged-from-multiple -->`; each bullet carries its own `<!-- Source: Debate, <ref> — merged per Change #8; Disposition: modified -->` tag naming its debate point.
- **Validation**: Structural integrity PASS (one new H2, placed last) | References PASS (SPEC:269, SPEC:195, CAPS:151, CAPS:128, AC-1.1, AC-2.8, item 13 present) | Contradictions PASS (every speculative item labelled SPECULATIVE; bullet 1's amendment requirement matches Changes 5 and 7)

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1 (line 6). Five H2 sections, no H3 or deeper, so no level gaps (H1 to H2 only).
- Section ordering: PASS. Safety (15), Reliability (26), How a person works day to day (39), Implementation cost (44), Open points (51), the required order.
- Document flow: PASS. No orphan text: every body line is a heading, the Position paragraph, the citation key paragraph, or a list bullet under an H2, and each has a provenance comment directly above it. The person section now holds one bullet (V1:18, unchanged), as Change 6 directs.
- Plain English and dash check: PASS. Grep for the em dash character finds it only on provenance comment lines; no body line contains one.

### Internal References
- Total references: 3
  1. "(see Implementation cost)" in Reliability bullet 1 (line 28): target H2 "Implementation cost" exists (line 44). Resolved.
  2. "Orca's guide" in Safety bullet 3 (line 21) with `[G]` lines 38 and 41: target is the `[G]` entry in the citation key (line 12, added by Change 1). Resolved.
  3. "the size of the known weakness" in Open points bullet 4 (line 59): target is the "Known weakness" bullet at the end of Reliability (line 36). Resolved.
- Resolved: 3
- Broken: 0
- Observation (not a broken reference): inline variant attributions "(V2:9)", "(V2:13)", "(V2:14)", "(V2:17)", "(V2:25)" follow the plan's integration text and executor note. The citation key has no V2 entry because the plan specifies none; the merge does not add one.

### Contradiction Re-Scan
- (a) "Deterministic" no longer stands unqualified: PASS. The only body use is "What is not deterministic is whether the command obeys the parse rule" (line 28); the word "Deterministic" survives only in a provenance comment (line 27).
- (b) Safety does not call preamble detection simply "safe": PASS. Line 21 says it "is safer for people than the environment route", then states that applying Orca's rule is the command's judgement and is hard to test. No other "safe" in Safety.
- (c) "cheap" in Implementation cost is qualified: PASS. Line 48 adds the explicit amendment to SA-2 (`SPEC:170`) or non-goal 1 (`SPEC:314`) and "cheap means cheap to edit, not free of a spec change", consistent with Change 5's "non-goal 1 forbids" (line 32).
- (d) Known weakness appears once, under Reliability: PASS. Grep finds "Known weakness" once (line 36); it is absent from the person section.
- New contradictions introduced: 0
- Details: none. Checked and cleared: (1) Safety bullet 2 still opens "Detection would misfire" while bullet 3 calls preamble detection safer for people; bullet 2's evidence is the environment route and bullet 3 compares against it explicitly, so they do not conflict. (2) Known weakness says a P1 command "has no gate" and runs in person mode; this agrees with "Phase-gated" (line 34). (3) Open points bullet 1 (preamble-triggered fallback) relies on the judgement Safety bullet 3 describes, and it is labelled SPECULATIVE with the same amendment requirement as Changes 5 and 7.

### Threshold Preservation and Dropped-Anchor Audit
Grep on `merged-output.md` for each value:

| Anchor | Expected disposition | Found | Result |
|---|---|---|---|
| "11 workers" | preserved-exact | line 19 | PASS |
| "2026-11-02" | preserved-exact | line 19 | PASS |
| "1.4.237" | preserved-exact | line 12 | PASS |
| `[G]` lines 38 and 41 | preserved-exact | line 21 | PASS |
| "Dispatched worker" (quoted) | preserved-exact | line 21 | PASS |
| "Ordinary terminal agent" (quoted) | preserved-exact | line 21 | PASS |
| "36 with pr-submit" | modified-with-rationale ("35 commands (36 with pr-submit, `SPEC:195`)") | line 59 | PASS |
| AC-1.1, AC-2.8, 7.2, 7.2 step-3, WC-5, WC-9, SA-1, SA-2, item 13, non-goal 1 | preserved-exact | all found (lines 17-63) | PASS |
| `ORCA_TERMINAL_HANDLE`, `agentTerminalHandle` | preserved-exact | lines 19, 61 | PASS |
| Plan SPEC list: 47, 53, 58, 69, 79, 169, 170, 182, 195, 234-246, 238, 257, 269, 314, 330, 391, 395, 397 | present | all 18 found | PASS |
| Plan CAPS list: 47, 52, 126, 128, 129, 148, 151 | present | all 7 found | PASS |
| Every SPEC and CAPS number already in V1 (328-331, 329, 55, 269, 395, 330, 73, 169, 257, 234-246, 54, 361, 170, 187-195, 58, 79, 47, 238, 55-58; CAPS:52) | preserved-exact | all found, values unchanged | PASS |
| `CLAUDE.md:74`, `remediation-handoff.md:239-242`, `SPEC:391` (Change 5) | preserved-exact | line 32 | PASS |

Dropped-anchor audit (anchors the plan drops on purpose; Grep confirms each is absent from the merged body):

| Anchor | Plan disposition | Grep result | Result |
|---|---|---|---|
| "2026-11-04" advocate report of the variable in a subagent shell | dropped-with-rationale (`refactor-plan-review.md`, Round 2, N1) | only in the header comment "Merge date: 2026-11-04T08:58:52Z", not in body | PASS |
| "14 P1 commands" | dropped-with-rationale (not re-verified) | absent | PASS |
| SPEC:207 / `SPEC:205-212` (AC-C1 grep exception) | dropped-with-rationale (claim false) | absent | PASS |
| `SPEC:189-195` for the 35-command count | replaced by `SPEC:195` | absent; `SPEC:195` present | PASS |
| `ORCA_TERMINAL_HANDLE` as a trigger (V2:3) | omitted; kept only as the observed misfire | appears only as the misfire (line 19) and the item 13 check (line 61) | PASS |
| "Shorter briefs" (V2:10) | omitted | absent | PASS |

No concrete anchor was replaced with vaguer text.

## Summary
- Total changes planned: 8
- Successfully applied: 8
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
