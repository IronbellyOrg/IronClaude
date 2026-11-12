# Cross-Validation Report (Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339), read-only `/sc:sweep`
**Date:** 2026-11-07
**Analysis type:** cross-validation (checklist items 6, 7, 8)
**Depth tier:** Deep
**Fix authorization:** false (no research file edited)
**Assigned files:** `research/scope-03-cli-patterns.md` (201 lines), `research/scope-04-409-layout.md` (332 lines), `research/06-orca-open-questions.md` (183 lines)
**Input only:** `research/research-notes.md` (AMBIGUITIES 1-11 and C1-C12 treated as known conflicts and not re-reported)

[PARTITION NOTE: Cross-file checks limited to assigned subset plus research-notes.md. Full cross-file analysis requires merging all partition reports.]

Method: every finding below was re-checked against the cited source (repo files with Read/Grep, `git show 495eb96d:<path>`, and read-only `orca-ide ... --help` / `skills get` output). No state-changing Orca, ccsession, sweep or close command was run.

---

## 1. Contradictions Found (checklist item 6)

### Finding 1 (IMPORTANT): `agentWait` null is read two incompatible ways, and 06 hides an Orca-internal conflict

- **06:134** maps "`agentWait` null or absent, or liveness `unverifiable`" to "could not determine". **06:141** says "null/absent means 'not seen', never 'not waiting'" and tags it [CODE-VERIFIED].
- **Orca's own sources disagree with each other.** `orca-ide orchestration worker-show --help` line 16 says: "Null means Orca looked and found no wait. An absent field means it never looked ... A waiting worker is healthy, not failed." `[G:recovery]` lines 58-61 and `[G]` lines 159-160 say "a null `agentWait` ... is that same absence seen again", but they say it only about **stall proof** ("Absence never authorizes stop, abandon, retry, or release").
- **research-notes.md:187** uses "`agentWait` null" as an input to the **working** class. If 06:134 is applied, no worker can ever be classified "working", because every healthy worker reads null. The two files disagree on the main healthy path of the sweep.
- **06's [CODE-VERIFIED] tag on line 141 does not hold for the help text,** which says the opposite about null. 06 picked the guide's reading and did not record that the help disagrees.
- **Remediation:**
  - Record the help-vs-guide conflict as an open item in 06 and in synthesis.
  - Adopt a split rule. Null means "no wait observed" and is valid input for "working". Null is never stall proof and never proves "not waiting" for a stop decision. Absent means "could not determine".
  - Re-tag 06:141 as [CODE-CONTRADICTED] by the help text and [CODE-VERIFIED] by the guide.

### Finding 2 (IMPORTANT): #409's "request" is narrower than the sweep's "waiting on a person" class

- **#409:** `495eb96d:.dev/design/orca-observer-20261106/data-dictionary.md:12` defines a Request as an "Explicit synthetic human question, not inferred from any blocked status". The Shift Brief counts "policy frozen" among retained problems (`layouts/agent_focus.py:168`), separate from the human requests (`:164-167`). `data-dictionary.md:27` keeps policy frozen as its own dimension.
- **Sweep:** research-notes.md:186 puts all of these into one "waiting on a person" class:
  - `agentWait` non-null
  - `worker_status: blocked` with `blocked_question`
  - a Ruling halt
  - a frozen `/sc:implement` plan (`WORKER-CONTRACT.md:133-136`)
  - an unowned ready Task (`:129`)
- **scope-04** offers #409's layout as the model for the "Needs a human" section (skeleton at `scope-04-409-layout.md:264-304`). It does not say that #409 forbids deriving a request from a blocked status. The two files therefore disagree about what may appear in the report's first section.
- **Remediation:**
  - Split the top section into two lists:
    - (a) Explicit questions: non-null `agentWait`, `blocked_question` text, or a pending Orca `ask` once a non-consuming read is confirmed.
    - (b) Frozen or blocked by policy: still needs the person, but labelled as derived from status.
  - State the split in synthesis, so the plan never invents question text for a frozen plan.

### Finding 3 (IMPORTANT): one sweep class per session conflicts with #409's independent dimensions

- **#409's model:**
  - `README.md:39-41` sets the independence rules.
  - `DESIGN-CONTRACT.md:11` says "stale != failed" and "Worker result is not admission".
  - `data-dictionary.md:19-28` lists ten separate dimensions.
  - `concepts.md:29` says "admission is a subset, not another lifecycle bucket".
- **Sweep vocabulary:** research-notes.md:186-191 gives each session a single class, and those classes mix freshness, lifecycle and result into one value. For example, "stale evidence" falls under "could not determine" (:189), and "finished" is a lifecycle state.
- **scope-04's skeleton** (`:289`) has dimension columns and **no class column**. So scope-04 and research-notes describe two different report models, and neither file mentions the other model.
- **Remediation:**
  - Synthesis must choose one model. Recommended: keep scope-04's dimension columns and add the sweep class as a **derived** column.
  - Write a precedence rule, for example: needs-person > stalled > could-not-determine > working > finished > idle.
  - The rule must name the dimension values that produce each class, so that "stale" never becomes "failed".

### Finding 4 (IMPORTANT): scope-03's read-only proof covers local writes only, not Orca-side consumption

- **scope-03:99** says the `AssertionError` + `isolated_filesystem()` pattern is "Directly reusable to prove `/sc:sweep` writes nothing but its report" [CODE-VERIFIED].
- That pattern proves two things: patched Python entry points are never reached, and cwd-relative files are not touched. It cannot prove that a subprocess call to Orca leaves Orca's state unchanged.
- **06 shows that some Orca reads change state:**
  - Plain `check` marks messages read, and a bound Run replays the same Delivery until `--ack` drains it (`check --help` lines 4-5 and 37).
  - 06:164 [UNVERIFIED]: `worktree ps --agent-wait` and the `agentWait` probe may send something to the agent's terminal.
  - `inbox` and `--unread` have no documented read-marking behaviour (`inbox --help` has no note).
- So scope-03's claim conflicts with 06's findings: the "directly reusable" proof would still pass for a sweep that drains the coordinator's inbox.
- **Remediation:**
  - Add an **argv allowlist test** on the single Orca subprocess seam (the one-helper pattern scope-03 already names).
  - Allowed: `check --peek`, `check --all`, `worker-list`, `worker-show`, `worker-read`, and `worktree ps` without `--agent-wait` until 06 item 10 is resolved.
  - Forbidden: plain `check`, `--ack`, `--wait`, `reply`, `ask`, `send`, `inbox`, `--unread`, and `check --format`. `check --help:28` documents `--format` as a screenshot image format, while `:36` describes it as text rendering; 06 already flags that conflict.
  - Keep the fallback to contract-only file reads when Orca is unavailable.
  - Narrow scope-03:99 to "proves no local writes".

### Finding 5 (IMPORTANT): scope-04's skeleton columns do not match the dimension order it cites, and two columns have no data source

- **scope-04:308** says the table columns "follow the dimension order in data-dictionary.md:19-27" and tags this [CODE-VERIFIED].
- The skeleton at **scope-04:289** has `Lifecycle | Phase | Health | Freshness (age) | Result | Admission | Policy`. It **omits approval** (`data-dictionary.md:22`) and **evidence** (`:26`). It also stops at :27, while scope-04:327 cites the dimensions as :19-28, so tests/review (:28) is dropped as well.
- **Admission and Phase have no source among the sweep's inputs:**
  - `integration-gaps.md:11-16` lists the admission record as "Not established", and `data-dictionary.md:25` says admission is "Defined by an explicit fixture record, never inferred".
  - No research file names a worker-contract or Orca field that gives Phase (`:20`, work/review/queue/dependency).
- **Remediation:**
  - Add the missing dimensions, or state why each one is left out.
  - Name a concrete source field for every column that stays.
  - Print "not observed" for Admission and Phase until a source exists.
  - Re-tag scope-04:308 as "partly verified: the columns are a subset, in order".

### Finding 6 (MINOR): research-notes section B is stale against 06 on `check`

- **research-notes.md:171** says `agentWait` "is the only non-consuming wait signal found", and says no read path is known to list pending questions without consuming them.
- **06** now documents that `--peek` and `--all` do not mark messages read (`check --help` lines 6-7; `[G:messaging]` lines 26-27). Both are capped at 100 rows with no cursor (`check --help:37`).
- research-notes is input only and is not edited here. **Remediation:** synthesis must take the message-read facts from 06, not from research-notes section B, and keep 06's 100-row truncation rule (06:72).

### Finding 7 (MINOR): scope-04 did not trace #409's source ledger or previews

- `495eb96d:.../README.md:9` names a "source ledger" and `:44` cites `sources.json`. `PREVIEWS.md` also exists in the package tree. scope-04 read neither.
- scope-04 marks its "Not read: generated files" claim as partly [CODE-CONTRADICTED] (scope-04:331), but it does not name what generates those files. `git grep` for `PREVIEWS`, `index.html` and `sources.json` across `*.py` and the tests at 495eb96d found no match (rc=1), so no generator exists in the package's code.
- **Remediation:** read `sources.json` and `PREVIEWS.md`, or state that they were left out. Record that no generator was found, so the plan does not assume the previews can be regenerated.

### Finding 8 (MINOR): live `worker-list` evidence in #409 was not used by any assigned file

- `495eb96d:.../integration-gaps.md:5` says "A live bounded fleet observation returned explicit totalCount and truncation". That is direct evidence for research-notes gap G-A (the worker-list row schema and paging), which research-notes.md:244 rates Critical.
- None of scope-03, scope-04 or 06 cites it. 06 relies only on `worker-list --help` lines 19-22 for paging.
- **Remediation:** the G-A gap-fill (planned `research/05-orca-row-schema.md`) should cite this line, and check whether `totalCount` is in the `worker-list` JSON.

## 2. Verified claims (sample re-checked by this partition)

| # | Claim | File | Checked against | Verdict |
|---|---|---|---|---|
| 1 | `check --format` documented as a screenshot format and also as text rendering | 06 | `check --help:28`, `:36` | VERIFIED (06 correctly flags the conflict) |
| 2 | `check --peek`/`--all` show at most 100 rows, no cursor; `worker-list` pages with `page.nextCursor` | 06 | `check --help:3`, `:37`; `worker-list --help:3`, `:19-22` | VERIFIED |
| 3 | `ask` timeout default 600000, max 1800000 | 06 | `ask --help:24` | VERIFIED (this also resolves `orca-capabilities.md` UNVERIFIED item 2 for CLI 1.4.245) |
| 4 | Stall needs positive proof; absence never authorizes stop | 06 | `[G]:154-161`; `[G:recovery]:54-61`; `WORKER-CONTRACT.md:45` | VERIFIED |
| 5 | `agentWait` null means "not seen" | 06:141 | `worker-show --help:16` | CONTRADICTED by help, VERIFIED by guide (Finding 1) |
| 6 | Read-only proof pattern at `test_contract_status_cli.py:18-22`, `:44-66` | scope-03:99 | file read | VERIFIED (citation); scope of the claim OVERSTATED (Finding 4) |
| 7 | CLI groups registered at `main.py:551-561`, `__main__` guard at `:564` | scope-03:200 | `main.py` grep | VERIFIED |
| 8 | `_POST_REFRESH_ADDITIONS` at `test_routing_refresh.py:33`, asserted at `:648` | scope-03:200 | grep | VERIFIED |
| 9 | `sc-swarm-wizard-protocol/SKILL.md:7` `allowed-tools` with `Bash(uv run superclaude swarm *)` | scope-03:194 | grep | VERIFIED |
| 10 | #409 Attention Ledger does not sort; no omission count in wide views | scope-04 | `agent_focus.py:41-53`, `:156-169` | VERIFIED (both CODE-CONTRADICTED against #409's own contract, as scope-04 says) |
| 11 | Ten dimensions at `data-dictionary.md:19-28`; required semantics at `DESIGN-CONTRACT.md:11` | scope-04:327 | `git show 495eb96d:` | VERIFIED |
| 12 | Skeleton columns follow `data-dictionary.md:19-27` order | scope-04:308 | `data-dictionary.md:19-28` | CONTRADICTED (subset; Finding 5) |
| 13 | Request is an explicit question, never inferred from a blocked status | (not stated by scope-04) | `data-dictionary.md:12` | Source fact; omitted by scope-04 (Finding 2) |

## 3. Compiled gaps, deduplicated (checklist item 7)

| # | Gap | Source files | Severity | Remediation |
|---|---|---|---|---|
| G1 | `agentWait` null meaning conflicts between help and guide; the sweep cannot classify "working" under 06:134 | 06, research-notes C | IMPORTANT | Split rule (Finding 1); record the Orca conflict as an open item |
| G2 | "Waiting on a person" mixes explicit questions with status-derived blocks, against #409's request rule | scope-04, research-notes C, 06 Q1/Q4 | IMPORTANT | Two lists: explicit questions, policy-frozen or blocked (Finding 2) |
| G3 | Single class per session vs independent dimensions; no precedence rule | scope-04, research-notes C | IMPORTANT | Class as a derived column with a written precedence rule (Finding 3) |
| G4 | No test proves the sweep never consumes or drains Orca messages | scope-03, 06 | IMPORTANT | argv allowlist test on the Orca seam (Finding 4) |
| G5 | Skeleton drops approval, evidence and tests/review; Admission and Phase have no source | scope-04 | IMPORTANT | Source per column; "not observed" for unsourced ones (Finding 5) |
| G6 | Whether `worktree ps --agent-wait` / the `agentWait` probe writes to the agent's terminal | 06 item 10 | IMPORTANT | Exclude `--agent-wait` until a handler read or a test-only run settles it |
| G7 | Whether Orca sets `agentWait` for a worker blocked in `ask` (changes the "contract breach" reading) | 06 item 11 | IMPORTANT | Same gap-fill as G6; until then, report non-null `agentWait` as "waiting", not as a breach |
| G8 | Whether a question has been answered cannot be read without consuming | 06:38, Q2 | IMPORTANT (already tracked as research-notes G-B) | Report "answered: could not determine" |
| G9 | `uv run superclaude sweep` may fail outside a uv project (pipx install); the skill must also run in other projects | scope-03 OQ3 | IMPORTANT | Decide the call form (`superclaude sweep` on PATH, with `uv run` fallback) and test it |
| G10 | Message listing capped at 100 rows with no cursor | 06:72 | MINOR (06 already gives a rule) | Keep 06's "truncated at 100" rule in the plan |
| G11 | research-notes section B is stale on `check` | research-notes | MINOR | Synthesis uses 06 (Finding 6) |
| G12 | `sources.json` and `PREVIEWS.md` not read; no preview generator found | scope-04 | MINOR | Finding 7 |
| G13 | `integration-gaps.md:5` live worker-list evidence unused | all three | MINOR | Cite in the G-A gap-fill (Finding 8) |
| G14 | Lazy vs eager `__init__`; HOW-WE-WORK table placement; command vs skill `allowed-tools`; UTILITIES table test pin | scope-03 OQ1, OQ2, OQ4, OQ6 | MINOR | Plan decisions, no further research needed |

No CRITICAL gap was found in this partition. Research-notes' own Critical gaps G-A and G-B are outside this partition's re-rating and stay Critical there.

## 4. Depth Assessment (checklist item 8)

**Expected depth:** Deep (data flow traces, integration point mapping, pattern analysis).

| File | Depth achieved | Missing depth elements |
|---|---|---|
| scope-03-cli-patterns.md | Deep. Registration path, routing registries, test seams and skill call form are traced with line citations; 58 re-verified findings, 3 CODE-CONTRADICTED, 3 UNVERIFIED. Spot checks here matched. | No trace of how the read-only proof would cover subprocess side effects (Finding 4). The pipx call path is left UNVERIFIED (G9). |
| scope-04-409-layout.md | Deep. Layout code, fixtures and contract are read line by line at 495eb96d, including where #409's code breaks its own contract. | No mapping from each #409 dimension to a sweep data source (Finding 5); no comparison with the sweep class vocabulary (Findings 2, 3); `sources.json`/`PREVIEWS.md` not read (Finding 7). |
| 06-orca-open-questions.md | Standard to Deep. Every help and guide citation checked here was accurate, and the file states that it used help text only. | No handler or compiled-code read (the method `orca-capabilities.md` used for its numeric limits), so items 10 and 11 stay UNVERIFIED. The help-vs-guide conflict on null `agentWait` was resolved silently instead of reported (Finding 1). |

**Overall:** the evidence quality is Deep-tier. The shortfall is in integration mapping: the three files are each sound on their own but were not reconciled with research-notes section C or with each other.

## 5. Recommendations

1. Before synthesis, fix the report model: dimension columns plus a derived class column with a written precedence rule (G3), and two top sections, explicit questions and policy-frozen (G2).
2. Adopt the null/absent split for `agentWait` and record the Orca help-vs-guide conflict as an open item (G1).
3. Make the Orca argv allowlist test an acceptance criterion of the implementation plan, alongside the scope-03 local-write proof (G4). Exclude `--agent-wait` until G6 is settled.
4. Give every report column a named source field; print "not observed" where none exists (G5).
5. Decide the CLI call form for installs outside IronClaude (G9).
6. Use 06, not research-notes section B, for `check` semantics (G11). Cite `integration-gaps.md:5` in the G-A gap-fill (G13).

Severity count: 0 CRITICAL, 5 IMPORTANT findings (1-5), 3 MINOR findings (6-8); 9 IMPORTANT and 5 MINOR deduplicated gaps.

## Verdict: FAIL
