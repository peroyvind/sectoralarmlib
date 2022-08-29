import time
import requests
import json
import re
import urllib.parse

base_url = 'https://mypagesapi.sectoralarm.net'


class SectorAlarm:

    def __init__(self, username, password, siteid, panelcode):
        self.username = username
        self.password = password
        self.code = panelcode
        self.siteid = siteid
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

        # After logging in, wait this many seconds to avoid being subsequently rate-limited.
        self.login_cooldown_sec = 5

        self.session = requests.session()
        self.version = None
        self.logged_in = False

    def Login(self):
        if self.logged_in:
            return

        params = {
            'userID': self.username,
            'password': self.password,
        }
        formdata = urllib.parse.urlencode(params)

        headers = {
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.user_agent,
        }

        response = self.session.post(base_url + '/User/Login?ReturnUrl=%2f', data=formdata, headers=headers)
        response.raise_for_status()

        if '<title>Login</title>' in response.text:
            raise RuntimeError('Wrong username or password')

        if not '<title>Sector Alarm</title>' in response.text:
            raise RuntimeError('Login Failed')

        x = re.findall("Scripts\/main.js\?(v[^\"&]+)\"", response.text)
        self.version = x[0].split('\'', 1)[0]
        self.logged_in = True

        time.sleep(self.login_cooldown_sec)

    def AlarmStatus(self):
        self.Login()

        payload = {'id': self.siteid, 'Version': self.version}

        headers = {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': self.user_agent,
        }

        response = self.session.post(base_url + '/Panel/GetOverview/', data=json.dumps(payload), headers=headers)
        response.raise_for_status()

        svar = json.loads(response.text)

        if svar['Panel']['ArmedStatus'] == 'disarmed':
            return 'OFF'
        elif svar['Panel']['ArmedStatus'] == 'partialarmed':
            return 'PARTIAL'
        else:
            return 'ON'

    def Arm(self):
        self.Login()

        payload = {'ArmCmd': 'Total', 'PanelCode': self.code, 'HasLocks': 'false', 'id': self.siteid}

        headers = {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.user_agent,
        }

        response = self.session.post(base_url + '/Panel/ArmPanel/', data=payload, headers=headers)
        response.raise_for_status()

        svar = json.loads(response.text)

        if svar['status'] != 'success':
            raise RuntimeError('Something went wrong while arming the alarm.')
        else:
            return 'Armed'

    def Disarm(self):
        self.Login()

        payload = {'ArmCmd': 'Disarm', 'PanelCode': self.code, 'HasLocks': 'false', 'id': self.siteid}

        headers = {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.user_agent,
        }

        response = self.session.post(base_url + '/Panel/ArmPanel/', data=payload, headers=headers)
        response.raise_for_status()

        svar = json.loads(response.text)

        if svar['status'] != 'success':
            raise RuntimeError('Something went wrong while disarming the alarm.')
        else:
            return 'Disarmed'

    def ArmPartial(self):
        self.Login()

        payload = {'ArmCmd': 'Partial', 'PanelCode': self.code, 'HasLocks': 'false', 'id': self.siteid}

        headers = {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.user_agent,
        }

        response = self.session.post(base_url + '/Panel/ArmPanel/', data=payload, headers=headers)
        response.raise_for_status()

        svar = json.loads(response.text)

        if svar['status'] != 'success':
            raise RuntimeError('Something went wrong while partial arming the alarm.')
        else:
            return 'PartialArmed'

    def GetTemps(self):
        self.Login()

        temps = []

        payload = {'id': self.siteid, 'Version': self.version}

        headers = {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': self.user_agent,
        }

        response = self.session.post(base_url + '/Panel/GetTempratures/', data=json.dumps(payload), headers=headers)
        response.raise_for_status()

        for temp in json.loads(response.text):
            temps.append((temp['Label'], temp['Temprature']))

        return temps
