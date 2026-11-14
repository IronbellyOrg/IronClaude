# Round 1 statement: advocate for variant 2 (proposal B, embed the JSON in the one report)

- Debate: Q9 (should the sweep's JSON ever be kept, and how), sc:adversarial Mode A, depth quick, Round 1
- Advocate: B (variant-2-original.md)
- Date: 2026-11-14
- Evidence re-read this session: `report.py:530-695`, `commands.py:268-281`, `test_cli_contract.py:1460-1481`, `test_readonly.py:285-314`, design `:33-35`, `:62-63`, `:125-153`, `:325-347`, `:558-563`, `.gitignore:254-257`, merged-requirements `:196-225`, `:399-402`, `:534-545`, `:616-619`, ADJ `:129-134`, `:344-362`, `:777-779`.

## 1. Position summary

B's lasting idea is sound: if the sweep's machine facts are ever kept, putting them inside the one dated report keeps NFR-001 ("a sweep adds exactly one report file") true and avoids a sidecar file. But B as written has two verified defects: it puts the block after the `Report complete` marker, which a pinned test forbids, and its fence is not protected against backticks in worker-written text. It also builds a store before any reader exists. I argue that B should be kept as the preferred storage form that A's Phase 2 tries first, not adopted now.

## 2. Steelman of each opposing variant

**A (not now; caller capture first; relax NFR-001 only if needed).** A is the spec's own recommended answer and default (merged-requirements `:536`; ADJ `:779`). It changes nothing in a newly reviewed tool, and it keeps PR #539 inside A-004's "no JSON key and no sidecar" limit. It also leaves the field list and retention to the first real reader, as ADJ A-001 (`:361`) says: "v2 names its field list first". Caller capture is cheap and already fits the output. The stdout JSON is printed only after the commit point and carries `report_path` (design `:563`; `commands.py:275-278`), so a caller that saves stdout gets the facts plus a pointer to the matching report, with no producer change. A also has the only explicit trigger ("a named reader ... needs stored sweep facts"), so SW-11 cannot drift.

**C (never, as a standing rule).** C is the most decisive answer. Today's consumer is "the coordinator or a person; no observer consumer" (merged-requirements `:221`), and Q17 is recommended "No, not now" (`:544`). Every store needs a "named store, owner, reader set, retention and file mode" before it is built (V2-04, `:401`). C refuses to create anything that lacks those five, removes an open item from wave W5, and records in the contract note that the JSON has no stored form. That stops anyone from building against a stored sweep file and keeps the observer and the sweep separate (ADJ E-03 `:129`, X-017 `:360`).

## 3. Strengths claimed (B)

1. **Keeps NFR-001's file count without relaxing the rule.** The rule counts files: "a successful run never leaves two files (NFR-001)" (design `:128`); "1 report and 1 JSON object on exit 0" (design `:347`). An embedded block adds no file. The `test_cli_contract.py:1474` assertion `_reports(env.sweeps) == [f"{STEM}.md"]` still holds. This is the one variant that stores facts without the "relax NFR-001 ... two pinned tests change" path that SW-11 (`:200`) and K-NFR001 (`:618`) attach to a stored file.
2. **No sidecar, so no new crash states.** Design `:131-153` lists every on-disk state a crash can leave, and it depends on one report name per run, published through `os.link`. A sidecar would add a second publish step and a second set of crash states. An embedded block rides the existing atomic publish (temp file, then `os.link`).
3. **The machine facts and the human report cannot separate.** Caller capture (A) stores the JSON wherever each caller chooses, apart from the report it describes. Embedding ties the facts to the report by construction, which is what a later reader browsing "by report date" needs.
4. **The data is already computed before publish.** `render` runs before `_publish`, and `to_json` runs after it only to add `report_path` (`commands.py:273-277`). Every other key is a pure function of `SweepResult` and `SweepContext` (`report.py:613-695`). The embedded object needs only that function without `report_path`, so no new collection, Orca call or git call is added (NFR-014's allow-list is untouched).
5. **One storage policy instead of one per caller.** A's own cost line says "two callers could store it differently". In B the sweep owns the format, and the location is the existing `.dev/sweeps/` folder (design GQ-106 `:63`).

## 4. Weaknesses identified in the others

1. **A's fallback skips the option that keeps NFR-001.** A goes from "caller capture" straight to "a later PR relaxes NFR-001 and changes the two tests". It never considers embedding in the existing report, which stores the facts without touching the rule. If capture fails a reader that is not the caller, A takes the most expensive path first.
2. **A's caller capture does not help a reader that is not the caller.** A says capture serves the coordinator, which already holds the JSON in its own call. The candidate readers ADJ names are v2 and a Coder#477 status record (`:361`). Neither is the caller, so capture serves them only if every caller agrees on one location and one format, which A leaves to each caller.
3. **C contradicts the spec's conditional on Q17.** The spec says "if yes later, Q9 becomes a real requirement" (`:544`). C instead makes any future need "a new owner question, not a revival of SW-11", and it effectively forces Q17 to "no" (C's own cost line). It also closes off ADJ A-001's candidate carriers (v2, Coder#477) before either has written its field list.
4. **C's rule cannot be enforced.** "Never stored by ... callers" is an instruction only; C concedes the sweep cannot enforce it. A standing rule that callers can break without anyone noticing is weaker than an open, triggered deferral.
5. **A and C both point readers back to the Markdown report.** A says "anyone who needs past machine facts must parse the Markdown report"; C says "Readers of past sweeps must parse Markdown, which is not a stable machine format". The report's text is sanitized and cut for tables (`cell` cuts to `CELL_MAX`, `report.py:602-605`), while the JSON is "sanitized but never cut" (design `:563`). The fallback both variants name is therefore lossy.

## 5. Concessions (B's real weaknesses, verified this session)

1. **"Append at the end" breaks a pinned test and the completeness marker.** `test_cli_contract.py:1476` asserts `report.read_text("utf-8").endswith("Report complete\n")`. The design treats `Report complete` as the sign of a complete report (`:139`, `:153`), and `render`'s docstring says the report ends in it (`report.py:609`). B's claim that NFR-001's tests "should pass unchanged" is therefore false as written: the `:1474` test function fails at `:1476` if the block follows the footer. A corrected B must insert the block before `_footer` (the last entry of `SECTIONS`, `report.py:545-558`), or inside it before the marker.
2. **The fence is not safe against worker-written text.** `sanitize` neutralises backslashes, `|`, `<`, `>`, `[` and `]` (`report.py:569-599`), not backticks. A worker-written string containing three backticks could close the fenced block early. B's "UNVERIFIED that the existing sanitizer covers fenced blocks" is now settled: it does not. A fix is needed, such as a fence longer than any backtick run in the payload, plus a test.
3. **No named reader exists.** "Consumer today: the coordinator or a person; no observer consumer" (merged-requirements `:221`). B builds a store for readers that have not written their field list, against ADJ A-001's "v2 names its field list first" (`:361`).
4. **"Retention follows the reports" means no retention policy.** Reports live in the gitignored `.dev/sweeps/` folder (`.gitignore:255-256`: "operator-local, never posted ... Never tracked"), and "the person deletes old reports by hand" (design `:35`, SP-22). An embedded store is therefore not durable and has no owner, which fails V2-04's "named store, owner, reader set, retention and file mode" (`:401`) if v2 relied on it.
5. **It changes a newly merged and reviewed tool.** `to_json` takes `report_path` as a required argument (`report.py:613-615`), so embedding needs a signature or call-order change, plus a test pinning that the embedded and stdout copies match apart from `report_path`.
6. **Reports get harder for people to read.** One JSON object per row and per worktree, never cut (design `:563`), can be long, at the bottom of a document that people read.

## 6. Shared assumptions

| ID | Response | Reason |
|---|---|---|
| A-001 (reports last long enough to be a record) | REJECT | Verified false as a guarantee. `.dev/sweeps/` is gitignored and "never tracked" (`.gitignore:255-256`), and retention is out of scope, with reports deleted by hand (design `:35`, SP-22). This hurts B most, because B's store is the report. It also hurts A and C, whose "parse the Markdown report" fallback has no durability promise either. Only A's caller capture can choose a durable location. |
| A-002 (readers share the sweep's host and checkout) | QUALIFY | True for today's only consumer, the coordinator in the same checkout (merged-requirements `:221`), and V2-04 requires that v2's first release "reads only what the same OS user on the same host can read" (`:401`). A same-host v2 is therefore within the assumption. A Coder#477 status record on another host is not, and none of the three variants provides a transport. |

## 7. Per-point positions

| Point | Better variant | Confidence | Note |
|---|---|---|---|
| S-001 (section set) | A, B and C tie (A listed) | 50% | Identical structure; no difference on merit |
| C-001 (is the JSON kept?) | A | 70% | No named reader today (`:221`); B's form is better kept as the stored option to try later |
| C-002 (NFR-001) | B | 60% | Embedding keeps the file count, but only if the block goes before `Report complete` (`test_cli_contract.py:1476`) |
| C-003 (SW-11) | A | 70% | Deferred with an explicit trigger beats both building now (B) and closing for good (C) |
| C-004 (who owns storage rules) | B | 55% | One producer-owned format beats one per caller, but "retention follows the reports" is no retention (SP-22) |
| C-005 (later readers) | A | 65% | Leaves the field list to the first reader (ADJ A-001 `:361`); B pre-empts it and C closes it |
| X-001 (keep before a named reader?) | A | 75% | V2-04 requires store, owner, reader set, retention and file mode first (`:401`) |
| X-002 (does keeping need relaxing NFR-001?) | B | 65% | Correct: an embedded block does not need it; A assumes any stored form does |
| A-001 (report durability) | A | 60% | Only caller capture can pick a durable location; B depends most on a non-durable folder |
| A-002 (same host) | A | 55% | None of the three solves cross-host transport; A's caller capture is the most open to adding one later |

## 8. Overall verdict

The owner should pick **A, amended with B's form as the first storage option**. Keep SW-11 deferred with A's trigger. When a named reader needs stored facts, Phase 2 should try, in order: caller capture; then embedding the JSON before the `Report complete` footer, with a backtick-safe fence and a test that the embedded and stdout copies match; and only then a sidecar that relaxes NFR-001.

Confidence: 70%.

Reason: no reader exists to set the field list or retention, and the reports holding B's block are not durable, but B's embedding is the only known path that stores the facts without breaking NFR-001, so it belongs in A's fallback order ahead of relaxing the rule.
