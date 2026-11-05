# Wave 1.6 Branch A (log-call inspection), persisted on receipt; degraded: false

query_target: src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh

| line | call_type | level | richness | note |
|---|---|---|---|---|
| 49-54 | fail() | stdout token fd3, detail fd4 | rich | `EVIDENCE_FAIL <reason>` + `collect-conflict-evidence: <detail>`, exit 2; reaches the caller during capture |
| 69 | check_deadline -> fail timeout | token + stderr | minimal | names neither the command nor elapsed time; runs only between commands |
| 76 | check_deadline before the command | token + stderr | minimal | keeps `remaining` >= 1 at :77 |
| 79-81 | timeout path, 124 -> fail timeout | token + stderr | rich | names the command; no `-k`, so a command ignoring TERM still hangs; other signal exits return without a message |
| 81, 86 | timeout fail inside capture / step 3a | n/a | silent (lost) | $TMP/err never printed on the timeout path; the EXIT cleanup deletes it |
| 82-84 | fallback without timeout | none | silent | command runs with no limit; nothing printed while it runs |
| 86 | check_deadline after the command | token + stderr | minimal | the only budget check in the fallback, after the command returns |
| 149 | fail out_not_empty (not a directory) | token + stderr | minimal | names only the raw --out |
| 150 | fail out_not_empty (not empty) | token + stderr | minimal | `ls -A 2>/dev/null`: an unreadable directory reads as empty and passes |
| 152, 157-158 | fail usage (mkdir/mktemp) | token + stderr | minimal | system error text dropped |
| 135-143 | rev-parse 2>/dev/null -> fail | token + stderr | minimal | git error suppressed |
| 166-176 | place -> fail unreadable | token + stderr | minimal | "cannot write $dest" |
| 185-188 | capture non-zero | stderr dump + token | rich | raw $TMP/err then "cannot read the evidence for $name"; exit code not reported |
| 193-197 | step 3a ls-files failure | stderr dump + token | rich | same pattern |
| 202, 210-215 | skipped record / missing stage | JSON `missing` | silent | intended |
| 238-243 | jq render failure -> fail usage | token + stderr | minimal | labelled usage |
| 38-40 | cleanup | none | silent | failures never reported |

- Hang without `timeout`: no output at all until the command returns (:82-86); a command that never returns never prints.
- out_not_empty names only the caller's --out (:149-150); attempt or cycle identity must be encoded in that path by the caller.
