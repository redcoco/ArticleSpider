# -*- coding: utf-8 -*-

from selenium import webdriver
import time


browser = webdriver.Chrome(executable_path="C:/Users/wenjuan/PycharmProjects/chromedriver.exe")

#模拟登陆知乎
# browser.get("https://www.zhihu.com/#signin")
#
# browser.find_element_by_css_selector(".qrcode-signin-container span.signin-switch-password").click()
#
# browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("15995848840")
#
# browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys(input("请输入密码\n>>>>>>"))
#
# # browser.find_element_by_css_selector(".Captcha-image").send_keys(input(">/n"))
# time.sleep(8)
# browser.find_element_by_css_selector(".view-signin button.sign-button").click()
# time.sleep(3)

#selenium模拟登录微博， 模拟鼠标下拉

browser.get("http://weibo.com/")
time.sleep(4)
browser.find_element_by_css_selector("#loginname").send_keys("liyao198705@sina.com")
browser.find_element_by_css_selector(".info_list.password .W_input").send_keys(input("请输入密码：\n"))
browser.find_element_by_css_selector(".info_list.login_btn .W_btn_a.btn_32px ").click()

# 实现模拟鼠标下拉滚动
for i in range(3):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    time.sleep(3)




page = browser.page_source

# browser.quit()
if __name__ == "__main__":
    print(page)
