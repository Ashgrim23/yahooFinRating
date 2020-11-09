from bs4 import BeautifulSoup as soup
import requests
import csv
from selenium import webdriver as WD
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import time
import sys

chrome_driver_path ="D:\Projects\yahooFinRating\chromedriver"
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
#options.add_argument('headless') #por alguna razon no funciona headless

def evalRGB(rgb):
    if (rgb=="rgb(255, 77, 82)"):
        return 'BAJA'
    elif (rgb=="rgb(26, 197, 103)"):
        return 'SUBE'
    elif (rgb=="rgb(70, 78, 86)"):
        return 'MANTIENE'
    else:
        return 'NA'

def extraeHtml(webdriver,pizarra):    
    url='https://finance.yahoo.com/quote/{pizarra}/analysis?p={pizarra}'.format(pizarra=pizarra)
    with webdriver as driver:        
        driver.get(url)
        items={
            'rating':'NA',
            'current':'NA',
            'average':'NA',
            'low':'NA',
            'high':'NA',
            'valuacion':'NA',
            'trend_short':'NA',
            'trend_mid':'NA',
            'trend_long':'NA'
        }
        
        wait = WebDriverWait(driver, 10)

        try:
            search=driver.find_element_by_xpath("//span[@data-reactid='249']")      
        except NoSuchElementException:  
            return False
        
        actions = ActionChains(driver)  
        actions.move_to_element(search).perform()
        try:
            wait.until(presence_of_element_located((By.TAG_NAME,"figcaption")))
        except TimeoutException:
            pass
        
        search=driver.find_element_by_xpath("//span[@data-reactid='321']")              
        actions.move_to_element(search).perform()

        try:
            wait.until(presence_of_element_located((By.XPATH,"//div[@data-test='rec-rating-txt']")))
            search = driver.find_element_by_xpath("//div[@data-test='rec-rating-txt']")        
            items['rating']=search.text        
        except TimeoutException:
            pass
        
        try:
            search = driver.find_element_by_xpath("//section[@data-test='price-targets']")
            precios=search.text.replace("\n"," ").split(" ")
            items['current']=precios[5]
            items['average']=precios[7]
            items['low']=precios[9]
            items['high']=precios[11]
        except NoSuchElementException:
            pass
        

        url='https://finance.yahoo.com/quote/{pizarra}?p={pizarra}'.format(pizarra=pizarra)
        driver.get(url)
        
        wait.until(presence_of_element_located((By.ID,"fr-val-mod")))
        search=driver.find_element_by_id("fr-val-mod")   
        items['valuacion']=search.text.replace("\n"," ").split(" ")[3]
        
        idShort=63
        idMid=72
        idLong=81
        try:
            wait.until(presence_of_element_located((By.XPATH,'//li[@data-reactid="{idShort}"]'.format(idShort=idShort))))
        except TimeoutException:
            idShort-=2
            idMid-=2
            idLong-=2        
                  
        wait.until(presence_of_element_located((By.XPATH,'//li[@data-reactid="{idShort}"]'.format(idShort=idShort))))
        
        


        search=driver.find_element_by_xpath('//li[@data-reactid="{idMid}"]'.format(idMid=idMid))
        svg=search.find_element_by_tag_name('svg')
        style=svg.get_attribute("style").split(";")[0].split(":")[1].strip()
        items['trend_short']=evalRGB(style)

        search=driver.find_element_by_xpath('//li[@data-reactid="{idMid}"]'.format(idMid=idMid))
        svg=search.find_element_by_tag_name('svg')
        style=svg.get_attribute("style").split(";")[0].split(":")[1].strip()
        items['trend_mid']=evalRGB(style)
        
        search=driver.find_element_by_xpath('//li[@data-reactid="{idLong}"]'.format(idLong=idLong))
        svg=search.find_element_by_tag_name('svg')
        style=svg.get_attribute("style").split(";")[0].split(":")[1].strip()
        items['trend_long']=evalRGB(style)

        print(items)
        driver.close()
        return items


if __name__ =='__main__':
    csv_file=open('data.csv')
    csv_reader=csv.reader(csv_file,delimiter='\t')
    f=open('scrapeado.csv','w+')   
    f.write('pizarra\tdescripcion\trating\tcurrent\taverage\tlow\thigh\tvaluacion\ttrend_short\ttrend_mid\ttrend_long\n')       
    for row in csv_reader:
        webdriver= WD.Chrome(executable_path=chrome_driver_path, options=options)
        print(row[0])
        items=extraeHtml(webdriver,row[0])
        string=row[0]+'\t'+row[1]
        if items!=False:
            string+='\t'+items['rating']+'\t'+items['current']+'\t'+items['average']+'\t'+items['low']+'\t'+items['high']+'\t'+items['valuacion']+'\t'+items['trend_short']+'\t'+items['trend_mid']+'\t'+items['trend_long']+'\n'
        else:
            string+='\tNA\n'
        f.write(string)    
        
    f.close()
            

