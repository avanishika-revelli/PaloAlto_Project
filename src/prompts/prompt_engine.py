import random

def generate_prompts(entries_df):
    """
    Returns a list of prompts ordered by relevance based on recent entries.
    Uses ONLY local data (sentiment + keywords/themes) for privacy.
    """
    # --- default prompts (when no history) ---
    base = [
        "What emotion is most present right now?",
        "What went okay today, even if it was small?",
        "What’s been weighing on you lately?",
        "If today had a headline, what would it be?",
        "What do you need most right now?"
    ]

    if entries_df is None or entries_df.empty:
        random.shuffle(base)
        return base

    df = entries_df.copy()
    df = df.sort_values("created_at").tail(10)  # last 10 entries

    avg_sent = float(df["sentiment"].mean()) if "sentiment" in df.columns else 0.0

    # keywords list-of-lists -> flat counts
    counts = {}
    if "keywords" in df.columns:
        for kws in df["keywords"]:
            for k in (kws or [])[:6]:
                k = str(k).lower()
                counts[k] = counts.get(k, 0) + 1

    def has_any(*words):
        return any(w in counts for w in words)

    # --- detect context signals ---
    work_stress = has_any("work", "deadline", "meeting", "boss") and avg_sent < -0.10
    stress_general = has_any("stress", "stressed", "anxious", "anxiety", "overwhelmed") or avg_sent < -0.25
    sleep = has_any("sleep", "insomnia", "rest", "tired", "exhausted")
    relationships = has_any("family", "partner", "relationship", "friends", "argument")
    health = has_any("exercise", "walk", "gym", "run", "wellness")
    self_criticism = has_any("hate", "worthless", "failure", "ashamed", "guilty")

    # --- prompt packs (empathetic + follow-up style) ---
    prompts = []

    if work_stress:
        prompts += [
            "Work has been feeling stressful lately — what felt most demanding today?",
            "Did you find any small moments of calm during work today?",
            "What’s one boundary that could make tomorrow feel 10% lighter?",
            "What part of work is within your control right now — even a little?"
        ]

    if stress_general:
        prompts += [
            "When things felt heavy today, what helped even a little?",
            "What’s one thing you can release for tonight?",
            "If your mind is loud right now, what would it need to feel safer or calmer?",
            "What would you say to a friend who felt the way you feel today?"
        ]

    if self_criticism:
        prompts += [
            "I’m hearing a lot of self-criticism — what’s the kinder version of what you’re trying to say?",
            "What happened that led to that thought about yourself?",
            "If you looked at this with compassion, what would you notice?",
            "What’s one small thing you did today that deserves credit?"
        ]

    if relationships:
        prompts += [
            "How did your relationships affect your mood today?",
            "Was there a moment you felt connected — or disconnected? What was happening?",
            "What’s one conversation you’re avoiding, and what do you wish it could sound like?"
        ]

    if sleep:
        prompts += [
            "How did your sleep affect your mood and energy today?",
            "What helped you rest (or what got in the way)?",
            "What’s one small step you could take tonight to support better rest?"
        ]

    if health:
        prompts += [
            "What did your body need today, and did you get any of it?",
            "When you moved or got outside, did anything shift emotionally?",
            "What’s one habit that’s been supporting you lately that you want to keep?"
        ]

    # tone-based prompts
    if avg_sent > 0.20:
        prompts += [
            "What’s been working well recently, and why?",
            "How can you build on today’s momentum?",
            "What are you proud of yourself for today?"
        ]
    elif -0.10 <= avg_sent <= 0.20:
        prompts += [
            "What was the most meaningful moment today (even if it was small)?",
            "What did you notice about your energy today?",
            "What’s something you want to remember from today?"
        ]

    # Always include some universal fallback prompts
    prompts += base

    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for p in prompts:
        if p not in seen:
            ordered.append(p)
            seen.add(p)

    return ordered
