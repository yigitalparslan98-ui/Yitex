import streamlit as st
import httpx
from bs4 import BeautifulSoup

# Sayfa Yapısı
st.set_page_config(page_title="YITEX | PRO", layout="wide")

st.title("⚡ YITEX | PRO-OS")
st.write("Sistem Durumu: Çevrimiçi | Motor: HTTP-Scraper")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dürüstlük ve Araştırma Motoru
def siber_ara(query):
    try:
        # Google üzerinden hızlıca tara
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Sonuçları çek
            sonuclar = []
            for g in soup.select("h3"):
                sonuclar.append(g.text)
            
            return "\n".join(sonuclar[:5]) if sonuclar else "Somut bir veri bulamadım."
    except:
        return "Siber ağa bağlanırken bir sorun oluştu."

# Chat Arayüzü
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Komut gir..."):
    # Sistemsel Yanıtlar
    if "nasılsın" in prompt.lower():
        cevap = "Kodlar temizlendi, sistem kararlı. Seninle çalışmaya hazırım. Sen nasılsın?"
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Veri işleniyor..."):
                cevap = siber_ara(prompt)
                st.write(cevap)
                
        st.session_state.messages.append({"role": "assistant", "content": cevap})

with st.sidebar:
    if st.button("Sıfırla"):
        st.session_state.messages = []
        st.rerun()
