from bs4 import BeautifulSoup
import requests

url = r"https://www.sfda.gov.sa/ar/licensed-establishments-list?pg=1"
r = requests.get(url)
page = BeautifulSoup(r.text , "lxml")
table = page.find( id="establishmentstable")
print(table.find_all("tbody"))