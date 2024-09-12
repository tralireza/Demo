import logging
import lxml.etree as et
from ncclient import manager
from ncclient.operations import RPCError

ncMgr, resetMgr = None, None
logger = logging.getLogger(__name__)

def init(appConfig):
   """
   initialise ncMgr adding a clousre to context to re-establish connection,
   if need be...
   return True if connection to remote host is successful,
   otherwise False to fast-fail
   """
   global resetMgr

   def resetMgr():
      """
      closure on appConfig to reset/retry ncMgr in case of connection loss
      """
      global ncMgr

      ncMgr = None
      try:
         ncMgr = manager.connect(port=830, timeout=90,
                                 host=appConfig['HOST'],
                                 username=appConfig['USR'], password=appConfig['PASSWD'],
                                 hostkey_verify=False, allow_agent=False,
                                 device_params={'name': 'iosxr'})
      except Exception as e:
         logger.error(e)

      return ncMgr is not None
      
   return resetMgr()

def dispatch(rpcXml):
   """
   send the rpc payload (sync), reset the connection manager (ncMgr) on Exception 
   """
   try:
      rspXml = ncMgr.dispatch(et.fromstring(rpcXml)).xml
   except RPCError as e:
      rspXml = e.xml
   except Exception as e:
      logger.info('retrying to connect to remote host ...')
      resetMgr()
      raise Exception()

   if et.iselement(rspXml):
      rspXml = et.tostring(rspXml, pretty_print=True).decode()

   try:
      rspOutput = et.tostring(et.fromstring(data.encode('utf-8')),
                              pretty_print=True).decode()
   except Exception:
      pass

   print(rspOutput)

