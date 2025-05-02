import streamlit as st
from openai import OpenAI

# === CONFIG ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
MODEL = "ft:gpt-3.5-turbo-0125:personal:blogger:BKfX4OnW"

# === QUESTIONS ===
QUESTIONS = [
    {"key": "topic", "text": "🌍 What destination, hotel, or travel experience is the blog post about?", "choices": None},
    {"key": "purpose", "text": "🎯 What is the main purpose of the blog post?", "choices": ["1️⃣ Attract tourists", "2️⃣ Promote bookings", "3️⃣ Boost SEO", "4️⃣ Educate travelers"]},
    {"key": "audience", "text": "👥 Who is the target audience?", "choices": ["1️⃣ Families", "2️⃣ Couples", "3️⃣ Solo travelers", "4️⃣ Digital nomads", "5️⃣ Wellness seekers"]},
    {"key": "tone", "text": "🗣️ What tone and style do you prefer?", "choices": ["1️⃣ Friendly", "2️⃣ Elegant", "3️⃣ Professional", "4️⃣ Storytelling", "5️⃣ Travel magazine-style"]},
    {"key": "content", "text": "🧳 What kind of content should be included?", "choices": ["1️⃣ Hotel overview", "2️⃣ SPA experience", "3️⃣ Local attractions", "4️⃣ Dining", "5️⃣ Tips & culture"]},
    {"key": "features", "text": "✨ Any unique features or USPs to highlight?", "choices": ["1️⃣ Natural mineral springs", "2️⃣ Sustainability", "3️⃣ Local heritage", "4️⃣ Luxury amenities"]},
    {"key": "links", "text": "🔗 Do you want me to reference or link to any website or platform?", "choices": None},
    {"key": "season", "text": "📅 Is this blog post seasonal or time-sensitive?", "choices": ["1️⃣ Spring", "2️⃣ Summer", "3️⃣ Autumn", "4️⃣ Winter", "5️⃣ Year-round"]},
    {"key": "structure", "text": "📝 Preferred word count or structure?", "choices": ["1️⃣ 800–1000 words", "2️⃣ Storytelling", "3️⃣ Top-10 list", "4️⃣ Itinerary style"]},
    {"key": "channel", "text": "📣 Where will this blog post be published or promoted?", "choices": ["1️⃣ Blog", "2️⃣ Social media", "3️⃣ Newsletter", "4️⃣ Booking site"]},
    {"key": "extras", "text": "💡 Any extra notes, keywords, or brand guidelines I should follow?", "choices": None},
    {"key": "language", "text": "🌐 What is your preferred language for this blog?", "choices": ["1️⃣ English", "2️⃣ Turkish", "3️⃣ German", "4️⃣ French"]}
]

# === INIT STATE ===
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.blog = None

# === APP TITLE ===
st.title("✍️ Hospitality Blog Creator")
st.markdown("Let’s build your perfect blog post. Answer the following:")

# === QUESTION FLOW ===
if st.session_state.step < len(QUESTIONS):
    q = QUESTIONS[st.session_state.step]
    with st.form(f"form_{q['key']}"):
        st.subheader(q["text"])
        if q["choices"]:
            for choice in q["choices"]:
                st.markdown(f"- {choice}")
            response = st.text_input("Select number(s) or type your answer:")
        else:
            response = st.text_input("Type your answer:")
        submitted = st.form_submit_button("Next")
        if submitted and response.strip():
            st.session_state.answers[q["key"]] = response.strip()
            st.session_state.step += 1
            st.rerun()

# === BLOG GENERATION ===
elif not st.session_state.blog:
    if st.button("🪄 Generate Blog Post"):
        summary = "\n".join([f"{k.replace('_',' ').capitalize()}: {v}" for k, v in st.session_state.answers.items()])

        full_prompt = f"""
You are a highly experienced travel blogger. Generate a professional, polished blog post based on the following brief:

🧾 BRIEF:
{summary}

✍️ FORMAT:
- Start with a bold title and emoji (e.g., 🧭 Title: ...)
- Include an ✈️ **intro** (1 paragraph)
- Then write 3–4 clear sections with markdown headings and emojis (## 🏛️ History, ## 🍽️ Dining, etc.)
- Finish with a **🎒 Conclusion**
- After the main post, add a **🔎 Meta Summary** section that includes:
    - **Keywords:**
    - **Extract:**
    - **Tweet:**
    - **Instagram Tags:**
    - **Image Prompt:**

💡 GUIDELINES:
- Follow a storytelling tone with vivid, engaging details
- Respect structure — don’t skip intro, sections, or meta summary
- Mention relevant places, culture, tips, and local flavor
- Write in the language selected (default: English)
- Do NOT invent random names unless cultural or artistic

"""

        with st.spinner("✍️ Writing your blog..."):
            result = client.chat.completions.create(
                model=MODEL,
                max_tokens=3000,
                temperature=0.8,
                messages=[
                    {"role": "system", "content": "You are a professional travel blogger who writes structured, engaging blogs with visual formatting."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            st.session_state.blog = result.choices[0].message.content

# === BLOG OUTPUT ===
if st.session_state.blog:
    st.subheader("📄 Your Blog Post")
    st.markdown(st.session_state.blog)

    if st.button("🔁 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.blog = None
        st.rerun()
