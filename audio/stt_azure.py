import azure.cognitiveservices.speech as speechsdk
import os

class AzureSTT:
    def __init__(self):
        # Récupération des variables d'environnement (ou mettre en dur pour tester)
        self.speech_key = os.environ.get("AZURE_SPEECH_KEY")
        self.service_region = os.environ.get("AZURE_SPEECH_REGION")

        if not self.speech_key or not self.service_region:
            raise ValueError("Clés Azure manquantes ! Vérifie tes variables d'environnement.")

        # Configuration du Speech Config
        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        
        # Important : Définir la langue en Français
        self.speech_config.speech_recognition_language = "fr-FR"

        # Configuration du micro
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        # Création du recognizer
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, 
            audio_config=self.audio_config
        )

    def listen(self):
        """
        Écoute une seule phrase (arrête automatiquement au silence).
        Retourne le texte reconnu ou None.
        """
        print("🎧 J'écoute (Azure)...")

        # recognize_once_async().get() est bloquant jusqu'à ce qu'une phrase soit finie
        result = self.speech_recognizer.recognize_once_async().get()

        # Gestion des résultats
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("String vide (bruit ou silence non reconnu).")
            return None
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f" Annulé : {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Erreur : {cancellation_details.error_details}")
            return None