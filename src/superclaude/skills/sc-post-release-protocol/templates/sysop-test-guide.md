<!--
Template: sysop/administrator-facing e2e human-test guide.
Only author these if sysop-only capabilities actually exist (see workstream E). If none exist, do NOT create this file — record "no sysop surface" instead.
A HUMAN runs this by hand. Every "expected result" MUST come from real code (cite it), never a guess.
Replace <bracketed> text; delete these comments.
-->

# Sysop E2E Test Guide — `<admin capability name>` (`<version>`)

- **Capability:** `<what this admin/operator feature does, one line>`
- **Audience:** system operator / administrator
- **Gate:** `<how this capability is gated — role check, --admin/--debug flag, env var, privileged command. cite the gating code file:line>`
- **Source of truth:** `<file:line / command derived from>`
- **Est. time:** `<minutes>`

## Preconditions

<Concrete state required, INCLUDING the privilege/gate that unlocks this capability.>

- `<version>` installed and reporting correctly
- **Privilege/gate satisfied:** `<how the operator enables/enters the gated mode — the real mechanism>`
- `<required config / access / target host>`
- `<any safety note: this touches admin state, run on a non-production target, etc.>`

## What you're verifying

<Plain-language statement of the admin capability and what "working" means, including that the gate correctly permits the authorized operator.>

---

## Steps

### Step 1 — Enter/enable the gated capability

**Do:**

```bash
<exact command / flag / role assumption that unlocks the capability>
```

**Expected result:** `<the capability becomes available / the gate opens — precise, checkable. Source: <gating code file:line>.>`

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Step 2 — `<admin action>`

**Do:**

```text
<action>
```

**Expected result:** `<precise outcome derived from <source citation>>`

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

<!-- add steps as needed -->

---

## Negative / gate check (recommended)

Verify the capability is **not** available without the privilege — a gate that doesn't gate is a finding.

| Try this (without privilege) | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `<invoke the admin action as an unprivileged user>` | `<denied / hidden / errors as designed>` | `<gating file:line>` | ☐ |

## Cleanup

<Return to a clean state: exit the gated mode, revert any admin state changed, restore config.>

## Overall result

☐ **PASS** — admin capability works and is correctly gated for `<version>`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `<version / commit>`
