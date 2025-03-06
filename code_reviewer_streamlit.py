import streamlit as st
import openai
import os

# Set up OpenAI API key
openai.api_key = st.secrets["openai_api_key"]

# Language detection based on file extension
def detect_language(file_name):
    if file_name.endswith(".py"):
        return "Python"
    elif file_name.endswith(".cpp") or file_name.endswith(".c"):
        return "C++"
    elif file_name.endswith(".java"):
        return "Java"
    else:
        return "Unknown"

# Get code review feedback using OpenAI API
def get_code_review(code, language, custom_prompt=""):
    """Get code review feedback using OpenAI API."""
    prompt = f"""
    Review the following {language} code and provide feedback on:
    1. Code quality and readability.
    2. Potential bugs or issues.
    3. Suggestions for improvement.
    {custom_prompt}

    Code:
    {code}
    """

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use GPT-3.5 or Codex
        prompt=prompt,
        max_tokens=500,  # Adjust based on the length of feedback
        temperature=0.5,  # Balance creativity and accuracy
    )

    return response.choices[0].text.strip()

def main():
    st.set_page_config(page_title="AI Code Reviewer", page_icon=":computer:", layout="wide")
    st.title("ByteBuddy: AI-Based Code Reviewer")
    st.write("Upload your code files for AI-powered code review.")

    # Upload multiple files
    uploaded_files = st.file_uploader("Upload code files", type=["py", "cpp", "c", "java"], accept_multiple_files=True)
    custom_prompt = st.text_area("Custom Prompt (optional)", placeholder="e.g., Focus on performance and security.")

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write(f"### Reviewing: `{uploaded_file.name}`")
            code = uploaded_file.read().decode("utf-8")

            # Detect the programming language
            language = detect_language(uploaded_file.name)
            st.write(f"**Detected Language:** {language}")

            # Display the code
            with st.expander("View Code"):
                st.code(code, language=language.lower())

            # Get code review
            if st.button(f"Review {uploaded_file.name}"):
                with st.spinner("Analyzing code..."):
                    feedback = get_code_review(code, language, custom_prompt)
                    st.write("### Feedback")
                    st.write(feedback)

                    # Download feedback
                    st.download_button(
                        label="Download Feedback",
                        data=feedback,
                        file_name=f"{uploaded_file.name}_review.txt",
                        mime="text/plain",
                    )

if __name__ == "__main__":
    main()