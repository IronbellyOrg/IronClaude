# Summary check: five file:line claims in summary.md

Checker: one fresh-context sub-agent that did not write summary.md. The harness blocked sub-agent file writes, so the worker saved the checker's returned text here unchanged except for this provenance line.

## Method
I checked 5 claims from `summary.md`, against the read-only clone `/tmp/tuibbs-review` at a6d7e7f. For each one I opened the cited lines with Read and compared them to what the summary says. When the cited lines did not cover the whole claim, I searched the clone to find where the rest really is. For claim 3 that meant checking where the default group resolver is installed and whether any production code passes a real one. For claim 5 it meant searching `docs/` for "hobby". Grades: PASS means the lines match the claim; MINOR means the claim is true but the lines or wording are loose; FAIL means the claim is false or not at the cited place. No files in the clone or the repo were changed, and no secret files were opened.

## Results

| # | Claim | Cited location | What the lines actually say (at most 3 quoted lines) | Grade |
|---|---|---|---|---|
| 1 | The plugin contract is one unary call with opaque bytes, so plugins cannot draw a screen | `proto/v1/plugin.proto:61-68` | `service ModuleService {` ... `rpc Dispatch(ModuleCall) returns (ModuleResult);` (lines 61, 67). The "opaque bytes" are elsewhere: `bytes args = 4;` (line 89) and `bytes payload = 2;` (line 108). | MINOR. The single unary call is at 61-68, but the opaque-bytes half of the claim is at 86-89 and 106-108. "Cannot draw a screen" is a fair inference, not something the file states. |
| 2 | Contains the rule "FR-X-13: no write-back" | `internal/serve/menu.go:637-640` | `// openWatchCmd subscribes the observing principal to sessionID through the SAME` / `// read-only Registry.Subscribe sink path as any watcher (FR-X-13: no write-back).` (lines 637-638) | PASS |
| 3 | The group resolver returns an empty set, so group-membership rules are always false | `internal/auth/provider.go:244-257` | `// installs a no-op resolver returning an empty set; the seam exists for` (line 246); `func (noGroups) ResolveGroups(context.Context, int64) ([]string, error) { return nil, nil }` (line 257). `NewProvider` falls back to `noGroups{}` when no resolver is given (line 350). No production code passes a real resolver; only tests set `Groups`. | PASS. "Always false" is an inference from the empty `Principal.Groups`, consistent with lines 244-248. |
| 4 | The module contract is frozen additive-only | `internal/plugin/dispatch.go:53-62` | `// Per M5-D22 (OPS-009 SDK freeze) the ModuleDispatcher contract is part` / `// of the surface frozen for v1` ... `// Additive evolution (a new field with a zero-value` / `// default, a new tier) is the only backward-compatible change` (lines 55-59) | MINOR. The lines match the claim as briefed. But summary.md line 9 calls this TUIBBS's "own JSON, additive-only habit", and these lines describe a Go interface and its protobuf form, not JSON. |
| 5 | The project is described as hobby / dogfood-only | `docs/scope.md:17-18` | `TUIBBS **v1 is a dogfood-only, AI-built multi-tenant SSH terminal platform**.` / `The sole intended v1 user is the AI engineering team building TUIBBS` (lines 17-18) | MINOR. "Dogfood-only" is at 17-18, but "hobby" is not in `scope.md`. It is in `docs/governance.md:90` ("not required for this hobby project") and several ADR and technical-reference docs. |

Verdict: PASS (no FAIL rows; rows 1, 4 and 5 are MINOR)

## Self-Audit
- I read every cited range directly. For each MINOR row I also found where the missing part really is: `plugin.proto:89` and `:108`, and `docs/governance.md:90`.
- For claim 3 I followed up beyond the cited lines: the default `noGroups{}` is installed at `provider.go:350`, and a search for `Groups:` across the clone found only tests and copy sites, no production wiring of a real resolver.
- I did not check `merged-requirements.md:328`, any other citation in the summary, or whether the plugin host is actually wired up. Those were outside this 5-claim sample.

## Worker note
Minor findings are recorded here as notes and were not fixed in summary.md: the JSON content type is at `internal/plugin/dispatch.go:146-151` (cited in assumptions.md row 3), the opaque bytes at `proto/v1/plugin.proto:89` and `:108`, and "hobby" at `docs/governance.md:90`.
