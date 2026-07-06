import json, pathlib, tempfile
from superclaude.cli.roadmap.id_registry import build_id_registry, extract_roadmap_ids
from superclaude.cli.roadmap import gates as _gates

def slice_section(text, heading):
    marker = f"\n## {heading}\n"
    if marker not in text:
        marker = f"## {heading}\n"
    start = text.index(marker) + len(marker)
    rest = text[start:]
    nxt = rest.find("\n## ")
    return rest if nxt == -1 else rest[:nxt]

fx = pathlib.Path("tests/roadmap/fixtures/recurrence/id_containment/milestone_id_case.md")
case = fx.read_text()
spec_body = slice_section(case, "spec")
roadmap_body = slice_section(case, "roadmap")

d = tempfile.mkdtemp(); tmp = pathlib.Path(d) / "spec.md"; tmp.write_text(spec_body)
reg = build_id_registry(tmp)
print("SPEC  fr=%s nfr=%s d=%s md=%s" % (list(reg.fr_ids), list(reg.nfr_ids), list(reg.d_ids), list(reg.md_ids)))
known = reg.union_of_known()
road = extract_roadmap_ids(roadmap_body)
phantoms = sorted(road - known)
print("ROADMAP ids =", sorted(road))
print("phantoms    =", phantoms)
print("md_in_phantoms =", sorted({p for p in phantoms if "-D" in p and p[:1] == "M"}))
sc = pathlib.Path(d) / "sc.json"; sc.write_text(json.dumps(reg.to_dict()))
_gates.set_id_registry_sidecar_path(sc)
res = _gates._roadmap_ids_within_spec(roadmap_body)
_gates.set_id_registry_sidecar_path(None)
print("result_type =", type(res).__name__)
print("result =", repr(res))
