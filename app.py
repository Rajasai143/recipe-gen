import streamlit as st
import os

# Try importing dotenv and handle the case where it is missing
try:
    from dotenv import load_dotenv
    # Load environment variables from a .env file
    load_dotenv()
except ModuleNotFoundError:
    st.error("Required module 'dotenv' not found. Please install it using 'pip install python-dotenv'.")
    st.stop()

# Try importing google.generativeai and handle errors if the module is missing
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    st.error("Required module 'google-generativeai' not found. Please install it using 'pip install google-generativeai'.")
    st.stop()

# Get the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY is not set. Please add it to your environment variables or .env file.")
    st.stop()

# Configure the Google Generative AI with the API key
genai.configure(api_key=api_key)

# Create a Gemini Pro model instance
try:
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
except Exception as e:
    st.error(f"Failed to initialize the Generative AI model: {e}")
    st.stop()

# Function to get a response from the Gemini Pro model
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error communicating with the Generative AI: {e}")
        return []

# Set Streamlit page configuration
st.set_page_config(page_title="Recipe Generator AI", layout="wide")

# Function to load custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file '{file_name}' not found.")

# Uncomment if you have a custom CSS file
# local_css("styles1.css")

st.header("Recipe Generator AI")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Input field for user ingredients
user_input = st.text_area("Enter the ingredients you have:", key="input")

# Button to generate a recipe
if st.button("Generate Recipe") and user_input:
    prompt = f"Generate a recipe using the following ingredients: {user_input}"
    response = get_gemini_response(prompt)

    # Display the generated recipe
    if response:
        st.subheader("Generated Recipe:")
        response_text = ""
        for chunk in response:
            response_text += chunk.text
        st.markdown(f'<div class="response">{response_text}</div>', unsafe_allow_html=True)
        # Update session chat history
        st.session_state["chat_history"].append(("You", user_input))
        st.session_state["chat_history"].append(("Bot", response_text))
    else:
        st.error("No response generated. Please try again later.")

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state["chat_history"]:
    if role == "Bot":
        st.markdown(f"**{role}:** {text}")
    else:
        st.write(f"{role}: {text}")
