
import streamlit as st
import openai

# === CONFIGURATION ===
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store in Streamlit secrets

FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal:blogger:BKfX4OnW"

# === SESSION STATE ===
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = False
    st.session_state.user_answers = {}
    st.session_state.show_blog = False

# === UI ===
st.title("📝 Hospitality Blog Assistant")
st.markdown("Ask me to write a blog post — I’ll ask a few quick questions to make it perfect.")

# === Initial Prompt ===
user_input = st.text_input("What would you like the blog post to be about?", "")

if user_input and not st.session_state.questions_asked:
    st.session_state.questions_asked = True
    st.session_state.user_request = user_input

# === Ask Questions ===
if st.session_state.questions_asked and not st.session_state.show_blog:
    st.markdown("Great! Just a few quick questions:")

    st.session_state.user_answers["audience"] = st.text_input("1. Who is your target audience?")
    st.session_state.user_answers["tone"] = st.text_input("2. What tone or style do you prefer?")
    st.session_state.user_answers["features"] = st.text_input("3. Any key features or angles to include?")

    if all(st.session_state.user_answers.values()):
        if st.button("Generate Blog Post"):
            # Construct the final prompt
            full_prompt = f"""
Please write a blog post based on the following details:
- Topic: {st.session_state.user_request}
- Audience: {st.session_state.user_answers['audience']}
- Tone: {st.session_state.user_answers['tone']}
- Features to include: {st.session_state.user_answers['features']}
""".strip()

            with st.spinner("Writing your blog post..."):
                response = openai.ChatCompletion.create(
                    model=FINE_TUNED_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a travel and hospitality blogger assistant."},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                blog_output = response["choices"][0]["message"]["content"]
                st.session_state.blog_output = blog_output
                st.session_state.show_blog = True

# === Display Final Blog Post ===
if st.session_state.show_blog:
    st.subheader("🧳 Your Blog Post")
    st.write(st.session_state.blog_output)

    if st.button("Start Over"):
        st.session_state.questions_asked = False
        st.session_state.user_answers = {}
        st.session_state.show_blog = False
        st.experimental_rerun()
