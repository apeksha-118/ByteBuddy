import os
import openai
import streamlit as st

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_code_review(code, language, custom_prompt):
    # Construct the prompt for the code review
    prompt = f"""
    Review the following {language} code for quality, style, and potential issues:
    
    {code}
    
    Additional instructions: {custom_prompt}
    """
    
    try:
        # Use the new completions.create method instead of ChatCompletion.create
        response = openai.completions.create(
            model="gpt-4",  # Or another model like "gpt-3.5-turbo"
            prompt=prompt,  # Pass the entire review prompt here
            max_tokens=1000  # Adjust based on expected response length
        )
        
        # Extract the feedback from the response
        feedback = response['choices'][0]['text']  # In new versions, it's 'text' instead of 'message'
        return feedback

    except openai.OpenAIError as e:  # Catching all OpenAI-related exceptions
        return f"An error occurred with the OpenAI API: {str(e)}"
    
    except Exception as e:  # Catch other unexpected exceptions
        return f"An unexpected error occurred: {str(e)}"

def review_code(code, language, custom_prompt):
    if not code.strip():
        return "Error: No code provided for review."
    
    try:
        feedback = get_code_review(code, language, custom_prompt)
        return feedback
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.title("ByteBuddy- Code Reviewer")
    
    uploaded_file = st.file_uploader("Upload your code file", type=["py", "js", "java", "cpp", "txt"])
    
    language = st.selectbox("Select the programming language:", ["Python", "JavaScript", "Java", "C++", "Other"])
    custom_prompt = st.text_input("Any specific instructions for the review?")

    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")
    else:
        code = st.text_area("Paste your code here:", height=200)
    
    if st.button("Review Code"):
        if not code.strip():
            st.warning("Please provide code to review, either by pasting or uploading a file.")
        else:
            with st.spinner("Reviewing your code..."):
                feedback = review_code(code, language, custom_prompt)
                st.success("Code review completed!")
                st.write(feedback)

if __name__ == "__main__":
    main()
