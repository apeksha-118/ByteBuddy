import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Directly set API key here if dotenv doesn't work
openai.api_key = "your-api-key-here"

st.set_page_config(page_title="ByteBuddy - AI Code Reviewer", layout="centered")
st.title("ByteBuddy - AI Code Reviewer")
st.write("Upload your code files or paste your code below for a detailed review.")

uploaded_files = st.file_uploader("Choose files to upload", type=["py", "java", "cpp", "c"], accept_multiple_files=True)
user_input = st.text_area("Or paste your code here:", "")
language = st.selectbox("Select the programming language:", ["Python", "Java", "C++", "C", "Other"])
custom_prompt = st.text_input("Any specific instructions for the review?")

if st.button("Review Code"):
    if uploaded_files or user_input.strip():
        try:
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    file_content = uploaded_file.getvalue().decode("utf-8")
                    prompt = f"""
                    Review the following {language} code for quality, style, potential issues, and improvements:
                    
                    {file_content}
                    
                    Additional instructions: {custom_prompt}
                    """
                    response = openai.completions.create(
                        model="gpt-4",
                        prompt=prompt,
                        max_tokens=1000
                    )
                    st.subheader(f"💡 Code Review for {uploaded_file.name}:")
                    st.write(response["choices"][0]["text"])

            if user_input.strip():
                prompt = f"""
                Review the following {language} code for quality, style, potential issues, and improvements:
                
                {user_input}
                
                Additional instructions: {custom_prompt}
                """
                response = openai.completions.create(
                    model="gpt-4",
                    prompt=prompt,
                    max_tokens=1000
                )
                st.subheader("💡 Code Review for Pasted Code:")
                st.write(response["choices"][0]["text"])

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload some code files or paste code for review.")
