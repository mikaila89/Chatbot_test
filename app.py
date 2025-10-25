import streamlit as st
import google.generativeai as genai
import pyttsx3
import tempfile
import threading
import time  # ✅ tambahkan ini untuk fungsi sleep

# === 1. KONFIGURASI GEMINI API ===
GEMINI_API_KEY = "AIzaSyBE9-DBPLH__WC2jrTJIb4jbWfTNb5lbMs"  # ganti dengan API key milikmu
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# === 2. KONFIGURASI SUARA (opsional di lokal) ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

# === 3. Fungsi TTS ===
def speak_text(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()

# === 4. Setup tampilan Streamlit ===
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

st.title("Chatbot Heru Arranuri, S.T")
st.caption("Ditenagai oleh Google Gemini API - versi Streamlit")

# === 5. Sidebar konfigurasi ===
with st.sidebar:
    st.header("⚙️ Pengaturan")
    voice_enabled = st.checkbox("Aktifkan suara (Text-to-Speech)", value=False)
    st.info("Ketik pertanyaan kamu di bawah lalu tekan ENTER untuk mengirim!")

# === 6. Tempat untuk menyimpan riwayat chat ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === 7. Input user ===
user_input = st.chat_input("Ketik pesan di sini...")

if user_input:
    # Tambahkan chat user ke riwayat
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Tampilkan segera di layar
    with st.chat_message("user"):
        st.markdown(user_input)

    # Proses ke Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = model.generate_content(user_input)
            reply = response.text.strip()
        except Exception as e:
            reply = f"[Error] {e}"

        # Efek “mengetik” per kata
        for word in reply.split():
            full_response += word + " "
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.05)  # ✅ ganti st.sleep jadi time.sleep
        message_placeholder.markdown(full_response)

        # Simpan ke riwayat
        st.session_state.chat_history.append({"role": "assistant", "text": full_response})

        # Jika suara diaktifkan
        if voice_enabled:
            speak_text(full_response)

# === 8. Tampilkan riwayat chat sebelumnya ===
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["text"])
