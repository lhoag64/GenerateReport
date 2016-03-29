import logging
from   report     import Report
from   report     import ParseUeIds
from   csvfile    import CsvFile

rdafiles = \
  { \
    0:r'test-data\test-case-1\160323_151426_NJRCSIT148_D500logs_NA_0001_600.csv', \
    1:r'test-data\test-case-1\160323_151426_NJRCSIT148_D500logs_NA_0001_601.csv', \
    2:r'test-data\test-case-1\160323_151426_NJRCSIT148_D500logs_NA_0001_602.csv', \
    3:r'test-data\test-case-1\160323_151426_NJRCSIT148_D500logs_NA_0001_603.csv', \
    4:r'test-data\test-case-1\160323_151426_NJRCSIT148_D500logs_NA_0001_604.csv'  \
  }

#-------------------------------------------------------------------------------
class LpParams:
  def __init__(self,text,ttype,ueIds):
    stxt = text.split(':')
    self.name = stxt[1]

    stxt = stxt[0].split('-')
    self.cs    = stxt[0].upper()
    self.type  = stxt[1].upper()
    self.ttype = ttype
    self.ueIds = ueIds

#-------------------------------------------------------------------------------
class StatsParams:
  def __init__(self,textList,ueIds):
    self.bearer = textList[0]
    self.qci    = textList[1]
    self.ttype  = textList[2]
    self.ueIds  = ueIds

#-------------------------------------------------------------------------------
class RdaParams:
  def __init__(self,textList):
    self.ueIds = ParseUeIds(textList[0])
    self.stats = StatsParams(textList[1:],self.ueIds)
    self.lpList = []
    for lpText in textList[4:]:
      self.lpList.append(LpParams(lpText,self.stats.ttype,self.ueIds))

#-------------------------------------------------------------------------------
class Column:
  def __init__(self,text,index):
    self.index = index
    first,sep,last = text.partition(' ')
    if (len(sep) > 0):
      self.service = first.upper()
      self.desc    = last
    else:
      self.service = ''
      self.desc    = first

#-------------------------------------------------------------------------------
class LoadProfile:
  summable = set(['Session Packets In','Session Packets Out'])
  def __init__(self,params):
    self.name  = params.name
    self.cs    = params.cs
    self.type  = params.type
    self.ttype = params.ttype
    self.ueIds = params.ueIds

    self.cols     = {}
    self.sums     = {}

  def GetTxSum(self):
    if (self.type == 'TX') : return self.sums['Session Packets Out']
    return 0.0

  def GetRxSum(self):
    if (self.type == 'RX') : return self.sums['Session Packets In']
    return 0.0

  #-----------------------------------------------------------------------------
  class TimeColumn:
    def __init__(self,col):
      self.desc  = col.desc
      self.index = col.index
      self.rows  = []

    def AddRow(self,val):
      self.rows.append(val[:19])

    def GetSum(self):
      return None

    def ProcessStats(self):
      pass

  class DataColumn:
    def __init__(self,col):
      self.desc  = col.desc
      self.index = col.index
      self.rows  = []
      self.sum   = 0.0

    def AddRow(self,val):
      self.rows.append(float(val))

    def GetSum(self):
      return self.sum

    def ProcessStats(self):
      for row in self.rows:
        self.sum += row

  #-----------------------------------------------------------------------------
  def ProcessStats(self):
    for ueid in self.cols:
      for colName in self.cols[ueid]:
        self.cols[ueid][colName].ProcessStats()
        if (colName in self.summable):
          if (colName not in self.sums):
            self.sums[colName] = 0.0
          self.sums[colName] += self.cols[ueid][colName].GetSum()
         
  #-----------------------------------------------------------------------------
  def UpdateUeIds(self,ueIds):
    if ((len(self.ueIds) == 1) and ('ALL' in self.ueIds)):
      self.ueIds = ueIds

  #-----------------------------------------------------------------------------
  def AddColumn(self,ueid,col):
    if (ueid not in self.cols):
      self.cols[ueid] = {}
    if (col.desc not in self.cols[ueid]):
      if (col.desc != 'Time'):
        dataCol = LoadProfile.DataColumn(col)
      else:
        dataCol = LoadProfile.TimeColumn(col)
      self.cols[ueid][col.desc] = dataCol
    else:
      logging.error('Adding duplicate column to LoadProfile')

#-------------------------------------------------------------------------------
class RdaStats:
  lpDict = None     # Load Profile by load profile name
  ueIds  = None     # UE ids

  def __init__(self,params):
    self.lpDict = {}
    self.ueIds  = params.ueIds
    self.bearer = params.bearer
    self.qci    = params.qci
    self.ttype  = params.ttype
    self.txSum  = 0.0
    self.rxSum  = 0.0

  def AddLp(self,lp):
    self.lpDict[lp.name] = lp

  #-----------------------------------------------------------------------------
  def ProcessStats(self):
    for lpName in self.lpDict:
      self.lpDict[lpName].ProcessStats()
      if (self.lpDict[lpName].type == 'TX'):
        self.txSum = self.lpDict[lpName].GetTxSum()
      if (self.lpDict[lpName].type == 'RX'):
        self.rxSum = self.lpDict[lpName].GetRxSum()
     
  #-----------------------------------------------------------------------------
  def UpdateUeIds(self,ueIds):
    if ((len(self.ueIds) == 1) and ('ALL' in self.ueIds)):
      self.ueIds = ueIds

  #-----------------------------------------------------------------------------
  def GetUeIds(self):
    return self.ueIds
 
  #-----------------------------------------------------------------------------
  def GetLpList(self):
    return self.lpList
 
#-------------------------------------------------------------------------------
class RdaReport(Report):
  statsList   = None
  lpDict      = None
  lpIds       = None
  desiredData = {'teraflow':('Time','In Service','Session Packets')}

  def __init__(self,rtype):
    self.statsList = []
    self.lpDict    = {}
    self.ueIds     = set([])
    self.rtype     = rtype

  def AddReport(self,textList):
    params = RdaParams(textList)
    for ueid in params.ueIds:
      if ((ueid not in self.ueIds) and (ueid != 'ALL')):
        self.ueIds.add(ueid)

    stats = RdaStats(params.stats)
    for lpParams in params.lpList:
      lp = LoadProfile(lpParams)
      if (lp.name not in self.lpDict):
        self.lpDict[lp.name] = lp
      stats.AddLp(lp)
    self.statsList.append(stats)

  #-----------------------------------------------------------------------------
  def ProcessReport(self):
    ueList = sorted(self.ueIds)

    # For each UE in the UE list read the RDA file and save information
    for ueid in ueList:
      rdaFile = CsvFile()
      rdaFile.Open(rdafiles[ueid])
      self.processFile(rdaFile,ueid)
      rdaFile.Close()

    for stats in self.statsList:
      stats.ProcessStats()

    for stats in self.statsList:
      text = '|'
      text += stats.bearer + '|'
      text += stats.qci + '|'
      text += 'TX:' + str(stats.txSum).rjust(6) + '|'
      text += 'RX:' + str(stats.rxSum).rjust(6) + '|'
      logging.debug(text)

  #-----------------------------------------------------------------------------
  def processFile(self,file,ueid):
    colDict = None
    lpDict  = {}

    for lp in self.lpDict:
      if (ueid in self.lpDict[lp].ueIds):
        if (lp not in lpDict):
          lpDict[lp] = self.lpDict[lp]
        else:
          logging.error('Attempting to add existing LoadProfile to dict')

    while (1):
      row = file.GetRow()
      if (row == None): break
      if (len(row) == 0)  : continue
      if (row[0][0:1] == '#'): continue
      if (row[1] == 'Time'):
        #
        # Parse the headers to get and cols that are desired
        #
        colDict = self.parseHdr(row)
        for lp in lpDict:
          self.lpDict[lp].AddColumn(ueid,colDict['Time'])
          for col in colDict[lp]:
            self.lpDict[lp].AddColumn(ueid,colDict[lp][col])
        continue

      self.parseData(row,ueid,colDict,lpDict)
    
  #-----------------------------------------------------------------------------
  def parseHdr(self,row):
    colIdx  = 0
    colDict = {}
    for col in row:
      if (len(col) > 0):
        stxt = col.split()
        if (col.startswith('Time')):
          colDict['Time'] = Column(col,colIdx)
        else:
          lpName = stxt[0].upper()
          if (lpName in self.lpDict):
            if (lpName not in colDict):
              colDict[lpName] = {}
            column = Column(col,colIdx)
            if (column.desc.startswith(self.desiredData[self.lpDict[lpName].ttype])):
              if (column.desc not in colDict[lpName]):
                colDict[lpName][column.desc] = column
              else:
                logging.error('Should not be here')

      colIdx += 1

    return colDict 
   
  #-----------------------------------------------------------------------------
  def parseData(self,row,ueid,dict,lpDict):
    for lp in lpDict:
      for col in lpDict[lp].cols[ueid]:
        lpDict[lp].cols[ueid][col].AddRow(row[lpDict[lp].cols[ueid][col].index])
   
  #-----------------------------------------------------------------------------
  def UpdateUeIds(self,ueIds):
    super().UpdateUeIds(ueIds)
    for lp in self.lpDict:
      self.lpDict[lp].UpdateUeIds(ueIds)
    for stats in self.statsList:
      stats.UpdateUeIds(ueIds)

  #-----------------------------------------------------------------------------
  def ReadData(self):
    pass

