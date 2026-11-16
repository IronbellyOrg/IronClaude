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
