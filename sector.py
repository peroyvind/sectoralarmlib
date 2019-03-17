import requests
import json
import sys

baseUrl = "https://mypagesapi.sectoralarm.net"
req = requests.session()

def login(userid, password):

    formdata = 'userID=' + userid + '&password=' + password

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

    #r = requests.session()
    r2 = req.post(baseUrl + '/User/Login?ReturnUrl=%2f', data=formdata, headers=headers)


def alarmstatus():
    r2 = req.post(baseUrl + '/Panel/GetOverview/')

    svar = json.loads(r2.text)


    if svar['Panel']['ArmedStatus'] == 'disarmed':
        return "OFF"
    elif svar['Panel']['ArmedStatus'] == 'armed':
        return "ON"

