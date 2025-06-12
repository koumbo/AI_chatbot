import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from voice_input_component import voice_input  # our custom component

st.title("🎙️ DailyDialog Voice Chatbot (Web-based)")

# Load model
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

tokenizer, model = load_model()

# Chat history
if "history" not in st.session_state:
    st.session_state.history = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Choose input mode
input_mode = st.radio("Choose input mode:", ["Text", "Voice (Web)"])
user_input = ""
# Handle input based on mode
if input_mode == "Voice (Web)":
    st.write("Click the mic button to speak:")
    user_input = voice_input()

    # Workaround: component sets user_input via session state
    if "voice" in st.session_state and st.session_state["voice"]:
        user_input = st.session_state["voice"]
    st.session_state["voice"] = None  # Reset after use

else:
    user_input = st.text_input("You:", "")

# Process input
if user_input and isinstance(user_input, str):
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = (
        torch.cat([st.session_state.history, input_ids], dim=-1)
        if st.session_state.history is not None else input_ids
    )

    st.session_state.history = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )

    output = tokenizer.decode(
        st.session_state.history[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", output))

# Show messages
for role, msg in st.session_state.messages:
    st.markdown(f"**{role}:** {msg}")
