import streamlit as st
import openai

# Load OpenAI key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Hospitality Blog Assistant", layout="wide")

st.title("✍️ Hospitality Blog Assistant")
st.markdown("Ask me to write a blog post — I’ll ask a few quick questions to make it perfect.")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# Questions for the user
questions = [
    {
        "key": "topic",
        "question": "📍 What destination, hotel, or travel experience is the blog post about?",
        "type": "text"
    },
    {
        "key": "purpose",
        "question": "🎯 What is the main purpose of the blog post?",
        "options": ["1️⃣ Attract tourists", "2️⃣ Promote bookings", "3️⃣ Boost SEO", "4️⃣ Educate travelers"]
    },
    {
        "key": "audience",
        "question": "👥 Who is the target audience?",
        "options": ["1️⃣ Families", "2️⃣ Couples", "3️⃣ Solo travelers", "4️⃣ Digital nomads", "5️⃣ Wellness seekers"]
    },
    {
        "key": "tone",
        "question": "🎨 What tone and style do you prefer?",
        "options": ["1️⃣ Friendly", "2️⃣ Elegant", "3️⃣ Professional", "4️⃣ Storytelling", "5️⃣ Travel magazine-style"]
    },
    {
        "key": "content",
        "question": "📚 What kind of content should be included?",
        "options": ["1️⃣ Hotel overview", "2️⃣ SPA experience", "3️⃣ Local attractions", "4️⃣ Dining", "5️⃣ Tips & culture"],
        "multi": True
    },
    {
        "key": "usps",
        "question": "⭐ Any unique features or USPs to highlight?",
        "options": ["1️⃣ Natural mineral springs", "2️⃣ Sustainability", "3️⃣ Local heritage", "4️⃣ Luxury amenities"],
        "multi": True
    },
    {
        "key": "reference",
        "question": "🔗 Do you want me to reference or link to any website or platform?",
        "type": "text"
    },
    {
        "key": "season",
        "question": "🗓️ Is this blog post seasonal or time-sensitive?",
        "options": ["1️⃣ Spring", "2️⃣ Summer", "3️⃣ Autumn", "4️⃣ Winter", "5️⃣ Year-round"]
    },
    {
        "key": "structure",
        "question": "📝 Preferred word count or structure?",
        "options": ["1️⃣ 800–1000 words", "2️⃣ Storytelling", "3️⃣ Top-10 list", "4️⃣ Itinerary style"]
    },
    {
        "key": "channel",
        "question": "📣 Where will this blog post be published or promoted?",
        "options": ["1️⃣ Blog", "2️⃣ Social media", "3️⃣ Newsletter", "4️⃣ Booking site"]
    },
    {
        "key": "notes",
        "question": "🧾 Any extra notes, keywords, or brand guidelines I should follow?",
        "type": "text"
    },
    {
        "key": "language",
        "question": "🌍 What is your preferred language for this blog?",
        "options": ["1️⃣ English", "2️⃣ Turkish", "3️⃣ German", "4️⃣ French"]
    }
]

# Ask questions step-by-step
q = questions[st.session_state.step]
st.markdown(f"**{q['question']}**")

if "options" in q:
    selected = st.multiselect("Choose one or more:" if q.get("multi") else "Choose one:", q["options"])
    if st.button("Next"):
        if selected:
            st.session_state.answers[q["key"]] = selected
            st.session_state.step += 1
elif q.get("type") == "text":
    response = st.text_input("Your answer")
    if st.button("Next"):
        if response:
            st.session_state.answers[q["key"]] = response
            st.session_state.step += 1

# Generate blog post after final step
if st.session_state.step >= len(questions):
    with st.spinner("Writing your blog post..."):
        system_prompt = "You are a professional yet engaging travel and hospitality blogger. Format output with clear headings, subheadings, emojis, and add metadata like keywords, summary, and hashtags for social media."
        user_prompt = f"""Create a travel blog post with the following details:

Destination/Experience: {st.session_state.answers['topic']}
Purpose: {st.session_state.answers['purpose']}
Audience: {st.session_state.answers['audience']}
Tone/Style: {st.session_state.answers['tone']}
Content to include: {st.session_state.answers['content']}
Unique Selling Points (USPs): {st.session_state.answers['usps']}
Reference/Link: {st.session_state.answers['reference']}
Season: {st.session_state.answers['season']}
Structure: {st.session_state.answers['structure']}
Channel: {st.session_state.answers['channel']}
Extra notes: {st.session_state.answers['notes']}
Language: {st.session_state.answers['language']}

The blog should be engaging, well-formatted using markdown, and include:
- A compelling title
- A short intro paragraph
- Multiple sections with emojis and informative subheadings
- Meta data block at the end: keywords, summary, hashtags, tweet, LinkedIn snippet
- Word count around 800–1000
"""

        completion = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0125:personal:blogger:BKfX4OnW",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=3000,
            temperature=0.8
        )

        blog = completion.choices[0].message.content
        st.markdown("## 🧳 Your Blog Post")
        st.markdown(blog)

    if st.button("🔁 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
