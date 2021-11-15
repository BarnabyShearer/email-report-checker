#! /usr/bin/env python3
"""Check DMARC reports."""

import email
import imaplib
import io
import zipfile
from typing import Any, List
from xml.etree import ElementTree

from .util import cli, search


def xml2dict(xml: Any) -> Any:
    """Convert xml to dict."""
    data = {}
    for child in list(xml):
        if len(list(child)) > 0:
            data[child.tag] = xml2dict(child)
        else:
            data[child.tag] = child.text or ""
    return data


def get_dmarc_report(msg: email.message.Message) -> Any:
    """Read DMARC report from message."""
    for attachment in msg.walk():
        if attachment.get_content_type() == "application/zip":
            fp = io.BytesIO(attachment.get_payload(decode=True))
            with zipfile.ZipFile(fp, "r") as zip:
                for name in zip.namelist():
                    with zip.open(name) as xml:
                        return xml2dict(ElementTree.parse(xml).getroot())


def report(mail: imaplib.IMAP4) -> List[Any]:
    """Read all DMARC reports from IMAP."""
    return [x for x in [get_dmarc_report(m) for m in search(mail, '(TO "+dmarc")')]]


def main() -> None:  # pragma: no cover
    """Entrypoint."""
    cli(report)


if __name__ == "__main__":  # pragma: no cover
    main()
