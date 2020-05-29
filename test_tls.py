import tls
import gzip
import unittest
import unittest.mock


class TestTLS(unittest.TestCase):
    def test_report(self):
        with unittest.mock.patch("tls.search"):
            with unittest.mock.patch("tls.get_tls_report"):
                tls.report(None)

    def test_get_tls_report_missing(self):
        msg = unittest.mock.Mock()
        msg.walk.return_value = []
        tls.get_tls_report(msg)

    def test_get_tls_report_other(self):
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/foo"
        tls.get_tls_report(msg)

    def test_get_tls_report(self):
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/tlsrpt+json"
        attachment.get_payload.return_value = "{}"
        tls.get_tls_report(msg)

    def test_get_tls_report_gzip(self):
        msg = unittest.mock.Mock()
        attachment = unittest.mock.Mock()
        msg.walk.return_value = [attachment]
        attachment.get_content_type.return_value = "application/tlsrpt+gzip"
        attachment.get_payload.return_value = gzip.compress(b"{}")
        tls.get_tls_report(msg)
