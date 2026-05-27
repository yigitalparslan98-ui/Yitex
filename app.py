import streamlit as st
import edge_tts
import asyncio
import wikipedia
import os

# Wikipedia'dan dürüst veri çekme
def siber_arastirma(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "Bu konuyu veritabanımda veya web'de dürüstçe bulamadım."

st.title("YITEX - Dürüst Siber Asistan")

# Ses Seçimi
ses = st.selectbox("Ses Profili:", ["tr-TR-KaanNeural", "tr-TR-DenizNeural"])

user_input = st.text_input("Söyle bakalım:")

if st.button("Analiz Et"):
    # Önce dürüst analiz
    cevap = siber_arastirma(user_input)
    st.write(f"**Yitex:** {cevap}")
    
    # Seslendir
    asyncio.run(edge_tts.Communicate(cevap, ses).save("out.mp3"))
    st.audio("out.mp3", autoplay=True)
