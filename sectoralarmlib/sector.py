import requests
import json
import sys
import re


baseUrl = "https://mypagesapi.sectoralarm.net"
req = requests.session()
version = ''

class SectorAlarm:

    def __init__(self, username, password, siteid, panelcode):
        self.username = username
        self.password = password
        self.code = panelcode
        self.siteid = siteid

    def Login(self):

        formdata = 'userID=' + self.username + '&password=' + self.password

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,sv;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(sys.getsizeof(formdata)),
            "Upgrade-Insecure-Requests" : '1',
            "User-Agent" : "Safari/537.36"
        }

        response = req.post(baseUrl + '/User/Login?ReturnUrl=%2f', data=formdata, headers=headers)
        
        if "<title>Login</title>" in response.text:
            raise RuntimeError("Wrong username or password")
        elif "<title>Sector Alarm</title>" in response.text:
            x = re.findall("Scripts\/main.js\?(v.+)\"", response.text)
            global version
            version = x[0].split('\"',1)[0]
            return "ok"
            
    def AlarmStatus(self):
        self.Login()

        payload = { "id": self.siteid, "Version":version  }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/json;charset=UTF-8',
            "Content-Length": str(sys.getsizeof(payload)),
            'Connection': 'keep-alive',
            'User-Agent' : 'Safari/537.36'
        }

        response = req.post(baseUrl + '/Panel/GetOverview/', data=json.dumps(payload), headers=headers)

        svar = json.loads(response.text)    


        if svar['Panel']['ArmedStatus'] == 'disarmed':
            return "OFF"
        elif svar['Panel']['ArmedStatus'] == 'partialarmed':
            return "PARTIAL"
        else:
            return "ON"

    def Arm(self):
        self.Login()

        payload = { "ArmCmd":"Total", "PanelCode":self.code, "HasLocks":"false", "id":self.siteid }

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,sv;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(sys.getsizeof(payload)),
            "Upgrade-Insecure-Requests" : '1',
            "User-Agent" : "Safari/537.36"
        }

        response = req.post(baseUrl + '/Panel/ArmPanel/', data=payload, headers=headers)

        svar = json.loads(response.text)

        if svar["status"] != "success":
            raise RuntimeError("Something went wrong while arming the alarm.")
        else:
            return "Armed"

    def Disarm(self):
        self.Login()

        payload = { "ArmCmd":"Disarm", "PanelCode":self.code, "HasLocks":"false", "id":self.siteid }

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,sv;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(sys.getsizeof(payload)),
            "Upgrade-Insecure-Requests" : '1',
            "User-Agent" : "Safari/537.36"
        }

        response = req.post(baseUrl + '/Panel/ArmPanel/', data=payload, headers=headers)
        
        svar = json.loads(response.text)

        if svar["status"] != "success":
            raise RuntimeError("Something went wrong while disarming the alarm.")
        else:
            return "Disarmed"

    def ArmPartial(self):
        self.Login()

        payload = { "ArmCmd":"Partial", "PanelCode":self.code, "HasLocks":"false", "id":self.siteid }

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,sv;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(sys.getsizeof(payload)),
            "Upgrade-Insecure-Requests" : '1',
            "User-Agent" : "Safari/537.36"
        }

        response = req.post(baseUrl + '/Panel/ArmPanel/', data=payload, headers=headers)
        
        svar = json.loads(response.text)

        if svar["status"] != "success":
            raise RuntimeError("Something went wrong while partial arming the alarm.")
        else:
            return "PartialArmed"


    def GetTemps(self):
        temps = []

        self.Login()

        payload = { "id": self.siteid, "Version":version  }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/json;charset=UTF-8',
            "Content-Length": str(sys.getsizeof(payload)),
            'Connection': 'keep-alive',
            'User-Agent' : 'Safari/537.36'
        }

        response = req.post(baseUrl + '/Panel/GetTempratures/', data=json.dumps(payload), headers=headers)

        for temp in json.loads(response.text):
            temps.append((temp["Label"], temp["Temprature"]))


        return temps
        
