# -*- coding: utf-8 -*-

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re

"""
通过request库实现登录
"""
agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookies未能加载")


def get_captcha():

    import time
    t = str(int(time.time() * 1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()
    from PIL import Image
    try:
        im = Image.open("captcha.jpg")
        im.show()
        im.close()
    except:
        pass
    captcha = input("请输入验证码\n>>>>>>")
    return captcha


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)".*', response.text, re.DOTALL)
    if match_obj:
        # print (match_obj.group(1))
        return (match_obj.group(1))
    else:
        return ""


def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print("手机号登录")
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xsrf": get_xsrf,
            "phone_num": account,
            "password": password,
            "captcha": get_captcha()
        }

        response_text = session.post(post_url, data=post_data, headers=header)
        session.cookies.save()
    else:
        if "@" in account:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": get_xsrf,
                "phone_num": account,
                "password": password
            }
            response_text = session.post(post_url, data=post_data, headers=header)
            session.cookies.save()


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def is_login():
    # 通过个人中心302是否登录
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirect=False)
    if response.status_code != 200:
        return False
    else:
        return True


if __name__ == "__main__":
    # zhihu_login("111","1111")
    # get_xsrf()
    get_captcha()
