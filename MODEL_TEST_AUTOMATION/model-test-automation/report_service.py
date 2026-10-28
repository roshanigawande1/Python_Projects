"""Create one readable report for a complete model-test run."""

from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


def write_run_reports(results: pd.DataFrame, run_folder: Path) -> tuple[Path, Path]:
    """Write the consolidated Excel and HTML reports and return their paths."""
    excel_path = run_folder / "AllModels_TestReport.xlsx"
    html_path = run_folder / "TestDashboard.html"

    summary = (
        results.groupby("Status", dropna=False)
        .size()
        .rename("Count")
        .reset_index()
    )

    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        results.to_excel(writer, sheet_name="All Test Results", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

        workbook = writer.book
        result_sheet = writer.sheets["All Test Results"]
        summary_sheet = writer.sheets["Summary"]

        header = workbook.add_format({
            "bold": True, "font_color": "#FFFFFF", "bg_color": "#1F4E78"
        })
        pass_format = workbook.add_format({"font_color": "#167A45"})
        fail_format = workbook.add_format({"font_color": "#B42318"})

        for column, name in enumerate(results.columns):
            result_sheet.write(0, column, name, header)
            width = min(max(len(name) + 2, 16), 52)
            result_sheet.set_column(column, column, width)

        status_col = results.columns.get_loc("Status")
        result_sheet.conditional_format(
            1, status_col, max(len(results), 1), status_col,
            {"type": "text", "criteria": "containing", "value": "PASS", "format": pass_format},
        )
        result_sheet.conditional_format(
            1, status_col, max(len(results), 1), status_col,
            {"type": "text", "criteria": "containing", "value": "FAIL", "format": fail_format},
        )
        result_sheet.freeze_panes(1, 0)
        summary_sheet.set_column("A:B", 18)

    status_counts = results["Status"].value_counts().to_dict()
    html_path.write_text(_dashboard_html(results, status_counts), encoding="utf-8")
    return excel_path, html_path


def _dashboard_html(results: pd.DataFrame, status_counts: dict[str, int]) -> str:
    rows = "\n".join(
        "<tr>" + "".join(
            f"<td>{_escape(value)}</td>" for value in row
        ) + "</tr>"
        for row in results[["ModelID", "TestID", "Status", "Details"]].fillna("").itertuples(index=False, name=None)
    )
    counts = json.dumps(status_counts)
    return f"""<!doctype html>
<html><head><meta charset=\"utf-8\"><title>Model Test Dashboard</title>
<style>body{{font-family:Arial;margin:32px;color:#1f2937}}table{{border-collapse:collapse;width:100%}}th,td{{padding:10px;border-bottom:1px solid #d1d5db;text-align:left}}th{{background:#1f4e78;color:white}}.cards{{display:flex;gap:12px;margin:18px 0}}.card{{padding:16px;border:1px solid #d1d5db;border-radius:8px;min-width:100px}}.card b{{font-size:24px}}</style>
</head><body><h1>Model Test Dashboard</h1><div class=\"cards\" id=\"cards\"></div>
<table><thead><tr><th>Model</th><th>Test ID</th><th>Status</th><th>Details</th></tr></thead><tbody>{rows}</tbody></table>
<script>const counts={counts}; document.getElementById('cards').innerHTML=Object.entries(counts).map(([key,value])=>`<div class=\"card\"><div>${{key}}</div><b>${{value}}</b></div>`).join('');</script>
</body></html>"""


def _escape(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
