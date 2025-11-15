"""
MathCopain Core Package
Logique métier et gestion d'état
"""

from .session_manager import SessionManager
from .data_manager import DataManager
from .adaptive_system import AdaptiveSystem
from .skill_tracker import SkillTracker
from . import exercise_generator

__all__ = [
    'SessionManager',
    'DataManager',
    'AdaptiveSystem',
    'SkillTracker',
    'exercise_generator',
]
