#!/usr/bin/env python
#coding:utf-8
__author__ = 'lideqiang'

'''
    1、截取屏幕获取验证码
    2、反填验证码进行跳过验证
    3、用微信网站进行验证：http://weixin.sogou.com/weixin?type=1&query=jiaojiaoma8&ie=utf8
'''

from selenium import webdriver
import re  
from PIL import Image,ImageEnhance 
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#加载orc图像识别类
from verifyCode import getCode
from wx_download import SeleniumDownloaderBackend
 
#截图或验证码图片保存地址  
screenImg = "/Users/lovechunqiu/work/selenium_verifyCode/upload/wx.png"

"""
    获取链接步骤
    1、打开weixin.sogo.com页面：腾讯体育【txsports】
    2、填写一个公众号【weixin.sogou.com的验证码】暂时忽略不考虑
    3、通过浏览器点击第一篇文章
    4、判断是否有验证码【微信本身的验证码】
    5、OCR图像识别
"""

#实例化
wxDown   = SeleniumDownloaderBackend()
#示例：腾讯体育
wechatid = 'txsports'
#返回页面URL和浏览器实例
baseUrl, browser = wxDown.download_wechat(wechatid)

#判断baseUrl是否为false
if baseUrl == False:
    print 'error'
    browser.quit()

#读取页面数据
browser.get(baseUrl)

#assert "请输入验证码" in browser.title
if(browser.title != '请输入验证码'):
    print '不需要数据验证码'
    browser.quit()
else:
    #打印出当前时间
    print "startDate:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    #获取验证码URL地址
    imgsrc = browser.find_element_by_id("verify_img").get_attribute('src')
    print imgsrc
    #time.sleep(10)

    #如果匹配验证码路径成功（说明有提示输入验证码），则需读取验证码！
    if re.match(r'http://mp.weixin.qq.com/mp/verifycode.*', imgsrc):
        #浏览器页面截屏
        browser.get_screenshot_as_file(screenImg)
        #定位验证码位置及大小
        location = browser.find_element_by_id('verify_img').location
        size   = browser.find_element_by_id('verify_img').size
        left   = location['x']
        top    = location['y']
        right  = location['x'] + size['width']
        bottom = location['y'] + size['height']
        #print left,top,right,bottom
        #从文件读取截图，截取验证码位置再次保存
        """
            注意：这块有个坑，获取的数值都是float，需要强制转化成int，否则会报错
        """
        img = Image.open(screenImg).crop((int(left), int(top), int(right), int(bottom)))
        #img.show()
        #time.sleep(10)
        img = img.convert('L')           #转换模式：L | RGB
        img = ImageEnhance.Contrast(img) #增强对比度
        img = img.enhance(2.0)           #增加饱和度
        img.save(screenImg)
        """
            换别的OCR图像识别
        """
        code = getCode(screenImg)
        browser.find_element_by_id("input").send_keys(code.strip())
        #输出识别码
        print(code.strip())

    #提交数据
    browser.find_element_by_id("bt").click()
    time.sleep(2)
    #打印出当前时间
    print "endDate:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    browser.quit()







