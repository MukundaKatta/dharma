"""Tests for dharma.recommender module."""

import pytest

from dharma.core import NodeStatus, ProgressTracker, Roadmap, SkillNode
from dharma.paths import get_roadmap
from dharma.recommender import GapAnalyzer, SkillRecommender


def _make_roadmap():
    """Create a small roadmap for recommender tests."""
    nodes = [
        SkillNode("python", "Python", "fundamentals", 1,
                  [], ["docs.python.org"], "Core Python", 40),
        SkillNode("sql", "SQL", "fundamentals", 1,
                  [], ["sqlzoo.net"], "Databases", 30),
        SkillNode("flask", "Flask", "tools", 2,
                  ["python"], ["flask.palletsprojects.com"], "Web framework", 25),
        SkillNode("orm", "SQLAlchemy", "tools", 2,
                  ["python", "sql"], ["sqlalchemy.org"], "ORM", 20),
        SkillNode("api", "REST APIs", "advanced", 3,
                  ["flask", "orm"], ["restfulapi.net"], "API design", 30),
    ]
    return Roadmap("test", "Test", "Test roadmap", nodes)


class TestSkillRecommender:
    def test_recommend_next_initial(self):
        rm = _make_roadmap()
        tracker = ProgressTracker(rm)
        rec = SkillRecommender(tracker)
        recs = rec.recommend_next(3)
        ids = [n.id for n in recs]
        assert "python" in ids or "sql" in ids
        assert "api" not in ids

    def test_recommend_next_after_progress(self):
        rm = _make_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_completed("python")
        tracker.mark_completed("sql")
        rec = SkillRecommender(tracker)
        recs = rec.recommend_next(3)
        ids = [n.id for n in recs]
        assert "flask" in ids
        assert "orm" in ids

    def test_recommend_by_category(self):
        rm = _make_roadmap()
        tracker = ProgressTracker(rm)
        rec = SkillRecommender(tracker)
        recs = rec.recommend_by_category("fundamentals")
        assert all(n.category == "fundamentals" for n in recs)

    def test_recommend_quick_wins(self):
        rm = _make_roadmap()
        tracker = ProgressTracker(rm)
        rec = SkillRecommender(tracker)
        quick = rec.recommend_quick_wins(max_hours=35)
        assert all(n.estimated_hours <= 35 for n in quick)

    def test_get_learning_path(self):
        rm = _make_roadmap()
        tracker = ProgressTracker(rm)
        rec = SkillRecommender(tracker)
        path = rec.get_learning_path("api")
        ids = [n.id for n in path]
        assert "api" in ids
        assert ids.index("python") < ids.index("flask")

    def test_learning_path_completed_target(self):
        rm = _make_roadmap()
        tracker = ProgressTracker(rm)
        tracker.mark_completed("python")
        tracker.mark_completed("sql")
        tracker.mark_completed("flask")
        tracker.mark_completed("orm")
        tracker.mark_completed("api")
        rec = SkillRecommender(tracker)
        path = rec.get_learning_path("api")
        assert path == []

    def test_learning_path_nonexistent(self):
        rm = _make_roadmap()
        tracker = ProgressTracker(rm)
        rec = SkillRecommender(tracker)
        assert rec.get_learning_path("nonexistent") == []


class TestGapAnalyzer:
    def test_missing_skills(self):
        rm = _make_roadmap()
        analyzer = GapAnalyzer({"python", "sql"}, rm)
        missing = analyzer.get_missing_skills()
        ids = [n.id for n in missing]
        assert "flask" in ids
        assert "python" not in ids

    def test_matched_skills(self):
        rm = _make_roadmap()
        analyzer = GapAnalyzer({"python", "sql"}, rm)
        matched = analyzer.get_matched_skills()
        ids = [n.id for n in matched]
        assert "python" in ids
        assert "flask" not in ids

    def test_readiness_score(self):
        rm = _make_roadmap()
        analyzer = GapAnalyzer({"python", "sql"}, rm)
        score = analyzer.get_readiness_score()
        assert score == 40.0

    def test_readiness_score_full(self):
        rm = _make_roadmap()
        all_ids = {n.id for n in rm.nodes}
        analyzer = GapAnalyzer(all_ids, rm)
        assert analyzer.get_readiness_score() == 100.0

    def test_priority_gaps(self):
        rm = _make_roadmap()
        analyzer = GapAnalyzer({"python", "sql"}, rm)
        gaps = analyzer.get_priority_gaps(3)
        assert len(gaps) > 0
        assert all(n.id not in {"python", "sql"} for n in gaps)

    def test_gap_summary(self):
        rm = _make_roadmap()
        analyzer = GapAnalyzer({"python"}, rm)
        summary = analyzer.get_gap_summary()
        assert summary["total_skills"] == 5
        assert summary["completed_skills"] == 1
        assert summary["missing_skills"] == 4
        assert "missing_by_category" in summary

    def test_empty_completion(self):
        rm = _make_roadmap()
        analyzer = GapAnalyzer(set(), rm)
        assert analyzer.get_readiness_score() == 0.0
        assert len(analyzer.get_missing_skills()) == 5
