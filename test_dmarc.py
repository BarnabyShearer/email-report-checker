import dmarc
import unittest
import unittest.mock


class TestDMARC(unittest.TestCase):
    def test_report(self):
        with unittest.mock.patch("dmarc.search"):
            with unittest.mock.patch("dmarc.get_dmarc_report"):
                dmarc.report(None)

    def test_get_dmarc_report_missing(self):
        msg = unittest.mock.Mock()
        msg.walk.return_value = []
        dmarc.get_dmarc_report(msg)

    def test_get_dmarc_report_other(self):
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/foo"
        dmarc.get_dmarc_report(msg)

    def test_get_dmarc_report_zip(self):
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/zip"
        with open("test.zip", "rb") as zip:
            attachment.get_payload.return_value = zip.read()
        dmarc.get_dmarc_report(msg)

    def test_get_dmarc_report_empty(self):
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/zip"
        attachment.get_payload.return_value = b"PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        dmarc.get_dmarc_report(msg)
