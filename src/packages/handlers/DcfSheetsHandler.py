from datetime import datetime
from src.packages.handlers.DriverHandler import DriverHandler
from src.packages.handlers.ExcelHandler import ExcelHandler
from openpyxl.worksheet.dimensions import SheetFormatProperties, ColumnDimension

class DcfSheetsHandler(ExcelHandler):
    def __init__(self, searchData, dataValues):
        super().__init__()
        self.sym=searchData["sym"]
        self.sd=searchData
        self.dv=dataValues
        
    def __projectedCashFlows(self):
        ws=self.createSheet("CF proyectados", 1)
        ws.sheet_format=SheetFormatProperties(defaultColWidth=24.43)
        ws.column_dimensions["A"]=ColumnDimension(ws, width=3)
        
        self.writeToRange(ws, "B2", "C2", [self.sym, ""], rangeNamedStyle="head")
        
        self.writeToRange(ws, "B3", "B5", ["Crecimiento de FCF", "Crecimiento estable", "WACC"])
        self.writeToRange(ws, "C3", "C5", [self.dv["growth"], self.sd["perpGrowth"], "=WACC!C22"], numberFormat="p")
        
        self.writeToRange(ws, "B7", "H7", ["Año", datetime.now().year-1, "=C7+1", "=D7+1", "=E7+1", "=F7+1", "=G7+1"], rangeNamedStyle="head")
        self.writeToRange(ws, "B8", "H8", ["FCF", self.dv["fcf"], "=C8*(1+$C$3)", "=D8*(1+$C$3)", "=E8*(1+$C$3)", "=F8*(1+$C$3)", "=G8*(1+$C$3)"], numberFormat="a") 
        self.writeToRange(ws, "B9", "H9", ["Valor terminal", "", "", "", "", "", "=H8*(1+$C$4)/($C$5-$C$4)"], numberFormat="a")
        self.writeToRange(ws, "B10", "H10", ["Total", "", "=SUM(D8:D9)", "=SUM(E8:E9)", "=SUM(F8:G9)", "=SUM(G8:G9)", "=SUM(H8:H9)"], rangeNamedStyle="total")
        
        self.writeToRange(ws, "B12", "C12", ["VPN de los FCF proy.", "=NPV(C5,D10:H10)"], rangeNamedStyle="bold")
        
        self.cellFormatNumber(ws, "D10", "a")
        self.cellFormatNumber(ws, "E10", "a")
        self.cellFormatNumber(ws, "F10", "a")
        self.cellFormatNumber(ws, "G10", "a")
        self.cellFormatNumber(ws, "H10", "a")
        self.cellFormatNumber(ws, "C12", "a")
        
    def __wacc(self):
        ws=self.wb.active
        ws.title="WACC"
        ws.sheet_format=SheetFormatProperties(defaultColWidth=24.43)
        ws.column_dimensions["A"]=ColumnDimension(ws, width=3)
        
        self.writeToRange(ws, "B2", "C2", ["Deuda", ""], "head")
        self.writeToRange(ws, "B3", "B9", ["Intereses", "Deuda financiera corto plazo", "Deuda financiera largo plazo", "Costo de la deuda", "Impuesto a las ganancias", "EBT", "t"])
        self.writeToRange(ws, "C3", "C9", [self.dv["intExpense"], self.dv["currDebt"], self.dv["longDebt"], "=IFERROR(C3/(C4+C5),0)", self.dv["taxProv"], self.dv["EBT"], "=C7/C8"], numberFormat="a")
        
        self.writeToRange(ws, "B11", "C11", ["Equity", ""], "head")
        self.writeToRange(ws, "B12", "B15", ["Rendimiento risk free", "Beta", "Rendimiento mercado", "Costo del equity"])
        self.writeToRange(ws, "C12", "C15", [self.dv["rfRate"], self.dv["beta"], self.sd["mktReturn"], "=(C14-C12)*C13+C12"], numberFormat="a")
       
        self.writeToRange(ws, "B17", "C17", ["WACC", ""], "head")
        self.writeToRange(ws, "B18", "B21", ["D", "E", "w_D", "w_E"])
        self.writeToRange(ws, "C18", "C21", ["=(C4+C5)", self.dv["mktCap"], "=IFERROR(C18/(C18+C19),0)", "=1-C20"], numberFormat="a")
        self.writeToRange(ws, "B22", "C22", ["WACC", "=C20*(1-C9)*C6+C21*C15"], "bold", numberFormat="p")
        
        self.cellFormatNumber(ws, "C22", "p")
        
    def __dcf(self):
        ws=self.createSheet("DCF", 0)
        ws.sheet_format=SheetFormatProperties(defaultColWidth=24.43)
        ws.column_dimensions["A"]=ColumnDimension(ws, width=3)
        
        self.writeToRange(ws, "B2", "B6", ["Enterprise Value", "Efectivo y equivalentes", "Deuda", "Equity Value", "Acciones"])
        self.writeToRange(ws, "C2", "C6", ["='CF proyectados'!C12", self.dv["cash"], "=WACC!C18", "=C2+C3-C4", self.dv["shares"]], numberFormat="a")
        self.writeToRange(ws, "B7", "C7", ["Precio intrínseco", "=IFERROR(C5/C6,0)"], "total", numberFormat="a")
        
        self.writeToRange(ws, "E2", "E5", ["Precio actual", "Precio intrínseco", "Crecimiento/Caída", "Comprar/Vender"], fontSize="14")
        self.writeToRange(ws, "F2", "F5", [self.dv["price"], "=C7", "=IFERROR(F3/F2-1,0)", '=IF(F4>0, "Comprar", IF(F4<=0, "Vender", ""))'], fontSize="14", numberFormat="a")
        
        self.conditionalFormatting(ws, "F4", 0)
        self.cellFormatNumber(ws, "F4", "p")
        self.setCellStyle(ws, "F5", "bold")
        self.cellFormatNumber(ws, "C7", "a")
    
        if(DriverHandler.valuesNotFound):
            self.writeToCell(ws, "B10", "VALUES NOT FOUND", "bold")
            self.writeToRange(ws, "B11", f"B{len(DriverHandler.valuesNotFound)+11-1}", DriverHandler.valuesNotFound, rangeNamedStyle="bad")
            
    def handleExcel(self):
        self.__wacc()
        self.__projectedCashFlows()
        self.__dcf()
        


        
        