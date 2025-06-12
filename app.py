# -*- coding: utf-8 -*-

import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import speech_recognition as sr
import pyttsx3

# Load pre-trained DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize chat history
chat_history_ids = None

# Initialize TTS engine
engine = pyttsx3.init()

# Function to generate bot response
def generate_response(user_input):
    global chat_history_ids
    
    # Encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    
    # Append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids
    
    # Generate a bot response
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # Decode the generated response
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return response

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.write("Could not request results; check your network connection.")
    return ""

# Streamlit app title
st.title("DailyDialog Chatbot")

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# User input form
with st.form(key='my_form'):
    user_input = st.text_input(label='You:', placeholder='Type your message here...')
    submit_button = st.form_submit_button(label='Send')

# Voice input button
voice_input_button = st.button('Speak')

# Process user input and generate response
if submit_button and user_input:
    response = generate_response(user_input)
    st.session_state.history.append(('You', user_input))
    st.session_state.history.append(('Bot', response))
    text_to_speech(response)

if voice_input_button:
    user_input = speech_to_text()
    if user_input:
        response = generate_response(user_input)
        st.session_state.history.append(('You', user_input))
        st.session_state.history.append(('Bot', response))
        text_to_speech(response)

# Display chat history
for sender, message in st.session_state.history:
    if sender == 'You':
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"**{sender}:** {message}")

