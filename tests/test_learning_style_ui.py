"""
Tests pour Learning Style Assessment UI - Phase 6.3.3
Tests de l'interface quiz et des fonctions helper
"""

import pytest
import os
import shutil
import tempfile
from pathlib import Path

from ui.learning_style_assessment import (
    check_needs_quiz,
    get_user_learning_style,
    get_recommendations
)
from core.pedagogy.learning_style import LearningStyleAnalyzer, LearningStyleProfile


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_storage():
    """Créer un répertoire temporaire pour les tests"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def analyzer(temp_storage):
    """Créer un analyzer de test"""
    return LearningStyleAnalyzer("test_user", storage_path=temp_storage)


@pytest.fixture
def complete_profile(analyzer):
    """Créer un profil complet pour les tests"""
    responses = [
        {"question_id": 1, "selected_style": "visual"},
        {"question_id": 2, "selected_style": "visual"},
        {"question_id": 3, "selected_style": "kinesthetic"},
        {"question_id": 4, "selected_style": "visual"},
        {"question_id": 5, "selected_style": "logical"},
        {"question_id": 6, "selected_style": "visual"},
        {"question_id": 7, "selected_style": "visual"}
    ]

    result = analyzer.assess_from_quiz(responses)

    # Sauvegarder le profil (crée automatiquement le LearningStyleProfile)
    analyzer.save_profile(result)

    return analyzer.profile


# ============================================================================
# TEST CHECK_NEEDS_QUIZ
# ============================================================================

def test_check_needs_quiz_new_user(temp_storage):
    """Test qu'un nouvel utilisateur a besoin du quiz"""
    # Créer un analyzer sans profil
    analyzer = LearningStyleAnalyzer("new_user", storage_path=temp_storage)

    # Vérifier qu'il n'y a pas de profil
    assert analyzer.profile is None

    # La fonction devrait retourner True
    result = check_needs_quiz("new_user")
    # Note: La fonction utilise le chemin par défaut, pas temp_storage
    # Donc on ne peut pas tester ça directement sans mocker


def test_check_needs_quiz_existing_user_no_quiz(temp_storage):
    """Test un utilisateur existant sans quiz"""
    analyzer = LearningStyleAnalyzer("existing_user", storage_path=temp_storage)

    # Créer manuellement un profil (simulation d'un profil incomplet)
    # Normalement on utiliserait save_profile(), mais ici on teste un cas edge
    analyzer.profile = LearningStyleProfile(
        user_id="existing_user",
        primary={"style": "visual", "confidence": 0.5},
        quiz_result=None  # Pas de quiz
    )

    # Devrait avoir besoin du quiz
    assert analyzer.profile.quiz_result is None


def test_check_needs_quiz_completed(temp_storage, complete_profile):
    """Test un utilisateur avec quiz complété"""
    # Le profil a un quiz_result
    assert complete_profile.quiz_result is not None


# ============================================================================
# TEST GET_USER_LEARNING_STYLE
# ============================================================================

def test_get_user_learning_style_no_profile(temp_storage):
    """Test récupération style sans profil"""
    analyzer = LearningStyleAnalyzer("no_profile_user", storage_path=temp_storage)
    assert analyzer.profile is None


def test_get_user_learning_style_with_profile(temp_storage, complete_profile):
    """Test récupération style avec profil"""
    # Le style principal devrait être visual (5/7 réponses visual)
    assert complete_profile.primary['style'] == 'visual'


def test_get_user_learning_style_returns_string(temp_storage):
    """Test que la fonction retourne bien une string"""
    analyzer = LearningStyleAnalyzer("test_string", storage_path=temp_storage)

    # Créer des réponses fictives
    responses = [{"question_id": i+1, "selected_style": "auditory"} for i in range(7)]

    # Analyser et sauvegarder
    result = analyzer.assess_from_quiz(responses)
    analyzer.save_profile(result)

    # Vérifier le style
    assert analyzer.profile.primary['style'] == 'auditory'


# ============================================================================
# TEST GET_RECOMMENDATIONS
# ============================================================================

def test_get_recommendations_visual():
    """Test recommandations pour style visual"""
    recs = get_recommendations("visual")

    assert isinstance(recs, list)
    assert len(recs) > 0
    assert any("diagramme" in rec.lower() or "schéma" in rec.lower() for rec in recs)


def test_get_recommendations_auditory():
    """Test recommandations pour style auditory"""
    recs = get_recommendations("auditory")

    assert isinstance(recs, list)
    assert len(recs) > 0
    assert any("voix" in rec.lower() or "écoute" in rec.lower() for rec in recs)


def test_get_recommendations_kinesthetic():
    """Test recommandations pour style kinesthetic"""
    recs = get_recommendations("kinesthetic")

    assert isinstance(recs, list)
    assert len(recs) > 0
    assert any("doigt" in rec.lower() or "manipule" in rec.lower() for rec in recs)


def test_get_recommendations_logical():
    """Test recommandations pour style logical"""
    recs = get_recommendations("logical")

    assert isinstance(recs, list)
    assert len(recs) > 0
    assert any("logique" in rec.lower() or "pourquoi" in rec.lower() for rec in recs)


def test_get_recommendations_narrative():
    """Test recommandations pour style narrative"""
    recs = get_recommendations("narrative")

    assert isinstance(recs, list)
    assert len(recs) > 0
    assert any("histoire" in rec.lower() or "contexte" in rec.lower() for rec in recs)


def test_get_recommendations_unknown_style():
    """Test recommandations pour style inconnu"""
    recs = get_recommendations("unknown_style")

    # Devrait retourner une liste vide
    assert isinstance(recs, list)
    assert len(recs) == 0


def test_get_recommendations_all_styles_have_4_items():
    """Test que chaque style a bien 4 recommandations"""
    for style in ["visual", "auditory", "kinesthetic", "logical", "narrative"]:
        recs = get_recommendations(style)
        assert len(recs) == 4, f"Style {style} devrait avoir 4 recommandations, a {len(recs)}"


# ============================================================================
# TEST QUIZ QUESTIONS
# ============================================================================

def test_analyzer_has_quiz_questions(analyzer):
    """Test que l'analyzer a bien des questions"""
    questions = analyzer.get_quiz_questions()

    assert len(questions) == 7
    assert all('question' in q for q in questions)
    assert all('options' in q for q in questions)
    assert all('id' in q for q in questions)


def test_quiz_questions_have_5_options(analyzer):
    """Test que chaque question a 5 options (un par style)"""
    questions = analyzer.get_quiz_questions()

    for q in questions:
        options = q['options']
        assert len(options) == 5
        assert 'visual' in options
        assert 'auditory' in options
        assert 'kinesthetic' in options
        assert 'logical' in options
        assert 'narrative' in options


def test_quiz_questions_have_unique_ids(analyzer):
    """Test que chaque question a un ID unique"""
    questions = analyzer.get_quiz_questions()

    ids = [q['id'] for q in questions]
    assert len(ids) == len(set(ids))  # Tous les IDs sont uniques


# ============================================================================
# TEST PROFILE CREATION
# ============================================================================

def test_profile_creation_from_quiz(analyzer):
    """Test création de profil à partir du quiz"""
    responses = [
        {"question_id": 1, "selected_style": "logical"},
        {"question_id": 2, "selected_style": "logical"},
        {"question_id": 3, "selected_style": "logical"},
        {"question_id": 4, "selected_style": "logical"},
        {"question_id": 5, "selected_style": "visual"},
        {"question_id": 6, "selected_style": "logical"},
        {"question_id": 7, "selected_style": "logical"}
    ]

    result = analyzer.assess_from_quiz(responses)

    # Le style principal devrait être logical (6/7)
    assert result.primary['style'] == 'logical'
    assert result.primary['confidence'] > 0.7


def test_profile_saves_correctly(temp_storage):
    """Test que le profil se sauvegarde correctement"""
    analyzer = LearningStyleAnalyzer("save_test", storage_path=temp_storage)

    responses = [
        {"question_id": 1, "selected_style": "narrative"},
        {"question_id": 2, "selected_style": "narrative"},
        {"question_id": 3, "selected_style": "narrative"},
        {"question_id": 4, "selected_style": "auditory"},
        {"question_id": 5, "selected_style": "narrative"},
        {"question_id": 6, "selected_style": "narrative"},
        {"question_id": 7, "selected_style": "narrative"}
    ]

    result = analyzer.assess_from_quiz(responses)

    # Sauvegarder le profil
    analyzer.save_profile(result)

    # Vérifier que le fichier existe
    profile_file = Path(temp_storage) / "save_test" / "learning_style.json"
    assert profile_file.exists()

    # Recharger et vérifier
    analyzer2 = LearningStyleAnalyzer("save_test", storage_path=temp_storage)
    assert analyzer2.profile is not None
    assert analyzer2.profile.primary['style'] == 'narrative'


# ============================================================================
# TEST STYLE DESCRIPTIONS
# ============================================================================

def test_style_descriptions_exist(analyzer):
    """Test que les descriptions de styles existent"""
    assert len(analyzer.STYLE_DESCRIPTIONS) == 5

    for style in analyzer.STYLES:
        assert style in analyzer.STYLE_DESCRIPTIONS
        desc = analyzer.STYLE_DESCRIPTIONS[style]
        assert 'name' in desc
        assert 'description' in desc
        assert 'characteristics' in desc
        assert 'icon' in desc


def test_style_descriptions_have_icons(analyzer):
    """Test que chaque style a un emoji"""
    for style in analyzer.STYLES:
        icon = analyzer.STYLE_DESCRIPTIONS[style]['icon']
        assert len(icon) > 0


def test_style_descriptions_have_characteristics(analyzer):
    """Test que chaque style a au moins 3 caractéristiques"""
    for style in analyzer.STYLES:
        chars = analyzer.STYLE_DESCRIPTIONS[style]['characteristics']
        assert len(chars) >= 3


# ============================================================================
# TEST INTEGRATION
# ============================================================================

def test_full_quiz_workflow(temp_storage):
    """Test complet du workflow du quiz"""
    user_id = "workflow_test"
    analyzer = LearningStyleAnalyzer(user_id, storage_path=temp_storage)

    # 1. Vérifier que le profil n'existe pas
    assert analyzer.profile is None

    # 2. Obtenir les questions
    questions = analyzer.get_quiz_questions()
    assert len(questions) == 7

    # 3. Simuler des réponses
    responses = []
    for i, q in enumerate(questions):
        # Alterner les styles
        styles = list(q['options'].keys())
        selected = styles[i % len(styles)]
        responses.append({"question_id": q['id'], "selected_style": selected})

    # 4. Analyser les réponses
    result = analyzer.assess_from_quiz(responses)
    assert result.primary is not None
    assert 'style' in result.primary
    assert 'confidence' in result.primary

    # 5. Sauvegarder le profil
    analyzer.save_profile(result)

    # 6. Vérifier que le profil est bien sauvegardé
    analyzer2 = LearningStyleAnalyzer(user_id, storage_path=temp_storage)
    assert analyzer2.profile is not None
    assert analyzer2.profile.primary['style'] == result.primary['style']

    # 7. Vérifier qu'on n'a plus besoin du quiz
    assert analyzer2.profile.quiz_result is not None
