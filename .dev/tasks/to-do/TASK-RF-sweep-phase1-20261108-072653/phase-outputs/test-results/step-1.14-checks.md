# Step 1.14 checks (item 11.1)

Run 2026-11-12 on `src/superclaude/commands/sweep.md` (second run: the first run found a literal `--unattended` in a sentence that said there is no such flag, so check 2 failed; the sentence was reworded to "There is no worker mode and no flag for one." and all checks were re-run).

## Check 1: no `src/superclaude` substring

Command: `grep -c 'src/superclaude' src/superclaude/commands/sweep.md`
```text
0
```

## Check 2: no Unattended mode heading or --unattended flag

Command: `grep -n '^## Unattended mode\|--unattended' src/superclaude/commands/sweep.md` (must print nothing)
```text
(grep exit 1; 1 means no match)
```

## Check 3: installed skill path in the Activation block

Command: `grep -nF '~/.claude/skills/sc-sweep-protocol/SKILL.md' src/superclaude/commands/sweep.md`
```text
49:- `~/.claude/skills/sc-sweep-protocol/SKILL.md`
```

## Check 4: project copy path (lookbehind rejects the installed path)

Command: `grep -nP '(?<!~/)\.claude/skills/sc-sweep-protocol/SKILL\.md' src/superclaude/commands/sweep.md`
```text
53:- `.claude/skills/sc-sweep-protocol/SKILL.md`
```

## Section line numbers (the Activation block is lines 42 to 56)
```text
18:## Triggers
22:## Usage
31:## Options
42:## Activation
57:## Boundaries
```

## Description wording

Command: `sed -n 3p src/superclaude/commands/sweep.md | grep -ciE 'stop|retry|release|merge|remov'` (must print 0)
```text
0
```

Result: all four checks hold (counts 0, no match, one line, one line) and the description holds none of the five words.
