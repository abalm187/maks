from keep_alive import keep_alive
keep_alive()
parameters = {
    "community-link": "http://aminoapps.com/c/ldrm-lkwry"
}

import os
import time
import json
import hmac
import base64
import random
os.system("pip3 install requests flask json_minify")
try:
    import requests
    from flask import Flask
    from json_minify import json_minify
except:
    os.system("pip3 install requests flask json_minify")
finally:
    import requests
    from flask import Flask
    from json_minify import json_minify

from threading import Thread
from uuid import uuid4
from hashlib import sha1

flask_app = Flask('')

@flask_app.route('/')
def home(): return " ~~8:> \n\t\t~~8:>"

def run(): flask_app.run(host = '0.0.0.0', port = random.randint(2000, 9000))

class Client:
    def __init__(self):
        self.api = "https://service.narvii.com/api/v1"
        self.device_Id = self.generate_device_Id()
        self.headers = {"NDCDEVICEID": self.device_Id, "SMDEVICEID": "b89d9a00-f78e-46a3-bd54-6507d68b343c", "Accept-Language": "en-EN", "Content-Type": "application/json; charset=utf-8", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)", "Host": "service.narvii.com", "Accept-Encoding": "gzip", "Connection": "Keep-Alive"}
        self.sid, self.auid = None, None

    def generate_device_Id(self):
        identifier = os.urandom(20)
        return ("32" + identifier.hex() + hmac.new(bytes.fromhex("76b4a156aaccade137b8b1e77b435a81971fbd3e"), b"\x32" + identifier, sha1).hexdigest()).upper()

    def generate_signature_message(self, data):
        signature_message = base64.b64encode(bytes.fromhex("32") + hmac.new(bytes.fromhex("fbf98eb3a07a9042ee5593b10ce9f3286a69d4e2"), data.encode("utf-8"), sha1).digest()).decode("utf-8")
        self.headers["NDC-MSG-SIG"] = signature_message
        return signature_message

    def login(self, email: str, password: str):
        data = json.dumps({"email": email, "secret": f"0 {password}", "deviceID": self.device_Id, "clientType": 100, "action": "normal", "timestamp": (int(time.time() * 1000))})
        self.generate_signature_message(data = data)
        request = requests.post(f"{self.api}/g/s/auth/login", data = data, headers = self.headers)
        try: self.sid, self.auid = request.json()["sid"], request.json()["auid"]
        except: pass
        return request.json()

    def send_active_object(self, comId: int, start_time: int = None, end_time: int = None, timers: list = None, tz: int = -time.timezone // 1000):
        data = {"userActiveTimeChunkList": [{"start": start_time, "end": end_time}], "timestamp": int(time.time() * 1000), "optInAdsFlags": 2147483647, "timezone": tz}
        if timers: data["userActiveTimeChunkList"] = timers
        data = json_minify(json.dumps(data))
        self.generate_signature_message(data = data)
        request = requests.post(f"{self.api}/x{comId}/s/community/stats/user-active-time?sid={self.sid}", data = data, headers = self.headers)
        return request.json()

    def watch_ad(self): return requests.post(f"{self.api}/g/s/wallet/ads/video/start?sid={self.sid}", headers = self.headers).json()

    def get_from_link(self, link: str): return requests.get(f"{self.api}/g/s/link-resolution?q={link}", headers = self.headers).json()

    def lottery(self, comId, time_zone: str = -int(time.timezone) // 1000):
        data = json.dumps({"timezone": time_zone, "timestamp": int(time.time() * 1000)})
        self.generate_signature_message(data = data)
        request = requests.post(f"{self.api}/x{comId}/s/check-in/lottery?sid={self.sid}", data = data, headers = self.headers)
        return request.json()

    def join_community(self, comId: int, inviteId: str = None):
        data = {"timestamp": int(time.time() * 1000)}
        if inviteId: data["invitationId"] = inviteId
        data = json.dumps(data)
        self.generate_signature_message(data=data)
        request = requests.post(f"{self.api}/x{comId}/s/community/join?sid={self.sid}", data = data, headers = self.headers)
        return request.json()

class App:
    def __init__(self):
        self.client = Client()
        extensions = self.client.get_from_link(parameters["community-link"])["linkInfoV2"]["extensions"]
        self.comId = extensions["community"]["ndcId"]
        try: self.invitationId = extensions["invitationId"]
        except: self.invitationId = None 
    def tzc(self): return int("+300")
    def generation(self, email: str, password: str) -> None:
        start_time = time.time()-3601
        while True:
            if time.time() - start_time >= 3600: 
                try:
                    print(f"\n[\033[1;31mcoins-generator\033[0m][\033[1;34mlogin\033[0m][{email}]: {self.client.login(email = email, password = password)['api:message']}.")
                    print(f"[\033[1;31mcoins-generator\033[0m][\033[1;36mjoin-community\033[0m]: {self.client.join_community(comId = self.comId, inviteId = self.invitationId)['api:message']}.")
                    print(f"[\033[1;31mcoins-generator\033[0m][\033[1;32mlottery\033[0m]: {self.client.lottery(comId = self.comId, time_zone = self.tzc())['api:message']}")
                    print(f"[\033[1;31mcoins-generator\033[0m][\033[1;33mwatch-ad\033[0m]: {self.client.watch_ad()['api:message']}.")
                    for i2 in range(25):
                        time.sleep(5)
                        print(f"[\033[1;31mcoins-generator\033[0m][\033[1;35mmain-proccess\033[0m][{email}]: {self.client.send_active_object(comId = self.comId, timers = [{'start': int(time.time()), 'end': int(time.time()) + 300} for _ in range(50)], tz = self.tzc())['api:message']}.")
                        print(f"[\033[1;31mcoins-generator\033[0m][\033[1;25;32mend\033[0m][{email}]: Finished.")
                        start_time = time.time()
                except Exception as error: print(f"[\033[1;31mC01?-G3?3R4?0R\033[0m]][\033[1;31merror\033[0m]]: {error}")
            else:
                print('3600 seconds haven\'t passed yet.')

    def run(self):
        print("COIN GENERATOR ")
        with open("accounts.json", "r") as emails:
            emails = json.load(emails)
            print(f"{len(emails)} Accounts loaded")
            for account in emails:
                self.client.device_Id = account["device"]
                self.client.headers["NDCDEVICEID"] = self.client.device_Id
                self.generation(email = account["email"], password = account["password"])
                    

if __name__ == "__main__":
    #Thread(target=run).start()
    App().run()
