from os import system
from src.packages.othersrc.genFunc import exitProgram, handleInput, displayLine, exitProgram, percetageStrToFloatStr


def __printListWithInput(listDescriptor, selectionList, listItemPrefix="", lastItemNoPrefix=True):
    userIn = 0
    displayLine(listDescriptor + " (enter: 1)", printLine=True, addLineBreak=True)
    for i in range(len(selectionList)):
        if(i==len(selectionList)-1 and lastItemNoPrefix):
            listItemPrefix=""
        displayLine("\t{}. {}{}".format(i+1, listItemPrefix, selectionList[i]), printLine=True, addLineBreak=True)
    
    while(not type(userIn)==int or userIn>len(selectionList)+1 or userIn<1):
        userIn=handleInput("Selección: ")
        if(not userIn):
            userIn=1
        else:
            try:
                userIn=int(userIn)
            except:
                userIn=0
        
    return userIn

def __clearConsole():
    system("cls")

def __mainProgMenu():
    sym=""
    perpGrowth=""
    mktReturn=""
    outputExcelName=""
    
    while(not sym):
        sym=handleInput("Activo a buscar: ").upper()
    
    while(not perpGrowth):
        perpGrowth=handleInput("Crecimiento perpetuo (x.xx%) (enter: 2.5%): ")
        if(not perpGrowth):
            perpGrowth = "2.5%"
        else:
            perpGrowth.replace(",", ".")    
            if(not perpGrowth.__contains__("%")):
                perpGrowth+="%"
        perpGrowth=float(percetageStrToFloatStr(perpGrowth))
            
    while(not mktReturn):
        mktReturn=handleInput("Rendimiento de mercado (x.xx%) (enter: 9.2%): ")
        if(not mktReturn):
            mktReturn = "9.2%"
        else:
            mktReturn.replace(",", ".")    
            if(not mktReturn.__contains__("%")):
                mktReturn+="%"
        mktReturn=float(percetageStrToFloatStr(mktReturn))
        
    while(not outputExcelName):
        outputExcelName=handleInput("Nombre del excel (enter: {}_dcf.xlsx): ".format(sym))
        if(not outputExcelName):
            outputExcelName="{}_dcf.xlsx".format(sym)
        else:
            if(not outputExcelName.__contains__(".")):
                outputExcelName += ".xlsx"
            
    __clearConsole()
    
    return {"sym":sym, "perpGrowth":perpGrowth, "mktReturn":mktReturn, "wbName":outputExcelName}

def mainMenu():
    selectionList=["Iniciar aplicación", "Volver"]
    __clearConsole()
    userIn=__printListWithInput("Menu principal:", selectionList)
    __clearConsole()
    match selectionList[userIn-1]:
        case "Iniciar aplicación":
            searchData=__mainProgMenu()
            return searchData
        case "Volver":
            return
            
def browserSelection():
    selectionList=["Firefox", "Chrome", "Cerrar programa"]
    userIn=__printListWithInput("Navegador a utilizar:", selectionList)
    match selectionList[userIn-1]:
        case "Firefox":
            return "f"
        case "Chrome":
            return "c"
        case "Cerrar programa":
            return
    
