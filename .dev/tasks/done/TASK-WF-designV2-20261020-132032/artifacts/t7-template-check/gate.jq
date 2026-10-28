# Invariant program J1-J22. Reads only $ledger (slurped candidates.json) and $review (raw REVIEW.md).
# Never reads jq_exit. Contains no single-quote character, so it is safe to paste inside single quotes.
def L: ($ledger[0] // {});
def C: (L.candidates // []);
def PL: "^[^\\s:]+:[0-9]+(-[0-9]+)?$";
def ispl: type == "string" and test(PL);
def nz: type == "string" and length > 0;
def DEF: C | map(select(.disposition == "defect"));
def UD: DEF | map(select(.merged_into == null));
def IDS: C | map(.id);
def BYID: C | map({key: (.id | tostring), value: .}) | from_entries;
def root_of($m; $id; $lim):
  {cur: $id, n: 0}
  | until(($m[.cur].merged_into // null) == null or .n > $lim; {cur: $m[.cur].merged_into, n: (.n + 1)})
  | if .n > $lim then null else .cur end;
def BASIS: ["critical:1","critical:2","critical:3","critical:4","high:1","high:2","high:3","high:4","high:5","high:6","medium:1","medium:2","medium:3","medium:4","medium:5","low:1","low:2","low:3","nit:1","nit:2","nit:3"];
def SEV: ["critical","high","medium","low","nit"];
def formok: type == "string" and (
  test("^checked: [^\\s:]+:[0-9]+(-[0-9]+)?( blocks| does_not_block)?$")
  or test("^not_applicable: \\S")
  or test("^mechanical: (grep .+ in [^ ]+ = 0 hits|lines [^ ]+ = [0-9]+)$"));
def blocking: [(.refutation_citation // empty), ((.refutation // [])[] | strings | capture("^checked: (?<c>[^ ]+) blocks$").c)];
def FENCE: "^ {0,3}(?<f>" + ([96] | implode) + "{3,}|~{3,})(?<info>.*)$";
def rows:
  reduce (($review | split("\n"))[] | rtrimstr("\r")) as $l ({f: null, o: []};
    ([$l | capture(FENCE)] | .[0]) as $m
    | if .f == null then
        if $m != null then .f = {c: ($m.f | .[0:1]), n: ($m.f | length)} else .o += [$l] end
      elif $m != null and ($m.f | .[0:1]) == .f.c and ($m.f | length) >= .f.n and ($m.info | test("^\\s*$")) then .f = null
      else . end) | .o;
def ann:
  reduce rows[] as $l ({sec: "header", sub: null, ent: null, kind: null, n: 0, out: []};
    ($l | test("^#{1,6}\\s")) as $head
    | (if $head then ($l | capture("^(?<h>#{1,6})\\s").h | length) else 0 end) as $lvl
    | (($l == "") or ($l | test("^\\s"))) as $cont
    | if $head then
        if $lvl == 2 then
          .sec = (if ($l | test("^##\\s+Findings")) then "findings" elif ($l | test("^##\\s+Architectural")) then "cross" else "other" end)
          | .sub = null | .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: true}]
        elif $lvl == 3 then
          .sub = (if ($l | test("[Nn]its")) then "nits" else "other" end) | .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: true}]
        elif $lvl == 4 and .sec == "findings" then
          .n += 1 | .ent = .n | .kind = "h"
          | .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: true}]
        elif $lvl >= 5 and .kind == "h" then
          .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: true}]
        else
          .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: true}]
        end
      elif ($l | test("^[-*]\\s")) then
        if .kind == "h" then
          .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: false}]
        elif (.sec == "cross" or (.sec == "findings" and .sub == "nits")) then
          .n += 1 | .ent = .n | .kind = "l"
          | .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "l", head: false}]
        else
          .ent = null | .kind = null
          | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: false}]
        end
      elif $cont then
        .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: .kind, head: false}]
      elif .kind == "h" then
        .out += [{t: $l, sec: .sec, sub: .sub, e: .ent, k: "h", head: false}]
      else
        .ent = null | .kind = null
        | .out += [{t: $l, sec: .sec, sub: .sub, e: null, k: null, head: false}]
      end) | .out;
def HTAG: "^#{1,6}\\s.*\\(id: (?<id>[^)\\s]+)\\)\\s*$";
def LTAG: "^\\s*[-*]\\s+<!-- id: (?<id>[^\\s]+) -->";
def tagof: (try capture(HTAG).id catch null) // (try capture(LTAG).id catch null);
def TAGS: [ann[] | .t | tagof | select(. != null)];
def ENTRIES: [ann[] | select(.e != null)] | group_by(.e) | map({sec: .[0].sec, k: .[0].k, start: .[0].t, lines: map(.t), id: ((.[0].t | tagof) // null)});
def haspl: test("(?:[A-Za-z0-9_@+.-]+/)+[A-Za-z0-9_@+.-]+:[0-9]+|[A-Za-z0-9_@+-]+\\.[A-Za-z0-9]{1,10}:[0-9]+");
def checks:
  {
    "SHAPE": (try (
      (L.run_status | IN("success","partial","failed"))
      and ((L.findings_count | type) == "object")
      and all(SEV[]; . as $s | (L.findings_count[$s] | type) == "number")
      and ((L.candidates | type) == "array")
      and all(C[]; (.evidence_sources | type) == "array"
        and all(.evidence_sources[]; (.hop | IN("observed","entrypoint","producer","guard","intent","prerequisite","scope"))
          and (.source | IN("local_read","head_object","diff_new_side")) and (.path_line | ispl)))
      and ((L.target | type) == "object")
      and ((L.coverage | type) == "object") and ((L.coverage.complete | type) == "boolean")
      and ((L.coverage.chunks_skipped | type) == "array") and ((L.coverage.input_truncated | type) == "boolean")
    ) catch false),
    "J1": (try all(C[]; (.disposition | IN("defect","unproven","rejected","intentional_limitation","documented_prerequisite")) and (.class | IN("behavioral","structural"))) catch false),
    "J2": (try all(C[]; ((.severity != null) == (.disposition == "defect")) and (.severity == null or (.severity | IN(SEV[])))) catch false),
    "J3": (try all(DEF[];
        (.claim.evidence_kind | IN("runtime_reproduced","static_traced","protocol_literal"))
        and (.claim.harm | nz) and (.claim.violated_requirement | nz)
        and ((.refutation | type) == "array") and ((.refutation | length) > 0) and all(.refutation[]; formok)
        and (if .class == "behavioral" then (.claim.reachability.entrypoint | nz)
             else (((.claim.intent_sources // []) | length) > 0) or any((.refutation // [])[]; startswith("mechanical: ")) end)) catch false),
    "J4": (try all(C[] | select(.disposition | IN("rejected","intentional_limitation","documented_prerequisite"));
        any((.disposition_reasons // [])[]; test("^A[1-7]")) and (.refutation_citation | ispl)) catch false),
    "J5": (try (all(C[]; all((.disposition_reasons // [])[]; type == "string" and test("^(A[1-7]|other:)")))
        and all(C[]; all((.excluded_consequences // [])[]; (.reason | type) == "string" and (.reason | test("^(A[1-7]|other:)"))))) catch false),
    "J6": (try (((IDS | length) == (IDS | unique | length))
        and (([C[].members[]?] | length) == ([C[].members[]?] | unique | length))
        and (((L.dropped_ungrounded // []) | map(if type == "object" then .id else . end)) as $d
             | all(([C[].members[]?] + IDS)[]; . as $i | ($d | index($i)) == null))) catch false),
    "J7": (try (BYID as $m | (C | length) as $n | all(C[] | select(.merged_into != null);
        ($m[.merged_into] != null) and (root_of($m; .id; $n) as $r | $r != null and $m[$r] != null))) catch false),
    "J8": (try (BYID as $m | (C | length) as $n | all(C[] | select(.disposition == "defect" and .merged_into == null);
        . as $r
        | ([C[] | select(root_of($m; .id; $n) == $r.id)]) as $g
        | if ($g | length) < 2 then true
          else all(($g | map(blocking) | flatten | unique)[]; . as $c | any(($r.refutation // [])[]; . == ("checked: " + $c + " does_not_block")))
          end)) catch false),
    "J9": (try (L.findings_count as $f | all(SEV[]; . as $s | $f[$s] == (UD | map(select(.severity == $s)) | length))) catch false),
    "J10": (try (([UD[] | select(.remediation_eligible == true and (.severity | IN("critical","high"))) | .id] | sort) as $e
        | ((L.remediation_ids // []) | sort) == $e
        and (L.remediation_count.critical == ([UD[] | select(.id | IN($e[])) | select(.severity == "critical")] | length))
        and (L.remediation_count.high == ([UD[] | select(.id | IN($e[])) | select(.severity == "high")] | length))) catch false),
    "J11": (try (all(C[] | select(.attribution.current_status == "absent"); .remediation_eligible == false)
        and all(DEF[] | select(.attribution.current_status == "absent"); L.target.mode == "pr")) catch false),
    "J12": (try (if L.target.mode == "snapshot" then all(C[]; .attribution.introduced_in == "not_applicable_snapshot") else true end) catch false),
    "J13": (try ((if L.target.mode == "pr" and L.target.head_match == false then
          (L.target.evidence_source != "local_read")
          and all(C[]; all((.evidence_sources // [])[]; .source != "local_read"))
        else true end)
        and all(DEF[]; all((.evidence_sources // [])[] | select(.source == "head_object"); L.target.head_object_check == "match"))) catch false),
    "J14": (try (all(C[] | select(.claim.qualification != null); .claim.qualification.scope_citation | ispl)
        and all(DEF[];
          (.severity_basis | IN(BASIS[]))
          and (if .claim.qualification != null and (.category | IN("security","data-integrity") | not) and ((.severity_basis | startswith("critical:")) | not)
               then (.severity | IN("medium","low","nit")) else true end))) catch false),
    "J15": (try all(DEF[] | select(.confidence == "low"); .hedge_resolved | nz) catch false),
    "J16": (try ((if L.coverage.complete == false then L.run_status != "success" else true end)
        and (if L.coverage.complete == true then
               ((L.coverage.chunks_skipped // []) | length) == 0 and L.coverage.input_truncated == false
               and all(C[]; all((.disposition_reasons // [])[]; contains("admission_incomplete") | not))
             else true end)) catch false),
    "J17": (try ((UD | map(.id)) as $u | all(TAGS[]; . as $t | ($u | index($t)) != null)) catch false),
    "J18": (try ([ENTRIES[] | select(.sec == "findings" and .k == "h") | .id] as $f | all(UD[] | select(.severity | IN("critical","high")); . as $d | ($f | index($d.id)) != null)) catch false),
    "J19": (try ((ENTRIES | length) == (TAGS | length) and all(ENTRIES[]; .id != null)) catch false),
    "J20": (try all(ann[] | select(.sec != "header" and .e == null); .t | haspl | not) catch false),
    "J21": (try (BYID as $m | all(ENTRIES[]; . as $e
        | ([$e.lines[] | capture("\\*\\*Evidence kind\\*\\*:\\s*`?(?<k>[a-z_]+)`?").k]) as $k
        | ($k | length) > 0 and $m[$e.id].claim.evidence_kind == $k[0])) catch false),
    "J22": (try all(rows[]; test("^#{1,6}\\s+Not Admitted"; "i") | not) catch false)
  };
checks | all(.[]; .)
