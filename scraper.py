from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, datetime
import pandas as pd
import os
import boto3
import logging
from botocore.exceptions import ClientError
from sqlalchemy import create_engine





#------------- Scraper Class---------------
class Scraper: 

    #------------- Initiate Chrome Browser---------------
    def __init__(self,url:str = 'https://www.hotukdeals.com/tag/electronics?page=1'):
        self.listofdict = list()
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.driver.get(url)
        self.s3_client = boto3.client('s3', aws_access_key_id ='',aws_secret_access_key = '', region_name = 'eu-west-2')

    #------------- Accept the Cookies---------------
    def accecept_cookies(self):
        try:
            time.sleep(5)
            self.driver.find_element(By.XPATH,'//button[@data-t="acceptAllBtn"]').click()
        except TimeoutException:
            print('No Cookies Found')

    #------------- Data Scrape from Container & Move to Next Page---------------
    def find_container(self):
        driver = self.driver
        time.sleep(5)
        #count the number of pages
        count = 0
        for pagenum in range(1,501):
            driver.get(f'https://www.hotukdeals.com/tag/electronics?page={pagenum}')
            time.sleep(5)
            #list the page container
            productcontainer = driver.find_elements(By.XPATH, '//article[@data-t="thread"]')
            print(len(productcontainer))        
            for singleproduct in productcontainer: 
                #dict to store data temporary          
                datadict = dict()
                try:datadict['Image'] = singleproduct.find_element(By.XPATH, './/img').get_attribute('src')
                except:datadict['Image'] = ''
                try:datadict['Title'] = singleproduct.find_element(By.XPATH, './/strong[@class="thread-title "]/a').text
                except:datadict['Title'] = ''
                try:datadict['Link'] = singleproduct.find_element(By.XPATH, './/a[@rel="nofollow noopener"]').get_attribute('href')
                except:
                    try:datadict['Link'] = singleproduct.find_element(By.XPATH, './/a[@rel="nofollow"]').get_attribute('href')
                    except:datadict['Link'] = ''
                try:datadict['Price'] = singleproduct.find_element(By.XPATH, './/span[@class="overflow--wrap-off"]/span').text
                except:datadict['Price'] = ''
                print(datadict)
                #append data in main list
                self.listofdict.append(datadict)
            #add the value for page number counting
            count+= 1
            #here you can set number of pages
            if count == 1:
                break
        time.sleep(5)
        driver.quit()
    
    #------------- Save Data ---------------
    def save_data(self):
        date = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        df = pd.DataFrame.from_dict(self.listofdict)
        print('\n\n  ************DATA FRAME**************')
        print(df)
        df.to_csv(f'HotukDeals-{date}.csv',index=False)
        df.to_json(f'HotukDeals-{date}.json') 
        df.to_json(f'HotukDealsData.json')       
        print('Saved Data in CSV!!')
        print('Saved Data in JSON!!')
    
    
    def upload_file(self):
        

        self.session = boto3.Session(
        aws_access_key_id= '',
        aws_secret_access_key='',
        region_name= ''
        )
        
        response = self.s3_client.upload_file(
            'HotukDealsData.json', 'dealsuk2022', 'HotukDealsData.json')
        s3 = self.session.resource('s3')
        
        s3.meta.client.upload_file('/Documents/UNI/AI/Data_Collection_Pipeline/HotukDealsData.json','HotukDealsData.json')
        s3.Bucket('dealsuk2022').upload_file('/Documents/UNI/AI/Data_Collection_Pipeline/HotukDealsData.json','HotukDealsData.json')

    def upload_to_RDS(self):
         
        DATABASE_TYPE = 'database_type'
        DBAPI = 'dbapi'
        ENDPOINT = 'endpoint' 
        USER = 'user'
        PASSWORD = 'password'
        PORT = 'port'
        DATABASE = 'database'

        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}").connect()
        
        self.deals_df = pd.DataFrame.from_dict(self.datadict)
        
        self.sofa_df.to_sql("deals_data_samples", engine, if_exists='replace')
        print("deals can be view an sql database")

        

        

    



if __name__ == "__main__":
    bot = Scraper()
    bot.accecept_cookies()
    try:
        bot.find_container()
        bot.save_data()
        bot.upload_file()
    except:
        bot.save_data()