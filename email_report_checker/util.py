"""Utils."""

import argparse
import email.message
import getpass
import imaplib
import json
import sys
from typing import Any, Callable, Generator, List, TypeVar

T = TypeVar("T")
Report = Callable[[imaplib.IMAP4], List[Any]]


def isok(check: str, data: List[T]) -> List[T]:
    """Convert strings other then OK into exceptions."""
    if check != "OK":
        raise Exception(check)
    return data


def search(
    mail: imaplib.IMAP4, criteria: str
) -> Generator[email.message.Message, None, None]:
    """IMAP search."""
    for uid in isok(*mail.uid("SEARCH", criteria))[0].split():
        yield email.message_from_bytes(isok(*mail.uid("FETCH", uid, "(RFC822)"))[0][1])


def imap(host: str, user: str, password: str, folder: str, report: Report) -> List[Any]:
    """Open IMAP email."""
    with imaplib.IMAP4_SSL(host) as mail:
        mail.login(user, password)
        mail.select(folder)
        return report(mail)


def cli(report: Report) -> None:
    """Wrap command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="IMAP host connect to (SSL required)")
    parser.add_argument("user")
    parser.add_argument("folder", help="IMAP folder containg the reports")
    args = parser.parse_args()
    password = getpass.getpass("Password:")
    data = imap(
        host=args.host,
        user=args.user,
        password=password,
        folder=args.folder,
        report=report,
    )
    json.dump(data, sys.stdout, indent=2)
