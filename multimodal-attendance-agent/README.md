# Multimodal Attendance & Engagement Agent

An offline-first prototype for classroom attendance records and basic video/audio activity analysis.

## Features
- Manual attendance entry, editing, local CSV persistence and CSV download.
- OpenCV HOG person detection on sampled video frames.
- WAV signal-energy activity estimate.
- Dashboard with attendance metrics, chart and rule-based suggestions.
- Local processing; uploaded media is analyzed temporarily and is not saved by this app.

## Requirements
- Python 3.11 recommended
- Windows, macOS or Linux
- A webcam/video file is optional; WAV file is optional

## Run locally
### Windows PowerShell
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run the environment's executable directly:
```powershell
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Modules
- `modules/vision.py`: sampled-frame people detection using OpenCV's HOG detector.
- `modules/audio.py`: WAV duration, RMS energy and estimated active-audio percentage.
- `modules/analytics.py`: attendance summaries and transparent rule-based suggestions.

## Important limitations and responsible use
This is an educational MVP, not a validated attendance or engagement measurement product. Person detection does not identify individuals or verify presence across a session. Audio energy does not prove speech, identify speakers, or measure attention. Do not use the outputs for grading, discipline or other consequential decisions without independent validation and human review. Obtain consent, follow institutional policies, protect records and delete test data when no longer needed.

## Suggested demo flow
1. Open the Dashboard tab.
2. Add two or three fictional students in Attendance.
3. Download the CSV.
4. Upload a short, consented video in Video Analysis.
5. Upload a PCM WAV file in Audio Analysis.
6. Show the project limitations and local-storage design.

## GitHub submission
1. Create a new **public** GitHub repository named `multimodal-attendance-agent` (unless your institution requires private).
2. Upload the project files, excluding `.venv`, private records and real classroom media.
3. Copy the repository URL.
4. Test the app locally before sharing any demo link.
5. Add the actual repository URL and a working demo URL to SkillWallet. Never invent a demo URL; if you cannot deploy it, ask the mentor whether a screen recording or local demonstration is accepted.

## Future improvements
- Add robust identity-aware attendance only with consent and approved safeguards.
- Add validated speech recognition or speaker-independent audio metrics if required.
- Add tests, user authentication, role-based access, encrypted storage and configurable retention.
- Deploy only after privacy, security and institutional review.
