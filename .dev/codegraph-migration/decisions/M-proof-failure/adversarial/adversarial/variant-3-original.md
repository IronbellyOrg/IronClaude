# Option C: split by failure class

- Integrity failure (hash mismatch or attestation failure): issue only, no branch, no PR (possible tampering; never put unverified hashes on a branch). Title "codegraph vX.Y.Z: integrity check failed".
- Behaviour failure (install, index, tools/list, drift): push the branch and open a DRAFT PR labelled `needs-codegraph-proof` with the failed stage and log tail, so a person can push a fix (for example an `MCP_TOOLS` or entry change) onto it.
- Infrastructure failure: neutral exit with a step summary and `::warning::`, no issue (retries next schedule), as Coder does.
- Rationale: matches the artifact to what a person can do next; keeps unverified bytes off branches.
- Cost: three paths to test instead of one or two.
