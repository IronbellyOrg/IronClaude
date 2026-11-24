# Spec-to-plan coverage

## Extraction

Independent requirements-analyst (requested model sonnet) read the source, plan, coverage algorithm and relevant source/test/docs. Pass 1: zero labeled requirement IDs; four heading-based tasks, no requirement-ID references. Pass 2: twelve quote-pinned inferred rows below, all from `../../source.md:1`. Thus coverage is inference-assisted (`parsed-sparse`), not undefined. The reviewer returned semantic PASS with no blockers; its containment estimates are not accepted as machine results. The main context computes exact containment separately. The truncated tail was subsequently received through SendMessage and is recorded below; no missing result is assumed.

## Requirement rows

All quotes below were independently extracted from `../../source.md:1`; parent substring assertions confirmed every quote exists verbatim. Synthetic IDs do not imply source labels.

| ID | Verbatim quote | Exact containment ratio | Match | Semantic coverage |
|---|---|---:|---|---|
| INF-001 | Create a checked implementation plan only for issue 568, swarm help advertises unsupported --custom-prompt-dir. | 0.4615 | none | Title, goal and Constraints |
| INF-002 | Preserve blocked/partial historical diagnosis and all pending verification requirements. | 0.5 | none | Constraints; Tasks 2 and 4 |
| INF-003 | Plan the supported two-help-description correction in src/superclaude/cli/swarm/commands.py using JobSpec custom_prompt_dir with lens custom | 0.9375 | Task 4 | Tasks 3 and 4 |
| INF-004 | reproducing regression tests failing before the edit and passing afterward | 0.625 | Task 1 | Tasks 1-4 red/green checkpoints |
| INF-005 | corrected public help captures | 0.75 | Task 2 | Task 4 repaired public outputs |
| INF-006 | rejection of unsupported run option | 1.0 | Task 2 | Tasks 2 and 4 parser checks |
| INF-007 | independent review | 1.0 | Task 4 | Constraints and Task 4 |
| INF-008 | No new CLI flag, prompt-loading changes, inline-custom-spec changes, injection-guard or metadata changes. | 0.6667 | Task 3 | Constraints; Tasks 3 and 4 |
| INF-009 | Work only in this isolated checkout. | 0.3333 | none | Constraints |
| INF-010 | Do not replay counter-update.py or change diagnostic counters | 0.4286 | none | Constraints |
| INF-011 | implement product code/tests, run models, commit, push, interact with GitHub or create worktrees | 0.5 | none | Prohibition inherited from preceding Do not; Constraints and Task 4 |
| INF-012 | User explicitly requests plan only, no implementation. | 0.4 | none | Constraints |

## Deterministic matching

Computed by a UV `--no-project` standard-library read-only script, not LLM estimates. Task bodies are split at `## Task N:` and terminated before the next phase heading. Global Constraints are not injected into the task text. Tokens are unique case-folded `[a-z0-9_]+` words; threshold >=0.6; ties choose the earliest task. Fixed stopwords: a all an and any are as at be been being but by can could did do does else for from had has have if in is it its may might must no not of on only or shall should that the then these this those to use using was were will with without would.

Parsed-only coverage: null (0 parsed rows), not a vacuous 100%. Union coverage: 0.5 (6/12). Unmapped union rows: INF-001, INF-002, INF-009, INF-010, INF-011, INF-012. S_dev_density=0.5. These values remain literal algorithm outputs; semantic review does not replace them with 1.0. The algorithm misses constraints placed outside task bodies and can match shared words to a task with the wrong semantic role (INF-005). Tier 2 must adjudicate actual source coverage rather than treat the ratio as either proof of correctness or proof of a missing requirement.

## Independent coverage findings

Reviewer verdict: PASS; zero blocking findings. The reviewer confirmed current help producers, reference symbols, root CliRunner imports/pattern, five related test files and transferred artifact existence. Its broad no-test-collision claim is retained as a reviewer search result, not an exhaustive fact. It did not verify the five pending rows (it searched the counter snapshot, not their actual tasklist); parent Read of diagnosability-tasklist.md already located the five explicit rows, so no missing-row conclusion follows.

Returned candidates, not automatic accepted defects:
- Minor hypothesis: whitespace normalization could miss a hyphen-wrapped rejected option token. Reviewer explicitly did not check Click's implementation; this remains an unverified library-formatting hypothesis, not a verified defect. Positive guidance checks and explicit red-run requirements still guard reproduction.
- Medium candidate: applied-fix review is required only in Task 4 acceptance and Constraints, without a fixed filename or standalone task. Reviewer says an executor might omit a distinct report. Parent notes that the governing workflow template makes final review executor-owned and forbids verification-only tasks; the plan explicitly requires a persisted independent report under ./artifacts/. Tier 2 must adjudicate whether the missing exact filename is substance or form. No plan edit authorized by a Medium alone.
- Minor contextual note: run help contains a directory path placeholder (`<custom-prompt-dir>/system.txt`), not the rejected CLI option token. It is explicitly out of scope and already dispositioned by the historical report, not an additional help defect to fix.

No files were written by the reviewer. Main context owns this on-disk receipt and all later gates.
