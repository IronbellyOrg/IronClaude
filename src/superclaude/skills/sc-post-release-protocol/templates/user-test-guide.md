<!--
Template: user-facing e2e human-test guide.
A HUMAN runs this by hand. Every "expected result" MUST come from real code (cite it), never a guess.
One guide per user-facing capability (or cohesive group). Replace <bracketed> text; delete these comments.
-->

# E2E Test Guide — `<capability name>` (`<version>`)

- **Capability:** `<what this feature does, one line>`
- **Audience:** end user / operator
- **Source of truth:** `<file:line, command, or entry point this guide was derived from>`
- **Est. time:** `<minutes>`

## Preconditions

<Everything that must be true before starting. Be concrete.>

- `<version>` installed and reporting correctly (`<how to check — the project's own version command, e.g.`<binary> --version`→ <version>`>)
- `<required config / env / sample data / state>`
- `<permissions or access needed>`

## What you're verifying

<Plain-language statement of the capability and what "working" means for it.>

---

## Steps

<!-- Each step: an unambiguous action, then the exact expected result derived from code. Mark PASS/FAIL. -->

### Step 1 — `<action name>`

**Do:**

```bash
<exact command / click path the user performs>
```

**Expected result:** `<precise, checkable outcome — exact output, file created, state change. Derived from <source citation>.>`

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Step 2 — `<action name>`

**Do:**

```text
<action>
```

**Expected result:** `<...>` (source: `<file:line>`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

<!-- add steps as needed -->

---

## Edge cases (optional but recommended)

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `<bad input / boundary>` | `<how it should handle it>` | `<file:line>` | ☐ |

## Cleanup

<How to return to a clean state after testing (delete artifacts, reset config, etc.).>

## Overall result

☐ **PASS** — capability works as documented for `<version>`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `<version / commit>`
