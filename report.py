import logging

#-------------------------------------------------------------------------------
def ParseUeIds(ueStr):
  ueIds = set([])

  stxt = ueStr.split(':')
  stxt = stxt[1].lstrip('[')
  stxt = stxt.rstrip(']')
  if (stxt.upper() == 'ALL'):
    ueIds.add('ALL')
    return ueIds
  stxt = stxt.split(',')
  for i in stxt:
    logging.debug(ueStr)
    grp = i.split('-')
    if (len(grp) == 2):
      for j in range(int(grp[0]),int(grp[1])+1):
        ueIds.add(int(j))
    else:
      ueIds.add(int(i))
  return ueIds


#-------------------------------------------------------------------------------
class Report:
  ueIds  = set([])
  rtype  = None

  #-----------------------------------------------------------------------------
  def __init__(self,rtype):
    self.rtype = rtype

  #-----------------------------------------------------------------------------
  def AddReport(self,textList):
    pass

  #-----------------------------------------------------------------------------
  def ParseUeIds(self,text):
    self.ueList = parseUeIds(text)
  
  #-----------------------------------------------------------------------------
  def UpdateUeIds(self,ueIds):
    if ((len(self.ueIds) == 1) and ('ALL' in self.ueIds)):
      self.ueIds = ueIds
