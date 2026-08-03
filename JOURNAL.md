# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/50

**Issue title:** Add a `has_tests` boolean to the repo analysis output

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The analysis output for a repo currently has no signal for whether it has tests. This logic lives in `agent/tools/github_tool.py`, in the `GitHubTool` class, which already fetches things like star count, language, and `has_readme` from the GitHub API. The pattern to follow already exists: there's a `_has_readme()` method that checks a repo via a GitHub API call, and `has_tests` would work the same way — checking for a `tests/`/`test/` folder, a `pytest.ini` file, or files matching `test_*.py`. This matters because the issue explicitly calls test coverage "a strong portfolio signal," so this feature makes the tool smarter about what makes a repo look good. Success looks like a new `has_tests` boolean appearing in the repo metadata dict alongside `has_readme` and `star_count`, backed by a test I write myself, since no test file exists yet for `github_tool.py`.

**Selection notes (is this issue right for me?):**
This task aligns well with my experience working on Python projects and navigating existing codebases. I've worked with repository structures and testing frameworks like pytest, and I'm confident I can contribute by implementing reliable test detection logic and integrating it cleanly into the analysis output.

**Branch name:** feat/50-has-tests-detection

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/Itsurguy2/pathreview/commit/98887e14dd3ee6ac5c5f41359c88305333593d1c

**Reproduction summary:**
Wrote a test in `tests/unit/test_github_tool.py` asserting that `GitHubTool.execute()` returns `has_tests: True` for a repo containing a `tests/` directory. Ran it locally and confirmed it fails today with `AssertionError: assert None is True`, since no `has_tests` key exists in the output at all.

**PLAN.md link:** https://github.com/Itsurguy2/pathreview/blob/feat/50-has-tests-detection/PLAN.md

**Walkthrough video (recommended):** [not recorded]

**Blockers or open questions:**
Still deciding between the GitHub Contents API vs. the recursive Git Trees API for finding test files anywhere in the repo (not just the root directory) — leaning toward the Trees API but need to check how it behaves on very large repos (truncation) before committing to it in Week 9.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
All 5 sub-tasks from `PLAN.md` are done. Went with the recursive Git Trees API (`GET /repos/{u}/{r}/git/trees/{default_branch}?recursive=1`) — one call gets the whole file tree instead of walking directories one at a time. Added `_has_tests()` to `GitHubTool`, mirroring `_has_readme()`'s structure, and wired the result into `_fetch_repo_metadata()`'s output. Expanded `tests/unit/test_github_tool.py` from the single Week 8 reproduction test to 6 cases: `tests/` dir, a nested `test/` dir, `pytest.ini`, a loose `test_*.py` file, the negative case, and graceful handling when the tree API call fails. Ran the full `tests/unit` suite before and after: 54 pre-existing failures before (unrelated files — PII scrubber, resume parser, tech detector, etc.), 53 after — the drop is our own test flipping from failing to passing, and no new failures anywhere else. Confirmed `agent/tools/github_tool.py` and `tests/unit/test_github_tool.py` individually pass ruff, black, and mypy with zero errors.

**Next steps:**
Open the PR (as a draft first) and get peer/mentor feedback in Slack before marking it ready for review.

**Blockers:**
None. The truncation question from Week 8 is still open as a known limitation, not a blocker — noted in the PR description for reviewers.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/ascherj/pathreview/pull/221

**Branch:** `feat/50-has-tests-detection`

**What you built:**
Added a `has_tests` boolean to the repo analysis output. `GitHubTool` now checks — via a single recursive call to GitHub's Git Trees API — whether a repo contains a `tests/`/`test/` directory, a `pytest.ini` file, or any `test_*.py` file anywhere in the tree, and surfaces the result alongside the existing `has_readme` and `star_count` fields.

**Tests added or updated:**
`tests/unit/test_github_tool.py` — grew from the single Week 8 reproduction test to 6 cases: a `tests/` directory, a nested `test/` directory, a `pytest.ini` file, a loose `test_*.py` file, the negative case (no signals present), and graceful degradation to `False` when the GitHub API call fails.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes
*(Both checked per the pre-existing-failures rule documented in the PR: `agent/tools/github_tool.py` and `tests/unit/test_github_tool.py` individually pass ruff/black/mypy with zero errors, and `tests/unit` went from 54 pre-existing failures to 53 — this change introduces no new failures anywhere in the suite. The repo-wide `make check`/`make test-unit` commands still fail overall due to unrelated pre-existing issues across ~26 other files, documented in the PR's "Notes for Reviewers.")*

**Draft PR feedback received from:** none
