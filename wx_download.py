#!/usr/bin/env python
#coding:utf-8
__author__ = 'lideqiang'

import time
from selenium import webdriver
from mayiproxy import generate_sign
from ua import getRandomUa

class SeleniumDownloaderBackend(object):

    def __init__(self):
        self.browser = self.get_browser()

    def get_browser(self):
        # 启动浏览器
        firefox_profile = webdriver.FirefoxProfile()
        #蚂蚁代理设置UA认证
        mayiAuthMd5, mayi_proxy, proxy_url, proxy_port = generate_sign()
        #动态获取UA，只返回一条
        getOnceUa = getRandomUa()
        #设置代理
        firefox_profile.set_preference("network.proxy.type", 1) # 1代表手动设置
        firefox_profile.set_preference("network.proxy.share_proxy_settings", True)  # 所有协议公用一种代理配置
        firefox_profile.set_preference("network.proxy.http", proxy_url)
        firefox_profile.set_preference("network.proxy.http_port", proxy_port)
        firefox_profile.set_preference("network.proxy.ssl", proxy_url)
        firefox_profile.set_preference("network.proxy.ssl_port", proxy_port)

        user_agent = "||%s||%s||" % (getOnceUa,mayiAuthMd5)
        firefox_profile.set_preference("general.useragent.override", user_agent)
        #路径
        executable_path = "/usr/local/Cellar/geckodriver/0.20.0/bin/geckodriver"
        browser = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=executable_path)
        return browser

    def download_wechat(self, wechatid):
        """ 根据微信号最新文章 """
        self.visit_wechat_index(wechatid)
        return self.visit_wechat_topic_list(wechatid),self.browser

    def visit_wechat_index(self, wechatid):
        """ 访问微信首页，输入微信id，点击搜公众号 """
        browser = self.browser
        browser.get("http://weixin.sogou.com/")
        element_querybox = browser.find_element_by_name('query')
        element_querybox.send_keys(wechatid)
        time.sleep(2)
        try:
            element_search_btn = browser.find_element_by_xpath("//input[@value='搜公众号']")
            print browser.title
            element_search_btn.click()
        except Exception,e:
            print Exception,":",e
            browser.quit()

    def visit_wechat_topic_list(self, wechatid):
        """ 找到微信号，并点击进入微信号的文章列表页面 """
        browser = self.browser
        # 找到搜索列表第一个微信号, 点击打开新窗口
        element_wechat = browser.find_element_by_xpath("//div[@class='txt-box']/p[@class='info']/label")
        element_wechat_title = browser.find_element_by_xpath("//div[@class='txt-box']/p[@class='tit']/a")
        if element_wechat and element_wechat.text == wechatid:
            # element_wechat_title.click()
            # 获取返回的url
            href = element_wechat_title.get_attribute('href')
            return href
        else:
            return False

