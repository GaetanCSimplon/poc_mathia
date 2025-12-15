import re

def clean_expression(expression: str) -> str:
    """
    Nettoie l'expression mathématique pour éviter les injections de code.
    Isolation des éléments minimaux: chiffres et opérateurs.
    """
    
    allowed_chars = r"[^0-9+\-*/().\s]"
    cleaned = re.sub(allowed_chars, "", expression)
    return cleaned

def calculate(expression: str) -> str:
    """Evalue une expression mathématique simple.
    Retourn le résultat sous forme de chaine de caractères ou un message d'erreur.
    

    Args:
        expression (str): expression à évaluer.

    Returns:
        str: Résultat de l'opération.
    """
    try:
        safe_expression = clean_expression(expression)
        if not safe_expression.strip():
            return "Erreur : Aucune expression mathématique valide détectée."
        result = eval(safe_expression)
        
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except ZeroDivisionError:
        return "Erreur: Impossible de diviser par zéro."
    except SyntaxError:
        return "Erreur: Syntaxe de calcul incorrecte."
    except Exception as e:
        return f"Erreur de calcul : {str(e)}"

# Test

if __name__ == "__main__":
    print("Test 1 :", calculate("12 + 5"))
    print("Test 2 (Complexe):", calculate("(10 * 3) / 2"))
    print("Test 3 (Sécurité):", calculate("import os; os.system('hack')"))