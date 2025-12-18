from audio.stt_azure import AzureSTT
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    ear = AzureSTT()
    
    print("--- Démarrage du système Vocal Azure ---")
    
    while True:
        try:
            # 1. Étape STT (Speech to Text)
            user_text = ear.listen()
            
            if user_text:
                print(f"👤 Tu as dit : {user_text}")

                # Commande pour quitter proprement
                if "arrête" in user_text.lower() or "stop" in user_text.lower():
                    print("👋 Arrêt du programme.")
                    break
                
                # 2. Étape TTS (Text to Speech) - Le mode Perroquet
                # Ici, on renvoie simplement ce qui a été entendu
                response_text = f"J'ai bien entendu : {user_text}"
                
                print(f"🤖 Système : {response_text}")
                # speak(response_text) # Décommente pour entendre la voix !

        except KeyboardInterrupt:
            print("\nArrêt forcé.")
            break

if __name__ == "__main__":
    main()