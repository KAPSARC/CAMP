from sys import displayhook
import xlwings as xw
import json
import os
from datetime import datetime
import confiq 


#Model File
MODEL_FILE_INPUT = confiq.DIR_PATH + '/models/model-file-camp-sankey.xlsx'
MODEL_SHEET_INPUT = 'app'
INPUT_FIELDS_RANGE = 'A4:H13' 
INPUTS_START_CELL = 'F5' #Start of Highlighted Fields



#-------------------------------------------
#       Public Methods
#-------------------------------------------

def modelFile():
    #app = xw.App(visible=False)
    wb = xw.Book(MODEL_FILE_INPUT)
    ws = wb.sheets[MODEL_SHEET_INPUT]
    
    return ws


def getInputsFields(ws):
    # getInputsFields
    data = ws.range(INPUT_FIELDS_RANGE).value
    return toDict(data)

def setInputsCell(ws, inputsList):
    # setInputValues by cell
    for i in inputsList:
        ws.range(i['id']).options(transpose=False).value = i['value']

def setInputs(ws, inputsList):
    # setInputValues by range
    ws.range(INPUTS_START_CELL).options(transpose=True).value = inputsList #changed it from True


app_dir= confiq.DIR_PATH 



def generateOutput():
    wb = xw.Book(MODEL_FILE_INPUT)
    ws = wb.sheets[MODEL_SHEET_INPUT]
    wb.save()
    
    command = 'python SankeyScript.py'
    os.popen(command)

    wb.close()
    print("generated !")

    
def displayOutput():
    with open("data.json") as FILE_OUTPUT:
        data = json.load(FILE_OUTPUT)
        #print(data)
    return data

# def getTitle():
#     with open("title.json") as f:
#         data = json.load(f)
#     return data
    


#-------------------------------------------
#       Private Methods
#-------------------------------------------
def toDict(data):
    """
        this restructure data
    """
    result=[]
    for row in data[1:]:
        result.append(dict(zip(data[0], row)))
    return result
