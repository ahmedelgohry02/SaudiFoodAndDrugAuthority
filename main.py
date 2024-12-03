# Importing the desired libraries
import pandas as pd
from openpyxl import load_workbook
import time
from selenium.webdriver import Keys, ActionChains
import pickle
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from queue import Queue


## Options for the driver and creating the driver
options = webdriver.ChromeOptions()
options.add_argument("disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)


## Function to load cookies 
def load_cookies():
    if os.path.isfile("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

## Function to save cookies 
def save_cookies() :
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))



## Creating the main function 
def main(driver,no_pages) :
    dic = {
        "اسم الشركة": [],
        "رقم السجل التجاري": [],
        "نوع الترخيص": [],
        "نوع النشاط": [],
        "رقم الترخيص": [],
        "المدينة": [],
        "رقم التواصل": [],
        "البريد الإلكتروني": [],
        "تاريخ انتهاء الترخيص": [],
        "مصنع": [],
        "نشاط": [],
        "مجال الغذاء": [],
        "مجال مستحضرات التجميل": [],
        "مجال الأجهزة الطبية": [],
        "مجال الدواء": [],
        "مجال الأعلاف": [],
        "مجال المبيدات": []
    }
    titles = list(dic.keys())
    all_results = pd.DataFrame(dic)
    driver.get(rf"https://www.sfda.gov.sa/ar/licensed-establishments-list?pg=1")
    load_cookies()
    time.sleep(2)
    for i in range(1,no_pages+1) :
        print(f"--------------------Scraping Page Number {i} -----------------")
        driver.get(rf"https://www.sfda.gov.sa/ar/licensed-establishments-list?pg={i}")
        save_cookies()
        loaded = WebDriverWait(driver, 10000).until(
            EC.visibility_of_element_located((By.ID, "establishmentstable"))
        )
        time.sleep(5)
        
        ## Find the details buttons
        buttons = driver.find_elements(
                    By.XPATH, "//a[contains(text(),'التفاصيل')]"
                )
        
        for button in buttons : 
            item_data = {}
            button.click()
            table = driver.find_element(By.CLASS_NAME , "modal-body").find_element(By.TAG_NAME , "tbody")
            rows = table.find_elements(By.TAG_NAME , "tr")
            t= 0
            for row in rows : 
                data = row.find_elements(By.TAG_NAME , "td")
                txt = data[1].text.strip()
                # print(title ,txt)
                item_data[f"{titles[t]}"] = txt
                t+=1
            print(item_data)
            all_results = pd.concat([all_results, pd.DataFrame([item_data])], ignore_index=True)
            ActionChains(driver)\
                .send_keys(Keys.ESCAPE)\
                .perform()
        all_results.to_excel("data.xlsx", index=False)

        

        print(len(buttons))






## Run the script
if __name__ == "__main__":
    main(driver , 1)
    

    

