#!/usr/bin/python

from datetime import datetime, timedelta
from typing import AnyStr, Dict

import requests
from bs4 import BeautifulSoup

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class IcingaClient:
    """
    This represents the client to interact with Icinga
    """

    def __init__(self, host: AnyStr, username: AnyStr, password: AnyStr):
        """
        Initializes a new client with an Icinga host
        :param host: Icinga host
        :param username: Icinga username for basic auth
        :param password: Icinga password for basic auth
        """
        self.host = host
        self.username = username
        self.password = password

    def summary(self, host: AnyStr) -> Dict:
        """

        :param host:
        :return:
        """
        payload = {'host': host}

        r = requests.get(self.host + '/cgi-bin/icinga/status.cgi', auth=(self.username, self.password), params=payload,
                         verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')

        summary = {}
        table = soup.find('table', attrs={'class': 'status'})
        if table:
            for row in table.findAll('tr', recursive=False):
                cols = row.find_all('td', recursive=False)
                serv = {}
                try:
                    service = cols[1].text.strip()
                    if service == '':
                        continue
                except IndexError:
                    continue

                serv['service'] = service

                status = row.find('td', attrs={'class', 'statusOK'})
                if status:
                    serv['status'] = status.text

                try:
                    info = cols[6]
                    if info:
                        serv['info'] = info.text
                except IndexError:
                    pass

                summary[serv['service']] = serv

        return summary

    def status(self, host: AnyStr, service: AnyStr) -> Dict:
        payload = {'host': host, 'service': service, 'type': 2}

        r = requests.get(self.host + '/cgi-bin/icinga/extinfo.cgi', auth=(self.username, self.password), params=payload,
                         verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('td', attrs={'class': 'stateInfoTable1'})
        if table:
            state = table.find_next('td', text='Current Status:').next_sibling.text.replace('\xa0', ' ')
            info = table.find_next('td', text='Status Information:').next_sibling.text
            lastcheck = table.find_next('td', text='Last Check Time:').next_sibling.text
            return {'service': service, 'state': state, 'info': info, 'last-check': lastcheck}
        else:
            return {}

    def downtime(self, host: AnyStr, service=None, expire_timedate=None, msg='') -> bool:
        if not expire_timedate:
            expire_timedate = {'hours': 1}

        payload = {
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': (datetime.utcnow() + timedelta(**expire_timedate)).strftime('%Y-%m-%d %H:%M:%S'),
            'com_data': str(msg),
            'cmd_mod': "2",
            'fixed': "1",
            'trigger': "0",
            'com_author': self.username,
            'btnSubmit': "Commit"
        }

        if service:
            payload['cmd_typ'] = "56"
            payload['hostservice'] = str(host) + "^" + str(service)
        else:
            payload['cmd_typ'] = "86"
            payload['host'] = str(host)

        r = requests.post(self.host + '/cgi-bin/icinga/cmd.cgi', data=payload, auth=(self.username, self.password),
                          verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')

        return bool(soup.find('div', attrs={'class': 'successMessage'}))
