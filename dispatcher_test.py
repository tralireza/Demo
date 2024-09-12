import dispatcher as m
import pytest
import os

@pytest.fixture()
def appConfig():
   appConfig = {
         'HOST': os.getenv('HOST', '127.0.0.1'),
         'USR': os.getenv('USR', ''),
         'PASSWD': os.getenv('PASSWD', ''),
         }  

   yield appConfig

def test_connToRemote(appConfig):
   host = appConfig['HOST']

   appConfig['HOST'] = '127.0.0.1'
   assert m.init(appConfig) == False

   appConfig['HOST'] = host
   assert m.init(appConfig) == True

def test_dispatch(appConfig):
   m.init(appConfig)

   assert m.dispatch('''
<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <target>
    <candidate/>
  </target>
  <config>
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-interface-cfg">
      <interface>
        <interface-name>Loopback9119</interface-name>
        <description>*** NC.py ***</description>
      </interface>
    </interfaces>
  </config>
</edit-config>
''') == True

