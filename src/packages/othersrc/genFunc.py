from os import makedirs
from sys import exit

from numpy import number
import src.packages.othersrc.constants as cts

def handleError(error):
    formattedLine="Error received '{}'. Continue? (y,n): ".format(error)
    userIn=handleInput(formattedLine)
    match userIn.lower():
        case 'y':
            return
        case 'n':
            exitProgram()
    handleError(error)

def exitProgram():
    exit()

def readFile(filename):
    with open(filename, "r") as file:
        return file.read()

def checkKeyInDict(dict, key, defaultValue=0):
    if(key in dict):
        return dict[key]

    return defaultValue

def displayLine(line, printLine=True, addLineBreak=True):
    printLine and print(line)

def handleInput(inputText):
    userInput=input(inputText)
    return userInput

def createDir(dirName):
    try:
        makedirs(dirName)
    except:
        pass
    
def percetageStrToFloatStr(numberStr):
    output=""
    try:
        output=str(float(numberStr[:numberStr.index("%")])/100)
    except:
        pass
    return output
        
    
