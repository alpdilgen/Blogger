import streamlit as st
from openai import OpenAI

# === CONFIGURATION ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal:blogger:BKfX4OnW"

# === SESSION STATE SETUP ===
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.show_blog = False

# === EXAMPLE BLOG TO IMITATE ===
EXAMPLE_POST = """
🧭 **Title:** Discovering the Soul of Tbilisi: A Hidden Gem in the Caucasus

✈️ **Intro:** Tbilisi, Georgia's quirky and colorful capital, blends Eastern charm with bohemian energy. Nestled between hills and the Mtkvari River, this city enchants travelers with its cobbled lanes, sulfur baths, and unforgettable food.

🏛️ **1. Cultural Echoes & Timeless Landmarks**
From the ancient Narikala Fortress to the winding streets of the Old Town, Tbilisi tells stories of Silk Road traders and revolutionaries. Don't miss the Holy Trinity Cathedral or the Soviet mosaics still decorating metro stations.

🍷 **2. Culinary Magic in Every Corner**
Feast on khinkali (dumplings) and khachapuri at retro-modern eateries. Try wine-tasting in cellars carved into cliffs – Georgia’s wine heritage spans 8,000 years!

🧵 **3. Hidden Treasures & Hipster Havens**
Walk through the art-covered streets of Fabrika, a Soviet sewing factory turned creative hub. Chill in vintage cafes or join a pop-up rooftop gig – locals will welcome you with open arms.

🎒 **Conclusion:** Tbilisi is not just a destination – it’s a mood. Whether you're a digital nomad, foodie, or culture-lover, this city has a rhythm you'll want to dance to.

🔎 **Meta Summary:**
- **Keywords:** Tbilisi, Georgia travel, hidden gems, Old Town, khachapuri, digital nomads
- **Extract:** "Tbilisi combines ancient grit with creative soul – a perfect city for curious travelers."
- **Tweet:** “Cobblestone lanes, wine cellars, rooftop gigs – Tbilisi, you’ve got my heart. 💛 #TravelGeorgia”
- **Image Prompt:** “Bohemian streets of Tbilisi, twilight, Georgian architecture, street art, wine glasses”
"""

# === INSTRUCTIONS ===
INSTRUCTIONS = (
    "You are a travel blog writer creating structured, engaging, beautifully formatted content.\\n"
    "Use markdown headers, subheadings, icons, and emojis. Respond in sections:\\n"
    "- Title (with emoji)\\n"
    "- Intro paragraph\\n"
    "- 3 sub-sections (with subheadings + emojis)\\n"
    "- Conclusion\\n"
    "- Meta summary (keywords, extract, tweet, image prompt)\\n"
    "⚠️ Important: DO NOT mention or combine other locations, countries, or cities. Only write about the destination provided.\\n"
    "✅ Validate that the city name and country in the title match the topic provided.\\n"
    "Keep the total blog around 700–750 words. Stay factual, helpful, and vivid like the example."
)

# === QUESTIONS ===
QUESTIONS = [
    ("🌍 What destination, hotel, or travel experience is the blog post about?", "topic"),
    ("🎯 What is the main purpose of the blog post?", "purpose"),
    ("👥 Who is the target audience?", "audience"),
    ("🗣️ What tone and style do you prefer?", "tone"),
    ("🧳 What kind of content should be included?", "content"),
    ("✨ Any unique features or USPs to highlight?", "features"),
    ("📣 Where will this blog post be published?", "channel"),
    ("🌐 What language should this blog be written in?", "language")
]

# === UI ===
st.title("🌍 Hospitality Blog Assistant")
st.markdown("Let’s create your blog post. I’ll ask you a few quick questions:")

# === QUESTION FLOW ===
if st.session_state.step < len(QUESTIONS):
    question, key = QUESTIONS[st.session_state.step]
    answer = st.text_input(question)
    if answer:
        st.session_state.answers[key] = answer.strip()
        st.session_state.step += 1
        st.rerun()
else:
    if not st.session_state.show_blog:
        if st.button("🪄 Generate Blog Post"):
            user_brief = "\\n".join([f"{k.capitalize()}: {v}" for k, v in st.session_state.answers.items()])
            prompt = f"{INSTRUCTIONS}\\n\\nHere is a sample blog:\\n{EXAMPLE_POST}\\n\\nNow write a new blog post based on this brief:\\n{user_brief}"

            with st.spinner("Crafting your precise, location-accurate blog post..."):
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

# === OUTPUT ===
if st.session_state.show_blog:
    st.subheader("📄 Your Blog Post")
    st.markdown(st.session_state.blog_output)

    if st.button("🔁 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.show_blog = False
        st.rerun()
