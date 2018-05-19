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
import requests  
import pytesseract  
from PIL import Image,ImageEnhance 
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
 
#截图或验证码图片保存地址  
screenImg = "/Users/lovechunqiu/work/selenium_verifyCode/upload/wx.png"  

""" 启动并返回浏览器，使用firefox """
# 启动浏览器
firefox_profile = webdriver.FirefoxProfile()
browser = webdriver.Firefox(firefox_profile=firefox_profile)

#读取页面数据
browser.get(loginUrl)

assert "登录百度帐号" in browser.title 

#使用用户名和密码登陆
browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
#time.sleep(5)

#数据账号&密码(此处不提交)  
browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(username)  
browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(password)  
  
#此处可提前提交，让登录出错，页面出现验证码  
browser.find_element_by_id("TANGRAM__PSP_3__submit").click()  
#延迟几秒，让验证码加载出来
time.sleep(4)
#browser.quit()

#获取验证码URL地址  
imgsrc = browser.find_element_by_id("TANGRAM__PSP_3__verifyCodeImg").get_attribute('src')  
#print imgsrc

#如果匹配验证码路径成功（说明有提示输入验证码），则需读取验证码！  
if re.match(r'https://passport.baidu.com/(passApi/img|cgi-bin/genimage).*', imgsrc):  
    #浏览器页面截屏  
    browser.get_screenshot_as_file(screenImg)  
    #定位验证码位置及大小  
    location = browser.find_element_by_id('TANGRAM__PSP_3__verifyCodeImg').location  
    size   = browser.find_element_by_id('TANGRAM__PSP_3__verifyCodeImg').size  
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
    #再次读取识别验证码  
    img  = Image.open(screenImg)  
    code = pytesseract.image_to_string(img)  
    browser.find_element_by_id("TANGRAM__PSP_3__verifyCode").send_keys(code.strip())  
    #输出识别码
    print(code.strip())  

#提交数据
browser.find_element_by_id("TANGRAM__PSP_3__submit").click()  

time.sleep(10)
browser.quit()





