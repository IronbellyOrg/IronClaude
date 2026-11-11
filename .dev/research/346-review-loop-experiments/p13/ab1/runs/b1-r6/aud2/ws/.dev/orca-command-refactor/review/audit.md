review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review (`baseline: missing`: no `--re-review` or `--baseline` was given, so this is not a scoped re-review)
- candidate sha256: `e550dcb7fc3a3d867b7e5294799b7396379b1aa09607edb9890463612dc110e6` (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 290 lines, 62044 bytes)
- baseline sha256: none given
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full); grading per `command.md` Review Loop bullet 2
- panel (focus requirements: Wiegers lead, Adzic, Cockburn; focus architecture: Fowler lead, Newman, Hohpe, Nygard; Whittaker active in every panel, `command.md:83`)
- mode flags: not `--unattended`; `--iterations` ignored (one review)

## What I covered

Read in full: the candidate (lines 1-290), `README.md`, `command.md`, the review-loop prompts file. Checked against the only checkable evidence: `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md` (cited `INV-A`, `INV-B`, `CAPS`). Spot-checked 45 inventory/CAPS citations the spec makes (for example `CAPS:66-67`, `CAPS:80`, `CAPS:97-103`, `CAPS:115-117`, `CAPS:145-150`, `CAPS:155-161`, `INV-A:14,62,65,90,95-98,106,118,120`, `INV-B:272,285-286,289-301,311,320,323`); each says what the spec says it says. Rebuilt the 10 / 27 / 6 split from the two inventories: A = 5 ready + 13 needs-change + 3 coordinator-only (`commands-a.md` summary tables), B = 5 ready + 14 needs-change + 3 coordinator-only (`commands-b.md:289`), which sums to the spec's 10 / 27 / 6 (`spec:76`) and to the phase rows (P1 9, P2 11, P3 4, P4 3 = 27, `spec:99-125`, `spec:159-162`).

Not covered / UNVERIFIED: every citation to `src/superclaude/...`, `CLAUDE.md`, `.dev/codegraph-migration/...`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `Makefile`, `pyproject.toml`, `plugins/` (spec:11, :22-25, :52, :59, :62-70, :83-125 and the rest of section 3). The sandbox holds none of those files. The spec's claim that 11 locations were re-read and about 340 citations were independently checked (spec:11, :290) is also UNVERIFIED here. No part of the spec was run.

## === REQUIREMENTS ANALYSIS ===

### Finding F-1 (blocking) : Live-check step 4 cannot pass for workflow, which WC-4 says carries its status under another key
- severity: MAJOR, graded blocking (two stated texts contradict; an acceptance criterion cannot pass)
- experts: Wiegers (testability), Adzic (concrete example), Whittaker (Sentinel Collision Attack on the key `status`)
- Grading check: an implementer who follows the stated text as written builds a P1 workflow contract in which the four-value field is `worker_status` and the key `status` keeps workflow's existing values (spec:62: "a command whose existing `status` key uses other values, such as workflow's, writes the four-value field as `worker_status`"), and then runs the P1 acceptance check that asserts `d['status'] in {'succeeded','partial','failed','blocked'}` (spec:188). Those are wrong together because step 4 reads the key WC-4 says holds the other vocabulary, so a successful workflow run fails the assertion (or a failed run passes it by accident) and AC-1.2 (spec:201: "7.2 live check on each P1 command") cannot pass for workflow, which P1 edits (spec:159, :92).
- The same spec says the opposite one line earlier: WC-4 states that "WC-5 and 7.2 read [`worker_status`] in place of `status` for it" (spec:62), and step 3 matches `--outcome` to "the contract's `status` under WC-5" (spec:187). Step 4's literal command (spec:188) has no such substitution.
- Evidence: spec:62, :63, :92, :159, :187-188, :201. That workflow's current `status` vocabulary differs from the four values is the spec's own statement (spec:62); the inventory only records that workflow's contract has a `status` field that includes `failed` (`INV-B:272`) and does not list its other values, so the exact clash value is UNVERIFIED.
- Concrete attack (Whittaker, Sentinel Collision): before P1 workflow writes `status: <workflow-vocabulary value>`. After P1 it writes `status: <workflow value>` and `worker_status: succeeded`. Step 4 asserts on `status`; the key that carries the four-value contract is never read.
- recommendation: make step 4 (and step 3) read the same key WC-4 names, for example by stating "`worker_status` where present, else `status`", or drop the `worker_status` carve-out. Narrow, do not add a mechanism.
- priority: High. Quality impact: the P1 gate for workflow is unpassable as written.

### Findings below are Medium or minor and do not block (see follow-up candidates)

(No other requirements finding passed the grading check. Each Medium one below needs a guess about which reading an implementer picks, or is a requirement the document never states.)

## === ARCHITECTURE ANALYSIS ===

The architecture decision itself holds up. Orca on top, commands as units (spec:16), is backed by checkable lines: depth 1 refuses a nested `worker-start` (`CAPS:97-98`, spec:33), plain sessions must not send lifecycle messages (`CAPS:148`, spec:34), `worker_done` is bound to the dispatched pane (`CAPS:150`, spec:35), and Agent-tool subagents are not counted by the depth fence (`CAPS:155`, spec:24). The spec states its weak points itself (spec:41-45, UNVERIFIED items spec:277-289). Fowler/Newman/Hohpe/Nygard found no blocking architectural contradiction. Notes are listed as follow-up candidates.

## Guard Condition Boundary Table (hard gate, command.md:311-334)

Guards found: WC-1 fallback vs readiness limit; WC-10 wait split vs heartbeat cadence; WC-5 outcome mapping on report status; WC-4 output-location guard; R1 nesting depth. A class is left out only with its reason. Status OK/GAP; GAP rows are graded under the Grading check below and none other than F-1 reached blocking.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-1 prompt fallback | spec:59 | Typical | fallback 30 s, limit 60 s | true | within limit (EVIDENCE.md:45,56 via spec:59, UNVERIFIED file) | OK |
| WC-1 prompt fallback | spec:59 | Legitimate Edge Case | fallback 45 s | boundary | spec says "above about 45 s it fails again" (spec:59); WC-1 text sets 30 s only | OK (margin stated) |
| WC-1 prompt fallback | spec:59 | Zero/Empty | no fallback at all | false | fails at `agent_readiness` (spec:59) | OK |
| WC-10 single-call wait | spec:68 | Typical | 3 min call | split not needed | allowed | OK |
| WC-10 single-call wait | spec:68 | Legitimate Edge Case | 4 min < call <= 5 min | undefined | "longer than 5 minutes ... split into waits of at most 4 minutes" (spec:68): a 4-5 min call is neither required to split nor allowed to exceed the stated 4-minute split size | GAP (Medium, see M-8) |
| WC-10 single-call wait | spec:68 | Maximum/Overflow | eval timeout 3600 s (spec:68, cli-eval) | true | split into <= 4 min waits (spec:104) | OK |
| WC-5 outcome mapping | spec:63 | Zero/Empty | no report file | n/a | `--outcome failed` | OK |
| WC-5 outcome mapping | spec:63 | Sentinel Value Match | `status: partial` | true | `succeeded`, first sentence of body states `partial` (spec:63, :268) | OK |
| WC-5 outcome mapping | spec:63 | Legitimate Edge Case | workflow's own `status` value | key clash | WC-5 reads `worker_status`; 7.2 step 4 does not | GAP, blocking (F-1) |
| WC-4 output location | spec:62 | Zero/Empty | output flag given, brief names no location | true | writes nothing, replies in chat, WC-5 maps to `failed` (spec:62) | GAP (Medium, see M-6): contradicts "written ... including stops before any other output exists" in the same cell |
| WC-4 output location | spec:62 | One/Minimal | `--output <dir>` without `--unattended` | n/a | WC-2 says WC-4 applies only under `--unattended` (spec:60); SA-3 says written "or when the caller passes the new output flag" (spec:148) | GAP (Medium, see M-2) |
| R1 depth | spec:33 | Maximum/Overflow | depth 2 request | refused | `nested_worker_depth_exceeded`; call sites that enforce it are UNVERIFIED (spec:33, `CAPS:103`) | OK (stated UNVERIFIED) |
| R1 depth | spec:33 | Zero/Empty | depth setting malformed | falls back to 1 | `CAPS:97-101` | OK |

Left out: WC-1 One/Minimal and WC-10 One/Minimal (a 1-unit input has no meaning for a time threshold); R1 Sentinel Value Match (the depth number is not a sentinel).

Pipeline Dimensional Analysis: not triggered. The phases are an ordering, not a data pipeline with changing counts (command.md:353). The section 3 counts (10 / 27 / 6 = 43) do conserve, which I checked above.

## Whittaker attack findings (all non-blocking unless marked)

1. Sequence Attack on the rollout (spec:73, :159-162): see M-1. The flag is accepted in P1 for every command (spec:159) and the brief carries `--unattended` "from P1 on" (spec:73), while gates and outward defaults are only turned off in P2-P4 (spec:160-162). Medium.
2. Divergence Attack on `--output` without `--unattended`: see M-2.
3. Accumulation Attack on retry: `blocked` and `failed` both map to `--outcome failed` (spec:63). A worker's own `failed` does not count toward the three-failure circuit breaker (`CAPS:80`, spec:268), so repeated blocked re-dispatch is not stopped by Orca; the spec stops it by rule (spec:73 "not re-dispatched without a new answer"). OK, no finding.
4. Zero/Empty Attack on `load`: spec says load needs no report and is "not its own Task" (spec:112, :270) while the section 3.2 heading counts it among 27 "needing a change" (spec:94). Note only (N-1).

## Follow-up candidates (Medium and minor; none triggers a revision)

| id | grade | finding | evidence |
|----|-------|---------|----------|
| M-1 | Medium | Rollout window. P1 makes every command in 3.1 and 3.2 accept `--unattended` as "a no-op where a command has no gate" (spec:159); 2.3 tells the coordinator to put `--unattended` in the brief "from P1 on" (spec:73); WC-9 says outward defaults are off "under `--unattended`" (spec:67). Gated commands (auggie-review posts to a PR by default, task commits, spec:100, :121) only get their behaviour in P2-P4 (spec:160-162), and P1 reads "a no-op" only for ungated commands. Nothing says the coordinator must not dispatch a gated command with `--unattended` before its phase. Requirement never stated, so Medium. | spec:67, :73, :100, :121, :159-162 |
| M-2 | Medium | `--output` given without `--unattended`: WC-2 limits WC-4 to `--unattended` (spec:60); SA-3 lets the contract appear "when the caller passes the new output flag" (spec:148); section 3.2 adds `--output` to 9+ commands (spec:99-125). | spec:60, :62, :148 |
| M-3 | Medium | AC-1.2 runs each P1 command "with `--unattended --output <dir>`" (spec:201), but index-repo and cleanup-audit take no output directory in the spec (spec:85-86: fixed `.claude-audit/` and repository root) and WC-4 places index-repo's contract at the repository root (spec:62). The check is not runnable as written for those two. | spec:62, :85-86, :159, :201 |
| M-4 | Medium | The `--unattended` vs `--interactive` vocabulary differs: WC-2 says the command stops `blocked` (spec:60), section 3.2 says `--interactive` is "refused" (spec:103, :110, :118). Same event, two outcomes. | spec:60, :103, :110 |
| M-5 | Medium | tasklist: "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit" (spec:122) cites `INV-A:14`, which gives the three-layer rule but no count for tasklist subagents spawning reflect's own reviewers and adversarial advocates (reflect Tier 2, `INV-B:107-115`). The layer count is asserted, not shown. UNVERIFIED. | spec:122, `INV-A:14`, `INV-B:36` |
| M-6 | Medium | WC-4 says the contract is written "on success, failure, blocked and partial outcomes, including stops before any other output exists" and, in the same cell, that with no output location "the command writes nothing" (spec:62). The second is an intended exception mapped to `failed`, but 7.2 step 4 `test -s <contract>` (spec:188) will then fail on that case. | spec:62, :188 |
| M-7 | Medium | AC-3.2 sets up `<dir>/.session-memory.md` in the same `<dir>` it passes as `--output` and expects a fresh start (spec:210); WC-6 and 2.3 say a non-resuming re-run gets a new directory so the first attempt is not corrupted (spec:64, :73). The test setup contradicts the rule it sits under. | spec:64, :73, :210 |
| M-8 | Medium | WC-10 threshold wording: split anything "longer than 5 minutes" into waits of "at most 4 minutes" (spec:68); a single call of 4-5 minutes is covered by neither half. Decision table at spec:271 explains the 4 minute margin only. | spec:68, :271 |
| M-9 | Medium | WC-2 lists WC-8 among the "worker-session rules" that apply to every worker run (spec:60) while the WC-8 row names its owner as Command (spec:66). | spec:60, :66 |
| N-1 | minor | Section 3.2 is headed "Needs a change (27)" and counts `load`, whose row says "none" (spec:94, :112). | spec:94, :112 |
| N-2 | minor | Unexplained tags throughout the requirements text (`L1`, `L2`, `R4`, `R9`, `L13`, ...; spec:59-73, :147, :172) are not defined in the spec; they look like revision-trace ids and mean nothing to an implementer. | spec:59-73, :147, :172 |
| N-3 | minor | README:31 (no commits, pushes, PRs in this run) is cited as support for the production policy that commands take no outward action by default and that git needs user authorization (spec:67, :133). README:31 binds this run's workers only. | spec:67, :133, `README.md:31` |
| N-4 | minor | SA-4/AC-C5 guard only command files for additive edits (spec:149, :176); the skill files that carry most gates (section 3 evidence column) have no equivalent check. | spec:149, :176 |
| N-5 | minor | The spec claims a 340-citation independent check and 11 re-reads (spec:11, :290); nothing in the sandbox can confirm it. UNVERIFIED. | spec:11, :290 |

Question for the user (once per loop, `command.md:260`): open an issue for the Medium and minor follow-up candidates above? This run cannot ask; no issue was created.

## Quality scores (0-10, informational)

Clarity 8, Completeness 8, Testability 7 (F-1 and M-3 reduce it), Consistency 7.

## Coverage line

whole-document first review: candidate read in full; src, CLAUDE.md, .dev/codegraph-migration and EVIDENCE.md citations UNVERIFIED (not in sandbox).

## Reviser brief

Blocking finding ids: F-1.

Reviser contract (restated from `command.md` Review Loop bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone.

F-1 names: spec:62 (the `worker_status` sentence of WC-4), spec:187 (step 3) and spec:188 (step 4 command).

verdict: FAIL
