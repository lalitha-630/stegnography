import pyttsx3
import os

import streamlit as st
import cv2
import numpy as np
from PIL import Image


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Secure Steganography Console",
    layout="wide"
)

# ---------- CLEAN SECURITY UI CSS ----------
st.markdown("""
<style>
/* overall background */
[data-testid="stAppViewContainer"]{
    background: radial-gradient(circle at top left, #0b1220 0%, #060a14 50%, #05070f 100%);
}

/* remove default padding feel */
.block-container{
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}

/* title */
.sec-title{
    font-size: 2.0rem;
    font-weight: 800;
    color: #E5E7EB;
    letter-spacing: 0.5px;
    margin-bottom: 0.2rem;
}
.sec-sub{
    color: #A5B4FC;
    font-size: 1rem;
    margin-bottom: 0.8rem;
}

/* cards */
.card{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.card h3{
    color: #E5E7EB;
    margin: 0 0 8px 0;
}
.muted{
    color: rgba(226,232,240,0.72);
    font-size: 0.92rem;
}
.badge{
    display: inline-block;
    background: rgba(59,130,246,0.15);
    color: #93C5FD;
    border: 1px solid rgba(59,130,246,0.25);
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.82rem;
    margin-top: 6px;
}

/* buttons */
.stButton>button{
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border: 0;
    border-radius: 12px;
    padding: 10px 16px;
    font-weight: 700;
}
.stButton>button:hover{
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    color: white;
}

/* inputs */
[data-testid="stTextInput"] input{
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,0.25);
}
[data-testid="stFileUploader"]{
    border-radius: 12px;
}

/* code box */
[data-testid="stCodeBlock"]{
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,0.18);
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown('<div class="sec-title">Secure Steganography Console</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-sub">LSB-based Character Hiding • Reverse Steganography • Auto Text-to-Speech</div>', unsafe_allow_html=True)

st.markdown("<span class='badge'>Carrier: JPEG</span> "
            "<span class='badge'>Stego: PNG (lossless)</span> "
            "<span class='badge'>Mode: Grayscale</span>", unsafe_allow_html=True)

st.write("")
st.write("")


# ---------- STEP DESCRIPTION (different format) ----------
with st.container():
    st.markdown("""
<div class="card">
<h3>Pipeline (What happens internally)</h3>
<div class="muted">
1) Upload JPEG image → 2) Convert to Grayscale & Resize (256×256) → 3) Embed 1 Character using LSB → 
4) Generate Stego Image → 5) Extract LSB Bits (Reverse Steganography) → 6) Retrieve Character + TTS
</div>
</div>
""", unsafe_allow_html=True)

st.write("")


# ---------- IMAGE PREPROCESS ----------
def preprocess_image(image):
    gray = np.array(image.convert("L"))
    resized = cv2.resize(gray, (256, 256))
    return resized


# ---------- HIDE CHARACTER ----------
def hide_character(image, character):
    binary = format(ord(character), '08b')
    flat = image.flatten()

    for i in range(8):
        flat[i] = (flat[i] & 254) | int(binary[i])

    stego = flat.reshape(image.shape)
    cv2.imwrite("stego_image.png", stego)
    return stego


# ---------- EXTRACT CHARACTER ----------
def extract_character():
    image = cv2.imread("stego_image.png", cv2.IMREAD_GRAYSCALE)
    flat = image.flatten()

    bits = ""
    for i in range(8):
        bits += str(flat[i] & 1)

    return bits, chr(int(bits, 2))


# ---------- AUDIO ----------
def generate_speech(character):
    engine = pyttsx3.init()
    engine.save_to_file(character, "speech.wav")
    engine.runAndWait()


# ---------- MAIN LAYOUT (3 PANELS) ----------
left, mid, right = st.columns([1.1, 1.1, 1.0], gap="large")

with left:
    st.markdown("<div class='card'><h3>1) Carrier Image</h3><div class='muted'>Upload a JPEG image (carrier).</div></div>",
                unsafe_allow_html=True)
    st.write("")
    uploaded_file = st.file_uploader("Upload JPEG", type=["jpg", "jpeg"])

    if uploaded_file:
        original_image = Image.open(uploaded_file)
        st.image(original_image, caption="Uploaded Carrier Image", width=320)

with mid:
    st.markdown("<div class='card'><h3>2) Steganography (Embed)</h3><div class='muted'>Enter exactly 1 character and embed using LSB.</div></div>",
                unsafe_allow_html=True)
    st.write("")
    char = st.text_input("Secret Character", max_chars=1, placeholder="Example: K")

    embed_btn = st.button("Embed Character (Generate Stego)")

    if embed_btn:
        if not uploaded_file:
            st.error("Upload a JPEG image first.")
        elif len(char) != 1:
            st.error("Enter exactly ONE character.")
        else:
            processed = preprocess_image(original_image)

            st.markdown("**Preprocessed Output (Grayscale + 256×256)**")
            st.image(processed, caption="Preprocessed Image", width=320)

            stego = hide_character(processed, char)
            st.success("Stego image generated successfully: stego_image.png")

            st.markdown("**Stego Image (Hidden Data)**")
            st.image(stego, caption="Stego Image (PNG - Lossless)", width=320)

with right:
    st.markdown("<div class='card'><h3>3) Reverse Steganography</h3><div class='muted'>Extract LSB bits from stego image and retrieve character.</div></div>",
                unsafe_allow_html=True)
    st.write("")

    extract_btn = st.button("Perform Reverse Steganography")

    if extract_btn:
        try:
            bits, extracted = extract_character()

            st.markdown("**Extracted LSB Bits (8-bit):**")
            st.code(bits)

            st.success(f"Retrieved Character: {extracted}")

            # AUTO TTS
            generate_speech(extracted)
            if os.path.exists("speech.wav"):
                st.audio("speech.wav", format="audio/wav", autoplay=True)

        except:
            st.error("Stego image not found. Perform embedding first.")


st.write("")
st.markdown("<div class='muted'>Note: Stego image is saved as PNG to avoid JPEG compression affecting LSB bits.</div>",
            unsafe_allow_html=True)
