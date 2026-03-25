"""Dharma - Interactive Developer Roadmaps.

Learning paths for AI/ML, data engineering, cloud architecture and more.
Skill tree with progress tracking, inspired by Hindu cosmic law (Dharma).
"""

from dharma.core import (
    NodeStatus,
    ProgressTracker,
    Roadmap,
    RoadmapEngine,
    SkillNode,
)
from dharma.paths import get_all_roadmaps, get_roadmap
from dharma.recommender import GapAnalyzer, SkillRecommender

__version__ = "0.1.0"
__all__ = [
    "NodeStatus",
    "ProgressTracker",
    "Roadmap",
    "RoadmapEngine",
    "SkillNode",
    "get_all_roadmaps",
    "get_roadmap",
    "GapAnalyzer",
    "SkillRecommender",
]
