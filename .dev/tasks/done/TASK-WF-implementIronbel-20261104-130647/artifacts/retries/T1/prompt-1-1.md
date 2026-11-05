0f91559cf77f8f18ce13aa537740195434862581
Review one task for spec compliance.

Task brief: Task T1 of plan /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md (lines 30-48), verbatim:
## Task 1: Add the hook script `block-bare-python.sh` and its plugin mirror

Create `src/superclaude/hooks/scripts/block-bare-python.sh` (mode 0755, `#!/usr/bin/env bash`, `set -u`), following the input, block and fail-open pattern of `src/superclaude/hooks/scripts/freshness-pre-edit.sh` (stdin read with `jq`, stderr message plus `exit 2` to block). Copy it byte-for-byte to `plugins/superclaude/hooks/scripts/block-bare-python.sh` (mode 0755).

Detection rules the script implements:

- Read `.tool_name` and `.tool_input.command`. Only `Bash` is checked; anything else exits 0.
- Split the command into simple commands at unquoted `;`, `&&`, `||`, `|`, `&`, newlines, `(`, `)`, `$(` and backticks. Text inside single quotes, and text inside double quotes, is never a command word (so commit messages, `echo "python3 ..."`, `grep 'pip install'` and `bash -c "python3 ..."` are not blocked). Backslash escapes outside single quotes are honoured when tracking quotes.
- In each simple command, skip leading `NAME=value` assignments, the shell keywords `if`, `then`, `elif`, `else`, `do`, `while`, `until`, `!`, `{`, and the wrappers `sudo`, `exec`, `nohup`, `time`, `nice`, `env` (plus its following options and `NAME=value` words), `timeout` (plus its options and its duration argument) and `command` (only when not followed by `-v` or `-V`, so `command -v python3` stays allowed). The next word is the command word.
- Block when the command word's basename is exactly `python`, `python3`, `pip` or `pip3`. `uv`, `uvx`, `which`, `type`, `command -v`, `grep`, `rg`, `ls`, `cat`, `git` and every other command word are allowed, whatever their arguments contain.
- Lines of a heredoc body are scanned like ordinary lines (a heredoc fed to `bash` with a `python3` line would run it). Document this as a known ceiling in a header comment: a heredoc that only writes text whose line starts with `python3` is blocked too.
- Tokenising is done in `jq` (regex `match`/`scan`) or `awk`, not a per-character bash loop, so a 100 KB command is checked in well under the 3-second registration timeout.

Block message on stderr, one or two lines, starting `UV-ONLY BLOCK:`, naming the offending command word, and telling the agent to use `uv run python ...` (or `uv pip ...` / `uvx ...`) instead, or `jq` to parse JSON. Keep a header comment stating the decision contract (allow exit 0, block exit 2 with stderr, never exit 1, fail open) and citing issue #357.

Acceptance criteria:
- `src/superclaude/hooks/scripts/block-bare-python.sh` and `plugins/superclaude/hooks/scripts/block-bare-python.sh` exist, are executable, and are byte-identical (`cmp` exits 0).
- Piping `{"tool_name":"Bash","tool_input":{"command":"echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'"}}` into the script exits 2 and stderr contains `uv run python` and `jq`; the same payload with command `echo '{}' | jq .` exits 0 with empty stderr. Both runs are recorded in `./artifacts/t1-manual-run.txt`.
- The script contains no call to `python`, `python3`, `pip` or `pip3` (`grep -nE '(^|[^a-z_])(python3?|pip3?)( |$)'` on it matches only comments and the message text, recorded in `./artifacts/t1-manual-run.txt`).

AC ids: T1.AC1 = plan line 46 (both files exist, executable, byte-identical); T1.AC2 = plan line 47 (blocked/allowed manual runs recorded in ./artifacts/t1-manual-run.txt); T1.AC3 = plan line 48 (no python/pip call in the script; grep recorded).
Implement-time amendments that apply to T1 (recorded in the package at /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/artifacts/amendments.md; the plan file itself is not edited): AMD-03, AMD-04, AMD-07 (scanner design, quoted substitution, fail-open by construction) and M-CEILINGS (documented ceilings in the header). Read that file for their text.
Package root for ./artifacts/ paths: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647

Global constraints: plan lines 17-26, verbatim:
## Constraints

- Requirements come from issue #357 (`gh issue view 357 --repo IronbellyOrg/IronClaude`), "Proposed fix" and "Done when". Done when, verbatim: a PreToolUse `Bash` hook blocks a command that runs bare `python`, `python3`, `pip` or `pip3`, with a message naming `uv run python` and `jq`; it allows `uv run python`, `uv pip` and `uvx`, and does not block commands that only mention python in arguments, paths or quoted text; tests cover both the blocked and the allowed cases, including commands chained with `&&`, `;` and `|`; `superclaude install` installs and registers the hook, and it fires for subagent Bash calls; `read-parse.md:8` uses `uv run python`; a fresh session that tries `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'` is blocked and pointed to `uv run python` or `jq`.
- Never run `superclaude install` (with or without `--force`) against the live `~/.claude`: other sessions are running. Installer checks use a temporary target path or a temporary HOME only. The live fresh-session check in Task 6 registers the hook through a temporary `--settings` file and never writes to `~/.claude/settings.json` or `~/.claude/hooks/`.
- The hook script is bash plus `jq`, modelled on `src/superclaude/hooks/scripts/freshness-pre-edit.sh`: read the PreToolUse JSON from stdin with `jq`, block with a message on stderr and exit 2, allow with exit 0, never exit 1, and fail open (exit 0) when `jq` is missing, the input is not valid JSON, the tool is not `Bash`, or `tool_input.command` is absent or empty. The hook itself must not run Python.
- Scope of "bare": the command word's basename is exactly `python`, `python3`, `pip` or `pip3` (so `/usr/bin/python3` and `.venv/bin/python` count). Versioned names such as `python3.12` are not part of issue #357 and get no test either way.
- UV for every Python operation in this work (`uv run pytest`, `uv run ruff`); never bare `python`, `python3`, `pip` or `pip3`.
- `src/superclaude/` is the source of truth: run `make sync-dev` after changing hooks or skills, and never stage `.claude/` paths other than `.claude/settings.json`.
- `plugins/superclaude/hooks/hooks.json` already differs from `src/superclaude/hooks/hooks.json` in unrelated entries (ccsession, pragmatic-subagent, auggie matcher). Add only the new registration there; fixing that older drift is out of scope.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included. Staging is not committing.

Start sha: 0f91559cf77f8f18ce13aa537740195434862581
Diff against the start snapshot: (new untracked files; full contents follow)
=== new file: src/superclaude/hooks/scripts/block-bare-python.sh
+++ b/src/superclaude/hooks/scripts/block-bare-python.sh
@@ -0,0 +1,279 @@
+#!/usr/bin/env bash
+# PreToolUse(Bash) UV-only gate (IronbellyOrg/IronClaude issue #357).
+#
+# Blocks a Bash tool call whose command runs bare `python`, `python3`, `pip`
+# or `pip3` as a command word, and tells the agent to use `uv run python`
+# (or `uv pip`, `uvx`) instead, or `jq` to parse JSON. Applies to subagent
+# Bash calls too, because PreToolUse hooks fire inside subagents.
+#
+# Decision contract (same as freshness-pre-edit.sh):
+#   allow -> exit 0; block -> one message on stderr + exit 2; never exit 1.
+#   Fail open (exit 0): jq or awk missing, input not valid JSON, tool is not
+#   Bash, no or empty tool_input.command, or any scanner error. The hook
+#   blocks only when the scanner positively reports a bare command word.
+#   The hook itself runs no Python.
+#
+# How a command is read: jq extracts tool_input.command and pipes it, on
+# stdin, to one stateful awk scanner (never through awk -v or the
+# environment, which mangle backslashes and fail above 128 KB). The scanner
+# tracks single, double and $'...' quotes, `#` comments, backslash-newline
+# continuation, $( ) and backtick substitutions (also inside double quotes;
+# the closing `)` resumes the outer word), $(( )) and (( )) arithmetic,
+# subshells, process substitution, case patterns, array assignments,
+# redirections, heredocs and here-strings. In each simple command it skips
+# NAME=value assignments, the keywords if/then/elif/else/do/while/until/!/{
+# and the wrappers sudo, nice, nohup, time, exec, timeout, env, command and
+# coproc (with their options; `command -v`/`-V` is a lookup and is allowed).
+# The next word, with quotes and backslashes removed, is the command word;
+# its basename is checked.
+#
+# Heredoc bodies: a quoted-delimiter body (<<'EOF', <<"EOF", <<\EOF) is
+# literal text and is not scanned, unless the heredoc's own command word is
+# a shell (bash, sh, zsh, dash, ksh), in which case its lines are scanned as
+# commands. An unquoted-delimiter body has literal quotes, but its $( ) and
+# backtick substitutions are scanned. <<- strips leading tabs from the
+# terminator line. <<< is a here-string, not a heredoc.
+#
+# Known ceilings (commands that run Python but are NOT blocked):
+#   - string arguments to another interpreter: bash -c / sh -c "python3 x",
+#     eval "python3 x", env -S "python3 x";
+#   - commands started by another program: xargs python3, find -exec python3;
+#   - a heredoc whose body is piped or redirected into a shell
+#     (cat <<'EOF' | bash) instead of being that shell's own heredoc;
+#   - ${...} parameter expansions are not parsed (${CMD:-python3} x);
+#   - nested backticks written with \` escapes;
+#   - versioned names such as python3.12 or pip3.11 (outside issue #357);
+#   - shell commands run by tools other than Bash (for example Monitor);
+#   - hosts without jq: the hook fails open for every command;
+#   - `claude --bare` sessions, which skip settings hooks.
+# Known false positive: a word that is not a command but sits in command
+# position, for example a heredoc body fed to a shell that only echoes text.
+
+set -u
+
+if ! command -v jq >/dev/null 2>&1; then
+    echo "block-bare-python: jq not found; allowing the command (fail open)." >&2
+    exit 0
+fi
+if ! command -v awk >/dev/null 2>&1; then
+    echo "block-bare-python: awk not found; allowing the command (fail open)." >&2
+    exit 0
+fi
+
+read -r -d '' SCANNER <<'AWK'
+function iscmd(t) { return t == "top" || t == "dol" || t == "bt" || t == "par" || t == "arr" }
+function isshell(b) { return b == "bash" || b == "sh" || b == "zsh" || b == "dash" || b == "ksh" }
+function iskw(w) {
+    return w == "if" || w == "then" || w == "elif" || w == "else" || w == "do" || \
+        w == "while" || w == "until" || w == "!" || w == "{" || w == "}" || \
+        w == "fi" || w == "done"
+}
+function iswrap(b) {
+    return b == "env" || b == "sudo" || b == "nice" || b == "nohup" || b == "time" || \
+        b == "exec" || b == "timeout" || b == "command" || b == "coproc"
+}
+function base(w,   n, parts) { n = split(w, parts, "/"); return n ? parts[n] : "" }
+function pushc(t) {
+    d++; ct[d] = t; inw[d] = 0; wd[d] = ""; noc[d] = (t == "arr"); need[d] = !noc[d]
+    wrap[d] = ""; parg[d] = 0; skn[d] = 0; cs[d] = 0; cmd[d] = ""
+}
+function pushq(t, o) { d++; ct[d] = t; own[d] = o; inw[o] = 1 }
+function pusha() { d++; ct[d] = "arith"; ad[d] = 2 }
+function owner(l) { return iscmd(ct[l]) ? l : ((ct[l] == "dq" || ct[l] == "sq" || ct[l] == "ansi") ? own[l] : 0) }
+function addc(o, c) { if (o) { inw[o] = 1; wd[o] = wd[o] c } }
+function sep(o) { endword(o); need[o] = !noc[o]; wrap[o] = ""; parg[o] = 0; skn[o] = 0 }
+function endword(o,   w, b, k) {
+    if (!inw[o]) return
+    w = wd[o]; inw[o] = 0; wd[o] = ""
+    if (skn[o]) { skn[o] = 0; return }
+    if (cs[o] == 1) { cs[o] = 2; return }
+    if (cs[o] == 2) { if (w == "in") cs[o] = 3; return }
+    if (cs[o] == 3) { if (w == "esac") { cs[o] = 0; need[o] = 0 }; return }
+    if (!need[o]) return
+    if (parg[o] > 0) { parg[o]--; return }
+    if (w ~ /^[A-Za-z_][A-Za-z0-9_]*\+?=/) return
+    if (wrap[o] != "") {
+        if (w ~ /^-/) {
+            if (wrap[o] == "command" && w ~ /^-[A-Za-z]*[vV]/) { need[o] = 0; return }
+            if ((wrap[o], w) in argopt) parg[o] = 1
+            return
+        }
+        if (wrap[o] == "timeout") { wrap[o] = "timeout-duration"; return }
+    }
+    if (iskw(w)) return
+    if (w == "esac") { cs[o] = 0; return }
+    if (w == "case") { cs[o] = 1; need[o] = 0; return }
+    if (w == "function") { parg[o] = 1; return }
+    b = base(w)
+    if (iswrap(b)) { wrap[o] = b; return }
+    need[o] = 0; cmd[o] = b
+    for (k = qh; k < qt; k++) if (hqown[k] == o && hqwait[k]) { hqwait[k] = 0; hqsh[k] = isshell(b) }
+    if (b == "python" || b == "python3" || b == "pip" || b == "pip3") { print b; exit }
+}
+function nexthdoc(   k) {
+    while (qh < qt) {
+        k = qh++
+        if (hqsh[k]) continue
+        d++; ct[d] = "hdoc"; hdelim[d] = hqd[k]; hstrip[d] = hqs[k]; hexp[d] = !hqq[k]
+        return
+    }
+}
+function heredoc(o, s, n, strip,   dl, q, ch) {
+    while (substr(s, i + 1, 1) == " " || substr(s, i + 1, 1) == "\t") i++
+    dl = ""; q = 0
+    while (i + 1 <= n) {
+        ch = substr(s, i + 1, 1)
+        if (ch == " " || ch == "\t" || ch == ";" || ch == "&" || ch == "|" || ch == "<" || ch == ">" || ch == "(" || ch == ")") break
+        i++
+        if (ch == "\047") { q = 1; while (i + 1 <= n && substr(s, i + 1, 1) != "\047") { i++; dl = dl substr(s, i, 1) }; i++; continue }
+        if (ch == "\"") { q = 1; while (i + 1 <= n && substr(s, i + 1, 1) != "\"") { i++; dl = dl substr(s, i, 1) }; i++; continue }
+        if (ch == "\\") { q = 1; i++; dl = dl substr(s, i, 1); continue }
+        dl = dl ch
+    }
+    hqd[qt] = dl; hqs[qt] = strip; hqq[qt] = q; hqown[qt] = o
+    if (need[o]) { hqwait[qt] = 1; hqsh[qt] = 0 } else { hqwait[qt] = 0; hqsh[qt] = isshell(cmd[o]) }
+    qt++
+}
+function cmdchar(s, n, c,   o, nx, t, p) {
+    o = d
+    if (c == "\\") { if (i == n) { i = n + 1; return }; i++; addc(o, substr(s, i, 1)); return }
+    if (c == "\047") { pushq("sq", o); return }
+    if (c == "\"") { pushq("dq", o); return }
+    if (c == "`") {
+        if (ct[o] == "bt") { endword(o); d--; return }
+        addc(o, "$()"); pushc("bt"); return
+    }
+    if (c == "$") {
+        nx = substr(s, i + 1, 1)
+        if (nx == "(") {
+            addc(o, "$()")
+            if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
+            return
+        }
+        if (nx == "\047") { i++; pushq("ansi", o); return }
+        if (nx == "\"") { i++; pushq("dq", o); return }
+        addc(o, c); return
+    }
+    if (c == "#" && !inw[o]) { i = n; return }
+    if (c == " " || c == "\t" || c == "\r") { endword(o); return }
+    if (c == "\n") { sep(o); if (qh < qt) nexthdoc(); return }
+    if (c == ";") {
+        sep(o); nx = substr(s, i + 1, 1)
+        if (nx == ";" || nx == "&") { i++; if (substr(s, i + 1, 1) == "&") i++; if (cs[o] >= 3) cs[o] = 3 }
+        return
+    }
+    if (c == "&") {
+        nx = substr(s, i + 1, 1)
+        if (nx == ">") { endword(o); i++; if (substr(s, i + 1, 1) == ">") i++; skn[o] = 1; return }
+        sep(o); if (nx == "&") i++
+        return
+    }
+    if (c == "|") { sep(o); nx = substr(s, i + 1, 1); if (nx == "|" || nx == "&") i++; return }
+    if (c == ">" || c == "<") {
+        nx = substr(s, i + 1, 1)
+        if (nx == "(") { endword(o); i++; pushc("par"); return }
+        if (inw[o] && wd[o] ~ /^[0-9]+$/) { inw[o] = 0; wd[o] = "" } else endword(o)
+        if (c == "<" && nx == "<") {
+            if (substr(s, i + 2, 1) == "<") { i += 2; skn[o] = 1; return }
+            i++
+            if (substr(s, i + 1, 1) == "-") { i++; heredoc(o, s, n, 1) } else heredoc(o, s, n, 0)
+            return
+        }
+        if (nx == ">" || nx == "&" || nx == "|") i++
+        skn[o] = 1; return
+    }
+    if (c == "(") {
+        if (inw[o] && wd[o] ~ /^[A-Za-z_][A-Za-z0-9_]*\+?=$/) { pushc("arr"); return }
+        endword(o)
+        if (substr(s, i + 1, 1) == ")") { i++; need[o] = !noc[o]; wrap[o] = ""; parg[o] = 0; return }
+        if (cs[o] == 3) return
+        if (need[o] && substr(s, i + 1, 1) == "(") { i++; pusha(); return }
+        pushc("par"); return
+    }
+    if (c == ")") {
+        if (cs[o] == 3) { endword(o); cs[o] = 4; need[o] = 1; wrap[o] = ""; parg[o] = 0; return }
+        endword(o)
+        t = ct[o]
+        if (t == "dol" || t == "par" || t == "arr") { d--; if (t == "par" && iscmd(ct[d])) need[d] = 0; return }
+        sep(o); return
+    }
+    addc(o, c)
+}
+function qchar(s, n, c,   o, t) {
+    t = ct[d]; o = own[d]
+    if (t == "sq") { if (c == "\047") d--; else addc(o, c); return }
+    if (t == "ansi") {
+        if (c == "\\") { i++; addc(o, substr(s, i, 1)); return }
+        if (c == "\047") d--; else addc(o, c)
+        return
+    }
+    if (c == "\"") { d--; return }
+    if (c == "\\") { if (i == n) { i = n + 1; return }; i++; addc(o, substr(s, i, 1)); return }
+    if (c == "`") { addc(o, "$()"); pushc("bt"); return }
+    if (c == "$" && substr(s, i + 1, 1) == "(") {
+        addc(o, "$()")
+        if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
+        return
+    }
+    addc(o, c)
+}
+function arithchar(s, n, c) {
+    if (c == "(") { ad[d]++; return }
+    if (c == ")") { ad[d]--; if (ad[d] <= 0) d--; return }
+    if (c == "$" && substr(s, i + 1, 1) == "(" && substr(s, i + 2, 1) != "(") { i++; pushc("dol") }
+}
+function hdocchar(s, n, c) {
+    if (!hexp[d]) return
+    if (c == "\\") { if (i == n) { hjoin = 1; i = n + 1; return }; i++; return }
+    if (c == "`") { pushc("bt"); return }
+    if (c == "$" && substr(s, i + 1, 1) == "(") {
+        if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
+    }
+}
+BEGIN {
+    argopt["sudo", "-u"] = 1; argopt["sudo", "-g"] = 1; argopt["sudo", "-C"] = 1
+    argopt["sudo", "-h"] = 1; argopt["sudo", "-p"] = 1; argopt["sudo", "-U"] = 1
+    argopt["sudo", "-r"] = 1; argopt["sudo", "-t"] = 1; argopt["sudo", "-D"] = 1
+    argopt["sudo", "-R"] = 1; argopt["nice", "-n"] = 1; argopt["env", "-u"] = 1
+    argopt["env", "-C"] = 1; argopt["exec", "-a"] = 1; argopt["timeout", "-s"] = 1
+    argopt["timeout", "-k"] = 1; argopt["time", "-f"] = 1; argopt["time", "-o"] = 1
+}
+{ L[NR] = $0 }
+END {
+    d = 0; pushc("top"); qh = 1; qt = 1; hjoin = 0
+    for (li = 1; li <= NR; li++) {
+        s = L[li]; n = length(s)
+        if (ct[d] == "hdoc") {
+            line = s
+            if (hstrip[d]) sub(/^\t+/, "", line)
+            if (!hjoin && line == hdelim[d]) { d--; nexthdoc(); continue }
+            hjoin = 0
+            if (!hexp[d]) continue
+        }
+        for (i = 1; i <= n + 1; i++) {
+            c = (i <= n) ? substr(s, i, 1) : "\n"
+            t = ct[d]
+            if (iscmd(t)) cmdchar(s, n, c)
+            else if (t == "dq" || t == "sq" || t == "ansi") qchar(s, n, c)
+            else if (t == "arith") arithchar(s, n, c)
+            else if (t == "hdoc") hdocchar(s, n, c)
+        }
+    }
+    while (d >= 1) { if (iscmd(ct[d])) endword(d); d-- }
+}
+AWK
+
+INPUT="$(cat 2>/dev/null || true)"
+[ -n "$INPUT" ] || exit 0
+
+WORD="$(printf '%s' "$INPUT" \
+    | jq -j 'if .tool_name == "Bash" then (.tool_input.command // "" | strings) else "" end' 2>/dev/null \
+    | LC_ALL=C awk "$SCANNER" 2>/dev/null)" || WORD=""
+
+case "$WORD" in
+    python|python3|pip|pip3) ;;
+    *) exit 0 ;;
+esac
+
+echo "UV-ONLY BLOCK: this command runs bare \`$WORD\`. Use \`uv run python ...\` (or \`uv pip ...\` / \`uvx ...\`) instead, or \`jq\` to parse JSON." >&2
+exit 2
=== new file: plugins/superclaude/hooks/scripts/block-bare-python.sh
+++ b/plugins/superclaude/hooks/scripts/block-bare-python.sh
@@ -0,0 +1,279 @@
+#!/usr/bin/env bash
+# PreToolUse(Bash) UV-only gate (IronbellyOrg/IronClaude issue #357).
+#
+# Blocks a Bash tool call whose command runs bare `python`, `python3`, `pip`
+# or `pip3` as a command word, and tells the agent to use `uv run python`
+# (or `uv pip`, `uvx`) instead, or `jq` to parse JSON. Applies to subagent
+# Bash calls too, because PreToolUse hooks fire inside subagents.
+#
+# Decision contract (same as freshness-pre-edit.sh):
+#   allow -> exit 0; block -> one message on stderr + exit 2; never exit 1.
+#   Fail open (exit 0): jq or awk missing, input not valid JSON, tool is not
+#   Bash, no or empty tool_input.command, or any scanner error. The hook
+#   blocks only when the scanner positively reports a bare command word.
+#   The hook itself runs no Python.
+#
+# How a command is read: jq extracts tool_input.command and pipes it, on
+# stdin, to one stateful awk scanner (never through awk -v or the
+# environment, which mangle backslashes and fail above 128 KB). The scanner
+# tracks single, double and $'...' quotes, `#` comments, backslash-newline
+# continuation, $( ) and backtick substitutions (also inside double quotes;
+# the closing `)` resumes the outer word), $(( )) and (( )) arithmetic,
+# subshells, process substitution, case patterns, array assignments,
+# redirections, heredocs and here-strings. In each simple command it skips
+# NAME=value assignments, the keywords if/then/elif/else/do/while/until/!/{
+# and the wrappers sudo, nice, nohup, time, exec, timeout, env, command and
+# coproc (with their options; `command -v`/`-V` is a lookup and is allowed).
+# The next word, with quotes and backslashes removed, is the command word;
+# its basename is checked.
+#
+# Heredoc bodies: a quoted-delimiter body (<<'EOF', <<"EOF", <<\EOF) is
+# literal text and is not scanned, unless the heredoc's own command word is
+# a shell (bash, sh, zsh, dash, ksh), in which case its lines are scanned as
+# commands. An unquoted-delimiter body has literal quotes, but its $( ) and
+# backtick substitutions are scanned. <<- strips leading tabs from the
+# terminator line. <<< is a here-string, not a heredoc.
+#
+# Known ceilings (commands that run Python but are NOT blocked):
+#   - string arguments to another interpreter: bash -c / sh -c "python3 x",
+#     eval "python3 x", env -S "python3 x";
+#   - commands started by another program: xargs python3, find -exec python3;
+#   - a heredoc whose body is piped or redirected into a shell
+#     (cat <<'EOF' | bash) instead of being that shell's own heredoc;
+#   - ${...} parameter expansions are not parsed (${CMD:-python3} x);
+#   - nested backticks written with \` escapes;
+#   - versioned names such as python3.12 or pip3.11 (outside issue #357);
+#   - shell commands run by tools other than Bash (for example Monitor);
+#   - hosts without jq: the hook fails open for every command;
+#   - `claude --bare` sessions, which skip settings hooks.
+# Known false positive: a word that is not a command but sits in command
+# position, for example a heredoc body fed to a shell that only echoes text.
+
+set -u
+
+if ! command -v jq >/dev/null 2>&1; then
+    echo "block-bare-python: jq not found; allowing the command (fail open)." >&2
+    exit 0
+fi
+if ! command -v awk >/dev/null 2>&1; then
+    echo "block-bare-python: awk not found; allowing the command (fail open)." >&2
+    exit 0
+fi
+
+read -r -d '' SCANNER <<'AWK'
+function iscmd(t) { return t == "top" || t == "dol" || t == "bt" || t == "par" || t == "arr" }
+function isshell(b) { return b == "bash" || b == "sh" || b == "zsh" || b == "dash" || b == "ksh" }
+function iskw(w) {
+    return w == "if" || w == "then" || w == "elif" || w == "else" || w == "do" || \
+        w == "while" || w == "until" || w == "!" || w == "{" || w == "}" || \
+        w == "fi" || w == "done"
+}
+function iswrap(b) {
+    return b == "env" || b == "sudo" || b == "nice" || b == "nohup" || b == "time" || \
+        b == "exec" || b == "timeout" || b == "command" || b == "coproc"
+}
+function base(w,   n, parts) { n = split(w, parts, "/"); return n ? parts[n] : "" }
+function pushc(t) {
+    d++; ct[d] = t; inw[d] = 0; wd[d] = ""; noc[d] = (t == "arr"); need[d] = !noc[d]
+    wrap[d] = ""; parg[d] = 0; skn[d] = 0; cs[d] = 0; cmd[d] = ""
+}
+function pushq(t, o) { d++; ct[d] = t; own[d] = o; inw[o] = 1 }
+function pusha() { d++; ct[d] = "arith"; ad[d] = 2 }
+function owner(l) { return iscmd(ct[l]) ? l : ((ct[l] == "dq" || ct[l] == "sq" || ct[l] == "ansi") ? own[l] : 0) }
+function addc(o, c) { if (o) { inw[o] = 1; wd[o] = wd[o] c } }
+function sep(o) { endword(o); need[o] = !noc[o]; wrap[o] = ""; parg[o] = 0; skn[o] = 0 }
+function endword(o,   w, b, k) {
+    if (!inw[o]) return
+    w = wd[o]; inw[o] = 0; wd[o] = ""
+    if (skn[o]) { skn[o] = 0; return }
+    if (cs[o] == 1) { cs[o] = 2; return }
+    if (cs[o] == 2) { if (w == "in") cs[o] = 3; return }
+    if (cs[o] == 3) { if (w == "esac") { cs[o] = 0; need[o] = 0 }; return }
+    if (!need[o]) return
+    if (parg[o] > 0) { parg[o]--; return }
+    if (w ~ /^[A-Za-z_][A-Za-z0-9_]*\+?=/) return
+    if (wrap[o] != "") {
+        if (w ~ /^-/) {
+            if (wrap[o] == "command" && w ~ /^-[A-Za-z]*[vV]/) { need[o] = 0; return }
+            if ((wrap[o], w) in argopt) parg[o] = 1
+            return
+        }
+        if (wrap[o] == "timeout") { wrap[o] = "timeout-duration"; return }
+    }
+    if (iskw(w)) return
+    if (w == "esac") { cs[o] = 0; return }
+    if (w == "case") { cs[o] = 1; need[o] = 0; return }
+    if (w == "function") { parg[o] = 1; return }
+    b = base(w)
+    if (iswrap(b)) { wrap[o] = b; return }
+    need[o] = 0; cmd[o] = b
+    for (k = qh; k < qt; k++) if (hqown[k] == o && hqwait[k]) { hqwait[k] = 0; hqsh[k] = isshell(b) }
+    if (b == "python" || b == "python3" || b == "pip" || b == "pip3") { print b; exit }
+}
+function nexthdoc(   k) {
+    while (qh < qt) {
+        k = qh++
+        if (hqsh[k]) continue
+        d++; ct[d] = "hdoc"; hdelim[d] = hqd[k]; hstrip[d] = hqs[k]; hexp[d] = !hqq[k]
+        return
+    }
+}
+function heredoc(o, s, n, strip,   dl, q, ch) {
+    while (substr(s, i + 1, 1) == " " || substr(s, i + 1, 1) == "\t") i++
+    dl = ""; q = 0
+    while (i + 1 <= n) {
+        ch = substr(s, i + 1, 1)
+        if (ch == " " || ch == "\t" || ch == ";" || ch == "&" || ch == "|" || ch == "<" || ch == ">" || ch == "(" || ch == ")") break
+        i++
+        if (ch == "\047") { q = 1; while (i + 1 <= n && substr(s, i + 1, 1) != "\047") { i++; dl = dl substr(s, i, 1) }; i++; continue }
+        if (ch == "\"") { q = 1; while (i + 1 <= n && substr(s, i + 1, 1) != "\"") { i++; dl = dl substr(s, i, 1) }; i++; continue }
+        if (ch == "\\") { q = 1; i++; dl = dl substr(s, i, 1); continue }
+        dl = dl ch
+    }
+    hqd[qt] = dl; hqs[qt] = strip; hqq[qt] = q; hqown[qt] = o
+    if (need[o]) { hqwait[qt] = 1; hqsh[qt] = 0 } else { hqwait[qt] = 0; hqsh[qt] = isshell(cmd[o]) }
+    qt++
+}
+function cmdchar(s, n, c,   o, nx, t, p) {
+    o = d
+    if (c == "\\") { if (i == n) { i = n + 1; return }; i++; addc(o, substr(s, i, 1)); return }
+    if (c == "\047") { pushq("sq", o); return }
+    if (c == "\"") { pushq("dq", o); return }
+    if (c == "`") {
+        if (ct[o] == "bt") { endword(o); d--; return }
+        addc(o, "$()"); pushc("bt"); return
+    }
+    if (c == "$") {
+        nx = substr(s, i + 1, 1)
+        if (nx == "(") {
+            addc(o, "$()")
+            if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
+            return
+        }
+        if (nx == "\047") { i++; pushq("ansi", o); return }
+        if (nx == "\"") { i++; pushq("dq", o); return }
+        addc(o, c); return
+    }
+    if (c == "#" && !inw[o]) { i = n; return }
+    if (c == " " || c == "\t" || c == "\r") { endword(o); return }
+    if (c == "\n") { sep(o); if (qh < qt) nexthdoc(); return }
+    if (c == ";") {
+        sep(o); nx = substr(s, i + 1, 1)
+        if (nx == ";" || nx == "&") { i++; if (substr(s, i + 1, 1) == "&") i++; if (cs[o] >= 3) cs[o] = 3 }
+        return
+    }
+    if (c == "&") {
+        nx = substr(s, i + 1, 1)
+        if (nx == ">") { endword(o); i++; if (substr(s, i + 1, 1) == ">") i++; skn[o] = 1; return }
+        sep(o); if (nx == "&") i++
+        return
+    }
+    if (c == "|") { sep(o); nx = substr(s, i + 1, 1); if (nx == "|" || nx == "&") i++; return }
+    if (c == ">" || c == "<") {
+        nx = substr(s, i + 1, 1)
+        if (nx == "(") { endword(o); i++; pushc("par"); return }
+        if (inw[o] && wd[o] ~ /^[0-9]+$/) { inw[o] = 0; wd[o] = "" } else endword(o)
+        if (c == "<" && nx == "<") {
+            if (substr(s, i + 2, 1) == "<") { i += 2; skn[o] = 1; return }
+            i++
+            if (substr(s, i + 1, 1) == "-") { i++; heredoc(o, s, n, 1) } else heredoc(o, s, n, 0)
+            return
+        }
+        if (nx == ">" || nx == "&" || nx == "|") i++
+        skn[o] = 1; return
+    }
+    if (c == "(") {
+        if (inw[o] && wd[o] ~ /^[A-Za-z_][A-Za-z0-9_]*\+?=$/) { pushc("arr"); return }
+        endword(o)
+        if (substr(s, i + 1, 1) == ")") { i++; need[o] = !noc[o]; wrap[o] = ""; parg[o] = 0; return }
+        if (cs[o] == 3) return
+        if (need[o] && substr(s, i + 1, 1) == "(") { i++; pusha(); return }
+        pushc("par"); return
+    }
+    if (c == ")") {
+        if (cs[o] == 3) { endword(o); cs[o] = 4; need[o] = 1; wrap[o] = ""; parg[o] = 0; return }
+        endword(o)
+        t = ct[o]
+        if (t == "dol" || t == "par" || t == "arr") { d--; if (t == "par" && iscmd(ct[d])) need[d] = 0; return }
+        sep(o); return
+    }
+    addc(o, c)
+}
+function qchar(s, n, c,   o, t) {
+    t = ct[d]; o = own[d]
+    if (t == "sq") { if (c == "\047") d--; else addc(o, c); return }
+    if (t == "ansi") {
+        if (c == "\\") { i++; addc(o, substr(s, i, 1)); return }
+        if (c == "\047") d--; else addc(o, c)
+        return
+    }
+    if (c == "\"") { d--; return }
+    if (c == "\\") { if (i == n) { i = n + 1; return }; i++; addc(o, substr(s, i, 1)); return }
+    if (c == "`") { addc(o, "$()"); pushc("bt"); return }
+    if (c == "$" && substr(s, i + 1, 1) == "(") {
+        addc(o, "$()")
+        if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
+        return
+    }
+    addc(o, c)
+}
+function arithchar(s, n, c) {
+    if (c == "(") { ad[d]++; return }
+    if (c == ")") { ad[d]--; if (ad[d] <= 0) d--; return }
+    if (c == "$" && substr(s, i + 1, 1) == "(" && substr(s, i + 2, 1) != "(") { i++; pushc("dol") }
+}
+function hdocchar(s, n, c) {
+    if (!hexp[d]) return
+    if (c == "\\") { if (i == n) { hjoin = 1; i = n + 1; return }; i++; return }
+    if (c == "`") { pushc("bt"); return }
+    if (c == "$" && substr(s, i + 1, 1) == "(") {
+        if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
+    }
+}
+BEGIN {
+    argopt["sudo", "-u"] = 1; argopt["sudo", "-g"] = 1; argopt["sudo", "-C"] = 1
+    argopt["sudo", "-h"] = 1; argopt["sudo", "-p"] = 1; argopt["sudo", "-U"] = 1
+    argopt["sudo", "-r"] = 1; argopt["sudo", "-t"] = 1; argopt["sudo", "-D"] = 1
+    argopt["sudo", "-R"] = 1; argopt["nice", "-n"] = 1; argopt["env", "-u"] = 1
+    argopt["env", "-C"] = 1; argopt["exec", "-a"] = 1; argopt["timeout", "-s"] = 1
+    argopt["timeout", "-k"] = 1; argopt["time", "-f"] = 1; argopt["time", "-o"] = 1
+}
+{ L[NR] = $0 }
+END {
+    d = 0; pushc("top"); qh = 1; qt = 1; hjoin = 0
+    for (li = 1; li <= NR; li++) {
+        s = L[li]; n = length(s)
+        if (ct[d] == "hdoc") {
+            line = s
+            if (hstrip[d]) sub(/^\t+/, "", line)
+            if (!hjoin && line == hdelim[d]) { d--; nexthdoc(); continue }
+            hjoin = 0
+            if (!hexp[d]) continue
+        }
+        for (i = 1; i <= n + 1; i++) {
+            c = (i <= n) ? substr(s, i, 1) : "\n"
+            t = ct[d]
+            if (iscmd(t)) cmdchar(s, n, c)
+            else if (t == "dq" || t == "sq" || t == "ansi") qchar(s, n, c)
+            else if (t == "arith") arithchar(s, n, c)
+            else if (t == "hdoc") hdocchar(s, n, c)
+        }
+    }
+    while (d >= 1) { if (iscmd(ct[d])) endword(d); d-- }
+}
+AWK
+
+INPUT="$(cat 2>/dev/null || true)"
+[ -n "$INPUT" ] || exit 0
+
+WORD="$(printf '%s' "$INPUT" \
+    | jq -j 'if .tool_name == "Bash" then (.tool_input.command // "" | strings) else "" end' 2>/dev/null \
+    | LC_ALL=C awk "$SCANNER" 2>/dev/null)" || WORD=""
+
+case "$WORD" in
+    python|python3|pip|pip3) ;;
+    *) exit 0 ;;
+esac
+
+echo "UV-ONLY BLOCK: this command runs bare \`$WORD\`. Use \`uv run python ...\` (or \`uv pip ...\` / \`uvx ...\`) instead, or \`jq\` to parse JSON." >&2
+exit 2
=== new file: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/artifacts/t1-manual-run.txt
+++ b/.dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/artifacts/t1-manual-run.txt
@@ -0,0 +1,17 @@
+# T1 manual run — 2026-11-04T14:32:22Z
+## cmp source vs plugin mirror
+cmp rc=0
+-rwxr-xr-x plugins/superclaude/hooks/scripts/block-bare-python.sh
+-rwxr-xr-x src/superclaude/hooks/scripts/block-bare-python.sh
+## blocked payload
+{"tool_name":"Bash","tool_input":{"command":"echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'"}}
+rc=2
+stderr: UV-ONLY BLOCK: this command runs bare `python3`. Use `uv run python ...` (or `uv pip ...` / `uvx ...`) instead, or `jq` to parse JSON.
+## allowed payload
+{"tool_name":"Bash","tool_input":{"command":"echo '{}' | jq ."}}
+rc=0
+stderr bytes: 0
+## grep for python/pip call words in the script (expect comments and message text only)
+38:#   - string arguments to another interpreter: bash -c / sh -c "python3 x",
+39:#     eval "python3 x", env -S "python3 x";
+278:echo "UV-ONLY BLOCK: this command runs bare \`$WORD\`. Use \`uv run python ...\` (or \`uv pip ...\` / \`uvx ...\`) instead, or \`jq\` to parse JSON." >&2

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
