from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as frfxService
from selenium.webdriver.chrome.service import Service as chrmService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import src.packages.othersrc.constants as cts
from src.packages.othersrc.genFunc import displayLine, handleError

class DriverHandler():
    
    valuesNotFound=[]
    
    @staticmethod
    def openBrowser(browserCode="f"):
        browserName=""
        try:
            if(browserCode=="f"):
                browserName="Firefox"
                displayLine(f"Abriendo navegador {browserName}...")
                service=frfxService(executable_path=GeckoDriverManager(path="./drivers", log_level=0, print_first_line=False).install(), log_path='/dev/null')
                driver = webdriver.Firefox(service=service)
            elif(browserCode=="c"):
                browserName="Chrome"
                displayLine(f"Abriendo navegador {browserName}...")
                service=chrmService(executable_path=ChromeDriverManager(path="./drivers", log_level=0, print_first_line=False).install(), log_path='/dev/null')
                driver = webdriver.Chrome(service=service)
        except:
            handleError("No se pudo inicializar el driver {}".format(browserName))
            return
        displayLine(f"Apertura del navegador exitosa")
        return driver
    
    @staticmethod
    def getHTML(driver, link, clickExpandButton=True):
        driver.get(link)
        if(clickExpandButton):
            clickedButton=DriverHandler.clickExpandButton(driver)
            if(not clickedButton):
                return False
            
        # html = driver.execute_script("return document.body.innerHTML;")
        return True
    
    @staticmethod
    def clickExpandButton(driver):
        button=""
        sleep(cts.SLEEP_SECONDS_BETWEEN_PETITIONS)
        try:
            button=driver.find_element(By.CLASS_NAME, value="expandPf")
        except:
            sleep(cts.SLEEP_SECONDS_BETWEEN_PETITIONS)
            try:
                button=driver.find_element(By.CLASS_NAME, value="expandPf")
            except:
                pass
                
        button and button.text=="Expand All" and button.click()
        try:
            button=driver.find_element(By.CLASS_NAME, value="expandPf")
            if(button.text=="Expand All"):
                return False
        except:
            return False
        return True
        
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
        try:
            elem=driver.find_element(by=By.XPATH, value='//*[@data-symbol="{}"][@data-test="qsp-price"]'.format(sym))
            # innerHtml=elem.get_attribute("innerHTML")
            return elem.text
        except:
            DriverHandler.valuesNotFound.append("Price")
            displayLine("ERROR: Price not found, setting value to 0")
            return "0"
    
    @staticmethod
    def getValueFromStatement(driver, elementTitle, nthChild=3):
        try:
            elem=DriverHandler.getElementByTitle(driver, elementTitle)
            row=DriverHandler.loopParentsUntilFound(elem, "D(tbr)")
            lastYearValue=row.find_element(By.CSS_SELECTOR, value=(f'div[data-test="fin-col"]:nth-child({nthChild})'))
            return lastYearValue.text
        except:
            return "0"
        
    @staticmethod
    def getValueFromOther(driver, elementText, nthChild=2):
        try:
            rowTitle=driver.find_element_by_xpath(f"//*[contains(text(), '{elementText}')]")
            # innerHtml=rowTitle.get_attribute("innerHTML")
            row=rowTitle.find_element(By.XPATH, value="./..").find_element(By.XPATH, value="./..")
            value=row.find_element(By.CSS_SELECTOR, value=(f"td:nth-child({nthChild})"))
            return value.text
        except:
            DriverHandler.valuesNotFound.append(elementText)
            displayLine(f"ERROR: {elementText} not found, setting value to 0")
            return "0"
    
        
    @staticmethod
    def getElementByTitle(driver, title):
        try:    
            elem=driver.find_element(by=By.XPATH, value='//*[@title="{}"]'.format(title))    
            return elem
        except:
            DriverHandler.valuesNotFound.append(title)
            displayLine(f"ERROR: {title} not found, setting value to 0")
            return "0"
    
    @staticmethod
    def getValueFromTreasuryRates(driver, bondSym):
        try:
            value=driver.find_element(by=By.XPATH, value='//*[@data-symbol="{}"]'.format(bondSym))
            return value.text
        except:
            DriverHandler.valuesNotFound.append(bondSym)
            displayLine(f"ERROR: {bondSym} not found, setting value to 0")
            return "0"

    @staticmethod
    def closeDriver(driver):
        driver.quit()