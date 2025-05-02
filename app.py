import streamlit as st
from openai import OpenAI

# === CONFIGURATION ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal:blogger:BKfX4OnW"

# === DEFINE QUESTION FLOW WITH MULTIPLE CHOICE OPTIONS ===
QUESTIONS = [
    {
        "key": "topic",
        "text": "🌍 What destination, hotel, or travel experience is the blog post about?",
        "choices": None
    },
    {
        "key": "purpose",
        "text": "🎯 What is the main purpose of the blog post?",
        "choices": ["1️⃣ Attract tourists", "2️⃣ Promote bookings", "3️⃣ Boost SEO", "4️⃣ Educate travelers"]
    },
    {
        "key": "audience",
        "text": "👥 Who is the target audience?",
        "choices": ["1️⃣ Families", "2️⃣ Couples", "3️⃣ Solo travelers", "4️⃣ Digital nomads", "5️⃣ Wellness seekers"]
    },
    {
        "key": "tone",
        "text": "🗣️ What tone and style do you prefer?",
        "choices": ["1️⃣ Friendly", "2️⃣ Elegant", "3️⃣ Professional", "4️⃣ Storytelling", "5️⃣ Travel magazine-style"]
    },
    {
        "key": "content",
        "text": "🧳 What kind of content should be included?",
        "choices": ["1️⃣ Hotel overview", "2️⃣ SPA experience", "3️⃣ Local attractions", "4️⃣ Dining", "5️⃣ Tips & culture"]
    },
    {
        "key": "features",
        "text": "✨ Any unique features or USPs to highlight?",
        "choices": ["1️⃣ Natural mineral springs", "2️⃣ Sustainability", "3️⃣ Local heritage", "4️⃣ Luxury amenities"]
    },
    {
        "key": "links",
        "text": "🔗 Do you want me to reference or link to any website or platform?",
        "choices": None
    },
    {
        "key": "season",
        "text": "📅 Is this blog post seasonal or time-sensitive?",
        "choices": ["1️⃣ Spring", "2️⃣ Summer", "3️⃣ Autumn", "4️⃣ Winter", "5️⃣ Year-round"]
    },
    {
        "key": "structure",
        "text": "📝 Preferred word count or structure?",
        "choices": ["1️⃣ 800–1000 words", "2️⃣ Storytelling", "3️⃣ Top-10 list", "4️⃣ Itinerary style"]
    },
    {
        "key": "channel",
        "text": "📣 Where will this blog post be published or promoted?",
        "choices": ["1️⃣ Blog", "2️⃣ Social media", "3️⃣ Newsletter", "4️⃣ Booking site"]
    },
    {
        "key": "extras",
        "text": "💡 Any extra notes, keywords, or brand guidelines I should follow?",
        "choices": None
    },
    {
        "key": "language",
        "text": "🌐 What is your preferred language for this blog?",
        "choices": ["1️⃣ English", "2️⃣ Turkish", "3️⃣ German", "4️⃣ French"]
    }
]

# === BLOG STYLE SAMPLE POST ===
EXAMPLE_POST = """
🧭 **Title:** Discovering the Soul of Tbilisi: A Hidden Gem in the Caucasus

✈️ **Intro:** Tbilisi, Georgia's quirky and colorful capital, blends Eastern charm with bohemian energy. Nestled between hills and the Mtkvari River, this city enchants travelers...

🏛️ **1. Cultural Echoes**
🍷 **2. Culinary Magic**
🧵 **3. Hidden Treasures**
🎒 **Conclusion**
🔎 **Meta Summary:** keywords, extract, tweet, image prompt
"""

# === INSTRUCTIONS ===
INSTRUCTIONS = (
    "You are a travel blog writer creating structured, engaging, beautifully formatted content.\\n"
    "Use markdown headers, emojis, subheadings, and clear sections:\\n"
    "- Title (with emoji)\\n"
    "- Intro paragraph\\n"
    "- 3 body sections with emoji headings\\n"
    "- Conclusion\\n"
    "- Metadata block: keywords, extract, tweet, image prompt\\n"
    "⚠️ Important: Only include the destination specified. Do not reference unrelated cities or countries.\\n"
    "✅ Validate the destination in the title matches the brief.\\n"
    "Output should be around 700–750 words. Match the clarity and format of the example provided."
)

# === SESSION STATE ===
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.show_blog = False

# === STREAMLIT UI ===
st.title("📝 Hospitality Blog Generator")
st.markdown("Let’s create a stunning travel blog post. I’ll ask a few quick questions:")

# === DISPLAY QUESTIONS ===
if st.session_state.step < len(QUESTIONS):
    current = QUESTIONS[st.session_state.step]
    st.subheader(current["text"])

    if current["choices"]:
        for choice in current["choices"]:
            st.markdown(f"- {choice}")
        response = st.text_input("Select number(s) or type your own answer:")
    else:
        response = st.text_input("Type your answer:")

    if response:
        st.session_state.answers[current["key"]] = response.strip()
        st.session_state.step += 1
        st.rerun()

# === GENERATE BLOG ===
elif not st.session_state.show_blog:
    if st.button("🪄 Generate Blog Post"):
        summary = "\\n".join([f"{k.capitalize()}: {v}" for k, v in st.session_state.answers.items()])
        prompt = f"{INSTRUCTIONS}\\n\\nHere is a sample blog:\\n{EXAMPLE_POST}\\n\\nNow write a new blog post using the following brief:\\n{summary}"

        with st.spinner("Creating your location-accurate blog..."):
            response = client.chat.completions.create(
                model=FINE_TUNED_MODEL,
                max_tokens=800,
                messages=[
                    {"role": "system", "content": "You are a precise, engaging travel blogger."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.session_state.blog_output = response.choices[0].message.content
            st.session_state.show_blog = True

# === DISPLAY BLOG POST ===
if st.session_state.show_blog:
    st.subheader("📄 Your Blog Post")
    st.markdown(st.session_state.blog_output)

    if st.button("🔁 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.show_blog = False
        st.rerun()
