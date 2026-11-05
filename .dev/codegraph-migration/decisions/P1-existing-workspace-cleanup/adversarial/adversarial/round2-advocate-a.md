# Round 2: Advocate for Variant 1 (Option A), rebuttals

Sources re-checked read-only: `install_mcp.py:40-61,951-999,1316-1343`, `main.py:189-275`, `install_codebase_memory.py:74-86`.

## Responses to criticisms

**1. Serena is opt-in (C). Conceded.** `"required": False` (`install_mcp.py:60`) is true, so is the pin being identical to Coder's bundle argv, and so is the churn. A cannot tell a deliberate user registration from a Coder one, and removing an entry whose ownership it cannot prove breaks the goal's hand-off clause (X-004). Amended A: remove `codebase-memory-mcp` automatically, because it came from IronClaude's required phase (`main.py:254-262`). For a `serena` entry with an exact known shape, install prints one line: "Legacy Serena registration kept; remove it with `claude mcp remove serena --scope user`." I reject C's new `--retire-legacy` flag. A printed command gives the same consent at no code cost, and no existing consented path covers serena anyway (see New evidence). The Coder case goes to C's Phase 2 handoff.

**2. Order versus the upstream uninstall (B). Order conceded; keeping the module rejected.** Existing code runs the native uninstall first and registration cleanup second (`install_mcp.py:993-999`), so A must not reverse that. Amended A: when the receipt `~/.local/bin/.superclaude-codebase-memory.json` is present (kind B), A leaves that registration in place and prints `codebase-memory-mcp uninstall -y`, so the upstream tool runs in its normal order. Keeping the receipt-gated removal "behind consent" would keep the 759-line module, its supervisor and its tests alive. That spends real code on kind-B workspaces whose existence is UNVERIFIED, and B itself concedes its timeout is really 300 s (`install_codebase_memory.py:28`).

**3. Delete receipt and marker only after the binary is gone (C). Conceded.** Amended A: delete the receipt and the `.pending` marker only when `~/.local/bin/codebase-memory-mcp` is absent, and only when each is a regular, single-link file owned by the user. Otherwise list them. While the binary exists, the receipt is the only proof that IronClaude installed it, so deleting it early would destroy evidence the upstream path may need.

**4. Exceptions or Coder's 60 s kill skip the step (B, C). Resolved by placement, not by hope.** The step depends on nothing that earlier steps produce. Amended A: run it first in `install`, right after the `--list` branch returns (`main.py:93-187`), inside its own broad `try/except` that only warns. Its cost (two file reads, at most one 10 s CLI call) then comes before any slow step, so neither a later kill nor a later exception can skip it. If it is interrupted anyway, the next install retries it at no extra cost, because the absence check runs first.

## Updated assessment

- **B (narrowed):** The good part (IronClaude-owned receipt and marker) is now in A without keeping the module. What remains of B is automated binary removal, which is not worth its cost.
- **C (narrowed):** C has correctly moved to "automatic for codebase-memory, consent for serena". A now agrees, with a printed command in place of a new flag. The two remaining differences are flag versus printed command, and whether to add a dry-run.

## New evidence

- `superclaude mcp --uninstall` accepts only `--servers codebase-memory-mcp` (`install_mcp.py:1320-1324`). No consented removal path for serena exists today. C's split therefore needs either new code (a flag) or a printed `claude mcp remove` command. The printed command is the cheaper way to get the same consent.
- `install_mcp.py:993-999` confirms the order: native uninstall first, then registration cleanup.

## Updated per-point positions (changed only)

| Point | Preferred | Reason |
|---|---|---|
| C-001 | merge: A automatic for codebase-memory; serena kept and a removal command printed | Opt-in server, ownership cannot be proven |
| C-002 | merge: A for codebase-memory; serena printed; receipt and marker deleted once the binary is absent | Ownership plus C's ordering rule |
| C-006 | C's handoff for serena; A for codebase-memory | The bundle re-adds serena |
| C-008 | A (amended): a receipt present means registration kept and the upstream command printed | Keeps the existing order without keeping the module |
| X-004 | C | Coder-owned leftovers are handed off |
| A-002 | C for serena; A for codebase-memory | Shape does not prove consent for an opt-in server |
| A-003 | A, step placed first and wrapped | Removes the kill and exception risk |
| A-005 | B's order, delivered by A's skip-and-print | Matches `install_mcp.py:993-999` |
| A-006 | C's condition | Delete only after the binary is absent; otherwise list |
