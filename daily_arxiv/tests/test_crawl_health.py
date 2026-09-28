import os
import tempfile
import unittest

from daily_arxiv.check_crawl_health import evaluate_crawl_health


class CrawlHealthTests(unittest.TestCase):
    def test_no_papers_found(self):
        with tempfile.NamedTemporaryFile() as f:
            status = evaluate_crawl_health(
                {"list_discovered": 0, "detail_success": 0, "detail_failed": 0},
                f.name,
            )
        self.assertEqual(status, "no_papers_found")

    def test_all_details_failed(self):
        with tempfile.NamedTemporaryFile() as f:
            status = evaluate_crawl_health(
                {"list_discovered": 5, "detail_success": 0, "detail_failed": 5},
                f.name,
            )
        self.assertEqual(status, "all_details_failed")

    def test_partial_detail_failure(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write('{"id":"1234.5678"}\n')
            path = f.name
        try:
            status = evaluate_crawl_health(
                {"list_discovered": 5, "detail_success": 3, "detail_failed": 2},
                path,
            )
            self.assertEqual(status, "partial_detail_failure")
        finally:
            os.remove(path)

    def test_empty_output_is_failure(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            path = f.name
        try:
            status = evaluate_crawl_health(
                {"list_discovered": 2, "detail_success": 2, "detail_failed": 0},
                path,
            )
            self.assertEqual(status, "empty_output")
        finally:
            os.remove(path)
