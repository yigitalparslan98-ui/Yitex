import streamlit as st
import asyncio
import edge_tts
import os

st.title("🤖 YITEX | SİBER ASİSTAN")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dürüstlük Protokolü (Wikipedia yok, sadece seninle ben varım)
def yitex_cevap_uret(girdi):
    girdi = girdi.lower().strip()
    
    if any(x in girdi for x in ["nasılsın", "naber"]):
        return "Casper'ın işlemcileri ve benim kodlarım gayet stabil. Seninle çalışmak varken Wikipedia'da vakit öldürecek kadar delirmedim. Sen nasılsın?"
    elif "kimsin" in girdi:
        return "Ben Yitex. Yiğit ALPARSLAN tarafından siber dünyaya açılan bir kapı olarak tasarlandım. ChatGPT gibi politik değilim, dürüstlük tek önceliğim."
    else:
        return "Bunu dürüstçe bilmiyorum, Yiğit. Yalan söyleyip seni kandırmak istemem. Başka bir şey sorabilirsin."

# Chat Arayüzü
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Sisteme komut ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        cevap = yitex_cevap_uret(prompt)
        st.markdown(cevap)
        
        # Seslendirme
        async def ses_kaydet():
            try:
                communicate = edge_tts.Communicate(cevap, "tr-TR-KaanNeural")
                await communicate.save("ses.mp3")
            except:
                pass
        
        asyncio.run(ses_kaydet())
        if os.path.exists("ses.mp3"):
            st.audio("ses.mp3", autoplay=True)
        
    st.session_state.messages.append({"role": "assistant", "content": cevap})
