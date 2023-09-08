# -*- coding: utf-8 -*-
import json
import requests
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#账户
EMAIL = os.environ["EMAILS"]
PASSWORD = os.environ["PASSWORD"]
DOMAIN = os.environ["DOMAIN"]

class SSPANEL:
    name = "SSPANEL"

    def __init__(self, check_item):
        self.check_item = check_item

    def sign(self, email, password, url):
        email = email.replace("@", "%40")
        try:
            session = requests.session()
            session.get(url=url, verify=False)
            login_url = url + "/auth/login"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            post_data = "email=" + email + "&passwd=" + password + "&code="
            post_data = post_data.encode()
            session.post(login_url, post_data, headers=headers, verify=False)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Referer": url + "/user",
            }
            response = session.post(url + "/user/checkin", headers=headers, verify=False)
            msg = response.json().get("msg")
        except Exception as e:
            msg = "签到失败"
        return msg

    
    def main(self):
        emails = self.check_item.get("email")
        password = self.check_item.get("password")
        url = self.check_item.get("url")

        for email in emails.split(","):
            sign_msg = self.sign(email=email, password=password, url=url)
            msg = [
                {"name": "帐号信息", "value": email[0:3]},
                {"name": "签到信息", "value": f"{sign_msg}"},
            ]
            msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
            print(msg)

        # 其他签到
        first = emails.split(",")[0]
        sign_msg = self.sign(email=first, password=password, url='https://portx.cc')
        print('portx:'+first[0:3]+sign_msg)
        return msg

if __name__ == "__main__":
    _check_item = {'email': EMAIL, 'password': PASSWORD, 'url': DOMAIN}
    SSPANEL(check_item=_check_item).main()
