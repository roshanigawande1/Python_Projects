"""Small adapter between Python orchestration and MATLAB/Simulink."""

from __future__ import annotations

from pathlib import Path
import time

import pandas as pd


class MatlabAdapter:
    """Run one model either in demonstration mode or through MATLAB Engine."""

    def __init__(self, matlab_scripts: Path, demo_mode: bool = False) -> None:
        self.matlab_scripts = matlab_scripts
        self.demo_mode = demo_mode
        self.engine = None

    def start(self) -> None:
        if self.demo_mode:
            return

        try:
            import matlab.engine # pyright: ignore[reportMissingImports]
        except ImportError as exc:
            raise RuntimeError(
                "MATLAB Engine for Python is not installed. Use Demo mode or install it."
            ) from exc

        self.engine = matlab.engine.start_matlab("-nodesktop -nosplash")
        self.engine.addpath(str(self.matlab_scripts), nargout=0)

    def stop(self) -> None:
        if self.engine is not None:
            self.engine.quit()
            self.engine = None

    def run_model(
        self,
        model_id: str,
        model_path: Path,
        test_file: Path,
        report_folder: Path,
        create_coverage: bool,
    ) -> pd.DataFrame:
        report_folder.mkdir(parents=True, exist_ok=True)

        if self.demo_mode:
            return self._run_demo(model_id, report_folder, create_coverage)

        if self.engine is None:
            raise RuntimeError("MATLAB Engine was not started.")

        self.engine.runOneModel(
            str(test_file),
            str(model_path),
            str(report_folder),
            bool(create_coverage),
            nargout=0,
        )

        result_path = report_folder / "TestExecutionReport.xlsx"
        if not result_path.exists():
            raise RuntimeError("MATLAB did not create TestExecutionReport.xlsx.")

        return pd.read_excel(result_path)

    @staticmethod
    def _run_demo(
        model_id: str, report_folder: Path, create_coverage: bool
    ) -> pd.DataFrame:
        """Create predictable sample results for a UI demonstration."""
        time.sleep(0.5)

        rows = [
            {
                "TestID": "TC_001",
                "Description": "Nominal operating condition",
                "Status": "PASS",
                "Details": "All expected outputs matched.",
            },
            {
                "TestID": "TC_002",
                "Description": "Boundary input condition",
                "Status": "FAIL" if model_id.lower().startswith("brake") else "PASS",
                "Details": (
                    "VehicleSpeed: expected 0.0, actual 4.2"
                    if model_id.lower().startswith("brake")
                    else "All expected outputs matched."
                ),
            },
            {
                "TestID": "TC_003",
                "Description": "Invalid sensor condition",
                "Status": "PASS",
                "Details": "All expected outputs matched.",
            },
        ]

        results = pd.DataFrame(rows)
        results.to_excel(report_folder / "TestExecutionReport.xlsx", index=False)

        if create_coverage:
            (report_folder / "ModelCoverageReport.html").write_text(
                "<h1>Demonstration coverage report</h1>"
                f"<p>Model: {model_id}</p>"
                "<p>Replace Demo mode with MATLAB Engine for real coverage.</p>",
                encoding="utf-8",
            )

        return results
