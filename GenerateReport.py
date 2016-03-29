import logging
from testparams      import TestParams
from cmdfile         import CmdFile 
from rdareport       import RdaReport
#from rdafile         import RdaFile
#from rdastats        import RdaStats


#-------------------------------------------------------------------------------
# Start of program
#-------------------------------------------------------------------------------
if (__name__ == '__main__'):
  logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s-%(levelname)s-%(message)s')
  logging.debug('Start of program')

  cmdfile = r'test-data\test-case-1\160323_151349_Command_Log000.txt'

  params   = None
  cmdFile  = CmdFile('Test-Case-X')

  params = cmdFile.Read(cmdfile)
  params.Update()

  params.ProcessReports()

  logging.debug('End of program')
