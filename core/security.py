"""
Security Module - PIN Hashing, Validation & Rate Limiting
Sécurisation authentification avec bcrypt et protection brute-force
"""

import bcrypt
import time
from typing import Tuple, Optional, Dict
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator
import logging

logger = logging.getLogger(__name__)


# ========== Pydantic Models pour Validation ==========

class PINValidator(BaseModel):
    """Validateur Pydantic pour PINs."""

    pin: str = Field(..., min_length=4, max_length=4)

    @field_validator('pin')
    @classmethod
    def validate_pin_digits(cls, v: str) -> str:
        """Vérifie que PIN contient exactement 4 chiffres."""
        if not v.isdigit():
            raise ValueError("PIN doit contenir uniquement des chiffres")
        if len(v) != 4:
            raise ValueError("PIN doit contenir exactement 4 chiffres")
        return v


class UsernameValidator(BaseModel):
    """Validateur Pydantic pour noms utilisateur."""

    username: str = Field(..., min_length=2, max_length=50)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Vérifie que username est valide."""
        v = v.strip()

        if len(v) < 2:
            raise ValueError("Le prénom doit contenir au moins 2 caractères")
        if len(v) > 50:
            raise ValueError("Le prénom est trop long (max 50 caractères)")

        # Autoriser lettres, espaces, tirets, apostrophes (français)
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ àâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ'-")
        if not all(c in allowed_chars for c in v):
            raise ValueError("Le prénom contient des caractères non autorisés")

        return v


# ========== Bcrypt PIN Hashing ==========

def hash_pin(pin: str) -> str:
    """
    Hash un PIN avec bcrypt.

    Args:
        pin: PIN en clair (4 chiffres)

    Returns:
        Hash bcrypt du PIN

    Raises:
        ValueError: Si PIN invalide
    """
    # Valider format PIN
    try:
        PINValidator(pin=pin)
    except Exception as e:
        raise ValueError(f"PIN invalide: {e}")

    # Générer salt et hasher
    salt = bcrypt.gensalt(rounds=12)  # 12 rounds = bon équilibre sécurité/performance
    hashed = bcrypt.hashpw(pin.encode('utf-8'), salt)

    return hashed.decode('utf-8')


def verify_pin(pin: str, hashed_pin: str) -> bool:
    """
    Vérifie un PIN contre son hash bcrypt.

    Args:
        pin: PIN en clair à vérifier
        hashed_pin: Hash bcrypt stocké

    Returns:
        True si PIN correct, False sinon
    """
    try:
        # Valider format PIN
        PINValidator(pin=pin)

        # Comparer avec bcrypt (timing-attack safe)
        return bcrypt.checkpw(pin.encode('utf-8'), hashed_pin.encode('utf-8'))

    except Exception as e:
        logger.warning(f"Erreur vérification PIN: {e}")
        return False


# ========== Rate Limiting ==========

class RateLimiter:
    """
    Rate limiter pour tentatives de connexion.
    Protection contre brute-force attacks.
    """

    def __init__(
        self,
        max_attempts: int = 5,
        window_minutes: int = 15,
        lockout_minutes: int = 30
    ):
        """
        Args:
            max_attempts: Nombre max de tentatives échouées
            window_minutes: Fenêtre de temps pour comptage (minutes)
            lockout_minutes: Durée de blocage après max_attempts (minutes)
        """
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes
        self.lockout_minutes = lockout_minutes

        # Stockage: {username: [timestamp1, timestamp2, ...]}
        self._attempts: Dict[str, list] = {}

        # Stockage lockouts: {username: lockout_until_timestamp}
        self._lockouts: Dict[str, datetime] = {}

    def is_locked_out(self, username: str) -> Tuple[bool, Optional[int]]:
        """
        Vérifie si utilisateur est bloqué.

        Args:
            username: Nom utilisateur

        Returns:
            (is_locked, seconds_remaining)
        """
        username_lower = username.lower().strip()

        # Vérifier si lockout actif
        if username_lower in self._lockouts:
            lockout_until = self._lockouts[username_lower]
            now = datetime.now()

            if now < lockout_until:
                # Encore bloqué
                seconds_remaining = int((lockout_until - now).total_seconds())
                return True, seconds_remaining
            else:
                # Lockout expiré, nettoyer
                del self._lockouts[username_lower]
                if username_lower in self._attempts:
                    del self._attempts[username_lower]

        return False, None

    def record_failed_attempt(self, username: str) -> Tuple[bool, int]:
        """
        Enregistre tentative échouée.

        Args:
            username: Nom utilisateur

        Returns:
            (should_lockout, attempts_remaining)
        """
        username_lower = username.lower().strip()
        now = datetime.now()

        # Nettoyer anciennes tentatives hors fenêtre
        self._cleanup_old_attempts(username_lower, now)

        # Ajouter nouvelle tentative
        if username_lower not in self._attempts:
            self._attempts[username_lower] = []

        self._attempts[username_lower].append(now)

        # Compter tentatives dans fenêtre
        attempts_count = len(self._attempts[username_lower])
        attempts_remaining = max(0, self.max_attempts - attempts_count)

        # Déclencher lockout si dépassement
        if attempts_count >= self.max_attempts:
            lockout_until = now + timedelta(minutes=self.lockout_minutes)
            self._lockouts[username_lower] = lockout_until
            logger.warning(
                f"User '{username}' locked out until {lockout_until} "
                f"({self.max_attempts} failed attempts)"
            )
            return True, 0

        return False, attempts_remaining

    def reset_attempts(self, username: str):
        """
        Réinitialise compteur après connexion réussie.

        Args:
            username: Nom utilisateur
        """
        username_lower = username.lower().strip()

        if username_lower in self._attempts:
            del self._attempts[username_lower]

        if username_lower in self._lockouts:
            del self._lockouts[username_lower]

    def _cleanup_old_attempts(self, username_lower: str, now: datetime):
        """Nettoie tentatives hors fenêtre de temps."""
        if username_lower not in self._attempts:
            return

        window_start = now - timedelta(minutes=self.window_minutes)

        # Garder seulement tentatives dans fenêtre
        self._attempts[username_lower] = [
            attempt_time for attempt_time in self._attempts[username_lower]
            if attempt_time >= window_start
        ]

        # Supprimer si vide
        if not self._attempts[username_lower]:
            del self._attempts[username_lower]


# ========== Singleton Global Rate Limiter ==========

# Instance globale pour toute l'application
_global_rate_limiter = RateLimiter(
    max_attempts=5,      # 5 tentatives max
    window_minutes=15,   # Dans une fenêtre de 15 minutes
    lockout_minutes=30   # Blocage 30 minutes
)


def get_rate_limiter() -> RateLimiter:
    """Retourne instance globale du rate limiter."""
    return _global_rate_limiter


# ========== Fonctions de Validation Publiques ==========

def validate_pin_format(pin: str) -> Tuple[bool, str]:
    """
    Valide format d'un PIN.

    Args:
        pin: PIN à valider

    Returns:
        (is_valid, error_message)
    """
    try:
        PINValidator(pin=pin)
        return True, ""
    except Exception as e:
        return False, str(e)


def validate_username_format(username: str) -> Tuple[bool, str]:
    """
    Valide format d'un nom d'utilisateur.

    Args:
        username: Nom à valider

    Returns:
        (is_valid, error_message)
    """
    try:
        UsernameValidator(username=username)
        return True, ""
    except Exception as e:
        return False, str(e)


# ========== Authentification Sécurisée Complète ==========

def authenticate_user(
    username: str,
    pin: str,
    hashed_pin: str
) -> Tuple[bool, str]:
    """
    Authentifie utilisateur avec rate limiting.

    Args:
        username: Nom utilisateur
        pin: PIN en clair
        hashed_pin: Hash bcrypt stocké

    Returns:
        (success, message)
    """
    rate_limiter = get_rate_limiter()

    # 1. Vérifier lockout
    is_locked, seconds_remaining = rate_limiter.is_locked_out(username)
    if is_locked:
        minutes = seconds_remaining // 60
        return False, f"Compte temporairement bloqué. Réessayez dans {minutes} minutes."

    # 2. Vérifier PIN
    pin_valid = verify_pin(pin, hashed_pin)

    if pin_valid:
        # Succès: réinitialiser compteur
        rate_limiter.reset_attempts(username)
        return True, "Authentification réussie"
    else:
        # Échec: enregistrer tentative
        should_lockout, attempts_remaining = rate_limiter.record_failed_attempt(username)

        if should_lockout:
            return False, f"Trop de tentatives échouées. Compte bloqué pour {rate_limiter.lockout_minutes} minutes."
        else:
            return False, f"PIN incorrect. {attempts_remaining} tentatives restantes."
