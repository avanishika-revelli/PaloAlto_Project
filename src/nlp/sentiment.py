import re

POSITIVE = {
    # Core happiness / positivity
    "happy", "happiness", "joy", "joyful", "glad", "pleased", "content", "satisfied",

    # Calm / peace
    "calm", "peaceful", "relaxed", "at ease", "grounded", "centered", "balanced",

    # Energy / motivation
    "energized", "motivated", "focused", "productive", "driven", "inspired",

    # Confidence / self-worth
    "confident", "proud", "capable", "strong", "accomplished", "competent",

    # Gratitude / appreciation
    "grateful", "thankful", "appreciative", "blessed",

    # Relief / release
    "relieved", "lighter", "unburdened", "free",

    # Connection / love
    "loved", "supported", "connected", "cared", "appreciated",

    # Hope / optimism
    "hopeful", "optimistic", "positive", "encouraged",

    # Satisfaction from action
    "progress", "improving", "better", "success", "win", "achievement"
}

NEGATIVE = {
    # Stress / anxiety
    "stressed", "stress", "anxious", "anxiety", "worried", "nervous", "uneasy",
    "overwhelmed", "pressure", "tense", "on edge",

    # Sadness / low mood
    "sad", "unhappy", "down", "low", "blue", "empty", "tearful", "heartbroken",
    "grief", "grieving",

    # Exhaustion / burnout
    "tired", "exhausted", "drained", "burnt out", "burnout", "fatigued", "worn out",

    # Anger / frustration
    "angry", "anger", "frustrated", "irritated", "annoyed", "resentful", "upset",

    # Hopelessness / helplessness
    "hopeless", "helpless", "stuck", "trapped", "defeated", "discouraged",

    # Guilt / shame
    "guilty", "ashamed", "shame", "regret", "regretful", "embarrassed",

    # Loneliness / disconnection
    "lonely", "alone", "isolated", "disconnected", "ignored", "unseen",

    # Fear / insecurity
    "afraid", "scared", "fearful", "insecure", "unsafe", "threatened",

    # Loss of control / uncertainty
    "confused", "uncertain", "lost", "directionless", "doubtful",

    # Pain / heaviness
    "hurts", "painful", "heavy", "weighed down", "burdened",

    # Failure / self-criticism
    "failure", "failing", "useless", "worthless", "inadequate",

    "hate", "hating", "self-hate"
}


_WORD = re.compile(r"[a-zA-Z']+")

def sentiment_score(text: str) -> float:
    """
    Simple local sentiment score in [-1, 1].
    Strips punctuation so 'stressed,' matches 'stressed'.
    """
    tokens = [t.lower() for t in _WORD.findall(text or "")]
    pos = sum(t in POSITIVE for t in tokens)
    neg = sum(t in NEGATIVE for t in tokens)

    if pos + neg == 0:
        return 0.0
    return (pos - neg) / (pos + neg)
