#! /usr/bin/env python3
"""Check TLS reports."""

import email
import gzip
import imaplib
import json
from typing import Any, List

from .util import cli, search


def get_tls_report(msg: email.message.Message) -> Any:
    """Read TLS report from message."""
    for attachment in msg.walk():
        if attachment.get_content_type() == "application/tlsrpt+gzip":
            return json.loads(gzip.decompress(attachment.get_payload(decode=True)))
        if attachment.get_content_type() == "application/tlsrpt+json":
            return json.loads(attachment.get_payload(decode=True))


def report(mail: imaplib.IMAP4) -> List[Any]:
    """Read all TLS reports from IMAP."""
    return [
        x
        for x in [
            get_tls_report(m) for m in search(mail, '(HEADER TLS-Report-Domain "")')
        ]
        if x
    ]


def main() -> None:  # pragma: no cover
    """Entrypoint."""
    cli(report)


if __name__ == "__main__":  # pragma: no cover
    main()
