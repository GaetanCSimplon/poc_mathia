import os
import time
from dotenv import load_dotenv

# Import des modules
from audio.stt_azure import AzureSTT
from audio.tts_azure import AzureTTS
from logic.llm_engine import get_ai_response

# Chargement env
load_dotenv()

def main():
    print("\n--- 🎓 MathIA : Interface Hybride (Texte & Voix) ---")
    print("Instructions :")
    print("1. Pour écrire : Tape ton message et valide.")
    print("2. Pour parler : Appuie simplement sur [ENTRÉE] pour activer le micro.")
    print("------------------------------------------------------------")

    # Initialisation
    try:
        ear = AzureSTT()
        mouth = AzureTTS()
        history = [] 
    except Exception as e:
        print(f" Erreur d'initialisation : {e}")
        return

    while True:
        try:
            # --- 1. CHOIX DU CANAL D'ENTRÉE ---
            user_input_text = input("\nToi (✍️  ou [Entrée] pour 🎤) : ").strip()

            # --- CAS A : MODE VOCAL (L'utilisateur a juste appuyé sur Entrée) ---
            if not user_input_text:
                print("J'écoute... (Parle maintenant)")
                
                # On active le STT
                user_message = ear.listen()
                
                if not user_message:
                    print("Ø (Aucun son détecté)")
                    continue
                
                print(f"🗣️  Transcrit : {user_message}")
                mode_vocal_actif = True # On marque que l'échange est vocal

            # --- CAS B : MODE TEXTUEL (L'utilisateur a écrit quelque chose) ---
            else:
                user_message = user_input_text
                mode_vocal_actif = False # On marque que l'échange est textuel

            # --- 2. GESTION DE SORTIE (Arrêt) ---
            if any(mot in user_message.lower() for mot in ["stop", "quitter", "exit", "au revoir"]):
                msg_fin = "Au revoir ! Reviens vite faire des maths."
                print(f"🤖 MathIA : {msg_fin}")
                if mode_vocal_actif:
                    mouth.speak(msg_fin)
                break

            # --- 3. CERVEAU (LLM) ---
            print("🧠 ...")
            
            # C'est ici que la magie opère : 
            # Si on vient du micro (mode_vocal_actif=True) -> Prompt Audio (Pas de LaTeX, réponse courte)
            # Si on vient du clavier (mode_vocal_actif=False) -> Prompt Texte (LaTeX, formatage riche)
            ai_response = get_ai_response(
                user_message=user_message, 
                conversation_history=history,
                is_voice_mode=mode_vocal_actif 
            )

            # --- 4. RESTITUTION (OUTPUT) ---
            
            # Dans tous les cas, on affiche la réponse (pour garder une trace écrite)
            print(f"🤖 MathIA : {ai_response}")

            # Si le mode vocal était actif, on active AUSSI la synthèse vocale
            if mode_vocal_actif:
                mouth.speak(ai_response)
            

            # --- 5. MÉMOIRE ---
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": ai_response})

        except KeyboardInterrupt:
            print("\nArrêt du programme.")
            break
        except Exception as e:
            print(f"⚠️ Erreur : {e}")

if __name__ == "__main__":
    main()