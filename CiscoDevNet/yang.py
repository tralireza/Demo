"""
Using a Cisco DevNet environment: IOS XR Programmabilty AlwaysOn
Cisco IOS XR 7.3.2
"""

import os
import xml.etree.ElementTree as ET
from ncclient import manager

host = os.getenv('HOST', 'sandbox-iosxr-1.cisco.com')
usr =  os.getenv('USR', 'admin')
passwd = os.getenv('PASSWD', '')

print('Connecting to "%s" with user: "%s", password: "%s" ...' % (host, usr, passwd))

ncMgr = manager.connect(port=830, host=host, username=usr, password=passwd, 
                        device_params={'name': 'csr'},
                        hostkey_verify=False, allow_agent=False)

print('Connected, downloading all "yang" modules ...')

caps = []
for t in ncMgr.server_capabilities:
   if '/ns/yang/' in t:
      yang = t[t.index('/ns/yang/')+9:]
      yang = yang[:yang.index('?')]

      print(" -> ", yang)
      """
      schema = ncMgr.get_schema(yang)

      root = ET.fromstring(schema.xml)
      with open('cisco_yang_modules/'+yang+'.yang', 'w') as f:
         f.write(list(root)[0].text)
      """
   else:
      caps.append(t)

print('--')
print('Other capabilities (Not-Downloaded) #%i:' % len(caps))
for t in caps:
   print(' *-> ', t)
