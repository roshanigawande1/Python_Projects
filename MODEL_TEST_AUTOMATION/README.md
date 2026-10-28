# MATLAB Model Test Automation

This project runs Excel-defined test cases for several Simulink models and creates one combined report.

## Demonstrate the project now

```powershell -how to install dependencies and run project using streamlit 
cd C:\Users\Roshani Gawande\Documents\Codex\2026-09-04\gi\outputs\model-test-automation
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run ui_app.py
or python -m streamlit run ui_app.py
```

Keep **Demo mode** enabled. The app shows realistic sample results without MATLAB or `.slx` files.

## Connect real MATLAB models

1. Install MATLAB, Simulink, and a compatible 64-bit Python version.
2. Install MATLAB Engine API in the same virtual environment:

   ```matlab
   cd(fullfile(matlabroot, "extern", "engines", "python"))
   system("python -m pip install .")
   ```

3. Put `.slx` models in `models/`.
4. Update `tests/ModelManifest.xlsx` with model and test workbook paths.
5. In every model, enable signal logging and log every signal named in the `Expected` sheet.
6. Disable Demo mode and click **Run selected models**.

## Workbook format

Each model test workbook needs these sheets:

- `TestCases`: `TestID`, `Description`, `StopTime`
- `Inputs`: `TestID`, `Variable`, `Value`
- `Expected`: `TestID`, `Signal`, `ExpectedFinalValue`, `AbsTol`

This starter accepts scalar numeric input values and compares the final logged signal value. Extend `runExcelModelTests.m` when your models use time-series inputs or need full signal comparison.

## Output

Every run creates a dated folder under `reports/`. It contains per-model Excel reports, an optional coverage HTML report, one combined Excel report, and an HTML dashboard.
