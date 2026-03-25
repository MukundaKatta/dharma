"""Tests for dharma.paths module."""

import pytest

from dharma.paths import get_all_roadmaps, get_roadmap, list_available_roles


class TestGetRoadmap:
    def test_ai_ml_engineer(self):
        rm = get_roadmap("ai-ml-engineer")
        assert rm is not None
        assert rm.id == "ai-ml-engineer"
        assert len(rm.nodes) >= 10

    def test_data_engineer(self):
        rm = get_roadmap("data-engineer")
        assert rm is not None
        assert len(rm.nodes) >= 10

    def test_cloud_architect(self):
        rm = get_roadmap("cloud-architect")
        assert rm is not None
        assert len(rm.nodes) >= 10

    def test_backend_developer(self):
        rm = get_roadmap("backend-developer")
        assert rm is not None
        assert len(rm.nodes) >= 10

    def test_fullstack_developer(self):
        rm = get_roadmap("fullstack-developer")
        assert rm is not None
        assert len(rm.nodes) >= 10

    def test_nonexistent_role(self):
        assert get_roadmap("quantum-physicist") is None


class TestGetAllRoadmaps:
    def test_returns_all_five(self):
        all_maps = get_all_roadmaps()
        assert len(all_maps) == 5

    def test_all_have_valid_prerequisites(self):
        for rid, rm in get_all_roadmaps().items():
            errors = rm.validate_prerequisites()
            assert errors == [], "Roadmap {} has errors: {}".format(rid, errors)

    def test_no_circular_deps_in_any(self):
        for rid, rm in get_all_roadmaps().items():
            assert rm.has_circular_dependencies() is False, (
                "Roadmap {} has circular deps".format(rid)
            )


class TestListAvailableRoles:
    def test_returns_sorted_list(self):
        roles = list_available_roles()
        assert roles == sorted(roles)
        assert len(roles) == 5
