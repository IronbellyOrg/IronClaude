"""Fill the mechanical placeholders of REPORT.md (header counts, status, INF table)."""
from pathlib import Path

OUT = Path(".dev/reflect/pre-design-20261108041729")
rep = (OUT / "REPORT.md").read_text()
table = (OUT / "artifacts/inf-table.md").read_text().rstrip("\n")
rep = rep.replace("{{INF_TABLE}}", table)
rep = rep.replace("status: {{RF_PLACEHOLDER:status}}", "status: partial")
rep = rep.replace("citations_total: {{RF_PLACEHOLDER:citations_total}}", "citations_total: 74")
rep = rep.replace("citations_revalidated: {{RF_PLACEHOLDER:citations_revalidated}}", "citations_revalidated: 74")
rep = rep.replace("citations_dropped: {{RF_PLACEHOLDER:citations_dropped}}", "citations_dropped: 1")
rep = rep.replace("Inferred-fraction: 1 / {{RF_PLACEHOLDER:citations_total}}", "Inferred-fraction: 1 / 74 = 0.01")
assert "RF_PLACEHOLDER" not in rep and "{{INF_TABLE}}" not in rep
(OUT / "REPORT.md").write_text(rep)
print("filled", len(rep.splitlines()), "lines")
