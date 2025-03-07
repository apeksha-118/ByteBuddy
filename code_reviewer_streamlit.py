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

    # Use the ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if GPT-4 is not available
        messages=[ 
            {"role": "system", "content": "You are a helpful and knowledgeable code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,  # Lower temperature for more focused and deterministic responses
        max_tokens=1000   # Adjust based on the expected length of the review
    )

    # Extract the feedback from the response
    feedback = response['choices'][0]['message']['content']
    return feedback

def review_code(code, language, custom_prompt):
    """
    Function to review code using OpenAI's API.
    """
    if not code.strip():
        return "Error: No code provided for review."
    
    try:
        feedback = get_code_review(code, language, custom_prompt)
        return feedback
    except openai.error.RateLimitError:
        return "Error: API rate limit exceeded. Please try again later."
    except openai.error.AuthenticationError:
        return "Error: Invalid API key. Please check your OpenAI API key."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.title("ByteBuddy- Code Reviewer")
    
    # File uploader to upload code file
    uploaded_file = st.file_uploader("Upload your code file", type=["py", "js", "java", "cpp", "txt"])
    
    # User inputs
    language = st.selectbox("Select the programming language:", ["Python", "JavaScript", "Java", "C++", "Other"])
    custom_prompt = st.text_input("Any specific instructions for the review?")

    if uploaded_file is not None:
        # Read the uploaded file's content
        code = uploaded_file.read().decode("utf-8")
    else:
        code = st.text_area("Paste your code here:", height=200)
    
    # Trigger code review
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
