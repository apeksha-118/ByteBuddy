import os
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ByteBuddy - AI Code Reviewer", layout="centered")
st.title("ByteBuddy - AI Code Reviewer")
st.write("Paste your code below for a detailed review.")

user_input = st.text_area("Enter your code:", "")

language = st.selectbox("Select the programming language:", ["Python", "Java", "C++", "C", "Other"])

custom_prompt = st.text_input("Any specific instructions for the review?")

if st.button("Review Code"):
    if user_input.strip():
        try:
            prompt = f"""
            Review the following {language} code for quality, style, potential issues, and improvements:
            
            {user_input}
            
            Additional instructions: {custom_prompt}
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable and helpful code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            
            st.subheader("💡 Code Review:")
            st.write(response["choices"][0]["message"]["content"])

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some code for review.")
