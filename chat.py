from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Function to load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

##Streamlit APP

st.set_page_config(page_title="Q&A BOT")
st.markdown(
    "<h1 style='text-align: center; color: #B78700; font-family: Arial;'>CHAT BOT 🏦</h1>",
    unsafe_allow_html=True
)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input =st.text_input("",placeholder="Type here..." , key="user_input")
submit = st.button("Submit")

if submit and user_input :
    respone = get_gemini_response(user_input)
    st.session_state['chat_history'].append(("👨‍💻",user_input))
    st.subheader("Response")
    for chunk in respone:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("🗿",chunk.text))
st.subheader("Chat History :")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")

with st.sidebar:
    st.title("Chat Settings")
    if st.button("Clear Chat History"):
        st.session_state['chat_history'] = []
        st.rerun()
    