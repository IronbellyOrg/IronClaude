# How to export a report

The exporter writes 3 report formats, and the guide lists each of them.

Only the `report.py` module renders a report, so no other module needs a format switch.

Export one report with this command:

```bash
exporter run --format csv --out reports/
```

The command prints `report_exporter done` when it ends.

## Retention window

The retention job removes an expired report. It never touches a report under legal hold.
