# Wave 1.5 Branch A (release-doc lookup) — returned by troubleshoot-analyst

```json
{"hit": false}
```
degraded: true (auggie not in the worker roster; Grep/Glob only)

Notes returned with the result:
- `.dev/releases/` (current/ only; complete/ absent in this worktree): no ccsession / alias proxy / setup_shim hits; "shim" hits there mean code-compatibility shims.
- `.dev/specs/ccsession-native-install.md:48` puts "the model shim's runtime behavior" out of scope; `:309` "shim not required" for naming.
- `.dev/specs/ccsession-native-install-design.md:307` lists "Gateway / shim / `lsof`" under Non-goals.
- `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:15` shows several Orca sessions sharing one shim (port 4111); `:45` a supervised worker used it too. Evidence that sharing is normal; no lifecycle rule.
