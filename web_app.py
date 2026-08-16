import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv
from google import genai
from PIL import Image
import io
import os

# 1. Page Configuration
st.set_page_config(
    page_title="JUIT AI Note Engine",
    page_icon="🎓",
    layout="wide"
)

# 2. PDF Generation Function
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    
    # Header for JUIT Branding
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, text="JUIT Academic Intelligence Hub", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Multiline text for notes
    pdf.set_font("Helvetica", size=11)
    
    # Clean and sanitize characters for Latin-1 compatibility
    replacements = {
        "—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "•": "*", "→": "->", "←": "<-", "≥": ">=", "≤": "<=", "≠": "!=",
        "≈": "~", "×": "*", "÷": "/", "…": "...", "°": " deg"
    }
    sanitized_text = text
    for k, v in replacements.items():
        sanitized_text = sanitized_text.replace(k, v)
        
    safe_text = sanitized_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, text=safe_text)
    
    # Return as in-memory bytes buffer
    pdf_buffer = io.BytesIO(bytes(pdf.output()))
    return pdf_buffer

# 3. Environment & Secrets Handling
load_dotenv()

# Detect pre-configured API Key from Streamlit Secrets or Environment Variable
detected_api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        detected_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not detected_api_key:
    detected_api_key = os.getenv("GEMINI_API_KEY", "")

# 4. Sidebar UI
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Allow user to provide/override API Key directly in UI
    user_api_key = st.text_input(
        "Google Gemini API Key",
        value=detected_api_key,
        type="password",
        help="Get a free Gemini API key at https://aistudio.google.com/app/apikey"
    )
    
    selected_model = st.selectbox(
        "AI Model",
        options=["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )
    
    st.markdown("---")
    st.header("📤 Upload Center")
    uploaded_file = st.file_uploader("Upload lecture photo / diagram", type=["jpg", "jpeg", "png", "webp"])
    process_btn = st.button("Generate & Prepare PDF 🚀", type="primary", use_container_width=True)

# Main Title & Subtitle
st.title("🎓 JUIT Smart Research Assistant")
st.caption("AI-Powered Lecture Note Extraction & Engineering Document Generator")

# API Key Validation Message
active_api_key = user_api_key.strip() if user_api_key else ""

if not active_api_key:
    st.info("💡 **Getting Started:** Enter your Google Gemini API Key in the sidebar. You can generate a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).")

# 5. Processing Logic
if uploaded_file and process_btn:
    if not active_api_key:
        st.error("🔑 Please provide a valid Gemini API Key in the sidebar before generating notes.")
    else:
        col1, col2 = st.columns([1, 1])
        image = Image.open(uploaded_file)
        
        with col1:
            st.subheader("📷 Source Image")
            st.image(image, caption=uploaded_file.name, use_container_width=True)

        with col2:
            st.subheader("📝 AI-Generated Academic Notes")
            with st.spinner(f"Analyzing with {selected_model}..."):
                try:
                    # Initialize client with the active API key
                    client = genai.Client(api_key=active_api_key)
                    
                    response = client.models.generate_content(
                        model=selected_model,
                        contents=[
                            image,
                            "Analyze this image and create comprehensive, well-structured academic engineering study notes. "
                            "Include summary, key formulas/concepts (use LaTeX for math: $$ or $), diagrams breakdown, "
                            "and code blocks where applicable. Format nicely with Markdown headings and bullet points."
                        ]
                    )
                    
                    notes_text = response.text
                    st.markdown(notes_text)
                    
                    # Prepare PDF Download
                    try:
                        pdf_output = create_pdf(notes_text)
                        st.download_button(
                            label="📥 Download Professional PDF",
                            data=pdf_output,
                            file_name="JUIT_Study_Notes.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as pdf_err:
                        st.warning(f"Could not generate PDF download: {pdf_err}")

                except Exception as e:
                    err_msg = str(e)
                    if "401" in err_msg or "UNAUTHENTICATED" in err_msg or "API_KEY_INVALID" in err_msg or "invalid authentication" in err_msg.lower():
                        st.error("🔑 **Authentication Error:** Invalid API Key. Please make sure you are using a valid Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).")
                    elif "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                        st.error("⏳ **Rate Limit Exceeded:** Free tier quota reached. Please wait a minute before retrying.")
                    elif "503" in err_msg or "high demand" in err_msg.lower() or "UNAVAILABLE" in err_msg:
                        st.error("⚠️ **Server at Capacity:** Google's AI servers are currently busy. Please retry in a few moments.")
                    else:
                        st.error(f"🔍 **Error:** {err_msg}")
elif not uploaded_file and process_btn:
    st.warning("⚠️ Please upload an image in the sidebar first.")
