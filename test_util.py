import util

import unittest
import unittest.mock


class TestUtil(unittest.TestCase):
    def test_isok_ok(self):
        self.assertEqual(util.isok("OK", ["Foobar"]), ["Foobar"])

    def test_isok_bad(self):
        with self.assertRaises(Exception):
            util.isok("BAD", ["Foobar"])

    def test_search(self):
        mail = unittest.mock.Mock()
        mail.uid.side_effect = [("OK", ["1"]), ("OK", [["1", b"2"]])]
        list(util.search(mail, "Foobar"))
        mail.uid.assert_any_call("SEARCH", "Foobar")
        mail.uid.assert_any_call("FETCH", "1", "(RFC822)")

    def test_imap(self):
        with unittest.mock.patch("imaplib.IMAP4_SSL") as mail:
            report = unittest.mock.Mock()
            util.imap("imap.gmail.com", "barnaby@example.com", "foo", "INBOX", report)
            report.assert_called_once()

    def test_cli(self):
        with unittest.mock.patch("util.imap") as imap:
            with unittest.mock.patch("argparse.ArgumentParser"):
                with unittest.mock.patch("getpass.getpass"):
                    imap.return_value = []
                    util.cli(None)
