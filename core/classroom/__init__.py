"""
Classroom management module for MathCopain Phase 7

Contains:
- CurriculumMapper: Maps exercises to French National Curriculum competencies
- AnalyticsEngine: Provides analytics and performance insights
"""

from .curriculum_mapper import CurriculumMapper
from .analytics_engine import AnalyticsEngine

__all__ = ['CurriculumMapper', 'AnalyticsEngine']
