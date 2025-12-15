# Fichier: app.py
import streamlit as st
from logic.llm_engine import get_ai_response

# 1. Configuration de la page
st.set_page_config(
    page_title="MathIA POC",
    page_icon="🦉",
    layout="centered"
)

st.title("🦉 MathIA")
st.caption("Ton assistant pédagogique pour les maths (CM1/CM2)")

# 2. Gestion de la Mémoire (Session State)
# On vérifie si l'historique existe, sinon on le crée.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Affichage de l'historique
# À chaque rechargement de page, on ré-affiche tout ce qui a été dit.
for message in st.session_state.messages:
    # On distingue l'affichage User (🧑‍🎓) et Assistant (🤖)
    avatar = "🧑‍🎓" if message["role"] == "user" else "🤖"
    
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 4. Zone de saisie utilisateur
# st.chat_input affiche la barre de texte en bas.
if prompt := st.chat_input("Pose ta question de maths ici..."):
    
    # A. On affiche tout de suite le message de l'utilisateur
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
    
    # B. On ajoute ce message à la mémoire
    st.session_state.messages.append({"role": "user", "content": prompt})

    # C. On fait appel à l'IA (Cerveau)
    # On affiche un petit spinner pendant que ça réfléchit
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Je réfléchis..."):
            try:
                # Appel à notre fonction logique (en lui passant l'historique)
                response_text = get_ai_response(
                    prompt, 
                    conversation_history=st.session_state.messages[:-1] # On exclut le tout dernier message qu'on vient d'ajouter pour éviter les doublons dans l'envoi
                )
                st.markdown(response_text)
                
                # D. On ajoute la réponse de l'IA à la mémoire
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Oups, une erreur est survenue : {e}")