import os
import azure.cognitiveservices.speech as speechsdk

class AzureTTS:
    def __init__(self):
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = os.getenv("AZURE_SPEECH_REGION")
        
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Voix française neurale
        speech_config.speech_synthesis_voice_name = "fr-FR-DeniseNeural" 
        
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    def speak(self, text):
        """Joue le texte sur les haut-parleurs"""
        print("MathIA parle...")
        result = self.synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.Canceled:
            details = result.cancellation_details
            print(f"Annulation : {details.reason}")
            if details.error_details:
                print(f"Détails de l'erreur : {details.error_details}")
        
