# stegnography
# 🔐 Secure Image Steganography (LSB) + Reverse Steganography + TTS

A Streamlit-based security application that hides a **single character** inside a **grayscale JPEG image** using **LSB (Least Significant Bit) steganography**, generates a **stego image**, and then performs **reverse steganography** to retrieve the hidden character.  
The extracted character is also converted into **speech (Text-to-Speech)**.

---

## ✅ Features
- Upload/select a **JPEG image**
- Automatically converts image to:
  - **Grayscale**
  - **Standard size (128 × 128)**
- Hide **one character** using **LSB steganography**
- Generates **Stego image**
- Performs **Reverse steganography** to extract the hidden character
- Converts extracted character into **speech (TTS)**
- Clean, security-themed UI with step-by-step flow

---

## 🧠 Technique Used
**LSB (Least Significant Bit) Steganography**
- Character → ASCII → 8-bit binary
- 8 bits are embedded into the LSB of the first 8 pixels
- Reverse steganography extracts those bits back to the original character

---

## 📂 Project Structure
Image_Steganography/
│
├── app.py
├── stego_image.png # generated after embedding
├── speech.wav # generated during extraction (TTS)
│
└── .streamlit/
└── config.toml # dark theme settings
