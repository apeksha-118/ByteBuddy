import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.set_page_config(page_title="ChatGPT with Streamlit", page_icon="🤖", layout="centered")
st.title("🤖 OpenAI Chatbot")
st.write("Ask me anything!")

# User input
user_input = st.text_area("Enter your question:", "")

if st.button("Ask"):
    if user_input.strip():
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_input}]
            )
            # Display AI response
            st.subheader("💡 Response:")
            st.write(response["choices"][0]["message"]["content"])
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using OpenAI & Streamlit")
