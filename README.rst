########
Icingapy
########

|License| |PyPI Downloads| |PyPI Version| |Build Status| |Coverage Status|

A library for interacting/scrapping Icinga 1 CGI endpoints.

Full Documentation can be found at: https://icingapy.readthedocs.io/

How to setup the client:

>>> from icingapy import IcingaClient
icinga = IcingaClient('icinga.host.com', 'admin', 'Ch@ng3m3!')

Icinga Client currently support three methods. **summary**, **status**, **downtime**

summary
  queries the *status.cgi* endpoint and parses the table for a list of services,
  their status and info.

>>> icinga.summary('testhost')
{'Current Load': {'service': 'Current Load', 'status': 'OK', 'info': 'OK - load average: 0.38, 0.33, 0.31'},
'Current Users': {'service': 'Current Users', 'status': 'OK', 'info': 'USERS OK - 0 users currently logged in'},
'Disk Space': {'service': 'Disk Space', 'info': 'DISK CRITICAL - free space: / 1423 MB (10% inode=53%): '},
'HTTP': {'service': 'HTTP', 'status': 'OK', 'info': 'HTTP OK: HTTP/1.1 301 Moved Permanently - 529 bytes in 0.000 second response time'},
'SSH': {'service': 'SSH', 'info': 'connect to address 127.0.0.1 and port 22: Connection refused'},
'Total Processes': {'service': 'Total Processes', 'status': 'OK', 'info': 'PROCS OK: 12 processes'}}

status
  queries the *extinfo.cgi* endpoint and parses the table to pull the same information
  (with the addition of last-check) as summary but for a single service

>>> icinga.status('testhost', 'Current Load')
{'service': 'Current Load',
'state': '  OK   (for  0d  1h 50m 10s)',
'info': 'OK - load average: 0.38, 0.33, 0.31',
'last-check': '2018-09-29 17:22:07'}

downtime
  queries the *cmd.cgi* endpoint to post a downtime for a particular host or service host. Returns True/False.
  service, expire_timedate, and msg are optional. Method defaults to a timedate of 1 hour.
  expire_timedate expects a dictionary with keys matching datetime.timedelta parameters.

>>> icinga.downtime(host='localhost', service='Disk Space', expire_timedate={'hours': 1}, msg='until logrotate'))
True

.. |License| image:: https://img.shields.io/pypi/l/icingapy.png
   :target: https://pypi.python.org/pypi/icingapy
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/icingapy.png
   :target: https://pypi.python.org/pypi/icingapy
.. |PyPI Version| image:: https://img.shields.io/pypi/v/icingapy.png
   :target: https://pypi.python.org/pypi/icingapy
.. |Build Status| image:: https://travis-ci.com/GenPage/icingapy.svg?branch=master
   :target: https://travis-ci.com/GenPage/icingapy
.. |Coverage Status| image:: https://codecov.io/gh/GenPage/icingapy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/GenPage/icingapy
