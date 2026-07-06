---
name: post-release-update
description: "DEPRECATED compatibility alias for /sc:post-release. Kept for one release/eval cycle so existing users invoking /post-release-update <version> continue to work; delegates to the new sc:post-release-protocol. Prefer /sc:post-release <version>."
allowed-tools: Read, Skill
argument-hint: "<version> — an existing release tag (e.g. v1.4.1)"
---

# post-release-update (Deprecated Compatibility Alias)

This skill is a **deprecated compatibility wrapper** retained for one release/eval cycle so existing invocations of `/post-release-update <version>` continue to work without breakage. It does **not** duplicate the five-workstream post-release protocol body — it is a delegation stub.

The full post-release follow-through protocol now lives behind the **`/sc:post-release`** command. To run it, invoke the new protocol skill:

> Skill sc:post-release-protocol

That protocol owns the Wave 0–5 behavior: tag-anchored scanning, ground-up vs additive mode detection, install-surface classification (`vm-e2e` / `local-deploy` / `package` / `no-install-surface`), the five workstreams A–E, golden-rule honesty discipline, the `post-release-report.md` + `post-release-manifest.json` outputs, the `SC:POST-RELEASE:RUN` / `SC:POST-RELEASE:RESULT` machine-readable headers, and the return contract.

New invocations should use **`/sc:post-release <version>`** rather than `/post-release-update`.

## Related commands

- `/sc:post-release <version>` — the current, supported post-release follow-through surface.
