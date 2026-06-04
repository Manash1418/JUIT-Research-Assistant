import streamlit as st
from fpdf import FPDF
from dotenv import load_dotenv
from google import genai
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="JUIT AI Note Engine", layout="wide")
st.title("🎓 JUIT Smart Research Assistant")

# 2. PDF Generation Function

# 2. PDF Generation Function
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    
    # Header for JUIT Branding
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(200, 10, txt="JUIT Academic Intelligence Hub", ln=True, align='C')
    pdf.ln(10)
    
    # Multiline text for notes
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, txt=text)
    
    # NEW FIX: Use a buffer to store the PDF in memory
    pdf_buffer = io.BytesIO()
    # Write the PDF data into the buffer
    pdf_buffer.write(pdf.output()) 
    # Move to the start of the buffer so Streamlit can read it
    pdf_buffer.seek(0) 
    
    return pdf_buffer

# 3. Load API and UI
load_dotenv()
client = genai.Client()

with st.sidebar:
    st.header("Upload Center")
    uploaded_file = st.file_uploader("Upload lecture photo", type=["jpg", "png"])
    process_btn = st.button("Generate & Prepare PDF 🚀")

if uploaded_file and process_btn:
    col1, col2 = st.columns(2)
    image = Image.open(uploaded_file)
    
    with col1:
        st.image(image, caption="Source Image", use_container_width=True)

    with col2:
    st.subheader("AI-Generated Academic Notes")
    with st.spinner("Analyzing engineering data..."):
        try:
            # 1. The original AI Request
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    image, 
                    "Analyze this image and create structured engineering study notes. "
                    "Use LaTeX for math and C code blocks for any code snippets."
                ]
            )
            
            # 2. Display the Notes if successful
            notes_text = response.text
            st.markdown(notes_text)
            
            # 3. Provide the PDF Download
            pdf_output = create_pdf(notes_text)
            st.download_button(
                label="📥 Download Professional PDF",
                data=pdf_output,
                file_name="JUIT_Study_Notes.pdf",
                mime="application/pdf"
            )

        # 4. The Smart Evaluator Fix: Catch the "Server Busy" (503) error
        except Exception as e:
            if "503" in str(e) or "high demand" in str(e).lower():
                st.error("⚠️ **Server at Capacity:** Google's AI is currently experiencing high demand. "
                         "Please wait a moment and click the button again.")
            else:
                # Catch any other unexpected issues
                st.warning(f"🔍 **Note:** An unexpected issue occurred. Technical details: {str(e)}")