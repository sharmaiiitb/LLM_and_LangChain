import openai
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("No OpenAI API key found. Please set your OpenAI API key in the .env file.")

def ask_question(subject, question):
    # Define the context based on the selected subject
    contexts = {
        "math": "You are a math tutor.",
        "science": "You are a science tutor.",
        "history": "You are a history tutor.",
        "geography": "You are a geography expert.",
        "literature": "You are a literature expert.",
        "physics": "You are a physics expert.",
        "chemistry": "You are a chemistry expert."
    }
    context = contexts.get(subject, "You are a knowledgeable tutor.")

    conversation = [
        {"role": "system", "content": context},
        {"role": "user", "content": question}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    reply = response['choices'][0]['message']['content']
    return reply

# Streamlit app layout
st.title("TutorGPT")
st.header("Ask questions from a tutor specialized in various subjects.")

# Dropdown menu for subject selection
subject = st.selectbox("Select Subject", ["math", "science", "history", "geography", "literature", "physics", "chemistry"])

# Text area for question input
question = st.text_area("Your Question", "")

# When the 'Ask' button is clicked, call the ask_question function
if st.button("Ask"):
    if question:
        with st.spinner("Thinking..."):
            answer = ask_question(subject, question)
            st.text_area("Tutor's Answer", answer, height=300)
    else:
        st.error("Please enter a question.")
