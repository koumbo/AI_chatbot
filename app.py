import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.title("💬 DailyDialog Chatbot (DialoGPT)")

# Load model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

tokenizer, model = load_model()

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = None
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:", "")

if user_input:
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([st.session_state.history, input_ids], dim=-1) if st.session_state.history is not None else input_ids

    st.session_state.history = model.generate(
        bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )

    output = tokenizer.decode(
        st.session_state.history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True
    )

    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", output))

# Display messages
for role, msg in st.session_state.messages:
    st.markdown(f"**{role}:** {msg}")
