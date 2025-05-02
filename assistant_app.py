
import streamlit as st
import openai
import time

# Set your API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Your Assistant ID
ASSISTANT_ID = "asst_EKN77Pmtm44LsaF6MkhUdCPe"

st.set_page_config(page_title="Hospitality Blog Assistant (Assistant API)", layout="wide")

st.title("✍️ Hospitality Blog Assistant")
st.markdown("Let’s write your perfect blog post together using OpenAI's Assistant API! 🧳")

# Initialize session state
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id

# Get user input
user_input = st.chat_input("What would you like the blog post to be about? (e.g., 'Plovdiv, Bulgaria')")

if user_input:
    # Step 1: Add user's message to the thread
    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    # Step 2: Run the assistant
    run = openai.beta.threads.runs.create(
        assistant_id=ASSISTANT_ID,
        thread_id=st.session_state.thread_id
    )

    # Step 3: Poll the run status
    with st.spinner("Writing your travel blog post... 🌍"):
        while True:
            status = openai.beta.threads.runs.retrieve(thread_id=st.session_state.thread_id, run_id=run.id)
            if status.status == "completed":
                break
            elif status.status == "failed":
                st.error("The assistant failed to generate a response. Please try again.")
                break
            time.sleep(1)

    # Step 4: Get assistant's messages
    messages = openai.beta.threads.messages.list(thread_id=st.session_state.thread_id)

    st.markdown("---")
    st.subheader("📝 Your Blog Post")
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            st.markdown(msg.content[0].text.value)
