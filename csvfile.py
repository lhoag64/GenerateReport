import logging
import csv

#-------------------------------------------------------------------------------
class CsvFile:
  def __init__(self):
    reader = None
    fp     = None

  def Open(self,filename):
    self.fp = open(filename,'r')
    self.reader = csv.reader(self.fp)

  def GetRow(self):
    try:
      return next(self.reader)
    except StopIteration:
      return None 

  def Close(self):
    self.fp.close()
