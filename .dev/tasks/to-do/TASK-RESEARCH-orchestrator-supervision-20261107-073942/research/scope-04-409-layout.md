# Scope 04: #409 observer layout for a static report

**Scope:** commit 495eb96d, `.dev/design/orca-observer-20261106/` (read via `git show`)
**Status:** Complete
**Date:** 2026-11-07

---

Citation format: `PKG/<file>:<line>` means `495eb96d:.dev/design/orca-observer-20261106/<file>:<line>`. Line numbers come from `git show 495eb96d:<path> | cat -n`.

## Files read (495eb96d:path, line count)

| File | Lines | Why read |
|---|---|---|
| `PKG/README.md` | 52 | Package index; set 2 lists Attention Ledger and Shift Brief (README.md:15) [CODE-VERIFIED] |
| `PKG/DESIGN-CONTRACT.md` | 17 | The "Required semantics" rules (DESIGN-CONTRACT.md:10-11) and layout interface [CODE-VERIFIED] |
| `PKG/data-dictionary.md` | 50 | Entities, independent state dimensions, measurements, missing-evidence rules [CODE-VERIFIED] (line count 50) |
| `PKG/integration-gaps.md` | 28 | "Proposed only" boundary and missing-data behavior [CODE-VERIFIED] (line count 28) |
| `PKG/concepts.md` | 51 | One-line intent per design: Attention Ledger (:23), Shift Brief (:31), compact-mode rules (:35-40) [CODE-VERIFIED] |
| `PKG/PLAN.md` | 73 | Shared data/display contract (:32-38), width rules (:56-57) [CODE-VERIFIED] |
| `PKG/QA.md` | 51 | What was and was not verified (:31-37) [CODE-VERIFIED] (the list runs to :38) |
| `PKG/canvas.py` | 122 | `header()`, `footer()`, `selected_summary()`: the header/freshness convention lives in code [CODE-VERIFIED] (canvas.py:73-81, :117-122) |
| `PKG/fixtures.py` | 122 | Fixture schema (field names and values actually emitted); `metrics()` derived counts [CODE-VERIFIED] (fixtures.py:11-87, :98-111) |
| `PKG/layouts/agent_focus.py` | 183 | `attention()` (:41-53), `shift()` (:156-169), `narrow()`/`listbox()` (:13-24), DESIGNS table (:171-183) [CODE-VERIFIED] |
| `PKG/agent-focus/exports/116/attention-ledger.txt` | 42 | Rendered example rows [CODE-VERIFIED] (line count 42) |
| `PKG/agent-focus/exports/80/attention-ledger.txt` | 42 | Rendered narrow example [CODE-VERIFIED] (line count 42) |
| `PKG/agent-focus/exports/116/shift-brief.txt` | 42 | Rendered example [CODE-VERIFIED] (line count 42) |
| `PKG/agent-focus/exports/80/shift-brief.txt` | 42 | Rendered at 80 (no narrow branch) [CODE-VERIFIED] (line count 42) |
| `PKG/tests/test_designs.py` | grep only | Footer and SYNTHETIC assertions (:87-88) [CODE-VERIFIED] |
| `PKG/render.py` | grep only | Gallery inspector: filter is inspector-only, count line (:98, :113, :116) [CODE-VERIFIED] |
| `PKG/agent-focus/manifest.json` | grep only | Slugs `attention-ledger` (:32), `shift-brief` (:144) [CODE-VERIFIED] |

Not read: PNG/SVG/ANSI/PDF/HTML artifacts, `layouts/group_a.py`, `layouts/group_b.py`, `sources.json`, `PREVIEWS.md`, `index.html`, scenario JSON (all generated from `fixtures.py`, see fixtures.py:114-122). [CODE-CONTRADICTED, partial] fixtures.py:114-122 (`write_fixtures`) writes only `fixture.json` and `scenarios/*.json`. `layouts/group_a.py` and `layouts/group_b.py` are hand-written layout source that render.py imports (render.py:21), not generated files, and render.py does not mention `sources.json`, `PREVIEWS.md` or `index.html` (grep of render.py, re-verified 2026-11-07). Only the scenario JSON half of the claim holds.

File naming: no file is literally called "fixture schema" or "required semantics". The fixture schema is code in `PKG/fixtures.py:11-87` (serialized to `PKG/fixture.json`, fixtures.py:116). The required semantics are the `## Required semantics` section of `PKG/DESIGN-CONTRACT.md:10-11`. Attention Ledger and Shift Brief are implemented in `PKG/layouts/agent_focus.py` and exported under `PKG/agent-focus/exports/{160,116,80}/`. [CODE-VERIFIED] (fixtures.py:11, :87, :116; DESIGN-CONTRACT.md:10-11; agent_focus.py:41, :156)

## Header and freshness convention (exact example lines, source path:line)

Every design calls `frame()` = `c.header(name,f,m); c.footer()` (PKG/layouts/agent_focus.py:9). [CODE-VERIFIED]

Header code (PKG/canvas.py:73-77): [CODE-VERIFIED] (`def header` at :73, body :74-77)
- Row 1: `"◈ "+title.upper()` left, `"SYNTHETIC · READ ONLY"` right (canvas.py:74-75). [CODE-VERIFIED]
- Row 2: `f"{len(f['orchestrators'])} owners / {m['total']} sessions / {m['worktrees']} mapped trees"` (canvas.py:76). [CODE-VERIFIED]
- Row 3: `f"08:00 UTC | msgs {messages.coverage} | workers {workers.age_s}s | checks {checks.age_s//60}m"` (canvas.py:77). [CODE-VERIFIED] (paraphrased: the code spells `f['sources']['messages']['coverage']` etc.)

Exact rendered example (PKG/agent-focus/exports/116/attention-ledger.txt:2-4): [CODE-VERIFIED]
```
  ◈ ATTENTION LEDGER                                                                       SYNTHETIC · READ ONLY
  8 owners / 80 sessions / 80 mapped trees
  08:00 UTC | msgs partial | workers 4s | checks 14m
```

Footer code (PKG/canvas.py:78-81), rendered (PKG/agent-focus/exports/116/attention-ledger.txt:41-42): [CODE-VERIFIED]
```
  j/k select · tab pane · / filter · enter evidence · p hold view
  LOCAL FIXTURE · source coverage is not fleet-wide assurance
```

Field semantics:
- "sessions" = `m['total']`, current (non-historical) sessions only (PKG/fixtures.py:99-103). Historical are counted separately as `m['historical']` (fixtures.py:103; data-dictionary.md:10). [CODE-VERIFIED]
- "mapped trees" = distinct worktree IDs referenced by current sessions, not inventory (`m['worktrees']` vs `m['inventory_worktrees']`, PKG/fixtures.py:104; data-dictionary.md:11). Unmapped sessions counted as `m['unmapped']` (fixtures.py:105). [CODE-VERIFIED]
- Source records carry `id`, `observed_at`, `age_s`, `coverage` (PKG/fixtures.py:14-18). Coverage values used: `complete fixture`, `partial`, `stale` (fixtures.py:14-18), `unavailable` (source-loss variant, fixtures.py:76). A test pins `age_s` = as_of minus observed_at (PKG/tests/test_designs.py:37). [CODE-VERIFIED]

Rules:
- "Header prints scope/freshness." (PKG/DESIGN-CONTRACT.md:11) [CODE-VERIFIED]
- "Header retains scope/freshness; decision, owner and affected scope never disappear." (PKG/PLAN.md:57) [CODE-VERIFIED]
- "Global counts must name scope and collection completeness; a selected filter must state its denominator." (PKG/integration-gaps.md:24) [CODE-VERIFIED]
- "Every export says SYNTHETIC / READ ONLY." (PKG/data-dictionary.md:3); asserted by PKG/tests/test_designs.py:87. [CODE-VERIFIED]

Caveats for reuse:
- The `08:00 UTC` clock is a hardcoded literal (canvas.py:77), not read from `f['as_of']` (fixtures.py:13). A real report must print its actual observation time. [CODE-VERIFIED]
- Only three of five sources reach the header (messages coverage, workers age, checks age); `cost` and `resources` do not (canvas.py:77 vs fixtures.py:17-18). [CODE-VERIFIED]
- The fixture `scope` object `{"host","expected_hosts","collection"}` (fixtures.py:21) is never printed, although DESIGN-CONTRACT.md:11 says the header prints scope. The only "scope" in the header is the owner/session/tree counts. [CODE-VERIFIED] (canvas.py:73-77 reads no `f['scope']`)
- The key-hint footer row is TUI-only (asserted by test_designs.py:88). The second footer row ("source coverage is not fleet-wide assurance", canvas.py:81) is a semantic disclaimer a static report can keep. [CODE-VERIFIED]

## Attention Ledger: columns, order, sort rule, retention rule ("seen is not resolved"), example rows (path:line)

Identity: slug `attention-ledger`, question "Which human questions remain unanswered?", omits "Resource telemetry" (PKG/layouts/agent_focus.py:174; PKG/agent-focus/manifest.json:32). Intent: "Spacious age-ranked question ledger and ownership rail. What is still waiting for a human? | Resources omitted; seen/delivered is not answered" (PKG/concepts.md:23). [CODE-VERIFIED]

Wide layout (width >= 116), PKG/layouts/agent_focus.py:44-53: [CODE-VERIFIED]
- Left heavy panel `OPEN HUMAN QUESTIONS` (:45). One block per request, fields in this order (:47-49): [CODE-VERIFIED]
  1. age `"{age_min:02} MIN"`
  2. `question` (bold)
  3. `"{requester} requests / {owner}"`: requesting orchestrator, then human decision owner
  4. `"Affected: " + ", ".join(affected)`: stable session IDs
- Right panel `SEEN IS NOT RESOLVED`: big count `len(f['requests'])` labelled "observed questions" (:51-52). [CODE-VERIFIED]
- Right listbox `RETAIN CONTEXT`, the seven facts a question keeps until closed (:53): "original question", "original age", "acting owner", "requesting orchestrator", "affected stable IDs", "source coverage", "explicit closure evidence". [CODE-VERIFIED]

Narrow layout (width < 116), :43 via `narrow()` (:22-24): header; `selected_summary` of the first request (PKG/canvas.py:117-122: question, `Owner {owner} | {n} sessions | {age}m observed`, `Evidence {evidence}`); then listbox `SELECTED SIGNALS` of `qlines(f)` = `"{id} {age_min:>2}m  {question}"` (agent_focus.py:11) plus "Questions stay until explicit resolution." and "No reply observed is not delivery failure." (:43). [CODE-VERIFIED]

Sort rule:
- Documented: "age-ranked" (PKG/concepts.md:23). [CODE-VERIFIED]
- [CODE-CONTRADICTED, partial] No sort in code; it iterates `f['requests']` in fixture order (agent_focus.py:46). The fixture is built oldest first, ages 45, 20, 10 (PKG/fixtures.py:50-53), so exports only look age-ranked. A static report must sort explicitly, oldest first, to honor concepts.md:23. Tie-break is unspecified.

Retention rule ("seen is not resolved"):
- Panel title "SEEN IS NOT RESOLVED" (agent_focus.py:51). [CODE-VERIFIED]
- "Questions stay until explicit resolution." / "No reply observed is not delivery failure." (agent_focus.py:43). [CODE-VERIFIED]
- "seen/delivered is not answered" (concepts.md:23). [CODE-VERIFIED]
- Request records carry `state: "unanswered observed"` (PKG/fixtures.py:55); closure is a separate explicit event, `kind: "resolved"`, "Prior docs question explicitly closed" (fixtures.py:63). [CODE-VERIFIED]
- "selecting a record does not acknowledge any message" (PKG/render.py:98). [CODE-VERIFIED]
- "Source loss does not resolve questions" (PKG/integration-gaps.md:24). [CODE-VERIFIED]
- A request is an "Explicit synthetic human question, not inferred from any blocked status" (PKG/data-dictionary.md:12). [CODE-VERIFIED]

Example rows, wide (PKG/agent-focus/exports/116/attention-ledger.txt:9-12, 17-20, 25-28): [CODE-VERIFIED] (blank padding rows :10, :18, :26 dropped in the excerpt)
```
 ┃  45 MIN     Choose schema compatibility policy
 ┃             O01 requests / Human operator
 ┃             Affected: S001, S011, S021, S031
 ┃  20 MIN     Confirm deployment window
 ┃             O02 requests / Human operator
 ┃             Affected: S002, S012
 ┃  10 MIN     Name the release reviewer
 ┃             O03 requests / Human operator
 ┃             Affected: S003, S013
```
Narrow (PKG/agent-focus/exports/80/attention-ledger.txt:7-9, 14-18, 37): [CODE-VERIFIED]
```
   Choose schema compatibility policy
   Owner Human operator | 4 sessions | 45m observed
   Evidence demo:messages/Q01
 │ Q01 45m  Choose schema compatibility policy
 │ Q02 20m  Confirm deployment window
 │ Q03 10m  Name the release reviewer
 │ Questions stay until explicit resolution.
 │ No reply observed is not delivery failure.
 │ 5/5 lines shown
```

Gaps: the wide view prints neither the request `id` nor its `evidence` reference (agent_focus.py:47-49); the narrow view and Shift Brief do (agent_focus.py:11, :165-167). The wide view has no bound on the request count (`y=8+i*8`, :47) and no omission count; tests only exercise the fixture's three requests (fixtures.py:50-53), so more than about four requests is untested at 42 rows. [CODE-VERIFIED] (agent_focus.py:11, :46-49, :165-167; fixtures.py:50-53)

## Shift Brief: sections and order (path:line)

Identity: slug `shift-brief`, question "What must the next human know?", omits "Raw transcripts" (PKG/layouts/agent_focus.py:182; manifest.json:144). Intent: "Large human-question count, short narrative and explicit unverified footer. ... Raw logs omitted; handover is not an assurance of completeness" (PKG/concepts.md:31). [CODE-VERIFIED]

Sections in order (PKG/layouts/agent_focus.py:156-169): [CODE-VERIFIED]
1. Header and footer (:158). [CODE-VERIFIED]
2. Heavy panel `HANDOVER / OBSERVED ATTENTION` (:159): [CODE-VERIFIED]
   - big count `len(f['requests'])` + "QUESTIONS NEED A HUMAN" (:160)
   - `"Messages "+messages.coverage+"; this is not an all-clear."` (:161)
   - first request's question (:162)
3. Per-request blocks, three lines each (:164-167): `"{id} / {age_min}m / {owner}"`, `question`, `"Affects " + ", ".join(affected) + " | " + evidence`. [CODE-VERIFIED]
4. Retained-problem line: `"{failed} failed reports retained / {stale} stale / {frozen} policy frozen"` (:168). [CODE-VERIFIED]
5. Boundary line: "Inspection only. Existing tools and humans retain every operational decision." (:169). [CODE-VERIFIED]

Rendered (PKG/agent-focus/exports/116/shift-brief.txt:9, 11, 13, 19-21, 37-38): [CODE-VERIFIED]
```
  ┃   ███             QUESTIONS NEED A HUMAN
  ┃   ███             Messages partial; this is not an all-clear.
  ┃   ███             Choose schema compatibility policy
     Q01 / 45m / Human operator
     Choose schema compatibility policy
     Affects S001, S011, S021, S031 | demo:messages/Q01
     8 failed reports retained / 5 stale / 1 policy frozen
     Inspection only. Existing tools and humans retain every operational decision.
```

Notes:
- No narrow branch (no `c.w<116` test in agent_focus.py:156-169); the 80-column export is the same layout clipped (PKG/agent-focus/exports/80/shift-brief.txt:38 ends "operational d…"). [CODE-VERIFIED]
- Shift Brief lists no sessions and no worktrees; it is questions first plus three counts. Neither Attention Ledger nor Shift Brief models "every session and worktree". Per-session and per-worktree inventory in #409 lives in other designs (Outcome Ledger rows `"{id} {owner}  {result or 'no report'}  {admission}"`, agent_focus.py:21; Worktree Atlas and Fleet Quilt in set 1, concepts.md:7, :9, not read here). [CODE-VERIFIED] (agent_focus.py:41-53, :156-169 list no sessions or worktrees; Fleet Quilt concepts.md:7, Worktree Atlas concepts.md:9)

## Data dictionary: entities and independent state dimensions, with allowed values (path:line)

Preamble: "All fields below belong to this offline design fixture. They are NOT undocumented Orca API names. Every export says SYNTHETIC / READ ONLY." (PKG/data-dictionary.md:3) [CODE-VERIFIED]

Entities (PKG/data-dictionary.md:7-15) with fixture fields (PKG/fixtures.py):

| Entity | Dictionary text (data-dictionary.md line) | Fixture fields (fixtures.py line) |
|---|---|---|
| Orchestrator | O01..; name and mission; "Illustrative owner, not a live coordinator binding" (:9) | `id, name, mission` (:19) [CODE-VERIFIED] |
| Session | S001..; owner ID and optional worktree ID; current counted separately from historical (:10) | `id, owner, worktree, lifecycle, phase, health, approval, freshness, age_s, result, admission, evidence, policy, revision, check_revision, tests, review, report, cost_usd, cost_window, cpu_pct, rss_mib, retry_count, retry_source, historical, label, timeline` (:30-43) [CODE-VERIFIED] |
| Worktree | W001..; branch, base, head, paths; inventory separate from mapped (:11) | `id, branch, base, head, dirty, paths, conflict, policy` (:45-47); `conflict` always "not established" (:47) [CODE-VERIFIED] |
| Request | Q01..; requester, human owner, affected session IDs; not inferred from blocked status (:12) | `id, question, owner, requester, age_min, affected, evidence, state` (:54-55) [CODE-VERIFIED] |
| Dependency | E01..; from/to owner, reason, affected sessions; declared only (:13) | `id, from, to, reason, sessions, evidence` (:58-60) [CODE-VERIFIED] |
| Event | stable id + monotonic seq; dedup by id, latest seq kept, shown in seq order (:14) | `id, seq, kind, text, ref` (:61-64); kinds `new, worsened, resolved, unchanged`; dedup `normalize_events` (:90-95) [CODE-VERIFIED] |
| Source | demo:workers/messages/checks/usage; coverage, observation time, age (:15) | `id, observed_at, age_s, coverage` for workers, messages, checks, cost, resources (:14-18) [CODE-VERIFIED] |

Independent state dimensions (PKG/data-dictionary.md:17-28):

| Dimension | Allowed values | Rule (quoted) | Line |
|---|---|---|---|
| lifecycle | running / settled / unknown | "Settlement does not admit a result." | :19 [CODE-VERIFIED] |
| phase | work / review / queue / dependency | "Phase is not health or percentage complete." | :20 [CODE-VERIFIED] |
| health | no issue observed / failed result / unknown | "Stale is handled separately." | :21 [CODE-VERIFIED] |
| approval | none observed / human decision observed | "A dependency wait does not imply approval." | :22 [CODE-VERIFIED] |
| freshness | fresh / stale, with age in seconds | "A stale pass cannot establish current readiness." | :23 [CODE-VERIFIED] |
| result | succeeded / partial / failed / null | "report outcomes, not transport events" | :24 [CODE-VERIFIED] |
| admission | admitted / not admitted | "never inferred from settlement, packet completeness or passing tests" | :25 [CODE-VERIFIED] |
| evidence | complete packet / partial packet | "Completeness means inspectable, not accepted." | :26 [CODE-VERIFIED] |
| policy | frozen / not frozen | "Frozen work remains inert; the gallery cannot lift it." | :27 [CODE-VERIFIED] |
| tests/review | null = unavailable; fixture emits tests `passed`/`failed`/null, review `recorded`/null (fixtures.py:37-38) | "Tests are tied to check_revision and must match current revision to count as current evidence." | :28 [CODE-VERIFIED] |

Fixture-only values: request `state` = "unanswered observed" (fixtures.py:55); worktree `dirty` boolean (fixtures.py:46). The approval dimension is set to "human decision observed" on every session a request affects (fixtures.py:56-57); "human decision observed" therefore means "a human question is open for this session", not "a human approved it". [CODE-VERIFIED]

Measurements (PKG/data-dictionary.md:32-40): cost_usd window 07:00-08:00 UTC, "Null is not zero" (:34); cpu_pct (:35); rss_mib (:36); retry_count "No terminal-output inference" (:37); request age_min "Oldest observed only when messages coverage incomplete" (:38); affected count "Set union, not sum of overlapping requests" (:39, implemented fixtures.py:102, :111); timeline 20 buckets x 3 min, "a gap is missing observation, not idle time" (:40). [CODE-VERIFIED]

Missing evidence (PKG/data-dictionary.md:50): "Unknown values remain unknown. An unavailable source retains explicit unavailable coverage; last-known fixture data cannot be presented as current confirmation. No all-clear, ready-to-merge, resource leak, dangerous worktree or proven Git-conflict inference is authorized by this dataset." [CODE-VERIFIED]

## Required semantics (each rule, quoted short, path:line)

From `PKG/DESIGN-CONTRACT.md:11` (single paragraph; each item is a sentence of that line): items 1-10 all [CODE-VERIFIED] against DESIGN-CONTRACT.md:11.
1. "All fixture values synthetic." [CODE-VERIFIED]
2. "Worker result is not admission." [CODE-VERIFIED]
3. "Dirty != dangerous; stale != failed; overlap != conflict; partial cost subtotal != total spend; tokens != progress." [CODE-VERIFIED]
4. "Evidence flags must use current revision equality." [CODE-VERIFIED]
5. "Do not show approval/dispatch/retry/merge actions, even greyed. Navigation only." [CODE-VERIFIED]
6. "Handle messages coverage unavailable vs partial." [CODE-VERIFIED]
7. "Header prints scope/freshness." [CODE-VERIFIED]
8. "Narrow views retain first human decision + owner + affected scope/freshness; use selected_summary helper if needed." [CODE-VERIFIED]
9. "Show omission counts when limited." [CODE-VERIFIED]
10. "Data model is proposed fixture schema, never Orca API schema." [CODE-VERIFIED]

Supporting statements elsewhere:
- "Lifecycle settlement, report status, acceptance, current tests and human approval are independent." (PKG/README.md:39) [CODE-VERIFIED]
- "Dirty is not dangerous, stale is not failed, overlap is not a proven merge conflict, and an inspectable evidence packet is not admitted." (PKG/README.md:40) [CODE-VERIFIED]
- "Spend is a measured subtotal with coverage and time window. Unknown cost does not become zero." (PKG/README.md:41) [CODE-VERIFIED]
- "Unknown values remain null/unknown, never zero or false." (PKG/PLAN.md:34) [CODE-VERIFIED]
- "Derived affected counts use set unions." (PKG/PLAN.md:36) [CODE-VERIFIED]
- "Use stable IDs, declared relationships and evidence references, not inferred joins from display names." (PKG/PLAN.md:33) [CODE-VERIFIED]
- "Imported evidence is inert. Sanitize ESC/CSI/OSC, C0/C1 controls, carriage returns and bidi controls before any renderer" (PKG/PLAN.md:38); implemented in `sanitize()` (PKG/canvas.py:10-17), tested with the `injection` variant (fixtures.py:85-86). [CODE-VERIFIED]
- "Color carries semantic status plus text markers; stale and frozen must not use failure semantics." (PKG/PLAN.md:54); "Labels retain meaning without color." (PKG/QA.md:13). Relevant to Markdown: meaning must be in words, not color. [CODE-VERIFIED]
- "Source loss does not resolve questions, fail sessions, unlock a policy freeze or authorize retries." (PKG/integration-gaps.md:24) [CODE-VERIFIED]
- "Workspace co-location alone is not ownership." (PKG/integration-gaps.md:12) [CODE-VERIFIED]
- "The design never uses worker_done alone as report validation or admission." (PKG/integration-gaps.md:7) [CODE-VERIFIED]
- Missing outcomes: "The shared ledger now says not observed unless a result exists." (PKG/QA.md:23); "missing test outcomes say unknown" (PKG/QA.md:27). [CODE-VERIFIED]
- Empty result: "No matching records. This is not an all-clear." (PKG/render.py:116); empty-state test (PKG/tests/test_designs.py:58). [CODE-VERIFIED]
- Historical records: "Historical records are named separately." (PKG/data-dictionary.md:46) [CODE-VERIFIED]
- Events: dedup by id, keep latest seq, display in seq order (PKG/data-dictionary.md:14; fixtures.py:90-95; test test_designs.py:55). [CODE-VERIFIED]

## Narrow-view and omission rules (path:line)

Narrow-view rules:
- "Narrow views retain first human decision + owner + affected scope/freshness" (PKG/DESIGN-CONTRACT.md:11). [CODE-VERIFIED]
- "116 must rearrange, 80 must simplify to selected detail." (PKG/DESIGN-CONTRACT.md:14) [CODE-VERIFIED]
- "narrow uses selected-detail views and pagination, not tiny type. Header retains scope/freshness; decision, owner and affected scope never disappear." (PKG/PLAN.md:57) [CODE-VERIFIED]
- "At 80, selected question/owner/affected scope and header freshness stay visible; secondary inventory is bounded with omission counts and remains accessible in the gallery inspector." (PKG/concepts.md:36) [CODE-VERIFIED]
- Implementation: in agent_focus.py the switch is `c.w<116` (e.g. :43), and `narrow()` = header + `selected_summary` + listbox (:22-24). `selected_summary` shows the first request's question, `Owner ... | N sessions | Nm observed`, and `Evidence ...`, or "No requests in this fixture; source coverage still matters." when none (PKG/canvas.py:117-122). [CODE-VERIFIED]

Omission rules:
- "Show omission counts when limited." (PKG/DESIGN-CONTRACT.md:11) [CODE-VERIFIED]
- "No clipped actionable fields or unaccounted omissions." (PKG/PLAN.md:66) [CODE-VERIFIED]
- "list omission counters now explicitly count text lines" (PKG/QA.md:27). [CODE-VERIFIED]
- Implementation: `listbox()` prints `f"{shown}/{len(lines)} lines shown"` on its last row (PKG/layouts/agent_focus.py:17); rendered "5/5 lines shown" (PKG/agent-focus/exports/80/attention-ledger.txt:37), "7/7 lines shown" (PKG/agent-focus/exports/116/attention-ledger.txt:37). [CODE-VERIFIED]
- Outcome Ledger narrow variant adds an explicit total: `f"{len(rows)} total report records; inspector has all."` (agent_focus.py:107). [CODE-VERIFIED]
- Filter denominators: gallery prints `"{n} inspector records / {N} global records (historical included if present). Overview not filtered."` (PKG/render.py:113); tested by test_filter_denominators (PKG/tests/test_designs.py:56-57). Overview counts stay global (PKG/data-dictionary.md:46). [CODE-VERIFIED]
- Long values: clipped by display width with "…" (or "~" in ASCII), full value available in the inspector (PKG/canvas.py:19-29; PKG/concepts.md:38). A static Markdown report has no inspector, so it should not clip IDs at all. [CODE-VERIFIED] (the last sentence is a recommendation, not a source claim)

[CODE-CONTRADICTED] The wide Attention Ledger (agent_focus.py:46-50) and Shift Brief (agent_focus.py:164-167) loop over all requests with no limit and no omission count, which breaks DESIGN-CONTRACT.md:11 when requests exceed the screen. Untested because the fixture always has three requests (fixtures.py:50-53) or zero (empty variant, fixtures.py:84).

## What is proposed only (not an Orca API) and must not be treated as a contract

- "The fixture schema, derived metrics, display buckets, source identifiers and navigation interactions are local design constructs." (PKG/integration-gaps.md:20) [CODE-VERIFIED]
- "Data model is proposed fixture schema, never Orca API schema." (PKG/DESIGN-CONTRACT.md:11) [CODE-VERIFIED]
- "They are NOT undocumented Orca API names." (PKG/data-dictionary.md:3) [CODE-VERIFIED]
- "Source-to-dashboard schema is proposed; fixture fields are not asserted Orca API fields." (PKG/QA.md:32) [CODE-VERIFIED]
- Source ids `demo:workers`, `demo:messages`, `demo:checks`, `demo:usage`, `demo:resources` and evidence refs like `demo:messages/Q01`, `demo:evidence/S00x/report.txt` are synthetic (PKG/fixtures.py:14-18, :38, :55). [CODE-VERIFIED]
- ID formats O01/S001/W001/Q01/E01/D01 (PKG/data-dictionary.md:9-14) are fixture conventions, not Orca identifiers. [CODE-VERIFIED]
- Not established by #409 (PKG/integration-gaps.md:9-16): complete non-consuming message enumeration beyond a 100-row CLI view (:11); authoritative mission/owner/task/session/worktree joins across hosts (:12); a coordinator admission record and revision-pinned verification feed (:13); complete cost/resource telemetry (:14); durable event replay (:15); native deep-link formats (:16). [CODE-VERIFIED]
- Not verified: "No capacity, latency, operational correctness or live Orca integration benchmark is claimed." (PKG/README.md:52); five-second readability is a target, not measured (PKG/QA.md:35). [CODE-VERIFIED]
- Renderer is Python/Pillow prototype, not production; Charm stack is only a "leading production candidate" (PKG/README.md:48). [CODE-VERIFIED]
- The package is unmerged (branch commit 495eb96d). Nothing in it is on master; any field names a sweep borrows are a choice by the sweep, not a dependency on a contract. [CODE-VERIFIED] (seed-brief.md:44 names the unmerged branch `docs/409-orca-dashboard-designs` at 495eb96d; 495eb96d is not an ancestor of origin/master and the package path is absent from master, re-verified 2026-11-07)

What a static report CAN safely reuse: the semantic rules (independence of dimensions, unknown stays unknown, seen is not resolved, set-union counts, omission counts, scope/freshness header, no actions). What it must NOT treat as fixed: field names, ID formats, source ids, the 3-minute timeline buckets, the 08:00 clock. [CODE-VERIFIED] (each rule is cited and tagged in the sections above; timeline buckets data-dictionary.md:40)

## Minimal Markdown skeleton a static report could follow (derived; mark as DERIVED)

DERIVED. Not in the #409 package. Built only from the sections above: header (canvas.py:73-77), Shift Brief order (agent_focus.py:156-169), Attention Ledger fields and retained context (agent_focus.py:47-53), state dimensions (data-dictionary.md:17-28), omission/denominator rules (DESIGN-CONTRACT.md:11; render.py:113), footer disclaimer (canvas.py:81).

```markdown
# Orchestrator sweep: <worktree-tree root>
READ ONLY · observed <YYYY-MM-DD HH:MM UTC>

Scope: <N> owners / <N> current sessions / <N> mapped worktrees (<N> worktrees in inventory, <N> unmapped sessions, <N> historical listed separately)
Sources: <source> <coverage> <age> | <source> <coverage> <age> | ...

## Waiting on a person: explicit questions (<N> open)
Messages coverage: partial (Orca questions are not enumerated; sources are return contracts and worker-show agentWait). This is not an all-clear.

| ID | Age | Question | Requested by | Decision owner | Affected | Evidence |
|---|---|---|---|---|---|---|
| ... sorted oldest first ... |

Questions stay until explicit resolution. Seen is not resolved. Answered: could not determine. No reply observed is not delivery failure.
Distinct affected sessions: <N> (set union, not a sum)

## Waiting on a person: frozen or blocked by policy (<N>, derived from status, not questions)
| Session | Reason (Ruling halt / frozen plan / foreign ready Task) | Evidence |
|---|---|---|

## Retained problems
<N> failed reports retained / <N> stale / <N> policy frozen

## Sessions (<shown>/<total> shown)
| Session | Owner | Worktree | Class (derived) | Lifecycle | Phase | Health | Approval | Freshness (age) | Result | Admission | Evidence | Policy | Tests/review |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
Unknown values print "unknown"; missing results print "not observed".

## Worktrees (<shown>/<total> shown)
| Worktree | Branch | Base | Head | Dirty | Mapped sessions | Policy |
|---|---|---|---|---|---|---|
Dirty is not dangerous. Shared paths are not a proven conflict.

## Historical sessions (<N>)
...

---
Inspection only. Existing tools and humans retain every operational decision.
Source coverage is not fleet-wide assurance.
```

Choices made in the skeleton that #409 does not dictate (flag for the plan):
- Question table puts `ID` and `Evidence` columns in; the wide Attention Ledger omits them (agent_focus.py:47-49) but Shift Brief carries both (:165-167). [CODE-VERIFIED] (cited facts only; the choice stays DERIVED)
- Session and worktree tables have no #409 equivalent in the two designs read; columns follow the dimension order in data-dictionary.md:19-27. [Partly verified: in the original skeleton the columns were a subset of the dimensions, in order (approval :22, evidence :26 and tests/review :28 were missing); gate fix B-14 added those three, so the Sessions table now carries all ten dimensions of data-dictionary.md:19-28 in order, plus the derived Class column] (the choice stays DERIVED)

### Gate fix B-11, B-12, B-14, B-28 (2026-11-07): how the skeleton maps the sweep's data

**One vocabulary (B-28).** Class names are the canonical set of `research-notes.md` Section C: waiting on a person, working, stalled (proved), fenced, finished, could not determine, idle. The skeleton uses no other class names.

**Two kinds of "waiting on a person" (B-11).** #409 defines a Request as an "Explicit synthetic human question, not inferred from any blocked status" (`495eb96d:.dev/design/orca-observer-20261106/data-dictionary.md:12`) and keeps policy separate ("policy: frozen / not frozen", `:27`; the Shift Brief counts "policy frozen" apart from requests, `layouts/agent_focus.py:164-168`). The skeleton therefore splits the top section: (a) explicit questions (non-null `agentWait`, `blocked_question` text; a pending `ask` only once a non-consuming read is confirmed, see 06 Gap 17) and (b) frozen or blocked by policy, labelled "derived from status, not questions". No question text is ever written for a (b) row.

**Model choice (B-12).** Dimensions stay independent columns, as #409 requires (`README.md:39-41`, `DESIGN-CONTRACT.md:11`, `data-dictionary.md:19-28`). The sweep class is one extra **derived** column, computed by the precedence of `research-notes.md` Section C (1 contract read first, 2 stalled (proved), 3 fenced, 4 waiting on a person, 5 working, 6 finished, 7 could not determine; idle only for person-started sessions). The class never overwrites a dimension: a stale row keeps Freshness "stale" and Health as observed, and its class is "could not determine", never "failed".

**Question and requester cells per fallback source (B-12).** #409's request record has a requester and a question (`data-dictionary.md:12`); the sweep's sources do not all carry them:

| Source | Question cell | Requested by | Decision owner | Evidence cell | Section |
|---|---|---|---|---|---|
| `return-contract.yaml` `worker_status: blocked` + `blocked_question` (WC-3/WC-4) | the `blocked_question` text | the worker's command and Task | unknown | contract path | (a) |
| non-null `observation.agentWait` (worker-show) | unknown (agentWait carries only its evidence type: hook, prompt-text or title, `worker-show --help` line 16) | worker handle (`assigneeHandle`) | unknown | `agentWait` evidence type | (a) |
| pending `ask` | not shown: no read path (G-B) | - | - | - | none |
| Ruling halt / frozen `/sc:implement` plan (`WORKER-CONTRACT.md:133-136`) | none (policy, not a question) | - | - | contract and ledger paths | (b) |
| foreign ready Task (`task-list --ready`, `WORKER-CONTRACT.md:129`) | none | - | - | Task id | (b) |

**Which classes reach which view (B-12).** The Attention Ledger equivalent ("explicit questions") holds only (a) rows. The Shift Brief count line holds: failed reports retained (finished rows with Result failed), stale (rows whose Freshness is stale) and policy frozen ((b) rows). Every class, including working, stalled (proved), fenced, finished, could not determine and idle, appears in the Sessions table's Class column; stalled (proved) and could not determine are also listed under Retained problems.

**Source field per column (B-14).**

| Column | Source | Value when no source |
|---|---|---|
| Session | Orca Task / Dispatch id from `worker-list`; transcript uuid for a person-started session | - |
| Owner | Run id (`run-list` / `worker-list --run`); "person" for a person-started session | unknown |
| Worktree | Orca `terminal.worktreePath`; transcript cwd for a person-started session | unknown |
| Class (derived) | `research-notes.md` Section C precedence | could not determine |
| Lifecycle (:19) | Orca `projection.outcome` and `stage.detail` (`settled` -> settled, else running) | unknown |
| Phase (:20) | none among the sweep's inputs | not observed |
| Health (:21) | return contract `worker_status: failed` -> failed result; liveness `unverifiable` -> unknown | unknown |
| Approval (:22) | candidate: `gate-list` gate `status` for the session's Task (`07-gate-gap-fill.md` Section B); value mapping [UNVERIFIED] | not observed |
| Freshness (:23) | Orca `evidence.liveStatus` and `observedAt` (`lc16-show-4.json:140-144`); transcript mtime for a person-started session | unknown |
| Result (:24) | return contract `worker_status` succeeded / partial / failed; `blocked` prints null (the class says waiting on a person) | not observed |
| Admission (:25) | none: "never inferred" (`:25`), no admission record (`integration-gaps.md:13`) | not observed |
| Evidence (:26) | DERIVED: contract `report_path` and every `artifacts` path exist -> complete packet, else partial packet | not observed |
| Policy (:27) | frozen test at `WORKER-CONTRACT.md:133` (contract + ledger) | not observed |
| Tests/review (:28) | none: no revision-pinned check feed (`integration-gaps.md:13`) | null (unavailable) |
- "SYNTHETIC" is dropped from the banner because a sweep reports real data; "READ ONLY" is kept (canvas.py:75). [CODE-VERIFIED] (cited facts only; the choice stays DERIVED)

## Open questions

1. Sort tie-break for the needs-a-human list: concepts.md:23 says "age-ranked" but code has no sort (agent_focus.py:46). Oldest first is implied; tie-break (by ID? by affected count?) is unspecified.
2. Where does a static sweep get "human questions"? #409 uses explicit request records (data-dictionary.md:12) and says complete non-consuming message enumeration is not established (integration-gaps.md:11). If the sweep cannot enumerate questions completely, the header must say messages coverage is partial or unavailable (DESIGN-CONTRACT.md:11). **Answered for the design (gate fix B-17):** Orca question enumeration is not established (06 Gaps 17-18: whether `check --all` returns `run:<id>` rows, which end of the 100-row cap is kept, and the `compatibilityAck` side effect are [UNVERIFIED]), so the sweep reports Orca questions as "could not determine", takes its explicit questions from the contract fallbacks (`blocked_question`, non-null `agentWait`) and prints "Messages coverage: partial" in the header.
3. What counts as "explicit closure evidence" (agent_focus.py:53) for a real session? #409 only models a `resolved` event in the fixture (fixtures.py:63).
4. Should the sweep print every source's coverage (five in the fixture) or only the three the header prints (canvas.py:77 vs fixtures.py:14-18)? Recommend all, since integration-gaps.md:24 asks global counts to name collection completeness.
5. Scope line: DESIGN-CONTRACT.md:11 says the header prints scope, but the fixture `scope` object (host, expected_hosts, collection; fixtures.py:21) is never rendered. A sweep over "one worktree tree" should print that root path as its scope.
6. Omission bound for a static file: #409 bounds lists by screen rows (agent_focus.py:15-17). A Markdown file has no height limit; decide whether to list everything (no omission) or cap and print `<shown>/<total>`.
7. Approval semantics: the fixture sets approval to "human decision observed" on sessions an open request affects (fixtures.py:56-57), which reads like "approved". The sweep should decide whether to keep that label or use a clearer one such as "human question open".
8. #409 is unmerged (495eb96d). If its layout changes before merge, which version does the sweep follow? Recommend pinning to the commit in the sweep's spec and noting it.

## Summary

- Header convention: title + READ ONLY; `<owners> owners / <sessions> sessions / <mapped> mapped trees`; `<clock> | msgs <coverage> | workers <age>s | checks <age>m` (PKG/canvas.py:73-77). Clock is hardcoded; scope object is not printed. [CODE-VERIFIED]
- Attention Ledger: per question age, question, requester / owner, affected IDs; count panel "SEEN IS NOT RESOLVED"; seven retained-context facts (PKG/layouts/agent_focus.py:44-53). "Age-ranked" is documented but not coded. [CODE-VERIFIED] (the "not coded" half is the [CODE-CONTRADICTED, partial] sort finding above)
- Shift Brief: count + "not an all-clear" coverage line, per-question blocks (id / age / owner, question, affects | evidence), then failed/stale/frozen counts, then "Inspection only" line (agent_focus.py:156-169). [CODE-VERIFIED]
- Ten independent state dimensions with closed value sets (PKG/data-dictionary.md:19-28); ten required-semantics rules (PKG/DESIGN-CONTRACT.md:11). [CODE-VERIFIED]
- Omission rule "`shown/total` lines shown" exists only in `listbox()` (agent_focus.py:17); the wide ledger and Shift Brief do not apply it. [CODE-VERIFIED] (the gap is the [CODE-CONTRADICTED] omission finding above)
- Everything about field names, IDs and sources is proposed only (integration-gaps.md:20; DESIGN-CONTRACT.md:11). [CODE-VERIFIED]
- Neither design lists every session and worktree; the sweep's inventory tables are DERIVED, not inherited. [CODE-VERIFIED] (agent_focus.py:41-53, :156-169 render requests and counts only)
- Verification 2026-11-07 (Step 2.4): every file:line citation re-checked against `git show 495eb96d:` stdout and seed-brief.md. 0 line numbers corrected; 3 findings [CODE-CONTRADICTED] (sort rule partial, wide-view omission count, and the "Not read" generated-files claim partial, the last one new); 0 [UNVERIFIED]; every other finding [CODE-VERIFIED]. The DERIVED skeleton keeps its DERIVED label.
