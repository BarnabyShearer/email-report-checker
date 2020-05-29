#! /usr/bin/env python3
from typing import Any, List

import email
import zipfile
import imaplib
import json
import io
import xml.etree.ElementTree as ET

from util import cli, search


def xml2dict(xml: Any) -> Any:
    data = {}
    for child in list(xml):
        if len(list(child)) > 0:
            data[child.tag] = xml2dict(child)
        else:
            data[child.tag] = child.text or ""
    return data


def get_dmarc_report(msg: email.message.Message) -> Any:
    for attachment in msg.walk():
        if attachment.get_content_type() == "application/zip":
            fp = io.BytesIO(attachment.get_payload(decode=True))
            with zipfile.ZipFile(fp, "r") as zip:
                for name in zip.namelist():
                    with zip.open(name) as xml:
                        return xml2dict(ET.parse(xml).getroot())


def report(mail: imaplib.IMAP4) -> List[Any]:
    return [x for x in [get_dmarc_report(m) for m in search(mail, '(TO "+dmarc")')]]


if __name__ == "__main__":  # pragma: no cover
    cli(report)
