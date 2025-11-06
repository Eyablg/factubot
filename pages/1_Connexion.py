import streamlit as st
import base64

# Function to encode an image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Paths for icons
factubot_icon_path = r"C:\Users\PC\ML\factubot\icon1.jpg"  # Path for FactuBot icon
login_icon_path = r"C:\Users\PC\ML\factubot\login1.jpg"  # Path for login icon

# Encode the icons in base64
try:
    factubot_icon_base64 = img_to_base64(factubot_icon_path)
    login_icon_base64 = img_to_base64(login_icon_path)
except FileNotFoundError as e:
    st.error(f"Icon file not found: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error loading icon: {e}")
    st.stop()

# Configuration de la page
st.set_page_config(
    page_title="FactuBot - Login",
    page_icon=f"data:image/jpeg;base64,{factubot_icon_base64}",
    layout="centered"
)

# CSS pour le style
st.markdown(
    f"""
    <style>
    body {{
        background: #f5f7fa;
    }}
    .page-title {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-bottom: 50px;
        margin-top: 30px;
    }}
    .page-title img {{
        width: 60px;
        height: 60px;
    }}
    .page-title h1 {{
        color: #1e3c72;
        font-size: 40px;
        margin: 0;
        font-weight: bold;
    }}
    .container {{
        background-color: rgba(255, 255, 255, 0);
        padding: 20px;
        border-radius: 15px;
        max-width: 400px;
        margin: 0 auto;
        box-shadow: none;
        text-align: center;
    }}
    .login-title {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
        margin-top: 30px; /* Added margin to move down the login section */
    }}
    .login-title img {{
        width: 35px;
        height: 35px;
    }}
    .login-title h2 {{
        color: #2e8b57;
        font-size: 28px;
        margin: 0;
        font-weight: bold;
    }}
    .stTextInput>div>div>input {{
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        margin-bottom: 15px;
    }}
    .stButton>button {{
        background-color: #2e8b57;
        color: white;
        font-size: 16px;
        padding: 12px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        display: block;
        margin: 20px auto;
        width: 100%;
        transition: background-color 0.3s;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: #3cb371;
    }}
    .stApp {{
        background: #f5f7fa;
    }}
    .error-message {{
        color: #d32f2f;
        font-size: 14px;
        text-align: center;
        margin-top: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Titre de la page avec icône FactuBot
st.markdown(
    f"""
    <div class="page-title">
        <img src="data:image/jpeg;base64,{factubot_icon_base64}">
        <h1>FactuBot</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Conteneur principal (transparent)
st.markdown('<div class="container">', unsafe_allow_html=True)

# Titre de connexion avec icône de login
st.markdown(
    f"""
    <div class="login-title">
        <img src="data:image/jpeg;base64,{login_icon_base64}">
        <h2>Login</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Champs de connexion
username = st.text_input("Username", key="username_input", placeholder="Enter your username")
password = st.text_input("Password", type="password", key="password_input", placeholder="Enter your password")

# Bouton pour accéder aux factures
if st.button("Get Your Invoice"):
    if username == "admin" and password == "admin":  # Vérification des identifiants
        st.switch_page("pages/2_Invoice.py")
    else:
        st.markdown('<p class="error-message">Invalid username or password. Please try again.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
