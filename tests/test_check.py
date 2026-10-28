"""Tests for link-check fallback classification. Run with: pytest"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.check import failed_urls, fallback_acceptable


def test_failed_urls_reads_error_statuses_from_stderr():
    output = "[503] https://example.com/a (at 1:1) | Service unavailable"
    assert failed_urls(output) == {"https://example.com/a"}


def test_failed_urls_reads_errors_and_timeouts_from_stdout():
    output = "\n".join(
        [
            "[ERROR] https://example.com/b (at 2:1) | TLS failure",
            "[TIMEOUT] https://example.com/c (at 3:1) | Timed out",
        ]
    )
    assert failed_urls(output) == {"https://example.com/b", "https://example.com/c"}


def test_fallback_accepts_reachable_and_bot_blocked_responses():
    for status in (200, 301, 403, 429):
        assert fallback_acceptable(status)


def test_fallback_rejects_missing_and_server_error_responses():
    for status in (None, 404, 500):
        assert not fallback_acceptable(status)
