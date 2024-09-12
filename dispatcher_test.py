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

