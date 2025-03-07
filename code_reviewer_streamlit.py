import os
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ByteBuddy - AI Code Reviewer", layout="centered")
st.title("ByteBuddy - AI Code Reviewer")
st.write("Upload your code files for a detailed review.")

# File uploader that allows multiple files (excluding .txt)
uploaded_files = st.file_uploader("Choose files to upload", type=["py", "java", "cpp", "c"], accept_multiple_files=True)

language = st.selectbox("Select the programming language:", ["Python", "Java", "C++", "C", "Other"])

custom_prompt = st.text_input("Any specific instructions for the review?")

if st.button("Review Code") and uploaded_files:
    try:
        for uploaded_file in uploaded_files:
            # Read the content of each file
            file_content = uploaded_file.getvalue().decode("utf-8")

            prompt = f"""
            Review the following {language} code for quality, style, potential issues, and improvements:
            
            {file_content}
            
            Additional instructions: {custom_prompt}
            """

            # Call OpenAI API for code review
            response = openai.completions.create(
                model="gpt-4",
                prompt=prompt,
                max_tokens=1000
            )
            
            st.subheader(f"💡 Code Review for {uploaded_file.name}:")
            st.write(response["choices"][0]["text"])

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please upload some code files for review.")
