import logging
import csv
#from   testparams import TestParams
#from   testparams import Report
#from   rdareport  import LoadProfile

#-------------------------------------------------------------------------------
class RdaFile:
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
    pass

  #desiredServices = ('Time','DL_TCP','UL_TCP','DL_UDP','UL_UDP')
#  desiredData  = {'teraflow':('Time','In Service','Session Packets')}
#  lpDict = {}
#
#  def __init__(self,file,ue,reports):
#    for report in reports:
#      for lp in report.lpList:
#        if (lp not in self.lpDict):
#            self.lpDict[lp.name] = lp
#
#    with open(file) as inpfile:
#       csvreader = csv.reader(inpfile)
#       for row in csvreader:
#         if (len(row) == 0)  : continue
#         if (row[0][0:1] == '#'): continue
#         if (row[1] == 'Time'):
#           #
#           # Parse the headers to get and cols that are desired
#           #
#           colDict = self.parseHdr(row)
#           continue
#
#         self.parseData(row,colDict)
#
#  #-------------------------------------------------------------------------------
#  def parseHdr(self,row):
#    colIdx  = 0
#    colDict = {}
#    for col in row:
#      if (len(col) > 0):
#        stxt = col.split()
#        if (col.startswith('Time')):
#          colDict['Time'] = Column(col,colIdx)
#        else:
#          lpName = stxt[0].upper()
#          if (lpName in self.lpDict):
#            if (lpName not in colDict):
#              colDict[lpName] = {}
#            column = Column(col,colIdx)
#            if (column.desc.startswith(self.desiredData[self.lpDict[lpName].ttype])):
#              if (column.desc not in colDict[lpName]):
#                colDict[lpName][column.desc] = column
#              else:
#                logging.error('Should not be here')
#
#      colIdx += 1
#
#    return colDict
#
#  #-------------------------------------------------------------------------------
#  def parseData(self,row,colList):
#    for name in self.lpDict:
#      logging.debug(name)



#    for i in dataDict:
#      for j in dataDict[i]:
#        if (dataDict[i][j].desc == 'Time'):
#          found = 0
#          time = row[j].rsplit('.')
#          for k in dataDict[i][j].rows:
#            if (k == time[0]):
#              found = 1
#              break
#          if (found == 0):
#            dataDict[i][j].rows.append(time[0])
#        else:
#          dataDict[i][j].rows.append(row[j])

'''

  #-------------------------------------------------------------------------------
  def parseData(self,row,dataDict):
    for i in dataDict:
      for j in dataDict[i]:
        if (dataDict[i][j].desc == 'Time'):
          found = 0
          time = row[j].rsplit('.')
          for k in dataDict[i][j].rows:
            if (k == time[0]):
              found = 1
              break
          if (found == 0):
            dataDict[i][j].rows.append(time[0])
        else:
          dataDict[i][j].rows.append(row[j])

  #-------------------------------------------------------------------------------
  def Read(self,file):

    colDict = None
    dataDict = {}

    with open(file) as inpfile:
       csvreader = csv.reader(inpfile)
       for row in csvreader:
         if (len(row) == 0)  : continue
         if (row[0][0:1] == '#'): continue
         if (row[1] == 'Time'):
           #
           # Parse the headers to get services and cols that are desired
           #
           colDict = self.parseHdr(row)

           #
           # Create dataDict
           #
           for index in colDict:
             item = colDict[index]
             if (len(item.service) == 0):
               time = item
             else:
               if (item.service not in dataDict):
                 dataDict[item.service] = {}
               dataDict[item.service][item.index] = item
             # add time to all services
             for i in dataDict:
               dataDict[i][time.index] = time
           continue

         #
         # Populate the dataDict with row informaiton
         #
         self.parseData(row,dataDict)

    self.dataDict = dataDict

    return dataDict
'''
