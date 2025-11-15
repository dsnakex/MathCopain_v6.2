"""
Tests pour core/security.py
Tests de sécurité: bcrypt, validation, rate limiting
"""

import pytest
import time
from datetime import datetime, timedelta
from core.security import (
    hash_pin,
    verify_pin,
    validate_pin_format,
    validate_username_format,
    authenticate_user,
    RateLimiter,
    get_rate_limiter,
    PINValidator,
    UsernameValidator
)


# ========== Tests Bcrypt Hashing ==========

class TestHashPIN:
    """Tests du hashing bcrypt des PINs."""

    def test_hash_pin_valid(self):
        """hash_pin() génère un hash bcrypt valide."""
        pin = "1234"
        hashed = hash_pin(pin)

        # Hash bcrypt commence par $2b$
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60  # Longueur standard bcrypt

    def test_hash_pin_different_each_time(self):
        """hash_pin() génère des hashs différents (salt aléatoire)."""
        pin = "5678"
        hash1 = hash_pin(pin)
        hash2 = hash_pin(pin)

        # Même PIN → hashs différents (salt aléatoire)
        assert hash1 != hash2

    def test_hash_pin_invalid_too_short(self):
        """hash_pin() rejette PIN trop court."""
        with pytest.raises(ValueError, match="PIN invalide"):
            hash_pin("123")

    def test_hash_pin_invalid_too_long(self):
        """hash_pin() rejette PIN trop long."""
        with pytest.raises(ValueError, match="PIN invalide"):
            hash_pin("12345")

    def test_hash_pin_invalid_non_digit(self):
        """hash_pin() rejette PIN non numérique."""
        with pytest.raises(ValueError, match="PIN invalide"):
            hash_pin("abcd")

    def test_hash_pin_invalid_mixed(self):
        """hash_pin() rejette PIN avec caractères mélangés."""
        with pytest.raises(ValueError, match="PIN invalide"):
            hash_pin("12a4")


class TestVerifyPIN:
    """Tests de vérification bcrypt."""

    def test_verify_pin_correct(self):
        """verify_pin() retourne True pour PIN correct."""
        pin = "9876"
        hashed = hash_pin(pin)

        assert verify_pin(pin, hashed) is True

    def test_verify_pin_incorrect(self):
        """verify_pin() retourne False pour PIN incorrect."""
        correct_pin = "1111"
        wrong_pin = "2222"
        hashed = hash_pin(correct_pin)

        assert verify_pin(wrong_pin, hashed) is False

    def test_verify_pin_invalid_format(self):
        """verify_pin() retourne False pour format invalide."""
        hashed = hash_pin("1234")

        # PIN invalide
        assert verify_pin("abc", hashed) is False
        assert verify_pin("12", hashed) is False

    def test_verify_pin_timing_safe(self):
        """verify_pin() utilise bcrypt (timing-attack safe)."""
        pin = "4321"
        hashed = hash_pin(pin)

        # Bcrypt est conçu pour être timing-safe
        # Test que ça ne lève pas d'exception
        assert verify_pin("0000", hashed) is False
        assert verify_pin(pin, hashed) is True


# ========== Tests Validation Pydantic ==========

class TestPINValidator:
    """Tests du validateur Pydantic de PIN."""

    def test_pin_validator_valid(self):
        """PINValidator accepte PIN valide."""
        validator = PINValidator(pin="1234")
        assert validator.pin == "1234"

    @pytest.mark.parametrize("valid_pin", ["0000", "9999", "5555", "1357"])
    def test_pin_validator_all_valid(self, valid_pin):
        """PINValidator accepte tous PINs valides."""
        validator = PINValidator(pin=valid_pin)
        assert validator.pin == valid_pin

    def test_pin_validator_too_short(self):
        """PINValidator rejette PIN trop court."""
        with pytest.raises(ValueError):
            PINValidator(pin="123")

    def test_pin_validator_too_long(self):
        """PINValidator rejette PIN trop long."""
        with pytest.raises(ValueError):
            PINValidator(pin="12345")

    def test_pin_validator_non_digit(self):
        """PINValidator rejette PIN non numérique."""
        with pytest.raises(ValueError, match="uniquement des chiffres"):
            PINValidator(pin="abcd")

    def test_pin_validator_mixed_characters(self):
        """PINValidator rejette PIN avec caractères mélangés."""
        with pytest.raises(ValueError):
            PINValidator(pin="12a4")

    def test_pin_validator_empty(self):
        """PINValidator rejette PIN vide."""
        with pytest.raises(ValueError):
            PINValidator(pin="")


class TestUsernameValidator:
    """Tests du validateur de nom d'utilisateur."""

    def test_username_validator_valid(self):
        """UsernameValidator accepte nom valide."""
        validator = UsernameValidator(username="Alice")
        assert validator.username == "Alice"

    @pytest.mark.parametrize("valid_name", [
        "Jean",
        "Marie-Claire",
        "François",
        "Zoé",
        "Jean-Pierre",
        "Anne-Sophie",
        "O'Connor"
    ])
    def test_username_validator_french_names(self, valid_name):
        """UsernameValidator accepte noms français."""
        validator = UsernameValidator(username=valid_name)
        assert validator.username == valid_name

    def test_username_validator_strips_whitespace(self):
        """UsernameValidator trim les espaces."""
        validator = UsernameValidator(username="  Alice  ")
        assert validator.username == "Alice"

    def test_username_validator_too_short(self):
        """UsernameValidator rejette nom trop court."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            UsernameValidator(username="A")

    def test_username_validator_too_long(self):
        """UsernameValidator rejette nom trop long."""
        long_name = "A" * 51
        with pytest.raises(Exception):  # Pydantic ValidationError
            UsernameValidator(username=long_name)

    def test_username_validator_invalid_characters(self):
        """UsernameValidator rejette caractères invalides."""
        with pytest.raises(ValueError, match="caractères non autorisés"):
            UsernameValidator(username="Alice123")

        with pytest.raises(ValueError, match="caractères non autorisés"):
            UsernameValidator(username="Alice@Test")


# ========== Tests Validation Functions ==========

class TestValidationFunctions:
    """Tests des fonctions publiques de validation."""

    def test_validate_pin_format_valid(self):
        """validate_pin_format() retourne True pour PIN valide."""
        is_valid, error = validate_pin_format("1234")
        assert is_valid is True
        assert error == ""

    def test_validate_pin_format_invalid(self):
        """validate_pin_format() retourne False et message pour PIN invalide."""
        is_valid, error = validate_pin_format("abc")
        assert is_valid is False
        assert len(error) > 0

    def test_validate_username_format_valid(self):
        """validate_username_format() retourne True pour nom valide."""
        is_valid, error = validate_username_format("Alice")
        assert is_valid is True
        assert error == ""

    def test_validate_username_format_invalid(self):
        """validate_username_format() retourne False et message pour nom invalide."""
        is_valid, error = validate_username_format("A")
        assert is_valid is False
        assert len(error) > 0


# ========== Tests Rate Limiter ==========

class TestRateLimiter:
    """Tests du rate limiter."""

    def test_rate_limiter_init(self):
        """RateLimiter initialise avec valeurs par défaut."""
        limiter = RateLimiter()
        assert limiter.max_attempts == 5
        assert limiter.window_minutes == 15
        assert limiter.lockout_minutes == 30

    def test_rate_limiter_custom_config(self):
        """RateLimiter accepte configuration personnalisée."""
        limiter = RateLimiter(max_attempts=3, window_minutes=10, lockout_minutes=20)
        assert limiter.max_attempts == 3
        assert limiter.window_minutes == 10
        assert limiter.lockout_minutes == 20

    def test_rate_limiter_no_lockout_initially(self):
        """RateLimiter: aucun lockout initial."""
        limiter = RateLimiter()
        is_locked, seconds = limiter.is_locked_out("alice")

        assert is_locked is False
        assert seconds is None

    def test_rate_limiter_record_failed_attempt(self):
        """RateLimiter enregistre tentatives échouées."""
        limiter = RateLimiter(max_attempts=3)

        # Première tentative
        should_lockout, remaining = limiter.record_failed_attempt("bob")
        assert should_lockout is False
        assert remaining == 2

        # Deuxième tentative
        should_lockout, remaining = limiter.record_failed_attempt("bob")
        assert should_lockout is False
        assert remaining == 1

        # Troisième tentative → lockout
        should_lockout, remaining = limiter.record_failed_attempt("bob")
        assert should_lockout is True
        assert remaining == 0

    def test_rate_limiter_lockout_enforced(self):
        """RateLimiter bloque après max_attempts."""
        limiter = RateLimiter(max_attempts=2, lockout_minutes=1)

        # 2 tentatives échouées
        limiter.record_failed_attempt("charlie")
        limiter.record_failed_attempt("charlie")

        # Vérifier lockout
        is_locked, seconds = limiter.is_locked_out("charlie")
        assert is_locked is True
        assert seconds > 0
        assert seconds <= 60  # Max 1 minute

    def test_rate_limiter_reset_attempts(self):
        """RateLimiter réinitialise compteur après succès."""
        limiter = RateLimiter(max_attempts=3)

        # 2 tentatives échouées
        limiter.record_failed_attempt("dave")
        limiter.record_failed_attempt("dave")

        # Succès → reset
        limiter.reset_attempts("dave")

        # Vérifier compteur réinitialisé
        should_lockout, remaining = limiter.record_failed_attempt("dave")
        assert remaining == 2  # Recommence à 0

    def test_rate_limiter_case_insensitive(self):
        """RateLimiter traite noms en case-insensitive."""
        limiter = RateLimiter(max_attempts=2)

        limiter.record_failed_attempt("Alice")
        limiter.record_failed_attempt("ALICE")

        # Devrait être locké (2 tentatives pour même utilisateur)
        is_locked, _ = limiter.is_locked_out("alice")
        assert is_locked is True

    def test_rate_limiter_different_users_independent(self):
        """RateLimiter: utilisateurs indépendants."""
        limiter = RateLimiter(max_attempts=2)

        # Alice: 2 tentatives
        limiter.record_failed_attempt("alice")
        limiter.record_failed_attempt("alice")

        # Bob: 1 tentative
        limiter.record_failed_attempt("bob")

        # Alice lockée, Bob non
        assert limiter.is_locked_out("alice")[0] is True
        assert limiter.is_locked_out("bob")[0] is False

    def test_rate_limiter_lockout_expiration(self):
        """RateLimiter: lockout expire après durée."""
        # Lockout très court pour test
        limiter = RateLimiter(max_attempts=1, lockout_minutes=0.01)  # ~0.6 secondes

        # Déclencher lockout
        limiter.record_failed_attempt("eve")

        # Vérifier locké
        assert limiter.is_locked_out("eve")[0] is True

        # Attendre expiration
        time.sleep(1)

        # Lockout doit être expiré
        assert limiter.is_locked_out("eve")[0] is False


class TestGlobalRateLimiter:
    """Tests du rate limiter global singleton."""

    def test_get_rate_limiter_returns_instance(self):
        """get_rate_limiter() retourne instance RateLimiter."""
        limiter = get_rate_limiter()
        assert isinstance(limiter, RateLimiter)

    def test_get_rate_limiter_singleton(self):
        """get_rate_limiter() retourne toujours même instance."""
        limiter1 = get_rate_limiter()
        limiter2 = get_rate_limiter()

        assert limiter1 is limiter2

    def test_global_rate_limiter_default_config(self):
        """Rate limiter global a configuration par défaut."""
        limiter = get_rate_limiter()

        assert limiter.max_attempts == 5
        assert limiter.window_minutes == 15
        assert limiter.lockout_minutes == 30


# ========== Tests Authentification Complète ==========

class TestAuthenticateUser:
    """Tests de la fonction d'authentification complète."""

    def test_authenticate_user_success(self):
        """authenticate_user() réussit avec PIN correct."""
        pin = "1234"
        hashed = hash_pin(pin)

        success, message = authenticate_user("alice", pin, hashed)

        assert success is True
        assert "réussie" in message.lower()

    def test_authenticate_user_wrong_pin(self):
        """authenticate_user() échoue avec PIN incorrect."""
        correct_pin = "1234"
        wrong_pin = "5678"
        hashed = hash_pin(correct_pin)

        success, message = authenticate_user("bob", wrong_pin, hashed)

        assert success is False
        assert "incorrect" in message.lower()
        assert "tentatives restantes" in message.lower()

    def test_authenticate_user_lockout_after_max_attempts(self):
        """authenticate_user() bloque après max tentatives."""
        # Créer nouveau limiter pour test isolé
        from core import security
        original_limiter = security._global_rate_limiter

        try:
            # Limiter temporaire avec 2 tentatives max
            test_limiter = RateLimiter(max_attempts=2, lockout_minutes=1)
            security._global_rate_limiter = test_limiter

            correct_pin = "1234"
            wrong_pin = "9999"
            hashed = hash_pin(correct_pin)

            # 2 tentatives échouées
            authenticate_user("testuser", wrong_pin, hashed)
            success, message = authenticate_user("testuser", wrong_pin, hashed)

            # Devrait être bloqué
            assert success is False
            assert "bloqué" in message.lower()

        finally:
            # Restaurer limiter original
            security._global_rate_limiter = original_limiter

    def test_authenticate_user_resets_on_success(self):
        """authenticate_user() réinitialise compteur après succès."""
        from core import security
        original_limiter = security._global_rate_limiter

        try:
            test_limiter = RateLimiter(max_attempts=5)  # 5 tentatives max
            security._global_rate_limiter = test_limiter

            pin = "1234"
            hashed = hash_pin(pin)

            # 2 échecs
            authenticate_user("resetuser", "0000", hashed)
            authenticate_user("resetuser", "0000", hashed)

            # Succès → reset
            success, msg = authenticate_user("resetuser", pin, hashed)
            assert success is True

            # Nouvelle tentative devrait recommencer à 5 essais
            success, message = authenticate_user("resetuser", "9999", hashed)
            assert "4 tentatives restantes" in message  # 5-1 = 4

        finally:
            security._global_rate_limiter = original_limiter


# ========== Tests Edge Cases ==========

class TestSecurityEdgeCases:
    """Tests de cas limites et edge cases."""

    def test_hash_pin_empty_string(self):
        """hash_pin() rejette string vide."""
        with pytest.raises(ValueError):
            hash_pin("")

    def test_verify_pin_empty_hash(self):
        """verify_pin() gère hash vide."""
        assert verify_pin("1234", "") is False

    def test_rate_limiter_cleanup_old_attempts(self):
        """RateLimiter nettoie anciennes tentatives."""
        # Fenêtre très courte pour test
        limiter = RateLimiter(max_attempts=5, window_minutes=0.01)

        # Tentative
        limiter.record_failed_attempt("cleanup_test")

        # Attendre expiration fenêtre
        time.sleep(1)

        # Nouvelle tentative (anciennes nettoyées)
        should_lockout, remaining = limiter.record_failed_attempt("cleanup_test")

        # Devrait recommencer à 0
        assert remaining == 4

    def test_username_validator_accents_french(self):
        """UsernameValidator gère accents français."""
        names = ["André", "Éléonore", "Gaëlle", "Noémie", "Chloé"]

        for name in names:
            validator = UsernameValidator(username=name)
            assert validator.username == name
