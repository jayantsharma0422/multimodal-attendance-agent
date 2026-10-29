import os
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

from modules.vision import analyze_video
from modules.audio import analyze_audio
from modules.analytics import make_recommendations, summarize_attendance

st.set_page_config(page_title="Multimodal Attendance & Engagement Agent",
                   page_icon="🎓", layout="wide")
st.title("🎓 Multimodal Attendance & Engagement Agent")
st.caption("Offline-first classroom attendance and session activity analytics — MVP")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")

def load_records():
    cols = ["date", "session", "student_id", "student_name", "status", "notes"]
    if os.path.exists(ATTENDANCE_FILE):
        try:
            df = pd.read_csv(ATTENDANCE_FILE).fillna("")
            for c in cols:
                if c not in df.columns:
                    df[c] = ""
            return df[cols]
        except Exception:
            pass
    return pd.DataFrame(columns=cols)

def save_records(df):
    df.to_csv(ATTENDANCE_FILE, index=False)

records = load_records()
tabs = st.tabs(["Dashboard", "Attendance", "Video Analysis", "Audio Analysis", "About"])

with tabs[0]:
    st.subheader("Session overview")
    total = len(records)
    present = int((records["status"].astype(str).str.lower() == "present").sum()) if total else 0
    rate = round(present / total * 100, 1) if total else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("Attendance records", total)
    c2.metric("Marked present", present)
    c3.metric("Recorded attendance rate", f"{rate}%")
    if total:
        st.dataframe(records, use_container_width=True)
        by_status = records["status"].value_counts().rename_axis("Status").reset_index(name="Count")
        st.plotly_chart(px.bar(by_status, x="Status", y="Count", title="Attendance by status"), use_container_width=True)
    else:
        st.info("No attendance records yet. Open the Attendance tab to add a session.")
    st.subheader("Suggested actions")
    for item in make_recommendations(records):
        st.write("• " + item)

with tabs[1]:
    st.subheader("Record attendance")
    st.write("This MVP stores attendance locally in data/attendance.csv.")
    with st.form("attendance_form", clear_on_submit=True):
        date = st.date_input("Session date", value=datetime.today().date())
        session = st.text_input("Session / class name", value="Class 1")
        student_id = st.text_input("Student ID")
        student_name = st.text_input("Student name")
        status = st.selectbox("Attendance status", ["Present", "Absent", "Late"])
        notes = st.text_input("Notes (optional)")
        submitted = st.form_submit_button("Save attendance")
    if submitted:
        if not student_id.strip() or not student_name.strip():
            st.error("Enter both Student ID and Student name.")
        else:
            new_row = pd.DataFrame([{
                "date": str(date), "session": session.strip(),
                "student_id": student_id.strip(), "student_name": student_name.strip(),
                "status": status, "notes": notes.strip()
            }])
            records = pd.concat([load_records(), new_row], ignore_index=True)
            save_records(records)
            st.success("Attendance saved locally.")
            st.rerun()

    st.subheader("Current records")
    records = load_records()
    if not records.empty:
        edited = st.data_editor(records, num_rows="dynamic", use_container_width=True, key="attendance_editor")
        left, right = st.columns(2)
        with left:
            if st.button("Save table edits"):
                save_records(edited)
                st.success("Table saved.")
                st.rerun()
        with right:
            csv_bytes = records.to_csv(index=False).encode("utf-8")
            st.download_button("Download attendance CSV", csv_bytes, "attendance.csv", "text/csv")
        if st.button("Delete all attendance records", type="secondary"):
            save_records(pd.DataFrame(columns=records.columns))
            st.rerun()
    else:
        st.caption("Records will appear here after you add them.")

with tabs[2]:
    st.subheader("Video activity analysis")
    st.warning("Privacy note: this module detects people in video frames; it does not identify students or automatically prove attendance. Use consented recordings and verify results manually.")
    video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
    sample_every = st.slider("Analyze every Nth frame", 1, 30, 5)
    if video is not None and st.button("Analyze video"):
        with st.spinner("Analyzing video locally..."):
            result = analyze_video(video, sample_every)
        if result.get("error"):
            st.error(result["error"])
        else:
            a, b, c = st.columns(3)
            a.metric("Frames sampled", result["frames_sampled"])
            b.metric("Frames with people detected", result["frames_with_people"])
            c.metric("Maximum people in a sampled frame", result["max_people"])
            st.write(f"Approximate video duration: {result['duration_seconds']:.1f} seconds")
            st.info("Treat these as approximate activity indicators, not verified student counts.")

with tabs[3]:
    st.subheader("Audio activity analysis")
    st.warning("This estimates sound/speech-like activity from signal energy. It does not transcribe speech, identify speakers, or measure learning.")
    audio = st.file_uploader("Upload a WAV audio file", type=["wav"])
    threshold = st.slider("Activity threshold (relative)", 0.01, 0.30, 0.05, 0.01)
    if audio is not None and st.button("Analyze audio"):
        with st.spinner("Analyzing audio locally..."):
            result = analyze_audio(audio, threshold)
        if result.get("error"):
            st.error(result["error"])
        else:
            a, b, c = st.columns(3)
            a.metric("Duration", f"{result['duration_seconds']:.1f} s")
            b.metric("Active audio", f"{result['active_percent']:.1f}%")
            c.metric("RMS energy", f"{result['rms']:.4f}")
            st.write("Interpretation:", result["interpretation"])

with tabs[4]:
    st.subheader("Project information")
    st.markdown("""
**Purpose:** A small offline-first prototype demonstrating multimodal classroom session support.

**Implemented in this MVP**
- Local attendance entry, editing, CSV export and persistent CSV storage.
- OpenCV HOG-based people detection on sampled video frames.
- WAV audio energy/activity estimation.
- Attendance dashboard, charts and rule-based recommendations.

**Limitations**
- Video detection is not face recognition and does not automatically assign identity.
- Audio activity is not speech recognition or a reliable measure of engagement.
- Recommendations are simple rules, not a trained AI model.
- For real deployment, add consent, access controls, retention policies, testing and institution approval.
""")
