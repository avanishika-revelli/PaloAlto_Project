from datetime import datetime, timedelta
from src.config import WEEK_DAYS

def weekly_reflection(entries):
    if entries.empty:
        return "No entries yet. A short check-in is enough to begin."

    cutoff = datetime.now() - timedelta(days=WEEK_DAYS)
    week = entries[entries["created_at"] >= cutoff]

    if week.empty:
        return "No entries this week. That’s okay—consistency can restart anytime."

    avg = week["sentiment"].mean()

    if avg < -0.2:
        mood = "heavier than usual"
    elif avg > 0.2:
        mood = "more positive than usual"
    else:
        mood = "steady"

    return (
        f"This week felt **{mood}** overall.\n\n"
        "Notice what helped on better days, even in small ways. "
        "What’s one support you could repeat next week?"
    )
