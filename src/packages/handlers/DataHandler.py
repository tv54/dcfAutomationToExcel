from src.packages.othersrc.genFunc import displayLine, percetageStrToFloatStr
from src.packages.handlers.DriverHandler import DriverHandler

class DataHandler():

    yfPrefixUrl = "https://finance.yahoo.com/"

    def __init__(self, sym, driver):
        self.sym=sym.upper()
        self.driver=driver
        
    def __getRequiredData(self):
        # ---- IS ----
        gotContent=self.__getHtmlBySearchType("is")
        if(not gotContent):
            return
        price=DriverHandler.getPrice(self.driver, self.sym).replace(",","")
        interestExpenseNonOperating=DriverHandler.getValueFromStatement(self.driver, "Interest Expense Non Operating").replace(",","")
        taxProvision=DriverHandler.getValueFromStatement(self.driver, "Tax Provision").replace(",","")
        preTaxIncome=DriverHandler.getValueFromStatement(self.driver, "Pretax Income").replace(",","")
        
        # ---- BSS ----
        gotContent=self.__getHtmlBySearchType("bss")
        if(not gotContent):
            return
        currentDebt=DriverHandler.getValueFromStatement(self.driver, "Current Debt", 2).replace(",","")
        longTermDebt=DriverHandler.getValueFromStatement(self.driver, "Long Term Debt", 2).replace(",","")
        cashAndEquivalents=DriverHandler.getValueFromStatement(self.driver, "Cash, Cash Equivalents & Short Term Investments", 2).replace(",","")
        shareIssued=DriverHandler.getValueFromStatement(self.driver, "Share Issued", 2).replace(",","")
        
        # ---- CFS ----
        gotContent=self.__getHtmlBySearchType("cfs")
        if(not gotContent):
            return
        freeCashFlow=DriverHandler.getValueFromStatement(self.driver, "Free Cash Flow").replace(",","")
        
        # ---- Analysis ----
        gotContent=self.__getHtmlBySearchType("analysis", clickExpandButton=False)
        if(not gotContent):
            return
        growthNextFiveYears=DriverHandler.getValueFromOther(self.driver, "Next 5 Years (per annum)")
        growthNextFiveYears=percetageStrToFloatStr(growthNextFiveYears)
        
        # ---- Statistics ----
        gotContent=self.__getHtmlBySearchType("stats", clickExpandButton=False)
        if(not gotContent):
            return
        betaFiveYear=DriverHandler.getValueFromOther(self.driver, "Beta (5Y Monthly)")
        marketCap=DriverHandler.getValueFromOther(self.driver, "Market Cap (intraday)")
        if(marketCap.__contains__("T")):
            marketCap=str(float(marketCap[:marketCap.index("T")])*1000000000000/1000)
        elif(marketCap.__contains__("B")):
            marketCap=str(float(marketCap[:marketCap.index("B")])*1000000000/1000)
        elif(marketCap.__contains__("M")):
            marketCap=str(float(marketCap[:marketCap.index("M")])*1000000/1000)
        elif(marketCap.__contains__("K")):
            marketCap=str(float(marketCap[:marketCap.index("K")])*1000/1000 )
        
        # ---- US bond rates ----
        gotContent=self.__getHtmlBySearchType("bonds", clickExpandButton=False)
        if(not gotContent):
            return
        riskFree=DriverHandler.getValueFromTreasuryRates(self.driver, "^TNX")+"%"
        riskFree=percetageStrToFloatStr(riskFree)
        
        displayLine("Todos los datos recuperados exitosamente")
        
        dv={
            "intExpense":float(interestExpenseNonOperating),
            "taxProv":float(taxProvision),
            "currDebt":float(currentDebt),
            "longDebt":float(longTermDebt),
            "cash":float(cashAndEquivalents),
            "shares":float(shareIssued),
            "fcf":float(freeCashFlow),
            "growth":float(growthNextFiveYears),
            "beta":float(betaFiveYear),
            "mktCap":float(marketCap),
            "rfRate":float(riskFree),
            "price":float(price),
            "EBT":float(preTaxIncome),
        }
        
        return dv
    
    def __getHtmlBySearchType(self, searchType, clickExpandButton=True):
        match searchType.lower():
            case "is":
                link=f"{self.yfPrefixUrl}quote/{self.sym}/financials?p={self.sym}"
                displayLine("Buscando valores del Estado de Resultados")
            case "bss":
                link=f"{self.yfPrefixUrl}quote/{self.sym}/balance-sheet?p={self.sym}"
                displayLine("Buscando valores del Balance General")
            case "cfs":
                link=f"{self.yfPrefixUrl}quote/{self.sym}/cash-flow?p={self.sym}"
                displayLine("Buscando valores del Estado de Flujo de Efectivo")
            case "analysis":
                clickExpandButton=False
                link=f"{self.yfPrefixUrl}quote/{self.sym}/analysis?p={self.sym}"
                displayLine("Buscando valores del Análisis del activo")
            case "stats":
                clickExpandButton=False
                link=f"{self.yfPrefixUrl}quote/{self.sym}/key-statistics?p={self.sym}"
                displayLine("Buscando valores de las Estadísticas del activo")
            case "bonds":
                clickExpandButton=False
                link=f"{self.yfPrefixUrl}bonds"
                displayLine("Buscando retorno risk free")
            case _:
                link=""
                
        return DriverHandler.getHTML(self.driver, link, clickExpandButton=clickExpandButton)
                
    def getAllData(self):
        dv=self.__getRequiredData()
        DriverHandler.closeDriver(self.driver)
        return dv