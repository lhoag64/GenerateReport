import logging

#-------------------------------------------------------------------------------
class Service:
  def __init__(self,text):
    self.name = text
    stxt = text.split('_')
    self.dir   = stxt[0]
    self.proto = stxt[1]
    if (stxt[3][0:1] == 'L'):
      self.lp = stxt[3]
      self.cs = 'CLIENT'
    elif (stxt[3][0:1] == 'S'):
      self.lp = stxt[4]
      self.cs = 'SERVER'
    self.lpIdx = int(self.lp[2:3])
    #logging.debug('-->|' + self.lp + '|' + str(self.lpIdx) + '|' + self.dir + '|' + self.proto + '|' + self.cs + '|' + self.name.ljust(18) + '|')

#-------------------------------------------------------------------------------
class Services:
  def __init__(self,text):
    pass

#-------------------------------------------------------------------------------
class RdaStats:
  services = None

  def __init__(self):
    pass

  #-------------------------------------------------------------------------------
  def ProcessStats(self,dataDict):
    services = {}
    #
    # Sort the informtion by LP,dir,proto
    #
    for i in dataDict:
      service = Service(i)
      lp = service.lp
      if lp not in services:
        services[lp] = {}
      dir = service.dir
      if dir not in services[lp]:
        services[lp][dir] = {}
      proto = service.proto
      if proto not in services[lp][dir]:
        services[lp][dir][proto] = {}
      cs = service.cs
      if cs not in services[lp][dir][proto]:
        services[lp][dir][proto][cs] = {}
      name = service.name
      if name not in services[lp][dir][proto][cs]:
        #logging.debug('|' + lp + '|' + '|' + dir + '|' + proto + '|' + cs + '|' + name.ljust(18) + '|')
        services[lp][dir][proto][cs][name] = []
        sortList = sorted(dataDict[i])
        for j in sortList:
          services[lp][dir][proto][cs][name].append(dataDict[i][j])

    self.services = services

    lpSet    = set([])
    dirSet   = set([])
    protoSet = set([])
    csSet    = set([])
    nameSet  = set([])

    for lp in services:
      lpSet.add(lp)
      for dir in services[lp]:
        dirSet.add(dir)
        for proto in services[lp][dir]:
          protoSet.add(proto)
          for cs in services[lp][dir][proto]:
            csSet.add(cs)
            for name in services[lp][dir][proto][cs]:
              nameSet.add(name)
              logging.debug('|' + lp + '|' + dir + '|' + proto + '|' + cs + '|' + name.ljust(18) + '|')

              service = services[lp][dir][proto][cs][name]

              for col in service:
                for row in col.rows:
                  if (len(col.service) > 0):
                    try:
                      val = int(row)
                    except ValueError:
                      val = 0
                    col.sum += val
                  else:
                    # Must be time
                    pass
                  #logging.debug(row)


    self.lpList    = sorted(lpSet)
    self.dirList   = sorted(dirSet)
    self.protoList = sorted(protoSet)
    self.csList    = sorted(csSet)
    self.nameList  = sorted(nameSet)
'''
    for lp in sortLp:
      sortDir = sorted(services[lp])
      for dir in sortDir:
        sortProto = sorted(services[lp][dir])
        for proto in services[lp][dir]:
          sortCs = sorted(services[lp][dir][proto])
          for cs in sortCs:
            sortName = sorted(services[lp][dir][proto][cs])
            for name in sortName:
              logging.debug(ws.title + '|' + str(wsCol).rjust(3) + '|' + lp + '|' + dir + '|' + proto + '|' + cs + '|' + name.ljust(18) + '|')
              service = services[lp][dir][proto][cs][name]

  sortLp = sorted(services)
  for lp in sortLp:
    CreateSheet(wb,lp)
    ws = GetSheetByName(wb,lp)
    for i in range(1,25):
      SetColumnWidth(ws,i,12)

  for lp in sortLp:
    ws = GetSheetByName(wb,lp)
    wsCol  = 1
    sortDir = sorted(services[lp])
    for dir in sortDir:
      sortProto = sorted(services[lp][dir])
      for proto in services[lp][dir]:
        sortCs = sorted(services[lp][dir][proto])
        for cs in sortCs:
          sortName = sorted(services[lp][dir][proto][cs])
          wsRow  = 1
          for name in sortName:
            logging.debug(ws.title + '|' + str(wsCol).rjust(3) + '|' + lp + '|' + dir + '|' + proto + '|' + cs + '|' + name.ljust(18) + '|')
            service = services[lp][dir][proto][cs][name]

            SetColumnWidth(ws,wsCol,20)
            SetCell(ws,wsRow,wsCol,name,{'vAlign':'C','hAlign':'L'})
            wsRow += 1

            for col in service:
              wsRow  = 2
              SetCell(ws,wsRow,wsCol,col.desc,{'vAlign':'C','hAlign':'C','wrap':'1'})
              wsRow += 1
              #logging.debug(str(wsCol).rjust(3) + ' ' + col.desc.ljust(40))
              for row in col.rows:
                try:
                  val = int(row)
                except ValueError:
                  val = row
                SetCell(ws,wsRow,wsCol,val,{'vAlign':'C','hAlign':'C'})
                wsRow += 1
              wsCol += 1
            wsCol += 2
'''