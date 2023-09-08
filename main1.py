# -*- coding: utf-8 -*-
import requests
import os
import json

def main():
    r = 1
    # 格式 [{"web":"https://ikuuu.art","accounts":["account1,password1","account2.com,password2"]},{"web":"https://portx.cc","accounts":["account1,password1"]}]    
    # data = json.loads(simple_config)
    
    data = json.loads(os.environ['IKUUU_JSON_CONFIG'])
    
    for obj in data:
        # 遍历对象的键值对
        web = obj['web']
        for e in obj['accounts']:
            print("----执行第" + str(r) + "个账号---------")
            email = e.split(',')[0]
            passwd = e.split(',')[1]
            print(f"web:{web}: {email[0:3]}")
            sign_in(web, email, passwd)
            r += 1

def sign_in(web, email, passwd):
    try:
        body = {"email" : email,"passwd" : passwd,}
        headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        resp = requests.session()
        login_url = web+'/auth/login'
        resp.post(login_url, headers=headers, data=body)
        sign_url = web+'/user/checkin'
        ss = resp.post(sign_url).json()
#         print(ss)
        if 'msg' in ss:
            print(ss['msg'])
    except Exception as e:
        print('请检查帐号配置是否错误')
        print("发生异常：", str(e))

if __name__ == '__main__':
    main()