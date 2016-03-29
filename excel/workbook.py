import openpyxl
import openpyxl.workbook
from   openpyxl.workbook import Workbook

def CreateWorkBook():
  return Workbook()

def CreateSheet(wb,name,index=None):
  wb.create_sheet(name,index)

def GetSheetByName(wb,name):
  return wb.get_sheet_by_name(name)

def SaveWorkBook(wb,fname):
  wb.remove_sheet(wb.get_sheet_by_name('Sheet'))
  wb.save(fname)



