"""
Générateurs d'exercices MathCopain
DEPRECATED: Backward compatibility wrapper for core.exercise_generator

⚠️ This module is deprecated. All exercise generation logic has been
   moved to core.exercise_generator. Please update your imports:

   OLD: from modules.exercices import generer_addition
   NEW: from core.exercise_generator import generer_addition

This file will be removed in a future version.
"""

# Re-export functions from core.exercise_generator for backward compatibility
from core.exercise_generator import (
    generer_addition,
    generer_soustraction,
    generer_tables,
    generer_division
)

__all__ = [
    'generer_addition',
    'generer_soustraction',
    'generer_tables',
    'generer_division'
]
