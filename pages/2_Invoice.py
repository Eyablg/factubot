import streamlit as st
import pytesseract
import re
import pandas as pd
import tempfile
from PIL import Image
import os
import base64

# Set the Tesseract path (pour Windows local uniquement)
if os.name == 'nt':  # Si le système est Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Sur Streamlit Cloud, Tesseract est installé via config.toml, donc pas besoin de chemin absolu

# Function to encode an image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Set paths for icons (chemins relatifs)
invoice_icon_path = "assets/invoice.jpg"
chatbot_icon_path = "assets/chatbot.jpg"
download_icon_path = "assets/download.jpg"

# Encode icons
invoice_icon_base64 = img_to_base64(invoice_icon_path)
chatbot_icon_base64 = img_to_base64(chatbot_icon_path)
download_icon_base64 = img_to_base64(download_icon_path)

st.set_page_config(
    page_title="FactuBot - Upload Invoice",
    page_icon=invoice_icon_path,
    layout="centered"
)

# Custom CSS for styling
st.markdown(f"""
<style>
.title {{
    color: #2c3e50;
    font-size: 35px;
    text-align: center;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}}
.title-icon {{
    width: 40px;
    height: 40px;
}}
.container {{
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    max-width: 800px;
    margin: 20px auto;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}}
.stApp {{
    background: #f8f9fa;
}}
.chat-container {{
    margin-top: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    height: 250px;
    overflow-y: scroll;
    background-color: #f9f9f9;
}}
.chat-message-user {{
    background-color: #81C784;
    color: #2c3e50;
    padding: 10px 15px;
    border-radius: 18px;
    margin: 5px;
    max-width: 70%;
    float: right;
    clear: both;
}}
.chat-message-bot {{
    background-color: #e8f5e9;
    color: #2c3e50;
    padding: 10px 15px;
    border-radius: 18px;
    margin: 5px;
    max-width: 70%;
    float: left;
    clear: both;
}}
.chat-buttons {{
    display: flex;
    justify-content: center;
    margin-top: 15px;
    gap: 10px;
}}
.chat-button {{
    background-color: #81C784;
    color: #2c3e50;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}}
.chat-button:hover {{
    background-color: #6ba872;
}}
.chatbot-title {{
    display: flex;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 10px;
}}
.chatbot-title h2 {{
    margin: 0;
    margin-left: 10px;
    color: #2c3e50;
}}
.help-button {{
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin-left: 10px;
}}
.help-button img {{
    width: 24px;
    height: 24px;
}}
.data-table {{
    margin-top: 20px;
    border-collapse: collapse;
    width: 100%;
}}
.data-table th, .data-table td {{
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}}
.data-table th {{
    background-color: #81C784;
    color: #2c3e50;
}}
.data-table tr:nth-child(even) {{
    background-color: #e8f5e9;
}}
.download-section {{
    display: flex;
    justify-content: center;
    margin-top: 20px;
}}
.download-button {{
    background-color: #81C784;
    color: #2c3e50;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}}
.download-button:hover {{
    background-color: #6ba872;
}}
.download-icon {{
    width: 20px;
    height: 20px;
}}
</style>
""", unsafe_allow_html=True)

# Title with invoice icon
st.markdown(f'''
<div class="title">
    <img class="title-icon" src="data:image/jpeg;base64,{invoice_icon_base64}">
    <h1>FactuBot - Upload Invoice</h1>
</div>
''', unsafe_allow_html=True)

# Initialize chat messages in session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chatbot_state" not in st.session_state:
    st.session_state.chatbot_state = "start"

# Function to add messages to the chat
def add_message(role, message):
    st.session_state.chat_messages.append({"role": role, "message": message})

# Upload image
uploaded_file = st.file_uploader("Upload an invoice image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully!")

    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Extract text from image using Pillow and pytesseract
    def extract_text_from_image(image_path):
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='fra+eng')
        return text

    # Analyze extracted text
    def analyze_text(text):
        nom_match = re.search(r'(Nom|Pour|Client|Commande Pour).*?:\s*(.*)', text)
        nom = nom_match.group(2).strip() if nom_match else "Nom non trouvé"
        adresse_match = re.search(r'(Adresse|Adr|Livraison|Livrer à).*?:\s*(.*)', text)
        adresse = adresse_match.group(2).strip() if adresse_match else "Adresse non trouvée"
        date_commande_match = re.search(r'(Commander|Commande|Date).*?:\s*(\d{2}\s\w+\s\d{4}|\d{2}/\d{2}/\d{4})', text)
        date_commande = date_commande_match.group(2).strip() if date_commande_match else "Date non trouvée"
        date_livraison_match = re.search(r'(Livraison|Délai|Livrer sous).*?:\s*(.*)', text)
        date_livraison = date_livraison_match.group(2).strip() if date_livraison_match else "5 jours ouvrables"
        produit_match = re.search(r'(\d+)\s*(iPhone|iPad|MacBook|AirPods|Apple Watch)', text, re.IGNORECASE)
        nombre_produits = produit_match.group(1).strip() if produit_match else "1"
        type_produit = produit_match.group(2).strip() if produit_match else "iPhone"
        couleurs_possibles = [
            r'\bnoir(s)?\b', r'\bblanc(s)?\b', r'\brouge(s)?\b', r'\bbleu(s)?\b',
            r'\bvert(s)?\b', r'\bjaune(s)?\b', r'\bgris\b', r'\brose(s)?\b',
            r'\bviolet(s)?\b', r'\bmarron(s)?\b', r'\borange(s)?\b', r'\bdor[éè](s)?\b'
        ]
        couleurs_mentionnees = []
        for couleur_pattern in couleurs_possibles:
            couleur_matches = re.finditer(couleur_pattern, text, re.IGNORECASE)
            for match in couleur_matches:
                couleurs_mentionnees.append(match.group().lower())
        couleurs_mentionnees = list(set(couleurs_mentionnees))
        couleurs_produit = []
        produit_couleur_match = re.search(r'(\d+)\s*(iPhone|iPad|MacBook|AirPods|Apple Watch).*?(:\s*|,)(.*)', text, re.IGNORECASE)
        if produit_couleur_match:
            couleurs_produit_text = produit_couleur_match.group(4).strip()
            for couleur_pattern in couleurs_possibles:
                couleur_matches = re.finditer(couleur_pattern, couleurs_produit_text, re.IGNORECASE)
                for match in couleur_matches:
                    couleurs_produit.append(match.group().lower())
        if not couleurs_produit and couleurs_mentionnees:
            couleurs_produit = couleurs_mentionnees
        couleurs = ", ".join(couleurs_produit) if couleurs_produit else ", ".join(couleurs_mentionnees) if couleurs_mentionnees else "Non précisé"
        prix_piece_match = re.search(r'(Prix|prix).*?:\s*(\d+\s?€)', text)
        prix_piece = prix_piece_match.group(2).strip() if prix_piece_match else "250€"
        prix_total = str(int(nombre_produits) * int(prix_piece.replace("€", "").strip())) + "€"
        return {
            "Nom": nom,
            "Adresse": adresse,
            "Date de Commande": date_commande,
            "Date de Livraison": date_livraison,
            "Nombre de Produits": nombre_produits,
            "Type de Produit": type_produit,
            "Couleurs": couleurs,
            "Prix par Pièce": prix_piece,
            "Prix Total": prix_total,
        }

    # Generate invoice HTML with soft green theme
    def generate_invoice_html(data):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                    border-bottom: 2px solid #81C784;
                    padding-bottom: 10px;
                }}
                .header h1 {{
                    color: #81C784;
                }}
                .info {{
                    margin-bottom: 20px;
                }}
                .info p {{
                    margin: 5px 0;
                }}
                .info strong {{
                    color: #81C784;
                }}
                .table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                .table th, .table td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                .table th {{
                    background-color: #81C784;
                    color: #2c3e50;
                }}
                .table tr:nth-child(even) {{
                    background-color: #e8f5e9;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>FACTURE</h1>
                <p>Date: {data['Date de Commande']}</p>
            </div>
            <div class="info">
                <p><strong>Nom du Client:</strong> {data['Nom']}</p>
                <p><strong>Adresse:</strong> {data['Adresse']}</p>
                <p><strong>Date de Livraison:</strong> {data['Date de Livraison']}</p>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>Type de Produit</th>
                        <th>Nombre de Produits</th>
                        <th>Couleurs</th>
                        <th>Prix par Pièce</th>
                        <th>Prix Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{data['Type de Produit']}</td>
                        <td>{data['Nombre de Produits']}</td>
                        <td>{data['Couleurs']}</td>
                        <td>{data['Prix par Pièce']}</td>
                        <td>{data['Prix Total']}</td>
                    </tr>
                </tbody>
            </table>
            <div class="footer">
                <p>Merci pour votre achat !</p>
            </div>
        </body>
        </html>
        """

    # Extract and analyze text
    text = extract_text_from_image(tmp_file_path)
    data = analyze_text(text)

    # Store data in session state
    st.session_state.invoice_data = data
    st.session_state.invoice_html = generate_invoice_html(data)

    # Display extracted data in a table
    st.subheader("Extracted Data")
    df = pd.DataFrame([data])
    st.table(df)

    # Display invoice preview
    st.subheader("Invoice Preview")
    st.components.v1.html(st.session_state.invoice_html, height=600)

    # Chatbot section with local chatbot icon
    st.markdown(f'''
    <div class="chatbot-title">
        <img src="data:image/jpeg;base64,{chatbot_icon_base64}" width="40" height="40">
        <h2>Chatbot</h2>
    </div>
    ''', unsafe_allow_html=True)

    # Initialize chatbot conversation
    if st.session_state.chatbot_state == "start":
        add_message("bot", "Hello! 👋")
        add_message("bot", "Please verify your invoice details above. Are the details correct?")
        st.session_state.chatbot_state = "ask_verification"

    # Display chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message-user">{message["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message-bot">{message["message"]}</div>', unsafe_allow_html=True)

    # Show "Yes/No" buttons if the chatbot is asking for verification
    if st.session_state.chatbot_state == "ask_verification":
        st.markdown('<div class="chat-buttons">', unsafe_allow_html=True)
        if st.button("👍 Yes", key="yes_button", help="Click to confirm"):
            add_message("user", "Yes")
            add_message("bot", "Great! You can now download your invoice.")
            st.session_state.chatbot_state = "download_prompt"
        if st.button("👎 No", key="no_button", help="Click if details are incorrect"):
            add_message("user", "No")
            add_message("bot", "Please check the details again. Let me know if you need any help!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Download section with icon and button (single button)
    if st.button("Download Invoice", key="download_invoice"):
        st.switch_page("pages/3_Download.py")

    # Clean up
    os.unlink(tmp_file_path)
