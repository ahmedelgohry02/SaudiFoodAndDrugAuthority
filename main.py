# Importing the desired libraries
import pandas as pd
import time
from selenium.webdriver import Keys, ActionChains
import pickle
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


## Options for the driver and creating the driver
options = webdriver.ChromeOptions()
options.add_argument("disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")
options.add_argument('--log-level=1')

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(200)
driver.set_script_timeout(200)


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
def main(driver,start,no_pages,d) :
    # dic = {
    #     "اسم الشركة": [],
    #     "رقم السجل التجاري": [],
    #     "نوع الترخيص": [],
    #     "نوع النشاط": [],
    #     "رقم الترخيص": [],
    #     "المدينة": [],
    #     "رقم التواصل": [],
    #     "البريد الإلكتروني": [],
    #     "تاريخ انتهاء الترخيص": [],
    #     "مصنع": [],
    #     "نشاط": [],
    #     "مجال الغذاء": [],
    #     "مجال مستحضرات التجميل": [],
    #     "مجال الأجهزة الطبية": [],
    #     "مجال الدواء": [],
    #     "مجال الأعلاف": [],
    #     "مجال المبيدات": []
    # }
    dic = {
        "اسم الشركة": [],
        "رقم الترخيص ": [],
        "رقم قائمة الاجهزة الطبية" : [],
        "نوع الجهاز": [],
        "وصف المنتج ": [],
        "الفئة ": [],
        "التصنيف": [],
        "gmdn ": [],
        "الممثل معتمد ": [],
        "تاريخ انتهاء ": [],
        "رقم تعريف الجهاز للمصنع": [],
        "الشركة الصانعة": [],
        " رقم الموديل": [],
        "الحالة  ": [],
        "النوع  ": [],
        "الاسم التجاري لملحقات الجهاز": [],
        "وصف ملحقات الجهاز": [],
        "ملحقات الجهاز GMDN": []
    }
    titles = list(dic.keys())
    all_results = pd.DataFrame(dic)
    # driver.get(rf"https://www.sfda.gov.sa/ar/licensed-establishments-list?pg=1")
    driver.get(rf"https://www.sfda.gov.sa/ar/medical-equipment-list?pg=1")
    
    load_cookies()
    time.sleep(2)
    try : 
        for i in range(start,no_pages+1) :
            print(f"--------------------Scraping Page Number {i} -----------------")
            # driver.get(rf"https://www.sfda.gov.sa/ar/licensed-establishments-list?pg={i}")
            driver.get(rf"https://www.sfda.gov.sa/ar/medical-equipment-list?pg={i}")
            
            save_cookies()
            loaded = WebDriverWait(driver, 1000).until(
                EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'التفاصيل')]"))
            )
            
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
                first = True
                for row in rows : 
                    data = row.find_elements(By.TAG_NAME , "td")
                    if first : 
                        time.sleep(.5)
                        first = False
                    txt = data[1].text.strip()
                    # print(title ,txt)
                    item_data[f"{titles[t]}"] = txt
                    t+=1
                # print(item_data)
                df = pd.DataFrame([item_data])
                # print(item_data)
                df = df.map(lambda x: x.encode('unicode_escape').
                decode('utf-8') if isinstance(x, str) else x)
                all_results = pd.concat([all_results, df], ignore_index=True)
                
                ActionChains(driver)\
                    .send_keys(Keys.ESCAPE)\
                    .perform()
            all_results.to_excel(f"data{d}.xlsx", index=False)
            if all_results.shape[0] >2000:
                all_results = pd.DataFrame(dic)
                d+=1
            print(len(buttons))
            if len(buttons) == 0 :
                with open("errorPages.txt", "a") as file:
                # Add a new line
                    file.write(f"\n{i}")
        return i ,d
    except Exception as e:
        with open("errorPages.txt", "a") as file:
                # Add a new line
                    file.write(f"\n{i}")
        print(e)
        return i+1,d




## Run the script
if __name__ == "__main__":
    end = 12000
    start = 11688
    d = 89

    while True : 
        s,w = main(driver,start,end ,d)
        if s == end :
            break
        else :
            start = s
            d = w+1
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(200)
            driver.set_script_timeout(200)
    print(d)

    

