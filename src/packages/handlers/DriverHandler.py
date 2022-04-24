import os
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as frfxService
from selenium.webdriver.chrome.service import Service as chrmService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from src.packages.othersrc.genFunc import displayLine, handleError

class DriverHandler():
    
    @staticmethod
    def openBrowser(browserCode="f"):
        browserName=""
        try:
            if(browserCode=="f"):
                browserName="Firefox"
                displayLine(f"Abriendo navegador {browserName}...")
                service=frfxService(executable_path=GeckoDriverManager(path="./drivers", log_level=0, print_first_line=False).install(), log_path=os.devnull)
                driver = webdriver.Firefox(service=service)
            elif(browserCode=="c"):
                browserName="Chrome"
                displayLine(f"Abriendo navegador {browserName}...")
                service=chrmService(executable_path=ChromeDriverManager(path="./drivers", log_level=0, print_first_line=False).install(), log_path=os.devnull)
                driver = webdriver.Chrome(service=service)
        except:
            handleError("No se pudo inicializar el driver {}".format(browserName))
            return
        displayLine(f"Apertura del navegador exitosa")
        return driver
    
    @staticmethod
    def getHTML(driver, link, clickExpandButton=True):
        driver.get(link)
        clickExpandButton and DriverHandler.clickExpandButton(driver)
        html = driver.execute_script("return document.body.innerHTML;")
        return BeautifulSoup(html,"lxml")
    
    @staticmethod
    def clickExpandButton(driver):
        sleep(0.5)
        try:
            button=driver.find_element(By.CLASS_NAME, value="expandPf")
        except:
            sleep(1)
            button=driver.find_element(By.CLASS_NAME, value="expandPf")
        button and button.text=="Expand All" and button.click()
        
    @staticmethod
    def loopParentsUntilFound(elem, parentClass):
        parent=elem.find_element(By.XPATH, value="./..")
        while(not parentClass in parent.get_attribute("class")):
            try:
                parent=parent.find_element(By.XPATH, value="./..")
            except:
                return None
        return parent
    
    @staticmethod
    def getPrice(driver, sym):
        elem=driver.find_element(by=By.XPATH, value='//*[@data-symbol="{}"][@data-test="qsp-price"]'.format(sym))   
        innerHtml=elem.get_attribute("innerHTML")
        return elem.text
    
    @staticmethod
    def getValueFromStatement(driver, elementTitle, nthChild=3):
        elem=DriverHandler.getElementByTitle(driver, elementTitle)
        row=DriverHandler.loopParentsUntilFound(elem, "D(tbr)")
        lastYearValue=row.find_element(By.CSS_SELECTOR, value=(f'div[data-test="fin-col"]:nth-child({nthChild})'))
            
        return lastYearValue.text
        
    @staticmethod
    def getValueFromOther(driver, elementText, nthChild=2):
        rowTitle=driver.find_element_by_xpath(f"//*[contains(text(), '{elementText}')]")
        # innerHtml=rowTitle.get_attribute("innerHTML")
        row=rowTitle.find_element(By.XPATH, value="./..").find_element(By.XPATH, value="./..")
        value=row.find_element(By.CSS_SELECTOR, value=(f"td:nth-child({nthChild})"))
        return value.text
    
    @staticmethod
    def closeDriver(driver):
        driver.quit()
        
    @staticmethod
    def getElementByTitle(driver, title):
        return driver.find_element(by=By.XPATH, value='//*[@title="{}"]'.format(title))    
    
    @staticmethod
    def getValueFromTreasuryRates(driver, bondSym):
        value=driver.find_element(by=By.XPATH, value='//*[@data-symbol="{}"]'.format(bondSym))
        return value.text