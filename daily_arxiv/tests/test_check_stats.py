import os
import tempfile
import unittest
from contextlib import contextmanager
from datetime import datetime, timezone
from unittest.mock import patch

from daily_arxiv import check_stats


@contextmanager
def chdir(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


class CheckStatsTests(unittest.TestCase):
    def test_utc_now_is_timezone_aware(self):
        self.assertEqual(check_stats.utc_now().tzinfo, timezone.utc)

    def test_no_papers_found_when_crawl_stats_are_zero(self):
        with patch.dict(
            os.environ,
            {"CRAWL_LIST_DISCOVERED": "0", "CRAWL_DETAIL_SUCCESS": "0", "CRAWL_DETAIL_FAILED": "0"},
            clear=False,
        ):
            self.assertEqual(check_stats.perform_deduplication(), "no_papers_found")

    def test_empty_today_file_is_crawl_failure(self):
        now = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            project_root = tmp
            data_dir = os.path.join(project_root, "data")
            os.makedirs(data_dir, exist_ok=True)
            today_file = os.path.join(data_dir, "2026-09-27.jsonl")
            open(today_file, "w", encoding="utf-8").close()

            workdir = os.path.join(project_root, "daily_arxiv")
            os.makedirs(workdir, exist_ok=True)

            with (
                chdir(workdir),
                patch("daily_arxiv.check_stats.utc_now", return_value=now),
                patch.dict(
                    os.environ,
                    {"CRAWL_LIST_DISCOVERED": "5", "CRAWL_DETAIL_SUCCESS": "0", "CRAWL_DETAIL_FAILED": "5"},
                    clear=False,
                ),
            ):
                self.assertEqual(check_stats.perform_deduplication(), "crawl_failure")
