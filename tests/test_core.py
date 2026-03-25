"""Tests for dharma.core module."""

import pytest

from dharma.core import (
    NodeStatus,
    ProgressTracker,
    Roadmap,
    RoadmapEngine,
    SkillNode,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_sample_roadmap():
    """Create a small roadmap for testing."""
    nodes = [
        SkillNode("python", "Python", "fundamentals", 1,
                  [], ["docs.python.org"], "Learn Python", 40),
        SkillNode("sql", "SQL", "fundamentals", 1,
                  [], ["sqlzoo.net"], "Learn SQL", 30),
        SkillNode("flask", "Flask", "tools", 2,
                  ["python"], ["flask.palletsprojects.com"], "Web framework", 25),
        SkillNode("orm", "SQLAlchemy ORM", "tools", 2,
                  ["python", "sql"], ["sqlalchemy.org"], "ORM library", 20),
        SkillNode("api", "REST API Design", "advanced", 3,
                  ["flask", "orm"], ["restfulapi.net"], "API design", 30),
    ]
    return Roadmap("test-roadmap", "Test Roadmap", "A test roadmap", nodes)


# ---------------------------------------------------------------------------
# SkillNode tests
# ---------------------------------------------------------------------------

class TestSkillNode:
    def test_create_valid_node(self):
        node = SkillNode("py", "Python", "fundamentals", 1)
        assert node.id == "py"
        assert node.title == "Python"
        assert node.level == 1
        assert node.prerequisites == []

    def test_invalid_level_low(self):
        with pytest.raises(ValueError):
            SkillNode("x", "X", "cat", 0)

    def test_invalid_level_high(self):
        with pytest.raises(ValueError):
            SkillNode("x", "X", "cat", 6)

    def test_empty_id_raises(self):
        with pytest.raises(ValueError):
            SkillNode("", "Title", "cat", 1)

    def test_empty_title_raises(self):
        with pytest.raises(ValueError):
            SkillNode("id", "", "cat", 1)

    def test_defaults(self):
        node = SkillNode("n", "Node", "cat", 3)
        assert node.resources == []
        assert node.description == ""
        assert node.estimated_hours == 0


# ---------------------------------------------------------------------------
# Roadmap tests
# ---------------------------------------------------------------------------

class TestRoadmap:
    def test_create_roadmap(self):
        rm = _make_sample_roadmap()
        assert rm.id == "test-roadmap"
        assert len(rm.nodes) == 5

    def test_get_node(self):
        rm = _make_sample_roadmap()
        assert rm.get_node("python").title == "Python"
        assert rm.get_node("nonexistent") is None

    def test_get_nodes_by_category(self):
        rm = _make_sample_roadmap()
        tools = rm.get_nodes_by_category("tools")
        assert len(tools) == 2

    def test_get_nodes_by_level(self):
        rm = _make_sample_roadmap()
        assert len(rm.get_nodes_by_level(1)) == 2
        assert len(rm.get_nodes_by_level(3)) == 1

    def test_get_categories(self):
        rm = _make_sample_roadmap()
        cats = rm.get_categories()
        assert cats == ["advanced", "fundamentals", "tools"]

    def test_total_estimated_hours(self):
        rm = _make_sample_roadmap()
        assert rm.get_total_estimated_hours() == 145

    def test_validate_prerequisites_valid(self):
        rm = _make_sample_roadmap()
        assert rm.validate_prerequisites() == []

    def test_validate_prerequisites_invalid(self):
        nodes = [
            SkillNode("a", "A", "cat", 1, ["missing"]),
        ]
        rm = Roadmap("bad", "Bad", "Bad roadmap", nodes)
        errors = rm.validate_prerequisites()
        assert len(errors) == 1
        assert "missing" in errors[0]

    def test_no_circular_dependencies(self):
        rm = _make_sample_roadmap()
        assert rm.has_circular_dependencies() is False

    def test_circular_dependencies_detected(self):
        nodes = [
            SkillNode("a", "A", "cat", 1, ["b"]),
            SkillNode("b", "B", "cat", 1, ["a"]),
        ]
        rm = Roadmap("circ", "Circular", "Has cycle", nodes)
        assert rm.has_circular_dependencies() is True

    def test_empty_id_raises(self):
        with pytest.raises(ValueError):
            Roadmap("", "Title", "Desc")

    def test_empty_title_raises(self):
        with pytest.raises(ValueError):
            Roadmap("id", "", "Desc")


# ---------------------------------------------------------------------------
# ProgressTracker tests
# ---------------------------------------------------------------------------

class TestProgressTracker:
    def test_initial_status(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        assert tracker.get_status("python") == NodeStatus.NOT_STARTED

    def test_mark_completed_no_prereqs(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        assert tracker.mark_completed("python") is True
        assert tracker.get_status("python") == NodeStatus.COMPLETED

    def test_mark_completed_with_unmet_prereqs(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        assert tracker.mark_completed("flask") is False

    def test_mark_completed_with_met_prereqs(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_completed("python")
        assert tracker.mark_completed("flask") is True

    def test_mark_in_progress(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_in_progress("python")
        assert tracker.get_status("python") == NodeStatus.IN_PROGRESS

    def test_mark_skipped(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_skipped("sql")
        assert tracker.get_status("sql") == NodeStatus.SKIPPED

    def test_get_completed_nodes(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_completed("python")
        tracker.mark_completed("sql")
        completed = tracker.get_completed_nodes()
        assert len(completed) == 2

    def test_get_available_nodes(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        available = tracker.get_available_nodes()
        ids = [n.id for n in available]
        assert "python" in ids
        assert "sql" in ids
        assert "flask" not in ids

    def test_suggest_next_steps(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        suggestions = tracker.suggest_next_steps(2)
        assert len(suggestions) <= 2
        assert all(isinstance(n, SkillNode) for n in suggestions)

    def test_completion_percentage(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        assert tracker.get_completion_percentage() == 0.0
        tracker.mark_completed("python")
        assert tracker.get_completion_percentage() == 20.0

    def test_progress_summary(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_completed("python")
        summary = tracker.get_progress_summary()
        assert summary["completed"] == 1
        assert summary["not_started"] == 4

    def test_category_progress(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_completed("python")
        prog = tracker.get_category_progress()
        assert prog["fundamentals"] == (1, 2)

    def test_estimated_remaining_hours(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        assert tracker.get_estimated_remaining_hours() == 145
        tracker.mark_completed("python")
        assert tracker.get_estimated_remaining_hours() == 105

    def test_reset(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_completed("python")
        tracker.reset()
        assert tracker.get_status("python") == NodeStatus.NOT_STARTED

    def test_invalid_node_id_raises(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        with pytest.raises(KeyError):
            tracker.get_status("nonexistent")

    def test_set_status_type_error(self):
        rm = _make_sample_roadmap()
        tracker = ProgressTracker(rm)
        with pytest.raises(TypeError):
            tracker.set_status("python", "completed")


# ---------------------------------------------------------------------------
# RoadmapEngine tests
# ---------------------------------------------------------------------------

class TestRoadmapEngine:
    def test_register_and_retrieve(self):
        engine = RoadmapEngine()
        rm = _make_sample_roadmap()
        engine.register_roadmap(rm)
        assert engine.get_roadmap("test-roadmap") is rm

    def test_list_roadmaps(self):
        engine = RoadmapEngine()
        engine.register_roadmap(_make_sample_roadmap())
        assert len(engine.list_roadmaps()) == 1

    def test_create_tracker(self):
        engine = RoadmapEngine()
        engine.register_roadmap(_make_sample_roadmap())
        tracker = engine.create_tracker("test-roadmap")
        assert isinstance(tracker, ProgressTracker)

    def test_create_tracker_unknown_roadmap(self):
        engine = RoadmapEngine()
        with pytest.raises(KeyError):
            engine.create_tracker("nonexistent")

    def test_search_nodes(self):
        engine = RoadmapEngine()
        engine.register_roadmap(_make_sample_roadmap())
        results = engine.search_nodes("python")
        assert len(results) >= 1

    def test_get_all_categories(self):
        engine = RoadmapEngine()
        engine.register_roadmap(_make_sample_roadmap())
        cats = engine.get_all_categories()
        assert "fundamentals" in cats

    def test_get_statistics(self):
        engine = RoadmapEngine()
        engine.register_roadmap(_make_sample_roadmap())
        stats = engine.get_statistics()
        assert stats["roadmap_count"] == 1
        assert stats["total_nodes"] == 5

    def test_register_invalid_type(self):
        engine = RoadmapEngine()
        with pytest.raises(TypeError):
            engine.register_roadmap("not a roadmap")

    def test_register_invalid_prerequisites(self):
        nodes = [SkillNode("a", "A", "cat", 1, ["missing"])]
        rm = Roadmap("bad", "Bad", "Bad", nodes)
        engine = RoadmapEngine()
        with pytest.raises(ValueError):
            engine.register_roadmap(rm)

    def test_register_circular_deps(self):
        nodes = [
            SkillNode("a", "A", "cat", 1, ["b"]),
            SkillNode("b", "B", "cat", 1, ["a"]),
        ]
        rm = Roadmap("circ", "Circ", "Circular", nodes)
        engine = RoadmapEngine()
        with pytest.raises(ValueError):
            engine.register_roadmap(rm)

    def test_get_tracker(self):
        engine = RoadmapEngine()
        engine.register_roadmap(_make_sample_roadmap())
        engine.create_tracker("test-roadmap", "user1")
        tracker = engine.get_tracker("test-roadmap", "user1")
        assert tracker is not None
