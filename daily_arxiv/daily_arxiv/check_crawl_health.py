#!/usr/bin/env python3
import argparse
import json
import os
import sys


def evaluate_crawl_health(stats: dict, data_file: str) -> str:
    list_discovered = int(stats.get("list_discovered", 0) or 0)
    detail_success = int(stats.get("detail_success", 0) or 0)
    detail_failed = int(stats.get("detail_failed", 0) or 0)

    if list_discovered == 0:
        return "no_papers_found"
    if detail_success == 0:
        return "all_details_failed"
    if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
        return "empty_output"
    if detail_failed > 0:
        return "partial_detail_failure"
    return "ok"


def main():
    parser = argparse.ArgumentParser(description="Check crawl health based on spider stats.")
    parser.add_argument("--stats-file", required=True)
    parser.add_argument("--data-file", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.stats_file):
        print("crawl_health=missing_stats")
        print("message=Crawl stats file is missing")
        sys.exit(2)

    with open(args.stats_file, "r", encoding="utf-8") as f:
        stats = json.load(f)

    status = evaluate_crawl_health(stats, args.data_file)
    print(f"crawl_health={status}")
    print(f"list_discovered={int(stats.get('list_discovered', 0) or 0)}")
    print(f"detail_success={int(stats.get('detail_success', 0) or 0)}")
    print(f"detail_failed={int(stats.get('detail_failed', 0) or 0)}")
    print(f"log_count_error={int(stats.get('log_count_error', 0) or 0)}")

    if status in {"all_details_failed", "empty_output", "missing_stats"}:
        print("message=Fatal crawl problem: details failed or output empty")
        sys.exit(2)
    if status == "partial_detail_failure":
        print("message=Partial detail failure detected")
        sys.exit(1)
    if status == "no_papers_found":
        print("message=No papers found on listing pages")
        sys.exit(3)

    print("message=Crawl health OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
