import os
from gtts import gTTS
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n"
    return text

def text_to_speech(text, output_filename):
    """Convert text to speech and save as MP3."""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_filename)
    print(f"✅ Audio saved as: {output_filename}")

def main():
    print("=== PDF to Audiobook Converter ===")
    pdf_path = input("Enter path to your PDF file: ").strip()

    if not os.path.exists(pdf_path):
        print("❌ File not found! Please check the path and try again.")
        return

    print("🔍 Extracting text from PDF...")
    extracted_text = extract_text_from_pdf(pdf_path)

    if not extracted_text.strip():
        print("❌ No readable text found in the PDF!")
        return

    output_filename = os.path.splitext(pdf_path)[0] + "_audiobook.mp3"

    print("🎧 Converting text to speech...")
    text_to_speech(extracted_text, output_filename)
    print("🎉 Conversion complete! Enjoy your audiobook.")

if __name__ == "__main__":
    main()
