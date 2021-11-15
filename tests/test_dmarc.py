"""Test the DMARC entrypoint."""

import unittest
import unittest.mock

from email_report_checker import dmarc


class TestDMARC(unittest.TestCase):
    """Test DMARC."""

    def test_report(self) -> None:
        """Test we can report."""
        with unittest.mock.patch("email_report_checker.dmarc.search"):
            with unittest.mock.patch("email_report_checker.dmarc.get_dmarc_report"):
                dmarc.report(None)  # type: ignore

    def test_get_dmarc_report_missing(self) -> None:
        """Test no report."""
        msg = unittest.mock.Mock()
        msg.walk.return_value = []
        dmarc.get_dmarc_report(msg)

    def test_get_dmarc_report_other(self) -> None:
        """Test wrong mime."""
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/foo"
        dmarc.get_dmarc_report(msg)

    def test_get_dmarc_report_zip(self) -> None:
        """Test real zip."""
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/zip"
        with open("test.zip", "rb") as zip:
            attachment.get_payload.return_value = zip.read()
        dmarc.get_dmarc_report(msg)

    def test_get_dmarc_report_empty(self) -> None:
        """Test empty."""
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/zip"
        attachment.get_payload.return_value = (
            b"PK\x05\x06\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00"
        )
        dmarc.get_dmarc_report(msg)
