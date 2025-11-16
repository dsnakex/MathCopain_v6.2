"""
Classroom management module for MathCopain Phase 8
Institutional deployment features for teachers
"""

from core.classroom.classroom_manager import ClassroomManager
from core.classroom.assignment_engine import AssignmentEngine
from core.classroom.curriculum_mapper import CurriculumMapper

__all__ = [
    'ClassroomManager',
    'AssignmentEngine',
    'CurriculumMapper'
]
