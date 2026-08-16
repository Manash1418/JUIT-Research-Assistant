# 🎓 JUIT Smart Research Assistant

> **AI-Powered Academic Intelligence & Lecture Note Extraction Hub**

JUIT Smart Research Assistant transforms lecture photos, handwritten notes, and engineering diagrams into beautifully structured academic study notes and downloadable PDFs using Google Gemini Vision AI.

---

## ✨ Features

- 📷 **Vision AI Extraction:** Convert board photos, handwritten notes, and textbook pages into structured text.
- 📐 **LaTeX Math Support:** Automatically formats mathematical formulas and equations ($...$ and $$...$$).
- 💻 **Syntax Highlighted Code:** Formats code snippets in C, C++, Python, and more.
- 📥 **PDF Export:** Download professional academic study PDFs with one click.
- ⚡ **Streamlit Web Application & CLI:** Run as an interactive web UI or terminal automation script.

---

## 🛠️ Tech Stack

- **Frontend / Web UI:** [Streamlit](https://streamlit.io/)
- **AI Model:** [Google Gemini API](https://ai.google.dev/) (`google-genai` SDK, `gemini-2.0-flash`)
- **PDF Generation:** `fpdf2`
- **Image Processing:** `Pillow`
- **Environment Management:** `python-dotenv`

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Manash1418/JUIT-Research-Assistant.git
cd JUIT-Research-Assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your Gemini API Key
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Run the Web Application
```bash
streamlit run web_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🖥️ CLI Usage

You can also run the note extraction script directly from the terminal:
```bash
python app.py
```
The generated notes will be saved automatically to `generated_notes.md`.

---

## ☁️ Deployment on Streamlit Cloud

1. Push your repository to GitHub.
2. Connect your repo on [Streamlit Community Cloud](https://share.streamlit.io/).
3. Set your main file path to `web_app.py`.
4. In **App Settings ➔ Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

---

## 📜 License

MIT License © [Manash Harsh](https://github.com/Manash1418)
