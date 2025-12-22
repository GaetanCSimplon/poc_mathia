# Fichier: logic/adaptive_engine.py
from mistralai import Mistral
import json
import os
from data.pedagogy_registry import ERROR_LIST_FOR_PROMPT, PEDAGOGY_DB
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def analyze_student_error(user_input, correct_result, history):
    """
    Identifie l'ID de l'erreur dans notre base de données.
    """
    
    # Prompt de classification
    # On lui donne la liste des erreurs possibles (ERROR_LIST_FOR_PROMPT)
    analysis_prompt = f"""
    Tu es un expert en diagnostic pédagogique primaire (Cycle 3).
    
    CONTEXTE :
    - Élève : "{user_input}"
    - Réponse attendue (Calculée) : {correct_result}
    
    BASE DE DONNÉES DES ERREURS CONNUES :
    {ERROR_LIST_FOR_PROMPT}
    - AUTRE: Erreur non listée ou pas d'erreur.

    TA MISSION :
    Identifie si l'élève commet une des erreurs listées ci-dessus.
    Si l'élève a bon, réponds "AUCUNE".
    
    Réponds UNIQUEMENT au format JSON :
    {{
        "error_id": "CODE_DE_L_ERREUR_OU_AUTRE",
        "justification": "Courte explication"
    }}
    """
    
    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        error_id = result.get("error_id", "UNKNOWN")
        
        # Sécurité : Si l'ID n'existe pas, on renvoie UNKNOWN
        if error_id not in PEDAGOGY_DB and error_id != "AUCUNE":
             return PEDAGOGY_DB["UNKNOWN"]
        
        if error_id == "AUCUNE":
            return None
            
        # On récupère la donnée riche depuis notre fichier Python
        return PEDAGOGY_DB[error_id]

    except Exception as e:
        print(f"Erreur diagnostic : {e}")
        return None