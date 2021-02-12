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
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

import time
import sys

chrome_driver_path ="D:\Projects\yahooFinRating\chromedriver"
#chrome_driver_path ="/mnt/d/Projects/yahooFinRating/chromedriver"
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--window-size=1400x1000")
options.add_argument('headless') #por alguna razon no funciona headless


def extraeHtml(webdriver,pizarra):    
    url='https://finance.yahoo.com/quote/{pizarra}/analysis?p={pizarra}'.format(pizarra=pizarra)
    with webdriver as driver:        
        driver.get(url)
        items={
            'rating':'NA',
            'PE':'NA'            
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
        
             

        url='https://finance.yahoo.com/quote/{pizarra}?p={pizarra}'.format(pizarra=pizarra)
        driver.get(url)
        
        try:
            wait.until(presence_of_element_located((By.XPATH,"//td[@data-test='EPS_RATIO-value']")))
            search = driver.find_element_by_xpath("//td[@data-test='EPS_RATIO-value']")          
            items['PE']=search.text
        except TimeoutException:
            pass
       
        print(items)
        driver.close()
        return items


if __name__ =='__main__':
    csv_file=open('data.csv', encoding="utf8")
    csv_reader=csv.reader(csv_file,delimiter='\t')
    f=open('scrapeado.csv','w+')   
    f.write('pizarra\tdescripcion\trating\tPE\n')       
    for row in csv_reader:
        webdriver= WD.Chrome(executable_path=chrome_driver_path, options=options)
        
        print(row[0])
        items=extraeHtml(webdriver,row[0])
        string=row[0]+'\t'+row[1]
        if items!=False:
            string+='\t'+items['rating']+'\t'+items['PE']+'\n'
        else:
            string+='\tNA\n'
        f.write(string)    
        
    f.close()
            

