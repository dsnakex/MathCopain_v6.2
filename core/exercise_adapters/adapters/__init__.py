"""
Exercise Adapters - Phase 6.3.2
Adapt exercise presentation according to learning style
"""

from .visual_adapter import VisualAdapter
from .auditory_adapter import AuditoryAdapter
from .kinesthetic_adapter import KinestheticAdapter
from .logical_adapter import LogicalAdapter
from .narrative_adapter import NarrativeAdapter

__all__ = [
    'VisualAdapter',
    'AuditoryAdapter',
    'KinestheticAdapter',
    'LogicalAdapter',
    'NarrativeAdapter'
]
