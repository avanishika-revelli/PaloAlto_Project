 **Echo (Private AI Journaling Companion)**

## **1\) Overview**

### **Problem**

Many people want the mental wellness benefits of journaling but struggle with:

* “blank page” anxiety (don’t know what to write)  
* inconsistency (hard to build a daily habit)  
* difficulty reflecting (entries become a log, not growth)  
* lack of insights (patterns are hard to spot manually)

### **Solution**

**Echo** is a private journaling companion that:

* guides users with **empathetic, context-aware prompts**  
* tracks **mood \+ sentiment** trends over time  
* extracts and displays **themes/keywords**  
* generates **weekly reflection summaries** that connect behavioral patterns to emotional outcomes

Echo is designed to be:

* **private** (local-first storage; no external API calls required)  
* **non-judgmental** (gentle language, neutral UX)  
* **fast and lightweight** (simple NLP heuristics, runs on commodity laptops)


## **2\) Key Product Features (Mapped to Requirements)**

### **A) Dynamic, Empathetic Prompts** 

* The prompt engine adapts prompts based on recent entries:  
  * detected themes (e.g., work, family, stress)  
  * sentiment (positive/neutral/challenging)  
  * journaling streak/engagement  
* Prompts are phrased as a **supportive conversation**, not generic templates.

**Examples**

* If themes include work \+ stress: “Where did you find even a small moment of calm today?”

* If positive trend: “What helped today go well and how can you repeat it tomorrow?”

### **B) Private Sentiment & Theme Analysis** 

Echo performs analysis locally:

* **Mood selection** (1–5 scale) captured at write-time  
* **Sentiment scoring** on journal text  
* **Theme extraction** via keyword/topic heuristics (fast and private)

Outputs:

* Sentiment distribution: Positive / Neutral / Challenging  
* Theme chips: “Work”, “Family”, “Wellness”, “Stress”, etc.  
* Timeline charts: “Mood over time”, “Sentiment over time”

### **C) Insightful Reflection Summaries** 

Weekly reflections identify:

* recurring themes  
* what correlates with higher mood days (patterns)  
* suggested gentle next steps

Examples of generated insights:

* “You felt most energized on days you mentioned a morning routine or going outside.”  
* “Work appeared frequently alongside stress—consider adding a short decompression ritual.”


### **D) Habit & Engagement Nudges** 

Echo uses light nudges:

* “No entry yet today two sentences count.”  
* streak counters  
* small progress reinforcement (“You checked in today”)

Design principle: motivate without pressure.

## **3\) UX / UI Design**

### **Navigation structure**

* **Write**: primary journaling experience (prompt \+ mood \+ text)  
* **Insights**: dashboards (sentiment trends, mood, themes)  
* **Reflections**: weekly summaries and pattern highlights  
* **About**: what Echo is \+ privacy statement


### **Core Write Page Interaction**

1. User sees a **Today’s Prompt** (refreshable/dismissible)  
2. User selects **How are you feeling?** (mood scale)  
3. User writes journal entry (text area)  
4. On save:  
   * entry is stored locally  
   * sentiment \+ keywords \+ theme assigned  
   * UI clears input for next entry

### **Design choices**

* Minimal friction: mood buttons \+ large text area  
* Prompts reduce blank-page anxiety  
* Clear privacy reassurance (“stored locally”)


## **4\) System Architecture**

Echo is structured as a modular Streamlit app:

### **Layers**

1. **UI Layer**  
   * page rendering (write, insights, reflections, about)  
   * layout and styling  
   * state handling (selected entry, prompt refresh, etc.)  
2. **Data Layer**  
   * SQLite persistence  
   * CRUD functions (insert, fetch, delete, summaries)  
   * schema management and migrations (if needed)

3. **NLP/Analysis Layer** (src/analysis/ or inside db/prompts modules)  
   * sentiment scoring  
   * keyword extraction  
   * theme classification  
   * aggregation for dashboards  
4. **Prompt Engine**  
   * prompt templates  
   * context-aware selection based on recent entries and stats

### **Why this architecture?**

* Clear separation of concerns  
* Easy to extend (swap NLP model later, change DB later)  
* Easier debugging and testability


## **5\) Tech Stack**

### **Frontend/UI**

* **Streamlit**  
  * fast prototyping  
  * easy deployment (Streamlit Cloud)  
  * responsive UI without building a full web frontend

### **Backend / Storage**

* **SQLite**  
  * local-first persistence  
  * lightweight, no server needed  
  * simple for hackathon environment

### **Data processing**

* **Pandas**  
  * aggregations for dashboards (daily averages, distribution, streaks)

### **Visualization**

* **Matplotlib** (or Streamlit native charts)  
  * mood timeline, sentiment trend, distribution bars

### **NLP**

* **Heuristic sentiment scoring**  
  * keyword lexicons  
  * simple scoring (fast and explainable)  
* **Theme extraction**  
  * keyword/topic mapping categories (work/family/health/etc.)

**Why heuristic NLP?**

* No external APIs → privacy-friendly  
* Low compute cost  
* Works offline  
* Explainable and controllable


## **6\) Data Model & Database Schema (Conceptual)**

### **entries table (core)**

Fields typically include:

* id (int, primary key)  
* created\_at (datetime)  
* text (string)  
* mood (int 1–5)  
* sentiment (float \-1 to \+1)  
* keywords (list or JSON string)  
* theme (string label)

### **Derived / computed metrics (not stored)**

Computed at runtime:

* daily average mood  
* daily average sentiment  
* sentiment distribution  
* theme counts  
* streak (consecutive days with entries)

**Why store both mood and sentiment?**

* Mood is explicit user intent  
* Sentiment is inferred from language  
* Comparing both can produce insights (“you rated neutral but language was negative”)

## **7\) Sentiment Analysis Design**

### **Approach**

* Normalize entry text (lowercase, tokenize)  
* Count matches against:  
  * positive lexicon  
  * negative lexicon  
* Score formula example:  
  * (pos\_count \- neg\_count) / (pos\_count \+ neg\_count \+ 1\)  
* Clamp to \[-1, \+1\]

### **Classification**

* Positive if score \> threshold (e.g., 0.15)  
* Challenging if score \< \-0.15  
* Neutral otherwise

**Why this design?**

* Transparent: easy to debug  
* Private: no API calls  
* Good enough for meaningful trends in a prototype

## **8\) Theme Extraction Design**

### **Approach**

A rule-based mapping from keywords to themes.  
Example:

* Work: “work, boss, deadline, meeting, office…”  
* Family: “mom, dad, sister, relationship…”  
* Wellness: “sleep, exercise, walk, meditate…”  
* Stress: “anxious, overwhelmed, pressure…”

Each entry can have:

* one “primary theme” (top-scoring category)  
* optional keyword list for UI display

**Why themes matter**

* Makes insights and prompt selection “feel personal”  
* Enables reflection summaries (“Work appears 3x this week”)


## **9\) Prompt Engine Design**

### **Inputs**

* Recent entries (last N)  
* Detected recent themes  
* Recent sentiment trend  
* Entry frequency/streak

### **Logic**

* If no recent entries → beginner-friendly prompts  
* If theme repeats → deeper follow-up prompts  
* If negative/challenging streak → grounding/self-compassion prompts  
* If positive streak → reinforcement \+ gratitude prompts

### **Output**

* A small list of candidate prompts  
* UI shows 1 prompt with refresh/dismiss

## **10\) Reflection Summaries (Weekly)**

### **What it does**

A weekly summary includes:

* most frequent themes  
* best mood day correlations (based on keywords/themes)  
* gentle growth suggestion

### **Algorithm (prototype)**

* group entries by day  
* compute daily avg mood \+ daily avg sentiment  
* find top themes  
* detect co-occurrences:  
  * theme X present on days with mood \>= 4  
* generate templated summary text

## **11\) Privacy & Trust Design**

### **Privacy posture**

* Local database (SQLite) by default  
* No external API calls required (no OpenAI calls)  
* No user tracking or analytics  
* Clear UI copy:  
  * “Stored locally”  
  * “Analysis performed privately”

### **When deployed on Streamlit Cloud**

**Important note:** In hosted mode, the app runs on Streamlit infrastructure.  
 For hackathon demos:

* Explain: “Demo is hosted for convenience. Local mode is supported by running locally.”  
* Future: encryption \+ per-user auth if needed.

### **Trust-building UX**

* Non-judgmental labels (“Challenging” vs “Negative”)  
* Gentle nudges (no guilt)  
* Easy “Clear all entries” option (user control)

## **12\) Error Handling & Code Quality Practices**

### **Patterns used**

* Defensive checks for empty dataframes  
* Try/except around DB writes  
* Validations: minimum text length  
* Safe defaults when columns missing (avoids KeyError)  
* Clear “no data yet” states in UI

### **Maintainability**

* Modular folder structure  
* functions small and single-purpose  
* session\_state used carefully for navigation and selection

## **13\) Known Limitations (Prototype)**

* Heuristic sentiment can miss nuance/sarcasm  
* Theme extraction is keyword-based (not semantic)  
* No user accounts (single-user local use)  
* Hosted deployment cannot guarantee “on-device” privacy  
* No encryption-at-rest (future improvement)

## **14\) Future Enhancements**

### **NLP / AI Improvements**

* Replace heuristic sentiment with:  
  * VADER (still local)  
  * small local transformer model (optional)  
* Better theme extraction:  
  * embeddings \+ clustering (local)  
  * topic modeling (LDA)

### **Privacy & Security**

* Encrypt journal DB locally (password-based)  
* Local-only mode toggle  
* Export/import encrypted journal backups  
* Optional biometric integration (future native app)

### **Engagement Improvements**

* Smart reminders (streak-based)  
* “2-minute journal mode” (ultra quick check-in)  
* Gentle CBT-style reframes (optional)

### **Insight Improvements**

* Correlation engine (e.g., “exercise correlates with mood \+1.2”)  
* Time-of-day writing impact  
* “Triggers and coping” detection patterns

### **Product Improvements**

* Search entries  
* Speech to text  
* Tag editing  
* Attachments/photos  
* Multi-device sync (opt-in, end-to-end encrypted)


## **15\) Deployment Plan**

### **For hackathon demo**

* Deploy via **Streamlit Community Cloud**  
* Provide public URL \+ demo video

### **For “real” product**

* Desktop app (local-only)  
* Mobile native app (on-device inference)  
* Optional secure cloud sync

