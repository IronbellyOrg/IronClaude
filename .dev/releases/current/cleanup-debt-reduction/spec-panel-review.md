# Cleanup Debt Reduction — Specification Panel Review

## Review contract and evidence limits

- Mode: critique; focus: requirements, architecture and testing, with preserved-state/guard correctness obligations.
- Review date: 2026-10-19. Input: the existing populated `cleanup-debt-reduction-spec.md`, not raw feature generation. The audit, merits debate and independent deletion-risk review are represented by that specification; this pass does not claim to have independently repeated the entire audit.
- All eleven perspectives below are **simulated analytical lenses**. The named people did not participate, endorse the document, or supply quotations.
- Authorized mutations: this report and the sibling specification only. No production/test edits, builds, tests, publishing, model/API execution or delegation were performed. Source retrieval is inspection, not runtime validation.
- The 488-line estimate is nonbinding. All ten candidates and all held/rejected boundaries remain in scope exactly as fenced by the specification. No semantic version is assigned by this review.
- Status vocabulary: **resolved** means a specification ambiguity was corrected and re-reviewed, not that implementation evidence passed; **pending implementation gate** is not PASS. A missing product/scope decision would be BLOCKED and named explicitly.

## 1. Sequential expert observations

The order is deliberately fixed; later perspectives build on earlier ones.

1. **Simulated Karl Wiegers — requirements.** FR/NFR identifiers, candidate IDs, explicit non-goals and eligibility evidence make this a useful implementation contract. The maintainer's goal is lower maintenance cost without reducing supported behavior or requirement coverage. Tighten the deletion gate to require observed passing migrated boundary assertions before deletion, rather than allowing test migration to be merely planned. Priority High; addressed by finding R1.
2. **Simulated Gojko Adzic — specification by example.** Empty collections, registered None, malformed delimiters and signed-looking confidence text need concrete before/after examples, not merely a list of categories. The boundary tables below supply executable-test design inputs, not execution results. Pin delimiter selection and confidence/cap examples in the spec. Priority High; addressed by R2/R4.
3. **Simulated Alistair Cockburn — actor and goal.** Primary actor is the maintainer implementing the cleanup; secondary actors are CLI/plugin users and the future release reviewer. Success is ten individually evidenced outcomes, not a target line count. Alternate flow is candidate BLOCKED, retain code, report exact reason; no implicit partial-release success. Existing scope is adequate; no invented end-user feature or publication use case.
4. **Simulated Martin Fowler — architecture.** Share only existing equivalent concrete primitives. Preserve per-module exports and effective patch lookup, and keep policy in recipes. Lower-layer utilities must not import roadmap; validation runners and the main roadmap sanitizer stay distinct. N worker records remain N; serialization byte counts are a separate dimension. No superclass, runner framework or new dependency is justified.
5. **Simulated Michael Nygard — failure mechanics.** Atomic replacement is not the same as crash-proof cleanup. The baseline attempts unlink on caught Exception, suppresses unlink OSError and re-raises the original failure; SIGKILL cannot execute cleanup. Encoding currently follows parent creation. Make those boundaries explicit rather than strengthen behavior during consolidation. Priority High; addressed by R3.
6. **Simulated James Whittaker — adversarial correctness.** Probe zero/empty, divergence, sentinel collision, sequence and accumulation separately. None is not an absent key; leading `---` is not necessarily well-formed YAML; counts C and B diverge on Unicode. Exact attack-template findings and populated guard tables below precede synthesis. These attacks are thought experiments, not observed test failures.
7. **Simulated Sam Newman — evolution and compatibility.** Repository-local caller absence cannot prove no external consumer. Supported-consumer conflict blocks removal; intentional internal symbol retirement must be recorded. Concrete passthrough must not depend on mutable registry contents. No version bump, generic compatibility shim or service decomposition belongs here.
8. **Simulated Gregor Hohpe — integration and quantity flow.** Embedding combines N labeled blocks into one prompt string; that is representation aggregation, not input loss. Worker normalization remains one record per input, including failed records. Reduced output is an existing aggregate, not a license to deduplicate. Preserve sanitizer-before-tool-write and contract/sentinel emission gates. Quantity accounting appears below.
9. **Simulated Lisa Crispin — risk-based testing.** Risk is concentrated in requirement ownership, recipe policy parity, filesystem failures and installed package resources. Unit-only helper parity is insufficient. Require both live validator paths, runtime logging/diagnostics/config ownership, failure injection, fixed-clock differential cases and wheel-from-sdist install checks. No existing test result is inferred from source inspection.
10. **Simulated Janet Gregory — quality agreement.** Keep three distinct claims separate: the spec is ready to plan, the tasklist covers it, and the implementation passed its gates. Preserve unchecked implementation work and a candidate/FR/NFR evidence ledger. A failed ownership migration must lead to an explicit blocked candidate, not disappearing tests.
11. **Simulated Kelsey Hightower — operational acceptance.** Verify the package users actually install: baseline manifests/hashes, direct wheel and sdist-derived wheel, both CLI entry points, pytest discovery and installed resources. Do not execute uploads to validate a retired publishing wrapper. A dependency lock change must not remove Black's allow-list permission or upgrade unrelated dependencies.

## 2. Scoped source navigation

All paths in this report are relative to `/config/workspace/IronClaude/.dev/worktrees/cleanup-release` unless explicitly absolute. Symbols, rather than stale line citations, are the navigation keys.

| Inspected surface | Review use | Limit |
|---|---|---|
| `src/superclaude/cli/swarm/normalize.py`: `_resolve_recipe`, `_PassthroughFallback`, `_atomic_write_text`; dispatcher excerpts | None/absent/invalid dispatch, parent-before-encoding, transaction and count accounting | No execution or proof of all callers |
| `src/superclaude/cli/swarm/reduce.py`: `_atomic_write_bytes` and emission excerpts | Same caught-Exception/unlink-OSError transaction; existing aggregation/emission boundaries | Retrieval inspection only |
| `src/superclaude/cli/tasklist/executor.py`, `src/superclaude/cli/roadmap/validate_executor.py`: `_embed_inputs`, `_sanitize_output`, runner setup | Identical helper bodies apart from local imports/logger; delimiter/error/order semantics | Main roadmap executor deliberately excluded from consolidation |
| Four `src/superclaude/cli/swarm/recipes/*_v1.py` candidate modules | Exports, confidence distinction, section/frontmatter functions, recipe constants and parsing policy | Policy differences retained, not normalized away |
| `pyproject.toml` | Hatchling wheel/sdist payload configuration, CLI/plugin entries, direct Black dependency, Ruff policy | No build or installed resource validation |
| `tests/swarm/test_imm6_atomic_write.py`, `tests/swarm/test_normalize.py` | Existing static transaction assertions and registered-None test intent | Reading a test is not a passing result |

Additional targeted inspection found requirement-labeled `TestNFR009Compliance` in `tests/cli_portify/test_failures.py`, helper imports in `tests/cli_portify/test_monitor.py`, and both wrapper-specific and behavioral tests in `tests/pipeline/test_integration_decompose.py`. This supports retaining the migration gate; it does **not** establish that the surviving live owners already cover those assertions. Eligibility and runtime coverage migration remain pending implementation evidence.

## 3. Findings, priority and applied resolution

Severity is the initial specification defect/clarity risk, not an assertion of a production bug. High/Medium/Low indicates implementation-planning priority. Quality impact is qualitative; no calibrated numerical score or test result is fabricated.

### Requirements analysis

| ID | Severity / priority | Simulated perspective | Confirmed issue or clarification | Correction and resolution | Quality impact |
|---|---|---|---|---|---|
| R1 | MINOR / High | Wiegers, Gregory | FR-01/04/10 and FR-11 already require migration, but a named prospective owner could be mistaken for completed coverage reconciliation | Added explicit passing migrated live-owner assertions before C01/C04/C10 deletion in §5.1; existing BLOCKED rule remains. Resolved as a clarity improvement, not a claim of a newly missing gate | Prevents planned coverage from being reported as observed coverage |
| R5 | MAJOR / High | Wiegers, Adzic, Hightower | FR-05 allowed only metadata exceptions to before/after payload hashes, yet this very release intentionally changes packaged Python sources/tests/config and may carry duplicate source payloads. Literal full-payload identity would reject authorized work | FR-05 and phase 1 now require a packaging-only baseline/paired-post on identical source/dependency snapshots except setup.py/MANIFEST.in, before other edits or in isolated copies. Final-release changes use per-path candidate-attributed deltas (including Black metadata), unchanged-resource hashes and no blanket exclusions. Added direct-wheel versus sdist-derived-wheel comparison; NFR-05 aligned. Resolved | Makes packaging acceptance satisfiable without permitting unexplained resource loss |

### Architecture and correctness analysis

| ID | Severity / priority | Simulated perspective | Confirmed issue or clarification | Correction and resolution | Quality impact |
|---|---|---|---|---|---|
| R2 | MAJOR / High | Fowler, Adzic, Whittaker | FR-06's 'frontmatter'/'valid delimiter' prose could be interpreted as YAML validation, unlike the existing startswith guard and first standalone delimiter search | FR-06 now pins leading-whitespace startswith no-op, exact multiline delimiter selection, missing-close behavior, prefix UTF-8 count, fixed temp sibling, logger and non-FileNotFound errors. Resolved | Avoids an accidental parsing or cleanup redesign |
| R3 | MAJOR / High | Nygard | FR-07's cleanup statement and registry invariant did not spell out failed unlink, uncaught termination and the parent-before-encoding ordering edge | FR-07 now pins caught Exception, fdopen failure, unlink-OSError suppression, original exception, mkdir/encoding/mkstemp sequencing and SIGKILL/BaseException limits. Resolved | Preserves baseline failure semantics rather than promising impossible kill-time cleanup |
| R6 | MINOR / Medium | Wiegers, Hohpe | Encoded-count initial value assumed encoding already succeeded; ordered worker flow and the sanitizer's distinct temp state were absent from the registry | §5.1 distinguishes not-yet-computed from B, enumerates evidence outcomes, adds ordered records and sanitizer count/temp state, and explicitly states no introduced application state. Resolved | Makes transient lifecycle and units explicit |

### Testing analysis

| ID | Severity / priority | Simulated perspective | Confirmed issue or clarification | Correction and resolution | Quality impact |
|---|---|---|---|---|---|
| R4 | MINOR / Medium | Adzic, Crispin | FR-03 already called for every cap and policy parity, but delegated concrete confidence/section/cap boundaries to the implementer | Added signed-looking first-digit examples, no-digit distinction, first-section/literal-frontmatter behavior and current numeric cap inventory with cap−1/cap/cap+1 cases. Resolved without changing parser policy | Gives deterministic test oracles instead of just test categories |

No confirmed issue justifies expanding the deletion scope. C01/C04 remain conditional: this review has not demonstrated requirement ownership or observed passing migrated tests. A future live/public consumer conflict, unknown owner, failed migration or missing package baseline makes that candidate BLOCKED under FR-11, not safe by assertion.

## 4. State registry validation and applicability

The spec is a behavior-preserving refactoring. It introduces **no new mutable application state**, CLI flag, environment variable, schema or persistent state machine. Registry/evidence additions describe existing transients and planning records only. Mutable local parser accumulators remain per-call and recipe-local; existing salvage, confinement and emission state is not redesigned.

| Registry entry / scope | Initial and valid domain check | Preserved invariant and transition | Review disposition |
|---|---|---|---|
| Recipe registry entry | Existing mapping; key absent, None, conforming Recipe or invalid non-None object | Membership checked before value; None uses concrete passthrough without mutation; valid object identity retained; invalid object errors | Explicit in FR-09 and G2; no lookup through mutable passthrough slot |
| Destination bytes | Existing full bytes or absent | Before successful replace retain old/absent; after successful replace complete new payload; caught or uncaught pre-replace failure cannot expose partial destination | FR-07; not a guarantee of directory fsync or cleanup after process death |
| Atomic temporary path | Absent before mkstemp; unique same-parent path after creation | Write/flush/fsync/close before replace; unlink attempted on caught Exception; failed unlink or uncaught termination may leave sibling | FR-07 now explicit; not generalized to preflight or sanitizer |
| Encoded count | Not yet computed before encoding; thereafter integer B ≥ 0 | Successful result reports B persisted bytes; exceptions do not return a successful count; caller's existing no-write count remains 0 | R6 fixes lifecycle; no new persistent field |
| Candidate outcome | Pending, Complete or Blocked in planning ledger | Complete requires eligibility and verification; failed/skipped evidence is not completion; retained blocker prevents full-release readiness | FR-11/12; no runtime enum implementation requested |
| Ordered worker records | Caller supplies N; empty allowed; new output list constructed | Successful return has N fresh records in same order without input mutation; status changes only through existing branches | §2/FR-03/FR-09; G2 and quantity diagram |
| Sanitizer prefix count/temp sibling | Count 0 on no-op; fixed suffix .tmp may already exist; prefix count after match | Return/log after successful replace only; non-FileNotFound read errors propagate; baseline temp/error semantics retained | R2/R6; no new atomicity or cleanup promise |
| Recipe local body/rows/sections | Per-call raw string; empty local lists/strings, existing defaults/caps | Parse/fallback/salvage policy stays local; accumulate rows in existing body order; fixed-clock rendering preserves outputs | G5; no new shared policy/state layer |
| Existing confinement/salvage/artifact status and held roadmap state | Existing initialization and readers/writers; not replaced by cleanup | Preserve rejection, emission and metadata contracts through live caller tests | FR-01/04/07/10 and held boundaries; no introduced state |

Registry validation is a consistency review of the written obligations, not runtime state-machine verification. Every lifecycle clarification above was checked against the relevant scoped source where inspected; broader caller and requirement ownership searches remain FR-11 work.

## 5. Quantity-flow accounting

```text
Validation: [N input paths] -> [N labeled fenced blocks, in input order]
          -> [1 joined embedded string; N=0 gives empty string]
          -> [existing separate runner -> sanitize -> existing tool-write phase]
          Read failure -> existing exception path, not a silently omitted block.

Workers:  [N WorkerResult records] -> [resolve once; map per record]
          -> [N fresh output records in same order on successful return]
          -> [existing reduce aggregate/contract/sentinel policy, unchanged]
          N=0 -> 0 records for a valid resolved recipe; resolver can still error.
          Hard-failed/empty records remain records; emitted files are not N by fiat.

Persistence: [text C code points] -> [UTF-8 payload B bytes]
          -> [write B -> flush -> fsync -> close -> replace]
          -> [B bytes persisted; successful helper returns B]
          Example: 'é' has C=1, B=2; '' has C=0, B=0.
Sanitize: [prefix C_p code points + retained suffix]
          -> [remove prefix; return len(prefix.encode('utf-8')) = B_p]
```

There is no newly authorized N→M worker filtering, scoring, deduplication, synthesis or reordering. Recipe parsing already discards structural/header noise and uses existing placeholder/fallback rendering; preserving N worker records does not mean every raw line becomes a finding. Existing reduction aggregation is unchanged and is not being flattened into a false N-files invariant. A returned output list count can be N while normalized artifact writes are fewer because existing gates suppress writes. Quantities are compared in their own units; C versus B mismatch is intentional encoding, not dropped records. No demonstrated dimensional contradiction remains in the revised spec.

## 6. Mandatory Guard Condition Boundary Table

The following seven columns are the protocol template. **OK means a specified, reviewable preservation obligation, not an executed or passing case.** Each family has at least six concrete rows. Guard Result names the branch decision; no blank behavior, unspecified outcome or GAP is hidden. Equivalent rows parameterize repeated branch shapes; unchanged parser/render policy is included to prevent accidental scope expansion during extraction. Out-of-contract inputs are identified explicitly rather than inventing new validation policy.

### G1 — Deletion eligibility (FR-11)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1.1 eligibility complete | FR-11 | Zero evidence | C01 evidence rows=0 | False | BLOCKED; retain helpers and report missing evidence | OK |
| G1.2 eligibility complete | FR-11 | Minimal eligible candidate | C10 current references checked, live-owner assertions migrated/passing, evidence complete | True | Only named wrapper/delegation test mechanics may retire; retain behavioral tests | OK |
| G1.3 eligibility complete | FR-01/11 | Typical requirement-bearing helper tests | C01 event/diagnostic assertions map to observed passing live-owner tests | True only after migration | Retire only disconnected named helpers; do not delete monitor test file | OK |
| G1.4 eligibility complete | FR-11 | Accumulation cannot substitute for missing item | 100 search hits; one unresolved dynamic registration | False | BLOCKED even if all other evidence is extensive | OK |
| G1.5 requirement owner known | FR-04/11 | Sentinel unknown owner | C04 NFR-009 owner absent from ledger | False | Retain helpers; no requirement waiver or invented runtime wiring | OK |
| G1.6 no supported conflict | FR-05/11 | Legitimate supported external consumer | Supported direct setuptools consumer found | False | Stop C05; exact compatibility/scope decision required before removal | OK |
| G1.7 no live caller | FR-11 | Repository runtime caller present | C01 live registration/caller found | False | Retain candidate, report caller; do not widen deletion or silently shim | OK |
| G1.8 evidence current | FR-11 | Revision changes after search | Search revision differs from implementation start | False | Refresh exact/dynamic/registration/doc evidence before eligibility decision | OK |
| G1.9 baseline exists | FR-05/11 | Missing baseline | C05 wheel/sdist manifests or tool versions absent | False | BLOCKED; do not substitute assumed package parity | OK |
| G1.10 migrated checks pass | FR-11 | Failure or not run | One migrated assertion fails or remains unexecuted | False | Deletion not eligible; distinguish failure/pending from PASS | OK |
| G1.11 requirement retirement justified | FR-11 | Helper-only import test | No behavior requirement, explicit internal-import retirement rationale | True only with all other gates | Retire obsolete mechanics assertion only; record rationale and external-search limits | OK |
| G1.12 full release complete | §9/FR-12 | One candidate blocked | Nine Complete, one Blocked | False | Release not ready; scope reduction requires explicit decision | OK |

### G2 — Recipe resolution and its preserved dispatch boundary (FR-09)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G2.1 membership | FR-09 | Empty unregistered name | name='', key absent | False | Raise KeyError; empty name is not fallback | OK |
| G2.2 registered None | FR-09 | Minimal raw payload | key exists=None, raw='a' | True | Concrete Passthrough returns exactly 'a', salvaged false, error None | OK |
| G2.3 protocol conformance | FR-09 | Typical registered recipe | entry is valid Recipe object r | True | Return r itself; no substitution or registry mutation | OK |
| G2.4 invalid non-None | FR-09 | Large invalid value | entry=10**100 | False | TypeError, not passthrough or implicit registration | OK |
| G2.5 registered None | FR-09 | Sentinel plus empty data | key exists=None, raw='' | True | Recipe returns empty text unchanged, salvaged false, error None; caller's no-body gate remains | OK |
| G2.6 registered None | FR-09 | Legitimate Unicode/whitespace | raw=' é\n  ' | True | Exact text preserved; no strip, scoring or salvage promotion | OK |
| G2.7 membership/value distinction | FR-09 | Absent key versus falsey object | absent key; separate registered entry=0 or False | False on respective checks | Absent -> KeyError; registered invalid non-None -> TypeError | OK |
| G2.8 concrete fallback independence | FR-09 | Mutable named passthrough entry replaced | REGISTRY['passthrough']=invalid object; another slot=None | None branch true | Other slot resolves concrete Passthrough independently; do not mutate registry | OK |
| G2.9 no promotion through fallback | FR-09 | Parse-error worker with nonempty raw | entry=None, worker.status=parse_error | Salvaged flag false | Keep parse_error; raw passthrough is not recovered structure | OK |
| G2.10 resolve before map | §2/FR-09 | Empty worker list | N=0 and valid recipe; separate absent recipe case | Map empty; resolution still runs | Valid recipe returns []; absent name still raises KeyError | OK |
| G2.11 hard failure short circuit | FR-03/07/09 | Existing timeout or proxy error | status=timeout or proxy_error | True | Do not invoke recipe or write normalized body; preserve existing metadata path and failure record | OK |
| G2.12 recipe exception | FR-03/09 | Normalizer raises | synthetic ValueError before result | Exception branch | Existing parse_error downgrade/error metadata; do not promote to success | OK |
| G2.13 salvage enabled gate | FR-03/09 | Parse-error recovery disabled | parse_error, enabled=False, recovered text present | False | Existing rejection reason/status/sidecar retained; no promotion | OK |
| G2.14 salvage structure gate | FR-03/09 | Recovery lacks flag or body | parse_error; (salvaged=False) or (text='') | False | Existing failed status/reason preserved even if the other condition holds | OK |
| G2.15 salvage success gate | FR-03/09 | Genuine recipe recovery | parse_error, enabled=True, salvaged=True, text nonempty | True | Existing success promotion with metadata/status agreement and encoded byte count | OK |
| G2.16 original status gate | FR-03/09 | Success is not promoted again | status=success, recipe returns nonempty text | Not parse_error | Preserve existing status and result handling; no new promotion semantics | OK |

### G3 — Sanitizer no-op/delimiter selection and embedding (FR-06)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G3.1 missing output | FR-06 | Zero/absent file | FileNotFoundError | True | Return 0; no temporary write or success log | OK |
| G3.2 no delimiter | FR-06 | Empty existing file | content='' | No match | Return 0 without write; preserve file | OK |
| G3.3 no delimiter | FR-06 | Minimal text | content='a' | No match | Return 0; unchanged | OK |
| G3.4 leading startswith | FR-06 | Typical leading YAML | content='---\nx: 1\n---\nbody' | True | Return 0; no rewriting, even if leading whitespace is present | OK |
| G3.5 first delimiter | FR-06 | Typical conversational prefix | content='Hi\n---\nx: 1\n---\nbody' | Match at first standalone delimiter | Retain from first delimiter; return 3 UTF-8 bytes; log after replace | OK |
| G3.6 prefix size | FR-06 | Long prefix and Unicode boundary | prefix=('é' repeated 1000)+'\n' | Match after prefix | Remove prefix; return 2001 bytes, not 1001 code points; no new size cap | OK |
| G3.7 sentinel collision | FR-06 | Leading malformed frontmatter | content='  ---not-yaml' or '---\nunclosed' | startswith True | No-op 0; do not validate or require closing YAML | OK |
| G3.8 embedded delimiter | FR-06 | Legitimate inline/indented marker | content='x---y' or 'x\n ---\nbody' | No standalone match | No-op 0; preserve text | OK |
| G3.9 delimiter suffix spaces | FR-06 | Standalone terminal delimiter | content='x\n--- \t' | Match | Retain '--- \t'; return 2; closing delimiter not required | OK |
| G3.10 repeated delimiter | FR-06 | Multiple matching delimiters | content='x\n---\na\n---\nb' | First match selected | Keep all content from first match, not last; return 2 | OK |
| G3.11 unrelated read failure | FR-06 | Not FileNotFound | PermissionError or UnicodeDecodeError | Missing-file guard False | Propagate; do not return 0 or log successful sanitation | OK |
| G3.12 temporary write failure | FR-06 | Existing destination retained | write_text to suffix .tmp raises | Replace not reached | Propagate; preserve baseline partial-temp behavior, no added cleanup contract | OK |
| G3.13 replace failure | FR-06 | Complete cleaned temp but replace errors | os.replace raises | Success False | Propagate; destination remains prior, temp may remain; no success log/count | OK |
| G3.14 caller logger | FR-06 | Successful cleaning through either runner | Same text on tasklist and roadmap validation paths | Success True | Existing caller-specific logging observability and sanitize-before-tool-write preserved | OK |
| G3.15 empty embedding | FR-06 | Zero input paths | inputs=[] | Empty True | Return ''; do not synthesize a block | OK |
| G3.16 ordered embedding | FR-06 | Minimal empty file, then duplicate/Unicode paths | inputs=[p,p,q], p content='', q content='é' | Nonempty True | Emit all three labeled fenced blocks in order, UTF-8 reads; no dedupe or filter | OK |
| G3.17 embedding failure | FR-06 | One unreadable input among N | read of p_i raises | Error | Propagate rather than omit the block; runner behavior unchanged | OK |
| G3.18 newline handling | FR-06 | Existing text newline conversion | CRLF or other baseline read_text/write_text newline input | Existing text semantics | Preserve baseline text I/O conversion; do not introduce raw-byte sanitizer or promise new byte identity to original newline encoding | OK |

### G4 — Atomic transaction outcome and caller emission guards (FR-07)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G4.1 empty payload | FR-07 | Zero bytes | data=b'' | Success | Complete transaction; destination empty; return 0 | OK |
| G4.2 minimal payload | FR-07 | One ASCII character | content='a', C=1, B=1 | Success | Persist b'a'; return 1 | OK |
| G4.3 normal UTF-8 | FR-07 | Unicode text | content='é', C=1, B=2 | Success | Persist two encoded bytes; return 2 | OK |
| G4.4 repeated whole writes | FR-07 | Accumulation/repetition | write b'A', then b'BB' | Each transaction successful | Final destination b'BB', never appended b'ABB'; counts 1 then 2 | OK |
| G4.5 old destination sentinel | FR-07 | Existing old bytes | old=b'prior', new=b'next' | Replace succeeds | Full new payload replaces full prior; no intermediate partial live file | OK |
| G4.6 absent destination | FR-07 | First write | No destination, valid parent | Success | New complete payload after replace; no live file before replace | OK |
| G4.7 mkdir failure | FR-07 | Parent unavailable | parent.mkdir raises PermissionError | Failure before encoding/create | Propagate original error; no new destination/temp | OK |
| G4.8 encoding failure | FR-07 | Legitimate failure boundary | content contains unpaired surrogate | UTF-8 encode raises | Parent creation still precedes encoding; no temp or destination change; propagate | OK |
| G4.9 mkstemp failure | FR-07 | Resource exhaustion before temp exists | ENOSPC or creation OSError | Failure before protected write | Propagate; no partial destination; no invented temporary cleanup target | OK |
| G4.10 fdopen failure | FR-07 | Descriptor open fails | os.fdopen raises Exception | Caught Exception | Attempt unlink; suppress only cleanup OSError; re-raise original; no partial destination | OK |
| G4.11 write failure | FR-07 | Partial temporary bytes | handle.write raises OSError | Caught Exception | Old/absent destination preserved; baseline cleanup attempt; original exception | OK |
| G4.12 flush failure | FR-07 | Data buffered but not committed | handle.flush raises | Caught Exception | No replace; old/absent live file; baseline cleanup and original failure | OK |
| G4.13 fsync failure | FR-07 | Flush succeeded, sync failed | os.fsync raises | Caught Exception | No replace; preserve live destination, attempt cleanup and re-raise | OK |
| G4.14 close failure | FR-07 | Context exit fails before replace | handle.close raises Exception | Caught Exception | No successful replace/count; same cleanup/propagation, no new swallowing | OK |
| G4.15 replace failure | FR-07 | Fully written temp, rename fails | os.replace raises before replacement | Caught Exception | Prior/absent destination intact; unlink attempt; original exception, not success | OK |
| G4.16 unlink failure | FR-07 | Cleanup also fails | primary OSError plus unlink OSError | Cleanup OSError suppressed | Raise original primary exception; temporary sibling may remain | OK |
| G4.17 kill/uncaught termination | FR-07 | Interrupted before replacement | SIGKILL or uncaught BaseException | Caught-Exception guard not entered | Old/absent live file; temp may remain; no kill-time cleanup guarantee | OK |
| G4.18 confined path | FR-07 | Symlink/output-root escape | Caller rejects proposed path | Emission not allowed | Existing rejection preserved before write; sharing mechanics does not widen permission | OK |
| G4.19 normalized-body emission | FR-07 | Empty body or absent final path | result.text='' or worker.final_path absent | Body write gate False | Preserve existing no-body emission and zero count while retaining record/meta behavior | OK |
| G4.20 meta emission | FR-07 | Sidecar path absent or present | meta_path=None versus valid confined path | Existing optional gate | Absent -> no sidecar; present -> existing status/error/salvage fields via atomic writer | OK |
| G4.21 reduce/contract/done gates | FR-07 | Raw/normalize versus terminal reduction cases | Existing mode/status/contract checks | Existing caller decision | Preserve exact merged/contract/sentinel emission or suppression and validated payload; no new policy in byte writer | OK |
| G4.22 scope exclusion | FR-07/§1.2 | Similar-looking preflight writer | Preflight-specific exception semantics | Consolidation guard False | Keep writer untouched; no exception-policy unification | OK |

### G5 — Recipe confidence, section, frontmatter, caps and unchanged local policy (FR-03)

For cap rows below, k ranges over the explicitly enumerated current caps in revised FR-03. These are concrete numeric cases, not a new configurable-cap feature. The cap+1 result is the first k code points after whitespace collapse, not first k UTF-8 bytes.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G5.1 empty raw body | FR-03 | Zero/whitespace input to all four recipes | raw='' or ' \n ' | Empty True | Existing empty raw body error, text='', salvaged=False; do not render stub | OK |
| G5.2 confidence empty | FR-03 | Empty/pure whitespace confidence | cell='' or '  ' | No digit | Empty string for bare/hypothesis/verdict confidence helpers | OK |
| G5.3 minimal confidence | FR-03 | Lower boundary | cell='0' | First digit match | Return '0'; no new lower-bound parser | OK |
| G5.4 ordinary confidence | FR-03 | Typical numeric text | cell='confidence 73%' | Digit run 73 | Return '73' | OK |
| G5.5 upper confidence | FR-03 | Maximum | cell='100' | Clamp at maximum | Return '100' | OK |
| G5.6 confidence overflow | FR-03 | Above maximum | cell='101' | Clamp | Return '100' | OK |
| G5.7 signed-looking text | FR-03 | Negative-looking sentinel collision | cell='-1' | First digit run 1 | Return '1', not 0 or -1 | OK |
| G5.8 multiple digit runs | FR-03 | Decimal/range-looking data | cell='12.5 then 99' | First run 12 | Return '12', not decimal normalization or last score | OK |
| G5.9 qualitative confidence | FR-03 | Legitimate no-digit text | cell=' high  confidence ' | No digit | Bare returns ''; hypothesis/verdict helper returns 'high confidence' | OK |
| G5.10 numeric conversion error | FR-03 | Unsupported digit conversion/limit | Digit-run input for which baseline int raises ValueError | Conversion exception | Preserve baseline exception and dispatch error handling; do not add new confidence fallback or score | OK |
| G5.11 frontmatter absent | FR-03 | Empty/minimal plain text | text='' or 'a' | Leading startswith False | Return input unchanged | OK |
| G5.12 leading frontmatter | FR-03 | Typical leading literal block | text=' \n---\nx: 1\n---\nbody' | Split count 3 | Return suffix '\nbody'; preserve leading-whitespace detection | OK |
| G5.13 malformed unclosed block | FR-03 | Opening without second literal delimiter | text='---\nx: 1' | Split count below 3 | Return whole original string unchanged | OK |
| G5.14 literal sentinel collision | FR-03 | Delimiters not standalone YAML | text='---x---body' | Split count 3 | Return 'body'; do not replace literal split with YAML/line parser | OK |
| G5.15 extra literal delimiters | FR-03 | Repeated delimiters | text='---x---body---tail' | maxsplit=2 | Return 'body---tail', not last fragment | OK |
| G5.16 nonleading marker | FR-03 | Legitimate body delimiter | text='body\n---\nx---z' | Leading startswith False | Return entire input unchanged | OK |
| G5.17 absent section | FR-03 | No matching heading | text='plain', heading='Notes' | Search False | Extract '' | OK |
| G5.18 empty section | FR-03 | Matching heading with no body | text='## Notes\n## Other\nx' | First match; next heading immediate | Extract ''; do not select a later repeated Notes | OK |
| G5.19 minimal section | FR-03 | Case-insensitive first heading | text='## nOtEs\na' | Match True | Extract 'a' | OK |
| G5.20 section termination | FR-03 | Typical next heading | text='## Notes\na  b\n## Other\nc' | Next-heading guard True | Extract 'a b'; exclude next section | OK |
| G5.21 section to EOF | FR-03 | No next heading | text='## Notes\na  b\n' | Next-heading guard False | Extract 'a b' through EOF, then cap | OK |
| G5.22 repeated heading | FR-03 | Sentinel/repetition | text='## Notes\nfirst\n## Notes\nsecond' | First match only | Extract 'first'; no merging/reordering | OK |
| G5.23 zero-cap helper input | FR-03 | Existing slicing boundary | extract_section('## Notes\na','Notes',0) | [:0] | Return ''; do not reject or reinterpret cap | OK |
| G5.24 negative-cap helper input | FR-03 | Existing Python slice behavior | Same body='abc', cap=-1 | [:-1] | Return 'ab'; no new validation beyond existing helper contract | OK |
| G5.25 cap-minus-one | FR-03 | Below each current cap | Repeated 'é' length 31/119/199/239/299/319/599 for k=32/120/200/240/300/320/600 | Length below k | Retain all k−1 code points for applicable field | OK |
| G5.26 cap | FR-03 | At each current cap | Repeated 'é' length 32/120/200/240/300/320/600 | Length equal k | Retain k code points unchanged | OK |
| G5.27 cap-plus-one | FR-03 | Above each current cap | Repeated 'é' length 33/121/201/241/301/321/601 | Length above k | Retain first k code points; byte length may be 2k | OK |
| G5.28 whitespace before cap | FR-03 | Legitimate collapsed text | section=' a   b ', cap=3 | Collapse then slice | Return 'a b', not first three raw characters | OK |
| G5.29 YAML escaping | FR-03 | Empty/quotes/backslashes/Unicode | scalar='', 'a"b', backslash, 'é' | Existing str/escape chain | Double-quote; escape backslashes before quotes; preserve Unicode and existing newline handling; do not add serializer policy | OK |
| G5.30 timestamp seam | FR-03 | Generated supplied or clock patched | generated fixed versus absent/falsy | Existing default gate | Supplied value retained; fallback uses effective existing per-module clock seam; freeze identically for parity | OK |
| G5.31 argument conversion | FR-03 | elapsed absent/falsey/invalid | 0, None, 'bad' | Existing int/default and except TypeError/ValueError | Keep 0 fallback and per-recipe defaults; preserve nonzero conversion behavior | OK |
| G5.32 bare finding acceptance | FR-03 | Structural/non-row and valid row | No pipe; width<5; invalid ID; empty claim; valid F-1 row | Existing row guards | Skip existing structural/invalid rows; append every valid row in order without scoring/dedup | OK |
| G5.33 bare severity/cite policy | FR-03 | Alias versus unknown and empty cite | critical/unknown; cite='none' versus 'x:1' | Existing lookup/membership | Preserve severity aliases/default med and empty-cite sentinel 'none'; retain other trimmed cite | OK |
| G5.34 table block reset | FR-03 | Pipe header before divider and non-pipe break | header -> divider -> data -> plain -> pipe | Existing saw_divider transitions | Skip pre-divider header; accept data after divider; reset on non-pipe and require next divider | OK |
| G5.35 table empty/trailing cells | FR-03 | Empty row or trailing pipe spaces | cells all removed versus nonempty prefix with empty tail | Existing pop/empty guards | Preserve current trailing-empty removal and structural-row skip, not a new row filter | OK |
| G5.36 findings widths | FR-03 | Width 1, 2, 3, 4 and over-wide | a; a/b; a/b/c; a/b/c/d; a/b/c/d/e | Existing positional conditions | Missing fields ''; fourth+ cells joined ' / ' into action; retain row order/caps | OK |
| G5.37 hypothesis width one | FR-03 | Minimal data row | cells=['a'] after divider | width==1 | Cause='a'; evidence/confidence/next-step empty | OK |
| G5.38 hypothesis width two | FR-03 | Two cells | ['a','b'] | width==2 | Cause='a', next-step='b', evidence/confidence empty | OK |
| G5.39 hypothesis width three | FR-03 | Three cells | ['a','b','c'] | width==3 | Cause='a', evidence='b', next-step='c', confidence empty | OK |
| G5.40 hypothesis width four | FR-03 | Four cells | ['a','b','73','c'] | width==4 | Cause/evidence/confidence/next-step preserve current mapping | OK |
| G5.41 hypothesis width five | FR-03 | Canonical width | ['a','b','c','73','d'] | width>=5 | Join evidence 'b \| c' using literal pipe separator; confidence='73', next-step='d' | OK |
| G5.42 hypothesis width over five | FR-03 | Accumulation/overflow width | ['a','b','c','d','73','e'] | width>=5 | Join all middle evidence with ' \| '; tail-anchor confidence and next-step; cap locally | OK |
| G5.43 verdict empty | FR-03 | Empty section | section='' or whitespace | Empty True | parse_verdict returns ('','','') | OK |
| G5.44 verdict separator | FR-03 | Each existing rationale separator | 'yes 73 — why', '--', spaced '-', or ': ' equivalent | First separator present | Head label/confidence separate from capped rationale; retain recognized separator variants | OK |
| G5.45 verdict no separator | FR-03 | Head only | 'yes 73' | Separator absent | label='yes', confidence='73', rationale='' | OK |
| G5.46 verdict label policy | FR-03 | Known alias, unknown label, no letter prefix | 'PASS', 'novel', '73' | Alias hit/miss/no match | Map known alias; preserve capped unknown 'novel'; empty label if no initial letter-run | OK |
| G5.47 verdict confidence zone | FR-03 | Rationale contains digits only | 'yes — needs 100 tests' | No digit in head | confidence='', rationale retained; do not mine rationale for confidence | OK |
| G5.48 verdict notes folding | FR-03 | Notes/Gaps/Concerns and empty variants | Three headings present; one may be empty | Per-heading nonempty guard | Extract first of each heading; concatenate nonempty parts in Notes/Gaps/Concerns order with pipe separator, cap 600 | OK |
| G5.49 parse-error recovery absent | FR-03 | No recipe-specific structure | Bare no findings/verdict; findings no rows/notes; hypothesis no rows/notes; verdict no label/rationale/notes | Recovery False | Existing recipe-specific error; empty text; salvaged=False | OK |
| G5.50 parse-error recovery present | FR-03 | Any accepted recipe structure | findings or verdict; table rows or notes; verdict label/rationale/notes | Recovery True | Existing render with salvaged=True; dispatcher policy still decides promotion | OK |
| G5.51 success freeform fallback | FR-03 | Success with no accepted structure | nonempty unstructured body | Existing success fallback | Bare capped verdict/placeholder; findings/hypothesis capped Notes/placeholder; verdict uncertain+capped rationale/placeholder | OK |
| G5.52 success structured | FR-03 | Valid existing structure | status=success with rows/sections | No freeform fallback | Render preserved fields/order/defaults with salvaged=False | OK |
| G5.53 renderer row/placeholder | FR-03 | Empty versus nonempty parsed rows | table [] versus [row1,row2] | Existing renderer branch | Preserve current empty placeholder row for table recipes and original row enumeration; no synthesized worker records | OK |
| G5.54 renderer field type | FR-03 | Bool/int/other metadata | False, 0, 'é' | Existing bool-before-int checks | Preserve lowercase boolean, integer and yaml_str output with existing key order | OK |
| G5.55 exported lookup seam | FR-03 | Supported module helper patched | Existing module iso_now/section helper/default constant seam | Existing effective lookup | Preserve exported names, __all__, default binding and effective patch behavior with only tiny adapters if required | OK |

### G6 — Distribution parity and release readiness (FR-05/FR-12)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G6.1 package baseline exists | FR-05/11 | Zero baseline records | manifests/hashes absent | False | BLOCKED C05; cannot assert parity | OK |
| G6.2 unchanged resource parity | FR-05 | Minimal unchanged resource | One packaged template unchanged | Hash/member equal | Preserve it in direct wheel, sdist and sdist-derived wheel where baseline packaging includes it | OK |
| G6.3 normal authorized deltas | FR-05 | Typical scoped source changes | C03 helper/import payload hashes change | Explicit path ledger matches candidate | Accept explained source delta, preserve distribution scope and unaffected resources | OK |
| G6.4 unexpected resource loss | FR-05 | Large archive hides one missing resource | 1000 members; one unchanged template absent | Parity False | Block readiness; no blanket resource exclusion or line-saving offset | OK |
| G6.5 metadata/container differences | FR-05 | Sentinel nondeterminism | Archive timestamp/generated metadata differs | Explained-only allowance | Enumerate attributable reasons; unexplained metadata/member changes block | OK |
| G6.6 supported legacy invocation | FR-05 | Legitimate consumer discovered | Supported setuptools caller found | Retirement eligibility False | Retain C05; explicit scope/compatibility decision required | OK |
| G6.7 wheel-from-sdist | FR-05 | Direct wheel passes, sdist wheel differs/fails | Missing installed plugin resource or build failure | Required gate False | Block readiness; direct-wheel success alone is insufficient | OK |
| G6.8 CLI/plugin/resources | FR-05/12 | Entry point or discovery failure | superclaude works, ic or pytest plugin/resource check fails | False | Block readiness; do not publish or call package parity PASS | OK |
| G6.9 build environment parity | FR-05 | Tool versions differ | Baseline/post backend versions unequal | Comparison invalid | Re-establish comparable evidence with same recorded tool versions before parity decision | OK |
| G6.10 release check results | FR-12 | All observed gates satisfactory | All ten eligible/verified; targeted/full/architecture/format/package checks observed | True | May report implementation readiness; publication/commit/version still separately authorized | OK |
| G6.11 skipped/not-run evidence | FR-12 | One required gate unexecuted | package install check=not run | False | Pending, not PASS; release not ready | OK |
| G6.12 new failure | FR-12 | Regression appears | Baseline passes, changed suite fails | False | Block readiness and report; do not opportunistically broaden cleanup | OK |
| G6.13 pre-existing failure | FR-12 | Identical baseline failure | Same command/context/failure before and after | Baseline exception recorded | Record explicitly; do not label failing check PASS or assert all tests green; still satisfy affected behavior gates | OK |
| G6.14 Black resolution | FR-08 | Direct dev requirement removed | Locked dev resolution no longer needs removed extra | Expected dependency delta | Update lock minimally; preserve Ruff policy and Black allow-list baseline | OK |
| G6.15 Black transitive remainder | FR-08 | Legitimate remaining dependency | Black still present transitively | Not automatically a failure | Report dependency reason; do not forcibly uninstall or remove allowance | OK |
| G6.16 unrelated lock churn | FR-08/12 | Noncandidate dependency upgrade | Ruff or unrelated packages unexpectedly change | Scope guard False | Reject unrelated churn; retain current pins/policies | OK |
| G6.17 held/rejected diff | §1.2/FR-12 | Tempting additional removal | Held roadmap helpers or preflight writer touched | Scope guard False | Exclude/restore only authorized candidate edits as separately authorized; no full-release success with scope drift | OK |
| G6.18 planning endpoint | FR-12/§10 | Spec review/tasklist/pre-reflection only | Implementation checklists unchecked | Planning only | No runtime PASS, shipping, version assignment, publishing or implementation execution implied | OK |
| G6.19 packaging-only pair | FR-05/§4.2 | Minimal controlled comparison | Same source/dependencies/tools; only setup.py and MANIFEST.in removed | Pair valid | Compare member/payload/resource identity with only retired-file and enumerated metadata exceptions before broader edits | OK |
| G6.20 contaminated packaging pair | FR-05/§4.2 | Source or dependency already changed | C03 source or Black requirement differs between arms | Pair invalid | Recreate controlled pair using safely isolated identical snapshots, not rollback of unrelated work; C05 remains blocked without valid pair | OK |

Boundary completion check: G1=12, G2=16, G3=18, G4=22, G5=55 and G6=20 rows (143 total). All seven columns are populated. There are no unresolved GAP rows. This is a manual completeness check of the documented guard families, not an automated test run. New branches found during implementation require extending cases/evidence, not silently weakening these obligations.

## 7. Whittaker adversarial attacks — exact template, all five methodologies

These are simulated pre-correction attacks/clarification probes, with before/after traces. 'Fails when' describes the challenged interpretation, not a claim that the implementation was run or that every probe exposed a new defect.

### W1 — FR-2.1 Zero/Empty Attack

I can break this specification by **Zero/Empty Attack**. The invariant at **FR-11 candidate eligibility** fails when **an empty evidence ledger or an empty search result is mistaken for proof that requirement ownership and caller checks passed**. Concrete attack: **before: C01 eligibility ledger has zero rows and no observed live-owner tests; step 1: interpret zero currently listed callers as zero possible consumers; step 2: remove helpers and requirement-bearing assertions; after: coverage can disappear without any recorded passing migration evidence**.

Probe severity MINOR / priority High; disposition rejected by the existing FR-11 blocker, reinforced by R1. This is a guarded counterfactual, not a newly discovered defect or observed deletion. Zero payload succeeds with B=0 under G4.1; zero workers preserve count under G2.10; zero baseline records block under G6.1. R6 separately fixes the count's not-yet-computed initialization, including encoding-error lifecycle.

### W2 — FR-2.2 Divergence Attack

I can break this specification by **Divergence Attack**. The invariant at **FR-05 baseline/post payload parity** fails when **authorized source cleanup changes payload hashes but only metadata exceptions are permitted**. Concrete attack: **before: baseline wheel includes the original normalize source and packaged source copy; step 1: perform authorized C09 fallback replacement; step 2: build post-change artifacts; after: source hashes diverge despite unchanged intended distribution scope, so literal whole-payload equality rejects the required implementation**.

Severity MAJOR; priority High; disposition resolved by R5's per-path candidate ledger and unchanged-resource checks. Actual artifact contents and builds remain unverified; the packaged-copy path is an explicit conditional obligation, not a claim about a built archive.

### W3 — FR-2.3 Sentinel Collision Attack

I can break this specification by **Sentinel Collision Attack**. The invariant at **FR-06 sanitizer no-op/delimiter selection** fails when **'valid frontmatter' is read as parsed YAML rather than the baseline leading startswith sentinel**. Concrete attack: **before: file contains '  ---not-yaml'; step 1: an extraction adds a YAML-validity check; step 2: it treats the input as malformed and rewrites or rejects it; after: baseline return 0 with unchanged contents has become a write/error despite the preservation requirement**.

Severity MAJOR; priority High; disposition resolved by R2. Registry None/absent/invalid distinction withstands the separate sentinel probe under G2; no removal of None support is authorized.

### W4 — FR-2.4 Sequence Attack

I can break this specification by **Sequence Attack**. The invariant at **FR-01/04/10, FR-11 coverage migration before deletion** fails when **naming a future live owner is mistaken for completion and deletion precedes observed passing migration assertions**. Concrete attack: **before: helper tests carry NFR-009 assertions and live-owner validation is only planned; step 1: list config/executor as owner; step 2: delete helper and its requirement-bearing tests; after: green remaining tests could omit the requirement entirely, even though the planned owner never demonstrated it**.

Severity MINOR clarification of an already-prohibitive gate; priority High; disposition R1 makes the existing ordering explicit. This sequence was already disallowed by FR-11; no observed coverage gap or successful migration is claimed.

### W5 — FR-2.5 Accumulation Attack

I can break this specification by **Accumulation Attack**. The invariant at **FR-03 cap parity and §2 C-versus-B accounting** fails when **an extracted cap is applied to UTF-8 bytes instead of collapsed text code points**. Concrete attack: **before: verdict rationale is 301 copies of 'é'; step 1: baseline collapses and slices at 300 code points; step 2: replacement slices at 300 bytes; after: baseline keeps 300 characters/600 bytes while replacement keeps 150 characters/300 bytes, silently reducing accepted text**.

Severity MINOR clarification because the preservation/units requirements already rule out this change; priority Medium; disposition R4's cap inventory/examples and G5.25–27 make the oracle concrete. No new maximum, scoring logic or overflow handling policy was introduced.

## 8. Re-review and final synthesis

Final synthesis is completed only after the populated guard table above. The revised specification was re-read and re-reviewed against R1–R6, the six guard families, state lifecycle, quantity units, all ten candidate fences and the source-derived examples. The final bounded re-review also incorporated the coordinator's source-order and packaging-pair clarifications: FR-07 explicitly rejects encode-as-call-argument before parent setup; FR-05/§4.2/NFR-05 separate the controlled packaging-only pair from final-release delta accounting. The literal-frontmatter example and exact sanitizer regex were reconciled, and escaped pipe separators keep the boundary tables seven-column Markdown.

### Re-review checklist

| Check | Observed review result | Remaining implementation obligation |
|---|---|---|
| C01–C10 identity and estimate | Ten candidates retained; 488 lines remains an estimate, not a quota | Measure actual source/config/docs/test/dependency deltas |
| Runtime coverage migration | Explicit live-owner passing assertions precede deletion; no owner presumed proven | Candidate-specific eligibility rows and observed migrated boundary checks |
| Architecture | No pipeline-to-roadmap import, runner extraction or new abstraction authorized | Import/cycle checks and both validator integration paths |
| Recipe extraction | Exports/patch seams, caps, confidence/frontmatter/section distinctions and local parser/salvage policy retained | Fixed-clock differential/golden cases and existing no-judging coverage |
| Atomicity | Normalize/reduce mechanics only; parent/encoding/exception/cleanup boundaries explicit | Failure injection and transaction-aware structural tests; no preflight changes |
| Concrete fallback | None/absent/invalid valid-recipe branches and registry independence explicit | Resolver and dispatcher checks, including empty N and no false salvage |
| Package parity | Packaging-only identical-snapshot pair scheduled before other edits or via isolated copies; final candidate-attributed deltas, unaffected hashes, wheel-from-sdist and installed resources all required | Real paired baselines/builds, final manifest accounting, installs/CLI/plugin checks |
| Black | Lock update required; direct dependency removal only; baseline allowance preserved | Clean locked resolution, minimal diff and transitive reason if applicable |
| Held/rejected scope | All named boundaries unchanged by the spec corrections | Explicit held/rejected diff snapshot and scope review |
| Evidence honesty | Planning review separated from execution readiness; no fabricated tests/removal proof | Command/context/result ledger and independent implementation QA |

### Consensus

- The existing audit/debate input is substantial enough for a scoped refactoring plan; it should not be regenerated as a new feature or general platform.
- Keep all ten candidate gates and all held/rejected exclusions. Reduced measured savings are acceptable; broadening deletion to compensate is not.
- Migration is an eligibility gate, not a promise that behavior is covered somewhere. Packaging and transaction guarantees require real evidence during execution.
- Shared implementation must not erase module seams or move policy across recipe/runner boundaries. No new dependency, framework or state machine is needed.
- A codename is sufficient. No package version, tag, PR, publication or implementation execution is implied by this review.

### Disagreements and resolution

- **Fowler versus Newman lens:** minimizing aliases would reduce code, but public/exported and effective monkeypatch seams may matter. Resolution: retain only required tiny adapters/re-exports, and block supported-contract conflict instead of adding a broad compatibility layer.
- **Nygard versus simplicity lens:** stronger cleanup/durability might sound safer, but changing syscall ordering, catch domains or directory-fsync policy is outside a preservation-only cleanup. Resolution: preserve baseline precisely; document existing orphan-temp possibility rather than silently strengthen policy.
- **Hightower versus literal package identity:** unchanged byte hashes everywhere would be simple to state but impossible after scoped code changes. Resolution: enumerate candidate-attributed source/test/config deltas while retaining strict unaffected-resource identity and direct/sdist-wheel comparison.
- **Crispin versus line-saving objective:** migrations and evidence can increase tests/documentation. Resolution: coverage and reproducibility outrank net-line savings; no broad test deletion.

These are tensions between simulated analytical lenses, not statements by real experts.

### Honest quality assessment and disposition

**Final specification status: REVIEWED — READY FOR TASK PLANNING, WITH IMPLEMENTATION ELIGIBILITY GATES PENDING.** There is no unresolved product/scope decision discovered by this bounded review; therefore the specification is not marked BLOCKED. The implementation and release are **not verified or ready** by this document. If future source/evidence exposes a supported consumer, unknown requirement owner, missing baseline or failing migration, the exact candidate is BLOCKED under FR-11 and the full release cannot be called complete without an explicit scope decision.

- **Clarity:** improved by exact sanitizer/transaction boundaries, current cap examples and explicit evidence ordering.
- **Completeness:** sufficient to construct a bounded tasklist for the ten candidates; future current-revision caller checks, ownership evidence and executable cases remain mandatory, not presumed results.
- **Testability:** concrete branch oracles and package/failure-injection gates are specified. No tests/builds were run in this pass.
- **Consistency:** the packaging hash contradiction was resolved with constrained deltas; counts C/B/N and transient initialization now have explicit domains.
- **Residual uncertainty:** source inspection is scoped and single-agent; eleven lenses do not equal eleven independent reviewers. Existing independent input was represented by the spec rather than re-executed. External consumer absence and safe deletion are not proven.

All six findings are resolved in the written specification, with no unresolved MAJOR/CRITICAL specification gap in this bounded pass. No quantitative quality score is claimed. Downstream work remains the existing tasklist/pre-reflection planning contract; implementation checklists must remain unchecked in this planning handoff.

