"""Core engine for Dharma developer roadmaps.

Provides the foundational data structures and logic for managing
skill trees, roadmaps, and developer progress tracking.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class NodeStatus(Enum):
    """Status of a skill node in a developer's learning journey."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


@dataclass
class SkillNode:
    """A single skill in a developer roadmap.

    Attributes:
        id: Unique identifier for the skill node.
        title: Human-readable name of the skill.
        category: Grouping category (e.g., 'fundamentals', 'tools', 'advanced').
        level: Difficulty level from 1 (beginner) to 5 (expert).
        prerequisites: List of skill node IDs that must be completed first.
        resources: List of learning resource URLs or descriptions.
        description: Optional longer description of the skill.
        estimated_hours: Estimated hours to learn this skill.
    """

    id: str
    title: str
    category: str
    level: int
    prerequisites: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    description: str = ""
    estimated_hours: int = 0

    def __post_init__(self):
        if self.level < 1 or self.level > 5:
            raise ValueError(
                "Skill level must be between 1 and 5, got {}".format(self.level)
            )
        if not self.id:
            raise ValueError("Skill node ID cannot be empty")
        if not self.title:
            raise ValueError("Skill node title cannot be empty")


@dataclass
class Roadmap:
    """A complete developer roadmap consisting of skill nodes.

    Attributes:
        id: Unique identifier for the roadmap.
        title: Human-readable title of the roadmap.
        description: Detailed description of the learning path.
        nodes: Ordered list of skill nodes in this roadmap.
    """

    id: str
    title: str
    description: str
    nodes: List[SkillNode] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            raise ValueError("Roadmap ID cannot be empty")
        if not self.title:
            raise ValueError("Roadmap title cannot be empty")

    def get_node(self, node_id):
        # type: (str) -> Optional[SkillNode]
        """Retrieve a skill node by its ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_nodes_by_category(self, category):
        # type: (str) -> List[SkillNode]
        """Get all nodes belonging to a specific category."""
        return [n for n in self.nodes if n.category == category]

    def get_nodes_by_level(self, level):
        # type: (int) -> List[SkillNode]
        """Get all nodes at a specific difficulty level."""
        return [n for n in self.nodes if n.level == level]

    def get_categories(self):
        # type: () -> List[str]
        """Return a sorted list of unique categories in this roadmap."""
        return sorted(set(n.category for n in self.nodes))

    def get_total_estimated_hours(self):
        # type: () -> int
        """Calculate total estimated learning hours for the roadmap."""
        return sum(n.estimated_hours for n in self.nodes)

    def validate_prerequisites(self):
        # type: () -> List[str]
        """Check that all prerequisite references are valid node IDs.

        Returns a list of error messages for invalid prerequisites.
        """
        node_ids = {n.id for n in self.nodes}
        errors = []
        for node in self.nodes:
            for prereq in node.prerequisites:
                if prereq not in node_ids:
                    errors.append(
                        "Node '{}' has invalid prerequisite '{}'".format(
                            node.id, prereq
                        )
                    )
        return errors

    def has_circular_dependencies(self):
        # type: () -> bool
        """Check whether the skill tree has any circular dependencies."""
        node_map = {n.id: n for n in self.nodes}
        visited = set()  # type: Set[str]
        rec_stack = set()  # type: Set[str]

        def _dfs(node_id):
            # type: (str) -> bool
            visited.add(node_id)
            rec_stack.add(node_id)
            node = node_map.get(node_id)
            if node:
                for prereq in node.prerequisites:
                    if prereq not in visited:
                        if _dfs(prereq):
                            return True
                    elif prereq in rec_stack:
                        return True
            rec_stack.discard(node_id)
            return False

        for n in self.nodes:
            if n.id not in visited:
                if _dfs(n.id):
                    return True
        return False


class ProgressTracker:
    """Tracks a developer's progress through a roadmap.

    Manages completion status of skill nodes, calculates progress
    metrics, and suggests the next steps in the learning journey.
    """

    def __init__(self, roadmap):
        # type: (Roadmap) -> None
        self._roadmap = roadmap
        self._status = {}  # type: Dict[str, NodeStatus]
        for node in roadmap.nodes:
            self._status[node.id] = NodeStatus.NOT_STARTED

    @property
    def roadmap(self):
        # type: () -> Roadmap
        """The roadmap being tracked."""
        return self._roadmap

    def get_status(self, node_id):
        # type: (str) -> NodeStatus
        """Get the current status of a specific node."""
        if node_id not in self._status:
            raise KeyError("Node '{}' not found in roadmap".format(node_id))
        return self._status[node_id]

    def set_status(self, node_id, status):
        # type: (str, NodeStatus) -> None
        """Set the status of a specific node."""
        if node_id not in self._status:
            raise KeyError("Node '{}' not found in roadmap".format(node_id))
        if not isinstance(status, NodeStatus):
            raise TypeError("Status must be a NodeStatus enum value")
        self._status[node_id] = status

    def mark_completed(self, node_id):
        # type: (str) -> bool
        """Mark a node as completed if all prerequisites are met.

        Returns True if the node was successfully marked, False if
        prerequisites are not satisfied.
        """
        if node_id not in self._status:
            raise KeyError("Node '{}' not found in roadmap".format(node_id))
        node = self._roadmap.get_node(node_id)
        if node is None:
            return False
        for prereq in node.prerequisites:
            if self._status.get(prereq) != NodeStatus.COMPLETED:
                return False
        self._status[node_id] = NodeStatus.COMPLETED
        return True

    def mark_in_progress(self, node_id):
        # type: (str) -> None
        """Mark a node as in progress."""
        self.set_status(node_id, NodeStatus.IN_PROGRESS)

    def mark_skipped(self, node_id):
        # type: (str) -> None
        """Mark a node as skipped."""
        self.set_status(node_id, NodeStatus.SKIPPED)

    def get_completed_nodes(self):
        # type: () -> List[SkillNode]
        """Return all completed skill nodes."""
        result = []
        for node in self._roadmap.nodes:
            if self._status[node.id] == NodeStatus.COMPLETED:
                result.append(node)
        return result

    def get_in_progress_nodes(self):
        # type: () -> List[SkillNode]
        """Return all nodes currently in progress."""
        return [
            n for n in self._roadmap.nodes
            if self._status[n.id] == NodeStatus.IN_PROGRESS
        ]

    def get_available_nodes(self):
        # type: () -> List[SkillNode]
        """Return nodes whose prerequisites are met but not yet started.

        These are the nodes the developer can begin working on next.
        """
        available = []
        for node in self._roadmap.nodes:
            if self._status[node.id] != NodeStatus.NOT_STARTED:
                continue
            prereqs_met = all(
                self._status.get(p) == NodeStatus.COMPLETED
                for p in node.prerequisites
            )
            if prereqs_met:
                available.append(node)
        return available

    def suggest_next_steps(self, max_suggestions=3):
        # type: (int) -> List[SkillNode]
        """Suggest next skill nodes to work on.

        Prioritizes by level (lower first) and then by how many
        downstream nodes they unlock.
        """
        available = self.get_available_nodes()
        node_map = {n.id: n for n in self._roadmap.nodes}

        def _downstream_count(node_id):
            # type: (str) -> int
            count = 0
            for n in self._roadmap.nodes:
                if node_id in n.prerequisites:
                    count += 1
            return count

        scored = []
        for node in available:
            downstream = _downstream_count(node.id)
            scored.append((node, node.level, -downstream))

        scored.sort(key=lambda x: (x[1], x[2]))
        return [s[0] for s in scored[:max_suggestions]]

    def get_completion_percentage(self):
        # type: () -> float
        """Calculate overall progress as a percentage."""
        if not self._roadmap.nodes:
            return 0.0
        completed = sum(
            1 for s in self._status.values() if s == NodeStatus.COMPLETED
        )
        return round(100.0 * completed / len(self._roadmap.nodes), 1)

    def get_progress_summary(self):
        # type: () -> Dict[str, int]
        """Get a summary count of nodes in each status."""
        summary = {status.value: 0 for status in NodeStatus}
        for status in self._status.values():
            summary[status.value] += 1
        return summary

    def get_category_progress(self):
        # type: () -> Dict[str, Tuple[int, int]]
        """Get progress per category as (completed, total) tuples."""
        categories = {}  # type: Dict[str, List[int]]
        for node in self._roadmap.nodes:
            if node.category not in categories:
                categories[node.category] = [0, 0]
            categories[node.category][1] += 1
            if self._status[node.id] == NodeStatus.COMPLETED:
                categories[node.category][0] += 1
        return {k: (v[0], v[1]) for k, v in categories.items()}

    def get_estimated_remaining_hours(self):
        # type: () -> int
        """Calculate estimated hours remaining for incomplete nodes."""
        remaining = 0
        for node in self._roadmap.nodes:
            if self._status[node.id] not in (
                NodeStatus.COMPLETED,
                NodeStatus.SKIPPED,
            ):
                remaining += node.estimated_hours
        return remaining

    def reset(self):
        # type: () -> None
        """Reset all progress to NOT_STARTED."""
        for node_id in self._status:
            self._status[node_id] = NodeStatus.NOT_STARTED


class RoadmapEngine:
    """Central engine for managing multiple roadmaps and tracking progress.

    Provides a registry of roadmaps and creates progress trackers
    for developers following specific learning paths.
    """

    def __init__(self):
        # type: () -> None
        self._roadmaps = {}  # type: Dict[str, Roadmap]
        self._trackers = {}  # type: Dict[str, ProgressTracker]

    def register_roadmap(self, roadmap):
        # type: (Roadmap) -> None
        """Register a roadmap in the engine."""
        if not isinstance(roadmap, Roadmap):
            raise TypeError("Expected a Roadmap instance")
        errors = roadmap.validate_prerequisites()
        if errors:
            raise ValueError(
                "Roadmap has invalid prerequisites: {}".format("; ".join(errors))
            )
        if roadmap.has_circular_dependencies():
            raise ValueError("Roadmap has circular dependencies")
        self._roadmaps[roadmap.id] = roadmap

    def get_roadmap(self, roadmap_id):
        # type: (str) -> Optional[Roadmap]
        """Retrieve a registered roadmap by ID."""
        return self._roadmaps.get(roadmap_id)

    def list_roadmaps(self):
        # type: () -> List[Roadmap]
        """Return all registered roadmaps."""
        return list(self._roadmaps.values())

    def create_tracker(self, roadmap_id, user_id="default"):
        # type: (str, str) -> ProgressTracker
        """Create a progress tracker for a user on a specific roadmap."""
        roadmap = self._roadmaps.get(roadmap_id)
        if roadmap is None:
            raise KeyError("Roadmap '{}' not found".format(roadmap_id))
        tracker_key = "{}:{}".format(user_id, roadmap_id)
        tracker = ProgressTracker(roadmap)
        self._trackers[tracker_key] = tracker
        return tracker

    def get_tracker(self, roadmap_id, user_id="default"):
        # type: (str, str) -> Optional[ProgressTracker]
        """Retrieve an existing tracker for a user and roadmap."""
        tracker_key = "{}:{}".format(user_id, roadmap_id)
        return self._trackers.get(tracker_key)

    def search_nodes(self, query):
        # type: (str) -> List[SkillNode]
        """Search all roadmaps for nodes matching a query string."""
        query_lower = query.lower()
        results = []
        for roadmap in self._roadmaps.values():
            for node in roadmap.nodes:
                if (
                    query_lower in node.title.lower()
                    or query_lower in node.category.lower()
                    or query_lower in node.description.lower()
                ):
                    results.append(node)
        return results

    def get_all_categories(self):
        # type: () -> List[str]
        """Return all unique categories across all roadmaps."""
        categories = set()  # type: Set[str]
        for roadmap in self._roadmaps.values():
            for node in roadmap.nodes:
                categories.add(node.category)
        return sorted(categories)

    def get_statistics(self):
        # type: () -> Dict[str, int]
        """Get overall statistics about registered roadmaps."""
        total_nodes = 0
        total_hours = 0
        for roadmap in self._roadmaps.values():
            total_nodes += len(roadmap.nodes)
            total_hours += roadmap.get_total_estimated_hours()
        return {
            "roadmap_count": len(self._roadmaps),
            "total_nodes": total_nodes,
            "total_estimated_hours": total_hours,
            "active_trackers": len(self._trackers),
        }
