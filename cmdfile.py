import logging
import csv
from testparams import TestParams



#-------------------------------------------------------------------------------
class CmdFile:
#  dataDict = None

  #-----------------------------------------------------------------------------
  def __init__(self,test):
    self.testName = test

  #-----------------------------------------------------------------------------
  def Read(self,file):

    testparams = TestParams()
    testparams.SetName(self.testName)
 
    state = 'Scan'
    with open(file) as inpfile:
      for line in inpfile:
        line = line.strip(' \n\r\t')
        upperLine = line.upper()
         
        if (upperLine.find('#$$COMMENT AUTOMATION') > 0):
          stxt = line.split()
          if (state == 'Scan'):
            if (stxt[4] == 'Param-Start' and (stxt[5].find(self.testName) >= 0)):
              state = 'Params'
          elif (state == 'Params'):
            if (stxt[4] == 'Param-End'):
              state = 'Scan'
            elif (stxt[4][:2] == 'UE'):
              testparams.ParseUeIds(stxt[4])
            elif (stxt[4][0:6] == 'REPORT'):
              testparams.AddReport(stxt[4:])

    return testparams



