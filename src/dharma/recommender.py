"""Skill recommendation and gap analysis for developer roadmaps.

Provides intelligent suggestions for next skills based on completed
progress and career goals, plus gap analysis between current skills
and role requirements.
"""

from typing import Dict, List, Optional, Set

from dharma.core import NodeStatus, ProgressTracker, Roadmap, SkillNode


class SkillRecommender:
    """Recommends next skills based on progress and career goals.

    Analyzes the dependency graph and current completion status to
    suggest the most impactful skills to learn next.
    """

    def __init__(self, tracker):
        # type: (ProgressTracker) -> None
        self._tracker = tracker
        self._roadmap = tracker.roadmap

    def recommend_next(self, max_results=5):
        # type: (int) -> List[SkillNode]
        """Recommend next skills to learn.

        Scoring considers: prerequisite completion, downstream impact,
        and skill level progression.
        """
        available = self._tracker.get_available_nodes()
        scored = []
        for node in available:
            score = self._compute_score(node)
            scored.append((score, node))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [node for _, node in scored[:max_results]]

    def _compute_score(self, node):
        # type: (SkillNode) -> float
        """Compute a priority score for a candidate node.

        Higher scores mean the node should be recommended sooner.
        """
        downstream = self._count_downstream(node.id)
        level_bonus = max(0, 6 - node.level)
        resource_bonus = min(len(node.resources), 3)
        return float(downstream * 3 + level_bonus * 2 + resource_bonus)

    def _count_downstream(self, node_id):
        # type: (str) -> int
        """Count how many nodes directly depend on the given node."""
        count = 0
        for node in self._roadmap.nodes:
            if node_id in node.prerequisites:
                count += 1
        return count

    def recommend_by_category(self, category):
        # type: (str) -> List[SkillNode]
        """Recommend available nodes filtered by category."""
        available = self._tracker.get_available_nodes()
        return [n for n in available if n.category == category]

    def recommend_quick_wins(self, max_hours=20):
        # type: (int) -> List[SkillNode]
        """Recommend available nodes that can be completed quickly."""
        available = self._tracker.get_available_nodes()
        quick = [n for n in available if n.estimated_hours <= max_hours]
        quick.sort(key=lambda n: n.estimated_hours)
        return quick

    def get_learning_path(self, target_node_id):
        # type: (str) -> List[SkillNode]
        """Compute the ordered list of incomplete nodes needed to reach
        a target node, including the target itself.

        Returns an empty list if the target is already completed or
        if the node ID is not found.
        """
        target = self._roadmap.get_node(target_node_id)
        if target is None:
            return []
        if self._tracker.get_status(target_node_id) == NodeStatus.COMPLETED:
            return []

        needed = []  # type: List[str]
        visited = set()  # type: Set[str]

        def _collect(nid):
            # type: (str) -> None
            if nid in visited:
                return
            visited.add(nid)
            node = self._roadmap.get_node(nid)
            if node is None:
                return
            for prereq in node.prerequisites:
                if self._tracker.get_status(prereq) != NodeStatus.COMPLETED:
                    _collect(prereq)
            if self._tracker.get_status(nid) != NodeStatus.COMPLETED:
                needed.append(nid)

        _collect(target_node_id)
        return [self._roadmap.get_node(nid) for nid in needed
                if self._roadmap.get_node(nid) is not None]


class GapAnalyzer:
    """Analyzes gaps between current skills and role requirements.

    Compares a developer's completed skills against a target roadmap
    to identify what's missing and prioritize learning.
    """

    def __init__(self, completed_skill_ids, target_roadmap):
        # type: (Set[str], Roadmap) -> None
        self._completed = set(completed_skill_ids)
        self._target = target_roadmap

    @property
    def target_roadmap(self):
        # type: () -> Roadmap
        """The target roadmap being analyzed against."""
        return self._target

    def get_missing_skills(self):
        # type: () -> List[SkillNode]
        """Return skills in the target roadmap that are not completed."""
        return [
            node for node in self._target.nodes
            if node.id not in self._completed
        ]

    def get_matched_skills(self):
        # type: () -> List[SkillNode]
        """Return skills in the target roadmap that are already completed."""
        return [
            node for node in self._target.nodes
            if node.id in self._completed
        ]

    def get_readiness_score(self):
        # type: () -> float
        """Calculate readiness percentage for the target role.

        Returns a value from 0.0 to 100.0.
        """
        if not self._target.nodes:
            return 0.0
        matched = sum(1 for n in self._target.nodes if n.id in self._completed)
        return round(100.0 * matched / len(self._target.nodes), 1)

    def get_priority_gaps(self, max_results=5):
        # type: (int) -> List[SkillNode]
        """Return the most impactful missing skills to close.

        Prioritizes lower-level foundational skills that unlock
        the most downstream nodes.
        """
        missing = self.get_missing_skills()
        target_ids = {n.id for n in self._target.nodes}

        def _unlock_count(node):
            # type: (SkillNode) -> int
            count = 0
            for other in self._target.nodes:
                if node.id in other.prerequisites and other.id not in self._completed:
                    count += 1
            return count

        scored = []
        for node in missing:
            prereqs_met = all(
                p in self._completed or p not in target_ids
                for p in node.prerequisites
            )
            if prereqs_met:
                unlocks = _unlock_count(node)
                scored.append((node.level, -unlocks, node.id, node))

        scored.sort(key=lambda x: (x[0], x[1], x[2]))
        return [n for _, _, _, n in scored[:max_results]]

    def get_gap_summary(self):
        # type: () -> Dict[str, object]
        """Return a summary of the gap analysis."""
        missing = self.get_missing_skills()
        matched = self.get_matched_skills()
        missing_hours = sum(n.estimated_hours for n in missing)
        missing_by_category = {}  # type: Dict[str, int]
        for node in missing:
            missing_by_category[node.category] = (
                missing_by_category.get(node.category, 0) + 1
            )
        return {
            "target_role": self._target.title,
            "total_skills": len(self._target.nodes),
            "completed_skills": len(matched),
            "missing_skills": len(missing),
            "readiness_score": self.get_readiness_score(),
            "estimated_hours_remaining": missing_hours,
            "missing_by_category": missing_by_category,
        }
