import streamlit as st
import asyncio
import edge_tts
import os

# [ARAYÜZ TASARIMI - CSS İLE SİBER GÖRÜNÜM]
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { border: 1px solid #00ffcc; background: #1a1a1a; color: white; }
    h1 { color: #ff00ff; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("--- YITEX SİBER ARAYÜZ ---")

# [SES MOTORU - HATA KORUMALI]
async def ses_uret(metin, ses):
    try:
        communicate = edge_tts.Communicate(metin, ses)
        await communicate.save("out.mp3")
        return True
    except Exception as e:
        return False

# [ANA MANTIĞI]
user_input = st.text_input("Komut Gir:")
ses = st.selectbox("Ses:", ["tr-TR-KaanNeural", "tr-TR-DenizNeural"])

if st.button("Sistemi Çalıştır"):
    # Basit bir cevap (Wikipedia veya yerel)
    cevap = f"Sistem taraması tamamlandı. {user_input} hakkında: Kıbrıs Türkçesi, tarihsel bir kökene sahiptir."
    
    st.write(f"**Yitex:** {cevap}")
    
    with st.spinner("Ses verisi işleniyor..."):
        basarili = asyncio.run(ses_uret(cevap, ses))
        if basarili:
            st.audio("out.mp3", autoplay=True)
        else:
            st.warning("Ses motoru şu an cevap vermiyor, sadece metin modu aktif.")
