email-report-checker
====================

RFC 7489 & 8460 SMTP Report Monitoring Utilities.

Note these are for my hobby domain, do not try running them on even moderate traffic MTAs

RFC 7489 Domain-based Message Authentication, Reporting, and Conformance (DMARC)
--------------------------------------------------------------------------------

First ensure your DMARC DNS TXT record contains `rua` and `ruf` to request reports:

    _dmarc.zi.is.		3600	IN	TXT	"v=DMARC1; p=reject; pct=100; ruf=mailto:b+dmarc@zi.is; rua=mailto:b+dmarc@zi.is; adkim=s; aspf=s"

Then load the reports via IMAP:

::

    ./dmarc.py m.zi.is b@zi.is Archive > dmarc.json

And report your statistics

::

    jq '[ .[].record.row | select(.source_ip == "68.183.35.248") | select(.policy_evaluated.dkim == "pass") | .count | tonumber] | add' dmarc.json
    jq '[ .[].record.row | select(.source_ip == "68.183.35.248") | select(.policy_evaluated.dkim == "fail") | .count | tonumber] | add' dmarc.json


RFC 8460 SMTP TLS Reporting
---------------------------

First create a DNS TXT record to request reports:

::

    _smtp._tls.zi.is.	3600	IN	TXT	"v=TLSRPTv1;rua=mailto:b+tls@zi.is"

Then load the reports via IMAP:

::

    ./tls.py m.zi.is b@zi.is Archive > tls.json

And report your statistics

::

    jq '[.[] | [.policies[].summary["total-successful-session-count"]] | add] | add' tls.json
    jq '[.[] | [.policies[].summary["total-failure-session-count"]] | add] | add' tls.json



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   email_report_checker

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
