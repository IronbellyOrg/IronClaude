# Input parse + STOP + package creation

## Source

Exactly one: existing file (`@path` unwraps) **or** non-empty leftover prompt.

## Validate first, then create

Validate every input and flag **before any write**. These STOPs create no package, no `source.md`, no yaml (chat only):
`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`.

`--output` is **retired**: any `--output` / `--output=…` token → STOP `E-LEGACY` ("`--output` removed; every plan is written to `.dev/tasks/to-do/<id>/`"). It is never parsed as a destination.

## Package identity

Every generation creates one **new** package under the current checkout: `.dev/tasks/to-do/<id>/`. Regeneration never reuses, merges into, or overwrites an existing package.

1. **Subject** — lower camelCase, **max 16** characters, no hyphens. Take the basename without extension (file source) or the inline prompt. Split into words with the regex `[A-Z]+(?![a-z])|[A-Z]?[a-z]+|[0-9]+` (ASCII only; every other character is a separator; camelCase and acronym boundaries split, so `authLogin` → `auth`,`Login` and `XMLParser` → `XML`,`Parser`). Lowercase each word, keep the first as is, capitalize the first letter of each later word, concatenate, truncate to **16**. If there are no words, or the first word starts with a digit, prepend the word `plan` (empty → `plan`; `2fa login` → words `2`,`fa`,`login` → `plan2FaLogin`). The result always matches `[a-z][A-Za-z0-9]{0,15}`.
2. **Timestamp** — current **UTC** `YYYYMMDD-HHMMSS`.
3. **ID** — `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`. The ID is the package directory name and the plan `slug`; it never changes after creation and is independent of the source's absolute path.
4. **Exclusive creation** — if `.dev/tasks/to-do/<id>` **or** `.dev/tasks/done/<id>` exists (`test -e` **or** `test -L`, so dangling symlinks count), do not touch it: retry with suffix `-2`, `-3`, … up to `-9` appended to the full ID. Create the leaf with plain `mkdir` (never `mkdir -p`, never `rm -rf`) so an existing leaf is a hard failure; only the parents (`.dev/tasks/to-do`) may be created with `-p`. If `-9` is also taken → STOP `E-PACKAGE-COLLISION` (no package created).

| Source or prompt | Subject |
|------------------|---------|
| `docs/PRD_User Auth.md` | `prdUserAuth` |
| `Add logout to the header and wire it to /logout` | `addLogoutToTheHe` (16-char cap) |
| `!!!.md` | `plan` (fallback) |
| `Ünïcode Café.md` | `nCodeCaf` |
| `authLogin.md` | `authLogin` (already camel) |
| `XMLParser.md` | `xmlParser` |
| `2fa login.md` | `plan2FaLogin` (leading digit) |

## Package contents

| File | Written by | Notes |
|------|------------|-------|
| `source.md` | this skill, **before** `<id>.md` | Snapshot of the source for **every** invocation: byte-exact copy of a file source, or the inline prompt text. Plan and contract point at the snapshot, never at the original path |
| `<id>.md` | this skill | The tasklist: filename is exactly the full directory basename + `.md`, including any `-2`..`-9` collision suffix (e.g. `TASK-WF-authLogin-20261001-063000.md`). `schema: workflow-plan/1.2`, `slug: <id>`. Never `plan.md` |
| `return-contract.yaml` | this skill | contract `1.1` |
| `progress.md`, `artifacts/` | `/sc:implement` | Not created here. No per-task or per-phase folders |

## STOP

| Code | When | Package? |
|------|------|----------|
| `E-NO-SOURCE` | no path and no prompt, or two file tokens | none |
| `E-EMPTY-SOURCE` | whitespace-only | none |
| `E-BAD-FLAG` | unknown enum | none |
| `E-LEGACY` | `--output`, `--parallel`, `--validate`, `--depth shallow\|normal` | none |
| `E-PACKAGE-COLLISION` | `-9` suffix also taken | none |
| `E-NO-PHASES` | Wave 1 extracted nothing | created → `failed` contract |
| `E-GATE` | Wave 3 schema/heading fail | created → `failed` contract |

Enums: strategy `systematic|agile|enterprise`; depth `quick|standard|deep`; handoff `none|design|implement|tasklist`.

Bash: only the package `mkdir` (exclusive leaf) and a single `rm` may change the filesystem; read-only helpers (`date -u`, `test -e`/`-L`, `tr`/`sed` for the subject, `grep` for gate checks) are fine. The single `rm` is of the draft `<id>.md` this run wrote when Wave 3 fails (never a directory, never anything else). Write `source.md` and `<id>.md` with the Write tool (a file source's text is read, then written verbatim).
