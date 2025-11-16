"""
Script pour enrichir error_taxonomy.json avec feedback_templates
Ajoute des templates de feedback pédagogiques à chaque erreur
"""

import json
from pathlib import Path
from typing import Dict, List, Any


# Templates de feedback par type de misconception
FEEDBACK_TEMPLATES = {
    # Addition
    "retenue": [
        "Attention à la retenue! Quand {a} + {b} = {sum}, et que {sum} ≥ 10, on doit reporter {carry} dizaine(s).",
        "Tu as oublié de reporter la retenue. Regarde: {a} + {b} = {correct}, pas {wrong}.",
        "Bravo pour le calcul, mais n'oublie pas: quand la somme des unités dépasse 10, on reporte une dizaine!"
    ],
    "commutativité": [
        "Super observation! En addition, l'ordre ne change pas le résultat: {a} + {b} = {b} + {a} = {result}.",
        "Tu peux vérifier: que tu fasses {a} + {b} ou {b} + {a}, tu trouveras toujours {result}!"
    ],
    "concept_addition": [
        "L'addition, c'est comme rassembler des objets. Si tu as {a} billes et qu'on t'en donne {b}, combien en as-tu?",
        "Essaie avec des cubes: prends {a} cubes, puis ajoutes-en {b}. Compte le total!"
    ],

    # Soustraction
    "emprunt": [
        "Pour soustraire {b} de {a}, tu dois emprunter une dizaine. {a} devient {a_transformed}, puis tu fais {calc}.",
        "Tu ne peux pas faire {digit_a} - {digit_b} ? Pas de problème! Emprunte 10 à la dizaine suivante.",
        "L'emprunt, c'est comme échanger un billet de 10€ contre 10 pièces de 1€. Essaie!"
    ],
    "ordre_soustraction": [
        "Attention! Dans la soustraction, l'ordre compte: {a} - {b} ≠ {b} - {a}.",
        "Tu dois toujours soustraire le plus petit du plus grand nombre (dans ta colonne)."
    ],

    # Multiplication
    "tables": [
        "Révise ta table de {n}: {n} × {m} = {result}, pas {wrong}.",
        "Astuce: {n} × {m}, c'est {n} groupes de {m}. Compte: {visualization}.",
        "Tu confonds avec une autre table? {n} × {m} = {correct}, mais {n} × {wrong_m} = {wrong}."
    ],
    "concept_multiplication": [
        "La multiplication, c'est une addition répétée: {a} × {b} = {a} + {a} + ... ({b} fois).",
        "Imagine {b} groupes de {a} objets. Combien d'objets en tout?",
        "C'est différent de l'addition! {a} × {b} = {result}, mais {a} + {b} = {sum}."
    ],
    "multiplication_par_0": [
        "Tout nombre multiplié par 0 donne 0! Si tu as 0 groupe de {n}, tu as {result} objets.",
        "{n} × 0 = 0, car tu n'as aucun groupe de {n}."
    ],

    # Division
    "concept_division": [
        "La division, c'est partager équitablement. {a} ÷ {b} = combien chacun reçoit si on partage {a} entre {b}?",
        "Pense à la division comme une soustraction répétée: combien de fois peux-tu retirer {b} de {a}?"
    ],
    "reste": [
        "Quand {a} ÷ {b}, il reste {r}. C'est normal! {b} × {q} = {product}, et {product} + {r} = {a}.",
        "Le reste ({r}) doit toujours être plus petit que le diviseur ({b})."
    ],

    # Fractions
    "fractions_addition": [
        "Pour additionner {a}/{b} + {c}/{d}, tu dois d'abord trouver un dénominateur commun!",
        "Ne pas additionner numérateurs et dénominateurs séparément! {a}/{b} + {c}/{d} ≠ {wrong_num}/{wrong_den}.",
        "Transforme en fractions équivalentes: {a}/{b} = {new_a}/{common}, {c}/{d} = {new_c}/{common}, puis additionne!"
    ],
    "fractions_equivalentes": [
        "{a}/{b} et {c}/{d} sont équivalentes! Multiplie ou divise numérateur ET dénominateur par le même nombre.",
        "Visualise: {a}/{b} représente la même portion que {c}/{d}. Dessine pour voir!"
    ],
    "fractions_comparaison": [
        "Pour comparer {a}/{b} et {c}/{d}, regarde la taille des parts, pas les nombres!",
        "Plus le dénominateur est grand, plus les parts sont PETITES. Donc 1/{big} < 1/{small}."
    ],

    # Décimaux
    "virgule_position": [
        "La virgule sépare les unités des dixièmes. Dans {number}, le chiffre {digit} est en position {position}.",
        "Aligne toujours les virgules en colonne quand tu additionnes ou soustrais!",
        "Dans {a} + {b}, place bien les virgules: {visualization}."
    ],
    "decimaux_comparaison": [
        "Pour comparer {a} et {b}, regarde chiffre par chiffre de gauche à droite.",
        "Plus de chiffres après la virgule ne signifie pas plus grand! {longer} < {shorter}."
    ],

    # Géométrie
    "perimetre_aire": [
        "Le périmètre mesure le TOUR de la figure, l'aire mesure la SURFACE.",
        "Périmètre de rectangle: {formula_p}. Aire: {formula_a}. Ce sont deux choses différentes!",
        "Tu confonds? Le périmètre c'est en {unit}, l'aire en {unit}²."
    ],
    "angles": [
        "Un angle ne dépend pas de la longueur des côtés, mais de leur écartement!",
        "Utilise ton rapporteur: place le centre sur le sommet, aligne le 0 sur un côté."
    ],

    # Mesures
    "conversions": [
        "Pour convertir {value} {from_unit} en {to_unit}: {operation}.",
        "Souviens-toi: 1 {big_unit} = {factor} {small_unit}.",
        "Tableau de conversion: {visualization}."
    ],

    # Générique
    "calcul_mental": [
        "Vérifie ton calcul: {a} {op} {b} = {correct}, pas {wrong}.",
        "Astuce: décompose {a} {op} {b} = ({decomp_a}) {op} ({decomp_b}) = {result}.",
        "Prends ton temps pour bien calculer!"
    ],
    "attention": [
        "Relis ton énoncé attentivement! On te demande {question}.",
        "Tu as fait une petite erreur d'inattention. La bonne réponse est {correct}.",
        "Bravo pour ta méthode! Juste une petite erreur de calcul: {correction}."
    ]
}


def generate_feedback_template(error_def: Dict[str, Any]) -> List[str]:
    """Génère des templates de feedback pour une erreur donnée"""

    error_id = error_def.get("id", "")
    misconception = error_def.get("misconception", "").lower()
    domain = extract_domain_from_id(error_id)

    templates = []

    # Sélectionner templates appropriés selon le type d'erreur
    if "retenue" in misconception and "addition" in domain:
        templates.extend(FEEDBACK_TEMPLATES["retenue"])
    elif "emprunt" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["emprunt"])
    elif "commuta" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["commutativité"])
    elif "multipli" in misconception and "addition" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["concept_multiplication"])
    elif "table" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["tables"])
    elif "fraction" in misconception and ("addition" in misconception or "additionne" in misconception):
        templates.extend(FEEDBACK_TEMPLATES["fractions_addition"])
    elif "équivalent" in misconception or "équival" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["fractions_equivalentes"])
    elif "virgule" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["virgule_position"])
    elif "périmètre" in misconception or "aire" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["perimetre_aire"])
    elif "conversion" in misconception or "unité" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["conversions"])
    elif "reste" in misconception and "division" in domain:
        templates.extend(FEEDBACK_TEMPLATES["reste"])
    elif "division" in misconception:
        templates.extend(FEEDBACK_TEMPLATES["concept_division"])
    elif "ordre" in misconception and "soustraction" in domain:
        templates.extend(FEEDBACK_TEMPLATES["ordre_soustraction"])
    elif error_id.startswith("CALC"):
        templates.extend(FEEDBACK_TEMPLATES["calcul_mental"])
        templates.extend(FEEDBACK_TEMPLATES["attention"])
    else:
        # Templates génériques basés sur le type
        if error_id.startswith("ADD"):
            templates.extend(FEEDBACK_TEMPLATES.get("concept_addition", []))
        elif error_id.startswith("MULT"):
            templates.extend(FEEDBACK_TEMPLATES.get("concept_multiplication", []))

        # Ajouter template générique
        templates.append(
            f"Tu as fait une erreur liée à: {misconception}. Revoyons ensemble ce concept!"
        )
        templates.append(
            "Pas de souci! Cette erreur est fréquente. Pratiquons ensemble."
        )

    # Ajouter template d'encouragement
    templates.append("Continue! Tu progresses bien. N'hésite pas à me demander de l'aide.")

    # Limiter à 3-5 templates par erreur
    return templates[:5] if len(templates) > 5 else templates


def extract_domain_from_id(error_id: str) -> str:
    """Extrait le domaine depuis l'ID d'erreur"""
    if error_id.startswith("ADD"):
        return "addition"
    elif error_id.startswith("SUB"):
        return "subtraction"
    elif error_id.startswith("MULT"):
        return "multiplication"
    elif error_id.startswith("DIV"):
        return "division"
    elif error_id.startswith("FRAC"):
        return "fractions"
    elif error_id.startswith("DEC"):
        return "decimals"
    elif error_id.startswith("GEO"):
        return "geometry"
    elif error_id.startswith("MEAS"):
        return "measurement"
    elif error_id.startswith("CALC"):
        return "calculation"
    return "unknown"


def generate_remediation_path(error_def: Dict[str, Any]) -> str:
    """Génère un chemin de remédiation pour l'erreur"""

    error_id = error_def.get("id", "")
    domain = extract_domain_from_id(error_id)
    misconception = error_def.get("misconception", "").lower()

    # Mapping vers chemins de remédiation
    remediation_paths = {
        "ADD_CONC": "addition_concepts_fundamentals",
        "ADD_PROC": "addition_procedure_practice",
        "SUB_CONC": "subtraction_concepts_fundamentals",
        "SUB_PROC": "subtraction_procedure_practice",
        "MULT_CONC": "multiplication_concepts_fundamentals",
        "MULT_PROC": "multiplication_procedure_practice",
        "DIV_CONC": "division_concepts_fundamentals",
        "DIV_PROC": "division_procedure_practice",
        "FRAC_CONC": "fractions_concepts_fundamentals",
        "FRAC_PROC": "fractions_operations_practice",
        "DEC_CONC": "decimals_concepts_fundamentals",
        "DEC_PROC": "decimals_operations_practice",
        "GEO_CONC": "geometry_concepts_fundamentals",
        "MEAS_CONC": "measurement_concepts_fundamentals",
        "CALC": "calculation_skills_practice"
    }

    # Trouver la clé correspondante
    for key, path in remediation_paths.items():
        if error_id.startswith(key):
            return path

    # Spécifiques
    if "retenue" in misconception:
        return "addition_with_carry_basics"
    elif "emprunt" in misconception:
        return "subtraction_with_borrowing_basics"
    elif "table" in misconception:
        return "multiplication_tables_mastery"

    return f"{domain}_review_basics"


def enrich_error_catalog(catalog: Dict[str, Any]) -> Dict[str, Any]:
    """Enrichit tout le catalogue avec feedback_templates et remediation_path"""

    enriched_count = 0

    for category_name, category_data in catalog.get("error_categories", {}).items():
        if "errors" not in category_data:
            continue

        for domain, errors_list in category_data["errors"].items():
            for error_def in errors_list:
                # Ajouter feedback_templates
                if "feedback_templates" not in error_def:
                    error_def["feedback_templates"] = generate_feedback_template(error_def)
                    enriched_count += 1

                # Ajouter remediation_path
                if "remediation_path" not in error_def:
                    error_def["remediation_path"] = generate_remediation_path(error_def)

    print(f"✅ Enrichi {enriched_count} erreurs avec feedback_templates et remediation_path")
    return catalog


def main():
    """Point d'entrée principal"""

    # Chemins
    project_root = Path(__file__).parent.parent
    taxonomy_path = project_root / "data" / "error_taxonomy.json"
    backup_path = project_root / "data" / "error_taxonomy.backup.json"

    print(f"📂 Chargement de {taxonomy_path}")

    # Charger catalogue actuel
    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Backup
    print(f"💾 Création backup: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    # Enrichir
    print("🔧 Enrichissement du catalogue...")
    enriched_catalog = enrich_error_catalog(catalog)

    # Mettre à jour metadata
    enriched_catalog["metadata"]["last_updated"] = "2025-11-15"
    enriched_catalog["metadata"]["enrichment_version"] = "6.4.1"

    # Sauvegarder
    print(f"💾 Sauvegarde catalogue enrichi: {taxonomy_path}")
    with open(taxonomy_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_catalog, f, indent=2, ensure_ascii=False)

    # Validation
    print("✅ Validation du JSON...")
    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        json.load(f)  # Juste pour vérifier que c'est valide

    print("\n🎉 Enrichissement terminé avec succès!")
    print(f"📊 Total erreurs: {enriched_catalog['metadata']['total_errors_cataloged']}")
    print(f"📝 Version: {enriched_catalog['metadata'].get('enrichment_version', 'N/A')}")


if __name__ == "__main__":
    main()
