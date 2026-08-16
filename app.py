import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load environment variables from the .env file
load_dotenv()

def generate_study_notes(image_path, user_prompt):
    # Initialize the client (it automatically picks up GEMINI_API_KEY from environment)
    client = genai.Client()
    
    # Open the image using Pillow
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: Could not find the image at '{image_path}'. Make sure you added it to the folder!")
        return None

    print("Processing image and generating structured notes... Please wait.")

    # Call the multimodal model
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[
            img, 
            user_prompt
        ]
    )
    
    return response.text

if __name__ == "__main__":
    # Specify the test image name
    sample_image = "sample.jpg" 
    
    # Define the core generation prompt
    prompt = (
        "Analyze this engineering resource image. Convert any handwritten notes, formulas, "
        "or diagrams into clean, highly structured student study notes. "
        "Use appropriate Markdown headings, bullet points, and wrap any mathematical equations "
        "in standard LaTeX notation (use $ for inline and $$ for block equations). "
        "If there is code, wrap it in clean, syntax-highlighted C code blocks."
    )
    
    # Run the pipeline
    notes = generate_study_notes(sample_image, prompt)
    
    if notes:
        # Save the result into a Markdown file
        with open("generated_notes.md", "w", encoding="utf-8") as f:
            f.write(notes)
        print("\nSuccess! Your notes have been saved to 'generated_notes.md'.")