# Integrated Q&A Chatbot with Text and Image Processing using Streamlit and Google Generative AI

# Imports and setup
import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to get response from Gemini model with separate handling for text and image
def get_gemini_response(text_input, image, text_model, image_model):
    try:
        if text_input and not image:
            response = text_model.generate_content(text_input)
        elif image:
            content = [text_input, image] if text_input else image
            response = image_model.generate_content(content)
        else:
            return "No input provided."
        return response.text
    except Exception as e:
        st.error(f"Error during model response generation: {e}")  
        return f"Sorry, I couldn't fetch a response due to an error: {e}"

st.set_page_config(page_title="Gemini Q&A Demo", layout="wide")
st.title("Gemini Application - Text and Image Analysis")

with st.sidebar:
    st.header("Navigation")
    mode = st.radio("Choose the analysis mode:", ("Text-based Q&A", "Image-based Q&A"))

    st.header("Instructions")
    st.write("""
        - Select the analysis mode above.
        - For text-based Q&A, enter your question in the text area on the left.
        - For image-based Q&A, upload an image on the left and optionally add a descriptive text.
        - Click 'Try it out!' below to get the analysis result.
    """)


user_input = None
image = None

if mode == "Text-based Q&A":
    st.subheader("Text-based Q&A")
    user_input = st.text_area("Enter your question:", key="text_input", height=150)
elif mode == "Image-based Q&A":
    st.subheader("Image-based Q&A")
    uploaded_file = st.file_uploader("Choose an image (jpg, jpeg, png):", type=["jpg", "jpeg", "png"], key="image_upload")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Try it out!")
text_model = genai.GenerativeModel('gemini-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')

if submit:
    with st.spinner('Generating response...'):
        response = get_gemini_response(user_input, image, text_model, image_model)
    
    if response:
        st.subheader("Analysis Result:")
        
        st.markdown(f"**Response:** {response}")

        with st.expander("See detailed analysis"):
            st.write(response)  

        feedback = st.selectbox("Was this analysis helpful?", ["Select an option", "Yes", "No"])
        if feedback != "Select an option":
            st.write("Thank you for your feedback!")