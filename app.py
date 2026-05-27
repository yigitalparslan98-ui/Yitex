import streamlit as st
import asyncio
import edge_tts
import os
from playwright.async_api import async_playwright

st.title("YITEX OS | SİBER ARAŞTIRMACI")

# Hafıza Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mozilla Motoru ile Araştırma
async def moz_ara(query):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(f"https://www.google.com/search?q={query}")
            # Google sonuçlarını çek (Başlık ve özet)
            results = await page.evaluate("""
                Array.from(document.querySelectorAll('h3, .VwiC3b')).map(e => e.innerText).slice(0, 4)
            """)
            await browser.close()
            return "\n".join(results)
        except Exception as e:
            await browser.close()
            return "Araştırma sırasında siber bir engel oluştu."

# Sidebar Hafızası
with st.sidebar:
    st.header("Siber Günlük")
    for msg in st.session_state.messages:
        st.write(f"- {msg['content'][:30]}...")
    if st.button("Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()

# Ana Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Yitex'e ne soralım?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mozilla motoru tarıyor..."):
            sonuc = asyncio.run(moz_ara(prompt))
            
            # Dürüstlük Protokolü: Sonuç boşsa dürüst ol.
            if not sonuc or len(sonuc) < 10:
                cevap = "Bunu web üzerinde dürüstçe bulamadım Yiğit. Yalan söyleyip seni kandıramam."
            else:
                cevap = f"Araştırmalarım sonucunda ulaştığım veriler:\n\n{sonuc}"
            
            st.write(cevap)
            
            # Sesli Yanıt (Hata Korumalı)
            async def ses_kaydet(metin):
                try:
                    communicate = edge_tts.Communicate(metin, "tr-TR-KaanNeural")
                    await communicate.save("temp.mp3")
                    return True
                except:
                    return False
            
            if asyncio.run(ses_kaydet(cevap)):
                st.audio("temp.mp3", format="audio/mp3", autoplay=True)
                
        st.session_state.messages.append({"role": "assistant", "content": cevap})
