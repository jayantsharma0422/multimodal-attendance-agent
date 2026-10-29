def summarize_attendance(records):
    if records is None or records.empty:
        return {"total": 0, "present": 0, "rate": 0.0}
    total = len(records)
    present = int((records["status"].astype(str).str.lower() == "present").sum())
    return {"total": total, "present": present, "rate": round(present / total * 100, 1)}

def make_recommendations(records):
    if records is None or records.empty:
        return [
            "Add attendance records to begin generating summaries.",
            "Test the video and audio modules with short, consented sample files.",
            "Review the results manually before using them for any decisions."
        ]
    status = records["status"].astype(str).str.lower()
    total = len(records)
    present = int((status == "present").sum())
    rate = present / total * 100 if total else 0
    tips = []
    if rate < 75:
        tips.append("Recorded attendance is below 75%; verify the records and follow up using your institution's normal process.")
    else:
        tips.append("Recorded attendance is at least 75%; continue monitoring trends across sessions.")
    if records["student_id"].nunique() < 2:
        tips.append("Add records for more students and sessions to make the dashboard more useful.")
    if "date" in records and records["date"].nunique() < 2:
        tips.append("Record multiple session dates to compare attendance over time.")
    tips.append("Treat audio/video activity as supporting indicators only, not as a direct measure of attention or learning.")
    return tips
