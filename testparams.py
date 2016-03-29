import logging
from   report    import Report
from   report    import ParseUeIds
from   rdareport import RdaReport

#-------------------------------------------------------------------------------
class TestParams:
  def __init__(self):
    self.name       = None
    self.rdaReport  = None
    self.esmReport  = None
    self.nasReport  = None
    self.rrcReport  = None
    self.ueIds      = set([])
    self.reports    = []

  #-----------------------------------------------------------------------------
  def SetName(self,name):
    self.name = name 

  #-----------------------------------------------------------------------------
  def AddReport(self,textList):
    stxt = textList[0].split(':')
    self.rtype = stxt[1]

    if (self.rtype == 'RDA'):
      if (self.rdaReport == None):
        report = RdaReport(self.rtype)
        self.rdaReport = report
      self.rdaReport.AddReport(textList[1:])
    if (self.rtype == 'ESM'):
      if (self.esmReport == None):
        report = Report(self.rtype)
        self.esmReport = report
      self.esmReport.AddReport(textList[1:])
    if (self.rtype == 'NAS'):
      if (self.nasReport == None):
        report = Report(self.rtype)
        self.nasReport = report
      self.nasReport.AddReport(textList[1:])
    if (self.rtype == 'RRC'):
      if (self.rrcReport == None):
        report = Report(self.rtype)
        self.rrcReport = report
      self.rrcReport.AddReport(textList[1:])

  #-----------------------------------------------------------------------------
  def ProcessReports(self):
    self.rdaReport.ProcessReport()
  
    #-----------------------------------------------------------------------------
  def ParseUeIds(self,ueStr):
    self.ueIds = ParseUeIds(ueStr)

  #-----------------------------------------------------------------------------
  def Update(self):

    if (self.rdaReport != None): self.reports.append(self.rdaReport)
    if (self.esmReport != None): self.reports.append(self.esmReport)
    if (self.nasReport != None): self.reports.append(self.nasReport)
    if (self.rrcReport != None): self.reports.append(self.rrcReport)

    for report in self.reports:
      report.UpdateUeIds(self.ueIds)