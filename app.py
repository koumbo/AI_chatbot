import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from voice_io_component import voice_io

st.set_page_config(page_title="Voice Chatbot", page_icon="🎙️")

st.title("🤖 Voice Chatbot with Input + Output")

# Load model
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

tokenizer, model = load_model()

# Initialize state
if "history" not in st.session_state:
    st.session_state.history = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Select input method
mode = st.radio("Choose input mode:", ["Text", "Voice (Browser)"])

if mode == "Text":
    user_input = st.text_input("You:", "")
else:
    # Call component, pass last bot message to read aloud
    last_bot_msg = ""
    for role, msg in reversed(st.session_state.messages):
        if role == "Bot":
            last_bot_msg = msg
            break

    user_input = voice_io(prompt_to_speak=last_bot_msg)

# Only respond if input exists
if user_input and isinstance(user_input, str) and user_input.strip():
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([st.session_state.history, input_ids], dim=-1) if st.session_state.history is not None else input_ids

    st.session_state.history = model.generate(
        bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        st.session_state.history[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", response))

# Display full chat history
for speaker, message in st.session_state.messages:
    if speaker == "You":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Bot:** {message}")
