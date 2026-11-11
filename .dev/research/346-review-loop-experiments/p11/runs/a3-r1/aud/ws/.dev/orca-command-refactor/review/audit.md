review: 1 of 3

# Whole-document audit of the Orca worker-contract spec (/sc:spec-panel, critique mode)

```yaml
specification_review:
  command: "/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture"
  kind: "first review of the whole document (labelled whole-document audit); not a scoped re-review"
  candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  candidate_sha256: d1f34e4bb75f645e00e9b421dc8abdf0366d981ef45c7dfcc8f6689db8833a6a   # sha256sum, 285 lines, 57973 bytes
  baseline: none given   # no --re-review and no --baseline, so no "baseline: missing" note applies
  reviewer_model: Sonnet 5.5 (claude-sonnet-5-5)
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]   # focus requirements + architecture, plus Whittaker (always active)
  focus_areas: [requirements, architecture]
  prompt_followed: "FIRST-REVIEW prompt, ~/.claude/rules/prompts/document_review_loop_prompts.md:27-32 (read in full)"
quality_assessment:   # 0-10
  clarity: 7
  completeness: 6
  testability: 6
  consistency: 6
```

Citation aliases. `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = line N of `.dev/orca-command-refactor/README.md`. `CMD:N` = line N of `command.md` (the /sc:spec-panel definition used for this run, inside the sandbox). `PROMPTS:N` = `~/.claude/rules/prompts/document_review_loop_prompts.md`. A `src/`, `CLAUDE.md`, `cmd/`, `sk/` or `.dev/evals/` citation that is not inside the workspace is UNVERIFIED here and is only trusted where an inventory quotes it.

## Coverage (what this review covered)

- Read in full: the candidate (SPEC:1-285), README (README:1-39), all three inventories (INV-A:1-120, INV-B:1-323, CAPS:1-188), CMD:1-491, PROMPTS:1-55.
- Checked against the inventories (all resolved to the cited line): every `INV-A:N`/`INV-B:N`/`CAPS:N` pointer in SPEC:21-37, 59-70, 83-92, 99-125, 132-137, 260-268; the 10 / 27 / 6 split (3.1 has 10 rows SPEC:83-92, 3.2 has 27 rows SPEC:99-125, section 4 has 6 rows SPEC:132-137, matching INV-A:73 and INV-B:278); the P1-P4 command lists against the 3.2 phase column (P1 9, P2 11, P3 4, P4 3 = 27; plus P2 gate fixes for 4 ready commands = 15 at SPEC:160).
- Checked by a shell test inside the sandbox: the regex in AC-C5 and AC-0.3 (finding M4).
- Not checkable here (no file in the workspace): every `cmd/`, `sk/`, `ag/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `install_core.py`, `pyproject.toml`, `Makefile`, `EVIDENCE.md`, `.dev/codegraph-migration/` citation, the E5 grep results (SPEC:25), the claims at SPEC:11 and SPEC:285 that earlier citation checks passed, and the existence of `review/spec-panel.md` and `review/disposition.md` (absent from the workspace, so the finding ids F1/F2 at SPEC:182,194-196 cannot be resolved). The spec's own wording that pr-submit's 600 s is a cumulative budget (SPEC:68, `sk/sc-pr-submit-protocol/SKILL.md:46-64`) differs from INV-B:95, which says "waits up to --timeout 600 s per wait"; UNVERIFIED which is right.
- Not covered: the Improve step (no revised spec is written by a review), `--focus correctness` artifacts (not requested; the Guard Condition Boundary Table and Quantity Flow Diagram below are produced because the spec contains guards and a multi-stage rollout).
- Brief clauses overridden: none. The brief neither widened scope nor graded any finding.

## Guard Condition Boundary Table (Nygard builds, Crispin-role completeness check, Whittaker attacks)

Hard gate (CMD:313-334): built before the findings. Classes left out are named in the one-line notes under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | SPEC:51,60,146,228 | Zero/Empty | flag absent | false | Today's behavior unchanged (SPEC:146) | OK |
| `--unattended` switch | SPEC:51,60 | Typical | standalone token on a worker command line | true | WC-2 gate resolution, WC-4 contract | OK |
| `--unattended` switch | SPEC:51,228 | Sentinel Value Match | the string `--unattended` inside quoted prompt content (for example `/sc:troubleshoot "login fails when --unattended is set"`) | unspecified | Not specified; D1(a) says only "testable by grep" (SPEC:228) | GAP (M7) |
| `--unattended` switch | SPEC:128 | Legitimate Edge Case | flag passed to one of the 6 coordinator-only commands | unspecified | SPEC:128 says they "get no `--unattended` mode"; what they do with the token is not said | GAP (M7) |
| Output location `<output-dir>` | SPEC:62 | Zero/Empty | `--unattended` with no output flag | unspecified | Not specified; WC-4 says the directory is "the directory the coordinator passed" | GAP (M7) |
| Output location `<output-dir>` | SPEC:62,73 | Typical | `--output <dir>` (brainstorm, reflect, adversarial, `--output-dir` for auggie-review) | true | `<dir>/return-contract.yaml` | OK |
| Output location `<output-dir>` | SPEC:62,87,90,200 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | unspecified | WC-4 calls the value a directory; SPEC:87,90 call it a file; AC-2.2 runs `--output <file>` and needs the contract | GAP (B2) |
| Output location `<output-dir>` | SPEC:62,85,86 | Legitimate Edge Case | command with a fixed or no output flag (cleanup-audit `.claude-audit/`, index-repo) | unspecified | Contract location not named | GAP (B2) |
| WC-5 outcome map | SPEC:63 | Zero/Empty | no report file exists | n/a | `--outcome failed` | OK |
| WC-5 outcome map | SPEC:63 | Typical | `status` = succeeded / partial / failed / blocked | n/a | succeeded, succeeded, failed, failed | OK |
| WC-5 outcome map | SPEC:62,63,263 | Sentinel Value Match | existing contract keeps its own `status` value outside the four | n/a | Not specified ("keep their fields", SPEC:62, versus a closed set, SPEC:263) | GAP (M11) |
| WC-5 outcome map | SPEC:63 | Legitimate Edge Case | audit verdict FAIL | n/a | `--outcome succeeded`, body states the verdict | OK |
| WC-10 wait split | SPEC:68,210 | Zero/Empty | no blocking wait | n/a | No action | OK |
| WC-10 wait split | SPEC:68 | Typical | wait of 4 min or less | n/a | Allowed | OK |
| WC-10 wait split | SPEC:68,210 | Maximum/Overflow | a single call of 4 to 5 min, or longer than 5 min | unspecified for 4-5 min | Over 5 min must be split to at most 4 min; AC-4.3 fails any call over 240 s; a 4.5 min call breaks the AC but not the requirement | GAP (M8) |
| `/sc:task` confidence | SPEC:121 | Zero/Empty | 0 | true | blocked | OK |
| `/sc:task` confidence | SPEC:121 | Legitimate Edge Case | 0.70 exactly | false | Text says "below 0.70" blocked, so 0.70 proceeds | OK |
| `/sc:task` EXEMPT commit/push | SPEC:67,121 | Legitimate Edge Case | brief wants the push | n/a | "refused unless authorized (WC-9)", but no flag exists (WC-9 needs "the command's own explicit flag") | GAP (M9) |
| roadmap resume | SPEC:118,205 | Typical | state exists, flag passed | true | resume | OK |
| roadmap resume | SPEC:205 | Legitimate Edge Case | state exists, no flag | false | starts fresh (AC-3.2) | OK |
| roadmap resume | SPEC:118 | Legitimate Edge Case | flag passed, no state file | unspecified | Not specified | GAP (M2) |
| retry output dir | SPEC:64,73 | Legitimate Edge Case | `--retry-of` worker given the same output directory | unspecified | "fresh output directory" (WC-6) but the coordinator passes the directory (WC-4) and the brief list omits "new directory per attempt" | GAP (M2) |
| nested-depth fence | SPEC:33,66 | Typical / Maximum | depth 1 / a command calls `worker-start` | true | refused, WC-8 forbids the call | OK |

Left out, with the reason: One/Minimal and Maximum classes for `--unattended`, for the output location and for the outcome map cannot occur (the values are booleans, a path, or a closed set); Maximum/Overflow for the confidence guard cannot occur (a score in 0-1); the nested-depth guard has no zero class because the fence is a fixed constant (CAPS:97).

FR-8/FR-9 grading (CMD:259,332-333): GAP rows B2 name a concrete wrong outcome and are blocking; the other GAP rows need a guess about which reading the implementer picks, or state a requirement the document never states, so they are Medium.

## Quantity Flow Diagram (Fowler leads, Whittaker attacks the divergence; pipeline = section 3 to section 6 to section 7)

```text
[43 commands, SPEC:76] --> [Section 4 filter: -6 coordinator-only, SPEC:128-137] --> [37 worker candidates: 10 ready + 27 change]
     |
     v
[P1 scope, SPEC:159: "--unattended flag accepted by every command in sections 3.1 and 3.2" = 37]
     |
     v
[AC-1.1, SPEC:195: section required in "every command in sections 3.1-3.2 except load" = 36]
     |
     +--> [Decidable without the user, SPEC:154 "Phases 1-3 need no user decision": 36 - 3 P4 commands = 33]
     +--> [P4 commands whose behavior waits on D2-D4, SPEC:162: implement, post-release, pr-submit = 3]   <-- MISMATCH (36 asserted, 33 decidable)
     +--> [pr-submit under recommended D3(a), SPEC:139,240: not a worker at all = 1 of the 3]
```

Under FR-19 (CMD:370-372) this dimensional mismatch is CRITICAL: AC-1.1 expects 36 sections at the end of P1, but only 33 are decidable then; this is finding B1.

## === REQUIREMENTS ANALYSIS ===

### B1 [CRITICAL, blocking] AC-1.1 and the P1 scope require unattended mode in the three commands whose behavior is deferred to the user's decisions
- Where: SPEC:159 (P1 "flag accepted by every command in sections 3.1 and 3.2"), SPEC:195 (AC-1.1 "every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section ... and no section-4 command has one"), against SPEC:154 ("Phase 4 waits for answers to D2-D4"), SPEC:162 (P4 = implement, post-release, pr-submit), SPEC:109,113,114 (their gate resolutions depend on D2/D4/D3), SPEC:128 and SPEC:139 (pr-submit "stays a worker candidate only if the user accepts D3"), SPEC:240 (D3(a), recommended: "no pr-submit changes in Phase 4").
- Grading check (PROMPTS:31): An implementer who follows the stated text as written builds, in Phase 1, a `## Unattended mode` section and an accepted `--unattended` flag in `implement`, `post-release` and `pr-submit` (to pass AC-1.1), and that is wrong because SPEC:154 and SPEC:162 make those three behaviors wait for D2-D4, SPEC:240 says the recommended D3 gives pr-submit no changes, and SPEC:128 says a command that is not a worker gets no unattended mode. Two stated texts contradict each other and AC-1.1 cannot be satisfied together with SPEC:162 and SPEC:240.
- Expert: Wiegers (consistency of requirements), Fowler (phase boundary), Whittaker (Sequence Attack): I can break this specification by **Sequence Attack**. The invariant at **SPEC:154-162** (user decisions precede the three safety-relevant commands) fails when **P1 is executed to pass AC-1.1**. Concrete attack: Before P1, `cmd/pr-submit.md` has no unattended mode (SPEC:25 baseline). P1 adds a section naming `return-contract.yaml` (SPEC:195). The user then picks D3(a). After P1, pr-submit ships an unattended mode that SPEC:240 says should not exist.
- Recommendation: narrow AC-1.1 and the P1 scope sentence to the commands outside P4 (the 33), and let the P4 phase add the three sections after D2-D4. Rationale: it deletes a clause rather than adding a mechanism, and it restores the order SPEC:154 already states.
- Priority: High. Quality impact: Consistency +2, Testability +1.

## === ARCHITECTURE ANALYSIS ===

### B2 [MAJOR, blocking] WC-4's contract location is undefined for commands whose `--output` is a file or that have no output flag, and an acceptance check depends on it
- Where: SPEC:62 (WC-4: "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"), SPEC:87 and SPEC:90 (init-lite and tdd: `--output <file>`), SPEC:85 and SPEC:86 (cleanup-audit fixed `.claude-audit/` directory; index-repo with brief flag "none"), SPEC:200 (AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and requires a contract with `status: blocked`), SPEC:183 (7.2 step 4: `test -s <contract>`). A repo-wide search of the candidate finds no sentence that maps a file-valued `--output` to a contract directory.
- Grading check (PROMPTS:31): An implementer who follows WC-4 as written builds a contract at `<tdd --output value>/return-contract.yaml` (a path below a file) for tdd and init-lite, and has no coordinator-passed directory for cleanup-audit and index-repo, and that is wrong because the report path "known before dispatch" (SPEC:62) cannot be named, and AC-2.2 plus step 4 cannot pass for the tdd gate run as written. Two stated texts (WC-4 and SPEC:87,90) contradict, and an acceptance criterion cannot pass.
- Corroboration: the command definition used for this audit already separates the two, "`--report-dir <dir>` only (`--output` is file-valued)" (CMD:460); the same split is not in the spec. This is corroboration only; the spec's own evidence (SPEC:87,90) suffices.
- Expert: Cockburn (who reads the contract and from where), Newman (interface consistency), Whittaker (Zero/Empty Attack): I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62** (report known before dispatch) fails when **the output flag is a file or missing**. Concrete attack: coordinator dispatches `/sc:tdd "auth" --unattended --output docs/TDD_AUTH.md`; the gate resolves blocked; the command must write `docs/TDD_AUTH.md/return-contract.yaml`; `docs/TDD_AUTH.md` is not a directory and the coordinator was never told another path; `worker_done --report-path` carries nothing openable.
- Recommendation: state in WC-4, in one sentence, where the contract goes for the three shapes (directory-valued output flag, file-valued flag, no flag), or name one distinct directory flag for the contract. Rationale: the three shapes are all in section 3, so the sentence adds no new mechanism.
- Priority: High. Quality impact: Testability +2, Completeness +1.

### Follow-up candidates (Medium: warnings, never trigger a revision, never in the Reviser brief)

- **M1 (Fowler).** P1 gives gated commands an accepted `--unattended` flag with unspecified behavior until P2. SPEC:159 says "a no-op where a command has no gate" but is silent for the 15 P2 commands and the 3 P4 commands that do have a gate. Reading A: the flag is inert and the gate still prompts or posts. Reading B: the gate resolution is live in P1. For auggie-review, Reading A means `--unattended` still posts to GitHub with no prompt (INV-A:38, SPEC:100) until P2, against WC-9 (SPEC:67). Needs a guess, so Medium.
- **M2 (Nygard).** Retry and fresh-directory rule. WC-6 (SPEC:64) says a command with no resume flag "writes each run into a fresh output directory", but WC-4 (SPEC:62) makes the directory the coordinator's, and the brief list (SPEC:73) does not tell the coordinator to pass a new directory per `--retry-of` attempt. A retry with the same directory overwrites the first attempt for every row marked "fresh dir" (for example SPEC:99-111). AC-3.2 (SPEC:205) shows the sharper case: roadmap "starts fresh" over an existing `.session-memory.md`, discarding resumable state when a retry brief omits the resume flag. No acceptance check covers WC-6 at all (finding M3). Missing requirement, so Medium.
- **M3 (Wiegers, traceability).** (a) Worker-session rules WC-3, WC-5, WC-7 and WC-12 are owned by the "worker session" (SPEC:61,63,65,70), yet the list of what the brief carries (SPEC:73) names none of them, and the Orca preamble (CAPS:73) fixes only the outcome flag, not the blocked-to-failed or partial-to-succeeded map. Nothing says what binds the worker session to the map. (b) Section 7 has no check for WC-3 (ask), WC-6 (retry) or WC-12 (consumer_fenced), and WC-10 is checked only for pr-submit (SPEC:210). Missing requirement, so Medium.
- **M4 (Crispin-role, Whittaker).** AC-C5 (SPEC:176) and AC-0.3 (SPEC:193) use `grep -E '^-[^-]'` to prove edits are additive. A removed Markdown bullet `- text` appears in a diff as `-- text`, which the pattern skips, and the three-dot form `master...HEAD` sees only committed changes. Tested in the sandbox: `printf -- '-- bullet\n--- a\n-x\n' | grep -E '^-[^-]'` printed only `-x`. SA-1 and SA-4 (SPEC:146,149) lean on this check. Command files are Markdown and the command definition used here is full of `- ` bullets (CMD:44-47, 53-56), so a deleted bullet passes. Check is weaker than its claim, so Medium.
- **M5 (Fowler).** AC-C1 (SPEC:172) greps `src/superclaude/core` and requires empty output, but P0 adds `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md`, both in `core/` (SPEC:52,158,150), and SA-2 (SPEC:147) allows an Orca mention "inside the contract file". If either file writes a lowercase `orca orchestration ask`, AC-C1 fails; whether it does depends on wording the spec does not fix. Medium.
- **M6 (Adzic).** AC-2.2 (SPEC:200) expects `worker_done --outcome failed` for a gate run, but WC-3 (SPEC:61) lets the worker session "instead ask the coordinator once". A worker that takes the `ask` branch ends in a `question` message, not `worker_done` (step 3 waits for either, SPEC:182), so the check outcome depends on a choice the brief does not forbid. Medium.
- **M7 (Whittaker, Sentinel Collision and Zero/Empty).** Two rows of the boundary table: the spec never says what counts as the `--unattended` token (quoted prompt text containing the string; CMD:459 shows the real command resolves this with a "standalone argument token outside any quoted argument" rule), nor what happens with `--unattended` and no output location, nor what a coordinator-only command does with the token. D1(a) calls the flag "cannot misfire on a person" (SPEC:228); a quoted prompt can still misfire it. Missing requirement, so Medium.
- **M8 (Nygard).** WC-10 (SPEC:68) triggers on a call "longer than 5 minutes", caps waits at 4 minutes, and cites a 5-minute heartbeat cadence (CAPS:130); AC-4.3 (SPEC:210) fails any call over 240 s. A single call of 4.5 minutes satisfies the trigger sentence but fails the AC, and two such calls in a row exceed the cadence. The thresholds also appear in the Decisions table (SPEC:266) as 4 minutes only. Medium.
- **M9 (Wiegers).** WC-9 (SPEC:67) turns an outward action on "only through the command's own explicit flag". `/sc:task` EXEMPT `commit`/`push` run with no skill and no flag (INV-B:204), yet SPEC:121 (P2, not deferred to P4) says they are "refused unless authorized (WC-9)". There is no flag to authorize with. Medium.
- **M10 (Newman).** WC-11 (SPEC:69) forbids two workers writing the same file but assigns the duty to commands' default output paths. Commands that edit shared source (cleanup, improve, document inline mode, implement: SPEC:103,107,109,110) write the user's tree, and the brief list (SPEC:73) names only "the worktree placement"; CAPS:115 says workers share the current worktree by default. How the coordinator keeps write sets disjoint is not stated. Medium.
- **M11 (Wiegers).** WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62) while the Decisions table fixes `status` to four values and AC step 4 asserts membership (SPEC:183,262). The existing vocabularies are not listed (workflow lists `status` with unlisted values, INV-B:272). UNVERIFIED whether any existing value falls outside the set. Medium.
- **M12 (Cockburn).** brainstorm is "ready today" with only `--output` and no `--interactive` (SPEC:84), but INV-A:39 records an optional Wave 4 handoff into `sc-tasklist-protocol` or `task-builder`, and tasklist is a needs-change command in this same spec (SPEC:122). The brief list does not say to suppress the handoff. The default handoff value is not in the inventory, so UNVERIFIED; Medium.
- **M13 (Nygard).** The `--unattended` rule for reflect and tasklist reuses the headless auto-accept (SPEC:88,122,151). INV-B:109 describes that rule as auto-accept for auto-fixable registers, but the spec does not say what an auto-accepted remediation does to the tree, and the tasklist row does not resolve the `needs_human_decision` HALT that INV-B:209 records at `SKILL.md:1631`. WC-2 (SPEC:60) forbids any person-blocking step, so that HALT is an unresolved gate. UNVERIFIED either way; Medium.

## Panel notes: consensus and disagreements

- Consensus (Wiegers, Fowler, Newman): the decision in section 1 is supported by the inventories (E1-E6, SPEC:21-26; R1-R5, SPEC:33-37) and the evidence-strength section is candid about what is unproven (SPEC:41-45). The 10 / 27 / 6 split and the phase counts reconcile with the inventories (see Coverage).
- Consensus: the rejected-alternative argument R1 rests on a presumed enforcement site that the spec itself marks UNVERIFIED (SPEC:33, CAPS:103); this does not change the decision because R2-R5 stand without it.
- Disagreement (Whittaker and Fowler): Whittaker would grade M1 blocking because of the auggie-review posting window; Fowler holds that the window needs an implementer to ship P1 alone and read the flag as live, which is a guess, so it stays Medium under PROMPTS:31.

## Minor notes (never fail the review)

- N1. Dangling finding ids `[F1]`, `[F2]` in normative text (SPEC:182,194,195,196) refer to `review/spec-panel.md`, absent from the workspace.
- N2. `load` is "changed" yet gets no section: SPEC:76 says "Every changed command also gains the `## Unattended mode` section"; SPEC:195-196 exclude it (SPEC:112 "P1 (usage line only)").
- N3. SPEC:122 says the tasklist reflect fan-out is "inside Claude Code's nesting limit" (INV-A:14), while INV-B:210 and INV-B:314 record the same nesting as UNVERIFIED; the spec does not mention the disagreement between the inventories.
- N4. AC-2.4 (SPEC:202) compares `--jq length` counts; `gh api` returns one page (30 by default), so a PR with 30 or more reviews or comments can show equal counts after a new post.
- N5. 7.2 step 5 (SPEC:184) searches a transcript for the string `AskUserQuestion`; command text read into a transcript can contain the word, so the search can false-fail.
- N6. The D1 example (SPEC:228) gives `/sc:troubleshoot ... --output .dev/troubleshoot/login/`; the inventory names only a default directory for troubleshoot (INV-B:242), not an `--output` flag. UNVERIFIED.
- N7. SPEC:22 (E2) says a command run by a worker has "the same tools" as one a person runs; CAPS:161 and EVIDENCE only show both are top-level Claude sessions.
- N8. WC-7 (SPEC:65) lists the lifecycle messages as heartbeat, ask, check, worker_done; SPEC:114 also uses `escalation` (CAPS:75).
- N9. AC-0.4 (SPEC:194) leaves step 4 ambiguous: the pass list says steps "1-3 and 5-7", then says step 4 "uses the command's existing report file", but step 4's YAML assertion (SPEC:183) cannot parse a Markdown `REPORT.md`.
- N10. SPEC:120 says to "add `--output`" to spec-panel; the command definition used here already lists `--output <file>` (CMD:22-23) and `--report-dir` (CMD:460). `cmd/spec-panel.md` is not in the workspace, so UNVERIFIED whether INV-B:182 is stale.

## Next step for the coordinator

The session that ran this review would ask the user once whether to open an issue for the Medium findings M1-M13 and the minor notes; this run is a sandboxed worker with no user channel, so it asked nothing and created nothing. The coordinator should ask. This is a labelled first review of the whole document; a later scoped re-review cannot give whole-document assurance (CMD:262).

## Reviser brief

Blocking finding ids: B1, B2. Nothing else is in scope.
- Revise only text a blocking finding names: B1 names SPEC:159 and SPEC:195 (and the phase list at SPEC:162 only as the reference); B2 names SPEC:62.
- Add no rule, mechanism or section that B1 or B2 does not call for. Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. For B1 the intended repair is narrowing the P1 flag sentence and AC-1.1 to the commands outside P4. For B2 the intended repair is one sentence in WC-4 that names the contract location for a directory-valued output flag, a file-valued output flag, and a command with no output flag.
- Report the byte size of the candidate before (57973) and after, and the bytes added and deleted per finding id.
- Leave minor notes and Medium findings (M1-M13, N1-N10) alone, even if a brief says "apply all findings".
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
