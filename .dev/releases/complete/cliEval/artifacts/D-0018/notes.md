# D-0018 — implementation notes

## Design choices

**Post-expansion eval count.** Two interpretations of "eval count" were
candidate: raw `evals[]` length vs. post-parameterize-expansion length.
We chose post-expansion because the operator-facing question is "how
many evals will run", and the parameterize block exists precisely so
one manifest row materialises N runs. Documenting the choice in the
spec means future contributors do not need to reverse-engineer it from
test expectations.

**SuiteLoader funnels every manifest.** `summarize_suites` calls
`SuiteLoader.load` for each discovered file rather than a stripped-down
schema-only reader. This costs a tiny bit of work (a full gate chain
per manifest) but eliminates the risk of `eval list` exposing a
malformed manifest that `eval run` would reject. The two surfaces stay
in sync by construction.

**`--suites-dir` instead of `--config`.** The roadmap COMP-005
`EvalConfig` does not yet expose a `suites_dir` field (it ships an
empty `paths` mapping by default). Rather than retrofit that field
here, the flag accepts an explicit directory override. When `EvalConfig`
grows a `suites_dir` field in a later milestone, the default lookup
can be re-routed through it without breaking the CLI surface.

**Empty-directory case is silent + exit 0.** FR-CLI2 AC explicitly
requires the empty case to exit 0. We considered emitting an exit-1
"empty suite directory" diagnostic but rejected it because (a) a fresh
checkout legitimately has no built-in suites at M1, and (b) callers
piping `--json` to `jq` would prefer an empty array to a non-zero exit.

## Things explicitly NOT done

- No filtering by category, capability, or name. FR-CLI2 is
  enumeration-only.
- No machine-readable error format for the exit-2 path. The stderr line
  is intentionally human-readable; future tooling that needs structured
  errors should consume the JSON payload from `eval doctor` or a
  dedicated `eval validate` command.
- No caching. `summarize_suites` re-reads every file on every call.

## Follow-ups

- When `EvalConfig` grows a `suites_dir` field, change
  `_DEFAULT_SUITES_DIR` to resolve through it.
- When built-in suites land under `src/superclaude/cli/eval/suites/`,
  add a non-empty default-listing assertion to the test suite.
