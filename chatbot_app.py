# import library
import dotenv
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# load environment
load_dotenv()

# initialize Gemini-Pro model and API
get_api_key = os.getenv("API_Key")
genai.configure(api_key = get_api_key)
model = genai.GenerativeModel("gemini-2.5-pro")

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role
  
# chat history object and store into Streamlit session state
if "chat" not in st.session_state:
  st.session_state.chat = model.start_chat(history=[])

# Display form title
st.title("Chat application using Gemini Pro")
st.subt

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
  with st.chat_message(role_to_streamlit(message.role)):
    st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("Ask anything"):
  # Display user's last message
  st.chat_message("user").markdown(prompt)

  # Send user entry to Gemini and read the response
  response = st.session_state.chat.send_message(prompt)

  # Display last
  with st.chat_message("assistant"):
    # handling error
    try:
      st.markdown(response.text)
    except ValueError as e:
      st.error(f"Error accessing response text: {e}")
