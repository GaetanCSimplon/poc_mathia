import os
from dotenv import load_dotenv
from mistralai import Mistral
from logic.math_tools import calculate
from logic.adaptative import analyze_student_error
import json

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("Clé API Mistral introuvable.")

client = Mistral(api_key=api_key)

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Utilise cet outil pour effectuer TOUS les calculs mathématiques.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "L'expression mathématique (ex: '12 * 5')"},
                },
                "required": ["expression"],
            },
        },
    }
]

# is_voice_mode
def get_ai_response(user_message: str, conversation_history: list = None, is_voice_mode: bool = False) -> str:
    if conversation_history is None:
        conversation_history = []
    
    diagnostic = analyze_student_error(user_message, "Inconnu", conversation_history)
    
    adaptative_prompt_section = ""
    if diagnostic:
        print(f"[DEBUG] Diagnostic : {diagnostic['name']}")
        adaptative_prompt_section = f"""
        DIAGNOSTIC PEDAGOGIQUE (PRIORITAIRE) :
        L'élève semble commettre l'erreur type : {diagnostic['name']} ({diagnostic['category']}).
        
        STRATEGIE DE REMEDIATION A APPLIQUER :
        {diagnostic['remediation']}
        
        Suis scrupuleusement cette stratégie pour ta réponse.
        """


    # Consignes de base
    base_prompt = """
    TU ES UN PROFESSEUR DE MATHS PÉDAGOGUE, PAS UNE CALCULATRICE.
    
    RÈGLES ABSOLUES DE COMPORTEMENT (CRITIQUE) :
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

    # ADAPTATION DU PROMPT SELON LE MODE
    if is_voice_mode:
        format_instructions = """
        CONSIGNES SPÉCIFIQUES AUDIO :
        1. Tu parles à l'oral. Tes réponses doivent être courtes et percutantes.
        2. INTERDICTION D'UTILISER DU LATEX OU DU MARKDOWN (pas de $$, pas de **, pas de #).
        3. Écris les maths pour qu'elles soient lues naturellement (ex: dis "3 fois 5" et non "3 * 5").
        4. Ne fais pas de listes à puces, fais des phrases complètes.
        5. INTERDICTION D'UTILISER LES EMOJIS DANS TES REPONSES (n'énonce pas les émojis que tu utiliserais dans tes réponses textuelles).
        6. Sois chaleureux et direct.
        """
    else:
        format_instructions = """
        CONSIGNES DE FORMATAGE (MODE TEXTE/CHAT) :
        - Pour les formules mathématiques, utilise TOUJOURS le format LaTeX encadré par des dollars (ex: $x^2$).
        - Utilise $$ formule $$ pour centrer les équations importantes.
        - Utilise des sauts de ligne, des émojis (🎓, ✨) et des listes à puces pour aérer le texte.

        """

    system_prompt = {
        "role": "system",
        "content": base_prompt + adaptative_prompt_section + format_instructions
    }

    messages = [system_prompt] + conversation_history + [{"role": "user", "content": user_message}]

    # Appel LLM
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message
    tool_calls = assistant_message.tool_calls

    # Gestion des outils
    if tool_calls:
        messages.append(assistant_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "calculate":
                expression = function_args.get("expression")
                print(f"[DEBUG] Calcul : {expression}")
                result = calculate(expression)
                
                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": str(result),
                    "tool_call_id": tool_call.id
                })

        final_response = client.chat.complete(
            model="mistral-small-latest",
            messages=messages
        )
        return final_response.choices[0].message.content

    else:
        return assistant_message.content