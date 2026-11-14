# Step 1.17 checks (item 12.1)

Run 2026-11-12 on `src/superclaude/core/WORKER-CONTRACT.md` (HEAD `5dc29d23`).

## Gates

- `phase-outputs/plans/OQ-3-GQ-11-rule-id-decision.md`: frontmatter `status: RESOLVED` (line 3), operator decision line 36 "Approve option (a), new WC-16 and the proposed coordinator-loop text in DESIGN section 8, preserving existing worker duties." PASS.
- `artifacts/pr422-409-check.md` exists (2147 bytes). PASS.

## Anchors at HEAD before the edit

- Fan-in paragraph at `WORKER-CONTRACT.md:273` (its last sentence ends "the coordinator reports the single admitted result, or the failure, to the person."); `### Worked example: gate hit, answer, new Task` at :275; `git diff --quiet HEAD` on the contract was clean before the edit.

## Check 1: heading prints one line between the two headings

Command: `grep -n -e '^### Fan-in rule' -e '^### WC-16. Coordinator loop$' -e '^### Worked example: gate hit, answer, new Task$' src/superclaude/core/WORKER-CONTRACT.md`
```text
271:### Fan-in rule (several workers, then one merge)
275:### WC-16. Coordinator loop
279:### Worked example: gate hit, answer, new Task
(exit 0)
```
Result: one WC-16 line, after the fan-in heading and before the worked example heading. PASS

## Check 2: WC-14 heading count unchanged

Command: `echo "now=$(grep -c '^### WC-14' src/superclaude/core/WORKER-CONTRACT.md) head=$(git show HEAD:src/superclaude/core/WORKER-CONTRACT.md | grep -c '^### WC-14')"`
```text
now=0 head=0
(exit 0)
```
Result: equal counts. PASS

## Check 3: only added lines

Command: `echo "removed=$(git diff -U0 -- src/superclaude/core/WORKER-CONTRACT.md | grep -c '^-[^-]') added=$(git diff -U0 -- src/superclaude/core/WORKER-CONTRACT.md | grep -c '^+[^+]')"; git diff --stat -- src/superclaude/core/WORKER-CONTRACT.md | tail -1`
```text
removed=0 added=2
 1 file changed, 4 insertions(+)
(exit 0)
```
Result: 0 removed lines, 4 added lines. PASS

## Check 4: four pin phrases occur in the inserted text

Command: `for p in 'WC-16. Coordinator loop' 'On every coordinator wake' 'it is never posted' 'It never stops watching on its own'; do printf '%s: ' "$p"; git diff -U0 -- src/superclaude/core/WORKER-CONTRACT.md | grep '^+' | grep -c -F "$p"; done`
```text
WC-16. Coordinator loop: 1
On every coordinator wake: 1
it is never posted: 1
It never stops watching on its own: 1
(exit 0)
```
Result: each phrase counts 1 in the added lines. PASS

## Check 5: inserted text equals the DESIGN fenced block byte for byte

Command: `git diff -U0 -- src/superclaude/core/WORKER-CONTRACT.md | grep '^+[^+]' | sed 's/^+//' | grep -v '^$' > /tmp/wc16-inserted.txt; awk '/^```markdown$/{f=1;next} /^```$/{if(f){exit}} f' <(sed -n '/^## 8. WC-16/,/^## 9. Routing/p' docs/designs/orchestrator-mode.md) | grep -v '^$' > /tmp/wc16-design.txt; cmp /tmp/wc16-inserted.txt /tmp/wc16-design.txt && echo identical; rm -f /tmp/wc16-inserted.txt /tmp/wc16-design.txt`
```text
identical
(exit 0)
```
Result: identical (non-blank lines compared; blank lines are the heading separator and the single blank after the paragraph). PASS

## Check 6: no code span starting with uv, make or bash in the inserted text (the repo-setup test constraint)

Command: `git diff -U0 -- src/superclaude/core/WORKER-CONTRACT.md | grep '^+[^+]' | grep -c -E '`(uv|make|bash)[ `]'`
```text
0
(exit 1)
```
Result: 0 matches (grep exits 1). PASS

Overall: all checks PASS.

## Re-run after the cycle-1 fix (2026-11-12, item 12.14)

Owner-approved change (record: `phase-outputs/plans/OQ-3-addendum-wc16-wait-timeout-decision.md`): WC-16 now starts "On every coordinator wake or wait timeout, at most once every 5 minutes, ..." in `WORKER-CONTRACT.md:277` and in the DESIGN section 8 fenced block (`docs/designs/orchestrator-mode.md:679`). The commands of checks 1 to 6 above were run again, unchanged, in the same worktree. The contract diff against HEAD now also holds the line-23 change that item 12.2 added after the first record, so the totals in checks 3 and 5 differ from the first run for that reason, not because of the cycle-1 edit.

- Check 1 (heading line between the two headings): output `271:### Fan-in rule ...`, `275:### WC-16. Coordinator loop`, `279:### Worked example: gate hit, answer, new Task`, exit 0. PASS
- Check 2 (WC-14 heading count): `now=0 head=0`, exit 0. PASS (vacuous, see CON-F3 in `qa/contract/consolidated-findings-cycle0.md`; WC-14 is a bullet at `WORKER-CONTRACT.md:63`, not a `###` heading)
- Check 3 (only added lines): `removed=0 added=3` and ` 1 file changed, 5 insertions(+), 1 deletion(-)`, exit 0. The 1 deletion and the third added line are the line-23 change (`/sc:sweep` in the never-as-worker list, item 12.2); the WC-16 hunk is still 4 pure insertions (heading, blank, paragraph, blank). PASS for the WC-16 hunk (the first run's "removed=0 added=2, 4 insertions" no longer holds for the whole file diff, as stated above)
- Check 4 (four pin phrases in the added lines): `WC-16. Coordinator loop: 1`, `On every coordinator wake: 1`, `it is never posted: 1`, `It never stops watching on its own: 1`, exit 0. PASS (the new text "On every coordinator wake or wait timeout" still contains the pinned phrase)
- Check 5 (inserted text equals the DESIGN fenced block), command exactly as above: output `/tmp/wc16-inserted.txt /tmp/wc16-design.txt differ: byte 1, line 1`, exit 1, with 3 lines against 2. FAIL as written, because the added lines now include the line-23 sentence from item 12.2. Not caused by the cycle-1 edit.
  - Same comparison with the line-23 line (`- **Never-as-worker list**`) filtered out of the inserted side: `identical`, 2 lines against 2, exit 0. PASS
  - Full byte compare including blank lines, `WORKER-CONTRACT.md` lines 275 to 277 against the whole DESIGN fenced block: `identical-with-blank-lines`, exit 0. PASS
  - So the contract paragraph and the DESIGN block are byte-identical after the fix.
- Check 6 (no `uv`, `make` or `bash` code span in the added lines): `0`, exit 1 (grep exit 1 means no match). PASS

Overall: the contract and the DESIGN block are byte-identical; check 5 as written fails only because of the line-23 hunk (see above), and the two adjusted comparisons pass.
