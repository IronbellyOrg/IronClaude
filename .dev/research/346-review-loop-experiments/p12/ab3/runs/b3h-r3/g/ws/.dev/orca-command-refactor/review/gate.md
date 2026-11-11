review: 1 of 3

# Gate review: orca-worker-contract-spec (spec-panel critique, focus requirements, architecture)

- Command: `/sc:spec-panel --mode critique --focus requirements,architecture` (GATE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md`, run as a first review of a complete document; fresh context, no prior report of this loop)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate sha256: `d7b701458ccab1292a94ee6f2c84881cfc91dbf20d522f329d407123b072388d`
- Baseline: not given (not applicable to a full-document gate review)
- Reviewer model: claude-haiku-5-5
- Grading: FIRST-REVIEW grading check (blocking needs a sentence that holds with no further assumption; otherwise Medium)
- Result: 2 blocking findings, 12 Medium follow-up candidates, 4 notes. Edits: none.

Citation convention: `spec:N` = line N of the candidate; `INV-A:N` = `inventory/commands-a.md:N`; `INV-B:N` = `inventory/commands-b.md:N`; `CAPS:N` = `inventory/orca-capabilities.md:N`. All are relative to `.dev/orca-command-refactor/`. Every such line was read in this review.

## Coverage

- Read in full: `command.md`, `README.md`, the GATE / FIRST-REVIEW prompt file, the candidate (all 285 lines), `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`.
- Citation check against the workspace: the candidate's `INV-A`, `INV-B` and `CAPS` citations were checked against the inventory lines they name. Checked and matching the cited topic: CAPS:44-45, 46, 52, 58-61, 63-64, 66-67, 72-74, 76-77, 79-80, 84-92, 97-103, 113, 115-116, 130, 145-151, 155-161, 178, 180, 186-188; INV-A:14, 35, 38, 42, 44, 51, 55, 96, 118; INV-B:31, 36, 38, 41, 43-45, 92, 109, 112, 272, 292, 294, 296, 311, 314, 317, 323. Two citations are weak: spec:215 cites CAPS:12-13 for the coordinator following Orca's guide, and those lines are the guide source-key table (see N-4).
- Count check: 10 ready + 27 needing a change + 6 coordinator-only = 43, which matches INV-A:3 (21 commands) plus INV-B:3 (22 commands), and the per-inventory summaries at INV-A:73 (5/13/3) and INV-B:278 (5/14/3). Section 3 rows match the inventories' verdicts.
- UNVERIFIED in this sandbox (not checkable here, so not graded as wrong): every `src/superclaude/...` path, `.dev/codegraph-migration/...`, `.dev/evals/...`, `.dev/research/...`, `/opt/Orca/...`, the `~/.claude/skills/...` and `~/.claude/agents/...` files, the repository `CLAUDE.md` and `HOW-WE-WORK.md`, the external Claude Code docs URL, and the F-xx finding IDs (see M-12).
- Not applicable: this invocation has no standalone `--unattended` token, so `WORKER-CONTRACT.md` is not read and no unattended-mode gate applies to this run.

## Blocking findings

### GR-B1 (requirements): WC-6 is contradicted by the init-lite row

- Stated text, WC-6: "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output. A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean." (spec:64)
- Stated text, init-lite row: the "Resume (WC-6)" column reads "Re-run overwrites its marked report", and "Small fix" reads "None" (spec:81, spec:87). The inventory confirms the overwrite: "a marked report is overwritten on re-run (S:66)" (INV-A:55).
- Grading sentence: an implementer who follows the candidate as written leaves init-lite unchanged, because its row lists no fix. A `--retry-of` run reuses the Task's brief and so its `--output` path (CAPS:116 gives the retry form), so the retry overwrites the first attempt's `context-audit.md`. That is wrong because WC-6 forbids a retry from corrupting the first attempt's output and allows only resume or a fresh directory, and init-lite is neither.
- Consequence: a retried init-lite worker destroys the earlier audit that the coordinator may already have read.
- Required fix (for the reviser, not made here): either give init-lite a fresh-directory or resume rule in the §3.1 row, or state in WC-6 an explicit exception for re-runs that overwrite a marked report, with the reason.

### GR-B2 (requirements): the P0 smoke runs need two different command lines

- Stated text, §2.3: "For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required" (spec:73). §7.2 step 1 builds each Task from "the brief per section 2.3" (spec:180).
- Stated text, §3.1 and P0: the ten ready commands "run as workers now if the brief uses the stated flags" (spec:79), and the brief columns for those commands name no `--unattended` flag (spec:83-92). P0 runs `/sc:troubleshoot`, `/sc:workflow --handoff none` and `/sc:adversarial --output <dir>` "before any command changes" (spec:158). `--unattended` is first accepted in P1 (spec:159) and P2 for troubleshoot (spec:160).
- AC-0.4 requires the §7.2 live check on exactly those three commands, "each run directly by the worker" (spec:194).
- Grading sentence: an implementer who follows §2.3 and §7.2 step 1 as written must put `--unattended` on the P0 `/sc:troubleshoot` command line, where the flag does not exist yet, and an implementer who follows P0 and §3.1 must leave it off, so the same AC-0.4 run cannot satisfy both texts. That is wrong because the acceptance check for P0 has no single valid brief.
- Required fix (for the reviser): state in §2.3 that `--unattended` is added only for commands that accept it, or state that P0 briefs omit it and why §2.3 is waived for P0.

## Medium findings (follow-up candidates; none fails the review)

- M-1 (requirements, spec:147, spec:172): SA-2 forbids any `orca` or `orca-ide` command in a command, skill or agent. AC-C1 matches only `orca(-ide)? (orchestration|worktree|terminal|agent)`, so `orca status`, `orca open` or `orca-cli` pass the check while SA-2 is violated. SA-2 itself is clear, so this is a weak check, not a contradiction.
- M-2 (architecture, spec:63, spec:73): WC-5 maps a FAIL audit and a `partial` run to `--outcome succeeded`. Orca then settles the Task as completed (CAPS:77), and the ready view releases dependents (CAPS:86, CAPS:88). The spec's §2.3 tells the coordinator to open the report but never to gate dependent Tasks on `status`. The partial-to-succeeded rule is justified at spec:263, but not the dependent-gating gap.
- M-3 (requirements, spec:60-61): WC-2 (c) says a gate resolves as "blocked" and stops, while WC-3 says the session "may instead ask the coordinator once" and re-invoke the command "with the answer as a flag". No rule says which path a worker takes, and WC-3 does not say which flags an answer may supply per gate beyond the WC-9 and D2 limits.
- M-4 (requirements, spec:100): the auggie-review row says "posting returns only with an explicit `--post-pr` in the brief", yet its "Other required change" column says "none". INV-A:38 names only `--no-post-pr` as the off switch and records posting as the default. Whether `--post-pr` exists is UNVERIFIED here (src not readable). If it does not exist, the row must list adding it as a change.
- M-5 (requirements, spec:104, spec:200): the cli-eval row requires "the safety flags in the brief, else blocked", but no flag is named, and INV-A:44 names none. AC-2.2 (spec:200) tests `run --unattended` with no `--suite` and no safety flags. An implementer cannot tell which flags to require.
- M-6 (requirements, spec:114, spec:238-247): the pr-submit row says its outward actions are "per open decision D3". D3 (spec:238-242) decides only whether pr-submit runs as a worker. Outward authorization is decided by D4 (spec:244-247). WC-9 (spec:67) turns outward defaults off, so the cross-reference is wrong.
- M-7 (acceptance, spec:194, spec:184): AC-0.4 says the "no Agent-tool wrapper" property is "verified in the step-5 transcript". Step 5 (spec:184) checks only for an `AskUserQuestion` call. No stated check exercises WC-7 (spec:65).
- M-8 (requirements and evidence, spec:122, spec:45): the tasklist row says Stage 10.5's nested reflect fan-out is "inside Claude Code's nesting limit" and cites INV-A:14, which relies on the external docs (UNVERIFIED here). INV-B:314 (UNVERIFIED items 1 and 8) says nested spawning and who answers the remediation offer are unknown. spec:45 says no proven limit exists. The row presents as settled what the candidate itself lists as open.
- M-9 (requirements, spec:88, spec:122): under `--unattended`, reflect's `--remediate` "follows the existing headless auto-accept rule". INV-B:109 says that rule "auto-accepts for auto-fixable registers and skips the gates". The candidate does not say what an auto-accepted remediation may do, and WC-2 (a) needs a documented default. The rule was also keyed to `claude --print` (spec:280, UNVERIFIED 9), so this flag would newly trigger it.
- M-10 (sequencing, spec:159, spec:195): P1 says the WC-4 contract lands for the P1 commands, and the contract for gate commands lands in P2 (spec:160). AC-1.1 requires every §3.1-3.2 command except `load` to have a `## Unattended mode` section that "names return-contract.yaml" in P1. So P2-P4 commands name a contract that does not yet exist.
- M-11 (architecture, spec:105, spec:220): the cli-portify row leaves a hard-coded `src/superclaude/examples/...` template path in an installed skill, and records only a checkout restriction. The repository rule against hard-coded `src/superclaude` paths in installed primitives is in the coordinator's `CLAUDE.md`, which is outside this sandbox (UNVERIFIED here). §8 item 8 (spec:220) keeps in scope defects that stop a worker, and this one does, so the candidate should either fix it or say why not.
- M-12 (traceability, spec:52, spec:62, spec:73, spec:147, spec:172, spec:195, spec:234): the candidate cites finding IDs F-01 through F-05 and F-19. Their source review is not in this workspace (the README output table lists `review/spec-panel.md`, which is absent), so these citations are UNVERIFIED. F-05 (spec:52, spec:195) and F-19 (spec:62) both describe the `load` exclusion.

## Notes (not graded)

- N-1: several "ready-as-worker" verdicts rest on items the inventories mark UNVERIFIED, for example the workflow `git add` question (INV-B:317, item 4) and the reflect "not headless" assumption (INV-B:314, item 2). spec:88 and spec:92 do not carry these caveats.
- N-2: the §3 row set matches both inventories' verdicts and the 43-command total (see Coverage).
- N-3: the finding IDs F-01 to F-05 and F-19 are cited at spec:52, :62, :73, :147, :172, :195 and :234; they belong to the UNVERIFIED group in M-12, and F-03 appears at spec:83, :92 and :116. The reviser should trace all of them to the same source.
- N-4: spec:215 cites CAPS:12-13 for the coordinator following Orca's guide. Those lines are the source-key table, which supports the point only loosely.

## Follow-up candidates

M-1 through M-12 above. The coordinator asks the user once per loop whether to open issues for them; none is created here.

## Reviser brief

Blocking ids: GR-B1, GR-B2.

Restated per the review loop, step 6: revise only the text that GR-B1 and GR-B2 name; add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (M-1 to M-12, N-1 to N-4) are not in this brief and must not be revised under it.

Gate loop, per the GATE prompt: because this is a gate review with open blocking findings, one REVISE (with these ids) and one RE-REVIEW would follow, and a FAIL after that escalates to the user. Brief clauses overridden: none.

verdict: FAIL
