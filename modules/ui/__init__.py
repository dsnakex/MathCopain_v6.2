"""UI Module pour MathCopain Design System"""

from .styles import setup_ui, load_custom_css
from .components import metric_card, progress_bar, info_box, badge

__all__ = [
    "setup_ui",
    "load_custom_css",
    "metric_card",
    "progress_bar",
    "info_box",
    "badge",
]
