from src.packages.handlers.MenuHandler import browserSelection, mainMenu
from src.packages.othersrc.genFunc import exitProgram, handleError
from src.packages.handlers.DataHandler import DataHandler
from src.packages.handlers.DriverHandler import DriverHandler
from src.packages.handlers.DcfSheetsHandler import DcfSheetsHandler

def main():
    browser = browserSelection()
    if(not browser):
        exitProgram()
    searchData=__getUserInputValues()
    if(not searchData):
        return main()
    driver=DriverHandler.openBrowser(browser)
    if(not driver):
        return main()
    
    dh=DataHandler(searchData["sym"], driver)
    dataValues=dh.getAllData()
    if(not dataValues):
        handleError("No se pudo acceder al contenido de la página ¿Reiniciar?")
        return main()
    sh=DcfSheetsHandler(searchData, dataValues)
    sh.handleExcel()
    sh.saveWorkbook(searchData["wbName"])

def __getUserInputValues():
    return mainMenu()
    
    