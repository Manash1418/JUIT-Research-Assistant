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

api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY", "")

# 4. Helper for Smart Model Generation with Automatic Fallbacks
def generate_with_fallback(client, image, prompt, preferred_model):
    candidate_models = [preferred_model]
    defaults = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.5-pro", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
    for m in defaults:
        if m not in candidate_models:
            candidate_models.append(m)
            
    last_err = None
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[image, prompt]
            )
            return response, model_name
        except Exception as err:
            last_err = err
            err_str = str(err)
            # If model 404 or deprecated/not found, try next model in candidate list
            if "404" in err_str or "NOT_FOUND" in err_str or "no longer available" in err_str.lower():
                continue
            else:
                raise err
    raise last_err

# 5. Sidebar UI
with st.sidebar:
    st.header("⚙️ Settings")
    selected_model = st.selectbox(
        "AI Model",
        options=["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.5-pro", "gemini-1.5-pro"],
        index=0
    )
    st.markdown("---")
    st.header("📤 Upload Center")
    uploaded_file = st.file_uploader("Upload lecture photo", type=["jpg", "jpeg", "png", "webp"])
    process_btn = st.button("Generate & Prepare PDF 🚀", type="primary", use_container_width=True)

# Main Title & Subtitle
st.title("🎓 JUIT Smart Research Assistant")
st.caption("AI-Powered Lecture Note Extraction & Engineering Document Generator")

# 6. Processing Logic
if uploaded_file and process_btn:
    if not api_key or "YOUR_ACTUAL" in api_key or api_key == "AQ...":
        st.error("🔑 **API Key Missing or Placeholder:** Please set a valid Gemini API key in your `.env` file or Streamlit Cloud Secrets.\n\n"
                 "👉 **Fix:** Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey) and add it to `GEMINI_API_KEY`.")
    else:
        col1, col2 = st.columns([1, 1])
        image = Image.open(uploaded_file)
        
        with col1:
            st.subheader("📷 Source Image")
            st.image(image, caption=uploaded_file.name, use_container_width=True)

        with col2:
            st.subheader("📝 AI-Generated Academic Notes")
            with st.spinner("Analyzing image and generating study notes..."):
                try:
                    # Initialize client with backend API key
                    client = genai.Client(api_key=api_key)
                    
                    prompt = (
                        "Analyze this image and create comprehensive, well-structured academic engineering study notes. "
                        "Include summary, key formulas/concepts (use LaTeX for math: $$ or $), diagrams breakdown, "
                        "and code blocks where applicable. Format nicely with Markdown headings and bullet points."
                    )
                    
                    response, used_model = generate_with_fallback(client, image, prompt, selected_model)
                    
                    notes_text = response.text
                    st.caption(f"✨ Generated using `{used_model}`")
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
                        st.error("🔑 **Authentication Failed:** The provided Gemini API Key is invalid or rejected by Google.\n\n"
                                 "👉 **Fix:** Update `GEMINI_API_KEY` with a valid key from [Google AI Studio](https://aistudio.google.com/app/apikey).")
                    elif "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                        st.error("⏳ **Rate Limit Exceeded:** Free tier quota reached. Please wait 1 minute before retrying.")
                    elif "503" in err_msg or "high demand" in err_msg.lower() or "UNAVAILABLE" in err_msg:
                        st.error("⚠️ **Server at Capacity:** Google's AI servers are currently busy. Please retry in a few moments.")
                    else:
                        st.error(f"🔍 **Note:** An unexpected issue occurred: {err_msg}")
elif not uploaded_file and process_btn:
    st.warning("⚠️ Please upload a lecture photo in the sidebar first.")
