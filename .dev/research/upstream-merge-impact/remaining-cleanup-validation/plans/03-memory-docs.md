---
version: "1"
priority: Medium
created_date: "2026-10-23"
---

# Correct memory documentation and examples

Source: ../REPORT.md (Correct memory documentation and examples); ../../docs-memory-releases.md
Goal: Make the linked memory guides, examples and references describe the existing implementation without changing working code, adding a backend or modifying legitimate data.

## Constraints

- Written plan only, based on the registered simple-task template; not a managed workflow package and not executed. Separate authorization is required before edits or runtime checks.
- Exact product allowlist: `docs/user-guide/memory-system.md`, `docs/memory/README.md`, `docs/memory/reflexion.jsonl.example`, `docs/mcp/mcp-integration-policy.md`, `docs/reference/pm-agent-autonomous-reflection.md`, `docs/memory/pm_context.md`, `docs/memory/token_efficiency_validation.md`, `docs/memory/WORKFLOW_METRICS_SCHEMA.md`. Limit edits to memory-specific claims/examples and directly affected links; do not rewrite unrelated MCP or token-policy sections.
- Preserve all working memory/pytest/PM code and exports, tests, pollution guards, `docs/memory/solutions_learned.jsonl`, all other real JSONL logs, and every legitimate mistake/pattern record byte-for-byte. Different record schemas are not permission to delete or migrate legitimate data.
- Do not implement MindBase, add redaction/filtering logic, change first-match semantics, add automatic activation, seed production storage, run destructive dedup/rotation/repair commands, or resurrect retired research notes/translations/test mistakes.
- Read the live implementation before each task. Before any authorized change, capture checkout/branch/HEAD/status and protected-file hashes. Keep task-owned evidence and any new checks under `../implementation-evidence/03-memory-docs/` only.
- Use UV for Python checks; any future execution of the existing class must use isolated task-owned memory and mistake directories, never production paths. No external service/install/build is necessary for this docs-only plan.
- No hard dependency on the root-plugin or gateway plan. Coordinate the shared subject of optional MindBase wording, but this plan alone owns `docs/mcp/mcp-integration-policy.md`.
- Do not duplicate the completed sync/coverage removal or completed pollution fix. No staging, commits, pushes, PR/remote-branch actions. Independent review must verify every task's claims and current protected-file preservation.
- Runtime results, external consumers/manual backend availability, benchmarks and estimates remain UNVERIFIED until actually measured; no such validation has run as part of preparing this plan.

## Phase 1: Correct the reader-facing memory contract

## Task 1: Align the two primary memory guides

Read `src/superclaude/pm_agent/reflexion.py`, `src/superclaude/pytest_plugin.py:71-145,172-196`, `tests/conftest.py:23-117`, and both `docs/user-guide/memory-system.md` / `docs/memory/README.md`. Capture the protected-file/data baseline before any edit. Correct the two guides to the real `ReflexionPattern` contract: explicit directory > nonempty environment override > CWD/docs/memory; `solutions_learned.jsonl` plus sibling mistakes directory; caller dictionaries, signature keys and retrieved solution/root-cause/prevention/timestamp fields; digit normalization/100-character truncation; whitespace-token-set intersection/union >=0.7; first matching stored row, no ranking/status/solved filter.

Describe explicit API use separately from the pytest marker/call-phase failure recorder. Remove automatic session loading, universal PM capture/solution application and implemented MindBase promises. Explain that the recorder persists supplied fields without redaction and may also write a mistake document; callers must redact before recording. Do not rewrite production code to match the prose. Replace destructive clear/dedup/repair/rotation recipes with backup-and-manual-review guidance, not the same recipes pointed at the real data file. Remove or mark performance/recurrence figures as unmeasured. Fix only the affected implementation/sample/reference links; do not restore deleted notes to satisfy links.

Acceptance criteria:
- Both guides agree with the exact live path/schema/activation/matching/order/backend contract, including inclusive 0.7 and no newest-first/deprecated-status guarantees.
- Privacy text does not guarantee automatic removal of secrets; it covers both storage outputs and pre-recording caller responsibility. No new unsafe seeding/delete/dedup recipe is introduced.
- The guide's matching example is numerically correct for its stated signature inputs. The existing message-only JWT example has 4 shared / 8 union words (50%), not 87.5%; do not describe it as a match at 70%.
- A task-owned claim matrix cites live source for each corrected behavior; protected code/data/guard hashes remain unchanged and only the two named guides change in this task.

## Task 2: Replace the synthetic example with compatible error records

Depends on: Task 1

Read `docs/memory/reflexion.jsonl.example`, the corrected two primary guides, and the unchanged recorder/reader. Keep the `.example` filename but replace its old task/mistake/fix/status rows with explicitly synthetic error-learning records using the real signature-bearing fields and useful solution/root-cause/prevention fields. Do not copy them into `solutions_learned.jsonl` or merge them with the four legitimate pattern rows. Correct both guides' links/example snippets to match this example; preserve any accurate generic JSONL explanation.

Create a small task-owned runnable sample check. Parse every example row as JSON without importing the memory recorder. Assert required illustrative keys/types, absence of real credentials/personal data, and consistency with documented outputs. If any behavioral reader smoke check is added, run the existing class only with explicit isolated storage rooted under this task's evidence directory, including its sibling mistakes output, and record the result separately from static parsing.

Acceptance criteria:
- Every example line is one valid synthetic JSON object with `error_type`, `error_message`, `test_name` and a useful `solution`; examples make no automatic schema-validation claim about the raw recorder.
- The sample has no old-schema seeding advice or claim that `status` affects matching, and guide snippets agree with the sample contract.
- The runnable parser check passes, and exact before/after hashes prove production memory/mistake records and all code/guards unchanged. Runtime is not claimed unless the isolated reader was actually exercised.
- This task changes only the named example and directly associated snippets/links in the two Task 1 guides; no real data migration occurs.

## Phase 2: Reconcile the linked reference chain

## Task 3: Correct memory policy and reflection-reference claims

Depends on: Task 2

Read `docs/mcp/mcp-integration-policy.md`, `docs/reference/pm-agent-autonomous-reflection.md`, the corrected guides/example, and the unchanged recorder/callers. Correct the policy's initial obsolete ReflexionMemory block and its later memory/history selection, session-start auto-load, post-implementation auto-save, file-memory prohibition, explicit memory-call prohibition and migration-removal/test claims. Preserve unrelated MCP policies; don't convert this into a general routing-guide rewrite. Distinguish optional manual external services from the unimplemented Python MindBase helper.

In the reflection reference, reconcile the error-learning layer, storage/backend promises, both conflicting record schemas and linked examples with the actual recorder and corrected guides. Describe explicit APIs and marked pytest capture, not automatic fixes for all sessions/errors. Mark unmeasured savings/recurrence promises as historical/unverified or remove the unsupported promise in the affected memory paragraphs. Correct broken directly affected links without recreating retired source/research files.

Acceptance criteria:
- These two files no longer contradict the actual directory precedence, raw error record, 70% inclusive set overlap, stored-order first-match or limited activation contract.
- They do not require deleting legitimate docs/memory, banning supported explicit memory calls, or assuming automatic MindBase availability/storage. Any old policy is labeled superseded rather than left as a current instruction.
- The reflection reference's multiple schema examples no longer conflict; all retained error-learning examples agree with Task 2's synthetic sample and actual lookup fields.
- Only memory-specific sections/affected links change. Unrelated policy/reference behavior, production code/data and pollution guards remain unchanged; claim matrix and link checks record these outcomes.

## Task 4: Qualify historical context, validation claims and metrics examples

Depends on: Task 3

Read `docs/memory/pm_context.md`, `docs/memory/token_efficiency_validation.md`, `docs/memory/WORKFLOW_METRICS_SCHEMA.md`, the prior three tasks' corrected guides/policy/reference/example, and the validation report's memory section. Qualify historical ReflexionMemory/MindBase integration and token/latency/savings/validation claims rather than presenting them as current measured behavior. Repair directly affected links to retired research notes by removing or explicitly marking historical references; do not restore those files.

Keep workflow metrics separate from error learning. Align the optional field example and table on the already documented `error_search_tool` field using an accurate local/none example, and label it a documented optional metric rather than an automatically emitted field. Do not rewrite metrics logs, add instrumentation or rename data in place.

Finish the task-owned runnable static check set: parse the synthetic JSONL; check affected local links and intended live source paths; assert corrected key claims and absence of the specifically retired active instructions; compare exact eight-file product scope and protected-file/data hashes. Capture outputs, distinguishing static validation from any genuinely run isolated behavior check. Do not import memory code merely to inspect it.

Acceptance criteria:
- The three named notes/schema no longer present unsupported backend/performance/automation claims as established facts; current documentation and historical estimates are visibly separate.
- Workflow metrics example/table agree on the documented optional field and remain distinct from error signatures/production storage. No metrics data or code changes.
- The whole linked eight-file chain has consistent class/path/schema/matching/order/activation/privacy/backend descriptions and resolved or explicitly historical links; sample parsing and all static checks pass.
- Baseline comparison confirms exactly the eight allowed product files changed and all production code/exports/PM protocol/tests/guards/real memory or mistake data remain byte-identical. Existing pollution cleanup, retired translations/research and completed sync/coverage removal are preserved.
- A fresh independent final reviewer checks all four tasks against actual current docs and recorded assertions. No missing result or unmeasured runtime claim is accepted as success; any unmet criterion blocks completion.
