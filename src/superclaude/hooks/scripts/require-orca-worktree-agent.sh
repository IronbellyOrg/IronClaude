#!/usr/bin/env bash
# PreToolUse(Bash) gate: every Orca worktree gets an agent.
#
# Blocks a Bash tool call whose command runs `orca worktree create` without
# `--agent` (or `--agent=...`), and tells the agent the exact form to use.
# Applies to subagent Bash calls too, because PreToolUse hooks fire inside
# subagents. Only the --agent requirement is enforced here; "no worktree for
# your own use" and "the creator owns the agent" are instruction text.
#
# Decision contract (same as block-bare-python.sh):
#   allow -> exit 0; block -> one message on stderr + exit 2; never exit 1.
#   Fail open (exit 0): jq or awk missing, input not valid JSON, tool is not
#   Bash, no or empty tool_input.command, or any scanner error. The hook
#   blocks only when the scanner positively reports a bare create.
#   The hook itself runs no Python.
#
# How a command is read: jq extracts tool_input.command and pipes it, on
# stdin, to one stateful awk scanner (never through awk -v or the
# environment, which mangle backslashes and fail above 128 KB). The scanner
# is the block-bare-python.sh tokenizer (quotes, $'...' escapes, `#` comments,
# backslash-newline continuation, $( ) and backtick substitutions, arithmetic,
# subshells, process substitution, case patterns, [[ ]] tests, function
# definitions, redirections, heredocs and here-strings; the wrappers sudo,
# nice, nohup, time, exec, timeout, env, command and coproc are skipped with
# their options), copied here because installed hooks are standalone files.
# Unlike block-bare-python.sh it does not stop at the command word: it collects
# the words of each simple command, resets the collection at every separator
# (; & && || | newline) and inside every substitution, and decides once the
# command's words are complete. A command is blocked when its command word is
# `orca` (or a path ending in /orca), its first two non-option arguments are
# `worktree` and `create`, and none of its own words is `--agent`, starts with
# `--agent=`, or is `--help` or `-h`. A flag in one command never satisfies
# another command.
#
# Not blocked: `orca worktree list`, `orca worktree create --help`, other orca
# subcommands, text that only mentions the phrase inside a quoted argument
# (`echo "orca worktree create"`), and any create that carries `--agent`.
#
# Known ceilings (creates that are NOT blocked):
#   - string arguments to another interpreter: bash -c / sh -c "orca ...",
#     eval "orca ...", env -S "orca ...", ssh host 'orca ...';
#   - commands started by another program: xargs orca, find -exec orca;
#   - a heredoc whose body is piped or redirected into a shell
#     (cat <<'EOF' | bash) instead of being that shell's own heredoc;
#   - a quoted value equal to --agent (orca worktree create --prompt "--agent")
#     counts as the flag, because quotes are removed before the comparison;
#   - a command word assembled from pieces (o$(printf rc)a worktree create);
#     a command word that starts with `$` (a variable, ${...} or $( ) such as
#     `$ORCA worktree create` or `$(printf orca) worktree create`) is treated as
#     a possible orca, so it is blocked when its first two non-option arguments
#     are `worktree` and `create` and it carries no --agent;
#   - nested backticks written with \` escapes;
#   - global orca options that take a separate value before `worktree`
#     (the value is read as the first non-option argument);
#   - wrapper options that take a value but are not in the scanner's tables;
#   - shell commands run by tools other than Bash (for example Monitor);
#   - hosts without jq or awk: the hook fails open for every command;
#   - `claude --bare` sessions, which skip settings hooks;
#   - humans and other agent tools that create worktrees themselves;
#   - scripts that call Orca as a subprocess (orca_worktree.py runs Orca itself,
#     not through the Bash tool, so its own create is outside this hook).

set -u

if ! command -v jq >/dev/null 2>&1; then
    echo "require-orca-worktree-agent: jq not found; allowing the command (fail open)." >&2
    exit 0
fi
if ! command -v awk >/dev/null 2>&1; then
    echo "require-orca-worktree-agent: awk not found; allowing the command (fail open)." >&2
    exit 0
fi

read -r -d '' SCANNER <<'AWK'
function iscmd(t) { return t == "top" || t == "dol" || t == "bt" || t == "par" || t == "arr" || t == "psub" }
function isshell(b) { return b == "bash" || b == "sh" || b == "zsh" || b == "dash" || b == "ksh" }
function iskw(w) {
    return w == "if" || w == "then" || w == "elif" || w == "else" || w == "do" || \
        w == "while" || w == "until" || w == "!" || w == "{" || w == "}" || \
        w == "fi" || w == "done"
}
function iswrap(b) {
    return b == "env" || b == "sudo" || b == "nice" || b == "nohup" || b == "time" || \
        b == "exec" || b == "timeout" || b == "command" || b == "coproc"
}
function base(w,   n, parts) { n = split(w, parts, "/"); return n ? parts[n] : "" }
function pushc(t) {
    d++; ct[d] = t; inw[d] = 0; wd[d] = ""; noc[d] = (t == "arr"); need[d] = !noc[d]
    wrap[d] = ""; parg[d] = 0; skn[d] = 0; cs[d] = 0; cmd[d] = ""; tst[d] = 0; wq[d] = 0
    isorca[d] = 0
}
# Per-command collection: once the command word is `orca`, every later word of
# that simple command is recorded (first two non-option words, --agent, --help).
function track(o, w) {
    if (w == "--agent" || w ~ /^--agent=/) hasagent[o] = 1
    else if (w == "--help" || w == "-h") hashelp[o] = 1
    else if (w !~ /^-/) { nargs[o]++; if (nargs[o] == 1) a1[o] = w; else if (nargs[o] == 2) a2[o] = w }
}
function fin(o) {
    if (!isorca[o]) return
    isorca[o] = 0
    if (a1[o] == "worktree" && a2[o] == "create" && !hasagent[o] && !hashelp[o]) { print "orca"; exit }
}
function pushq(t, o) { d++; ct[d] = t; own[d] = o; inw[o] = 1; wq[o] = 1; anul[d] = 0 }
function pusha() { d++; ct[d] = "arith"; ad[d] = 2 }
function owner(l) { return iscmd(ct[l]) ? l : ((ct[l] == "dq" || ct[l] == "sq" || ct[l] == "ansi") ? own[l] : 0) }
function addc(o, c) { if (o) { inw[o] = 1; wd[o] = wd[o] c } }
function sep(o) { endword(o); fin(o); need[o] = !noc[o]; wrap[o] = ""; parg[o] = 0; skn[o] = 0; tst[o] = 0 }
function dig(set, ch) { return ch == "" ? 0 : index(set, ch) }
function endword(o,   w, b, k, q) {
    if (!inw[o]) return
    w = wd[o]; inw[o] = 0; wd[o] = ""; q = wq[o]; wq[o] = 0
    if (skn[o]) { skn[o] = 0; return }
    if (cs[o] == 1) { cs[o] = 2; return }
    if (cs[o] == 2) { if (w == "in") cs[o] = 3; return }
    if (cs[o] == 3) { if (w == "esac") { cs[o] = 0; need[o] = 0 }; return }
    if (!need[o]) { if (isorca[o]) track(o, w); return }
    if (parg[o] > 0) { parg[o]--; return }
    if (w ~ /^[A-Za-z_][A-Za-z0-9_]*\+?=/) return
    if (wrap[o] != "") {
        if (w ~ /^-/) {
            if (wrap[o] == "command" && w ~ /^-[A-Za-z]*[vV]/) { need[o] = 0; return }
            if (w ~ /^--[A-Za-z]/) {
                if (w !~ /=/ && index(lopt[wrap[o]], " " w)) parg[o] = 1
                return
            }
            for (k = 2; k <= length(w); k++)
                if ((wrap[o], "-" substr(w, k, 1)) in argopt) { if (k == length(w)) parg[o] = 1; break }
            return
        }
        if (wrap[o] == "timeout") { wrap[o] = "timeout-duration"; return }
    }
    if (!q) {
        if (iskw(w)) return
        if (w == "esac") { cs[o] = 0; return }
        if (w == "case") { cs[o] = 1; need[o] = 0; return }
        if (w == "function") { parg[o] = 1; return }
        if (w == "[[") { tst[o] = 1; need[o] = 0; cmd[o] = w; return }
    }
    if (substr(s, i) ~ /^[ \t]*\([ \t]*\)/) { cmd[o] = w; return }
    b = base(w)
    if (iswrap(b)) { wrap[o] = b; return }
    need[o] = 0; cmd[o] = b
    for (k = qh; k < qt; k++) if (hqown[k] == o && hqwait[k]) { hqwait[k] = 0; hqsh[k] = isshell(b) }
    if (b == "orca" || b ~ /^\$/) { isorca[o] = 1; nargs[o] = 0; a1[o] = ""; a2[o] = ""; hasagent[o] = 0; hashelp[o] = 0 }
}
function nexthdoc(   k) {
    while (qh < qt) {
        k = qh++
        if (hqsh[k]) continue
        d++; ct[d] = "hdoc"; hdelim[d] = hqd[k]; hstrip[d] = hqs[k]; hexp[d] = !hqq[k]
        return
    }
}
function heredoc(o, s, n, strip,   dl, q, ch) {
    while (substr(s, i + 1, 1) == " " || substr(s, i + 1, 1) == "\t") i++
    dl = ""; q = 0
    while (i + 1 <= n) {
        ch = substr(s, i + 1, 1)
        if (ch == " " || ch == "\t" || ch == ";" || ch == "&" || ch == "|" || ch == "<" || ch == ">" || ch == "(" || ch == ")") break
        i++
        if (ch == "\047") { q = 1; while (i + 1 <= n && substr(s, i + 1, 1) != "\047") { i++; dl = dl substr(s, i, 1) }; i++; continue }
        if (ch == "\"") { q = 1; while (i + 1 <= n && substr(s, i + 1, 1) != "\"") { i++; dl = dl substr(s, i, 1) }; i++; continue }
        if (ch == "\\") { q = 1; i++; dl = dl substr(s, i, 1); continue }
        dl = dl ch
    }
    hqd[qt] = dl; hqs[qt] = strip; hqq[qt] = q; hqown[qt] = o
    if (need[o]) { hqwait[qt] = 1; hqsh[qt] = 0 } else { hqwait[qt] = 0; hqsh[qt] = isshell(cmd[o]) }
    qt++
}
function cmdchar(s, n, c,   o, nx, t, p) {
    o = d
    if (c == "\\") { if (i == n) { i = n + 1; return }; i++; wq[o] = 1; addc(o, substr(s, i, 1)); return }
    if (c == "\047") { pushq("sq", o); return }
    if (c == "\"") { pushq("dq", o); return }
    if (c == "`") {
        if (ct[o] == "bt") { endword(o); fin(o); d--; return }
        addc(o, "$()"); pushc("bt"); return
    }
    if (c == "$") {
        nx = substr(s, i + 1, 1)
        if (nx == "(") {
            addc(o, "$()")
            if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
            return
        }
        if (nx == "\047") { i++; pushq("ansi", o); return }
        if (nx == "\"") { i++; pushq("dq", o); return }
        addc(o, c); return
    }
    if (tst[o]) {
        if (c == " " || c == "\t" || c == "\r" || c == "\n") { endword(o); return }
        nx = substr(s, i + 2, 1)
        if (c == "]" && !inw[o] && substr(s, i + 1, 1) == "]" && (nx == "" || index(" \t\r;&|)<>", nx))) {
            i++; tst[o] = 0; return
        }
        addc(o, c); return
    }
    if (c == "#" && !inw[o]) { i = n; return }
    if (c == " " || c == "\t" || c == "\r") { endword(o); return }
    if (c == "\n") { sep(o); if (qh < qt) nexthdoc(); return }
    if (c == ";") {
        sep(o); nx = substr(s, i + 1, 1)
        if (nx == ";" || nx == "&") { i++; if (substr(s, i + 1, 1) == "&") i++; if (cs[o] >= 3) cs[o] = 3 }
        return
    }
    if (c == "&") {
        nx = substr(s, i + 1, 1)
        if (nx == ">") { endword(o); i++; if (substr(s, i + 1, 1) == ">") i++; skn[o] = 1; return }
        sep(o); if (nx == "&") i++
        return
    }
    if (c == "|") { sep(o); nx = substr(s, i + 1, 1); if (nx == "|" || nx == "&") i++; return }
    if (c == ">" || c == "<") {
        nx = substr(s, i + 1, 1)
        if (nx == "(") {
            endword(o); i++
            if (skn[o]) skn[o] = 0; else addc(o, "<()")
            pushc("psub"); return
        }
        if (inw[o] && !wq[o] && wd[o] ~ /^([0-9]+|\{[A-Za-z_][A-Za-z0-9_]*\})$/) { inw[o] = 0; wd[o] = ""; wq[o] = 0 } else endword(o)
        if (c == "<" && nx == "<") {
            if (substr(s, i + 2, 1) == "<") { i += 2; skn[o] = 1; return }
            i++
            if (substr(s, i + 1, 1) == "-") { i++; heredoc(o, s, n, 1) } else heredoc(o, s, n, 0)
            return
        }
        if (nx == ">" || nx == "&" || nx == "|") i++
        skn[o] = 1; return
    }
    if (c == "(") {
        if (inw[o] && wd[o] ~ /^[A-Za-z_][A-Za-z0-9_]*\+?=$/) { pushc("arr"); return }
        endword(o)
        if (match(substr(s, i + 1), /^[ \t]*\)/)) { i += RLENGTH; need[o] = !noc[o]; wrap[o] = ""; parg[o] = 0; return }
        if (cs[o] == 3) return
        if (need[o] && substr(s, i + 1, 1) == "(") { i++; pusha(); return }
        pushc("par"); return
    }
    if (c == ")") {
        if (cs[o] == 3) { endword(o); cs[o] = 4; need[o] = 1; wrap[o] = ""; parg[o] = 0; return }
        endword(o); fin(o)
        t = ct[o]
        if (t == "dol" || t == "par" || t == "arr" || t == "psub") { d--; if (t == "par" && iscmd(ct[d])) need[d] = 0; return }
        sep(o); return
    }
    addc(o, c)
}
function achr(v) {
    v = v % 256
    if (v == 0) { anul[d] = 1; return "" }
    return v < 128 ? sprintf("%c", v) : "?"
}
function ansiesc(s, o,   e, v, k, m, h) {
    i++; e = substr(s, i, 1)
    if (e == "") return
    if (e == "x" || e == "u" || e == "U") {
        m = (e == "x") ? 2 : ((e == "u") ? 4 : 8); v = 0
        for (k = 0; k < m && (h = dig("0123456789abcdef", tolower(substr(s, i + 1, 1)))); k++) { v = v * 16 + h - 1; i++ }
        if (k == 0) addc(o, "\\" e); else addc(o, achr(v))
        return
    }
    if ((h = dig("01234567", e))) {
        v = h - 1
        for (k = 1; k < 3 && (h = dig("01234567", substr(s, i + 1, 1))); k++) { v = v * 8 + h - 1; i++ }
        addc(o, achr(v)); return
    }
    if (e == "c") { i++; addc(o, substr(s, i, 1) == "@" ? achr(0) : "?"); return }
    if (dig("abeEfnrtv", e)) { addc(o, "?"); return }
    if (e == "\\" || e == "\047" || e == "\"" || e == "?") { addc(o, e); return }
    addc(o, "\\" e)
}
function qchar(s, n, c,   o, t) {
    t = ct[d]; o = own[d]
    if (t == "sq") { if (c == "\047") d--; else addc(o, c); return }
    if (t == "ansi") {
        if (c == "\047") { d--; return }
        if (c == "\\") { if (anul[d]) i++; else ansiesc(s, o); return }
        if (!anul[d]) addc(o, c)
        return
    }
    if (c == "\"") { d--; return }
    if (c == "\\") { if (i == n) { i = n + 1; return }; i++; addc(o, substr(s, i, 1)); return }
    if (c == "`") { addc(o, "$()"); pushc("bt"); return }
    if (c == "$" && substr(s, i + 1, 1) == "(") {
        addc(o, "$()")
        if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
        return
    }
    addc(o, c)
}
function arithchar(s, n, c) {
    if (c == "(") { ad[d]++; return }
    if (c == ")") { ad[d]--; if (ad[d] <= 0) d--; return }
    if (c == "`") { pushc("bt"); return }
    if (c == "$" && substr(s, i + 1, 1) == "(" && substr(s, i + 2, 1) != "(") { i++; pushc("dol") }
}
function hdocchar(s, n, c) {
    if (!hexp[d]) return
    if (c == "\\") { if (i == n) { hjoin = 1; i = n + 1; return }; i++; return }
    if (c == "`") { pushc("bt"); return }
    if (c == "$" && substr(s, i + 1, 1) == "(") {
        if (substr(s, i + 2, 1) == "(") { i += 2; pusha() } else { i++; pushc("dol") }
    }
}
BEGIN {
    argopt["sudo", "-u"] = 1; argopt["sudo", "-g"] = 1; argopt["sudo", "-C"] = 1
    argopt["sudo", "-h"] = 1; argopt["sudo", "-p"] = 1; argopt["sudo", "-U"] = 1
    argopt["sudo", "-r"] = 1; argopt["sudo", "-t"] = 1; argopt["sudo", "-D"] = 1
    argopt["sudo", "-R"] = 1; argopt["nice", "-n"] = 1; argopt["env", "-u"] = 1
    argopt["env", "-C"] = 1; argopt["exec", "-a"] = 1; argopt["timeout", "-s"] = 1
    argopt["timeout", "-k"] = 1; argopt["time", "-f"] = 1; argopt["time", "-o"] = 1
    argopt["sudo", "-T"] = 1; argopt["env", "-a"] = 1
    lopt["sudo"] = " --user --group --close-from --host --prompt --other-user --role --type --chdir --chroot --command-timeout "
    lopt["nice"] = " --adjustment "; lopt["env"] = " --unset --chdir --argv0 "
    lopt["timeout"] = " --signal --kill-after "; lopt["time"] = " --format --output "
}
{ L[NR] = $0 }
END {
    d = 0; pushc("top"); qh = 1; qt = 1; hjoin = 0
    for (li = 1; li <= NR; li++) {
        s = L[li]; n = length(s)
        if (ct[d] == "hdoc") {
            line = s
            if (hstrip[d]) sub(/^\t+/, "", line)
            if (!hjoin && line == hdelim[d]) { d--; nexthdoc(); continue }
            hjoin = 0
            if (!hexp[d]) continue
        }
        for (i = 1; i <= n + 1; i++) {
            c = (i <= n) ? substr(s, i, 1) : "\n"
            t = ct[d]
            if (iscmd(t)) cmdchar(s, n, c)
            else if (t == "dq" || t == "sq" || t == "ansi") qchar(s, n, c)
            else if (t == "arith") arithchar(s, n, c)
            else if (t == "hdoc") hdocchar(s, n, c)
        }
    }
    while (d >= 1) { if (iscmd(ct[d])) { endword(d); fin(d) }; d-- }
}
AWK

INPUT="$(cat 2>/dev/null || true)"
[ -n "$INPUT" ] || exit 0

WORD="$(printf '%s' "$INPUT" \
    | jq -j 'if .tool_name == "Bash" then (.tool_input.command // "" | strings) else "" end' 2>/dev/null \
    | LC_ALL=C awk "$SCANNER" 2>/dev/null)" || WORD=""

[ "$WORD" = "orca" ] || exit 0

cat >&2 <<'MSG'
ORCA WORKTREE BLOCK: every Orca worktree gets an agent, and this command runs `orca worktree create` without `--agent`.
Use: orca worktree create --name <name> --agent claude --prompt "<task>"
The eligible session that creates the worktree owns that agent.
A supervised coordinator is person-opened; workers cannot create worktrees or dispatch workers.
Supervised workers use `orca orchestration worker-start`.
MSG
exit 2
