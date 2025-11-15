"""
Exercise Generator - Générateur d'exercices MathCopain
Centralise toute la logique de génération d'exercices
"""

import random
from datetime import date
from typing import Dict, Any, Optional, Tuple


# =============== EXERCICES DE BASE ===============

def generer_addition(niveau: str) -> Dict[str, Any]:
    """
    Génère exercice d'addition selon niveau.

    Args:
        niveau: CE1, CE2, CM1, ou CM2

    Returns:
        Dict avec 'question' et 'reponse'
    """
    if niveau == "CE1":
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif niveau == "CE2":
        a, b = random.randint(10, 50), random.randint(10, 50)
    elif niveau == "CM1":
        a, b = random.randint(50, 100), random.randint(50, 100)
    else:  # CM2
        a, b = random.randint(100, 200), random.randint(100, 200)

    return {
        'question': f"{a} + {b}",
        'reponse': a + b
    }


def generer_soustraction(niveau: str) -> Dict[str, Any]:
    """
    Génère exercice de soustraction selon niveau.

    Args:
        niveau: CE1, CE2, CM1, ou CM2

    Returns:
        Dict avec 'question' et 'reponse'
    """
    if niveau == "CE1":
        a, b = random.randint(10, 20), random.randint(1, 10)
    elif niveau == "CE2":
        a, b = random.randint(50, 100), random.randint(10, 50)
    elif niveau == "CM1":
        a, b = random.randint(100, 500), random.randint(50, 100)
    else:  # CM2
        a, b = random.randint(500, 1000), random.randint(100, 500)

    return {
        'question': f"{a} - {b}",
        'reponse': a - b
    }


def generer_tables(niveau: str) -> Dict[str, Any]:
    """
    Génère exercice de multiplication (tables) selon niveau.

    Args:
        niveau: CE1, CE2, CM1, ou CM2

    Returns:
        Dict avec 'question' et 'reponse'
    """
    if niveau == "CE1":
        table, mult = random.randint(2, 5), random.randint(1, 10)
    elif niveau == "CE2":
        table, mult = random.randint(2, 9), random.randint(1, 10)
    elif niveau == "CM1":
        table, mult = random.randint(1, 12), random.randint(1, 12)
    else:  # CM2
        table, mult = random.randint(1, 15), random.randint(1, 15)

    return {
        'question': f"{table} × {mult}",
        'reponse': table * mult
    }


def generer_division(niveau: str) -> Dict[str, Any]:
    """
    Génère exercice de division selon niveau.

    Args:
        niveau: CE1, CE2, CM1, ou CM2

    Returns:
        Dict avec 'question', 'reponse', et 'reste'
    """
    if niveau == "CE1":
        # CE1 : pas encore de divisions, fallback sur tables
        return generer_tables(niveau)

    elif niveau == "CE2":
        # CE2 : divisions simples (quotient exact)
        quotient = random.randint(2, 9)
        diviseur = random.randint(2, 5)
        dividende = quotient * diviseur

    elif niveau == "CM1":
        # CM1 : divisions plus grandes, avec ou sans reste
        if random.random() < 0.7:  # 70% sans reste
            quotient = random.randint(3, 12)
            diviseur = random.randint(2, 9)
            dividende = quotient * diviseur
        else:  # 30% avec reste
            diviseur = random.randint(3, 7)
            quotient = random.randint(3, 9)
            reste = random.randint(1, diviseur - 1)
            dividende = (quotient * diviseur) + reste

    else:  # CM2
        # CM2 : divisions complexes, souvent avec reste
        if random.random() < 0.5:  # 50% sans reste
            quotient = random.randint(5, 15)
            diviseur = random.randint(3, 12)
            dividende = quotient * diviseur
        else:  # 50% avec reste
            diviseur = random.randint(4, 9)
            quotient = random.randint(4, 12)
            reste = random.randint(1, diviseur - 1)
            dividende = (quotient * diviseur) + reste

    return {
        'question': f"{dividende} ÷ {diviseur}",
        'reponse': dividende // diviseur,
        'reste': dividende % diviseur
    }


# =============== EXERCICES AVANCÉS ===============

def generer_probleme(niveau: str) -> Dict[str, Any]:
    """
    Génère problème mathématique contextuel.

    Args:
        niveau: CE1, CE2, CM1, ou CM2

    Returns:
        Dict avec 'question' et 'reponse'
    """
    contextes = [
        ("Marie a {a} billes. Son ami lui en donne {b}.", "Combien a-t-elle ?", "addition"),
        ("Théo a {a} euros. Il achète quelque chose qui coûte {b} euros.", "Combien lui reste-t-il ?", "soustraction"),
        ("Il y a {a} rangées de {b} chaises.", "Combien de chaises en tout ?", "multiplication"),
        ("On partage {a} bonbons entre {b} enfants.", "Combien chacun a ?", "division")
    ]

    contexte_base, question, operation = random.choice(contextes)

    # Paramètres selon niveau: (a_min, a_max, b_min, b_max)
    params = {
        'CE1': (5, 20, 2, 10),
        'CE2': (20, 50, 5, 30),
        'CM1': (50, 200, 10, 50)
    }
    a1, a2, b1, b2 = params.get(niveau, (100, 500, 20, 100))

    a, b = random.randint(a1, a2), random.randint(b1, b2)
    contexte = contexte_base.format(a=a, b=b)

    # Calculer réponse selon opération
    if operation == "addition":
        reponse = a + b
    elif operation == "soustraction":
        if a < b:
            a, b = b, a  # Assurer résultat positif
        reponse = a - b
    elif operation == "multiplication":
        reponse = a * b
    else:  # division
        reponse = a // b if b > 0 else 0

    return {
        'question': f"{contexte} {question}",
        'reponse': reponse
    }


def generer_droite_numerique(niveau: str) -> Dict[str, Any]:
    """
    Génère exercice de droite numérique (estimation).

    Args:
        niveau: CE1, CE2, CM1, ou CM2

    Returns:
        Dict avec 'nombre', 'min', 'max'
    """
    max_val = {
        "CE1": 100,
        "CE2": 1000,
        "CM1": 10000
    }.get(niveau, 100000)

    nombre = random.randint(0, max_val)

    return {
        'nombre': nombre,
        'min': 0,
        'max': max_val
    }


def calculer_score_droite(reponse: int, correct: int) -> Tuple[int, str]:
    """
    Calcule score pour exercice droite numérique selon distance.

    Args:
        reponse: Réponse utilisateur
        correct: Réponse correcte

    Returns:
        Tuple (points, message)
    """
    distance = abs(reponse - correct)
    max_val = correct if correct > 0 else 100

    if distance <= max_val * 0.10:
        return 20, "Excellent ! (±10%)"
    elif distance <= max_val * 0.20:
        return 5, "Presque ! (±20%)"
    else:
        return 0, f"Trop loin (distance: {distance})"


def generer_memory_emoji(niveau: str) -> Dict[str, Any]:
    """
    Génère jeu de memory avec emojis.

    Args:
        niveau: CE1, CE2, CM1, ou CM2

    Returns:
        Dict avec 'cards', 'revealed', 'matched'
    """
    emojis = [
        '🍎', '🐶', '🎨', '🌟', '🎭', '🎸',
        '🚀', '🏆', '🎮', '🍕', '🐱', '⚽',
        '🎪', '🎯', '🌈', '🍦'
    ]

    # Nombre de paires selon niveau
    if niveau == "CE1":
        paires = emojis[:4]
    elif niveau == "CE2":
        paires = emojis[:6]
    elif niveau == "CM1":
        paires = emojis[:8]
    else:  # CM2
        paires = emojis[:10]

    # Dupliquer et mélanger
    cards = paires + paires
    random.shuffle(cards)

    return {
        'cards': cards,
        'revealed': set(),
        'matched': set()
    }


def generer_daily_challenge() -> Dict[str, Any]:
    """
    Génère défi du jour (même défi pour tous le même jour).

    Returns:
        Dict avec 'type', 'objectif', 'text'
    """
    today = str(date.today())

    # Seed avec date pour avoir même défi chaque jour
    random.seed(today)

    challenges = [
        {
            'type': 'addition',
            'objectif': 5,
            'text': 'Enchaîne 5 bonnes réponses en Addition'
        },
        {
            'type': 'soustraction',
            'objectif': 5,
            'text': 'Enchaîne 5 bonnes réponses en Soustraction'
        },
        {
            'type': 'tables',
            'objectif': 5,
            'text': 'Enchaîne 5 bonnes réponses aux Tables'
        },
        {
            'type': 'droite',
            'objectif': 3,
            'text': 'Fais 3 bonnes estimations à la Droite'
        }
    ]

    challenge = random.choice(challenges)

    # Reset seed pour ne pas affecter autres générations
    random.seed()

    return challenge


# =============== EXPLICATIONS PÉDAGOGIQUES ===============

def generer_explication(
    exercice_type: str,
    question: str,
    reponse_utilisateur: Any,
    reponse_correcte: Any
) -> str:
    """
    Génère explication pédagogique selon type d'exercice et erreur.

    Args:
        exercice_type: Type exercice (addition, soustraction, multiplication, division)
        question: Question posée (ex: "5 + 3")
        reponse_utilisateur: Réponse donnée par utilisateur
        reponse_correcte: Réponse correcte

    Returns:
        Texte markdown avec explication détaillée
    """
    if exercice_type == "addition":
        return _expliquer_addition(question, reponse_correcte)
    elif exercice_type == "soustraction":
        return _expliquer_soustraction(question, reponse_correcte)
    elif exercice_type == "multiplication":
        return _expliquer_multiplication(question, reponse_correcte)
    elif exercice_type == "division":
        return _expliquer_division(question, reponse_correcte)
    else:
        return "Regarde bien le calcul et réessaye!"


def _expliquer_addition(question: str, reponse_correcte: int) -> str:
    """Explication pédagogique pour addition."""
    a, b = map(int, question.replace(" ", "").split("+"))

    # Décomposition par dizaines
    if a >= 10 or b >= 10:
        dizaine_a = (a // 10) * 10
        unite_a = a % 10
        dizaine_b = (b // 10) * 10
        unite_b = b % 10

        explication = f"""
💡 **Décomposons ensemble:**

{a} = {dizaine_a} + {unite_a}
{b} = {dizaine_b} + {unite_b}

**Étape 1:** Additionne les dizaines
→ {dizaine_a} + {dizaine_b} = {dizaine_a + dizaine_b}

**Étape 2:** Additionne les unités
→ {unite_a} + {unite_b} = {unite_a + unite_b}

**Étape 3:** Somme finale
→ {dizaine_a + dizaine_b} + {unite_a + unite_b} = **{reponse_correcte}**
"""
    else:
        # Méthode des bonds
        explication = f"""
💡 **Méthode des bonds:**

Commence à {a}
→ Fais un bond de {b}
→ Tu arrives à **{reponse_correcte}**

Ou autrement: {a} + {b//2} = {a + b//2}, puis +{b - b//2} = **{reponse_correcte}**
"""

    # Astuce selon difficulté
    if b == 9:
        astuce = f"✨ **Astuce:** Pour +9, fais +10 puis -1 → {a}+10={a+10}, puis -1={reponse_correcte}"
    elif b == 8:
        astuce = f"✨ **Astuce:** Pour +8, fais +10 puis -2 → {a}+10={a+10}, puis -2={reponse_correcte}"
    else:
        astuce = ""

    return explication + "\n" + astuce


def _expliquer_soustraction(question: str, reponse_correcte: int) -> str:
    """Explication pédagogique pour soustraction."""
    a, b = map(int, question.replace(" ", "").split("-"))

    # Vérifier si retenue
    if a % 10 < b % 10:
        explication = f"""
💡 **Soustraction avec retenue:**

{a} - {b} = ?

**Problème:** On ne peut pas enlever {b % 10} de {a % 10}

**Solution:**
1. Emprunte une dizaine
2. {a} devient {(a//10 - 1)*10 + 10 + a%10}
3. Maintenant: {10 + a%10} - {b%10} = {10 + a%10 - b%10}
4. Puis: {(a//10 - 1)*10} - {(b//10)*10} = {(a//10 - 1)*10 - (b//10)*10}
5. Total: **{reponse_correcte}**
"""
    else:
        explication = f"""
💡 **Soustraction simple:**

{a} - {b} = ?

Enlève les dizaines: {(a//10)*10} - {(b//10)*10} = {(a//10 - b//10)*10}
Enlève les unités: {a%10} - {b%10} = {a%10 - b%10}
Résultat: **{reponse_correcte}**
"""

    return explication


def _expliquer_multiplication(question: str, reponse_correcte: int) -> str:
    """Explication pédagogique pour multiplication."""
    table, mult = map(int, question.replace(" ", "").replace("×", " ").split())

    # Stratégies selon multiplication
    strategies = []

    # Stratégie 1: Doubler
    if mult % 2 == 0:
        demi = mult // 2
        strategies.append(
            f"**Méthode 1 (Doubler):**\n"
            f"{table}×{demi} = {table*demi}\n"
            f"Double: {table*demi}×2 = **{reponse_correcte}**"
        )

    # Stratégie 2: Par 10
    if mult <= 10:
        strategies.append(
            f"**Méthode 2 (Par 10):**\n"
            f"{table}×10 = {table*10}\n"
            f"Enlève {table}×{10-mult}: {table*10} - {table*(10-mult)} = **{reponse_correcte}**"
        )

    # Stratégie 3: Décomposer
    if mult >= 6:
        strategies.append(
            f"**Méthode 3 (Décomposer):**\n"
            f"{table}×5 = {table*5}\n"
            f"{table}×{mult-5} = {table*(mult-5)}\n"
            f"Somme: {table*5} + {table*(mult-5)} = **{reponse_correcte}**"
        )

    explication = f"💡 **Plusieurs façons de calculer {table}×{mult}:**\n\n"
    explication += "\n\n".join(strategies)
    explication += f"\n\n✨ **Choisis la méthode qui te semble la plus facile!**"

    return explication


def _expliquer_division(question: str, reponse_correcte: int) -> str:
    """Explication pédagogique pour division."""
    try:
        dividende, diviseur = map(int, question.replace(" ", "").replace("÷", " ").split())
    except:
        return "Regarde bien le calcul et réessaye!"

    quotient = dividende // diviseur
    reste = dividende % diviseur

    explication = f"""
💡 **Division : {dividende} ÷ {diviseur}**

**Méthode 1 : Par les tables**
Cherche dans la table de {diviseur} :
"""

    # Afficher table de référence
    table_ref = []
    for i in range(1, 13):
        resultat = diviseur * i
        if resultat <= dividende + diviseur:
            if resultat == dividende:
                table_ref.append(f"✅ {diviseur} × {i} = {resultat} ← C'est ça!")
            elif resultat < dividende:
                table_ref.append(f"{diviseur} × {i} = {resultat}")
            else:
                table_ref.append(f"⚠️ {diviseur} × {i} = {resultat} (trop grand)")
                break

    explication += "\n" + "\n".join(table_ref)

    if reste > 0:
        explication += f"""

**Attention : Il y a un reste!**
{dividende} = ({diviseur} × {quotient}) + {reste}

Donc : **{dividende} ÷ {diviseur} = {quotient} reste {reste}**
"""
    else:
        explication += f"""

**Résultat exact : {dividende} ÷ {diviseur} = {quotient}**
"""

    explication += """

✨ **Astuce :** Pour vérifier, multiplie le quotient par le diviseur!
"""

    return explication
