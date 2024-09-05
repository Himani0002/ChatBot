from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google Generative AI with the API key
genai.configure(api_key=os.getenv("Google_API_KEY"))

# Initialize the model and chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get response from Gemini LLM
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Set Streamlit page configuration
st.set_page_config(page_title="Q&A Demo")

# Streamlit header
st.header("Gemini LLM Application")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input field for user question
input = st.text_input("Input:", key="input")

# Submit button to ask the question
submit = st.button("Ask the question")

# If submit is clicked and input is not empty
if submit and input:
    response = get_gemini_response(input)
    st.session_state["chat_history"].append(("You", input))
    
    st.subheader("The Response is")
    
    # Display the response from Gemini LLM
    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append(("Bot", chunk.text))
    
    st.subheader("The chat history is")
    
    # Display the chat history
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
