import time
import pandas
import xlsxwriter
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
data=pandas.read_excel('adrrr.xlsx')#读取1.xlsx文件
xls=xlsxwriter.Workbook('adr.xlsx')#创建ad.xlsx文件
sht1=xls.add_worksheet('sheet1')#创建sheet1工作表
sht1.write(0,0,'地址')#A1
sht1.write(0,1,'Walk Score')#B1
sht1.write(0,2,'Transit Score')#C1
sht1.write(0,3,'Bike Score')#D1
x=1#下标
browser = webdriver.Chrome()#启动Google驱动
for i in data.values:
    url = 'https://www.walkscore.com/score/'
    browser.get(url)#访问网站
    Wait(browser, 10).until(EC.presence_of_element_located((By.ID, 'gs-street')))#等待搜索框加载完毕
    browser.find_element(by=By.ID,value='gs-street').clear()#清空搜索框
    browser.find_element(by=By.ID, value='gs-street').send_keys(i[1]+',New York,NY')#输入搜索数据到搜索框中
    time.sleep(0.3)#等待0.3秒
    browser.find_element(by=By.ID,value='score_btn').click()#单击Score按钮
    time.sleep(0.3)#等待0.3秒
    try:
        Wait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'clearfix.score-div')))#等待所需数据加载完毕
    except:
        continue
    html=etree.HTML(browser.page_source)#对HTML文本进行初始化
    print(i[1]+',New York,NY',end='\t')
    sht1.write(x, 0 ,i[1]+',New York,NY')
    for i in html.xpath('//div[@class="clearfix score-div"]'):#使用for循环获取所需数据并写入文件中
        if i.xpath('div/img/@alt')[0].split()[1]=='Walk':
            sht1.write(x,1,i.xpath('div/img/@alt')[0].split()[0])
            print(i.xpath('div/img/@alt')[0].split()[0], end='\t')
        elif i.xpath('div/img/@alt')[0].split()[1]=='Transit':
            sht1.write(x,2,i.xpath('div/img/@alt')[0].split()[0])
            print(i.xpath('div/img/@alt')[0].split()[0], end='\t')
        elif i.xpath('div/img/@alt')[0].split()[1]=='Bike':
            sht1.write(x,3,i.xpath('div/img/@alt')[0].split()[0])
            print(i.xpath('div/img/@alt')[0].split()[0], end='\t')
    print()
    x+=1
xls.close()#关闭保存数据
