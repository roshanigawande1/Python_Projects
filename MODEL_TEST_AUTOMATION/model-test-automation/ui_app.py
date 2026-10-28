"""Streamlit UI for MATLAB Model Test Automation."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from orchestrator import run_manifest, validate_manifest

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MANIFEST = PROJECT_ROOT / "tests" / "ModelManifest.xlsx"

st.set_page_config(page_title="Model Test Automation", page_icon="✅", layout="wide")
st.title("MATLAB Model Test Automation")
st.caption("Python manages the run. MATLAB/Simulink executes the models.")

with st.sidebar:
    st.header("Project input")
    uploaded_manifest = st.file_uploader("Upload ModelManifest.xlsx", type=["xlsx"])
    demo_mode = st.toggle("Demo mode", value=True, help="Runs sample results without MATLAB.")
    create_coverage = st.checkbox("Generate coverage HTML reports", value=True)
    st.info("Use Demo mode for an interview demonstration. Disable it for real .slx models.")

manifest_path = DEFAULT_MANIFEST
if uploaded_manifest is not None:
    uploaded_dir = PROJECT_ROOT / "reports" / "uploaded-input"
    uploaded_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = uploaded_dir / uploaded_manifest.name
    manifest_path.write_bytes(uploaded_manifest.getvalue())

st.subheader("Execution options")
left, right = st.columns([2, 1])
with left:
    st.text_input("Manifest", value=str(manifest_path), disabled=True)
with right:
    st.selectbox("Execution mode", ["Serial — recommended", "Parallel — future option"], disabled=True)

validation_errors = validate_manifest(manifest_path, PROJECT_ROOT, demo_mode)
if validation_errors:
    st.error("Fix these items before running:\n\n" + "\n".join(f"- {error}" for error in validation_errors))
    run_allowed = False
else:
    st.success("Manifest validation passed.")
    run_allowed = True

if st.button("Run selected models", type="primary", disabled=not run_allowed):
    progress = st.progress(0, text="Preparing test run")
    log = st.empty()

    def update_progress(done: int, total: int, message: str) -> None:
        progress.progress(int(100 * done / total), text=message)
        log.code(message)

    try:
        results, run_folder, excel_path, dashboard_path = run_manifest(
            manifest_path=manifest_path,
            project_root=PROJECT_ROOT,
            create_coverage=create_coverage,
            demo_mode=demo_mode,
            progress_callback=update_progress,
        )
        progress.progress(100, text="Test run completed")
        st.session_state["last_results"] = results
        st.session_state["last_run_folder"] = run_folder
        st.session_state["combined_excel"] = excel_path
        st.session_state["dashboard"] = dashboard_path
        st.success(f"Reports saved in {run_folder}")
    except Exception as exc:
        st.exception(exc)

if "last_results" in st.session_state:
    results = st.session_state["last_results"]
    st.subheader("Results dashboard")
    total, passed, failed, errors = st.columns(4)
    total.metric("Total test cases", len(results))
    passed.metric("Passed", int((results.Status == "PASS").sum()))
    failed.metric("Failed", int((results.Status == "FAIL").sum()))
    errors.metric("Errors", int((results.Status == "ERROR").sum()))

    st.dataframe(results, use_container_width=True, hide_index=True)

    st.subheader("Downloads")
    excel_path = st.session_state["combined_excel"]
    dashboard_path = st.session_state["dashboard"]
    st.download_button("Download combined Excel report", excel_path.read_bytes(), excel_path.name)
    st.download_button("Download HTML dashboard", dashboard_path.read_bytes(), dashboard_path.name)
    st.caption(f"Individual reports are in: {st.session_state['last_run_folder']}")
