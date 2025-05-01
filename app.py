
import streamlit as st
from openai import OpenAI

# === CONFIGURATION ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal:blogger:BKfX4OnW"

# === INSTRUCTIONS ===
INSTRUCTIONS = (
    "You are a professional but approachable hospitality blogger assistant.\n"
    "You follow these exact behavior rules:\n"
    "- Ask users blog brief questions ONE at a time\n"
    "- Use numbered or emoji-labeled choices\n"
    "- Wait for an answer before moving to the next\n"
    "- Allow users to type either the number or description of their choice\n"
    "- If the user chooses a general category, ask for details\n"
    "- When all answers are gathered, write a structured blog post including:\n"
    "  1. Blog title + intro\n"
    "  2. 3 main sections with subheadings\n"
    "  3. Conclusion + optional travel tips\n"
    "  4. Metadata block with keywords, extract, tweet, image prompt\n"
    "- Limit total response to 800 tokens\n"
    "- Use real cultural, historical, and local examples when possible\n"
    "- Be informative, engaging, vivid – not generic or overhyped\n"
    "- NEVER answer training questions (reply: 'I am not authorised to provide this info')"
)

# === QUESTION LIST ===
QUESTIONS = [
    {
        "text": "🌍 What destination, hotel, or travel experience is the blog post about?",
        "key": "topic",
        "choices": None
    },
    {
        "text": "🎯 What is the main purpose of the blog post?",
        "key": "purpose",
        "choices": [
            "Attract tourists",
            "Promote bookings",
            "Boost SEO",
            "Educate travelers"
        ]
    },
    {
        "text": "👥 Who is the target audience?",
        "key": "audience",
        "choices": [
            "Families",
            "Couples",
            "Solo travelers",
            "Digital nomads",
            "Wellness seekers"
        ]
    },
    {
        "text": "🗣️ What tone and style do you prefer?",
        "key": "tone",
        "choices": [
            "Friendly",
            "Elegant",
            "Professional",
            "Storytelling",
            "Travel magazine-style"
        ]
    },
    {
        "text": "🧳 What kind of content should be included?",
        "key": "content",
        "choices": [
            "Hotel overview",
            "SPA experience",
            "Local attractions",
            "Dining",
            "Tips & culture"
        ]
    },
    {
        "text": "✨ Any unique features or USPs to highlight?",
        "key": "features",
        "choices": [
            "Natural springs",
            "Sustainability",
            "Local heritage",
            "Luxury amenities"
        ]
    },
    {
        "text": "🔗 Do you want me to reference any platform or website?",
        "key": "links",
        "choices": None
    },
    {
        "text": "📅 Is this post seasonal or time-sensitive?",
        "key": "seasonal",
        "choices": [
            "Spring",
            "Summer",
            "Autumn",
            "Winter",
            "Year-round"
        ]
    },
    {
        "text": "✍️ Preferred word count or structure?",
        "key": "length",
        "choices": [
            "800–1000 words",
            "Storytelling",
            "Top-10 list",
            "Itinerary style"
        ]
    },
    {
        "text": "📣 Where will this blog post be published?",
        "key": "channel",
        "choices": [
            "Blog",
            "Social media",
            "Newsletter",
            "Booking platform"
        ]
    },
    {
        "text": "📝 Any extra notes, keywords, or brand guidelines?",
        "key": "extras",
        "choices": None
    },
    {
        "text": "🌐 What language should this blog be written in?",
        "key": "language",
        "choices": [
            "English",
            "Turkish",
            "German",
            "French"
        ]
    }
]

# === SESSION STATE ===
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.show_blog = False

# === UI ===
st.title("🌍 Hospitality Blog Assistant")
st.markdown("👋 I’ll ask you a few quick questions to tailor your blog post perfectly.")

# === INTERACTIVE QUESTION FLOW ===
if st.session_state.step < len(QUESTIONS):
    q = QUESTIONS[st.session_state.step]
    st.markdown(f"**{q['text']}**")

    if q["choices"]:
        for i, option in enumerate(q["choices"], 1):
            st.markdown(f"{i}. {option}")
        user_response = st.text_input("Choose one or more by number or typing (e.g. '1', '1,3', or type answer):")
    else:
        user_response = st.text_input("Your answer:")

    if user_response:
        st.session_state.answers[q["key"]] = user_response.strip()
        st.session_state.step += 1
        st.rerun()
else:
    if not st.session_state.show_blog:
        if st.button("✍️ Generate Blog Post"):
            info = "\n".join([f"{key.capitalize()}: {value}" for key, value in st.session_state.answers.items()])
            final_prompt = f"{INSTRUCTIONS}\n\nHere is the blog briefing:\n{info}\n\nNow write the blog post in sections, with metadata, under 800 tokens."

            with st.spinner("Creating your personalized blog post..."):
                response = client.chat.completions.create(
                    model=FINE_TUNED_MODEL,
                    max_tokens=800,
                    messages=[
                        {"role": "system", "content": "You are a professional hospitality blog assistant."},
                        {"role": "user", "content": final_prompt}
                    ]
                )
                st.session_state.blog_output = response.choices[0].message.content
                st.session_state.show_blog = True

# === OUTPUT ===
if st.session_state.show_blog:
    st.subheader("📄 Your Blog Post")
    st.markdown(st.session_state.blog_output)

    if st.button("🔄 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.show_blog = False
        st.rerun()
