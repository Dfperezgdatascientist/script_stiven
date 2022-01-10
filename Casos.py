# -*- coding: utf-8 -*-

## Librerias
import os
import sys
import time
import shutil
import datetime
import pandas as pd
from openpyxl import *
from pyautogui import *
from automagica import *
from datetime import date
from pyautogui import sleep
from selenium import webdriver
import win32com.client as win
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

today = datetime.date.today()
#today = datetime.datetime(2020, 10, 2, 14, 13, 24, 154621)
now = today - datetime.timedelta(days=31)
fec1 = now.strftime("%m/%d/%Y")

WINDOW_SIZE = "3000,3000"

chrome_options = Options()  

chrome_options.add_experimental_option("prefs", {
  "download.default_directory": r"D:\Emergencia\Descargas\IDCASOS",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
#chrome_options.binary_location = CHROME_PATH
#chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)


browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)

carpeta = 'D:/Emergencia/Descargas/IDCASOS'
extension = ".xls"
one = ".xlsx"
os.chdir(carpeta) 

for i in os.listdir(carpeta): #recorrer todos los items de la carpeta
    if i.endswith(one): #comprueba la extensión .xlsx  
        rcuadro= os.path.abspath(i) #obtiene la ruta completa de los archivos  
        os.remove(rcuadro)

ruta = '//10.1.1.7/01 Oficina Planeación y Control/01 Analytics/Sebas/ClasificaciondeCasosOficial/'+'/CasosTemporal'+'.xlsx' 

movil = '//10.1.1.7/01 Oficina Planeación y Control/01 Analytics/Daniel/TipiGobAnt/'+'/CasosTemporal'+'.xlsx'

print('open browser')
#browser = Chrome()
browser.get('http://apolo/formgobernacion/index.php?from=L2Zvcm1nb2Jlcm5hY2lvbi9tYW5hZ2VfZm9ybXMucGhw')
browser.maximize_window()
wait(1)
user = browser.find_element_by_id('admin_username')
user.send_keys('efrain.galvis@emtelco.com.co')
enter = browser.find_element_by_id('admin_password')
enter.send_keys('Emtelco2020')
log = browser.find_element_by_xpath('//*[@id="submit_button"]')
log.click()
wait(1)
pag2 = browser.find_element_by_xpath('//*[@id="pagebtn_3"]')
pag2.click()
wait(1)

gov = browser.find_element_by_xpath('//*[@id="liform_116332"]/div[4]/h3')
gov.click()
wait(1)
entries = browser.find_element_by_xpath('//*[@id="liform_116332"]/div[5]/a')
entries.click()
filt = browser.find_element_by_xpath('//*[@id="entry_filter"]')
filt.click()
fecha = browser.find_element_by_xpath('//*[@id="filterkeyword_1"]')
fecha.clear()
fecha.send_keys(fec1)
sleep(1)
apply = browser.find_element_by_xpath('//*[@id="me_filter_pane_submit"]')
apply.click()
wait(1)
che1 = browser.find_element_by_xpath('//*[@id="col_select"]')
che1.click()
wait(1)
meall = browser.find_element_by_xpath('//*[@id="me_select_all"]')
meall.click()
wait(1)
xport = browser.find_element_by_xpath('//*[@id="entry_export"]')
xport.click()
filer = browser.find_element_by_xpath('//*[@id="export_as_excel"]')
filer.click()
sleep(30)

while not os.listdir(carpeta)!=[]:
  sleep(2)
while os.listdir(carpeta)[0].endswith(extension) is False:
  sleep(3)


##aplicar la macro cambiar el archvo a la ruta y eliminarlo de descarga
for item in os.listdir(carpeta): #recorrer todos los items de la carpeta
    if item.endswith(extension): #comprueba la extensión .zip   
        nombrearchivo= os.path.abspath(item) #obtiene la ruta completa de los archivos
        fname = nombrearchivo
  
df=pd.read_excel(fname)
df.to_excel(ruta,index=False)

df.to_excel(movil,index=False)
dff = pd.read_excel('D:/Emergencia/Descargas/Respaldos/CasosOficial.xlsx')
dfone=pd.concat([dff,df])
print('Se completo 1')
dfone.drop_duplicates(inplace=True)
dfone = dfone.sort_values('Entry #')
dfone.to_excel('//10.1.1.7/01 Oficina Planeación y Control/01 Analytics/Sebas/ClasificaciondeCasosOficial/CasosOficial.xlsx',index=False)
dfone.to_excel('//10.1.1.7/01 Oficina Planeación y Control/01 Analytics/Daniel/TipiGobAnt/CasosOficial.xlsx',index=False)
dfone.to_excel('D:/Emergencia/Descargas/Respaldos/CasosOficial.xlsx',index=False)
sleep(10)

print('Se completo la descarga')
sleep(2)

browser.quit()

#hotkey('ctrl', 'c')