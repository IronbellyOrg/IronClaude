import json, pathlib, importlib.util, sys, tempfile, os

# reuse the test's slicer + the real modules
spec = importlib.util.spec_from_file_location("trr", "tests/roadmap/test_recurrence_regression.py")
trr = importlib.util.module_from_spec(spec); sys.modules["trr"] = trr; spec.loader.exec_module(trr)
from superclaude.cli.roadmap.id_registry import build_id_registry, extract_roadmap_ids
from superclaude.cli.roadmap import gates as _gates

fx = pathlib.Path("tests/roadmap/fixtures/recurrence/id_containment/milestone_id_case.md")
case = fx.read_text()
spec_body = trr._slice_section(case, "spec")
roadmap_body = trr._slice_section(case, "roadmap")

d = tempfile.mkdtemp(); tmp = pathlib.Path(d) / "spec.md"; tmp.write_text(spec_body)
reg = build_id_registry(tmp)
print("SPEC registry:")
print("  fr_ids  =", list(reg.fr_ids))
print("  nfr_ids =", list(reg.nfr_ids))
print("  d_ids   =", list(reg.d_ids))
print("  md_ids  =", list(reg.md_ids))
known = reg.union_of_known()
road = extract_roadmap_ids(roadmap_body)
phantoms = sorted(road - known)
print("ROADMAP extracted ids =", sorted(road))
print("union_of_known        =", sorted(known))
print("phantoms (road-known) =", phantoms)
sc = pathlib.Path(d) / "sidecar.json"; sc.write_text(json.dumps(reg.to_dict()))
_gates.set_id_registry_sidecar_path(sc)
res = _gates._roadmap_ids_within_spec(roadmap_body)
_gates.set_id_registry_sidecar_path(None)
print("_roadmap_ids_within_spec result type:", type(res).__name__)
print("_roadmap_ids_within_spec result:", repr(res)[:200])
print("md_in_phantoms:", {p for p in phantoms if "-D" in p and p[:1] == "M"})
