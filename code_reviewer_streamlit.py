import os
import openai
import toml
import streamlit as st

# Load the API key from a TOML file
def load_api_key_from_toml():
    try:
        # Load the TOML file
        config = toml.load("secrets.toml")
        
        # Extract the API key from the [openai] section
        api_key = config['openai']['api_key']
        
        return api_key
    
    except FileNotFoundError:
        st.error("The 'secrets.toml' file containing the API key was not found.")
        return None
    except KeyError:
        st.error("API key not found in the 'secrets.toml' file.")
        return None

# Set OpenAI API key from the secrets file
openai.api_key = load_api_key_from_toml()

def get_code_review(code, language, custom_prompt):
    prompt = f"""
    Review the following {language} code for quality, style, and potential issues:
    
    {code}
    
    Additional instructions: {custom_prompt}
    """
    
    try:
        response = openai.completions.create(
            model="gpt-4",  
            prompt=prompt,  
            max_tokens=1000  
        )
        
        feedback = response['choices'][0]['text']  
        return feedback

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
