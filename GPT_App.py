import streamlit as st
from openai import OpenAI

# Load API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# System-level prompt for tone and behavior
SYSTEM_PROMPT = """
You are a professional yet casual travel and hospitality blog writer. Write structured, informative, visually engaging blog posts. Use a warm tone, section headings, emojis, real tips, and local flavor. Finish with a metadata block (summary, keywords, tags, social snippet).
"""

# Blog brief questions
questions = [
    {"key": "destination", "prompt": "📍 What destination, hotel, or travel experience is the blog post about?"},
    {"key": "purpose", "prompt": "🎯 What is the main purpose?\n1️⃣ Attract tourists\n2️⃣ Promote bookings\n3️⃣ Boost SEO\n4️⃣ Educate travelers"},
    {"key": "audience", "prompt": "👥 Who is the target audience?\n1️⃣ Families\n2️⃣ Couples\n3️⃣ Solo travelers\n4️⃣ Digital nomads\n5️⃣ Wellness seekers"},
    {"key": "tone", "prompt": "🎨 Preferred tone & style?\n1️⃣ Friendly\n2️⃣ Elegant\n3️⃣ Professional\n4️⃣ Storytelling\n5️⃣ Travel magazine-style"},
    {"key": "content", "prompt": "📋 What should be included?\n1️⃣ Hotel overview\n2️⃣ SPA experience\n3️⃣ Local attractions\n4️⃣ Dining\n5️⃣ Tips & culture"},
    {"key": "usps", "prompt": "🌟 Any unique features to highlight?\n1️⃣ Mineral springs\n2️⃣ Sustainability\n3️⃣ Local heritage\n4️⃣ Luxury amenities"},
    {"key": "links", "prompt": "🔗 Any reference or website to include?"},
    {"key": "seasonal", "prompt": "🗓️ Is the post seasonal?\n1️⃣ Spring\n2️⃣ Summer\n3️⃣ Autumn\n4️⃣ Winter\n5️⃣ Year-round"},
    {"key": "structure", "prompt": "✍️ Preferred structure?\n1️⃣ 800–1000 words\n2️⃣ Storytelling\n3️⃣ Top-10 list\n4️⃣ Itinerary style"},
    {"key": "platform", "prompt": "📢 Where will it be published?\n1️⃣ Blog\n2️⃣ Social media\n3️⃣ Newsletter\n4️⃣ Booking site"},
    {"key": "notes", "prompt": "📝 Any keywords, metadata, or social formats (e.g. Instagram, LinkedIn) to include?"},
    {"key": "language", "prompt": "🌍 Preferred language?\n1️⃣ English\n2️⃣ Turkish\n3️⃣ German\n4️⃣ French"},
]

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Page config
st.set_page_config(page_title="GPT Travel Blog Assistant", layout="centered")
st.title("🧳 GPT Travel Blog Assistant")

# Question display and input
if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Question {st.session_state.step + 1} of {len(questions)}")
    response = st.text_input(q["prompt"], key=f"input_{st.session_state.step}")

    col1, col2 = st.columns([1, 3])
    with col2:
        next_btn = st.button("➡️ Next")

    if response and next_btn:
        st.session_state.answers[q["key"]] = response
        st.session_state.step += 1
        st.rerun()  # ✅ Updated line

elif st.session_state.step == len(questions):
    st.success("✅ All questions answered. Generating your blog post...")
    with st.spinner("Crafting your tailored blog post..."):

        # Build prompt string
        user_prompt = "Please write a travel blog post based on the following brief:\n\n"
        for q in questions:
            answer = st.session_state.answers.get(q["key"], "N/A")
            user_prompt += f"- {q['prompt'].split('?')[0]}: {answer}\n"

        # OpenAI call
        completion = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:personal:blogger:BKfX4OnW",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )

        blog = completion.choices[0].message.content
        st.markdown("---")
        st.subheader("📄 Your Blog Post")
        st.markdown(blog)
        st.session_state.step += 1

else:
    st.info("🔁 Refresh the page to start over or generate a new post.")
