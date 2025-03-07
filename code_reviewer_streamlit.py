import os
import openai
import streamlit as st

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_code_review(code, language, custom_prompt):
    prompt = f"""
    Review the following {language} code for quality, style, and potential issues:
    
    {code}
    
    Additional instructions: {custom_prompt}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[ 
                {"role": "system", "content": "You are a helpful and knowledgeable code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        feedback = response['choices'][0]['message']['content']
        return feedback

    except openai.RateLimitError as e:
        return f"Error: API rate limit exceeded. Please try again later. ({str(e)})"
    
    except openai.AuthenticationError as e:
        return f"Error: Invalid API key. Please check your OpenAI API key. ({str(e)})"

    except openai.OpenAIError as e:
        return f"An error occurred with the OpenAI API: {str(e)}"
    
    except Exception as e:
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
