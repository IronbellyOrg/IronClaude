# Persisted by the orchestrator from reviewer-3's returned card (reflect-reviewer, opus, persona refactorer). Claims condensed; IDs, evidence, classes, severities and recommendations kept.
reviewer: reviewer-3
persona: refactorer
model: opus
verdict: revise   # 1 blocking (R3-1), 8 minor; scope and structure otherwise sound
self_reported_confidence: 0.84
scope_check: {confined_to_data_plus_one_shared_path_fix: true, new_mechanism: none, forbidden_file_edits: none, claude_dir_staging: none, python_fix_converges_all_failure_paths: true}
findings:
  - id: R3-1
    claim: "The manual proof isolates only HOME; CLAUDE_CONFIG_DIR (claude CLI, install_mcp) and XDG_CONFIG_HOME (Ponytail ledger/config) would bypass it if exported."
    evidence: ["TASK-WF-closeIronbellyOr-20261104-124207.md:29,79,103", "docs/getting-started/installation.md:362-366", "src/superclaude/cli/install_mcp.py:721-726"]
    deviation_class: drift
    severity: blocking   # orchestrator note: both variables verified unset in this worker (12:48Z); fix is one env -u prefix
    recommendation: "Run every manual step as env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME HOME=$H ...; log that neither variable is set inside."
  - id: R3-2
    claim: "'At most 5 changed lines' ambiguous (4 insertions + 3 deletions)."
    evidence: ["TASK-WF-closeIronbellyOr-20261104-124207.md:57,64", "merged-requirements.md:111"]
    grounding_gap: counting rule
    severity: minor
    recommendation: "numstat <= 5 insertions and <= 5 deletions, all inside install_plugins."
  - id: R3-3
    claim: "Dependencies stricter than needed: Task 2 independent of Task 1; Task 3 needs Task 1 only."
    evidence: ["TASK-WF-closeIronbellyOr-20261104-124207.md:55,73,96"]
    grounding_gap: dependency precision
    severity: minor
    recommendation: "Sequential execution is still safe; no change needed to run."
  - id: R3-4
    claim: "Docs edits are not verified: tests/docs/test_retired_docs_absent.py reads every docs/**/*.md; pre-commit markdownlint --fix runs on installation.md."
    evidence: ["source.md:1", "tests/docs/test_retired_docs_absent.py:39-44", ".pre-commit-config.yaml:74-88"]
    deviation_class: drift
    severity: minor
    recommendation: "Run uv run pytest tests/docs and markdownlint on installation.md."
  - id: R3-5
    claim: "Task 3's 'every behaviour claim matches the lite facts' cannot hold: Task 3 requires claims outside the facts block (bare /ponytail, new-session reset, project settings precedence, PONYTAIL DEFAULT SET, node, upgrade path); the reset clause was grounded only on the off path."
    evidence: ["TASK-WF-closeIronbellyOr-20261104-124207.md:19-24,80-83,89", "merged-requirements.md:140"]
    grounding_gap: source for non-off reset
    severity: minor
    recommendation: "Ground each extra claim in upstream or brainstorm lines, or drop it."
  - id: R3-6
    claim: "Task 1 JSON shape vs file style: existing marketplaces are expanded over six lines; appending edits the prior last line's comma."
    evidence: ["src/superclaude/cli/user_settings_defaults.json:10-13,28-49", "TASK-WF-closeIronbellyOr-20261104-124207.md:39,47"]
    grounding_gap: formatting
    severity: minor
    recommendation: "Use the expanded form; diff = three entries + three trailing commas."
  - id: R3-7
    claim: "Task 4 asks for a link to the installation section; Task 3 adds no heading."
    evidence: ["TASK-WF-closeIronbellyOr-20261104-124207.md:75,99", "docs/getting-started/installation.md:331"]
    grounding_gap: link target
    severity: minor
    recommendation: "Link the file (optionally the Step 3 anchor); add no heading."
  - id: R3-8
    claim: "Manual proof does not belong in the CHANGELOG task; the Orca step can eat 25 s of the 30 s budget, so M1a may time out for unrelated reasons."
    evidence: ["TASK-WF-closeIronbellyOr-20261104-124207.md:103-106", "src/superclaude/cli/install_user_setup.py:34-35,215-228,316-323"]
    grounding_gap: proof placement and budget
    severity: minor
    recommendation: "Record whether Orca was on PATH and the time used so a time-limit FAIL can be told apart."
  - id: R3-9
    claim: "./artifacts/ base path not spelled out."
    evidence: ["TASK-WF-closeIronbellyOr-20261104-124207.md:67,103"]
    grounding_gap: base path
    severity: minor
    recommendation: "Use the package artifacts/ folder."
verified_adherent: "Task 1 matches Design 3.1 with lite; fill semantics install_user_setup.py:36,150-164; no per-plugin code :266-284; test ranges accurate; T5c string matches :258; superseded package untouched; only installation.md:354 says 'six plugins'."
