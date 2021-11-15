"""Test utils."""

import unittest
import unittest.mock

from email_report_checker import util


class TestUtil(unittest.TestCase):
    """Test Utils."""

    def test_isok_ok(self) -> None:
        """Test isok."""
        self.assertEqual(util.isok("OK", ["Foobar"]), ["Foobar"])

    def test_isok_bad(self) -> None:
        """Test isok bad."""
        with self.assertRaises(Exception):
            util.isok("BAD", ["Foobar"])

    def test_search(self) -> None:
        """Test search."""
        mail = unittest.mock.Mock()
        mail.uid.side_effect = [("OK", ["1"]), ("OK", [["1", b"2"]])]
        list(util.search(mail, "Foobar"))
        mail.uid.assert_any_call("SEARCH", "Foobar")
        mail.uid.assert_any_call("FETCH", "1", "(RFC822)")

    def test_imap(self) -> None:
        """Test IMAP reading."""
        with unittest.mock.patch("imaplib.IMAP4_SSL"):
            report = unittest.mock.Mock()
            util.imap("imap.gmail.com", "barnaby@example.com", "foo", "INBOX", report)
            report.assert_called_once()

    def test_cli(self) -> None:
        """Test CLI wrapper."""
        with unittest.mock.patch("email_report_checker.util.imap") as imap:
            with unittest.mock.patch("argparse.ArgumentParser"):
                with unittest.mock.patch("getpass.getpass"):
                    imap.return_value = []
                    util.cli(None)  # type: ignore
