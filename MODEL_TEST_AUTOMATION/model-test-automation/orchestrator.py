"""Validate a manifest, run every model, and collect one run result."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable

import pandas as pd

from matlab_adapter import MatlabAdapter
from report_service import write_run_reports

REQUIRED_MANIFEST_COLUMNS = {"ModelID", "ModelFile", "TestFile", "Enabled"}


def validate_manifest(manifest_path: Path, project_root: Path, demo_mode: bool) -> list[str]:
    """Return validation messages. An empty list means execution may start."""
    errors: list[str] = []
    try:
        manifest = pd.read_excel(manifest_path)
    except Exception as exc:
        return [f"Cannot read the manifest: {exc}"]

    missing = REQUIRED_MANIFEST_COLUMNS - set(manifest.columns)
    if missing:
        errors.append("Missing columns: " + ", ".join(sorted(missing)))
        return errors

    if manifest.empty:
        errors.append("The manifest has no models.")

    if not (manifest["Enabled"] == 1).any():
        errors.append("No model has Enabled = 1.")

    if not demo_mode:
        for _, row in manifest[manifest["Enabled"] == 1].iterrows():
            model_file = _resolve(project_root, row["ModelFile"])
            test_file = _resolve(project_root, row["TestFile"])
            if not model_file.exists():
                errors.append(f"Missing model: {model_file}")
            if not test_file.exists():
                errors.append(f"Missing test workbook: {test_file}")
    return errors


def run_manifest(
    manifest_path: Path,
    project_root: Path,
    create_coverage: bool,
    demo_mode: bool,
    progress_callback: Callable[[int, int, str], None] | None = None,
) -> tuple[pd.DataFrame, Path, Path, Path]:
    """Run all enabled models and return results plus output locations."""
    validation_errors = validate_manifest(manifest_path, project_root, demo_mode)
    if validation_errors:
        raise ValueError("\n".join(validation_errors))

    manifest = pd.read_excel(manifest_path)
    selected = manifest[manifest["Enabled"] == 1].copy()
    timestamp = datetime.now().strftime("Run_%Y%m%d_%H%M%S")
    run_folder = project_root / "reports" / timestamp
    run_folder.mkdir(parents=True, exist_ok=True)

    adapter = MatlabAdapter(project_root / "matlab", demo_mode=demo_mode)
    result_frames: list[pd.DataFrame] = []

    try:
        adapter.start()
        for completed, (_, row) in enumerate(selected.iterrows(), start=1):
            model_id = str(row["ModelID"])
            if progress_callback:
                progress_callback(completed - 1, len(selected), f"Running {model_id}")

            model_folder = run_folder / model_id
            try:
                model_results = adapter.run_model(
                    model_id=model_id,
                    model_path=_resolve(project_root, row["ModelFile"]),
                    test_file=_resolve(project_root, row["TestFile"]),
                    report_folder=model_folder,
                    create_coverage=create_coverage,
                )
                model_results.insert(0, "ModelID", model_id)
                result_frames.append(model_results)
            except Exception as exc:
                result_frames.append(pd.DataFrame([{
                    "ModelID": model_id,
                    "TestID": "NOT_RUN",
                    "Description": "Model execution failed",
                    "Status": "ERROR",
                    "Details": str(exc),
                }]))

            if progress_callback:
                progress_callback(completed, len(selected), f"Completed {model_id}")
    finally:
        adapter.stop()

    results = pd.concat(result_frames, ignore_index=True)
    excel_path, dashboard_path = write_run_reports(results, run_folder)
    return results, run_folder, excel_path, dashboard_path


def _resolve(project_root: Path, value: object) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else project_root / path
