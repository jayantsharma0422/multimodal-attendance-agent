import pandas as pd
from modules.analytics import summarize_attendance, make_recommendations

def test_empty_summary():
    result = summarize_attendance(pd.DataFrame(columns=["status", "student_id", "date"]))
    assert result["total"] == 0
    assert result["present"] == 0

def test_summary():
    df = pd.DataFrame({
        "status": ["Present", "Absent", "Present"],
        "student_id": ["1", "2", "3"],
        "date": ["2026-01-01", "2026-01-01", "2026-01-02"]
    })
    result = summarize_attendance(df)
    assert result["total"] == 3
    assert result["present"] == 2
    assert result["rate"] == 66.7
