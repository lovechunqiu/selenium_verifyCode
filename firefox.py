#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lideqiang87@gmail.com'

from selenium import webdriver
import time
from mayiproxy import generate_sign
from ua import getRandomUa

#from pyvirtualdisplay import Display
#display = Display(visible=0, size=(800, 600))
#display.start()

# 启动浏览器
firefox_profile = webdriver.FirefoxProfile()
#蚂蚁代理设置UA认证
mayiAuthMd5, mayi_proxy, proxy_url, proxy_port = generate_sign()
#print generate_sign()
#time.sleep(1000)

#动态获取UA，只返回一条
getOnceUa = getRandomUa()
#设置代理
firefox_profile.set_preference("network.proxy.type", 1) # 1代表手动设置
firefox_profile.set_preference("network.proxy.share_proxy_settings", True)  # 所有协议公用一种代理配置
firefox_profile.set_preference("network.proxy.http", proxy_url)
firefox_profile.set_preference("network.proxy.http_port", int(proxy_port))
firefox_profile.set_preference("network.proxy.ssl", proxy_url)
firefox_profile.set_preference("network.proxy.ssl_port", int(proxy_port))

user_agent = "||%s||%s||" % (getOnceUa,mayiAuthMd5)
firefox_profile.set_preference("general.useragent.override", user_agent)

browser = webdriver.Firefox(firefox_profile=firefox_profile)

#读取页面数据
target_url = "http://puffsite.198791.com/"
browser.get(target_url)

print browser.title
#print browser.page_source 
print 'Browser will close'
browser.quit()
print 'Browser closed'


