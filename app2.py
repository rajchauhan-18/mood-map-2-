import streamlit as st
import time
import pandas as pd

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Mood Map & Resource Bot", layout="centered")

st.title("🧠 Mood Map & Resource Bot")
st.write("A simple mental well-being support app")

# ===============================
# NLP FUNCTION (RULE-BASED)
# ===============================
def detect_mood_from_text(text):
    text = text.lower()

    if any(word in text for word in ["sad", "lonely", "tired", "cry", "hopeless"]):
        return "Sad 😔"
    elif any(word in text for word in ["angry", "mad", "frustrated", "irritated"]):
        return "Angry 😠"
    elif any(word in text for word in ["anxious", "worried", "nervous", "panic"]):
        return "Anxious 😰"
    elif any(word in text for word in ["happy", "excited", "good", "great"]):
        return "Happy 😊"
    else:
        return None

# ===============================
# RESOURCE DATABASE
# ===============================
MOOD_RESOURCES = {
    "Happy 😊": {
        "message": "That's great! Keep nurturing your positive energy 🌟",
        "resources": [
            "Share your happiness with someone",
            "Practice gratitude",
            "Enjoy your favorite activity"
        ]
    },
    "Sad 😔": {
        "message": "I'm sorry you're feeling this way 💙",
        "resources": [
            "Talk to someone you trust",
            "Write your thoughts in a journal",
            "Take rest and be kind to yourself"
        ]
    },
    "Angry 😠": {
        "message": "Anger is natural. Let's calm things down 😌",
        "resources": [
            "Deep breathing",
            "Step away from the situation",
            "Physical movement like walking"
        ]
    },
    "Anxious 😰": {
        "message": "You're not alone. Let's ground you 🧘",
        "resources": [
            "4-7-8 breathing technique",
            "Focus on present surroundings",
            "Limit overthinking triggers"
        ]
    }
}

# ===============================
# USER LOCATION
# ===============================
country = st.selectbox("🌍 Select your country", ["India", "USA", "Other"])

# ===============================
# TEXT INPUT (NLP)
# ===============================
st.subheader("📝 Describe how you are feeling")
user_text = st.text_area("You may type how you feel (optional)")

# ===============================
# MANUAL MOOD SELECTION
# ===============================
mood = st.radio(
    "Or select your mood:",
    list(MOOD_RESOURCES.keys())
)

# ===============================
# INTENSITY SLIDER
# ===============================
intensity = st.slider("How intense is this feeling?", 1, 10)

# ===============================
# REASON CAPTURE
# ===============================
reason = st.text_area("What do you think caused this feeling? (optional)")

# ===============================
# SESSION STATE
# ===============================
if "history" not in st.session_state:
    st.session_state.history = []

# ===============================
# NLP OVERRIDE
# ===============================
if user_text.strip():
    detected = detect_mood_from_text(user_text)
    if detected:
        mood = detected
        st.info(f"🧠 Detected mood from text: {mood}")

# ===============================
# GET SUPPORT
# ===============================
if st.button("Get Support"):
    data = MOOD_RESOURCES[mood]

    st.subheader("💬 Support Message")
    st.success(data["message"])

    st.subheader("🛠️ Helpful Resources")
    for r in data["resources"]:
        st.write("•", r)

    # Personalized coping plan
    st.subheader("🧭 Your Coping Plan")
    if mood == "Sad 😔":
        st.write("1. Take rest\n2. Express emotions\n3. Reach out for support")
    elif mood == "Anxious 😰":
        st.write("1. Slow breathing\n2. Ground yourself\n3. Avoid overstimulation")
    elif mood == "Angry 😠":
        st.write("1. Pause\n2. Walk away\n3. Reflect calmly")
    else:
        st.write("Continue positive habits and self-care")

    # Emergency detection
    if mood in ["Sad 😔", "Anxious 😰"] and intensity >= 8:
        st.error("🚨 High emotional distress detected")

        if country == "India":
            st.write("📞 Emergency: 112")
            st.write("📞 Kiran Helpline: 1800-599-0019")
        elif country == "USA":
            st.write("📞 Suicide & Crisis Lifeline: 988")
        else:
            st.write("📞 Contact local emergency services")

    # Gentle reminder
    if mood == "Sad 😔":
        st.info("💙 Reminder: Feelings change. You are not alone.")

    # Save history
    st.session_state.history.append((mood, intensity))

# ===============================
# MOOD HISTORY & TRENDS
# ===============================
if st.session_state.history:
    st.subheader("📊 Mood History")
    for i, (m, inten) in enumerate(st.session_state.history, start=1):
        st.write(f"{i}. {m} | Intensity: {inten}")

    sad_count = sum(1 for m, _ in st.session_state.history if m == "Sad 😔")
    if sad_count >= 3:
        st.warning("You’ve been feeling sad frequently. Consider reaching out for help.")

    # Download report
    df = pd.DataFrame(st.session_state.history, columns=["Mood", "Intensity"])
    st.download_button(
        "⬇️ Download Mood Report",
        df.to_csv(index=False),
        "mood_report.csv"
    )

# ===============================
# SELF-HELP ACTIVITY
# ===============================
st.subheader("🧘 Self-Help Activity")
activity = st.selectbox(
    "Choose an activity",
    ["Breathing", "Gratitude", "Grounding"]
)

if activity == "Breathing" and st.button("Start Breathing"):
    for _ in range(3):
        st.write("Inhale 🌬️")
        time.sleep(2)
        st.write("Exhale 😌")
        time.sleep(2)

elif activity == "Gratitude":
    st.text_input("Write one thing you're grateful for today:")

elif activity == "Grounding":
    st.write("Name 3 things you can see around you")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("Educational project only. Not a replacement for professional mental health care.")
