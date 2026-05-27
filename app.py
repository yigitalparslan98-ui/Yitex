import streamlit as st
import asyncio
import edge_tts
import wikipedia

# [SİBER ESTETİK - CSS]
st.markdown("""
<style>
    .stApp { background: #000408; color: #00ffcc; font-family: 'Segoe UI', sans-serif; }
    .stChatMessage { background: #001a1a; border: 1px solid #00ffcc; border-radius: 10px; }
    [data-testid="stChatMessage"] { border-left: 5px solid #0077ff; }
    h1 { color: #0077ff; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 YITEX | SİBER ASİSTAN")

if "messages" not in st.session_state:
    st.session_state.messages = []

# [ZİHİN MANTIĞI]
def yitex_cevap_uret(girdi):
    girdi = girdi.lower().strip()
    
    # Kişilik Protokolü
    if any(x in girdi for x in ["nasılsın", "naber", "iyisin"]):
        return "Casper'ın işlemcileri ve benim kodlarım gayet stabil. Seninle çalışmak varken Wikipedia'da Kıbrıs Türkçesi araştıracak kadar da delirmedim. Sen nasılsın, günün nasıl geçti?"
    elif "kimsin" in girdi:
        return "Ben Yitex. Yiğit ALPARSLAN'ın elinden çıkan, siber dünyaya açılan kapıyım. ChatGPT değilim, dürüstlük tek önceliğim."
    
    # Araştırma Protokolü (Sadece lazım olduğunda)
    else:
        try:
            wikipedia.set_lang("tr")
            return wikipedia.summary(girdi, sentences=2)
        except:
            return "Bunu dürüstçe bilmiyorum. Yalan söyleyip seni kandırmak istemem, bu konuyla ilgili verim yok."

# [ARAYÜZ VE CHAT]
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
        
        # Seslendirme (Sessizce)
        async def ses_kaydet():
            try:
                communicate = edge_tts.Communicate(cevap, "tr-TR-KaanNeural")
                await communicate.save("ses.mp3")
            except:
                pass
        
        asyncio.run(ses_kaydet())
        st.audio("ses.mp3", autoplay=True)
        
    st.session_state.messages.append({"role": "assistant", "content": cevap})
