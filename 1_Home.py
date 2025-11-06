import streamlit as st
import base64

# Function to encode an image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Function to set background image
def set_background_image(image_path):
    img_base64 = img_to_base64(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Paths for background and icon images
background_image_path = r"C:\Users\PC\ML\factubot\background1.jpg"
icon_path = r"C:\Users\PC\ML\factubot\icon1.jpg"

# Set background image
set_background_image(background_image_path)

# Encode the icon in base64
try:
    icon_base64 = img_to_base64(icon_path)
except FileNotFoundError:
    st.error("Icon file not found. Please check the path.")
    st.stop()
except Exception as e:
    st.error(f"Error loading icon: {e}")
    st.stop()

# Configure page
st.set_page_config(
    page_title="FactuBot - Home",
    page_icon=f"data:image/jpeg;base64,{icon_base64}",
    layout="centered"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .title-overlay {
        position: fixed;
        top: 15%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #00BFFF;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        z-index: 1;
    }
    .subtitle-overlay {
        position: fixed;
        top: 23%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #1e3c72;
        font-size: 20px;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        z-index: 1;
    }
    .container {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 30px;
        border-radius: 15px;
        max-width: 400px;
        margin: 300px auto;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .welcome-text {
        color: #1e3c72;
        font-size: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .stButton>button {
        background-color: #0077cc;
        color: white;
        font-size: 16px;
        padding: 12px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        display: block;
        margin: 0 auto;
        width: 200px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #0055aa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title overlay
st.markdown(
    """
    <div class="title-overlay">FactuBot</div>
    """,
    unsafe_allow_html=True
)

# Subtitle overlay
st.markdown(
    """
    <div class="subtitle-overlay">Your AI Billing Assistant</div>
    """,
    unsafe_allow_html=True
)

# Sign In button container
st.markdown(
    """
    <div class="container">
    <p class="welcome-text">Welcome to FactuBot</p>
    """,
    unsafe_allow_html=True
)

# Sign In button using Streamlit's button
sign_in_button = st.button("Sign In", key="sign_in")

# Close container div
st.markdown("</div>", unsafe_allow_html=True)

# Handle button click
if sign_in_button:
    st.switch_page("pages/1_Connexion.py")
