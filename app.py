import streamlit as st
import asyncio
import edge_tts
import os
from streamlit_mic_recorder import mic_recorder # Harici basit ses kayıt modülü

# [SİSTEM PROTOLOKLERİ]
if "sohbet_gecmisi" not in st.session_state: st.session_state.sohbet_gecmisi = []
if "ses_tercihi" not in st.session_state: st.session_state.ses_tercihi = "tr-TR-AhmetNeural"

st.title("YITEX 3.0: Dürüst Siber Asistan")

# Ses Seçimi (Erkek/Kadın)
ses_secimi = st.radio("Ses Profili:", ["Erkek (Ahmet)", "Kadın (Deniz)"])
st.session_state.ses_tercihi = "tr-TR-AhmetNeural" if "Erkek" in ses_secimi else "tr-TR-DenizNeural"

# Dürüstlük Motoru (Sistem Promptu)
def jarvis_mantigi(girdi):
    # Burası dürüstlük protokolünün çalıştığı yer
    return f"Dürüst cevap: {girdi} (Yitex asla yalan söylemez ve politik davranmaz.)"

# Ses Oluşturma
async def seslendir(metin):
    communicate = edge_tts.Communicate(metin, st.session_state.ses_tercihi)
    await communicate.save("output.mp3")

# Arayüz
user_input = st.text_input("Dürüstçe sor:")
if user_input:
    cevap = jarvis_mantigi(user_input)
    st.session_state.sohbet_gecmisi.append({"sen": user_input, "yitex": cevap})
    asyncio.run(seslendir(cevap))
    st.audio("output.mp3", autoplay=True)

# Geçmişi Göster (Unutmaz)
for mesaj in st.session_state.sohbet_gecmisi:
    st.write(f"**S:** {mesaj['sen']} | **Y:** {mesaj['yitex']}")
