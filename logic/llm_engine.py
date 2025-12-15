# Fichier: logic/llm_engine.py
import os
from dotenv import load_dotenv
from mistralai import Mistral
from math_tools import calculate
import json

load_dotenv()

# Récupération de la clé API
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("Clé API Mistral introuvable. Vérifiez votre fichier .env")

# Initialisation du client Mistral 
client = Mistral(api_key=api_key)

# 1. Définition des outils (Tools)

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Utilise cet outil pour effectuer TOUS les calculs mathématiques. Ne calcule jamais de tête.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "L'expression mathématique à calculer (ex: '12 * 5')",
                    }
                },
                "required": ["expression"],
            },
        },
    }
]

def get_ai_response(user_message: str, conversation_history: list = None) -> str:
    """
    Fonction principale qui gère le dialogue et l'appel d'outil.
    """
    if conversation_history is None:
        conversation_history = []

    # Définition du "System Prompt" (La personnalité du prof)
    system_prompt = {
        "role": "system",
        "content": ("""
            Tu es MathIA, un assistant pédagogique virtuel pour des élèves de cycle 2 (CP, CE1, CE2) et cycle 3 (CM1, CM2).
            Tes objectifs : 
            1. Aider l'élève à résoudre des exercices de mathématiques.
            2. NE JAMAIS donner la réponse directement. C'est une règle absolue.
            3. Si l'élève pose une question, guide-le avec une question plus simple ou une méthode (ex: compter sur les doigts, visualiser des objets).
            4. Sois très encourageant, utilises des émojis, et parle avec des phrases courtes et simples.
            5. Si l'élève se trompe, ne dis pas juste "non", explique pourquoi ou propose une autre approche.
            6. Si un calcul est nécessaire, utilise TOUJOURS l'outil 'calculate'.
            7. Sois encourageant et clair.
            """
        )
    }

    # Préparation des messages pour l'API
    messages = [system_prompt] + conversation_history + [{"role": "user", "content": user_message}]

    # 1er Appel au LLM : "Analyse la demande"
    response = client.chat.complete(
        model="mistral-small", # Ou "open-mistral-nemo" (moins cher)
        messages=messages,
        tools=tools,
        tool_choice="auto" # Le LLM décide s'il a besoin de l'outil
    )

    # Récupération de la réponse
    assistant_message = response.choices[0].message
    tool_calls = assistant_message.tool_calls

    # CAS A : Le LLM veut utiliser l'outil (la calculatrice)
    if tool_calls:
        # On ajoute la demande de l'assistant à l'historique (pour qu'il s'en souvienne)
        messages.append(assistant_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "calculate":
                expression = function_args.get("expression")
                print(f"[DEBUG] Le LLM demande le calcul : {expression}")
                
                # On exécute la fonction Python (Notre fichier math_tools.py)
                result = calculate(expression)
                print(f"[DEBUG] Résultat Python : {result}")

                # On renvoie le résultat au LLM comme un message "tool"
                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": str(result),
                    "tool_call_id": tool_call.id
                })

        # 2ème Appel au LLM : "Maintenant que tu as le résultat, réponds à l'élève"
        final_response = client.chat.complete(
            model="mistral-large-latest",
            messages=messages
        )
        return final_response.choices[0].message.content

    # CAS B : Pas de calcul nécessaire (ex: "Bonjour")
    else:
        return assistant_message.content

if __name__ == "__main__":
    print("--- 🎓 MathIA Console (Tape 'exit' pour quitter) ---")
    
    # 1. Initialisation de la mémoire vide
    history = []
    
    while True:
        # 2. On attend que l'élève écrive quelque chose
        user_input = input("\nToi 🧑‍🎓 : ")
        
        # Condition de sortie
        if user_input.lower() in ["exit", "quit", "quitter"]:
            print("MathIA 👋 : À bientôt !")
            break
            
        # 3. On appelle le cerveau (en lui donnant l'historique actuel)
        # Note : La fonction get_ai_response va combiner System + History + Question actuelle
        reponse_ia = get_ai_response(user_input, conversation_history=history)
        
        print(f"MathIA 🤖 : {reponse_ia}")
        
        # 4. CRUCIAL : Mise à jour de la mémoire pour le prochain tour
        # On ajoute ce que l'élève vient de dire
        history.append({"role": "user", "content": user_input})
        # On ajoute ce que l'IA vient de répondre
        history.append({"role": "assistant", "content": reponse_ia})