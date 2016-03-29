import logging
from   report     import Report
from   report     import ParseUeIds
from   rdafile    import RdaFile

rdafiles = \
  { \
    0:'160323_151426_NJRCSIT148_D500logs_NA_0001_600.csv', \
    1:'160323_151426_NJRCSIT148_D500logs_NA_0001_601.csv', \
    2:'160323_151426_NJRCSIT148_D500logs_NA_0001_602.csv', \
    3:'160323_151426_NJRCSIT148_D500logs_NA_0001_603.csv', \
    4:'160323_151426_NJRCSIT148_D500logs_NA_0001_604.csv'  \
  }

#-------------------------------------------------------------------------------
class LpParams:
  def __init__(self,text,ttype):
    stxt = text.split(':')
    self.name = stxt[1]

    stxt = stxt[0].split('-')
    self.cs    = stxt[0].upper()
    self.type  = stxt[1].upper()
    self.ttype = ttype

#-------------------------------------------------------------------------------
class StatsParams:
  def __init__(self,textList):
    self.ueIds  = ParseUeIds(textList[0])
    self.bearer = textList[1]
    self.qci    = textList[2]
    self.ttype  = textList[3]

#-------------------------------------------------------------------------------
class RdaParams:
  def __init__(self,textList):
    self.stats = StatsParams(textList)
    self.lpList = []
    for lpText in textList[4:]:
      self.lpList.append(LpParams(lpText,self.stats.ttype))

#-------------------------------------------------------------------------------
class Column:
  def __init__(self,text,index):
    self.text  = text
    self.index = index
    self.order = None
    # TODO: Move or make a Column for rdastats
    self.sum   = 0
    self.rows  = []
    first,sep,last = text.partition(' ')
    if (len(sep) > 0):
      self.service = first.upper()
      self.desc    = last
    else:
      self.service = ''
      self.desc    = first

#-------------------------------------------------------------------------------
class LoadProfile:
  def __init__(self,params):
    self.name  = params.name
    self.cs    = params.cs
    self.type  = params.type
    self.ttype = params.ttype
    self.cols  = {}

  def AddColumn(self,col):
    if (col not in self.cols):
      self.cols[col] = col
    else:
      logging.error('Adding duplicate column to LoadProfile')

#  def UpdateUeList(self,ueList):
#    if (self.ueList[0] == 'ALL'):
#      self.ueList = ueList
#      for i in ueList:
#        self.ueSet.add(i)

#-------------------------------------------------------------------------------
class RdaStats:
  lpDict      = {}  # Load Profile by load profile name
#  lpNameList  = []  # Load Profile Name in sorted list
  ueIds       = {}  # List of UE ids
  ueData      = {}  # Dict of UE data by UE

  def __init__(self,params):
    self.ueIds  = params.ueIds
    self.bearer = params.bearer
    self.qci    = params.qci
    self.ttype  = params.ttype

  def AddLp(self,lp):
    self.lpDict[lp.name] = lp

#    for lpText in textList[4:]:
#      lp = LoadProfile(lpText,self.ttype,self.ueList)
#      if (lp.name not in self.lpDict):
#        self.lpDict[lp.name] = lp
#      else:
#        logging.error('Load Profile duplicated in RdaStats')
#    self.lpNameList = sorted(self.lpDict)

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
  statsList    = []
  lpDict       = {}
  lpNameList   = []
  lpIds        = set([])
  desiredData  = {'teraflow':('Time','In Service','Session Packets')}

  def __init__(self,rtype):
    self.rtype = rtype

  def AddReport(self,textList):
    params = RdaParams(textList)

    stats = RdaStats(params.stats)
    for lpParams in params.lpList:
      lp = LoadProfile(lpParams)
      if (lp.name not in self.lpDict):
        self.lpDict[lp.name] = lp
      stats.AddLp(lp)
    self.statsList.append(stats)



#    stats = RdaStats(textList)
#    self.statsList.append(stats)

#    for stats in self.statsList:
#      for lpName in stats.lpNameList:
#        if (lpName not in self.lpDict

#    lpList = stats.GetLpList()
#    for lpName in lpList:
#      if (lpName not in self.lpDict):
#        self.lpDict[lpName] = self.statsList

  #-----------------------------------------------------------------------------
  def ProcessReport(self):

    # Get a list of all UEs that results are desired for
    #ueSet = set([])
    #for stats in self.statsList:
    #  ueIds = stats.GetUeIds()
    #  for ue in ueIds:
    #    ueSet.add(ue)
    ueList = sorted(self.ueIds)

    # For each UE in the UE list read the RDA file and save information
    for ueid in ueList:
      rdaFile = RdaFile()
      rdaFile.Open(rdafiles[ueid])
      self.processFile(rdaFile,ueid)

  #-----------------------------------------------------------------------------
  def processFile(self,file,ueid):
    colDict = None

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
        for lp in self.lpDict:
          logging.debug(lp)
          self.lpDict[lp].AddColumn(colDict['Time'])
        #for i in colDict:
        #  logging.debug(i)
        #continue

      self.parseData(row,colDict)
    
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
  def parseData(self,row,dict):
    pass
   
  #-----------------------------------------------------------------------------
  def UpdateUeIds(self,ueIds):
    super().UpdateUeIds(ueIds)
    for stats in self.statsList:
      stats.UpdateUeIds(ueIds)

  #-----------------------------------------------------------------------------
  def ReadData(self):
    pass

