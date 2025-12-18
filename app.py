import streamlit as st
from logic.llm_engine import get_ai_response
from audio.stt_azure import AzureSTT
from audio.tts_azure import AzureTTS

# 1. Configuration de la page
st.set_page_config(page_title="MathIA POC", page_icon="🦉", layout="centered")

# --- CSS POUR LE BOUTON FLOTTANT ---
# Cela va fixer le bouton en bas à droite, juste au-dessus de la zone de saisie
st.markdown("""
    <style>
    /* Cibler le bouton à l'intérieur de la div stButton */
    div.stButton > button {
        position: fixed;
        bottom: 80px; /* Ajusté pour être juste au-dessus du chat_input */
        right: 30px;
        z-index: 999; /* Pour être sûr qu'il soit au-dessus du texte */
        border-radius: 50%; /* Le rendre rond */
        height: 60px;
        width: 60px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        background-color: #FF4B4B; /* Couleur rouge Streamlit (optionnel) */
        color: white;
        font-size: 24px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #FF2B2B; /* Couleur au survol */
    }
    </style>
""", unsafe_allow_html=True)

st.title("🦉 MathIA")

# Chargement Audio
@st.cache_resource
def load_audio_modules():
    try:
        ear = AzureSTT()
        mouth = AzureTTS()
        return ear, mouth
    except Exception as e:
        st.error(f"Erreur Audio : {e}")
        return None, None

ear, mouth = load_audio_modules()

# Gestion Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- LE BOUTON MICRO  ---
if st.button("🎙️"): 
    if ear and mouth:
        # On utilise un conteneur vide pour afficher le statut "J'écoute" en haut
        status_placeholder = st.empty()
        with status_placeholder.container():
            st.info("👂 J'écoute... Parle maintenant !")
            
            # A. Écoute
            user_audio_text = ear.listen()
        
        # On efface le message "J'écoute" une fois fini
        status_placeholder.empty()

        if user_audio_text:
            st.session_state.messages.append({"role": "user", "content": user_audio_text})
            
            with st.spinner("Je réfléchis (Audio)..."):
                try:
                    response_text = get_ai_response(
                        user_audio_text, 
                        conversation_history=st.session_state.messages[:-1],
                        is_voice_mode=True 
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    mouth.speak(response_text)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur IA : {e}")
        else:
            st.warning("Je n'ai rien entendu.")

# --- AFFICHAGE DE L'HISTORIQUE ---

for message in st.session_state.messages:
    avatar = "🧑‍🎓" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- ZONE DE TEXTE ---
if prompt := st.chat_input("Écris ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Je réfléchis..."):
            response_text = get_ai_response(
                prompt, 
                conversation_history=st.session_state.messages[:-1],
                is_voice_mode=False 
            )
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})