import streamlit as st
import pdfkit
import tempfile
import os

# Configuration de la page (utilisez un emoji ou une URL pour page_icon)
st.set_page_config(
    page_title="FactuBot - Download Invoice",
    page_icon="📄",  # Utilisez un emoji ou une URL
    layout="centered"
)

# CSS personnalisé
st.markdown("""
<style>
.title {
    color: #1e3c72;
    font-size: 35px;
    margin: 0;
}
.stApp {
    background: #f5f7fa;
}
.container {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    max-width: 800px;
    margin: 20px auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Chemin absolu vers l'icône
icon_path = r"C:\Users\PC\ML\factubot\download.jpg"

# Vérifiez que le fichier existe
if not os.path.exists(icon_path):
    st.error(f"Le fichier {icon_path} n'existe pas.")
else:
    # Afficher l'icône et le titre côte à côte
    col1, col2 = st.columns([0.2, 1])
    with col1:
        st.image(icon_path, width=50)
    with col2:
        st.markdown('<h1 class="title">FactuBot - Download Invoice</h1>', unsafe_allow_html=True)

# Vérifier si les données de facture existent
if "invoice_data" not in st.session_state or "invoice_html" not in st.session_state:
    st.error("No invoice data found. Please upload an invoice first.")
    if st.button("Go Back to Upload Page"):
        st.switch_page("pages/2_Invoice.py")
else:
    # Afficher l'aperçu de la facture
    st.subheader("Invoice Preview")
    st.components.v1.html(st.session_state.invoice_html, height=600)

    # Générer et télécharger le PDF
    if st.button("Download Invoice as PDF"):
        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdfkit.from_string(st.session_state.invoice_html, tmp_pdf.name, configuration=config)
            tmp_pdf_path = tmp_pdf.name
        with open(tmp_pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="invoice.pdf",
                mime="application/pdf"
            )
        os.unlink(tmp_pdf_path)

    # Bouton pour revenir à la page précédente
    if st.button("Go Back to Upload Page"):
        st.switch_page("pages/2_Invoice.py")
