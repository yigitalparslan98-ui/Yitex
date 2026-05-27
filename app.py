import streamlit as st
import asyncio
import os
from playwright.async_api import async_playwright

# [SİSTEM BAŞLATICI - Firefox'u sunucuya kurar]
if not os.path.exists("firefox_installed.txt"):
    os.system("playwright install firefox")
    with open("firefox_installed.txt", "w") as f: f.write("installed")

# [PRO ARAYÜZ (CSS)]
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0b0e14 0%, #1a1f2e 100%); color: #00f2ff; font-family: 'Inter', sans-serif; }
    .stChatFloatingInputContainer { background: #0b0e14; border-top: 1px solid #00f2ff; }
    .stChatMessage { border-radius: 15px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 242, 255, 0.2); }
    h1 { color: #00f2ff; text-transform: uppercase; letter-spacing: 2px; }
    .css-1544g2n { color: #00f2ff !important; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ YITEX | PRO-OS")
st.subheader("Siber Araştırmacı v6.0")

# [SİSTEM DURUMU]
col1, col2 = st.columns(2)
with col1: st.metric("Motor", "Mozilla Gecko")
with col2: st.metric("Durum", "Aktif")

if "messages" not in st.session_state: st.session_state.messages = []

# [ARAŞTIRMA MOTORU]
async def moz_ara(query):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.google.com/search?q={query}")
        # Daha geniş veri çekme
        results = await page.evaluate("Array.from(document.querySelectorAll('h3, .VwiC3b')).map(e => e.innerText).slice(0, 5)")
        await browser.close()
        return "\n\n".join(results)

# [CHAT MANTIĞI]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Siber vizör aktif... Bir komut gir."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mozilla motoru derin tarama yapıyor..."):
            sonuc = asyncio.run(moz_ara(prompt))
            
            # Pro Yanıt Düzeni
            if not sonuc:
                cevap = "Sistem dürüst: Bu konuda web üzerinde somut bir veri bulamadım."
            else:
                cevap = f"**Siber Tarama Sonucu:**\n\n{sonuc}"
            
            st.write(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

# Sidebar Pro-Settings
with st.sidebar:
    st.title("SİSTEM KONTROL")
    if st.button("Hafızayı Temizle"):
        st.session_state.messages = []
        st.rerun()
