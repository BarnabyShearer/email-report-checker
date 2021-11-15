"""Test TLS entrypoint."""

import gzip
import unittest
import unittest.mock

from email_report_checker import tls


class TestTLS(unittest.TestCase):
    """Test TLS Report."""

    def test_report(self) -> None:
        """Test reporting."""
        with unittest.mock.patch("email_report_checker.tls.search"):
            with unittest.mock.patch("email_report_checker.tls.get_tls_report"):
                tls.report(None)  # type: ignore

    def test_get_tls_report_missing(self) -> None:
        """Test missing."""
        msg = unittest.mock.Mock()
        msg.walk.return_value = []
        tls.get_tls_report(msg)

    def test_get_tls_report_other(self) -> None:
        """Test wrong MIME."""
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/foo"
        tls.get_tls_report(msg)

    def test_get_tls_report(self) -> None:
        """Test empty report."""
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/tlsrpt+json"
        attachment.get_payload.return_value = "{}"
        tls.get_tls_report(msg)

    def test_get_tls_report_gzip(self) -> None:
        """Test empty gzipped report."""
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/tlsrpt+gzip"
        attachment.get_payload.return_value = gzip.compress(b"{}")
        tls.get_tls_report(msg)
