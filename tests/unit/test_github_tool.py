"""Tests for github_tool.py"""

from unittest.mock import MagicMock

import pytest

from agent.tools.github_tool import GitHubTool


@pytest.mark.unit
class TestGitHubToolHasTests:
    """Reproduction for issue #50: repo analysis output has no has_tests signal."""

    @pytest.fixture
    def tool(self) -> GitHubTool:
        return GitHubTool()

    def test_repo_metadata_includes_has_tests_field(
        self, tool: GitHubTool, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A repo whose file tree contains a tests/ directory should be flagged.

        Issue #50 repro: GitHubTool.execute() currently has no has_tests key
        in its output at all, so this assertion fails today with
        AssertionError: None != True. There is no _has_tests() method on
        GitHubTool, unlike the existing _has_readme() method it should mirror.
        """
        mock_repo_response = MagicMock()
        mock_repo_response.raise_for_status.return_value = None
        mock_repo_response.json.return_value = {
            "name": "sample-repo",
            "description": "A sample repo",
            "language": "Python",
            "stargazers_count": 5,
            "forks_count": 1,
            "open_issues_count": 0,
            "pushed_at": "2026-01-01T00:00:00Z",
            "topics": [],
            "homepage": "",
        }

        mock_head_response = MagicMock(status_code=200)

        monkeypatch.setattr("httpx.get", lambda *a, **k: mock_repo_response)
        monkeypatch.setattr("httpx.head", lambda *a, **k: mock_head_response)

        result = tool.execute({"github_username": "octocat", "repo_name": "sample-repo"})

        assert result.success is True
        assert result.data.get("has_tests") is True
