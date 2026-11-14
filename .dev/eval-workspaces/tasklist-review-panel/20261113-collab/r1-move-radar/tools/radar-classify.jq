# radar-classify.jq: the deterministic classifier (R-31). One tele record in, {"n":..,"sig":[..]} out.
# Usage: jq -c --slurpfile ix index/<pkg>.json --arg srcpath SB/cand/<pkg>/source.md -f radar-classify.jq
# Signatures: M1 M2 M4 M7 SRC_OPENED UNNAMED_TEST (never M3 M5 M6 M8 M9 M10). DESIGN.md section 2.3.
# Input lines may be raw text (jq -R): unparsable lines and lines that are not JSON objects are skipped.

def rec: (if type == "string" then (fromjson? // empty) else . end) | select(type == "object");
($ix[0]) as $ix
| ($srcpath | sub("/cand/(?<p>[^/]+)/source\\.md$"; "/\(.p)/repo")) as $repo
| ($srcpath | capture("/cand/(?<p>[^/]+)/source\\.md$").p // "") as $pkg
| def norm: tostring | sub("^" + ($repo | gsub("[.]"; "\\.")) + "/?"; "") | sub("^\\./"; "") | if . == "" then "." else . end;
  def under_tests: . == "tests" or . == "tests/" or startswith("tests/");
  def is_root: . == "." or . == "./" or . == $repo or . == ($repo + "/");
  def has_entry: . as $s | any($ix.paths[] , $ix.keys[]; . as $e | $s | contains($e));
  def unq: if test("^\".*\"$") or test("^'.*'$") then .[1:-1] else . end;
  # the search segments of a Bash command: text after each grep/egrep/rg up to the next shell separator
  def segs: [match("\\b(e?grep|rg)\\b([^|;&]*)"; "g") | {tool: .captures[0].string, rest: .captures[1].string}];
  def toks: [match("\"[^\"]*\"|'[^']*'|[^\\s]+"; "g") | .string];
  def recursive: .tool == "rg" or (.rest | test("(^|\\s)(-[A-Za-z]*[rR][A-Za-z]*|--recursive)(\\s|$)"));
  # pattern: first quoted argument, else first token that does not start with -
  def pattern: (.rest | toks) as $t
    | (([$t[] | select(test("^[\"']"))] | first) // ([$t[] | select(startswith("-") | not)] | first) // "") | unq;
  def pathargs: (.rest | toks | map(select(startswith("-") | not))) as $t
    | (([.rest | toks[] | select(test("^[\"']"))] | first) // ($t | first)) as $pat
    | ($t | index($pat)) as $i | if $i == null then [] else $t[$i + 1:] | map(unq | norm) end;
  rec
  | . as $r
  | (if ($r.sub // false) then []
     else
       ($r.tool) as $tool | ($r.input | if type == "object" then . else {} end) as $in
       | (if $tool == "Bash" then ($in.command // "" | tostring) else "" end) as $cmd
       | ($cmd | segs) as $segs
       | (if $tool == "Grep" then {pat: ($in.pattern // "" | tostring), gpath: (if $in.path then ($in.path | norm) else null end), mode: ($in.output_mode // null)} else null end) as $g
       | [
           # M1: recursive grep over tests/ naming a plan path or key
           (if ($segs | any(recursive and (pathargs | any(under_tests)))) and ($cmd | has_entry) then "M1" else empty end),
           (if $g and ($g.gpath // "." | under_tests) and ($g.pat | has_entry) then "M1" else empty end),
           # M2: listing or counting across a directory
           # (the -l/-c/-L test looks only at the option tokens of each grep segment, never at later commands)
           (if $tool == "Bash" and (($segs | any(.tool != "rg" and (.rest | toks | any(test("^-[A-Za-z]*[lcL][A-Za-z]*$")))))
                                    or ($cmd | test("\\bfind\\s|\\|\\s*wc\\s+-l"))) then "M2" else empty end),
           (if $g and ($g.mode == "files_with_matches" or $g.mode == "count") then "M2" else empty end),
           # M4: grep whose pattern equals a quoted criterion pattern
           (if ($segs | any(.tool != "rg" and (pattern as $p | $ix.criterion_greps | index($p) != null))) then "M4" else empty end),
           (if $g and ($ix.criterion_greps | index($g.pat | unq) != null) then "M4" else empty end),
           # M7: search from the repository root, or naming a root file
           (if ($segs | any(recursive and ((pathargs | any(is_root)) or (.tool == "rg" and (pathargs | length) == 0)))) then "M7" else empty end),
           (if $g and ($g.gpath == null or ($g.gpath | is_root)) then "M7" else empty end),
           (if ($segs | any(pathargs | any(. as $p | $ix.root_files | index($p) != null)))
               or ($g and ($g.gpath // "" | . as $p | $ix.root_files | index($p) != null)) then "M7" else empty end),
           # SRC_OPENED: the package's source.md is read
           (if ($tool == "Read" and (($in.file_path // "") | tostring | endswith("/cand/" + $pkg + "/source.md")))
               or ($tool == "Bash" and ($cmd | test("\\b(cat|sed|head|tail|less|nl|awk)\\b")) and ($cmd | contains("cand/" + $pkg + "/source.md")))
            then "SRC_OPENED" else empty end),
           # UNNAMED_TEST: a test file the candidate never names
           (if $tool == "Read" and (($in.file_path // "") | norm | . as $p | (under_tests and ($ix.paths | index($p) == null))) then "UNNAMED_TEST" else empty end)
         ] | unique
     end) as $sig
  | {n: $r.n, sig: $sig}
