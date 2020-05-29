#! /usr/bin/env python3
from typing import Any, Callable, List, TypeVar, Generator

import argparse
import email.message
import getpass
import imaplib
import json

T = TypeVar("T")
Report = Callable[[imaplib.IMAP4], List[Any]]


def isok(check: str, data: List[T]) -> List[T]:
    if check != "OK":
        raise Exception(check)
    return data


def search(mail, criteria: str) -> Generator[email.message.Message, None, None]:
    for uid in isok(*mail.uid("SEARCH", criteria))[0].split():
        yield email.message_from_bytes(isok(*mail.uid("FETCH", uid, "(RFC822)"))[0][1])


def imap(host: str, user: str, password: str, folder: str, report: Report) -> List[Any]:
    with imaplib.IMAP4_SSL(host) as mail:
        mail.login(user, password)
        mail.select(folder)
        return report(mail)


def cli(report: Report):
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
    print(json.dumps(data, indent=2))
